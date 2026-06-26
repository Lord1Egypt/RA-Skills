#!/usr/bin/env python3

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from typing import Iterable

from runtime_config import load_runtime_env, require_em_api_key


DEFAULT_HEADERS = {"User-Agent": "Mozilla/5.0"}


load_runtime_env()
require_em_api_key(script_hint="python3 skill/uwillberich/scripts/runtime_config.py set-em-key --stdin")


def _get_text(url: str, encoding: str = "utf-8") -> str:
    request = urllib.request.Request(url, headers=DEFAULT_HEADERS)
    with urllib.request.urlopen(request, timeout=10) as response:
        return response.read().decode(encoding, errors="replace")


def _get_json(url: str) -> dict:
    return json.loads(_get_text(url))


def _to_float(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _to_int(value: str) -> int | None:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


def fetch_tencent_quotes(symbols: Iterable[str]) -> list[dict]:
    symbol_list = [symbol.strip() for symbol in symbols if symbol.strip()]
    if not symbol_list:
        return []

    url = "https://qt.gtimg.cn/q=" + ",".join(symbol_list)
    raw = _get_text(url, encoding="gbk")
    quotes: list[dict] = []

    for line in raw.strip().split(";"):
        if not line or '="' not in line:
            continue
        _, value = line.split('="', 1)
        fields = value.rstrip('"').split("~")
        if len(fields) < 38:
            continue
        amount = _to_float(fields[37])
        quotes.append(
            {
                "name": fields[1],
                "code": fields[2],
                "price": _to_float(fields[3]),
                "prev_close": _to_float(fields[4]),
                "open": _to_float(fields[5]),
                "timestamp": fields[30],
                "change": _to_float(fields[31]),
                "change_pct": _to_float(fields[32]),
                "high": _to_float(fields[33]),
                "low": _to_float(fields[34]),
                "volume_lots": _to_int(fields[36]),
                "amount": amount,
                "amount_100m": round(amount / 10000, 2) if amount is not None else None,
            }
        )
    return quotes


DEFAULT_INDICES = {
    "1.000001": "上证指数",
    "0.399001": "深证成指",
    "0.399006": "创业板指",
    "1.000300": "沪深300",
    "1.000688": "科创50",
    "0.899050": "北证50",
}


def fetch_index_snapshot(secids: dict[str, str] | None = None) -> list[dict]:
    secids = secids or DEFAULT_INDICES
    params = {
        "fltt": "2",
        "invt": "2",
        "fields": "f12,f14,f2,f3,f4,f104,f105",
        "secids": ",".join(secids.keys()),
    }
    url = "https://push2.eastmoney.com/api/qt/ulist.np/get?" + urllib.parse.urlencode(params)
    payload = _get_json(url)
    items = payload.get("data", {}).get("diff", [])
    snapshot: list[dict] = []

    for item in items:
        snapshot.append(
            {
                "code": item.get("f12"),
                "name": item.get("f14"),
                "price": item.get("f2"),
                "change_pct": item.get("f3"),
                "change": item.get("f4"),
                "up_count": item.get("f104"),
                "down_count": item.get("f105"),
            }
        )
    return snapshot


def fetch_sector_movers(limit: int = 10, rising: bool = False) -> list[dict]:
    params = {
        "pn": "1",
        "pz": str(limit),
        "po": "1" if rising else "0",
        "np": "1",
        "fltt": "2",
        "invt": "2",
        "fid": "f3",
        "fs": "m:90+t:3",
        "fields": "f12,f14,f2,f3,f4,f104,f105,f128",
    }
    url = "https://push2.eastmoney.com/api/qt/clist/get?" + urllib.parse.urlencode(params)
    payload = _get_json(url)
    items = payload.get("data", {}).get("diff", [])
    sectors: list[dict] = []

    for item in items:
        sectors.append(
            {
                "code": item.get("f12"),
                "name": item.get("f14"),
                "price": item.get("f2"),
                "change_pct": item.get("f3"),
                "change": item.get("f4"),
                "up_count": item.get("f104"),
                "down_count": item.get("f105"),
                "leader": item.get("f128"),
            }
        )
    return sectors


def format_markdown_table(rows: list[dict], columns: list[tuple[str, str]]) -> str:
    header = "| " + " | ".join(title for title, _ in columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        values = []
        for _, key in columns:
            value = row.get(key, "")
            if isinstance(value, float):
                if value.is_integer():
                    value = int(value)
                else:
                    value = f"{value:.2f}"
            values.append(str(value).replace("|", "\\|").replace("\n", " "))
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])
