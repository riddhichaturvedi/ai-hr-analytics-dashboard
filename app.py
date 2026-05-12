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
# ---------------- PREDICTIONS ----------------
ml_df = df.copy()

if model is not None:

    try:
        ml_df_encoded = pd.get_dummies(ml_df, drop_first=True)

        # ensure all required features exist
        for col in feature_cols:
            if col not in ml_df_encoded.columns:
                ml_df_encoded[col] = 0

        ml_df_encoded = ml_df_encoded[feature_cols]

        probs = model.predict_proba(ml_df_encoded)[:, 1]

        ml_df["Attrition_Probability"] = probs
        ml_df["RiskScore"] = probs * 100

        def ml_risk(p):
            if p > 0.7:
                return "High Risk"
            elif p > 0.4:
                return "Medium Risk"
            else:
                return "Low Risk"

        ml_df["ML_Risk"] = ml_df["Attrition_Probability"].apply(ml_risk)

    except Exception as e:
        st.error(f"ML Error: {e}")

        # SAFE FALLBACK (IMPORTANT)
        ml_df["Attrition_Probability"] = 0
        ml_df["RiskScore"] = 0
        ml_df["ML_Risk"] = "Unknown"

# always keep df usable
df = ml_df