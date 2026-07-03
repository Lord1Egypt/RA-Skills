#!/usr/bin/env python3
"""
小智实时监控预警 v2 — 融合 7大预警规则 + 三级分级预警 + 智能频率
融合自：stock-monitor(7大规则) + stock-monitor-skill(分级+动态止盈) + 原monitor.py(异动)

7大预警规则：
1. 成本百分比 — 盈利+15% / 亏损-12%
2. 日内涨跌幅 — 个股±4% / ETF±2%
3. 成交量异动 — 放量>2倍5日均量 / 缩量<0.5倍
4. 均线金叉/死叉 — MA5上穿/下穿MA10
5. RSI超买超卖 — RSI>70超买 / RSI<30超卖
6. 跳空缺口 — 向上/向下跳空>1%
7. 动态止盈 — 盈利10%+后回撤5%/10%

三级预警：
🚨 紧急级 — 多条件共振(≥3条件同时触发)
⚠️ 警告级 — 2个条件触发
📢 提醒级 — 单一条件触发
"""
import sys, os, json, re, urllib.request, urllib.parse, time
from datetime import datetime, date, timedelta
from pathlib import Path

if sys.stdout.encoding and 'UTF-8' not in sys.stdout.encoding.upper():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
os.environ.setdefault('PYTHONIOENCODING', 'utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch_stock import fetch_stock, fetch_hot_sectors

# ========================================
# 配置路径
# ========================================
WORKSPACE_ROOT = Path(os.environ.get("OPENCLAW_WORKSPACE", Path.cwd()))
MONITOR_DIR = WORKSPACE_ROOT / "data" / "stock-monitor"
MONITOR_DIR.mkdir(parents=True, exist_ok=True)

CONFIG_FILE = MONITOR_DIR / "config.json"
STATE_FILE  = MONITOR_DIR / "state.json"
LOG_FILE    = MONITOR_DIR / "log.jsonl"

HEADERS = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.eastmoney.com"}

# ========================================
# 默认配置
# ========================================
DEFAULT_CONFIG = {
    "update_time": datetime.now().isoformat(),
    "pools": {
        "self_select": {
            "stocks": {
                "600519": {"name": "贵州茅台", "type": "individual", "cost": None, "base_price": None},
                "300750": {"name": "宁德时代", "type": "individual", "cost": None, "base_price": None},
                "688981": {"name": "中芯国际", "type": "individual", "cost": None, "base_price": None},
                "601899": {"name": "紫金矿业", "type": "individual", "cost": None, "base_price": None},
                "603993": {"name": "洛阳钼业", "type": "individual", "cost": None, "base_price": None},
                "000630": {"name": "铜陵有色", "type": "individual", "cost": None, "base_price": None},
                "600036": {"name": "招商银行", "type": "individual", "cost": None, "base_price": None},
                "000001": {"name": "平安银行", "type": "individual", "cost": None, "base_price": None},
            },
            "alerts": {
                "cost_pct_above": 15.0,
                "cost_pct_below": -12.0,
                "change_pct_above": 4.0,
                "change_pct_below": -4.0,
                "volume_surge": 2.0,
                "volume_shrink": 0.5,
                "ma_monitor": True,
                "rsi_monitor": True,
                "gap_monitor": True,
                "trailing_stop": True,
            }
        }
    },
    "global_alerts": {
        "etf_change_pct_above": 2.0,
        "etf_change_pct_below": -2.0,
        "sector_surge_pct": 5.0,
    }
}

# ========================================
# 状态管理
# ========================================
def load_config() -> dict:
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text("utf-8"))
        except (json.JSONDecodeError, Exception):
            pass
    return dict(DEFAULT_CONFIG)

def save_config(cfg: dict):
    CONFIG_FILE.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), "utf-8")

def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text("utf-8"))
        except (json.JSONDecodeError, Exception):
            pass
    return {"last_check": None, "alerted": {}, "highest_profits": {}}

def save_state(state: dict):
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), "utf-8")

def log_event(event: dict):
    event["ts"] = datetime.now().isoformat()
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

# ========================================
# 数据获取
# ========================================
def get_market_prefix(full_code: str):
    """返回(market_id, clean_code)"""
    code = full_code.strip()
    if any(code.startswith(p) for p in ('60','68','11','51','58')):
        return 1, code
    elif any(code.startswith(p) for p in ('00','30','15','12','16','13')):
        return 0, code
    return 2, code

def fetch_eastmoney_detail(code: str) -> dict:
    """从东方财富获取详细行情（含换手率、量比、振幅、成交量）"""
    market, clean = get_market_prefix(code)
    url = (f"http://push2.eastmoney.com/api/qt/stock/get?"
           f"secid={market}.{clean}"
           "&fields=f43,f48,f57,f58,f60,f116,f162,f167,f168,f170,f292,f15,f17")
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=5) as resp:
            d = json.loads(resp.read().decode()).get("data", {}) or {}
            if not d.get("f43"): return {}
            return {
                "price": (d.get("f43", 0) or 0) / 100,
                "prev_close": (d.get("f60", 0) or 0) / 100,
                "change_pct": (d.get("f170", 0) or 0) / 100,
                "amount": (d.get("f48", 0) or 0) / 1e8,
                "volume": d.get("f15", 0) or 0,
                "amplitude": (d.get("f167", 0) or 0) / 100,
                "turnover_pct": (d.get("f168", 0) or 0) / 100,
                "volume_ratio": (d.get("f292", 0) or 0) / 100,
                "pe": (d.get("f162", 0) or 0) / 100 if d.get("f162") else None,
                "market_cap": (d.get("f116", 0) or 0) / 1e8,
                "high": (d.get("f17", 0) or 0) / 100,
                "low": (d.get("f15", 0) or 0) / 100,
            }
    except Exception:
        return {}

def fetch_avg_volume(code: str, days: int = 5) -> float:
    """获取5日均量（从历史K线估算）"""
    # 简版：从最近几天的交易量估算
    # 实际应该调用K线API，这里用成交量反推
    detail = fetch_eastmoney_detail(code)
    if not detail:
        return 0
    # 如果量比可用，反推5日均量
    vol_ratio = detail.get("volume_ratio", 0)
    current_vol = detail.get("amount", 0)
    if vol_ratio and vol_ratio > 0 and current_vol > 0:
        return current_vol / vol_ratio
    return current_vol  # fallback

def fetch_kline(code: str, ktype: str = "KLINE_TYPE_DAILY", limit: int = 60) -> list:
    """获取日K线数据用于技术指标计算"""
    market, clean = get_market_prefix(code)
    secid = f"{market}.{clean}"
    url = (f"https://push2his.eastmoney.com/api/qt/stock/kline/get?"
           f"secid={secid}&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61"
           f"&klt=101&fqt=1&end=20500101&lmt={limit}")
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode()).get("data", {}) or {}
            klinedata = data.get("klines", [])
            result = []
            for line in klinedata:
                parts = line.split(",")
                # f51=日期 f52=开盘 f53=收盘 f54=最高 f55=最低 f56=成交量 f57=成交额
                if len(parts) >= 8:
                    result.append({
                        "date": parts[0],
                        "open": float(parts[1]),
                        "close": float(parts[2]),
                        "high": float(parts[3]),
                        "low": float(parts[4]),
                        "volume": float(parts[5]),
                        "amount": float(parts[6]),
                    })
            return result
    except Exception:
        return []

def calc_ma(kline: list, period: int = 5) -> list:
    """计算移动平均线"""
    closes = [k["close"] for k in kline]
    ma = []
    for i in range(len(closes)):
        if i < period - 1:
            ma.append(None)
        else:
            ma.append(sum(closes[i-period+1:i+1]) / period)
    return ma

def calc_rsi(kline: list, period: int = 14) -> list:
    """计算RSI"""
    closes = [k["close"] for k in kline]
    rsi = []
    for i in range(len(closes)):
        if i < period:
            rsi.append(None)
            continue
        gains, losses = 0, 0
        for j in range(i - period + 1, i + 1):
            diff = closes[j] - closes[j-1]
            if diff > 0: gains += diff
            else: losses -= diff
        if losses == 0:
            rsi_val = 100
        else:
            rs = gains / period / (losses / period)
            rsi_val = 100 - 100 / (1 + rs)
        rsi.append(round(rsi_val, 2))
    return rsi

# ========================================
# 7大预警规则引擎
# ========================================
def check_alerts(code: str, stock_cfg: dict, state: dict) -> list:
    """对单只股票运行7大预警规则"""
    detail = fetch_eastmoney_detail(code)
    if not detail:
        return []

    alerts = []
    today = date.today().isoformat()
    price = detail.get("price", 0)
    chg_pct = detail.get("change_pct", 0)
    amount_yi = detail.get("amount", 0)
    vol_ratio = detail.get("volume_ratio", 0)
    amplitude = detail.get("amplitude", 0)
    prev_close = detail.get("prev_close", 0)
    stock_type = stock_cfg.get("type", "individual")
    stock_name = stock_cfg.get("name", code)
    cost = stock_cfg.get("cost")
    base_price = stock_cfg.get("base_price", prev_close)
    alerts_cfg = stock_cfg.get("alerts", {})

    triggered_conditions = []
    triggered_details = []

    # --- 规则1: 成本百分比 ---
    if cost and cost > 0:
        profit_pct = (price - cost) / cost * 100
        threshold_above = alerts_cfg.get("cost_pct_above", 15.0)
        threshold_below = alerts_cfg.get("cost_pct_below", -12.0)

        # 首次到达成本阈值
        alert_key = f"{code}_cost_{today}"
        if profit_pct >= threshold_above and alert_key not in state.get("alerted", {}):
            triggered_conditions.append("cost_profit")
            triggered_details.append(f"🎯 盈利 {profit_pct:.1f}% (目标价 ¥{cost*(1+threshold_above/100):.2f})")

        if profit_pct <= threshold_below and alert_key not in state.get("alerted", {}):
            triggered_conditions.append("cost_loss")
            triggered_details.append(f"📉 亏损 {profit_pct:.1f}% (止损价 ¥{cost*(1+threshold_below/100):.2f})")

    # --- 规则2: 日内涨跌幅 ---
    if stock_type == "individual":
        chg_threshold_above = alerts_cfg.get("change_pct_above", 4.0)
        chg_threshold_below = alerts_cfg.get("change_pct_below", -4.0)
        # ETF/黄金用全局配置
    elif stock_type == "etf":
        chg_threshold_above = DEFAULT_CONFIG["global_alerts"]["etf_change_pct_above"]
        chg_threshold_below = DEFAULT_CONFIG["global_alerts"]["etf_change_pct_below"]
    else:
        chg_threshold_above = 4.0
        chg_threshold_below = -4.0

    alert_key_daily = f"{code}_daily_{today}"
    if chg_pct >= chg_threshold_above and alert_key_daily not in state.get("alerted", {}):
        triggered_conditions.append("daily_surge")
        triggered_details.append(f"📊 日内大涨 {chg_pct:.2f}% (阈值 +{chg_threshold_above:.1f}%)")
    elif chg_pct <= chg_threshold_below and alert_key_daily not in state.get("alerted", {}):
        triggered_conditions.append("daily_plunge")
        triggered_details.append(f"📊 日内大跌 {chg_pct:.2f}% (阈值 {chg_threshold_below:.1f}%)")

    # --- 规则3: 成交量异动 ---
    avg_vol = fetch_avg_volume(code)
    alert_key_vol = f"{code}_vol_{today}"
    if avg_vol > 0 and amount_yi > 0:
        vol_surge_threshold = alerts_cfg.get("volume_surge", 2.0)
        vol_shrink_threshold = alerts_cfg.get("volume_shrink", 0.5)
        vol_ratio_to_avg = amount_yi / avg_vol if avg_vol > 0 else 0

        if vol_ratio_to_avg >= vol_surge_threshold and alert_key_vol not in state.get("alerted", {}):
            triggered_conditions.append("volume_surge")
            triggered_details.append(f"📊 放量 {vol_ratio_to_avg:.1f}倍 ({amount_yi:.1f}亿)")
        elif vol_ratio_to_avg <= vol_shrink_threshold and alert_key_vol not in state.get("alerted", {}):
            triggered_conditions.append("volume_shrink")
            triggered_details.append(f"📊 缩量 {vol_ratio_to_avg:.1f}倍 ({amount_yi:.1f}亿)")

    # --- 规则4: 均线金叉/死叉 ---
    if alerts_cfg.get("ma_monitor", True):
        kline = fetch_kline(code)
        if kline and len(kline) >= 15:
            ma5 = calc_ma(kline, 5)
            ma10 = calc_ma(kline, 10)
            # 检查最新两根K线的MA关系变化
            if len(ma5) >= 2 and ma5[-2] is not None and ma5[-1] is not None and ma10[-2] is not None and ma10[-1] is not None:
                alert_key_ma = f"{code}_ma_{today}"
                prev_cross = ma5[-2] - ma10[-2]
                curr_cross = ma5[-1] - ma10[-1]
                # 金叉: 之前MA5<MA10, 现在MA5>MA10
                if prev_cross <= 0 and curr_cross > 0 and alert_key_ma not in state.get("alerted", {}):
                    triggered_conditions.append("ma_golden_cross")
                    triggered_details.append(f"🌟 均线金叉 (MA5¥{ma5[-1]:.2f}上穿MA10¥{ma10[-1]:.2f})")
                # 死叉: 之前MA5>MA10, 现在MA5<MA10
                elif prev_cross >= 0 and curr_cross < 0 and alert_key_ma not in state.get("alerted", {}):
                    triggered_conditions.append("ma_death_cross")
                    triggered_details.append(f"💀 均线死叉 (MA5¥{ma5[-1]:.2f}下穿MA10¥{ma10[-1]:.2f})")

    # --- 规则5: RSI超买超卖 ---
    if alerts_cfg.get("rsi_monitor", True):
        kline = fetch_kline(code)
        if kline and len(kline) >= 20:
            rsi_vals = calc_rsi(kline)
            if rsi_vals and rsi_vals[-1] is not None:
                alert_key_rsi = f"{code}_rsi_{today}"
                if rsi_vals[-1] > 70 and alert_key_rsi not in state.get("alerted", {}):
                    triggered_conditions.append("rsi_overbought")
                    triggered_details.append(f"🔥 RSI超买 ({rsi_vals[-1]:.1f} > 70)")
                elif rsi_vals[-1] < 30 and alert_key_rsi not in state.get("alerted", {}):
                    triggered_conditions.append("rsi_oversold")
                    triggered_details.append(f"❄️ RSI超卖 ({rsi_vals[-1]:.1f} < 30)")

    # --- 规则6: 跳空缺口 ---
    if alerts_cfg.get("gap_monitor", True) and prev_close > 0:
        open_gap_pct = (price - prev_close) / prev_close * 100
        gap_diff = chg_pct - amplitude  # 跳空约等于涨跌幅-振幅
        alert_key_gap = f"{code}_gap_{today}"
        if abs(gap_diff) >= 1.0 and alert_key_gap not in state.get("alerted", {}):
            direction = "向上" if open_gap_pct > 0 else "向下"
            triggered_conditions.append("gap")
            triggered_details.append(f"🕳️ {direction}跳空 {open_gap_pct:.1f}% (缺口幅度 {abs(gap_diff):.1f}%)")

    # --- 规则7: 动态止盈 ---
    if alerts_cfg.get("trailing_stop", True) and cost and cost > 0:
        current_profit = (price - cost) / cost * 100
        highest_key = f"{code}_highest_profit"
        highest_profit = state.get("highest_profits", {}).get(highest_key, current_profit)
        alert_key_trail = f"{code}_trail_{today}"

        # 记录最高盈利
        if current_profit > highest_profit:
            state.setdefault("highest_profits", {})[highest_key] = current_profit
            highest_profit = current_profit

        # 当最高盈利>=10%后，回撤触发
        if highest_profit >= 10.0:
            drawdown = highest_profit - current_profit
            if drawdown >= 5.0 and alert_key_trail not in state.get("alerted", {}):
                triggered_conditions.append("trailing_stop_5")
                triggered_details.append(f"📉 利润回撤 {drawdown:.1f}% (最高盈利{highest_profit:.1f}% → 当前{current_profit:.1f}%)")
            if drawdown >= 10.0:
                # 10%回撤也触发，但不重复标记
                tc = "trailing_stop_10"
                if tc not in triggered_conditions:
                    triggered_conditions.append(tc)
                    triggered_details.append(f"🚨 大幅回撤 {drawdown:.1f}% (建议减仓保护利润)")

    # ========================================
    # 三级分级
    # ========================================
    alert_count = len(triggered_conditions)
    if alert_count >= 3:
        level = "emergency"
        level_emoji = "🚨"
        level_label = "紧急"
    elif alert_count == 2:
        level = "warning"
        level_emoji = "⚠️"
        level_label = "警告"
    elif alert_count == 1:
        level = "info"
        level_emoji = "📢"
        level_label = "提醒"
    else:
        return []

    # 颜色按中国习惯
    color = "🔴" if chg_pct >= 0 else "🟢"

    # 生成预警记录
    alert_record = {
        "code": code,
        "name": stock_name,
        "price": price,
        "change_pct": chg_pct,
        "level": level,
        "level_emoji": level_emoji,
        "level_label": level_label,
        "color": color,
        "alert_count": alert_count,
        "conditions": triggered_conditions,
        "details": triggered_details,
        "pe": detail.get("pe"),
        "turnover": detail.get("turnover_pct"),
        "volume_ratio": vol_ratio,
        "amount_yi": amount_yi,
        "source": "东方财富",
    }

    # 标记已预警（防止重复触发）
    state.setdefault("alerted", {}).update({
        f"{code}_cost_{today}": True,
        f"{code}_daily_{today}": True,
        f"{code}_vol_{today}": True,
        f"{code}_ma_{today}": True,
        f"{code}_rsi_{today}": True,
        f"{code}_gap_{today}": True,
        f"{code}_trail_{today}": True,
    })

    return [alert_record]


def check_sector_alerts(cfg: dict) -> list:
    """板块异动监测"""
    alerts = []
    try:
        sectors = fetch_hot_sectors()
        if not sectors:
            return []
        for sec in sectors:
            chg = sec.get("change_pct", 0)
            if chg >= cfg.get("global_alerts", {}).get("sector_surge_pct", 5.0):
                alerts.append({
                    "type": "sector_surge",
                    "name": sec["name"],
                    "change_pct": chg,
                    "level": "warning",
                    "level_emoji": "⚠️",
                    "level_label": "警告",
                    "detail": f"🔥 {sec['name']}板块暴拉 {chg:+.2f}%",
                })
    except Exception:
        pass
    return alerts


# ========================================
# 格式化输出
# ========================================
def fmt_alert(alert: dict) -> str:
    """单条预警格式化"""
    emoji = alert.get("level_emoji", "📢")
    level = alert.get("level_label", "提醒")
    color = alert.get("color", "")
    name = alert.get("name", "")
    code = alert.get("code", "")
    price = alert.get("price", 0)
    chg = alert.get("change_pct", 0)
    details = alert.get("details", [])

    lines = [
        f"{emoji}【{level}】{color} {name} ({code})",
        f"{'=' * 40}",
        f"💰 当前价格: ¥{price:.2f} ({chg:+.2f}%)",
    ]
    if alert.get("pe"): lines.append(f"📊 PE: {alert['pe']}")
    if alert.get("turnover"): lines.append(f"📊 换手率: {alert['turnover']}%")
    if alert.get("volume_ratio"): lines.append(f"📊 量比: {alert['volume_ratio']}")

    lines.append("")
    lines.append(f"🎯 触发预警 ({alert.get('alert_count', 0)}项):")
    for d in details:
        lines.append(f"  • {d}")

    lines.append(f"  📡 {alert.get('source', '')}")
    return "\n".join(lines)

def fmt_alerts(alerts: list, pool_name: str = "自选池") -> str:
    """完整预警报告"""
    if not alerts:
        return "✅ 无异常信号"

    emergency = [a for a in alerts if a.get("level") == "emergency"]
    warning = [a for a in alerts if a.get("level") == "warning"]
    info = [a for a in alerts if a.get("level") == "info"]

    lines = [
        f"🚨 **小智监控预警**",
        f"  监测池: {pool_name}",
        f"  时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
    ]

    for group in [("紧急级", emergency, "🚨"), ("警告级", warning, "⚠️"), ("提醒级", info, "📢")]:
        if group[1]:
            lines.append(f"--- {group[2]} {group[0]} ({len(group[1])}条) ---")
            for a in group[1]:
                for d in a.get("details", []):
                    lines.append(f"  • {d}")
                price = a.get("price", 0)
                chg = a.get("change_pct", 0)
                name = a.get("name", "")
                code = a.get("code", "")
                lines.append(f"  ├ {name}({code}) ¥{price:.2f} ({chg:+.2f}%)")
                lines.append("")

    lines.append(f"共 {len(alerts)} 条预警 (紧急{len(emergency)} / 警告{len(warning)} / 提醒{len(info)})")
    return "\n".join(lines)


# ========================================
# 主流程
# ========================================
def main_run() -> dict:
    """
    运行一次完整监控检查
    返回: {"alerts": [...], "emergency": int, "warning": int, "info": int}
    """
    cfg = load_config()
    state = load_state()

    all_alerts = []
    today = date.today().isoformat()

    # 每天重置预警状态（续警机制）
    last_check = state.get("last_check", "")
    if last_check != today:
        state["alerted"] = {}
        state["last_check"] = today

    # 遍历所有池
    for pool_name, pool_cfg in cfg.get("pools", {}).items():
        pool_alerts_cfg = pool_cfg.get("alerts", {})
        for code, stock_cfg in pool_cfg.get("stocks", {}).items():
            # 合并个股配置+池级配置
            full_cfg = dict(stock_cfg)
            full_cfg["alerts"] = pool_alerts_cfg
            alerts = check_alerts(code, full_cfg, state)
            all_alerts.extend(alerts)

    # 板块异动
    sector_alerts = check_sector_alerts(cfg)
    all_alerts.extend(sector_alerts)

    # 保存状态
    save_state(state)

    # 记录日志
    for a in all_alerts:
        log_event({"type": "alert", "data": {k: v for k, v in a.items() if k not in ("details",)}})

    result = {
        "count": len(all_alerts),
        "emergency": len([a for a in all_alerts if a.get("level") == "emergency"]),
        "warning": len([a for a in all_alerts if a.get("level") == "warning"]),
        "info": len([a for a in all_alerts if a.get("level") == "info"]),
        "alerts": all_alerts,
    }
    return result


# ========================================
# CLI入口
# ========================================
def main():
    import argparse
    parser = argparse.ArgumentParser(description="小智实时监控预警 v2 — 7大规则 + 三级分级")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    parser.add_argument("--config", action="store_true", help="显示当前配置")
    parser.add_argument("--add-stock", nargs=2, metavar=("CODE", "NAME"), help="添加监控股票")
    parser.add_argument("--remove-stock", metavar="CODE", help="移除监控股票")
    parser.add_argument("--set-cost", nargs=2, metavar=("CODE", "PRICE"), help="设置持仓成本")
    parser.add_argument("--log", action="store_true", help="查看最近预警日志")
    parser.add_argument("--watchlist", action="store_true", help="查看当前监控列表")
    args = parser.parse_args()

    if args.config:
        cfg = load_config()
        print(json.dumps(cfg, ensure_ascii=False, indent=2))
        return

    if args.add_stock:
        code, name = args.add_stock
        cfg = load_config()
        cfg.setdefault("pools", {}).setdefault("self_select", {}).setdefault("stocks", {})[code] = {
            "name": name, "type": "individual", "cost": None, "base_price": None
        }
        save_config(cfg)
        print(f"✅ 已添加 {name}({code}) 到监控池")
        return

    if args.remove_stock:
        code = args.remove_stock
        cfg = load_config()
        pool = cfg.get("pools", {}).get("self_select", {}).get("stocks", {})
        if code in pool:
            name = pool[code]["name"]
            del pool[code]
            save_config(cfg)
            print(f"✅ 已移除 {name}({code}) 从监控池")
        else:
            print(f"❌ 未找到 {code}")
        return

    if args.set_cost:
        code, price = args.set_cost
        try:
            price = float(price)
            cfg = load_config()
            stock = cfg.get("pools", {}).get("self_select", {}).get("stocks", {}).get(code)
            if stock:
                stock["cost"] = price
                save_config(cfg)
                print(f"✅ 已设置 {stock['name']}({code}) 持仓成本: ¥{price:.2f}")
            else:
                print(f"❌ 未找到 {code}，先 --add-stock 添加")
        except ValueError:
            print("❌ 价格格式错误")
        return

    if args.log:
        if LOG_FILE.exists():
            lines = []
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                count = 0
                for line in f:
                    if line.strip():
                        try:
                            evt = json.loads(line)
                            lines.append(f"{evt.get('ts','')} [{evt.get('type','')}] {json.dumps(evt.get('data',{}), ensure_ascii=False)}")
                            count += 1
                        except json.JSONDecodeError:
                            pass
                        if count >= 30:
                            break
            print("\n".join(reversed(lines)) if lines else "暂无日志")
        else:
            print("暂无日志")
        return

    if args.watchlist:
        cfg = load_config()
        for pool_name, pool_cfg in cfg.get("pools", {}).items():
            print(f"\n📋 {pool_name}:")
            for code, info in pool_cfg.get("stocks", {}).items():
                cost = info.get("cost")
                cost_str = f"成本¥{cost:.2f}" if cost else "未设置"
                print(f"  {info['name']}({code}) {cost_str}")
        return

    # 默认：运行一次监控检查
    result = main_run()
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        alerts = result["alerts"]
        pool_name = list(load_config().get("pools", {}).keys())[0] if load_config().get("pools") else ""
        if alerts:
            print(fmt_alerts(alerts, pool_name))
        else:
            print("✅ 无异常信号")


if __name__ == "__main__":
    main()
