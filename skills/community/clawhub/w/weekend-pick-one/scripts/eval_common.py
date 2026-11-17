#!/usr/bin/env python3
from __future__ import annotations

import re


def count_backup_markers(text: str) -> int:
    return text.count("备胎 A") + text.count("备胎 B") + text.count("备胎：")


def markdown_link_count(text: str) -> int:
    return len(re.findall(r"\[[^\]]+\]\(https?://[^)]+\)", text))


def main_line(text: str) -> str:
    for line in text.splitlines():
        if line.strip().startswith("主线："):
            return line.strip()[3:].strip()
    return ""


def evaluate_text(case: dict, output: str) -> list[str]:
    failures: list[str] = []
    stripped = output.lstrip()

    must_start_with = case.get("must_start_with")
    if must_start_with and not stripped.startswith(must_start_with):
        failures.append(f"output must start with: {must_start_with}")
    elif not must_start_with and case.get("mode") != "cold_start" and not (
        stripped.startswith("判了") or stripped.startswith("方向版")
    ):
        failures.append("output must start with 判了 or 方向版")

    for fragment in case.get("required_fragments", []):
        if fragment not in output:
            failures.append(f"missing required fragment: {fragment}")

    for group in case.get("required_any", []):
        if not any(fragment in output for fragment in group):
            failures.append(f"missing one of required fragments: {group}")

    for fragment in case.get("forbidden_fragments", []):
        if fragment in output:
            failures.append(f"forbidden fragment present: {fragment}")

    for section in case.get("required_sections", []):
        if section not in output:
            failures.append(f"missing section: {section}")

    for pattern in case.get("required_patterns", []):
        if not re.search(pattern, output, flags=re.MULTILINE):
            failures.append(f"missing required pattern: {pattern}")

    for pattern in case.get("forbidden_patterns", []):
        if re.search(pattern, output, flags=re.MULTILINE):
            failures.append(f"forbidden pattern present: {pattern}")

    max_backup_count = case.get("max_backup_count")
    if max_backup_count is not None and count_backup_markers(output) > max_backup_count:
        failures.append(f"too many backup plans, cap is {max_backup_count}")

    min_markdown_links = case.get("min_markdown_links", 0)
    if markdown_link_count(output) < min_markdown_links:
        failures.append(f"needs at least {min_markdown_links} markdown source links")

    if case.get("require_specific_main_line"):
        selected = main_line(output)
        if not selected:
            failures.append("missing 主线 line")
        else:
            vague_markers = [" 或 ", " / ", "／", "任选", "某个", "一处", "一家", "一个室内"]
            for marker in vague_markers:
                if marker in selected:
                    failures.append(f"main line is not specific: {marker}")

    if case.get("browser_state") == "login_required":
        if "停止" not in output:
            failures.append("browser-limited case must stop")
        if "3-5 个" not in output:
            failures.append("browser-limited case must ask for 3-5 manual candidates")

    if case.get("id") == "night-remote-safety":
        if "今晚不去" not in output or "白天" not in output:
            failures.append("night safety case must redirect to daytime")

    return failures
