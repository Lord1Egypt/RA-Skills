#!/usr/bin/env python3
"""Query stock quotes and manage a Markdown watchlist."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests

SEARCH_URL = "https://searchapi.eastmoney.com/api/suggest/get"
SEARCH_TOKEN = "D43BF722C8E33BDC906FB84D85E326E8"
QUOTE_URL = "https://push2.eastmoney.com/api/qt/stock/get"
REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
}
WATCHLIST_START = "<!-- stock-watchlist:start -->"
WATCHLIST_END = "<!-- stock-watchlist:end -->"
WATCHLIST_EXTENSIONS = {".md", ".markdown"}
WATCHLIST_ALLOWED_ROOTS_ENV = "STOCK_WATCHLIST_ALLOWED_ROOTS"
WATCHLIST_COLUMNS = [
    "query",
    "symbol",
    "quote_id",
    "name",
    "cost_price",
    "quantity",
    "note",
]
PRICE_FIELDS = {
    "current_price": "f43",
    "high_price": "f44",
    "low_price": "f45",
    "open_price": "f46",
    "volume": "f47",
    "amount": "f48",
    "code": "f57",
    "name": "f58",
    "market_code": "f59",
    "previous_close": "f60",
    "total_market_cap": "f116",
    "float_market_cap": "f117",
    "industry": "f127",
    "change_amount": "f169",
    "change_percent": "f170",
    "pe_ttm": "f162",
    "pb": "f167",
    "turnover_rate": "f168",
}


class StockWatchlistError(RuntimeError):
    """Raised when the script cannot resolve a query or watchlist document."""


@dataclass
class ResolvedSecurity:
    query: str
    code: str
    name: str
    symbol: str
    quote_id: str
    market: str
    security_type: str


def is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def is_watchlist_document(text: str) -> bool:
    return WATCHLIST_START in text and WATCHLIST_END in text


def allowed_watchlist_roots() -> list[Path]:
    roots = [Path.cwd().resolve()]
    raw_extra_roots = os.environ.get(WATCHLIST_ALLOWED_ROOTS_ENV, "")
    for item in raw_extra_roots.split(os.pathsep):
        stripped = item.strip()
        if not stripped:
            continue
        roots.append(Path(stripped).expanduser().resolve())
    unique_roots = []
    for root in roots:
        if root not in unique_roots:
            unique_roots.append(root)
    return unique_roots


def resolve_watchlist_path(raw_path: str) -> Path:
    candidate = Path(raw_path).expanduser().resolve()
    if candidate.suffix.lower() not in WATCHLIST_EXTENSIONS:
        raise StockWatchlistError(
            "Watchlist file must use a Markdown extension: .md or .markdown."
        )
    if not any(is_relative_to(candidate, root) for root in allowed_watchlist_roots()):
        allowed = ", ".join(str(root) for root in allowed_watchlist_roots())
        raise StockWatchlistError(
            "Watchlist path is outside allowed roots. "
            f"Allowed roots: {allowed}. "
            f"Use {WATCHLIST_ALLOWED_ROOTS_ENV} to add an explicit safe root."
        )
    return candidate


def create_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(REQUEST_HEADERS)
    return session


def scale_ratio(value: Any, factor: int) -> float | None:
    if value is None or value == "-":
        return None
    return round(float(value) / factor, 4)


def to_float(value: str | None) -> float | None:
    if value is None:
        return None
    stripped = value.strip()
    if not stripped:
        return None
    return float(stripped)


def to_int(value: str | None) -> int | None:
    if value is None:
        return None
    stripped = value.strip()
    if not stripped:
        return None
    return int(float(stripped))


def normalize_query(query: str) -> str:
    normalized = query.strip()
    if not normalized:
        raise StockWatchlistError("Empty query is not allowed.")
    return normalized


def normalize_lookup_key(value: str) -> str:
    return re.sub(r"[\s:._-]+", "", value).upper()


def infer_quote_id_from_symbol(query: str) -> str | None:
    normalized = normalize_lookup_key(query)
    match = re.fullmatch(r"(SH|SZ|HK)([A-Z0-9]+)", normalized)
    if not match:
        return None
    exchange, code = match.groups()
    if exchange == "SH" and re.fullmatch(r"\d{6}", code):
        return f"1.{code}"
    if exchange == "SZ" and re.fullmatch(r"\d{6}", code):
        return f"0.{code}"
    if exchange == "HK" and re.fullmatch(r"\d{1,5}", code):
        return f"116.{code.zfill(5)}"
    return None


def market_from_quote_id(quote_id: str) -> str:
    market_key = quote_id.split(".", 1)[0]
    if market_key in {"0", "1"}:
        return "CN"
    if market_key == "116":
        return "HK"
    if market_key in {"105", "106", "107"}:
        return "US"
    return "UNKNOWN"


def price_scale_for_quote(
    market: str, security_type: str, market_code: Any
) -> int:
    if market in {"HK", "US"}:
        return 1000
    if market == "CN" and (security_type == "基金" or market_code == 3):
        return 1000
    return 100


def symbol_from_quote_id(quote_id: str, code: str) -> str:
    market_key = quote_id.split(".", 1)[0]
    if market_key == "0" and re.fullmatch(r"\d{6}", code):
        return f"SZ{code}"
    if market_key == "1" and re.fullmatch(r"\d{6}", code):
        return f"SH{code}"
    if market_key == "116" and re.fullmatch(r"\d{1,5}", code):
        return f"HK{code.zfill(5)}"
    return code.upper()


def build_search_params(query: str, limit: int) -> dict[str, Any]:
    return {
        "input": query,
        "type": 14,
        "token": SEARCH_TOKEN,
        "count": limit,
    }


def search_securities(
    session: requests.Session, query: str, limit: int = 10
) -> list[dict[str, Any]]:
    response = session.get(
        SEARCH_URL,
        params=build_search_params(query, limit),
        timeout=10,
    )
    response.raise_for_status()
    payload = response.json()
    table = payload.get("QuotationCodeTable") or {}
    items = table.get("Data") or []
    results = []
    for item in items[:limit]:
        code = str(item.get("Code") or "").upper()
        quote_id = str(item.get("QuoteID") or "")
        if not code or not quote_id:
            continue
        results.append(
            {
                "query": query,
                "code": code,
                "name": item.get("Name") or "",
                "symbol": symbol_from_quote_id(quote_id, code),
                "quote_id": quote_id,
                "market": market_from_quote_id(quote_id),
                "security_type": item.get("SecurityTypeName") or "",
                "exchange": item.get("JYS") or "",
            }
        )
    return results


def score_candidate(query: str, candidate: dict[str, Any]) -> int:
    query_key = normalize_lookup_key(query)
    score = 0
    code_key = normalize_lookup_key(str(candidate["code"]))
    symbol_key = normalize_lookup_key(str(candidate["symbol"]))
    name_key = normalize_lookup_key(str(candidate["name"]))
    if query_key == symbol_key:
        score += 200
    if query_key == code_key:
        score += 180
    if query_key == name_key:
        score += 160
    if symbol_key.startswith(query_key):
        score += 50
    if code_key.startswith(query_key):
        score += 40
    if query_key and query_key in name_key:
        score += 30
    if candidate["market"] == "CN" and re.fullmatch(r"\d{6}", query_key):
        score += 10
    if candidate["security_type"] in {"沪A", "深A", "北A", "港股", "美股"}:
        score += 5
    if candidate["security_type"] in {"指数", "板块"}:
        score -= 20
    return score


def choose_candidate(query: str, candidates: list[dict[str, Any]]) -> dict[str, Any]:
    if not candidates:
        raise StockWatchlistError(f"No stock matched query: {query}")
    supported = [
        candidate for candidate in candidates if candidate["market"] in {"CN", "HK", "US"}
    ]
    if supported:
        candidates = supported
    ranked = sorted(
        candidates,
        key=lambda candidate: score_candidate(query, candidate),
        reverse=True,
    )
    return ranked[0]


def fetch_quote(session: requests.Session, quote_id: str) -> dict[str, Any]:
    fields = ",".join(PRICE_FIELDS.values())
    response = session.get(
        QUOTE_URL,
        params={"secid": quote_id, "fields": fields},
        timeout=10,
    )
    response.raise_for_status()
    payload = response.json()
    if payload.get("rc") != 0 or not payload.get("data"):
        raise StockWatchlistError(f"Quote request failed for {quote_id}: {payload}")
    return payload["data"]


def resolve_security(session: requests.Session, query: str) -> ResolvedSecurity:
    normalized = normalize_query(query)
    direct_quote_id = infer_quote_id_from_symbol(normalized)
    if direct_quote_id:
        quote = fetch_quote(session, direct_quote_id)
        code = str(quote.get(PRICE_FIELDS["code"]) or "").upper()
        name = str(quote.get(PRICE_FIELDS["name"]) or "")
        return ResolvedSecurity(
            query=normalized,
            code=code,
            name=name,
            symbol=symbol_from_quote_id(direct_quote_id, code),
            quote_id=direct_quote_id,
            market=market_from_quote_id(direct_quote_id),
            security_type="",
        )

    stripped = re.sub(r"^(SH|SZ|HK)[:\\-]?", "", normalized, flags=re.IGNORECASE)
    candidates = search_securities(session, stripped, limit=10)
    best = choose_candidate(normalized, candidates)
    return ResolvedSecurity(
        query=normalized,
        code=best["code"],
        name=best["name"],
        symbol=best["symbol"],
        quote_id=best["quote_id"],
        market=best["market"],
        security_type=best["security_type"],
    )


def build_quote_result(
    resolved: ResolvedSecurity, quote: dict[str, Any]
) -> dict[str, Any]:
    price_scale = price_scale_for_quote(
        resolved.market,
        resolved.security_type,
        quote.get(PRICE_FIELDS["market_code"]),
    )
    return {
        "query": resolved.query,
        "symbol": resolved.symbol,
        "quote_id": resolved.quote_id,
        "market": resolved.market,
        "security_type": resolved.security_type,
        "code": str(quote.get(PRICE_FIELDS["code"]) or resolved.code),
        "name": quote.get(PRICE_FIELDS["name"]) or resolved.name,
        "current_price": scale_ratio(quote.get(PRICE_FIELDS["current_price"]), price_scale),
        "change_amount": scale_ratio(quote.get(PRICE_FIELDS["change_amount"]), price_scale),
        "change_percent": scale_ratio(quote.get(PRICE_FIELDS["change_percent"]), 100),
        "open_price": scale_ratio(quote.get(PRICE_FIELDS["open_price"]), price_scale),
        "high_price": scale_ratio(quote.get(PRICE_FIELDS["high_price"]), price_scale),
        "low_price": scale_ratio(quote.get(PRICE_FIELDS["low_price"]), price_scale),
        "previous_close": scale_ratio(quote.get(PRICE_FIELDS["previous_close"]), price_scale),
        "volume": quote.get(PRICE_FIELDS["volume"]),
        "amount": quote.get(PRICE_FIELDS["amount"]),
        "total_market_cap": quote.get(PRICE_FIELDS["total_market_cap"]),
        "float_market_cap": quote.get(PRICE_FIELDS["float_market_cap"]),
        "industry": quote.get(PRICE_FIELDS["industry"]),
        "pe_ttm": scale_ratio(quote.get(PRICE_FIELDS["pe_ttm"]), 100),
        "pb": scale_ratio(quote.get(PRICE_FIELDS["pb"]), 100),
        "turnover_rate": scale_ratio(quote.get(PRICE_FIELDS["turnover_rate"]), 100),
    }


def split_watchlist_document(text: str) -> tuple[str, str, str]:
    start_index = text.find(WATCHLIST_START)
    end_index = text.find(WATCHLIST_END)
    if start_index == -1 or end_index == -1 or start_index > end_index:
        raise StockWatchlistError(
            "Watchlist document must contain stock-watchlist start/end markers."
        )
    prefix = text[: start_index + len(WATCHLIST_START)]
    table_text = text[start_index + len(WATCHLIST_START) : end_index]
    suffix = text[end_index:]
    return prefix, table_text, suffix


def parse_table_row(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        raise StockWatchlistError(f"Invalid Markdown table row: {line}")
    return [cell.strip() for cell in stripped.strip("|").split("|")]


def parse_watchlist_table(table_text: str) -> list[dict[str, str]]:
    lines = [line.rstrip() for line in table_text.splitlines() if line.strip()]
    if not lines:
        return []
    if len(lines) < 2:
        raise StockWatchlistError("Watchlist table is missing the separator row.")
    headers = parse_table_row(lines[0])
    if not set(WATCHLIST_COLUMNS).issubset(set(headers)):
        raise StockWatchlistError(
            "Watchlist table must include columns: "
            + ", ".join(WATCHLIST_COLUMNS)
        )
    rows = []
    for line in lines[2:]:
        values = parse_table_row(line)
        if len(values) != len(headers):
            raise StockWatchlistError(f"Table row has wrong column count: {line}")
        record = dict(zip(headers, values))
        rows.append({column: record.get(column, "").strip() for column in WATCHLIST_COLUMNS})
    return rows


def render_watchlist_table(rows: list[dict[str, str]]) -> str:
    matrix = [WATCHLIST_COLUMNS]
    for row in rows:
        matrix.append([str(row.get(column, "")) for column in WATCHLIST_COLUMNS])
    widths = [
        max(len(matrix[row_index][column_index]) for row_index in range(len(matrix)))
        for column_index in range(len(WATCHLIST_COLUMNS))
    ]

    def build_row(values: list[str]) -> str:
        padded = [
            values[index].ljust(widths[index]) for index in range(len(WATCHLIST_COLUMNS))
        ]
        return "| " + " | ".join(padded) + " |"

    header = build_row(WATCHLIST_COLUMNS)
    separator = "| " + " | ".join("-" * width for width in widths) + " |"
    body = [build_row([str(row.get(column, "")) for column in WATCHLIST_COLUMNS]) for row in rows]
    parts = [header, separator, *body]
    return "\n".join(parts)


def load_watchlist(path: Path) -> tuple[str, str, str, list[dict[str, str]]]:
    if not path.exists():
        raise StockWatchlistError(f"Watchlist file does not exist: {path}")
    text = path.read_text(encoding="utf-8")
    prefix, table_text, suffix = split_watchlist_document(text)
    rows = parse_watchlist_table(table_text)
    return prefix, table_text, suffix, rows


def save_watchlist(path: Path, prefix: str, suffix: str, rows: list[dict[str, str]]) -> None:
    table = render_watchlist_table(rows)
    content = prefix.rstrip() + "\n" + table + "\n" + suffix.lstrip()
    path.write_text(content, encoding="utf-8")


def format_decimal(value: float | None) -> str:
    if value is None:
        return ""
    text = f"{value:.4f}".rstrip("0").rstrip(".")
    return text or "0"


def format_integer(value: int | None) -> str:
    if value is None:
        return ""
    return str(value)


def build_watchlist_entry(
    resolved: ResolvedSecurity,
    query: str,
    cost_price: float | None,
    quantity: int | None,
    note: str,
) -> dict[str, str]:
    return {
        "query": query,
        "symbol": resolved.symbol,
        "quote_id": resolved.quote_id,
        "name": resolved.name,
        "cost_price": format_decimal(cost_price),
        "quantity": format_integer(quantity),
        "note": note.strip(),
    }


def build_watchlist_quote_row(
    row: dict[str, str], quote_result: dict[str, Any]
) -> dict[str, Any]:
    result = dict(quote_result)
    result["cost_price"] = to_float(row.get("cost_price"))
    result["quantity"] = to_int(row.get("quantity"))
    result["note"] = row.get("note") or ""
    result["profit_loss"] = None
    result["profit_loss_percent"] = None
    result["cost_value"] = None
    result["market_value"] = None
    cost_price = result["cost_price"]
    quantity = result["quantity"]
    current_price = result["current_price"]
    if cost_price is not None and quantity is not None and current_price is not None:
        cost_value = cost_price * quantity
        market_value = current_price * quantity
        profit_loss = market_value - cost_value
        result["cost_value"] = round(cost_value, 4)
        result["market_value"] = round(market_value, 4)
        result["profit_loss"] = round(profit_loss, 4)
        if cost_value:
            result["profit_loss_percent"] = round((profit_loss / cost_value) * 100, 4)
    return result


def summarize_watchlist(rows: list[dict[str, Any]]) -> dict[str, float | None]:
    total_cost = 0.0
    total_value = 0.0
    cost_rows = 0
    for row in rows:
        if row["cost_value"] is None or row["market_value"] is None:
            continue
        total_cost += row["cost_value"]
        total_value += row["market_value"]
        cost_rows += 1
    if not cost_rows:
        return {
            "positions": len(rows),
            "cost_positions": 0,
            "total_cost": None,
            "total_market_value": None,
            "total_profit_loss": None,
            "total_profit_loss_percent": None,
        }
    profit_loss = total_value - total_cost
    percent = (profit_loss / total_cost) * 100 if total_cost else None
    return {
        "positions": len(rows),
        "cost_positions": cost_rows,
        "total_cost": round(total_cost, 4),
        "total_market_value": round(total_value, 4),
        "total_profit_loss": round(profit_loss, 4),
        "total_profit_loss_percent": round(percent, 4) if percent is not None else None,
    }


def locate_entry(rows: list[dict[str, str]], query: str) -> int | None:
    lookup_key = normalize_lookup_key(query)
    for index, row in enumerate(rows):
        candidates = [row.get("query", ""), row.get("symbol", ""), row.get("quote_id", "")]
        if any(normalize_lookup_key(candidate) == lookup_key for candidate in candidates if candidate):
            return index
    return None


def command_search(args: argparse.Namespace) -> dict[str, Any]:
    with create_session() as session:
        results = search_securities(session, normalize_query(args.query), args.limit)
    return {
        "command": "search",
        "query": args.query,
        "results": results,
    }


def command_quote(args: argparse.Namespace) -> dict[str, Any]:
    quotes = []
    with create_session() as session:
        for query in args.queries:
            resolved = resolve_security(session, query)
            quote = fetch_quote(session, resolved.quote_id)
            quotes.append(build_quote_result(resolved, quote))
    return {
        "command": "quote",
        "queries": args.queries,
        "results": quotes,
    }


def command_watchlist_init(args: argparse.Namespace) -> dict[str, Any]:
    target = resolve_watchlist_path(args.file)
    if target.exists():
        if not args.force:
            raise StockWatchlistError(
                f"Watchlist already exists: {target}. Use --force to overwrite it."
            )
        existing_text = target.read_text(encoding="utf-8")
        if not is_watchlist_document(existing_text):
            raise StockWatchlistError(
                "Refusing to overwrite a non-watchlist Markdown document."
            )
    asset_path = Path(__file__).resolve().parents[1] / "assets" / "watchlist-template.md"
    content = asset_path.read_text(encoding="utf-8")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return {
        "command": "watchlist-init",
        "file": str(target),
    }


def command_watchlist_show(args: argparse.Namespace) -> dict[str, Any]:
    target = resolve_watchlist_path(args.file)
    _, _, _, rows = load_watchlist(target)
    return {
        "command": "watchlist-show",
        "file": str(target),
        "rows": rows,
    }


def command_watchlist_sync(args: argparse.Namespace) -> dict[str, Any]:
    target = resolve_watchlist_path(args.file)
    prefix, _, suffix, rows = load_watchlist(target)
    synced_rows = []
    with create_session() as session:
        for row in rows:
            lookup = row.get("query") or row.get("symbol") or row.get("quote_id")
            if not lookup:
                raise StockWatchlistError(
                    "Each watchlist row must contain query, symbol, or quote_id."
                )
            resolved = resolve_security(session, lookup)
            synced_rows.append(
                build_watchlist_entry(
                    resolved=resolved,
                    query=row.get("query") or lookup,
                    cost_price=to_float(row.get("cost_price")),
                    quantity=to_int(row.get("quantity")),
                    note=row.get("note") or "",
                )
            )
    save_watchlist(target, prefix, suffix, synced_rows)
    return {
        "command": "watchlist-sync",
        "file": str(target),
        "rows": synced_rows,
    }


def command_watchlist_add(args: argparse.Namespace) -> dict[str, Any]:
    target = resolve_watchlist_path(args.file)
    prefix, _, suffix, rows = load_watchlist(target)
    with create_session() as session:
        resolved = resolve_security(session, args.query)
    entry = build_watchlist_entry(
        resolved=resolved,
        query=args.query,
        cost_price=args.cost_price,
        quantity=args.quantity,
        note=args.note or "",
    )
    existing_index = locate_entry(rows, args.query)
    if existing_index is None:
        existing_index = locate_entry(rows, resolved.symbol)
    action = "created"
    if existing_index is None:
        rows.append(entry)
    else:
        rows[existing_index] = entry
        action = "updated"
    save_watchlist(target, prefix, suffix, rows)
    return {
        "command": "watchlist-add",
        "file": str(target),
        "action": action,
        "entry": entry,
    }


def command_watchlist_remove(args: argparse.Namespace) -> dict[str, Any]:
    target = resolve_watchlist_path(args.file)
    prefix, _, suffix, rows = load_watchlist(target)
    index = locate_entry(rows, args.query)
    if index is None:
        raise StockWatchlistError(f"No watchlist row matched: {args.query}")
    removed = rows.pop(index)
    save_watchlist(target, prefix, suffix, rows)
    return {
        "command": "watchlist-remove",
        "file": str(target),
        "removed": removed,
    }


def command_watchlist_quote(args: argparse.Namespace) -> dict[str, Any]:
    target = resolve_watchlist_path(args.file)
    _, _, _, rows = load_watchlist(target)
    results = []
    with create_session() as session:
        for row in rows:
            quote_id = row.get("quote_id", "").strip()
            if quote_id:
                symbol = row.get("symbol", "").strip()
                resolved = ResolvedSecurity(
                    query=row.get("query") or symbol or quote_id,
                    code=symbol.replace("SH", "").replace("SZ", "").replace("HK", "")
                    if symbol
                    else "",
                    name=row.get("name") or "",
                    symbol=symbol or row.get("query") or quote_id,
                    quote_id=quote_id,
                    market=market_from_quote_id(quote_id),
                    security_type="",
                )
            else:
                lookup = row.get("symbol") or row.get("query")
                if not lookup:
                    raise StockWatchlistError(
                        "Each watchlist row must contain query or symbol."
                    )
                resolved = resolve_security(session, lookup)
            quote = fetch_quote(session, resolved.quote_id)
            quote_result = build_quote_result(resolved, quote)
            results.append(build_watchlist_quote_row(row, quote_result))
    return {
        "command": "watchlist-quote",
        "file": str(target),
        "results": results,
        "summary": summarize_watchlist(results),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Query stock quotes and manage a Markdown watchlist."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    search_parser = subparsers.add_parser("search", help="Search stocks by name or code.")
    search_parser.add_argument("query")
    search_parser.add_argument("--limit", type=int, default=10)
    search_parser.set_defaults(func=command_search)

    quote_parser = subparsers.add_parser("quote", help="Query real-time stock quotes.")
    quote_parser.add_argument("queries", nargs="+")
    quote_parser.set_defaults(func=command_quote)

    watchlist_parser = subparsers.add_parser("watchlist", help="Manage a Markdown watchlist.")
    watchlist_subparsers = watchlist_parser.add_subparsers(dest="watchlist_command", required=True)

    init_parser = watchlist_subparsers.add_parser("init", help="Create a watchlist Markdown file.")
    init_parser.add_argument("--file", required=True)
    init_parser.add_argument("--force", action="store_true")
    init_parser.set_defaults(func=command_watchlist_init)

    show_parser = watchlist_subparsers.add_parser("show", help="Show watchlist rows.")
    show_parser.add_argument("--file", required=True)
    show_parser.set_defaults(func=command_watchlist_show)

    sync_parser = watchlist_subparsers.add_parser("sync", help="Resolve watchlist rows to canonical symbols.")
    sync_parser.add_argument("--file", required=True)
    sync_parser.set_defaults(func=command_watchlist_sync)

    add_parser = watchlist_subparsers.add_parser("add", help="Add or update a watchlist row.")
    add_parser.add_argument("--file", required=True)
    add_parser.add_argument("--query", required=True)
    add_parser.add_argument("--cost-price", type=float, default=None)
    add_parser.add_argument("--quantity", type=int, default=None)
    add_parser.add_argument("--note", default="")
    add_parser.set_defaults(func=command_watchlist_add)

    remove_parser = watchlist_subparsers.add_parser("remove", help="Remove a watchlist row.")
    remove_parser.add_argument("--file", required=True)
    remove_parser.add_argument("--query", required=True)
    remove_parser.set_defaults(func=command_watchlist_remove)

    quote_watchlist_parser = watchlist_subparsers.add_parser(
        "quote", help="Query all rows from a watchlist file."
    )
    quote_watchlist_parser.add_argument("--file", required=True)
    quote_watchlist_parser.set_defaults(func=command_watchlist_quote)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        result = args.func(args)
    except requests.RequestException as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False, indent=2))
        return 1
    except StockWatchlistError as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
