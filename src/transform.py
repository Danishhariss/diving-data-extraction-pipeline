import pandas as pd


def build_dataframe(records):
    df = pd.DataFrame(records)

    if df.empty:
        raise ValueError("No records were extracted. Please check the scraper logic.")

    expected_columns = [
        "athlete",
        "country",
        "rank",
        "age",
        "final_points",
        "points_behind",
        "dive_round",
        "dive_code",
        "difficulty",
        "judge_1",
        "judge_2",
        "judge_3",
        "judge_4",
        "judge_5",
        "judge_6",
        "judge_7",
        "dive_score",
        "cumulative_score",
    ]

    df = df[expected_columns]

    numeric_columns = [
        "rank",
        "age",
        "final_points",
        "points_behind",
        "dive_round",
        "difficulty",
        "judge_1",
        "judge_2",
        "judge_3",
        "judge_4",
        "judge_5",
        "judge_6",
        "judge_7",
        "dive_score",
        "cumulative_score",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    return df


def export_outputs(df, csv_path, excel_path):
    df.to_csv(csv_path, index=False)
    df.to_excel(excel_path, index=False)

    print(f"CSV exported to: {csv_path}")
    print(f"Excel exported to: {excel_path}")