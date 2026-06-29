#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np
import rasterio
import shapefile
from rasterio.features import rasterize, shapes
from rasterio.transform import xy


GRASS_DRAINAGE_OFFSETS = {
    1: (-1, 1),
    2: (-1, 0),
    3: (-1, -1),
    4: (0, -1),
    5: (1, -1),
    6: (1, 0),
    7: (1, 1),
    8: (0, 1),
}

LANDUSE_PERVIOUSNESS = {
    "Commercial": 0.20,
    "Public": 0.45,
    "Recreation and Open Space": 0.75,
    "Rural": 0.85,
    "Natural Park Zone": 0.95,
}

SOIL_DRAINAGE_ABILITY = {
    "-": 0.00,
    "VP": 0.10,
    "P": 0.25,
    "I": 0.45,
    "MW": 0.70,
    "W": 0.90,
    "R": 1.00,
}


def read_raster(path: Path) -> tuple[np.ndarray, dict[str, Any]]:
    with rasterio.open(path) as ds:
        arr = ds.read(1, masked=True).astype("float64").filled(np.nan)
        meta = ds.meta.copy()
        meta.update(transform=ds.transform, crs=ds.crs, shape=ds.shape, res=ds.res)
    return arr, meta


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True), encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    fields = fields or ["id"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_raster(path: Path, values: np.ndarray, template_meta: dict[str, Any], *, dtype: str = "float32") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    meta = dict(template_meta)
    meta.update(count=1, dtype=dtype, nodata=-9999.0 if dtype.startswith("float") else 0)
    out = values.astype(dtype, copy=True)
    if dtype.startswith("float"):
        out = np.where(np.isfinite(out), out, -9999.0).astype(dtype)
    with rasterio.open(path, "w", **{k: v for k, v in meta.items() if k not in {"shape", "res"}}) as ds:
        ds.write(out, 1)


def first_shape(path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    reader = shapefile.Reader(str(path))
    fields = [field[0] for field in reader.fields[1:]]
    return reader.shape(0).__geo_interface__, dict(zip(fields, reader.record(0)))


def rasterize_field(
    path: Path,
    *,
    field: str,
    out_shape: tuple[int, int],
    transform: rasterio.Affine,
    mapping: dict[str, float] | None = None,
) -> tuple[np.ndarray, np.ndarray, dict[str, int], dict[int, float]]:
    reader = shapefile.Reader(str(path))
    fields = [f[0] for f in reader.fields[1:]]
    if field not in fields:
        raise ValueError(f"Field '{field}' not found in {path}")
    idx = fields.index(field)
    codes: dict[str, int] = {}
    numeric_values: dict[str, float] = {}
    feats = []
    next_code = 1
    for shape_record in reader.iterShapeRecords():
        value = str(shape_record.record[idx] or "").strip() or "UNKNOWN"
        if value not in codes:
            codes[value] = next_code
            next_code += 1
            numeric_values[value] = float(mapping[value]) if mapping and value in mapping else float(codes[value])
        feats.append((shape_record.shape.__geo_interface__, codes[value]))
    categorical = rasterize(feats, out_shape=out_shape, transform=transform, fill=0, all_touched=True, dtype="int32")
    value_by_code = {code: numeric_values[value] for value, code in codes.items()}
    numeric = np.zeros(out_shape, dtype="float64")
    for code, value in value_by_code.items():
        numeric[categorical == code] = value
    return categorical, numeric, codes, value_by_code


def slope_percent_and_classes(dem: np.ndarray, cell_size_m: float, boundary: np.ndarray, bins: int) -> tuple[np.ndarray, np.ndarray, list[float]]:
    gy, gx = np.gradient(dem.astype(float), cell_size_m, cell_size_m)
    slope_pct = np.sqrt(gx * gx + gy * gy) * 100.0
    valid = boundary & np.isfinite(slope_pct)
    quantiles = np.quantile(slope_pct[valid], np.linspace(0, 1, bins + 1)) if np.any(valid) else np.arange(bins + 1)
    quantiles = np.unique(quantiles)
    classes = np.zeros(dem.shape, dtype="int32")
    if quantiles.size > 1:
        classes[valid] = np.digitize(slope_pct[valid], quantiles[1:-1], right=True) + 1
    return slope_pct, classes, [float(v) for v in quantiles]


def triangular_mu(values: np.ndarray, valid: np.ndarray) -> np.ndarray:
    out = np.full(values.shape, np.nan, dtype="float64")
    if not np.any(valid):
        return out
    lo = float(np.nanmin(values[valid]))
    hi = float(np.nanmax(values[valid]))
    if hi == lo:
        out[valid] = 1.0
        return out
    vals = values[valid]
    peak = float(np.nanmean(vals))
    left = vals <= peak
    mu = np.empty(vals.shape, dtype="float64")
    mu[left] = (vals[left] - lo) / max(1e-12, peak - lo)
    mu[~left] = (hi - vals[~left]) / max(1e-12, hi - peak)
    out[valid] = np.clip(mu, 0.0, 1.0)
    return out


def fuzzy_jaccard(u: np.ndarray, v: np.ndarray, weights: np.ndarray) -> float:
    mask = np.isfinite(u) & np.isfinite(v)
    if not np.any(mask):
        return float("nan")
    numerator = float(np.sum(weights[mask] * np.minimum(u[mask], v[mask])))
    denominator = float(np.sum(weights[mask] * np.maximum(u[mask], v[mask])))
    return 0.0 if denominator <= 0 else numerator / denominator


class GrassFlowGraph:
    def __init__(self, drainage: np.ndarray, valid: np.ndarray) -> None:
        self.drainage = drainage
        self.valid = valid
        self.nrows, self.ncols = drainage.shape
        self.next_cell: dict[tuple[int, int], tuple[int, int] | None] = {}
        self.inflows: dict[tuple[int, int], list[tuple[int, int]]] = defaultdict(list)
        self._build()

    def is_valid(self, r: int, c: int) -> bool:
        return 0 <= r < self.nrows and 0 <= c < self.ncols and self.valid[r, c] and np.isfinite(self.drainage[r, c])

    def _build(self) -> None:
        for r, c in np.argwhere(self.valid & np.isfinite(self.drainage)):
            code = int(abs(self.drainage[r, c]))
            offset = GRASS_DRAINAGE_OFFSETS.get(code)
            cell = (int(r), int(c))
            nxt = None
            if offset is not None:
                nr, nc = int(r + offset[0]), int(c + offset[1])
                if self.is_valid(nr, nc):
                    nxt = (nr, nc)
                    self.inflows[nxt].append(cell)
            self.next_cell[cell] = nxt

    def upstream_cells(self, outlet: tuple[int, int]) -> set[tuple[int, int]]:
        seen: set[tuple[int, int]] = set()
        stack = [outlet]
        while stack:
            cell = stack.pop()
            if cell in seen:
                continue
            seen.add(cell)
            stack.extend(self.inflows.get(cell, []))
        return seen


def upstream_metrics(
    graph: GrassFlowGraph,
    cells: set[tuple[int, int]],
    triples: np.ndarray,
    membership: np.ndarray,
    flow_acc: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    wje = np.full(graph.drainage.shape, np.nan, dtype="float64")
    nwje = np.full(graph.drainage.shape, np.nan, dtype="float64")
    counts = np.zeros(graph.drainage.shape, dtype="float64")
    mu_sum = np.zeros((*graph.drainage.shape, 3), dtype="float64")
    mu_avg = np.full((*graph.drainage.shape, 3), np.nan, dtype="float64")
    bags: dict[tuple[int, int], Counter] = {cell: Counter() for cell in cells}
    ordered = sorted(cells, key=lambda cell: float(flow_acc[cell]) if np.isfinite(flow_acc[cell]) else 0.0)
    for cell in ordered:
        r, c = cell
        current = bags[cell]
        triple = tuple(int(v) for v in triples[r, c])
        if all(v > 0 for v in triple):
            current[triple] += 1
        if np.all(np.isfinite(membership[r, c])):
            mu_sum[r, c] += membership[r, c]
            counts[r, c] += 1.0
        values = np.asarray(list(current.values()), dtype="float64")
        if values.size:
            p = values / values.sum()
            h = -float(np.sum(p * np.log(p)))
            wje[r, c] = h
            nwje[r, c] = 0.0 if values.size == 1 else h / math.log(values.size)
        if counts[r, c] > 0:
            mu_avg[r, c] = mu_sum[r, c] / counts[r, c]
        downstream = graph.next_cell.get(cell)
        if downstream in bags:
            bags[downstream] += current
            dr, dc = downstream
            mu_sum[dr, dc] += mu_sum[r, c]
            counts[dr, dc] += counts[r, c]
    return wje, nwje, counts, mu_sum, mu_avg


def longest_flowpath(graph: GrassFlowGraph, cells: set[tuple[int, int]], outlet: tuple[int, int], flow_acc: np.ndarray) -> list[tuple[int, int]]:
    ordered = sorted(cells, key=lambda cell: float(flow_acc[cell]) if np.isfinite(flow_acc[cell]) else 0.0)
    length: dict[tuple[int, int], int] = {}
    upstream_parent: dict[tuple[int, int], tuple[int, int] | None] = {}
    for cell in ordered:
        best_child = None
        best_len = 0
        for child in graph.inflows.get(cell, []):
            if child in cells and length.get(child, 0) > best_len:
                best_child = child
                best_len = length[child]
        length[cell] = best_len + 1
        upstream_parent[cell] = best_child
    path = []
    cur: tuple[int, int] | None = outlet
    seen: set[tuple[int, int]] = set()
    while cur is not None and cur not in seen:
        seen.add(cur)
        path.append(cur)
        cur = upstream_parent.get(cur)
    return list(reversed(path))


def choose_split_points(
    path: list[tuple[int, int]],
    nwje: np.ndarray,
    mu_avg: np.ndarray,
    graph: GrassFlowGraph,
    flow_acc: np.ndarray,
    transform: rasterio.Affine,
    *,
    min_spacing_cells: int,
    target_count: int,
    delta_quantile: float,
    dissim_quantile: float,
    paper_delta_threshold: float,
    paper_similarity_threshold: float,
    paper_only_splits: bool,
) -> tuple[list[dict[str, Any]], dict[tuple[int, int], dict[str, Any]]]:
    weights = np.array([1 / 3, 1 / 3, 1 / 3], dtype="float64")
    outlet = path[-1]
    outlet_mu = mu_avg[outlet]
    rows: list[dict[str, Any]] = []
    delta_values = []
    dissim_values = []
    for idx, cell in enumerate(path):
        r, c = cell
        x_coord, y_coord = xy(transform, r, c, offset="center")
        if idx == 0:
            delta_seq = 0.0
            wfjs_seq = 1.0
        else:
            pr, pc = path[idx - 1]
            delta_seq = float(nwje[pr, pc] - nwje[r, c]) if np.isfinite(nwje[pr, pc]) and np.isfinite(nwje[r, c]) else float("nan")
            wfjs_seq = fuzzy_jaccard(mu_avg[pr, pc], mu_avg[r, c], weights)
        wfjs_out = fuzzy_jaccard(mu_avg[r, c], outlet_mu, weights)
        delta_out = float(nwje[r, c] - nwje[outlet]) if np.isfinite(nwje[r, c]) and np.isfinite(nwje[outlet]) else float("nan")
        junction = 1 if len([child for child in graph.inflows.get(cell, []) if child in graph.next_cell]) >= 2 else 0
        row = {
            "path_index": idx + 1,
            "row": r,
            "col": c,
            "x": float(x_coord),
            "y": float(y_coord),
            "flow_accumulation": float(flow_acc[r, c]) if np.isfinite(flow_acc[r, c]) else None,
            "NWJE": float(nwje[r, c]) if np.isfinite(nwje[r, c]) else None,
            "delta_NWJE_seq": delta_seq if np.isfinite(delta_seq) else None,
            "delta_NWJE_outlet": delta_out if np.isfinite(delta_out) else None,
            "WFJS_seq": wfjs_seq if np.isfinite(wfjs_seq) else None,
            "WFJS_outlet": wfjs_out if np.isfinite(wfjs_out) else None,
            "stream_junction": junction,
        }
        rows.append(row)
        if idx > 0 and np.isfinite(delta_seq):
            delta_values.append(abs(delta_seq))
        if idx > 0 and np.isfinite(wfjs_seq):
            dissim_values.append(1.0 - wfjs_seq)
    delta_thr = float(np.quantile(delta_values, delta_quantile)) if delta_values else float("inf")
    dissim_thr = float(np.quantile(dissim_values, dissim_quantile)) if dissim_values else float("inf")

    ranked: list[tuple[float, int]] = []
    for idx, row in enumerate(rows[1:-1], start=1):
        d = abs(float(row["delta_NWJE_seq"] or 0.0))
        s = 1.0 - float(row["WFJS_seq"] or 1.0)
        j = float(row["stream_junction"])
        acc = float(row["flow_accumulation"] or 0.0)
        acc_term = math.log1p(max(0.0, acc)) / 12.0
        score = 0.45 * d + 0.35 * s + 0.15 * j + 0.05 * acc_term
        paper_preserve = d >= paper_delta_threshold and float(row["WFJS_seq"] or 1.0) <= paper_similarity_threshold
        paper_lump = d <= paper_delta_threshold and float(row["WFJS_seq"] or 0.0) >= paper_similarity_threshold
        row["split_score"] = round(score, 6)
        row["paper_preserve_heterogeneity"] = paper_preserve
        row["paper_hp_rea_lump_interval"] = paper_lump
        row["split_trigger"] = bool(paper_preserve or d >= delta_thr or s >= dissim_thr or j > 0)
        if row["split_trigger"]:
            ranked.append((score + (1.0 if paper_preserve else 0.0), idx))

    selected_indices: list[int] = []
    preserve_ranked = [(score, idx) for score, idx in ranked if rows[idx].get("paper_preserve_heterogeneity")]
    secondary_ranked = [
        (score, idx)
        for score, idx in ranked
        if not rows[idx].get("paper_preserve_heterogeneity") and not rows[idx].get("paper_hp_rea_lump_interval")
    ]
    for _score, idx in sorted(preserve_ranked, reverse=True):
        if all(abs(idx - prev) >= min_spacing_cells for prev in selected_indices):
            selected_indices.append(idx)
    if not paper_only_splits:
        for _score, idx in sorted(secondary_ranked, reverse=True):
            if target_count and len(selected_indices) >= max(0, target_count - 1):
                break
            if all(abs(idx - prev) >= min_spacing_cells for prev in selected_indices):
                selected_indices.append(idx)
    selected_indices.sort()
    for idx in selected_indices:
        rows[idx]["selected_split"] = True
    selected = {path[idx]: rows[idx] for idx in selected_indices}
    return rows, selected
def assign_path_segments(
    graph: GrassFlowGraph,
    cells: set[tuple[int, int]],
    outlet: tuple[int, int],
    path: list[tuple[int, int]],
    selected_splits: dict[tuple[int, int], dict[str, Any]],
) -> tuple[np.ndarray, dict[int, dict[str, Any]]]:
    split_indices = [idx for idx, cell in enumerate(path) if cell in selected_splits]
    breakpoints = [0, *split_indices, len(path) - 1]
    segment_by_path_cell: dict[tuple[int, int], int] = {}
    for seg_idx in range(1, len(breakpoints)):
        start = breakpoints[seg_idx - 1]
        end = breakpoints[seg_idx]
        for idx in range(start, end + 1):
            segment_by_path_cell[path[idx]] = seg_idx
    labels = np.zeros(graph.drainage.shape, dtype="int32")
    nearest_path_segment: dict[tuple[int, int], int] = {}
    path_set = set(path)
    for cell in cells:
        cur = cell
        seen = set()
        while cur not in path_set and cur not in seen:
            seen.add(cur)
            nxt = graph.next_cell.get(cur)
            if nxt is None:
                break
            cur = nxt
        nearest_path_segment[cell] = segment_by_path_cell.get(cur, len(breakpoints) - 1)
    for (r, c), seg_id in nearest_path_segment.items():
        labels[r, c] = int(seg_id)
    metrics = {seg_id: {"segment_id": f"E{seg_id}"} for seg_id in sorted(set(nearest_path_segment.values()))}
    return labels, metrics


def polygonize(labels: np.ndarray, template_meta: dict[str, Any], out_path: Path, metrics: dict[int, dict[str, Any]]) -> None:
    features = []
    for geom, value in shapes(labels.astype("int32"), mask=labels > 0, transform=template_meta["transform"]):
        label = int(value)
        features.append({"type": "Feature", "properties": metrics.get(label, {"segment_id": f"E{label}"}), "geometry": geom})
    crs = template_meta["crs"]
    fc = {
        "type": "FeatureCollection",
        "name": out_path.stem,
        "crs": {"type": "name", "properties": {"name": crs.to_string() if crs else ""}},
        "features": features,
    }
    write_json(out_path, fc)


def point_geojson(rows: list[dict[str, Any]], transform: rasterio.Affine, out_path: Path, crs: Any) -> None:
    features = []
    for row in rows:
        if not row.get("selected_split"):
            continue
        x, y = xy(transform, int(row["row"]), int(row["col"]), offset="center")
        props = dict(row)
        props["x"] = float(x)
        props["y"] = float(y)
        features.append({"type": "Feature", "properties": props, "geometry": {"type": "Point", "coordinates": [float(x), float(y)]}})
    fc = {
        "type": "FeatureCollection",
        "name": out_path.stem,
        "crs": {"type": "name", "properties": {"name": crs.to_string() if crs else ""}},
        "features": features,
    }
    write_json(out_path, fc)


def segment_metrics(
    labels: np.ndarray,
    *,
    nwje: np.ndarray,
    wje: np.ndarray,
    wfjs_outlet: np.ndarray,
    flow_acc: np.ndarray,
    cell_area_ha: float,
) -> dict[int, dict[str, Any]]:
    metrics: dict[int, dict[str, Any]] = {}
    for label in sorted(int(v) for v in np.unique(labels) if v > 0):
        mask = labels == label
        metrics[label] = {
            "segment_id": f"E{label}",
            "cell_count": int(np.sum(mask)),
            "area_ha": round(float(np.sum(mask) * cell_area_ha), 6),
            "mean_WJE": round(float(np.nanmean(wje[mask])), 6),
            "mean_NWJE": round(float(np.nanmean(nwje[mask])), 6),
            "max_NWJE": round(float(np.nanmax(nwje[mask])), 6),
            "mean_WFJS_outlet": round(float(np.nanmean(wfjs_outlet[mask])), 6),
            "max_flow_accumulation": round(float(np.nanmax(flow_acc[mask])), 6),
        }
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser(description="Paper-consistent WJE/NWJE/WFJS flowpath split-lump subcatchment partition.")
    parser.add_argument("--dem", type=Path, required=True)
    parser.add_argument("--boundary-shp", type=Path, required=True)
    parser.add_argument("--landuse-shp", type=Path, required=True)
    parser.add_argument("--soil-shp", type=Path, required=True)
    parser.add_argument("--flow-accumulation", type=Path, required=True)
    parser.add_argument("--drainage-direction", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--slope-bins", type=int, default=5)
    parser.add_argument("--target-subcatchments", type=int, default=40)
    parser.add_argument("--min-split-spacing-cells", type=int, default=4)
    parser.add_argument("--delta-quantile", type=float, default=0.80)
    parser.add_argument("--dissimilarity-quantile", type=float, default=0.80)
    parser.add_argument("--paper-delta-threshold", type=float, default=0.015)
    parser.add_argument("--paper-similarity-threshold", type=float, default=0.95)
    parser.add_argument(
        "--paper-only-splits",
        action="store_true",
        help="Use only the paper preserve rule as split points; ignore secondary engineering split triggers.",
    )
    args = parser.parse_args()

    dem, meta = read_raster(args.dem)
    flow_acc, _ = read_raster(args.flow_accumulation)
    drainage, _ = read_raster(args.drainage_direction)
    boundary_geom, boundary_record = first_shape(args.boundary_shp)
    boundary = rasterize([(boundary_geom, 1)], out_shape=meta["shape"], transform=meta["transform"], fill=0, all_touched=True, dtype="uint8").astype(bool)
    valid = boundary & np.isfinite(dem) & np.isfinite(flow_acc) & np.isfinite(drainage)

    land_class, land_numeric, land_codes, land_values = rasterize_field(
        args.landuse_shp,
        field="CLASS",
        out_shape=meta["shape"],
        transform=meta["transform"],
        mapping=LANDUSE_PERVIOUSNESS,
    )
    soil_class, soil_numeric, soil_codes, soil_values = rasterize_field(
        args.soil_shp,
        field="DRAIN_1",
        out_shape=meta["shape"],
        transform=meta["transform"],
        mapping=SOIL_DRAINAGE_ABILITY,
    )
    slope_pct, slope_class, slope_bins = slope_percent_and_classes(dem, abs(float(meta["res"][0])), valid, args.slope_bins)
    triples = np.dstack([soil_class, land_class, slope_class]).astype("int32")

    mu_slope = triangular_mu(slope_pct, valid)
    mu_land = triangular_mu(land_numeric, valid & (land_numeric > 0))
    mu_soil = triangular_mu(soil_numeric, valid & (soil_numeric > 0))
    membership = np.dstack([mu_soil, mu_land, mu_slope])

    graph = GrassFlowGraph(drainage, valid)
    outlet = tuple(int(v) for v in np.argwhere(valid & (flow_acc == np.nanmax(np.where(valid, flow_acc, np.nan))))[0])
    contributing = graph.upstream_cells(outlet)
    wje, nwje, upstream_count, _mu_sum, mu_avg = upstream_metrics(graph, contributing, triples, membership, flow_acc)
    path = longest_flowpath(graph, contributing, outlet, flow_acc)
    path_rows, selected_splits = choose_split_points(
        path,
        nwje,
        mu_avg,
        graph,
        flow_acc,
        meta["transform"],
        min_spacing_cells=args.min_split_spacing_cells,
        target_count=args.target_subcatchments,
        delta_quantile=args.delta_quantile,
        dissim_quantile=args.dissimilarity_quantile,
        paper_delta_threshold=args.paper_delta_threshold,
        paper_similarity_threshold=args.paper_similarity_threshold,
        paper_only_splits=args.paper_only_splits,
    )

    weights = np.array([1 / 3, 1 / 3, 1 / 3], dtype="float64")
    wfjs_outlet = np.full(flow_acc.shape, np.nan, dtype="float64")
    outlet_mu = mu_avg[outlet]
    for r, c in contributing:
        wfjs_outlet[r, c] = fuzzy_jaccard(mu_avg[r, c], outlet_mu, weights)
    labels, _ = assign_path_segments(graph, contributing, outlet, path, selected_splits)
    metrics = segment_metrics(
        labels,
        nwje=nwje,
        wje=wje,
        wfjs_outlet=wfjs_outlet,
        flow_acc=flow_acc,
        cell_area_ha=abs(float(meta["res"][0]) * float(meta["res"][1])) / 10000.0,
    )

    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_raster(args.out_dir / "watershed_joint_entropy.tif", wje, meta)
    write_raster(args.out_dir / "normalized_watershed_joint_entropy.tif", nwje, meta)
    write_raster(args.out_dir / "upstream_contributing_cell_count.tif", upstream_count, meta)
    write_raster(args.out_dir / "wfjs_to_outlet.tif", wfjs_outlet, meta)
    write_raster(args.out_dir / "paper_entropy_partition_labels.tif", labels, meta, dtype="int32")
    polygonize(labels, meta, args.out_dir / "paper_entropy_partition.geojson", metrics)
    point_geojson(path_rows, meta["transform"], args.out_dir / "selected_split_points.geojson", meta["crs"])
    write_csv(args.out_dir / "longest_flowpath_metrics.csv", path_rows)
    write_json(
        args.out_dir / "paper_entropy_partition_summary.json",
        {
            "ok": True,
            "method": "Paper-consistent WJE/NWJE over U(g), upstream-averaged fuzzy memberships, pathwise WFJS, delta NWJE, and split/lump segmentation along the longest D8 flow path.",
            "boundary_record": {k: boundary_record.get(k) for k in ["NAME", "OUTLET", "AREA", "WIDTH", "SLOPE"]},
            "outlet_cell": {"row": outlet[0], "col": outlet[1], "flow_accumulation": float(flow_acc[outlet])},
            "contributing_cell_count": len(contributing),
            "longest_flowpath_cell_count": len(path),
            "selected_split_count": len(selected_splits),
            "final_subcatchment_count": len(metrics),
            "parameters": {
                "target_subcatchments": args.target_subcatchments,
                "min_split_spacing_cells": args.min_split_spacing_cells,
                "delta_quantile": args.delta_quantile,
                "dissimilarity_quantile": args.dissimilarity_quantile,
                "paper_delta_threshold": args.paper_delta_threshold,
                "paper_similarity_threshold": args.paper_similarity_threshold,
                "paper_only_splits": args.paper_only_splits,
                "split_score": "0.45*abs(delta_NWJE_seq)+0.35*(1-WFJS_seq)+0.15*stream_junction+0.05*log1p(flow_accumulation)/12",
                "paper_preserve_rule": f"preserve/split when abs(delta_NWJE_seq) >= {args.paper_delta_threshold} and WFJS_seq <= {args.paper_similarity_threshold}",
                "paper_lump_rule": f"safe lump interval when abs(delta_NWJE_seq) <= {args.paper_delta_threshold} and WFJS_seq >= {args.paper_similarity_threshold}",
            },
            "landuse_codes": land_codes,
            "landuse_perviousness": land_values,
            "soil_codes": soil_codes,
            "soil_drainage_ability": soil_values,
            "slope_bins_pct": slope_bins,
            "outputs": {
                "partition_geojson": str(args.out_dir / "paper_entropy_partition.geojson"),
                "split_points_geojson": str(args.out_dir / "selected_split_points.geojson"),
                "path_metrics_csv": str(args.out_dir / "longest_flowpath_metrics.csv"),
            },
            "segment_metrics": metrics,
        },
    )
    print(json.dumps({"ok": True, "out_dir": str(args.out_dir), "final_subcatchment_count": len(metrics), "selected_split_count": len(selected_splits)}, indent=2))


if __name__ == "__main__":
    main()
