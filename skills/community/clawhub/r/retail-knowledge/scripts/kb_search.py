#!/usr/bin/env python3
"""
kb_search.py — Search the retail knowledge base by query string

Usage:
    python3 kb_search.py --kb <knowledge_base.json> --query "<text>" \
                          [--domain products|policies|promotions|faqs|all] \
                          [--top 3]

Output: JSON array of top matching entries with relevance scores
"""

import sys
import json
import re
import argparse
from pathlib import Path


# ─── Field weights for relevance scoring ─────────────────────────────────────

PRODUCT_WEIGHTS = {
    "name": 3,
    "tags": 2,
    "description": 1,
    "category": 1,
    "subcategory": 1,
    "suitable_for": 2,
}

POLICY_WEIGHTS = {
    "title": 3,
    "keywords": 2,
    "full_text": 1,
    "type": 1,
}

PROMO_WEIGHTS = {
    "title": 3,
    "rules": 2,
    "applicable_to": 2,
    "type": 1,
}

FAQ_WEIGHTS = {
    "question": 3,
    "keywords": 2,
    "answer": 1,
    "category": 1,
}


# ─── Tokenizer (simple; handles Chinese & Latin) ─────────────────────────────

def tokenize(text: str) -> set[str]:
    """Split text into tokens: Chinese chars + Latin words."""
    if not text:
        return set()
    # Extract individual Chinese chars (each is a token)
    chinese = set(re.findall(r"[\u4e00-\u9fff]", text))
    # Extract Latin words
    latin = set(w.lower() for w in re.findall(r"[a-zA-Z0-9]+", text) if len(w) > 1)
    # Also add bigrams for Chinese (2-char n-grams)
    text_cn = re.sub(r"[^\u4e00-\u9fff]", "", text)
    bigrams = {text_cn[i:i+2] for i in range(len(text_cn)-1)}
    return chinese | latin | bigrams


def score_entry(entry: dict, query_tokens: set[str], weights: dict) -> float:
    """Score a KB entry against query tokens using field weights."""
    total = 0.0
    for field, weight in weights.items():
        value = entry.get(field)
        if not value:
            continue
        # Flatten lists to string
        if isinstance(value, list):
            value = " ".join(str(v) for v in value)
        field_tokens = tokenize(str(value))
        overlap = len(query_tokens & field_tokens)
        total += overlap * weight
    return total


# ─── Domain-specific search ───────────────────────────────────────────────────

def search_products(products: list, query_tokens: set, top: int) -> list:
    scored = []
    for p in products:
        s = score_entry(p, query_tokens, PRODUCT_WEIGHTS)
        if s > 0:
            scored.append({"score": s, "domain": "product", "entry": p})
    return sorted(scored, key=lambda x: x["score"], reverse=True)[:top]


def search_policies(policies: list, query_tokens: set, top: int) -> list:
    # Also boost by explicit type match
    TYPE_KEYWORDS = {
        "return":    {"退货", "退款", "退换", "无理由", "七天", "7天"},
        "warranty":  {"保修", "质保", "三包", "维修"},
        "promotion": {"活动", "优惠", "折扣", "满减", "赠品"},
        "membership": {"会员", "积分", "等级", "vip"},
    }
    scored = []
    for p in policies:
        s = score_entry(p, query_tokens, POLICY_WEIGHTS)
        # Type boost: if query tokens match a type's keywords, boost matching type entries
        for ptype, type_kws in TYPE_KEYWORDS.items():
            if query_tokens & type_kws and p.get("type") == ptype:
                s += 3
        if s > 0:
            scored.append({"score": s, "domain": "policy", "entry": p})
    return sorted(scored, key=lambda x: x["score"], reverse=True)[:top]


def search_promotions(promos: list, query_tokens: set, top: int) -> list:
    from datetime import datetime, timezone
    today = datetime.now(timezone.utc).date().isoformat()
    scored = []
    for p in promos:
        # Skip expired promotions
        end_date = p.get("end_date")
        if end_date and end_date < today:
            continue
        s = score_entry(p, query_tokens, PROMO_WEIGHTS)
        if s > 0:
            scored.append({"score": s, "domain": "promotion", "entry": p})
    return sorted(scored, key=lambda x: x["score"], reverse=True)[:top]


def search_faqs(faqs: list, query_tokens: set, top: int) -> list:
    scored = []
    for f in faqs:
        s = score_entry(f, query_tokens, FAQ_WEIGHTS)
        if s > 0:
            scored.append({"score": s, "domain": "faq", "entry": f})
    return sorted(scored, key=lambda x: x["score"], reverse=True)[:top]


# ─── Main search dispatcher ───────────────────────────────────────────────────

def search(kb: dict, query: str, domain: str = "all", top: int = 3) -> list:
    query_tokens = tokenize(query)
    if not query_tokens:
        return []

    results = []

    if domain in ("products", "all"):
        results += search_products(kb.get("products", []), query_tokens, top)

    if domain in ("policies", "all"):
        results += search_policies(kb.get("policy_entries", []), query_tokens, top)

    if domain in ("promotions", "all"):
        results += search_promotions(kb.get("promotions", []), query_tokens, top)

    if domain in ("faqs", "all"):
        results += search_faqs(kb.get("faqs", []), query_tokens, top)

    # For "all" mode, re-rank globally and return top N
    if domain == "all":
        results = sorted(results, key=lambda x: x["score"], reverse=True)[:top]

    return results


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Search retail knowledge base")
    parser.add_argument("--kb", required=True, help="Path to knowledge_base.json")
    parser.add_argument("--query", required=True, help="Search query text")
    parser.add_argument("--domain", default="all",
                        choices=["products", "policies", "promotions", "faqs", "all"])
    parser.add_argument("--top", type=int, default=3, help="Max results to return")
    parser.add_argument("--scores", action="store_true", help="Include relevance scores in output")
    args = parser.parse_args()

    kb_path = Path(args.kb)
    if not kb_path.exists():
        print(f"Error: Knowledge base not found: {kb_path}", file=sys.stderr)
        sys.exit(1)

    kb = json.loads(kb_path.read_text(encoding="utf-8"))
    results = search(kb, args.query, args.domain, args.top)

    if not results:
        print(json.dumps({"results": [], "found": 0}, ensure_ascii=False))
        return

    output = []
    for r in results:
        item = {"domain": r["domain"], "entry": r["entry"]}
        if args.scores:
            item["relevance_score"] = r["score"]
        output.append(item)

    print(json.dumps({"results": output, "found": len(output)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
