# Notes

## Core Concept

Image Updater is a separate controller that runs alongside ArgoCD. It continuously monitors container registries for new image tags and automatically updates your applications when changes are detected.

## How It Works

1. Registry Polling
- Runs on a schedule (every 2 minutes by default)
- Queries your ECR repository for available image tags
- Compares against what's currently deployed

2. Tag Filtering & Strategy
- Uses configurable filters to determine which tags to consider
- Applies update strategies (latest, semver, digest-based, etc.)
- In your case: only watch for changes to the `production` tag

3. Application Update
- When a new `production` tag is detected, it updates the ArgoCD Application
- Modifies the image reference in the Application spec
- ArgoCD then syncs the change to your cluster

## Your Workflow Integration

Step 1: Install Image Updater
```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj-labs/argocd-image-updater/stable/manifests/install.yaml
```

Step 2: Configure Your ArgoCD Application
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: gitops-praq-prod
  namespace: argocd
  annotations:
    # Tell Image Updater to watch this image
    argocd-image-updater.argoproj.io/image-list: app=123456789.dkr.ecr.us-west-2.amazonaws.com/gitops-praq
    
    # Only consider the 'production' tag
    argocd-image-updater.argoproj.io/app.image-tag-filter: ^production$
    
    # Update strategy: replace with latest matching tag
    argocd-image-updater.argoproj.io/app.update-strategy: latest
    
    # Optional: write back to git or just update in-cluster
    argocd-image-updater.argoproj.io/write-back-method: application
spec:
  source:
    repoURL: https://github.com/your-username/gitops-praq
    path: k8s/production
    targetRevision: HEAD
  destination:
    server: https://kubernetes.default.svc
    namespace: production
```

Step 3: Your Deployment Manifest
```yaml
# k8s/production/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gitops-praq
spec:
  template:
    spec:
      containers:
      - name: app
        # Image Updater will automatically update this reference
        image: 123456789.dkr.ecr.us-west-2.amazonaws.com/gitops-praq:production
```

## Complete Flow

1. Your CI/CD → Pushes new `production` tag to ECR
2. Image Updater → Detects the tag change (within 2 minutes)
3. Image Updater → Updates the ArgoCD Application spec
4. ArgoCD → Syncs the new image to Kubernetes
5. Kubernetes → Rolls out the deployment

## Key Benefits

No Git Commits - Updates happen in-cluster or via ArgoCD Application CRDs
Fast Detection - 2-minute polling cycle (configurable)
Tag Filtering - Only watches tags you care about
Multiple Strategies - Latest, semver, digest-based updates
ECR Support - Works great with AWS ECR (handles authentication)

## Configuration Options

```yaml
annotations:
  # Watch multiple images
  argocd-image-updater.argoproj.io/image-list: app=repo1:tag1,sidecar=repo2:tag2
  
  # Semver filtering (for versioned releases)
  argocd-image-updater.argoproj.io/app.image-tag-filter: ^v\d+\.\d+\.\d+$
  
  # Custom polling interval
  argocd-image-updater.argoproj.io/app.image-poll-interval: 5m
  
  # Write back to git (if you want commit history)
  argocd-image-updater.argoproj.io/write-back-method: git
```
