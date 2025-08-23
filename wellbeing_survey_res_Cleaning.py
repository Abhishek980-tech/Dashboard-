# week1_data_cleaning.py
# Week 1: Data Cleaning & Setup for Wellbeing Survey Dataset

import pandas as pd
import re

def main():
    # ---------------------------
    # Step 1: Load & Inspect Data
    # ---------------------------
    file_path = "wellbeing_survey_res.csv"   # ensure this CSV is in the same folder
    df = pd.read_csv(file_path, encoding="utf-8")

    print("="*60)
    print("Initial Shape:", df.shape)
    print("Columns:", df.columns.tolist())
    print("="*60)

    # ---------------------------
    # Step 2: Handle Missing Values
    # ---------------------------
    print("\nMissing values before cleaning:\n", df.isnull().sum())

    threshold = 0.4 * len(df)  # drop col if >40% missing
    df = df.dropna(axis=1, thresh=len(df) - threshold)

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())

    categorical_cols = df.select_dtypes(include=["object"]).columns
    for col in categorical_cols:
        df[col] = df[col].fillna(df[col].mode()[0])

    print("\nMissing values after cleaning:\n", df.isnull().sum())

    # ---------------------------
    # Step 3: Standardize Columns
    # ---------------------------
    # Convert Age to numeric
    if "Age (years)" in df.columns:
        df["Age (years)"] = pd.to_numeric(df["Age (years)"], errors="coerce")

    # Convert Sleep hours like "9 hours" -> 9
    if "Average sleep hours per night (past 2 weeks)" in df.columns:
        df["Average sleep hours per night (past 2 weeks)"] = (
            df["Average sleep hours per night (past 2 weeks)"]
            .astype(str)
            .str.extract(r"(\d+)")  # extract digits
            .astype(float)
        )

    # Convert Deadlines/Exams to numeric
    if "How many deadlines/exams in the next 7 days?" in df.columns:
        df["How many deadlines/exams in the next 7 days?"] = pd.to_numeric(
            df["How many deadlines/exams in the next 7 days?"], errors="coerce"
        ).fillna(0)

    # Convert Timestamp
    if "Timestamp" in df.columns:
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")

    # ---------------------------
    # Step 4: Clean Multi-Choice Responses
    # ---------------------------
    multi_choice_cols = [
        "Which wellness/mental health apps have you used in the last 6 months? (select all that apply)",
        "Which emotions did you often experience in the last week? (select all that apply)"
    ]

    for col in multi_choice_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).apply(
                lambda x: [i.strip().title() for i in re.split(r",|;", x) if i.strip() != ""]
            )

    # ---------------------------
    # Step 5: Encode Likert Scale Responses
    # ---------------------------
    likert_map = {
        "Strongly disagree": 1,
        "Disagree": 2,
        "Neutral": 3,
        "Agree": 4,
        "Strongly agree": 5
    }

    likert_cols = [
        "I am concerned about privacy of my journals.",
        "I prefer on-device processing even if features are limited.",
        "I am okay with personalized nudges if they help my wellbeing.",
        "I am willing to share anonymized analytics for research."
    ]

    for col in likert_cols:
        if col in df.columns:
            df[col] = df[col].map(likert_map).fillna(df[col])

    # ---------------------------
    # Step 6: Save Cleaned Dataset
    # ---------------------------
    output_file = "wellbeing_survey_res_Cleaned.csv"
    df.to_csv(output_file, index=False, encoding="utf-8")

    print("\n✅ Data cleaning complete. Saved as:", output_file)
    print("Final Shape:", df.shape)


if __name__ == "__main__":
    main()
