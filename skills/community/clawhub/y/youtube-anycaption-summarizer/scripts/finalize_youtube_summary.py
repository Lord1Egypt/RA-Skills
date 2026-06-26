#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path


def parse_workflow_metadata(raw_text: str) -> dict:
    match = re.search(r"## Workflow Metadata \(JSON\)\s*```json\s*(\{.*?\})\s*```", raw_text, re.S)
    if not match:
        raise RuntimeError("Could not find workflow metadata JSON in raw transcript")
    return json.loads(match.group(1))


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute final end-to-end timing after summary generation")
    parser.add_argument("raw_transcript")
    parser.add_argument("summary_file")
    parser.add_argument("--summary-start-epoch", type=float, default=None)
    parser.add_argument("--format", choices=["json", "text"], default="json")
    args = parser.parse_args()

    raw_text = Path(args.raw_transcript).read_text(encoding="utf-8", errors="ignore")
    metadata = parse_workflow_metadata(raw_text)
    summary_path = Path(args.summary_file)
    summary_end_epoch = summary_path.stat().st_mtime
    workflow_start = metadata["workflow_started_at_epoch"]
    deterministic_total = metadata["timings_seconds"].get("script_total_so_far")

    report = {
        "title": metadata.get("title"),
        "video_id": metadata.get("video_id"),
        "raw_transcript": str(Path(args.raw_transcript).resolve()),
        "summary": str(summary_path.resolve()),
        "deterministic_total_seconds": deterministic_total,
        "summary_generation_seconds": None,
        "end_to_end_total_seconds": round(summary_end_epoch - workflow_start, 2),
    }

    if args.summary_start_epoch is not None:
        report["summary_generation_seconds"] = round(summary_end_epoch - args.summary_start_epoch, 2)

    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Title: {report['title']}")
        print(f"Deterministic total: {report['deterministic_total_seconds']}s")
        if report['summary_generation_seconds'] is not None:
            print(f"Summary generation: {report['summary_generation_seconds']}s")
        print(f"End-to-end total: {report['end_to_end_total_seconds']}s")


if __name__ == "__main__":
    main()
