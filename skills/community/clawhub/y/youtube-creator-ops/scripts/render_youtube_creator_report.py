#!/usr/bin/env python3
"""Render a markdown report from a YouTube publish run manifest."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

SECRET_PATTERNS = (
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}", re.IGNORECASE),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}", re.IGNORECASE),
    re.compile(r"sk-[A-Za-z0-9]{20,}", re.IGNORECASE),
    re.compile(r"AIza[0-9A-Za-z\\-_]{20,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}", re.IGNORECASE),
    re.compile(r"Bearer\\s+[A-Za-z0-9._-]{10,}", re.IGNORECASE),
)
URL_PATTERN = re.compile(r"https?://[^\s<>()\"']+")


def load_manifest(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def is_absolute_or_private(path_text: str) -> bool:
    return path_text.startswith("/") or path_text.startswith("~") or ":\\" in path_text or path_text.startswith("file://")


def safe_display_path(path_text: str) -> str:
    value = path_text.strip()
    if not value:
        return "n/a"
    if is_absolute_or_private(value):
        return "[redacted-private-path]"
    return value


def safe_public_url(url: str) -> str:
    value = url.strip()
    if not value:
        return "n/a"
    try:
        parts = urlsplit(value)
    except ValueError:
        return "[redacted-private-url]"
    host = (parts.hostname or "").lower()
    if parts.scheme != "https":
        return "[redacted-private-url]"
    if host == "youtu.be":
        return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))
    if host in {"youtube.com", "www.youtube.com", "m.youtube.com"} and (
        parts.path == "/watch" or parts.path.startswith("/shorts/")
    ):
        return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))
    if host in {"midjourney.com", "www.midjourney.com", "suno.com", "www.suno.com", "app.suno.com"}:
        return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))
    return "[redacted-private-url]"


def redact_secret_like_text(value: str) -> str:
    output = value
    for pattern in SECRET_PATTERNS:
        output = pattern.sub("[redacted-secret-like-value]", output)
    return output


def sanitize_text(value: str) -> str:
    text = str(value or "").strip()
    if not text:
        return "n/a"
    text = redact_secret_like_text(text)
    return URL_PATTERN.sub(lambda match: safe_public_url(match.group(0)), text)


def safe_browser_profile(value: str) -> str:
    return "[redacted-browser-profile]" if str(value or "").strip() else "n/a"


def format_artifacts(artifacts: dict[str, str]) -> list[str]:
    labels = {
        "screenshot": "screenshot",
        "snapshot_json": "snapshot",
        "console_log": "console",
        "video_proof": "video",
    }
    out: list[str] = []
    for key, label in labels.items():
        value = artifacts.get(key, "").strip()
        if value:
            out.append(f"{label}: `{safe_display_path(value)}`")
    return out


def format_provenance(entries: list[dict[str, object]]) -> list[str]:
    lines: list[str] = []
    for index, entry in enumerate(entries, start=1):
        lines.append(f"### Provenance {index}: {sanitize_text(entry.get('role', ''))} via {sanitize_text(entry.get('provider', ''))}")
        if entry.get("asset_id"):
            lines.append(f"- Asset ID: {sanitize_text(entry['asset_id'])}")
        if entry.get("model"):
            lines.append(f"- Model: {sanitize_text(entry['model'])}")
        if entry.get("prompt_ref"):
            lines.append(f"- Prompt ref: {sanitize_text(entry['prompt_ref'])}")
        if entry.get("source_url"):
            lines.append(f"- Source URL: {safe_public_url(str(entry['source_url']))}")
        if entry.get("license"):
            lines.append(f"- License: {sanitize_text(entry['license'])}")
        lines.append(f"- Public credits required: {'yes' if bool(entry.get('public_credits_required')) else 'no'}")
        if entry.get("attribution_text"):
            lines.append(f"- Attribution text: {sanitize_text(entry['attribution_text'])}")
        if entry.get("notes"):
            lines.append(f"- Notes: {sanitize_text(entry['notes'])}")
        lines.append("")
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, help="Run manifest JSON.")
    parser.add_argument("--out", required=True, help="Output markdown file.")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).expanduser().resolve()
    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    payload = load_manifest(manifest_path)
    run = payload.get("run", {})
    assets = payload.get("assets", {})
    summary = payload.get("summary", {})
    steps = payload.get("steps", [])
    provenance = payload.get("provenance", [])

    lines = [
        "# OpenClaw YouTube Publish Report",
        "",
        f"- Run: `{run.get('run_id', '')}`",
        f"- Channel: {sanitize_text(run.get('channel', ''))}",
        f"- Goal: {sanitize_text(run.get('goal', ''))}",
        f"- Browser profile: {safe_browser_profile(run.get('browser_profile', ''))}",
        f"- Kind: {run.get('kind', '')}",
        f"- Stage: {run.get('stage', '')}",
        f"- Visibility: {run.get('visibility', '')}",
        f"- Audience: {run.get('audience', '')}",
        f"- Studio URL: {safe_public_url(run.get('target_url', ''))}",
        f"- Video file: {safe_display_path(assets.get('video_file', ''))}",
        f"- Title: {sanitize_text(assets.get('title', ''))}",
        f"- Description file: {safe_display_path(assets.get('description_file', ''))}",
        f"- Thumbnail file: {safe_display_path(assets.get('thumbnail_file', ''))}",
        f"- Overall status: **{summary.get('status', 'unknown')}**",
        f"- Passed / Failed / Blocked: {summary.get('passed_steps', 0)} / {summary.get('failed_steps', 0)} / {summary.get('blocked_steps', 0)}",
        f"- Published URL: {safe_public_url(summary.get('published_url', ''))}",
    ]

    for source in assets.get("asset_sources", []):
        value = str(source or "").strip()
        if value:
            lines.append(f"- Asset source: {sanitize_text(value)}")

    if provenance:
        lines.extend(["", "## Asset Provenance", ""])
        lines.extend(format_provenance(provenance))

    lines.extend(["", "## Steps", ""])

    for index, step in enumerate(steps, start=1):
        lines.append(f"### {index}. {step.get('step_id', f'step-{index}')}")
        lines.append(f"- Surface: {sanitize_text(step.get('surface', ''))}")
        lines.append(f"- Status: **{step.get('status', 'unknown')}**")
        lines.append(f"- Action: {sanitize_text(step.get('action', ''))}")
        lines.append(f"- Expected: {sanitize_text(step.get('expected', ''))}")
        lines.append(f"- Actual: {sanitize_text(step.get('actual', ''))}")
        if step.get("note"):
            lines.append(f"- Note: {sanitize_text(step['note'])}")
        if step.get("issue_keys"):
            lines.append(f"- Issue keys: {sanitize_text(', '.join(step['issue_keys']))}")
        if step.get("published_url"):
            lines.append(f"- Published URL: {safe_public_url(step['published_url'])}")
        artifact_parts = format_artifacts(step.get("artifacts", {}))
        if artifact_parts:
            lines.append(f"- Artifacts: {'; '.join(artifact_parts)}")
        lines.append("")

    out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
