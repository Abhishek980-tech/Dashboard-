# extended_eda_static_interactive.py
# Full EDA with Static (PNG), Interactive (HTML) Charts + Excel & Text Summary

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import openpyxl


def find_column(df, possible_names):
    """Helper to detect column name variations"""
    for name in possible_names:
        if name in df.columns:
            return name
    return None


def main():
    file_path = "wellbeing_survey_res_Cleaned.csv"
    df = pd.read_csv(file_path, encoding="utf-8")

    print("Available columns:", df.columns.tolist())
    summary_text = []

    with pd.ExcelWriter("EDA_Summary.xlsx", engine="openpyxl") as writer:

        # ---------------------------
        # Age Distribution
        # ---------------------------
        age_col = find_column(df, ["Age_Group", "Age", "Age (years)"])
        if age_col:
            age_counts = df[age_col].value_counts()
            age_counts.to_excel(writer, sheet_name="Age_Distribution")
            summary_text.append(f"Most common age group: {age_counts.idxmax()} ({age_counts.max()} respondents)")

            plt.figure(figsize=(6, 4))
            age_counts.plot(kind="bar", color="skyblue")
            plt.title("Age Distribution")
            plt.savefig("eda_age_distribution.png")
            plt.close()

            fig_age = px.bar(age_counts.reset_index(),
                             x=age_counts.index,
                             y=age_counts.values,
                             labels={"x": "Age", "y": "Count"},
                             title="Age Distribution")
            fig_age.write_html("eda_age_distribution.html")

        # ---------------------------
        # Gender Distribution
        # ---------------------------
        gender_col = find_column(df, ["Gender", "gender"])
        if gender_col:
            gender_counts = df[gender_col].value_counts()
            gender_counts.to_excel(writer, sheet_name="Gender_Distribution")
            summary_text.append(f"Gender split: {gender_counts.to_dict()}")

            plt.figure(figsize=(5, 4))
            gender_counts.plot(kind="pie", autopct="%1.1f%%")
            plt.title("Gender Distribution")
            plt.ylabel("")
            plt.savefig("eda_gender_distribution.png")
            plt.close()

            fig_gender = px.pie(df, names=gender_col, title="Gender Distribution")
            fig_gender.write_html("eda_gender_distribution.html")

        # ---------------------------
        # Role Distribution
        # ---------------------------
        role_col = find_column(df, ["Role", "Primary role"])
        if role_col:
            role_counts = df[role_col].value_counts()
            role_counts.to_excel(writer, sheet_name="Role_Distribution")
            summary_text.append(f"Most common role: {role_counts.idxmax()} ({role_counts.max()} respondents)")

            plt.figure(figsize=(7, 5))
            role_counts.plot(kind="bar", color="orange")
            plt.title("Role Distribution")
            plt.savefig("eda_role_distribution.png")
            plt.close()

            fig_role = px.bar(role_counts.reset_index(),
                              x=role_counts.index,
                              y=role_counts.values,
                              labels={"x": "Role", "y": "Count"},
                              title="Role Distribution")
            fig_role.write_html("eda_role_distribution.html")

        # ---------------------------
        # Country Distribution
        # ---------------------------
        country_col = find_column(df, ["Country", "Country/Region"])
        if country_col:
            country_counts = df[country_col].value_counts()
            country_counts.to_excel(writer, sheet_name="Country_Distribution")

            plt.figure(figsize=(8, 5))
            country_counts.head(10).plot(kind="bar", color="teal")
            plt.title("Top 10 Countries")
            plt.savefig("eda_country_distribution.png")
            plt.close()

            fig_country = px.bar(country_counts.head(10).reset_index(),
                                 x=country_counts.head(10).index,
                                 y=country_counts.head(10).values,
                                 labels={"x": "Country", "y": "Count"},
                                 title="Top 10 Countries")
            fig_country.write_html("eda_country_distribution.html")

        # ---------------------------
        # Stress Analysis
        # ---------------------------
        stress_col = find_column(df, ["Stress_Category", "Stress Level", "Stress"])
        if stress_col:
            stress_counts = df[stress_col].value_counts()
            stress_counts.to_excel(writer, sheet_name="Stress_Distribution")
            summary_text.append(f"Highest stress group: {stress_counts.idxmax()} ({stress_counts.max()} respondents)")

            plt.figure(figsize=(5, 4))
            stress_counts.plot(kind="bar", color="salmon")
            plt.title("Stress Level Distribution")
            plt.savefig("eda_stress_distribution.png")
            plt.close()

            fig_stress = px.bar(stress_counts.reset_index(),
                                x=stress_counts.index,
                                y=stress_counts.values,
                                labels={"x": "Stress", "y": "Count"},
                                title="Stress Level Distribution")
            fig_stress.write_html("eda_stress_distribution.html")

            if role_col:
                stress_role = pd.crosstab(df[role_col], df[stress_col])
                stress_role.to_excel(writer, sheet_name="Stress_By_Role")

                stress_role.plot(kind="bar", figsize=(7, 5))
                plt.title("Stress Levels by Role")
                plt.savefig("eda_stress_by_role.png")
                plt.close()

                fig_stress_role = px.bar(stress_role, barmode="group", title="Stress Levels by Role")
                fig_stress_role.write_html("eda_stress_by_role.html")

        # ---------------------------
        # AI Tool Usage
        # ---------------------------
        ai_col = find_column(df, ["Used_AI_Tool", "AI Tool Usage", "AI_Usage"])
        if ai_col:
            ai_counts = df[ai_col].value_counts()
            ai_counts.to_excel(writer, sheet_name="AI_Tool_Usage")
            summary_text.append(f"AI tool usage: {ai_counts.to_dict()}")

            plt.figure(figsize=(5, 4))
            ai_counts.plot(kind="pie", autopct="%1.1f%%")
            plt.title("AI Tool Usage (Yes/No)")
            plt.ylabel("")
            plt.savefig("eda_ai_tool_usage.png")
            plt.close()

            fig_ai = px.pie(df, names=ai_col, title="AI Tool Usage (Yes/No)")
            fig_ai.write_html("eda_ai_tool_usage.html")

        # ---------------------------
        # App Usage
        # ---------------------------
        apps_col = find_column(df, ["Wellness_Apps", "Which wellness/mental health apps have you used in the last 6 months? (select all that apply)"])
        if apps_col:
            apps_exploded = df[apps_col].astype(str).str.split(",").explode()
            app_counts = apps_exploded.value_counts()
            app_counts.to_excel(writer, sheet_name="App_Usage")
            summary_text.append(f"Most popular app: {app_counts.idxmax()} ({app_counts.max()} users)")

            plt.figure(figsize=(7, 5))
            app_counts.plot(kind="bar", color="blue")
            plt.title("Wellness App Usage")
            plt.savefig("eda_app_usage.png")
            plt.close()

            fig_apps = px.bar(app_counts.reset_index(),
                              x=app_counts.index,
                              y=app_counts.values,
                              labels={"x": "App", "y": "Count"},
                              title="Wellness App Usage")
            fig_apps.write_html("eda_app_usage.html")

        # ---------------------------
        # Concerns
        # ---------------------------
        concerns_col = find_column(df, ["Concerns_List", "Concerns", "Mental Health Concerns"])
        if concerns_col:
            concerns_exploded = df[concerns_col].astype(str).str.split(",").explode()
            top_concerns = concerns_exploded.value_counts()
            top_concerns.to_excel(writer, sheet_name="Concerns")
            summary_text.append(f"Top concern: {top_concerns.idxmax()} ({top_concerns.max()} respondents)")

            plt.figure(figsize=(7, 5))
            top_concerns.plot(kind="bar", color="purple")
            plt.title("Top Reported Mental Health Concerns")
            plt.savefig("eda_concerns.png")
            plt.close()

            fig_concerns = px.bar(top_concerns.reset_index(),
                                  x=top_concerns.index,
                                  y=top_concerns.values,
                                  labels={"x": "Concern", "y": "Count"},
                                  title="Top Reported Mental Health Concerns")
            fig_concerns.write_html("eda_concerns.html")

        # ---------------------------
        # Desired Features
        # ---------------------------
        features_col = find_column(df, ["Desired_Features", "Features", "Wanted Features"])
        if features_col:
            features_exploded = df[features_col].astype(str).str.split(",").explode()
            top_features = features_exploded.value_counts()
            top_features.to_excel(writer, sheet_name="Desired_Features")
            summary_text.append(f"Most wanted feature: {top_features.idxmax()} ({top_features.max()} requests)")

            plt.figure(figsize=(7, 5))
            top_features.plot(kind="barh", color="green")
            plt.title("Most Wanted Features")
            plt.savefig("eda_features.png")
            plt.close()

            fig_features = px.bar(top_features.reset_index(),
                                  x=top_features.index,
                                  y=top_features.values,
                                  labels={"x": "Feature", "y": "Count"},
                                  title="Most Wanted Features")
            fig_features.write_html("eda_features.html")

        # ---------------------------
        # Privacy & Preferences
        # ---------------------------
        privacy_col = find_column(df, ["Consent", "I am 18+ and I consent to anonymous data collection for academic purposes only."])
        if privacy_col:
            privacy_counts = df[privacy_col].value_counts()
            privacy_counts.to_excel(writer, sheet_name="Consent")
            summary_text.append(f"Consent responses: {privacy_counts.to_dict()}")

            plt.figure(figsize=(5, 4))
            privacy_counts.plot(kind="bar", color="gray")
            plt.title("Consent Responses")
            plt.savefig("eda_consent.png")
            plt.close()

            fig_privacy = px.bar(privacy_counts.reset_index(),
                                 x=privacy_counts.index,
                                 y=privacy_counts.values,
                                 labels={"x": "Response", "y": "Count"},
                                 title="Consent Responses")
            fig_privacy.write_html("eda_consent.html")

        # ---------------------------
        # Correlation Heatmap
        # ---------------------------
        numeric_cols = df.select_dtypes(include=["int64", "float64"])
        if not numeric_cols.empty:
            corr = numeric_cols.corr()
            corr.to_excel(writer, sheet_name="Correlation")

            plt.figure(figsize=(6, 5))
            sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
            plt.title("Correlation Heatmap (Numeric Features)")
            plt.savefig("eda_correlation.png")
            plt.close()

            fig_corr = px.imshow(corr.values,
                                 labels=dict(x="Features", y="Features", color="Correlation"),
                                 x=corr.columns.tolist(),
                                 y=corr.index.tolist(),
                                 text_auto=True,
                                 color_continuous_scale="RdBu_r",
                                 title="Correlation Heatmap (Numeric Features)")
            fig_corr.write_html("eda_correlation.html")

    # ---------------------------
    # Save Text Summary
    # ---------------------------
    with open("EDA_Text_Summary.txt", "w") as f:
        for line in summary_text:
            f.write(line + "\n")

    print("\n✅ EDA complete.")
    print("📊 Static charts saved as PNG")
    print("🖱️ Interactive charts saved as HTML")
    print("📑 Summary tables saved to EDA_Summary.xlsx")
    print("📝 Insights saved to EDA_Text_Summary.txt")


if __name__ == "__main__":
    main()
