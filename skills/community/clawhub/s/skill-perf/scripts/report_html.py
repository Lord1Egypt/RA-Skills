#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
report_html.py
--------------
生成专业的 HTML 性能测试报告。
被 snapshot.py 调用，也可独立使用。

用法:
    # 从 snapshot.py 调用
    python3 snapshot.py report --session agent:main:cron:xxx --html

    # 独立使用
    python3 report_html.py --json '{"tokens":...}' --output report.html
"""

import json
import html as html_mod
from datetime import datetime
from pathlib import Path


def _fmt(n) -> str:
    """格式化数字，加千分位"""
    if isinstance(n, (int, float)):
        return f"{n:,.0f}" if isinstance(n, float) and n == int(n) else f"{n:,}"
    return str(n)


def _pct_bar(pct: float, color: str = "#4f46e5") -> str:
    """生成百分比进度条 HTML"""
    pct = max(0, min(100, pct))
    return f'''<div class="pct-bar">
        <div class="pct-fill" style="width:{pct}%;background:{color}"></div>
        <span class="pct-label">{pct:.1f}%</span>
    </div>'''


_OPENCLAW_ICON_B64 = (
    "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"
)


def _detect_billing_model(model: str, provider: str) -> str:
    """
    根据 model / modelProvider 字段推断计费模型类型。
    返回: 'kimi' | 'bailian' | 'minimax' | 'anthropic' | 'unknown'
    """
    m = (model or "").lower()
    p = (provider or "").lower()

    # 百炼（DashScope）托管的模型：隐式缓存，命中 0.20×（非 Kimi 原生的 0.10×）
    if "bailian" in p:
        return "bailian"
    if "kimi" in m or "moonshot" in m or "kimi" in p:
        return "kimi"
    if "claude" in m or "anthropic" in p:
        return "anthropic"
    if "minimax" in m or "minimax" in p:
        return "minimax"
    # fallback: treat unknown endpoints as kimi-compatible (most OpenClaw deployments)
    return "kimi"


# 计费系数表：cache_read_coeff, cache_write_coeff, note
_BILLING_PROFILES = {
    "kimi": {
        "cache_read_coeff":  0.10,  # 命中折扣 90%（Kimi 原生接口）
        "cache_write_coeff": 1.00,  # 无写入溢价（全自动缓存）
        "cache_write_label": "无溢价（自动缓存）",
        "provider_name": "Kimi K2.5 / Moonshot AI（原生）",
        "note": "Kimi 自动 Prompt Cache，命中按 0.1×，无缓存写入溢价",
        "disclaimer": "Kimi 原生接口自动缓存，折扣 90%（0.10×）",
    },
    "bailian": {
        "cache_read_coeff":  0.20,  # 百炼隐式缓存命中折扣 80%（注意：非 10%）
        "cache_write_coeff": 1.00,  # 隐式缓存无写入溢价
        "cache_write_label": "无溢价（隐式自动缓存）",
        "provider_name": "阿里云百炼 (Bailian / DashScope)",
        "note": "百炼隐式缓存自动生效，命中按 0.20×（折扣 80%），低于 Kimi/Anthropic 的 0.10×",
        "disclaimer": "百炼显式缓存命中为 0.10×；此处按默认隐式缓存（0.20×）估算。若 cacheWrite>0 则走显式缓存，应改用 0.10×",
    },
    "minimax": {
        "cache_read_coeff":  0.10,
        "cache_write_coeff": 1.25,
        "cache_write_label": "溢价 1.25×（需 cache_control）",
        "provider_name": "MiniMax",
        "note": "MiniMax Prompt Caching，命中 0.1×，写入 1.25×",
        "disclaimer": "MiniMax 需显式 cache_control 配置",
    },
    "anthropic": {
        "cache_read_coeff":  0.10,
        "cache_write_coeff": 1.25,
        "cache_write_label": "溢价 1.25×（需 cache_control）",
        "provider_name": "Anthropic Claude",
        "note": "Anthropic Prompt Caching，命中 0.1×，写入 1.25×",
        "disclaimer": "折扣系数来自 Anthropic 官方定价文档",
    },
    "unknown": {
        "cache_read_coeff":  0.10,
        "cache_write_coeff": 1.25,
        "cache_write_label": "溢价 1.25×（假设）",
        "provider_name": "未知提供商",
        "note": "无法识别模型提供商，使用 Kimi/Anthropic 默认系数（0.1× / 1.25×）",
        "disclaimer": "⚠️ 无法识别模型，按通用系数估算，建议手动确认",
    },
}


def _cache_status_badge(status: str) -> str:
    """Cache 状态徽章"""
    colors = {
        "warm": ("#059669", "#d1fae5", "🟢"),
        "cold": ("#2563eb", "#dbeafe", "🔵"),
        "partial": ("#d97706", "#fef3c7", "🟡"),
        "none": ("#6b7280", "#f3f4f6", "⚪"),
    }
    fg, bg, icon = colors.get(status, ("#6b7280", "#f3f4f6", "⚪"))
    return f'<span class="badge" style="background:{bg};color:{fg}">{icon} {status}</span>'


def _confidence_card_html(conf: dict) -> str:
    """置信度分析卡片 HTML"""
    if not conf:
        return ""
    level = conf.get("level", "medium")
    score = conf.get("score", 50)
    level_icon = conf.get("level_icon", "🟡")
    level_text = conf.get("level_text", "中")
    interpretation = html_mod.escape(conf.get("interpretation", ""))
    net = conf.get("net", 0)
    net_ratio = conf.get("net_ratio_pct", 0)

    # 颜色映射
    colors = {"high": "#34d399", "medium": "#fbbf24", "low": "#f87171"}
    bg_colors = {"high": "rgba(52,211,153,0.08)", "medium": "rgba(251,191,36,0.08)", "low": "rgba(248,113,113,0.08)"}
    border_colors = {"high": "rgba(52,211,153,0.3)", "medium": "rgba(251,191,36,0.3)", "low": "rgba(248,113,113,0.3)"}
    clr = colors.get(level, "#fbbf24")
    bg = bg_colors.get(level, "rgba(251,191,36,0.08)")
    border = border_colors.get(level, "rgba(251,191,36,0.3)")

    # 评分仪表盘
    gauge_html = f'''<div style="text-align:center;margin-bottom:0.75rem">
        <div style="font-size:2.5rem;line-height:1">{level_icon}</div>
        <div style="font-size:1.5rem;font-weight:700;color:{clr}">{score}</div>
        <div style="font-size:0.7rem;color:var(--text-dim)">/ 100  {level_text}置信度</div>
    </div>'''

    # 评分条
    bar_html = _pct_bar(score, clr)

    # 影响因素列表
    factor_rows = ""
    for f in conf.get("factors", []):
        factor_icon = html_mod.escape(f.get("icon", ""))
        factor_name = html_mod.escape(f.get("name", ""))
        factor_val = html_mod.escape(f.get("value", ""))
        factor_detail = html_mod.escape(f.get("detail", ""))
        factor_rows += f'''<tr>
            <td style="white-space:nowrap">{factor_icon} {factor_name}</td>
            <td><strong>{factor_val}</strong><br><span style="font-size:0.75rem;color:var(--text-dim)">{factor_detail}</span></td>
        </tr>'''

    # 警告列表
    warnings_html = ""
    if conf.get("warnings"):
        w_items = "".join(f"<li style='margin-bottom:0.25rem'>{html_mod.escape(w)}</li>" for w in conf["warnings"])
        warnings_html = f'''<div style="margin-top:0.75rem;padding:0.6rem 0.75rem;background:rgba(251,191,36,0.08);border-left:3px solid #fbbf24;border-radius:4px">
            <div style="font-size:0.75rem;font-weight:600;color:#fbbf24;margin-bottom:0.3rem">⚠️ 注意事项</div>
            <ul style="font-size:0.78rem;color:var(--text-dim);padding-left:1rem">{w_items}</ul>
        </div>'''

    return f'''<div class="section" style="background:{bg};border:1px solid {border}">
    <h2>🔍 数据置信度分析</h2>
    <div style="display:grid;grid-template-columns:auto 1fr;gap:1.5rem;align-items:start">
        <div style="min-width:120px">
            {gauge_html}
            {bar_html}
        </div>
        <div>
            <p style="color:var(--text);margin-bottom:0.75rem">{interpretation}</p>
            <table>
                <tr><th>因素</th><th>说明</th></tr>
                {factor_rows}
            </table>
            {warnings_html}
        </div>
    </div>
</div>'''


def _anomaly_card(anomaly: dict) -> str:
    """异常卡片"""
    is_warn = anomaly.get("level") == "warn"
    cls = "anomaly-warn" if is_warn else "anomaly-info"
    icon = "⚠️" if is_warn else "ℹ️"
    return f'''<div class="anomaly-card {cls}">
        <span class="anomaly-icon">{icon}</span>
        <div>
            <code>{anomaly.get("code", "")}</code>
            <p>{html_mod.escape(anomaly.get("message", ""))}</p>
        </div>
    </div>'''


def _calibration_history_html(history: list, current_noise: int, is_subagent: bool = False) -> str:
    """生成标定历史表格 HTML（只显示最近 5 条）"""
    if not history:
        return ""
    recent = history[-5:]
    rows = ""
    total_count = len(history)
    title_note = "subagent 标定历史（今天跑的记录，历史仅作参考）" if is_subagent else "标定历史（底噪使用本次标定，历史仅作参考）"
    for idx, h in enumerate(recent):
        i = total_count - len(recent) + idx + 1
        noise = h.get("noise", 0)
        total = h.get("total_tokens", noise)  # subagent_history 没有 total_tokens，用 noise 代替
        diff = noise - current_noise
        diff_str = f"+{diff:,}" if diff > 0 else f"{diff:,}" if diff < 0 else "0"
        diff_color = "var(--red)" if abs(diff) > 500 else "var(--text-dim)"
        ts = h.get("calibrated_at", "")[:16]
        is_used = (noise == current_noise)
        row_style = " style=\"background:rgba(52,211,153,0.08)\"" if is_used else ""
        latest_badge = " <span style='font-size:0.65rem;background:#d1fae5;color:#059669;padding:1px 5px;border-radius:3px;vertical-align:middle'>used</span>" if is_used else ""
        total_cell = "-" if is_subagent else _fmt(total)
        rows += f"""<tr{row_style}>
            <td>#{i}{latest_badge}</td>
            <td class="num">{total_cell}</td>
            <td class="num">{_fmt(noise)}</td>
            <td class="num" style="color:{diff_color}">{diff_str}</td>
            <td style="color:var(--text-dim);font-size:0.75rem">{ts}</td>
        </tr>"""
    return f"""<div style="margin-top:0.75rem">
        <div style="font-size:0.75rem;color:var(--text-dim);margin-bottom:0.3rem">{title_note}</div>
        <table>
            <tr><th>#</th><th style="text-align:right">totalTokens</th><th style="text-align:right">noise</th><th style="text-align:right">偏差</th><th>时间</th></tr>
            {rows}
        </table>
    </div>"""


def _noise_breakdown_html(cache_r: int, input_t: int, output_t: int,
                          skills_prompt_tokens: int, skills_count: int, noise: int) -> str:
    """生成底噪构成推算 HTML 块"""
    if not (cache_r > 0 and skills_prompt_tokens > 0):
        return ""
    fw = max(0, cache_r - skills_prompt_tokens)
    msg_out = input_t + output_t
    est = round(cache_r * 0.1 + msg_out)

    def pct(v): return f"{round(v / max(1, noise) * 100, 1):.1f}%"

    return (
        '<div class="noise-explain" style="margin-top:0">'
        f'<p style="font-size:0.8rem"><strong>底噪 = {_fmt(noise)} tokens（计费口径）的构成推算</strong><br>'
        f'实际 System Prompt ≈ {_fmt(cache_r)} tokens（cacheRead），按 0.1× 折扣计费：</p>'
        '<table style="font-size:0.8rem;margin-top:0.5rem">'
        '<tr><th>组成部分</th><th style="text-align:right">Tokens（原始）</th>'
        '<th style="text-align:right">折扣计费</th><th>占底噪</th></tr>'
        f'<tr><td>技能清单描述（{skills_count} 个 skill 的 name+desc）</td>'
        f'<td class="num" style="color:var(--blue)">{_fmt(skills_prompt_tokens)}</td>'
        f'<td class="num">~{_fmt(round(skills_prompt_tokens * 0.1))}</td>'
        f'<td style="color:var(--text-dim)">{pct(skills_prompt_tokens * 0.1)}</td></tr>'
        f'<tr><td>框架层（工具描述、安全指令、运行时元数据）</td>'
        f'<td class="num" style="color:var(--blue)">{_fmt(fw)}</td>'
        f'<td class="num">~{_fmt(round(fw * 0.1))}</td>'
        f'<td style="color:var(--text-dim)">{pct(fw * 0.1)}</td></tr>'
        f'<tr><td>任务消息 + LLM 输出（不可缓存）</td>'
        f'<td class="num">{_fmt(msg_out)}</td>'
        f'<td class="num">{_fmt(msg_out)}</td>'
        f'<td style="color:var(--text-dim)">{pct(msg_out)}</td></tr>'
        '<tr style="border-top:2px solid var(--border)">'
        '<td><strong>合计（估算底噪）</strong></td><td class="num"></td>'
        f'<td class="num" style="color:var(--orange)"><strong>~{_fmt(est)}</strong></td>'
        f'<td style="color:var(--text-dim)">实测={_fmt(noise)}</td></tr>'
        '</table>'
        '<p style="font-size:0.72rem;margin-top:0.5rem;color:var(--text-dim)">'
        '注：框架层不可直接测量，通过 cacheRead − 技能清单推算。实测底噪用空 skill 标定。</p>'
        '</div>'
    )


def _bootstrap_files_html(bootstrap_files: list, bootstrap_total_tokens: int, cache_r: int) -> str:
    """渲染 Bootstrap 文件构成表格"""
    if not bootstrap_files:
        return ""

    existing = [f for f in bootstrap_files if f["exists"]]
    if not existing:
        return ""

    max_tokens = max((f["tokens"] for f in existing), default=1) or 1

    rows = ""
    for f in bootstrap_files:
        fname = f["name"]
        tokens = f["tokens"]
        chars  = f["chars"]
        exists = f["exists"]
        if not exists:
            rows += f"<tr style='opacity:0.35'><td><code>{html_mod.escape(fname)}</code></td><td colspan='3' style='color:var(--text-dim);font-size:0.8rem'>— 不存在</td></tr>\n"
            continue
        bar_pct = round(tokens / max_tokens * 100, 1)
        pct_of_cache = f"{tokens / max(cache_r, 1) * 100:.1f}%" if cache_r > 0 else "—"
        bar = f'<div style="background:rgba(99,102,241,0.3);border-radius:3px;height:6px;width:{bar_pct}%;min-width:2px;display:inline-block"></div>'
        rows += (
            f"<tr>"
            f"<td><code style='color:var(--accent)'>{html_mod.escape(fname)}</code></td>"
            f"<td class='num'>{_fmt(tokens)}</td>"
            f"<td style='padding-left:0.5rem;vertical-align:middle'>{bar}</td>"
            f"<td style='color:var(--text-dim);font-size:0.8rem'>{_fmt(chars)} chars / {pct_of_cache} of cacheRead</td>"
            f"</tr>\n"
        )

    total_pct_of_cache = f"{bootstrap_total_tokens / max(cache_r, 1) * 100:.1f}%" if cache_r > 0 else "—"
    return f"""
<div class="noise-explain" style="margin-top:1rem;padding:0.9rem 1rem 0.75rem">
    <div style="font-size:0.8rem;font-weight:600;color:var(--text);margin-bottom:0.6rem">
        📁 Bootstrap 文件构成（{len(existing)} 个文件，共 {_fmt(bootstrap_total_tokens)} tokens，占 cacheRead 约 {total_pct_of_cache}）
    </div>
    <div style="font-size:0.75rem;color:var(--text-dim);margin-bottom:0.75rem;line-height:1.6">
        以下文件每次都完整注入 system prompt（构成 cacheRead 的主要来源之一）。
        单文件上限 20,000 字符，所有文件总上限 150,000 字符。
    </div>
    <table style="font-size:0.82rem;width:100%">
        <tr style="color:var(--text-dim);font-size:0.72rem;text-transform:uppercase;letter-spacing:0.05em">
            <th style="text-align:left;padding-bottom:0.4rem">文件</th>
            <th style="text-align:right;padding-bottom:0.4rem">Tokens</th>
            <th style="padding-bottom:0.4rem"></th>
            <th style="text-align:left;padding-bottom:0.4rem">详情</th>
        </tr>
        {rows}
        <tr style="border-top:1px dashed var(--border);font-weight:600">
            <td>合计</td>
            <td class="num" style="color:var(--accent)">{_fmt(bootstrap_total_tokens)}</td>
            <td></td>
            <td style="color:var(--text-dim);font-size:0.8rem">≈ {total_pct_of_cache} of cacheRead</td>
        </tr>
    </table>
</div>"""


def _donut_chart_html(segments: list, title: str = "", size: int = 180) -> str:
    """
    生成内联 SVG 甜甜圈图。
    segments: [{"label": str, "value": int, "color": str}, ...]
    """
    import math
    total = sum(s["value"] for s in segments)
    if total <= 0:
        return ""

    cx = cy = size / 2
    r_outer = size / 2 - 4
    r_inner = r_outer * 0.58
    stroke_w = r_outer - r_inner

    def polar(cx, cy, r, deg):
        rad = math.radians(deg - 90)
        return cx + r * math.cos(rad), cy + r * math.sin(rad)

    def arc_path(cx, cy, r, start_deg, end_deg):
        large = 1 if (end_deg - start_deg) > 180 else 0
        x1, y1 = polar(cx, cy, r, start_deg)
        x2, y2 = polar(cx, cy, r, end_deg)
        return f"M {x1:.2f} {y1:.2f} A {r:.2f} {r:.2f} 0 {large} 1 {x2:.2f} {y2:.2f}"

    def segment_path(cx, cy, r_outer, r_inner, start_deg, end_deg):
        x1o, y1o = polar(cx, cy, r_outer, start_deg)
        x2o, y2o = polar(cx, cy, r_outer, end_deg)
        x2i, y2i = polar(cx, cy, r_inner, end_deg)
        x1i, y1i = polar(cx, cy, r_inner, start_deg)
        large = 1 if (end_deg - start_deg) > 180 else 0
        return (f"M {x1o:.2f} {y1o:.2f} "
                f"A {r_outer:.2f} {r_outer:.2f} 0 {large} 1 {x2o:.2f} {y2o:.2f} "
                f"L {x2i:.2f} {y2i:.2f} "
                f"A {r_inner:.2f} {r_inner:.2f} 0 {large} 0 {x1i:.2f} {y1i:.2f} Z")

    paths = []
    cur = 0.0
    for seg in segments:
        pct = seg["value"] / total
        end = cur + pct * 360
        # avoid full circle (360 = no arc)
        end_draw = min(end, cur + pct * 360 - 0.01) if pct >= 1.0 else end
        d = segment_path(cx, cy, r_outer, r_inner, cur, end_draw)
        paths.append(f'<path d="{d}" fill="{seg["color"]}" opacity="0.9"/>')
        cur = end

    # legend rows
    legend_items = ""
    for seg in segments:
        pct = seg["value"] / total * 100
        legend_items += (
            f'<div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.35rem">'
            f'<div style="width:10px;height:10px;border-radius:2px;background:{seg["color"]};flex-shrink:0"></div>'
            f'<div style="font-size:0.78rem;color:var(--text-dim);flex:1">{html_mod.escape(seg["label"])}</div>'
            f'<div style="font-size:0.78rem;font-weight:600;color:var(--text)">{_fmt(seg["value"])}</div>'
            f'<div style="font-size:0.72rem;color:var(--text-dim);min-width:3.5rem;text-align:right">{pct:.1f}%</div>'
            f'</div>'
        )

    title_svg = f'<text x="{cx:.1f}" y="{cy - 6:.1f}" text-anchor="middle" font-size="11" fill="var(--text-dim)">{html_mod.escape(title)}</text>' if title else ""
    total_svg = f'<text x="{cx:.1f}" y="{cy + 10:.1f}" text-anchor="middle" font-size="13" font-weight="600" fill="var(--text)">{_fmt(total)}</text>'

    svg = (
        f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">'
        + "".join(paths)
        + title_svg + total_svg
        + "</svg>"
    )

    return (
        f'<div style="display:flex;align-items:center;gap:1.5rem;flex-wrap:wrap;margin-top:0.75rem">'
        f'<div style="flex-shrink:0">{svg}</div>'
        f'<div style="flex:1;min-width:160px">{legend_items}</div>'
        f'</div>'
    )


def _cache_breakdown_html(cache_r: int, sp_breakdown: dict,
                          bootstrap_total_tokens: int,
                          skills_prompt_tokens: int) -> str:
    """
    渲染 cacheRead 构成饼图。
    使用 systemPromptReport 数据 + 实测 bootstrap/skills。
    """
    if cache_r <= 0:
        return ""

    bs_tok     = bootstrap_total_tokens or sp_breakdown.get("bootstrap_tokens", 0)
    skills_tok = skills_prompt_tokens or sp_breakdown.get("skills_list_tokens", 0)
    tools_tok  = sp_breakdown.get("tools_tokens", 0)
    # framework = 剩余部分（不可直接测量，通过差值推算）
    known = bs_tok + skills_tok + tools_tok
    framework_tok = max(0, cache_r - known)

    segments = [
        {"label": f"框架层指令 (OpenClaw 内部)",   "value": framework_tok, "color": "#818cf8"},
        {"label": f"工具 JSON Schema ({sp_breakdown.get('tools_count', '?')} 个工具)",
                                                   "value": tools_tok,     "color": "#f472b6"},
        {"label": f"技能描述列表 ({sp_breakdown.get('skills_count', '?')} 个 skill)",
                                                   "value": skills_tok,    "color": "#60a5fa"},
        {"label": f"Bootstrap 文件 ({len([1])} 组)", "value": bs_tok,       "color": "#34d399"},
    ]
    # filter zero
    segments = [s for s in segments if s["value"] > 0]

    chart = _donut_chart_html(segments, title="cacheRead", size=170)
    note = (
        "<div style='font-size:0.72rem;color:var(--text-dim);margin-top:0.6rem;line-height:1.6'>"
        "⚠️ <strong>框架层指令</strong>为 OpenClaw 内部内容，不可直接测量，通过"
        " <code>cacheRead − 可测量部分</code> 推算。"
        " Bootstrap 文件 + 技能描述 + 工具 Schema 是可直接读取并计算的部分。"
        "</div>"
    )
    return (
        "<div class='noise-explain' style='margin-top:0.75rem'>"
        "<div style='font-size:0.82rem;font-weight:600;color:var(--text);margin-bottom:0.25rem'>"
        "🥧 cacheRead 构成分析</div>"
        + chart + note +
        "</div>"
    )


def _hero_stacked_bar(total_t: int, cache_billed: int, input_t: int,
                      output_t: int, noise: int) -> str:
    """
    Full-width stacked bar inside hero showing how total_t is composed:
    [cacheRead×coeff] [inputTokens] [outputTokens] [底噪]
    The bar makes it visual why input+output ≠ total.
    """
    if total_t <= 0:
        return ""
    net = max(0, total_t - noise)
    segs = [
        {"label": f"Cache 折算 ({cache_billed:,})", "value": cache_billed, "color": "#34d399"},
        {"label": f"Input ({input_t:,})", "value": input_t, "color": "#818cf8"},
        {"label": f"Output ({output_t:,})", "value": output_t, "color": "#f472b6"},
        {"label": f"底噪 ({noise:,})", "value": noise, "color": "#fbbf24"},
    ]
    segs = [s for s in segs if s["value"] > 0]

    bars = ""
    legend = ""
    for s in segs:
        pct = s["value"] / total_t * 100
        bars += f'<div class="hero-bar-seg" style="width:{pct:.2f}%;background:{s["color"]};opacity:0.85"></div>'
        legend += (
            f'<div class="hero-bar-item">'
            f'<div class="hero-bar-dot" style="background:{s["color"]}"></div>'
            f'{html_mod.escape(s["label"])} <span style="opacity:0.6">({pct:.1f}%)</span>'
            f'</div>'
        )

    return (
        f'<div class="hero-bar">'
        f'<div style="font-size:0.65rem;color:var(--text-dim);margin-bottom:0.3rem;letter-spacing:0.05em;text-transform:uppercase">'
        f'Total {_fmt(total_t)} 的构成</div>'
        f'<div class="hero-bar-track">{bars}</div>'
        f'<div class="hero-bar-legend">{legend}</div>'
        f'</div>'
    )


def _step_breakdown_html(steps: list, net_tokens: int) -> str:
    """
    生成步骤 token 估算区块（Top3 高亮）。
    steps: _analyze_step_breakdown() 返回的列表
    net_tokens: skill 净消耗（用于计算各步骤占比）
    """
    if not steps:
        return ""

    # 过滤掉空步骤，按 est_tokens 降序排列
    valid = [s for s in steps if s.get("est_tokens", 0) > 0]
    if not valid:
        return ""

    total_est = sum(s["est_tokens"] for s in valid)
    sorted_steps = sorted(valid, key=lambda s: s["est_tokens"], reverse=True)
    top3_indices = {s["index"] for s in sorted_steps[:3]}

    # 颜色映射
    TOOL_COLORS = {
        "read":    "#60a5fa",   # blue
        "exec":    "#a78bfa",   # purple
        "process": "#f472b6",   # pink
        "write":   "#fbbf24",   # orange
        "browser": "#34d399",   # green
    }
    ROLE_COLORS = {
        "assistant": "#818cf8",
        "user":      "#94a3b8",
    }

    def _step_color(step: dict) -> str:
        tn = step.get("tool_name", "")
        role = step.get("role", "")
        for k, c in TOOL_COLORS.items():
            if k in tn.lower():
                return c
        return ROLE_COLORS.get(role, "#64748b")

    def _step_label(step: dict) -> str:
        tn = step.get("tool_name", "")
        role = step.get("role", "")
        hint = step.get("hint", "")  # snapshot.py 提取的参数摘要
        if role == "toolResult" and tn:
            label = html_mod.escape(tn)
            if hint:
                short = html_mod.escape(hint[:40] + ("…" if len(hint) > 40 else ""))
                label += f" <span style='color:var(--text-dim);font-weight:400;font-size:0.8em'>({short})</span>"
            return label
        return html_mod.escape(role or "?")

    rows_html = ""
    for s in valid:  # 按调用顺序（index 原始顺序），Top3 高亮
        color = _step_color(s)
        est = s["est_tokens"]
        chars = s["chars"]
        pct_of_total = est / total_est * 100 if total_est > 0 else 0
        pct_of_net = est / net_tokens * 100 if net_tokens > 0 else 0
        is_top3 = s["index"] in top3_indices
        rank = next((i + 1 for i, x in enumerate(sorted_steps[:3]) if x["index"] == s["index"]), None)

        medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, "") if is_top3 else ""
        highlight_style = "background:rgba(251,191,36,0.06);border-left:2px solid #fbbf24;" if is_top3 else ""

        bar_w = min(100, pct_of_total)
        rows_html += f"""
        <tr style="{highlight_style}">
          <td style="color:{color};font-weight:{'600' if is_top3 else '400'};white-space:nowrap">
            {medal} {_step_label(s)}
          </td>
          <td style="text-align:right;font-variant-numeric:tabular-nums;color:var(--text-dim)">{chars:,}</td>
          <td style="text-align:right;font-variant-numeric:tabular-nums;color:{color};font-weight:{'700' if is_top3 else '400'}">~{est:,}</td>
          <td style="width:120px;padding-left:0.5rem">
            <div style="background:var(--border);border-radius:4px;height:6px;overflow:hidden">
              <div style="width:{bar_w:.1f}%;background:{color};height:100%;border-radius:4px"></div>
            </div>
          </td>
          <td style="text-align:right;color:var(--text-dim);font-size:0.8em">{pct_of_net:.0f}%</td>
        </tr>"""

    return f"""<div class="section">
  <h2>🔬 各步骤 Token 估算 <span style="font-size:0.72em;font-weight:400;color:var(--text-dim);margin-left:0.5rem">⚠️ 估算值（字符数÷2.67），仅供参考</span></h2>
  <p style="color:var(--text-dim);font-size:0.82em;margin-bottom:1rem">
    基于 sessions_history 消息内容字符数估算（chars ÷ 2.67，按 50% 中文 + 50% 英文混合比例：中文 ~2 chars/token，英文 ~4 chars/token，加权平均 ~2.67 chars/token）。实际误差约 ±20%。
    合计估算 <strong style="color:var(--text)">{_fmt(total_est)} tokens</strong>，净消耗 <strong style="color:var(--green)">{_fmt(net_tokens)} tokens</strong>。
  </p>
  <table style="width:100%">
    <thead>
      <tr style="color:var(--text-dim);font-size:0.78em">
        <th style="text-align:left;padding-bottom:0.5rem">步骤</th>
        <th style="text-align:right">字符数</th>
        <th style="text-align:right">估算 tokens</th>
        <th style="padding-left:0.5rem">占比</th>
        <th style="text-align:right">占净消耗</th>
      </tr>
    </thead>
    <tbody>{rows_html}
    </tbody>
  </table>
  <p style="margin-top:0.75rem;font-size:0.78em;color:var(--text-dim)">
    🥇🥈🥉 = Top3 消耗步骤 · 占净消耗% = 该步骤估算 token ÷ NET_TOKENS
  </p>
</div>"""


def generate_html_report(data: dict, report_type: str = "report") -> str:
    """
    生成完整的 HTML 报告。

    data: 报告数据，包含 tokens, diagnostics 等
    report_type: "report" (Cron session) 或 "after" (before/after delta)
    """
    tokens = data.get("tokens", data.get("delta", {}))
    diag = data.get("diagnostics", {})
    ca = diag.get("cache_analysis", {})
    eff = diag.get("efficiency", {})
    meta = diag.get("session_metadata", {})
    anomalies = diag.get("anomalies", [])
    recs = diag.get("recommendations", [])
    summary = data.get("summary", {})
    cal = data.get("calibration", {})
    conf = data.get("confidence", {})

    # 从数据中获取 job_name 和被测 skill
    job_name = data.get("job_name", "")
    skill_name = data.get("skill_name", "")

    # 基本信息
    title = data.get("label", data.get("session_key", "Skill Performance Report"))
    model = meta.get("model", data.get("model", ""))[:50]
    provider = meta.get("model_provider", "")
    ts = data.get("updated_at") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    duration = data.get("duration_sec", summary.get("duration_sec", ""))

    # 从 session_key 提取 agent 名称
    session_key = data.get("session_key", meta.get("session_id", ""))
    # session_key 格式: agent:<agentId>:cron:xxx  或 agent:<agentId>:main
    _sk_parts = session_key.split(":")
    if len(_sk_parts) >= 2 and _sk_parts[0] == "agent":
        agent_id = _sk_parts[1]
    else:
        agent_id = "main"  # 默认

    # 直接使用 agent_id 作为显示名，不做硬编码映射
    agent_display = agent_id

    # 计费模型识别
    billing_type = _detect_billing_model(model, provider)
    billing = _BILLING_PROFILES[billing_type]
    cr_coeff = billing["cache_read_coeff"]
    cw_coeff = billing["cache_write_coeff"]

    total_t = tokens.get("total", tokens.get("total_delta", 0))
    input_t = tokens.get("input", 0)
    output_t = tokens.get("output", 0)
    cache_r = tokens.get("cache_read", 0)
    cache_w = tokens.get("cache_write", 0)
    noise = tokens.get("system_noise", summary.get("system_noise", 0))
    # net_t: 优先从字段读，但若字段缺失或为 0 而 noise>0 则直接用 total-noise 重算
    _net_field = tokens.get("net_tokens", summary.get("net_skill_tokens", None))
    if _net_field is not None and (_net_field > 0 or noise == 0):
        net_t = _net_field
    else:
        net_t = max(0, total_t - noise)

    ctx_window = meta.get("context_window", 0)
    ctx_usage = meta.get("context_usage_pct", 0)
    skills_count = meta.get("registered_skills_count", 0)

    cache_hit = ca.get("cache_hit_rate", 0)
    cache_status = ca.get("cache_status", "none")
    cache_savings = ca.get("estimated_savings", 0)
    savings_pct = ca.get("savings_pct", 0)

    output_ratio = eff.get("output_ratio", 0)
    net_ratio = eff.get("net_ratio", 0)

    skills_prompt_tokens = data.get("skills_prompt_tokens", 0)
    bootstrap_files  = data.get("bootstrap_files", [])
    bootstrap_total_tokens = data.get("bootstrap_total_tokens", 0)
    bootstrap_total_chars  = data.get("bootstrap_total_chars", 0)
    sp_breakdown = data.get("system_prompt_breakdown", {})
    task_message_tokens = data.get("task_message_tokens", 0)
    # 实际发给模型的总 input = cacheRead + inputTokens
    total_input_sent = cache_r + input_t
    # 优先用本次实际底噪：只要 noise > 0 就用（自动识别伴侣 or --noise 参数皆可）
    noise_source = data.get("noise_source", "")
    _cal_noise_file = cal.get("calibration_noise", noise)
    if noise > 0:
        # 本次有实测底噪（自动识别标定伴侣 或 --noise 参数），优先显示
        cal_noise = noise
        cal_at = data.get("updated_at", "")
        cal_at_label = "本次测量"
    else:
        cal_noise = _cal_noise_file
        cal_at = cal.get("calibrated_at", "")
        cal_at_label = ""
    cal_runs = cal.get("runs_averaged", 0)
    # subagent 报告优先显示 subagent_history（今天跑的记录）
    subagent_history = data.get("subagent_history", [])
    cal_history = subagent_history if subagent_history else cal.get("history", [])
    cal_skill_tokens = cal.get("calibration_skill_md_tokens", 338)
    is_calibrated = cal_noise > 0

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>📊 skill-perf | {html_mod.escape(str(title))}</title>
<style>
:root {{
    --bg: #0f172a;
    --card: #1e293b;
    --card-hover: #334155;
    --border: #334155;
    --text: #e2e8f0;
    --text-dim: #94a3b8;
    --accent: #818cf8;
    --accent-bg: rgba(129,140,248,0.1);
    --green: #34d399;
    --green-bg: rgba(52,211,153,0.1);
    --blue: #60a5fa;
    --blue-bg: rgba(96,165,250,0.1);
    --orange: #fbbf24;
    --orange-bg: rgba(251,191,36,0.1);
    --red: #f87171;
    --red-bg: rgba(248,113,113,0.1);
    --pink: #f472b6;
}}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', Roboto, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
    padding: 2rem;
    max-width: 960px;
    margin: 0 auto;
}}
.header {{
    text-align: center;
    margin-bottom: 1.5rem;
    padding-bottom: 1.25rem;
    border-bottom: 1px solid var(--border);
}}
.header h1 {{
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--accent);
    margin-bottom: 0.4rem;
}}
.header .subtitle {{
    color: var(--text-dim);
    font-size: 0.82rem;
    word-break: break-all;
}}
.header .meta {{
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 1rem 2rem;
    margin-top: 0.6rem;
    font-size: 0.78rem;
    color: var(--text-dim);
}}
.header .meta span {{ display: flex; align-items: center; gap: 0.3rem; }}

/* ── Hero block ── */
.hero {{
    background: linear-gradient(135deg, rgba(52,211,153,0.12) 0%, rgba(52,211,153,0.04) 100%);
    border: 2px solid rgba(52,211,153,0.35);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
}}
.hero-main {{
    flex: 1;
    min-width: 200px;
}}
.hero-label {{
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--green);
    opacity: 0.8;
    margin-bottom: 0.2rem;
}}
.hero-value {{
    font-size: 4rem;
    font-weight: 800;
    color: var(--green);
    line-height: 1;
    font-variant-numeric: tabular-nums;
    letter-spacing: -0.02em;
}}
.hero-unit {{
    font-size: 1.2rem;
    font-weight: 400;
    color: var(--green);
    opacity: 0.7;
    margin-left: 0.3rem;
}}
.hero-formula {{
    font-size: 0.82rem;
    color: var(--text-dim);
    margin-top: 0.5rem;
    font-family: 'SF Mono', 'Fira Code', monospace;
}}
.hero-formula .hl-total {{ color: var(--accent); font-weight: 600; }}
.hero-formula .hl-noise {{ color: var(--orange); font-weight: 600; }}
.hero-formula .hl-net {{ color: var(--green); font-weight: 700; }}
.hero-side {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.6rem 1.2rem;
    min-width: 220px;
}}
.hero-stat {{
    display: flex;
    flex-direction: column;
}}
.hero-stat-label {{
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: var(--text-dim);
}}
.hero-stat-value {{
    font-size: 1.2rem;
    font-weight: 700;
    font-variant-numeric: tabular-nums;
}}
.hero-bar {{
    margin-top: 1rem;
    width: 100%;
}}
.hero-bar-track {{
    display: flex;
    height: 8px;
    border-radius: 4px;
    overflow: hidden;
    gap: 1px;
    background: rgba(255,255,255,0.05);
}}
.hero-bar-seg {{
    height: 100%;
    transition: width 0.5s ease;
}}
.hero-bar-legend {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.25rem 1rem;
    margin-top: 0.4rem;
}}
.hero-bar-item {{
    display: flex;
    align-items: center;
    gap: 0.3rem;
    font-size: 0.65rem;
    color: var(--text-dim);
}}
.hero-bar-dot {{
    width: 7px;
    height: 7px;
    border-radius: 2px;
    flex-shrink: 0;
}}
/* ── Flow diagram ── */
.flow-section {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1.5rem;
}}
.flow-section h2 {{
    font-size: 0.9rem;
    font-weight: 600;
    margin-bottom: 1rem;
    color: var(--text-dim);
    text-transform: uppercase;
    letter-spacing: 0.06em;
}}
.flow-row {{
    display: flex;
    align-items: stretch;
    gap: 0;
    flex-wrap: wrap;
}}
.flow-box {{
    background: rgba(255,255,255,0.04);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.85rem 1.1rem;
    flex: 1;
    min-width: 130px;
}}
.flow-box-label {{
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: var(--text-dim);
    margin-bottom: 0.2rem;
}}
.flow-box-value {{
    font-size: 1.25rem;
    font-weight: 700;
    font-variant-numeric: tabular-nums;
}}
.flow-arrow {{
    display: flex;
    align-items: center;
    padding: 0 0.5rem;
    color: var(--text-dim);
    font-size: 1.2rem;
    flex-shrink: 0;
}}
.flow-sub {{
    font-size: 0.72rem;
    color: var(--text-dim);
    margin-top: 0.15rem;
    line-height: 1.4;
}}

.section {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1.5rem;
}}
.section h2 {{
    font-size: 0.9rem;
    font-weight: 600;
    margin-bottom: 0.75rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid var(--border);
    color: var(--text);
}}
.two-col {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
}}
@media (max-width: 640px) {{
    .two-col {{ grid-template-columns: 1fr; }}
    .hero {{ flex-direction: column; gap: 1rem; padding: 1.5rem; }}
    .hero-value {{ font-size: 3rem; }}
}}

table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85rem;
}}
th, td {{
    padding: 0.55rem 0.6rem;
    text-align: left;
    border-bottom: 1px solid var(--border);
}}
th {{
    color: var(--text-dim);
    font-weight: 500;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}
td {{ font-variant-numeric: tabular-nums; }}
td.num {{ text-align: right; font-family: 'SF Mono', 'Fira Code', monospace; }}
tr:last-child td {{ border-bottom: none; }}
tr:hover td {{ background: rgba(255,255,255,0.02); }}

.badge {{
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    padding: 0.2rem 0.6rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
}}
.pct-bar {{
    position: relative;
    height: 8px;
    background: var(--border);
    border-radius: 4px;
    overflow: hidden;
    min-width: 100px;
}}
.pct-fill {{
    height: 100%;
    border-radius: 4px;
    transition: width 0.6s ease;
}}
.pct-label {{
    position: absolute;
    right: -3rem;
    top: -0.15rem;
    font-size: 0.7rem;
    color: var(--text-dim);
    white-space: nowrap;
}}
.pct-row {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
}}

.anomaly-card {{
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    margin-bottom: 0.5rem;
    font-size: 0.85rem;
}}
.anomaly-card code {{
    font-size: 0.7rem;
    padding: 0.1rem 0.4rem;
    border-radius: 4px;
    background: rgba(255,255,255,0.1);
}}
.anomaly-card p {{ margin-top: 0.25rem; color: var(--text-dim); }}
.anomaly-warn {{ background: var(--orange-bg); border-left: 3px solid var(--orange); }}
.anomaly-info {{ background: var(--blue-bg); border-left: 3px solid var(--blue); }}
.anomaly-icon {{ font-size: 1.1rem; flex-shrink: 0; }}

.rec-list {{ list-style: none; }}
.rec-list li {{
    padding: 0.5rem 0.75rem;
    margin-bottom: 0.4rem;
    background: var(--accent-bg);
    border-radius: 6px;
    font-size: 0.85rem;
    border-left: 3px solid var(--accent);
}}
.rec-list li::before {{
    content: "💡";
    margin-right: 0.5rem;
}}

.footer {{
    text-align: center;
    padding-top: 1.5rem;
    color: var(--text-dim);
    font-size: 0.75rem;
}}
.footer a {{ color: var(--accent); text-decoration: none; }}

.noise-explain {{
    background: rgba(248,113,113,0.05);
    border: 1px solid rgba(248,113,113,0.2);
    border-radius: 8px;
    padding: 0.75rem 1rem;
    margin-bottom: 1rem;
    font-size: 0.875rem;
    color: var(--text-dim);
    line-height: 1.7;
}}
.noise-explain strong {{ color: var(--text); }}
.noise-explain code {{
    background: rgba(255,255,255,0.08);
    padding: 0.1rem 0.4rem;
    border-radius: 4px;
    font-size: 0.8rem;
}}

.formula-box {{
    background: rgba(251,191,36,0.06);
    border: 1px solid rgba(251,191,36,0.25);
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
    text-align: center;
}}
.formula-title {{
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-dim);
    margin-bottom: 0.75rem;
}}
.formula, .formula-detail {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
    font-family: 'SF Mono', 'Fira Code', monospace;
}}
.formula {{ font-size: 1.1rem; font-weight: 600; margin-bottom: 0.4rem; }}
.formula-detail {{ font-size: 0.85rem; color: var(--text-dim); }}
.formula span:not(.formula-var) {{ color: var(--text-dim); }}
.formula-var {{ font-weight: 700; }}
.formula-var.green {{ color: var(--green); }}
.formula-var.accent {{ color: var(--accent); }}
.formula-var.orange {{ color: var(--orange); }}

details summary {{
    cursor: pointer;
    font-size: 0.82rem;
    color: var(--text-dim);
    padding: 0.3rem 0;
    user-select: none;
}}
details summary:hover {{ color: var(--text); }}
details[open] summary {{ margin-bottom: 0.75rem; color: var(--text); }}
</style>
</head>
<body>

<div class="header">
    <div style="display:flex;align-items:center;justify-content:center;gap:0.6rem;margin-bottom:0.5rem">
        <img src="data:image/png;base64,{_OPENCLAW_ICON_B64}" width="24" height="24" style="border-radius:5px;flex-shrink:0" alt="OpenClaw">
        <span style="font-size:0.75rem;color:var(--text-dim);letter-spacing:0.05em">OpenClaw · skill-perf</span>
    </div>
    <h1>Skill Performance Report</h1>
    <div class="subtitle">{html_mod.escape(str(title))}</div>
    <div class="meta">
        {"<span style='font-size:1rem;font-weight:700;color:var(--green)'>🧪 " + html_mod.escape(job_name) + "</span>" if job_name else ""}
        {"<span style='font-weight:600;color:var(--accent)'>📦 被测 Skill: " + html_mod.escape(skill_name) + "</span>" if skill_name else ""}
        <span>🤖 {html_mod.escape(agent_display)}</span>
        <span>🕐 {html_mod.escape(str(ts))}</span>
        {"<span>⏱ " + str(duration) + "s</span>" if duration else ""}
        <span style="color:{'#f87171' if not is_calibrated else 'inherit'}">{"⚠️ 未标定（使用默认底噪）" if not is_calibrated else "✅ 已标定"}</span>
    </div>
</div>

<!-- ═══ HERO: net_tokens ═══ -->
<div class="hero">
    <div style="display:flex;align-items:center;gap:2.5rem;flex-wrap:wrap;width:100%">
    <div class="hero-main">
        <div class="hero-label">{html_mod.escape(skill_name) if skill_name else (html_mod.escape(job_name) if job_name else "Skill")} 净消耗 (net_tokens)</div>
        <div class="hero-value">{_fmt(net_t)}<span class="hero-unit">tokens</span></div>
        <div class="hero-formula">
            <span class="hl-net">{_fmt(net_t)}</span>
            <span style="opacity:0.5"> = </span>
            <span class="hl-total">{_fmt(total_t)}</span>
            <span style="opacity:0.4"> − </span>
            <span class="hl-noise">{_fmt(noise)}</span>
            <span style="opacity:0.4;font-size:0.75rem"> (totalTokens − 底噪)</span>
        </div>
    </div>
    <div class="hero-side">
        <div class="hero-stat">
            <span class="hero-stat-label">Input (新鲜)</span>
            <span class="hero-stat-value" style="color:var(--accent)">{_fmt(input_t)}</span>
        </div>
        <div class="hero-stat">
            <span class="hero-stat-label">Output (生成)</span>
            <span class="hero-stat-value" style="color:var(--pink)">{_fmt(output_t)}</span>
        </div>
        <div class="hero-stat">
            <span class="hero-stat-label">Cache 折算计费</span>
            <span class="hero-stat-value" style="color:var(--green)">{_fmt(round(cache_r * cr_coeff))}</span>
        </div>
        <div class="hero-stat">
            <span class="hero-stat-label">底噪 (扣除)</span>
            <span class="hero-stat-value" style="color:var(--orange)">{_fmt(noise)}</span>
        </div>
        <div class="hero-stat">
            <span class="hero-stat-label">Total (计费)</span>
            <span class="hero-stat-value" style="color:var(--text-dim)">{_fmt(total_t)}</span>
        </div>
        <div class="hero-stat">
            <span class="hero-stat-label">Cache 命中率</span>
            <span class="hero-stat-value" style="color:var(--blue)">{cache_hit:.0f}<span style="font-size:0.75rem;font-weight:400">%</span></span>
        </div>
    </div>
    </div>
    {_hero_stacked_bar(total_t, round(cache_r * cr_coeff), input_t, output_t, noise)}
</div>

<!-- ═══ TOKEN FLOW ═══ -->
<div class="flow-section">
    <h2>Token 流向 — 本次任务花了什么</h2>
    <div class="flow-row">
        <div class="flow-box">
            <div class="flow-box-label">📨 发送给 LLM</div>
            <div class="flow-box-value" style="color:var(--accent)">{_fmt(cache_r + input_t)}</div>
            <div class="flow-sub">
                cacheRead {_fmt(cache_r)} <span style="opacity:0.5">({int(cache_r/(cache_r+input_t+0.001)*100)}%)</span><br>
                inputTokens {_fmt(input_t)} <span style="opacity:0.5">({int(input_t/(cache_r+input_t+0.001)*100)}%)</span>
                {"<br><span style='opacity:0.6'>└ 任务消息 ~" + _fmt(task_message_tokens) + " / 其余 ~" + _fmt(max(0,input_t-task_message_tokens)) + "</span>" if task_message_tokens > 0 else ""}
            </div>
        </div>
        <div class="flow-arrow">→</div>
        <div class="flow-box" style="border-color:rgba(96,165,250,0.4)">
            <div class="flow-box-label">🧠 LLM</div>
            <div class="flow-box-value" style="color:var(--blue)">处理中</div>
            <div class="flow-sub">{html_mod.escape(str(provider or model[:20]))}<br>cache 命中 {cache_hit:.0f}%</div>
        </div>
        <div class="flow-arrow">→</div>
        <div class="flow-box">
            <div class="flow-box-label">📤 输出 (output)</div>
            <div class="flow-box-value" style="color:var(--pink)">{_fmt(output_t)}</div>
            <div class="flow-sub">LLM 生成内容<br>占总计费 {output_ratio:.1f}%</div>
        </div>
        <div class="flow-arrow" style="font-size:1.5rem;font-weight:700;color:var(--green)">⇒</div>
        <div class="flow-box" style="background:rgba(52,211,153,0.08);border-color:rgba(52,211,153,0.4)">
            <div class="flow-box-label">✅ 净消耗</div>
            <div class="flow-box-value" style="color:var(--green)">{_fmt(net_t)}</div>
            <div class="flow-sub">扣除底噪 {_fmt(noise)}<br>= net_tokens</div>
        </div>
    </div>
</div>

<!-- ═══ 两列：计费明细 + 参考信息 ═══ -->
<div class="two-col">
    <div class="section">
        <h2>💰 计费明细</h2>
        <div style="font-size:0.72rem;color:var(--text-dim);margin-bottom:0.6rem">
            计费模型：<strong style="color:var(--text)">{billing["provider_name"]}</strong>
            <span style="margin-left:0.5rem;background:{"#dbeafe" if billing_type=="kimi" else "#fef3c7"};color:{"#1d4ed8" if billing_type=="kimi" else "#92400e"};padding:1px 6px;border-radius:4px;font-size:0.7rem">
                {billing_type.upper()}{"（默认）" if billing_type=="unknown" else ""}
            </span>
        </div>
        <table>
            <tr><th>字段</th><th style="text-align:right">值</th><th>说明</th></tr>
            <tr style="background:rgba(52,211,153,0.06)">
                <td><strong style="color:var(--green)">net_tokens</strong></td>
                <td class="num" style="color:var(--green);font-weight:700">{_fmt(net_t)}</td>
                <td style="color:var(--text-dim)">skill 净消耗（去底噪）</td>
            </tr>
            <tr>
                <td>totalTokens</td>
                <td class="num" style="color:var(--accent)">{_fmt(total_t)}</td>
                <td style="color:var(--text-dim)">实际计费量</td>
            </tr>
            <tr>
                <td>inputTokens</td>
                <td class="num">{_fmt(input_t)}</td>
                <td style="color:var(--text-dim)">新鲜发送</td>
            </tr>
            <tr>
                <td>outputTokens</td>
                <td class="num">{_fmt(output_t)}</td>
                <td style="color:var(--text-dim)">LLM 生成</td>
            </tr>
            <tr style="background:rgba(52,211,153,0.03)">
                <td>cacheRead</td>
                <td class="num" style="color:var(--green)">{_fmt(cache_r)}</td>
                <td style="color:var(--text-dim)">{int((1-cr_coeff)*100)}% 折扣 ({cr_coeff}×)</td>
            </tr>
            <tr>
                <td>cacheWrite</td>
                <td class="num">{_fmt(cache_w)}</td>
                <td style="color:var(--text-dim)">{billing["cache_write_label"]}</td>
            </tr>
            <tr style="background:rgba(251,191,36,0.05)">
                <td>底噪</td>
                <td class="num" style="color:var(--orange)">{_fmt(noise)}</td>
                <td style="color:var(--text-dim)">{"已标定 (本次实测)" if noise_source == "--noise 参数" else ("已标定" if is_calibrated else "⚠️ 默认值未标定")}</td>
            </tr>
        </table>
        <div style="font-size:0.68rem;color:var(--text-dim);margin-top:0.5rem;padding-top:0.4rem;border-top:1px dashed var(--border)">
            💡 {html_mod.escape(billing["disclaimer"])}
        </div>
    </div>

    <div class="section">
        <h2>🔍 Cache &amp; 效率</h2>
        <table>
            <tr><td>Cache 状态</td><td>{_cache_status_badge(cache_status)}</td></tr>
            <tr>
                <td>命中率</td>
                <td class="pct-row">{_pct_bar(cache_hit, "#34d399")}</td>
            </tr>
            {"<tr><td>节省估算</td><td style='color:var(--green)'>" + _fmt(cache_savings) + " tokens</td></tr>" if cache_savings > 0 else ""}
            <tr>
                <td>Output 占比</td>
                <td class="pct-row">{_pct_bar(output_ratio, "#f472b6")}</td>
            </tr>
            <tr>
                <td>净消耗占比</td>
                <td class="pct-row">{_pct_bar(net_ratio, "#818cf8")}</td>
            </tr>
            {"<tr><td>输出速率</td><td>" + f'{eff.get("output_tokens_per_sec", 0):.1f}' + " tok/s</td></tr>" if "output_tokens_per_sec" in eff else ""}
        </table>
        <details style="margin-top:0.75rem">
            <summary>▸ cacheRead 构成分析</summary>
            {_cache_breakdown_html(cache_r, sp_breakdown, bootstrap_total_tokens, skills_prompt_tokens)}
        </details>
    </div>
</div>

{_confidence_card_html(conf)}

{_step_breakdown_html(data.get("step_breakdown", []), net_t)}

{"<div class='section'><h2>⚠️ 异常检测</h2>" + "".join(_anomaly_card(a) for a in anomalies) + "</div>" if anomalies else ""}

{"<div class='section'><h2>💡 优化建议</h2><ul class='rec-list'>" + "".join(f"<li>{html_mod.escape(r)}</li>" for r in recs) + "</ul></div>" if recs else ""}

<div class="section">
    <h2>🔬 底噪标定 (Baseline Noise)</h2>
    <div class="noise-explain">
        <p>底噪是每次 Cron isolated session 的<strong>固定开销</strong>，等于一个"空 skill"（无实际工作）所消耗的 totalTokens。
        不同的 OpenClaw 实例、agent 配置、甚至不同运行时刻，底噪都可能不同，<strong>需要在本机标定</strong>。</p>
    </div>
    <div class="formula-box">
        <div class="formula-title">净消耗计算公式</div>
        <div class="formula">
            <span class="formula-var green">net_tokens</span>
            <span>=</span>
            <span class="formula-var accent">totalTokens</span>
            <span>−</span>
            <span class="formula-var orange">底噪</span>
        </div>
        <div class="formula-detail">
            <span class="formula-var green">{_fmt(net_t)}</span>
            <span>=</span>
            <span class="formula-var accent">{_fmt(total_t)}</span>
            <span>−</span>
            <span class="formula-var orange">{_fmt(noise)}</span>
        </div>
    </div>
    {_noise_breakdown_html(cache_r, input_t, output_t, skills_prompt_tokens, skills_count, noise)}
    <table style="margin-top:1rem">
        <tr><th colspan="2">本机标定状态</th></tr>
        <tr><td>标定状态</td><td>{"<span class='badge' style='background:#d1fae5;color:#059669'>✅ 已标定</span> (使用本次标定值)" if is_calibrated else "<span class='badge' style='background:#fef3c7;color:#d97706'>⚠️ 未标定（使用默认值）</span>"}</td></tr>
        <tr><td>底噪值</td><td><strong style="color:var(--orange)">{_fmt(cal_noise)} tokens</strong></td></tr>
        {"<tr><td>标定时间</td><td>" + ("<span style='color:var(--green);font-weight:600'>" + html_mod.escape(cal_at_label) + "</span>") + "</td></tr>" if cal_at_label else ("<tr><td>标定时间</td><td>" + html_mod.escape(str(cal_at)[:19]) + "</td></tr>" if cal_at else "")}
        <tr><td>标定工具</td><td><code>skill-calibration</code> (SKILL.md = {cal_skill_tokens} tokens)</td></tr>
    </table>
    {_calibration_history_html(cal_history, cal_noise, is_subagent=bool(data.get("subagent_history"))) if cal_history else ""}
    <div class="noise-explain" style="margin-top:1rem">
        <p style="font-size:0.75rem"><strong>底噪受以下因素影响</strong>（环境变化后建议重新标定）：</p>
        <table style="font-size:0.8rem">
            <tr><td>🛠️ 工具数量</td><td>注册工具越多，工具描述越多（主要在框架层，占 ~97%）</td></tr>
            <tr><td>📚 技能数量</td><td>技能清单描述注入 system prompt{" (当前: " + str(skills_count) + " 个，约 " + _fmt(skills_prompt_tokens) + " tokens)" if skills_count else ""}</td></tr>
            <tr><td>📁 Workspace 文件</td><td>Bootstrap 文件（AGENTS.md / SOUL.md / MEMORY.md 等）每次全量注入{" (" + str(len([f for f in bootstrap_files if f["exists"]])) + " 个文件，共 " + _fmt(bootstrap_total_tokens) + " tokens，占 cacheRead 约 " + (f"{bootstrap_total_tokens/max(cache_r,1)*100:.1f}%" if cache_r else "?") + "，详见底部 Bootstrap 文件详情)" if bootstrap_files else ""}</td></tr>
            <tr><td>🤖 模型/提供商</td><td>不同 tokenizer 编码效率不同，cacheRetention 配置影响命中</td></tr>
            <tr><td>🔄 OpenClaw 版本</td><td>版本升级可能改变框架层 system prompt 内容</td></tr>
        </table>
        <p style="font-size:0.75rem;margin-top:0.5rem;color:var(--accent)"><strong>重新标定命令</strong>：<code>python3 calibrate.py auto</code> 或 <code>python3 calibrate.py save --total &lt;totalTokens&gt;</code></p>
    </div>
</div>

<div class="section">
    <h2>📦 Session 元数据</h2>
    <table>
        <tr style="background:rgba(129,140,248,0.08)"><td><strong>测试 Agent</strong></td><td><strong style="color:var(--accent)">{html_mod.escape(agent_display)}</strong> <span style="color:var(--text-dim);font-size:0.8rem">({html_mod.escape(session_key[:70])})</span></td></tr>
        {"<tr><td>模型</td><td><code>" + html_mod.escape(str(model)) + "</code></td></tr>" if model else ""}
        {"<tr><td>提供商</td><td>" + html_mod.escape(str(provider)) + "</td></tr>" if provider else ""}
        {"<tr><td>上下文窗口</td><td>" + _fmt(ctx_window) + " tokens</td></tr>" if ctx_window else ""}
        {"<tr><td>上下文使用率</td><td class='pct-row'>" + _pct_bar(ctx_usage, "#60a5fa" if ctx_usage < 80 else "#f87171") + "</td></tr>" if ctx_usage else ""}
        {"<tr><td>注册技能数</td><td>" + str(skills_count) + "</td></tr>" if skills_count else ""}
        <tr><td>系统底噪</td><td>{_fmt(noise)} tokens</td></tr>
    </table>
</div>

{"<div class='section'><h2>📁 Bootstrap 文件详情</h2>" + _bootstrap_files_html(bootstrap_files, bootstrap_total_tokens, cache_r) + "</div>" if bootstrap_files and any(f["exists"] for f in bootstrap_files) else ""}

<div class="footer">
    Generated by <a href="#">skill-perf</a> · {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
</div>

</body>
</html>'''


def save_html_report(data: dict, output_path: str = None, report_type: str = "report") -> str:
    """生成并保存 HTML 报告，返回文件路径"""
    html_content = generate_html_report(data, report_type)

    if output_path is None:
        reports_dir = Path.home() / ".openclaw" / "skills" / "skill-perf" / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        skill_name = data.get("skill_name") or data.get("label") or data.get("session_key", "")
        # 清理文件名
        safe_label = "".join(c if c.isalnum() or c in "-_" else "_" for c in str(skill_name))[:40] if skill_name else ""
        suffix = f"_{safe_label}" if safe_label else ""
        output_path = str(reports_dir / f"{ts}_report{suffix}.html")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(html_content, encoding="utf-8")
    return output_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="生成 HTML 性能报告")
    parser.add_argument("--json", required=True, help="报告 JSON 数据（文件路径或 JSON 字符串）")
    parser.add_argument("--output", "-o", default=None, help="输出 HTML 文件路径")
    args = parser.parse_args()

    # 支持文件路径或 JSON 字符串
    json_input = args.json
    if Path(json_input).exists():
        data = json.loads(Path(json_input).read_text(encoding="utf-8"))
    else:
        data = json.loads(json_input)

    path = save_html_report(data, args.output)
    print(f"✅ HTML 报告已生成: {path}")
