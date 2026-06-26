#!/usr/bin/env python3.11
"""Infer metric/dimension/time semantics from query catalog."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterator, List, Optional

AGG_RE = re.compile(r"\b(sum|count|avg|min|max)\s*\(", re.IGNORECASE)
TIME_NAME_RE = re.compile(r"\b(date|dt|day|week|month|year|time|hour)\b", re.IGNORECASE)
TIME_FIELD_RE = re.compile(
    r"(^|_)(dt|date|day|week|month|year|time|hour|minute|second|timestamp|ts|at)$",
    re.IGNORECASE,
)
WHERE_RE = re.compile(
    r"\bwhere\b(?P<body>.*?)(\bgroup\s+by\b|\border\s+by\b|\bhaving\b|\blimit\b|\bunion\b|$)",
    re.IGNORECASE | re.DOTALL,
)
IDENT_OR_FUNC = r"(?:[a-zA-Z_][\w$]*(?:\.[a-zA-Z_][\w$]*)*|`[^`]+`|\"[^\"]+\"|\[[^\]]+\]|[a-zA-Z_][\w$]*\s*\([^()]*\))"
BETWEEN_PRED_RE = re.compile(
    rf"^\s*(?P<expr>{IDENT_OR_FUNC})\s+between\s+(?P<left>.+?)\s+and\s+(?P<right>.+?)\s*$",
    re.IGNORECASE | re.DOTALL,
)
IN_PRED_RE = re.compile(
    rf"^\s*(?P<expr>{IDENT_OR_FUNC})\s+(?P<op>in|not\s+in)\s*\((?P<vals>.*)\)\s*$",
    re.IGNORECASE | re.DOTALL,
)
IS_NULL_PRED_RE = re.compile(
    rf"^\s*(?P<expr>{IDENT_OR_FUNC})\s+is\s+(?P<op>not\s+null|null)\s*$",
    re.IGNORECASE | re.DOTALL,
)
CMP_PRED_RE = re.compile(
    rf"^\s*(?P<expr>{IDENT_OR_FUNC})\s*(?P<op>>=|<=|<>|!=|=|>|<|like|ilike)\s*(?P<val>.+?)\s*$",
    re.IGNORECASE | re.DOTALL,
)
BETWEEN_SCAN_RE = re.compile(
    rf"(?P<expr>{IDENT_OR_FUNC})\s+between\s+(?P<left>.+?)\s+and\s+(?P<right>.+?)(?=(\s+and\s+|\s+or\s+|$))",
    re.IGNORECASE | re.DOTALL,
)
IN_SCAN_RE = re.compile(
    rf"(?P<expr>{IDENT_OR_FUNC})\s+(?P<op>in|not\s+in)\s*\((?P<vals>[^)]*)\)",
    re.IGNORECASE | re.DOTALL,
)
CMP_SCAN_RE = re.compile(
    rf"(?P<expr>{IDENT_OR_FUNC})\s*(?P<op>>=|<=|<>|!=|=|>|<|like|ilike)\s*(?P<val>(?:'[^']*'|\"[^\"]*\"|\{{\{{[^}}]+\}}\}}|:[a-zA-Z_][a-zA-Z0-9_]*|\$[a-zA-Z_][a-zA-Z0-9_]*|\?|[0-9]+(?:\.[0-9]+)?|[a-zA-Z_][a-zA-Z0-9_\.]*))",
    re.IGNORECASE | re.DOTALL,
)
PLACEHOLDER_RE = re.compile(r"(\{\{[^}]+\}\}|:[a-zA-Z_][a-zA-Z0-9_]*|\$[a-zA-Z_][a-zA-Z0-9_]*|\?)")
NUMBER_RE = re.compile(r"^-?\d+(?:\.\d+)?$")
INT_RE = re.compile(r"^-?\d+$")
DATE_FUNCTION_RE = re.compile(
    r"^(date|to_date|str_to_date|date_trunc|timestamp|to_timestamp)\s*\(|^cast\s*\(.*\s+as\s+(date|timestamp).*$",
    re.IGNORECASE,
)

DATE_STRING_FORMATS = [
    (re.compile(r"^\d{4}-\d{2}-\d{2}$"), "yyyy-mm-dd"),
    (re.compile(r"^\d{4}/\d{2}/\d{2}$"), "yyyy/mm/dd"),
    (re.compile(r"^\d{8}$"), "yyyymmdd"),
    (re.compile(r"^\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}$"), "yyyy-mm-dd hh:mm:ss"),
    (
        re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+\-]\d{2}:?\d{2})?$"),
        "iso-8601",
    ),
]


def extract_select_clause(sql: str) -> str:
    normalized = " ".join(sql.strip().split())
    lower = normalized.lower()
    s_idx = lower.find("select ")
    if s_idx < 0:
        return ""
    f_idx = lower.find(" from ", s_idx)
    if f_idx < 0:
        return normalized[s_idx + 7 :]
    return normalized[s_idx + 7 : f_idx]


def split_select_items(select_clause: str) -> List[str]:
    items: List[str] = []
    buf: List[str] = []
    depth = 0
    for ch in select_clause:
        if ch == "(":
            depth += 1
        elif ch == ")" and depth > 0:
            depth -= 1
        if ch == "," and depth == 0:
            item = "".join(buf).strip()
            if item:
                items.append(item)
            buf = []
            continue
        buf.append(ch)
    final = "".join(buf).strip()
    if final:
        items.append(final)
    return items


def extract_alias(expr: str, idx: int) -> str:
    m = re.search(r"\s+as\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*$", expr, re.IGNORECASE)
    if m:
        return m.group(1)

    tail = expr.strip().split()
    if len(tail) > 1 and re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", tail[-1]):
        return tail[-1]

    return f"col_{idx:02d}"


def detect_role(alias: str, expr: str) -> str:
    if AGG_RE.search(expr):
        return "metric"

    if TIME_NAME_RE.search(alias) or TIME_NAME_RE.search(expr):
        return "time"

    return "dimension"


def detect_grain(fields: List[Dict]) -> str:
    has_time = any(f["role"] == "time" for f in fields)
    dim_count = sum(1 for f in fields if f["role"] in {"dimension", "time"})
    metric_count = sum(1 for f in fields if f["role"] == "metric")

    if has_time and metric_count:
        return "time_series"
    if dim_count == 0 and metric_count:
        return "single_value"
    if dim_count >= 1 and metric_count:
        return "categorical"
    return "detail"


def to_field_name(expr: str) -> str:
    cleaned = expr.strip().strip("()")
    ident_list = re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", cleaned)
    if not ident_list:
        return cleaned.lower()
    return ident_list[-1].lower()


def is_time_field(expr: str, field: str) -> bool:
    return bool(TIME_NAME_RE.search(expr) or TIME_NAME_RE.search(field) or TIME_FIELD_RE.search(field))


def normalize_operator(op: str) -> str:
    return " ".join(op.strip().lower().split())


def extract_where_clause(sql: str) -> str:
    normalized = " ".join(sql.strip().split())
    m = WHERE_RE.search(normalized)
    if not m:
        return ""
    return m.group("body").strip()


def has_outer_parentheses(expr: str) -> bool:
    expr = expr.strip()
    if len(expr) < 2 or expr[0] != "(" or expr[-1] != ")":
        return False

    depth = 0
    quote: Optional[str] = None
    for i, ch in enumerate(expr):
        if quote:
            if ch == quote and (i == 0 or expr[i - 1] != "\\"):
                quote = None
            continue
        if ch in {"'", '"', "`"}:
            quote = ch
            continue
        if ch == "(":
            depth += 1
            continue
        if ch == ")":
            depth -= 1
            if depth == 0 and i < len(expr) - 1:
                return False
            continue

    return depth == 0 and quote is None


def strip_outer_parentheses(expr: str) -> str:
    out = expr.strip()
    while has_outer_parentheses(out):
        out = out[1:-1].strip()
    return out


def split_top_level_boolean(expr: str, keyword: str) -> List[str]:
    keyword = keyword.lower()
    lower = expr.lower()

    parts: List[str] = []
    last = 0
    i = 0
    depth = 0
    quote: Optional[str] = None
    between_pending = False

    while i < len(expr):
        ch = expr[i]

        if quote:
            if ch == quote and (i == 0 or expr[i - 1] != "\\"):
                quote = None
            i += 1
            continue

        if ch in {"'", '"', "`"}:
            quote = ch
            i += 1
            continue

        if ch == "(":
            depth += 1
            i += 1
            continue

        if ch == ")":
            depth = max(0, depth - 1)
            i += 1
            continue

        if depth == 0 and (ch.isalpha() or ch == "_"):
            start = i
            i += 1
            while i < len(expr) and (expr[i].isalnum() or expr[i] == "_"):
                i += 1
            token = lower[start:i]

            if token == "between":
                between_pending = True
                continue

            if token == "and" and between_pending:
                between_pending = False
                continue

            if token == keyword and not between_pending:
                part = expr[last:start].strip()
                if part:
                    parts.append(part)
                last = i
                continue

            continue

        i += 1

    tail = expr[last:].strip()
    if tail:
        parts.append(tail)

    return parts


def build_boolean_ast(expr: str) -> Dict:
    expr = strip_outer_parentheses(expr)
    if not expr:
        return {"type": "empty"}

    or_parts = split_top_level_boolean(expr, "or")
    if len(or_parts) > 1:
        return {"type": "or", "children": [build_boolean_ast(p) for p in or_parts]}

    and_parts = split_top_level_boolean(expr, "and")
    if len(and_parts) > 1:
        return {"type": "and", "children": [build_boolean_ast(p) for p in and_parts]}

    return {"type": "predicate", "text": strip_outer_parentheses(expr)}


def iter_predicates(ast: Dict) -> Iterator[str]:
    node_type = ast.get("type")
    if node_type == "predicate":
        text = ast.get("text", "").strip()
        if text:
            yield text
        return
    for child in ast.get("children", []):
        yield from iter_predicates(child)


def split_csv_top_level(text: str) -> List[str]:
    items: List[str] = []
    buf: List[str] = []
    depth = 0
    quote: Optional[str] = None

    for i, ch in enumerate(text):
        if quote:
            buf.append(ch)
            if ch == quote and (i == 0 or text[i - 1] != "\\"):
                quote = None
            continue

        if ch in {"'", '"', "`"}:
            quote = ch
            buf.append(ch)
            continue

        if ch == "(":
            depth += 1
            buf.append(ch)
            continue

        if ch == ")":
            depth = max(0, depth - 1)
            buf.append(ch)
            continue

        if ch == "," and depth == 0:
            item = "".join(buf).strip()
            if item:
                items.append(item)
            buf = []
            continue

        buf.append(ch)

    final = "".join(buf).strip()
    if final:
        items.append(final)
    return items


def parse_int_date_format(text: str) -> Optional[str]:
    if not re.fullmatch(r"\d+", text):
        return None

    if len(text) == 8:
        try:
            datetime.strptime(text, "%Y%m%d")
            return "yyyymmdd_int"
        except ValueError:
            return None

    if len(text) == 10:
        value = int(text)
        if 946684800 <= value <= 4102444800:
            return "unix_seconds_int"

    if len(text) == 13:
        value = int(text)
        if 946684800000 <= value <= 4102444800000:
            return "unix_milliseconds_int"

    return None


def parse_date_string_format(text: str) -> Optional[str]:
    for pattern, fmt in DATE_STRING_FORMATS:
        if pattern.fullmatch(text):
            # Validate yyyymmdd string to avoid 20249999 false positives.
            if fmt == "yyyymmdd":
                try:
                    datetime.strptime(text, "%Y%m%d")
                except ValueError:
                    return None
            return fmt
    return None


def parse_value_info(raw_value: str) -> Dict:
    value = raw_value.strip().rstrip(";").strip()

    if PLACEHOLDER_RE.search(value):
        return {
            "mode": "parameterized",
            "type": "parameter",
            "format": None,
            "is_date": False,
            "sample": value[:80],
        }

    if (value.startswith("'") and value.endswith("'")) or (value.startswith('"') and value.endswith('"')):
        inner = value[1:-1].strip()
        date_fmt = parse_date_string_format(inner)
        if date_fmt:
            return {
                "mode": "literal",
                "type": "date",
                "format": date_fmt,
                "is_date": True,
                "sample": value[:80],
            }
        int_date_fmt = parse_int_date_format(inner)
        if int_date_fmt:
            return {
                "mode": "literal",
                "type": "date",
                "format": int_date_fmt,
                "is_date": True,
                "sample": value[:80],
            }
        return {
            "mode": "literal",
            "type": "string",
            "format": None,
            "is_date": False,
            "sample": value[:80],
        }

    if DATE_FUNCTION_RE.search(value):
        return {
            "mode": "literal",
            "type": "date",
            "format": "date_function",
            "is_date": True,
            "sample": value[:80],
        }

    if INT_RE.fullmatch(value):
        int_date_fmt = parse_int_date_format(value)
        if int_date_fmt:
            return {
                "mode": "literal",
                "type": "date",
                "format": int_date_fmt,
                "is_date": True,
                "sample": value[:80],
            }
        return {
            "mode": "literal",
            "type": "number",
            "format": "integer",
            "is_date": False,
            "sample": value[:80],
        }

    if NUMBER_RE.fullmatch(value):
        return {
            "mode": "literal",
            "type": "number",
            "format": "float",
            "is_date": False,
            "sample": value[:80],
        }

    date_fmt = parse_date_string_format(value)
    if date_fmt:
        return {
            "mode": "literal",
            "type": "date",
            "format": date_fmt,
            "is_date": True,
            "sample": value[:80],
        }

    if value.lower() in {"current_date", "current_timestamp", "now()"}:
        return {
            "mode": "literal",
            "type": "date",
            "format": "date_keyword",
            "is_date": True,
            "sample": value[:80],
        }

    if re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_\.]*", value):
        return {
            "mode": "literal",
            "type": "identifier",
            "format": None,
            "is_date": False,
            "sample": value[:80],
        }

    return {
        "mode": "literal",
        "type": "unknown",
        "format": None,
        "is_date": False,
        "sample": value[:80],
    }


def summarize_value_infos(operator: str, value_infos: List[Dict]) -> Dict:
    op = normalize_operator(operator)

    modes = {v["mode"] for v in value_infos}
    types = {v["type"] for v in value_infos}
    formats = [v["format"] for v in value_infos if v.get("format")]
    all_date = all(v["is_date"] for v in value_infos if v["mode"] == "literal") and any(v["is_date"] for v in value_infos)
    any_date = any(v["is_date"] for v in value_infos)
    all_number = all(v["type"] == "number" for v in value_infos if v["mode"] == "literal") and any(
        v["type"] == "number" for v in value_infos
    )

    mode = "parameterized" if "parameterized" in modes else "literal"

    if op == "between":
        if any_date:
            value_type = "date_range"
        elif all_number:
            value_type = "number_range"
        else:
            value_type = "range"
    elif op in {"in", "not in"}:
        if all_date:
            value_type = "date_set"
        elif all_number:
            value_type = "number_set"
        elif types == {"string"}:
            value_type = "string_set"
        else:
            value_type = "set"
    else:
        value_type = value_infos[0]["type"] if value_infos else "unknown"

    value_format = None
    if formats:
        unique_formats = sorted(set(formats))
        value_format = unique_formats[0] if len(unique_formats) == 1 else "mixed"

    return {
        "value_mode": mode,
        "value_type": value_type,
        "value_format": value_format,
        "is_date_value": any_date,
    }


def infer_filter_widget(operator: str, is_time: bool, value_type: str) -> str:
    op = normalize_operator(operator)
    if op == "between":
        return "date_range" if is_time or value_type == "date_range" else "number_range"
    if op in {"in", "not in"}:
        return "multi_select"
    if op in {"like", "ilike"}:
        return "search"
    if op in {"is null", "is not null"}:
        return "select"
    if is_time:
        return "date_select"
    if value_type in {"number", "number_set", "number_range"}:
        return "number_input"
    return "select"


def parse_predicate(predicate: str, parse_mode: str) -> Optional[Dict]:
    text = strip_outer_parentheses(predicate.strip())
    if not text:
        return None

    m = BETWEEN_PRED_RE.match(text)
    if m:
        expr = m.group("expr").strip()
        left = parse_value_info(m.group("left"))
        right = parse_value_info(m.group("right"))
        summary = summarize_value_infos("between", [left, right])
        field = to_field_name(expr)
        time_field = is_time_field(expr, field) or summary["is_date_value"]
        value_type = summary["value_type"]
        if time_field and value_type == "range":
            value_type = "date_range"
        return {
            "field": field,
            "expression": expr,
            "operator": "between",
            "value_mode": summary["value_mode"],
            "value_type": value_type,
            "value_format": summary["value_format"],
            "value_sample": f"{left['sample']} and {right['sample']}"[:80],
            "suggested_widget": infer_filter_widget("between", time_field, value_type),
            "is_time": time_field,
            "source_clause": "where",
            "parse_mode": parse_mode,
        }

    m = IN_PRED_RE.match(text)
    if m:
        expr = m.group("expr").strip()
        op = normalize_operator(m.group("op"))
        values = split_csv_top_level(m.group("vals"))
        infos = [parse_value_info(v) for v in values if v.strip()]
        if not infos:
            infos = [parse_value_info(m.group("vals"))]
        summary = summarize_value_infos(op, infos)
        field = to_field_name(expr)
        time_field = is_time_field(expr, field) or summary["is_date_value"]
        return {
            "field": field,
            "expression": expr,
            "operator": op,
            "value_mode": summary["value_mode"],
            "value_type": summary["value_type"],
            "value_format": summary["value_format"],
            "value_sample": ", ".join(v["sample"] for v in infos)[:80],
            "suggested_widget": infer_filter_widget(op, time_field, summary["value_type"]),
            "is_time": time_field,
            "source_clause": "where",
            "parse_mode": parse_mode,
        }

    m = IS_NULL_PRED_RE.match(text)
    if m:
        expr = m.group("expr").strip()
        op = normalize_operator(f"is {m.group('op')}")
        field = to_field_name(expr)
        time_field = is_time_field(expr, field)
        return {
            "field": field,
            "expression": expr,
            "operator": op,
            "value_mode": "literal",
            "value_type": "null_check",
            "value_format": None,
            "value_sample": op,
            "suggested_widget": infer_filter_widget(op, time_field, "null_check"),
            "is_time": time_field,
            "source_clause": "where",
            "parse_mode": parse_mode,
        }

    m = CMP_PRED_RE.match(text)
    if m:
        expr = m.group("expr").strip()
        op = normalize_operator(m.group("op"))
        info = parse_value_info(m.group("val"))
        summary = summarize_value_infos(op, [info])
        field = to_field_name(expr)
        time_field = is_time_field(expr, field) or summary["is_date_value"]
        value_type = summary["value_type"]
        if time_field and value_type in {"unknown", "identifier", "parameter"}:
            value_type = "date"
        return {
            "field": field,
            "expression": expr,
            "operator": op,
            "value_mode": summary["value_mode"],
            "value_type": value_type,
            "value_format": summary["value_format"],
            "value_sample": info["sample"][:80],
            "suggested_widget": infer_filter_widget(op, time_field, value_type),
            "is_time": time_field,
            "source_clause": "where",
            "parse_mode": parse_mode,
        }

    return None


def covered_by_span(spans: List[tuple[int, int]], start: int, end: int) -> bool:
    for s, e in spans:
        if start >= s and end <= e:
            return True
    return False


def regex_fallback_filters(where_clause: str) -> List[Dict]:
    candidates: List[Dict] = []
    spans: List[tuple[int, int]] = []

    for pattern in (BETWEEN_SCAN_RE, IN_SCAN_RE, CMP_SCAN_RE):
        for m in pattern.finditer(where_clause):
            start, end = m.span()
            if covered_by_span(spans, start, end):
                continue
            spans.append((start, end))
            parsed = parse_predicate(m.group(0), parse_mode="regex_fallback")
            if parsed:
                candidates.append(parsed)

    return candidates


def dedupe_filters(filters: List[Dict]) -> List[Dict]:
    seen = set()
    out: List[Dict] = []
    for item in filters:
        key = (
            item.get("field"),
            item.get("operator"),
            item.get("value_mode"),
            item.get("value_type"),
            item.get("value_sample"),
        )
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def extract_dsl_filters(sql: str) -> List[Dict]:
    where_clause = extract_where_clause(sql)
    if not where_clause:
        return []

    ast = build_boolean_ast(where_clause)
    parsed: List[Dict] = []
    for predicate in iter_predicates(ast):
        item = parse_predicate(predicate, parse_mode="dsl_ast")
        if item:
            parsed.append(item)

    if not parsed:
        parsed = regex_fallback_filters(where_clause)

    return dedupe_filters(parsed)


def infer_query_semantics(query: Dict) -> Dict:
    sql = query.get("sql", "")
    select_clause = extract_select_clause(sql)
    items = split_select_items(select_clause)

    fields: List[Dict] = []
    for idx, item in enumerate(items, start=1):
        alias = extract_alias(item, idx)
        role = detect_role(alias, item)
        fields.append(
            {
                "name": alias,
                "expression": item,
                "role": role,
                "is_aggregate": bool(AGG_RE.search(item)),
            }
        )

    grain = detect_grain(fields)
    dsl_filters = extract_dsl_filters(sql)
    dsl_filter_fields = [f["field"] for f in dsl_filters]

    return {
        "id": query.get("id"),
        "title": query.get("title", ""),
        "grain": grain,
        "field_count": len(fields),
        "fields": fields,
        "metrics": [f["name"] for f in fields if f["role"] == "metric"],
        "dimensions": [f["name"] for f in fields if f["role"] == "dimension"],
        "time_fields": [f["name"] for f in fields if f["role"] == "time"],
        "dsl_filters": dsl_filters,
        "dsl_filter_fields": dsl_filter_fields,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Infer semantics from query catalog")
    parser.add_argument("--input", required=True, help="Path to query_catalog.json")
    parser.add_argument("--output", required=True, help="Path to semantic_catalog.json")
    args = parser.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.output)

    payload = json.loads(in_path.read_text(encoding="utf-8"))
    queries = payload.get("queries", [])

    semantic_queries = [infer_query_semantics(q) for q in queries]

    result = {
        "source": payload.get("source", ""),
        "query_count": len(semantic_queries),
        "queries": semantic_queries,
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Inferred semantics for {len(semantic_queries)} queries -> {out_path}")


if __name__ == "__main__":
    main()
