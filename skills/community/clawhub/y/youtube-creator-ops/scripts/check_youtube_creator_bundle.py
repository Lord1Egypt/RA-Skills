#!/usr/bin/env python3
"""Validate a YouTube publish run bundle before sharing it."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

ARTIFACT_FIELDS = ("screenshot", "snapshot_json", "console_log", "video_proof")
ASSET_FIELDS = ("video_file", "description_file", "thumbnail_file")
STEP_TEXT_FIELDS = ("action", "expected", "actual", "note")
SECRET_PATTERNS = (
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}", re.IGNORECASE),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}", re.IGNORECASE),
    re.compile(r"sk-[A-Za-z0-9]{20,}", re.IGNORECASE),
    re.compile(r"AIza[0-9A-Za-z\\-_]{20,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}", re.IGNORECASE),
    re.compile(r"Bearer\\s+[A-Za-z0-9._-]{10,}", re.IGNORECASE),
)
URL_PATTERN = re.compile(r"https?://[^\s<>()\"']+")


def add_finding(findings: list[dict], severity: str, code: str, message: str, step_id: str = "") -> None:
    findings.append({"severity": severity, "code": code, "message": message, "step_id": step_id})


def load_manifest(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def is_absolute_or_private(path_text: str) -> bool:
    return path_text.startswith("/") or path_text.startswith("~") or ":\\" in path_text or path_text.startswith("file://")


def display_path_label(path: Path) -> str:
    return path.name or "."


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


def has_secret_like_text(value: str) -> bool:
    return any(pattern.search(value) for pattern in SECRET_PATTERNS)


def has_private_or_query_url(value: str) -> bool:
    for match in URL_PATTERN.finditer(value):
        raw = match.group(0)
        if safe_public_url(raw) != raw:
            return True
    return False


def inspect_text_field(findings: list[dict], value: str, field_name: str, step_id: str = "") -> None:
    text_value = str(value or "").strip()
    if not text_value:
        return
    if has_private_or_query_url(text_value):
        add_finding(
            findings,
            "warning",
            "private-step-url" if step_id else "private-provenance-url",
            f"{field_name} contains a private or query URL that will be redacted in the shareable report.",
            step_id,
        )
    if has_secret_like_text(text_value):
        add_finding(
            findings,
            "error",
            "secret-like-step-text" if step_id else "secret-like-provenance-text",
            f"{field_name} contains secret-like text that should be removed before sharing the bundle.",
            step_id,
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, help="Run manifest JSON.")
    parser.add_argument("--repo-root", default=".", help="Optional repo root for artifact existence checks.")
    parser.add_argument("--out", required=True, help="Output JSON report.")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).expanduser().resolve()
    repo_root = Path(args.repo_root).expanduser().resolve()
    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    payload = load_manifest(manifest_path)
    findings: list[dict] = []

    run = payload.get("run", {})
    assets = payload.get("assets", {})
    if not run.get("run_id"):
        add_finding(findings, "error", "missing-run-id", "Run ID is required.")
    if not run.get("channel"):
        add_finding(findings, "error", "missing-channel", "Channel name is required.")
    if not run.get("goal"):
        add_finding(findings, "error", "missing-goal", "Goal is required.")
    if not run.get("browser_profile"):
        add_finding(findings, "warning", "missing-browser-profile", "Browser profile is missing from the manifest.")
    if not assets.get("video_file"):
        add_finding(findings, "warning", "missing-video-file", "Video file path is not recorded.")
    if not assets.get("title"):
        add_finding(findings, "warning", "missing-title", "Planned title is not recorded.")
    for field in ASSET_FIELDS:
        asset_path = str(assets.get(field, "")).strip()
        if not asset_path:
            continue
        if is_absolute_or_private(asset_path):
            add_finding(findings, "error", "absolute-asset-path", f"{field} uses an absolute or private path.")
            continue
        candidate = repo_root / asset_path
        if not candidate.exists():
            add_finding(findings, "warning", "missing-asset", f"{field} path does not exist under repo root: {asset_path}")
    for index, source in enumerate(assets.get("asset_sources", []), start=1):
        source_text = str(source or "").strip()
        if not source_text:
            continue
        source_label = f"asset_sources[{index}]"
        inspect_text_field(findings, source_text, source_label)
    for index, entry in enumerate(payload.get("provenance", []), start=1):
        if not isinstance(entry, dict):
            add_finding(findings, "error", "invalid-provenance-entry", f"provenance[{index}] must be an object.")
            continue
        role = str(entry.get("role") or "").strip()
        provider = str(entry.get("provider") or "").strip()
        if not role or not provider:
            add_finding(findings, "error", "missing-provenance-fields", f"provenance[{index}] must include role and provider.")
        for field_name in ("asset_id", "source_url", "prompt_ref", "model", "license", "attribution_text", "notes"):
            inspect_text_field(findings, str(entry.get(field_name, "") or ""), f"provenance[{index}].{field_name}")

    steps = payload.get("steps", [])
    if not steps:
        add_finding(findings, "error", "no-steps", "Bundle has no recorded steps.")

    for index, step in enumerate(steps, start=1):
        step_id = step.get("step_id", f"step-{index}")
        if not step.get("action"):
            add_finding(findings, "error", "missing-action", "Step is missing action text.", step_id)
        if not step.get("expected"):
            add_finding(findings, "error", "missing-expected", "Step is missing expected behavior.", step_id)
        if not step.get("actual"):
            add_finding(findings, "error", "missing-actual", "Step is missing actual behavior.", step_id)
        for field in STEP_TEXT_FIELDS:
            inspect_text_field(findings, str(step.get(field, "") or ""), field, step_id)

        status = step.get("status")
        if status not in {"passed", "failed", "blocked"}:
            add_finding(findings, "error", "invalid-status", "Step status must be passed, failed, or blocked.", step_id)

        artifacts = step.get("artifacts", {})
        screenshot = artifacts.get("screenshot", "")
        if status in {"failed", "blocked"} and not screenshot:
            add_finding(findings, "warning", "missing-screenshot", "Failed or blocked step should include a screenshot.", step_id)
        if status == "failed" and not step.get("note") and not step.get("issue_keys"):
            add_finding(findings, "warning", "missing-failure-detail", "Failed step should include a note or issue key.", step_id)

        for field in ARTIFACT_FIELDS:
            artifact_path = str(artifacts.get(field, "")).strip()
            if not artifact_path:
                continue
            if is_absolute_or_private(artifact_path):
                add_finding(findings, "error", "absolute-artifact-path", f"{field} uses an absolute or private path.", step_id)
                continue
            candidate = repo_root / artifact_path
            if not candidate.exists():
                add_finding(findings, "warning", "missing-artifact", f"{field} path does not exist under repo root: {artifact_path}", step_id)

    errors = sum(1 for finding in findings if finding["severity"] == "error")
    warnings = sum(1 for finding in findings if finding["severity"] == "warning")
    report = {
        "manifest": display_path_label(manifest_path),
        "repo_root": display_path_label(repo_root),
        "status": "ok" if errors == 0 else "fix_required",
        "errors": errors,
        "warnings": warnings,
        "findings": findings,
    }
    out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
