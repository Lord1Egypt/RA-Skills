#!/usr/bin/env python3
"""
收支管理系统
支持个人日常开支和店铺经营数据管理
"""
import json
import os
import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# 数据目录
DATA_DIR = Path.home() / "private_data" / "openclaw" / "workspace" / "data" / "finance"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# 数据文件
PERSONAL_EXPENSES = DATA_DIR / "personal_expenses.json"
SHOP_PURCHASES = DATA_DIR / "shop_purchases.json"
SHOP_SALES = DATA_DIR / "shop_sales.json"
SETTINGS = DATA_DIR / "settings.json"

# 初始化数据文件
def init_files():
    for f in [PERSONAL_EXPENSES, SHOP_PURCHASES, SHOP_SALES]:
        if not f.exists():
            f.write_text("[]")
    if not SETTINGS.exists():
        SETTINGS.write_text(json.dumps({
            "monthly_budget": 5000,
            "operating_costs": 0,
            "expense_categories": [
                "餐饮", "购物", "交通", "住房", "医疗", "通讯", "娱乐", "教育", "其他"
            ]
        }, ensure_ascii=False, indent=2))

# 加载/保存JSON
def load_json(path: Path) -> list | dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except:
        return [] if "expenses" in str(path) or "purchases" in str(path) or "sales" in str(path) else {}

def save_json(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

# 日期处理
def parse_date(date_str: str) -> str:
    """解析日期字符串"""
    today = datetime.now()
    if date_str in ["今天", "今日"]:
        return today.strftime("%Y-%m-%d")
    elif date_str in ["昨天", "昨日"]:
        return (today - timedelta(days=1)).strftime("%Y-%m-%d")
    elif date_str in ["前天"]:
        return (today - timedelta(days=2)).strftime("%Y-%m-%d")
    # 尝试解析具体日期
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
    except:
        return today.strftime("%Y-%m-%d")

def get_month_range(year: int = None, month: int = None) -> tuple:
    """获取月份范围"""
    today = datetime.now()
    year = year or today.year
    month = month or today.month
    start = datetime(year, month, 1)
    if month == 12:
        end = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        end = datetime(year, month + 1, 1) - timedelta(days=1)
    return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")

# ========== 个人开支 ==========
def add_expense(category: str, amount: float, note: str = "", date: str = "今天"):
    """添加个人开支"""
    init_files()
    expenses = load_json(PERSONAL_EXPENSES)
    
    expense = {
        "id": len(expenses) + 1,
        "date": parse_date(date),
        "category": category,
        "amount": float(amount),
        "note": note,
        "created_at": datetime.now().isoformat()
    }
    expenses.append(expense)
    save_json(PERSONAL_EXPENSES, expenses)
    
    # 检查预算
    budget_info = check_budget_silent()
    if budget_info:
        used_pct = budget_info["used_percent"]
        if used_pct >= 100:
            return f"✅ 已记录！⚠️ 已超支 {budget_info['over']} 元"
        elif used_pct >= 80:
            return f"✅ 已记录！⚠️ 注意，本月已使用 {used_pct:.0f}% 预算"
    return f"✅ 已记录：{category} {amount}元"

def check_budget(month: int = None, year: int = None) -> dict:
    """检查预算使用情况"""
    init_files()
    settings = load_json(SETTINGS)
    budget = settings.get("monthly_budget", 5000)
    
    start_date, end_date = get_month_range(year, month)
    expenses = load_json(PERSONAL_EXPENSES)
    
    month_expenses = [e for e in expenses 
                      if start_date <= e["date"] <= end_date]
    
    total = sum(e["amount"] for e in month_expenses)
    used_pct = (total / budget * 100) if budget > 0 else 0
    remaining = budget - total
    
    # 分类统计
    by_category = {}
    for e in month_expenses:
        cat = e["category"]
        by_category[cat] = by_category.get(cat, 0) + e["amount"]
    
    return {
        "budget": budget,
        "spent": total,
        "remaining": remaining,
        "used_percent": used_pct,
        "over": total - budget if total > budget else 0,
        "by_category": by_category,
        "month": month or datetime.now().month,
        "year": year or datetime.now().year
    }

def check_budget_silent() -> Optional[dict]:
    """静默检查预算（用于提醒）"""
    return check_budget()

def get_expenses_by_period(period: str = "month", category: str = None) -> dict:
    """获取指定时期的开支"""
    init_files()
    expenses = load_json(PERSONAL_EXPENSES)
    today = datetime.now()
    
    if period == "today":
        target_date = today.strftime("%Y-%m-%d")
        filtered = [e for e in expenses if e["date"] == target_date]
    elif period == "week":
        week_ago = (today - timedelta(days=7)).strftime("%Y-%m-%d")
        filtered = [e for e in expenses if e["date"] >= week_ago]
    elif period == "month":
        start_date, end_date = get_month_range()
        filtered = [e for e in expenses if start_date <= e["date"] <= end_date]
    elif period == "year":
        year = today.year
        filtered = [e for e in expenses if e["date"].startswith(str(year))]
    else:
        filtered = expenses
    
    if category:
        filtered = [e for e in filtered if e["category"] == category]
    
    total = sum(e["amount"] for e in filtered)
    return {"expenses": filtered, "total": total, "count": len(filtered)}

def set_budget(amount: float):
    """设置月度预算"""
    init_files()
    settings = load_json(SETTINGS)
    settings["monthly_budget"] = float(amount)
    save_json(SETTINGS, settings)
    return f"✅ 已设置月度预算：{amount}元"

# ========== 店铺管理 ==========
def add_purchase(product: str, quantity: int, price: float, date: str = "今天"):
    """记录进货"""
    init_files()
    purchases = load_json(SHOP_PURCHASES)
    
    purchase = {
        "id": len(purchases) + 1,
        "date": parse_date(date),
        "product": product,
        "quantity": int(quantity),
        "unit_price": float(price),
        "total": float(price) * int(quantity),
        "created_at": datetime.now().isoformat()
    }
    purchases.append(purchase)
    save_json(SHOP_PURCHASES, purchases)
    
    return f"✅ 已记录进货：{product} x{quantity}台，单价{price}元，总计{purchase['total']}元"

def add_sale(product: str, quantity: int, price: float, date: str = "今天"):
    """记录销售"""
    init_files()
    sales = load_json(SHOP_SALES)
    
    sale = {
        "id": len(sales) + 1,
        "date": parse_date(date),
        "product": product,
        "quantity": int(quantity),
        "unit_price": float(price),
        "total": float(price) * int(quantity),
        "created_at": datetime.now().isoformat()
    }
    sales.append(sale)
    save_json(SHOP_SALES, sales)
    
    # 计算利润
    profit = calculate_profit(sale)
    return f"✅ 已记录销售：{product} x{quantity}台，单价{price}元，总计{sale['total']}元，预估利润{profit:.0f}元"

def calculate_profit(sale: dict = None) -> float:
    """计算毛利（先进先出法）"""
    purchases = load_json(SHOP_PURCHASES)
    sales = load_json(SHOP_SALES)
    
    if sale:
        # 单笔销售利润
        product = sale["product"]
        sold_qty = sale["quantity"]
        sale_price = sale["unit_price"]
        
        # 获取该产品的所有进货，按日期排序
        product_purchases = sorted(
            [p for p in purchases if p["product"] == product],
            key=lambda x: x["date"]
        )
        
        remaining = sold_qty
        cost = 0
        for p in product_purchases:
            if remaining <= 0:
                break
            # 简单计算：按最近进货价
            cost += p["unit_price"] * min(remaining, p["quantity"])
            remaining -= min(remaining, p["quantity"])
        
        return sale_price * sold_qty - cost
    return 0

def get_stock() -> dict:
    """获取库存（按商品）"""
    purchases = load_json(SHOP_PURCHASES)
    sales = load_json(SHOP_SALES)
    
    stock = {}
    for p in purchases:
        product = p["product"]
        stock[product] = stock.get(product, {"qty": 0, "cost": 0})
        stock[product]["qty"] += p["quantity"]
        stock[product]["cost"] += p["total"]
    
    for s in sales:
        product = s["product"]
        if product in stock:
            stock[product]["qty"] -= s["quantity"]
    
    # 计算平均成本
    for product in stock:
        if stock[product]["qty"] > 0:
            stock[product]["avg_cost"] = stock[product]["cost"] / stock[product]["qty"]
        else:
            stock[product]["avg_cost"] = 0
    
    return stock

def shop_report(period: str = "month") -> dict:
    """店铺报表"""
    init_files()
    purchases = load_json(SHOP_PURCHASES)
    sales = load_json(SHOP_SALES)
    settings = load_json(SETTINGS)
    
    today = datetime.now()
    
    # 筛选日期
    if period == "month":
        start_date, end_date = get_month_range()
    elif period == "year":
        start_date = f"{today.year}-01-01"
        end_date = today.strftime("%Y-%m-%d")
    else:
        start_date = "2000-01-01"
        end_date = "2099-12-31"
    
    period_sales = [s for s in sales if start_date <= s["date"] <= end_date]
    period_purchases = [p for p in purchases if start_date <= p["date"] <= end_date]
    
    # 统计
    total_sales = sum(s["total"] for s in period_sales)
    total_purchases = sum(p["total"] for p in period_purchases)
    
    # 计算毛利
    gross_profit = 0
    product_profit = {}
    for s in period_sales:
        profit = calculate_profit(s)
        gross_profit += profit
        product = s["product"]
        product_profit[product] = product_profit.get(product, 0) + profit
    
    # 运营费用
    operating_costs = settings.get("operating_costs", 0)
    net_profit = gross_profit - operating_costs
    
    # 按商品统计
    product_sales = {}
    for s in period_sales:
        product = s["product"]
        product_sales[product] = product_sales.get(product, {"qty": 0, "amount": 0})
        product_sales[product]["qty"] += s["quantity"]
        product_sales[product]["amount"] += s["total"]
    
    return {
        "period": period,
        "start_date": start_date,
        "end_date": end_date,
        "total_sales": total_sales,
        "total_purchases": total_purchases,
        "gross_profit": gross_profit,
        "operating_costs": operating_costs,
        "net_profit": net_profit,
        "profit_margin": (net_profit / total_sales * 100) if total_sales > 0 else 0,
        "product_sales": product_sales,
        "product_profit": product_profit,
        "sales_count": len(period_sales)
    }

def set_operating_costs(amount: float):
    """设置运营费用"""
    init_files()
    settings = load_json(SETTINGS)
    settings["operating_costs"] = float(amount)
    save_json(SETTINGS, settings)
    return f"✅ 已设置月度运营费用：{amount}元"

# ========== 格式化输出 ==========
def format_budget_report(info: dict) -> str:
    """格式化预算报告"""
    year = info["year"]
    month = info["month"]
    budget = info["budget"]
    spent = info["spent"]
    remaining = info["remaining"]
    used_pct = info["used_percent"]
    over = info["over"]
    by_cat = info["by_category"]
    
    warning = ""
    if used_pct >= 100:
        warning = f"⚠️ 已超支 {over:.0f} 元！"
    elif used_pct >= 80:
        warning = f"⚠️ 预算使用 {used_pct:.0f}%，注意超支风险"
    else:
        warning = f"✅ 预算使用 {used_pct:.0f}%"
    
    lines = [
        f"📊 {year}年{month:02d}月开支报告",
        "━" * 20,
        f"预算：{budget:.0f}元",
        f"已花费：{spent:.0f}元 ({used_pct:.0f}%)",
        f"剩余：{remaining:.0f}元",
        warning,
        "━" * 20,
        "分类明细："
    ]
    
    # 按金额排序
    sorted_cats = sorted(by_cat.items(), key=lambda x: x[1], reverse=True)
    for cat, amount in sorted_cats:
        pct = (amount / spent * 100) if spent > 0 else 0
        lines.append(f"  {cat}：{amount:.0f}元 ({pct:.0f}%)")
    
    return "\n".join(lines)

def format_shop_report(info: dict) -> str:
    """格式化店铺报表"""
    period = info["period"]
    total_sales = info["total_sales"]
    total_purchases = info["total_purchases"]
    gross_profit = info["gross_profit"]
    operating_costs = info["operating_costs"]
    net_profit = info["net_profit"]
    margin = info["profit_margin"]
    product_sales = info["product_sales"]
    product_profit = info["product_profit"]
    
    lines = [
        f"📈 店铺{'月度' if period == 'month' else '年度'}经营报表",
        "━" * 24,
        f"销售总额：{total_sales:,.0f}元",
        f"进货成本：{total_purchases:,.0f}元",
        f"毛利润：{gross_profit:,.0f}元",
        f"运营费用：{operating_costs:,.0f}元",
        f"净利润：{net_profit:,.0f}元 (利润率 {margin:.1f}%)",
        "━" * 24,
        "商品销售："
    ]
    
    # 按销售额排序
    sorted_products = sorted(product_sales.items(), key=lambda x: x[1]["amount"], reverse=True)
    for product, data in sorted_products[:10]:
        qty = data["qty"]
        amount = data["amount"]
        profit = product_profit.get(product, 0)
        lines.append(f"  {product}：销售{qty}台，金额{amount:.0f}元，利润{profit:.0f}元")
    
    return "\n".join(lines)

# ========== 主入口 ==========
def main():
    parser = argparse.ArgumentParser(description="收支管理系统")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # add-expense
    p_expense = subparsers.add_parser("add-expense", help="添加开支")
    p_expense.add_argument("--category", required=True)
    p_expense.add_argument("--amount", required=True, type=float)
    p_expense.add_argument("--note", default="")
    p_expense.add_argument("--date", default="今天")
    
    # set-budget
    p_budget = subparsers.add_parser("set-budget", help="设置预算")
    p_budget.add_argument("--amount", required=True, type=float)
    
    # check-budget
    subparsers.add_parser("check-budget", help="查看预算")
    
    # expenses
    p_exp = subparsers.add_parser("expenses", help="开支记录")
    p_exp.add_argument("--period", default="month")
    p_exp.add_argument("--category", default=None)
    
    # add-purchase
    p_pur = subparsers.add_parser("add-purchase", help="添加进货")
    p_pur.add_argument("--product", required=True)
    p_pur.add_argument("--qty", required=True, type=int)
    p_pur.add_argument("--price", required=True, type=float)
    p_pur.add_argument("--date", default="今天")
    
    # add-sale
    p_sale = subparsers.add_parser("add-sale", help="添加销售")
    p_sale.add_argument("--product", required=True)
    p_sale.add_argument("--qty", required=True, type=int)
    p_sale.add_argument("--price", required=True, type=float)
    p_sale.add_argument("--date", default="今天")
    
    # stock
    subparsers.add_parser("stock", help="库存查询")
    
    # shop-report
    p_report = subparsers.add_parser("shop-report", help="店铺报表")
    p_report.add_argument("--period", default="month")
    
    # set-costs
    p_costs = subparsers.add_parser("set-costs", help="设置运营费用")
    p_costs.add_argument("--amount", required=True, type=float)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == "add-expense":
        print(add_expense(args.category, args.amount, args.note, args.date))
    elif args.command == "set-budget":
        print(set_budget(args.amount))
    elif args.command == "check-budget":
        print(format_budget_report(check_budget()))
    elif args.command == "expenses":
        result = get_expenses_by_period(args.period, args.category)
        print(f"共 {result['count']} 笔，总计 {result['total']:.0f} 元")
    elif args.command == "add-purchase":
        print(add_purchase(args.product, args.qty, args.price, args.date))
    elif args.command == "add-sale":
        print(add_sale(args.product, args.qty, args.price, args.date))
    elif args.command == "stock":
        stock = get_stock()
        print("📦 当前库存：")
        for product, data in stock.items():
            print(f"  {product}：{data['qty']}台，成本{data.get('avg_cost', 0):.0f}元/台")
    elif args.command == "shop-report":
        print(format_shop_report(shop_report(args.period)))
    elif args.command == "set-costs":
        print(set_operating_costs(args.amount))

if __name__ == "__main__":
    main()