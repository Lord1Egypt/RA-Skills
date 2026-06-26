#!/usr/bin/env python3
"""Field index utilities: lookup from openapi_field_index.json."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
INDEX_FILENAME = "openapi_field_index.json"
DEFAULT_DESC_MAX = 500
MIN_SUFFIX_LEN = 4
NOT_FOUND = "文档未收录"
FILTERED_HINT = (
    "说明或 key 已命中，但被 --path-contains / --path-prefix / --method / --operation-id 过滤清空；"
    "请放宽或去掉过滤条件。"
)


@dataclass(frozen=True)
class Entry:
    key: str
    description: str
    source_file: str
    line: int
    http_method: str | None = None
    path: str | None = None
    operation_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "description": self.description,
            "source_file": self.source_file,
            "line": self.line,
            "http_method": self.http_method,
            "path": self.path,
            "operation_id": self.operation_id,
        }


def strip_cell(value: str) -> str:
    text = value.strip()
    if len(text) >= 2 and text[0] == "`" and text[-1] == "`":
        text = text[1:-1]
    return text.strip()


def entry_from_dict(item: dict[str, Any]) -> Entry | None:
    try:
        return Entry(
            key=str(item["key"]).strip(),
            description=str(item["description"]).strip(),
            source_file=str(item.get("source_file", "")).strip(),
            line=int(item.get("line", 0)),
            http_method=item.get("http_method"),
            path=item.get("path"),
            operation_id=item.get("operation_id"),
        )
    except (KeyError, TypeError, ValueError):
        return None


def load_index_payload(index_path: Path) -> tuple[list[Entry], dict[str, Any]]:
    if not index_path.is_file():
        print(
            f"错误: 未找到索引文件 {index_path}。请重新运行 swagger-skills 生成器。",
            file=sys.stderr,
        )
        raise SystemExit(2)
    try:
        data = json.loads(index_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"错误: 索引 JSON 无法解析: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
    raw = data.get("entries")
    if not isinstance(raw, list):
        print("错误: 索引 JSON 缺少有效的 entries 数组", file=sys.stderr)
        raise SystemExit(2)
    entries: list[Entry] = []
    for item in raw:
        if isinstance(item, dict):
            entry = entry_from_dict(item)
            if entry and entry.key and entry.description:
                entries.append(entry)
    meta = {
        "index_file": str(index_path.resolve()),
        "generated_utc": data.get("generated_utc"),
        "entry_count": len(entries),
    }
    return entries, meta


def canonical_api_path(path: str | None) -> str:
    if path is None or not str(path).strip():
        return ""
    normalized = str(path).strip().replace("\\", "/")
    if not normalized.startswith("/"):
        normalized = "/" + normalized
    normalized = normalized.rstrip("/")
    return re.sub(r"/v\d+$", "/{version}", normalized)


def entries_matching_route(
    entries: list[Entry],
    method: str | None,
    path_actual: str | None,
) -> list[Entry]:
    if not method or not path_actual:
        return []
    method_upper = method.strip().upper()
    want = canonical_api_path(path_actual)
    if not want:
        return []
    output: list[Entry] = []
    for entry in entries:
        if not entry.http_method or entry.http_method.strip().upper() != method_upper:
            continue
        if not entry.path:
            continue
        if canonical_api_path(entry.path) == want:
            output.append(entry)
    return output


def lookup_by_key(entries: list[Entry], query: str) -> list[Entry]:
    normalized = strip_cell(query).strip()
    if not normalized:
        return []
    exact = [entry for entry in entries if entry.key == normalized]
    if exact:
        return exact
    allow_suffix = len(normalized) >= MIN_SUFFIX_LEN or "." in normalized
    if not allow_suffix:
        return []
    suffix_dot = "." + normalized
    suffix_br = "]." + normalized
    return [
        entry
        for entry in entries
        if entry.key.endswith(suffix_dot) or entry.key.endswith(suffix_br)
    ]


def lookup_by_desc(entries: list[Entry], phrase: str, max_results: int) -> tuple[list[Entry], bool]:
    normalized = phrase.strip()
    if not normalized:
        return [], False
    matches = [entry for entry in entries if normalized in entry.description]
    if len(matches) <= max_results:
        return matches, False
    return matches[:max_results], True


def entry_passes_filters(
    entry: Entry,
    *,
    path_contains: str | None,
    path_prefix: str | None,
    method: str | None,
    operation_id_sub: str | None,
) -> bool:
    if method:
        if not entry.http_method or entry.http_method.upper() != method.strip().upper():
            return False
    if path_contains:
        if not entry.path or path_contains.strip() not in entry.path:
            return False
    if path_prefix:
        if not entry.path or not entry.path.startswith(path_prefix.strip()):
            return False
    if operation_id_sub:
        if not entry.operation_id or operation_id_sub.strip() not in entry.operation_id:
            return False
    return True


def apply_filters(
    matches: list[Entry],
    *,
    path_contains: str | None,
    path_prefix: str | None,
    method: str | None,
    operation_id_sub: str | None,
) -> tuple[list[Entry], bool]:
    if not (
        path_contains and path_contains.strip()
        or path_prefix and path_prefix.strip()
        or method and method.strip()
        or operation_id_sub and operation_id_sub.strip()
    ):
        return matches, False
    output = [
        entry
        for entry in matches
        if entry_passes_filters(
            entry,
            path_contains=path_contains,
            path_prefix=path_prefix,
            method=method,
            operation_id_sub=operation_id_sub,
        )
    ]
    return output, len(matches) > 0 and len(output) == 0


def cmd_index(_root: Path, _out_path: Path) -> int:
    print(
        "index 子命令暂不支持从 references 重建索引。"
        "请重新运行 swagger-skills 生成器（build_swagger_skill.py）以更新 openapi_field_index.json。",
        file=sys.stderr,
    )
    return 2


def cmd_lookup(
    *,
    index_path: Path,
    by_desc: bool,
    queries: list[str],
    max_desc: int,
    path_contains: str | None,
    path_prefix: str | None,
    method: str | None,
    operation_id_sub: str | None,
) -> int:
    entries, index_meta = load_index_payload(index_path)
    results: list[dict[str, Any]] = []
    all_ok = True

    for query in queries:
        if by_desc:
            matches, truncated = lookup_by_desc(entries, query, max_desc)
            mode = "by_desc"
        else:
            matches = lookup_by_key(entries, query)
            truncated = False
            mode = "by_key"

        pre_count = len(matches)
        matches, filtered_out = apply_filters(
            matches,
            path_contains=path_contains,
            path_prefix=path_prefix,
            method=method,
            operation_id_sub=operation_id_sub,
        )
        found = len(matches) > 0
        if not found:
            all_ok = False

        block: dict[str, Any] = {
            "query": query,
            "mode": mode,
            "found": found,
            "matches": [match.to_dict() for match in matches],
        }
        if truncated:
            block["truncated"] = True
            block["hint"] = f"命中超过 {max_desc} 条，已截断；请缩小关键词后重试。"
        if filtered_out:
            block["filtered_out"] = True
            block["pre_filter_count"] = pre_count
            block["hint"] = FILTERED_HINT
            block["not_found_reason"] = NOT_FOUND
        elif not found:
            block["not_found_reason"] = NOT_FOUND

        results.append(block)

    print(json.dumps({"index": index_meta, "results": results}, ensure_ascii=False, indent=2))
    return 0 if all_ok else 1


def ensure_utf8_stdout() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except (OSError, ValueError, AttributeError):
            pass


def main() -> int:
    ensure_utf8_stdout()
    parser = argparse.ArgumentParser(
        description="lookup：从 openapi_field_index.json 查询字段说明。",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("index", help="暂不支持；请重新运行 swagger-skills 生成器")

    lookup_parser = sub.add_parser("lookup", help="从索引 JSON 查询字段")
    lookup_parser.add_argument("--index", type=Path, default=None, metavar="FILE")
    lookup_parser.add_argument("--desc", action="store_true")
    lookup_parser.add_argument("--max", type=int, default=DEFAULT_DESC_MAX, metavar="N")
    lookup_parser.add_argument("--path-contains", default=None, metavar="SUB")
    lookup_parser.add_argument("--path-prefix", default=None, metavar="PREFIX")
    lookup_parser.add_argument("--method", default=None, metavar="VERB")
    lookup_parser.add_argument("--operation-id", default=None, metavar="SUB")
    lookup_parser.add_argument("queries", nargs="+")

    args = parser.parse_args()

    if args.command == "index":
        out = ROOT / INDEX_FILENAME
        return cmd_index(ROOT, out)

    index_path = args.index if args.index is not None else ROOT / INDEX_FILENAME
    return cmd_lookup(
        index_path=index_path,
        by_desc=args.desc,
        queries=list(args.queries),
        max_desc=max(1, args.max),
        path_contains=args.path_contains,
        path_prefix=args.path_prefix,
        method=args.method,
        operation_id_sub=args.operation_id,
    )


if __name__ == "__main__":
    sys.exit(main())
