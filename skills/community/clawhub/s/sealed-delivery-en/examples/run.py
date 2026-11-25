"""Delivery entry point: read the customer's local sales data, run the forecast,
and write results to a target file.

Works under sealed execution as well:
- imports `model` at the same level (MGC recognizes it)
- creates the output directory itself (MGC does not do that for you)
- reads input, writes output, never touches the network

Usage:
    python run.py --input sales.csv --output predictions.json --horizon 3
Environment fallbacks:
    FORECAST_INPUT / FORECAST_OUTPUT / FORECAST_HORIZON
"""

import argparse
import csv
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import model


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sales forecasting")
    parser.add_argument(
        "--input", default=os.environ.get("FORECAST_INPUT", "sales.csv")
    )
    parser.add_argument(
        "--output", default=os.environ.get("FORECAST_OUTPUT", "predictions.json")
    )
    parser.add_argument(
        "--horizon", type=int, default=int(os.environ.get("FORECAST_HORIZON", "3"))
    )
    parser.add_argument("--window", type=int, default=3)
    return parser.parse_args()


def load_series(path: Path) -> tuple[list[str], list[float]]:
    months, values = [], []
    with path.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            months.append(row["month"])
            values.append(float(row["sales"]))
    if not values:
        raise ValueError("input has no rows")
    return months, values


def main() -> int:
    args = parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"input not found: {input_path}", file=sys.stderr)
        return 2

    months, values = load_series(input_path)
    points = model.forecast(values, args.horizon, args.window)

    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "license": "trial" if model.TRIAL_MODE else "licensed",
        "input_rows": len(values),
        "window": args.window,
        "horizon": len(points),
        "summary": {
            "last_actual": values[-1],
            "growth_rate": round(model.growth_rate(values), 4),
            "next_forecast": points[0] if points else None,
        },
        "points": [
            {"period": f"T+{i + 1}", "forecast": value}
            for i, value in enumerate(points)
        ],
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(json.dumps(result["summary"], ensure_ascii=False))
    print(f"predictions written: {output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
