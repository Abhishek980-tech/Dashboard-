# moodra_dashboard.py
# Moodra Interactive Dashboard Website (Streamlit)

import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# -------------------------
# Load Data
# -------------------------
df = pd.read_csv("wellbeing_survey_res_Cleaned.csv")

# -------------------------
# App Branding
# -------------------------
st.set_page_config(page_title="Moodra Dashboard", layout="wide")
st.title(" Moodra - Your mood, your mantra — tracked, protected, and supported.")
st.markdown("Gain insights from survey data on stress, AI usage, and mental health trends.")

# -------------------------
# Filters
# -------------------------
with st.sidebar:
    st.markdown("### 🎭 Moodra")
    st.markdown("---")
    st.header("🔍 Filters")

    age_filter = st.multiselect(
        "Age Group",
        options=df["Age (years)"].dropna().unique(),
        default=df["Age (years)"].dropna().unique()
    )

    gender_filter = st.multiselect(
        "Gender",
        options=df["Gender (optional)"].dropna().unique(),
        default=df["Gender (optional)"].dropna().unique()
    )

    role_filter = st.multiselect(
        "Role",
        options=df["Primary role"].dropna().unique(),
        default=df["Primary role"].dropna().unique()
    )

    # Stress column detection
    stress_col = next((col for col in df.columns if "stress" in col.lower()), None)
    stress_filter = st.multiselect(
        "Stress Level",
        options=df[stress_col].dropna().unique() if stress_col else [],
        default=df[stress_col].dropna().unique() if stress_col else []
    ) if stress_col else None

    # Wellness Apps multi-select filter (if present)
    apps_col = next((col for col in df.columns if "wellness apps" in col.lower()), None)
    apps_filter = st.multiselect(
        "Wellness Apps",
        options=df[apps_col].dropna().unique() if apps_col else [],
        default=df[apps_col].dropna().unique() if apps_col else []
    ) if apps_col else None

# -------------------------
# Apply Filters
# -------------------------
df_filtered = df[
    df["Age (years)"].isin(age_filter) &
    df["Gender (optional)"].isin(gender_filter) &
    df["Primary role"].isin(role_filter)
]

if stress_filter and stress_col:
    df_filtered = df_filtered[df_filtered[stress_col].isin(stress_filter)]

if apps_filter and apps_col:
    df_filtered = df_filtered[df_filtered[apps_col].isin(apps_filter)]

# -------------------------
# KPI Summary Cards
# -------------------------
st.subheader("📊 Summary Insights")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Responses", len(df_filtered))
with col2:
    st.metric("Unique Roles", df_filtered["Primary role"].nunique())
with col3:
    if "Overall mood today" in df.columns:
        mood_counts = df_filtered["Overall mood today"].value_counts()
        st.metric("Most Common Mood", f"{mood_counts.idxmax() if len(mood_counts) > 0 else 'N/A'}")

st.markdown("---")

# -------------------------
# Distribution Charts
# -------------------------
col1, col2 = st.columns(2)
with col1:
    if "Age (years)" in df.columns:
        age_counts = df_filtered["Age (years)"].value_counts().reset_index()
        age_counts.columns = ["Age", "Count"]
        fig_age = px.bar(age_counts, x="Age", y="Count", title="Age Distribution")
        st.plotly_chart(fig_age, use_container_width=True)

with col2:
    if "Gender (optional)" in df.columns:
        fig_gender = px.pie(df_filtered, names="Gender (optional)", title="Gender Distribution")
        st.plotly_chart(fig_gender, use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    if "Primary role" in df.columns:
        role_counts = df_filtered["Primary role"].value_counts().reset_index()
        role_counts.columns = ["Role", "Count"]
        fig_role = px.bar(role_counts, x="Role", y="Count", title="Role Distribution")
        st.plotly_chart(fig_role, use_container_width=True)

with col4:
    if "Overall mood today" in df.columns:
        mood_counts = df_filtered["Overall mood today"].value_counts().reset_index()
        mood_counts.columns = ["Mood", "Count"]
        fig_mood = px.bar(mood_counts, x="Mood", y="Count", title="Mood Distribution")
        st.plotly_chart(fig_mood, use_container_width=True)

# -------------------------
# Stress Level Analysis
# -------------------------
if stress_col:
    st.subheader("🧠 Stress Level Analysis")

    
    stress_colors = {level: px.colors.qualitative.Plotly[i % 10] for i, level in enumerate(df_filtered[stress_col].dropna().unique())}

    # Basic distribution
    stress_counts = df_filtered[stress_col].value_counts().reset_index()
    stress_counts.columns = ["Stress Level", "Count"]
    fig_stress = px.bar(stress_counts, x="Stress Level", y="Count", title="Stress Level Distribution", color="Stress Level", color_discrete_map=stress_colors)
    st.plotly_chart(fig_stress, use_container_width=True)

    # Gender
    if "Gender (optional)" in df.columns:
        fig_stress_gender = px.histogram(df_filtered, x=stress_col, color="Gender (optional)", barmode="group", title="Stress Level by Gender")
        st.plotly_chart(fig_stress_gender, use_container_width=True)

    # Role
    if "Primary role" in df.columns:
        fig_stress_role = px.histogram(df_filtered, x=stress_col, color="Primary role", barmode="group", title="Stress Level by Role")
        st.plotly_chart(fig_stress_role, use_container_width=True)

    # Age
    if "Age (years)" in df.columns:
        fig_stress_age = px.histogram(df_filtered, x=stress_col, color="Age (years)", barmode="group", title="Stress Level by Age Group")
        st.plotly_chart(fig_stress_age, use_container_width=True)


# Journaling & Sleep

col5, col6 = st.columns(2)
with col5:
    if "How often do you journal?" in df.columns:
        fig_journal = px.pie(df_filtered, names="How often do you journal?", title="Journaling Frequency")
        st.plotly_chart(fig_journal, use_container_width=True)

with col6:
    if "Average sleep hours per night (past 2 weeks)" in df.columns:
        sleep_counts = df_filtered["Average sleep hours per night (past 2 weeks)"].value_counts().reset_index()
        sleep_counts.columns = ["Sleep Duration", "Count"]
        fig_sleep = px.bar(sleep_counts, x="Sleep Duration", y="Count", title="Sleep Duration Distribution")
        st.plotly_chart(fig_sleep, use_container_width=True)

# Privacy Concerns
if "I am concerned about privacy of my journals." in df.columns:
    privacy_counts = df_filtered["I am concerned about privacy of my journals."].value_counts().reset_index()
    privacy_counts.columns = ["Response", "Count"]
    fig_privacy = px.bar(privacy_counts, x="Response", y="Count", title="Privacy Concerns")
    st.plotly_chart(fig_privacy, use_container_width=True)

# Download
st.markdown("---")
st.subheader("⬇️ Download Insights")
csv_data = df_filtered.to_csv(index=False).encode("utf-8")
st.download_button("Download Filtered Data (CSV)", data=csv_data, file_name="moodra_filtered_data.csv", mime="text/csv")

excel_buffer = BytesIO()
df_filtered.to_excel(excel_buffer, index=False, engine="openpyxl")
st.download_button("Download Filtered Data (Excel)", data=excel_buffer, file_name="moodra_filtered_data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


# footer
st.markdown("---")
st.markdown( """
    <style>
        .footer-icons img {
            filter: grayscale(100%);
            transition: all 0.3s ease;
        }
        .footer-icons img:hover {
            filter: grayscale(0%);
            transform: scale(1.2);
        }
    </style>
    <div style='text-align: center; font-size:12px; color: gray;'>
        <strong>Moodra</strong> • Empowering wellbeing through insights<br>
        © 2025 Moodra Inc. All rights reserved.<br>
        Version: 1.0.0<br>
        Developed by: Abhishek Bahuguna<br>
        Contact: <a href='mailto:support@moodra.com'>support@moodra.com</a><br><br>
        <span class='footer-icons'>
            <a href='https://www.linkedin.com/in/abhishek-bahuguna-74b86b249/' target='_blank'>
                <img src='https://img.icons8.com/ios-glyphs/24/000000/linkedin.png' style='vertical-align:middle; margin-right:10px;'/>
            </a>
            <a href='https://github.com/Abhishek980-tech' target='_blank'>
                <img src='https://img.icons8.com/ios-glyphs/24/000000/github.png' style='vertical-align:middle; margin-right:10px;'/>
            </a>
    </div>
    """,
    unsafe_allow_html=True
)


