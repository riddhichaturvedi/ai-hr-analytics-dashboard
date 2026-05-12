import streamlit as st
import pandas as pd
import plotly.express as px

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

ml_df = df.copy()

# ---------------- FEATURE ENGINEERING ----------------
features = ["JobSatisfaction", "WorkLifeBalance"]

if "OverTime" in ml_df.columns:
    ml_df["OverTime"] = ml_df["OverTime"].map({"Yes": 1, "No": 0})
    features.append("OverTime")

# Encode target
if "Attrition" in ml_df.columns:
    ml_df["Attrition"] = ml_df["Attrition"].map({"Yes": 1, "No": 0})

# Drop missing values
ml_df = ml_df.dropna(subset=features + ["Attrition"])

X = ml_df[features]
y = ml_df["Attrition"]

# ---------------- TRAIN MODEL ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LogisticRegression()
model.fit(X_train, y_train)

# ---------------- PREDICTIONS ----------------
ml_df["Attrition_Probability"] = model.predict_proba(X)[:, 1]

ml_df["RiskScore"] = ml_df["Attrition_Probability"] * 100

ml_df["RiskLevel"] = ml_df["RiskScore"].apply(
    lambda x: "High Risk" if x >= 60 else "Low Risk"
)


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI HR Dashboard",
    layout="wide"
)

# ---------------- UI CSS ----------------
st.markdown("""
<style>

/* ---------------- MAIN APP ---------------- */

.stApp {
    background:
    radial-gradient(circle at top left, rgba(59,130,246,0.16) 0%, transparent 28%),
    radial-gradient(circle at top right, rgba(168,85,247,0.18) 0%, transparent 24%),
    radial-gradient(circle at bottom center, rgba(14,165,233,0.10) 0%, transparent 22%),
    linear-gradient(135deg, #020617 0%, #07111f 42%, #020617 100%);
    color: #f8fafc;
}

/* ---------------- LAYOUT ---------------- */

.block-container {
    padding-top: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
    padding-bottom: 2rem;
    max-width: 100%;
}

/* ---------------- SIDEBAR ---------------- */

section[data-testid="stSidebar"] {
    background:
    linear-gradient(
    180deg,
    rgba(15,23,42,0.98) 0%,
    rgba(17,24,39,0.98) 100%
    );
    border-right: 1px solid rgba(255,255,255,0.05);
}

section[data-testid="stSidebar"] * {
    color: #f8fafc !important;
}

/* ---------------- HERO SECTION ---------------- */

.hero-container {
    margin-top: 10px;
    margin-bottom: 40px;
}

.hero-title {
    font-size: 76px;
    font-weight: 900;
    line-height: 0.95;
    letter-spacing: -4px;
    color: white;
    margin-bottom: 20px;
}

.hero-subtitle {
    color: #94a3b8;
    font-size: 20px;
    font-weight: 500;
    margin-bottom: 34px;
}

.hero-panel {

    max-width: 1050px;

    padding: 28px 34px;

    border-radius: 28px;

    background:
    linear-gradient(
    135deg,
    rgba(15,23,42,0.88),
    rgba(30,41,59,0.62)
    );

    border: 1px solid rgba(255,255,255,0.08);

    backdrop-filter: blur(18px);

    box-shadow:
    0 10px 40px rgba(0,0,0,0.38),
    inset 0 1px 0 rgba(255,255,255,0.03);
}

.hero-panel p {
    margin: 0;
    color: #cbd5e1;
    font-size: 18px;
    line-height: 1.9;
    font-weight: 500;
}

/* ---------------- KPI CARDS ---------------- */

div[data-testid="metric-container"] {

    background:
    linear-gradient(
    135deg,
    rgba(15,23,42,0.82),
    rgba(30,41,59,0.72)
    );

    border: 1px solid rgba(255,255,255,0.06);

    padding: 28px;

    border-radius: 26px;

    backdrop-filter: blur(18px);

    box-shadow:
    0 8px 30px rgba(0,0,0,0.34),
    inset 0 1px 0 rgba(255,255,255,0.03);

    transition: all 0.25s ease;
}

div[data-testid="metric-container"]:hover {

    transform: translateY(-5px);

    border: 1px solid rgba(96,165,250,0.38);

    box-shadow:
    0 12px 40px rgba(59,130,246,0.16);
}

div[data-testid="metric-container"] label {

    color: #94a3b8 !important;

    font-size: 13px !important;

    font-weight: 700 !important;

    text-transform: uppercase;

    letter-spacing: 1px;
}

div[data-testid="metric-container"] [data-testid="stMetricValue"] {

    color: white;

    font-size: 42px !important;

    font-weight: 900 !important;
}

/* ---------------- CHARTS ---------------- */

div[data-testid="stPlotlyChart"] {

    background:
    linear-gradient(
    135deg,
    rgba(15,23,42,0.72),
    rgba(17,24,39,0.66)
    );

    border-radius: 28px;

    padding: 24px;

    border: 1px solid rgba(255,255,255,0.05);

    box-shadow:
    0 8px 28px rgba(0,0,0,0.32);

    margin-bottom: 28px;
}

/* ---------------- TABLES ---------------- */

div[data-testid="stDataFrame"] {

    background:
    linear-gradient(
    135deg,
    rgba(15,23,42,0.82),
    rgba(17,24,39,0.76)
    );

    border-radius: 24px;

    border: 1px solid rgba(255,255,255,0.05);

    padding: 12px;

    box-shadow:
    0 8px 24px rgba(0,0,0,0.25);
}

/* ---------------- TABLE HEADER ---------------- */

thead tr th {

    background-color: #0f172a !important;

    color: white !important;

    font-weight: 700 !important;
}

/* ---------------- BUTTON ---------------- */

.stDownloadButton button {

    background:
    linear-gradient(
    135deg,
    #2563eb,
    #7c3aed
    );

    color: white;

    border: none;

    border-radius: 16px;

    padding: 14px 24px;

    font-weight: 700;

    transition: 0.25s ease;
}

.stDownloadButton button:hover {

    transform: translateY(-2px);

    box-shadow:
    0 10px 25px rgba(124,58,237,0.35);
}

/* ---------------- INFO BOX ---------------- */

div[data-testid="stAlert"] {

    background:
    linear-gradient(
    135deg,
    rgba(15,23,42,0.78),
    rgba(30,41,59,0.62)
    );

    border: 1px solid rgba(96,165,250,0.15);

    border-radius: 22px;

    color: white;
}

/* ---------------- TEXT ---------------- */

h2, h3 {
    color: white !important;
    font-weight: 800 !important;
}

p {
    color: #94a3b8;
}

/* ---------------- REMOVE EMPTY ELEMENTS ---------------- */

.element-container:has(style) {
    display: none;
}

/* ---------------- SCROLLBAR ---------------- */

::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: #020617;
}

::-webkit-scrollbar-thumb {
    background: #334155;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("hr_data.csv")
    df.columns = [c.replace(" ", "") for c in df.columns]
    return df

df = load_data()

# ---------------- ML MODEL ----------------
def train_model(data):

    if "Attrition" not in data.columns:
        return None, None

    ml_df = data.copy()

    ml_df["Attrition"] = ml_df["Attrition"].apply(
        lambda x: 1 if x == "Yes" else 0
    )

    ml_df = pd.get_dummies(ml_df, drop_first=True)

    X = ml_df.drop("Attrition", axis=1)
    y = ml_df["Attrition"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    return model, X.columns

model, feature_cols = train_model(df)

# ---------------- PREDICTIONS ----------------
if model is not None:

    ml_df = df.copy()
    ml_df_encoded = pd.get_dummies(ml_df, drop_first=True)

    for col in feature_cols:
        if col not in ml_df_encoded.columns:
            ml_df_encoded[col] = 0

    ml_df_encoded = ml_df_encoded[feature_cols]

    ml_df["Attrition_Probability"] = model.predict_proba(
        ml_df_encoded
    )[:, 1]

    def ml_risk(p):

        if p > 0.7:
            return "High Risk"

        elif p > 0.4:
            return "Medium Risk"

        else:
            return "Low Risk"

    ml_df["ML_Risk"] = ml_df["Attrition_Probability"].apply(ml_risk)

    df = ml_df

# ---------------- HERO SECTION ----------------
st.markdown("""
<div class="hero-container">

<div class="hero-title">
AI-POWERED HR<br>
ANALYTICS DASHBOARD
</div>

<div class="hero-subtitle">
Attrition Intelligence • Workforce Analytics • AI Predictions
</div>

<div class="hero-panel">

<p>
Machine learning powered HR intelligence system designed to predict employee attrition,
analyze workforce behavior, identify organizational risk patterns,
and support strategic HR decision-making through advanced workforce analytics.
</p>

</div>

</div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.header("FILTERS")

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

# ---------------- KPI CALCULATIONS ----------------
employee_count = len(df)

attrition_rate = (
    (df["Attrition"] == "Yes").mean() * 100
    if "Attrition" in df.columns else 0
)

avg_salary = (
    df["MonthlyIncome"].mean()
    if "MonthlyIncome" in df.columns else 0
)

avg_satisfaction = (
    df["JobSatisfaction"].mean()
    if "JobSatisfaction" in df.columns else 0
)

# ---------------- KPI SECTION ----------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("TOTAL EMPLOYEES", employee_count)

with col2:
    st.metric("ATTRITION RATE", f"{attrition_rate:.1f}%")

with col3:
    st.metric("AVG SALARY", f"${avg_salary:,.0f}")

with col4:
    st.metric("AVG SATISFACTION", f"{avg_satisfaction:.1f}")

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- AI RISK KPI ----------------
if "Attrition_Probability" in df.columns:

    avg_risk = df["Attrition_Probability"].mean() * 100

    st.metric(
        "AVG ATTRITION RISK (AI)",
        f"{avg_risk:.1f}%"
    )

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- ML RISK CHART ----------------
if "ML_Risk" in df.columns:

    risk_chart = df["ML_Risk"].value_counts().reset_index()
    risk_chart.columns = ["Risk", "Count"]

    fig = px.bar(
        risk_chart,
        x="Risk",
        y="Count",
        title="AI Predicted Risk Distribution",
        color="Risk",
        color_discrete_map={
            "Low Risk": "#38bdf8",
            "Medium Risk": "#8b5cf6",
            "High Risk": "#f43f5e"
        }
    )

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_size=24,
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor='rgba(255,255,255,0.08)'),
        margin=dict(l=10,r=10,t=60,b=10),
        legend_title_text=''
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------- HIGH RISK TABLE ----------------
if "Attrition_Probability" in df.columns:

    st.subheader("High Risk Employees")

    high_risk = df[df["Attrition_Probability"] > 0.7]

    st.dataframe(
        high_risk.sort_values(
            "Attrition_Probability",
            ascending=False
        ).head(10),
        use_container_width=True
    )

st.subheader("ML-Based Attrition Prediction")

st.dataframe(
    ml_df[[
        "JobSatisfaction",
        "WorkLifeBalance",
        "Attrition_Probability",
        "RiskScore",
        "RiskLevel"
    ]].sort_values("RiskScore", ascending=False).head(20),
    use_container_width=True
)

# ---------------- CHARTS ----------------
c1, c2 = st.columns(2)

with c1:

    if "Department" in df.columns and "Attrition" in df.columns:

        chart = (
            df[df["Attrition"] == "Yes"]
            .groupby("Department")
            .size()
            .reset_index(name="Count")
        )

        fig = px.bar(
            chart,
            x="Department",
            y="Count",
            title="Attrition by Department",
            color_discrete_sequence=["#60a5fa"]
        )

        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            xaxis=dict(showgrid=False),
            yaxis=dict(gridcolor='rgba(255,255,255,0.08)')
        )

        st.plotly_chart(fig, use_container_width=True)

with c2:

    if "Gender" in df.columns:

        chart = (
            df.groupby("Gender")
            .size()
            .reset_index(name="Count")
        )

        fig = px.pie(
            chart,
            names="Gender",
            values="Count",
            hole=0.68,
            title="Gender Distribution",
            color_discrete_sequence=["#38bdf8", "#8b5cf6"]
        )

        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )

        st.plotly_chart(fig, use_container_width=True)

# ---------------- TENURE ----------------
if "YearsAtCompany" in df.columns:

    chart = (
        df.groupby("YearsAtCompany")
        .size()
        .reset_index(name="Employees")
    )

    fig = px.line(
        chart,
        x="YearsAtCompany",
        y="Employees",
        title="Employee Tenure Trend"
    )

    fig.update_traces(
        line_color="#38bdf8",
        line_width=4
    )

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        yaxis=dict(gridcolor='rgba(255,255,255,0.08)')
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------- SALARY ----------------
if "MonthlyIncome" in df.columns:

    fig = px.histogram(
        df,
        x="MonthlyIncome",
        title="Salary Distribution",
        color_discrete_sequence=["#8b5cf6"]
    )

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        yaxis=dict(gridcolor='rgba(255,255,255,0.08)')
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------- AI INSIGHTS ----------------
st.subheader("AI INSIGHTS")

st.info("""
• Sales department shows highest attrition.

• Overtime significantly increases exit probability.

• R&D shows stronger retention patterns.

• ML model predicts individual attrition risk scores.
""")

st.download_button(
    "EXPORT DATA",
    df.to_csv(index=False),
    file_name="hr_report.csv"
)

# ---------------- ML TABLE ----------------
st.subheader("AI ATTRITION RISK (ML MODEL)")

if "Attrition_Probability" in df.columns:

    show_cols = [
        c for c in [
            "EmployeeNumber",
            "Department",
            "JobSatisfaction",
            "WorkLifeBalance",
            "Attrition_Probability",
            "ML_Risk"
        ] if c in df.columns
    ]

    st.dataframe(
        df[show_cols]
        .sort_values(
            "Attrition_Probability",
            ascending=False
        )
        .head(20),
        use_container_width=True
    )