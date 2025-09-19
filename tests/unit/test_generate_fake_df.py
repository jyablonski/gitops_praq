from src.main import generate_fake_df


def test_generate_fake_df():
    df = generate_fake_df()
    assert df.shape == (3, 3)
    assert list(df.columns) == ["id", "name", "age"]
    assert df["id"].to_list() == [1, 2, 3]
    assert df["name"].to_list() == ["Alice", "Bob", "Charlie"]
    assert df["age"].to_list() == [25, 30, 35]
