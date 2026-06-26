"""
train.py
--------
Train a RandomForest classifier to predict availability_bucket from
categorical station features. Saves the fitted pipeline as a pickle.

Usage:
    python train.py
    python train.py --csv data/training/dc_bikeshare_training.csv
"""

import argparse
import os
import pickle

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder

from features import FEATURE_COLS, TARGET_COL

MODEL_PATH = "models/dc_bikeshare_model.pkl"


def main():
    parser = argparse.ArgumentParser(description="Train DC Bikeshare availability classifier.")
    parser.add_argument("--csv", default="data/training/dc_bikeshare_training.csv")
    args = parser.parse_args()

    print(f"[train] Loading {args.csv}...")
    df = pd.read_csv(args.csv)
    print(f"[train] {len(df):,} rows loaded")

    X = df[FEATURE_COLS]
    y = df[TARGET_COL]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline = Pipeline([
        ("enc", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)),
        ("clf", RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)),
    ])

    print("[train] Fitting RandomForest...")
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    print("[train] Evaluation on held-out test set:")
    print(classification_report(y_test, y_pred))

    os.makedirs("models", exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(pipeline, f)
    print(f"[train] Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    main()
