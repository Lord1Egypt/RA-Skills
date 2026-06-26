#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大米系统检查脚本 v2.0 - 库存提醒 + 对账提醒
"""

import json
from datetime import date, datetime, timedelta
from pathlib import Path

DATA_FILE = Path.home() / ".openclaw" / "workspace" / "rice-shop-records.json"


def load_records():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def get_stock_info(record):
    if not record.get("purchases"):
        return {"total": 0, "days_left": -1, "expected_date": "无记录"}
    
    total_quantity = sum(p.get("quantity", 0) for p in record["purchases"])
    if total_quantity <= 0:
        return {"total": 0, "days_left": -1, "expected_date": "已吃完"}
    
    dates = [datetime.strptime(p["date"], "%Y-%m-%d").date() for p in record["purchases"]]
    earliest = min(dates)
    
    today = date.today()
    people = record.get("people", 1)
    daily_rate = record.get("daily_rate", 0.4)
    frequency = record.get("frequency", "daily")
    
    days_passed = max(0, (today - earliest).days)
    
    if frequency == "workdays":
        workdays = sum(1 for i in range(days_passed + 1) if (earliest + timedelta(i)).weekday() < 5)
        consumed = workdays * people * daily_rate
    elif frequency == "weekends":
        weekends = sum(1 for i in range(days_passed + 1) if (earliest + timedelta(i)).weekday() >= 5)
        consumed = weekends * people * daily_rate
    else:
        consumed = days_passed * people * daily_rate
    
    remaining = total_quantity - consumed
    if remaining <= 0:
        return {"total": total_quantity, "days_left": -1, "expected_date": "已吃完"}
    
    if frequency == "workdays":
        dpj = 7 / (people * daily_rate * 5) if people * daily_rate > 0 else 999
    elif frequency == "weekends":
        dpj = 7 / (people * daily_rate * 2) if people * daily_rate > 0 else 999
    else:
        dpj = 1 / (people * daily_rate) if people * daily_rate > 0 else 999
    
    days_left = int(remaining * dpj)
    expected_date = (today + timedelta(days=days_left)).strftime("%Y-%m-%d")
    
    return {"total": total_quantity, "days_left": days_left, "expected_date": expected_date}


def main():
    records = load_records()
    today = date.today()
    
    alerts = []
    settle_alerts = []
    
    for r in records:
        stock_info = get_stock_info(r)
        
        # 库存提醒
        if stock_info["days_left"] < 0:
            alerts.append(f"🚨 【{r['owner']}】的大米已耗尽！请立即采购！")
        elif stock_info["days_left"] <= 3:
            alerts.append(f"⚠️ 【{r['owner']}】的大米预计 {stock_info['days_left']} 天后（{stock_info['expected_date']}）吃完，建议提醒采购！")
        
        # 对账提醒
        for p in r.get("purchases", []):
            if not p.get("paid", True) and p.get("settle_date"):
                try:
                    settle_d = datetime.strptime(p["settle_date"], "%Y-%m-%d").date()
                    if settle_d <= today:
                        acct = "对公转账" if p.get("account_type") == "corporate" else "对私"
                        amount = p.get("total_amount", 0)
                        overdue = (today - settle_d).days
                        settle_alerts.append(f"💰 【{r['owner']}】{p['settle_date']}到期未付款（欠款{amount}元，{acct}），已逾期{overdue}天，请提醒收款！")
                except:
                    pass
    
    # 输出
    if alerts or settle_alerts:
        print(f"🍚 **大米采购管理系统提醒**（{today.strftime('%Y-%m-%d')}）")
        print()
        
        if alerts:
            print("**📦 库存提醒**")
            for a in alerts:
                print(a)
            print()
        
        if settle_alerts:
            print("**💰 对账提醒**")
            for a in settle_alerts:
                print(a)
    else:
        print(f"🍚 检查完成（{today.strftime('%Y-%m-%d')}）：所有客户库存充足，无到期未付款项 ✅")


if __name__ == "__main__":
    main()
