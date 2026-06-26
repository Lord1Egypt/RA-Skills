#!/usr/bin/env python3.11
"""Run end-to-end SQL markdown to BI scaffold pipeline."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run_step(cmd: list[str]) -> None:
    print("[RUN]", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main() -> None:
    if sys.version_info[:2] != (3, 11):
        raise RuntimeError("python3.11 is required for this pipeline")

    parser = argparse.ArgumentParser(description="Run SQL->BI pipeline")
    parser.add_argument("--input", required=True, help="Path to sql.md")
    parser.add_argument("--out", required=True, help="Output directory")
    parser.add_argument(
        "--with-services",
        action="store_true",
        help="Also generate backend/frontend service bundle under <out>/services",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    query_catalog = out / "query_catalog.json"
    semantic_catalog = out / "semantic_catalog.json"
    chart_plan = out / "chart_plan.json"
    dashboard = out / "dashboard.json"
    ui_dir = out / "ui"

    py = sys.executable

    run_step([py, str(root / "parse_sql_md.py"), "--input", args.input, "--output", str(query_catalog)])
    run_step([py, str(root / "infer_semantics.py"), "--input", str(query_catalog), "--output", str(semantic_catalog)])
    run_step([
        py,
        str(root / "recommend_chart.py"),
        "--input",
        str(semantic_catalog),
        "--query-catalog",
        str(query_catalog),
        "--output",
        str(chart_plan),
    ])
    run_step([
        py,
        str(root / "build_dashboard_spec.py"),
        "--queries",
        str(query_catalog),
        "--semantics",
        str(semantic_catalog),
        "--charts",
        str(chart_plan),
        "--output",
        str(dashboard),
    ])
    run_step([py, str(root / "generate_ui_scaffold.py"), "--dashboard", str(dashboard), "--out", str(ui_dir)])

    if args.with_services:
        services_dir = out / "services"
        run_step([
            py,
            str(root / "generate_service_bundle.py"),
            "--artifacts",
            str(out),
            "--output",
            str(services_dir),
        ])

    print(f"Pipeline completed. Output at {out}")


if __name__ == "__main__":
    main()
