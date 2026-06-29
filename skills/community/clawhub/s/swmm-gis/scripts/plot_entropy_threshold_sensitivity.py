#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import rasterio
from matplotlib.lines import Line2D


DEFAULT_VARIANTS = [
    ("A", "Strict baseline", "0.015", "0.95", "baseline_paperonly"),
    ("B", "Lower entropy-change threshold", "0.010", "0.95", "fine_delta"),
    ("C", "Stricter similarity threshold", "0.015", "0.97", "fine_similarity"),
    ("D", "Fine entropy + similarity", "0.010", "0.97", "fine_both"),
    ("E", "Very fine paper rule", "0.008", "0.98", "very_fine"),
]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def configure_plot() -> None:
    plt.rcParams.update(
        {
            "font.family": "Arial",
            "font.size": 12,
            "axes.titlesize": 12,
            "axes.labelsize": 12,
            "xtick.labelsize": 12,
            "ytick.labelsize": 12,
            "legend.fontsize": 12,
        }
    )


def load_path_rows(base: Path) -> list[dict[str, str]]:
    with (base / "longest_flowpath_metrics.csv").open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def plot_decision_spaces(sensitivity_dir: Path, variants: list[tuple[str, str, str, str, str]], out_path: Path) -> None:
    fig, axs = plt.subplots(1, len(variants), figsize=(21, 4.8), dpi=220, sharey=True)
    if len(variants) == 1:
        axs = [axs]
    for ax, (letter, label, delta_s, sim_s, dirname) in zip(axs, variants):
        base = sensitivity_dir / dirname
        delta = float(delta_s)
        sim = float(sim_s)
        summary = read_json(base / "paper_entropy_partition_summary.json")
        rows = load_path_rows(base)
        x, y, selected = [], [], []
        for row in rows[1:-1]:
            if row.get("delta_NWJE_seq") and row.get("WFJS_seq"):
                x.append(abs(float(row["delta_NWJE_seq"])))
                y.append(float(row["WFJS_seq"]))
                selected.append(row.get("selected_split") == "True")
        x_arr = np.asarray(x, dtype=float)
        y_arr = np.asarray(y, dtype=float)
        selected_arr = np.asarray(selected, dtype=bool)
        xmax = max(0.08, float(np.nanmax(x_arr)) * 1.05)
        ax.scatter(x_arr[~selected_arr], y_arr[~selected_arr], s=10, c="0.72", alpha=0.65, linewidths=0, rasterized=True)
        ax.scatter(x_arr[selected_arr], y_arr[selected_arr], s=34, c="#d7191c", edgecolors="black", linewidths=0.45, zorder=3)
        ax.axvline(delta, color="#d7191c", linestyle="--", linewidth=1.1)
        ax.axhline(sim, color="#d7191c", linestyle="--", linewidth=1.1)
        ax.fill_between([0, delta], sim, 1.02, color="#2ca25f", alpha=0.08, linewidth=0)
        ax.fill_between([delta, xmax], 0, sim, color="#d7191c", alpha=0.07, linewidth=0)
        ax.set_xlim(0, xmax)
        ax.set_ylim(0.55, 1.02)
        ax.grid(True, alpha=0.24, linewidth=0.6)
        ax.tick_params(direction="in", top=True, right=True, length=4, width=0.8)
        ax.set_title(
            f"{letter}. {label}\n"
            f"Split rule: |dNWJE| >= {delta_s}; WFJS <= {sim_s}\n"
            f"{summary['final_subcatchment_count']} subcatchments"
        )
        ax.set_xlabel("|dNWJE_seq|")
    axs[0].set_ylabel("WFJS_seq")
    handles = [
        Line2D([0], [0], marker="o", color="none", markerfacecolor="0.72", markeredgecolor="none", markersize=7, label="Flowpath cells"),
        Line2D([0], [0], marker="o", color="none", markerfacecolor="#d7191c", markeredgecolor="black", markersize=8, label="Selected split points"),
        Line2D([0], [0], color="#d7191c", linestyle="--", linewidth=1.2, label="Threshold lines"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, -0.02))
    fig.suptitle("Paper-rule split/lump decision spaces for threshold sensitivity", y=1.04, fontsize=12)
    fig.tight_layout(rect=[0, 0.08, 1, 0.98])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)


def plot_watershed_partitions(
    sensitivity_dir: Path,
    stream_path: Path,
    variants: list[tuple[str, str, str, str, str]],
    out_path: Path,
    case_label: str,
) -> None:
    with rasterio.open(stream_path) as ds:
        stream = ds.read(1, masked=True).astype(float).filled(np.nan)
    stream_mask = np.where(np.isfinite(stream) & (stream > 0), 1.0, np.nan)

    fig, axs = plt.subplots(1, len(variants), figsize=(21, 7), dpi=220)
    if len(variants) == 1:
        axs = [axs]
    for ax, (letter, label, delta_s, sim_s, dirname) in zip(axs, variants):
        base = sensitivity_dir / dirname
        with rasterio.open(base / "paper_entropy_partition_labels.tif") as ds:
            labels = ds.read(1, masked=True).astype(float).filled(np.nan)
            bounds = ds.bounds
        extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]
        summary = read_json(base / "paper_entropy_partition_summary.json")
        rows = load_path_rows(base)
        path_xy = [(float(row["x"]), float(row["y"])) for row in rows]
        selected_rows = [row for row in rows if row.get("selected_split") == "True"]
        ax.imshow(labels, extent=extent, origin="upper", cmap="tab20", interpolation="nearest")
        ax.imshow(stream_mask, extent=extent, origin="upper", cmap="gray_r", interpolation="nearest", alpha=0.95)
        ax.plot([p[0] for p in path_xy], [p[1] for p in path_xy], color="#0057ff", linewidth=1.05)
        if selected_rows:
            ax.scatter(
                [float(row["x"]) for row in selected_rows],
                [float(row["y"]) for row in selected_rows],
                s=22,
                c="#d7191c",
                edgecolors="black",
                linewidths=0.45,
                zorder=3,
            )
        ax.set_title(f"{letter}. {label}\n|dNWJE| >= {delta_s}; WFJS <= {sim_s}\n{summary['final_subcatchment_count']} subcatchments")
        ax.set_aspect("equal")
        ax.axis("off")
    handles = [
        Line2D([0], [0], color="black", linewidth=2, label="Extracted stream network"),
        Line2D([0], [0], color="#0057ff", linewidth=1.5, label="Longest flow path"),
        Line2D([0], [0], marker="o", color="none", markerfacecolor="#d7191c", markeredgecolor="black", markersize=8, label="Selected split point"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, -0.01))
    fig.suptitle(f"Effect of paper-rule thresholds on {case_label} subcatchment partition", y=1.02, fontsize=12)
    fig.tight_layout(rect=[0, 0.06, 1, 0.98])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot paper-rule entropy threshold sensitivity figures.")
    parser.add_argument("--sensitivity-dir", type=Path, required=True)
    parser.add_argument("--stream", type=Path, required=True)
    parser.add_argument("--out-decision", type=Path, required=True)
    parser.add_argument("--out-partitions", type=Path, required=True)
    parser.add_argument("--case-label", default="the watershed")
    args = parser.parse_args()

    configure_plot()
    plot_decision_spaces(args.sensitivity_dir, DEFAULT_VARIANTS, args.out_decision)
    plot_watershed_partitions(args.sensitivity_dir, args.stream, DEFAULT_VARIANTS, args.out_partitions, args.case_label)
    print(
        json.dumps(
            {
                "ok": True,
                "decision_spaces": str(args.out_decision),
                "watershed_partitions": str(args.out_partitions),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
