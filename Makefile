.PHONY: test
test:
	@docker compose -f docker/docker-compose-test.yaml down
	@docker compose -f docker/docker-compose-test.yaml up --exit-code-from test_runner --build --abort-on-container-exit

.PHONY: build
build:
	docker build -f docker/Dockerfile -t ingestion_script_prod .