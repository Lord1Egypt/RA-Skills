#!/usr/bin/env python3
"""
Skill Doctor — chart.py
Generates a simple trend chart from locally stored state history.

Reads only ~/.skill-doctor/state/*.json — no network calls.
Requires matplotlib (pip install matplotlib --break-system-packages).
"""

import sys
from datetime import datetime
from pathlib import Path


def generate_chart(structured_results: list[dict], charts_dir: Path):
    try:
        import matplotlib
        matplotlib.use("Agg")  # headless, no display needed
        import matplotlib.pyplot as plt
    except ImportError:
        print(
            "⚠️  matplotlib not installed — skipping --chart.\n"
            "   Install with: pip install matplotlib --break-system-packages",
            file=sys.stderr,
        )
        return

    if not structured_results:
        print("⚠️  No data to chart.", file=sys.stderr)
        return

    charts_dir.mkdir(parents=True, exist_ok=True)

    labels = [r["key"] for r in structured_results]
    downloads = [r["current"]["downloads"] for r in structured_results]
    active = [r["current"]["active_installs"] for r in structured_results]

    fig, ax = plt.subplots(figsize=(10, 5))
    x = range(len(labels))
    width = 0.35

    ax.bar([i - width / 2 for i in x], downloads, width, label="Downloads")
    ax.bar([i + width / 2 for i in x], active, width, label="Active Installs")

    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, rotation=30, ha="right")
    ax.set_ylabel("Count")
    ax.set_title("Skill Doctor — Portfolio Snapshot")
    ax.legend()
    fig.tight_layout()

    out_path = charts_dir / f"snapshot-{datetime.now().strftime('%Y%m%d-%H%M')}.png"
    fig.savefig(out_path, dpi=150)
    plt.close(fig)

    print(f"📊 Chart saved to {out_path}")
