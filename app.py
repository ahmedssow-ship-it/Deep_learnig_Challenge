
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
import os

# chemins
TRUE_LABELS = "data/test_true_labels.csv"
LEADERBOARD = "leaderboard.csv"

st.title("🚲 Bike Sharing Challenge Leaderboard")

# charger les vraies valeurs
true_df = pd.read_csv(TRUE_LABELS)

# upload
team_name = st.text_input("Team Name")

uploaded_file = st.file_uploader("Upload your submission.csv", type=["csv"])

if uploaded_file is not None and team_name != "":

    submission = pd.read_csv(uploaded_file)

    if "count" not in submission.columns:
        st.error("Submission must contain column 'count'")

    elif len(submission) != len(true_df):
        st.error("Submission size does not match test set")

    else:

        rmse = np.sqrt(mean_squared_error(true_df["count"], submission["count"]))

        st.success(f"RMSE Score: {rmse:.4f}")

        # charger leaderboard
        if os.path.exists(LEADERBOARD):
            leaderboard = pd.read_csv(LEADERBOARD)
        else:
            leaderboard = pd.DataFrame(columns=["team", "rmse"])

        # ajouter nouvelle entrée
        new_row = pd.DataFrame({
            "team":[team_name],
            "rmse":[rmse]
        })

        leaderboard = pd.concat([leaderboard, new_row], ignore_index=True)

        leaderboard = leaderboard.sort_values("rmse")

        leaderboard.to_csv(LEADERBOARD, index=False)

        st.subheader("🏆 Leaderboard")
        st.dataframe(leaderboard.reset_index(drop=True))

else:

    if os.path.exists(LEADERBOARD):
        leaderboard = pd.read_csv(LEADERBOARD)

        st.subheader("🏆 Current Leaderboard")
        st.dataframe(leaderboard.reset_index(drop=True))
    