#!/usr/bin/env python3
"""Reversible Keyword Masking CLI."""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import getpass
import json
import os
import re
import secrets
import shutil
import subprocess
import sys
import tempfile
import zipfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml
except Exception as exc:  # pragma: no cover
    raise SystemExit("Missing dependency: PyYAML. Install with: python -m pip install pyyaml") from exc

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
except Exception as exc:  # pragma: no cover
    raise SystemExit("Missing dependency: cryptography. Install with: python -m pip install cryptography") from exc


PLACEHOLDER_RE = re.compile(r"\[\[[A-Z][A-Z0-9]*_\d{4,}\]\]")
MALFORMED_RE = re.compile(
    r"(?<!\[)\[[A-Z][A-Z0-9]*[_-]\d{3,}\](?!\])"  # single ASCII brackets: [ORG_0001]
    r"|\[\[[A-Z][A-Z0-9]*[-]\d{3,}\]\]"  # double ASCII brackets with a hyphen: [[ORG-0001]]
    r"|[【]+[A-Z][A-Z0-9]*[_-]\d{3,}[】]+"  # full-width brackets: 【【ORG_0001】】
)
TEXT_SUFFIXES = {".txt", ".md", ".markdown"}
DOC_SUFFIX = ".doc"
DOCX_SUFFIX = ".docx"
WORD_SUFFIXES = {DOC_SUFFIX, DOCX_SUFFIX}
KDF_ITERATIONS = 390000
PRESERVED_LABELS = {
    "开户名称",
    "开户行",
    "开户银行",
    "银行账号",
    "银行帐号",
    "银行账户",
    "银行帐户",
    "账号",
    "帐号",
    "账户",
    "帐户",
    "税号",
    "纳税人识别号",
    "统一社会信用代码",
    "名称",
    "单位地址",
    "电话",
}


@dataclass(frozen=True)
class Rule:
    category: str
    value: str | None = None
    pattern: str | None = None
    source: str = "manual"


@dataclass(frozen=True)
class Match:
    start: int
    end: int
    category: str
    value: str
    source: str


@dataclass
class DocxTextSegment:
    element: Any
    start: int
    end: int
    part_name: str
    attr_name: str | None = None


@dataclass
class DocxXmlPart:
    name: str
    root: Any
    changed: bool = False


@dataclass
class DocxTextModel:
    text: str
    segments: list[DocxTextSegment]
    parts: dict[str, DocxXmlPart]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="rkm", description="Reversible Keyword Masking")
    parser.add_argument("--key-env", default="RKM_KEY", help="environment variable containing the mapping password")
    parser.add_argument("--password-file", help="read the mapping password from a local file")
    parser.add_argument("--dpapi-password-file", help="read the mapping password from a Windows DPAPI-sealed file (see seal-password)")
    sub = parser.add_subparsers(dest="command", required=True)

    seal = sub.add_parser("seal-password", help="seal a mapping password into a Windows DPAPI-protected file (Windows only)")
    seal.add_argument("--out", required=True, help="path to write the DPAPI-sealed password file")
    seal.set_defaults(func=cmd_seal_password)

    protect = sub.add_parser("protect", help="mask sensitive keywords and write an encrypted mapping")
    protect.add_argument("input")
    protect.add_argument("--keywords", help="YAML file with keywords and regex patterns")
    protect.add_argument("--custom-keywords", help="plain-text file of custom keywords separated by newline, 、, or ； (see references/custom-keywords.txt)")
    protect.add_argument("--term", action="append", default=[], help="ad hoc keyword to mask; may be repeated")
    protect.add_argument("--preset", action="append", default=[], choices=["cn-sensitive"], help="built-in pattern preset; may be repeated")
    protect.add_argument("--out", required=True, help="masked output file")
    protect.add_argument("--map", required=True, help="encrypted mapping output file")
    protect.add_argument("--opaque", action="store_true", help="use generic [[K_0001]] placeholders instead of typed prefixes")
    protect.add_argument("--safe-name", action="store_true", help="replace output basenames with neutral rkm-* names to avoid leaking source titles")
    protect.add_argument("--dry-run", action="store_true", help="preview candidate masks without writing any file")
    protect.add_argument("--report", help="write a JSON processing report to this path (no raw values)")
    protect.add_argument("--force", action="store_true", help="mask even if the input already contains [[...]] placeholders")
    protect.set_defaults(func=cmd_protect)

    scan = sub.add_parser("scan", help="preview candidate masks without writing files or a mapping")
    scan.add_argument("input")
    scan.add_argument("--keywords", help="YAML file with keywords and regex patterns")
    scan.add_argument("--custom-keywords", help="plain-text file of custom keywords separated by newline, 、, or ； (see references/custom-keywords.txt)")
    scan.add_argument("--term", action="append", default=[], help="ad hoc keyword to mask; may be repeated")
    scan.add_argument("--preset", action="append", default=[], choices=["cn-sensitive"], help="built-in pattern preset; may be repeated")
    scan.add_argument("--opaque", action="store_true", help="use generic [[K_0001]] placeholders instead of typed prefixes")
    scan.add_argument("--show-values", action="store_true", help="show full raw candidate values (local terminal only; off by default)")
    scan.add_argument("--json", action="store_true", help="print machine-readable JSON")
    scan.add_argument("--report", help="write the scan report to this JSON path")
    scan.set_defaults(func=cmd_scan)

    verify = sub.add_parser("verify", help="verify placeholders in an edited masked file")
    verify.add_argument("input")
    verify.add_argument("--map", required=True, help="encrypted mapping file")
    verify.add_argument("--json", action="store_true", help="print machine-readable JSON")
    verify.add_argument("--repair", action="store_true", help="repair malformed placeholders into a copy (requires --out)")
    verify.add_argument("--out", help="write a repaired copy of the document to this path")
    verify.add_argument("--report", help="write the verify report to this JSON path (no raw values)")
    verify.set_defaults(func=cmd_verify)

    restore = sub.add_parser("restore", help="restore placeholders from an encrypted mapping")
    restore.add_argument("input")
    restore.add_argument("--map", required=True, help="encrypted mapping file")
    restore.add_argument("--out", required=True, help="restored output file")
    restore.add_argument("--allow-warnings", action="store_true", help="restore even if verification reports warnings")
    restore.set_defaults(func=cmd_restore)

    args = parser.parse_args(argv)
    return args.func(args)


def cmd_protect(args: argparse.Namespace) -> int:
    input_path = Path(args.input)
    output_path = Path(args.out)
    map_path = Path(args.map)
    if args.safe_name:
        safe_id = secrets.token_hex(4)
        output_path = unique_path(output_path.with_name(f"rkm-masked-{safe_id}{output_path.suffix or input_path.suffix}"))
        map_path = unique_path(map_path.with_name(f"rkm-map-{safe_id}.json"))
    rules = load_rules(
        Path(args.keywords) if args.keywords else None,
        args.term,
        args.preset,
        Path(args.custom_keywords) if args.custom_keywords else None,
    )
    if not rules:
        raise SystemExit("No keywords or patterns were provided. Use --keywords, --custom-keywords, or --term.")

    if args.dry_run:
        report = build_scan_report(input_path, rules, args.opaque, show_values=False)
        print_scan_report(report)
        print("Dry run: no files were written.")
        if args.report:
            write_json_report(args.report, report)
        return 0

    if not args.force:
        existing = PLACEHOLDER_RE.findall(read_document_text(input_path))
        if existing:
            raise SystemExit(
                f"Input already contains {len(existing)} placeholder-like token(s); it may already be masked. "
                "Re-masking would nest placeholders and break restoration. Pass --force to override."
            )

    suffix = input_path.suffix.lower()
    if suffix in TEXT_SUFFIXES:
        text = read_document_text(input_path)
        selected = select_matches(text, rules)
        records, edits = build_records_and_edits(selected, args.opaque)
        masked = apply_spans(text, edits)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        write_text_exact(output_path, masked)
        total_spans = len(edits)
    elif suffix in WORD_SUFFIXES:
        records, masked, total_spans = mask_word(input_path, output_path, rules, args.opaque)
    else:
        raise SystemExit(f"Unsupported file type: {input_path.suffix}")

    payload = {
        "version": 1,
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source_file": str(input_path),
        "masked_file": str(output_path),
        "opaque": bool(args.opaque),
        "rules": [rule_to_dict(rule) for rule in rules],
        "records": records,
    }
    password = get_password(args)
    write_encrypted_json(map_path, payload, password)

    remaining = select_matches(masked, rules)
    remaining_categories = sorted({"K" if args.opaque else normalize_category(match.category) for match in remaining})

    print(f"Masked file: {output_path}")
    print(f"Encrypted mapping: {map_path}")
    print(f"Unique placeholders: {len(records)}")
    print(f"Total masked spans: {total_spans}")
    if remaining:
        print(f"WARNING: {len(remaining)} sensitive span(s) are still detectable in the masked output (possible under-masking).")
        print(f"Categories: {', '.join(remaining_categories)}")
        print("Review the masked file and refine keywords/patterns before sending it to an AI model.")

    if args.report:
        write_json_report(
            args.report,
            {
                "command": "protect",
                "created_at": payload["created_at"],
                "source_file": str(input_path),
                "masked_file": str(output_path),
                "map_file": str(map_path),
                "unique_placeholders": len(records),
                "total_masked_spans": total_spans,
                "by_category": dict(Counter(record["category"] for record in records)),
                "placeholders": [
                    {"placeholder": record["placeholder"], "category": record["category"], "source": record["source"]}
                    for record in records
                ],
                "under_masking": {"detected": len(remaining), "categories": remaining_categories},
            },
        )
        print(f"Report: {args.report}")
    return 0


def build_records_and_edits(selected: list[Match], opaque: bool) -> tuple[list[dict[str, str]], list[tuple[int, int, str]]]:
    placeholder_by_value: dict[tuple[str, str], str] = {}
    records: list[dict[str, str]] = []
    counters: dict[str, int] = {}
    edits: list[tuple[int, int, str]] = []
    for match in selected:
        category = "K" if opaque else normalize_category(match.category)
        key = (category, match.value)
        placeholder = placeholder_by_value.get(key)
        if placeholder is None:
            counters[category] = counters.get(category, 0) + 1
            placeholder = f"[[{category}_{counters[category]:04d}]]"
            placeholder_by_value[key] = placeholder
            records.append(
                {
                    "placeholder": placeholder,
                    "value": match.value,
                    "category": category,
                    "source": match.source,
                }
            )
        edits.append((match.start, match.end, placeholder))
    return records, edits


def apply_spans(text: str, edits: list[tuple[int, int, str]]) -> str:
    for start, end, replacement in sorted(edits, key=lambda item: item[0], reverse=True):
        text = text[:start] + replacement + text[end:]
    return text


def cmd_scan(args: argparse.Namespace) -> int:
    input_path = Path(args.input)
    rules = load_rules(
        Path(args.keywords) if args.keywords else None,
        args.term,
        args.preset,
        Path(args.custom_keywords) if args.custom_keywords else None,
    )
    if not rules:
        raise SystemExit("No keywords or patterns were provided. Use --keywords, --custom-keywords, or --term.")
    report = build_scan_report(input_path, rules, args.opaque, show_values=args.show_values)
    if args.report:
        write_json_report(args.report, report)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_scan_report(report)
        if args.report:
            print(f"Report: {args.report}")
    return 0


def build_scan_report(input_path: Path, rules: list[Rule], opaque: bool, *, show_values: bool) -> dict[str, Any]:
    text = read_document_text(input_path)
    selected = select_matches(text, rules)
    records, edits = build_records_and_edits(selected, opaque)
    occurrences = Counter(placeholder for _, _, placeholder in edits)
    candidates = [
        {
            "placeholder": record["placeholder"],
            "category": record["category"],
            "source": record["source"],
            "occurrences": occurrences[record["placeholder"]],
            "value": record["value"] if show_values else redact_value(record["value"]),
        }
        for record in records
    ]
    return {
        "command": "scan",
        "input": str(input_path),
        "unique_values": len(records),
        "total_spans": len(edits),
        "by_category": dict(Counter(record["category"] for record in records)),
        "values_shown": bool(show_values),
        "candidates": candidates,
    }


def redact_value(value: str) -> str:
    length = len(value)
    if length <= 1:
        return "*"
    if length <= 3:
        return value[0] + "*" * (length - 1)
    return value[0] + "*" * (length - 2) + value[-1]


def print_scan_report(report: dict[str, Any]) -> None:
    print("Scan Report (no files written)")
    print(f"Input: {report['input']}")
    print(f"Candidates: {report['unique_values']} unique value(s) across {report['total_spans']} span(s)")
    if report["by_category"]:
        summary = ", ".join(f"{category}={count}" for category, count in sorted(report["by_category"].items()))
        print(f"By category: {summary}")
    if not report["values_shown"]:
        print("(values redacted; pass --show-values to reveal them on a local terminal)")
    for candidate in report["candidates"]:
        print(f"- [{candidate['category']}] {candidate['value']}  x{candidate['occurrences']}  ({candidate['source']})")


def write_json_report(path: str, data: dict[str, Any]) -> None:
    report_path = Path(path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    for index in range(2, 1000):
        candidate = path.with_name(f"{path.stem}-{index}{path.suffix}")
        if not candidate.exists():
            return candidate
    raise SystemExit(f"Could not create a unique output path near: {path}")


def cmd_verify(args: argparse.Namespace) -> int:
    password = get_password(args)
    mapping = read_encrypted_json(Path(args.map), password)
    input_path = Path(args.input)
    text = read_document_text(input_path)
    report = verify_text(text, mapping)

    repair_summary: dict[str, Any] | None = None
    if args.repair:
        if not args.out:
            raise SystemExit("--repair requires --out to write the repaired file.")
        expected = {record["placeholder"] for record in mapping.get("records", [])}
        repaired, unrepaired = apply_repairs(input_path, Path(args.out), expected)
        report = verify_text(read_document_text(Path(args.out)), mapping)
        repair_summary = {"out": str(args.out), "repaired": repaired, "unrepaired": unrepaired}

    if args.report:
        data = dict(report)
        data["command"] = "verify"
        data["input"] = str(input_path)
        if repair_summary is not None:
            data["repair"] = repair_summary
        write_json_report(args.report, data)

    if args.json:
        out = dict(report)
        if repair_summary is not None:
            out["repair"] = repair_summary
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        if repair_summary is not None:
            print_repair_summary(repair_summary)
        print_verify_report(report)
        if args.report:
            print(f"Report: {args.report}")
    return 0 if report["status"] == "PASS" else 2


def apply_repairs(input_path: Path, output_path: Path, expected: set[str]) -> tuple[list[dict[str, str]], list[str]]:
    suffix = input_path.suffix.lower()
    if suffix in TEXT_SUFFIXES:
        text = read_document_text(input_path)
        edits, repaired, unrepaired = compute_repairs(text, expected)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        write_text_exact(output_path, apply_spans(text, edits))
        return repaired, unrepaired
    if suffix in WORD_SUFFIXES:
        return repair_word(input_path, output_path, expected)
    raise SystemExit(f"Unsupported file type: {input_path.suffix}")


def compute_repairs(text: str, expected: set[str]) -> tuple[list[tuple[int, int, str]], list[dict[str, str]], list[str]]:
    canonical_by_key = {placeholder_key(placeholder): placeholder for placeholder in expected}
    edits: list[tuple[int, int, str]] = []
    repaired: list[dict[str, str]] = []
    unrepaired: list[str] = []
    for match in MALFORMED_RE.finditer(text):
        token = match.group(0)
        target = canonical_by_key.get(placeholder_key(token))
        if target is not None:
            edits.append((match.start(), match.end(), target))
            repaired.append({"from": token, "to": target})
        else:
            unrepaired.append(token)
    return edits, repaired, unrepaired


def placeholder_key(token: str) -> tuple[str, int] | str:
    inner = token.strip("[]【】").replace("-", "_").strip()
    match = re.match(r"([A-Z][A-Z0-9]*)_0*(\d+)$", inner)
    if match:
        return match.group(1), int(match.group(2))
    return inner


def print_repair_summary(summary: dict[str, Any]) -> None:
    print("Repair Summary")
    print(f"Repaired file: {summary['out']}")
    if summary["repaired"]:
        print(f"Repaired {len(summary['repaired'])} malformed placeholder(s):")
        for item in summary["repaired"]:
            print(f"- {item['from']} -> {item['to']}")
    if summary["unrepaired"]:
        print(f"Could not repair {len(summary['unrepaired'])} token(s) (no matching placeholder):")
        for token in summary["unrepaired"]:
            print(f"- {token}")
    print()


def cmd_restore(args: argparse.Namespace) -> int:
    password = get_password(args)
    mapping = read_encrypted_json(Path(args.map), password)
    input_path = Path(args.input)
    text = read_document_text(input_path)
    report = verify_text(text, mapping)
    if report["status"] != "PASS" and not args.allow_warnings:
        print_verify_report(report)
        print("Refusing to restore because verification reported warnings. Re-run with --allow-warnings to override.", file=sys.stderr)
        return 2

    records = mapping["records"]
    output_path = Path(args.out)
    suffix = input_path.suffix.lower()
    if suffix in TEXT_SUFFIXES:
        restored = restore_text(text, records)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        write_text_exact(output_path, restored)
    elif suffix in WORD_SUFFIXES:
        restore_word(input_path, output_path, records)
    else:
        raise SystemExit(f"Unsupported file type: {input_path.suffix}")
    print(f"Restored file: {args.out}")
    return 0


def load_rules(
    path: Path | None,
    terms: Iterable[str],
    presets: Iterable[str] = (),
    custom_path: Path | None = None,
) -> list[Rule]:
    rules: list[Rule] = []
    for preset in presets:
        rules.extend(builtin_preset_rules(preset))
    if custom_path:
        for keyword in load_custom_keywords(custom_path):
            rules.append(Rule(category="custom", value=keyword, source="custom-file"))
    if path:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if isinstance(data, list):
            rules.extend(Rule(category="K", value=str(item), source="keywords") for item in data if str(item).strip())
        elif isinstance(data, dict):
            rules.extend(parse_keywords(data.get("keywords", {})))
            patterns = data.get("patterns", {})
            if isinstance(patterns, dict):
                for category, pattern in patterns.items():
                    if pattern:
                        rules.append(Rule(category=str(category), pattern=str(pattern), source="pattern"))
        else:
            raise SystemExit(f"Unsupported keyword file shape: {path}")

    for term in terms:
        if term.strip():
            rules.append(Rule(category="K", value=term.strip(), source="term"))
    return rules


def rule_to_dict(rule: Rule) -> dict[str, str]:
    data = {"category": rule.category, "source": rule.source}
    if rule.value is not None:
        data["value"] = rule.value
    if rule.pattern is not None:
        data["pattern"] = rule.pattern
    return data


def rule_from_dict(data: Any) -> Rule | None:
    if not isinstance(data, dict):
        return None
    category = str(data.get("category") or "K")
    value = data.get("value")
    pattern = data.get("pattern")
    source = str(data.get("source") or "mapping")
    if value is not None:
        return Rule(category=category, value=str(value), source=source)
    if pattern is not None:
        return Rule(category=category, pattern=str(pattern), source=source)
    return None


def rules_from_mapping(mapping: dict[str, Any]) -> list[Rule]:
    rules: list[Rule] = []
    for item in mapping.get("rules", []):
        rule = rule_from_dict(item)
        if rule is not None:
            rules.append(rule)
    return rules


def load_custom_keywords(path: Path) -> list[str]:
    """Load custom keywords from a plain-text file.

    Each keyword sits on its own line, or several keywords share a line
    separated by the Chinese punctuation 、 or ；. Blank lines and lines whose
    first non-space character is '#' (comments) are ignored. Original order is
    preserved and duplicates are dropped so placeholders stay stable.
    """
    raw = path.read_text(encoding="utf-8")
    keywords: list[str] = []
    seen: set[str] = set()
    for line in raw.splitlines():
        if line.lstrip().startswith("#"):
            continue
        for token in re.split(r"[、；]+", line):
            keyword = token.strip()
            if keyword and keyword not in seen:
                seen.add(keyword)
                keywords.append(keyword)
    return keywords


def builtin_preset_rules(name: str) -> list[Rule]:
    if name != "cn-sensitive":
        raise SystemExit(f"Unsupported preset: {name}")
    date_gap = r"[ \t　·.．。]*"
    wrapped_year = rf"[【\[\(（]?{date_gap}[12][0-9]{{3}}{date_gap}[】\]\)）]?"
    wrapped_month = rf"[【\[\(（]?{date_gap}[0-9０-９]{{1,2}}{date_gap}[】\]\)）]?"
    wrapped_day = rf"[【\[\(（]?{date_gap}[0-9０-９]{{1,2}}{date_gap}[】\]\)）]?"
    date_part = rf"{wrapped_year}{date_gap}年{date_gap}{wrapped_month}{date_gap}月(?:{date_gap}{wrapped_day}{date_gap}日)?"
    return [
        Rule(category="organization", pattern=r"(?:(?![与和及暨、])[\u4e00-\u9fffA-Za-z0-9（）()·]){2,40}(?:公司|集团|委员会|管委会|财政局|办公室|中心|分局|总局|部门|银行)", source="preset:cn-sensitive"),
        Rule(category="person", pattern=r"(?:姓[·.．。… \t　]{0,8}名|联系人及电话|联系人及联系方式|联系人|经办人|负责人|申请人|填报人|制表人|审核人|审批人|签发人|法定代表人|姓名)[：:·.．。 \t　]*(?:\n+|[：: \t　]+)(?![\u7532\u4e59\u4e19\u4e01\u620a]\u65b9)([\u4e00-\u9fff]{2,4})", source="preset:cn-sensitive"),
        Rule(category="address", pattern=r"(?:公司注册地址|注册地址|联系人地址|联系地址|通讯地址|通信地址|办公地址|经营地址|住所地|住所|地址)[：:·.．。 \t　]*(?:\n+|[：: \t　]+)([^\n\r]{4,160}(?:路|街|道|大道|号|弄|巷|栋|座|楼|层|室|单元|园|区|院|村|大厦|广场|中心|WORLD)[^\n\r]{0,80})", source="preset:cn-sensitive"),
        Rule(category="address", pattern=r"(?:北京市|上海市|天津市|重庆市|深圳市|广州市|杭州市|南京市|成都市|武汉市|西安市|苏州市|东莞市|佛山市|珠海市|龙岗区|南山区|福田区|罗湖区|宝安区|坂田街道)(?:(?!公司|集团|协议|合同|项目|以下简称|与|就|达成|[。；;]).){4,100}(?:路|街|道|大道|号|弄|巷|栋|座|楼|层|室|单元|园|区|院|村|大厦|广场|中心|WORLD)(?:(?!公司|集团|协议|合同|项目|以下简称|与|就|达成|[。；;]).){0,60}", source="preset:cn-sensitive"),
        Rule(category="bank", pattern=r"(?:开户行|开户银行)[：:·.．。 \t　]*(?:\n+|[：: \t　]+)([^\n\r]{2,100}(?:银行|支行|分行|营业部|信用社)[^\n\r]{0,60})", source="preset:cn-sensitive"),
        Rule(category="bank_account", pattern=r"(?:银行账号|银行帐号|银行账户|银行帐户|账号|帐号|账户|帐户)[：:·.．。 \t　]*(?:\n+|[：: \t　]+)(?:[_＿\s]+)?([0-9０-９](?:[0-9０-９\s_＿-]*[0-9０-９]){7,29})(?:[_＿\s]+)?", source="preset:cn-sensitive"),
        Rule(category="tax_no", pattern=r"(?:税号|纳税人识别号|统一社会信用代码)[：:·.．。 \t　]*(?:\n+|[：: \t　]+)([0-9A-Z]{10,30})", source="preset:cn-sensitive"),
        Rule(category="duration_part", pattern=r"(?:合作期限|合同期限|协议期限|服务期限|有效期|期限)[^，。；;\n]{0,16}?为[：:·.．。 \t　]*[【\[\(（][ \t　·.．。]*([0-9０-９一二三四五六七八九十百千万/／_＿-]+)(?=[ \t　·.．。]*[】\]\)）][ \t　·.．。]*(?:年|个月|月|日))", source="preset:cn-sensitive:component"),
        Rule(category="date_part", pattern=rf"[【\[\(（]{date_gap}([12][0-9]{{3}})(?={date_gap}[】\]\)）]{date_gap}年)", source="preset:cn-sensitive:component"),
        Rule(category="date_part", pattern=rf"年{date_gap}[【\[\(（]{date_gap}([0-9０-９]{{1,2}})(?={date_gap}[】\]\)）]{date_gap}月)", source="preset:cn-sensitive:component"),
        Rule(category="date_part", pattern=rf"月{date_gap}[【\[\(（]{date_gap}([0-9０-９]{{1,2}})(?={date_gap}[】\]\)）]{date_gap}日)", source="preset:cn-sensitive:component"),
        Rule(category="duration", pattern=r"(?:合作期限|合同期限|协议期限|服务期限|有效期|期限)[^，。；;\n]{0,16}?为[：:·.．。 \t　]*([【\[\(（]?[ \t　·.．。]*(?:[0-9０-９一二三四五六七八九十百千万/／_＿-]+)[ \t　·.．。]*[】\]\)）]?[ \t　·.．。]*(?:年|个月|月|日))", source="preset:cn-sensitive"),
        Rule(category="date", pattern=rf"{date_part}{date_gap}(?:起{date_gap})?(?:至|到|[-－—~～]){date_gap}{date_part}", source="preset:cn-sensitive"),
        Rule(category="date", pattern=rf"(?:{date_part}|[12][0-9]{{3}}{date_gap}年{date_gap}第{date_gap}[一二三四1-4]{date_gap}季度)", source="preset:cn-sensitive"),
        Rule(category="amount", pattern=r"(?:人民币|¥|￥)\s*[【\[\(（]?\s*(?:[0-9０-９]{1,3}(?:[,，][0-9０-９]{3})+(?:[.．][0-9０-９]+)?|[0-9０-９]+(?:[.．][0-9０-９]+)?)\s*[·.．\s]*[】\]\)）]?\s*(?:万元|亿元|元|万|亿)", source="preset:cn-sensitive"),
        Rule(category="amount", pattern=r"(?:人民币|¥|￥)?\s*(?:[0-9０-９]{1,3}(?:[,，][0-9０-９]{3})+(?:[.．][0-9０-９]+)?|[0-9０-９]+(?:[.．][0-9０-９]+)?)\s*(?:万元|亿元|元|万|亿)", source="preset:cn-sensitive"),
        Rule(category="amount", pattern=r"(?<![A-Za-z0-9])(?:[0-9０-９]{1,3}(?:[,，][0-9０-９]{3})+(?:[.．][0-9０-９]+)?|[0-9０-９]+[.．][0-9０-９]+)(?![A-Za-z0-9])", source="preset:cn-sensitive"),
        Rule(category="amount", pattern=r"[零〇一二三四五六七八九十百千][零〇一二三四五六七八九十百千万亿]*(?:点[零〇一二三四五六七八九]+)?(?:万元|亿元|元|万|亿)", source="preset:cn-sensitive"),
        Rule(category="phone", pattern=r"\b1[3-9]\d{9}\b", source="preset:cn-sensitive"),
        Rule(category="phone", pattern=r"\b0\d{2,3}[-－]?\d{7,8}\b", source="preset:cn-sensitive"),
        Rule(category="email", pattern=r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", source="preset:cn-sensitive"),
        Rule(category="id_card", pattern=r"\b\d{17}[\dXx]\b", source="preset:cn-sensitive"),
        Rule(category="bank_card", pattern=r"(?<![A-Za-z0-9])(?:[0-9０-９](?:[0-9０-９\s_＿-]*[0-9０-９]){11,18})(?![A-Za-z0-9])", source="preset:cn-sensitive"),
    ]


def parse_keywords(keywords: Any) -> list[Rule]:
    rules: list[Rule] = []
    if isinstance(keywords, list):
        return [Rule(category="K", value=str(item), source="keywords") for item in keywords if str(item).strip()]
    if not isinstance(keywords, dict):
        return rules
    for category, values in keywords.items():
        if isinstance(values, str):
            values = [values]
        if not isinstance(values, list):
            continue
        for value in values:
            value_str = str(value).strip()
            if value_str:
                rules.append(Rule(category=str(category), value=value_str, source="keywords"))
    return rules


def select_matches(text: str, rules: list[Rule]) -> list[Match]:
    matches: list[Match] = []
    for rule in rules:
        if rule.value:
            if is_preserved_label(rule.value):
                continue
            for found in re.finditer(re.escape(rule.value), text):
                matches.append(Match(found.start(), found.end(), rule.category, found.group(0), rule.source))
        elif rule.pattern:
            try:
                compiled = re.compile(rule.pattern)
            except re.error as exc:
                raise SystemExit(f"Invalid regex for {rule.category}: {exc}") from exc
            for found in compiled.finditer(text):
                start, end, value = selected_regex_span(found)
                if value and not is_preserved_label(value):
                    matches.append(Match(start, end, rule.category, value, rule.source))

    selected: list[Match] = []
    occupied: list[tuple[int, int]] = []
    for match in sorted(matches, key=match_sort_key):
        if any(not (match.end <= start or match.start >= end) for start, end in occupied):
            continue
        selected.append(match)
        occupied.append((match.start, match.end))
    return sorted(selected, key=lambda item: item.start)


def match_sort_key(match: Match) -> tuple[int, int, int]:
    if match.source in {"keywords", "custom-file", "term"}:
        priority = 0
    elif match.source.endswith(":component"):
        priority = 1
    else:
        priority = 2
    return priority, -(match.end - match.start), match.start


def is_preserved_label(value: str) -> bool:
    normalized = re.sub(r"[：:·.．。…\s]+", "", value)
    return normalized in PRESERVED_LABELS


def selected_regex_span(found: re.Match[str]) -> tuple[int, int, str]:
    for index, value in enumerate(found.groups(), start=1):
        if value:
            start, end = found.span(index)
            return start, end, value
    return found.start(), found.end(), found.group(0)


def restore_text(text: str, records: list[dict[str, str]]) -> str:
    value_by_placeholder = {record["placeholder"]: record["value"] for record in records}
    return PLACEHOLDER_RE.sub(lambda m: value_by_placeholder.get(m.group(0), m.group(0)), text)


def read_document_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in TEXT_SUFFIXES:
        return path.read_text(encoding="utf-8-sig")
    if suffix in WORD_SUFFIXES:
        return load_word_text_model(path).text
    raise SystemExit(f"Unsupported file type: {path.suffix}")


def write_text_exact(path: Path, text: str) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write(text)


def mask_word(input_path: Path, output_path: Path, rules: list[Rule], opaque: bool) -> tuple[list[dict[str, str]], str, int]:
    if input_path.suffix.lower() == DOCX_SUFFIX and output_path.suffix.lower() != DOC_SUFFIX:
        return mask_docx(input_path, output_path, rules, opaque)
    with tempfile.TemporaryDirectory(prefix="rkm-word-") as tmp:
        tmp_dir = Path(tmp)
        work_input = input_path
        if input_path.suffix.lower() == DOC_SUFFIX:
            work_input = tmp_dir / "input.docx"
            convert_word_document(input_path, work_input)
        work_output = output_path if output_path.suffix.lower() != DOC_SUFFIX else tmp_dir / "masked.docx"
        records, masked, applied = mask_docx(work_input, work_output, rules, opaque)
        if output_path.suffix.lower() == DOC_SUFFIX:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            convert_word_document(work_output, output_path)
        return records, masked, applied


def mask_docx(input_path: Path, output_path: Path, rules: list[Rule], opaque: bool) -> tuple[list[dict[str, str]], str, int]:
    model = load_docx_text_model(input_path)
    selected = select_matches(model.text, rules)
    records, edits = build_records_and_edits(selected, opaque)
    applied = apply_docx_xml_edits(model, edits)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    save_docx_text_model(input_path, output_path, model)
    masked = rebuild_docx_model_text(model)
    return records, masked, applied


def restore_word(input_path: Path, output_path: Path, records: list[dict[str, str]]) -> None:
    if input_path.suffix.lower() == DOCX_SUFFIX and output_path.suffix.lower() != DOC_SUFFIX:
        restore_docx(input_path, output_path, records)
        return
    with tempfile.TemporaryDirectory(prefix="rkm-word-") as tmp:
        tmp_dir = Path(tmp)
        work_input = input_path
        if input_path.suffix.lower() == DOC_SUFFIX:
            work_input = tmp_dir / "input.docx"
            convert_word_document(input_path, work_input)
        work_output = output_path if output_path.suffix.lower() != DOC_SUFFIX else tmp_dir / "restored.docx"
        restore_docx(work_input, work_output, records)
        if output_path.suffix.lower() == DOC_SUFFIX:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            convert_word_document(work_output, output_path)


def repair_word(input_path: Path, output_path: Path, expected: set[str]) -> tuple[list[dict[str, str]], list[str]]:
    if input_path.suffix.lower() == DOCX_SUFFIX and output_path.suffix.lower() != DOC_SUFFIX:
        model = load_docx_text_model(input_path)
        edits, repaired, unrepaired = compute_repairs(model.text, expected)
        apply_docx_xml_edits(model, edits)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        save_docx_text_model(input_path, output_path, model)
        return repaired, unrepaired
    with tempfile.TemporaryDirectory(prefix="rkm-word-") as tmp:
        tmp_dir = Path(tmp)
        work_input = input_path
        if input_path.suffix.lower() == DOC_SUFFIX:
            work_input = tmp_dir / "input.docx"
            convert_word_document(input_path, work_input)
        model = load_docx_text_model(work_input)
        edits, repaired, unrepaired = compute_repairs(model.text, expected)
        apply_docx_xml_edits(model, edits)
        work_output = output_path if output_path.suffix.lower() != DOC_SUFFIX else tmp_dir / "repaired.docx"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        save_docx_text_model(work_input, work_output, model)
        if output_path.suffix.lower() == DOC_SUFFIX:
            convert_word_document(work_output, output_path)
        return repaired, unrepaired


def restore_docx(input_path: Path, output_path: Path, records: list[dict[str, str]]) -> None:
    model = load_docx_text_model(input_path)
    value_by_placeholder = {record["placeholder"]: record["value"] for record in records}
    edits: list[tuple[int, int, str]] = []
    for match in PLACEHOLDER_RE.finditer(model.text):
        placeholder = match.group(0)
        if placeholder in value_by_placeholder:
            edits.append((match.start(), match.end(), value_by_placeholder[placeholder]))
    apply_docx_xml_edits(model, edits)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    save_docx_text_model(input_path, output_path, model)


def load_word_text_model(path: Path) -> DocxTextModel:
    if path.suffix.lower() == DOCX_SUFFIX:
        return load_docx_text_model(path)
    if path.suffix.lower() == DOC_SUFFIX:
        with tempfile.TemporaryDirectory(prefix="rkm-word-") as tmp:
            converted = Path(tmp) / "input.docx"
            convert_word_document(path, converted)
            return load_docx_text_model(converted)
    raise SystemExit(f"Unsupported file type: {path.suffix}")


def convert_word_document(input_path: Path, output_path: Path) -> None:
    input_path = input_path.resolve()
    output_path = output_path.resolve()
    if input_path.suffix.lower() not in WORD_SUFFIXES or output_path.suffix.lower() not in WORD_SUFFIXES:
        raise SystemExit(f"Unsupported Word conversion: {input_path.suffix} -> {output_path.suffix}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if input_path.suffix.lower() == output_path.suffix.lower():
        shutil.copy2(input_path, output_path)
        return
    errors: list[str] = []
    if convert_word_with_com(input_path, output_path, errors):
        return
    if convert_word_with_libreoffice(input_path, output_path, errors):
        return
    details = " ".join(errors).strip()
    if details:
        details = " " + details
    raise SystemExit(
        "Cannot convert legacy .doc files locally. Install Microsoft Word or LibreOffice/soffice, "
        f"or convert the file to .docx first.{details}"
    )


def convert_word_with_com(input_path: Path, output_path: Path, errors: list[str]) -> bool:
    if sys.platform != "win32":
        return False
    powershell = shutil.which("powershell.exe") or shutil.which("powershell")
    if not powershell:
        errors.append("PowerShell was not found for Word COM conversion.")
        return False
    file_format = 16 if output_path.suffix.lower() == DOCX_SUFFIX else 0
    script = r"""
$ErrorActionPreference = 'Stop'
$word = $null
$doc = $null
try {
  $word = New-Object -ComObject Word.Application
  $word.Visible = $false
  $word.DisplayAlerts = 0
  $doc = $word.Documents.Open($env:RKM_WORD_INPUT, $false, $true, $false)
  $doc.SaveAs2($env:RKM_WORD_OUTPUT, [int]$env:RKM_WORD_FORMAT)
} finally {
  if ($doc -ne $null) { $doc.Close($false) | Out-Null }
  if ($word -ne $null) { $word.Quit() | Out-Null }
}
"""
    env = os.environ.copy()
    env["RKM_WORD_INPUT"] = str(input_path)
    env["RKM_WORD_OUTPUT"] = str(output_path)
    env["RKM_WORD_FORMAT"] = str(file_format)
    creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    result = subprocess.run(
        [powershell, "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-Command", script],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        creationflags=creationflags,
        timeout=120,
    )
    if result.returncode == 0 and output_path.exists():
        return True
    message = (result.stderr or result.stdout).strip()
    errors.append(f"Word COM conversion failed: {message or 'unknown error'}.")
    return False


def convert_word_with_libreoffice(input_path: Path, output_path: Path, errors: list[str]) -> bool:
    executable = find_libreoffice()
    if not executable:
        errors.append("LibreOffice/soffice was not found.")
        return False
    target_ext = output_path.suffix.lower().lstrip(".")
    with tempfile.TemporaryDirectory(prefix="rkm-lo-") as tmp:
        tmp_dir = Path(tmp)
        result = subprocess.run(
            [executable, "--headless", "--convert-to", target_ext, "--outdir", str(tmp_dir), str(input_path)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=120,
        )
        converted = tmp_dir / f"{input_path.stem}.{target_ext}"
        if not converted.exists():
            matches = list(tmp_dir.glob(f"*.{target_ext}"))
            converted = matches[0] if matches else converted
        if result.returncode == 0 and converted.exists():
            shutil.copy2(converted, output_path)
            return True
        message = (result.stderr or result.stdout).strip()
        errors.append(f"LibreOffice conversion failed: {message or 'unknown error'}.")
        return False


def find_libreoffice() -> str | None:
    for name in ("soffice", "libreoffice"):
        found = shutil.which(name)
        if found:
            return found
    candidates = [
        Path(os.environ.get("ProgramFiles", "")) / "LibreOffice" / "program" / "soffice.exe",
        Path(os.environ.get("ProgramFiles(x86)", "")) / "LibreOffice" / "program" / "soffice.exe",
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return None


def load_docx_text_model(path: Path) -> DocxTextModel:
    try:
        from lxml import etree
    except Exception as exc:  # pragma: no cover
        raise SystemExit("Missing dependency: lxml. Install with: python -m pip install lxml") from exc

    parser = etree.XMLParser(resolve_entities=False, recover=True)
    text_parts: list[str] = []
    segments: list[DocxTextSegment] = []
    parts: dict[str, DocxXmlPart] = {}
    position = 0
    with zipfile.ZipFile(path) as package:
        for info in package.infolist():
            if not is_docx_text_xml(info.filename):
                continue
            raw = package.read(info.filename)
            try:
                root = etree.fromstring(raw, parser)
            except Exception:
                continue
            part = DocxXmlPart(info.filename, root)
            before = position
            position = append_docx_xml_text(part, text_parts, segments, position)
            if position > before:
                parts[info.filename] = part
                text_parts.append("\n")
                position += 1
    if text_parts and text_parts[-1] == "\n":
        text_parts.pop()
    return DocxTextModel("".join(text_parts), segments, parts)


def is_docx_text_xml(name: str) -> bool:
    return name.startswith("word/") and name.endswith(".xml")


def append_docx_xml_text(
    part: DocxXmlPart,
    text_parts: list[str],
    segments: list[DocxTextSegment],
    position: int,
) -> int:
    current_paragraph: Any = None
    for element in part.root.iter():
        for attr_name, text in iter_visible_text_values(element):
            paragraph = nearest_word_paragraph(element)
            if current_paragraph is not None and paragraph is not current_paragraph:
                text_parts.append("\n")
                position += 1
            current_paragraph = paragraph
            text_parts.append(text)
            start = position
            position += len(text)
            segments.append(DocxTextSegment(element, start, position, part.name, attr_name))
    return position


VISIBLE_TEXT_ATTRS = {"string", "title", "descr"}


def iter_visible_text_values(element: Any) -> Iterable[tuple[str | None, str]]:
    if isinstance(getattr(element, "tag", None), str) and element.tag.endswith("}t"):
        text = element.text or ""
        if text:
            yield None, text
    for attr_name, value in element.attrib.items():
        if attr_local_name(attr_name) in VISIBLE_TEXT_ATTRS and value:
            yield attr_name, value


def attr_local_name(name: str) -> str:
    return name.rsplit("}", 1)[-1]


def nearest_word_paragraph(element: Any) -> Any:
    parent = element.getparent()
    while parent is not None:
        if isinstance(getattr(parent, "tag", None), str) and parent.tag.endswith("}p"):
            return parent
        parent = parent.getparent()
    return element.getparent()


def apply_docx_xml_edits(model: DocxTextModel, edits: list[tuple[int, int, str]]) -> int:
    applied = 0
    for start, end, replacement in sorted(edits, key=lambda item: item[0], reverse=True):
        affected = [segment for segment in model.segments if segment.start < end and segment.end > start]
        if not affected:
            continue
        covered = sum(min(segment.end, end) - max(segment.start, start) for segment in affected)
        if covered != end - start:
            continue
        first = affected[0]
        last = affected[-1]
        for segment in affected:
            text = segment_text(segment)
            local_start = max(0, start - segment.start)
            local_end = min(len(text), end - segment.start)
            if segment is first:
                keep_left = text[:local_start]
                keep_right = text[local_end:] if segment is last else ""
                set_segment_text(segment, keep_left + replacement + keep_right)
            elif segment is last:
                set_segment_text(segment, text[local_end:])
            else:
                set_segment_text(segment, "")
            model.parts[segment.part_name].changed = True
        applied += 1
    return applied


def segment_text(segment: DocxTextSegment) -> str:
    if segment.attr_name is None:
        return segment.element.text or ""
    return segment.element.attrib.get(segment.attr_name, "")


def set_segment_text(segment: DocxTextSegment, value: str) -> None:
    if segment.attr_name is None:
        segment.element.text = value
    else:
        segment.element.attrib[segment.attr_name] = value


def rebuild_docx_model_text(model: DocxTextModel) -> str:
    text_parts: list[str] = []
    position = 0
    for part in model.parts.values():
        position = append_docx_xml_text(part, text_parts, [], position)
        if position:
            text_parts.append("\n")
            position += 1
    if text_parts and text_parts[-1] == "\n":
        text_parts.pop()
    return "".join(text_parts)


def save_docx_text_model(input_path: Path, output_path: Path, model: DocxTextModel) -> None:
    from lxml import etree

    with zipfile.ZipFile(input_path, "r") as source, zipfile.ZipFile(output_path, "w") as target:
        for info in source.infolist():
            part = model.parts.get(info.filename)
            if part is not None and part.changed:
                data = etree.tostring(part.root, encoding="UTF-8", xml_declaration=True, standalone=True)
            else:
                data = source.read(info.filename)
            target.writestr(info, data)


def normalize_category(category: str) -> str:
    aliases = {
        "organization": "ORG",
        "organizations": "ORG",
        "org": "ORG",
        "orgs": "ORG",
        "company": "ORG",
        "companies": "ORG",
        "person": "PERSON",
        "persons": "PERSON",
        "people": "PERSON",
        "name": "PERSON",
        "names": "PERSON",
        "project": "PROJECT",
        "projects": "PROJECT",
        "contract": "CONTRACT",
        "contracts": "CONTRACT",
        "contract_no": "CONTRACT",
        "contract_numbers": "CONTRACT",
        "phone": "PHONE",
        "email": "EMAIL",
        "id": "ID",
        "id_card": "ID",
        "date": "DATE",
        "date_part": "DATE",
        "dates": "DATE",
        "amount": "AMOUNT",
        "amounts": "AMOUNT",
        "money": "AMOUNT",
        "duration": "DURATION",
        "duration_part": "DURATION",
        "durations": "DURATION",
        "term": "DURATION",
        "terms": "DURATION",
        "address": "ADDRESS",
        "addresses": "ADDRESS",
        "location": "ADDRESS",
        "locations": "ADDRESS",
        "bank": "BANK",
        "bank_name": "BANK",
        "bank_account": "BANKACCOUNT",
        "bank_accounts": "BANKACCOUNT",
        "tax": "TAX",
        "tax_no": "TAX",
        "tax_number": "TAX",
    }
    key = category.strip().lower().replace("-", "_").replace(" ", "_")
    if key in aliases:
        return aliases[key]
    normalized = re.sub(r"[^A-Za-z0-9]", "", category).upper()
    return normalized or "K"


def get_password(args: argparse.Namespace) -> bytes:
    dpapi_file = getattr(args, "dpapi_password_file", None)
    if dpapi_file:
        sealed = base64.b64decode(Path(dpapi_file).read_text(encoding="utf-8").strip())
        password = dpapi_unseal(sealed).decode("utf-8").strip()
    elif args.password_file:
        password = Path(args.password_file).read_text(encoding="utf-8").strip()
    else:
        password = os.environ.get(args.key_env)
    if not password:
        if sys.stdin.isatty():
            password = getpass.getpass(f"Mapping password ({args.key_env}): ")
        else:
            raise SystemExit(f"Set {args.key_env}, or pass --password-file / --dpapi-password-file for non-interactive use.")
    if len(password) < 8:
        raise SystemExit("Mapping password must be at least 8 characters.")
    return password.encode("utf-8")


def cmd_seal_password(args: argparse.Namespace) -> int:
    password = os.environ.get(args.key_env)
    if not password and sys.stdin.isatty():
        password = getpass.getpass(f"Mapping password to seal ({args.key_env}): ")
    if not password:
        raise SystemExit(f"Set {args.key_env} or run on an interactive terminal to seal a password.")
    if len(password) < 8:
        raise SystemExit("Mapping password must be at least 8 characters.")
    sealed = dpapi_seal(password.encode("utf-8"))
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(base64.b64encode(sealed).decode("ascii"), encoding="utf-8")
    print(f"Sealed password file: {out_path}")
    print("Use it with: --dpapi-password-file " + str(out_path))
    print("This file can only be unsealed by the current Windows user account on this machine.")
    return 0


def dpapi_seal(data: bytes) -> bytes:
    return _dpapi_call(data, encrypt=True)


def dpapi_unseal(blob: bytes) -> bytes:
    return _dpapi_call(blob, encrypt=False)


def _dpapi_call(data: bytes, *, encrypt: bool) -> bytes:
    if sys.platform != "win32":
        raise SystemExit("DPAPI password sealing is only available on Windows.")
    import ctypes
    from ctypes import wintypes

    class DATA_BLOB(ctypes.Structure):
        _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]

    buffer = ctypes.create_string_buffer(data, len(data))
    blob_in = DATA_BLOB(len(data), ctypes.cast(buffer, ctypes.POINTER(ctypes.c_char)))
    blob_out = DATA_BLOB()
    crypt32 = ctypes.windll.crypt32
    function = crypt32.CryptProtectData if encrypt else crypt32.CryptUnprotectData
    # CRYPTPROTECT_UI_FORBIDDEN = 0x1 keeps the call non-interactive.
    ok = function(ctypes.byref(blob_in), None, None, None, None, 0x1, ctypes.byref(blob_out))
    if not ok:
        action = "seal" if encrypt else "unseal"
        raise SystemExit(f"Windows DPAPI failed to {action} the password (error {ctypes.GetLastError()}).")
    try:
        return ctypes.string_at(blob_out.pbData, blob_out.cbData)
    finally:
        ctypes.windll.kernel32.LocalFree(blob_out.pbData)


def derive_key(password: bytes, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=KDF_ITERATIONS)
    return kdf.derive(password)


def write_encrypted_json(path: Path, payload: dict[str, Any], password: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    salt = os.urandom(16)
    nonce = os.urandom(12)
    key = derive_key(password, salt)
    ciphertext = AESGCM(key).encrypt(nonce, json.dumps(payload, ensure_ascii=False).encode("utf-8"), None)
    envelope = {
        "rkm": 1,
        "alg": "AES-256-GCM",
        "kdf": "PBKDF2-HMAC-SHA256",
        "iterations": KDF_ITERATIONS,
        "salt": b64(salt),
        "nonce": b64(nonce),
        "ciphertext": b64(ciphertext),
    }
    path.write_text(json.dumps(envelope, ensure_ascii=False, indent=2), encoding="utf-8")


def read_encrypted_json(path: Path, password: bytes) -> dict[str, Any]:
    envelope = json.loads(path.read_text(encoding="utf-8"))
    if envelope.get("rkm") != 1:
        raise SystemExit("Unsupported mapping file format.")
    salt = b64decode(envelope["salt"])
    nonce = b64decode(envelope["nonce"])
    ciphertext = b64decode(envelope["ciphertext"])
    try:
        plaintext = AESGCM(derive_key(password, salt)).decrypt(nonce, ciphertext, None)
    except Exception as exc:
        raise SystemExit("Could not decrypt mapping file. Check the mapping password and file.") from exc
    return json.loads(plaintext.decode("utf-8"))


RESIDUAL_MIN_LEN = 4
ASCII_VALUE_RE = re.compile(r"[A-Za-z0-9._%+@-]+")


def occurs_standalone(value: str, text: str) -> bool:
    """True if value appears as a standalone token, not merely as a substring of a larger ASCII token."""
    if ASCII_VALUE_RE.fullmatch(value):
        return re.search(r"(?<![A-Za-z0-9])" + re.escape(value) + r"(?![A-Za-z0-9])", text) is not None
    return value in text


def verify_text(text: str, mapping: dict[str, Any]) -> dict[str, Any]:
    records = mapping.get("records", [])
    expected = {record["placeholder"] for record in records}
    found = set(PLACEHOLDER_RE.findall(text))
    missing = sorted(expected - found)
    unknown = sorted(found - expected)
    malformed = sorted(set(MALFORMED_RE.findall(text)))
    residual = [
        {"placeholder": record["placeholder"], "category": record["category"]}
        for record in records
        if len(record["value"]) >= RESIDUAL_MIN_LEN and occurs_standalone(record["value"], text)
    ]
    unmapped_sensitive = find_unmapped_sensitive(text, mapping)
    status = "PASS" if not missing and not unknown and not malformed and not residual and not unmapped_sensitive else "WARNING"
    return {
        "status": status,
        "expected_count": len(expected),
        "found_count": len(found),
        "missing": missing,
        "unknown": unknown,
        "malformed": malformed,
        "residual": residual,
        "unmapped_sensitive": unmapped_sensitive,
    }


def find_unmapped_sensitive(text: str, mapping: dict[str, Any]) -> list[dict[str, Any]]:
    rules = rules_from_mapping(mapping)
    if not rules:
        return []
    mapped_values = {record.get("value") for record in mapping.get("records", [])}
    items: list[dict[str, Any]] = []
    seen: set[tuple[str, str, int, int]] = set()
    for match in select_matches(text, rules):
        if PLACEHOLDER_RE.search(match.value):
            continue
        if match.value in mapped_values:
            continue
        category = normalize_category(match.category)
        key = (category, match.source, match.start, match.end)
        if key in seen:
            continue
        seen.add(key)
        items.append({"category": category, "source": match.source})
    return items


def print_verify_report(report: dict[str, Any]) -> None:
    print("Verify Report")
    print(f"Status: {report['status']}")
    print(f"Expected placeholders: {report['expected_count']}")
    print(f"Found placeholders: {report['found_count']}")
    for key in ("missing", "unknown", "malformed"):
        values = report[key]
        if values:
            print(f"{key.capitalize()}:")
            for value in values:
                print(f"- {value}")
    residual = report.get("residual", [])
    if residual:
        print(f"Residual original values: {len(residual)} (raw values hidden; original keywords still present in the document)")
        for item in residual:
            print(f"- {item['placeholder']} ({item['category']})")
    unmapped_sensitive = report.get("unmapped_sensitive", [])
    if unmapped_sensitive:
        print(f"Unmapped sensitive spans: {len(unmapped_sensitive)} (raw values hidden; values were not present in the encrypted mapping)")
        for item in unmapped_sensitive:
            print(f"- {item['category']} ({item['source']})")


def b64(value: bytes) -> str:
    return base64.b64encode(value).decode("ascii")


def b64decode(value: str) -> bytes:
    return base64.b64decode(value.encode("ascii"))


if __name__ == "__main__":
    raise SystemExit(main())
