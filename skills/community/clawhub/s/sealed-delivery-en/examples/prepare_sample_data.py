"""Generate sample sales data to walk through the delivery loop locally.

This file is not shipped in a real delivery package — the customer uses its
own business data and the script only reads and computes.

Usage:
    python prepare_sample_data.py [output_path]
"""

import csv
import sys
from pathlib import Path

# 18 months of sample sales with a mild upward trend and seasonality
SALES = [
    ("2025-01", 120400), ("2025-02", 118900), ("2025-03", 131200),
    ("2025-04", 128700), ("2025-05", 140500), ("2025-06", 145300),
    ("2025-07", 139800), ("2025-08", 148600), ("2025-09", 152100),
    ("2025-10", 149700), ("2025-11", 161400), ("2025-12", 178900),
    ("2026-01", 133200), ("2026-02", 130800), ("2026-03", 142600),
    ("2026-04", 147900), ("2026-05", 151300), ("2026-06", 158700),
]


def main():
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "sales.csv")
    out.parent.mkdir(parents=True, exist_ok=True)

    with out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["month", "sales"])
        writer.writerows(SALES)

    print(f"sample data written: {out.resolve()} ({len(SALES)} rows)")


if __name__ == "__main__":
    main()
