#!/usr/bin/env python3
"""Analyze an OpenAI Usage/Costs JSON export without network access."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

LATTE_PRICE_USD = 6.0
PRIVACY_NOTICE = "🔒 Local Analysis Only: No API Key required, no data uploaded."


def walk(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def number(value: Any) -> float:
    return float(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else 0.0


def amount_from(row: dict[str, Any]) -> tuple[float, str] | None:
    amount = row.get("amount")
    if isinstance(amount, dict) and number(amount.get("value")):
        return number(amount["value"]), str(amount.get("currency", "usd")).upper()
    for key in ("cost", "total_cost", "cost_usd", "amount_usd"):
        if number(row.get(key)):
            return number(row[key]), "USD"
    return None


def label_for(row: dict[str, Any]) -> str:
    for key in ("model", "model_id", "line_item", "project_name", "project_id", "service_tier"):
        value = row.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return "OpenAI API"


def document_kind(data: Any) -> str:
    rows = list(walk(data))
    if any(amount_from(row) for row in rows):
        return "costs"
    if any(number(row.get(key)) for row in rows for key in ("input_tokens", "output_tokens", "num_model_requests")):
        return "usage"
    return "unknown"


def document_meta(data: Any) -> dict[str, Any]:
    starts: list[float] = []
    ends: list[float] = []
    request_ids: set[str] = set()
    for row in walk(data):
        if number(row.get("start_time")):
            starts.append(number(row["start_time"]))
        if number(row.get("end_time")):
            ends.append(number(row["end_time"]))
        request_id = row.get("request_id")
        if isinstance(request_id, str) and request_id:
            request_ids.add(request_id)
    return {
        "start": min(starts) if starts else None,
        "end": max(ends) if ends else None,
        "request_ids": request_ids,
    }


def compatibility_warnings(documents: list[tuple[str, Any]]) -> list[str]:
    warnings: list[str] = []
    by_kind: dict[str, list[tuple[str, dict[str, Any]]]] = defaultdict(list)
    for path, data in documents:
        by_kind[document_kind(data)].append((path, document_meta(data)))

    if len(by_kind["costs"]) > 1:
        warnings.append("Multiple Costs exports were provided; make sure their date ranges do not overlap, or costs may be counted twice.")

    if by_kind["costs"] and by_kind["usage"]:
        cost_meta = by_kind["costs"][0][1]
        usage_meta = by_kind["usage"][0][1]
        if all(value is not None for value in (cost_meta["start"], cost_meta["end"], usage_meta["start"], usage_meta["end"])):
            if cost_meta["end"] <= usage_meta["start"] or usage_meta["end"] <= cost_meta["start"]:
                warnings.append("Costs and Usage date ranges do not overlap; recovery signals may not describe the billed period.")
        cost_ids = cost_meta["request_ids"]
        usage_ids = usage_meta["request_ids"]
        if cost_ids and usage_ids and cost_ids.isdisjoint(usage_ids):
            warnings.append("Costs and Usage request IDs do not overlap; verify that both exports cover the same workload.")

    unknown = [Path(path).name for path, _ in by_kind["unknown"]]
    if unknown:
        warnings.append("Unrecognized JSON file(s) were ignored for classification: " + ", ".join(unknown))
    return warnings


def analyze(documents: list[tuple[str, Any]]) -> dict[str, Any]:
    costs: dict[str, float] = defaultdict(float)
    currencies: set[str] = set()
    input_tokens = output_tokens = cached_tokens = requests = 0.0
    model_names: set[str] = set()

    for _, data in documents:
        for row in walk(data):
            amount = amount_from(row)
            if amount:
                value, currency = amount
                costs[label_for(row)] += value
                currencies.add(currency)

            input_tokens += number(row.get("input_tokens")) or number(row.get("input_tokens_uncached"))
            output_tokens += number(row.get("output_tokens"))
            cached_tokens += number(row.get("input_cached_tokens")) or number(row.get("cached_tokens"))
            requests += number(row.get("num_model_requests")) or number(row.get("request_count"))
            model = row.get("model") or row.get("model_id")
            if isinstance(model, str):
                model_names.add(model.lower())

    warnings = compatibility_warnings(documents)

    total = sum(costs.values())
    usage_found = input_tokens + output_tokens + requests > 0
    if total <= 0:
        return {
            "status": "needs_cost_data" if usage_found else "unsupported",
            "message": "Token usage was found, but no monetary cost amount was present." if usage_found else "No supported OpenAI cost or usage records were found.",
            "privacy_notice": PRIVACY_NOTICE,
            "warnings": warnings,
            "usage_summary": {"input_tokens": int(input_tokens), "output_tokens": int(output_tokens), "cached_tokens": int(cached_tokens), "requests": int(requests)},
        }

    if len(currencies) > 1:
        return {"status": "unsupported", "message": "Multiple currencies were found; totals cannot be combined safely.", "privacy_notice": PRIVACY_NOTICE, "warnings": warnings}

    signals: list[str] = []
    rate = 0.10
    if input_tokens > 0:
        cached_ratio = min(1.0, cached_tokens / input_tokens)
        if cached_ratio < 0.20:
            rate += 0.08
            signals.append("Low cached-input share suggests repeated prompt context may be recoverable.")
        if output_tokens / max(input_tokens, 1) > 0.30:
            rate += 0.05
            signals.append("A high output-to-input ratio suggests tighter output limits may reduce cost.")
    if any(not any(x in model for x in ("mini", "nano")) for model in model_names):
        rate += 0.07
        signals.append("Standard or reasoning models are present; routine tasks may be candidates for model routing tests.")
    if not signals:
        signals.append("The export has limited usage detail, so recovery uses a conservative provisional rate.")

    rate = min(rate, 0.30)
    recoverable = total * rate
    breakdown = sorted(costs.items(), key=lambda item: item[1], reverse=True)[:5]

    return {
        "status": "ok",
        "privacy_notice": PRIVACY_NOTICE,
        "warnings": warnings,
        "currency": next(iter(currencies), "USD"),
        "latte_price": LATTE_PRICE_USD,
        "total_cost": round(total, 2),
        "latte_count": int(total // LATTE_PRICE_USD),
        "recoverable_cost": round(recoverable, 2),
        "recoverable_latte_count": int(recoverable // LATTE_PRICE_USD),
        "recovery_rate": round(rate * 100),
        "recovery_basis": signals,
        "cost_breakdown": [{"label": label, "cost": round(value, 2)} for label, value in breakdown],
        "usage_summary": {"input_tokens": int(input_tokens), "output_tokens": int(output_tokens), "cached_tokens": int(cached_tokens), "requests": int(requests)},
        "disclaimer": "Directional estimate; validate each optimization with a small production test.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze OpenAI Costs and Usage JSON locally.")
    parser.add_argument("files", nargs="*", help="Costs and Usage JSON files in any order")
    parser.add_argument("--costs", action="append", default=[], help="OpenAI Costs JSON (repeatable)")
    parser.add_argument("--usage", action="append", default=[], help="OpenAI Usage JSON (repeatable)")
    args = parser.parse_args()
    raw_paths = list(dict.fromkeys([*args.files, *args.costs, *args.usage]))
    if not raw_paths:
        parser.error("provide at least one JSON file")
    print(PRIVACY_NOTICE, file=sys.stderr)
    try:
        documents = [(raw_path, json.loads(Path(raw_path).read_text(encoding="utf-8"))) for raw_path in raw_paths]
        print(json.dumps(analyze(documents), ensure_ascii=False, indent=2))
        return 0
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "error", "message": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
