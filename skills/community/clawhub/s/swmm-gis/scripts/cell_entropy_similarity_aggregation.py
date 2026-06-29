#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np
import rasterio
import shapefile
from rasterio.features import rasterize, shapes

from flowpath_entropy_partition import (
    LANDUSE_PERVIOUSNESS,
    SOIL_DRAINAGE_ABILITY,
    first_shape,
    fuzzy_jaccard,
    rasterize_field,
    read_raster,
    slope_percent_and_classes,
    triangular_mu,
    write_json,
    write_raster,
)


NEIGHBOR_OFFSETS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1), (0, 1),
    (1, -1), (1, 0), (1, 1),
]


def local_normalized_joint_entropy(triples: np.ndarray, valid: np.ndarray, radius: int) -> np.ndarray:
    out = np.full(valid.shape, np.nan, dtype="float64")
    nrows, ncols = valid.shape
    for r, c in np.argwhere(valid):
        r0 = max(0, int(r) - radius)
        r1 = min(nrows, int(r) + radius + 1)
        c0 = max(0, int(c) - radius)
        c1 = min(ncols, int(c) + radius + 1)
        window_valid = valid[r0:r1, c0:c1]
        window_triples = triples[r0:r1, c0:c1][window_valid]
        counts = Counter(tuple(int(v) for v in row) for row in window_triples if np.all(row > 0))
        if not counts:
            continue
        values = np.asarray(list(counts.values()), dtype="float64")
        probs = values / values.sum()
        entropy = -float(np.sum(probs * np.log(probs)))
        out[r, c] = 0.0 if len(counts) == 1 else entropy / math.log(len(counts))
    return out


def neighbor_fuzzy_similarity(membership: np.ndarray, valid: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    mean_similarity = np.full(valid.shape, np.nan, dtype="float64")
    min_similarity = np.full(valid.shape, np.nan, dtype="float64")
    weights = np.array([1 / 3, 1 / 3, 1 / 3], dtype="float64")
    nrows, ncols = valid.shape
    for r, c in np.argwhere(valid):
        vals = []
        for dr, dc in NEIGHBOR_OFFSETS:
            nr, nc = int(r + dr), int(c + dc)
            if 0 <= nr < nrows and 0 <= nc < ncols and valid[nr, nc]:
                sim = fuzzy_jaccard(membership[r, c], membership[nr, nc], weights)
                if np.isfinite(sim):
                    vals.append(sim)
        if vals:
            mean_similarity[r, c] = float(np.mean(vals))
            min_similarity[r, c] = float(np.min(vals))
    return mean_similarity, min_similarity


def classify_cells(
    local_nwje: np.ndarray,
    mean_similarity: np.ndarray,
    valid: np.ndarray,
    *,
    entropy_threshold: float,
    similarity_threshold: float,
    lump_entropy_threshold: float,
    lump_similarity_threshold: float,
) -> np.ndarray:
    labels = np.zeros(valid.shape, dtype="int32")
    preserve = valid & (local_nwje >= entropy_threshold) & (mean_similarity <= similarity_threshold)
    lumpable = valid & ((local_nwje <= lump_entropy_threshold) | (mean_similarity >= lump_similarity_threshold))
    uncertain = valid & ~(preserve | lumpable)
    labels[lumpable] = 1
    labels[uncertain] = 2
    labels[preserve] = 3
    return labels


def write_polygons(path: Path, labels: np.ndarray, template_meta: dict[str, Any]) -> None:
    features = []
    transform = template_meta["transform"]
    label_names = {1: "lumpable", 2: "transitional", 3: "preserve_discrete"}
    for geom, value in shapes(labels.astype("int16"), mask=labels > 0, transform=transform):
        label = int(value)
        features.append(
            {
                "type": "Feature",
                "properties": {"class_id": label, "aggregation_class": label_names.get(label, "unknown")},
                "geometry": geom,
            }
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"type": "FeatureCollection", "features": features}, indent=2), encoding="utf-8")


def write_summary_csv(path: Path, labels: np.ndarray, local_nwje: np.ndarray, mean_similarity: np.ndarray, valid: np.ndarray) -> None:
    rows = []
    names = {1: "lumpable", 2: "transitional", 3: "preserve_discrete"}
    for label, name in names.items():
        mask = valid & (labels == label)
        rows.append(
            {
                "class_id": label,
                "aggregation_class": name,
                "cell_count": int(np.sum(mask)),
                "mean_local_nwje": float(np.nanmean(local_nwje[mask])) if np.any(mask) else None,
                "mean_neighbor_wfjs": float(np.nanmean(mean_similarity[mask])) if np.any(mask) else None,
            }
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Infer local cell-level lump/preserve relations from entropy and fuzzy similarity without flow routing.")
    parser.add_argument("--dem", type=Path, required=True)
    parser.add_argument("--boundary-shp", type=Path, required=True)
    parser.add_argument("--landuse-shp", type=Path, required=True)
    parser.add_argument("--soil-shp", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--landuse-field", default="CLASS")
    parser.add_argument("--soil-field", default="DRAIN_1")
    parser.add_argument("--window-radius", type=int, default=1)
    parser.add_argument("--slope-bins", type=int, default=5)
    parser.add_argument("--entropy-threshold", type=float, default=0.70)
    parser.add_argument("--similarity-threshold", type=float, default=0.80)
    parser.add_argument("--lump-entropy-threshold", type=float, default=0.35)
    parser.add_argument("--lump-similarity-threshold", type=float, default=0.92)
    args = parser.parse_args()

    dem, meta = read_raster(args.dem)
    boundary_geom, _record = first_shape(args.boundary_shp)
    boundary = rasterize(
        [(boundary_geom, 1)],
        out_shape=meta["shape"],
        transform=meta["transform"],
        fill=0,
        all_touched=True,
        dtype="uint8",
    ).astype(bool)
    valid = boundary & np.isfinite(dem)
    cell_size = float(abs(meta["res"][0]))
    slope_pct, slope_class, slope_bins = slope_percent_and_classes(dem, cell_size, valid, args.slope_bins)
    land_class, land_numeric, land_codes, land_values = rasterize_field(
        args.landuse_shp,
        field=args.landuse_field,
        out_shape=meta["shape"],
        transform=meta["transform"],
        mapping=LANDUSE_PERVIOUSNESS,
    )
    soil_class, soil_numeric, soil_codes, soil_values = rasterize_field(
        args.soil_shp,
        field=args.soil_field,
        out_shape=meta["shape"],
        transform=meta["transform"],
        mapping=SOIL_DRAINAGE_ABILITY,
    )
    valid &= (land_class > 0) & (soil_class > 0) & (slope_class > 0)
    triples = np.dstack([soil_class, land_class, slope_class]).astype("int32")
    mu_soil = triangular_mu(soil_numeric, valid & (soil_numeric > 0))
    mu_land = triangular_mu(land_numeric, valid & (land_numeric > 0))
    mu_slope = triangular_mu(slope_pct, valid & np.isfinite(slope_pct))
    membership = np.dstack([mu_soil, mu_land, mu_slope])

    local_nwje = local_normalized_joint_entropy(triples, valid, max(1, args.window_radius))
    mean_similarity, min_similarity = neighbor_fuzzy_similarity(membership, valid)
    labels = classify_cells(
        local_nwje,
        mean_similarity,
        valid,
        entropy_threshold=args.entropy_threshold,
        similarity_threshold=args.similarity_threshold,
        lump_entropy_threshold=args.lump_entropy_threshold,
        lump_similarity_threshold=args.lump_similarity_threshold,
    )

    out_dir = args.out_dir
    write_raster(out_dir / "cell_local_nwje.tif", local_nwje, meta)
    write_raster(out_dir / "cell_neighbor_wfjs_mean.tif", mean_similarity, meta)
    write_raster(out_dir / "cell_neighbor_wfjs_min.tif", min_similarity, meta)
    write_raster(out_dir / "cell_entropy_similarity_aggregation.tif", labels.astype("float32"), meta)
    write_polygons(out_dir / "cell_entropy_similarity_aggregation.geojson", labels, meta)
    write_summary_csv(out_dir / "cell_entropy_similarity_summary.csv", labels, local_nwje, mean_similarity, valid)

    summary = {
        "ok": True,
        "generated_by": "cell_entropy_similarity_aggregation",
        "method_boundary": "Local cell-neighborhood entropy and adjacency fuzzy similarity; no flow accumulation, D8 routing, or upstream contributing area is used.",
        "inputs": {
            "dem": str(args.dem),
            "boundary": str(args.boundary_shp),
            "landuse": str(args.landuse_shp),
            "soil": str(args.soil_shp),
            "landuse_field": args.landuse_field,
            "soil_field": args.soil_field,
        },
        "parameters": {
            "window_radius": args.window_radius,
            "slope_bins": args.slope_bins,
            "entropy_threshold": args.entropy_threshold,
            "similarity_threshold": args.similarity_threshold,
            "lump_entropy_threshold": args.lump_entropy_threshold,
            "lump_similarity_threshold": args.lump_similarity_threshold,
        },
        "class_counts": {
            "lumpable": int(np.sum(labels == 1)),
            "transitional": int(np.sum(labels == 2)),
            "preserve_discrete": int(np.sum(labels == 3)),
        },
        "outputs": {
            "local_nwje": str(out_dir / "cell_local_nwje.tif"),
            "mean_neighbor_wfjs": str(out_dir / "cell_neighbor_wfjs_mean.tif"),
            "min_neighbor_wfjs": str(out_dir / "cell_neighbor_wfjs_min.tif"),
            "aggregation_raster": str(out_dir / "cell_entropy_similarity_aggregation.tif"),
            "aggregation_geojson": str(out_dir / "cell_entropy_similarity_aggregation.geojson"),
            "summary_csv": str(out_dir / "cell_entropy_similarity_summary.csv"),
        },
        "code_maps": {
            "1": "lumpable",
            "2": "transitional",
            "3": "preserve_discrete",
        },
        "landuse_codes": land_codes,
        "landuse_perviousness": land_values,
        "soil_codes": soil_codes,
        "soil_drainage_ability": soil_values,
        "slope_bins": slope_bins,
    }
    write_json(out_dir / "cell_entropy_similarity_summary.json", summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
