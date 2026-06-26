#!/usr/bin/env python3
"""
预算管理工具

支持设定月度分类预算、查询执行进度、超支预警、预算模板生成。
纯 Python 标准库，基础功能零外部依赖。

用法:
    python budget.py /path/to/ledger.csv --set 餐饮 2000
    python budget.py /path/to/ledger.csv --set 交通 800
    python budget.py /path/to/ledger.csv --progress 2026-05
    python budget.py /path/to/ledger.csv --alert 2026-05
    python budget.py /path/to/ledger.csv --template 15000
    python budget.py /path/to/ledger.csv --template 15000 --ratio 40 30 20 10
    python budget.py /path/to/ledger.csv --list
    python budget.py /path/to/ledger.csv --remove 餐饮
"""

import csv
import re
import sys
import argparse
import json
from datetime import datetime
from pathlib import Path

def _safe_write_path(path: Path) -> bool:
    """安全校验：只允许写入 ~/.openclaw/workspace/ 范围内的路径，返回 True/False"""
    try:
        if str(path.resolve()).startswith(str(Path.home() / ".openclaw" / "workspace")):
            return True
    except Exception:
        pass
    return False

from collections import defaultdict


# ==================== 默认分类 ====================

DEFAULT_CATEGORIES = [
    "餐饮", "交通", "居住", "购物", "娱乐",
    "医疗", "通讯", "教育", "社交", "其他",
]

# 50/30/20 法则默认比例
TEMPLATE_503020 = {
    "餐饮": 0.18,
    "交通": 0.07,
    "居住": 0.22,
    "购物": 0.07,
    "娱乐": 0.07,
    "医疗": 0.02,
    "通讯": 0.02,
    "教育": 0.03,
    "社交": 0.04,
    "其他": 0.01,
}


# ==================== 预算文件操作 ====================

def _budget_path(ledger_path: str) -> Path:
    """预算文件路径：与账本同目录，后缀 .budget.json。"""
    p = Path(ledger_path)
    return p.parent / (p.stem + ".budget.json")


def load_budgets(ledger_path: str) -> dict:
    """加载预算配置。"""
    bp = _budget_path(ledger_path)
    if bp.exists():
        data = json.loads(bp.read_text(encoding="utf-8"))
        return data
    return {"meta": {"created": None, "updated": None}, "categories": {}}


def save_budgets(ledger_path: str, data: dict):
    """保存预算配置。"""
    bp = _budget_path(ledger_path)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    if not data.get("meta", {}).get("created"):
        data.setdefault("meta", {})["created"] = now
    data["meta"]["updated"] = now
    if not _safe_write_path(bp):
        raise ValueError(f"不允许写入该路径：{bp}（必须在 ~/.openclaw/workspace/ 范围内）")
    bp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# ==================== 账本解析 ====================

def parse_csv_ledger(filepath: str, month: str = None) -> dict:
    """
    解析 CSV 格式账本，提取指定月份的各分类支出。
    month: YYYY-MM 格式，None 则返回全部
    返回 {分类名: 金额, ...}
    格式: 日期,类型,金额,分类,描述,账户
    """
    p = Path(filepath)
    if not p.exists():
        print(f"❌ 账本文件不存在: {filepath}")
        sys.exit(1)

    # 解析目标月份
    target_prefix = None
    if month:
        # month 格式: 2026-05 -> 匹配 2026-05-DD
        target_prefix = month.strip()  # e.g. "2026-05"

    content = p.read_text(encoding="utf-8-sig")
    expenses = defaultdict(float)

    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # 跳过余额行
        if line.startswith("余额,"):
            continue

        parts = next(csv.reader([line]))
        if len(parts) < 6:
            continue

        date_str = parts[0].strip()
        txn_type = parts[1].strip()
        try:
            amount = float(parts[2].strip())
        except ValueError:
            continue

        category = parts[3].strip()

        if txn_type == "余额":
            continue

        if not re.match(r"\d{4}-\d{2}-\d{2}", date_str):
            continue

        # 按月份过滤
        if target_prefix and not date_str.startswith(target_prefix):
            continue

        # 只统计支出
        if txn_type == "支出":
            # 取一级分类
            root_cat = category.split(":")[0] if category else "其他"
            expenses[root_cat] += amount

    return {k: v for k, v in expenses.items() if v > 0}


# ==================== 核心逻辑 ====================

def set_budget(ledger_path: str, category: str, amount: float):
    """设定/更新分类预算。"""
    data = load_budgets(ledger_path)
    data["categories"][category] = round(amount, 2)
    save_budgets(ledger_path, data)
    print(f"✅ 已设定预算：{category} = ¥{amount:,.2f}/月")


def remove_budget(ledger_path: str, category: str):
    """移除分类预算。"""
    data = load_budgets(ledger_path)
    if category in data["categories"]:
        del data["categories"][category]
        save_budgets(ledger_path, data)
        print(f"🗑️  已移除预算：{category}")
    else:
        print(f"⚠️  未找到预算：{category}")


def list_budgets(ledger_path: str):
    """列出所有预算。"""
    data = load_budgets(ledger_path)
    cats = data.get("categories", {})

    if not cats:
        print("\n  尚未设定任何预算。\n")
        print("  使用 --set 分类 金额 来添加预算。")
        print("  使用 --template 月收入 来生成模板。\n")
        return

    total = sum(cats.values())
    print(f"\n{'='*55}")
    print(f"  📐 当前预算配置（合计 ¥{total:,.2f}/月）")
    print(f"{'='*55}")
    print(f"  {'分类':<16} {'预算':>12} {'占比':>8}")
    print(f"  {'─'*40}")
    for cat, amt in sorted(cats.items(), key=lambda x: x[1], reverse=True):
        pct = (amt / total * 100) if total > 0 else 0
        print(f"  {cat:<16} {fmt(amt):>12} {pct:>7.1f}%")
    print(f"  {'─'*40}")
    print(f"  {'合计':<16} {fmt(total):>12}")
    print(f"{'='*55}\n")


def get_progress(ledger_path: str, month: str) -> list:
    """计算预算执行进度。返回 [(分类, 已花费, 预算, 百分比), ...]"""
    data = load_budgets(ledger_path)
    budgets = data.get("categories", {})

    if not budgets:
        print("⚠️  尚未设定预算。使用 --set 或 --template 先设定。")
        return []
    else:
        # 有预算定义（即使当月无消费），正常计算进度
        pass

    actual = parse_csv_ledger(ledger_path, month=month)
    month_actual = actual

    results = []
    for cat, budget_amt in sorted(budgets.items()):
        spent = month_actual.get(cat, 0.0)
        pct = (spent / budget_amt * 100) if budget_amt > 0 else 0
        results.append((cat, spent, budget_amt, pct))

    return results


def print_progress(ledger_path: str, month: str):
    """打印预算执行进度。"""
    results = get_progress(ledger_path, month)
    if not results:
        return

    month_display = _month_display(month)
    total_spent = sum(r[1] for r in results)
    total_budget = sum(r[2] for r in results)

    print(f"\n📊 {month_display} 预算执行情况\n")
    print(f"  {'分类':<16} {'已花':>12} {'预算':>12} {'进度':>20} {'状态'}")
    print(f"  {'─'*72}")

    for cat, spent, budget, pct in results:
        bar = _make_bar(pct, 18)
        status = _status_label(pct)
        print(f"  {cat:<16} {fmt(spent):>12} / {fmt(budget):<10} {bar} {pct:>5.1f}%  {status}")

    print(f"  {'─'*72}")
    total_pct = (total_spent / total_budget * 100) if total_budget > 0 else 0
    total_bar = _make_bar(min(total_pct, 150), 18)
    total_status = _status_label(total_pct)
    print(f"  {'合计':<16} {fmt(total_spent):>12} / {fmt(total_budget):<10} {total_bar} {total_pct:>5.1f}%  {total_status}")
    print()


def print_alert(ledger_path: str, month: str):
    """打印超支预警。"""
    results = get_progress(ledger_path, month)
    if not results:
        return

    month_display = _month_display(month)
    alerts = [(cat, spent, budget, pct) for cat, spent, budget, pct in results if pct >= 80]

    if not alerts:
        print(f"\n✅ {month_display} 所有分类预算状态良好（均 < 80%）\n")
        return

    alerts.sort(key=lambda x: x[3], reverse=True)

    print(f"\n🚨 {month_display} 预算预警\n")

    over_budget = [a for a in alerts if a[3] >= 100]
    near_budget = [a for a in alerts if 80 <= a[3] < 100]

    if over_budget:
        print(f"  ❌ 已超支（{len(over_budget)} 项）：")
        for cat, spent, budget, pct in over_budget:
            over = spent - budget
            print(f"     {cat:<16} 超 {fmt(over):>10}（{pct:.1f}%）")
        total_over = sum(a[1] - a[2] for a in over_budget)
        print(f"     {'超支合计：':<16} {fmt(total_over):>10}")

    if near_budget:
        print(f"\n  ⚠️ 接近上限（{len(near_budget)} 项，剩余 < 20%）：")
        for cat, spent, budget, pct in near_budget:
            remaining = budget - spent
            days_left = _days_left_in_month(month)
            daily_ok = remaining / max(days_left, 1)
            print(f"     {cat:<16} 剩 {fmt(remaining):>10}（日均可用 {fmt(daily_ok)}/天）")

    if not over_budget and near_budget:
        print(f"\n  💡 本月尚未超支，但注意控制以上分类支出。")
    print()


def generate_template(ledger_path: str, income: float, ratio=None):
    """生成预算模板。
    
    警告：此操作会覆盖已有的分类预算定义。如需保留现有预算，请先查看 --list。
    """
    data = {"meta": {"created": None, "updated": None}, "categories": {}}

    existing = load_budgets(ledger_path)
    if existing.get("categories"):
        cat_count = len(existing["categories"])
        print(f"⚠️  当前已有 {cat_count} 个分类预算设定，执行 --template 会覆盖这些设定。")
        ans = input("   确认覆盖？输入「覆盖」确认：").strip()
        if ans != "覆盖":
            print("❌ 已取消模板生成")
            return

    if ratio and len(ratio) != 4:
        print("❌ --ratio 需要提供 4 个比例值，如 40 30 20 10")
        sys.exit(1)

    # 计算各分类预算金额
    if ratio:
        needs_pct, wants_pct, flex_pct, other_pct = [r / 100.0 for r in ratio]
        spend_budget = income * (1 - flex_pct - other_pct)  # flex/other 留出部分
        savings = income * flex_pct
        other_total = income * other_pct
        # 按比例分配 needs 和 wants
        needs_share = needs_pct / (needs_pct + wants_pct) if (needs_pct + wants_pct) > 0 else 0.5
        wants_share = 1 - needs_share
        template = {
            "餐饮": needs_share * 0.40,
            "交通": needs_share * 0.15,
            "居住": needs_share * 0.30,
            "通讯": needs_share * 0.08,
            "医疗": needs_share * 0.07,
            "购物": wants_share * 0.30,
            "娱乐": wants_share * 0.25,
            "教育": wants_share * 0.25,
            "社交": wants_share * 0.20,
            "其他": 0.01,
        }
    else:
        template = TEMPLATE_503020
        spend_budget = income * 0.8  # 50/30/20 中 80% 用于支出
        savings = income * 0.2
        other_total = 0

    print(f"\n📐 预算模板生成（月收入 ¥{income:,.2f}）")
    print(f"{'='*55}\n")

    # 大类汇总
    needs_cats = ["餐饮", "交通", "居住", "通讯", "医疗"]
    wants_cats = ["购物", "娱乐", "教育", "社交"]

    print(f"  建议月度分配：")
    needs_total = sum(template.get(c, 0) for c in needs_cats) * spend_budget
    wants_total = sum(template.get(c, 0) for c in wants_cats) * spend_budget
    print(f"  ┌─ 必要支出（需求）  ¥{needs_total:>12,.2f}  ({needs_total/income*100:.0f}%)")
    print(f"  ├─ 弹性支出（想要）  ¥{wants_total:>12,.2f}  ({wants_total/income*100:.0f}%)")
    print(f"  └─ 储蓄/投资         ¥{savings:>12,.2f}  ({savings/income*100:.0f}%)")
    if other_total > 0:
        print(f"     其他预留          ¥{other_total:>12,.2f}  ({other_total/income*100:.0f}%)")
    print(f"\n  {'─'*50}")
    print(f"  {'分类':<16} {'预算':>12} {'占比':>8}")
    print(f"  {'─'*40}")

    for cat in DEFAULT_CATEGORIES:
        pct = template.get(cat, 0.01)
        amt = pct * spend_budget
        data["categories"][cat] = round(amt, 2)
        pct_disp = pct * 100
        print(f"  {cat:<16} {fmt(amt):>12} {pct_disp:>7.1f}%")

    print(f"  {'─'*40}")
    total = sum(data["categories"].values())
    print(f"  {'合计':<16} {fmt(total):>12}")

    save_budgets(ledger_path, data)
    print(f"\n  💾 预算已保存到 {_budget_path(ledger_path).name}")
    print(f"  ✅ 可用 --progress 查看执行进度\n")


# ==================== 工具函数 ====================

def fmt(amount: float) -> str:
    """格式化金额。"""
    return f"¥{amount:,.2f}"


def _make_bar(pct: float, width: int = 18) -> str:
    """生成进度条。"""
    filled = min(int(pct / 100 * width), width)
    if pct > 100:
        filled = width
    bar = "█" * filled + "░" * (width - filled)
    return bar


def _status_label(pct: float) -> str:
    """根据百分比返回状态标签。"""
    if pct >= 100:
        return "❌ 已超支"
    elif pct >= 90:
        return "⚠️ 快超了"
    elif pct >= 75:
        return "🔸 注意"
    else:
        return "✅"


def _month_display(month: str) -> str:
    """YYYY-MM → YYYY年M月"""
    try:
        parts = month.split("-")
        return f"{parts[0]}年{int(parts[1])}月"
    except Exception:
        return month


def _days_left_in_month(month: str) -> int:
    """计算当月剩余天数。"""
    try:
        year, mon = int(month.split("-")[0]), int(month.split("-")[1])
        today = datetime.now()
        if today.year == year and today.month == mon:
            from calendar import monthrange
            _, last_day = monthrange(year, mon)
            return max(last_day - today.day, 1)
        else:
            from calendar import monthrange
            _, last_day = monthrange(year, mon)
            return last_day
    except Exception:
        return 30


# ==================== CLI ====================

def main():
    parser = argparse.ArgumentParser(
        description="预算管理工具（CSV格式账本）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python budget.py ./my.csv --set 餐饮 2000
  python budget.py ./my.csv --set 交通 800
  python budget.py ./my.csv --progress 2026-05
  python budget.py ./my.csv --alert 2026-05
  python budget.py ./my.csv --template 15000
  python budget.py ./my.csv --template 15000 --ratio 40 30 20 10
  python budget.py ./my.csv --list
  python budget.py ./my.csv --remove 餐饮
        """,
    )

    parser.add_argument("ledger", help="账本CSV文件路径")
    parser.add_argument("--set", nargs=2, metavar=("分类", "金额"), help="设定月度分类预算")
    parser.add_argument("--remove", metavar="分类", help="移除分类预算")
    parser.add_argument("--progress", metavar="YYYY-MM", help="查询预算执行进度")
    parser.add_argument("--alert", metavar="YYYY-MM", help="超支预警")
    parser.add_argument("--template", metavar="月收入", type=float, help="生成预算模板")
    parser.add_argument("--ratio", nargs=4, metavar=("需求", "想要", "弹性", "其他"),
                        type=float, help="自定义分配比例（配合 --template）")
    parser.add_argument("--list", action="store_true", help="列出所有预算")

    args = parser.parse_args()

    if args.set:
        cat, amt = args.set
        try:
            amount = float(amt)
        except ValueError:
            print(f"❌ 金额无效: {amt}")
            sys.exit(1)
        set_budget(args.ledger, cat, amount)

    elif args.remove:
        remove_budget(args.ledger, args.remove)

    elif args.progress:
        print_progress(args.ledger, args.progress)

    elif args.alert:
        print_alert(args.ledger, args.alert)

    elif args.template:
        generate_template(args.ledger, args.template, args.ratio)

    elif args.list:
        list_budgets(args.ledger)

    else:
        this_month = datetime.now().strftime("%Y-%m")
        print_progress(args.ledger, this_month)


if __name__ == "__main__":
    main()