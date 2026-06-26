#!/usr/bin/env python3
"""Render common plots from a small JSON spec.

Design goals:
- Always produce a clean PNG (no overlaps)
- Sensible defaults (labels, grid, legend)
- Minimal schema; easy to extend

Usage:
  python plot_from_spec.py --spec spec.json --out out.png
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

try:
    import seaborn as sns
except Exception:
    sns = None


def _maybe_set_theme():
    if sns is not None:
        sns.set_theme(style="whitegrid")
    else:
        mpl.rcParams.update(
            {
                "axes.grid": True,
                "grid.alpha": 0.25,
            }
        )


def _load_csv(path: str) -> Dict[str, np.ndarray]:
    import csv

    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"CSV not found: {path}")

    with p.open("r", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        raise ValueError(f"CSV is empty: {path}")

    cols = reader.fieldnames or []
    out: Dict[str, List[float]] = {c: [] for c in cols}

    for r in rows:
        for c in cols:
            v = r.get(c)
            if v is None:
                out[c].append(np.nan)
            else:
                out[c].append(float(v))

    return {k: np.asarray(v, dtype=float) for k, v in out.items()}


def _as_array(value: Any, data: Dict[str, Any]) -> np.ndarray:
    if isinstance(value, str):
        if value not in data:
            raise KeyError(f"Unknown data key/column: {value}")
        return np.asarray(data[value], dtype=float)
    return np.asarray(value, dtype=float)


def render(spec: Dict[str, Any], out_path: str):
    kind = spec.get("kind", "line")

    figsize = tuple(spec.get("figsize", [10, 6]))
    dpi = int(spec.get("dpi", 250))

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi, constrained_layout=True)

    title = spec.get("title")
    xlabel = spec.get("xlabel")
    ylabel = spec.get("ylabel")

    if title:
        ax.set_title(str(title))
    if xlabel:
        ax.set_xlabel(str(xlabel))
    if ylabel:
        ax.set_ylabel(str(ylabel))

    grid = spec.get("grid", True)
    ax.grid(bool(grid))

    data_spec = spec.get("data", {})
    data: Dict[str, Any] = {}

    if isinstance(data_spec, dict) and "csv" in data_spec:
        data = {**_load_csv(str(data_spec["csv"]))}
    elif isinstance(data_spec, dict):
        # inline arrays
        data = {k: v for k, v in data_spec.items()}

    series = spec.get("series", []) or []

    if kind in ("line", "scatter"):
        for s in series:
            x = _as_array(s.get("x"), data)
            y = _as_array(s.get("y"), data)
            label = s.get("label")
            color = s.get("color")
            style = s.get("style", "-")
            alpha = s.get("alpha", 1.0)
            lw = s.get("lw", 2.0)
            ms = s.get("ms", 30)

            if kind == "line":
                ax.plot(x, y, style, label=label, color=color, alpha=alpha, linewidth=lw)
            else:
                ax.scatter(x, y, label=label, color=color, alpha=alpha, s=ms)

    elif kind == "hist":
        for s in series:
            x = _as_array(s.get("x"), data)
            label = s.get("label")
            bins = int(s.get("bins", 50))
            alpha = float(s.get("alpha", 0.7))
            ax.hist(x, bins=bins, alpha=alpha, label=label)

    elif kind == "heatmap":
        z = None
        if "z" in data:
            z = np.asarray(data["z"], dtype=float)
        elif "csv" in data_spec:
            # If CSV used: treat as numeric matrix with no headers
            z = np.loadtxt(str(data_spec["csv"]), delimiter=",")
        if z is None:
            raise ValueError("heatmap requires data.z (2D array) or data.csv")

        cmap = spec.get("cmap", "viridis")
        im = ax.imshow(z, aspect="auto", cmap=cmap)
        fig.colorbar(im, ax=ax, shrink=0.85)

    elif kind == "bar":
        # Bar chart: categorical x with numeric y.
        # Supports multiple series:
        # - bar_mode="grouped" (default)
        # - bar_mode="stacked"
        bar_mode = str(spec.get("bar_mode", "grouped")).lower()

        if not series:
            raise ValueError("bar requires non-empty series")

        # x values: take from the first series
        x0_raw = series[0].get("x")
        if isinstance(x0_raw, str):
            if x0_raw not in data:
                raise KeyError(f"Unknown data key/column: {x0_raw}")
            x_vals = list(data[x0_raw])
        else:
            x_vals = list(x0_raw)

        idx = np.arange(len(x_vals), dtype=float)
        ax.set_xticks(idx)
        ax.set_xticklabels([str(v) for v in x_vals])

        # Grouped layout params
        default_total_width = float(spec.get("bar_total_width", 0.8))
        nser = len(series)
        default_width = default_total_width / max(1, nser) if bar_mode == "grouped" else default_total_width

        if bar_mode == "stacked":
            bottom = np.zeros(len(x_vals), dtype=float)
            for s in series:
                # allow per-series x but must match categories length
                y = _as_array(s.get("y"), data)
                if len(y) != len(x_vals):
                    raise ValueError("All bar series must have the same length as x")
                label = s.get("label")
                color = s.get("color")
                alpha = float(s.get("alpha", 0.9))
                width = float(s.get("width", default_width))
                edgecolor = s.get("edgecolor", None)
                ax.bar(idx, y, width=width, bottom=bottom, label=label, color=color, alpha=alpha, edgecolor=edgecolor)
                bottom = bottom + y

        else:  # grouped
            offsets = (np.arange(nser) - (nser - 1) / 2.0) * default_width
            for j, s in enumerate(series):
                y = _as_array(s.get("y"), data)
                if len(y) != len(x_vals):
                    raise ValueError("All bar series must have the same length as x")
                label = s.get("label")
                color = s.get("color")
                alpha = float(s.get("alpha", 0.9))
                width = float(s.get("width", default_width))
                edgecolor = s.get("edgecolor", None)
                ax.bar(idx + offsets[j], y, width=width, label=label, color=color, alpha=alpha, edgecolor=edgecolor)

        # Improve readability for long category labels
        for tick in ax.get_xticklabels():
            tick.set_rotation(int(spec.get("xtick_rotation", 0)))
            tick.set_ha(spec.get("xtick_ha", "center"))

    else:
        raise ValueError(f"Unknown kind: {kind}")

    legend = spec.get("legend", {}) or {}
    show_legend = bool(legend.get("show", True))
    if show_legend and any(s.get("label") for s in series):
        loc = legend.get("loc", "best")
        ax.legend(loc=loc)

    # Final overlap guard
    try:
        fig.tight_layout()
    except Exception:
        pass

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True, help="Path to JSON spec")
    ap.add_argument("--out", required=True, help="Output PNG path")
    args = ap.parse_args()

    _maybe_set_theme()

    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    render(spec, args.out)


if __name__ == "__main__":
    main()
