#!/usr/bin/env python3
"""采购订单模板 — 免费版：生成标准化PO、自动编号、金额计算。

Usage:
    python3 purchase_order.py --supplier "宏达五金" --items '[{"name":"螺丝M6","qty":10000,"price":0.12}]'
    python3 purchase_order.py --supplier "宏达五金" --items '...' --buyer "采购部" --date "2025-03-15"
    python3 purchase_order.py --supplier "A" --items '...' --file /tmp/po.json
"""

import argparse
import json
import sys
from datetime import datetime


def generate_po(supplier: str, items: list[dict], buyer: str = "采购部",
                date: str | None = None, po_no: str | None = None) -> dict:
    now = datetime.now()
    po_date = date or now.strftime("%Y-%m-%d")
    po_number = po_no or f"PO-{now.strftime('%Y%m%d')}-{hash(supplier) % 10000:04d}"

    lines = []
    total = 0.0
    for i, item in enumerate(items, 1):
        name = item.get("name", "未命名")
        qty = float(item.get("qty", 0))
        price = float(item.get("price", 0))
        spec = item.get("spec", "—")
        amount = qty * price
        total += amount
        lines.append({
            "line": i,
            "name": name,
            "spec": spec,
            "qty": qty,
            "unit": item.get("unit", "个"),
            "price": price,
            "amount": amount,
        })

    tax = total * 0.13  # 默认13%增值税
    grand_total = total + tax

    return {
        "po_no": po_number,
        "date": po_date,
        "supplier": supplier,
        "buyer": buyer,
        "lines": lines,
        "subtotal": total,
        "tax": tax,
        "tax_rate": "13%",
        "grand_total": grand_total,
    }


def render_md(po: dict) -> str:
    lines = [
        f"## 📋 采购订单 (Purchase Order)",
        "",
        f"| 项目 | 内容 |",
        f"|------|------|",
        f"| **订单编号** | {po['po_no']} |",
        f"| **日期** | {po['date']} |",
        f"| **供应商** | {po['supplier']} |",
        f"| **采购方** | {po['buyer']} |",
        "",
        "### 订单明细",
        "",
        "| 行号 | 物料 | 规格 | 数量 | 单位 | 单价 | 金额 |",
        "|------|------|------|------|------|------|------|",
    ]

    for l in po["lines"]:
        lines.append(
            f"| {l['line']} | {l['name']} | {l['spec']} | {l['qty']:,.0f} "
            f"| {l['unit']} | ¥{l['price']:.4f} | ¥{l['amount']:,.2f} |"
        )

    lines.extend([
        "",
        f"**小计:** ¥{po['subtotal']:,.2f}",
        f"**增值税 ({po['tax_rate']}):** ¥{po['tax']:,.2f}",
        f"**合计:** ¥{po['grand_total']:,.2f}",
        "",
        "---",
        "*SupplyFlow 采购订单模板 · 免费版*",
        "",
    ])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="采购订单生成")
    parser.add_argument("--supplier", type=str, required=True, help="供应商名称")
    parser.add_argument("--items", type=str, required=True, help="JSON array of line items")
    parser.add_argument("--buyer", type=str, default="采购部", help="采购方")
    parser.add_argument("--date", type=str, help="订单日期 YYYY-MM-DD")
    parser.add_argument("--po-no", type=str, help="订单编号")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    items = json.loads(args.items)
    po = generate_po(args.supplier, items, args.buyer, args.date, args.po_no)

    if args.json:
        print(json.dumps(po, ensure_ascii=False, indent=2))
    else:
        print(render_md(po))


if __name__ == "__main__":
    main()
