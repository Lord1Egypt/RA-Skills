#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

from backfill_detected_language import update_raw_transcript, update_summary
from finalize_youtube_summary import parse_workflow_metadata

PLACEHOLDER_MARKERS = [
    "Placeholder created by workflow script",
    "## Status\nPlaceholder created by workflow script",
]


def extract_markdown_section(text: str, header: str) -> str | None:
    pattern = re.compile(rf"^## {re.escape(header)}\s*\n(.*?)(?=^##\s+|\Z)", re.M | re.S)
    match = pattern.search(text)
    if not match:
        return None
    return match.group(1).strip()


def first_nonempty_line(text: str | None) -> str | None:
    if not text:
        return None
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return None


def parse_bullets(text: str | None) -> list[str]:
    if not text:
        return []
    bullets: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        match = re.match(r"^[-*•]\s+(.*)$", stripped)
        if match:
            bullets.append(match.group(1).strip())
    if bullets:
        return bullets
    fallback_lines = [line.strip() for line in text.splitlines() if line.strip()]
    return fallback_lines[:5]


def build_short_summary_bullets(summary_text: str) -> list[str]:
    bullets: list[str] = []
    executive = extract_markdown_section(summary_text, "Executive Summary")
    if executive:
        first_paragraph = re.split(r"\n\s*\n", executive.strip())[0].strip()
        if first_paragraph:
            bullets.append(" ".join(first_paragraph.split()))

    key_takeaways = parse_bullets(extract_markdown_section(summary_text, "Key Takeaways"))
    for bullet in key_takeaways:
        if bullet not in bullets:
            bullets.append(bullet)
        if len(bullets) >= 6:
            break
    return bullets[:6]


def render_session_report(report: dict) -> str:
    backfill_display = report.get("backfilled_language") if report.get("language_backfilled") else "not needed"
    short_summary_lines = report.get("short_summary_bullets") or ["Summary completed successfully."]
    short_summary_block = "\n".join(f"• {line}" for line in short_summary_lines)
    return (
        f"Video\n"
        f"• {report.get('title')}\n"
        f"• URL: [{report.get('source_url')}]({report.get('source_url')})\n\n"
        f"Result\n"
        f"• video_id: {report.get('video_id')}\n"
        f"• Summary language: {report.get('summary_language')}\n"
        f"• Transcript source: {report.get('transcript_source')}\n"
        f"• Status: postprocess_complete = {str(report.get('postprocess_complete')).lower()}\n"
        f"• Language backfilled: {backfill_display}\n"
        f"• end_to_end_total_seconds: {report.get('end_to_end_total_seconds')}\n\n"
        f"Output paths\n"
        f"• Transcript:\n{report.get('raw_transcript')}\n"
        f"• Summary:\n{report.get('summary')}\n\n"
        f"Short summary\n"
        f"{short_summary_block}"
    )


def ensure_final_summary(summary_path: Path) -> None:
    text = summary_path.read_text(encoding="utf-8", errors="ignore")
    for marker in PLACEHOLDER_MARKERS:
        if marker in text:
            raise RuntimeError(
                "Summary file still contains placeholder text. Overwrite it with the final polished summary before running complete_youtube_summary.py"
            )


def finalize_report(raw_transcript: Path, summary_file: Path, summary_start_epoch: float | None) -> dict:
    raw_text = raw_transcript.read_text(encoding="utf-8", errors="ignore")
    summary_text = summary_file.read_text(encoding="utf-8", errors="ignore")
    metadata = parse_workflow_metadata(raw_text)
    summary_end_epoch = summary_file.stat().st_mtime
    workflow_start = metadata["workflow_started_at_epoch"]
    deterministic_total = metadata["timings_seconds"].get("script_total_so_far")

    report = {
        "title": metadata.get("title"),
        "source_url": metadata.get("source_url"),
        "video_id": metadata.get("video_id"),
        "raw_transcript": str(raw_transcript.resolve()),
        "summary": str(summary_file.resolve()),
        "deterministic_total_seconds": deterministic_total,
        "summary_generation_seconds": None,
        "end_to_end_total_seconds": round(summary_end_epoch - workflow_start, 2),
        "detected_language": metadata.get("detected_language"),
        "language_detection_confident": metadata.get("language_detection_confident"),
        "summary_language": first_nonempty_line(extract_markdown_section(summary_text, "Summary Language")) or metadata.get("detected_language"),
        "transcript_source": first_nonempty_line(extract_markdown_section(summary_text, "Transcript Source Method")) or metadata.get("source_method"),
        "short_summary_bullets": build_short_summary_bullets(summary_text),
        "postprocess_complete": True,
    }
    if summary_start_epoch is not None:
        report["summary_generation_seconds"] = round(summary_end_epoch - summary_start_epoch, 2)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a final summary, optionally backfill language, and compute end-to-end timing")
    parser.add_argument("raw_transcript")
    parser.add_argument("summary_file")
    parser.add_argument("--language", help="Language tag chosen by the current LLM/session, e.g. en, zh-CN, es")
    parser.add_argument("--summary-start-epoch", type=float, default=None)
    parser.add_argument("--format", choices=["json", "session", "both"], default="json")
    args = parser.parse_args()

    raw_path = Path(args.raw_transcript)
    summary_path = Path(args.summary_file)

    ensure_final_summary(summary_path)

    if args.language:
        update_raw_transcript(raw_path, args.language)
        update_summary(summary_path, args.language)

    report = finalize_report(raw_path, summary_path, args.summary_start_epoch)
    if args.language:
        report["language_backfilled"] = True
        report["backfilled_language"] = args.language
    else:
        report["language_backfilled"] = False
        report["backfilled_language"] = None
    report["session_report"] = render_session_report(report)

    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif args.format == "session":
        print(report["session_report"])
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        print("\n---SESSION_REPORT---\n")
        print(report["session_report"])


if __name__ == "__main__":
    main()
