#!/usr/bin/env python3
"""Build one compact context bundle for daily grading."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from run_log import Timer, append_run_log, new_run_id  # noqa: E402


MAX_ACTIVE_CONTEXT_BYTES = 2500
MAX_PROFILE_BYTES = 1800


def read_text(path: Path, *, max_bytes: int | None = None) -> tuple[str, bool]:
    if not path.exists():
        return "", False
    data = path.read_bytes()
    truncated = False
    if max_bytes is not None and len(data) > max_bytes:
        data = data[:max_bytes]
        truncated = True
    return data.decode("utf-8", errors="replace"), truncated


def load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as f:
        value = json.load(f)
    return value if isinstance(value, dict) else None


def extract_updated(text: str) -> str:
    match = re.search(r"^- Updated:\s*(.+)$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def compact_git_sync(config: dict[str, Any] | None) -> dict[str, Any]:
    git_sync = config.get("git_sync", {}) if config else {}
    pages = config.get("pages", {}) if config else {}
    if not isinstance(git_sync, dict):
        git_sync = {}
    if not isinstance(pages, dict):
        pages = {}
    return {
        "workspace_role": config.get("workspace_role") if config else "",
        "git_sync_enabled": bool(git_sync.get("enabled")),
        "auto_pull_before_task": bool(git_sync.get("auto_pull_before_task")),
        "auto_commit_after_task": bool(git_sync.get("auto_commit_after_task")),
        "auto_push_after_task": bool(git_sync.get("auto_push_after_task")),
        "defer_push_after_grading": bool(git_sync.get("defer_push_after_grading", False)),
        "pages_enabled": bool(pages.get("enabled")),
        "pages_auto_publish_worksheets": bool(pages.get("auto_publish_worksheets")),
    }


def build_context(workspace: Path) -> dict[str, Any]:
    files_read: list[str] = []
    warnings: list[str] = []

    config_path = workspace / ".zhizhi-math-coach/config.json"
    config = load_json(config_path)
    if config is not None:
        files_read.append(".zhizhi-math-coach/config.json")
    else:
        warnings.append("missing .zhizhi-math-coach/config.json")

    active_path = workspace / "memory/active-context.md"
    active_context, active_truncated = read_text(active_path, max_bytes=MAX_ACTIVE_CONTEXT_BYTES)
    if active_context:
        files_read.append("memory/active-context.md")
    else:
        warnings.append("missing memory/active-context.md; read long-term/short-term/progress as fallback")
    if active_truncated:
        warnings.append(f"memory/active-context.md exceeded {MAX_ACTIVE_CONTEXT_BYTES} bytes and was truncated")

    profile_path = workspace / "curriculum/profile.md"
    profile, profile_truncated = read_text(profile_path, max_bytes=MAX_PROFILE_BYTES)
    if profile:
        files_read.append("curriculum/profile.md")
    else:
        warnings.append("missing curriculum/profile.md")
    if profile_truncated:
        warnings.append(f"curriculum/profile.md exceeded {MAX_PROFILE_BYTES} bytes and was truncated")

    return {
        "mode_default": "fast_grade_light_record",
        "active_context_updated": extract_updated(active_context),
        "git_sync": compact_git_sync(config),
        "files_read": files_read,
        "warnings": warnings,
        "grading_rubric_digest": {
            "confidence": ["高: direct evidence or repeated pattern", "中: answer suggests cause but work incomplete", "低: final answer only or multiple causes possible"],
            "error_layers": ["阅读理解", "题型判断", "概念理解", "计算技能", "步骤遗漏", "审题习惯", "表达书写", "粗心偶发", "问法未识别", "条件误用", "中间量缺失", "两步逻辑漏步"],
            "auto_upgrade": [
                "same cause appears in two or more wrong/uncertain items",
                "active weak point looks like relapse, transfer failure, or spaced forgetting",
                "formal test, teacher-marked paper, phase review, midterm/final, or official school mistake set",
                "high-confidence new durable weak point",
            ],
        },
        "active_context": active_context,
        "curriculum_profile": profile,
    }


def render_markdown(context: dict[str, Any]) -> str:
    git_sync = context["git_sync"]
    lines = [
        "# Grading Context",
        "",
        f"- Default mode: {context['mode_default']}",
        f"- Active context updated: {context.get('active_context_updated') or 'unknown'}",
        f"- Git sync enabled: {git_sync['git_sync_enabled']}",
        f"- Defer push after grading: {git_sync['defer_push_after_grading']}",
        f"- Files read: {', '.join(context['files_read']) or 'none'}",
    ]
    if context["warnings"]:
        lines.extend(["", "## Warnings", "", *[f"- {warning}" for warning in context["warnings"]]])
    lines.extend(
        [
            "",
            "## Active Context",
            "",
            context["active_context"] or "missing",
            "",
            "## Curriculum Profile",
            "",
            context["curriculum_profile"] or "missing",
            "",
            "## Grading Rubric Digest",
            "",
            "- Confidence: 高 / 中 / 低.",
            "- Separate reading, modeling, concept, calculation, step, checking, and expression errors.",
            "- Auto-upgrade to full_archive only from evidence, then open matching history selectively.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build compact grading context for zhizhi-math-coach.")
    parser.add_argument("--workspace", type=Path, default=Path("."), help="Personal learning repository root.")
    parser.add_argument("--format", choices=["json", "md"], default="md")
    parser.add_argument("--output", type=Path, help="Optional output path. Defaults to stdout.")
    parser.add_argument("--run-id", default="", help="Optional run id for .zhizhi-math-coach/run-log.jsonl.")
    parser.add_argument("--no-log", action="store_true", help="Do not append run-log.jsonl.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    timer = Timer()
    workspace = args.workspace.resolve()
    run_id = args.run_id or new_run_id()
    ok = False
    context: dict[str, Any] = {}
    try:
        context = build_context(workspace)
        output = json.dumps(context, ensure_ascii=False, indent=2) + "\n" if args.format == "json" else render_markdown(context)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(output, encoding="utf-8")
        else:
            print(output, end="")
        ok = True
        return 0
    finally:
        if not args.no_log:
            append_run_log(
                workspace,
                {
                    "run_id": run_id,
                    "script": "build_grading_context.py",
                    "ok": ok,
                    "duration_ms": timer.elapsed_ms(),
                    "files_read": context.get("files_read", []),
                    "warnings": context.get("warnings", []),
                },
            )


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
