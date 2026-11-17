#!/usr/bin/env python3
"""
研木 — 金融数据采集脚本
采集目标公司及可比公司的核心财务数据
"""
import json
import sys
import argparse
from typing import Dict, List, Any, Optional
import urllib.request

# ============ 内置财务数据库（课程演示用） ============
# 包含课程中所有可研究标的的历史财务数据和预测

FINANCIAL_DB = {
    # 宁德时代 300750.SZ
    "300750.SZ": {
        "name": "宁德时代",
        "market": "a-share",
        "shares_outstanding": 46.27,  # 亿股
        "current_price": 384.78,
        "market_cap": 17803.77,  # 亿元
        
        # 历史财务数据
        "history": {
            "2023": {"revenue": 4009, "net_income": 441, "nopat": 519, 
                     "ebit": 611, "capex": -336, "nwc_change": 80, "fcf": 592,
                     "gross_margin": 22.9, "net_margin": 11.0,
                     "roic": 18.5, "roce": 21.2},
            "2024": {"revenue": 3620, "net_income": 507, "nopat": 596,
                     "ebit": 701, "capex": -382, "nwc_change": -43, "fcf": 658,
                     "gross_margin": 24.3, "net_margin": 14.0,
                     "roic": 19.8, "roce": 22.5},
            "2025": {"revenue": 4237, "net_income": 722, "nopat": 846,
                     "ebit": 995, "capex": -450, "nwc_change": -85, "fcf": 909,
                     "gross_margin": 26.3, "net_margin": 17.0,
                     "roic": 22.1, "roce": 25.3},
        },
        
        # 分析师一致预期
        "estimates": {
            "2026E": {"revenue": 6080, "net_income": 962, "eps": 20.80, "growth": 33.2},
            "2027E": {"revenue": 7429, "net_income": 1206, "eps": 26.07, "growth": 25.4},
            "2028E": {"revenue": 8874, "net_income": 1464, "eps": 31.64, "growth": 21.4},
        },
        
        # 估值数据
        "valuation": {
            "pe_ttm": 22.4,
            "pb": 5.41,
            "ps_est": 4.2,
            "ev_ebitda": 30.0,
            "roe": 24.91,
            "debt_ratio": 61.94,
            "net_cash": 2138.57,
        },
    },
    
    # 比亚迪 002594.SZ
    "002594.SZ": {
        "name": "比亚迪",
        "market": "a-share",
        "shares_outstanding": 29.1,
        "current_price": 271.80,
        "market_cap": 7907,
        "history": {
            "2023": {"revenue": 6023, "net_income": 300, "nopat": 380,
                     "ebit": 447, "capex": -1200, "nwc_change": -200, "fcf": -520,
                     "gross_margin": 20.2, "net_margin": 5.0,
                     "roic": 8.5, "roce": 10.2},
            "2024": {"revenue": 6160, "net_income": 310, "nopat": 392,
                     "ebit": 461, "capex": -1100, "nwc_change": -50, "fcf": -220,
                     "gross_margin": 19.8, "net_margin": 5.0,
                     "roic": 7.9, "roce": 9.8},
            "2025": {"revenue": 7771, "net_income": 412, "nopat": 510,
                     "ebit": 600, "capex": -900, "nwc_change": 50, "fcf": 162,
                     "gross_margin": 20.5, "net_margin": 5.3,
                     "roic": 9.2, "roce": 11.5},
        },
        "estimates": {
            "2026E": {"revenue": 9200, "net_income": 520, "eps": 17.87, "growth": 26.2},
            "2027E": {"revenue": 10500, "net_income": 620, "eps": 21.30, "growth": 19.2},
            "2028E": {"revenue": 11800, "net_income": 720, "eps": 24.74, "growth": 16.1},
        },
        "valuation": {
            "pe_ttm": 28.7, "pb": 3.41, "ps_est": 0.98, "ev_ebitda": 20.0,
            "roe": 11.5, "debt_ratio": 62.3, "net_cash": -850,
        },
    },
    
    # 贵州茅台 600519.SH
    "600519.SH": {
        "name": "贵州茅台",
        "market": "a-share",
        "shares_outstanding": 12.56,
        "current_price": 1500.00,
        "market_cap": 18840,
        "history": {
            "2023": {"revenue": 1506, "net_income": 747, "nopat": 877,
                     "ebit": 1032, "capex": -25, "nwc_change": 30, "fcf": 725,
                     "gross_margin": 91.9, "net_margin": 49.6,
                     "roic": 30.5, "roce": 35.2},
            "2024": {"revenue": 1600, "net_income": 800, "nopat": 940,
                     "ebit": 1106, "capex": -30, "nwc_change": 20, "fcf": 770,
                     "gross_margin": 91.5, "net_margin": 50.0,
                     "roic": 29.8, "roce": 34.5},
            "2025": {"revenue": 1720, "net_income": 860, "nopat": 1010,
                     "ebit": 1188, "capex": -28, "nwc_change": 15, "fcf": 830,
                     "gross_margin": 91.8, "net_margin": 50.0,
                     "roic": 30.2, "roce": 35.0},
        },
        "estimates": {
            "2026E": {"revenue": 1850, "net_income": 920, "eps": 73.25, "growth": 7.0},
            "2027E": {"revenue": 1980, "net_income": 985, "eps": 78.42, "growth": 7.1},
            "2028E": {"revenue": 2110, "net_income": 1050, "eps": 83.60, "growth": 6.6},
        },
        "valuation": {
            "pe_ttm": 21.5, "pb": 7.8, "ps_est": 10.5, "ev_ebitda": 18.0,
            "roe": 35.0, "debt_ratio": 20.0, "net_cash": 800,
        },
    },
    
    # 腾讯 00700.HK
    "00700.HK": {
        "name": "腾讯控股",
        "market": "hk",
        "shares_outstanding": 92.5,
        "current_price": 420.00,  # HKD
        "market_cap": 38850,  # 亿HKD
        "history": {
            "2023": {"revenue": 6090, "net_income": 1577, "nopat": 1750,
                     "ebit": 2059, "capex": -450, "nwc_change": -100, "fcf": 1750,
                     "gross_margin": 48.0, "net_margin": 25.9,
                     "roic": 15.2, "roce": 18.5},
            "2024": {"revenue": 6603, "net_income": 1700, "nopat": 1887,
                     "ebit": 2220, "capex": -500, "nwc_change": -80, "fcf": 1820,
                     "gross_margin": 49.5, "net_margin": 25.7,
                     "roic": 16.1, "roce": 19.2},
            "2025": {"revenue": 7200, "net_income": 1900, "nopat": 2109,
                     "ebit": 2481, "capex": -520, "nwc_change": -90, "fcf": 1950,
                     "gross_margin": 50.2, "net_margin": 26.4,
                     "roic": 17.5, "roce": 20.8},
        },
        "estimates": {
            "2026E": {"revenue": 7900, "net_income": 2100, "eps": 22.70, "growth": 10.5},
            "2027E": {"revenue": 8600, "net_income": 2300, "eps": 24.86, "growth": 9.5},
            "2028E": {"revenue": 9300, "net_income": 2500, "eps": 27.03, "growth": 8.7},
        },
        "valuation": {
            "pe_ttm": 22.9, "pb": 5.8, "ps_est": 5.2, "ev_ebitda": 18.5,
            "roe": 25.0, "debt_ratio": 40.0, "net_cash": 1500,
        },
    },
    
    # NVIDIA
    "NVDA": {
        "name": "NVIDIA",
        "market": "us",
        "shares_outstanding": 25.0,
        "current_price": 950.00,  # USD
        "market_cap": 23750,  # 亿USD
        "history": {
            "2024": {"revenue": 1305, "net_income": 730, "nopat": 745,
                     "ebit": 760, "capex": -20, "nwc_change": 50, "fcf": 670,
                     "gross_margin": 72.0, "net_margin": 55.9,
                     "roic": 60.0, "roce": 65.0},
            "2025": {"revenue": 1500, "net_income": 850, "nopat": 867,
                     "ebit": 885, "capex": -25, "nwc_change": 60, "fcf": 780,
                     "gross_margin": 73.0, "net_margin": 56.7,
                     "roic": 62.0, "roce": 67.0},
        },
        "estimates": {
            "2026E": {"revenue": 1800, "net_income": 1000, "eps": 40.00, "growth": 17.6},
            "2027E": {"revenue": 2100, "net_income": 1150, "eps": 46.00, "growth": 15.0},
        },
        "valuation": {
            "pe_ttm": 32.5, "pb": 25.0, "ps_est": 15.8, "ev_ebitda": 28.0,
            "roe": 60.0, "debt_ratio": 25.0, "net_cash": 400,
        },
    },
}




def fetch_live_price(ticker: str, market: str) -> Optional[float]:
    """从新浪财经获取实时股价，支持A股/港股/美股"""
    ticker_code = ticker.replace(".SH","").replace(".SZ","").replace(".HK","").replace(".US","")
    
    if market == "a-share":
        if ticker_code.startswith(("600","601","603","605","688")):
            prefix = "sh"
        elif ticker_code.startswith(("000","001","002","003","300","301")):
            prefix = "sz"
        else:
            return None
        url = f"https://hq.sinajs.cn/list={prefix}{ticker_code}"
    elif market == "hk":
        url = f"https://hq.sinajs.cn/list=rt_hk{ticker_code}"
    elif market == "us":
        url = f"https://hq.sinajs.cn/list=gb_{ticker_code.lower()}"
    else:
        return None
    
    req = urllib.request.Request(url, headers={
        "Referer": "https://finance.sina.com.cn",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
    })
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            text = resp.read().decode("gbk")
        if "=" in text and '"' in text:
            data = text.split('"')[1].split(",")
            if market == "hk" and len(data) >= 7:
                p = float(data[6])
                if p > 0: return p
            elif market == "us" and len(data) >= 2:
                p = float(data[1])
                if p > 0: return p
            elif market == "a-share" and len(data) >= 4:
                p = float(data[3])
                if p > 0: return p
    except Exception:
        pass
    return None


def get_financial_data(ticker: str, comps: List[str] = None) -> Dict:
    """获取目标公司及可比公司的财务数据"""
    result = {}
    
    # 获取目标公司数据
    if ticker not in FINANCIAL_DB:
        print(f"⚠️ 股票 {ticker} 数据暂未收录", file=sys.stderr)
        return result
    
    target_data = FINANCIAL_DB[ticker].copy()
    
    # 尝试获取实时股价并覆盖硬编码价格
    live_price = fetch_live_price(ticker, target_data.get("market", "a-share"))
    if live_price:
        old_price = target_data.get("current_price", 0)
        target_data["current_price"] = live_price
        # 重新计算市值 = 总股本 × 最新股价
        shares = target_data.get("shares_outstanding", 0)
        if shares > 0:
            target_data["market_cap"] = round(live_price * shares, 2)
        # 重新计算PE(TTM)
        if "history" in target_data and target_data["history"]:
            last_year = sorted(target_data["history"].keys())[-1]
            last_eps = target_data["history"][last_year]["net_income"] / shares if shares > 0 else 0
            if last_eps > 0:
                target_data["valuation"] = dict(target_data.get("valuation", {}))
                target_data["valuation"]["pe_ttm"] = round(live_price / last_eps, 1)
        print(f"✅ 已获取实时股价: ¥{old_price} → ¥{live_price}", file=sys.stderr)
    
    result["target"] = target_data
    
    # 获取可比公司数据
    if comps:
        result["comps"] = {}
        for c in comps:
            if c in FINANCIAL_DB:
                result["comps"][c] = FINANCIAL_DB[c]
            else:
                print(f"⚠️ 可比公司 {c} 数据暂未收录", file=sys.stderr)
    
    return result


def format_financial_summary(data: Dict) -> str:
    """格式化输出财务数据摘要"""
    target = data.get("target", {})
    if not target:
        return "⚠️ 未找到相关数据"
    
    lines = [
        f"📊 **财务数据摘要 · {target['name']} ({target.get('ticker', '')})**\n",
        f"━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"📍 市场: {target.get('market', 'N/A')}",
        f"💰 当前股价: ¥{target.get('current_price', 'N/A')}",
        f"📈 市值: {target.get('market_cap', 'N/A')}亿元",
        f"📋 总股本: {target.get('shares_outstanding', 'N/A')}亿股",
        f"",
    ]
    
    # 历史财务数据
    history = target.get("history", {})
    lines.append("━━━ 历史财务数据 ━━━")
    for year, h in sorted(history.items()):
        lines.append(
            f"  **{year}** | 营收 ¥{h['revenue']}亿 | 净利 ¥{h['net_income']}亿 "
            f"| FCF ¥{h['fcf']}亿 | 毛利率 {h['gross_margin']}%"
        )
    
    # 分析师预期
    est = target.get("estimates", {})
    lines.append(f"\n━━━ 分析师一致预期 (共{target.get('num_analysts', 0)}家) ━━━")
    for year, e in sorted(est.items()):
        lines.append(f"  **{year}** | 营收 ¥{e['revenue']}亿 | 净利 ¥{e['net_income']}亿 | EPS ¥{e.get('eps', 'N/A')} | 增速 {e.get('growth', 'N/A')}%")
    
    # 估值指标
    val = target.get("valuation", {})
    lines.append(f"\n━━━ 当前估值指标 ━━━")
    lines.append(f"  PE(TTM): {val.get('pe_ttm', 'N/A')}x")
    lines.append(f"  PB: {val.get('pb', 'N/A')}x")
    lines.append(f"  ROE: {val.get('roe', 'N/A')}%")
    lines.append(f"  净现金: ¥{val.get('net_cash', 'N/A')}亿")
    
    # 可比公司
    comps = data.get("comps", {})
    if comps:
        lines.append(f"\n━━━ 可比公司数据 ━━━")
        for code, cdata in comps.items():
            v = cdata.get("valuation", {})
            lines.append(
                f"  **{cdata['name']}** ({code}): "
                f"市值 ¥{cdata.get('market_cap', 'N/A')}亿 | "
                f"PE {v.get('pe_ttm', 'N/A')}x | "
                f"ROE {v.get('roe', 'N/A')}%"
            )
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="金融数据采集")
    parser.add_argument("--ticker", "-t", required=True, help="目标公司股票代码")
    parser.add_argument("--market", "-m", default="a-share", help="市场类型")
    parser.add_argument("--comps", help="可比公司代码，逗号分隔")
    parser.add_argument("--output", choices=["json", "text"], default="text")
    args = parser.parse_args()
    
    comps_list = args.comps.split(",") if args.comps else []
    data = get_financial_data(args.ticker, comps_list)
    
    if args.output == "json":
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(format_financial_summary(data))


if __name__ == "__main__":
    main()
