#!/usr/bin/env python3
"""库存追踪 — 免费版：实时监控库存水平、预警、价值汇总。

Usage:
    python3 inventory_tracker.py --items '[{"name":"螺丝M6","qty":5000,"min":1000,"unit":"个","cost":0.15}]'
    python3 inventory_tracker.py --file inventory.json
    python3 inventory_tracker.py --items '...' --json
"""

import argparse
import json
import sys


def track_inventory(items: list[dict]) -> dict:
    results = []
    total_value = 0.0
    alerts = []

    for item in items:
        name = item.get("name", "未命名")
        qty = float(item.get("qty", 0))
        min_qty = float(item.get("min", 0))
        unit = item.get("unit", "个")
        unit_cost = float(item.get("cost", 0))

        value = qty * unit_cost
        total_value += value

        if qty <= 0:
            status = "缺货"
            alerts.append(f"🔴 {name}: 库存为0，立即采购！")
        elif qty <= min_qty:
            status = "偏低"
            alerts.append(f"🟡 {name}: 库存{qty}{unit}，低于安全线{min_qty}{unit}")
        elif qty <= min_qty * 1.5:
            status = "关注"
        else:
            status = "正常"

        ratio = (qty / min_qty * 100) if min_qty > 0 else float("inf")

        results.append({
            "name": name,
            "qty": qty,
            "min": min_qty,
            "unit": unit,
            "ratio": f"{ratio:.0f}%",
            "unit_cost": unit_cost,
            "value": value,
            "status": status,
        })

    return {"items": results, "total_value": total_value, "alerts": alerts}


def render_md(data: dict) -> str:
    lines = ["## 📦 库存追踪报告\n"]

    # Summary
    items = data["items"]
    total = data["total_value"]
    alerts = data["alerts"]

    lines.append(f"**库存SKU数:** {len(items)}  |  **总库存价值:** ¥{total:,.2f}\n")

    if alerts:
        lines.append("### ⚠️ 预警")
        for a in alerts:
            lines.append(f"- {a}")
        lines.append("")

    # Table
    lines.append("| 物料 | 数量 | 安全线 | 比率 | 单价 | 价值 | 状态 |")
    lines.append("|------|------|--------|------|------|------|------|")
    for it in items:
        lines.append(
            f"| {it['name']} | {it['qty']:,.0f}{it['unit']} | {it['min']:,.0f}{it['unit']} "
            f"| {it['ratio']} | ¥{it['unit_cost']:.4f} | ¥{it['value']:,.2f} | {it['status']} |"
        )

    lines.append("")
    lines.append("---\n*SupplyFlow 库存追踪 · 免费版*\n")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="库存追踪工具")
    parser.add_argument("--items", type=str, help="JSON array of items")
    parser.add_argument("--file", type=str, help="JSON file with items array")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    if args.file:
        with open(args.file) as f:
            items = json.load(f)
    elif args.items:
        items = json.loads(args.items)
    else:
        parser.print_help()
        sys.exit(1)

    data = track_inventory(items)

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(render_md(data))


if __name__ == "__main__":
    main()
