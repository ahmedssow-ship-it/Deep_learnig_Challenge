import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
import os
from datetime import datetime

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

    if "count" not in submission.columns:
        st.error("Le fichier doit contenir une colonne 'count'")
    elif len(submission) != len(true_df):
        st.error(f"Taille incorrecte : {len(submission)} lignes au lieu de {len(true_df)}")
    else:
        # Calcul du RMSE
        rmse = np.sqrt(mean_squared_error(true_df["count"], submission["count"]))
        # Date et heure actuelle (format: YYYY-MM-DD HH:MM)
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
       
        st.balloons()
        st.success(f"Score calculé avec succès pour {team_name} !")
        st.metric(label="Ton RMSE", value=f"{rmse:.4f}")

        # Gestion du Leaderboard
        if os.path.exists(LEADERBOARD):
            leaderboard = pd.read_csv(LEADERBOARD)
        else:
            # Création avec la colonne de temps
            leaderboard = pd.DataFrame(columns=["team", "rmse", "last_submission"])

        # Nouvelle donnée
        new_data = pd.DataFrame({
            "team": [team_name],
            "rmse": [rmse],
            "last_submission": [now]
        })
       
        leaderboard = pd.concat([leaderboard, new_data], ignore_index=True)
       
        # LOGIQUE : On garde le meilleur score par équipe.
        # Si scores égaux, on garde la soumission la plus récente.
        leaderboard = leaderboard.sort_values(by=["rmse", "last_submission"], ascending=[True, False])
        leaderboard = leaderboard.drop_duplicates(subset="team", keep="first")
       
        leaderboard.to_csv(LEADERBOARD, index=False)

# --- AFFICHAGE DU LEADERBOARD ---
st.subheader("🏆 Classement Actuel")

if os.path.exists(LEADERBOARD):
    df_display = pd.read_csv(LEADERBOARD)
   
    # Ajout automatique du Rang (1, 2, 3...)
    df_display.insert(0, 'Rank', range(1, len(df_display) + 1))
   
    # Renommer les colonnes pour l'esthétique
    df_display.columns = ["Rang", "Équipe", "RMSE", "Dernière Soumission"]

    # Stylisation
    st.dataframe(
        df_display.style.highlight_min(axis=0, color='lightgreen', subset=['RMSE'])
        .format({"RMSE": "{:.4f}"}),
        use_container_width=True,
        hide_index=True # On cache l'index Pandas car on a notre colonne Rang
    )
else:
    st.info("Aucune soumission pour le moment. Soyez les premiers !")
