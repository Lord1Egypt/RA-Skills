"""
examples/etf_prophet/train.py
------------------------------
Reference implementation: train a Facebook Prophet model per ETF ticker
and save the training CSV in the format expected by setup_dataset.py.

This is an example of Step 1 for any user of the superwise-drift-detection-skill:
  1. Train your model → save training data as a CSV  ← this file shows how
  2. Run setup_dataset.py to upload that CSV to Superwise
  3. Deploy scheduler.py to Render and point INFERENCE_ENDPOINT_URL at app.py

After running this script:
    python examples/etf_prophet/train.py

You will have:
    data/training/etf_combined_training.csv   (upload this to Superwise)
    models/<TICKER>_model.pkl                  (Prophet models — used by predict.py)

Then run:
    python setup_dataset.py \
        --training-csv data/training/etf_combined_training.csv \
        --model-name etf_prophet \
        --key-col ticker_date
"""

import os
import pickle

import pandas as pd
import yfinance as yf
from prophet import Prophet

TICKERS = ["AIQ", "XAIX", "BOTZ", "CHAT", "SMH"]
TRAINING_YEARS = 2
MODELS_DIR = "models"
TRAINING_DIR = os.path.join("data", "training")

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(TRAINING_DIR, exist_ok=True)


def fetch_training_data(ticker: str) -> pd.DataFrame:
    """Fetch 2 years of daily close prices from yfinance."""
    raw = yf.download(ticker, period=f"{TRAINING_YEARS}y", auto_adjust=True, progress=False)
    df = raw[["Close"]].reset_index()
    df.columns = ["ds", "y"]
    df["ds"] = pd.to_datetime(df["ds"]).dt.tz_localize(None)
    df["ticker"] = ticker
    return df.dropna()


def train_and_save(ticker: str) -> pd.DataFrame:
    df = fetch_training_data(ticker)
    model = Prophet(daily_seasonality=False, weekly_seasonality=True, yearly_seasonality=True)
    model.fit(df[["ds", "y"]])

    path = os.path.join(MODELS_DIR, f"{ticker}_model.pkl")
    with open(path, "wb") as f:
        pickle.dump(model, f)

    print(f"[train] {ticker}: trained on {len(df)} rows → {path}")
    return df


def main():
    all_frames = []

    for ticker in TICKERS:
        df = train_and_save(ticker)
        all_frames.append(df)

    combined = pd.concat(all_frames, ignore_index=True)
    # Synthetic key for deduplication in Superwise
    combined["ticker_date"] = combined["ticker"] + "_" + combined["ds"].astype(str)
    combined["ds"] = combined["ds"].astype(str)

    out_path = os.path.join(TRAINING_DIR, "etf_combined_training.csv")
    combined.to_csv(out_path, index=False)
    print(f"\n[train] Combined training CSV saved → {out_path}")
    print(f"[train] Rows: {len(combined)}")
    print(f"\nNext step:")
    print(f"  python setup_dataset.py --training-csv {out_path} --model-name etf_prophet --key-col ticker_date")


if __name__ == "__main__":
    main()
