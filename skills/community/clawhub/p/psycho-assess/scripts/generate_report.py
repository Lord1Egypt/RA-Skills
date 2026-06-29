#!/usr/bin/env python3
"""
心理测评 HTML 报告生成器
将评分结果 JSON 注入 HTML 模板，生成最终可视化报告

用法: python generate_report.py --results '<json_string>' --output <file.html>
       python generate_report.py --results-file '<json_path>' --output <file.html>
"""

import json
import sys
import os
from datetime import datetime


def get_template_path():
    """Get template path relative to this script"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "..", "assets", "report_template.html")


def bar_color(score, max_score):
    """Get color based on score ratio"""
    ratio = score / max_score
    if ratio < 0.2:
        return "#22C55E"
    elif ratio < 0.4:
        return "#22C55E"
    elif ratio < 0.6:
        return "#EAB308"
    elif ratio < 0.8:
        return "#F97316"
    else:
        return "#EF4444"


def bfi_dim_color(score):
    """Color for Big Five dimensions"""
    if score >= 4:
        return "#3B82F6"  # blue
    elif score >= 3:
        return "#EAB308"  # yellow
    elif score >= 2:
        return "#F97316"  # orange
    else:
        return "#8B5CF6"  # purple


def generate_report(results, date_str=""):
    """Generate complete HTML report from scoring results"""
    template_path = get_template_path()
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"模板文件不存在: {template_path}")

    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()

    if not date_str:
        date_str = datetime.now().strftime("%Y年%m月%d日 %H:%M")

    html = html.replace("{{DATE}}", date_str)

    # --- Summary Grid ---
    summary_parts = []
    scales_to_show = ["PHQ-9", "GAD-7", "PSS-10", "RSES"]
    for sk in scales_to_show:
        if sk in results and "total_score" in results[sk]:
            r = results[sk]
            t = r.get("threshold", {})
            summary_parts.append(
                f'<div class="summary-item">'
                f'<div class="summary-dot" style="background:{t.get("color","#94A3B8")}"></div>'
                f'<div><div class="label">{r["name"]}</div>'
                f'<div style="font-size:12px;color:#64748B;">{t.get("severity","")}</div></div>'
                f'<div class="value" style="margin-left:auto;">{r["total_score"]}<span style="font-size:12px;font-weight:400;color:#94A3B8">/{r["max_score"]}</span></div>'
                f'</div>'
            )
    html = html.replace("{{SUMMARY_GRID}}", "\n".join(summary_parts))

    # --- Scale Results ---
    scale_html_parts = []
    for sk in scales_to_show:
        if sk in results and "total_score" in results[sk]:
            r = results[sk]
            t = r.get("threshold", {})
            color = t.get("color", "#94A3B8")
            pct = r.get("percentage", 0)

            # Determine interpretation box style
            box_class = "info" if pct < 30 else ("caution" if pct < 60 else "warning")

            # PHQ-9 Q9 warning
            q9_html = ""
            if r.get("q9_warning"):
                q9_html = '<div class="q9-warning"><span class="icon">⚠️</span><span>检测到PHQ-9第9题（自伤念头）非"完全不会"回答，这是一个需要特别关注的信号。如果您正在经历自伤念头，请立即联系心理援助热线或前往医院。</span></div>'

            scale_html_parts.append(
                f'<div class="card">'
                f'<h2>{r["name"]}</h2>'
                f'<div class="score-row">'
                f'<div class="score-badge" style="background:{color}">'
                f'<span class="num">{r["total_score"]}</span>'
                f'<span class="unit">/{r["max_score"]}</span>'
                f'</div>'
                f'<div style="flex:1;min-width:200px;">'
                f'<div class="progress-bar"><div class="progress-fill" style="width:{pct}%;background:{color}"></div></div>'
                f'<div class="threshold-labels"><span>0</span><span>{r["max_score"]}</span></div>'
                f'<div style="margin-top:4px;font-size:13px;font-weight:600;color:{color};">{t.get("severity",r.get("level",""))}</div>'
                f'</div></div>'
                f'<div class="interpretation-box {box_class}">{r.get("interpretation","")}</div>'
                f'{q9_html}'
                f'{("<div style=\"margin-top:12px;font-size:12px;color:#94A3B8;\">"+r.get("note","")+"</div>" if r.get("note") else "")}'
                f'</div>'
            )
    html = html.replace("{{SCALE_RESULTS}}", "\n".join(scale_html_parts))

    # --- BFI-10 Radar ---
    bfi = results.get("BFI-10", {})
    if "dimensions" in bfi:
        # SVG Radar Chart
        dims = bfi["dimensions"]
        dim_names = list(dims.keys())
        svg = generate_radar_svg(dim_names, dims)
        html = html.replace("{{BFI_RADAR}}", f'<div class="card"><h2>🎭 大五人格画像</h2><div class="radar-container">{svg}</div></div>')

        # BFI Dimension Cards
        dim_cards = []
        for dim_name, dim_data in dims.items():
            score = dim_data["score"]
            color = bfi_dim_color(score)
            dim_cards.append(
                f'<div class="dim-card" style="border-color:{color}">'
                f'<div class="dim-name">{dim_name}</div>'
                f'<div class="dim-score" style="color:{color}">{score}</div>'
                f'<div class="dim-desc">{dim_data["high_desc"] if score >= 3 else dim_data["low_desc"]}</div>'
                f'</div>'
            )
        html = html.replace("{{BFI_DIMENSIONS}}", f'<div class="dimension-cards">{"".join(dim_cards)}</div>')
    else:
        html = html.replace("{{BFI_RADAR}}", "").replace("{{BFI_DIMENSIONS}}", "")

    # --- Warnings ---
    summary = results.get("_summary", {})
    warnings = summary.get("warnings", [])
    if warnings:
        warn_html = ['<div class="card"><h2>⚠️ 需要关注的信号</h2>']
        for w in warnings:
            warn_html.append(f'<div class="alert {w["level"]}"><span>{"🔴" if w["level"]=="high" else "🟠" if w["level"]=="medium" else "🟡"}</span><span>{w["text"]}</span></div>')
        warn_html.append('</div>')
        html = html.replace("{{WARNINGS}}", "\n".join(warn_html))
    else:
        html = html.replace("{{WARNINGS}}", "")

    # --- Recommendations ---
    recs = summary.get("recommendations", [])
    if recs:
        rec_html = []
        for i, rec in enumerate(recs, 1):
            rec_html.append(f'<li><span class="num">{i}</span><span>{rec}</span></li>')
        html = html.replace("{{RECOMMENDATIONS}}", "\n".join(rec_html))
    else:
        html = html.replace("{{RECOMMENDATIONS}}", "<li>保持当前健康生活方式</li>")

    # --- Hotlines ---
    hotlines = summary.get("hotlines", [])
    hl_html = []
    for hl in hotlines:
        hl_html.append(f'<div class="hotline"><div class="name">{hl["name"]}</div><div class="number">{hl["number"]}</div></div>')
    html = html.replace("{{HOTLINES}}", "\n".join(hl_html))

    return html


def generate_radar_svg(dim_names, dims):
    """Generate SVG radar chart for Big Five"""
    cx, cy = 200, 200
    radius = 140
    levels = 5
    n = len(dim_names)

    import math
    # Calculate points
    def get_point(i, value_ratio, r):
        angle = -math.pi / 2 + (2 * math.pi * i / n)
        r_scaled = r * (value_ratio / levels)
        x = cx + r_scaled * math.cos(angle)
        y = cy + r_scaled * math.sin(angle)
        return x, y

    svg_parts = [f'<svg width="420" height="420" viewBox="0 0 420 420" xmlns="http://www.w3.org/2000/svg">']

    # Background circles
    for level in range(1, levels + 1):
        r = radius * level / levels
        svg_parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#E2E8F0" stroke-width="1" stroke-dasharray="4,4"/>')

    # Axis lines
    for i in range(n):
        angle = -math.pi / 2 + (2 * math.pi * i / n)
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        svg_parts.append(f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="#CBD5E1" stroke-width="1"/>')

    # Data polygon
    data_points = []
    for i, dim_name in enumerate(dim_names):
        score = dims[dim_name]["score"]
        r_val = radius * (score / 5)
        x, y = get_point(i, 0, 0)
        x_adj = cx + r_val * math.cos(-math.pi / 2 + (2 * math.pi * i / n))
        y_adj = cy + r_val * math.sin(-math.pi / 2 + (2 * math.pi * i / n))
        data_points.append(f"{x_adj:.1f},{y_adj:.1f}")

    svg_parts.append(f'<polygon points="{" ".join(data_points)}" fill="rgba(139,92,246,0.25)" stroke="#8B5CF6" stroke-width="2"/>')

    # Labels
    for i, dim_name in enumerate(dim_names):
        angle = -math.pi / 2 + (2 * math.pi * i / n)
        score = dims[dim_name]["score"]
        label_r = radius + 30
        x = cx + label_r * math.cos(angle)
        y = cy + label_r * math.sin(angle)
        text_anchor = "middle"
        if abs(x - cx) < 10:
            text_anchor = "middle"
        elif x > cx:
            text_anchor = "start"
        else:
            text_anchor = "end"

        # Short name
        short_name = dim_name.split("(")[0] if "(" in dim_name else dim_name
        svg_parts.append(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{text_anchor}" font-size="13" fill="#64748B" font-weight="600">{short_name}</text>')
        score_y = y + 16
        svg_parts.append(f'<text x="{x:.1f}" y="{score_y:.1f}" text-anchor="{text_anchor}" font-size="12" fill="#8B5CF6" font-weight="700">{score}</text>')

    svg_parts.append('</svg>')
    return "\n".join(svg_parts)


def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print("心理测评 HTML 报告生成器")
        print("用法:")
        print("  python generate_report.py --results '<json>' --output report.html")
        print("  python generate_report.py --results-file '<json_path>' --output report.html")
        return

    try:
        results = None
        if "--results" in args:
            idx = args.index("--results")
            results = json.loads(args[idx + 1])
        elif "--results-file" in args:
            idx = args.index("--results-file")
            with open(args[idx + 1], "r", encoding="utf-8") as f:
                results = json.load(f)
        else:
            print(json.dumps({"error": "请提供 --results 或 --results-file"}, ensure_ascii=False))
            return

        output_path = "psycho_report.html"
        if "--output" in args:
            idx = args.index("--output")
            output_path = args[idx + 1]

        html = generate_report(results)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

        print(json.dumps({"status": "ok", "output": os.path.abspath(output_path)}, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
