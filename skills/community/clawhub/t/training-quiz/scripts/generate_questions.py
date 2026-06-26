#!/usr/bin/env python3
"""
generate_questions.py — Auto-generate quiz questions from the retail knowledge base

Usage:
    python3 generate_questions.py --kb knowledge_base.json \
                                   --count 10 \
                                   [--mode flashcard|mcq|scenario|policy|mixed] \
                                   [--difficulty easy|medium|hard|mixed] \
                                   [--focus products|policies|promotions|all]

Output: JSON array of quiz questions
"""

import json
import random
import argparse
from pathlib import Path


def make_factual_question(product: dict) -> dict | None:
    """Generate a factual recall question from a product entry."""
    name = product.get("name", "")
    if not name:
        return None

    candidates = []

    if product.get("price"):
        candidates.append({
            "question": f"这款「{name}」的售价是多少？",
            "answer": f"¥{product['price']:.0f}",
            "type": "flashcard",
            "difficulty": "easy",
            "category": "pricing",
            "source_sku": product.get("sku"),
        })

    if product.get("description"):
        desc = product["description"][:80]
        candidates.append({
            "question": f"请简单介绍一下「{name}」这款产品的主要特点。",
            "answer": desc,
            "type": "flashcard",
            "difficulty": "medium",
            "category": "product_knowledge",
            "source_sku": product.get("sku"),
        })

    if product.get("suitable_for"):
        suitable = "、".join(product["suitable_for"][:3])
        candidates.append({
            "question": f"「{name}」适合哪类人群使用？",
            "answer": suitable,
            "type": "flashcard",
            "difficulty": "easy",
            "category": "recommendation",
            "source_sku": product.get("sku"),
        })

    variants = product.get("variants", [])
    for v in variants:
        if v.get("attribute") == "size" and v.get("values"):
            sizes = "、".join(v["values"])
            candidates.append({
                "question": f"「{name}」有哪些尺码可以选择？",
                "answer": sizes,
                "type": "flashcard",
                "difficulty": "easy",
                "category": "variants",
                "source_sku": product.get("sku"),
            })
            break

    return random.choice(candidates) if candidates else None


def make_mcq_question(product: dict, all_products: list) -> dict | None:
    """Generate a multiple choice question with distractors."""
    name = product.get("name", "")
    price = product.get("price")
    if not name or not price:
        return None

    price = float(price)
    # Generate distractors
    other_prices = [
        float(p.get("price", 0)) for p in all_products
        if p.get("price") and p.get("name") != name and float(p.get("price", 0)) != price
    ]
    random.shuffle(other_prices)

    options = [price]
    # Add price variants
    options.append(round(price * 1.15, 0))
    options.append(round(price * 0.85, 0))
    if other_prices:
        options.append(other_prices[0])
    else:
        options.append(round(price * 1.3, 0))

    options = list(dict.fromkeys(options))  # deduplicate
    random.shuffle(options)
    correct_idx = options.index(price)
    labels = ["A", "B", "C", "D"]

    return {
        "question": f"「{name}」的正常售价是多少？",
        "options": {labels[i]: f"¥{v:.0f}" for i, v in enumerate(options[:4])},
        "correct": labels[correct_idx],
        "answer": f"¥{price:.0f}",
        "type": "mcq",
        "difficulty": "easy",
        "category": "pricing",
        "source_sku": product.get("sku"),
    }


def make_policy_question(policy: dict) -> dict | None:
    """Generate a policy knowledge question."""
    title = policy.get("title", "")
    conditions = policy.get("conditions", [])
    full_text = policy.get("full_text", "")

    if not title or (not conditions and not full_text):
        return None

    if conditions:
        # Pick one condition as the answer
        condition = random.choice(conditions)
        return {
            "question": f"根据「{title}」，顾客需要满足什么条件才能申请？",
            "answer": condition,
            "type": "flashcard",
            "difficulty": "medium",
            "category": "policy",
            "source_policy": policy.get("policy_id"),
        }

    # True/False from full text
    if full_text:
        return {
            "question": f"关于「{title}」，请简述主要规定。",
            "answer": full_text[:200],
            "type": "flashcard",
            "difficulty": "hard",
            "category": "policy",
            "source_policy": policy.get("policy_id"),
        }
    return None


def make_scenario_question(product: dict, policy: dict | None = None) -> dict | None:
    """Generate a role-play scenario question."""
    name = product.get("name", "")
    suitable = product.get("suitable_for", [])
    if not name:
        return None

    scenarios = []

    if suitable:
        target = random.choice(suitable)
        scenarios.append({
            "question": f"情景练习：顾客问「{name}适合{target}吗？」，你会怎么回答？",
            "answer": f"是的，{name}非常适合{target}。" + (f" {product.get('description', '')[:60]}" if product.get("description") else ""),
            "type": "scenario",
            "difficulty": "medium",
            "category": "recommendation",
        })

    if product.get("price"):
        scenarios.append({
            "question": f"情景练习：顾客看中了「{name}」，但说有点贵，你会怎么说？",
            "answer": "应对价格异议：首先认可顾客的感受，然后强调产品价值（品质/功能/适用场景），可以提及当前活动优惠，以及同价位的对比优势。",
            "type": "scenario",
            "difficulty": "hard",
            "category": "sales_skill",
        })

    if policy:
        scenarios.append({
            "question": f"情景练习：顾客购买{name}后第3天说不满意想退货，你会怎么处理？",
            "answer": f"先表示理解，然后按退货政策处理：{policy.get('full_text', '')[:100]}",
            "type": "scenario",
            "difficulty": "medium",
            "category": "after_sales",
        })

    return random.choice(scenarios) if scenarios else None


def make_faq_question(faq: dict) -> dict | None:
    """Turn a FAQ entry into a quiz question."""
    q = faq.get("question", "")
    a = faq.get("answer", "")
    if not q or not a:
        return None
    return {
        "question": f"如果顾客问：「{q}」，正确答案是什么？",
        "answer": a,
        "type": "flashcard",
        "difficulty": "easy",
        "category": faq.get("category", "faq"),
        "source_faq": faq.get("faq_id"),
    }


def generate_quiz(kb: dict, count: int, mode: str, difficulty: str, focus: str) -> list:
    products = kb.get("products", [])
    policies = kb.get("policy_entries", [])
    faqs = kb.get("faqs", [])

    questions = []

    # Sample source data
    sample_products = random.sample(products, min(len(products), count * 2))
    sample_policies = random.sample(policies, min(len(policies), 5))
    return_policy = next((p for p in policies if p.get("type") == "return"), None)

    for p in sample_products:
        if mode in ("flashcard", "mixed") and focus in ("products", "all"):
            q = make_factual_question(p)
            if q and (difficulty == "mixed" or q["difficulty"] == difficulty):
                questions.append(q)

        if mode in ("mcq", "mixed") and focus in ("products", "all"):
            q = make_mcq_question(p, products)
            if q and (difficulty == "mixed" or q["difficulty"] == difficulty):
                questions.append(q)

        if mode in ("scenario", "mixed"):
            q = make_scenario_question(p, return_policy)
            if q and (difficulty == "mixed" or q["difficulty"] == difficulty):
                questions.append(q)

    for pol in sample_policies:
        if mode in ("policy", "flashcard", "mixed") and focus in ("policies", "all"):
            q = make_policy_question(pol)
            if q and (difficulty == "mixed" or q["difficulty"] == difficulty):
                questions.append(q)

    for faq in faqs[:count]:
        if mode in ("flashcard", "mixed") and focus in ("all",):
            q = make_faq_question(faq)
            if q:
                questions.append(q)

    # Shuffle and trim to requested count
    random.shuffle(questions)
    return questions[:count]


def main():
    parser = argparse.ArgumentParser(description="Generate quiz questions from knowledge base")
    parser.add_argument("--kb", required=True, help="knowledge_base.json path")
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--mode", default="mixed",
                        choices=["flashcard", "mcq", "scenario", "policy", "mixed"])
    parser.add_argument("--difficulty", default="mixed",
                        choices=["easy", "medium", "hard", "mixed"])
    parser.add_argument("--focus", default="all",
                        choices=["products", "policies", "all"])
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    kb = json.loads(Path(args.kb).read_text(encoding="utf-8"))
    questions = generate_quiz(kb, args.count, args.mode, args.difficulty, args.focus)

    result = {
        "total": len(questions),
        "mode": args.mode,
        "difficulty": args.difficulty,
        "questions": questions,
    }

    output_json = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(output_json, encoding="utf-8")
        print(f"✅ Generated {len(questions)} questions → {args.output}", file=__import__("sys").stderr)
    else:
        print(output_json)


if __name__ == "__main__":
    main()
