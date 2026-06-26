"""Daily prediction pipeline using Tencent daily data only.

For each target stock, load cached or fresh daily OHLCV history,
compute the same technical features used during training, and predict
the next trading day's direction based on the latest bar on or before
the target date.
"""
import json
import os
import sys
import time
from datetime import datetime, timedelta

import akshare as ak
import joblib
import numpy as np
import pandas as pd

import config
from features import add_technical_features


PREDICTION_COLUMNS = [
    "股票代码",
    "股票名称",
    "当前时间",
    "预测生成时间",
    "当前价格",
    "预测结果",
    "上涨概率",
    "下跌概率",
    "数据频率",
]


def load_model():
    model = joblib.load(config.MODEL_PATH)
    with open(config.FEATURE_PATH) as f:
        feature_names = json.load(f)
    scaler = joblib.load(config.SCALER_PATH)
    return model, feature_names, scaler


def code_to_tx_symbol(code):
    code = str(code).zfill(6)
    return f"sh{code}" if code.startswith("6") else f"sz{code}"


def parse_target_date(target_dt=None):
    """Parse a datetime/date string and return a normalized trade-date timestamp."""
    if target_dt is None:
        return pd.Timestamp(datetime.now().date())
    return pd.to_datetime(target_dt).normalize()


def _normalize_prediction_history(df):
    """Normalize prediction history schema for backward-compatible appends."""
    normalized_df = df.copy()
    normalized_df["股票代码"] = normalized_df["股票代码"].astype(str).str.zfill(6)
    normalized_df["当前时间"] = pd.to_datetime(normalized_df["当前时间"]).dt.strftime("%Y-%m-%d")
    if "预测生成时间" not in normalized_df.columns:
        normalized_df["预测生成时间"] = normalized_df["当前时间"] + " 00:00:00"
    normalized_df["预测生成时间"] = pd.to_datetime(normalized_df["预测生成时间"]).dt.strftime("%Y-%m-%d %H:%M:%S")
    return normalized_df.reindex(columns=PREDICTION_COLUMNS)


def _save_prediction_snapshot(batch_df, batch_timestamp):
    """Persist a per-run snapshot alongside the append-only master history."""
    batch_tag = pd.to_datetime(batch_timestamp).strftime("%Y%m%d_%H%M%S")
    snapshot_path = os.path.join(config.PREDICTION_HISTORY_DIR, f"predictions_{batch_tag}.csv")
    batch_df.to_csv(snapshot_path, index=False, encoding="utf-8-sig")
    return snapshot_path


def _dedupe_prediction_master(df):
    """Keep one prediction per stock per trade date, preferring the latest batch."""
    deduped_df = _normalize_prediction_history(df)
    deduped_df = deduped_df.sort_values(
        ["预测生成时间", "当前时间", "股票代码"],
        ascending=[False, False, True],
    )
    deduped_df = deduped_df.drop_duplicates(
        subset=["股票代码", "当前时间"],
        keep="first",
    )
    return deduped_df.reset_index(drop=True)


def _merge_prediction_history(new_rows):
    """Update the prediction master table and persist the current batch snapshot."""
    new_df = _normalize_prediction_history(pd.DataFrame(new_rows))
    if os.path.exists(config.PREDICTION_PATH):
        history_df = _normalize_prediction_history(pd.read_csv(config.PREDICTION_PATH))
        merged_df = pd.concat([history_df, new_df], ignore_index=True)
    else:
        merged_df = new_df

    merged_df = _dedupe_prediction_master(merged_df)
    merged_df.to_csv(config.PREDICTION_PATH, index=False, encoding="utf-8-sig")
    snapshot_path = _save_prediction_snapshot(new_df, new_df.iloc[0]["预测生成时间"])
    return merged_df, snapshot_path


def _normalize_daily_df(df):
    """Normalize Tencent daily columns to the training schema."""
    df = df.copy()
    df.rename(columns={"date": "datetime"}, inplace=True)
    df["datetime"] = pd.to_datetime(df["datetime"])
    if "volume" not in df.columns and "amount" in df.columns:
        df["volume"] = df["amount"]
    for c in ["open", "close", "high", "low", "volume"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df.sort_values("datetime").reset_index(drop=True)


def load_cached_daily_data(code):
    """Load cached daily training data if available."""
    cache_path = os.path.join(config.DATA_DIR, f"{str(code).zfill(6)}_daily.csv")
    if not os.path.exists(cache_path):
        return None
    try:
        return _normalize_daily_df(pd.read_csv(cache_path))
    except Exception:
        return None


def fetch_daily_data_tx(code, target_date, lookback_days=450, forward_days=5):
    """Fetch daily data via Tencent API around the target trade date."""
    end = target_date + timedelta(days=forward_days)
    start = target_date - timedelta(days=lookback_days)
    tx_sym = code_to_tx_symbol(code)
    try:
        df = ak.stock_zh_a_hist_tx(
            symbol=tx_sym,
            start_date=start.strftime("%Y%m%d"),
            end_date=end.strftime("%Y%m%d"),
            adjust="qfq",
        )
        if df is not None and not df.empty:
            return _normalize_daily_df(df)
    except Exception:
        pass
    return None


def load_daily_data_for_prediction(code, target_dt):
    """Load enough daily history for feature generation and the target bar."""
    target_date = parse_target_date(target_dt)
    cached_df = load_cached_daily_data(code)
    if cached_df is not None and not cached_df.empty:
        hist_df = cached_df[cached_df["datetime"] <= target_date].copy()
        if len(hist_df) >= 120:
            return hist_df, "daily.tencent"

    fetched_df = fetch_daily_data_tx(code, target_date)
    if fetched_df is None or fetched_df.empty:
        return None, None

    hist_df = fetched_df[fetched_df["datetime"] <= target_date].copy()
    if len(hist_df) < 50:
        return None, None
    return hist_df, "daily.tencent"


def predict_single(code, name, model, feature_names, scaler, target_dt=None):
    """Predict for one stock at target_dt, return result dict or None."""
    target_date = parse_target_date(target_dt)

    df, freq = load_daily_data_for_prediction(code, target_date)
    if df is None:
        print(f"  Warning: Insufficient data for {name}({code})")
        return None

    df = add_technical_features(df)
    for m in feature_names:
        if m not in df.columns:
            df[m] = 0.0

    mask = df["datetime"] <= target_date
    if mask.sum() == 0:
        mask = pd.Series([True] * len(df), index=df.index)

    target_row = df.loc[mask].iloc[[-1]].copy()
    X = target_row[feature_names].values
    X = np.nan_to_num(X, nan=0.0)
    X = scaler.transform(X)
    prob = model.predict_proba(X)[0]
    pred_label = int(prob[1] >= 0.5)

    raw_dt = pd.to_datetime(target_row["datetime"].values[0])
    pred_time = raw_dt.strftime("%Y-%m-%d")

    return {
        "股票代码": code,
        "股票名称": name,
        "当前时间": pred_time,
        "当前价格": round(float(target_row["close"].values[0]), 2),
        "预测结果": "上涨" if pred_label == 1 else "下跌",
        "上涨概率": round(float(prob[1]), 4),
        "下跌概率": round(float(prob[0]), 4),
        "数据频率": freq,
    }


def run_prediction(target_dt=None):
    """Run prediction for all target stocks at the given time."""
    target_dt = parse_target_date(target_dt).strftime("%Y-%m-%d")
    batch_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("=" * 60)
    print("  Stock Price Direction Prediction - Daily Prediction Pipeline")
    print(f"  Target date: {target_dt}")
    print(f"  Generated at: {batch_timestamp}")
    print("=" * 60)

    model, feature_names, scaler = load_model()

    results = []
    for code, name in config.TARGET_STOCKS.items():
        print(f"  Predicting {name} ({code}) @ {target_dt} ...")
        r = predict_single(code, name, model, feature_names, scaler, target_dt=target_dt)
        if r:
            r["预测生成时间"] = batch_timestamp
            results.append(r)
        time.sleep(config.FETCH_DELAY)

    if results:
        history_df, snapshot_path = _merge_prediction_history(results)
        current_df = history_df[history_df["预测生成时间"] == batch_timestamp].copy()
        print(f"\n  Prediction history saved -> {config.PREDICTION_PATH}")
        print(f"  Batch snapshot saved -> {snapshot_path}")
        print(current_df.to_string(index=False))
    else:
        print("  No predictions generated.")

    print("\nPrediction complete!\n")
    return results


if __name__ == "__main__":
    dt = sys.argv[1] if len(sys.argv) > 1 else None
    run_prediction(target_dt=dt)
