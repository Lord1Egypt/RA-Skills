#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[3]
FLOWPATH_SCRIPT = Path(__file__).resolve().with_name("flowpath_entropy_partition.py")
PLOT_SCRIPT = Path(__file__).resolve().with_name("plot_entropy_threshold_sensitivity.py")
QGIS_PREP_SCRIPT = Path(__file__).resolve().with_name("qgis_prepare_swmm_inputs.py")

DEFAULT_QGIS_PROCESS = "/Applications/QGIS-final-4_0_2.app/Contents/MacOS/qgis_process"
DEFAULT_PROJ_LIB = "/Applications/QGIS-final-4_0_2.app/Contents/Resources/qgis/proj"
DEFAULT_GISBASE = "/Applications/GRASS-8.4.app/Contents/Resources"

PAPER_VARIANTS = [
    ("baseline_paperonly", 0.015, 0.95),
    ("fine_delta", 0.010, 0.95),
    ("fine_similarity", 0.015, 0.97),
    ("fine_both", 0.010, 0.97),
    ("very_fine", 0.008, 0.98),
]


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True), encoding="utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_inventory(paths: dict[str, Path]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for name, path in paths.items():
        out[name] = {
            "path": str(path),
            "exists": path.exists(),
            "size_bytes": path.stat().st_size if path.exists() and path.is_file() else None,
            "sha256": sha256_file(path) if path.exists() and path.is_file() else None,
        }
    return out


def run_command(cmd: list[str], *, env: dict[str, str] | None, cwd: Path, audit: list[dict[str, Any]]) -> str:
    started = datetime.now(timezone.utc).isoformat()
    proc = subprocess.run(cmd, cwd=str(cwd), env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    record = {
        "cmd": cmd,
        "started_at_utc": started,
        "finished_at_utc": datetime.now(timezone.utc).isoformat(),
        "returncode": proc.returncode,
        "stdout_tail": proc.stdout[-4000:],
        "stderr_tail": proc.stderr[-4000:],
    }
    audit.append(record)
    if proc.returncode != 0:
        raise RuntimeError(f"Command failed rc={proc.returncode}: {' '.join(cmd)}\n{proc.stderr}")
    return proc.stdout


def qgis_env(args: argparse.Namespace) -> dict[str, str]:
    env = os.environ.copy()
    if args.proj_lib:
        env["PROJ_LIB"] = str(args.proj_lib)
    if args.gisbase:
        env["GISBASE"] = str(args.gisbase)
    return env


def qgis_version(qgis_process: Path, env: dict[str, str], audit: list[dict[str, Any]], cwd: Path) -> str:
    try:
        stdout = run_command([str(qgis_process), "--version"], env=env, cwd=cwd, audit=audit)
        return stdout.strip()
    except Exception as exc:  # pragma: no cover - version is best-effort audit metadata
        return f"unavailable: {exc}"


def grass_version(gisbase: Path | None) -> str:
    candidate = Path("/Applications/GRASS-8.4.app/Contents/Resources/bin/grass")
    if gisbase:
        candidate = Path(gisbase) / "bin" / "grass"
    if not candidate.exists():
        return "unavailable"
    proc = subprocess.run([str(candidate), "--version"], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return (proc.stdout or proc.stderr).strip().splitlines()[0] if proc.returncode == 0 else "unavailable"


def run_qgis_watershed(
    *,
    qgis_process: Path,
    env: dict[str, str],
    cwd: Path,
    dem: Path,
    threshold: int,
    out_dir: Path,
    audit: list[dict[str, Any]],
) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    outputs = {
        "accumulation": out_dir / f"acc_{threshold}.tif",
        "drainage": out_dir / f"drain_{threshold}.tif",
        "basin": out_dir / f"basin_{threshold}.tif",
        "stream": out_dir / f"stream_{threshold}.tif",
    }
    cmd = [
        str(qgis_process),
        "run",
        "grass:r.watershed",
        "--",
        f"elevation={dem}",
        f"threshold={threshold}",
        "convergence=5",
        "memory=300",
        "-s=true",
        "-a=true",
        f"accumulation={outputs['accumulation']}",
        f"drainage={outputs['drainage']}",
        f"basin={outputs['basin']}",
        f"stream={outputs['stream']}",
        f"GRASS_REGION_PARAMETER={dem}",
        "GRASS_REGION_CELLSIZE_PARAMETER=0",
    ]
    run_command(cmd, env=env, cwd=cwd, audit=audit)
    return outputs


def run_entropy_partition(
    *,
    dem: Path,
    boundary: Path,
    landuse: Path,
    soil: Path,
    accumulation: Path,
    drainage: Path,
    out_dir: Path,
    delta: float,
    similarity: float,
    paper_only: bool,
    audit: list[dict[str, Any]],
) -> dict[str, Any]:
    cmd = [
        "python3",
        str(FLOWPATH_SCRIPT),
        "--dem",
        str(dem),
        "--boundary-shp",
        str(boundary),
        "--landuse-shp",
        str(landuse),
        "--soil-shp",
        str(soil),
        "--flow-accumulation",
        str(accumulation),
        "--drainage-direction",
        str(drainage),
        "--out-dir",
        str(out_dir),
        "--target-subcatchments",
        "999" if paper_only else "45",
        "--min-split-spacing-cells",
        "4",
        "--paper-delta-threshold",
        str(delta),
        "--paper-similarity-threshold",
        str(similarity),
    ]
    if paper_only:
        cmd.append("--paper-only-splits")
    stdout = run_command(cmd, env=None, cwd=REPO_ROOT, audit=audit)
    summary_path = out_dir / "paper_entropy_partition_summary.json"
    return json.loads(summary_path.read_text(encoding="utf-8")) if summary_path.exists() else {"stdout": stdout}


def run_standard_partition(
    *,
    qgis_process: Path,
    env: dict[str, str],
    cwd: Path,
    basin_raster: Path,
    threshold: int,
    out_dir: Path,
    audit: list[dict[str, Any]],
) -> dict[str, Any]:
    """Vectorize GRASS basin raster into subcatchment GeoJSON (no entropy)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_shp = out_dir / f"basins_raw_{threshold}.shp"
    run_command(
        [
            str(qgis_process), "run", "gdal:polygonize", "--",
            f"INPUT={basin_raster}",
            "BAND=1",
            "FIELD=basin_id",
            f"OUTPUT={raw_shp}",
        ],
        env=env, cwd=cwd, audit=audit,
    )
    out_geojson = out_dir / "standard_subcatchments.geojson"
    run_command(
        ["ogr2ogr", "-f", "GeoJSON", "-where", "basin_id != 0", str(out_geojson), str(raw_shp)],
        env=None, cwd=cwd, audit=audit,
    )
    gj = json.loads(out_geojson.read_text(encoding="utf-8"))
    for feat in gj.get("features", []):
        bid = feat["properties"].get("basin_id", "?")
        feat["properties"]["segment_id"] = f"S{bid}"
    out_geojson.write_text(json.dumps(gj, indent=2), encoding="utf-8")
    return {"subcatchments_geojson": str(out_geojson), "count": len(gj.get("features", []))}


def rank_subcatchment_entropy(partition_dir: Path, out_path: Path) -> dict[str, Any] | None:
    """Read entropy partition GeoJSON, rank subcatchments by WJE descending."""
    geojson_path = partition_dir / "paper_entropy_partition.geojson"
    if not geojson_path.exists():
        return None
    gj = json.loads(geojson_path.read_text(encoding="utf-8"))
    rows = []
    for feat in gj.get("features", []):
        props = feat.get("properties", {})
        sid = props.get("segment_id", props.get("basin_id", "?"))
        wje = next((props[k] for k in ("mean_wje", "wje", "WJE") if k in props), None)
        nwje = next((props[k] for k in ("mean_nwje", "nwje", "NWJE") if k in props), None)
        rows.append({"segment_id": sid, "wje": wje, "nwje": nwje})
    rows.sort(key=lambda r: (r["wje"] is None, -(r["wje"] or 0)))
    for i, row in enumerate(rows):
        row["entropy_rank"] = i + 1
    result = {
        "subcatchment_count": len(rows),
        "note": "Rank 1 = highest WJE = most spatially heterogeneous. Prioritise these for finer delineation.",
        "ranked": rows,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def write_method_summary(path: Path, manifest: dict[str, Any]) -> None:
    lines = [
        "# QGIS Entropy-Guided Subcatchment Audit Summary",
        "",
        f"- Case: `{manifest['case_id']}`",
        f"- Generated: `{manifest['generated_at_utc']}`",
        f"- QGIS: `{manifest.get('qgis_version', '')}`",
        f"- GRASS: `{manifest.get('grass_version', '')}`",
        "",
        "## Workflow",
        "- Validate raw GIS layer paths and CRS sidecars.",
        "- Run QGIS Processing `grass:r.watershed` for flow accumulation, drainage direction, basin labels, and stream network.",
        "- Compute paper-consistent WJE/NWJE over upstream `U(g)` and WFJS along the longest D8 flow path.",
        "- Apply strict paper-rule threshold sensitivity for subcatchment partitioning.",
        "",
        "## Evidence Boundary",
        manifest["evidence_boundary"],
        "",
        "## Threshold Sensitivity",
        "| Variant | Delta threshold | WFJS threshold | Subcatchments |",
        "|---|---:|---:|---:|",
    ]
    for row in manifest["threshold_sensitivity"]:
        lines.append(
            f"| {row['variant']} | {row['delta_threshold']} | {row['similarity_threshold']} | {row['final_subcatchment_count']} |"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run raw watershed GIS -> QGIS/GRASS -> subcatchment partition (entropy or standard).")
    parser.add_argument("--mode", choices=["entropy", "standard"], default="entropy",
                        help="entropy: paper-rule WJE/NWJE/WFJS partition with threshold sensitivity (default). standard: direct GRASS basin polygonization, no entropy.")
    parser.add_argument("--case-id", default="qgis-entropy-case")
    parser.add_argument("--case-label", help="Human-readable label for figures and audit summaries. Defaults to case-id.")
    parser.add_argument("--dem", type=Path, required=True)
    parser.add_argument("--boundary", type=Path, required=True)
    parser.add_argument("--landuse", type=Path, required=True)
    parser.add_argument("--soil", type=Path, required=True)
    parser.add_argument("--rainfall", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--stream-threshold", type=int, default=100)
    parser.add_argument("--qgis-process", type=Path, default=Path(DEFAULT_QGIS_PROCESS))
    parser.add_argument("--proj-lib", type=Path, default=Path(DEFAULT_PROJ_LIB))
    parser.add_argument("--gisbase", type=Path, default=Path(DEFAULT_GISBASE))
    parser.add_argument("--normalize-layers", action="store_true", help="Reproject DEM/boundary/landuse/soil to one CRS and clip them by the boundary before hydrology.")
    parser.add_argument("--target-crs", help="Optional CRS auth id, WKT/PROJ string, or layer path for normalization. Defaults to boundary CRS.")
    parser.add_argument("--target-resolution", type=float, help="Optional target raster resolution in target CRS units during normalization.")
    parser.add_argument("--dem-resampling", type=int, default=1, help="GDAL resampling enum for DEM reprojection; default 1 is bilinear.")
    parser.add_argument("--categorical-resampling", type=int, default=0, help="GDAL resampling enum for categorical rasters; default 0 is nearest.")
    parser.add_argument("--skip-qgis", action="store_true", help="Reuse existing threshold_sweep rasters in out-dir/01_gis/threshold_sweep.")
    args = parser.parse_args()

    out_dir = args.out_dir.resolve()
    raw_dir = out_dir / "00_raw"
    gis_dir = out_dir / "01_gis"
    params_dir = out_dir / "02_params"
    figures_dir = out_dir / "07_figures"
    audit_dir = out_dir / "audit"
    memory_dir = out_dir / "memory"
    commands: list[dict[str, Any]] = []
    generated_at = datetime.now(timezone.utc).isoformat()
    env = qgis_env(args)

    input_paths = {
        "dem": args.dem.resolve(),
        "boundary": args.boundary.resolve(),
        "landuse": args.landuse.resolve(),
        "soil": args.soil.resolve(),
    }
    if args.rainfall:
        input_paths["rainfall"] = args.rainfall.resolve()
    for name, path in input_paths.items():
        if not path.exists():
            raise FileNotFoundError(f"Missing {name}: {path}")

    raw_dir.mkdir(parents=True, exist_ok=True)
    original_input_paths = dict(input_paths)
    normalized_manifest: dict[str, Any] | None = None
    if args.normalize_layers:
        normalize_cmd = [
            "python3",
            str(QGIS_PREP_SCRIPT),
            "normalize-layers",
            "--dem",
            str(input_paths["dem"]),
            "--boundary",
            str(input_paths["boundary"]),
            "--landuse",
            str(input_paths["landuse"]),
            "--soil",
            str(input_paths["soil"]),
            "--out-dir",
            str(raw_dir / "normalized_layers"),
            "--qgis-process",
            str(args.qgis_process),
            "--proj-lib",
            str(args.proj_lib),
            "--gisbase",
            str(args.gisbase),
            "--dem-resampling",
            str(args.dem_resampling),
            "--categorical-resampling",
            str(args.categorical_resampling),
        ]
        if args.target_crs:
            normalize_cmd.extend(["--target-crs", args.target_crs])
        if args.target_resolution:
            normalize_cmd.extend(["--target-resolution", str(args.target_resolution)])
        normalized_stdout = run_command(normalize_cmd, env=None, cwd=REPO_ROOT, audit=commands)
        normalized_manifest = json.loads(normalized_stdout)
        normalized_outputs = normalized_manifest["outputs"]
        input_paths.update(
            {
                "dem": Path(normalized_outputs["dem"]).resolve(),
                "boundary": Path(normalized_outputs["boundary"]).resolve(),
                "landuse": Path(normalized_outputs["landuse"]).resolve(),
                "soil": Path(normalized_outputs["soil"]).resolve(),
            }
        )

    load_layer_cmd = [
        "python3",
        str(QGIS_PREP_SCRIPT),
        "load-layers",
        "--out",
        str(raw_dir / "qgis_layers_manifest.json"),
        "--dem",
        str(input_paths["dem"]),
        "--boundary",
        str(input_paths["boundary"]),
        "--landuse",
        str(input_paths["landuse"]),
        "--soil",
        str(input_paths["soil"]),
    ]
    if "rainfall" in input_paths:
        load_layer_cmd.extend(["--rainfall", str(input_paths["rainfall"])])
    run_command(
        load_layer_cmd,
        env=None,
        cwd=REPO_ROOT,
        audit=commands,
    )
    run_command(
        [
            "python3",
            str(QGIS_PREP_SCRIPT),
            "validate-crs",
            "--layers-manifest",
            str(raw_dir / "qgis_layers_manifest.json"),
            "--out",
            str(raw_dir / "qgis_crs_report.json"),
        ],
        env=None,
        cwd=REPO_ROOT,
        audit=commands,
    )

    threshold_dir = gis_dir / "threshold_sweep"
    if args.skip_qgis:
        hydrology = {
            "accumulation": threshold_dir / f"acc_{args.stream_threshold}.tif",
            "drainage": threshold_dir / f"drain_{args.stream_threshold}.tif",
            "basin": threshold_dir / f"basin_{args.stream_threshold}.tif",
            "stream": threshold_dir / f"stream_{args.stream_threshold}.tif",
        }
        for label, path in hydrology.items():
            if not path.exists():
                raise FileNotFoundError(f"--skip-qgis requested but {label} raster is missing: {path}")
    else:
        hydrology = run_qgis_watershed(
            qgis_process=args.qgis_process,
            env=env,
            cwd=REPO_ROOT,
            dem=input_paths["dem"],
            threshold=args.stream_threshold,
            out_dir=threshold_dir,
            audit=commands,
        )

    # ── Branch on mode ──────────────────────────────────────────────────────
    if args.mode == "standard":
        standard_dir = params_dir / "standard_partition"
        standard = run_standard_partition(
            qgis_process=args.qgis_process,
            env=env,
            cwd=REPO_ROOT,
            basin_raster=hydrology["basin"],
            threshold=args.stream_threshold,
            out_dir=standard_dir,
            audit=commands,
        )
        manifest = {
            "schema_version": "1.0",
            "mode": "standard",
            "generated_by": "qgis_raw_to_entropy_partition",
            "generated_at_utc": generated_at,
            "case_id": args.case_id,
            "normalization_enabled": args.normalize_layers,
            "normalized_layers_manifest": str(raw_dir / "normalized_layers" / "qgis_normalized_layers_manifest.json") if args.normalize_layers else None,
            "qgis_version": qgis_version(args.qgis_process, env, commands, REPO_ROOT) if args.qgis_process.exists() else "unavailable",
            "grass_version": grass_version(args.gisbase),
            "inputs": file_inventory(input_paths),
            "original_inputs": file_inventory(original_input_paths),
            "normalization": normalized_manifest,
            "hydrology_outputs": file_inventory(hydrology),
            "standard_partition": standard,
            "audit_artifacts": {
                "processing_commands": str(audit_dir / "processing_commands.json"),
                "input_checksums": str(audit_dir / "input_checksums.json"),
            },
            "evidence_boundary": "GRASS r.watershed basin polygonization only; no entropy diagnostics.",
        }
        write_json(audit_dir / "processing_commands.json", {"commands": commands})
        write_json(audit_dir / "input_checksums.json", manifest["inputs"])
        write_json(audit_dir / "qgis_standard_run_manifest.json", manifest)
        write_json(memory_dir / "qgis_standard_subcatchment_memory.json", manifest)
        (memory_dir / "qgis_standard_subcatchment_memory.md").write_text(
            f"# QGIS Standard Subcatchment Memory\n\n"
            f"- Case: `{args.case_id}`\n"
            f"- Mode: standard (GRASS basin polygonization, no entropy)\n"
            f"- Subcatchments: `{standard['subcatchments_geojson']}`\n"
            f"- Count: {standard['count']}\n",
            encoding="utf-8",
        )
        print(json.dumps({"ok": True, "mode": "standard", "out_dir": str(out_dir),
                          "subcatchments_geojson": standard["subcatchments_geojson"],
                          "subcatchment_count": standard["count"],
                          "manifest": str(audit_dir / "qgis_standard_run_manifest.json")}, indent=2))

    else:  # entropy
        baseline_dir = params_dir / "paper_entropy_partition"
        baseline = run_entropy_partition(
            dem=input_paths["dem"],
            boundary=input_paths["boundary"],
            landuse=input_paths["landuse"],
            soil=input_paths["soil"],
            accumulation=hydrology["accumulation"],
            drainage=hydrology["drainage"],
            out_dir=baseline_dir,
            delta=0.015,
            similarity=0.95,
            paper_only=False,
            audit=commands,
        )

        sensitivity_dir = params_dir / "threshold_sensitivity"
        sensitivity_rows = []
        for name, delta, similarity in PAPER_VARIANTS:
            summary = run_entropy_partition(
                dem=input_paths["dem"],
                boundary=input_paths["boundary"],
                landuse=input_paths["landuse"],
                soil=input_paths["soil"],
                accumulation=hydrology["accumulation"],
                drainage=hydrology["drainage"],
                out_dir=sensitivity_dir / name,
                delta=delta,
                similarity=similarity,
                paper_only=True,
                audit=commands,
            )
            sensitivity_rows.append(
                {
                    "variant": name,
                    "delta_threshold": delta,
                    "similarity_threshold": similarity,
                    "final_subcatchment_count": summary.get("final_subcatchment_count"),
                    "selected_split_count": summary.get("selected_split_count"),
                    "summary_json": str(sensitivity_dir / name / "paper_entropy_partition_summary.json"),
                    "partition_geojson": str(sensitivity_dir / name / "paper_entropy_partition.geojson"),
                }
            )
        write_json(sensitivity_dir / "threshold_sensitivity_summary.json", sensitivity_rows)
        (sensitivity_dir / "threshold_sensitivity_summary.csv").write_text(
            "variant,delta_threshold,similarity_threshold,final_subcatchment_count,selected_split_count,summary_json,partition_geojson\n"
            + "\n".join(
                f"{row['variant']},{row['delta_threshold']},{row['similarity_threshold']},{row['final_subcatchment_count']},{row['selected_split_count']},{row['summary_json']},{row['partition_geojson']}"
                for row in sensitivity_rows
            )
            + "\n",
            encoding="utf-8",
        )

        run_command(
            [
                "python3", str(PLOT_SCRIPT),
                "--sensitivity-dir", str(sensitivity_dir),
                "--stream", str(hydrology["stream"]),
                "--out-decision", str(figures_dir / "paper_rule_decision_spaces_5panel.png"),
                "--out-partitions", str(figures_dir / "paper_rule_watershed_partitions_5panel.png"),
                "--case-label", args.case_label or args.case_id,
            ],
            env=None, cwd=REPO_ROOT, audit=commands,
        )

        hotspot = rank_subcatchment_entropy(baseline_dir, audit_dir / "entropy_hotspot_ranking.json")

        manifest = {
            "schema_version": "1.0",
            "mode": "entropy",
            "generated_by": "qgis_raw_to_entropy_partition",
            "generated_at_utc": generated_at,
            "case_id": args.case_id,
            "normalization_enabled": args.normalize_layers,
            "normalized_layers_manifest": str(raw_dir / "normalized_layers" / "qgis_normalized_layers_manifest.json") if args.normalize_layers else None,
            "qgis_version": qgis_version(args.qgis_process, env, commands, REPO_ROOT) if args.qgis_process.exists() else "unavailable",
            "grass_version": grass_version(args.gisbase),
            "inputs": file_inventory(input_paths),
            "original_inputs": file_inventory(original_input_paths),
            "normalization": normalized_manifest,
            "hydrology_outputs": file_inventory(hydrology),
            "baseline_entropy_partition": {
                "summary": baseline,
                "out_dir": str(baseline_dir),
            },
            "threshold_sensitivity": sensitivity_rows,
            "entropy_hotspot_ranking": str(audit_dir / "entropy_hotspot_ranking.json") if hotspot else None,
            "figures": file_inventory(
                {
                    "decision_spaces": figures_dir / "paper_rule_decision_spaces_5panel.png",
                    "watershed_partitions": figures_dir / "paper_rule_watershed_partitions_5panel.png",
                }
            ),
            "audit_artifacts": {
                "processing_commands": str(audit_dir / "processing_commands.json"),
                "input_checksums": str(audit_dir / "input_checksums.json"),
                "output_inventory": str(audit_dir / "output_inventory.json"),
                "method_summary": str(audit_dir / "method_summary.md"),
            },
            "evidence_boundary": "GIS preprocessing and entropy-guided SWMM subcatchment spatial-unit selection; not calibrated SWMM hydrologic validation.",
        }
        write_json(audit_dir / "processing_commands.json", {"commands": commands})
        write_json(audit_dir / "input_checksums.json", manifest["inputs"])
        write_json(audit_dir / "output_inventory.json", manifest)
        write_json(audit_dir / "qgis_entropy_run_manifest.json", manifest)
        write_method_summary(audit_dir / "method_summary.md", manifest)
        write_json(memory_dir / "qgis_entropy_subcatchment_memory.json", manifest)
        (memory_dir / "qgis_entropy_subcatchment_memory.md").write_text(
            f"# QGIS Entropy Subcatchment Memory\n\n"
            f"- Case: `{args.case_id}`\n"
            f"- Evidence boundary: {manifest['evidence_boundary']}\n"
            f"- Manifest: `{audit_dir / 'qgis_entropy_run_manifest.json'}`\n"
            f"- Decision-space figure: `{figures_dir / 'paper_rule_decision_spaces_5panel.png'}`\n"
            f"- Watershed partition figure: `{figures_dir / 'paper_rule_watershed_partitions_5panel.png'}`\n"
            + (f"- Entropy hotspot ranking: `{audit_dir / 'entropy_hotspot_ranking.json'}`\n" if hotspot else ""),
            encoding="utf-8",
        )
        print(json.dumps({"ok": True, "mode": "entropy", "out_dir": str(out_dir),
                          "manifest": str(audit_dir / "qgis_entropy_run_manifest.json"),
                          "entropy_hotspot_ranking": str(audit_dir / "entropy_hotspot_ranking.json") if hotspot else None}, indent=2))


if __name__ == "__main__":
    main()
