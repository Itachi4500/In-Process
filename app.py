import streamlit as st
import pandas as pd
from utils.cleaner import clean_data
from utils.eda import run_eda
from utils.visualizer import show_visuals
from utils.modeler import run_modeling
from utils.exporter import export_data
from utils.powerbi_pipeline import powerbi_pipeline
from utils.live_dashboard import live_dashboard
from utils.refresh import refresh_data
from utils.memory import remember, recall, show_memory, clear_all_memory
from utils.layout import select_dashboard_size

# ------------------------------
# 🌙 Theme Switcher
# ------------------------------
theme = st.sidebar.radio("🎨 Select Theme", ["Light", "Dark"], index=0)

light_css = """
<style>
body {
    background-color: #f9f9fb;
    color: #000;
}
</style>
"""

dark_css = """
<style>
body {
    background-color: #1e1e2f;
    color: #f5f5f5;
}
.sidebar .sidebar-content {
    background-color: #2c2f3a;
    color: #f5f5f5;
}
</style>
"""

st.markdown(light_css if theme == "Light" else dark_css, unsafe_allow_html=True)

# ------------------------------
# 🎉 CSS: Sidebar + Animations
# ------------------------------
st.markdown("""
    <style>
    .main {
        animation: fadein 1s ease-in;
    }
    @keyframes fadein {
        0% {opacity: 0;}
        100% {opacity: 1;}
    }
    .sidebar .sidebar-content {
        padding: 1rem;
        background-color: #f0f2f6;
        border-right: 2px solid #ddd;
    }
    .block-container {
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------------
# 🤖 Branding Header
# ------------------------------
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Robot_icon.svg/240px-Robot_icon.svg.png", width=70)
st.sidebar.markdown("## 🤖 <b>Data Scientist Assistant</b>", unsafe_allow_html=True)

# ------------------------------
# Navigation Menu
# ------------------------------
menu = {
    "📁 Upload Dataset": "Upload Dataset",
    "🧹 Data Cleaning": "Data Cleaning",
    "📊 Exploratory Data Analysis": "Exploratory Data Analysis",
    "📈 Visualization": "Visualization",
    "🧠 Feature Engineering & Modeling": "Feature Engineering & Modeling",
    "📌 Evaluation & Tuning": "Evaluation & Tuning",
    "⬇️ Export Dataset": "Export Dataset",
    "📝 Generate Report": "Generate Report",
    "📊 Power BI Pipeline": "Power BI",
    "📡 Live Dashboard": "Dashboard"

}
choice = st.sidebar.radio("📂 **Select Operation**", list(menu.keys()))

# Refresh the dataset
# Maintain dataset state
if "uploaded_df" in st.session_state:
    st.session_state.df = st.session_state.uploaded_df
if "cleaned_df" in st.session_state:
    st.session_state.df = st.session_state.cleaned_df

refresh_data()

# ------------------------------
# Dataset State
# ------------------------------
if "df" not in st.session_state:
    st.session_state.df = None
if "cleaned_df" in st.session_state:
    st.session_state.df = st.session_state.cleaned_df

st.sidebar.markdown("---")
if st.session_state.df is not None:
    st.sidebar.success("✅ Dataset Loaded")
    st.sidebar.write(f"Rows: {st.session_state.df.shape[0]}")
    st.sidebar.write(f"Columns: {st.session_state.df.shape[1]}")
else:
    st.sidebar.error("🚫 No Dataset Loaded")

# ------------------------------
# 🧭 Main Navigation Logic
# ------------------------------
st.title(menu[choice])
st.markdown("---")

uploaded_file = st.file_uploader("📁 Upload your dataset", type=["csv", "xlsx"])
if choice == "📁 Upload Dataset":
    df = upload_data()
    
    if uploaded_file is not None:
        file_name = uploaded_file.name
        try:
            if file_name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            elif file_name.endswith(".xlsx"):
                df = pd.read_excel(uploaded_file)
            else:
                st.warning("⚠️ Please upload a CSV or Excel file.")
                df = None
    
            if df is not None:
                st.session_state.uploaded_df = df
                st.success("✅ File uploaded and saved successfully!")
                st.write(df.head())

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")


        cleaning_steps = []

        # 1. Drop missing values
        if st.button("🧽 Drop Missing Values"):
            df.dropna(inplace=True)
            cleaning_steps.append("Dropped missing values")
            st.success("Missing values removed!")

        # 2. Normalize numerical columns
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        cols_to_scale = st.multiselect("🔄 Normalize columns", numeric_cols)

        if st.button("⚖️ Normalize Selected Columns"):
            for col in cols_to_scale:
                min_val = df[col].min()
                max_val = df[col].max()
                df[col] = (df[col] - min_val) / (max_val - min_val)
            cleaning_steps.append(f"Normalized columns: {', '.join(cols_to_scale)}")
            st.success("Selected columns normalized!")

        # Save final cleaned DataFrame
        st.session_state.cleaned_df = df

        # 🧠 Memory Logic
        if cleaning_steps:
            remember("cleaning_steps", cleaning_steps)

        st.markdown("---")
        st.markdown("### 🧠 Cleaning Memory")

        steps = recall("cleaning_steps")
        if steps:
            st.info(f"Cleaning steps learned: {steps}")

        show_memory()

        if st.button("🗑️ Clear Memory"):
            clear_all_memory()
            st.success("Memory cleared.")


elif choice == "📊 Exploratory Data Analysis":
    if st.session_state.df is not None:
        run_eda(st.session_state.df)
    else:
        st.warning("⚠️ Please upload a dataset first.")

elif choice == "📈 Visualization":
    if st.session_state.df is not None:
        show_visuals(st.session_state.df)
    else:
        st.warning("⚠️ Please upload a dataset first.")

elif choice == "🧠 Feature Engineering & Modeling":
    if st.session_state.df is not None:
        run_modeling(st.session_state.df)
    else:
        st.warning("⚠️ Please upload a dataset first.")

elif choice == "📌 Evaluation & Tuning":
    st.info("📌 Model evaluation & tuning is handled during modeling. See results after training.")

elif choice == "⬇️ Export Dataset":
    if st.session_state.df is not None:
        export_data(st.session_state.df)
    else:
        st.warning("⚠️ Please upload a dataset first.")
# Bower BI Pipeline
elif choice == "📊 Power BI Pipeline":
    if "cleaned_df" in st.session_state:
        df = st.session_state.cleaned_df
        powerbi_pipeline(df)
    else:
        st.warning("⚠️ Please upload and clean your dataset first.")
        
# Live Dashboard
elif choice == "📡 Live Dashboard":
    if "cleaned_df" in st.session_state:
        df = st.session_state.cleaned_df
        live_dashboard(df)
    else:
        st.warning("Please upload and clean your dataset first.")

# ------------------------------
# 📝 Auto-Generated Report Modal
# ------------------------------
elif choice == "📝 Generate Report":
    if st.session_state.df is not None:
        st.subheader("📄 Data Summary Report")

        with st.expander("📌 View Quick Stats"):
            st.write(st.session_state.df.describe(include="all").transpose())

        with st.expander("🧠 Feature Summary"):
            st.write("Total columns:", st.session_state.df.shape[1])
            st.write("Categorical columns:", list(st.session_state.df.select_dtypes(include='object').columns))
            st.write("Numeric columns:", list(st.session_state.df.select_dtypes(include=['int64', 'float64']).columns))

        with st.expander("🚨 Missing Values Summary"):
            st.write(st.session_state.df.isnull().sum().to_frame(name="Missing Values"))

        st.success("✅ Report Ready — You can export or take screenshots.")
    else:
        st.warning("⚠️ Upload and clean a dataset before generating the report.")
        

