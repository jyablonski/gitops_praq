import polars as pl


def generate_fake_df():
    df = pl.DataFrame(
        {"id": [1, 2, 3], "name": ["Alice", "Bob", "Charlie"], "age": [25, 30, 35]}
    )
    return df


if __name__ == "__main__":
    df = generate_fake_df()
    print(df)
    print("Exiting ...")
