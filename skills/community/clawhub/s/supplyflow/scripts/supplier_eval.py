#!/usr/bin/env python3
"""供应商评估基础 — 免费版：多维度评分、排名、基础对比。

Usage:
    python3 supplier_eval.py --suppliers '[{"name":"宏达五金","price_score":8,"quality_score":9,"delivery_score":7,"service_score":6}]'
    python3 supplier_eval.py --file suppliers.json
    python3 supplier_eval.py --suppliers '...' --weights '[0.3,0.35,0.2,0.15]'
"""

import argparse
import json
import sys

DEFAULT_WEIGHTS = {
    "price": 0.30,
    "quality": 0.35,
    "delivery": 0.20,
    "service": 0.15,
}


def evaluate_suppliers(suppliers: list[dict], weights: dict | None = None) -> dict:
    w = weights or DEFAULT_WEIGHTS
    results = []

    for s in suppliers:
        name = s.get("name", "未命名")
        price = float(s.get("price_score", 5))
        quality = float(s.get("quality_score", 5))
        delivery = float(s.get("delivery_score", 5))
        service = float(s.get("service_score", 5))

        total = (
            price * w["price"]
            + quality * w["quality"]
            + delivery * w["delivery"]
            + service * w["service"]
        )

        strengths = []
        weaknesses = []
        dims = {"价格": price, "质量": quality, "交期": delivery, "服务": service}
        for dim, score in dims.items():
            if score >= 8:
                strengths.append(dim)
            elif score <= 5:
                weaknesses.append(dim)

        if total >= 8:
            grade = "A"
        elif total >= 7:
            grade = "B"
        elif total >= 6:
            grade = "C"
        else:
            grade = "D"

        results.append({
            "name": name,
            "price": price,
            "quality": quality,
            "delivery": delivery,
            "service": service,
            "total": round(total, 2),
            "grade": grade,
            "strengths": strengths,
            "weaknesses": weaknesses,
        })

    results.sort(key=lambda x: x["total"], reverse=True)
    return {"suppliers": results, "weights": w}


def render_md(data: dict) -> str:
    suppliers = data["suppliers"]
    w = data["weights"]

    lines = ["## 🏭 供应商评估报告\n"]
    lines.append(f"**评分权重:** 价格{w['price']:.0%} · 质量{w['quality']:.0%} · 交期{w['delivery']:.0%} · 服务{w['service']:.0%}\n")

    lines.append("| 排名 | 供应商 | 价格 | 质量 | 交期 | 服务 | 综合分 | 等级 |")
    lines.append("|------|--------|------|------|------|------|--------|------|")
    for i, s in enumerate(suppliers, 1):
        medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, f" {i}")
        lines.append(
            f"| {medal} | {s['name']} | {s['price']} | {s['quality']} | {s['delivery']} "
            f"| {s['service']} | {s['total']} | {s['grade']} |"
        )

    lines.append("")
    lines.append("### 📊 分析")
    for s in suppliers:
        if s["strengths"]:
            lines.append(f"- **{s['name']}**: 优势={', '.join(s['strengths'])}")
        if s["weaknesses"]:
            lines.append(f"  ⚠️ 待改善={', '.join(s['weaknesses'])}")

    lines.append("")
    lines.append("---\n*SupplyFlow 供应商评估 · 免费版*\n")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="供应商评估工具")
    parser.add_argument("--suppliers", type=str, help="JSON array of suppliers")
    parser.add_argument("--file", type=str, help="JSON file")
    parser.add_argument("--weights", type=str, help="JSON array of 4 weights [price,quality,delivery,service]")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    if args.file:
        with open(args.file) as f:
            suppliers = json.load(f)
    elif args.suppliers:
        suppliers = json.loads(args.suppliers)
    else:
        parser.print_help()
        sys.exit(1)

    weights = None
    if args.weights:
        w = json.loads(args.weights)
        weights = {"price": w[0], "quality": w[1], "delivery": w[2], "service": w[3]}

    data = evaluate_suppliers(suppliers, weights)

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(render_md(data))


if __name__ == "__main__":
    main()
