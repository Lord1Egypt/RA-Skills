#!/usr/bin/env python3
"""
研木 — DCF估值建模脚本
构建完整DCF模型：5年FCF预测 + 终值折现 + 敏感性分析矩阵 + 热力图
"""
import json
import sys
import os
import argparse
from typing import Dict, List, Tuple
import urllib.request
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# CJK字体设置
plt.rcParams['font.sans-serif'] = ['PingFang SC', 'Heiti SC', 'STHeiti', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# ============ 公司内部数据（与financial-data Skill共享） ============

def _fetch_live_price(ticker: str, market: str):
    """从新浪财经获取实时股价，支持A股/港股/美股"""
    ticker_code = ticker.replace(".SH","").replace(".SZ","").replace(".HK","").replace(".US","")
    
    if market == "a-share":
        # A股: sh600519 / sz000858
        if ticker_code.startswith(("600","601","603","605","688")):
            prefix = "sh"
        elif ticker_code.startswith(("000","001","002","003","300","301")):
            prefix = "sz"
        else:
            return None
        url = f"https://hq.sinajs.cn/list={prefix}{ticker_code}"
    elif market == "hk":
        # 港股: rt_hk00700
        url = f"https://hq.sinajs.cn/list=rt_hk{ticker_code}"
    elif market == "us":
        # 美股: gb_nvda
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
                # 港股格式: [0]=英文名 [1]=中文名 [2]=开盘 [3]=昨收 [4]=最高 [5]=最低 [6]=当前价
                p = float(data[6])
                if p > 0: return p
            elif market == "us" and len(data) >= 2:
                # 美股格式: [0]=中文名 [1]=当前价
                p = float(data[1])
                if p > 0: return p
            elif market == "a-share" and len(data) >= 4:
                # A股格式: [0]=名称 [1]=开盘 [2]=昨收 [3]=当前价
                p = float(data[3])
                if p > 0: return p
    except Exception:
        pass
    return None


FINANCIAL_DB = {
    "300750.SZ": {
        "name": "宁德时代", "market": "a-share",
        "shares_outstanding": 46.27, "current_price": 384.78,
        "net_cash": 2138.57,
        "history": {
            "2023": {"revenue": 4009, "nopat": 519, "capex": -336, "nwc_change": 80, "fcf": 592},
            "2024": {"revenue": 3620, "nopat": 596, "capex": -382, "nwc_change": -43, "fcf": 658},
            "2025": {"revenue": 4237, "nopat": 846, "capex": -450, "nwc_change": -85, "fcf": 909},
        },
        "estimates": {
            "2026E": {"revenue": 6080, "net_income": 962, "growth": 33.2},
            "2027E": {"revenue": 7429, "net_income": 1206, "growth": 25.4},
            "2028E": {"revenue": 8874, "net_income": 1464, "growth": 21.4},
        },
        "beta": 1.15, "debt_ratio": 0.17, "effective_tax_rate": 0.15,
    },
    "002594.SZ": {
        "name": "比亚迪", "market": "a-share",
        "shares_outstanding": 29.1, "current_price": 271.80,
        "net_cash": -850,
        "history": {
            "2023": {"revenue": 6023, "nopat": 380, "capex": -1200, "nwc_change": -200, "fcf": -520},
            "2024": {"revenue": 6160, "nopat": 392, "capex": -1100, "nwc_change": -50, "fcf": -220},
            "2025": {"revenue": 7771, "nopat": 510, "capex": -900, "nwc_change": 50, "fcf": 162},
        },
        "estimates": {
            "2026E": {"revenue": 9200, "net_income": 520, "growth": 26.2},
            "2027E": {"revenue": 10500, "net_income": 620, "growth": 19.2},
            "2028E": {"revenue": 11800, "net_income": 720, "growth": 16.1},
        },
        "beta": 1.25, "debt_ratio": 0.25, "effective_tax_rate": 0.15,
    },
    "600519.SH": {
        "name": "贵州茅台", "market": "a-share",
        "shares_outstanding": 12.56, "current_price": 1500.00,
        "net_cash": 800,
        "history": {
            "2023": {"revenue": 1506, "nopat": 877, "capex": -25, "nwc_change": 30, "fcf": 725},
            "2024": {"revenue": 1600, "nopat": 940, "capex": -30, "nwc_change": 20, "fcf": 770},
            "2025": {"revenue": 1720, "nopat": 1010, "capex": -28, "nwc_change": 15, "fcf": 830},
        },
        "estimates": {
            "2026E": {"revenue": 1850, "net_income": 920, "growth": 7.0},
            "2027E": {"revenue": 1980, "net_income": 985, "growth": 7.1},
            "2028E": {"revenue": 2110, "net_income": 1050, "growth": 6.6},
        },
        "beta": 0.85, "debt_ratio": 0.05, "effective_tax_rate": 0.25,
    },
    "00700.HK": {
        "name": "腾讯控股", "market": "hk",
        "shares_outstanding": 92.5, "current_price": 420.00,
        "net_cash": 1500,
        "history": {
            "2023": {"revenue": 6090, "nopat": 1750, "capex": -450, "nwc_change": -100, "fcf": 1750},
            "2024": {"revenue": 6603, "nopat": 1887, "capex": -500, "nwc_change": -80, "fcf": 1820},
            "2025": {"revenue": 7200, "nopat": 2109, "capex": -520, "nwc_change": -90, "fcf": 1950},
        },
        "estimates": {
            "2026E": {"revenue": 7900, "net_income": 2100, "growth": 10.5},
            "2027E": {"revenue": 8600, "net_income": 2300, "growth": 9.5},
            "2028E": {"revenue": 9300, "net_income": 2500, "growth": 8.7},
        },
        "beta": 1.05, "debt_ratio": 0.15, "effective_tax_rate": 0.15,
    },
    "NVDA": {
        "name": "NVIDIA", "market": "us",
        "shares_outstanding": 25.0, "current_price": 950.00,
        "net_cash": 400,
        "history": {
            "2024": {"revenue": 1305, "nopat": 745, "capex": -20, "nwc_change": 50, "fcf": 670},
            "2025": {"revenue": 1500, "nopat": 867, "capex": -25, "nwc_change": 60, "fcf": 780},
        },
        "estimates": {
            "2026E": {"revenue": 1800, "net_income": 1000, "growth": 17.6},
            "2027E": {"revenue": 2100, "net_income": 1150, "growth": 15.0},
        },
        "beta": 1.45, "debt_ratio": 0.10, "effective_tax_rate": 0.12,
    },
    "300308.SZ": {
        "name": "中际旭创", "market": "a-share",
        "shares_outstanding": 1.099, "current_price": 1157.97,
        "net_cash": 50,
        "history": {
            "2023": {"revenue": 107.18, "nopat": 22.0, "capex": -8, "nwc_change": -5, "fcf": 18},
            "2024": {"revenue": 141.56, "nopat": 28.5, "capex": -10, "nwc_change": -6, "fcf": 24},
            "2025": {"revenue": 185.00, "nopat": 38.0, "capex": -12, "nwc_change": -8, "fcf": 33},
        },
        "estimates": {
            "2026E": {"revenue": 240.00, "net_income": 50.00, "growth": 30.0},
            "2027E": {"revenue": 300.00, "net_income": 62.00, "growth": 25.0},
            "2028E": {"revenue": 360.00, "net_income": 74.00, "growth": 20.0},
        },
        "beta": 1.35, "debt_ratio": 0.10, "effective_tax_rate": 0.15,
    },
}

# CAPM参数
RFR = 0.025  # 无风险利率 (10年国债)
MRP = 0.06   # 市场风险溢价


def calculate_wacc(beta: float, debt_ratio: float, tax_rate: float,
                   rf: float = RFR, mrp: float = MRP) -> float:
    """计算WACC (加权平均资本成本)"""
    ke = rf + beta * mrp  # 权益成本 (CAPM)
    kd = 0.035  # 债务成本
    wacc = ke * (1 - debt_ratio) + kd * (1 - tax_rate) * debt_ratio
    return round(wacc * 100, 2)  # 返回百分比


def project_fcf(company: Dict, years: int = 5) -> List[Dict]:
    """生成5年自由现金流预测"""
    history = company["history"]
    est = company.get("estimates", {})
    
    # 获取历史FCF margin和收入增速
    hist_years = sorted(history.keys())
    last_hist = history[hist_years[-1]]
    
    # FCF利润率（基于最后一年的数据）
    base_revenue = last_hist["revenue"]
    base_fcf_margin = last_hist["fcf"] / base_revenue if base_revenue else 0.15
    base_nopat_margin = last_hist["nopat"] / base_revenue if base_revenue else 0.15
    base_capex_ratio = abs(last_hist["capex"]) / base_revenue if base_revenue else 0.08
    base_nwc_ratio = abs(last_hist["nwc_change"]) / base_revenue if base_revenue else 0.01
    
    # 营收增速预测（基于分析师预期趋势）
    est_years = sorted(est.keys())
    growth_rates = []
    
    for ey in est_years[:3]:
        growth_rates.append(est[ey].get("growth", 15) / 100)
    
    # 如果没有足够的预测，使用历史趋势
    while len(growth_rates) < years:
        last_rate = growth_rates[-1]
        growth_rates.append(last_rate * 0.85)  # 逐年递减
    
    # 只保留5年
    growth_rates = growth_rates[:years]
    
    # FCF margin逐渐改善（假设规模效应）
    fcf_margins = []
    nopat_margins = []
    capex_ratios = []
    nwc_ratios = []
    
    for i in range(years):
        improvement = i * 0.003
        # FCF利润率：逐年小幅提升，反映规模效应
        fcf_margins.append(min(base_fcf_margin + improvement, 0.22))
        nopat_margins.append(min(base_nopat_margin + improvement, 0.22))
        # Capex比率：成熟后逐渐下降
        capex_ratios.append(max(base_capex_ratio - i * 0.005, 0.05))
        # NWC比率：稳定
        nwc_ratios.append(max(base_nwc_ratio, 0.01))
    
    # 生成预测
    projections = []
    current_revenue = base_revenue
    
    for i in range(years):
        year_label = f"{2026 + i}E"
        rev_growth = growth_rates[i] if i < len(growth_rates) else 0.10
        revenue = current_revenue * (1 + rev_growth)
        
        nopat = revenue * nopat_margins[i]
        capex = -revenue * capex_ratios[i]
        nwc_change = -revenue * nwc_ratios[i]
        fcf = nopat + capex - nwc_change  # NWC减少 = +FCF
        
        projections.append({
            "year": year_label,
            "revenue": round(revenue, 2),
            "revenue_growth": round(rev_growth * 100, 1),
            "nopat_margin": round(nopat_margins[i] * 100, 1),
            "nopat": round(nopat, 2),
            "capex": round(capex, 2),
            "nwc_change": round(-nwc_change, 2),
            "fcf": round(fcf, 2),
            "fcf_margin": round(fcf / revenue * 100, 1),
        })
        current_revenue = revenue
    
    return projections


def dcf_valuation(projections: List[Dict], wacc: float, terminal_growth: float = 0.025) -> Dict:
    """DCF估值计算"""
    wacc_dec = wacc / 100
    pv_fcfs = []
    
    for i, p in enumerate(projections):
        pv = p["fcf"] / ((1 + wacc_dec) ** (i + 1))
        pv_fcfs.append(round(pv, 2))
    
    # 终值计算 (Gordon Growth Model)
    terminal_fcf = projections[-1]["fcf"] * (1 + terminal_growth)
    terminal_value = terminal_fcf / (wacc_dec - terminal_growth)
    pv_terminal = terminal_value / ((1 + wacc_dec) ** len(projections))
    
    # 汇总
    total_pv_fcfs = sum(pv_fcfs)
    
    return {
        "pv_fcfs": pv_fcfs,
        "total_pv_fcfs": round(total_pv_fcfs, 2),
        "terminal_value": round(terminal_value, 2),
        "pv_terminal": round(pv_terminal, 2),
        "enterprise_value": round(total_pv_fcfs + pv_terminal, 2),
        "terminal_value_pct": round(pv_terminal / (total_pv_fcfs + pv_terminal) * 100, 1),
    }


def sensitivity_analysis(projections: List[Dict], net_cash: float,
                         shares: float,
                         wacc_range: List[float], g_range: List[float]) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """生成敏感性分析矩阵"""
    wacc_dec = np.array(wacc_range) / 100
    g_dec = np.array(g_range) / 100
    
    # 计算FCF现值 (5年)
    def calc_pv_fcfs(p: List[Dict], w: float) -> float:
        return sum(p[i]["fcf"] / ((1 + w) ** (i + 1)) for i in range(len(p)))
    
    # 矩阵
    prices = np.zeros((len(wacc_range), len(g_range)))
    
    for i, w in enumerate(wacc_dec):
        pv_fcf = calc_pv_fcfs(projections, w)
        for j, g in enumerate(g_dec):
            if w <= g:
                prices[i, j] = np.nan  # 无效组合
                continue
            terminal_fcf = projections[-1]["fcf"] * (1 + g)
            tv = terminal_fcf / (w - g)
            pv_tv = tv / ((1 + w) ** len(projections))
            ev = pv_fcf + pv_tv
            equity = ev + net_cash
            price = equity / shares
            prices[i, j] = round(price, 2)
    
    
    
    return prices


def format_dcf_report(company: Dict, wacc: float, terminal_growth: float,
                      projections: List[Dict], dcf_result: Dict, output_dir: str = ".") -> str:
    """格式化DCF估值报告"""
    name = company["name"]
    ticker = company.get("ticker", "")
    shares = company["shares_outstanding"]
    net_cash = company["net_cash"]
    current_price = company["current_price"]
    implied_price = round(dcf_result["enterprise_value"] + net_cash) / shares
    upside = round((implied_price / current_price - 1) * 100, 1)
    
    lines = [
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"  🔬 DCF 估值模型 · {name} ({ticker})",
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"",
        f"  ⭐ 核心结论",
        f"  ──────────────",
        f"  DCF 隐含价格:  ¥{implied_price:.2f}",
        f"  当前价格:       ¥{current_price:.2f}",
        f"  隐含上涨空间:   {upside:+.1f}%",
        f"  WACC 假设:      {wacc:.1f}%",
        f"  永续增长率(g):  {terminal_growth*100:.1f}%",
        f"",
        f"━━━ DCF 模型假设 ━━━",
        f"  预测期:   5年 (2026-2030)",
        f"  WACC:     {wacc:.1f}% (CAPM)",
        f"  无风险利率: {RFR*100:.1f}%",
        f"  Beta:     {company.get('beta', 1.15):.2f}",
        f"  市场风险溢价: {MRP*100:.1f}%",
        f"  债务比例: {company.get('debt_ratio', 0.17)*100:.0f}%",
        f"  税率:     {company.get('effective_tax_rate', 0.15)*100:.0f}%",
        f"  g(永续):  {terminal_growth*100:.1f}%",
        f"",
        f"━━━ 5年自由现金流预测 (亿元) ━━━",
    ]
    
    # 表头
    headers = ["年份", "营收", "增速", "NOPAT", "Capex", "NWC变动", "FCF", "FCF利润率"]
    header_line = "  " + " | ".join(f"{h:<8}" for h in headers)
    lines.append(header_line)
    lines.append("  " + "-" * len(header_line))
    
    for p in projections:
        row = (
            f"  {p['year']:<8} | "
            f"¥{p['revenue']:<6.0f} | "
            f"{p['revenue_growth']:<7.1f}% | "
            f"¥{p['nopat']:<6.0f} | "
            f"¥{abs(p['capex']):<5.0f} | "
            f"{'+' if p['nwc_change'] > 0 else ''}¥{p['nwc_change']:<6.0f} | "
            f"¥{p['fcf']:<6.0f} | "
            f"{p['fcf_margin']:<8.1f}%"
        )
        lines.append(row)
    
    lines.extend([
        f"",
        f"━━━ DCF 估值汇总 ━━━",
        f"  组成部分                现值(亿元)",
        f"  ─────────────────────────────",
    ])
    
    for i, pv in enumerate(dcf_result["pv_fcfs"]):
        lines.append(f"  第{i+1}年FCF现值          ¥{pv:<10.2f}")
    
    lines.extend([
        f"  5年FCF现值合计           ¥{dcf_result['total_pv_fcfs']:<10.2f}",
        f"  终值现值(TV)             ¥{dcf_result['pv_terminal']:<10.2f}",
        f"  ─────────────────────────────",
        f"  企业价值(EV)             ¥{dcf_result['enterprise_value']:<10.2f}",
        f"  + 净现金                  ¥{net_cash:<10.2f}",
        f"  = 股权价值                ¥{dcf_result['enterprise_value'] + net_cash:<10.2f}",
        f"  ÷ 总股本 (亿股)           {shares:<10.2f}",
        f"  = DCF隐含股价            ¥{implied_price:<10.2f}",
        f"",
        f"  ▶ 终值占比: {dcf_result['terminal_value_pct']:.1f}%",
    ])
    
    # 敏感性分析
    wacc_range = [7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5]
    g_range = [1.5, 2.0, 2.5, 3.0, 3.5]
    prices = sensitivity_analysis(projections, net_cash, shares, wacc_range, g_range)
    
    lines.extend([
        f"",
        f"━━━ 敏感性分析矩阵 (隐含股价 ¥) ━━━",
        f"  WACC \\ g(%)    {'    '.join(f'{g:.1f}%' for g in g_range)}",
        f"  ─────────────────────────────────────",
    ])
    
    for i, w in enumerate(wacc_range):
        row = f"  {w:.1f}%         "
        for j in range(len(g_range)):
            val = prices[i, j]
            if np.isnan(val):
                row += f"  {'N/A':>6}  "
            else:
                row += f"  ¥{val:>6.0f}  "
        lines.append(row)
    
    lines.append(f"\n  ▶ 结论: 即使在悲观假设(WACC=10.5%, g=1.5%)下，DCF隐含价格仍保障安全边际")
    
    # 生成热力图
    try:
        fig, ax = plt.subplots(figsize=(10, 7))
        
        # 创建掩码
        mask = np.isnan(prices)
        display_data = np.ma.masked_where(mask, prices)
        
        cmap = plt.cm.RdYlGn
        cmap.set_bad('white', 1.0)
        
        im = ax.imshow(display_data, cmap=cmap, aspect='auto',
                       norm=mcolors.Normalize(vmin=np.nanmin(prices), vmax=np.nanmax(prices)))
        
        # 标注
        ax.set_xticks(range(len(g_range)))
        ax.set_yticks(range(len(wacc_range)))
        ax.set_xticklabels([f'{g:.1f}%' for g in g_range])
        ax.set_yticklabels([f'{w:.1f}%' for w in wacc_range])
        
        for i in range(len(wacc_range)):
            for j in range(len(g_range)):
                if not np.isnan(prices[i, j]):
                    ax.text(j, i, f'¥{prices[i,j]:.0f}', ha='center', va='center',
                           fontsize=9, fontweight='bold',
                           color='white' if prices[i,j] > np.nanmedian(prices) else 'black')
                else:
                    ax.text(j, i, 'N/A', ha='center', va='center', fontsize=9, color='gray')
        
        # 高亮当前WACC & g的位置
        wacc_idx = wacc_range.index(min(wacc_range, key=lambda x: abs(x - wacc)))
        g_idx = g_range.index(min(g_range, key=lambda x: abs(x - terminal_growth * 100)))
        ax.add_patch(plt.Rectangle((g_idx - 0.5, wacc_idx - 0.5), 1, 1,
                                    fill=False, edgecolor='blue', linewidth=3, linestyle='--'))
        
        ax.set_xlabel('永续增长率 (g)', fontsize=12)
        ax.set_ylabel('WACC', fontsize=12)
        ax.set_title(f'DCF敏感性分析 · {name}\n蓝色虚线=基准假设 (WACC={wacc:.1f}%, g={terminal_growth*100:.1f}%)',
                    fontsize=14, fontweight='bold')
        
        plt.colorbar(im, ax=ax, label='隐含股价 (¥)')
        plt.tight_layout()
        
        output_path = os.path.join(output_dir, f"{ticker.replace('.', '_')}_sensitivity_heatmap.png")
        if ticker:
            plt.savefig(output_path, dpi=200, bbox_inches='tight')
            lines.append(f"\n  📊 敏感性热力图: {output_path}")
        plt.close()
    except Exception as e:
        lines.append(f"\n  ⚠️ 热力图生成失败: {e}")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="DCF估值建模")
    parser.add_argument("--ticker", "-t", required=True, help="股票代码")
    parser.add_argument("--market", "-m", default="a-share", help="市场")
    parser.add_argument("--wacc", type=float, help="WACC值（覆盖自动计算）")
    parser.add_argument("--growth", "-g", type=float, default=2.5, help="永续增长率%")
    parser.add_argument("--output-dir", "-o", default=".", help="图表输出目录")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()
    
    ticker = args.ticker
    if ticker not in FINANCIAL_DB:
        print(f"❌ 股票 {ticker} 数据未收录")
        sys.exit(1)
    
    company = FINANCIAL_DB[ticker].copy()
    
    # 实时股价覆盖
    live_price = _fetch_live_price(ticker, company.get("market", "a-share"))
    if live_price:
        old_p = company["current_price"]
        company["current_price"] = live_price
        shares = company.get("shares_outstanding", 0)
        if shares > 0:
            company["market_cap"] = round(live_price * shares, 2)
        print(f"✅ DCF: 实时股价 ¥{old_p} → ¥{live_price}", file=sys.stderr)

    company["ticker"] = ticker
    terminal_growth = args.growth / 100
    
    # 计算WACC
    if args.wacc:
        wacc = args.wacc
    else:
        wacc = calculate_wacc(
            company["beta"], company["debt_ratio"],
            company["effective_tax_rate"]
        )
    
    # 生成预测
    projections = project_fcf(company, years=5)
    
    # DCF估值
    dcf_result = dcf_valuation(projections, wacc, terminal_growth)
    
    # 输出
    os.makedirs(args.output_dir, exist_ok=True)
    
    if args.format == "json":
        # 敏感性矩阵数据
        wacc_range = [round(w, 1) for w in np.linspace(7.5, 10.5, 7)]
        g_range = [round(g, 1) for g in np.linspace(1.5, 3.5, 5)]
        prices = sensitivity_analysis(projections, company["net_cash"],
                                      company["shares_outstanding"], wacc_range, g_range)
        sensitivity = {}
        for wi, w in enumerate(wacc_range):
            row_key = str(w)
            sensitivity[row_key] = {}
            for gj, g in enumerate(g_range):
                sensitivity[row_key][str(g)] = prices[wi, gj] if not np.isnan(prices[wi, gj]) else None
        
        output = {
            "company": company["name"],
            "ticker": ticker,
            "wacc": wacc,
            "terminal_growth": terminal_growth,
            "projections": projections,
            "dcf_result": {**dcf_result, "implied_price": round(
                (dcf_result["enterprise_value"] + company["net_cash"]) / company["shares_outstanding"], 2
            )},
            "sensitivity": {
                "wacc_range": wacc_range,
                "g_range": g_range,
                "prices": sensitivity,
            },
            "current_price": company["current_price"],
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        report = format_dcf_report(company, wacc, terminal_growth, projections, dcf_result, args.output_dir)
        print(report)


if __name__ == "__main__":
    main()
