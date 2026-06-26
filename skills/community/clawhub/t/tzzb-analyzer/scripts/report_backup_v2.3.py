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


def build_morning_report(overview: dict, items: list, today_trades: list, news: list) -> str:
    """早盘报告（含当日交易信息）"""
    now = datetime.now()
    total_asset = _to_float(overview.get("total_asset"))
    total_value = _to_float(overview.get("total_value"))
    money_remain = _to_float(overview.get("money_remain"))
    position_rate = (total_value / total_asset * 100) if total_asset else 0

    lines = []
    lines.append(f"# 📈 早盘操作指导 {now.strftime('%m/%d %H:%M')}\n")
    lines.append("---")
    lines.append("## 📊 账户概况")
    lines.append(f"| 项目 | 数值 |")
    lines.append(f"|------|------|")
    lines.append(f"| 总资产 | {total_asset:,.0f} 元 |")
    lines.append(f"| 持仓市值 | {total_value:,.0f} 元 |")
    lines.append(f"| 可用资金 | {money_remain:,.0f} 元 |")
    lines.append(f"| 仓位 | {position_rate:.1f}% |")
    lines.append(f"| 持仓数量 | {len(items)} 只 |")
    lines.append("")

    # 今日交易（如果有）
    if today_trades:
        lines.append("## 💹 今日交易记录")
        stocks = aggregate_trades(today_trades)
        current_prices = {p.get("stock_code"): _to_float(p.get("current_price")) for p in items}
        lines.append(review_aggregated_trades(stocks, current_prices))
        lines.append("")
    else:
        lines.append("## 💹 今日交易")
        lines.append("今日暂无交易记录。\n")

    # 隔夜消息
    lines.append("## 🌍 隔夜消息面")
    if news:
        for n in news[:5]:
            lines.append(f"- **{n.get('title', '')}**")
            if n.get("summary"):
                lines.append(f"  {n['summary'][:60]}...")
    else:
        lines.append("暂无最新消息，请关注盘中动态。")
    lines.append("")

    # 大盘预判
    lines.append("## 🔮 今日大盘预判")
    if position_rate < 20:
        lines.append("当前仓位较轻，建议以观察为主，谨慎开仓，不盲目追高。")
    elif position_rate < 60:
        lines.append("仓位适中，可参与但控制节奏，重点关注持仓股动向。")
    else:
        lines.append("⚠️ 仓位较重，注意逢高适当减仓，控制风险。")
    lines.append("")

    # 个股建议
    if items:
        lines.append("## 🎯 持仓个股操作建议")
        for pos in sorted(items, key=lambda x: _to_float(x.get("hold_profit", 0)), reverse=True):
            name = pos.get("stock_name", "?")
            code = pos.get("stock_code", "")
            profit = _to_float(pos.get("hold_profit"))
            profit_rate = _to_float(pos.get("hold_rate", 0)) * 100
            cost = _to_float(pos.get("cost_price"))
            current = _to_float(pos.get("current_price"))
            hold_days = _to_int(pos.get("hold_days"))

            tag = gen_profit_tag(profit_rate)
            lines.append(f"### {name}（{code}） {tag}")
            lines.append(f"- 现价 {current:.2f} / 成本 {cost:.2f} / 浮盈 {profit:+,.0f} 元（{profit_rate:+.1f}%）")

            if profit_rate < -5:
                lines.append(f"> ⚠️ 亏损较大，设定止损线，跌破成本7%坚决止损")
            elif profit_rate > 15:
                lines.append(f"> 🔴 涨幅较大，可分批止盈")
            elif hold_days > 180:
                lines.append(f"> 📅 长线持仓，定期检视基本面")
            else:
                lines.append(f"> ✅ 正常持有，关注开盘半小时走势")
            lines.append("")
    else:
        lines.append("## 🎯 操作建议")
        lines.append("当前无持仓，建议继续观望。\n")

    lines.append("---")
    lines.append("⚠️ **免责声明**：以上分析仅供参考，不构成任何投资建议。股市有风险，投资需谨慎，盈亏自负。")

    return "\n".join(lines)


def build_midday_report(overview: dict, items: list, today_trades: list, news: list) -> str:
    """午盘报告"""
    now = datetime.now()
    total_asset = _to_float(overview.get("total_asset"))
    total_value = _to_float(overview.get("total_value"))
    money_remain = _to_float(overview.get("money_remain"))
    position_rate = (total_value / total_asset * 100) if total_asset else 0

    lines = []
    lines.append(f"# 🕐 午盘操作指导 {now.strftime('%m/%d %H:%M')}\n")
    lines.append("---")

    lines.append("## 📊 上午行情回顾")
    if items:
        total_profit = sum(_to_float(p.get("hold_profit", 0)) for p in items)
        lines.append(f"持仓整体浮盈：{total_profit:+,.0f} 元  |  仓位 {position_rate:.1f}%")
    lines.append("")

    # 今日交易
    if today_trades:
        lines.append("## 💹 今日交易记录")
        stocks = aggregate_trades(today_trades)
        current_prices = {p.get("stock_code"): _to_float(p.get("current_price")) for p in items}
        lines.append(review_aggregated_trades(stocks, current_prices))
        lines.append("")
    else:
        lines.append("## 💹 今日交易")
        lines.append("今日暂无交易记录。\n")

    # 盘中消息
    lines.append("## 📰 盘中重要消息")
    if news:
        for n in news[:4]:
            lines.append(f"- **{n.get('title', '')}**")
    else:
        lines.append("暂无最新消息。")
    lines.append("")

    # 下午建议
    lines.append("## 🎯 下午操作建议")
    if items:
        for pos in items:
            name = pos.get("stock_name", "?")
            code = pos.get("stock_code", "")
            profit_rate = _to_float(pos.get("hold_rate", 0)) * 100

            if profit_rate < -3:
                lines.append(f"- **{name}**（{code}）：亏损扩大，午后低走考虑止损")
            elif profit_rate > 10:
                lines.append(f"- **{name}**（{code}）：盈利可观，可分批止盈")
            else:
                lines.append(f"- **{name}**（{code}）：维持持有，等待机会")
    else:
        lines.append("无持仓，午后继续保持观望。")

    if position_rate > 75:
        lines.append("")
        lines.append("⚠️ **仓位提醒**：仓位较重，午后冲高适当减仓至七成以下。")

    lines.append("---")
    lines.append("⚠️ **免责声明**：以上分析仅供参考，不构成任何投资建议。股市有风险，投资需谨慎，盈亏自负。")

    return "\n".join(lines)


def build_close_report(overview: dict, items: list, today_trades: list, all_trades: list) -> str:
    """收盘复盘报告"""
    now = datetime.now()
    total_asset = _to_float(overview.get("total_asset"))
    total_value = _to_float(overview.get("total_value"))
    money_remain = _to_float(overview.get("money_remain"))
    position_rate = (total_value / total_asset * 100) if total_asset else 0
    total_unrealized = sum(_to_float(p.get("hold_profit", 0)) for p in items)

    lines = []
    lines.append(f"# 📉 收盘复盘与次日指导 {now.strftime('%m/%d')}\n")
    lines.append("---")

    # 账户日终概况
    lines.append("## 📊 账户日终概况")
    lines.append(f"| 项目 | 数值 |")
    lines.append(f"|------|------|")
    lines.append(f"| 总资产 | {total_asset:,.0f} 元 |")
    lines.append(f"| 持仓市值 | {total_value:,.0f} 元 |")
    lines.append(f"| 可用资金 | {money_remain:,.0f} 元 |")
    lines.append(f"| 仓位 | {position_rate:.1f}% |")
    lines.append(f"| 持仓盈亏 | {total_unrealized:+,.0f} 元 |")
    lines.append(f"| 持仓数量 | {len(items)} 只 |")
    lines.append("")

    # 今日交易复盘（核心新增）
    lines.append("## 💹 今日交易复盘")
    if today_trades:
        stocks = aggregate_trades(today_trades)
        current_prices = {p.get("stock_code"): _to_float(p.get("current_price")) for p in items}
        lines.append(review_aggregated_trades(stocks, current_prices))
    else:
        lines.append("今日无交易操作。")
    lines.append("")

    # 持仓逐一点评
    if items:
        lines.append("## 📋 持仓逐一点评")
        for pos in items:
            name = pos.get("stock_name", "?")
            code = pos.get("stock_code", "")
            cost = _to_float(pos.get("cost_price"))
            current = _to_float(pos.get("current_price"))
            profit = _to_float(pos.get("hold_profit"))
            profit_rate = _to_float(pos.get("hold_rate", 0)) * 100
            hold_days = _to_int(pos.get("hold_days"))
            position_rate_item = _to_float(pos.get("position_rate", 0))

            tag = gen_profit_tag(profit_rate)
            lines.append(f"### {name}（{code}） {tag}")
            lines.append(f"- 现价 **{current:.2f}** / 成本 {cost:.2f} / 浮盈 {profit:+,.0f} 元（{profit_rate:+.1f}%）")
            lines.append(f"- 持股 **{hold_days}** 天 / 仓位 {position_rate_item:.1f}%")

            if profit_rate > 10:
                lines.append(f"> 🔴 涨幅较大，注意高位回调，可分批止盈保护利润")
            elif profit_rate > 0:
                lines.append(f"> 🟢 盈利状态，设定动态止盈位")
            elif profit_rate > -5:
                lines.append(f"> 🟡 小幅亏损，耐心等待反弹")
            elif profit_rate > -15:
                lines.append(f"> 🟠 亏损较大，跌破支撑位严格执行止损")
            else:
                lines.append(f"> 🔴 亏损严重，**次日低开即考虑止损**")

            if hold_days > 365:
                lines.append(f"> 📅 持仓超1年，重新评估持有逻辑是否成立")

            lines.append("")
    else:
        lines.append("当前无持仓。\n")

    # 交易纪律自检
    lines.append("## ✅ 交易纪律自检")
    buy_count = sum(1 for t in today_trades if "买" in t.get("trade_type", ""))
    sell_count = sum(1 for t in today_trades if "卖" in t.get("trade_type", ""))

    if buy_count > 3:
        lines.append(f"- ⚠️ 买入 {buy_count} 笔，频率偏高，警惕冲动交易")
    elif buy_count > 0:
        lines.append(f"- ✅ 买入 {buy_count} 笔，操作节奏正常")
    else:
        lines.append("- 📝 今日无买入，观望为主")

    if sell_count > 0:
        lines.append(f"- 📤 卖出 {sell_count} 笔，请确认卖出理由清晰")
    lines.append("- 是否执行了止损计划？  □ 是  □ 否")
    lines.append("- 是否追涨杀跌？  □ 是  □ 否")
    lines.append("- 仓位是否符合计划？  □ 是  □ 否")
    lines.append("")

    # 风险提示
    risk_lines = []
    for pos in items:
        if _to_float(pos.get("position_rate", 0)) > 30:
            risk_lines.append(f"⚠️ {pos.get('stock_name')} 仓位过重（{_to_float(pos.get('position_rate', 0)):.1f}%）")
    if any(_to_float(p.get("hold_rate", 0)) * 100 < -15 for p in items):
        risk_lines.append("🔴 存在大幅亏损持仓，请严格执行止损")
    if position_rate > 80:
        risk_lines.append(f"⚠️ 总仓位过重（{position_rate:.1f}%），建议预留现金")

    if risk_lines:
        lines.append("## ⚠️ 风险提示")
        for r in risk_lines:
            lines.append(f"- {r}")
        lines.append("")

    # 次日操作计划
    lines.append("## 🎯 次日操作计划")
    if items:
        for pos in items:
            name = pos.get("stock_name", "?")
            code = pos.get("stock_code", "")
            cost = _to_float(pos.get("cost_price"))
            current = _to_float(pos.get("current_price"))
            profit_rate = _to_float(pos.get("hold_rate", 0)) * 100

            stop_loss = current * 0.93  # 7% 止损
            if profit_rate > 10:
                # 设定止盈位：高于成本15%部分分批卖
                target = cost * 1.15
                lines.append(f"- **{name}**（{code}）：持有，止盈位 {target:.2f}（+15%），跌破 {stop_loss:.2f} 止盈")
            elif profit_rate > 0:
                lines.append(f"- **{name}**（{code}）：持有，止损位 {stop_loss:.2f}（-7%）")
            else:
                stop_loss_key = max(cost * 0.95, current * 0.97)  # 5%或3%
                lines.append(f"- **{name}**（{code}）：关注 {stop_loss_key:.2f} 支撑，跌破坚决止损")
    else:
        lines.append("无持仓，建议明日继续观望，等待市场明朗。")

    lines.append("")
    lines.append("---")
    lines.append("⚠️ **免责声明**：以上分析仅供参考，不构成任何投资建议。股市有风险，投资需谨慎，盈亏自负。")

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
