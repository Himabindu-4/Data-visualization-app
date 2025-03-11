import streamlit as st
import pandas as pd
import plotly.express as px

# Set Streamlit page config
st.set_page_config(page_title="Data Visualization App", layout="wide")

# Title
st.title("📊 Interactive Data Visualization System")

# File Upload
uploaded_file = st.file_uploader("📂 Upload a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    # Read the dataset
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.write("### 📜 Preview of Dataset")
        st.dataframe(df.head())

        # Show dataset statistics
        st.write("### 📊 Dataset Statistics")
        st.write(df.describe())

        # Convert categorical data to string type
        for col in df.select_dtypes(include=["object"]).columns:
            df[col] = df[col].astype(str)

        # Select numeric columns for visualization
        numeric_cols = df.select_dtypes(include=["number"]).columns

        # Sidebar for Visualization Selection
        st.sidebar.header("📈 Select Visualization Type")
        chart_type = st.sidebar.radio(
            "Choose the type of chart",
            ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart", "Correlation Heatmap"]
        )

        # X and Y Axis Selection for Graphs
        x_axis = st.sidebar.selectbox("Select X-axis", df.columns)
        y_axis = st.sidebar.selectbox("Select Y-axis", numeric_cols, index=0 if len(numeric_cols) > 0 else None)

        # Generate the selected chart
        if chart_type == "Bar Chart":
            if x_axis and y_axis:
                fig = px.bar(df, x=x_axis, y=y_axis, title=f"Bar Chart: {x_axis} vs {y_axis}")
                st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Line Chart":
            if x_axis and y_axis:
                fig = px.line(df, x=x_axis, y=y_axis, title=f"Line Chart: {x_axis} vs {y_axis}")
                st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Scatter Plot":
            if x_axis and y_axis:
                fig = px.scatter(df, x=x_axis, y=y_axis, title=f"Scatter Plot: {x_axis} vs {y_axis}")
                st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Pie Chart":
            category_col = st.sidebar.selectbox("Select Categorical Column for Pie Chart", df.select_dtypes(include=['object']).columns)
            if category_col:
                fig = px.pie(df, names=category_col, title=f"Pie Chart of {category_col}")
                st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Correlation Heatmap":
            st.write("### 🔥 Correlation Heatmap")
            df_numeric = df.select_dtypes(include=['number'])
            if not df_numeric.empty:
                fig_corr = px.imshow(df_numeric.corr(), text_auto=True, title="Feature Correlation")
                st.plotly_chart(fig_corr, use_container_width=True)
            else:
                st.warning("⚠ No numeric columns available for correlation heatmap.")

    except Exception as e:
        st.error(f"Error loading file: {e}")

else:
    st.info("📂 Please upload a file to get started!")
