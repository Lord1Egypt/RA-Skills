#!/usr/bin/env python3
"""供应链风险评估 — 付费版：多维度风险分析、预警、缓解建议。

Usage:
    python3 supply_risk.py --suppliers '[{"name":"A","country":"CN","single_source":false,"lead_days":7,"alt_available":true}]'
    python3 supply_risk.py --suppliers '...' --json
"""

import argparse
import json
import sys

RISK_CATEGORIES = {
    "single_source": {"name": "单一来源", "weight": 0.25, "desc": "无备选供应商"},
    "geography": {"name": "地域集中", "weight": 0.20, "desc": "供应商地域集中"},
    "lead_time": {"name": "交期风险", "weight": 0.15, "desc": "交期过长或波动"},
    "quality": {"name": "质量风险", "weight": 0.20, "desc": "历史质量问题"},
    "financial": {"name": "财务风险", "weight": 0.10, "desc": "供应商财务状况"},
    "dependency": {"name": "依赖度", "weight": 0.10, "desc": "对该供应商依赖度"},
}

HIGH_RISK_COUNTRIES = ["US", "EU", "JP"]  # 高贸易摩擦风险


def assess_risk(suppliers: list[dict]) -> dict:
    results = []
    overall_score = 0

    for s in suppliers:
        name = s.get("name", "未命名")
        country = s.get("country", "CN")
        single_source = s.get("single_source", False)
        lead_days = float(s.get("lead_days", 7))
        alt_available = s.get("alt_available", not single_source)
        defect_rate = float(s.get("defect_rate", 0))
        spend_pct = float(s.get("spend_pct", 10))
        financial_health = s.get("financial_health", "stable")  # stable, warning, critical

        # Calculate sub-scores (0-10, higher = more risky)
        scores = {}

        # Single source risk
        scores["single_source"] = 10 if single_source else (3 if not alt_available else 0)

        # Geography risk
        if country in HIGH_RISK_COUNTRIES:
            scores["geography"] = 8
        elif country == "CN":
            scores["geography"] = 2
        else:
            scores["geography"] = 4

        # Lead time risk
        if lead_days > 60:
            scores["lead_time"] = 9
        elif lead_days > 30:
            scores["lead_time"] = 7
        elif lead_days > 14:
            scores["lead_time"] = 4
        else:
            scores["lead_time"] = 1

        # Quality risk
        if defect_rate > 5:
            scores["quality"] = 10
        elif defect_rate > 2:
            scores["quality"] = 7
        elif defect_rate > 0.5:
            scores["quality"] = 4
        else:
            scores["quality"] = 1

        # Financial risk
        if financial_health == "critical":
            scores["financial"] = 10
        elif financial_health == "warning":
            scores["financial"] = 6
        else:
            scores["financial"] = 1

        # Dependency risk
        if spend_pct > 30:
            scores["dependency"] = 10
        elif spend_pct > 15:
            scores["dependency"] = 7
        elif spend_pct > 5:
            scores["dependency"] = 4
        else:
            scores["dependency"] = 1

        # Weighted total
        total = sum(
            scores[k] * RISK_CATEGORIES[k]["weight"]
            for k in RISK_CATEGORIES
        )

        # Risk level
        if total >= 7:
            level = "高"
            icon = "🔴"
        elif total >= 4:
            level = "中"
            icon = "🟡"
        else:
            level = "低"
            icon = "🟢"

        # Identify top risks
        top_risks = sorted(
            [(k, scores[k]) for k in scores if scores[k] >= 5],
            key=lambda x: x[1],
            reverse=True,
        )

        results.append({
            "name": name,
            "country": country,
            "scores": scores,
            "total": round(total, 1),
            "level": level,
            "icon": icon,
            "top_risks": top_risks,
        })

    overall_score = sum(r["total"] for r in results) / len(results) if results else 0
    high_count = sum(1 for r in results if r["level"] == "高")

    return {
        "suppliers": results,
        "overall_score": round(overall_score, 1),
        "high_risk_count": high_count,
        "total_suppliers": len(results),
    }


def render_md(data: dict) -> str:
    lines = ["## ⚠️ 供应链风险评估报告\n"]

    lines.append(
        f"**评估供应商:** {data['total_suppliers']} 家  |  "
        f"综合风险分: {data['overall_score']:.1f}/10  |  "
        f"高风险: {data['high_risk_count']} 家\n"
    )

    # Summary table
    lines.append("| 供应商 | 国家 | 综合风险 | 等级 | 主要风险 |")
    lines.append("|--------|------|----------|------|----------|")
    for s in data["suppliers"]:
        risk_names = ", ".join(
            RISK_CATEGORIES[k]["name"] for k, _ in s["top_risks"][:2]
        ) or "无显著风险"
        lines.append(
            f"| {s['icon']} {s['name']} | {s['country']} | {s['total']} "
            f"| {s['level']} | {risk_names} |"
        )

    lines.append("")
    lines.append("### 📊 风险维度详情")
    lines.append("")
    lines.append("| 供应商 | 单一来源 | 地域 | 交期 | 质量 | 财务 | 依赖度 |")
    lines.append("|--------|----------|------|------|------|------|--------|")
    for s in data["suppliers"]:
        sc = s["scores"]
        lines.append(
            f"| {s['name']} | {sc['single_source']} | {sc['geography']} | "
            f"{sc['lead_time']} | {sc['quality']} | {sc['financial']} | {sc['dependency']} |"
        )

    lines.append("")
    lines.append("### 💡 缓解建议")
    lines.append("")

    for s in data["suppliers"]:
        if s["level"] in ("高", "中"):
            lines.append(f"**{s['name']}** ({s['level']}风险):")
            if s["scores"]["single_source"] >= 5:
                lines.append("- 开发备选供应商，至少1家合格替代")
            if s["scores"]["geography"] >= 5:
                lines.append("- 考虑本地化或多元化采购渠道")
            if s["scores"]["lead_time"] >= 5:
                lines.append("- 增加安全库存，与供应商协商缩短交期")
            if s["scores"]["quality"] >= 5:
                lines.append("- 加强来料检验，推动供应商质量改善计划")
            if s["scores"]["financial"] >= 5:
                lines.append("- 关注供应商财务状况，准备应急替代方案")
            if s["scores"]["dependency"] >= 5:
                lines.append("- 降低对该供应商的采购占比至15%以下")
            lines.append("")

    lines.append("---\n*SupplyFlow 供应链风险评估 · 付费版*\n")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="供应链风险评估")
    parser.add_argument("--suppliers", type=str, required=True, help="JSON array")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    suppliers = json.loads(args.suppliers)
    data = assess_risk(suppliers)

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(render_md(data))


if __name__ == "__main__":
    main()
