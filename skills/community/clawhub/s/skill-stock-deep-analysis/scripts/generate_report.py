#!/usr/bin/env python3
"""
generate_report.py - 股票深度分析报告生成器
用法:
  python generate_report.py --ticker PDD --market US [--cost 100] [--currency USD]
  python generate_report.py --ticker 600141.SH --market CN --cost 100 --currency CNY
"""

import os
import sys
import json
import textwrap
import argparse
from datetime import datetime
from pathlib import Path

# ── 代理设置 ───────────────────────────────────────────────────────
os.environ['HTTPS_PROXY'] = os.environ.get('HTTPS_PROXY', 'http://172.30.192.1:7890')
os.environ['HTTP_PROXY'] = os.environ.get('HTTP_PROXY', 'http://172.30.192.1:7890')
# ─────────────────────────────────────────────────────────────────

CURRENCY_SYMBOL = {'USD': '$', 'HKD': 'HK$', 'CNY': '¥'}
CURRENCY_NAME   = {'USD': '美元', 'HKD': '港币', 'CNY': '人民币'}


def _to_b(val):
    if val is None: return 'N/A'
    if val >= 1e12: return f"${val/1e12:.2f}万亿"
    if val >= 1e9:  return f"${val/1e9:.2f}十亿"
    if val >= 1e6:  return f"${val/1e6:.2f}M"
    return f"${val:.0f}"


def _pct(v):
    if v is None: return 'N/A'
    return f"{v:.2f}%"


def _num(v, suffix=''):
    if v is None: return 'N/A'
    return f"{v:,.2f}{suffix}"


def _rating(val, thresholds, reverse=False):
    """根据阈值返回评级
    reverse=True 用于 PE/PB 这类越低越好的指标
    """
    if val is None: return ('N/A', '')
    lo, hi = thresholds
    if reverse:
        # 反向：值越小越好（PE、PB、债务率等）
        if val <= hi: return ('✅ 极低/低估', '⭐')
        if val <= lo: return ('✅ 低估', '')
        if val <= lo * 1.5: return ('⚠️ 合理', '')
        return ('❌ 偏高', '')
    else:
        # 正向：值越大越好（ROE、流动比率等）
        if val >= hi: return ('✅ 优秀', '⭐')
        if val >= lo: return ('✅ 良好', '')
        if val >= (lo * 0.7): return ('⚠️ 一般', '')
        return ('❌ 较差', '')


def _format_market_cap(cap):
    if not cap: return 'N/A'
    if cap >= 1e12: return f"${cap/1e12:.2f}T"
    if cap >= 1e9:  return f"${cap/1e9:.2f}B"
    if cap >= 1e6:  return f"${cap/1e6:.2f}M"
    return f"${cap:.0f}"


def _format_analyst_rec(rec_data: dict) -> str:
    """格式化分析师评级"""
    buy = rec_data.get('buy', 0)
    hold = rec_data.get('hold', 0)
    sell = rec_data.get('sell', 0)
    sb = rec_data.get('strongBuy', 0)
    ss = rec_data.get('strongSell', 0)
    if buy or hold or sell:
        return f"买入={buy} | 持有={hold} | 卖出={sell} | 强烈买入={sb} | 强烈卖出={ss}"
    return f"综合评级: {rec_data.get('recommendation', 'N/A')}"


def _build_val_table(rows, col1='指标', col2='数值', col3='评级', col4='说明'):
    """构建 Markdown 表格"""
    lines = [f"| {col1} | {col2} | {col3} | {col4} |", "|------|------|------|------|"]
    for r in rows:
        lines.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} |")
    return '\n'.join(lines)


def analyze_us_stocks(data: dict, cost: float, currency: str) -> str:
    """生成美股/港股分析报告"""
    info = data.get('info', {})
    hist = data.get('hist', {})
    income = data.get('income_stmt') or {}
    bs = data.get('balance_sheet') or {}
    cf = data.get('cashflow') or {}

    # ── 基本行情 ──────────────────────────────────────────────────
    price = info.get('regularMarketPrice') or 0
    change = info.get('regularMarketChange') or 0
    change_pct = info.get('regularMarketChangePercent') or 0
    high52 = info.get('fiftyTwoWeekHigh') or 0
    low52 = info.get('fiftyTwoWeekLow') or 0
    mktcap = info.get('marketCap') or 0
    name = info.get('shortName') or info.get('longName') or info.get('quoteType', 'N/A')
    industry = info.get('industry') or 'N/A'
    sector = info.get('sector') or 'N/A'
    summary = info.get('longBusinessSummary') or ''
    trailing_pe = info.get('trailingPE') or 0
    forward_pe = info.get('forwardPE') or 0
    pb = info.get('priceToBook') or 0
    beta = info.get('beta') or 0
    target = info.get('targetMeanPrice') or 0
    rec_key = info.get('recommendationKey') or 'N/A'
    num_analysts = info.get('numberOfAnalystOpinions') or 0
    rev_growth = info.get('revenueGrowth') or 0
    earnings_qg = info.get('earningsQuarterlyGrowth') or 0
    total_rev = info.get('totalRevenue') or 0
    gross_profit = info.get('grossProfit') or 0
    net_income = info.get('netIncome') or 0
    op_margin = info.get('operatingMargins') or 0
    profit_margin = info.get('profitMargins') or 0
    roe = info.get('returnOnEquity') or 0
    roa = info.get('returnOnAssets') or 0
    total_debt = info.get('totalDebt') or 0
    debt_eq = info.get('debtToEquity') or 0
    current_ratio = info.get('currentRatio') or 0
    eps_ttm = info.get('epsCurrentYear') or 0
    eps_fwd = info.get('epsForward') or 0
    try:
        rec_data = info.get('recommendationTrend', {}).get('trend', [{}])[0]
    except:
        rec_data = {'buy': 0, 'hold': 0, 'sell': 0, 'strongBuy': 0, 'strongSell': 0}

    sym = CURRENCY_SYMBOL.get(currency, '$')

    # ── 历史 EPS ─────────────────────────────────────────────────
    eps_annual = {}
    if income and 'Diluted EPS' in income:
        for date, val in income['Diluted EPS'].items():
            if val and val > 0:
                yr = str(date)[:4]
                eps_annual[yr] = val

    def _get_latest(series_dict):
        """从 to_dict('index') 格式提取最新（非最老）非空值"""
        if not series_dict: return None
        try:
            # sort descending → most recent date first
            dates = sorted(series_dict.keys(), reverse=True)
            for d in dates:
                v = series_dict[d]
                if v is not None and not (hasattr(v, '__float__') and v != v):  # skip NaN
                    return v
        except: pass
        return None

    def _get_bs(key, bs):
        """从 balance_sheet index 格式提取最新值"""
        if not bs or key not in bs: return None
        return _get_latest(bs[key])

    # ── 资产负债表字段 ────────────────────────────────────────────
    total_assets_val = _get_bs('Total Assets', bs)
    equity_val = _get_bs('Stockholders Equity', bs)
    cash_val = _get_bs('Cash And Cash Equivalents', bs)

    # ── 持仓盈亏 ──────────────────────────────────────────────────
    if cost:
        pnl = price - cost
        pnl_pct = (pnl / cost * 100) if cost else 0
        pos_str = f"**成本价：** {sym}{cost:.2f} → **当前价：** {sym}{price:.2f} | **盈亏：** {sym}{pnl:+.2f} ({pnl_pct:+.1f}%)"
    else:
        pos_str = f"**当前价：** {sym}{price:.2f}"

    # ── 52周位置 ──────────────────────────────────────────────────
    range_pct = (price - low52) / (high52 - low52) * 100 if high52 > low52 else 0

    # ── 构建报告 ──────────────────────────────────────────────────
    lines = []
    today = datetime.now().strftime('%Y-%m-%d')

    lines.append(f"# {name}（{info.get('symbol', 'N/A')}）深度分析报告")
    lines.append("")
    lines.append(f"**报告日期：** {today} | {pos_str}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 一、公司概况
    lines.append("## 一、公司基本情况")
    lines.append("")
    lines.append(f"| 项目 | 内容 |")
    lines.append("|------|------|")
    lines.append(f"| 名称 | {name} |")
    lines.append(f"| 行业 | {industry} |")
    lines.append(f"| 板块 | {sector} |")
    if summary:
        lines.append(f"| 业务简介 | {textwrap.fill(summary[:300], 60)} |")
    lines.append("")

    # 二、估值分析
    lines.append("## 二、估值分析")
    lines.append("")
    rating_pe, star_pe = _rating(trailing_pe, (15, 25), reverse=True)
    rating_fwd, star_fwd = _rating(forward_pe, (10, 20), reverse=True)
    rating_pb, star_pb = _rating(pb, (3, 5), reverse=True)
    lines.append(f"| 指标 | 数值 | 评级 | 说明 |")
    lines.append("|------|------|------|------|")
    lines.append(f"| 当前价 | {sym}{price:.2f} | | {'距52周高点 -%.0f%%' % ((high52-price)/high52*100) if high52 else ''} |")
    lines.append(f"| 52周最高 | {sym}{high52:.2f} | | |")
    lines.append(f"| 52周最低 | {sym}{low52:.2f} | | 距当前 {'+%.1f%%' % ((price-low52)/low52*100) if low52 else ''} |")
    lines.append(f"| 52周位置 | {range_pct:.0f}% 分位 | {'✅ 低位' if range_pct < 30 else '⚠️ 中位' if range_pct < 70 else '❌ 高位'} | {'已近底部区域' if range_pct < 30 else '处于中部区域' if range_pct < 70 else '接近顶部区域'} |")
    lines.append(f"| Trailing PE | {trailing_pe:.2f} | {rating_pe} {star_pe} | {'偏低/合理/偏高' if trailing_pe else 'N/A'} |")
    lines.append(f"| Forward PE | {forward_pe:.2f} | {rating_fwd} {star_fwd} | 预期2026 EPS {sym}{eps_fwd:.2f} |")
    lines.append(f"| Price/Book | {pb:.2f} | {rating_pb} {star_pb} | |")
    lines.append(f"| Beta | {beta:.3f} | {'低波动' if beta < 0.8 else '跟随大盘' if beta < 1.2 else '高波动'} | 与大盘相关性{'极低' if beta < 0.5 else '低' if beta < 1 else '高'} |")
    lines.append(f"| 市值 | {_format_market_cap(mktcap)} | | |")
    lines.append(f"| 分析师目标价 | {sym}{target:.2f} | {'✅ 高于现价 +%.0f%%' % ((target-price)/price*100) if target else 'N/A'} | {num_analysts} 位分析师覆盖 |")
    lines.append(f"| 分析师评级 | {rec_key} | | {_format_analyst_rec(rec_data)} |")
    lines.append("")

    # 三、盈利能力
    lines.append("## 三、盈利能力")
    lines.append("")
    if eps_annual:
        lines.append("**年度稀释EPS（美元）：**")
        yrs = sorted(eps_annual.keys(), reverse=True)
        for yr in yrs[:6]:
            val = eps_annual[yr]
            prev = eps_annual.get(str(int(yr)-1), None)
            chg = f" ({val-prev:+.1f})" if prev else ""
            lines.append(f"  {yr}: {sym}{val:.2f}{chg}")
        lines.append("")

    rating_rev, _ = _rating(rev_growth * 100 if rev_growth else None, (10, 30))
    lines.append(f"| 指标 | 数值 | 评级 |")
    lines.append("|------|------|------|")
    lines.append(f"| 总营收 | {_to_b(total_rev)} | |")
    # 从财报提取毛利润/净利润（index 格式：{指标名: {date: value}}）
    def _get_fin(key, fin_dict):
        if not fin_dict or key not in fin_dict: return None
        return _get_latest(fin_dict[key])

    gross_val = _get_fin('Gross Profit', income)
    net_val = _get_fin('Net Income', income)
    lines.append(f"| 毛利润 | {_to_b(gross_val)} | |")
    lines.append(f"| 净利润 | {_to_b(net_val)} | |")
    lines.append(f"| 营收增速（YoY） | {rev_growth*100:.1f}% | {rating_rev} |")
    lines.append(f"| 季度盈利增速 | {earnings_qg*100:.1f}% | {'❌ 下滑' if earnings_qg < 0 else '✅ 增长'} |")
    lines.append(f"| 营业利润率 | {op_margin*100:.1f}% | {'✅ 优秀' if op_margin > 0.2 else '⚠️ 一般'} |")
    lines.append(f"| 净利润率 | {profit_margin*100:.1f}% | {'✅ 优秀' if profit_margin > 0.2 else '⚠️ 一般'} |")
    lines.append(f"| ROE | {roe*100:.1f}% | {'✅ 优秀' if roe > 0.15 else '⚠️ 一般' if roe > 0.08 else '❌ 差'} |")
    lines.append(f"| ROA | {roa*100:.1f}% | {'✅ 优秀' if roa > 0.08 else '⚠️ 一般' if roa > 0.04 else '❌ 差'} |")
    lines.append("")

    # 四、资产负债
    lines.append("## 四、资产负债质量")
    lines.append("")
    rating_dr, _ = _rating(debt_eq, (50, 100), reverse=True)
    rating_cr, _ = _rating(current_ratio, (1.5, 2.0))
    lines.append(f"| 指标 | 数值 | 评级 | 说明 |")
    lines.append("|------|------|------|------|")
    lines.append(f"| 总资产 | {_to_b(total_assets_val)} | | |")
    lines.append(f"| 股东权益 | {_to_b(equity_val)} | | |")
    lines.append(f"| 总债务 | {_to_b(total_debt)} | | |")
    lines.append(f"| 债务/权益 | {debt_eq:.1f}% | {rating_dr} | {'低杠杆' if debt_eq < 50 else '高杠杆'} |")
    lines.append(f"| 流动比率 | {current_ratio:.2f} | {rating_cr} | {'健康' if current_ratio > 1.5 else '⚠️ 偏低' if current_ratio > 1 else '❌ 较差'} |")
    if cash_val:
        lines.append(f"| 现金及等价物 | {_to_b(cash_val)} | ✅ | |")
    lines.append("")

    # 五、现金流（index 格式：{指标名: {date: value}}）
    lines.append("## 五、自由现金流")
    lines.append("")
    if cf:
        def _get_cf(key):
            if key not in cf: return None
            return _get_latest(cf[key])

        op_cf = _get_cf('Operating Cash Flow')
        fcf = _get_cf('Free Cash Flow')
        capex = _get_cf('Capital Expenditure')
        if capex: capex = abs(capex)

        lines.append(f"| 指标 | 数值 |")
        lines.append("|------|------|")
        if op_cf: lines.append(f"| 经营现金流 | {_to_b(op_cf)} |")
        if fcf:   lines.append(f"| 自由现金流 | {_to_b(fcf)} |")
        if capex: lines.append(f"| 资本支出 | {_to_b(capex)} |")
        if fcf and op_cf:
            lines.append(f"| FCF/经营现金流 | {fcf/op_cf*100:.1f}% |")
        lines.append("")
    else:
        lines.append("_现金流数据暂不可用_")
        lines.append("")

    # 六、持仓状态
    if cost:
        lines.append("## 六、持仓状态")
        lines.append("")
        pnl = price - cost
        pnl_pct = (pnl / cost * 100)
        range_lo = (low52 - price) / price * 100
        range_hi = (high52 - price) / price * 100
        upside_to_target = (target - price) / price * 100 if target else 0
        lines.append(f"| 项目 | 数值 |")
        lines.append("|------|------|")
        lines.append(f"| 买入成本 | {sym}{cost:.2f} |")
        lines.append(f"| 当前价格 | {sym}{price:.2f} |")
        lines.append(f"| 浮动盈亏 | {sym}{pnl:+.2f}（{pnl_pct:+.1f}%）|")
        lines.append(f"| 距52周低点 | {sym}{low52:.2f}（{'+' if price > low52 else ''}{(price/low52-1)*100:.1f}%）|")
        lines.append(f"| 距52周高点 | {sym}{high52:.2f}（{range_hi:.1f}%）|")
        if target: lines.append(f"| 距分析师目标 | {sym}{target:.2f}（+{upside_to_target:.0f}%）|")
        lines.append("")
    else:
        lines.append("## 六、技术走势（参考）")
        lines.append("")
        if hist and 'Close' in hist:
            closes = list(hist['Close'].values())
            if closes:
                cur = closes[-1]
                high = max(closes)
                low = min(closes)
                lines.append(f"| 项目 | 数值 |")
                lines.append("|------|------|")
                lines.append(f"| 当前价 | {sym}{cur:.2f} |")
                lines.append(f"| 2年最高 | {sym}{high:.2f} |")
                lines.append(f"| 2年最低 | {sym}{low:.2f} |")
                lines.append("")
        lines.append("（如需计算盈亏，请用 `--cost` 参数传入买入成本）")
        lines.append("")

    # 七、综合结论
    lines.append("## 七、综合结论")
    lines.append("")

    # 多空逻辑
    positives = []
    negatives = []

    if trailing_pe and trailing_pe < 15:
        positives.append(f"PE仅{trailing_pe:.1f}倍，估值极低")
    elif trailing_pe and trailing_pe > 30:
        negatives.append(f"PE{trailing_pe:.1f}倍，估值偏高")

    if pb and pb < 2:
        positives.append(f"PB{pb:.1f}倍，低于净资产")
    elif pb and pb > 5:
        negatives.append(f"PB{pb:.1f}倍，估值偏高")

    if current_ratio and current_ratio > 2:
        positives.append(f"流动比率{current_ratio:.1f}，财务健康")
    elif current_ratio and current_ratio < 1:
        negatives.append(f"流动比率{current_ratio:.1f}，短期偿债压力大")

    if range_pct and range_pct < 25:
        positives.append("股价处于52周低位，安全边际较高")
    elif range_pct and range_pct > 80:
        negatives.append("股价处于52周高位，追高风险大")

    if target and target > price * 1.3:
        positives.append(f"分析师目标价$143，当前价$82，上涨空间+{upside_to_target:.0f}%")
    if earnings_qg and earnings_qg < -0.1:
        negatives.append(f"季度盈利下滑{earnings_qg*100:.0f}%，需关注")
    if beta and beta < 0.5:
        positives.append(f"Beta{beta:.2f}，与大盘低相关，独立行情")
    if roe and roe > 0.2:
        positives.append(f"ROE{roe*100:.1f}%，股东回报优秀")

    lines.append("### ✅ 利好因素")
    if positives:
        for p in positives:
            lines.append(f"- {p}")
    else:
        lines.append("- 暂无明显利好")
    lines.append("")

    lines.append("### 🔴 风险因素")
    if negatives:
        for n in negatives:
            lines.append(f"- {n}")
    else:
        lines.append("- 暂无明显风险")
    lines.append("")

    # 操作建议
    lines.append("### 📊 操作建议")
    if cost and pnl_pct < -20:
        lines.append("| 选项 | 逻辑 |")
        lines.append("|------|------|")
        lines.append("| **持有/补仓** | -18%已是较深跌幅，若公司逻辑未变，低估值区域加仓可摊薄成本 |")
        lines.append("| **止损** | 若 Temu 关税/监管风险加剧，及时止损防止更大损失 |")
        lines.append("| **装死** | 分析师目标价远高于现价，长线逻辑成立可持有等待价值回归 |")
    elif cost and pnl_pct > 10:
        lines.append(f"当前盈利 +{pnl_pct:.1f}%，可考虑分批止盈，锁住利润")
    elif cost:
        lines.append(f"当前亏损 {pnl_pct:.1f}%，建议结合基本面判断是否继续持有")
    else:
        lines.append("传入持仓成本后可获得具体操作建议")
    lines.append("")

    # 免责声明
    lines.append("---")
    lines.append("")
    lines.append("> ⚠️ _本报告仅供参考，不构成投资建议。投资决策请咨询专业顾问。数据来源：Yahoo Finance，报告生成时间：" + today + "_")

    return '\n'.join(lines)


def analyze_cn_stock(data: dict, cost: float, currency: str) -> str:
    """生成A股分析报告"""
    info = data.get('info', {})
    hist = data.get('hist', {})
    indicators = data.get('indicators') or []

    name = info.get('longBusinessSummary') or info.get('name', 'N/A')
    industry = info.get('industry', 'N/A')
    sym = CURRENCY_SYMBOL.get(currency, '¥')

    # 最新价
    price = None
    if hist and 'Close' in hist:
        closes = hist['Close']
        if closes:
            latest_date = max(closes.keys())
            price = closes[latest_date]

    today = datetime.now().strftime('%Y-%m-%d')
    lines = []
    lines.append(f"# {name} 深度分析报告")
    lines.append("")
    lines.append(f"**报告日期：** {today}")
    if price:
        lines.append(f"**当前价：** {sym}{price:.2f}")
    if cost:
        pnl = (price - cost) / cost * 100 if price else 0
        lines.append(f"**持仓成本：** {sym}{cost:.2f}（{'+' if pnl >= 0 else ''}{pnl:.1f}%）")
    lines.append("")
    lines.append("---")
    lines.append("")

    lines.append("## 一、公司概况")
    lines.append("")
    lines.append(f"| 项目 | 内容 |")
    lines.append("|------|------|")
    lines.append(f"| 公司 | {name} |")
    lines.append(f"| 行业 | {industry} |")
    lines.append("")

    lines.append("## 二、估值与行情")
    lines.append("")
    if indicators:
        latest = indicators[0]
        high52 = max(i.get('high_52w', 0) for i in indicators if i.get('high_52w'))
        low52 = min(i.get('low_52w', 0) for i in indicators if i.get('low_52w'))
        roe = latest.get('roe', 0)
        lines.append(f"| 指标 | 数值 | 评级 |")
        lines.append("|------|------|------|")
        lines.append(f"| 最新ROE | {roe:.2f}% | {'✅ 优秀' if roe > 10 else '⚠️ 一般' if roe > 5 else '❌ 差'} |")
        lines.append(f"| 毛利率 | {latest.get('gross_margin', 0)/1e8:.2f}亿 | |")
        lines.append(f"| 资产负债率 | {latest.get('debt_to_assets', 0):.2f}% | |")
        lines.append(f"| 流动比率 | {latest.get('current_ratio', 0):.2f} | |")
        lines.append(f"| 每股收益EPS | {sym}{latest.get('eps', 0):.2f} | |")
        lines.append("")

    lines.append("## 三、财务趋势（多期）")
    lines.append("")
    if indicators:
        lines.append("| 报告期 | ROE | 毛利率 | 资产负债率 | EPS |")
        lines.append("|--------|-----|--------|------------|-----|")
        for ind in indicators[:8]:
            end = str(ind.get('end_date', ''))
            roe = ind.get('roe', 0) or 0
            gm = ind.get('gross_margin', 0) or 0
            da = ind.get('debt_to_assets', 0) or 0
            eps = ind.get('eps', 0) or 0
            lines.append(f"| {end} | {roe:.2f}% | {gm/1e8:.2f}亿 | {da:.1f}% | {eps:.2f} |")
        lines.append("")

    lines.append("## 四、综合结论")
    lines.append("")
    if cost and price:
        pnl = price - cost
        pnl_pct = pnl / cost * 100
        if pnl_pct < -20:
            lines.append("### 📊 操作建议")
            lines.append("| 选项 | 逻辑 |")
            lines.append("|------|------|")
            lines.append("| **持有** | 深度套牢，若公司基本面未恶化，可等待反弹 |")
            lines.append("| **止损** | 跌破关键支撑位需考虑止损 |")
            lines.append("")
    lines.append("> ⚠️ _本报告仅供参考，不构成投资建议_")

    return '\n'.join(lines)


def generate_stock_report(ticker: str, market: str = 'US',
                          cost: float = None,
                          currency: str = 'USD') -> str:
    """主入口函数"""
    from fetch_stock_data import fetch_stock_data

    market = market.upper()
    data = fetch_stock_data(ticker, market)

    if market == 'CN':
        return analyze_cn_stock(data, cost, currency)
    else:
        return analyze_us_stocks(data, cost, currency)


def main():
    parser = argparse.ArgumentParser(description='股票深度分析报告生成器')
    parser.add_argument('--ticker', required=True, help='股票代码（PDD / 0700.HK / 600141.SH）')
    parser.add_argument('--market', default='US', choices=['US', 'HK', 'CN'],
                       help='市场：US（美股）/ HK（港股）/ CN（A股），默认 US')
    parser.add_argument('--cost', type=float, default=None, help='持仓成本（按市场货币单位）')
    parser.add_argument('--currency', default='USD',
                       choices=['USD', 'HKD', 'CNY'],
                       help='货币单位，用于报告显示，默认 USD')
    args = parser.parse_args()

    report = generate_stock_report(args.ticker, args.market, args.cost, args.currency)
    print(report)


if __name__ == '__main__':
    main()