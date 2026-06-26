"""
predict.py
----------
Fetch live Capital Bikeshare station data via pybikes, engineer categorical
features, run the trained model, and return inference records for Superwise.

Output shape (matches skill.py's _ingest_inference_records):
    {"records": [...], "count": N}

Usage:
    python predict.py
"""

import os
import pickle
from datetime import datetime, timezone

import pandas as pd
import pybikes

from features import (
    FEATURE_COLS, TARGET_COL,
    day_type, hour_bucket, season, station_size_bucket,
)

MODEL_PATH = "models/dc_bikeshare_model.pkl"


def run_predictions() -> dict:
    now = datetime.now(timezone.utc)
    hb = hour_bucket(now.hour)
    dt = day_type(now.weekday())
    sn = season(now.month)

    print("[predict] Fetching live Capital Bikeshare data via pybikes...")
    network = pybikes.get("capital-bikeshare")
    network.update()
    stations = network.stations
    print(f"[predict] {len(stations)} stations fetched")

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"No model at {MODEL_PATH}. Run train.py first.")

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    rows = []
    meta = []
    for station in stations:
        slots = int(station.extra.get("slots") or 10)
        has_eb = "yes" if station.extra.get("has_ebikes") else "no"
        size = station_size_bucket(slots)

        rows.append({
            "station_size_bucket": size,
            "has_ebikes": has_eb,
            "hour_bucket": hb,
            "day_type": dt,
            "season": sn,
        })
        meta.append({
            "station_id": station.extra.get("uid", ""),
            "station_name": station.name,
            "station_size_bucket": size,
            "has_ebikes": has_eb,
            "hour_bucket": hb,
            "day_type": dt,
            "season": sn,
        })

    X = pd.DataFrame(rows, columns=FEATURE_COLS)
    predictions = model.predict(X)

    records = []
    for i, m in enumerate(meta):
        record = dict(m)
        record[TARGET_COL] = predictions[i]
        records.append(record)

    print(f"[predict] {len(records)} inference records generated")
    return {"records": records, "count": len(records)}


if __name__ == "__main__":
    result = run_predictions()
    from collections import Counter
    buckets = Counter(r["availability_bucket"] for r in result["records"])
    print(f"\n[predict] availability_bucket distribution: {dict(buckets)}")
