#!/usr/bin/env python3
"""Analyze Gemini billing and usage JSON locally, without network access."""

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


def nested(row: dict[str, Any], parent: str, child: str) -> Any:
    value = row.get(parent)
    if isinstance(value, dict):
        return value.get(child)
    return row.get(f"{parent}_{child}") or row.get(f"{parent}.{child}")


def decimal_value(value: Any) -> Decimal | None:
    if not isinstance(value, (str, int, float)) or isinstance(value, bool):
        return None
    try:
        return Decimal(str(value))
    except InvalidOperation:
        return None


def integer(value: Any) -> int:
    return int(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else 0


def gemini_text(row: dict[str, Any]) -> str:
    values = [
        nested(row, "service", "description"),
        nested(row, "sku", "description"),
        row.get("service_description"),
        row.get("sku_description"),
        row.get("model"),
        row.get("modelVersion"),
        row.get("description"),
    ]
    return " ".join(str(value).lower() for value in values if value is not None)


def is_gemini_billing_row(row: dict[str, Any]) -> bool:
    if decimal_value(row.get("cost")) is None:
        return False
    text = gemini_text(row)
    return "gemini" in text or "generative language" in text or ("vertex ai" in text and "generative" in text)


def credits_total(row: dict[str, Any]) -> Decimal:
    credits = row.get("credits")
    if not isinstance(credits, list):
        return Decimal("0")
    return sum((decimal_value(item.get("amount")) or Decimal("0") for item in credits if isinstance(item, dict)), Decimal("0"))


def billing_cost(row: dict[str, Any]) -> tuple[Decimal, str] | None:
    if not is_gemini_billing_row(row):
        return None
    cost = decimal_value(row.get("cost"))
    if cost is None:
        return None
    currency = str(row.get("currency") or "USD").upper()
    return cost + credits_total(row), currency


def label_for(row: dict[str, Any]) -> str:
    for value in (nested(row, "sku", "description"), row.get("sku_description"), row.get("model"), row.get("modelVersion"), nested(row, "project", "id")):
        if isinstance(value, str) and value.strip():
            return value.strip()
    return "Gemini API"


def usage_metadata(row: dict[str, Any]) -> dict[str, Any] | None:
    value = row.get("usageMetadata") or row.get("usage_metadata")
    return value if isinstance(value, dict) else None


def document_kind(data: Any) -> str:
    rows = list(walk(data))
    if any(is_gemini_billing_row(row) for row in rows):
        return "billing"
    if any(usage_metadata(row) is not None for row in rows):
        return "usage"
    if any(decimal_value(row.get("cost")) is not None for row in rows):
        return "non_gemini_billing"
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
    projects: set[str] = set()
    for row in walk(data):
        for key in ("usage_start_time", "usageStartTime", "timestamp", "createTime"):
            parsed = parse_time(row.get(key))
            if parsed:
                starts.append(parsed)
        for key in ("usage_end_time", "usageEndTime", "timestamp", "createTime"):
            parsed = parse_time(row.get(key))
            if parsed:
                ends.append(parsed)
        project = nested(row, "project", "id") or row.get("project_id")
        if isinstance(project, str) and project:
            projects.add(project)
    return {"start": min(starts) if starts else None, "end": max(ends) if ends else None, "projects": projects}


def compatibility_warnings(documents: list[tuple[str, Any]]) -> list[str]:
    warnings: list[str] = []
    by_kind: dict[str, list[tuple[str, dict[str, Any]]]] = defaultdict(list)
    for path, data in documents:
        by_kind[document_kind(data)].append((path, document_meta(data)))
    if len(by_kind["billing"]) > 1:
        warnings.append("Multiple Gemini billing exports were provided; overlapping rows may count cost twice.")
    if by_kind["billing"] and by_kind["usage"]:
        bill, usage = by_kind["billing"][0][1], by_kind["usage"][0][1]
        if all((bill["start"], bill["end"], usage["start"], usage["end"])):
            if bill["end"] < usage["start"] or usage["end"] < bill["start"]:
                warnings.append("Billing and usage date ranges do not overlap; usage signals may not describe the billed period.")
        if bill["projects"] and usage["projects"] and bill["projects"].isdisjoint(usage["projects"]):
            warnings.append("Billing and usage project IDs do not overlap; verify that both exports cover the same project.")
    non_gemini = [Path(path).name for path, _ in by_kind["non_gemini_billing"]]
    if non_gemini:
        warnings.append("Billing file(s) contained no clearly identified Gemini rows and were not counted: " + ", ".join(non_gemini))
    unknown = [Path(path).name for path, _ in by_kind["unknown"]]
    if unknown:
        warnings.append("Unrecognized JSON file(s): " + ", ".join(unknown))
    return warnings


def analyze(documents: list[tuple[str, Any]]) -> dict[str, Any]:
    costs: dict[str, Decimal] = defaultdict(Decimal)
    currencies: set[str] = set()
    prompt = candidates = cached = thoughts = tool_prompt = total_tokens = 0
    models: set[str] = set()
    billing_texts: list[str] = []
    large_prompt = False

    for _, data in documents:
        for row in walk(data):
            cost = billing_cost(row)
            if cost:
                value, currency = cost
                costs[label_for(row)] += value
                currencies.add(currency)
                billing_texts.append(gemini_text(row))
            metadata = usage_metadata(row)
            if metadata:
                row_prompt = integer(metadata.get("promptTokenCount") or metadata.get("prompt_token_count"))
                prompt += row_prompt
                candidates += integer(metadata.get("candidatesTokenCount") or metadata.get("candidates_token_count"))
                cached += integer(metadata.get("cachedContentTokenCount") or metadata.get("cached_content_token_count"))
                thoughts += integer(metadata.get("thoughtsTokenCount") or metadata.get("thoughts_token_count"))
                tool_prompt += integer(metadata.get("toolUsePromptTokenCount") or metadata.get("tool_use_prompt_token_count"))
                total_tokens += integer(metadata.get("totalTokenCount") or metadata.get("total_token_count"))
                large_prompt = large_prompt or row_prompt > 200_000
            model = row.get("modelVersion") or row.get("model")
            if isinstance(model, str):
                models.add(model.lower())

    warnings = compatibility_warnings(documents)
    total = sum(costs.values(), Decimal("0"))
    usage_found = prompt + candidates + cached + thoughts + tool_prompt + total_tokens > 0
    base = {"privacy_notice": PRIVACY_NOTICE, "warnings": warnings}
    if total <= 0:
        return {**base, "status": "needs_billing_data" if usage_found else "unsupported", "message": "Gemini usage was found, but no attributable Cloud Billing cost was present." if usage_found else "No supported Gemini billing or usage records were found."}
    if len(currencies) > 1:
        return {**base, "status": "unsupported", "message": "Multiple currencies were found; totals cannot be combined safely."}

    signals: list[str] = []
    rate = Decimal("0.08")
    if prompt and cached / prompt < 0.20:
        rate += Decimal("0.08")
        signals.append("Low cached-content share suggests repeated prompt context may be recoverable with context caching.")
    if any("pro" in model or "ultra" in model for model in models) or any("pro" in text for text in billing_texts):
        rate += Decimal("0.06")
        signals.append("Gemini Pro usage is present; routine tasks may be candidates for Flash routing tests.")
    if not any("batch" in text for text in billing_texts):
        rate += Decimal("0.04")
        signals.append("No Batch SKU appears in billing; asynchronous workloads may be candidates for batch processing.")
    if prompt and (candidates + thoughts) / prompt > 0.30:
        rate += Decimal("0.04")
        signals.append("Generated and thinking tokens are high relative to prompt tokens; tighter output or thinking limits may reduce cost.")
    if large_prompt:
        rate += Decimal("0.04")
        signals.append("At least one prompt exceeded 200K tokens; trimming context may reduce long-context cost.")
    if tool_prompt:
        signals.append("Tool-use prompt tokens are present; simplify tool schemas and pass only relevant tools per request.")
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
        "usage_summary": {"prompt_tokens": prompt, "candidate_tokens": candidates, "cached_content_tokens": cached, "thought_tokens": thoughts, "tool_prompt_tokens": tool_prompt, "total_tokens": total_tokens},
        "disclaimer": "Directional estimate; validate each optimization with a small production test.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze Gemini billing and usage JSON locally.")
    parser.add_argument("files", nargs="*", help="Billing and usage JSON files in any order")
    parser.add_argument("--billing", action="append", default=[], help="Google Cloud Billing JSON (repeatable)")
    parser.add_argument("--usage", action="append", default=[], help="Gemini usageMetadata JSON (repeatable)")
    args = parser.parse_args()
    paths = list(dict.fromkeys([*args.files, *args.billing, *args.usage]))
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
