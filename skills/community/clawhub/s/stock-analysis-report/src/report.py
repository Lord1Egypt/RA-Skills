from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Union

from src.models import MarketAnalysisResult, StockAnalysisResult

logger = logging.getLogger(__name__)

_REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")


def _ensure_reports_dir() -> str:
    os.makedirs(_REPORTS_DIR, exist_ok=True)
    return _REPORTS_DIR


def _format_price(val) -> str:
    if val is None or val == 0:
        return "—"
    return f"{val:.2f}"


def _format_volume(val) -> str:
    if val is None or val == 0:
        return "—"
    abs_val = abs(val)
    sign = "-" if val < 0 else ""
    if abs_val >= 1e8:
        return f"{sign}{abs_val / 1e8:.2f}亿"
    if abs_val >= 1e4:
        return f"{sign}{abs_val / 1e4:.2f}万"
    return f"{val:.0f}"


def _status_icon(status: str) -> str:
    return {"满足": "✅", "注意": "⚠️", "不满足": "❌"}.get(status, "❓")


def _change_icon(pct: float) -> str:
    if pct > 0:
        return "🟢"
    if pct < 0:
        return "🔴"
    return "⚪"


def _score_bar(score: int, width: int = 20) -> str:
    filled = round(score / 100 * width)
    empty = width - filled
    if score >= 70:
        color = "🟩"
    elif score >= 40:
        color = "🟨"
    else:
        color = "🟥"
    return f"{color * filled}{'⬜' * empty}"


def _action_emoji(action: str) -> str:
    return {"买入": "🟢", "观望": "🟡", "卖出": "🔴"}.get(action, "⚪")


def _sentiment_emoji(sentiment: str) -> str:
    return {"偏多": "🟢", "中性": "🟡", "偏空": "🔴"}.get(sentiment, "⚪")


def generate_stock_report(result: StockAnalysisResult) -> str:
    lines: list[str] = []

    today = datetime.now().strftime("%Y-%m-%d")
    title = f"{result.stock_name or result.stock_code}（{result.stock_code}）分析报告"
    lines.append(f"# {title}")
    lines.append("")

    action_icon = _action_emoji(result.action)
    lines.append(f"> 📅 {today} | {_action_emoji(result.action)} {result.action or '—'} | "
                 f"📊 {_score_bar(result.score)} {result.score}/100 | "
                 f"📈 {result.trend or '—'}")
    lines.append("")

    if result.core_conclusion:
        lines.append("## 💡 核心观点")
        lines.append("")
        lines.append(f"**{result.core_conclusion}**")
        lines.append("")

    rt = result.realtime
    if rt and rt.price > 0:
        lines.append("## 📈 实时行情")
        lines.append("")
        sign = "+" if rt.change_pct > 0 else ""
        change_icon = _change_icon(rt.change_pct)
        lines.append(f"| 当前价 | 涨跌幅 | 涨跌额 | 今开 | 最高 | 最低 | 成交量 | 成交额 | 换手率 | 振幅 |")
        lines.append(f"|--------|--------|--------|------|------|------|--------|--------|--------|------|")
        lines.append(f"| {change_icon} {rt.price:.2f} | {sign}{rt.change_pct:.2f}% | {sign}{rt.change_amt:.2f} "
                     f"| {_format_price(rt.open)} | {_format_price(rt.high)} | {_format_price(rt.low)} "
                     f"| {_format_volume(rt.volume)} | {_format_volume(rt.turnover)} "
                     f"| {rt.turnover_rate:.2f}% | {rt.amplitude:.2f}% |")
        lines.append("")

    valuation = result.valuation
    if valuation and (valuation.pe_ttm > 0 or valuation.pb > 0):
        lines.append("## 📐 估值数据")
        lines.append("")
        lines.append("| 指标 | 数值 | 历史分位 |")
        lines.append("|------|------|----------|")
        if valuation.pe_ttm > 0:
            pe_pct = f"{valuation.pe_percentile:.1f}%" if valuation.pe_percentile > 0 else "—"
            lines.append(f"| 市盈率(TTM) | {valuation.pe_ttm:.1f} | {pe_pct} |")
        if valuation.pb > 0:
            pb_pct = f"{valuation.pb_percentile:.1f}%" if valuation.pb_percentile > 0 else "—"
            lines.append(f"| 市净率 | {valuation.pb:.2f} | {pb_pct} |")
        lines.append("")

    financial = result.financial
    if financial and any(v != 0 for v in [
        financial.net_profit, financial.revenue, financial.roe,
        financial.gross_margin, financial.debt_ratio,
    ]):
        lines.append("## 📋 核心财务指标")
        lines.append("")
        lines.append("| 指标 | 数值 |")
        lines.append("|------|------|")
        if financial.net_profit != 0:
            lines.append(f"| 归母净利润 | {_format_volume(financial.net_profit)} |")
        if financial.revenue != 0:
            lines.append(f"| 营业收入 | {_format_volume(financial.revenue)} |")
        if financial.net_profit_yoy != 0:
            icon = "🟢" if financial.net_profit_yoy > 0 else "🔴"
            lines.append(f"| 净利润同比 | {icon} {financial.net_profit_yoy:.2f}% |")
        if financial.revenue_yoy != 0:
            icon = "🟢" if financial.revenue_yoy > 0 else "🔴"
            lines.append(f"| 营收同比 | {icon} {financial.revenue_yoy:.2f}% |")
        if financial.roe != 0:
            lines.append(f"| ROE | {financial.roe:.2f}% |")
        if financial.gross_margin != 0:
            lines.append(f"| 毛利率 | {financial.gross_margin:.2f}% |")
        if financial.debt_ratio != 0:
            lines.append(f"| 资产负债率 | {financial.debt_ratio:.2f}% |")
        if financial.forecast_profit != 0:
            lines.append(f"| 预测净利润 | {_format_volume(financial.forecast_profit)} |")
        if financial.forecast_growth != 0:
            icon = "🟢" if financial.forecast_growth > 0 else "🔴"
            lines.append(f"| 预测增长率 | {icon} {financial.forecast_growth:.2f}% |")
        if financial.institution_holding_pct != 0:
            lines.append(f"| 机构持股比例 | {financial.institution_holding_pct:.2f}% |")
        lines.append("")

    capital_flow = result.capital_flow
    if capital_flow and any(v != 0 for v in [
        capital_flow.super_large_net, capital_flow.large_net,
        capital_flow.ddx, capital_flow.ddy, capital_flow.ddz,
    ]):
        lines.append("## 💸 主力资金流向")
        lines.append("")
        lines.append("| 资金类型 | 净额 |")
        lines.append("|----------|------|")
        if capital_flow.super_large_net != 0:
            icon = "🟢" if capital_flow.super_large_net > 0 else "🔴"
            lines.append(f"| {icon} 超大单 | {_format_volume(capital_flow.super_large_net)} |")
        if capital_flow.large_net != 0:
            icon = "🟢" if capital_flow.large_net > 0 else "🔴"
            lines.append(f"| {icon} 大单 | {_format_volume(capital_flow.large_net)} |")
        if capital_flow.medium_net != 0:
            icon = "🟢" if capital_flow.medium_net > 0 else "🔴"
            lines.append(f"| {icon} 中单 | {_format_volume(capital_flow.medium_net)} |")
        if capital_flow.small_net != 0:
            icon = "🟢" if capital_flow.small_net > 0 else "🔴"
            lines.append(f"| {icon} 小单 | {_format_volume(capital_flow.small_net)} |")
        lines.append("")
        if any(v != 0 for v in [capital_flow.ddx, capital_flow.ddy, capital_flow.ddz]):
            lines.append("| 技术指标 | 数值 | 含义 |")
            lines.append("|----------|------|------|")
            if capital_flow.ddx != 0:
                icon = "🟢" if capital_flow.ddx > 0 else "🔴"
                lines.append(f"| {icon} DDX | {capital_flow.ddx:.2f} | 大单动向 |")
            if capital_flow.ddy != 0:
                icon = "🟢" if capital_flow.ddy > 0 else "🔴"
                lines.append(f"| {icon} DDY | {capital_flow.ddy:.2f} | 筹码集中度变化 |")
            if capital_flow.ddz != 0:
                icon = "🟢" if capital_flow.ddz > 0 else "🔴"
                lines.append(f"| {icon} DDZ | {capital_flow.ddz:.2f} | 资金强度 |")
            lines.append("")

    tech = result.tech
    if tech and (tech.ma5 > 0 or tech.ma20 > 0):
        lines.append("## 📊 技术指标")
        lines.append("")
        lines.append(f"| MA5 | MA10 | MA20 | MA60 | 多头排列 | 乖离率 | 量比 | 短期趋势 |")
        lines.append(f"|-----|------|------|------|----------|--------|------|----------|")
        bullish = "✅ 是" if tech.is_bullish_alignment else "❌ 否"
        bias_icon = "⚠️" if abs(tech.bias) > 5 else "✅"
        lines.append(f"| {tech.ma5:.2f} | {tech.ma10:.2f} | {tech.ma20:.2f} | {tech.ma60:.2f} "
                     f"| {bullish} | {bias_icon} {tech.bias:.2f}% | {tech.volume_ratio:.2f} "
                     f"| {tech.recent_trend or '—'} |")
        lines.append("")

    chip = result.chip
    if chip and chip.avg_cost > 0:
        lines.append("## 🎯 筹码分布")
        lines.append("")
        profit_icon = "🟢" if chip.profit_ratio > 50 else "🔴"
        lines.append(f"| 获利比例 | 平均成本 | 集中度 | 90%成本 | 10%成本 |")
        lines.append(f"|----------|----------|--------|---------|---------|")
        lines.append(f"| {profit_icon} {chip.profit_ratio:.1f}% | {chip.avg_cost:.2f} "
                     f"| {chip.concentration:.2f}% | {chip.profit_90_cost:.2f} | {chip.profit_10_cost:.2f} |")
        lines.append("")
        if chip.avg_cost > 0 and rt and rt.price > 0:
            ratio = min(1.0, rt.price / (chip.avg_cost * 2))
            lines.append(f"**价格位置**：当前 {rt.price:.2f} 相对平均成本 {chip.avg_cost:.2f}")
            lines.append(f"```")
            lines.append(f"  10%成本 ←{'─' * 6} 平均成本 ←{'─' * 6} 90%成本")
            lines.append(f"  {chip.profit_10_cost:.2f}      {chip.avg_cost:.2f}      {chip.profit_90_cost:.2f}")
            lines.append(f"       {'▔' * 10} 当前价 {rt.price:.2f}")
            lines.append(f"```")
            lines.append("")

    if result.buy_price is not None or result.stop_loss_price is not None or result.target_price is not None:
        lines.append("## 💰 关键价位")
        lines.append("")
        lines.append(f"| 方向 | 买入价 | 止损价 | 目标价 | 盈亏比 |")
        lines.append(f"|------|--------|--------|--------|--------|")
        risk_reward = "—"
        if result.buy_price and result.stop_loss_price and result.target_price:
            risk = result.buy_price - result.stop_loss_price
            reward = result.target_price - result.buy_price
            if risk > 0:
                risk_reward = f"{reward / risk:.1f}:1"
        lines.append(f"| {_action_emoji(result.action)} {result.action or '—'} "
                     f"| {_format_price(result.buy_price)} | {_format_price(result.stop_loss_price)} "
                     f"| {_format_price(result.target_price)} | {risk_reward} |")
        lines.append("")

    if result.checklist:
        passed = sum(1 for item in result.checklist if item.status == "满足")
        total = len(result.checklist)
        lines.append(f"## ✅ 操作检查清单（{passed}/{total} 通过）")
        lines.append("")
        lines.append("| 条件 | 状态 | 详情 |")
        lines.append("|------|------|------|")
        for item in result.checklist:
            icon = _status_icon(item.status)
            lines.append(f"| {item.condition} | {icon} {item.status} | {item.detail} |")
        lines.append("")

    if result.risk_alerts or result.positive_catalysts:
        lines.append("## ⚡ 风险与催化")
        lines.append("")
        if result.risk_alerts:
            lines.append("**风险警报**：")
            for alert in result.risk_alerts:
                lines.append(f"- 🔴 {alert}")
            lines.append("")
        if result.positive_catalysts:
            lines.append("**利好催化**：")
            for catalyst in result.positive_catalysts:
                lines.append(f"- 🟢 {catalyst}")
            lines.append("")

    if result.news:
        total = len(result.news)
        lines.append(f"## 📰 近期资讯（{total}条）")
        lines.append("")
        for item in result.news:
            date_str = f"[{item.date}] " if item.date else ""
            type_tag = {"report": "[研报]", "announcement": "[公告]"}.get(item.info_type, "")
            source_str = f" — {item.source}" if item.source else ""
            lines.append(f"- {date_str}**{type_tag}{item.title}**{source_str}")
            text = item.snippet or item.content
            if text:
                lines.append(f"  > {text[:300]}")
        lines.append("")

    if result.raw_report:
        lines.append("## 📝 深度分析")
        lines.append("")
        lines.append(result.raw_report)
        lines.append("")

    if result.strategy:
        lines.append("## 🎯 操作建议")
        lines.append("")
        lines.append(result.strategy)
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(f"⚠️ {result.disclaimer}")

    return "\n".join(lines)


def generate_market_report(result: MarketAnalysisResult) -> str:
    lines: list[str] = []

    date_str = result.date or datetime.now().strftime("%Y-%m-%d")
    title = f"A股市场复盘报告 — {date_str}"
    lines.append(f"# {title}")
    lines.append("")

    sentiment_icon = _sentiment_emoji(result.sentiment)
    lines.append(f"> 📅 {date_str} | {sentiment_icon} 市场情绪：{result.sentiment or '—'}")
    lines.append("")

    if result.core_conclusion:
        lines.append("## 💡 核心观点")
        lines.append("")
        lines.append(f"**{result.core_conclusion}**")
        lines.append("")

    if result.indices:
        lines.append("## 📈 主要指数")
        lines.append("")
        lines.append("| 指数 | 收盘 | 涨跌幅 | 涨跌额 |")
        lines.append("|------|------|--------|--------|")
        for idx in result.indices:
            icon = _change_icon(idx.change_pct)
            sign = "+" if idx.change_pct > 0 else ""
            lines.append(f"| {icon} {idx.name} | {idx.close:.2f} | {sign}{idx.change_pct:.2f}% | {sign}{idx.change_amt:.2f} |")
        lines.append("")

    stat = result.statistics
    if stat.up_count > 0 or stat.down_count > 0:
        total = stat.up_count + stat.down_count + stat.flat_count
        up_ratio = stat.up_count / total if total > 0 else 0
        down_ratio = stat.down_count / total if total > 0 else 0
        flat_ratio = stat.flat_count / total if total > 0 else 0

        lines.append("## 📊 市场统计")
        lines.append("")
        lines.append(f"| 上涨 🟢 | 下跌 🔴 | 平盘 ⚪ | 涨停 🔥 | 跌停 ❄️ |")
        lines.append(f"|---------|---------|---------|---------|---------|")
        lines.append(f"| {stat.up_count} | {stat.down_count} | {stat.flat_count} "
                     f"| {stat.limit_up_count} | {stat.limit_down_count} |")
        lines.append("")
        lines.append("**涨跌比例**：")
        bar_width = 30
        up_fill = round(up_ratio * bar_width)
        down_fill = round(down_ratio * bar_width)
        flat_fill = bar_width - up_fill - down_fill
        lines.append(f"```")
        lines.append(f"  🟢 上涨 {up_ratio:.1%}  {'█' * up_fill}")
        lines.append(f"  ⚪ 平盘 {flat_ratio:.1%}  {'█' * flat_fill}")
        lines.append(f"  🔴 下跌 {down_ratio:.1%}  {'█' * down_fill}")
        lines.append(f"```")
        lines.append("")

    if result.top_sectors or result.bottom_sectors:
        lines.append("## 🔥 板块排名")
        lines.append("")

        if result.top_sectors:
            max_pct = max(abs(s.change_pct) for s in result.top_sectors) if result.top_sectors else 1
            lines.append("**领涨板块**：")
            lines.append("")
            for s in result.top_sectors:
                bar_len = max(1, round(s.change_pct / max_pct * 15)) if max_pct > 0 else 0
                lines.append(f"  🔥 {s.name:<8} {'█' * bar_len} +{s.change_pct:.2f}%  龙头：{s.lead_stock or '—'}")
            lines.append("")

        if result.bottom_sectors:
            max_pct = max(abs(s.change_pct) for s in result.bottom_sectors) if result.bottom_sectors else 1
            lines.append("**领跌板块**：")
            lines.append("")
            for s in result.bottom_sectors:
                bar_len = max(1, round(abs(s.change_pct) / max_pct * 15)) if max_pct > 0 else 0
                lines.append(f"  ❄️ {s.name:<8} {'░' * bar_len} {s.change_pct:.2f}%  龙头：{s.lead_stock or '—'}")
            lines.append("")

    if result.strategy:
        lines.append("## 🎯 操作建议")
        lines.append("")
        lines.append(result.strategy)
        lines.append("")

    if result.raw_report:
        lines.append("## 📝 详细复盘")
        lines.append("")
        lines.append(result.raw_report)
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(f"⚠️ {result.disclaimer}")

    return "\n".join(lines)


def save_report(result: Union[StockAnalysisResult, MarketAnalysisResult],
                output_dir: Union[str, None] = None) -> str:
    if output_dir is None:
        output_dir = _ensure_reports_dir()
    else:
        os.makedirs(output_dir, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")

    if isinstance(result, StockAnalysisResult):
        code = result.stock_code or "unknown"
        filename = f"{code}_{today}.md"
        content = generate_stock_report(result)
    elif isinstance(result, MarketAnalysisResult):
        filename = f"market_{today}.md"
        content = generate_market_report(result)
    else:
        raise ValueError(f"不支持的结果类型: {type(result)}")

    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    logger.info("报告已保存: %s", filepath)
    return filepath
