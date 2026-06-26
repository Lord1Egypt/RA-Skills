#!/usr/bin/env python3
"""
股票调仓监控脚本
监控多个条件，当条件满足时提醒调仓
用法：python3 stocks_rebalance_monitor.py [config_file]
"""

import json
import os
import sys
from datetime import datetime, timedelta
import urllib.request

def get_config_path():
    if len(sys.argv) > 1:
        return sys.argv[1]
    return os.path.expanduser("~/.openclaw/workspace/memory/stocks_rebalance_config.json")

def get_state_path():
    return os.path.expanduser("~/.openclaw/workspace/memory/stocks_rebalance_alert.json")

def load_config():
    config_path = get_config_path()
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    print(f"配置文件不存在：{config_path}")
    sys.exit(1)

def load_state():
    state_path = get_state_path()
    if os.path.exists(state_path):
        with open(state_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_state(state):
    state_path = get_state_path()
    os.makedirs(os.path.dirname(state_path), exist_ok=True)
    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def get_price(symbol):
    """获取实时股价"""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=5m&range=1d"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())
        if "chart" in data and "result" in data["chart"] and data["chart"]["result"]:
            result = data["chart"]["result"][0]
            meta = result.get("meta", {})
            price = meta.get("regularMarketPrice")
            if price:
                return float(price)
        return None
    except Exception as e:
        print(f"获取 {symbol} 股价失败：{e}")
        return None

def check_condition(stock_name, condition, stocks_config):
    """检查单个条件"""
    symbol = stocks_config[stock_name]["symbol"]
    currency = stocks_config[stock_name]["currency"]
    target = condition["target"]
    cond_type = condition["type"]
    
    price = get_price(symbol)
    if not price:
        return None, None
    
    triggered = False
    message = None
    
    if cond_type == "price_above" and price >= target:
        triggered = True
        message = f"🚀 {stock_name} 涨到 {currency}{price:.2f}（目标：{currency}{target}）"
    elif cond_type == "price_below" and price <= target:
        triggered = True
        message = f"📉 {stock_name} 跌到 {currency}{price:.2f}（目标：{currency}{target}）"
    
    if triggered:
        if "message" in condition:
            message = f"{message} - {condition['message']}"
    
    return triggered, message

def check_rule(rule, stocks_config):
    """检查调仓规则"""
    if not rule.get("enabled", True):
        return None
    
    now = datetime.now()
    state = load_state()
    rule_name = rule["name"]
    
    # 初始化规则状态
    if rule_name not in state:
        state[rule_name] = {
            "active": False,
            "last_triggered": None,
            "repeat_count": 0,
            "triggered_conditions": []
        }
    
    rule_state = state[rule_name]
    
    # 检查 cooldown（冷却期只在完成所有重复提醒后才开始）
    if rule_state.get("last_triggered") and not rule_state.get("active", False):
        cooldown_hours = rule.get("cooldown_hours", 24)
        last_time = datetime.fromisoformat(rule_state["last_triggered"])
        if now - last_time < timedelta(hours=cooldown_hours):
            return None  # 还在冷却期内
    
    conditions = rule.get("conditions", [])
    notify_when = rule.get("notify_when", "all")
    repeat_times = rule.get("repeat_times", 1)
    repeat_interval = rule.get("repeat_interval_minutes", 5)
    
    triggered_conditions = []
    all_messages = []
    
    for cond in conditions:
        stock_name = cond["stock"]
        if stock_name not in stocks_config:
            print(f"警告：股票 {stock_name} 未在配置中找到")
            continue
        
        triggered, message = check_condition(stock_name, cond, stocks_config)
        if triggered:
            triggered_conditions.append(cond)
            if message:
                all_messages.append(message)
    
    # 判断是否所有条件都满足
    all_conditions_met = False
    if notify_when == "any" and len(triggered_conditions) > 0:
        all_conditions_met = True
    elif notify_when == "all" and len(triggered_conditions) == len(conditions):
        all_conditions_met = True
    
    # 如果条件满足，开始或继续重复提醒
    if all_conditions_met:
        # 如果是第一次触发或重新开始
        if not rule_state.get("active", False):
            rule_state["active"] = True
            rule_state["repeat_count"] = 0
            rule_state["start_time"] = now.isoformat()
        
        # 检查是否已达到重复次数
        if rule_state["repeat_count"] >= repeat_times:
            # 已完成所有重复，重置状态并进入冷却期
            rule_state["active"] = False
            rule_state["last_triggered"] = now.isoformat()
            rule_state["repeat_count"] = 0
            save_state(state)
            return None
        
        # 如果是第一次触发，或者距离上次提醒已经过了指定间隔
        should_notify = False
        if rule_state["repeat_count"] == 0:
            should_notify = True
        else:
            last_repeat = rule_state.get("last_repeat_time")
            if last_repeat:
                last_repeat_time = datetime.fromisoformat(last_repeat)
                if now - last_repeat_time >= timedelta(minutes=repeat_interval):
                    should_notify = True
        
        if should_notify:
            rule_state["repeat_count"] += 1
            rule_state["last_repeat_time"] = now.isoformat()
            
            # 生成通知消息
            rule_message = f"📊 **调仓提醒：{rule_name}** (第 {rule_state['repeat_count']}/{repeat_times} 次)\n\n"
            rule_message += "\n".join(all_messages)
            rule_message += f"\n\n触发时间：{now.strftime('%Y-%m-%d %H:%M')}"
            
            save_state(state)
            return rule_message
        else:
            return None
    else:
        # 条件不满足，重置状态
        rule_state["active"] = False
        rule_state["repeat_count"] = 0
        save_state(state)
        return None

def main():
    config = load_config()
    stocks = config.get("stocks", {})
    rules = config.get("rebalance_rules", [])
    
    if not rules:
        print("请先配置调仓规则")
        return
    
    results = []
    for rule in rules:
        result = check_rule(rule, stocks)
        if result:
            results.append(result)
    
    if not results:
        return
    
    for r in results:
        print(r)

if __name__ == "__main__":
    main()
