from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from utils import json_fail


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def load_answer(args: argparse.Namespace) -> str:
    if args.answer_file:
        return Path(args.answer_file).read_text(encoding="utf-8")
    return args.answer or ""


def load_allowed_sources(args: argparse.Namespace) -> list[str]:
    values = []
    if args.allowed_sources:
        values.extend(re.split(r"[\n,;|]+", args.allowed_sources))
    if args.allowed_sources_file:
        text = Path(args.allowed_sources_file).read_text(encoding="utf-8")
        try:
            data = json.loads(text)
            if isinstance(data, list):
                values.extend(str(x) for x in data)
            elif isinstance(data, dict):
                values.extend(str(x) for x in data.get("sources", []))
        except json.JSONDecodeError:
            values.extend(re.split(r"[\n,;|]+", text))
    return [v.strip() for v in values if v.strip()]


def source_block(text: str) -> str:
    match = re.search(r"(?im)^(来源|sources)\s*[:：]\s*(.*)$", text)
    if not match:
        return ""
    return text[match.start():].strip()


def source_lines(block: str) -> list[str]:
    body = re.sub(r"(?im)^(来源|sources)\s*[:：]\s*", "", block).strip()
    return [line.strip(" -\t") for line in body.splitlines() if line.strip(" -\t")]


def is_no_answer(text: str) -> bool:
    markers = [
        "没有找到",
        "没有答案",
        "无法基于知识库回答",
        "不能基于知识库回答",
        "no answer",
        "not found",
    ]
    lowered = text.lower()
    return any(marker in lowered for marker in markers)


def has_non_empty_source(block: str) -> bool:
    lines = source_lines(block)
    if not lines:
        return False
    empty_values = {"无", "none", "n/a", "没有", "null", "-"}
    return any(line.lower() not in empty_values for line in lines)


def unmatched_source_lines(lines: list[str], allowed: list[str]) -> list[str]:
    if not allowed:
        return []
    normalized_allowed = [item.lower() for item in allowed]
    unmatched = []
    for line in lines:
        lowered = line.lower()
        if lowered in {"无", "none", "n/a", "没有", "null", "-"}:
            continue
        if not any(item and (item in lowered or lowered in item) for item in normalized_allowed):
            unmatched.append(line)
    return unmatched


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--answer", default="")
    parser.add_argument("--answer_file", default="")
    parser.add_argument("--allowed_sources", default="", help="comma/newline separated pages actually read for this answer")
    parser.add_argument("--allowed_sources_file", default="", help="JSON/text file containing pages actually read")
    args = parser.parse_args()

    text = load_answer(args).strip()
    if not text:
        out(json_fail("empty_answer", "回答为空。"))
        return
    block = source_block(text)
    if not block:
        out(json_fail("missing_sources", "回答缺少“来源：”部分。"))
        return
    if is_no_answer(text):
        if has_non_empty_source(block):
            out(json_fail("no_answer_sources_must_be_empty", "无答案场景必须写“来源：无”，不能列出知识库页面作为答案来源。"))
            return
        out({"success": True, "valid": True, "no_answer": True})
        return
    if not has_non_empty_source(block):
        out(json_fail("empty_sources", "回答不是无答案场景，但来源为空。"))
        return
    allowed = load_allowed_sources(args)
    unmatched = unmatched_source_lines(source_lines(block), allowed)
    if unmatched:
        data = json_fail("source_not_in_allowed_hits", "回答来源不在本次实际读取的知识库页面中。")
        data["unmatched_sources"] = unmatched
        data["allowed_sources"] = allowed
        out(data)
        return
    out({"success": True, "valid": True, "no_answer": False, "checked_allowed_sources": bool(allowed)})


if __name__ == "__main__":
    main()
