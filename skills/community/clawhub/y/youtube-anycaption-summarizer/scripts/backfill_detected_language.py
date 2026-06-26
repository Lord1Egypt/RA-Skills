#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path


WORKFLOW_METADATA_RE = re.compile(r"## Workflow Metadata \(JSON\)\s*```json\s*(\{.*?\})\s*```", re.S)


def replace_section(text: str, start_header: str, next_header: str, value: str) -> str:
    pattern = re.compile(rf"({re.escape(start_header)}\s*\n)(.*?)(\n{re.escape(next_header)})", re.S)

    def repl(match: re.Match[str]) -> str:
        return f"{match.group(1)}{value}\n{match.group(3)}"

    updated, count = pattern.subn(repl, text, count=1)
    if count != 1:
        raise RuntimeError(f"Could not replace section between '{start_header}' and '{next_header}'")
    return updated


def update_raw_transcript(raw_path: Path, language: str) -> None:
    text = raw_path.read_text(encoding="utf-8", errors="ignore")
    text = replace_section(text, "## Language", "## Generated At", language)

    match = WORKFLOW_METADATA_RE.search(text)
    if not match:
        raise RuntimeError("Could not find workflow metadata JSON in raw transcript")
    metadata = json.loads(match.group(1))
    previous_raw = metadata.get("detected_language_raw")
    if "detected_language_raw_before_backfill" not in metadata:
        metadata["detected_language_raw_before_backfill"] = previous_raw
    metadata["detected_language_raw"] = f"llm:{language}"
    metadata["detected_language"] = language
    metadata["language_detection_confident"] = True
    metadata["language_detection_resolution"] = "llm-backfill"

    replacement = "## Workflow Metadata (JSON)\n```json\n" + json.dumps(metadata, ensure_ascii=False, indent=2) + "\n```"
    text = WORKFLOW_METADATA_RE.sub(replacement, text, count=1)
    raw_path.write_text(text, encoding="utf-8")


def update_summary(summary_path: Path, language: str) -> None:
    text = summary_path.read_text(encoding="utf-8", errors="ignore")
    if "## Summary Language" in text and "## Transcript Source Method" in text:
        text = replace_section(text, "## Summary Language", "## Transcript Source Method", language)
    elif "## Source Transcript" in text:
        text = text.replace("## Source Transcript", f"## Summary Language\n{language}\n\n## Source Transcript", 1)
    elif "## Video ID" in text:
        text = re.sub(r"(## Video ID\s*\n.*?\n)", rf"\1\n## Summary Language\n{language}\n", text, count=1, flags=re.S)
    else:
        text = f"## Summary Language\n{language}\n\n" + text
    summary_path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Backfill detected language into raw transcript and summary markdown files")
    parser.add_argument("raw_transcript")
    parser.add_argument("summary_file")
    parser.add_argument("--language", required=True, help="Language tag chosen by the current LLM/session, e.g. en, zh-CN, es")
    args = parser.parse_args()

    language = args.language.strip()
    if not language:
        raise RuntimeError("--language cannot be empty")

    raw_path = Path(args.raw_transcript)
    summary_path = Path(args.summary_file)
    update_raw_transcript(raw_path, language)
    update_summary(summary_path, language)

    print(json.dumps({
        "raw_transcript": str(raw_path.resolve()),
        "summary": str(summary_path.resolve()),
        "language": language,
        "status": "ok"
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
