
    
import pandas as pd
import numpy as np
import argparse
import os
from sklearn.metrics import mean_squared_error


def evaluate_submission(submission_file, true_labels_file, leaderboard_file, team_name):

    # Charger les données
    true_df = pd.read_csv(true_labels_file)
    submission_df = pd.read_csv(submission_file)

    # Vérifier les colonnes
    if "count" not in submission_df.columns:
        raise ValueError("Submission file must contain a 'count' column")

    if len(submission_df) != len(true_df):
        raise ValueError("Submission size does not match test set")

    # Calcul du RMSE
    rmse = np.sqrt(mean_squared_error(true_df["count"], submission_df["count"]))

    print(f"Team: {team_name}")
    print(f"RMSE Score: {rmse:.4f}")

    # Charger le leaderboard ou en créer un nouveau
    if os.path.exists(leaderboard_file):
        leaderboard = pd.read_csv(leaderboard_file)
    else:
        leaderboard = pd.DataFrame(columns=["team", "rmse"])

    # Ajouter le nouveau score
    new_row = pd.DataFrame({
        "team": [team_name],
        "rmse": [rmse]
    })

    leaderboard = pd.concat([leaderboard, new_row], ignore_index=True)

    # Trier par meilleur score
    leaderboard = leaderboard.sort_values(by="rmse")

    # Sauvegarder
    leaderboard.to_csv(leaderboard_file, index=False)

    print("
Updated Leaderboard:")
    print(leaderboard)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Evaluate Bike Sharing Challenge Submission")

    parser.add_argument("--submission", type=str, required=True,
                        help="Path to submission.csv")

    parser.add_argument("--true_labels", type=str, required=True,
                        help="Path to test_true_labels.csv")

    parser.add_argument("--team", type=str, required=True,
                        help="Team name")

    parser.add_argument("--leaderboard", type=str, default="leaderboard.csv",
                        help="Leaderboard file")

    args = parser.parse_args()

    evaluate_submission(
        args.submission,
        args.true_labels,
        args.leaderboard,
        args.team
    )
    