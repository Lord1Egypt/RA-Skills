#!/usr/bin/env python3
"""
Comprehensive Analysis Report Generator

Combines fundamental, technical, valuation, and risk analysis into a single
investment thesis report using the template in assets/templates/analysis_report.md.

Usage:
    from report_generator import generate_report
    report = generate_report('sh510300', name='沪深300ETF')
    print(report)
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
import sys

# Ensure utils can be imported when running standalone
sys.path.insert(0, str(Path(__file__).parent))

from utils import fetch_tencent_kline
from technical_analysis import analyze as tech_analyze
from valuation_analysis import analyze as val_analyze, ValuationMetrics
from risk_analysis import analyze as risk_analyze
from fundamental_analysis import analyze as fund_analyze

# Template path (prefer simple version)
TEMPLATE_SIMPLE = Path(__file__).parent.parent / "assets/templates/analysis_report_simple.md"
TEMPLATE_FULL = Path(__file__).parent.parent / "assets/templates/analysis_report.md"


def get_current_price(ticker: str) -> Optional[float]:
    data = fetch_tencent_kline(ticker, days=5)
    if data and data['close']:
        return float(data['close'][-1])
    return None


def calculate_price_changes(ticker: str) -> Dict[str, float]:
    data = fetch_tencent_kline(ticker, days=200)
    if not data or len(data['close']) < 130:
        return {}
    closes = data['close']
    changes = {}
    if len(closes) >= 22:
        changes['1m'] = (closes[-1] / closes[-22] - 1) * 100
    if len(closes) >= 66:
        changes['3m'] = (closes[-1] / closes[-66] - 1) * 100
    if len(closes) >= 132:
        changes['6m'] = (closes[-1] / closes[-132] - 1) * 100
    return changes


def fetch_industry_benchmark(ticker: str) -> Dict:
    try:
        val_result = val_analyze(ticker)
        return {
            'industry_pe_median': val_result['metrics'].industry_pe_median,
            'industry_pb_median': val_result['metrics'].industry_pb_median,
            'industry_name': val_result['metrics'].industry_pe_median
        }
    except:
        return {'industry_pe_median': None, 'industry_pb_median': None, 'industry_name': '未知'}


def translate_zone(zone: str) -> str:
    mapping = {'undervalued': '低估', 'normal': '正常', 'overvalued': '高估', 'unknown': '数据不足'}
    return mapping.get(zone, zone)


def translate_trend(trend: str) -> str:
    mapping = {'bullish': '上涨', 'bearish': '下跌', 'sideways': '震荡'}
    return mapping.get(trend, trend)


def generate_score_components(ticker: str, tech_summary: str, val_metrics: ValuationMetrics,
                             risk_metrics, fund_summary: str) -> Dict[str, float]:
    scores = {}
    # Fundamental
    if fund_summary and '优秀' in fund_summary:
        scores['fundamental'] = 9.0
    elif fund_summary and '良好' in fund_summary:
        scores['fundamental'] = 7.5
    elif fund_summary and '偏低' in fund_summary:
        scores['fundamental'] = 4.0
    else:
        scores['fundamental'] = 5.0
    # Valuation
    if val_metrics.pe_zone == 'undervalued':
        scores['valuation'] = 9.0
    elif val_metrics.pe_zone == 'overvalued':
        scores['valuation'] = 3.0
    else:
        scores['valuation'] = 6.0
    # Technical
    if '上涨' in tech_summary or 'bullish' in tech_summary:
        scores['technical'] = 8.0
    elif '下跌' in tech_summary or 'bearish' in tech_summary:
        scores['technical'] = 3.0
    else:
        scores['technical'] = 5.5
    # Risk
    if hasattr(risk_metrics, 'sharpe_ratio') and risk_metrics.sharpe_ratio:
        if risk_metrics.sharpe_ratio > 1.5:
            scores['risk'] = 9.0
        elif risk_metrics.sharpe_ratio > 1.0:
            scores['risk'] = 7.5
        elif risk_metrics.sharpe_ratio > 0.5:
            scores['risk'] = 6.0
        else:
            scores['risk'] = 4.0
    else:
        scores['risk'] = 5.0
    return scores


def generate_recommendation(total_score: float, component_scores: Dict) -> str:
    if total_score >= 8.0:
        return "**买入** (综合评分优秀，各维度均表现良好)"
    elif total_score >= 6.5:
        return "**增持** (整体质地较好，适合逐步配置)"
    elif total_score >= 5.0:
        return "**中性** (无显著亮点或风险，建议观望)"
    elif total_score >= 4.0:
        return "**减持** (部分指标较弱，建议降低仓位)"
    else:
        return "**卖出** (多项指标不佳，风险较大)"


def generate_risk_warnings(risk_metrics, tech_snapshot, val_metrics) -> str:
    warnings = []
    if hasattr(risk_metrics, 'max_drawdown') and risk_metrics.max_drawdown:
        if risk_metrics.max_drawdown > 30:
            warnings.append(f"⚠️ 历史最大回撤高达{risk_metrics.max_drawdown:.1f}%，波动风险较大")
    if hasattr(tech_snapshot, 'trend'):
        if tech_snapshot.trend == 'bearish':
            warnings.append("⚠️ 当前技术面处于下跌趋势，建议等待企稳信号")
        elif tech_snapshot.trend == 'sideways' and tech_snapshot.trend_strength == 'weak':
            warnings.append("⚠️ 技术面震荡偏弱，缺乏明确方向")
    if val_metrics.pe_zone == 'overvalued':
        warnings.append(f"⚠️ 估值处于历史偏高区域（PE分位数{val_metrics.pe_percentile:.0f}%）")
    if hasattr(tech_snapshot, 'rsi_14') and tech_snapshot.rsi_14:
        if tech_snapshot.rsi_14 > 75:
            warnings.append(f"⚠️ RSI({tech_snapshot.rsi_14:.0f})显示超买，短期有回调风险")
        elif tech_snapshot.rsi_14 < 25:
            warnings.append(f"⚠️ RSI({tech_snapshot.rsi_14:.0f})显示超卖，可能存在反弹机会")
    if not warnings:
        warnings.append("✅ 暂无显著风险预警")
    return "\n".join([f"- {w}" for w in warnings])


def fill_template(ticker: str, name: str, tech_result: Dict, val_result: Dict, risk_result: Dict, fund_result: Dict) -> str:
    tech_snap = tech_result.get('snapshot')
    val_metrics = val_result.get('metrics')
    risk_metrics = risk_result.get('metrics') if 'metrics' in risk_result else risk_result
    fund_metrics = fund_result.get('metrics') if 'metrics' in fund_result else None

    # Gather data
    current_price = get_current_price(ticker) or (tech_snap.current_price if tech_snap else None)
    data_date = datetime.now().strftime("%Y-%m-%d")
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    price_changes = calculate_price_changes(ticker)
    change_1m = price_changes.get('1m')
    change_5d = tech_snap.price_change_5d if tech_snap else None
    change_20d = tech_snap.price_change_20d if tech_snap else None

    industry = fetch_industry_benchmark(ticker)
    industry_pb_median = industry.get('industry_pb_median')

    pe_zone = translate_zone(val_metrics.pe_zone) if val_metrics else '未知'
    pb_zone = translate_zone(val_metrics.pb_zone) if val_metrics else '未知'
    overall_rating = translate_zone(val_metrics.overall_rating) if val_metrics else '未知'

    pe_premium = None
    pe_premium_comment = ''
    if val_metrics and val_metrics.pe and industry.get('industry_pe_median'):
        pe_premium = (val_metrics.pe - industry['industry_pe_median']) / industry['industry_pe_median'] * 100
        if pe_premium > 20:
            pe_premium_comment = '显著高于行业'
        elif pe_premium > 5:
            pe_premium_comment = '略高于行业'
        elif pe_premium < -20:
            pe_premium_comment = '显著低于行业'
        elif pe_premium < -5:
            pe_premium_comment = '略低于行业'
        else:
            pe_premium_comment = '与行业持平'

    tech_summary = tech_result.get('summary', '暂无技术面数据')

    vol = getattr(risk_metrics, 'annualized_volatility', None)
    max_dd = getattr(risk_metrics, 'max_drawdown', None)
    sharpe = getattr(risk_metrics, 'sharpe_ratio', None)
    beta = getattr(risk_metrics, 'beta', None)

    fund_summary = fund_result.get('summary', '暂无基本面数据') if fund_result else '暂无基本面数据'

    comp_scores = generate_score_components(ticker, tech_summary, val_metrics, risk_metrics, fund_summary)
    total_score = sum(comp_scores.values()) / len(comp_scores) * 10

    recommendation = generate_recommendation(total_score, comp_scores)
    risk_warnings = generate_risk_warnings(risk_metrics, tech_snap, val_metrics)

    # RSI comment
    rsi_comment = '超买' if tech_snap and tech_snap.rsi_14 and tech_snap.rsi_14 > 70 else ('超卖' if tech_snap and tech_snap.rsi_14 and tech_snap.rsi_14 < 30 else '中性') if tech_snap and tech_snap.rsi_14 else 'N/A'

    replacements = {
        '{{ticker}}': ticker,
        '{{name}}': name,
        '{{date}}': data_date,
        '{{data_date}}': data_date,
        '{{generated_at}}': generated_at,
        '{{current_price}}': f"{current_price:.2f}" if current_price else 'N/A',
        '{{price_change_5d}}': f"{change_5d:+.1f}%" if change_5d else 'N/A',
        '{{price_change_20d}}': f"{change_20d:+.1f}%" if change_20d else 'N/A',
        '{{pe}}': f"{val_metrics.pe:.1f}" if val_metrics and val_metrics.pe else 'N/A',
        '{{pe_percentile}}': f"{val_metrics.pe_percentile:.0f}" if val_metrics and val_metrics.pe_percentile else 'N/A',
        '{{pe_percentile_comment}}': pe_zone,
        '{{pe_zone}}': pe_zone,
        '{{industry_pe_median}}': f"{industry.get('industry_pe_median', 'N/A'):.1f}" if industry.get('industry_pe_median') else 'N/A',
        '{{pe_premium}}': f"{pe_premium:.1f}" if pe_premium else 'N/A',
        '{{pe_premium_comment}}': pe_premium_comment,
        '{{industry_pb_median}}': f"{industry_pb_median:.2f}" if industry_pb_median else 'N/A',
        '{{pb}}': f"{val_metrics.pb:.2f}" if val_metrics and val_metrics.pb else 'N/A',
        '{{pb_percentile}}': f"{val_metrics.pb_percentile:.0f}" if val_metrics and val_metrics.pb_percentile else 'N/A',
        '{{pb_zone}}': pb_zone,
        '{{pe_5y_median}}': f"{val_metrics.pe_5y_median:.1f}" if val_metrics and val_metrics.pe_5y_median else 'N/A',
        '{{pb_5y_median}}': f"{val_metrics.pb_5y_median:.2f}" if val_metrics and val_metrics.pb_5y_median else 'N/A',
        '{{overall_rating}}': overall_rating,
        '{{tech_summary}}': tech_summary,
        '{{trend}}': translate_trend(tech_snap.trend) if tech_snap and tech_snap.trend else 'N/A',
        '{{trend_strength}}': tech_snap.trend_strength if tech_snap and tech_snap.trend_strength else 'N/A',
        '{{above_ma20}}': '之上' if tech_snap and tech_snap.above_ma20 else ('之下' if tech_snap else 'N/A'),
        '{{ma20}}': f"{tech_snap.ma20:.2f}" if tech_snap and tech_snap.ma20 else 'N/A',
        '{{rsi_14}}': f"{tech_snap.rsi_14:.1f}" if tech_snap and tech_snap.rsi_14 else 'N/A',
        '{{rsi_comment}}': rsi_comment,
        '{{support_levels}}': ', '.join([f"{s:.2f}" for s in tech_snap.support_levels]) if tech_snap and tech_snap.support_levels else 'N/A',
        '{{resistance_levels}}': ', '.join([f"{s:.2f}" for s in tech_snap.resistance_levels]) if tech_snap and tech_snap.resistance_levels else 'N/A',
        '{{annualized_volatility}}': f"{vol:.1f}" if vol else 'N/A',
        '{{max_drawdown}}': f"{max_dd:.1f}" if max_dd else 'N/A',
        '{{sharpe_ratio}}': f"{sharpe:.2f}" if sharpe else 'N/A',
        '{{beta}}': f"{beta:.2f}" if beta else 'N/A',
        '{{score_fundamental}}': f"{comp_scores.get('fundamental', 5):.1f}",
        '{{score_technical}}': f"{comp_scores.get('technical', 5):.1f}",
        '{{score_valuation}}': f"{comp_scores.get('valuation', 5):.1f}",
        '{{score_risk}}': f"{comp_scores.get('risk', 5):.1f}",
        '{{score_fundamental_weighted}}': f"{comp_scores.get('fundamental', 5) * 0.3:.2f}",
        '{{score_technical_weighted}}': f"{comp_scores.get('technical', 5) * 0.2:.2f}",
        '{{score_valuation_weighted}}': f"{comp_scores.get('valuation', 5) * 0.3:.2f}",
        '{{score_risk_weighted}}': f"{comp_scores.get('risk', 5) * 0.2:.2f}",
        '{{total_score}}': f"{total_score:.2f}",
        '{{recommendation}}': recommendation,
        '{{reason_1}}': f"基本面评分{comp_scores.get('fundamental', 5):.1f}/10，{translate_zone(pe_zone)}估值" if comp_scores else '综合评分中等',
        '{{reason_2}}': f"技术面处于{translate_trend(tech_snap.trend) if tech_snap else '震荡'}状态" if tech_snap else '技术面缺乏明显信号',
        '{{reason_3}}': f"波动率{vol:.1f}%" if vol else '风险指标中性',
        '{{risk_warnings}}': risk_warnings,
        '{{generated_at}}': generated_at,
    }

    # Choose template
    if TEMPLATE_SIMPLE.exists():
        template_file = TEMPLATE_SIMPLE
    elif TEMPLATE_FULL.exists():
        template_file = TEMPLATE_FULL
    else:
        return generate_simple_report(ticker, name, tech_result, val_result, risk_result, fund_result)

    with open(template_file, 'r', encoding='utf-8') as f:
        template = f.read()

    content = template
    for key, value in replacements.items():
        if value is None:
            value = 'N/A'
        content = content.replace(key, str(value))

    return content


def generate_simple_report(ticker: str, name: str, tech_result: Dict, val_result: Dict, risk_result: Dict, fund_result: Dict) -> str:
    lines = [
        f"# 投资分析报告：{name} ({ticker})",
        f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## 技术面摘要",
        tech_result.get('summary', '暂无'),
        "",
        "## 估值摘要",
        val_result.get('summary', '暂无'),
        "",
        "## 风险指标",
        risk_result.get('summary', '暂无'),
        "",
        "## 基本面摘要",
        fund_result.get('summary', '暂无'),
        "",
        "---",
        "注：此为简版报告，完整模板需要 assets/templates/analysis_report.md"
    ]
    return "\n".join(lines)


def generate_report(ticker: str, name: Optional[str] = None, 
                   lookback_days: int = 250) -> str:
    if not name:
        name = ticker
    print(f"Generating report for {name} ({ticker})...")
    tech_result = tech_analyze(ticker, lookback_days)
    val_result = val_analyze(ticker)
    risk_result = risk_analyze(ticker, period_days=252)
    fund_result = fund_analyze(ticker)
    report = fill_template(ticker, name, tech_result, val_result, risk_result, fund_result)
    print("Done.")
    return report


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Generate stock/ETF analysis report')
    parser.add_argument('ticker', help='Stock/ETF code (e.g., sh510300)')
    parser.add_argument('--name', help='Name of the instrument (optional)')
    parser.add_argument('--output', help='Output file (default: stdout)')
    args = parser.parse_args()

    try:
        report = generate_report(args.ticker, args.name)
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"Report saved to {args.output}")
        else:
            print(report)
    except Exception as e:
        print(f"Error generating report: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
