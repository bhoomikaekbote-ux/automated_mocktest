import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import numpy as np

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Student Performance Analytics",
    page_icon="📊",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
if os.path.exists("student_exam_performance.csv"):
    try:
        df = pd.read_csv("student_exam_performance.csv")

        st.dataframe(df)

        st.write("Display the column names:")
        st.write(df.columns)

    except Exception as e:
        st.error(f"Error reading file: {e}")

else:
    st.error("Dataset file not found")


# ---------------- SIDEBAR ----------------

st.sidebar.title("Dashboard Filters")

# gender_filter = st.sidebar.multiselect(
#     "Gender",
#     options=df["gender"].unique(),
#     default=df["gender"].unique()
# )

# Remove extra spaces from column names
df.columns = df.columns.str.strip()

# Show columns for debugging
st.write("Columns:", df.columns.tolist())

# Check if gender column exists
if "Gender" in df.columns:

    st.sidebar.title("Dashboard Filters")

    gender_filter = st.sidebar.multiselect(
        "Gender",
        options=df["Gender"].unique(),
        default=df["Gender"].unique()
    )

else:
    st.error("Column 'gender' not found in dataset")

education_filter = st.sidebar.multiselect(
    "Parental Education",
    options=df["Parental_Education_Level"].unique(),
    default=df["Parental_Education_Level"].unique()
)

filtered_df = df[
    (df["gender"].isin(gender_filter)) &
    (df["parental level of education"].isin(education_filter))
]

# ---------------- TITLE ----------------

st.title("📊 Student Exam Analytics Dashboard")

st.markdown(
    "Interactive dashboard for deep analytics and insights"
)

# ---------------- KPI SECTION ----------------

avg_math = round(filtered_df["math score"].mean(), 2)
avg_reading = round(filtered_df["reading score"].mean(), 2)
avg_writing = round(filtered_df["writing score"].mean(), 2)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Math Avg", avg_math)
c2.metric("Reading Avg", avg_reading)
c3.metric("Writing Avg", avg_writing)
c4.metric("Students", filtered_df.shape[0])

st.divider()

# ---------------- DATASET PREVIEW ----------------

st.subheader("Dataset Preview")

st.dataframe(
    filtered_df.head(10),
    use_container_width=True
)

# ---------------- CHARTS ----------------

col1, col2 = st.columns(2)

with col1:

    fig_gender = px.pie(
        filtered_df,
        names="gender",
        title="Gender Distribution"
    )

    st.plotly_chart(
        fig_gender,
        use_container_width=True
    )

with col2:

    fig_lunch = px.bar(
        filtered_df["lunch"].value_counts(),
        title="Lunch Distribution"
    )

    st.plotly_chart(
        fig_lunch,
        use_container_width=True
    )

# Average scores by gender

gender_avg = filtered_df.groupby(
    "gender"
)[["math score",
   "reading score",
   "writing score"]].mean().reset_index()

fig_scores = px.bar(
    gender_avg,
    x="gender",
    y=[
        "math score",
        "reading score",
        "writing score"
    ],
    barmode="group",
    title="Average Scores by Gender"
)

st.plotly_chart(
    fig_scores,
    use_container_width=True
)

# Histogram

fig_hist = px.histogram(
    filtered_df,
    x="math score",
    nbins=25,
    title="Math Score Distribution"
)

st.plotly_chart(
    fig_hist,
    use_container_width=True
)

# Boxplot

fig_box = px.box(
    filtered_df,
    x="parental level of education",
    y="math score",
    color="gender",
    title="Math Score vs Parent Education"
)

st.plotly_chart(
    fig_box,
    use_container_width=True
)

# Correlation heatmap

corr = filtered_df[
    ["math score",
     "reading score",
     "writing score"]
].corr()

heatmap = go.Figure(
    data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        text=np.round(corr.values,2),
        texttemplate="%{text}"
    )
)

heatmap.update_layout(
    title="Correlation Heatmap"
)

st.plotly_chart(
    heatmap,
    use_container_width=True
)

# ---------------- INSIGHTS ----------------

st.subheader("Insights")

highest_math = filtered_df["math score"].max()
lowest_math = filtered_df["math score"].min()

st.success(
    f"Highest Math Score: {highest_math}"
)

st.error(
    f"Lowest Math Score: {lowest_math}"
)

if avg_math > 65:
    st.info(
        "Students perform well in mathematics."
    )
else:
    st.warning(
        "Mathematics performance needs improvement."
    )

if avg_reading > avg_writing:
    st.info(
        "Reading scores are stronger than writing scores."
    )
else:
    st.info(
        "Writing scores are stronger than reading scores."
    )

# ---------------- RAW DATA ----------------

with st.expander("View Full Dataset"):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# ---------------- FOOTER ----------------

st.markdown("---")
st.caption("Built with Streamlit + Plotly")
