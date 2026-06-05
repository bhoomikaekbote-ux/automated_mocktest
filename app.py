```python
import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Student Analytics Dashboard",
    layout="wide"
)

@st.cache_data
def load_data():

    files = os.listdir(".")

    st.sidebar.write("Repository Files:")
    st.sidebar.write(files)

    csv_file = None

    for file in files:
        if file.endswith(".csv"):
            csv_file = file
            break

    if csv_file is None:
        st.error("No CSV file found in repository folder")
        st.write("Current files:", files)
        st.stop()

    st.success(f"Loaded file: {csv_file}")

    df = pd.read_csv(csv_file)

    return df

df = load_data()

st.title("📊 Student Performance Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Average Math",
    round(df["math score"].mean(), 2)
)

col2.metric(
    "Average Reading",
    round(df["reading score"].mean(), 2)
)

col3.metric(
    "Average Writing",
    round(df["writing score"].mean(), 2)
)

st.subheader("Dataset Preview")
st.dataframe(df.head())

st.subheader("Columns")
st.write(df.columns.tolist())
```
