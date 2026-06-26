#!/usr/bin/env python3
"""成本优化分析 — 付费版：ABC分类、降本潜力、议价空间分析。

Usage:
    python3 cost_optimize.py --items '[{"name":"钢材","monthly_qty":5000,"unit_cost":12,"annual_spend":720000}]'
    python3 cost_optimize.py --items '...' --benchmark '{"钢材":10,"铝材":25}'
"""

import argparse
import json
import sys


def abc_classify(items: list[dict]) -> list[dict]:
    """ABC analysis based on annual spend."""
    total_spend = sum(
        float(it.get("monthly_qty", 0)) * float(it.get("unit_cost", 0)) * 12
        for it in items
    )

    enriched = []
    for it in items:
        monthly_qty = float(it.get("monthly_qty", 0))
        unit_cost = float(it.get("unit_cost", 0))
        monthly_spend = monthly_qty * unit_cost
        annual_spend = monthly_spend * 12

        enriched.append({
            "name": it.get("name", "未命名"),
            "monthly_qty": monthly_qty,
            "unit_cost": unit_cost,
            "monthly_spend": monthly_spend,
            "annual_spend": annual_spend,
            "spend_pct": (annual_spend / total_spend * 100) if total_spend > 0 else 0,
        })

    enriched.sort(key=lambda x: x["annual_spend"], reverse=True)

    cumulative = 0
    for it in enriched:
        cumulative += it["spend_pct"]
        if cumulative <= 80:
            it["abc_class"] = "A"
        elif cumulative <= 95:
            it["abc_class"] = "B"
        else:
            it["abc_class"] = "C"

    return enriched, total_spend


def analyze_costs(items: list[dict], benchmark: dict | None = None) -> dict:
    classified, total_spend = abc_classify(items)

    analysis = []
    total_savings = 0.0

    for it in classified:
        name = it["name"]
        annual = it["annual_spend"]
        abc = it["abc_class"]
        unit_cost = it["unit_cost"]

        # Benchmark comparison
        bench_price = benchmark.get(name) if benchmark else None
        bench_gap = None
        bench_savings = 0

        if bench_price and bench_price < unit_cost:
            bench_gap = round((unit_cost - bench_price) / unit_cost * 100, 1)
            bench_savings = (unit_cost - bench_price) * it["monthly_qty"] * 12
            total_savings += bench_savings

        # Volume discount potential
        if abc == "A":
            discount_potential = 0.05  # 5% for A items
        elif abc == "B":
            discount_potential = 0.03
        else:
            discount_potential = 0.01

        volume_savings = annual * discount_potential
        total_savings += volume_savings

        # Sourcing strategy
        if abc == "A":
            strategy = "战略合作 / 长期协议 / 年度招标"
        elif abc == "B":
            strategy = "定期比价 / 多源采购"
        else:
            strategy = "标准化 / 集中采购 / 框架协议"

        analysis.append({
            **it,
            "bench_price": bench_price,
            "bench_gap": bench_gap,
            "bench_savings": bench_savings,
            "discount_potential": discount_potential,
            "volume_savings": volume_savings,
            "total_potential_savings": bench_savings + volume_savings,
            "strategy": strategy,
        })

    return {
        "items": analysis,
        "total_annual_spend": total_spend,
        "total_potential_savings": total_savings,
        "savings_pct": round(total_savings / total_spend * 100, 1) if total_spend > 0 else 0,
        "abc_summary": {
            "A": sum(1 for i in analysis if i["abc_class"] == "A"),
            "B": sum(1 for i in analysis if i["abc_class"] == "B"),
            "C": sum(1 for i in analysis if i["abc_class"] == "C"),
        },
    }


def render_md(data: dict) -> str:
    lines = ["## 💰 成本优化分析报告\n"]

    lines.append(
        f"**年度总采购额:** ¥{data['total_annual_spend']:,.2f}  |  "
        f"潜在降本: ¥{data['total_potential_savings']:,.2f} ({data['savings_pct']:.1f}%)\n"
    )

    # ABC Summary
    abc = data["abc_summary"]
    lines.append(
        f"**ABC分类:** A类={abc['A']}项(80%金额) · B类={abc['B']}项(15%) · C类={abc['C']}项(5%)\n"
    )

    # Detail table
    lines.append("| 分类 | 物料 | 月用量 | 单价 | 年花费 | 价差 | 潜在节省 | 策略 |")
    lines.append("|------|------|--------|------|--------|------|----------|------|")
    for it in data["items"]:
        gap_str = f"{it['bench_gap']}%" if it["bench_gap"] is not None else "—"
        savings_str = f"¥{it['total_potential_savings']:,.0f}"
        lines.append(
            f"| {it['abc_class']} | {it['name']} | {it['monthly_qty']:,.0f} "
            f"| ¥{it['unit_cost']:.2f} | ¥{it['annual_spend']:,.0f} "
            f"| {gap_str} | {savings_str} | {it['strategy']} |"
        )

    lines.append("")
    lines.append("### 🎯 重点降本建议")
    lines.append("")

    # Top 3 savings opportunities
    top3 = sorted(data["items"], key=lambda x: x["total_potential_savings"], reverse=True)[:3]
    for it in top3:
        if it["total_potential_savings"] > 0:
            lines.append(
                f"- **{it['name']}** ({it['abc_class']}类): 年花费¥{it['annual_spend']:,.0f}，"
                f"潜在节省¥{it['total_potential_savings']:,.0f}"
            )
            if it["bench_gap"]:
                lines.append(f"  当前价高于市场{it['bench_gap']}%，建议重新议价或引入竞争")
            lines.append(f"  推荐策略: {it['strategy']}")

    lines.append("")
    lines.append("---\n*SupplyFlow 成本优化分析 · 付费版*\n")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="成本优化分析")
    parser.add_argument("--items", type=str, required=True, help="JSON array of items")
    parser.add_argument("--benchmark", type=str, help="JSON: {\"name\": benchmark_price}")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    items = json.loads(args.items)
    benchmark = json.loads(args.benchmark) if args.benchmark else None
    data = analyze_costs(items, benchmark)

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(render_md(data))


if __name__ == "__main__":
    main()
