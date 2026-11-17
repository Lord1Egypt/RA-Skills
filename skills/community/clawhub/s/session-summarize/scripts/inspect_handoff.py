#!/usr/bin/env python3
"""Read a saved handoff and compare its workspace metadata with current Git state."""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPORT_METADATA = re.compile(r"\A<!-- summarize-handoff schema=2 (?P<json>\{.*\}) -->\r?\n")
POINTER_METADATA = re.compile(r"\A<!-- summarize-pointer schema=1 (?P<json>\{.*\}) -->\r?\n")
LEGACY_METADATA = re.compile(r"\A<!-- summarize-handoff schema=1 created_at=")


def git_value(root: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, check=False)
    except OSError:
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def read_json_header(path: Path, pattern) -> dict[str, str] | None:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    match = pattern.match(text)
    if not match:
        return None
    try:
        return json.loads(match.group("json"))
    except json.JSONDecodeError:
        return None


def inspect(project_root: Path) -> dict[str, object]:
    latest = project_root / ".transfers" / "latest.md"
    try:
        latest_text = latest.read_text(encoding="utf-8")
    except OSError:
        latest_text = ""
    if LEGACY_METADATA.match(latest_text):
        return {"status": "旧格式，未验证", "reason": "schema=1 报告没有任务和工作区绑定", "report": str(latest)}
    pointer = read_json_header(latest, POINTER_METADATA)
    if not pointer:
        return {"status": "受阻", "reason": "未找到有效的 schema=1 latest 指针", "latest": str(latest)}
    report_ref = Path(str(pointer.get("report", "")))
    if report_ref.is_absolute() or report_ref.parts[:1] != ("handoffs",) or ".." in report_ref.parts:
        return {"status": "受阻", "reason": "latest 指针越界或不在 .transfers/handoffs/ 内", "latest": str(latest)}
    handoffs_lexical = project_root / ".transfers" / "handoffs"
    is_junction = getattr(handoffs_lexical, "is_junction", lambda: False)()
    if handoffs_lexical.is_symlink() or is_junction:
        return {"status": "受阻", "reason": "handoffs 目录是 symlink 或 junction", "latest": str(latest)}
    handoffs = handoffs_lexical.resolve()
    report = (project_root / ".transfers" / report_ref).resolve()
    try:
        report.relative_to(handoffs)
    except ValueError:
        return {"status": "受阻", "reason": "latest 指针解析后越出 .transfers/handoffs/", "latest": str(latest)}
    metadata = read_json_header(report, REPORT_METADATA)
    if not metadata:
        return {"status": "受阻", "reason": "latest 指向的报告缺失或不是 schema=2", "report": str(report)}
    current = {
        "project_root": str(project_root.resolve()),
        "branch": git_value(project_root, "branch", "--show-current"),
        "head": git_value(project_root, "rev-parse", "HEAD"),
    }
    mismatches = [
        key for key in ("project_root", "branch", "head")
        if os.path.normcase(str(metadata.get(key))) != os.path.normcase(str(current.get(key)))
    ]
    return {
        "status": "已验证" if not mismatches else "过期参考",
        "mismatches": mismatches,
        "saved": {key: metadata.get(key) for key in ("task_id", "project_root", "branch", "head", "goal_digest", "created_at")},
        "current": current,
        "report": str(report.resolve()),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect latest summarize handoff without writing files.")
    parser.add_argument("project_root", type=Path)
    args = parser.parse_args()
    print(json.dumps(inspect(args.project_root), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
