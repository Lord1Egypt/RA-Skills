"""
Markdown 输出渲染器 — 三种模式各自的模板。
"""
from __future__ import annotations

from datetime import datetime

from .indicators import derive_operation_levels, derive_stop_loss, judge_stance
from .portfolio import (
    calc_guarantee_ratio,
    grade_guarantee_ratio,
    risk_rank_key,
)


def _fmt_pnl(pct: float | None) -> str:
    if pct is None:
        return "-"
    return f"+{pct}%" if pct >= 0 else f"{pct}%"


# ====== 模式 P：持仓简报 ======

def render_portfolio(holdings: list[dict], total_mv: float, total_margin: float) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    md = [f"# 📊 盘前持仓简报 — {now}\n"]

    # 头部：总市值 + 融资 + 担保比例
    ratio = calc_guarantee_ratio(total_mv, total_margin)
    if ratio:
        md.append(
            f"**总市值**：¥{total_mv:,.0f} · "
            f"**融资余额**：¥{total_margin:,.0f} · "
            f"**担保比例**：**{ratio}%**\n"
        )
        md.append(f"### 担保比例评估: {grade_guarantee_ratio(ratio)}\n")
    else:
        md.append(f"**总市值**：¥{total_mv:,.0f}\n")

    # 公告告警（置顶）
    has_announce = any(h.get("announce") for h in holdings)
    if has_announce:
        md.append("## 📢 近 14 日重要公告告警\n")
        for h in holdings:
            for a in h.get("announce", []):
                emoji = "🔴" if a["level"] == "HIGH" else "🟡"
                md.append(
                    f"- {emoji} **{h['name']}** [{a.get('date','?')}] "
                    f"[{a.get('tag','')}] {a['title']}"
                )
        md.append("")
        md.append("> ⚠️ **以上公告可能影响评估，建议在技术面分析之上调整出手节奏。**\n")

    # 按风险排序
    holdings = sorted(holdings, key=risk_rank_key)

    # 一、实时态势
    md.append("## 一、持仓实时态势\n")
    md.append("| 股票 | 现价 | 涨跌幅 | 成本 | 浮盈% | 仓位% | 赛道 |")
    md.append("|------|-----:|-------:|-----:|------:|------:|------|")
    for h in holdings:
        rt = h.get("rt") or {}
        marks = []
        if h.get("is_heavy"): marks.append("🎯")
        if h.get("has_margin"): marks.append("🔥")
        if h.get("is_loss"): marks.append("📉")
        prefix = "".join(marks) or "🔵"
        md.append(
            f"| {prefix} {h['name']} {h['code']} | "
            f"{h.get('price','-')} | {rt.get('pct_change','-')}% | "
            f"{h.get('cost','-')} | {_fmt_pnl(h.get('pnl_pct'))} | "
            f"{h.get('weight','-')}% | {h.get('sector','')} |"
        )
    md.append("")

    # 二、关键均线 + 三档止损
    md.append("## 二、关键均线 + 三档硬止损\n")
    for h in holdings:
        hist = h.get("hist") or {}
        sl = h.get("sl") or {}
        flag = "🎯" if h.get("is_heavy") else ("🔥" if h.get("has_margin") else "🔵")
        md.append(
            f"### {flag} {h['name']} {h['code']} — "
            f"成本 {h.get('cost','-')} / 浮盈 {_fmt_pnl(h.get('pnl_pct'))}"
        )
        if hist.get("last"):
            ma20, last = hist.get("ma20"), hist.get("last")
            pos_state = ""
            if ma20 and last:
                pos_state = "✅ 站上 MA20" if last > ma20 else "⚠️ 跌破 MA20"
            md.append(
                f"- 现价 **{hist.get('last')}** {pos_state} | "
                f"MA5={hist.get('ma5','-')} MA10={hist.get('ma10','-')} "
                f"MA20={hist.get('ma20','-')} MA30={hist.get('ma30','-')}"
            )
            if hist.get("pct_40d") is not None:
                md.append(
                    f"- 40 日涨幅 **{hist.get('pct_40d')}%** | "
                    f"区间 {hist.get('low_n','-')} ~ {hist.get('high_n','-')}"
                )
        if sl:
            md.append(f"- 🚨 预警 **{sl.get('warn_line','-')}** → {sl.get('warn_action')}")
            md.append(f"- 🚨 风控 **{sl.get('risk_line','-')}** → {sl.get('risk_action')}")
            md.append(f"- 🚨 清仓 **{sl.get('cut_line','-')}** → {sl.get('cut_action')}")
        md.append("")

    # 三、操作清单
    md.append("## 三、📋 今早可执行的条件单\n")
    md.append("✅ **开盘前 5 分钟内设好**：")
    md.append("| 优先级 | 股票 | 触发位 | 动作 |")
    md.append("|:---:|------|-------:|------|")
    for h in holdings:
        sl = h.get("sl") or {}
        if not sl.get("risk_line"):
            continue
        if h.get("is_loss") and h.get("has_margin"):
            pri = "P0 🚨"
        elif h.get("is_heavy"):
            pri = "P1 🎯"
        elif h.get("has_margin"):
            pri = "P1 🔥"
        else:
            pri = "P2"
        md.append(f"| {pri} | {h['name']} | {sl['risk_line']} | {sl['risk_action']} |")
    md.append("")
    md.append("🔥 **融资管理**：担保比例 < 170% 主动降仓 / 优先还亏损票 / 强势票暂不还")
    md.append("")
    md.append("## 四、今晚问自己 3 个问题")
    md.append("1. 已经赚多少？是否到落袋点？")
    md.append("2. 哪只技术位最弱？能不能借反弹减？")
    md.append("3. 担保比例够不够安全？")
    return "\n".join(md)


# ====== 模式 S：单股深度 ======

def render_single(code: str, realtime: dict, hist: dict) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    name = realtime.get("name", code) if realtime else code
    md = [f"# 🔍 {name} {code} 实时分析 — {now}\n"]

    md.append("## 一、态势速判\n")
    md.append(f"**{judge_stance(realtime, hist)}**\n")

    md.append("## 二、技术面\n")
    if realtime:
        amount = realtime.get("amount", 0)
        amount_str = f"{amount/1e8:.2f} 亿" if amount and amount > 1e8 else f"{amount:.0f}"
        md.append(
            f"- 现价: **{realtime.get('price','-')}** | "
            f"涨跌幅: **{realtime.get('pct_change','-')}%** | "
            f"换手: {realtime.get('turnover_rate','-')}% | "
            f"成交额: {amount_str}"
        )
    if hist.get("ma5"):
        md.append(
            f"- 均线: MA5={hist.get('ma5')} MA10={hist.get('ma10')} "
            f"MA20={hist.get('ma20')} MA30={hist.get('ma30')}"
        )
    if hist.get("high_n"):
        md.append(f"- 近 N 日: 高 **{hist.get('high_n')}** / 低 **{hist.get('low_n')}**")
    if hist.get("pct_40d") is not None:
        md.append(f"- 40 日涨幅: **{hist.get('pct_40d')}%**")
    md.append("")

    md.append("## 三、操作位建议\n")
    levels = derive_operation_levels(realtime, hist)
    sl = derive_stop_loss(realtime, hist)
    if levels:
        md.append("| 类型 | 价位 | 触发动作 |")
        md.append("|------|-----:|---------|")
        md.append(f"| 介入位（MA10）| {levels.get('介入位','-')} | 站稳后小仓位试探 |")
        md.append(f"| 加仓位（前高）| {levels.get('加仓位','-')} | 突破前高确认 |")
        md.append(f"| 止损位（MA20）| {levels.get('止损位','-')} | 跌破后减仓 |")
        md.append(f"| 短线止盈位 | {levels.get('止盈位_短线','-')} | 触及落袋 1/3 |")
        md.append(f"| 波段止盈位 | {levels.get('止盈位_波段','-')} | 触及落袋 1/2 |")
    if sl:
        md.append(
            f"\n**止损三档**：预警 {sl['warn_line']} → "
            f"风控 {sl['risk_line']} → 清仓 {sl['cut_line']}"
        )
    md.append("")

    md.append("## 四、跟踪要点\n")
    md.append("- 关注是否站稳/跌破上方关键均线")
    md.append("- 关注量价是否共振（放量上涨为多头信号，缩量上涨警惕）")
    md.append("- 关注大盘环境与板块联动")
    return "\n".join(md)


# ====== 模式 M：多股对比 ======

def render_multi(rows: list[dict]) -> str:
    """rows: [{code, name, price, pct, ma5_dev, ma20_dev, turnover, pct_40d, score}, ...]"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    md = [f"# 📊 多股对比分析 — {now}\n"]

    rows = sorted(rows, key=lambda x: -x["score"])

    md.append("## 一、横向对比表\n")
    md.append(
        "| 排名 | 股票 | 现价 | 涨跌幅 | MA5偏离 | MA20偏离 | "
        "换手% | 40日涨幅 | 综合分 | 标签 |"
    )
    md.append(
        "|:---:|------|-----:|-------:|--------:|---------:|"
        "------:|---------:|-------:|------|"
    )
    for i, r in enumerate(rows, 1):
        if i == 1 and r["score"] > 3:
            tag = "⭐"
        elif r["score"] < -3:
            tag = "⚠️"
        else:
            tag = "🟡"
        md.append(
            f"| {i} | {r['name']} {r['code']} | {r['price']} | "
            f"{r['pct']}% | {r['ma5_dev']}% | {r['ma20_dev']}% | "
            f"{r['turnover']}% | {r['pct_40d']}% | {r['score']} | {tag} |"
        )
    md.append("")

    md.append("## 二、关键差异点\n")
    if len(rows) >= 2:
        top, bot = rows[0], rows[-1]
        md.append(f"- **{top['name']} vs {bot['name']}**：")
        md.append(
            f"  - {top['name']} 综合分 {top['score']}（强势特征：MA5偏离 "
            f"{top['ma5_dev']}% / 40日涨幅 {top['pct_40d']}%）"
        )
        md.append(
            f"  - {bot['name']} 综合分 {bot['score']}（偏弱：MA20偏离 "
            f"{bot['ma20_dev']}%）"
        )
    md.append("")

    md.append("## 三、判断（不构成投资建议）\n")
    if rows:
        md.append(f"- ⭐ **优势更明显**：{rows[0]['name']}")
        md.append(f"  理由：综合分 {rows[0]['score']}，量价/趋势/动能综合最优")
        if len(rows) > 2:
            md.append(f"- 🟡 **保持观察**：{rows[1]['name']}（综合分 {rows[1]['score']}）")
        if rows[-1]["score"] < 0:
            md.append(f"- ⚠️ **谨慎对待**：{rows[-1]['name']}（综合分 {rows[-1]['score']}）")
    return "\n".join(md)
