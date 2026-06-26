#!/usr/bin/env python3
"""Plot Token Throughput per GPU vs. Interactivity from InferenceX-compatible CSVs."""

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


AMD_HARDWARE = {"mi355x", "mi300x", "mi308x", "mi325x", "mi350x"}

RED_PALETTE = [
    "#FF3333", "#FF6666", "#CC3333", "#FF9999", "#E64545",
    "#FF4D4D", "#B22222", "#FF7777", "#D94444", "#FF5555",
]
GREEN_PALETTE = [
    "#AAFF00", "#44CC44", "#00CC66", "#88DD44", "#22AA22",
    "#66EE66", "#33BB33", "#55DD00", "#00AA55", "#77CC33",
]


def load_csv(filepath):
    rows = []
    with open(filepath) as f:
        lines = [l for l in f if not l.startswith("#")]
    reader = csv.DictReader(lines)
    for row in reader:
        rows.append(row)
    return rows


def is_amd(hw):
    return hw.lower() in AMD_HARDWARE


def build_series(rows):
    """Group rows into series keyed by (Hardware, Framework, TP, SpecDecoding).

    Each series is a list of (interactivity, throughput_gpu, concurrency) tuples.
    """
    series = defaultdict(list)
    for row in rows:
        hw = row.get("Hardware", "")
        fw = row.get("Framework", "")
        tp = row.get("TP", "")
        spec = row.get("Spec Decoding", "none")
        con = row.get("Concurrency", "")
        interactivity = row.get("Mean Interactivity (tok/s/user)", "")
        throughput_gpu = row.get("Throughput/GPU (tok/s)", "")
        if not interactivity or not throughput_gpu:
            continue
        try:
            x = float(interactivity)
            y = float(throughput_gpu)
            con_val = int(con)
        except (ValueError, TypeError):
            continue
        key = (hw, fw, tp, spec if spec else "none")
        series[key].append((x, y, con_val))
    return series


def make_label(hw, fw, tp, spec):
    parts = [hw.upper(), f"TP{tp}"]
    if spec and spec != "none":
        parts.append(spec.upper())
    parts.append(f"({fw.capitalize()})")
    return " ".join(parts)


def assign_colors(series_keys):
    amd_keys = sorted([k for k in series_keys if is_amd(k[0])])
    nv_keys = sorted([k for k in series_keys if not is_amd(k[0])])
    colors = {}
    for i, k in enumerate(amd_keys):
        colors[k] = RED_PALETTE[i % len(RED_PALETTE)]
    for i, k in enumerate(nv_keys):
        colors[k] = GREEN_PALETTE[i % len(GREEN_PALETTE)]
    return colors


def main():
    parser = argparse.ArgumentParser(description="Plot Throughput/GPU vs Interactivity")
    parser.add_argument("csvs", nargs="+", help="One or more InferenceX-compatible CSV files")
    parser.add_argument("--output", "-o", default=None, help="Output image path (default: auto-named .png)")
    parser.add_argument("--title", default="Token Throughput per GPU vs. Interactivity",
                        help="Plot title")
    parser.add_argument("--subtitle", default=None,
                        help="Subtitle (default: auto from CSV data)")
    parser.add_argument("--dpi", type=int, default=150, help="Output DPI")
    args = parser.parse_args()

    all_rows = []
    for csv_path in args.csvs:
        all_rows.extend(load_csv(csv_path))

    if not all_rows:
        print("Error: No data found in CSV files", file=sys.stderr)
        sys.exit(1)

    series = build_series(all_rows)
    colors = assign_colors(series.keys())

    if args.subtitle is None:
        r = all_rows[0]
        model = r.get("Model", "")
        prec = r.get("Precision", "")
        isl = r.get("ISL", "")
        osl = r.get("OSL", "")
        date_str = r.get("Date", "")
        isl_k = f"{int(isl)//1024}K" if isl and int(isl) >= 1024 else isl
        osl_k = f"{int(osl)//1024}K" if osl and int(osl) >= 1024 else osl
        args.subtitle = f"{model} \u2022 {prec.upper()} \u2022 {isl_k} / {osl_k} \u2022 Updated: {date_str}"

    fig, ax = plt.subplots(figsize=(12, 7))
    fig.patch.set_facecolor("#1a1a1a")
    ax.set_facecolor("#1a1a1a")

    for key in sorted(series.keys()):
        hw, fw, tp, spec = key
        color = colors[key]
        label = make_label(hw, fw, tp, spec)
        points = sorted(series[key], key=lambda p: p[0], reverse=True)
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]

        ax.plot(xs, ys, color=color, linewidth=2, marker="o",
                markersize=6, markerfacecolor=color,
                markeredgecolor="white", markeredgewidth=0.5,
                label=label, zorder=3)

        for x, y, con in points:
            ax.annotate(str(con), (x, y), textcoords="offset points",
                        xytext=(0, 10), ha="center", fontsize=7,
                        color="white", fontweight="bold", zorder=4)

    ax.set_xlabel("Interactivity (tok/s/user)", color="white", fontsize=12)
    ax.set_ylabel("Token Throughput per GPU (tok/s/gpu)", color="white", fontsize=12)
    ax.set_title(args.title, color="white", fontsize=14, fontweight="bold",
                 loc="left", pad=20)
    ax.text(0.0, 1.02, args.subtitle, transform=ax.transAxes,
            color="#aaaaaa", fontsize=9, va="bottom")

    ax.tick_params(colors="white", which="both")
    ax.spines["bottom"].set_color("#444444")
    ax.spines["left"].set_color("#444444")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, color="#333333", linewidth=0.5, alpha=0.5)

    ax.yaxis.set_major_formatter(ticker.FuncFormatter(
        lambda v, _: f"{v/1000:.1f}k" if v >= 1000 else f"{v:.0f}"
    ))

    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)

    ax.legend(loc="upper right", facecolor="#242424", edgecolor="#444444",
              fontsize=9, labelcolor="white", framealpha=0.9)

    plt.tight_layout()

    if args.output:
        out_path = args.output
    else:
        out_path = str(Path(args.csvs[0]).parent / "interactivity_plot.png")

    fig.savefig(out_path, dpi=args.dpi, facecolor=fig.get_facecolor(),
                edgecolor="none", bbox_inches="tight")
    print(f"Plot saved to {out_path}")
    plt.close()


if __name__ == "__main__":
    main()
