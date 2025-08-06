import pandas as pd

def recommend_banks(preferences, bank_data_path="data/banks.csv"):
    df = pd.read_csv(bank_data_path)
    if preferences["student_friendly"]:
        df = df[df["Student Friendly"] == "Yes"]
    df = df[df["Monthly Fee"] <= preferences["max_fee"]]
    df = df[df["APY"] >= preferences["min_apy"]]
    df["score"] = df["APY"] * 1.5 + df["Mobile Rating"] - df["Monthly Fee"] * 0.2
    df = df.sort_values("score", ascending=False)
    return df
