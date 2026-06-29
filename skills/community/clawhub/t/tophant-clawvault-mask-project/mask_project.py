#!/usr/bin/env python3
"""Standalone OpenClaw skill for masking company project documents."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

VERSION = "0.1.0"
MASK = "numbered_mask"
MAX_FILE_BYTES = 5 * 1024 * 1024
NO_MATCH_WARNING = "No matching sensitive content was found. This does not guarantee the document is safe; it only means the current policy did not match."


@dataclass(frozen=True)
class MatchSpan:
    start: int
    end: int
    label: str
    priority: int

    @property
    def length(self) -> int:
        return self.end - self.start


def default_policy() -> dict[str, Any]:
    """Return the built-in conservative company-project masking policy."""
    return {
        "version": 1,
        "name": "company-project-default",
        "mode": "literal_mask",
        "replacement": MASK,
        "restore": False,
        "merge_adjacent": True,
        "rules": [
            {
                "id": "company_name_cn_labeled",
                "type": "regex",
                "label": "company_name",
                "description": "Chinese company names introduced by business labels",
                "pattern": r"(?P<label>(?:客户公司|合作公司|供应商|甲方|乙方|公司名称)\s*[:：为是]?\s*)(?P<value>[一-鿿A-Za-z0-9（）()·]{2,40}(?:有限责任公司|股份有限公司|集团有限公司|科技有限公司|咨询有限公司|集团|公司))",
                "priority": 130,
                "mask_group": "value",
            },
            {
                "id": "company_name_cn",
                "type": "regex",
                "label": "company_name",
                "description": "Chinese company or organization names with business suffixes",
                "pattern": r"(?<![一-鿿A-Za-z0-9])(?!(?:客户公司|合作公司|供应商|甲方|乙方|公司名称)\s*[:：])[一-鿿A-Za-z0-9（）()·]{2,40}(?:有限责任公司|股份有限公司|集团有限公司|科技有限公司|咨询有限公司|集团|公司)",
                "priority": 100,
                "mask_group": None,
            },
            {
                "id": "company_name_en_labeled",
                "type": "regex",
                "label": "company_name",
                "description": "English company names introduced by business labels",
                "pattern": r"(?P<label>(?:Client Company|Customer Company|Partner Company|Vendor|Supplier|Company Name)[ \t]*[:=]?[ \t]*)(?P<value>[A-Z][A-Za-z0-9&.,' -]{1,60}[ \t](?:LLC|Inc\.?|Ltd\.?|Limited|Corporation|Corp\.?|Technologies|Technology|Group|Company))\b",
                "priority": 125,
                "mask_group": "value",
            },
            {
                "id": "company_name_en",
                "type": "regex",
                "label": "company_name",
                "description": "English company names with common suffixes",
                "pattern": r"\b[A-Z][A-Za-z0-9&.,' -]{1,60}[ \t](?:LLC|Inc\.?|Ltd\.?|Limited|Corporation|Corp\.?)\b",
                "priority": 80,
                "mask_group": None,
            },
            {
                "id": "project_amount_labeled",
                "type": "regex",
                "label": "project_amount",
                "description": "Project amount values introduced by business labels",
                "pattern": r"(?P<label>(?:Project Amount|Contract Amount|Contract Total|Project Budget|Budget|Quote|Amount|项目金额|合同金额|合同总额|项目预算|预算|报价|金额)[ \t]*[:：=为是]?[ \t]*)(?P<value>(?:USD|EUR|GBP|RMB|CNY|US\$|\$|€|£|¥|人民币)?[ \t]*(?:[0-9][0-9,]*(?:\.[0-9]+)?|[一二三四五六七八九十百千万亿两〇零]+)[ \t]*(?:dollars?|yuan|RMB|CNY|元|万元|万|亿元|亿)?)",
                "priority": 120,
                "mask_group": "value",
            },
            {
                "id": "project_amount_unlabeled",
                "type": "regex",
                "label": "project_amount",
                "description": "Standalone currency amount values",
                "pattern": r"(?:USD|EUR|GBP|RMB|CNY|US\$|\$|€|£|¥|人民币)\s*(?:[0-9][0-9,]*(?:\.[0-9]+)?|[一二三四五六七八九十百千万亿两〇零]+)\s*(?:dollars?|yuan|RMB|CNY|元|万元|万|亿元|亿)?|\b[0-9][0-9,]*(?:\.[0-9]+)?\s*(?:dollars?|yuan|RMB|CNY|万元|亿元|元)\b",
                "priority": 60,
                "mask_group": None,
            },
            {
                "id": "person_name_contextual",
                "type": "regex",
                "label": "person_name",
                "description": "Person names introduced by role/contact labels",
                "pattern": r"(?P<label>(?:Project Manager|Client Manager|Contact|Owner|Manager|Director|Legal Representative|Representative|负责人|联系人|项目经理|客户经理|经理|总监|法人|代表)[ \t]*[:：=为是]?[ \t]*)(?P<value>(?:[A-Z][a-z]+(?:[ \t]+[A-Z][a-z]+){0,3}|[一-鿿]{2,4}))",
                "priority": 110,
                "mask_group": "value",
            },
        ],
    }


def json_response(payload: dict[str, Any], exit_code: int = 0) -> int:
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return exit_code


def save_json(path: str, payload: dict[str, Any]) -> str:
    target = Path(path).expanduser()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return str(target)


def load_policy(path: str | None) -> dict[str, Any]:
    if not path:
        return default_policy()
    policy_path = Path(path).expanduser()
    data = json.loads(policy_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Policy must be a JSON object")
    return data


def validate_policy(policy: dict[str, Any]) -> None:
    if policy.get("mode") != "literal_mask":
        raise ValueError("Only literal_mask policies are supported")
    if policy.get("replacement", MASK) != MASK:
        raise ValueError("Only numbered_mask replacement is supported")
    if policy.get("restore") is not False:
        raise ValueError("Policy restore must be false")
    rules = policy.get("rules")
    if not isinstance(rules, list):
        raise ValueError("Policy rules must be a list")


def read_input_file(file_path: str) -> tuple[Path, str]:
    path = Path(file_path).expanduser()
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    if not path.is_file():
        raise ValueError(f"Not a file: {file_path}")
    size = path.stat().st_size
    if size > MAX_FILE_BYTES:
        raise ValueError(f"File too large: {size} bytes exceeds {MAX_FILE_BYTES} bytes")
    return path, path.read_text(encoding="utf-8", errors="replace")


def collect_matches(text: str, policy: dict[str, Any]) -> list[MatchSpan]:
    matches: list[MatchSpan] = []
    for rule in policy.get("rules", []):
        if not isinstance(rule, dict) or rule.get("type") != "regex":
            continue
        label = str(rule.get("label") or "unknown")
        priority = int(rule.get("priority") or 0)
        pattern = str(rule.get("pattern") or "")
        mask_group = rule.get("mask_group")
        if not pattern:
            continue
        compiled = re.compile(pattern, re.MULTILINE)
        for match in compiled.finditer(text):
            if mask_group:
                try:
                    start, end = match.span(str(mask_group))
                except IndexError:
                    start, end = match.span()
            else:
                start, end = match.span()
            if start >= 0 and end > start:
                matches.append(MatchSpan(start=start, end=end, label=label, priority=priority))
    return matches


def overlaps(a: MatchSpan, b: MatchSpan) -> bool:
    return a.start < b.end and b.start < a.end


def select_non_overlapping(matches: list[MatchSpan]) -> list[MatchSpan]:
    ordered = sorted(matches, key=lambda m: (-m.priority, -m.length, m.start, m.end, m.label))
    selected: list[MatchSpan] = []
    for candidate in ordered:
        if not any(overlaps(candidate, existing) for existing in selected):
            selected.append(candidate)
    return sorted(selected, key=lambda m: (m.start, m.end, m.label))


def merge_adjacent_spans(spans: list[MatchSpan]) -> list[MatchSpan]:
    if not spans:
        return []
    merged: list[MatchSpan] = [spans[0]]
    for span in spans[1:]:
        last = merged[-1]
        if span.start <= last.end:
            merged[-1] = MatchSpan(
                start=last.start,
                end=max(last.end, span.end),
                label=last.label if last.label == span.label else "mixed",
                priority=max(last.priority, span.priority),
            )
        else:
            merged.append(span)
    return merged


def mask_text(text: str, spans: list[MatchSpan]) -> str:
    replacements = {
        span: f"[mask_{index}]"
        for index, span in enumerate(sorted(spans, key=lambda m: (m.start, m.end, m.label)), start=1)
    }
    sanitized = text
    for span in sorted(spans, key=lambda m: m.start, reverse=True):
        sanitized = sanitized[: span.start] + replacements[span] + sanitized[span.end :]
    return sanitized


def count_by_label(spans: list[MatchSpan]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for span in spans:
        counts[span.label] = counts.get(span.label, 0) + 1
    return counts


def command_generate_policy(args: argparse.Namespace) -> int:
    policy = default_policy()
    saved_path = save_json(args.save_policy, policy) if args.save_policy else None
    return json_response(
        {
            "success": True,
            "action": "generate-policy",
            "policy_name": policy["name"],
            "replacement": policy["replacement"],
            "restore": policy["restore"],
            "rules": [
                {
                    "id": rule["id"],
                    "label": rule["label"],
                    "description": rule["description"],
                    "priority": rule["priority"],
                    "mask_group": rule["mask_group"],
                }
                for rule in policy["rules"]
            ],
            "saved_policy": saved_path,
        }
    )


def command_mask_file(args: argparse.Namespace) -> int:
    policy = load_policy(args.policy)
    validate_policy(policy)
    saved_policy = save_json(args.save_policy, policy) if args.save_policy else None
    input_path, content = read_input_file(args.path)

    raw_matches = collect_matches(content, policy)
    selected = select_non_overlapping(raw_matches)
    replacement_spans = merge_adjacent_spans(selected) if policy.get("merge_adjacent", True) else selected
    sanitized = mask_text(content, replacement_spans) if selected else content

    output_path = None
    if args.output:
        output = Path(args.output).expanduser()
        if output.resolve(strict=False) == input_path.resolve(strict=False):
            return json_response(
                {
                    "success": False,
                    "error": "Output path must be different from the input file path",
                },
                exit_code=1,
            )
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(sanitized, encoding="utf-8")
        output_path = str(output)

    warnings = [] if selected else [NO_MATCH_WARNING]
    return json_response(
        {
            "success": True,
            "action": "mask-file",
            "input_file": str(input_path),
            "output_file": output_path,
            "saved_policy": saved_policy,
            "replacement": MASK,
            "restore": False,
            "detections": len(selected),
            "counts_by_label": count_by_label(selected),
            "warnings": warnings,
            "sanitized_content": sanitized,
        }
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Mask sensitive company-project document content")
    parser.add_argument("--version", action="version", version=VERSION)
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser("generate-policy", help="Generate the default masking policy")
    generate.add_argument("--save-policy", help="Write the generated policy JSON to this path")
    generate.set_defaults(func=command_generate_policy)

    mask_file = subparsers.add_parser("mask-file", help="Mask a local project document")
    mask_file.add_argument("path", help="Path to the local document to mask")
    mask_file.add_argument("--output", help="Optional path for sanitized output content")
    mask_file.add_argument("--save-policy", help="Write the effective policy JSON to this path")
    mask_file.add_argument("--policy", help="Load a custom policy JSON from this path")
    mask_file.set_defaults(func=command_mask_file)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:
        return json_response(
            {
                "success": False,
                "error": str(exc),
            },
            exit_code=1,
        )


if __name__ == "__main__":
    raise SystemExit(main())
