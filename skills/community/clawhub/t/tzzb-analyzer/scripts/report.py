#!/usr/bin/env python3
"""
同花顺持仓 - 定时报告生成器 v2.0
支持早盘、午盘、收盘三种报告模式，自动获取持仓+交易数据，整合免费新闻源，输出 Markdown 并推送飞书

用法:
    python report.py morning   # 早盘报告（9:25前）
    python report.py midday    # 午盘报告（12:55前）
    python report.py close    # 收盘复盘（17:00后）
    python report.py --feishu  # 输出飞书富文本格式
"""

import sys
import json
import os
import subprocess
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict


# ============ 路径配置 ============
SKILL_DIR = Path(__file__).parent.parent
SCRIPTS_DIR = Path(__file__).parent
TZzb_PARSER_DIR = SCRIPTS_DIR / "tzzb_parser"
if str(TZzb_PARSER_DIR) not in sys.path:
    sys.path.insert(0, str(TZzb_PARSER_DIR))

MEMORY_DIR = SKILL_DIR / "memory"
DATA_DIR = SKILL_DIR / "data"
MEMORY_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

# ============ 工具函数 ============
def _to_float(v, default=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return default

def _to_int(v, default=0):
    try:
        return int(v)
    except (TypeError, ValueError):
        return default

def _load_json(path: Path, default=None):
    if path.exists():
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return default if default is not None else {}

def _run_cmd(cmd: list, timeout=30) -> str:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return result.stdout.strip()
    except Exception:
        return ""


# ============ 数据获取（一次 CDP 会话）============
def get_all_tzzb():
    """
    一次性从同花顺获取持仓 + 交易记录，共用一次 Chrome 会话
    返回 (positions_data, trades_data)
    """
    from main import fetch_positions, fetch_trade_records
    from cookie_extractor import cdp_session

    positions = {}
    trades = {}
    try:
        with cdp_session() as (context, page):
            positions = fetch_positions(context=context, page=page)
            trades = fetch_trade_records(context=context, page=page)
    except Exception as e:
        positions = {"ok": False, "error": str(e)}
        trades = {"ok": False, "error": str(e)}
    return positions, trades


def get_tzzb_positions() -> dict:
    from main import fetch_positions
    from cookie_extractor import cdp_session
    try:
        with cdp_session() as (context, page):
            return fetch_positions(context=context, page=page)
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ============ 新闻获取（东方财富 RSS，无需 API Key）============
def fetch_news_from_mcp(queries: list[str], max_results: int = 5) -> list[dict]:
    """
    新闻获取接口。
    新闻数据由调用方通过 --news 参数传入（JSON 格式）。
    本函数仅作参数验证，返回空列表（实际数据由 main() 从 --news 解析）。
    """
    return []  # 实际数据从 CLI --news 参数注入，详见 main() 中的 json.loads(news_raw)
    """
    通过东方财富 RSS 获取财经新闻，无需 API Key
    用内置 urllib + re，正则提取 title/link/description
    """
    import re
    import ssl
    import urllib.request

    all_news = []
    rss_urls = [
        "https://feed.eastmoney.com/moneyflow.html",
        "https://news.eastmoney.com/rss.xml",
    ]
    req_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "*/*",
    }

    for rss_url in rss_urls:
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            req = urllib.request.Request(rss_url, headers=req_headers)
            with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
                raw = resp.read().decode("utf-8-sig", errors="ignore")

            # 用正则提取标题（支持 CDATA 和普通标签）
            titles = re.findall(
                r'<title[^>]*>(?:<!\[CDATA\[([^\]]*)\]\]>|https?://[^\s<]*)</title>',
                raw, re.IGNORECASE
            )
            # 去掉 feed 名称（第一个 title 通常是 feed 名）
            titles = [t.strip() for t in titles if t.strip()]
            titles = titles[1:] if len(titles) > 1 else titles

            # 提取 link
            links = re.findall(
                r'<link[^>]*>(?:<!\[CDATA\[([^\]]*)\]\]>|https?://[^\s<]+)</link>',
                raw, re.IGNORECASE
            )
            links = [l.strip() for l in links if l.strip().startswith("http")]

            # 提取 description
            descs_raw = re.findall(
                r'<description[^>]*>(?:<!\[CDATA\[([^\]]*)\]\]>|([^<]*)<)', raw, re.IGNORECASE
            )
            descs = [re.sub(r"<[^>]+>", "", (d[0] or d[1] or "")).strip() for d in descs_raw]

            for i, title in enumerate(titles[:30]):
                if not title or len(title) < 4:
                    continue
                summary = descs[i][:100] if i < len(descs) else ""
                link = links[i] if i < len(links) else ""
                for q in queries:
                    if q.lower() in title.lower() or q.lower() in summary.lower():
                        all_news.append({"title": title, "summary": summary, "link": link})
                        break
        except Exception:
            pass

    # 去重
    seen = set()
    deduped = []
    for n in all_news:
        key = n["title"][:30]
        if key not in seen:
            seen.add(key)
            deduped.append(n)
    return deduped[:15]


# ============ 数据解析 ============
def parse_positions(positions_data: dict) -> tuple[dict, list]:
    if not positions_data.get("ok"):
        return {}, []
    data = positions_data.get("data", {})
    return data.get("overview", {}), data.get("items", [])


def parse_trades(trades_data: dict) -> list:
    if not trades_data.get("ok"):
        return []
    return trades_data.get("data", {}).get("items", [])


def get_today_trades(trades: list) -> list:
    today_str = datetime.now().strftime("%Y-%m-%d")
    return [t for t in trades if t.get("trade_date", "").startswith(today_str)]


def get_recent_trades(trades: list, days: int = 5) -> list:
    """获取最近N天的交易"""
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    return [t for t in trades if t.get("trade_date", "") >= cutoff]


# ============ 交易复盘核心算法 ============
def aggregate_trades(trades: list) -> dict:
    """
    按股票聚合交易，计算加权平均成本和真实盈亏
    返回: {stock_code: {"name":, "buy_records":[], "sell_records":[],
                        "avg_cost": float, "total_buy_qty": int, "total_sell_qty": int,
                        "remaining_qty": int, "realized_pl": float}}
    """
    stocks = defaultdict(lambda: {
        "name": "", "buy_records": [], "sell_records": [],
        "avg_cost": 0.0, "total_buy_qty": 0, "total_sell_qty": 0,
        "remaining_qty": 0, "realized_pl": 0.0
    })

    for t in trades:
        code = t.get("stock_code", "")
        name = t.get("stock_name", "")
        trade_type = t.get("trade_type", "")
        price = _to_float(t.get("price"))
        qty = _to_int(t.get("quantity"))
        fee = _to_float(t.get("fee"))
        date = t.get("trade_date", "")

        record = {"date": date, "price": price, "qty": qty, "fee": fee}

        if "买" in trade_type:
            stocks[code]["name"] = name
            stocks[code]["buy_records"].append(record)
            stocks[code]["total_buy_qty"] += qty
        elif "卖" in trade_type:
            stocks[code]["name"] = name
            stocks[code]["sell_records"].append(record)
            stocks[code]["total_sell_qty"] += qty

    # 计算剩余持仓和已实现盈亏
    for code, s in stocks.items():
        remaining = s["total_buy_qty"] - s["total_sell_qty"]
        s["remaining_qty"] = max(0, remaining)

        # 已实现盈亏（按FIFO匹配买卖）
        buy_fifo = list(reversed(s["buy_records"]))  # 最近的先卖
        sell_fifo = list(reversed(s["sell_records"]))
        realized = 0.0
        buy_pool = []  # (price, qty)

        for rec in buy_fifo:
            buy_pool.append((rec["price"], rec["qty"], rec["fee"]))

        for sell in sell_fifo:
            sell_qty = sell["qty"]
            sell_price = sell["price"]
            while sell_qty > 0 and buy_pool:
                bp_price, bp_qty, bp_fee = buy_pool.pop(0)
                matched = min(sell_qty, bp_qty)
                realized += (sell_price - bp_price) * matched
                sell_qty -= matched
                if bp_qty > matched:
                    buy_pool.insert(0, (bp_price, bp_qty - matched, 0))
            # 手续费
            realized -= sell.get("fee", 0)

        s["realized_pl"] = realized

        # 加权平均成本（剩余持仓）
        if s["remaining_qty"] > 0:
            total_cost = sum(r["price"] * r["qty"] + r["fee"] for r in s["buy_records"])
            s["avg_cost"] = total_cost / s["total_buy_qty"]  # 按买入总量均摊

    return stocks


def review_aggregated_trades(stocks_trades: dict, current_prices: dict) -> str:
    """
    对聚合后的交易数据进行复盘点评
    current_prices: {stock_code: current_price}
    """
    if not stocks_trades:
        return "今日无交易记录。"

    lines = []
    total_realized = 0.0
    total_unrealized = 0.0

    for code, s in sorted(stocks_trades.items(), key=lambda x: x[1]["realized_pl"], reverse=True):
        name = s["name"] or code
        remaining = s["remaining_qty"]
        avg_cost = s["avg_cost"]
        current = current_prices.get(code, 0)
        realized = s["realized_pl"]

        # 已买卖总览
        buy_total = sum(r["price"] * r["qty"] for r in s["buy_records"])
        sell_total = sum(r["price"] * r["qty"] for r in s["sell_records"])
        buy_fee = sum(r["fee"] for r in s["buy_records"])
        sell_fee = sum(r["fee"] for r in s["sell_records"])

        lines.append(f"### {name}（{code}）")
        lines.append(f"- 买入 {s['total_buy_qty']} 股 / 卖出 {s['total_sell_qty']} 股 / 剩余 {remaining} 股")
        lines.append(f"- 买入总额 {buy_total:,.0f} 元（含费 {buy_fee:.2f} 元）")
        if s["sell_records"]:
            lines.append(f"- 卖出总额 {sell_total:,.0f} 元（含费 {sell_fee:.2f} 元）")
        lines.append(f"- **已实现盈亏：{realized:+,.0f} 元**")

        # 剩余持仓点评
        if remaining > 0 and current > 0:
            unrealized = (current - avg_cost) * remaining
            total_unrealized += unrealized
            unrealized_pct = (current - avg_cost) / avg_cost * 100 if avg_cost else 0
            lines.append(f"- 当前价 {current:.2f} / 平均成本 {avg_cost:.2f}")
            lines.append(f"- **浮动盈亏：{unrealized:+,.0f} 元（{unrealized_pct:+.1f}%）**")

            if unrealized > 0:
                lines.append(f"> 🟢 买入后上涨，{'注意分批止盈' if unrealized_pct > 10 else '可继续持有'}")
            elif unrealized < -buy_total * 0.05:
                lines.append(f"> 🔴 浮亏超5%，注意止损纪律，跌破成本价7%坚决执行")
            else:
                lines.append(f"> 🟡 小幅浮亏，继续持有观察")
        elif remaining > 0 and current == 0:
            lines.append(f"> ⚠️ 剩余 {remaining} 股暂无行情，按买入成本持有")
        else:
            lines.append(f"> 📗 已全部卖出，{'盈利了结' if realized > 0 else '亏损出场'}")

        # 手续费评价
        total_fee = buy_fee + sell_fee
        if total_fee > 0 and buy_total > 0:
            fee_rate = total_fee / buy_total
            if fee_rate > 0.003:
                lines.append(f"> ⚠️ 手续费率偏高（{fee_rate:.3%}），建议比较券商费率")

        total_realized += realized
        lines.append("")

    # 汇总
    lines.append("#### 📊 今日交易汇总")
    lines.append(f"- 已实现盈亏合计：**{total_realized:+,.0f} 元**")
    lines.append(f"- 浮动盈亏合计：**{total_unrealized:+,.0f} 元**")
    lines.append(f"- 当日综合盈亏：**{total_realized + total_unrealized:+,.0f} 元**")

    return "\n".join(lines)


# ============ 报告生成 ============
def gen_profit_tag(pct: float) -> str:
    if pct > 10:
        return "🔴强势"
    elif pct > 3:
        return "🟢上涨"
    elif pct > 0:
        return "🟢微涨"
    elif pct > -5:
        return "🟡微亏"
    elif pct > -15:
        return "🟠亏损"
    else:
        return "🔴深套"


# ========== 报告辅助函数 ==========

def _verdict_emoji(action: str) -> str:
    return {"持有": "🔵", "加仓": "🟢", "减仓": "🟠", "止损": "🔴"}.get(action, "⚪")


def _stock_verdict(cost: float, current: float, hold_days: int, profit_rate: float):
    """
    返回 (动作结论, 理由, 止损价)
    决策逻辑：
      亏损 > 15%  → 止损（严格执行）
      亏损 8%~15% → 止损（不等了）
      亏损 3%~8%  → 减仓（跌破成本8%止损）
      亏损 0~3%   → 持有（等反弹）
      盈利 0~8%   → 持有（跌破成本卖）
      盈利 8~15%  → 持有（允许回撤）
      盈利 > 15%  → 减仓（分批止盈）
    """
    if profit_rate < -15:
        action = "止损"
        reason = "亏损已超15%，进入深套区，止损是唯一纪律，次日低开果断执行"
        stop_loss = current * 0.97
    elif profit_rate < -8:
        action = "止损"
        reason = f"亏损{profit_rate:.1f}%，建议现价清仓，不再等待"
        stop_loss = current * 0.97
    elif profit_rate < -3:
        action = "减仓"
        reason = f"亏损{profit_rate:.1f}%，建议减半仓，剩余设定止损在成本价"
        stop_loss = cost * 0.97
    elif profit_rate < 0:
        action = "持有"
        reason = "微亏，不急于操作，等待明日反弹出现"
        stop_loss = cost * 0.97
    elif profit_rate < 8:
        action = "持有"
        reason = "小幅盈利，设定成本价为红线，跌破即卖出"
        stop_loss = cost * 0.999  # 极靠近成本，视觉上用相同价位表示"成本线即止损线"
    elif profit_rate < 15:
        action = "持有"
        reason = "盈利可观，继续持有让利润奔跑，设定回撤止盈"
        stop_loss = current * 0.93
    else:
        action = "减仓"
        reason = f"盈利{profit_rate:.1f}%，建议分批止盈，先卖一半保留利润"
        stop_loss = current * 0.90

    if hold_days > 180 and action in ("持有",):
        reason += "（长线持仓，注意定期检视基本面是否有变化）"

    return action, reason, stop_loss


def _cost_visual(cost: float, current: float, stop_loss: float) -> str:
    """
    ASCII 成本可视化示例：
         4.89止损
         5.21成本
         5.26现价
    """
    labels = sorted([
        (round(stop_loss, 2), f"止损 {round(stop_loss, 2)}"),
        (round(cost, 2),      f"成本 {round(cost, 2)}"),
        (round(current, 2),   f"现价 {round(current, 2)}"),
    ])
    mn = labels[0][0]
    mx = labels[-1][0]
    rng = mx - mn if mx != mn else 0.01

    parts = []
    for price, label in labels:
        pos = int((price - mn) / rng * 10) if rng > 0 else 5
        bar = "·" * pos + "◆" + "·" * (10 - pos)
        parts.append(f"  [{bar}] {label}")

    return "\n".join(parts)


def _verdict_summary(overview: dict, items: list):
    """返回 (总体结论, 仓位说明)"""
    total_asset = _to_float(overview.get("total_asset"))
    total_value = _to_float(overview.get("total_value"))
    position_rate = (total_value / total_asset * 100) if total_asset else 0
    total_profit = sum(_to_float(p.get("hold_profit", 0)) for p in items)

    if not items:
        verdict = "空仓观望"
        msg = "无持仓"
    elif position_rate > 80:
        verdict = "减仓控制风险"
        msg = f"仓位过重({position_rate:.0f}%)"
    elif position_rate < 20:
        verdict = "轻仓布局"
        msg = f"仓位较轻({position_rate:.0f}%)"
    else:
        verdict = "仓位适中"
        msg = f"仓位正常({position_rate:.0f}%)"

    profit_msg = f"整体{'盈利' if total_profit >= 0 else '亏损'}{abs(total_profit):.0f}元"
    return f"{verdict} | {profit_msg}", msg


# ========== 早盘报告 ==========
def build_morning_report(overview: dict, items: list, today_trades: list, news: list) -> str:
    now = datetime.now()
    total_asset = _to_float(overview.get("total_asset"))
    money_remain = _to_float(overview.get("money_remain"))
    total_profit = sum(_to_float(p.get("hold_profit", 0)) for p in items)
    verdict, pos_msg = _verdict_summary(overview, items)

    lines = []
    lines.append(f"# 📈 早盘操作指导  {now.strftime('%m/%d %H:%M')}")
    lines.append("")
    lines.append("---")
    lines.append("## 📊 账户状态")
    lines.append(f"| 项目 | 数值 |")
    lines.append(f"|------|------|")
    lines.append(f"| 总资产 | {total_asset:,.0f} 元 |")
    lines.append(f"| 可用资金 | {money_remain:,.0f} 元 |")
    lines.append(f"| 浮盈亏 | {total_profit:+,.0f} 元 |")
    lines.append(f"| {pos_msg} |")
    lines.append("")

    if today_trades:
        lines.append("## 💹 今日交易")
        stocks = aggregate_trades(today_trades)
        cp = {p.get("stock_code"): _to_float(p.get("current_price")) for p in items}
        lines.append(review_aggregated_trades(stocks, cp))
        lines.append("")
    else:
        lines.append("## 💹 今日交易")
        lines.append("暂无交易记录。")
        lines.append("")

    if news:
        lines.append("## 🌍 隔夜消息面")
        for n in news[:4]:
            lines.append(f"- **{n.get('title', '')}**")
            if n.get('snippet'):
                lines.append(f"  {n['snippet'][:60]}")
        lines.append("")

    total_value = _to_float(overview.get("total_value"))
    position_rate = (total_value / total_asset * 100) if total_asset else 0
    lines.append("## 🔮 今日大盘预判")
    if position_rate < 20:
        lines.append("**结论：轻仓布局** — 可用资金充裕，等待盘中买点出现，不追高。")
    elif position_rate > 75:
        lines.append("**结论：逢高减仓** — 仓位偏重，若大盘冲高可适当减至七成。")
    else:
        lines.append("**结论：持仓观望** — 仓位适中，不盲目加减仓，等待信号。")
    lines.append("")

    if items:
        lines.append("## 🎯 持仓操作建议")
        for pos in sorted(items, key=lambda x: _to_float(x.get("hold_profit", 0))):
            name = pos.get("stock_name", "?")
            code = pos.get("stock_code", "")
            cost = _to_float(pos.get("cost_price"))
            current = _to_float(pos.get("current_price"))
            hold_days = _to_int(pos.get("hold_days"))
            profit = _to_float(pos.get("hold_profit"))
            profit_rate = _to_float(pos.get("hold_rate", 0)) * 100

            action, reason, stop_loss = _stock_verdict(cost, current, hold_days, profit_rate)
            emoji = _verdict_emoji(action)

            lines.append(f"### {emoji} {name}（{code}）**{action}**")
            lines.append("```")
            lines.append(_cost_visual(cost, current, stop_loss))
            lines.append("```")
            lines.append(f"今日：{current:.2f}元  成本：{cost:.2f}元  浮盈：{profit:+,.0f}元（{profit_rate:+.1f}%）")
            lines.append(f"**建议：{reason}**")
            if stop_loss > 0:
                lines.append(f"止损价：{stop_loss:.2f}元（跌破即执行）")
            lines.append("")
    else:
        lines.append("## 🎯 操作建议")
        lines.append("空仓，建议继续观望。")
        lines.append("")

    lines.append("---")
    lines.append("⚠️ **免责声明**：以上为个人分析，不构成投资建议。股市有风险，盈亏自负。")
    return "\n".join(lines)


# ========== 午盘报告 ==========
def build_midday_report(overview: dict, items: list, today_trades: list, news: list) -> str:
    now = datetime.now()
    total_asset = _to_float(overview.get("total_asset"))
    total_value = _to_float(overview.get("total_value"))
    position_rate = (total_value / total_asset * 100) if total_asset else 0
    total_profit = sum(_to_float(p.get("hold_profit", 0)) for p in items)

    lines = []
    lines.append(f"# 🕐 午盘操作指导  {now.strftime('%m/%d %H:%M')}")
    lines.append("")
    lines.append("---")
    lines.append("## 📊 上午盘面状态")
    lines.append(f"| 项目 | 数值 |")
    lines.append(f"|------|------|")
    lines.append(f"| 浮盈亏 | {total_profit:+,.0f} 元 |")
    lines.append(f"| 仓位 | {position_rate:.0f}% |")
    lines.append(f"| 持仓 | {len(items)} 只 |")
    lines.append("")

    if today_trades:
        lines.append("## 💹 今日交易")
        stocks = aggregate_trades(today_trades)
        cp = {p.get("stock_code"): _to_float(p.get("current_price")) for p in items}
        lines.append(review_aggregated_trades(stocks, cp))
        lines.append("")
    else:
        lines.append("## 💹 今日交易")
        lines.append("暂无交易。")
        lines.append("")

    if news:
        lines.append("## 📰 盘中重要消息")
        for n in news[:3]:
            lines.append(f"- **{n.get('title', '')}**")
        lines.append("")

    lines.append("## 🎯 下午操作结论")
    if items:
        for pos in items:
            name = pos.get("stock_name", "?")
            code = pos.get("stock_code", "")
            cost = _to_float(pos.get("cost_price"))
            current = _to_float(pos.get("current_price"))
            hold_days = _to_int(pos.get("hold_days"))
            profit = _to_float(pos.get("hold_profit"))
            profit_rate = _to_float(pos.get("hold_rate", 0)) * 100

            action, reason, stop_loss = _stock_verdict(cost, current, hold_days, profit_rate)
            emoji = _verdict_emoji(action)

            lines.append(f"{emoji} **{name}**（{code}）**{action}**")
            lines.append(f"  现价 {current:.2f} / 成本 {cost:.2f} / {profit:+,.0f}元（{profit_rate:+.1f}%）")
            lines.append(f"  {reason}")
            if stop_loss > 0:
                lines.append(f"  止损价 {stop_loss:.2f}元，跌破严格执行")
            lines.append("")
    else:
        lines.append("空仓，下午继续保持观望。")

    if position_rate > 75:
        lines.append("")
        lines.append("⚠️ **仓位提醒**：当前仓位偏重，建议尾盘前适当减仓。")

    lines.append("---")
    lines.append("⚠️ **免责声明**：以上为个人分析，不构成投资建议。股市有风险，盈亏自负。")
    return "\n".join(lines)


# ========== 收盘报告 ==========
def build_close_report(overview: dict, items: list, today_trades: list, all_trades: list) -> str:
    now = datetime.now()
    total_asset = _to_float(overview.get("total_asset"))
    total_value = _to_float(overview.get("total_value"))
    money_remain = _to_float(overview.get("money_remain"))
    position_rate = (total_value / total_asset * 100) if total_asset else 0
    total_profit = sum(_to_float(p.get("hold_profit", 0)) for p in items)
    verdict, pos_msg = _verdict_summary(overview, items)

    lines = []
    lines.append(f"# 📉 收盘复盘  {now.strftime('%m/%d')}")
    lines.append("")
    lines.append("---")

    lines.append("## 🎯 今日结论（最重要）")
    if items:
        for pos in items:
            name = pos.get("stock_name", "?")
            code = pos.get("stock_code", "")
            cost = _to_float(pos.get("cost_price"))
            current = _to_float(pos.get("current_price"))
            hold_days = _to_int(pos.get("hold_days"))
            profit = _to_float(pos.get("hold_profit"))
            profit_rate = _to_float(pos.get("hold_rate", 0)) * 100

            action, reason, stop_loss = _stock_verdict(cost, current, hold_days, profit_rate)
            emoji = _verdict_emoji(action)

            lines.append(f"{emoji} **{name}**（{code}）**{action}**")
            lines.append(f"  {reason}")
    else:
        lines.append("空仓观望，无操作。")
    lines.append("")

    lines.append("## 📊 账户总览")
    lines.append(f"| 项目 | 数值 |")
    lines.append(f"|------|------|")
    lines.append(f"| 总资产 | {total_asset:,.0f} 元 |")
    lines.append(f"| 持仓市值 | {total_value:,.0f} 元 |")
    lines.append(f"| 可用资金 | {money_remain:,.0f} 元 |")
    lines.append(f"| 仓位 | {position_rate:.0f}% {'（正常）' if 20 <= position_rate <= 75 else '（轻仓）' if position_rate < 20 else '（重仓）'} |")
    lines.append(f"| 浮盈亏 | {total_profit:+,.0f} 元 |")
    lines.append("")

    if today_trades:
        lines.append("## 💹 今日交易复盘")
        stocks = aggregate_trades(today_trades)
        cp = {p.get("stock_code"): _to_float(p.get("current_price")) for p in items}
        lines.append(review_aggregated_trades(stocks, cp))
        lines.append("")
    else:
        lines.append("## 💹 今日交易")
        lines.append("无操作，观望为主。")
        lines.append("")

    if items:
        lines.append("## 📋 持仓逐一点评")
        for pos in items:
            name = pos.get("stock_name", "?")
            code = pos.get("stock_code", "")
            cost = _to_float(pos.get("cost_price"))
            current = _to_float(pos.get("current_price"))
            hold_days = _to_int(pos.get("hold_days"))
            profit = _to_float(pos.get("hold_profit"))
            profit_rate = _to_float(pos.get("hold_rate", 0)) * 100

            action, reason, stop_loss = _stock_verdict(cost, current, hold_days, profit_rate)
            emoji = _verdict_emoji(action)

            lines.append(f"### {emoji} {name}（{code}）**{action}**")
            lines.append("```")
            lines.append(_cost_visual(cost, current, stop_loss))
            lines.append("```")
            lines.append(f"| 项目 | 数值 |")
            lines.append(f"|------|------|")
            lines.append(f"| 现价 | {current:.2f} 元 |")
            lines.append(f"| 成本 | {cost:.2f} 元 |")
            lines.append(f"| 浮盈亏 | {profit:+,.0f} 元（{profit_rate:+.1f}%） |")
            lines.append(f"| 持股 | {hold_days} 天 |")
            lines.append(f"| 止损价 | {stop_loss:.2f} 元（跌破执行） |")
            lines.append("")
            lines.append(f"**理由：{reason}**")
            lines.append("")
    else:
        lines.append("空仓。")
        lines.append("")

    buy_count = sum(1 for t in today_trades if "买" in t.get("trade_type", ""))
    sell_count = sum(1 for t in today_trades if "卖" in t.get("trade_type", ""))

    lines.append("## ✅ 交易纪律自检（今晚填写）")
    if buy_count > 0:
        lines.append(f"- 今日买入 {buy_count} 笔，是否符合计划？  □ 是  □ 否")
    if sell_count > 0:
        lines.append(f"- 今日卖出 {sell_count} 笔，原因？  □ 止盈  □ 止损  □ 其他：_____")
    lines.append("- 是否有冲动交易（上头买/恐慌卖）？  □ 是  □ 否")
    lines.append("- 仓位是否符合计划？  □ 是  □ 否")
    lines.append("")

    lines.append("## 🎯 次日操作计划（含具体价格）")
    if items:
        for pos in items:
            name = pos.get("stock_name", "?")
            code = pos.get("stock_code", "")
            cost = _to_float(pos.get("cost_price"))
            current = _to_float(pos.get("current_price"))
            profit_rate = _to_float(pos.get("hold_rate", 0)) * 100

            if profit_rate > 15:
                target = current * 0.95
                lines.append(f"- **{name}**（{code}）**减仓**")
                lines.append(f"  现价 {current:.2f}，明日跌破 {target:.2f}（-5%）减半仓止盈")
                lines.append(f"  若继续涨至 {current * 1.05:.2f}，再卖剩1/3")
            elif profit_rate > 0:
                lines.append(f"- **{name}**（{code}）**持有**")
                lines.append(f"  止损设成本价 {cost:.2f}，跌破即卖出（保住利润）")
            else:
                key_level = cost * 0.97
                lines.append(f"- **{name}**（{code}）**止损/减仓**")
                lines.append(f"  关注 {key_level:.2f} 元支撑（成本{cost:.2f}的97%）")
                lines.append(f"  跌破 {key_level:.2f} 减仓一半；跌破 {cost * 0.95:.2f} 清仓止损")
    else:
        lines.append("空仓，建议明日继续观望。")

    lines.append("")
    lines.append("---")
    lines.append("⚠️ **免责声明**：以上为个人分析，不构成投资建议。股市有风险，盈亏自负。")
    return "\n".join(lines)


# ============ 飞书富文本格式 ============
def format_feishu_card(markdown: str) -> dict:
    """
    将 Markdown 报告转换为飞书 Interactive 消息卡片
    """
    import re
    # 简化处理：拆分为多个文本段落
    sections = []
    current_text = ""

    for line in markdown.split("\n"):
        if line.startswith("# ") and not current_text.strip():
            current_text = line.replace("# ", "**").replace("**", "") + "\n"
        elif line.startswith("## "):
            if current_text.strip():
                sections.append({"tag": "markdown", "content": current_text.strip()})
            current_text = "**" + line.replace("## ", "") + "**\n"
        elif line.startswith("### "):
            if current_text.strip():
                sections.append({"tag": "markdown", "content": current_text.strip()})
            current_text = line.replace("### ", "**") + "**\n"
        elif line.startswith("> "):
            current_text += line.replace("> ", "") + "\n"
        elif line.startswith("#### "):
            if current_text.strip():
                sections.append({"tag": "markdown", "content": current_text.strip()})
            current_text = line.replace("#### ", "") + "\n"
        elif line.startswith("- "):
            current_text += "• " + line[2:] + "\n"
        elif line.startswith("⚠️ ") or line.startswith("🔴 ") or line.startswith("🟢 ") or line.startswith("📗 "):
            current_text += line + "\n"
        elif line.startswith("|") and " | " in line:
            # 表格简化处理
            parts = [p.strip().strip("|") for p in line.split("|")]
            if all(p.replace("-", "").replace(":", "").strip() == "" for p in parts):
                continue  # 分隔线
            current_text += "  ".join(p for p in parts if p) + "\n"
        elif line.strip() == "---":
            continue
        else:
            current_text += line + "\n"

    if current_text.strip():
        sections.append({"tag": "markdown", "content": current_text.strip()})

    return {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {"tag": "plain_text", "content": "📊 持仓报告"},
                "template": "blue"
            },
            "elements": sections
        }
    }


# ============ 主入口 ============
def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="同花顺持仓定时报告生成器 v2.0")
    parser.add_argument("mode", choices=["morning", "midday", "close"], nargs="?",
                        help="报告模式: morning(早盘) / midday(午盘) / close(收盘)")
    parser.add_argument("--positions-only", action="store_true",
                        help="仅获取持仓数据")
    parser.add_argument("--feishu", action="store_true",
                        help="输出飞书富文本格式")
    parser.add_argument("--news", default=None,
                        help="新闻数据（JSON 数组格式），由调用方通过 MCP web_search 获取后传入")
    parser.add_argument("--queries", default="美股,A股政策,大宗商品,人民币",
                        help="新闻搜索关键词，逗号分隔（仅在 --news 未提供时使用）")
    args = parser.parse_args()
    if not args.mode and not args.positions_only:
        parser.error("mode is required unless --positions-only is set")

    # 解析新闻数据（由外部 MCP 工具获取后通过 --news 注入）
    news = []
    if args.news:
        try:
            news = json.loads(args.news)
        except Exception:
            print("警告: --news 参数解析失败，将跳过新闻", file=sys.stderr)

    # 统一获取持仓+交易（一次 CDP 会话）
    print(f"[{args.mode}] 正在连接同花顺...", flush=True)
    positions, trades = get_all_tzzb()
    if not positions.get("ok"):
        print(f"获取持仓失败: {positions.get('error')}", file=sys.stderr)
        sys.exit(1)

    overview, items = parse_positions(positions)
    all_trades = parse_trades(trades)
    today_trades = get_today_trades(all_trades) if all_trades else []

    if args.positions_only:
        print(json.dumps({"ok": True, "overview": overview, "items": items,
                          "today_trades": today_trades}, ensure_ascii=False, indent=2))
        return

    if args.mode == "morning":
        report = build_morning_report(overview, items, today_trades, news)
    elif args.mode == "midday":
        report = build_midday_report(overview, items, today_trades, news)
    else:
        report = build_close_report(overview, items, today_trades, all_trades)

    # 保存报告
    report_path = DATA_DIR / f"report_{args.mode}_{datetime.now().strftime('%Y%m%d')}.md"
    report_path.write_text(report, encoding="utf-8")
    print(f"报告已保存: {report_path}")

    if args.feishu:
        feishu_data = format_feishu_card(report)
        feishu_path = DATA_DIR / f"report_{args.mode}_{datetime.now().strftime('%Y%m%d')}_feishu.json"
        feishu_path.write_text(json.dumps(feishu_data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"飞书格式已保存: {feishu_path}")
    else:
        print()
        print(report)


if __name__ == "__main__":
    main()
