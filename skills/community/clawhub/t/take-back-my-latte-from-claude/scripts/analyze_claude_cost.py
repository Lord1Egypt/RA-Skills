#!/usr/bin/env python3
"""Analyze Anthropic Usage and Cost Report JSON locally, without network access."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

LATTE_PRICE_USD = Decimal("6.00")
PRIVACY_NOTICE = "🔒 Local Analysis Only: No API Key required, no data uploaded."


def walk(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def number(value: Any) -> int:
    return int(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else 0


def decimal_value(value: Any) -> Decimal | None:
    if not isinstance(value, (str, int, float)) or isinstance(value, bool):
        return None
    try:
        return Decimal(str(value))
    except InvalidOperation:
        return None


def cost_from(row: dict[str, Any]) -> tuple[Decimal, str] | None:
    # Anthropic Cost Report amounts are decimal strings in minor units (cents).
    amount = decimal_value(row.get("amount"))
    currency = row.get("currency")
    if amount is not None and isinstance(currency, str):
        return amount / Decimal("100"), currency.upper()
    # Claude Code Usage Report exposes estimated_cost in minor units.
    estimated = row.get("estimated_cost")
    if isinstance(estimated, dict):
        value = decimal_value(estimated.get("amount"))
        currency = estimated.get("currency")
        if value is not None and isinstance(currency, str):
            return value / Decimal("100"), currency.upper()
    return None


def label_for(row: dict[str, Any]) -> str:
    for key in ("model", "description", "cost_type", "product", "workspace_id", "service_tier"):
        value = row.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return "Claude API"


def is_usage_row(row: dict[str, Any]) -> bool:
    return any(key in row for key in ("uncached_input_tokens", "cache_read_input_tokens", "output_tokens", "model_breakdown"))


def document_kind(data: Any) -> str:
    rows = list(walk(data))
    if any(cost_from(row) for row in rows):
        return "costs"
    if any(is_usage_row(row) for row in rows):
        return "usage"
    return "unknown"


def parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def document_meta(data: Any) -> dict[str, Any]:
    starts, ends = [], []
    workspaces: set[str] = set()
    for row in walk(data):
        start, end = parse_time(row.get("starting_at")), parse_time(row.get("ending_at"))
        if start:
            starts.append(start)
        if end:
            ends.append(end)
        workspace = row.get("workspace_id")
        if isinstance(workspace, str) and workspace:
            workspaces.add(workspace)
    return {
        "start": min(starts) if starts else None,
        "end": max(ends) if ends else None,
        "workspaces": workspaces,
        "has_more": data.get("has_more") is True if isinstance(data, dict) else False,
    }


def compatibility_warnings(documents: list[tuple[str, Any]]) -> list[str]:
    warnings: list[str] = []
    by_kind: dict[str, list[tuple[str, dict[str, Any]]]] = defaultdict(list)
    for path, data in documents:
        by_kind[document_kind(data)].append((path, document_meta(data)))
    if len(by_kind["costs"]) > 1:
        warnings.append("Multiple Cost Reports were provided; overlapping date ranges may count cost twice.")
    if any(meta["has_more"] for entries in by_kind.values() for _, meta in entries):
        warnings.append("At least one export has has_more=true; add the remaining pages for a complete report.")
    if by_kind["costs"] and by_kind["usage"]:
        cost_meta, usage_meta = by_kind["costs"][0][1], by_kind["usage"][0][1]
        if all((cost_meta["start"], cost_meta["end"], usage_meta["start"], usage_meta["end"])):
            if cost_meta["end"] <= usage_meta["start"] or usage_meta["end"] <= cost_meta["start"]:
                warnings.append("Cost and Usage date ranges do not overlap; usage signals may not describe the billed period.")
        if cost_meta["workspaces"] and usage_meta["workspaces"] and cost_meta["workspaces"].isdisjoint(usage_meta["workspaces"]):
            warnings.append("Cost and Usage workspace IDs do not overlap; verify that both exports cover the same workspace.")
    unknown = [Path(path).name for path, _ in by_kind["unknown"]]
    if unknown:
        warnings.append("Unrecognized JSON file(s): " + ", ".join(unknown))
    return warnings


def analyze(documents: list[tuple[str, Any]]) -> dict[str, Any]:
    costs: dict[str, Decimal] = defaultdict(Decimal)
    currencies: set[str] = set()
    uncached = cache_read = cache_write = output = web_searches = 0
    models: set[str] = set()
    service_tiers: set[str] = set()
    long_context = False

    for _, data in documents:
        for row in walk(data):
            cost = cost_from(row)
            if cost:
                value, currency = cost
                costs[label_for(row)] += value
                currencies.add(currency)
            uncached += number(row.get("uncached_input_tokens"))
            cache_read += number(row.get("cache_read_input_tokens"))
            output += number(row.get("output_tokens"))
            creation = row.get("cache_creation")
            if isinstance(creation, dict):
                cache_write += sum(number(value) for value in creation.values())
            model = row.get("model")
            if isinstance(model, str):
                models.add(model.lower())
            tier = row.get("service_tier")
            if isinstance(tier, str):
                service_tiers.add(tier.lower())
            if row.get("context_window") == "200k-1M":
                long_context = True
            tools = row.get("server_tool_use")
            if isinstance(tools, dict):
                web_searches += number(tools.get("web_search_requests"))

    warnings = compatibility_warnings(documents)
    total = sum(costs.values(), Decimal("0"))
    usage_found = uncached + cache_read + cache_write + output + web_searches > 0
    base = {"privacy_notice": PRIVACY_NOTICE, "warnings": warnings}
    if total <= 0:
        return {**base, "status": "needs_cost_data" if usage_found else "unsupported", "message": "Usage was found, but no monetary Cost Report amount was present." if usage_found else "No supported Claude cost or usage records were found."}
    if len(currencies) > 1:
        return {**base, "status": "unsupported", "message": "Multiple currencies were found; totals cannot be combined safely."}

    signals: list[str] = []
    rate = Decimal("0.08")
    total_input = uncached + cache_read + cache_write
    if total_input and cache_read / total_input < 0.20:
        rate += Decimal("0.08")
        signals.append("Low cache-read share suggests repeated context may be recoverable with prompt caching.")
    if any("opus" in model for model in models):
        rate += Decimal("0.06")
        signals.append("Opus usage is present; routine tasks may be candidates for Sonnet or Haiku routing tests.")
    if usage_found and not ({"batch", "flex", "flex_discount"} & service_tiers):
        rate += Decimal("0.04")
        signals.append("No discounted service tier appears in usage; asynchronous workloads may be candidates for Batch or Flex.")
    if uncached and output / uncached > 0.30:
        rate += Decimal("0.04")
        signals.append("High output relative to uncached input suggests tighter output limits may reduce cost.")
    if long_context:
        rate += Decimal("0.04")
        signals.append("Long-context usage is present; trimming context may avoid premium 200K+ rates.")
    if web_searches:
        signals.append("Server-side web searches are present; verify that every search adds enough value to justify its separate cost.")
    if not signals:
        signals.append("The export has limited optimization detail, so recovery uses a conservative provisional rate.")

    rate = min(rate, Decimal("0.30"))
    recoverable = total * rate
    breakdown = sorted(costs.items(), key=lambda item: item[1], reverse=True)[:5]
    money = lambda value: float(value.quantize(Decimal("0.01")))
    return {
        **base,
        "status": "ok",
        "currency": next(iter(currencies), "USD"),
        "latte_price": money(LATTE_PRICE_USD),
        "total_cost": money(total),
        "latte_count": int(total // LATTE_PRICE_USD),
        "recoverable_cost": money(recoverable),
        "recoverable_latte_count": int(recoverable // LATTE_PRICE_USD),
        "recovery_rate": int(rate * 100),
        "recovery_basis": signals[:5],
        "cost_breakdown": [{"label": label, "cost": money(value)} for label, value in breakdown],
        "usage_summary": {"uncached_input_tokens": uncached, "cache_read_input_tokens": cache_read, "cache_creation_input_tokens": cache_write, "output_tokens": output, "web_search_requests": web_searches},
        "disclaimer": "Directional estimate; validate each optimization with a small production test.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze Claude Cost and Usage JSON locally.")
    parser.add_argument("files", nargs="*", help="Cost and Usage JSON files in any order")
    parser.add_argument("--costs", action="append", default=[], help="Claude Cost Report JSON (repeatable)")
    parser.add_argument("--usage", action="append", default=[], help="Claude Usage Report JSON (repeatable)")
    args = parser.parse_args()
    paths = list(dict.fromkeys([*args.files, *args.costs, *args.usage]))
    if not paths:
        parser.error("provide at least one JSON file")
    print(PRIVACY_NOTICE, file=sys.stderr)
    try:
        documents = [(path, json.loads(Path(path).read_text(encoding="utf-8"))) for path in paths]
        print(json.dumps(analyze(documents), ensure_ascii=False, indent=2))
        return 0
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "error", "privacy_notice": PRIVACY_NOTICE, "message": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
