#!/usr/bin/env python3
"""基础记账工具 - 免费版
用法:
  python3 bookkeeping.py --action add --date 2024-03-15 --category 办公费 --amount 2825 --desc "购买办公用品"
  python3 bookkeeping.py --action list [--month 2024-03] [--category 办公费]
  python3 bookkeeping.py --action summary [--month 2024-03]
  python3 bookkeeping.py --action delete --id <记录ID>

数据存储在脚本同目录下的 bookkeeping_data.json
"""

import argparse
import json
import os
import sys
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bookkeeping_data.json")

CATEGORIES = {
    "收入": {"type": "income", "color": "🟢"},
    "办公费": {"type": "expense", "color": "🔵"},
    "差旅费": {"type": "expense", "color": "🟡"},
    "工资": {"type": "expense", "color": "🔴"},
    "采购": {"type": "expense", "color": "🟣"},
    "服务费": {"type": "expense", "color": "🟠"},
    "房租": {"type": "expense", "color": "⚪"},
    "水电费": {"type": "expense", "color": "⚪"},
    "交通费": {"type": "expense", "color": "🟤"},
    "招待费": {"type": "expense", "color": "🟠"},
    "其他": {"type": "expense", "color": "⚪"},
}


def load_data():
    """加载记账数据"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"records": [], "next_id": 1}


def save_data(data):
    """保存记账数据"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_record(data, date, category, amount, desc, invoice_no=""):
    """添加记账记录"""
    record = {
        "id": data["next_id"],
        "date": date,
        "category": category,
        "amount": amount,
        "desc": desc,
        "invoice_no": invoice_no,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    cat_info = CATEGORIES.get(category, CATEGORIES["其他"])
    record["type"] = cat_info["type"]

    data["records"].append(record)
    data["next_id"] += 1
    return record


def list_records(data, month=None, category=None, limit=50):
    """列出记账记录"""
    records = data["records"]

    if month:
        records = [r for r in records if r["date"].startswith(month)]
    if category:
        records = [r for r in records if r["category"] == category]

    # 按日期倒序
    records = sorted(records, key=lambda x: x["date"], reverse=True)
    return records[:limit]


def get_summary(data, month=None):
    """生成汇总"""
    records = data["records"]
    if month:
        records = [r for r in records if r["date"].startswith(month)]

    summary = {
        "period": month or "全部",
        "total_income": 0,
        "total_expense": 0,
        "net": 0,
        "by_category": {},
        "count": len(records),
    }

    for r in records:
        if r["type"] == "income":
            summary["total_income"] += r["amount"]
        else:
            summary["total_expense"] += r["amount"]
            cat = r["category"]
            if cat not in summary["by_category"]:
                summary["by_category"][cat] = 0
            summary["by_category"][cat] += r["amount"]

    summary["net"] = summary["total_income"] - summary["total_expense"]
    return summary


def format_record(r):
    cat_info = CATEGORIES.get(r["category"], CATEGORIES["其他"])
    sign = "+" if r["type"] == "income" else "-"
    return (
        f"  #{r['id']:04d} {r['date']} {cat_info['color']} {r['category']:<8s} "
        f"{sign}¥{r['amount']:>10,.2f}  {r['desc']}"
    )


def format_summary(s):
    lines = [
        f"\n📊 财务汇总 ({s['period']})",
        "=" * 50,
        f"  记录数: {s['count']} 条",
        f"  总收入: ¥{s['total_income']:>12,.2f} 🟢",
        f"  总支出: ¥{s['total_expense']:>12,.2f} 🔴",
        f"  净{'利润' if s['net'] >= 0 else '亏损'}: ¥{abs(s['net']):>11,.2f} {'🟢' if s['net'] >= 0 else '🔴'}",
    ]

    if s["by_category"]:
        lines.append("\n  📂 按类别:")
        sorted_cats = sorted(s["by_category"].items(), key=lambda x: x[1], reverse=True)
        for cat, amount in sorted_cats:
            cat_info = CATEGORIES.get(cat, CATEGORIES["其他"])
            pct = (amount / s["total_expense"] * 100) if s["total_expense"] > 0 else 0
            lines.append(f"    {cat_info['color']} {cat:<8s} ¥{amount:>10,.2f}  ({pct:.1f}%)")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="基础记账工具")
    parser.add_argument("--action", choices=["add", "list", "summary", "delete"],
                        required=True, help="操作类型")
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"),
                        help="日期 (YYYY-MM-DD)")
    parser.add_argument("--category", help=f"类别: {', '.join(CATEGORIES.keys())}")
    parser.add_argument("--amount", type=float, help="金额")
    parser.add_argument("--desc", help="描述")
    parser.add_argument("--invoice-no", default="", help="发票号码")
    parser.add_argument("--month", help="筛选月份 (YYYY-MM)")
    parser.add_argument("--id", type=int, help="记录ID")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    args = parser.parse_args()

    data = load_data()

    if args.action == "add":
        if not args.category or args.amount is None:
            print("❌ 添加记录需要 --category 和 --amount")
            sys.exit(1)
        if args.category not in CATEGORIES:
            print(f"❌ 未知类别: {args.category}")
            print(f"支持的类别: {', '.join(CATEGORIES.keys())}")
            sys.exit(1)

        record = add_record(data, args.date, args.category, args.amount,
                            args.desc or "", args.invoice_no)
        save_data(data)

        if args.json:
            print(json.dumps(record, ensure_ascii=False, indent=2))
        else:
            print(f"✅ 记录已添加:")
            print(format_record(record))

    elif args.action == "list":
        records = list_records(data, args.month, args.category)
        if not records:
            print("📭 暂无记录")
            return

        if args.json:
            print(json.dumps(records, ensure_ascii=False, indent=2))
        else:
            print(f"\n📋 记账记录 ({len(records)} 条)")
            print("=" * 50)
            for r in records:
                print(format_record(r))

    elif args.action == "summary":
        summary = get_summary(data, args.month)
        if args.json:
            print(json.dumps(summary, ensure_ascii=False, indent=2))
        else:
            print(format_summary(summary))

    elif args.action == "delete":
        if args.id is None:
            print("❌ 删除记录需要 --id")
            sys.exit(1)

        before = len(data["records"])
        data["records"] = [r for r in data["records"] if r["id"] != args.id]
        after = len(data["records"])

        if before == after:
            print(f"❌ 未找到ID为 {args.id} 的记录")
        else:
            save_data(data)
            print(f"✅ 已删除记录 #{args.id}")


if __name__ == "__main__":
    main()
