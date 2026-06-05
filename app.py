```python
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Student Exam Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("student_exam_performance.csv")
    return df

df = load_data()

# ---------------- SIDEBAR ----------------
st.sidebar.title("📌 Dashboard Filters")

gender_filter = st.sidebar.multiselect(
    "Select Gender",
    options=df["gender"].unique(),
    default=df["gender"].unique()
)

parent_filter = st.sidebar.multiselect(
    "Parental Education",
    options=df["parental level of education"].unique(),
    default=df["parental level of education"].unique()
)

filtered_df = df[
    (df["gender"].isin(gender_filter)) &
    (df["parental level of education"].isin(parent_filter))
]

# ---------------- HEADER ----------------
st.title("📊 Student Performance Analytics Dashboard")
st.markdown("Deep Analytics & Insights using Streamlit")

# ---------------- KPIs ----------------
math_avg = round(filtered_df["math score"].mean(), 2)
reading_avg = round(filtered_df["reading score"].mean(), 2)
writing_avg = round(filtered_df["writing score"].mean(), 2)

col1, col2, col3 = st.columns(3)

col1.metric("📘 Average Math Score", math_avg)
col2.metric("📗 Average Reading Score", reading_avg)
col3.metric("📙 Average Writing Score", writing_avg)

st.divider()

# ---------------- DATA PREVIEW ----------------
st.subheader("📄 Dataset Preview")
st.dataframe(filtered_df.head(10), use_container_width=True)

# ---------------- CHARTS ----------------

# Gender Distribution
fig_gender = px.pie(
    filtered_df,
    names="gender",
    title="Gender Distribution"
)

# Lunch Type
fig_lunch = px.bar(
    filtered_df["lunch"].value_counts(),
    title="Lunch Type Count",
    labels={"value": "Count", "index": "Lunch"}
)

# Average Scores by Gender
avg_gender = filtered_df.groupby("gender")[[
    "math score",
    "reading score",
    "writing score"
]].mean().reset_index()

fig_avg_gender = px.bar(
    avg_gender,
    x="gender",
    y=["math score", "reading score", "writing score"],
    barmode="group",
    title="Average Scores by Gender"
)

# Correlation Heatmap
corr = filtered_df[[
    "math score",
    "reading score",
    "writing score"
]].corr()

fig_heatmap = go.Figure(
    data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        text=np.round(corr.values, 2),
        texttemplate="%{text}",
        colorscale="Viridis"
    )
)

fig_heatmap.update_layout(title="Score Correlation Heatmap")

# Score Distribution
fig_hist = px.histogram(
    filtered_df,
    x="math score",
    nbins=20,
    title="Math Score Distribution"
)

# Parental Education Analysis
fig_parent = px.box(
    filtered_df,
    x="parental level of education",
    y="math score",
    color="gender",
    title="Math Score vs Parent Education"
)

# ---------------- DISPLAY CHARTS ----------------

col4, col5 = st.columns(2)

with col4:
    st.plotly_chart(fig_gender, use_container_width=True)

with col5:
    st.plotly_chart(fig_lunch, use_container_width=True)

st.plotly_chart(fig_avg_gender, use_container_width=True)

col6, col7 = st.columns(2)

with col6:
    st.plotly_chart(fig_heatmap, use_container_width=True)

with col7:
    st.plotly_chart(fig_hist, use_container_width=True)

st.plotly_chart(fig_parent, use_container_width=True)

# ---------------- INSIGHTS ----------------

st.subheader("🧠 AI Generated Insights")

top_math = filtered_df["math score"].max()
low_math = filtered_df["math score"].min()

st.success(f"Highest Math Score: {top_math}")
st.error(f"Lowest Math Score: {low_math}")

if math_avg > 65:
    st.info("Students are performing well in Mathematics.")
else:
    st.warning("Math performance needs improvement.")

if reading_avg > writing_avg:
    st.info("Reading scores are higher than writing scores.")
else:
    st.info("Writing scores are stronger than reading scores.")

# ---------------- RAW DATA ----------------
with st.expander("🔍 View Full Dataset"):
    st.dataframe(filtered_df, use_container_width=True)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("Developed using Python, Streamlit & Plotly")
```

