#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
from swmmtoolbox import extract

from entropy_metrics import calculate_entropy_record


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True), encoding="utf-8")


def extract_series(out_path: Path, node: str) -> tuple[Any, np.ndarray]:
    series = extract(str(out_path), f"node,{node},Total_inflow").iloc[:, 0]
    return series.index, series.to_numpy(dtype=float)


def trial_out_paths(run_dir: Path) -> list[Path]:
    paths = sorted((run_dir / "trials").glob("mc_trial_*/model.out"))
    if not paths:
        raise ValueError(f"No Monte Carlo trial model.out files found under {run_dir / 'trials'}")
    return paths


def build_ensemble_payload(run_dir: Path, node: str) -> dict[str, Any]:
    paths = trial_out_paths(run_dir)
    time = None
    values = []
    for path in paths:
        this_time, series = extract_series(path, node)
        if time is None:
            time = this_time
        values.append(series)
    arr = np.asarray(values, dtype=float)
    return {
        "metric": f"node,{node},Total_inflow",
        "node": node,
        "source": "swmmtoolbox extract from Monte Carlo trial .out files",
        "sample_count": int(arr.shape[0]),
        "time_count": int(arr.shape[1]),
        "time": [str(t) for t in time],
        "values": arr.tolist(),
    }


def max_entropy(record: dict[str, Any]) -> float | None:
    values = [float(v) for v in record.get("entropy", []) if v is not None]
    return max(values) if values else None


def mean_entropy(record: dict[str, Any]) -> float | None:
    values = [float(v) for v in record.get("entropy", []) if v is not None]
    return float(np.mean(values)) if values else None


def plot_entropy_curves(records: dict[str, dict[str, Any]], out_png: Path) -> None:
    plt.rcParams.update({"font.family": "Arial", "font.size": 9, "xtick.direction": "in", "ytick.direction": "in"})
    fig, ax = plt.subplots(figsize=(9, 3.4), dpi=300, constrained_layout=True)
    start = np.datetime64("1994-01-11T00:00:00")
    end = np.datetime64("1994-01-11T12:00:00")
    for node, record in records.items():
        time = np.asarray(record["time"], dtype="datetime64[ns]")
        entropy = np.asarray([np.nan if v is None else float(v) for v in record["entropy"]], dtype=float)
        mask = (time >= start) & (time <= end)
        plot_time = [datetime.fromisoformat(str(value)) for value in np.asarray(record["time"], dtype=object)[mask]]
        ax.plot(plot_time, entropy[mask], linewidth=1.8, label=node)
    ax.set_title("Monte Carlo output entropy")
    ax.set_ylabel("Normalized entropy")
    ax.set_xlabel("Time on 1994-01-11")
    ax.set_ylim(-0.03, 1.03)
    ax.grid(True, linestyle=":", alpha=0.4)
    ax.legend(loc="upper right", framealpha=0.95)
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, bbox_inches="tight")
    plt.close(fig)


def propagate_entropy(run_dir: Path, *, nodes: list[str], bins: int, out_dir: Path) -> dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    ensemble_dir = out_dir / "ensembles"
    entropy_dir = out_dir / "entropy"
    records: dict[str, dict[str, Any]] = {}
    node_summaries: list[dict[str, Any]] = []
    for node in nodes:
        payload = build_ensemble_payload(run_dir, node)
        ensemble_path = ensemble_dir / f"{node}_ensemble.json"
        write_json(ensemble_path, payload)
        record = calculate_entropy_record(payload, bins=bins)
        record["node"] = node
        entropy_path = entropy_dir / f"{node}_entropy.json"
        write_json(entropy_path, record)
        records[node] = record
        node_summaries.append(
            {
                "node": node,
                "metric": record["metric"],
                "sample_count": record["sample_count"],
                "time_count": record["time_count"],
                "max_entropy": max_entropy(record),
                "mean_entropy": mean_entropy(record),
                "ensemble_json": str(ensemble_path),
                "entropy_json": str(entropy_path),
            }
        )
    figure = out_dir / "entropy_curves.png"
    plot_entropy_curves(records, figure)
    summary = {
        "ok": True,
        "mode": "monte_carlo_output_entropy",
        "run_dir": str(run_dir),
        "bins": bins,
        "nodes": node_summaries,
        "figure": str(figure),
        "interpretation": "Normalized Shannon entropy of Monte Carlo output ensembles; this is not calibration performance.",
    }
    write_json(out_dir / "entropy_summary.json", summary)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract Monte Carlo SWMM output ensembles and compute entropy curves.")
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--nodes", nargs="+", default=["J6", "OUT_0"])
    parser.add_argument("--bins", type=int, default=10)
    parser.add_argument("--out-dir", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    out_dir = args.out_dir or (args.run_dir / "entropy")
    print(json.dumps(propagate_entropy(args.run_dir, nodes=args.nodes, bins=args.bins, out_dir=out_dir), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
