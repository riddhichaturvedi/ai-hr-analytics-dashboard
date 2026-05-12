import streamlit as st
import pandas as pd
import plotly.express as px

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI HR Dashboard",
    layout="wide"
)

# ---------------- UI CSS ----------------
st.markdown("""
<style>
.stApp {
    background:
    radial-gradient(circle at top left, rgba(59,130,246,0.16) 0%, transparent 28%),
    radial-gradient(circle at top right, rgba(168,85,247,0.18) 0%, transparent 24%),
    radial-gradient(circle at bottom center, rgba(14,165,233,0.10) 0%, transparent 22%),
    linear-gradient(135deg, #020617 0%, #07111f 42%, #020617 100%);
    color: #f8fafc;
}

.block-container {
    padding: 2rem 3rem;
    max-width: 100%;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(15,23,42,0.98), rgba(17,24,39,0.98));
    border-right: 1px solid rgba(255,255,255,0.05);
}

section[data-testid="stSidebar"] * {
    color: #f8fafc !important;
}

.hero-title {
    font-size: 70px;
    font-weight: 900;
    color: white;
    line-height: 1;
}

.hero-subtitle {
    color: #94a3b8;
    font-size: 18px;
    margin-bottom: 30px;
}

div[data-testid="metric-container"] {
    background: rgba(15,23,42,0.85);
    padding: 20px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.06);
}
</style>
""", unsafe_allow_html=True)

# ---------------- DATA LOAD ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("hr_data.csv")
    df.columns = [c.replace(" ", "") for c in df.columns]
    return df

df = load_data()

if df.empty:
    st.error("Dataset not found or empty")
    st.stop()

# ---------------- ML MODEL ----------------
def train_model(data):

    if "Attrition" not in data.columns:
        return None, None

    ml_df = data.copy()

    ml_df["Attrition"] = ml_df["Attrition"].apply(lambda x: 1 if x == "Yes" else 0)

    ml_df = pd.get_dummies(ml_df, drop_first=True)

    X = ml_df.drop("Attrition", axis=1)
    y = ml_df["Attrition"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    return model, X.columns

model, feature_cols = train_model(df)

# ---------------- PREDICTIONS ----------------
ml_df = df.copy()

if model is not None:

    try:
        ml_df_encoded = pd.get_dummies(ml_df, drop_first=True)

        for col in feature_cols:
            if col not in ml_df_encoded.columns:
                ml_df_encoded[col] = 0

        ml_df_encoded = ml_df_encoded[feature_cols]

        probs = model.predict_proba(ml_df_encoded)[:, 1]

        ml_df["Attrition_Probability"] = probs
        ml_df["RiskScore"] = probs * 100

        def risk(p):
            if p > 0.7:
                return "High Risk"
            elif p > 0.4:
                return "Medium Risk"
            else:
                return "Low Risk"

        ml_df["ML_Risk"] = ml_df["Attrition_Probability"].apply(risk)

    except Exception as e:
        st.error(f"ML Error: {e}")
        ml_df["Attrition_Probability"] = 0
        ml_df["RiskScore"] = 0
        ml_df["ML_Risk"] = "Unknown"

df = ml_df

# ---------------- HERO ----------------
st.markdown("""
<div class="hero-title">AI-POWERED HR ANALYTICS DASHBOARD</div>
<div class="hero-subtitle">Attrition Intelligence • Workforce Analytics • ML Predictions</div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR FILTERS ----------------
if "Department" in df.columns:
    dept = st.sidebar.multiselect(
        "Department",
        df["Department"].unique(),
        default=df["Department"].unique()
    )
    df = df[df["Department"].isin(dept)]

if "Gender" in df.columns:
    gender = st.sidebar.multiselect(
        "Gender",
        df["Gender"].unique(),
        default=df["Gender"].unique()
    )
    df = df[df["Gender"].isin(gender)]

# ---------------- KPI ----------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Employees", len(df))

col2.metric(
    "Attrition Rate",
    f"{(df['Attrition']=='Yes').mean()*100:.1f}%" if "Attrition" in df else "0%"
)

col3.metric(
    "Avg Salary",
    f"{df['MonthlyIncome'].mean():,.0f}" if "MonthlyIncome" in df else "0"
)

col4.metric(
    "Avg Satisfaction",
    f"{df['JobSatisfaction'].mean():.1f}" if "JobSatisfaction" in df else "0"
)

# ---------------- ML KPI ----------------
if "Attrition_Probability" in df.columns:
    st.metric(
        "Avg AI Risk",
        f"{df['Attrition_Probability'].mean()*100:.1f}%"
    )

# ---------------- ML CHART ----------------
if "ML_Risk" in df.columns:

    risk_df = df["ML_Risk"].value_counts().reset_index()
    risk_df.columns = ["Risk", "Count"]

    fig = px.bar(risk_df, x="Risk", y="Count", color="Risk")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- TABLE ----------------
if "Attrition_Probability" in df.columns:

    st.subheader("High Risk Employees")

    st.dataframe(
        df.sort_values("Attrition_Probability", ascending=False).head(10),
        use_container_width=True
    )

# ---------------- CHARTS ----------------
if "Department" in df.columns and "Attrition" in df.columns:

    chart = df[df["Attrition"]=="Yes"].groupby("Department").size().reset_index(name="Count")

    fig = px.bar(chart, x="Department", y="Count", title="Attrition by Department")
    st.plotly_chart(fig, use_container_width=True)

if "Gender" in df.columns:

    chart = df.groupby("Gender").size().reset_index(name="Count")

    fig = px.pie(chart, names="Gender", values="Count", hole=0.6)
    st.plotly_chart(fig, use_container_width=True)

# ---------------- INSIGHTS ----------------
st.subheader("AI Insights")

st.info("""
- Sales has highest attrition risk
- Overtime increases employee exit probability
- ML model predicts individual risk scoring
""")

# ---------------- DOWNLOAD ----------------
st.download_button(
    "Download Report",
    df.to_csv(index=False),
    file_name="hr_report.csv"
)

# ---------------- FINAL TABLE ----------------
if "Attrition_Probability" in df.columns:

    st.subheader("ML Risk Table")

    st.dataframe(
        df[[
            c for c in [
                "Department",
                "JobSatisfaction",
                "WorkLifeBalance",
                "Attrition_Probability",
                "ML_Risk"
            ] if c in df.columns
        ]].head(20),
        use_container_width=True
    )