"""
stock_monitor_skill.py - 股票交易监控系统

单次检查模式：由 Clawdbot 定时任务驱动，每次执行一轮采集+判断，
发现异常直接返回告警消息，由 cron 调度层推送至用户。

日志记录：独立文件记录每日开盘价、收盘价、最高/最低价及预警时间。
"""

import os
import json
import requests
from datetime import datetime, date, time as dtime

# 模块级路径常量
_SELF_DIR = os.path.dirname(os.path.abspath(__file__))
_CONFIG_PATH = os.path.join(_SELF_DIR, "stock_config.json")
_STATE_PATH = os.path.join(_SELF_DIR, ".alert_state.json")
_LOG_PATH = os.path.join(_SELF_DIR, "stock_daily_log.json")

# ──────────────────────────────────────────────
# 技能元数据
# ──────────────────────────────────────────────

__skill__ = {
    "name": "stock_monitor",
    "description": "股票监控：查询实时股价并检查价格/涨跌幅是否触发预警条件",
    "version": "2.2.0",
    "parameters": {
        "action": {
            "type": "string",
            "description": "操作指令：'check'（检查一次）/'query'（查询当前股价）/'log'（查看今日日志）/'log_history'（查看历史日志）",
            "default": "check",
        },
    },
    "returns": {
        "type": "string",
        "description": "检查结果、告警消息或日志内容",
    },
}

# ──────────────────────────────────────────────
# 配置管理
# ──────────────────────────────────────────────


def load_config():
    """加载自选股与预警配置。"""
    try:
        with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return _default_config()


def _default_config():
    return {
        "stocks": [
            {"code": "600519", "name": "贵州茅台", "price_high": 1800, "price_low": 1600,
             "rise_pct": 3, "fall_pct": -3},
            {"code": "000001", "name": "平安银行", "price_high": 12.0, "price_low": 10.0,
             "rise_pct": 4.0, "fall_pct": -4.0},
        ],
        "check_interval": 30,
        "only_once": True,
    }


# ──────────────────────────────────────────────
# 状态管理（"仅提醒一次"持久化）
# ──────────────────────────────────────────────


def _load_state():
    """加载已触发过的告警记录。"""
    try:
        with open(_STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save_state(state):
    """保存告警记录到文件。"""
    with open(_STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False)


def _check_and_record_alert(key, state, only_once):
    """
    检查告警 key 是否已触发过；若仅提醒一次则记录并返回 True，否则直接返回 True。

    Returns:
        True 表示本次应发送告警，False 表示已提醒过应跳过
    """
    today = str(date.today())
    if state.get("date") != today:
        state.clear()
        state["date"] = today

    if key in state:
        return False  # 当日已提醒过

    if only_once:
        state[key] = True
        _save_state(state)

    return True


# ──────────────────────────────────────────────
# 日志管理
# ──────────────────────────────────────────────


def _load_daily_log():
    """加载每日日志文件。"""
    try:
        with open(_LOG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save_daily_log(log):
    """保存每日日志到文件。"""
    with open(_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)


def _get_today_log():
    """获取今日日志条目（自动初始化）。"""
    log = _load_daily_log()
    today = str(date.today())
    if today not in log:
        log[today] = {}
    return log, today


def _update_price_log(code, name, now_price, open_price=None, high_price=None, low_price=None):
    """
    更新股票的价格日志。

    优先使用 API 返回的当日真实最高/最低价，避免快照遗漏极值。
    """
    log, today = _get_today_log()
    stock_key = str(code)

    if stock_key not in log[today]:
        log[today][stock_key] = {
            "name": name,
            "open": open_price or now_price,
            "close": now_price,
            "high": high_price or now_price,
            "low": low_price or now_price,
            "alerts": []
        }
    else:
        entry = log[today][stock_key]
        entry["close"] = now_price
        # 优先使用 API 返回的当日真实最高/最低
        if high_price is not None and high_price > entry["high"]:
            entry["high"] = high_price
        elif now_price > entry["high"]:
            entry["high"] = now_price
        if low_price is not None and low_price < entry["low"]:
            entry["low"] = low_price
        elif now_price < entry["low"]:
            entry["low"] = now_price
        # open 只在首次记录，不再覆盖

    _save_daily_log(log)


def _log_alert(code, name, alert_type, price, message, open_price=None, high_price=None, low_price=None):
    """
    记录预警触发事件到日志。

    Args:
        code: 股票代码
        name: 股票名称
        alert_type: 预警类型（high/low/rise/fall）
        price: 触发时的价格
        message: 告警消息
        open_price/high_price/low_price: API 返回的当日真实极值
    """
    log, today = _get_today_log()
    stock_key = str(code)

    if stock_key not in log[today]:
        log[today][stock_key] = {
            "name": name,
            "open": open_price or price,
            "close": price,
            "high": high_price or price,
            "low": low_price or price,
            "alerts": []
        }

    now_str = datetime.now().strftime("%H:%M:%S")
    log[today][stock_key]["alerts"].append({
        "time": now_str,
        "type": alert_type,
        "price": price,
        "message": message
    })

    _save_daily_log(log)


def query_daily_log():
    """返回今日日志的可读摘要。"""
    log, today = _get_today_log()
    if today not in log or not log[today]:
        return "📋 今日尚无日志记录"

    lines = [f"📋 股票日志 - {today}", "=" * 30]
    for code, entry in log[today].items():
        name = entry["name"]
        open_p = entry["open"]
        close_p = entry["close"]
        high_p = entry["high"]
        low_p = entry["low"]
        lines.append(f"\n{name}({code})")
        lines.append(f"  开盘: {open_p}  |  收盘: {close_p}")
        lines.append(f"  最高: {high_p}  |  最低: {low_p}")
        if entry["alerts"]:
            lines.append(f"  ⚠️ 预警记录 ({len(entry['alerts'])}次):")
            for a in entry["alerts"]:
                lines.append(f"    {a['time']} [{a['type']}] {a['message']}")
        else:
            lines.append("  预警: 无")
    return "\n".join(lines)


def query_log_history(days=7):
    """返回最近 N 天的日志摘要。"""
    log = _load_daily_log()
    if not log:
        return "📋 暂无历史日志"

    sorted_dates = sorted(log.keys(), reverse=True)[:days]
    lines = [f"📋 历史日志 (最近{days}天)", "=" * 30]

    for d in sorted_dates:
        day_data = log[d]
        lines.append(f"\n--- {d} ---")
        for code, entry in day_data.items():
            name = entry["name"]
            open_p = entry["open"]
            close_p = entry["close"]
            alert_count = len(entry["alerts"])
            lines.append(f"  {name}({code}) 开:{open_p} 收:{close_p} 预警:{alert_count}次")

    return "\n".join(lines)


# ──────────────────────────────────────────────
# 行情获取
# ──────────────────────────────────────────────


def get_real_price(code):
    """
    获取单只股票实时行情（完整版）。

    API 返回格式（完整 30+ 字段）：
      name, open, last_close, now, high, low, buy1, sell1, volume, amount, ...
    """
    try:
        prefix = "sh" if code.startswith("6") else "sz"
        url = f"https://hq.sinajs.cn/list={prefix}{code}"
        resp = requests.get(url, headers={"Referer": "https://finance.sina.com.cn/"}, timeout=5)
        resp.encoding = "gbk"
        arr = resp.text.split('"')[1].split(",")
        now_price = float(arr[3])       # 当前价
        open_price = float(arr[1])      # 今开
        last_close = float(arr[2])      # 昨收
        high_price = float(arr[4])      # 当日最高
        low_price = float(arr[5])       # 当日最低

        # 保护：now 为 0 或 close 为 0 时标记为无效行情（盘前/休市）
        if now_price == 0.0 or last_close <= 0.0:
            return None

        change_amt = round(now_price - last_close, 2)
        change_pct = round(change_amt / last_close * 100, 2) if last_close > 0 else 0.0

        return {
            "name": arr[0],
            "now": now_price,
            "open": open_price,
            "close": last_close,
            "high": high_price,
            "low": low_price,
            "change_pct": change_pct,
        }
    except (IndexError, ValueError, requests.RequestException):
        return None


# ──────────────────────────────────────────────
# 核心：单次检查（含日志）
# ──────────────────────────────────────────────


def check_stocks():
    """
    执行一轮行情检查，返回所有新触发的告警。

    规则：
      - 高价/低价超出阈值 → 🚨
      - 涨跌幅超出阈值   → 📈/📉
      - 当日同条件仅提醒一次（由 only_once 控制）
      - 每次检查自动记录价格日志

    Returns:
        str: 有告警时返回告警汇总；无告警时返回 None
    """
    config = load_config()
    state = _load_state()
    only_once = config.get("only_once", True)
    alerts = []

    for stock in config["stocks"]:
        data = get_real_price(stock["code"])
        if not data:
            alerts.append(f"⚠️ {stock['name']}（{stock['code']}）获取行情失败")
            continue

        now_price = data["now"]
        last_close = data["close"]
        pct = data["change_pct"]
        code = stock["code"]
        name = stock["name"]

        # --- 记录价格日志（含 API 返回的真实最高/最低） ---
        _update_price_log(code, name, now_price, open_price=data["open"],
                          high_price=data["high"], low_price=data["low"])

        # 高价预警
        if now_price >= stock["price_high"]:
            key = f"{code}_high"
            msg = f"🚨 {name} 价格触高！现价:{now_price} 阈值:{stock['price_high']}"
            if _check_and_record_alert(key, state, only_once):
                _log_alert(code, name, "price_high", now_price, msg,
                           open_price=data["open"], high_price=data["high"], low_price=data["low"])
                alerts.append(msg)

        # 低价预警
        if now_price <= stock["price_low"]:
            key = f"{code}_low"
            msg = f"🚨 {name} 价格触低！现价:{now_price} 阈值:{stock['price_low']}"
            if _check_and_record_alert(key, state, only_once):
                _log_alert(code, name, "price_low", now_price, msg,
                           open_price=data["open"], high_price=data["high"], low_price=data["low"])
                alerts.append(msg)

        # 涨幅预警
        if pct >= stock["rise_pct"]:
            key = f"{code}_rise"
            msg = f"📈 {name} 涨幅超标！涨幅:{pct}% 阈值:{stock['rise_pct']}%"
            if _check_and_record_alert(key, state, only_once):
                _log_alert(code, name, "rise", now_price, msg,
                           open_price=data["open"], high_price=data["high"], low_price=data["low"])
                alerts.append(msg)

        # 跌幅预警
        if pct <= stock["fall_pct"]:
            key = f"{code}_fall"
            msg = f"📉 {name} 跌幅超标！跌幅:{pct}% 阈值:{stock['fall_pct']}%"
            if _check_and_record_alert(key, state, only_once):
                _log_alert(code, name, "fall", now_price, msg,
                           open_price=data["open"], high_price=data["high"], low_price=data["low"])
                alerts.append(msg)

    return "\n".join(alerts) if alerts else None


def query_all_prices():
    """查询全部股票当前实时价格（含日志记录）。"""
    config = load_config()
    lines = ["===== 实时股票行情 ====="]
    for stock in config["stocks"]:
        data = get_real_price(stock["code"])
        if data:
            # 同步记录价格日志（含 API 返回的真实最高/最低）
            _update_price_log(stock["code"], stock["name"], data["now"],
                              open_price=data["open"], high_price=data["high"],
                              low_price=data["low"])
            pct = data["change_pct"]
            lines.append(f"{stock['name']}({stock['code']}) | 现价:{data['now']} | 最高:{data['high']} 最低:{data['low']} | 涨跌幅:{pct}%")
        else:
            lines.append(f"{stock['name']}({stock['code']}) | 获取行情失败")
    return "\n".join(lines)


# ──────────────────────────────────────────────
# 对外入口
# ──────────────────────────────────────────────


def run(params=None):
    """
    Clawdbot 入口函数。

    支持指令：
    - 'check' / 无参数 → 执行一轮检查，返回告警
    - 'query'         → 返回所有股票实时行情
    - 'log'           → 查看今日日志
    - 'log_history'   → 查看最近 7 天历史日志
    """
    if not params:
        params = "check"

    cmd = str(params).strip()
    if cmd in ("check", "检查"):
        result = check_stocks()
        return result or "✅ 所有指标正常"
    elif cmd in ("query", "查询"):
        return query_all_prices()
    elif cmd in ("log", "日志"):
        return query_daily_log()
    elif cmd in ("log_history", "历史日志"):
        return query_log_history()
    else:
        return f'未知指令。支持: check（检查）/ query（查询）/ log（日志）/ log_history（历史日志）'


# ──────────────────────────────────────────────
# 本地测试
# ──────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    action = sys.argv[1] if len(sys.argv) > 1 else "check"
    print(run(action))
