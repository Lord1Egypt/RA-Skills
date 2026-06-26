#!/usr/bin/env python3

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run the topic-driven Sopaper Evidence workflow: generate a search plan, search external "
            "sources, generate cautious claims, fetch external source notes, and produce the draft evidence pack."
        )
    )
    parser.add_argument("topic", help="Research topic or paper theme.")
    parser.add_argument(
        "--output-dir",
        default="output/topic-evidence-pipeline",
        help="Directory for generated outputs. Default: output/topic-evidence-pipeline",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=8,
        help="Maximum number of search results to keep. Default: 8",
    )
    parser.add_argument(
        "--result-artifacts",
        nargs="*",
        default=[],
        help="Structured result-artifact files to ingest into the downstream evidence pipeline.",
    )
    parser.add_argument(
        "--result-dir",
        nargs="*",
        default=[],
        help="Directories to scan recursively for .csv, .tsv, and .json result artifacts.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parent.parent
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    plan_path = output_dir / "search-plan.md"
    claims_path = output_dir / "generated-claims.md"
    source_list_path = output_dir / "topic-source-list.md"

    run_python(root / "scripts" / "generate_search_plan.py", [args.topic, "-o", str(plan_path)])
    run_python(root / "scripts" / "generate_topic_claims.py", [args.topic, "-o", str(claims_path)])
    run_python(
        root / "scripts" / "search_external_sources.py",
        ["--topic", args.topic, "--plan", str(plan_path), "--output", str(source_list_path), "--limit", str(args.limit)],
    )
    run_python(
        root / "scripts" / "run_evidence_pipeline.py",
        [
            "--sources",
            str(source_list_path),
            "--claims",
            str(claims_path),
            "--fetch-external",
            "--verify-fetched",
            *(
                ["--result-artifacts", *[str(Path(value).expanduser().resolve()) for value in args.result_artifacts]]
                if args.result_artifacts
                else []
            ),
            *(
                ["--result-dir", *[str(Path(value).expanduser().resolve()) for value in args.result_dir]]
                if args.result_dir
                else []
            ),
            "--output-dir",
            str(output_dir / "pipeline"),
        ],
    )
    print("Topic-driven pipeline complete.")
    print(f"search_plan: {plan_path}")
    print(f"generated_claims: {claims_path}")
    print(f"source_list: {source_list_path}")
    print(f"pipeline_dir: {output_dir / 'pipeline'}")
    return 0


def run_python(script: Path, arguments: list[str]) -> None:
    subprocess.run([sys.executable, str(script), *arguments], check=True)


if __name__ == "__main__":
    raise SystemExit(main())
