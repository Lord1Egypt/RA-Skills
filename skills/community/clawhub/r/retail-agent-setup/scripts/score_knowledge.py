#!/usr/bin/env python3
"""
score_knowledge.py — Score the completeness and quality of a retail agent knowledge base

Usage:
    python3 score_knowledge.py --kb <knowledge_base.json> [--role <role_id>] [--report]

Input:  knowledge_base.json — combined output from parse_products.py + parse_policy.py
Output: score report (JSON or human-readable)

Score breakdown (total 100):
  Products     30 pts
  Policies     25 pts
  Promotions   15 pts
  FAQs         15 pts
  Store Info   10 pts
  Staff/Escalation  5 pts
"""

import sys
import json
import argparse
from pathlib import Path


# ─── Scoring dimensions ───────────────────────────────────────────────────────

def score_products(kb: dict) -> dict:
    """Score product catalog completeness. Max 30 pts."""
    products = kb.get("products", [])
    if not products:
        return {"score": 0, "max": 30, "detail": "No products found", "status": "❌"}

    total = len(products)
    has_name      = sum(1 for p in products if p.get("name"))
    has_desc      = sum(1 for p in products if p.get("description"))
    has_price     = sum(1 for p in products if p.get("price"))
    has_category  = sum(1 for p in products if p.get("category"))
    has_variants  = sum(1 for p in products if p.get("variants"))

    # Weighted subscores out of 30
    name_score     = round(has_name / total * 8)
    desc_score     = round(has_desc / total * 10)
    price_score    = round(has_price / total * 7)
    cat_score      = round(has_category / total * 3)
    variant_score  = round(has_variants / total * 2)

    total_score = name_score + desc_score + price_score + cat_score + variant_score
    pct = round(has_desc / total * 100)

    status = "✅" if total_score >= 24 else "⚠️" if total_score >= 15 else "❌"
    return {
        "score": total_score,
        "max": 30,
        "status": status,
        "detail": f"{total} products | descriptions: {pct}% | prices: {round(has_price/total*100)}%",
        "subscores": {
            "names": f"{name_score}/8",
            "descriptions": f"{desc_score}/10",
            "prices": f"{price_score}/7",
            "categories": f"{cat_score}/3",
            "variants": f"{variant_score}/2",
        }
    }


def score_policies(kb: dict) -> dict:
    """Score policy coverage. Max 25 pts."""
    policies = [e for e in kb.get("policy_entries", []) if e.get("type") in ("return", "warranty", "general")]

    critical_policies = {
        "return":    ("退换货政策", 10),
        "warranty":  ("质保/三包政策", 8),
        "general":   ("其他通用政策", 7),
    }

    score = 0
    found = {}
    for ptype, (label, pts) in critical_policies.items():
        matching = [e for e in policies if e.get("type") == ptype and e.get("full_text", "").strip()]
        if matching:
            score += pts
            found[label] = "✅"
        else:
            found[label] = "❌"

    status = "✅" if score >= 20 else "⚠️" if score >= 10 else "❌"
    return {
        "score": score,
        "max": 25,
        "status": status,
        "detail": " | ".join(f"{k}: {v}" for k, v in found.items()),
    }


def score_promotions(kb: dict) -> dict:
    """Score promotion data. Max 15 pts."""
    promos = kb.get("promotions", [])
    if not promos:
        return {"score": 0, "max": 15, "status": "❌", "detail": "No promotions found (add current offers)"}

    active = [p for p in promos if p.get("rules") or p.get("title")]
    score = min(15, len(active) * 5)
    status = "✅" if score >= 10 else "⚠️" if score >= 5 else "❌"
    return {
        "score": score,
        "max": 15,
        "status": status,
        "detail": f"{len(active)} active promotion(s) found",
    }


def score_faqs(kb: dict) -> dict:
    """Score FAQ coverage. Max 15 pts."""
    faqs = kb.get("faqs", [])
    if not faqs:
        return {"score": 0, "max": 15, "status": "❌", "detail": "No FAQs found"}

    score = min(15, len(faqs) * 1)  # 1 pt per FAQ, max 15
    status = "✅" if score >= 10 else "⚠️" if score >= 5 else "❌"
    return {
        "score": score,
        "max": 15,
        "status": status,
        "detail": f"{len(faqs)} FAQ entries",
    }


def score_store_info(kb: dict) -> dict:
    """Score basic store information. Max 10 pts."""
    info = kb.get("store_info", {})
    fields = {
        "name":    ("门店名称", 2),
        "address": ("地址",     2),
        "hours":   ("营业时间", 3),
        "phone":   ("联系方式", 3),
    }
    score = 0
    found = {}
    for key, (label, pts) in fields.items():
        if info.get(key):
            score += pts
            found[label] = "✅"
        else:
            found[label] = "❌"

    status = "✅" if score >= 8 else "⚠️" if score >= 4 else "❌"
    return {
        "score": score,
        "max": 10,
        "status": status,
        "detail": " | ".join(f"{k}: {v}" for k, v in found.items()),
    }


def score_staff(kb: dict) -> dict:
    """Score escalation contact configuration. Max 5 pts."""
    staff = kb.get("staff", [])
    escalation = kb.get("escalation_contact", {})

    has_escalation = bool(escalation.get("name") or escalation.get("wecom_id") or escalation.get("phone"))
    has_staff_list = len(staff) > 0

    score = 0
    if has_escalation:
        score += 4
    if has_staff_list:
        score += 1

    status = "✅" if score >= 4 else "⚠️" if score >= 1 else "❌"
    return {
        "score": score,
        "max": 5,
        "status": status,
        "detail": f"Escalation contact: {'✅' if has_escalation else '❌'} | Staff list: {'✅' if has_staff_list else '❌'}",
    }


# ─── Top-level scoring ────────────────────────────────────────────────────────

def score_knowledge_base(kb: dict, role_id: str = "general") -> dict:
    dimensions = {
        "products":    score_products(kb),
        "policies":    score_policies(kb),
        "promotions":  score_promotions(kb),
        "faqs":        score_faqs(kb),
        "store_info":  score_store_info(kb),
        "staff":       score_staff(kb),
    }

    total = sum(d["score"] for d in dimensions.values())
    max_score = sum(d["max"] for d in dimensions.values())  # always 100

    # Overall status
    if total >= 80:
        overall_status = "✅ Ready to launch"
    elif total >= 60:
        overall_status = "⚠️ Usable — fill gaps before launch"
    elif total >= 40:
        overall_status = "⚠️ Partial — stop and collect more data"
    else:
        overall_status = "❌ Too sparse — cannot launch yet"

    # Gap recommendations
    gaps = []
    if dimensions["products"]["score"] < 20:
        gaps.append("Import or expand product catalog (descriptions are critical)")
    if dimensions["policies"]["score"] < 15:
        gaps.append("Upload return/exchange and warranty policy documents")
    if dimensions["promotions"]["score"] == 0:
        gaps.append("Add current promotions and discount rules")
    if dimensions["faqs"]["score"] < 5:
        gaps.append("Add at least 5–10 common customer FAQs")
    if dimensions["store_info"]["score"] < 6:
        gaps.append("Fill in store name, hours, address, and contact number")
    if dimensions["staff"]["score"] == 0:
        gaps.append("Add at least one escalation contact (manager name + phone/WeCom)")

    return {
        "overall_score": total,
        "overall_status": overall_status,
        "dimensions": dimensions,
        "top_gaps": gaps[:3],  # show top 3 most impactful
        "recommendation": "Proceed to Step 04" if total >= 80 else "Fix top gaps, then re-run score",
    }


# ─── Human-readable report ────────────────────────────────────────────────────

def print_report(result: dict):
    score = result["overall_score"]
    print(f"\n{'═'*50}")
    print(f"  Knowledge Base Score: {score}/100  {result['overall_status']}")
    print(f"{'═'*50}")
    for dim_name, dim in result["dimensions"].items():
        label = dim_name.replace("_", " ").title().ljust(18)
        bar_filled = round(dim["score"] / dim["max"] * 10)
        bar = "█" * bar_filled + "░" * (10 - bar_filled)
        print(f"  {dim['status']} {label} [{bar}] {dim['score']}/{dim['max']}")
        print(f"       {dim['detail']}")
    print(f"{'─'*50}")
    if result["top_gaps"]:
        print("  Top gaps to fix:")
        for i, gap in enumerate(result["top_gaps"], 1):
            print(f"    {i}. {gap}")
    print(f"{'─'*50}")
    print(f"  → {result['recommendation']}")
    print(f"{'═'*50}\n")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Score retail agent knowledge base completeness")
    parser.add_argument("--kb", required=True, help="Path to knowledge_base.json")
    parser.add_argument("--role", default="general", help="Agent role (for role-specific weighting)")
    parser.add_argument("--report", action="store_true", help="Print human-readable report")
    parser.add_argument("--output", default=None, help="Save JSON result to file")
    args = parser.parse_args()

    kb_path = Path(args.kb)
    if not kb_path.exists():
        print(f"Error: File not found: {kb_path}", file=sys.stderr)
        sys.exit(1)

    kb = json.loads(kb_path.read_text(encoding="utf-8"))
    result = score_knowledge_base(kb, args.role)

    if args.report:
        print_report(result)
    
    output_json = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(output_json, encoding="utf-8")
        print(f"✅ Score report saved → {args.output}", file=sys.stderr)
    else:
        if not args.report:
            print(output_json)


if __name__ == "__main__":
    main()
