#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def _pick_first(*values):
    for value in values:
        if value not in (None, "", [], {}):
            return value
    return None


def _summary_from_analysis(host_analysis: dict, source_url: str | None = None) -> dict:
    product = host_analysis.get("product") or {}
    marketing = host_analysis.get("marketing") or {}
    constraints = host_analysis.get("constraints") or {}
    return {
        "productName": _pick_first(product.get("productName"), product.get("productSubtype"), product.get("productType")),
        "productTypeHint": product.get("productType"),
        "detectedForms": product.get("categoryForms") or [x for x in [product.get("productSubtype"), product.get("productType")] if x],
        "sellingPoints": product.get("coreBenefits") or product.get("features") or [],
        "targetAudiences": product.get("targetAudiences") or [],
        "platformHints": marketing.get("platformPreference") or ["tiktok"],
        "contentAngles": marketing.get("contentAngles") or [],
        "creatorTypes": marketing.get("creatorTypes") or [],
        "brand": product.get("brand"),
        "sourcePlatform": (marketing.get("platformPreference") or [None])[0],
        "productUrl": _pick_first(product.get("sourceUrl"), source_url),
        "regions": constraints.get("regions") or [],
        "languages": constraints.get("languages") or ["en"],
    }


def _build_host_analysis(request: dict) -> dict:
    mode = str(request.get("mode") or "")
    raw_input = request.get("rawInput") or ((request.get("input") or {}).get("url")) or ""
    partial = ((request.get("input") or {}).get("partialSignals") or {})
    brief = ((request.get("input") or {}).get("brief") or request.get("brief") or {})
    product_name = _pick_first(
        partial.get("title"),
        brief.get("productName"),
        brief.get("product_name"),
        "Example Product",
    )
    brand = _pick_first(partial.get("brand"), brief.get("brand"), "Example Brand")
    features = [str(x).strip() for x in (partial.get("features") or []) if str(x).strip()][:5]
    source_platform = _pick_first(partial.get("sourcePlatform"), brief.get("platform"), "amazon")
    regions = brief.get("targetMarkets") or brief.get("regions") or ["us"]
    if isinstance(regions, str):
        regions = [regions]
    host_analysis = {
        "product": {
            "productName": product_name,
            "productType": "consumer product",
            "productSubtype": "product from url" if mode == "host_url_analysis_request" else "campaign product",
            "categoryForms": ["consumer product"],
            "coreBenefits": features[:3] or ["clear product value proposition"],
            "functions": features[3:] or ["content-friendly product demo"],
            "targetAudiences": ["relevant creators and shoppers"],
            "brand": brand,
            "price": partial.get("price"),
            "sourceUrl": raw_input,
            "pageTitle": partial.get("title") or product_name,
            "features": features,
        },
        "marketing": {
            "platformPreference": ["tiktok"],
            "creatorTypes": ["lifestyle creator", "review creator"],
            "creatorIntent": ["product review", "problem-solution content"],
            "contentAngles": ["review", "demo", "comparison"],
        },
        "constraints": {
            "regions": [str(x).lower() for x in regions if str(x).strip()] or ["us"],
            "languages": ["en"],
            "hasEmail": True,
        },
    }
    return host_analysis


def main() -> int:
    ap = argparse.ArgumentParser(description="Example hostAnalysis executor for WotoHub")
    ap.add_argument("--input", required=True, help="Path to host analysis request JSON")
    ap.add_argument("--output", help="Path to write executor output JSON")
    args = ap.parse_args()

    request = json.loads(Path(args.input).read_text(encoding="utf-8"))
    host_analysis = _build_host_analysis(request)
    product_summary = _summary_from_analysis(host_analysis, source_url=request.get("rawInput") or ((request.get("input") or {}).get("url")))
    result = {
        "hostAnalysis": host_analysis,
        "productSummary": product_summary,
        "executorMeta": {
            "example": True,
            "mode": request.get("mode"),
        },
    }
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
