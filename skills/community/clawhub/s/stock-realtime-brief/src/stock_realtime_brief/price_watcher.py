#!/usr/bin/env python3
"""
A 股盯盘 Agent · v1.0

功能：
1. A 股开市期间（9:30-11:30, 13:00-15:00）每 60 秒检查一次
2. 当价格触发条件时，向用户 QQ 发提醒
3. 同一条件每天最多触发 1 次（防垃圾消息）
4. 触发后 cooldown 60 分钟

数据源：腾讯股票实时 API
通知：openclaw qqbot send
"""
import json
import urllib.request
import subprocess
import time
from pathlib import Path
from datetime import datetime, time as dtime

ROOT = Path(__file__).resolve().parent.parent
WATCHLIST_PATH = ROOT / "configs" / "watchlist.json"
STATE_PATH = ROOT / "data" / "watcher_state.json"
LOG_PATH = ROOT / "data" / "logs" / f"watcher_{datetime.now():%Y%m%d}.log"

# A 股交易时段（北京时间）
TRADING_HOURS = [
    (dtime(9, 25), dtime(11, 30)),   # 上午（含集合竞价）
    (dtime(13, 0), dtime(15, 0)),    # 下午
]

# QQ 通知目标（来自配置）
USER_CHAT_ID = "9F067036FA0E02061F67D46AB31B4D2C"
QQ_CHANNEL = "qqbot"

LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

def log(msg: str):
    """日志（北京时间）"""
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def is_trading_time() -> bool:
    """是否 A 股交易时间（北京时间）"""
    now = datetime.now()
    if now.weekday() >= 5:  # 周末
        return False
    tnow = now.time()
    for start, end in TRADING_HOURS:
        if start <= tnow <= end:
            return True
    return False

def fetch_price(code: str) -> dict | None:
    """腾讯实时 API 拉价格"""
    sym = ('sz' if code.startswith(('0', '3')) else 'sh') + code
    url = f"https://qt.gtimg.cn/q={sym}"
    try:
        req = urllib.request.Request(url, headers={'Referer': 'https://gu.qq.com/'})
        with urllib.request.urlopen(req, timeout=8) as r:
            text = r.read().decode('gbk', errors='ignore')
        parts = text.split('~')
        if len(parts) < 50:
            return None
        return {
            'name': parts[1],
            'price': float(parts[3]),
            'prev': float(parts[4]),
            'open': float(parts[5]),
            'high': float(parts[33]),
            'low': float(parts[34]),
            'change_pct': float(parts[32]) if parts[32] else 0,
            'turnover_rate': float(parts[38]) if parts[38] else 0,
            'vol_ratio': float(parts[49]) if len(parts) > 49 and parts[49] else 0,
        }
    except Exception as e:
        log(f"⚠️ 拉价格失败 {code}: {e}")
        return None

def check_condition(price: float, op: str, trigger: float) -> bool:
    """检查价格条件"""
    if op == '<=':
        return price <= trigger
    elif op == '<':
        return price < trigger
    elif op == '>=':
        return price >= trigger
    elif op == '>':
        return price > trigger
    elif op == '==':
        return abs(price - trigger) < 0.01
    return False

def load_state() -> dict:
    """加载状态（防止重复触发）"""
    if STATE_PATH.exists():
        with open(STATE_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_state(state: dict):
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def send_qq_message(message: str) -> bool:
    """通过 openclaw CLI 发送 QQ 消息"""
    try:
        cmd = [
            "openclaw", "message", "send",
            "--channel", "qqbot",
            "--target", USER_CHAT_ID,
            "--message", message,
        ]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if r.returncode == 0:
            log(f"✅ 已发送 QQ 消息")
            return True
        else:
            log(f"❌ 发送失败 (rc={r.returncode}): {r.stderr[:300]}")
            return False
    except Exception as e:
        log(f"❌ 发送异常: {e}")
        return False


def build_alert_message(rule: dict, quote: dict) -> str:
    """构造提醒消息"""
    msg_lines = [
        f"🚨 价格触发提醒 · {datetime.now():%H:%M:%S}",
        "",
        f"📊 {rule['stock_name']} ({rule['code']})",
        f"  现价: ¥{quote['price']:.2f}  涨跌 {quote['change_pct']:+.2f}%",
        f"  今日: 开 ¥{quote['open']} 高 ¥{quote['high']} 低 ¥{quote['low']}",
        f"  换手 {quote['turnover_rate']}%  量比 {quote['vol_ratio']}",
        "",
        f"⚡ 触发条件: {rule['name']}",
        f"  价格 {rule['operator']} ¥{rule['trigger_price']} ✅",
        "",
        f"💡 操作建议:",
        f"  {rule['action_hint']}",
        "",
        f"📋 决策理由:",
        f"  {rule['logic']}",
        "",
        "⚠️ 提醒：触发只是必要条件，不是充分条件",
        "  请结合 量价 + 板块 + 大盘 + 时效 综合判断后再行动",
    ]
    return "\n".join(msg_lines)

def check_rules():
    """检查所有规则"""
    if not WATCHLIST_PATH.exists():
        log("❌ watchlist.json 不存在")
        return
    
    with open(WATCHLIST_PATH, encoding="utf-8") as f:
        watchlist = json.load(f)
    
    state = load_state()
    today = datetime.now().strftime("%Y-%m-%d")
    
    for rule in watchlist["rules"]:
        if not rule.get("enabled", True):
            continue
        
        rule_id = rule["id"]
        code = rule["code"]
        
        # 检查今日是否已触发达上限
        today_state = state.get(today, {}).get(rule_id, {})
        trigger_count = today_state.get("trigger_count", 0)
        last_trigger = today_state.get("last_trigger_time")
        
        if trigger_count >= rule.get("max_triggers_per_day", 1):
            continue
        
        # 冷却时间检查
        if last_trigger:
            last_dt = datetime.fromisoformat(last_trigger)
            cooldown = rule.get("cooldown_minutes", 60)
            if (datetime.now() - last_dt).total_seconds() < cooldown * 60:
                continue
        
        # 拉价格
        quote = fetch_price(code)
        if not quote:
            continue
        
        # 检查条件
        price = quote["price"]
        if check_condition(price, rule["operator"], rule["trigger_price"]):
            log(f"🚨 触发: {rule['name']} | 现价 ¥{price} {rule['operator']} ¥{rule['trigger_price']}")
            
            # 发消息
            msg = build_alert_message(rule, quote)
            if send_qq_message(msg):
                # 更新状态
                if today not in state:
                    state[today] = {}
                state[today][rule_id] = {
                    "trigger_count": trigger_count + 1,
                    "last_trigger_time": datetime.now().isoformat(),
                    "trigger_price": price,
                }
                save_state(state)
        else:
            # 静默记录（每 5 分钟才打一次价格 log）
            now_minute = datetime.now().minute
            if now_minute % 5 == 0:
                log(f"  {rule['stock_name']} {code}: ¥{price} (目标 {rule['operator']} ¥{rule['trigger_price']}) - 未触发")

def main_loop():
    """主循环"""
    log("🚀 A 股盯盘 Agent 启动")
    log(f"📋 用户: {USER_CHAT_ID}")
    log(f"⏰ 当前: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    with open(WATCHLIST_PATH, encoding="utf-8") as f:
        wl = json.load(f)
    log(f"📊 监控规则 {len(wl['rules'])} 条:")
    for r in wl['rules']:
        log(f"   • {r['stock_name']} {r['code']} {r['operator']} ¥{r['trigger_price']}")
    
    log("")
    
    while True:
        try:
            if is_trading_time():
                check_rules()
                time.sleep(60)  # 交易时间每 60 秒检查一次
            else:
                # 非交易时间：每 5 分钟检查一次（仅用于状态日志）
                now = datetime.now()
                if now.minute % 30 == 0 and now.second < 5:
                    log(f"⏸  非交易时间 {now:%H:%M} (周{['一','二','三','四','五','六','日'][now.weekday()]})")
                time.sleep(60)
        except KeyboardInterrupt:
            log("👋 手动停止")
            break
        except Exception as e:
            log(f"❌ 主循环异常: {e}")
            time.sleep(30)

if __name__ == "__main__":
    main_loop()
