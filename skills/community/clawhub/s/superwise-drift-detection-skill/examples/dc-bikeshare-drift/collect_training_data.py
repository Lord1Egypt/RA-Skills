"""
collect_training_data.py
------------------------
Fetch real Capital Bikeshare station infrastructure via pybikes (station names,
capacities, e-bike presence), then generate synthetic historical availability
records using realistic DC commute patterns.

Training data is grounded in the real station network but uses synthetic
availability values — this represents "expected normal operation" that the
drift policy will compare against.

Usage:
    python collect_training_data.py
    python collect_training_data.py --snapshots 100
"""

import argparse
import os
import random
import uuid
from datetime import datetime, timedelta, timezone

import pandas as pd
import pybikes

from features import (
    FEATURE_COLS, TARGET_COL,
    availability_bucket, day_type, hour_bucket, season, station_size_bucket,
)

random.seed(42)


def _synthetic_availability_pct(
    hour: int, is_weekday: bool, size: str, sn: str
) -> float:
    """
    Estimate a realistic availability percentage for DC Capital Bikeshare.
    Lower during rush hours (bikes being ridden), higher at night (bikes parked).
    """
    base = 0.55

    if 0 <= hour < 6:
        base += 0.20       # night: bikes resting at stations
    elif 6 <= hour < 10:
        base -= 0.25       # morning rush: bikes being taken
    elif 10 <= hour < 16:
        base -= 0.05       # midday: moderate use
    elif 16 <= hour < 20:
        base -= 0.20       # evening rush: second peak
    else:
        base += 0.05       # evening: bikes returning

    if is_weekday:
        base -= 0.05       # weekdays busier overall

    season_offsets = {"summer": -0.10, "spring": -0.05, "fall": 0.0, "winter": 0.08}
    base += season_offsets.get(sn, 0.0)

    # Smaller stations swing more wildly
    noise = {"small": 0.30, "medium": 0.20, "large": 0.12}[size]
    base += random.uniform(-noise, noise)

    return max(0.02, min(0.98, base))


def main():
    parser = argparse.ArgumentParser(description="Generate DC Bikeshare training data.")
    parser.add_argument(
        "--snapshots", type=int, default=50,
        help="Synthetic historical snapshots per station (default: 50)"
    )
    args = parser.parse_args()

    print("[collect] Fetching Capital Bikeshare station infrastructure via pybikes...")
    network = pybikes.get("capital-bikeshare")
    network.update()
    stations = network.stations
    print(f"[collect] {len(stations)} stations fetched")

    records = []
    base_date = datetime(2024, 1, 1, tzinfo=timezone.utc)

    for station in stations:
        slots = int(station.extra.get("slots") or 10)
        has_eb = "yes" if station.extra.get("has_ebikes") else "no"
        size = station_size_bucket(slots)
        station_id = station.extra.get("uid") or str(uuid.uuid4())

        for _ in range(args.snapshots):
            # Random timestamp spanning ~1 year of history
            ts = base_date + timedelta(hours=random.randint(0, 8760))
            h = ts.hour
            hb = hour_bucket(h)
            dt = day_type(ts.weekday())
            sn = season(ts.month)

            pct = _synthetic_availability_pct(h, dt == "weekday", size, sn)
            # Convert pct to bikes available (for availability_bucket helper)
            synthetic_bikes = round(pct * slots)
            avail = availability_bucket(synthetic_bikes, slots)

            records.append({
                "station_id": station_id,
                "station_name": station.name,
                "station_size_bucket": size,
                "has_ebikes": has_eb,
                "hour_bucket": hb,
                "day_type": dt,
                "season": sn,
                TARGET_COL: avail,
            })

    df = pd.DataFrame(records)
    os.makedirs("data/training", exist_ok=True)
    out_path = "data/training/dc_bikeshare_training.csv"
    df.to_csv(out_path, index=False)

    print(f"[collect] {len(df):,} records saved to {out_path}")
    print(f"[collect] availability_bucket distribution:")
    print(df[TARGET_COL].value_counts().to_string())
    print(f"[collect] station_size_bucket distribution:")
    print(df["station_size_bucket"].value_counts().to_string())


if __name__ == "__main__":
    main()
