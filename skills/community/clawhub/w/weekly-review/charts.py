"""生成与定稿一致的两张辅助图（纯标准库 SVG）.

1. chart-时间分布-*.svg — 横向条形：本周时间投入分布
2. chart-归因Token-*.svg — 左右双柱：低效归因分布 + Token 消耗趋势
"""

from __future__ import annotations

import html
import re
from pathlib import Path
from typing import Any

FONT = "Segoe UI, Microsoft YaHei, PingFang SC, sans-serif"

# 与参考图接近的配色
COLORS_TIME = ["#E89A3C", "#2A9D8F", "#1D3557", "#A8B5C4", "#C5CAD1"]
COLORS_ATTR = ["#E89A3C", "#E07A7A", "#2A9D8F", "#A8B5C4"]
COLORS_TOKEN = ["#A8B5C4", "#2A9D8F", "#E89A3C"]


def _esc(s: str) -> str:
    return html.escape(str(s), quote=True)


def _parse_num(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value).replace(",", "").replace("约", "").replace("≈", "")
    if "万" in s:
        m = re.search(r"([\d.]+)", s)
        return float(m.group(1)) * 10000 if m else None
    m = re.search(r"([\d.]+)", s)
    return float(m.group(1)) if m else None


def _horizontal_bars(
    title: str,
    items: list[tuple[str, float]],
    *,
    xlabel: str,
    width: int = 900,
    height: int | None = None,
) -> str:
    """定稿风格：横向条形图，右侧标注「Xh · N%」."""
    if not items:
        items = [("无数据", 0.0)]
    items = sorted(items, key=lambda x: x[1], reverse=True)
    total = sum(v for _, v in items) or 1.0
    n = len(items)
    row_h = 48
    margin_l, margin_r, margin_t, margin_b = 160, 120, 64, 56
    height = height or (margin_t + margin_b + n * row_h + 8)
    plot_w = width - margin_l - margin_r
    plot_h = n * row_h
    vmax = max(v for _, v in items) * 1.15 or 1.0

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">',
        f'<rect width="100%" height="100%" fill="#FFFFFF"/>',
        f'<text x="{width/2}" y="36" text-anchor="middle" font-family="{FONT}" '
        f'font-size="20" font-weight="700" fill="#1A1A1A">{_esc(title)}</text>',
    ]

    # 竖向浅网格
    ticks = 9
    for i in range(ticks + 1):
        x = margin_l + plot_w * i / ticks
        val = vmax * i / ticks
        parts.append(
            f'<line x1="{x:.1f}" y1="{margin_t}" x2="{x:.1f}" '
            f'y2="{margin_t + plot_h}" stroke="#E8E8E8" stroke-width="1"/>'
        )
        parts.append(
            f'<text x="{x:.1f}" y="{margin_t + plot_h + 18}" text-anchor="middle" '
            f'font-family="{FONT}" font-size="11" fill="#888">{val:.0f}</text>'
        )

    # 轴线
    parts.append(
        f'<line x1="{margin_l}" y1="{margin_t}" x2="{margin_l}" '
        f'y2="{margin_t + plot_h}" stroke="#666" stroke-width="1.2"/>'
    )
    parts.append(
        f'<line x1="{margin_l}" y1="{margin_t + plot_h}" x2="{margin_l + plot_w}" '
        f'y2="{margin_t + plot_h}" stroke="#666" stroke-width="1.2"/>'
    )
    parts.append(
        f'<text x="{margin_l + plot_w/2}" y="{height - 14}" text-anchor="middle" '
        f'font-family="{FONT}" font-size="12" fill="#555">{_esc(xlabel)}</text>'
    )

    for i, (lab, val) in enumerate(items):
        y0 = margin_t + i * row_h + 10
        bar_h = 22
        bw = (val / vmax) * plot_w if vmax else 0
        color = COLORS_TIME[i] if i < len(COLORS_TIME) else COLORS_TIME[-1]
        parts.append(
            f'<text x="{margin_l - 10}" y="{y0 + bar_h - 4}" text-anchor="end" '
            f'font-family="{FONT}" font-size="13" fill="#222">{_esc(lab)}</text>'
        )
        parts.append(
            f'<rect x="{margin_l}" y="{y0}" width="{bw:.1f}" height="{bar_h}" '
            f'fill="{color}" rx="2"/>'
        )
        pct = 100.0 * val / total
        label = f"{val:.1f}h · {pct:.0f}%"
        parts.append(
            f'<text x="{margin_l + bw + 8:.1f}" y="{y0 + bar_h - 5}" '
            f'font-family="{FONT}" font-size="13" font-weight="600" '
            f'fill="#222">{_esc(label)}</text>'
        )

    parts.append("</svg>")
    return "\n".join(parts)


def _vertical_panel(
    title: str,
    items: list[tuple[str, float]],
    *,
    ylabel: str,
    colors: list[str],
    x: float,
    y: float,
    w: float,
    h: float,
    value_fmt: str = "{:.0f}",
) -> list[str]:
    """在大画布内画一个竖直柱状面板（无背景网格，数值在柱顶）."""
    if not items:
        items = [("无数据", 0.0)]
    margin_l, margin_r, margin_t, margin_b = 48, 16, 44, 78
    plot_w = w - margin_l - margin_r
    plot_h = h - margin_t - margin_b
    vmax = max(v for _, v in items) * 1.2 or 1.0
    n = len(items)
    gap = 18
    bar_w = max(28.0, (plot_w - gap * (n + 1)) / n)

    parts = [
        f'<text x="{x + w/2}" y="{y + 26}" text-anchor="middle" font-family="{FONT}" '
        f'font-size="15" font-weight="700" fill="#1A1A1A">{_esc(title)}</text>',
        f'<line x1="{x + margin_l}" y1="{y + margin_t}" x2="{x + margin_l}" '
        f'y2="{y + margin_t + plot_h}" stroke="#555" stroke-width="1.2"/>',
        f'<line x1="{x + margin_l}" y1="{y + margin_t + plot_h}" '
        f'x2="{x + margin_l + plot_w}" y2="{y + margin_t + plot_h}" '
        f'stroke="#555" stroke-width="1.2"/>',
        f'<text x="{x + 14}" y="{y + margin_t + plot_h/2}" text-anchor="middle" '
        f'transform="rotate(-90 {x + 14} {y + margin_t + plot_h/2})" '
        f'font-family="{FONT}" font-size="11" fill="#555">{_esc(ylabel)}</text>',
    ]

    # y ticks（无网格线，仅刻度）
    for i in range(5):
        yy = y + margin_t + plot_h - plot_h * i / 4
        val = vmax * i / 4
        parts.append(
            f'<text x="{x + margin_l - 6}" y="{yy + 4:.1f}" text-anchor="end" '
            f'font-family="{FONT}" font-size="10" fill="#888">{val:.1f}</text>'
        )

    for i, (lab, val) in enumerate(items):
        bx = x + margin_l + gap + i * (bar_w + gap)
        bh = (val / vmax) * plot_h if vmax else 0
        by = y + margin_t + plot_h - bh
        color = colors[i % len(colors)]
        parts.append(
            f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bar_w:.1f}" height="{bh:.1f}" '
            f'fill="{color}" rx="2"/>'
        )
        parts.append(
            f'<text x="{bx + bar_w/2:.1f}" y="{by - 6:.1f}" text-anchor="middle" '
            f'font-family="{FONT}" font-size="12" font-weight="700" fill="#222">'
            f"{_esc(value_fmt.format(val))}</text>"
        )
        # 多行标签：按固定宽度折行
        lines = _wrap_label(lab, 6)
        for li, line in enumerate(lines[:3]):
            parts.append(
                f'<text x="{bx + bar_w/2:.1f}" y="{y + margin_t + plot_h + 16 + li * 14}" '
                f'text-anchor="middle" font-family="{FONT}" font-size="11" '
                f'fill="#333">{_esc(line)}</text>'
            )
    return parts


def _wrap_label(text: str, max_chars: int) -> list[str]:
    text = str(text)
    if len(text) <= max_chars:
        return [text]
    lines: list[str] = []
    buf = ""
    for ch in text:
        buf += ch
        if len(buf) >= max_chars:
            lines.append(buf)
            buf = ""
    if buf:
        lines.append(buf)
    return lines


def _dual_vertical(
    left_title: str,
    left_items: list[tuple[str, float]],
    right_title: str,
    right_items: list[tuple[str, float]],
    *,
    width: int = 1100,
    height: int = 480,
) -> str:
    """定稿风格：左右并排两张竖直柱状图."""
    mid = width / 2
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#FFFFFF"/>',
    ]
    parts.extend(
        _vertical_panel(
            left_title,
            left_items,
            ylabel="条目数",
            colors=COLORS_ATTR,
            x=0,
            y=8,
            w=mid - 10,
            h=height - 16,
            value_fmt="{:.0f}",
        )
    )
    parts.extend(
        _vertical_panel(
            right_title,
            right_items,
            ylabel="百万 token",
            colors=COLORS_TOKEN,
            x=mid + 10,
            y=8,
            w=mid - 20,
            h=height - 16,
            value_fmt="{:.2f}",
        )
    )
    parts.append("</svg>")
    return "\n".join(parts)


def _collect_time_items(data: dict[str, Any]) -> tuple[list[tuple[str, float]], float]:
    charts = data.get("charts_data") or {}
    raw = charts.get("time_distribution") or charts.get("时间分布")
    items: list[tuple[str, float]] = []
    if raw:
        for row in raw:
            lab = str(row.get("label") or row.get("name") or "—")
            h = _parse_num(row.get("hours") if row.get("hours") is not None else row.get("value"))
            if h is not None:
                items.append((lab, h))
    if not items:
        for p in data.get("projects") or []:
            title = str(p.get("title") or p.get("name") or "主题")
            h = _parse_num(title) or _parse_num(p.get("hours"))
            if h is None:
                continue
            short = title.split("（")[0].split("(")[0].strip()
            items.append((short, h))
        for o in data.get("other_projects") or []:
            h = _parse_num(o.get("hours"))
            if h is not None:
                items.append((str(o.get("name") or "其他"), h))
    active = sum(v for _, v in items)
    d = data.get("dashboard") or {}
    if d.get("active_hours") is not None:
        active = float(d["active_hours"])
    elif d.get("metrics"):
        for m in d["metrics"]:
            if "真实活跃" in str(m.get("name") or ""):
                parsed = _parse_num(m.get("value"))
                if parsed is not None:
                    active = parsed
                break
    return items, active


def _collect_attribution(data: dict[str, Any]) -> list[tuple[str, float]]:
    charts = data.get("charts_data") or {}
    raw = charts.get("attribution") or charts.get("低效归因")
    if raw:
        out: list[tuple[str, float]] = []
        for row in raw:
            lab = str(row.get("label") or row.get("name") or "—")
            c = _parse_num(row.get("count") if row.get("count") is not None else row.get("value"))
            if c is not None:
                out.append((lab, c))
        if out:
            return out
    # 从 problems 的 root_cause / category 聚合
    counts: dict[str, float] = {}
    for p in data.get("problems") or []:
        lab = str(p.get("root_cause") or p.get("category") or "未分类")
        # 拼成参考图风格：【用户】指令模糊
        cat = str(p.get("category") or "")
        root = str(p.get("root_cause") or "")
        if cat and root and cat not in root:
            lab = f"{cat}{root}" if "【" in cat else f"{cat} {root}"
        elif cat:
            lab = cat
        counts[lab] = counts.get(lab, 0) + 1
    return list(counts.items()) or [("暂无", 0)]


def _collect_token_trend(data: dict[str, Any]) -> list[tuple[str, float]]:
    charts = data.get("charts_data") or {}
    raw = charts.get("token_trend") or charts.get("Token趋势")
    if raw:
        out: list[tuple[str, float]] = []
        for row in raw:
            lab = str(row.get("label") or row.get("name") or "—")
            v = row.get("millions")
            if v is None:
                v = row.get("value")
            num = _parse_num(v)
            if num is not None:
                # 若给的是原始 token，转百万
                if num > 100:
                    num = num / 1_000_000
                out.append((lab, num))
        if out:
            return out
    # 仅本周：从 dashboard Token 推一个点
    d = data.get("dashboard") or {}
    week = 0.0
    if d.get("tokens") is not None:
        t = _parse_num(d["tokens"]) or 0
        week = t / 1_000_000 if t > 100 else t
    elif d.get("metrics"):
        for m in d["metrics"]:
            if "Token" in str(m.get("name") or ""):
                t = _parse_num(m.get("value")) or 0
                week = t / 1_000_000 if t > 100 else t
                break
    return [("前两周", 0.0), ("上周", 0.0), ("本周", week)]


def build_chart_payloads(data: dict[str, Any]) -> dict[str, str]:
    period = data.get("period") or {}
    end = period.get("end") or "week"
    time_items, active = _collect_time_items(data)
    attr_items = _collect_attribution(data)
    token_items = _collect_token_trend(data)

    time_svg = _horizontal_bars(
        f"本周时间投入分布 (真实活跃 ≈ {active:.0f}h)",
        time_items or [("未分类", active or 1.0)],
        xlabel="真实活跃时长 (小时，已剔除挂机 idle)",
    )
    dual_svg = _dual_vertical(
        "本周低效条目归因分布",
        attr_items,
        "Token 消耗趋势（百万）",
        token_items,
    )
    return {
        f"chart-时间分布-{end}.svg": time_svg,
        f"chart-归因Token-{end}.svg": dual_svg,
    }


def write_charts(data: dict[str, Any], charts_dir: str | Path) -> list[str]:
    out_dir = Path(charts_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    names: list[str] = []
    for name, svg in build_chart_payloads(data).items():
        (out_dir / name).write_text(svg, encoding="utf-8")
        names.append(name)
    return names
