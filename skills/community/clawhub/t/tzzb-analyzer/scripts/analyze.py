#!/usr/bin/env python3
"""
同花顺投资账本持仓分析器 v2.0
用法:
    python analyze.py analyze     - 生成持仓分析报告
    python analyze.py positions   - 获取持仓数据
    python analyze.py watchlist  - 获取自选股
    python analyze.py trades     - 获取交易记录
    python analyze.py status     - 检查 Chrome 连接
"""

import sys
import json
import os
import argparse
from pathlib import Path
from datetime import datetime

# ============ 路径配置 ============
SKILL_DIR = Path(__file__).parent.parent
SCRIPTS_DIR = Path(__file__).parent
MEMORY_DIR = SKILL_DIR / "memory"
DATA_DIR = SKILL_DIR / "data"
MEMORY_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

# 内置 tzzb_parser 源码路径
TZzb_PARSER_DIR = SCRIPTS_DIR / "tzzb_parser"
if str(TZzb_PARSER_DIR) not in sys.path:
    sys.path.insert(0, str(TZzb_PARSER_DIR))

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


def _yahoo_ticker(code: str, market: str) -> str:
    """同花顺代码 -> Yahoo Finance 代码"""
    code = str(code).strip()
    market = str(market).strip()
    if market in ("1", "sh", "ss", "sse"):
        return f"{code}.SS"
    elif market in ("0", "2", "sz", "szse"):
        return f"{code}.SZ"
    return f"{code}.SZ" if not code.startswith("6") else f"{code}.SS"


def _config_path(name: str) -> Path:
    return MEMORY_DIR / name


def _load_json(path: Path, default=None):
    if path.exists():
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return default if default is not None else {}


# ============ 数据获取（一次 CDP 会话）============
def _fetch_all_via_cdp():
    """一次性从同花顺获取所有数据，共用一次 Chrome 会话"""
    from main import fetch_watchlist, fetch_positions, fetch_trade_records
    from cookie_extractor import cdp_session

    result = {}
    exit_code = 0
    with cdp_session() as (context, page):
        result["watchlist"] = fetch_watchlist(context=context, page=page)
        if not result["watchlist"].get("ok"):
            exit_code = 1
        result["positions"] = fetch_positions(context=context, page=page)
        if not result["positions"].get("ok"):
            exit_code = 1
        result["trades"] = fetch_trade_records(context=context, page=page)
        if not result["trades"].get("ok"):
            exit_code = 1
    return result, exit_code


def fetch_positions_raw():
    from main import fetch_positions
    from cookie_extractor import cdp_session
    with cdp_session() as (context, page):
        return fetch_positions(context=context, page=page)


def check_status():
    try:
        import urllib.request
        resp = urllib.request.urlopen("http://127.0.0.1:9222/json", timeout=5)
        tabs = json.loads(resp.read())
        return {"ok": True, "tabs": len(tabs), "details": tabs}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ============ 行情获取 ============
def fetch_yahoo_quotes(tickers: list[str]) -> dict[str, dict]:
    """预留接口，暂未使用（tzzb 已提供现价，无需额外获取）"""
    return {}


# ============ 板块识别 ============
def _identify_sector(stock_name: str, stock_code: str) -> str:
    """根据股票名称识别所属行业板块"""
    name = stock_name
    code = str(stock_code)

    sector_map = {
        "医药": ["恒瑞", "药明", "迈瑞", "乐普", "联影", "迪安", "贝瑞", "华大基因", "创新医疗",
                 "东诚药业", "沃华医药", "仁和药业", "万邦德", "华特达因", "西藏药业", "药捷安康",
                 "王子新材", "联影医疗", "乐普医疗"],
        "农牧渔": ["牧原", "圣农", "立华", "天康", "大北农", "新希望", "民和", "隆平高科", "万向德农",
                   "双塔食品", "智慧农业", "国投丰乐", "桂发祥"],
        "新能源/光伏": ["阳光电源", "隆基绿能", "晶澳科技", "特变电工", "TCL中环", "科士达", "巨星科技",
                       "永鼎股份"],
        "半导体/芯片": ["兆易创新", "通富微电", "士兰微", "康强电子", "上海贝岭", "博通集成", "睿能科技"],
        "消费电子": ["立讯精密", "歌尔股份", "漫步者", "京东方A", "TCL科技", "欧菲光", "海信视像",
                    "安洁科技", "华映科技", "凯盛新能", "彩虹股份", "三力士", "劲嘉股份"],
        "AI/软件": ["科大讯飞", "中国软件", "电科数字", "大智慧", "东方财富", "漫步者", "共达电声",
                   "奥拓电子", "分众传媒", "人民网", "国脉文化"],
        "通信": ["中兴通讯", "海能达", "通宇通讯", "三维通信", "东信和平", "闻泰科技", "华胜天成"],
        "新能源汽车": ["比亚迪", "长安汽车", "北汽蓝谷", "宇通客车", "中通客车", "香山股份", "科达利",
                      "杰克科技", "小康股份"],
        "金融": ["招商银行", "平安银行", "中信证券", "华泰证券", "中信建投", "天风证券", "中原证券",
                "华鑫股份", "越秀资本", "太平洋", "湘财股份", "华创云信"],
        "房地产/基建": ["万科A", "滨江集团", "荣盛发展", "合肥城建", "浙江交科", "宁波港", "上港集团",
                       "西部建设", "中储股份", "浙江建投", "沙河股份"],
        "军工/卫星": ["中国卫星", "中国卫通", "中船科技", "中国长城", "大唐电信", "特力A", "全柴动力"],
        "稀土/有色": ["中国稀土", "中稀有色", "宝钛股份", "贵研铂业", "四川金顶", "丰元股份", "雄韬股份",
                     "露笑科技", "三维化学", "联化科技", "密尔克卫", "华友钴业", "国风新材", "新奥股份"],
        "电力/能源": ["中国核电", "西昌电力", "绿色动力", "江苏新能", "宝丰能源"],
        "医药ETF": ["医疗ETF", "医药ETF", "恒生医药", "创新药ETF"],
        "港股科技": ["恒生科技", "小米", "阿里健康", "微创医疗", "阿里巴巴", "腾讯"],
        "其他": [],
    }

    for sector, keywords in sector_map.items():
        for kw in keywords:
            if kw in name:
                return sector
    return "综合"


# ============ 持仓分析 ============
def analyze_positions(positions_data: dict, config: dict = None) -> dict:
    """生成持仓分析报告"""
    config = config or {}
    data = positions_data.get("data", {})
    overview = data.get("overview", {})
    items = data.get("items", [])

    if not items:
        return {
            "ok": True,
            "report": {
                "overview": _build_overview(overview, []),
                "positions": [],
                "sector_distribution": [],
                "risk_alerts": ["当前无持仓"],
                "suggestions": ["暂无持仓，建议观望"],
                "summary": "当前无持仓",
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            },
        }

    # 获取实时行情
    tickers = []
    for pos in items:
        code = pos.get("stock_code", "")
        market = pos.get("market", "")
        if code:
            tickers.append(_yahoo_ticker(code, market))

    quotes = fetch_yahoo_quotes(tickers) if tickers else {}

    # 解析每只持仓
    analyzed = []
    total_cost = 0.0
    total_value = 0.0
    total_profit = 0.0
    sector_value = {}

    for pos in items:
        code = str(pos.get("stock_code", ""))
        market = str(pos.get("market", ""))
        ticker = _yahoo_ticker(code, market)
        quote = quotes.get(ticker, {})

        cost_price = _to_float(pos.get("cost_price"))
        hold_count = _to_int(pos.get("hold_count"))
        market_value = _to_float(pos.get("market_value"))
        hold_profit = _to_float(pos.get("hold_profit"))
        position_rate = _to_float(pos.get("position_rate"))
        hold_days = _to_int(pos.get("hold_days"))
        current_price = _to_float(pos.get("current_price"))

        # 用 Yahoo 行情补充
        if quote.get("price") and quote["price"] > 0:
            current_price = quote["price"]
            market_value = current_price * hold_count
            if cost_price:
                hold_profit = (current_price - cost_price) * hold_count

        profit_pct = (current_price - cost_price) / cost_price * 100 if cost_price else 0
        cost_total = cost_price * hold_count
        total_cost += cost_total
        total_value += market_value
        total_profit += hold_profit

        sector = _identify_sector(pos.get("stock_name", ""), code)
        if sector not in sector_value:
            sector_value[sector] = 0.0
        sector_value[sector] += market_value

        analyzed.append({
            "stock_code": code,
            "stock_name": pos.get("stock_name", "?"),
            "ticker": ticker,
            "hold_count": hold_count,
            "cost_price": round(cost_price, 3),
            "current_price": round(current_price, 3),
            "market_value": round(market_value, 2),
            "hold_profit": round(hold_profit, 2),
            "profit_pct": round(profit_pct, 2),
            "hold_days": hold_days,
            "today_change_pct": 0,
            "position_rate": round(position_rate, 2),
            "sector": sector,
        })

    # 排序
    sort_by = config.get("report", {}).get("sort_by", "profit_pct")
    if sort_by == "market_value":
        analyzed.sort(key=lambda x: x["market_value"], reverse=True)
    else:
        analyzed.sort(key=lambda x: x["profit_pct"])

    total_asset = _to_float(overview.get("total_asset"))
    money_remain = _to_float(overview.get("money_remain"))
    position_rate_pct = (total_value / total_asset * 100) if total_asset else 0

    # 板块分布
    sector_dist = [
        {"sector": s, "value": round(v, 2), "pct": round(v / total_value * 100, 1) if total_value else 0}
        for s, v in sorted(sector_value.items(), key=lambda x: -x[1])
    ]

    # 风险提示
    risk_alerts = []
    for p in analyzed:
        if p["position_rate"] > 30:
            risk_alerts.append(
                f"⚠️ {p['stock_name']}（{p['stock_code']}）仓位过重，占总资产 {p['position_rate']:.1f}%"
            )
        if p["profit_pct"] < -20:
            risk_alerts.append(
                f"🔴 {p['stock_name']}（{p['stock_code']}）亏损达 {p['profit_pct']:.1f}%，注意止损"
            )
        if p["hold_days"] > 365:
            risk_alerts.append(
                f"📅 {p['stock_name']}（{p['stock_code']}）持仓 {p['hold_days']} 天，建议重新评估"
            )

    # 优化建议
    suggestions = []
    if position_rate_pct > 80:
        suggestions.append(f"当前仓位较重（{position_rate_pct:.1f}%），建议预留现金应对波动")
    loss_count = sum(1 for p in analyzed if p["hold_profit"] < 0)
    if loss_count > len(analyzed) * 0.5 and len(analyzed) > 1:
        suggestions.append(f"亏损股占比过高（{loss_count}/{len(analyzed)}），建议精简弱势股")
    long_hold = sum(1 for p in analyzed if p["hold_days"] > 180)
    if long_hold > 0:
        suggestions.append(f"存在 {long_hold} 只持仓超半年的股票，注意定期检视")
    if len(analyzed) >= 3:
        max_pos = max(analyzed, key=lambda x: x["position_rate"])
        if max_pos["position_rate"] > 40:
            suggestions.append(f"最大持仓 {max_pos['stock_name']} 占比 {max_pos['position_rate']:.1f}%，集中度高")

    worst = min(analyzed, key=lambda x: x["profit_pct"])
    best = max(analyzed, key=lambda x: x["profit_pct"])
    suggestions.append(
        f"本月最佳：{best['stock_name']}（{best['profit_pct']:+.1f}%）最差：{worst['stock_name']}（{worst['profit_pct']:+.1f}%）"
    )

    profit_sign_str = "盈利" if total_profit >= 0 else "亏损"
    profit_rate_fmt = total_profit/total_cost*100 if total_cost else 0
    summary = (
        f"总资产 {total_asset:,.2f} 元，持仓市值 {total_value:,.2f} 元（{position_rate_pct:.1f}% 仓位），"
        f"可用资金 {money_remain:,.2f} 元，持有 {len(analyzed)} 只股票。"
        f"整体{profit_sign_str} {abs(total_profit):,.2f} 元（{profit_rate_fmt:+.2f}%）。"
    )

    report = {
        "overview": {
            "total_asset": round(total_asset, 2),
            "total_value": round(total_value, 2),
            "money_remain": round(money_remain, 2),
            "position_rate": round(position_rate_pct, 2),
            "total_profit": round(total_profit, 2),
            "profit_rate": round((total_profit / total_cost * 100) if total_cost else 0, 2),
            "stock_count": len(analyzed),
        },
        "positions": analyzed,
        "sector_distribution": sector_dist,
        "risk_alerts": risk_alerts,
        "suggestions": suggestions,
        "summary": summary,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    return {"ok": True, "report": report}


def _build_overview(overview: dict, items: list) -> dict:
    total_asset = _to_float(overview.get("total_asset"))
    total_value = _to_float(overview.get("total_value"))
    money_remain = _to_float(overview.get("money_remain"))
    position_rate = _to_float(overview.get("position_rate")) * 100 if overview.get("position_rate") else 0
    return {
        "total_asset": round(total_asset, 2),
        "total_value": round(total_value, 2),
        "money_remain": round(money_remain, 2),
        "position_rate": round(position_rate, 2),
        "total_profit": 0,
        "profit_rate": 0,
        "stock_count": len(items),
    }


# ============ 报告格式化 ============
def format_report(report: dict) -> str:
    lines = []
    ov = report.get("overview", {})

    lines.append("=" * 52)
    lines.append(f"   同花顺持仓分析报告  {report.get('generated_at', '')}")
    lines.append("=" * 52)

    lines.append("\n📊 账户概览")
    lines.append(f"   总资产    {ov.get('total_asset', 0):>12,.2f}  元")
    lines.append(f"   持仓市值  {ov.get('total_value', 0):>12,.2f}  元")
    lines.append(f"   可用资金  {ov.get('money_remain', 0):>12,.2f}  元")
    lines.append(f"   仓位水平  {ov.get('position_rate', 0):>12.1f}  %")
    profit = ov.get("total_profit", 0)
    profit_rate = ov.get("profit_rate", 0)
    p_sign = "+" if profit >= 0 else ""
    lines.append(f"   整体盈亏  {p_sign}{profit:>11,.2f}  元  ({p_sign}{profit_rate:.2f}%)")
    lines.append(f"   股票数量  {ov.get('stock_count', 0):>12}  只")

    positions = report.get("positions", [])
    if positions:
        lines.append("\n📋 持仓明细（按收益率排序）")
        hdr = f"{'名称':<8} {'代码':<8} {'持仓':>6} {'成本':>8} {'现价':>8} {'市值':>10} {'盈亏':>10} {'收益率':>8} {'持股天':>6}"
        lines.append(hdr)
        lines.append("-" * len(hdr))
        for p in positions:
            name = p.get("stock_name", "?")[:8]
            code = p.get("stock_code", "")
            cnt = p.get("hold_count", 0)
            cost = p.get("cost_price", 0)
            price = p.get("current_price", 0)
            mv = p.get("market_value", 0)
            pf = p.get("hold_profit", 0)
            pct = p.get("profit_pct", 0)
            days = p.get("hold_days", 0)
            s_profit = "+" if pf >= 0 else ""
            s_pct = "+" if pct >= 0 else ""
            lines.append(
                f"{name:<8} {code:<8} {cnt:>6} {cost:>8.2f} {price:>8.2f} "
                f"{mv:>10,.0f} {s_profit}{abs(pf):>9,.0f} {s_pct}{abs(pct):>5.1f}%  {days:>5}"
            )

    sectors = report.get("sector_distribution", [])
    if sectors:
        lines.append("\n🏭 板块分布")
        for s in sectors:
            lines.append(f"   {s['sector']:<14} {s['value']:>10,.0f} 元  {s['pct']:>5.1f}%")

    alerts = report.get("risk_alerts", [])
    if alerts:
        lines.append("\n⚠️ 风险提示")
        for a in alerts:
            lines.append(f"   {a}")

    suggestions = report.get("suggestions", [])
    if suggestions:
        lines.append("\n💡 优化建议")
        for s in suggestions:
            lines.append(f"   • {s}")

    lines.append(f"\n📝 {report.get('summary', '')}")
    lines.append("\n" + "=" * 52)
    lines.append("   仅供参考，不构成投资建议")
    lines.append("=" * 52)
    return "\n".join(lines)


# ============ 主函数 ============
def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="同花顺投资账本持仓分析器 v2.0")
    parser.add_argument("cmd", choices=["status", "positions", "watchlist", "trades", "analyze", "monitor"],
                        help="命令")
    args = parser.parse_args()

    if args.cmd == "status":
        result = check_status()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.cmd == "positions":
        print("正在连接同花顺投资账本...", flush=True)
        raw = fetch_positions_raw()
        out = {"type": "positions", "positions": raw}
        print(json.dumps(out, ensure_ascii=False, indent=2))
        (DATA_DIR / "positions.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        return

    if args.cmd == "watchlist":
        from main import fetch_watchlist
        from cookie_extractor import cdp_session
        print("正在连接同花顺投资账本...", flush=True)
        with cdp_session() as (context, page):
            raw = fetch_watchlist(context=context, page=page)
        out = {"type": "watchlist", "watchlist": raw}
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    if args.cmd == "trades":
        from main import fetch_trade_records
        from cookie_extractor import cdp_session
        print("正在连接同花顺投资账本...", flush=True)
        with cdp_session() as (context, page):
            raw = fetch_trade_records(context=context, page=page)
        out = {"type": "trades", "trades": raw}
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    if args.cmd == "monitor":
        from scripts.monitor import run_monitor
        run_monitor()
        return

    if args.cmd == "analyze":
        print("正在连接同花顺投资账本...", flush=True)
        raw, exit_code = _fetch_all_via_cdp()
        if exit_code != 0:
            print("获取持仓失败，请确认已登录同花顺投资账本", file=sys.stderr)
            sys.exit(1)

        positions = raw.get("positions", {})
        if not positions.get("ok"):
            print(f"获取持仓失败: {positions.get('error')}", file=sys.stderr)
            sys.exit(1)

        print("正在获取市场行情并分析...", flush=True)
        config = _load_json(_config_path("positions_config.json"))
        analysis = analyze_positions(positions, config)
        report = analysis["report"]

        # 保存
        (DATA_DIR / "analysis_report.json").write_text(
            json.dumps(analysis, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        (DATA_DIR / "positions.json").write_text(
            json.dumps(raw.get("positions", {}), ensure_ascii=False, indent=2), encoding="utf-8"
        )

        print(format_report(report))


if __name__ == "__main__":
    main()
