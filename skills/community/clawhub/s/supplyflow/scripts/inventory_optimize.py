#!/usr/bin/env python3
"""库存优化建议 — 付费版：EOQ经济批量、安全库存、Reorder Point计算。

Usage:
    python3 inventory_optimize.py --items '[{"name":"轴承6205","monthly_demand":2000,"lead_days":14,"unit_cost":8.5,"holding_rate":0.25}]'
    python3 inventory_optimize.py --items '...' --json
"""

import argparse
import json
import math
import sys


def optimize_inventory(items: list[dict]) -> dict:
    results = []
    total_current_cost = 0.0
    total_optimized_cost = 0.0

    for it in items:
        name = it.get("name", "未命名")
        monthly_demand = float(it.get("monthly_demand", 0))
        annual_demand = monthly_demand * 12
        lead_days = float(it.get("lead_days", 7))
        unit_cost = float(it.get("unit_cost", 0))
        holding_rate = float(it.get("holding_rate", 0.25))  # annual holding cost %
        order_cost = float(it.get("order_cost", 500))  # per order cost
        demand_std = float(it.get("demand_std", monthly_demand * 0.15))  # demand std dev
        service_level = float(it.get("service_level", 0.95))  # target fill rate

        # Z-score for service level
        z_map = {0.90: 1.28, 0.95: 1.65, 0.975: 1.96, 0.99: 2.33}
        z = z_map.get(round(service_level, 3), 1.65)

        # Daily demand
        daily_demand = monthly_demand / 30
        lead_demand = daily_demand * lead_days

        # EOQ (Economic Order Quantity)
        h = unit_cost * holding_rate  # holding cost per unit per year
        if h > 0 and order_cost > 0:
            eoq = math.sqrt(2 * annual_demand * order_cost / h)
        else:
            eoq = monthly_demand

        # Safety Stock = Z * σ_d * √L
        safety_stock = z * demand_std * math.sqrt(lead_days / 30)

        # Reorder Point
        reorder_point = lead_demand + safety_stock

        # Optimal order frequency
        orders_per_year = annual_demand / eoq if eoq > 0 else 12

        # Costs
        ordering_cost = orders_per_year * order_cost
        holding_cost = (eoq / 2 + safety_stock) * h
        total_opt = ordering_cost + holding_cost

        # Current cost (assume order = monthly demand)
        current_orders = 12
        current_ordering = current_orders * order_cost
        current_holding = (monthly_demand / 2 + safety_stock) * h
        total_current = current_ordering + current_holding

        savings = total_current - total_opt

        results.append({
            "name": name,
            "monthly_demand": monthly_demand,
            "unit_cost": unit_cost,
            "eoq": round(eoq),
            "safety_stock": round(safety_stock),
            "reorder_point": round(reorder_point),
            "orders_per_year": round(orders_per_year, 1),
            "ordering_cost": round(ordering_cost),
            "holding_cost": round(holding_cost),
            "total_optimized_cost": round(total_opt),
            "total_current_cost": round(total_current),
            "savings": round(savings),
            "current_stock_days": round(monthly_demand / 30 * 30 / daily_demand) if daily_demand > 0 else 0,
        })

        total_current_cost += total_current
        total_optimized_cost += total_opt

    return {
        "items": results,
        "total_current_cost": round(total_current_cost),
        "total_optimized_cost": round(total_optimized_cost),
        "total_savings": round(total_current_cost - total_optimized_cost),
    }


def render_md(data: dict) -> str:
    lines = ["## 📦 库存优化建议\n"]

    lines.append(
        f"**当前库存成本:** ¥{data['total_current_cost']:,.0f}/年  |  "
        f"优化后成本: ¥{data['total_optimized_cost']:,.0f}/年  |  "
        f"潜在节省: ¥{data['total_savings']:,.0f}/年\n"
    )

    lines.append("| 物料 | EOQ | 安全库存 | 再订货点 | 年订单数 | 当前成本 | 优化成本 | 节省 |")
    lines.append("|------|-----|----------|----------|----------|----------|----------|------|")
    for it in data["items"]:
        savings_icon = "✅" if it["savings"] > 0 else "—"
        lines.append(
            f"| {it['name']} | {it['eoq']:,.0f} | {it['safety_stock']:,.0f} "
            f"| {it['reorder_point']:,.0f} | {it['orders_per_year']} "
            f"| ¥{it['total_current_cost']:,.0f} | ¥{it['total_optimized_cost']:,.0f} "
            f"| {savings_icon} ¥{it['savings']:,.0f} |"
        )

    lines.append("")
    lines.append("### 💡 优化建议")
    lines.append("")

    for it in data["items"]:
        lines.append(f"**{it['name']}:**")
        lines.append(f"- 建议每次订购 **{it['eoq']:,.0f}** 个（经济批量）")
        lines.append(f"- 当库存降至 **{it['reorder_point']:,.0f}** 个时触发补货")
        lines.append(f"- 保持 **{it['safety_stock']:,.0f}** 个安全库存")
        lines.append(f"- 年度建议订货 **{it['orders_per_year']}** 次")
        lines.append("")

    lines.append("---\n*SupplyFlow 库存优化 · 付费版*\n")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="库存优化工具")
    parser.add_argument("--items", type=str, required=True, help="JSON array")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    items = json.loads(args.items)
    data = optimize_inventory(items)

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(render_md(data))


if __name__ == "__main__":
    main()
