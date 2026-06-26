#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from youtube_shared import (
    apply_filters,
    dataset_markdown,
    detailed_summary_from_record,
    extract_top_phrases,
    filtered_dir,
    language_for_record,
    parse_date_value,
    parse_metadata_filters,
    read_json,
    reports_dir,
    summary_from_record,
    summary_needs_refresh,
    transcript_source_label,
    transcripts_dir,
    write_json,
    write_records_csv,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build filtered JSON, CSV, and markdown reports from YouTube metadata and transcripts."
    )
    parser.add_argument("--input-json", required=True, help="Path to a dataset JSON file with transcript fields")
    parser.add_argument("--output-root", default="output")
    parser.add_argument("--output-prefix", required=True)
    parser.add_argument("--since-date")
    parser.add_argument("--until-date")
    parser.add_argument("--topic-filter")
    parser.add_argument("--speaker-filter")
    parser.add_argument("--metadata-filter", action="append", default=[])
    parser.add_argument("--report-title", default="YouTube Analysis Report")
    parser.add_argument("--write-video-markdown", action="store_true")
    return parser.parse_args()


def load_records(path: Path) -> tuple[dict, list[dict]]:
    payload = read_json(path)
    if isinstance(payload, dict):
        return payload, list(payload.get("videos", []))
    if isinstance(payload, list):
        return {}, list(payload)
    return {}, []


def write_video_markdown(output_dir: Path, records: list[dict]) -> None:
    transcript_path = transcripts_dir(output_dir)
    for record in records:
        note_path = transcript_path / f"{record['video_id']}.md"
        lines = [
            f"# {record.get('title') or record['video_id']}",
            "",
            f"- URL: {record.get('url')}",
            f"- Upload date: {record.get('upload_date') or 'unknown'}",
            f"- Language: {record.get('detected_language') or language_for_record(record) or 'unknown'}",
            f"- Transcript source: {transcript_source_label(record.get('transcript_status'))}",
            f"- Words: {record.get('transcript_word_count', 0)}",
            "",
            "## Summary",
            "",
            record.get("detailed_summary") or record.get("summary") or detailed_summary_from_record(record),
            "",
        ]
        note_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def build_report_markdown(title: str, records: list[dict], args: argparse.Namespace) -> str:
    criteria = [
        f"- Since date: {args.since_date or 'none'}",
        f"- Until date: {args.until_date or 'none'}",
        f"- Topic filter: {args.topic_filter or 'none'}",
        f"- Speaker filter: {args.speaker_filter or 'none'}",
        f"- Metadata filters: {', '.join(args.metadata_filter) or 'none'}",
    ]
    return dataset_markdown(title=title, records=records, criteria_lines=criteria)


def main() -> None:
    args = parse_args()
    since_date = parse_date_value(args.since_date)
    until_date = parse_date_value(args.until_date)
    metadata_filters = parse_metadata_filters(args.metadata_filter)

    output_dir = Path(args.output_root) / args.output_prefix
    filtered_path = filtered_dir(output_dir)
    reports_path = reports_dir(output_dir)
    payload, records = load_records(Path(args.input_json))

    filtered_records = apply_filters(
        records,
        since_date=since_date,
        until_date=until_date,
        topic_filter=args.topic_filter,
        speaker_filter=args.speaker_filter,
        metadata_filters=metadata_filters,
        include_transcript=True,
    )

    for record in filtered_records:
        record["detected_language"] = record.get("detected_language") or language_for_record(record)
        record["top_phrases"] = record.get("top_phrases") or extract_top_phrases(record)
        record["summary"] = summary_from_record(record) if summary_needs_refresh(record.get("summary")) else record.get("summary")
        record["detailed_summary"] = (
            detailed_summary_from_record(record)
            if summary_needs_refresh(record.get("detailed_summary"))
            else record.get("detailed_summary")
        )

    payload = dict(payload) if isinstance(payload, dict) else {}
    payload["videos"] = filtered_records
    payload["filters_applied"] = {
        "since_date": since_date,
        "until_date": until_date,
        "topic_filter": args.topic_filter,
        "speaker_filter": args.speaker_filter,
        "metadata_filters": metadata_filters,
    }

    write_json(filtered_path / f"{args.output_prefix}_videos.final.json", payload)
    write_records_csv(filtered_records, filtered_path / f"{args.output_prefix}_videos.csv")
    (filtered_path / f"{args.output_prefix}_videos.md").write_text(
        dataset_markdown(title="Filtered Videos", records=filtered_records),
        encoding="utf-8",
    )
    (reports_path / f"{args.output_prefix}_report.md").write_text(
        build_report_markdown(args.report_title, filtered_records, args),
        encoding="utf-8",
    )

    if args.write_video_markdown:
        write_video_markdown(output_dir, filtered_records)

    print(f"Wrote report artifacts for {len(filtered_records)} videos.", flush=True)


if __name__ == "__main__":
    main()
