import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import glob
import numpy as np

st.set_page_config(
    page_title="Student Performance Analytics",
    page_icon="📊",
    layout="wide"
)

# ---------------- LOAD DATA ----------------

@st.cache_data
def load_data():

    csv_files = glob.glob("*.csv")

    if len(csv_files) == 0:
        st.error("No CSV file found in repository folder")
        st.write("Upload dataset in same folder as app.py")
        st.stop()

    file_name = csv_files[0]

    st.sidebar.success(f"Loaded File: {file_name}")

    df = pd.read_csv(file_name)

    return df

df = load_data()

# ---------------- TITLE ----------------

st.title("📊 Student Exam Performance Dashboard")

# ---------------- SIDEBAR ----------------

st.sidebar.header("Filters")

gender = st.sidebar.multiselect(
    "Gender",
    df["gender"].unique(),
    default=df["gender"].unique()
)

filtered = df[df["gender"].isin(gender)]

# ---------------- KPI ----------------

c1, c2, c3 = st.columns(3)

c1.metric(
    "Avg Math",
    round(filtered["math score"].mean(), 2)
)

c2.metric(
    "Avg Reading",
    round(filtered["reading score"].mean(), 2)
)

c3.metric(
    "Avg Writing",
    round(filtered["writing score"].mean(), 2)
)

st.divider()

# ---------------- DATA ----------------

st.subheader("Dataset Preview")

st.dataframe(filtered.head())

# ---------------- CHARTS ----------------

fig1 = px.histogram(
    filtered,
    x="math score",
    nbins=20,
    title="Math Score Distribution"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

avg_gender = filtered.groupby("gender")[
    ["math score","reading score","writing score"]
].mean().reset_index()

fig2 = px.bar(
    avg_gender,
    x="gender",
    y=["math score","reading score","writing score"],
    barmode="group",
    title="Average Scores by Gender"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

corr = filtered[
    ["math score","reading score","writing score"]
].corr()

fig3 = go.Figure(
    data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns
    )
)

fig3.update_layout(
    title="Correlation Heatmap"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ---------------- INSIGHTS ----------------

st.subheader("Insights")

st.success(
    f"Highest Math Score: {filtered['math score'].max()}"
)

st.info(
    f"Average Reading Score: {round(filtered['reading score'].mean(),2)}"
)

if filtered["math score"].mean() > 65:
    st.write("Students perform well in mathematics.")
else:
    st.write("Mathematics performance needs improvement.")

# ---------------- RAW DATA ----------------

with st.expander("View Complete Dataset"):
    st.dataframe(filtered)
