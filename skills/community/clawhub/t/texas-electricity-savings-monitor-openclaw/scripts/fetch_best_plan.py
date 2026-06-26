#!/usr/bin/env python3
"""Fetch the best available electricity plan using the same API sequence as the frontend."""

from __future__ import annotations

import argparse
import json
from typing import Dict, List

from normalize_address_query import normalize_raw_address_query
from powerlego_api import build_personalized_energy_url, get_plan, get_utility, usage_estimator


def clean(value: str | None) -> str:
    return (value or "").strip()


def build_address1(street: str, unit: str) -> str:
    return f"{clean(street)} {clean(unit)}".strip()


def dollars_to_cents(value: object) -> float:
    return round(float(value or 0) * 100, 3)


def normalize_plan(plan: Dict[str, object]) -> Dict[str, object]:
    return {
        "provider": plan.get("provider_name", ""),
        "provider_id": plan.get("provider_id", ""),
        "plan_name": plan.get("plan_name", ""),
        "base_rate": dollars_to_cents(plan.get("base_rate", 0)),
        "base_rate_unit": "¢/kWh",
        "rate": float(plan.get("rate", 0) or 0),
        "rate_unit": "¢/kWh",
        "contract_length": plan.get("contract_term", ""),
    }


def summarize_usage(usage_data: Dict[str, float | int]) -> Dict[str, object]:
    monthly_pairs = [
        (int(month), float(value))
        for month, value in usage_data.items()
    ]
    monthly_pairs.sort(key=lambda item: item[0])

    annual_total = round(sum(value for _, value in monthly_pairs), 2)
    average_monthly = round(annual_total / len(monthly_pairs), 2) if monthly_pairs else 0.0
    peak_month, peak_usage = max(monthly_pairs, key=lambda item: item[1]) if monthly_pairs else (0, 0.0)

    return {
        "annual_total_kwh": annual_total,
        "average_monthly_kwh": average_monthly,
        "peak_month": peak_month,
        "peak_month_kwh": round(peak_usage, 2),
    }


def resolve_address_fields(args: argparse.Namespace) -> Dict[str, str]:
    normalized_query = (
        normalize_raw_address_query(args.address_query)
        if clean(args.address_query)
        else None
    )
    normalized = normalized_query["normalized"] if normalized_query else {}

    street = clean(args.street) or normalized.get("street", "")
    unit = clean(args.unit) or normalized.get("unit", "")
    city = clean(args.city) or normalized.get("city", "")
    state = clean(args.state) or normalized.get("state", "TX")
    zipcode = clean(args.zipcode) or normalized.get("zipcode", "")

    return {
        "street": street,
        "unit": unit,
        "city": city,
        "state": state or "TX",
        "zipcode": zipcode,
        "address1": build_address1(street, unit),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch the best available plan for a confirmed Texas address.",
    )
    parser.add_argument("--address-query", default="")
    parser.add_argument("--street", default="")
    parser.add_argument("--unit", default="")
    parser.add_argument("--city", default="")
    parser.add_argument("--state", default="TX")
    parser.add_argument("--zipcode", default="")
    args = parser.parse_args()

    address = resolve_address_fields(args)
    required_fields = [
        field for field in ("street", "city", "state", "zipcode")
        if not clean(address[field])
    ]
    if required_fields:
        raise SystemExit(
            f"Missing required address fields for plan lookup: {', '.join(required_fields)}"
        )

    usage_response = usage_estimator(
        address1=address["address1"],
        city=address["city"],
        state=address["state"],
        zipcode=address["zipcode"],
    )
    if usage_response.get("status") != 1 or not usage_response.get("usages"):
        raise SystemExit("Usage estimator did not return monthly usage data.")

    usage_data = usage_response["usages"]
    usage_summary = summarize_usage(usage_data)
    utility_response = get_utility(address["zipcode"])
    if not isinstance(utility_response, list) or not utility_response:
        raise SystemExit("Utility lookup did not return any utility codes.")

    selected_utility = utility_response[0]
    utility_code = selected_utility.get("utility_code")
    if not utility_code:
        raise SystemExit("Utility lookup response did not include utility_code.")

    plan_response = get_plan(
        zipcode=address["zipcode"],
        utility_code=utility_code,
        usage_data=usage_data,
    )
    plan_status = (plan_response or {}).get("status")
    plans = ((plan_response or {}).get("response") or {}).get("plans") or []
    normalized_plans: List[Dict[str, object]] = sorted(
        (normalize_plan(plan) for plan in plans),
        key=lambda item: item["rate"],
    )
    top_plans = normalized_plans[:5]
    current_best_plan = top_plans[0] if top_plans else {}
    diagnostic_state = "live_plans_available" if top_plans else "no_live_plans_returned"

    result = {
        "address": address,
        "address_name": ((usage_response.get("address") or {}).get("address") or address["address1"]),
        "current_best_plan": current_best_plan,
        "estimated_usage": {"monthly": usage_data},
        "estimated_usage_summary": usage_summary,
        "esiid": ((usage_response.get("address") or {}).get("esiid") or ""),
        "personalized_energy_url": build_personalized_energy_url(
            city=address["city"],
            zipcode=address["zipcode"],
            address1=address["address1"],
        ),
        "top_plans": top_plans,
        "upstream": {
            "diagnostic_state": diagnostic_state,
            "plan_count": len(plans),
            "plan_status": plan_status,
            "selected_utility_code": utility_code,
            "usage_status": usage_response.get("status"),
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
