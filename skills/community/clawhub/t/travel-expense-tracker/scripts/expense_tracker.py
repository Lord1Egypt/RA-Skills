#!/usr/bin/env python3
"""旅行记账助手 - Travel Expense Tracker"""

import json
import os
import sys
from datetime import datetime

# ====== 参考汇率(2026年6月，仅供参考) ======
EXCHANGE_RATES = {
    "CNY": 1.0,
    "USD": 7.25,
    "EUR": 7.85,
    "GBP": 9.20,
    "JPY": 0.048,
    "KRW": 0.0053,
    "THB": 0.20,
    "SGD": 5.40,
    "AUD": 4.70,
    "NZD": 4.35,
    "HKD": 0.93,
    "TWD": 0.24,
    "MYR": 1.55,
    "VND": 0.00028,
    "IDR": 0.00044,
    "PHP": 0.125,
    "AED": 1.97,
    "CHF": 8.25,
    "TRY": 0.22,
    "RUB": 0.082,
    "INR": 0.086,
    "CAD": 5.30,
    "BRL": 1.35,
    "MXN": 0.37,
    "ZAR": 0.39,
    "EGP": 0.14,
    "SAR": 1.93,
    "MOP": 0.90,
}

# ====== 消费分类 ======
CATEGORIES = {
    "餐饮": ["餐饮", "吃饭", "美食", "小吃", "早餐", "午餐", "晚餐", "咖啡", "饮料", "food", "meal"],
    "交通": ["交通", "打车", "地铁", "公交", "出租车", "机票", "火车", "船票", "租车", "加油", "transport", "taxi"],
    "住宿": ["住宿", "酒店", "民宿", "青旅", "hostel", "hotel"],
    "购物": ["购物", "买", "纪念品", "药妆", "免税", "shopping"],
    "门票": ["门票", "景点", "景区", "博物馆", "主题公园", "ticket", "entrance"],
    "通讯": ["通讯", "SIM卡", "eSIM", "电话", "流量", "WiFi"],
    "签证": ["签证", "签证费", "visa"],
    "保险": ["保险", "旅行险", "insurance"],
    "其他": ["其他", "other", "misc"],
}

# 数据存储目录
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "travel_expenses")


def to_cny(amount, currency):
    """将金额换算为人民币"""
    rate = EXCHANGE_RATES.get(currency.upper(), None)
    if rate is None:
        return None, f"不支持的货币：{currency}，支持：{', '.join(sorted(EXCHANGE_RATES.keys()))}"
    return round(amount * rate, 2), None


def classify_category(input_cat):
    """智能分类匹配"""
    input_lower = input_cat.strip().lower()
    for cat, keywords in CATEGORIES.items():
        for kw in keywords:
            if kw in input_lower or input_lower in kw:
                return cat
    return "其他"


def load_trips():
    """加载所有旅行数据"""
    os.makedirs(DATA_DIR, exist_ok=True)
    index_file = os.path.join(DATA_DIR, "index.json")
    if os.path.exists(index_file):
        with open(index_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_trips(trips):
    """保存所有旅行数据"""
    os.makedirs(DATA_DIR, exist_ok=True)
    index_file = os.path.join(DATA_DIR, "index.json")
    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(trips, f, ensure_ascii=False, indent=2)


def load_expenses(trip_name):
    """加载指定旅行的消费记录"""
    safe_name = trip_name.replace("/", "_").replace(" ", "_")
    expense_file = os.path.join(DATA_DIR, f"{safe_name}.json")
    if os.path.exists(expense_file):
        with open(expense_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"trip": trip_name, "expenses": [], "budget": {}}


def save_expenses(trip_name, data):
    """保存指定旅行的消费记录"""
    os.makedirs(DATA_DIR, exist_ok=True)
    safe_name = trip_name.replace("/", "_").replace(" ", "_")
    expense_file = os.path.join(DATA_DIR, f"{safe_name}.json")
    with open(expense_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def cmd_add_expense(params):
    """记录一笔消费"""
    trip = params.get("trip", "")
    amount = params.get("amount", 0)
    currency = params.get("currency", "CNY")
    category = params.get("category", "其他")
    description = params.get("description", "")
    date = params.get("date", datetime.now().strftime("%Y-%m-%d"))

    if not trip:
        return {"error": "请提供旅行名称"}
    
    try:
        amount = float(amount)
        if amount <= 0:
            return {"error": "金额必须大于0"}
    except (ValueError, TypeError):
        return {"error": "请输入有效金额"}

    # 汇率换算
    amount_cny, err = to_cny(amount, currency)
    if err:
        return {"error": err}

    # 智能分类
    matched_cat = classify_category(category)

    # 加载并保存
    data = load_expenses(trip)
    expense = {
        "id": len(data["expenses"]) + 1,
        "date": date,
        "amount": amount,
        "currency": currency.upper(),
        "amount_cny": amount_cny,
        "category": matched_cat,
        "description": description,
    }
    data["expenses"].append(expense)
    save_expenses(trip, data)

    return {
        "status": "已记录",
        "trip": trip,
        "expense": expense,
        "total_expenses": len(data["expenses"]),
        "total_cny": round(sum(e["amount_cny"] for e in data["expenses"]), 2),
    }


def cmd_expense_summary(params):
    """查看消费汇总"""
    trip = params.get("trip", "")
    group_by = params.get("group_by", "category")

    if not trip:
        return {"error": "请提供旅行名称"}

    data = load_expenses(trip)
    expenses = data.get("expenses", [])

    if not expenses:
        return {"trip": trip, "message": "暂无消费记录", "total_cny": 0}

    total_cny = round(sum(e["amount_cny"] for e in expenses), 2)

    result = {
        "trip": trip,
        "total_expenses": len(expenses),
        "total_cny": total_cny,
        "currencies_used": list(set(e["currency"] for e in expenses)),
    }

    # 按分类汇总
    if group_by == "category" or group_by == "all":
        by_category = {}
        for e in expenses:
            cat = e["category"]
            if cat not in by_category:
                by_category[cat] = {"count": 0, "total_cny": 0}
            by_category[cat]["count"] += 1
            by_category[cat]["total_cny"] = round(by_category[cat]["total_cny"] + e["amount_cny"], 2)
        
        # 按金额排序
        sorted_cats = sorted(by_category.items(), key=lambda x: x[1]["total_cny"], reverse=True)
        result["by_category"] = [{cat: info} for cat, info in sorted_cats]

    # 按日期汇总
    if group_by == "date" or group_by == "all":
        by_date = {}
        for e in expenses:
            d = e["date"]
            if d not in by_date:
                by_date[d] = {"count": 0, "total_cny": 0}
            by_date[d]["count"] += 1
            by_date[d]["total_cny"] = round(by_date[d]["total_cny"] + e["amount_cny"], 2)
        
        sorted_dates = sorted(by_date.items(), key=lambda x: x[0])
        result["by_date"] = [{d: info} for d, info in sorted_dates]

    # 按币种汇总
    if group_by == "currency" or group_by == "all":
        by_currency = {}
        for e in expenses:
            cur = e["currency"]
            if cur not in by_currency:
                by_currency[cur] = {"count": 0, "total_original": 0, "total_cny": 0}
            by_currency[cur]["count"] += 1
            by_currency[cur]["total_original"] = round(by_currency[cur]["total_original"] + e["amount"], 2)
            by_currency[cur]["total_cny"] = round(by_currency[cur]["total_cny"] + e["amount_cny"], 2)
        
        result["by_currency"] = by_currency

    # 最近5笔消费
    result["recent"] = data["expenses"][-5:]

    return result


def cmd_budget_check(params):
    """预算管理与超支检查"""
    trip = params.get("trip", "")
    total_budget = params.get("total_budget", 0)
    daily_budget = params.get("daily_budget", 0)
    days = params.get("days", 0)

    if not trip:
        return {"error": "请提供旅行名称"}

    data = load_expenses(trip)
    expenses = data.get("expenses", [])

    # 更新预算
    if total_budget:
        try:
            data.setdefault("budget", {})["total_budget"] = float(total_budget)
        except (ValueError, TypeError):
            pass
    if daily_budget:
        try:
            data.setdefault("budget", {})["daily_budget"] = float(daily_budget)
        except (ValueError, TypeError):
            pass
    if days:
        try:
            data.setdefault("budget", {})["days"] = int(days)
        except (ValueError, TypeError):
            pass
    
    save_expenses(trip, data)
    
    budget = data.get("budget", {})
    total_spent = round(sum(e["amount_cny"] for e in expenses), 2)
    
    result = {
        "trip": trip,
        "total_spent_cny": total_spent,
        "total_expenses": len(expenses),
    }

    # 总预算检查
    tb = budget.get("total_budget", 0)
    if tb:
        result["total_budget"] = tb
        result["budget_remaining"] = round(tb - total_spent, 2)
        result["budget_used_pct"] = round(total_spent / tb * 100, 1)
        if total_spent > tb:
            result["⚠️ 超支"] = f"已超出预算¥{round(total_spent - tb, 2)}"
        elif total_spent > tb * 0.8:
            result["⚠️ 接近预算"] = f"已使用{round(total_spent/tb*100, 1)}%预算"

    # 日均预算检查
    db = budget.get("daily_budget", 0)
    trip_days = budget.get("days", 0)
    if db and trip_days:
        result["daily_budget"] = db
        result["trip_days"] = trip_days
        
        # 按日期汇总消费
        by_date = {}
        for e in expenses:
            d = e["date"]
            by_date[d] = by_date.get(d, 0) + e["amount_cny"]
        
        daily_breakdown = []
        over_budget_days = []
        for d, spent in sorted(by_date.items()):
            daily_breakdown.append({"date": d, "spent": round(spent, 2), "budget": db})
            if spent > db:
                over_budget_days.append({"date": d, "spent": round(spent, 2), "over": round(spent - db, 2)})
        
        result["daily_breakdown"] = daily_breakdown
        if over_budget_days:
            result["over_budget_days"] = over_budget_days
        
        # 剩余日均可用
        days_with_expenses = len(by_date)
        remaining_days = max(trip_days - days_with_expenses, 0)
        if remaining_days > 0:
            remaining_budget = max(tb - total_spent, 0) if tb else db * remaining_days
            result["remaining_daily_budget"] = round(remaining_budget / remaining_days, 2)
            result["remaining_days"] = remaining_days

    # 如果没有设置预算，给出建议
    if not tb and not db:
        result["budget_tip"] = "尚未设置预算，建议设置 total_budget 和 days 参数来管理预算"

    return result


# ====== 主入口 ======
TOOLS = {
    "add_expense": cmd_add_expense,
    "expense_summary": cmd_expense_summary,
    "budget_check": cmd_budget_check,
}


def main():
    if len(sys.argv) < 3:
        print(json.dumps({"error": "用法: python3 expense_tracker.py <tool> '<json_params>'", "tools": list(TOOLS.keys())}, ensure_ascii=False))
        return

    tool = sys.argv[1]
    try:
        params = json.loads(sys.argv[2])
    except json.JSONDecodeError:
        print(json.dumps({"error": "参数JSON解析失败"}, ensure_ascii=False))
        return

    handler = TOOLS.get(tool)
    if not handler:
        print(json.dumps({"error": f"未知工具: {tool}", "tools": list(TOOLS.keys())}, ensure_ascii=False))
        return

    result = handler(params)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
