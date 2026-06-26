#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sina Futures public webpage interface helper.

Capabilities:
- Fetch futures quotes from hq.sinajs.cn
- Load exchange / product / contract mappings from Sina public JS resources
- Normalize commonly used fields
- CLI output as json or table

Examples:
  python3 sina_futures.py quote AG0 AU0 PG2607 EB2607
  python3 sina_futures.py validate PG2607 EB2607 AG0
  python3 sina_futures.py prefix AG
  python3 sina_futures.py search 液化气
  python3 sina_futures.py dropdown --exchange 上期所
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

from urllib.parse import urlencode
from urllib.request import Request, urlopen

SINAHQ_URL = "https://hq.sinajs.cn"
SYMBOL_JS_URL = "https://finance.sina.com.cn/futures/quotes/iframe/js/futures_symbol_js.js"
FUTURES_INFO_JS_URL = "https://finance.sina.com.cn/iframe/futures_info_cff.js"

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://finance.sina.com.cn/",
}


@dataclass
class FutureQuote:
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


def safe_float(v: Any) -> Optional[float]:
    try:
        if v is None or v == "":
            return None
        return float(v)
    except Exception:
        return None


def safe_get(arr: List[str], idx: int, default=None):
    return arr[idx] if 0 <= idx < len(arr) else default


def parse_hq_text(text: str) -> Dict[str, List[str]]:
    result: Dict[str, List[str]] = {}
    for line in text.strip().split(";"):
        line = line.strip()
        if not line:
            continue
        m = re.match(r'var\s+hq_str_([^=]+)="(.*)"', line, flags=re.S)
        if not m:
            continue
        code = m.group(1).strip()
        payload = m.group(2)
        result[code] = payload.split(",")
    return result


class SinaFuturesClient:
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self._symbol_mapping_cache: Optional[Dict[str, Any]] = None
        self._dropdown_mapping_cache: Optional[Dict[str, Any]] = None

    def _get_text(self, url: str, params: Optional[dict] = None, encoding: str = "gb18030") -> str:
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
        with urlopen(req, timeout=self.timeout) as resp:
            raw = resp.read()
        return raw.decode(encoding, errors="replace")

    def fetch_raw_quotes(self, codes: List[str]) -> Dict[str, List[str]]:
        params = {
            "rn": str(int(time.time() * 1000)),
            "list": ",".join(codes),
        }
        text = self._get_text(SINAHQ_URL, params=params, encoding="gb18030")
        return parse_hq_text(text)

    def normalize_quote(self, code: str, fields: List[str]) -> FutureQuote:
        return FutureQuote(
            code=code,
            name=safe_get(fields, 0),
            time_hms=safe_get(fields, 1),
            open=safe_float(safe_get(fields, 2)),
            high=safe_float(safe_get(fields, 3)),
            low=safe_float(safe_get(fields, 4)),
            last=safe_float(safe_get(fields, 5)),
            bid=safe_float(safe_get(fields, 6)),
            ask=safe_float(safe_get(fields, 7)),
            prev_close_or_settle=safe_float(safe_get(fields, 8)),
            settle_or_avg=safe_float(safe_get(fields, 10)),
            bid_vol=safe_float(safe_get(fields, 11)),
            ask_vol=safe_float(safe_get(fields, 12)),
            volume=safe_float(safe_get(fields, 13)),
            open_interest=safe_float(safe_get(fields, 14)),
            exchange_short=safe_get(fields, 15),
            product_name=safe_get(fields, 16),
            date=safe_get(fields, 17),
            raw_fields=fields,
        )

    def fetch_quotes(self, codes: List[str]) -> Dict[str, FutureQuote]:
        raw = self.fetch_raw_quotes(codes)
        return {code: self.normalize_quote(code, fields) for code, fields in raw.items()}

    def fetch_quotes_as_dict(self, codes: List[str]) -> Dict[str, Dict[str, Any]]:
        return {code: asdict(q) for code, q in self.fetch_quotes(codes).items()}

    def get_symbol_mapping(self) -> Dict[str, Any]:
        if self._symbol_mapping_cache is not None:
            return self._symbol_mapping_cache
        text = self._get_text(SYMBOL_JS_URL, encoding="utf-8")
        m = re.search(r'var\s+jys_data\s*=\s*(\{.*?\})\s*/\*', text, flags=re.S)
        if not m:
            m = re.search(r'var\s+jys_data\s*=\s*(\{.*\})', text, flags=re.S)
        if not m:
            raise ValueError("Unable to locate jys_data JSON in futures_symbol_js.js")
        self._symbol_mapping_cache = json.loads(m.group(1))
        return self._symbol_mapping_cache

    def get_dropdown_mapping(self) -> Dict[str, Any]:
        if self._dropdown_mapping_cache is not None:
            return self._dropdown_mapping_cache
        text = self._get_text(FUTURES_INFO_JS_URL, encoding="gb18030")

        jys_map: Dict[int, str] = {}
        for idx, name in re.findall(r'JYS\[(\d+)\]\s*=\s*[\'"]([^\'"]+)[\'"]', text):
            jys_map[int(idx)] = name

        pz_map: Dict[int, Dict[int, str]] = {}
        for jys_idx, pz_idx, pz_name in re.findall(r'PZ\[(\d+)\]\[(\d+)\]\s*=\s*[\'"]([^\'"]+)[\'"]', text):
            pz_map.setdefault(int(jys_idx), {})[int(pz_idx)] = pz_name

        yf_map: Dict[int, Dict[int, Dict[int, Dict[str, str]]]] = {}
        for jys_idx, pz_idx, yf_idx, contract_name, contract_code in re.findall(
            r'YF\[(\d+)\]\[(\d+)\]\[(\d+)\]\s*=\s*new Array\("([^"]+)","([^"]+)"\)', text
        ):
            j, p, y = int(jys_idx), int(pz_idx), int(yf_idx)
            yf_map.setdefault(j, {}).setdefault(p, {})[y] = {
                "name": contract_name,
                "code": contract_code,
            }

        result: Dict[str, Any] = {}
        for jys_idx, exchange_name in jys_map.items():
            if jys_idx == 0:
                continue
            result[exchange_name] = {}
            for pz_idx, pz_name in pz_map.get(jys_idx, {}).items():
                contracts = []
                for _, contract in sorted(yf_map.get(jys_idx, {}).get(pz_idx, {}).items(), key=lambda x: x[0]):
                    contracts.append(contract)
                result[exchange_name][pz_name] = contracts

        self._dropdown_mapping_cache = result
        return result

    def find_contracts_by_prefix(self, prefix: str) -> Dict[str, str]:
        mapping = self.get_symbol_mapping()
        found: Dict[str, str] = {}

        def walk(obj):
            nonlocal found
            if isinstance(obj, dict):
                if prefix in obj and isinstance(obj[prefix], dict):
                    found = obj[prefix]
                    return
                for v in obj.values():
                    if not found:
                        walk(v)

        walk(mapping)
        return found

    def search_contract_code(self, keyword: str) -> List[Dict[str, str]]:
        mapping = self.get_symbol_mapping()
        results: List[Dict[str, str]] = []

        def walk(obj, path=None):
            if path is None:
                path = []
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if isinstance(v, dict):
                        walk(v, path + [str(k)])
                    else:
                        ks, vs = str(k), str(v)
                        if keyword.lower() in ks.lower() or keyword in vs:
                            results.append({"code": ks, "name": vs, "path": " / ".join(path)})

        walk(mapping)
        return results

    def validate_codes(self, codes: List[str]) -> Dict[str, bool]:
        raw = self.fetch_raw_quotes(codes)
        out = {}
        for code in codes:
            fields = raw.get(code, [])
            out[code] = bool(fields and any(x.strip() for x in fields))
        return out


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


def cmd_quote(client: SinaFuturesClient, args):
    data = client.fetch_quotes_as_dict(args.codes)
    if args.format == "json":
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    rows = []
    for code, q in data.items():
        rows.append({
            "code": code,
            "name": q.get("name"),
            "last": q.get("last"),
            "high": q.get("high"),
            "low": q.get("low"),
            "volume": q.get("volume"),
            "oi": q.get("open_interest"),
            "date": q.get("date"),
            "time": q.get("time_hms"),
        })
    print_table(rows, ["code", "name", "last", "high", "low", "volume", "oi", "date", "time"])


def cmd_validate(client: SinaFuturesClient, args):
    print(json.dumps(client.validate_codes(args.codes), ensure_ascii=False, indent=2))


def cmd_prefix(client: SinaFuturesClient, args):
    print(json.dumps(client.find_contracts_by_prefix(args.prefix), ensure_ascii=False, indent=2))


def cmd_search(client: SinaFuturesClient, args):
    print(json.dumps(client.search_contract_code(args.keyword), ensure_ascii=False, indent=2))


def cmd_dropdown(client: SinaFuturesClient, args):
    data = client.get_dropdown_mapping()
    if args.exchange:
        data = {args.exchange: data.get(args.exchange, {})}
    print(json.dumps(data, ensure_ascii=False, indent=2))


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


def cmd_page_meta(client: SinaFuturesClient, args):
    url = f"https://finance.sina.com.cn/futures/quotes/{args.code}.shtml"
    text = client._get_text(url, encoding="gb18030")
    title = None
    m = re.search(r'<title>(.*?)</title>', text, flags=re.S | re.I)
    if m:
        title = m.group(1).strip()

    result = {
        "code": args.code,
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
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_url(_client: SinaFuturesClient, args):
    url = SINAHQ_URL + "?" + urlencode({"rn": str(int(time.time() * 1000)), "list": ",".join(args.codes)})
    print(url)


def build_parser():
    parser = argparse.ArgumentParser(description="Sina futures public quote helper")
    sub = parser.add_subparsers(dest="command", required=True)

    p_quote = sub.add_parser("quote", help="Fetch quotes for one or more contract codes")
    p_quote.add_argument("codes", nargs="+", help="Contract codes, e.g. AG0 PG2607 EB2607")
    p_quote.add_argument("--format", choices=["json", "table"], default="json")
    p_quote.set_defaults(func=cmd_quote)

    p_validate = sub.add_parser("validate", help="Validate whether codes return data")
    p_validate.add_argument("codes", nargs="+")
    p_validate.set_defaults(func=cmd_validate)

    p_prefix = sub.add_parser("prefix", help="List contracts by product prefix, e.g. AG/PG/EB")
    p_prefix.add_argument("prefix")
    p_prefix.set_defaults(func=cmd_prefix)

    p_search = sub.add_parser("search", help="Search code mapping by code or Chinese name")
    p_search.add_argument("keyword")
    p_search.set_defaults(func=cmd_search)

    p_dropdown = sub.add_parser("dropdown", help="Dump dropdown mapping from public JS")
    p_dropdown.add_argument("--exchange", help="Filter exchange name, e.g. 上期所")
    p_dropdown.set_defaults(func=cmd_dropdown)

    p_page = sub.add_parser("page-meta", help="Extract embedded metadata from a Sina futures quote page")
    p_page.add_argument("code", help="Contract code, e.g. PG2607")
    p_page.set_defaults(func=cmd_page_meta)

    p_url = sub.add_parser("url", help="Print the raw quote URL for given codes")
    p_url.add_argument("codes", nargs="+")
    p_url.set_defaults(func=cmd_url)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    client = SinaFuturesClient()
    args.func(client, args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
