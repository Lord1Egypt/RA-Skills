#!/usr/bin/env python3
"""供应商绩效报告 — 付费版：OTD、质量、响应、综合评分、趋势。

Usage:
    python3 supplier_perf.py --data '{"suppliers":[{"name":"宏达","otd":95,"defect":0.8,"response_h":4,"quarterly_spend":180000}]}'
    python3 supplier_perf.py --data '...' --json
"""

import argparse
import json
import sys


def eval_performance(data: dict) -> dict:
    suppliers = data.get("suppliers", [])
    results = []

    for s in suppliers:
        name = s.get("name", "未命名")
        otd = float(s.get("otd", 90))  # On-Time Delivery %
        defect = float(s.get("defect", 1.0))  # Defect rate %
        response_h = float(s.get("response_h", 8))  # Response time hours
        quarterly_spend = float(s.get("quarterly_spend", 0))

        # OTD score (0-100)
        if otd >= 98:
            otd_score = 100
        elif otd >= 95:
            otd_score = 85 + (otd - 95) * 10 / 3
        elif otd >= 90:
            otd_score = 60 + (otd - 90) * 25 / 5
        elif otd >= 80:
            otd_score = 30 + (otd - 80) * 30 / 10
        else:
            otd_score = max(0, otd * 0.3)

        # Quality score (lower defect = better)
        if defect <= 0.1:
            quality_score = 100
        elif defect <= 0.5:
            quality_score = 90 - (defect - 0.1) * 25
        elif defect <= 1.0:
            quality_score = 70 - (defect - 0.5) * 60
        elif defect <= 2.0:
            quality_score = 40 - (defect - 1.0) * 30
        else:
            quality_score = max(0, 10 - (defect - 2.0) * 10)

        # Response score
        if response_h <= 2:
            response_score = 100
        elif response_h <= 4:
            response_score = 90 - (response_h - 2) * 10
        elif response_h <= 8:
            response_score = 70 - (response_h - 4) * 7.5
        elif response_h <= 24:
            response_score = 40 - (response_h - 8) * 2.5
        else:
            response_score = max(0, 10 - (response_h - 24) * 0.5)

        # Weighted total
        total = otd_score * 0.40 + quality_score * 0.35 + response_score * 0.25

        # Grade
        if total >= 90:
            grade = "A+"
        elif total >= 80:
            grade = "A"
        elif total >= 70:
            grade = "B"
        elif total >= 60:
            grade = "C"
        else:
            grade = "D"

        # Trend indicator (based on current scores)
        if total >= 85:
            trend = "📈 优秀"
        elif total >= 70:
            trend = "➡️ 良好"
        elif total >= 60:
            trend = "📉 需改善"
        else:
            trend = "🔴 风险"

        results.append({
            "name": name,
            "otd": otd,
            "defect": defect,
            "response_h": response_h,
            "quarterly_spend": quarterly_spend,
            "otd_score": round(otd_score, 1),
            "quality_score": round(quality_score, 1),
            "response_score": round(response_score, 1),
            "total": round(total, 1),
            "grade": grade,
            "trend": trend,
        })

    results.sort(key=lambda x: x["total"], reverse=True)
    return {"suppliers": results}


def render_md(data: dict) -> str:
    lines = ["## 📊 供应商绩效报告\n"]

    lines.append("| 排名 | 供应商 | OTD | 不良率 | 响应 | 季度花费 | 综合分 | 等级 | 趋势 |")
    lines.append("|------|--------|-----|--------|------|----------|--------|------|------|")
    for i, s in enumerate(data["suppliers"], 1):
        medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, f" {i}")
        lines.append(
            f"| {medal} | {s['name']} | {s['otd']}% | {s['defect']}% "
            f"| {s['response_h']}h | ¥{s['quarterly_spend']:,.0f} "
            f"| {s['total']} | {s['grade']} | {s['trend']} |"
        )

    lines.append("")
    lines.append("### 📋 详细评分")
    lines.append("")
    lines.append("| 供应商 | 交期得分(40%) | 质量得分(35%) | 响应得分(25%) | 总分 |")
    lines.append("|--------|---------------|---------------|---------------|------|")
    for s in data["suppliers"]:
        lines.append(
            f"| {s['name']} | {s['otd_score']} | {s['quality_score']} "
            f"| {s['response_score']} | {s['total']} |"
        )

    lines.append("")
    lines.append("### 💡 改善建议")
    lines.append("")

    for s in data["suppliers"]:
        issues = []
        if s["otd"] < 95:
            issues.append(f"交期仅{s['otd']}%，需提升物流计划")
        if s["defect"] > 1:
            issues.append(f"不良率{s['defect']}%，超出1%目标")
        if s["response_h"] > 8:
            issues.append(f"响应{s['response_h']}h，需加快沟通")

        if issues:
            lines.append(f"**{s['name']}** ({s['grade']}级):")
            for issue in issues:
                lines.append(f"- {issue}")
            lines.append("")

    # Summary stats
    spends = [s["quarterly_spend"] for s in data["suppliers"]]
    total_spend = sum(spends)
    avg_otd = sum(s["otd"] for s in data["suppliers"]) / len(data["suppliers"]) if data["suppliers"] else 0
    avg_defect = sum(s["defect"] for s in data["suppliers"]) / len(data["suppliers"]) if data["suppliers"] else 0

    lines.append("### 📈 整体表现")
    lines.append(f"- 供应商总数: {len(data['suppliers'])} 家")
    lines.append(f"- 季度总采购: ¥{total_spend:,.0f}")
    lines.append(f"- 平均OTD: {avg_otd:.1f}%")
    lines.append(f"- 平均不良率: {avg_defect:.2f}%")

    lines.append("")
    lines.append("---\n*SupplyFlow 供应商绩效报告 · 付费版*\n")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="供应商绩效报告")
    parser.add_argument("--data", type=str, required=True, help="JSON data")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    data = json.loads(args.data)
    result = eval_performance(data)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render_md(result))


if __name__ == "__main__":
    main()
