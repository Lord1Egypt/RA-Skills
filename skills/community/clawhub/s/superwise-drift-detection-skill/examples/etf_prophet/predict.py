"""
examples/etf_prophet/predict.py
--------------------------------
Reference implementation: load saved Prophet models and generate 30-day
forward predictions. Called nightly by app.py's /predict endpoint.

Output shape (matches what skill.py's _fetch_inference_records() expects):
    {"records": [{"ticker": "AIQ", "ds": "2026-05-01", "yhat": 28.4, ...}, ...]}
"""

import os
import pickle
from datetime import datetime, timezone

import pandas as pd
import yfinance as yf

TICKERS = ["AIQ", "XAIX", "BOTZ", "CHAT", "SMH"]
MODELS_DIR = "models"
FORECAST_DAYS = 30


def load_model(ticker: str):
    path = os.path.join(MODELS_DIR, f"{ticker}_model.pkl")
    if not os.path.exists(path):
        raise FileNotFoundError(f"No model found for {ticker} at {path}. Run train.py first.")
    with open(path, "rb") as f:
        return pickle.load(f)


def predict_ticker(ticker: str) -> list[dict]:
    model = load_model(ticker)
    future = model.make_future_dataframe(periods=FORECAST_DAYS)
    forecast = model.predict(future).tail(FORECAST_DAYS)

    # Fetch recent actuals to include in the inference record
    actuals = yf.download(ticker, period="30d", auto_adjust=True, progress=False)
    actual_mean = float(actuals["Close"].values.mean()) if not actuals.empty else None

    records = []
    for _, row in forecast.iterrows():
        records.append({
            "ticker": ticker,
            "ds": str(row["ds"].date()),
            "yhat": round(float(row["yhat"]), 4),
            "yhat_lower": round(float(row["yhat_lower"]), 4),
            "yhat_upper": round(float(row["yhat_upper"]), 4),
            "actual_mean_30d": round(actual_mean, 4) if actual_mean else None,
            "run_at": datetime.now(timezone.utc).isoformat(),
        })

    return records


def run_predictions() -> dict:
    """Generate predictions for all tickers. Returns the /predict response payload."""
    all_records = []
    for ticker in TICKERS:
        try:
            records = predict_ticker(ticker)
            all_records.extend(records)
            print(f"[predict] {ticker}: {len(records)} forecast records generated")
        except Exception as exc:
            print(f"[predict] {ticker}: failed — {exc}")

    return {"records": all_records, "count": len(all_records)}


if __name__ == "__main__":
    result = run_predictions()
    print(f"\n[predict] Total records: {result['count']}")
