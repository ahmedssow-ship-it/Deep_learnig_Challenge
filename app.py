import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
import os

# Configuration des fichiers
TRUE_LABELS = "Dataset/test_true_labels.csv"
LEADERBOARD = "leaderboard.csv"

st.set_page_config(page_title="Bike Sharing Challenge", layout="centered")

st.title("🚲 Bike Sharing Challenge Leaderboard")

# --- CHARGEMENT DES DONNÉES ---
if not os.path.exists(TRUE_LABELS):
    st.error(f"Fichier {TRUE_LABELS} introuvable sur le serveur.")
    st.stop()

true_df = pd.read_csv(TRUE_LABELS)

# --- FORMULAIRE DE SOUMISSION ---
with st.sidebar:
    st.header("Soumettre un résultat")
    team_name = st.text_input("Nom de l'équipe", placeholder="Ex: DataWarriors")
    uploaded_file = st.file_uploader("Fichier submission.csv", type=["csv"])
    submit_button = st.button("Calculer le score")

if submit_button and uploaded_file and team_name:
    submission = pd.read_csv(uploaded_file)

    # Validation simple
    if "count" not in submission.columns:
        st.error("Le fichier doit contenir une colonne 'count'")
    elif len(submission) != len(true_df):
        st.error(f"Taille incorrecte : {len(submission)} lignes au lieu de {len(true_df)}")
    else:
        # Calcul du score : RMSE
        # Equation: $RMSE = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2}$
        rmse = np.sqrt(mean_squared_error(true_df["count"], submission["count"]))
       
        st.balloons()
        st.success(f"Score calculé avec succès pour {team_name} !")
        st.metric(label="Ton RMSE", value=f"{rmse:.4f}")

        # Gestion du Leaderboard
        if os.path.exists(LEADERBOARD):
            leaderboard = pd.read_csv(LEADERBOARD)
        else:
            leaderboard = pd.DataFrame(columns=["team", "rmse"])

        # Logique : On ne garde que le MEILLEUR score par équipe
        new_data = pd.DataFrame({"team": [team_name], "rmse": [rmse]})
        leaderboard = pd.concat([leaderboard, new_data], ignore_index=True)
       
        # Garder le min par équipe et trier
        leaderboard = leaderboard.groupby("team", as_index=False)["rmse"].min()
        leaderboard = leaderboard.sort_values("rmse").reset_index(drop=True)
       
        leaderboard.to_csv(LEADERBOARD, index=False)

# --- AFFICHAGE DU LEADERBOARD ---
st.subheader("🏆 Classement Actuel")

if os.path.exists(LEADERBOARD):
    df_display = pd.read_csv(LEADERBOARD)
   
    # Styliser le tableau
    st.dataframe(
        df_display.style.highlight_min(axis=0, color='lightgreen', subset=['rmse'])
        .format({"rmse": "{:.4f}"}),
        use_container_width=True
    )
else:
    st.info("Aucune soumission pour le moment. Soyez les premiers !")
