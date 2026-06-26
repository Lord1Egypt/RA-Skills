#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unified Sina market helper v1.

Supports:
- detect: detect stock/futures market type from user input
- stock-quote: A-share / HK quote via hq.sinajs.cn
- futures-quote: domestic futures quote via hq.sinajs.cn
- futures-page: futures page metadata fallback via finance.sina.com.cn/futures/quotes/<code>.shtml
- inspect: unified workflow that tries stock, futures, then futures page fallback

Examples:
  python3 sina_market.py detect 600519 00700 AG0 PG2607
  python3 sina_market.py stock-quote 600519 000001 00700 --format json
  python3 sina_market.py futures-quote AG0 AU0 SC0 --format json
  python3 sina_market.py futures-page PG2607
  python3 sina_market.py inspect 600519 00700 AG0 PG2607 EB2605 --format json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode
from urllib.request import Request, urlopen

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://finance.sina.com.cn/",
}

SINAHQ_URL = "https://hq.sinajs.cn"
FUTURES_PAGE_BASE = "https://finance.sina.com.cn/futures/quotes"
CHINESE_MAPPING_PATH = Path(__file__).resolve().parent.parent / "references" / "chinese_futures_mapping.json"

try:
    CHINESE_FUTURES_MAPPING = json.loads(CHINESE_MAPPING_PATH.read_text(encoding="utf-8"))
except Exception:
    CHINESE_FUTURES_MAPPING = {}


def safe_float(v: Any) -> Optional[float]:
    try:
        if v in (None, ""):
            return None
        return float(v)
    except Exception:
        return None


def safe_int(v: Any) -> Optional[int]:
    try:
        if v in (None, ""):
            return None
        return int(float(v))
    except Exception:
        return None


def safe_get(arr: List[str], idx: int, default=None):
    return arr[idx] if 0 <= idx < len(arr) else default


def decode_response(raw: bytes, preferred: str = "gb18030") -> str:
    for enc in [preferred, "gbk", "utf-8"]:
        try:
            return raw.decode(enc)
        except Exception:
            continue
    return raw.decode(preferred, errors="replace")


def fetch_text(url: str, params: Optional[dict] = None, encoding: str = "gb18030") -> str:
    if params and "list" in params:
        other = {k: v for k, v in params.items() if k != "list"}
        qs = urlencode(other)
        if qs:
            full_url = f"{url}?{qs}&list={params['list']}"
        else:
            full_url = f"{url}?list={params['list']}"
    elif params:
        full_url = url + "?" + urlencode(params)
    else:
        full_url = url
    req = Request(full_url, headers=DEFAULT_HEADERS)
    with urlopen(req, timeout=10) as resp:
        raw = resp.read()
    return decode_response(raw, preferred=encoding)


@dataclass
class StockQuote:
    input_symbol: str
    code: str
    market: str
    name: Optional[str] = None
    price: Optional[float] = None
    change: Optional[float] = None
    change_percent: Optional[float] = None
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    prev_close: Optional[float] = None
    volume: Optional[Any] = None
    amount: Optional[Any] = None
    turnover: Optional[Any] = None
    raw_fields: Optional[List[str]] = None


@dataclass
class FuturesQuote:
    input_symbol: str
    code: str
    name: Optional[str] = None
    date: Optional[str] = None
    time_hms: Optional[str] = None
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    last: Optional[float] = None
    bid: Optional[float] = None
    ask: Optional[float] = None
    prev_close_or_settle: Optional[float] = None
    settle_or_avg: Optional[float] = None
    bid_vol: Optional[float] = None
    ask_vol: Optional[float] = None
    volume: Optional[float] = None
    open_interest: Optional[float] = None
    exchange_short: Optional[str] = None
    product_name: Optional[str] = None
    raw_fields: Optional[List[str]] = None


def normalize_chinese_futures_symbol(symbol: str) -> Optional[str]:
    s = symbol.strip()
    if s in CHINESE_FUTURES_MAPPING:
        mapped = CHINESE_FUTURES_MAPPING[s]
        if re.fullmatch(r"[A-Za-z]{1,3}\d{3,4}", mapped):
            return mapped.upper()
    m = re.fullmatch(r"(.+?)(\d{3,4})", s)
    if not m:
        return None
    name, month = m.group(1), m.group(2)
    if name in CHINESE_FUTURES_MAPPING:
        return (CHINESE_FUTURES_MAPPING[name] + month).upper()
    return None


def detect_symbol(symbol: str) -> Dict[str, Any]:
    s = symbol.strip()
    chinese_future = normalize_chinese_futures_symbol(s)
    if chinese_future:
        return {"input": symbol, "normalized": chinese_future, "market_type": "futures", "route": "futures-page-or-hq", "detected_from": "chinese-name"}
    if re.fullmatch(r"sh\d{6}", s, flags=re.I):
        return {"input": symbol, "normalized": s.lower(), "market_type": "a-share", "route": "stock-hq"}
    if re.fullmatch(r"sz\d{6}", s, flags=re.I):
        return {"input": symbol, "normalized": s.lower(), "market_type": "a-share", "route": "stock-hq"}
    if re.fullmatch(r"hk\d{5}", s, flags=re.I):
        return {"input": symbol, "normalized": s.lower(), "market_type": "hk-stock", "route": "stock-hq"}
    if re.fullmatch(r"\d{6}", s):
        code = f"sh{s}" if s.startswith("6") else f"sz{s}"
        return {"input": symbol, "normalized": code, "market_type": "a-share", "route": "stock-hq"}
    if re.fullmatch(r"\d{5}", s):
        return {"input": symbol, "normalized": f"hk{s}", "market_type": "hk-stock", "route": "stock-hq"}
    if re.fullmatch(r"[A-Za-z]{1,3}0", s):
        return {"input": symbol, "normalized": s.upper(), "market_type": "futures", "route": "futures-hq"}
    if re.fullmatch(r"[A-Za-z]{1,3}\d{3,4}([A-Za-z]-\d+)?", s):
        return {"input": symbol, "normalized": s.upper(), "market_type": "futures", "route": "futures-page-or-hq"}
    return {"input": symbol, "normalized": s, "market_type": "unknown", "route": "unknown"}


def parse_hq_text(text: str) -> Dict[str, List[str]]:
    result: Dict[str, List[str]] = {}
    for line in text.strip().split(";"):
        line = line.strip()
        if not line:
            continue
        m = re.match(r'var\s+hq_str_([^=]+)="(.*)"', line, flags=re.S)
        if not m:
            continue
        result[m.group(1).strip()] = m.group(2).split(",")
    return result


def fetch_hq_codes(codes: List[str]) -> Dict[str, List[str]]:
    params = {"rn": str(int(time.time() * 1000)), "list": ",".join(codes)}
    text = fetch_text(SINAHQ_URL, params=params, encoding="gb18030")
    return parse_hq_text(text)


def parse_stock_quote(input_symbol: str, normalized_code: str, fields: List[str]) -> StockQuote:
    if normalized_code.startswith("hk"):
        current = safe_float(safe_get(fields, 3))
        prev = safe_float(safe_get(fields, 6))
        return StockQuote(
            input_symbol=input_symbol,
            code=normalized_code,
            market="港股",
            name=safe_get(fields, 1),
            price=current,
            change=(current - prev) if current is not None and prev is not None else None,
            change_percent=((current - prev) / prev * 100) if current is not None and prev not in (None, 0) else None,
            open=safe_float(safe_get(fields, 2)),
            high=safe_float(safe_get(fields, 4)),
            low=safe_float(safe_get(fields, 5)),
            prev_close=prev,
            volume=safe_get(fields, 9),
            amount=safe_get(fields, 10),
            raw_fields=fields,
        )

    # Sina A-share common format:
    # 0 name, 1 open, 2 prev_close, 3 current, 4 high, 5 low, 8 volume, 9 amount, 30 date, 31 time
    current = safe_float(safe_get(fields, 3))
    prev = safe_float(safe_get(fields, 2))
    return StockQuote(
        input_symbol=input_symbol,
        code=normalized_code,
        market="A股",
        name=safe_get(fields, 0),
        price=current,
        change=(current - prev) if current is not None and prev is not None else None,
        change_percent=((current - prev) / prev * 100) if current is not None and prev not in (None, 0) else None,
        open=safe_float(safe_get(fields, 1)),
        high=safe_float(safe_get(fields, 4)),
        low=safe_float(safe_get(fields, 5)),
        prev_close=prev,
        volume=safe_int(safe_get(fields, 8)),
        amount=safe_get(fields, 9),
        turnover=None,
        raw_fields=fields,
    )


def parse_futures_quote(input_symbol: str, code: str, fields: List[str]) -> FuturesQuote:
    open_px = safe_float(safe_get(fields, 2))
    high_px = safe_float(safe_get(fields, 3))
    low_px = safe_float(safe_get(fields, 4))

    raw_last = safe_float(safe_get(fields, 5))
    bid_px = safe_float(safe_get(fields, 6))
    ask_px = safe_float(safe_get(fields, 7))
    ref_px = safe_float(safe_get(fields, 8))
    settle_px = safe_float(safe_get(fields, 10))

    # Sina domestic futures payloads are not fully uniform across commodity families.
    # For many contracts (e.g. PG/PP/V and similar goods), field 5 is often 0.000 while
    # field 8 carries the meaningful current/reference price that sits near bid/ask.
    # Keep the original field mapped into prev_close_or_settle for transparency, but
    # surface a practical `last` for cross-product use by falling back to field 8 when
    # field 5 is empty/zero.
    last_px = raw_last
    if last_px in (None, 0.0) and ref_px not in (None, 0.0):
        last_px = ref_px

    return FuturesQuote(
        input_symbol=input_symbol,
        code=code,
        name=safe_get(fields, 0),
        time_hms=safe_get(fields, 1),
        open=open_px,
        high=high_px,
        low=low_px,
        last=last_px,
        bid=bid_px,
        ask=ask_px,
        prev_close_or_settle=ref_px,
        settle_or_avg=settle_px,
        bid_vol=safe_float(safe_get(fields, 11)),
        ask_vol=safe_float(safe_get(fields, 12)),
        volume=safe_float(safe_get(fields, 13)),
        open_interest=safe_float(safe_get(fields, 14)),
        exchange_short=safe_get(fields, 15),
        product_name=safe_get(fields, 16),
        date=safe_get(fields, 17),
        raw_fields=fields,
    )


def parse_js_value(text: str, key: str):
    m = re.search(rf'{re.escape(key)}\s*=\s*"([^"]*)"', text)
    if m:
        return m.group(1)
    m = re.search(rf'{re.escape(key)}\s*=\s*(\[[^;]*\]|\{{[^;]*\}}|[^;]+);', text, flags=re.S)
    if m:
        raw = m.group(1).strip()
        try:
            return json.loads(raw)
        except Exception:
            return raw
    return None


def try_futures_hq(symbol: str) -> Optional[FuturesQuote]:
    candidates = []
    upper = symbol.upper()
    candidates.append(upper)
    if not upper.startswith("nf_"):
        candidates.append("nf_" + upper)
    seen = []
    uniq = []
    for c in candidates:
        if c not in seen:
            seen.append(c)
            uniq.append(c)
    try:
        raw = fetch_hq_codes(uniq)
    except Exception as e:
        # Sina hq API may return 403 for some symbols (e.g. WH2605).
        # Fall through to page-metadata fallback instead of crashing.
        return None
    for code in uniq:
        fields = raw.get(code, [])
        if fields and any(x.strip() for x in fields):
            return parse_futures_quote(symbol, code, fields)
    return None


def fetch_futures_page_meta(code: str) -> Dict[str, Any]:
    url = f"{FUTURES_PAGE_BASE}/{code}.shtml"
    text = fetch_text(url, encoding="gb18030")
    title = None
    m = re.search(r'<title>(.*?)</title>', text, flags=re.S | re.I)
    if m:
        title = m.group(1).strip()
    return {
        "code": code,
        "page_url": url,
        "title": title,
        "futures_app.name": parse_js_value(text, "futures_app.name"),
        "futures_app.code": parse_js_value(text, "futures_app.code"),
        "futures_app.chicang_code": parse_js_value(text, "futures_app.chicang_code"),
        "futures_app.vote_code": parse_js_value(text, "futures_app.vote_code"),
        "futures_app.hold_flash_code": parse_js_value(text, "futures_app.hold_flash_code"),
        "futures_app.transcation_date": parse_js_value(text, "futures_app.transcation_date"),
        "futures_app.dm_name": parse_js_value(text, "futures_app.dm_name"),
        "futures_app.dm_bid": parse_js_value(text, "futures_app.dm_bid"),
        "futures_app.type": parse_js_value(text, "futures_app.type"),
        "futures_app.hot_list": parse_js_value(text, "futures_app.hot_list"),
        "futures_app.inner_futures_per_month": parse_js_value(text, "futures_app.inner_futures_per_month"),
        "page_exists": bool(parse_js_value(text, "futures_app.code")),
    }


def print_table(rows: List[Dict[str, Any]], columns: List[str]):
    widths = {c: len(c) for c in columns}
    for row in rows:
        for c in columns:
            widths[c] = max(widths[c], len(str(row.get(c, ""))))
    header = " | ".join(c.ljust(widths[c]) for c in columns)
    sep = "-+-".join("-" * widths[c] for c in columns)
    print(header)
    print(sep)
    for row in rows:
        print(" | ".join(str(row.get(c, "")).ljust(widths[c]) for c in columns))


def cmd_detect(_args):
    rows = [detect_symbol(s) for s in _args.symbols]
    print(json.dumps(rows, ensure_ascii=False, indent=2))


def cmd_stock_quote(args):
    detected = [detect_symbol(s) for s in args.symbols]
    selected = [d for d in detected if d["route"] == "stock-hq"]
    codes = [d["normalized"] for d in selected]
    raw = fetch_hq_codes(codes) if codes else {}
    data = {}
    for d in selected:
        fields = raw.get(d["normalized"], [])
        data[d["input"]] = asdict(parse_stock_quote(d["input"], d["normalized"], fields)) if fields else {
            "input_symbol": d["input"], "code": d["normalized"], "market": d["market_type"], "error": "empty response"
        }
    if args.format == "json":
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        rows = []
        for v in data.values():
            rows.append({
                "input": v.get("input_symbol"), "code": v.get("code"), "market": v.get("market"), "name": v.get("name"),
                "price": v.get("price"), "chg%": v.get("change_percent"), "high": v.get("high"), "low": v.get("low")
            })
        print_table(rows, ["input", "code", "market", "name", "price", "chg%", "high", "low"])


def cmd_futures_quote(args):
    detected = [detect_symbol(s) for s in args.symbols]
    selected = [d for d in detected if d["market_type"] == "futures"]
    data = {}
    for d in selected:
        quote = try_futures_hq(d["normalized"])
        if quote is not None:
            data[d["input"]] = asdict(quote)
        else:
            # Try Sina.shtml page to find continuous contract code as fallback
            continuous_note = None
            try:
                meta = fetch_futures_page_meta(d["normalized"])
                vote_code = meta.get("futures_app.vote_code")
                if vote_code:
                    quote = try_futures_hq(vote_code)
                    if quote is not None:
                        fq = asdict(quote)
                        fq["continuous_note"] = (
                            f"Sina has no data for {d['normalized']}; "
                            f"showing continuous contract {vote_code} instead."
                        )
                        data[d["input"]] = fq
                        continue
            except Exception:
                pass
            data[d["input"]] = {"input_symbol": d["input"], "code": d["normalized"], "error": "empty response"}
    if args.format == "json":
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        rows = []
        for v in data.values():
            rows.append({
                "input": v.get("input_symbol"), "code": v.get("code"), "name": v.get("name"), "last": v.get("last"),
                "high": v.get("high"), "low": v.get("low"), "volume": v.get("volume"), "oi": v.get("open_interest")
            })
        print_table(rows, ["input", "code", "name", "last", "high", "low", "volume", "oi"])


def cmd_futures_page(args):
    print(json.dumps(fetch_futures_page_meta(args.code.upper()), ensure_ascii=False, indent=2))


def inspect_symbol(symbol: str) -> Dict[str, Any]:
    det = detect_symbol(symbol)
    item: Dict[str, Any] = {"detect": det}
    if det["route"] == "stock-hq":
        raw = fetch_hq_codes([det["normalized"]])
        fields = raw.get(det["normalized"], [])
        has_hq = bool(fields and any(x.strip() for x in fields))
        item["availability"] = {
            "hq_quote": has_hq,
            "page_meta": False,
            "mode": "stock-hq" if has_hq else "stock-empty",
        }
        item["stock_quote"] = asdict(parse_stock_quote(symbol, det["normalized"], fields)) if has_hq else None
    elif det["market_type"] == "futures":
        quote = try_futures_hq(det["normalized"])
        has_hq = quote is not None
        if has_hq:
            fq = asdict(quote)
            item["availability"] = {
                "hq_quote": True,
                "page_meta": False,
                "mode": "futures-hq",
            }
            item["futures_quote"] = fq
        else:
            item["futures_quote"] = None
            continuous_code = None
            page_404 = False
            try:
                meta = fetch_futures_page_meta(det["normalized"])
                month_list = None
                continuous_code = meta.get("futures_app.vote_code")
                inner = meta.get("futures_app.inner_futures_per_month")
                if isinstance(inner, dict):
                    month_list = inner.get("data")
                page_exists = bool(meta.get("page_exists"))
                page_404 = (not page_exists)
                item["availability"] = {
                    "hq_quote": False,
                    "page_meta": page_exists,
                    "mode": "page-fallback" if page_exists else "unsupported",
                    "continuous_code": continuous_code,
                    "month_list": month_list,
                }
                item["futures_page_meta"] = meta
            except Exception as e:
                page_404 = True
                item["availability"] = {
                    "hq_quote": False,
                    "page_meta": False,
                    "mode": "unsupported",
                }
                item["futures_page_meta_error"] = str(e)
            # Last resort: try the continuous contract via hq if page was 404.
            # Sina carries some products (e.g. WH/strong wheat) only as continuous.
            if page_404 and continuous_code:
                quote = try_futures_hq(continuous_code)
                if quote is not None:
                    fq = asdict(quote)
                    item["availability"]["mode"] = "continuous-fallback"
                    item["availability"]["continuous_fallback"] = True
                    item["futures_quote"] = fq
                    item["futures_quote"]["continuous_note"] = (
                        f"Sina has no data for {det['normalized']}; "
                        f"showing continuous contract {continuous_code} instead."
                    )
    else:
        item["availability"] = {
            "hq_quote": False,
            "page_meta": False,
            "mode": "unknown",
        }
    return item


def cmd_inspect(args):
    out = {symbol: inspect_symbol(symbol) for symbol in args.symbols}
    print(json.dumps(out, ensure_ascii=False, indent=2))


def cmd_coverage_test(args):
    rows = []
    for symbol in args.symbols:
        item = inspect_symbol(symbol)
        det = item.get("detect", {})
        av = item.get("availability", {})
        rows.append({
            "input": symbol,
            "normalized": det.get("normalized"),
            "market": det.get("market_type"),
            "mode": av.get("mode"),
            "hq": av.get("hq_quote"),
            "page": av.get("page_meta"),
            "continuous": av.get("continuous_code"),
            "months": len(av.get("month_list") or []),
        })
    if args.format == "json":
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        print_table(rows, ["input", "normalized", "market", "mode", "hq", "page", "continuous", "months"])


def build_parser():
    parser = argparse.ArgumentParser(description="Unified Sina market helper")
    sub = parser.add_subparsers(dest="command", required=True)

    p_detect = sub.add_parser("detect", help="Detect market type for symbols")
    p_detect.add_argument("symbols", nargs="+")
    p_detect.set_defaults(func=cmd_detect)

    p_stock = sub.add_parser("stock-quote", help="Fetch A-share / HK stock quotes")
    p_stock.add_argument("symbols", nargs="+")
    p_stock.add_argument("--format", choices=["json", "table"], default="json")
    p_stock.set_defaults(func=cmd_stock_quote)

    p_fut = sub.add_parser("futures-quote", help="Fetch domestic futures quotes")
    p_fut.add_argument("symbols", nargs="+")
    p_fut.add_argument("--format", choices=["json", "table"], default="json")
    p_fut.set_defaults(func=cmd_futures_quote)

    p_page = sub.add_parser("futures-page", help="Extract metadata from a Sina futures quote page")
    p_page.add_argument("code")
    p_page.set_defaults(func=cmd_futures_page)

    p_inspect = sub.add_parser("inspect", help="Unified inspect with fallback")
    p_inspect.add_argument("symbols", nargs="+")
    p_inspect.add_argument("--format", choices=["json"], default="json")
    p_inspect.set_defaults(func=cmd_inspect)

    p_cov = sub.add_parser("coverage-test", help="Batch coverage test across stock/futures/page-fallback modes")
    p_cov.add_argument("symbols", nargs="+")
    p_cov.add_argument("--format", choices=["json", "table"], default="table")
    p_cov.set_defaults(func=cmd_coverage_test)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
