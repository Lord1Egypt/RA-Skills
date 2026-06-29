#!/usr/bin/env python3
"""
HTML报告生成器
用法: python generate_report.py --score-json <path> --output <html_path>
从评分JSON生成交互式HTML可视化报告
"""

import json
import argparse
from pathlib import Path
from datetime import datetime

# ─── HTML 报告模板 ──────────────────────────────────────────

REPORT_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>简历-JD 匹配度评分报告 | {candidate} → {target_job}</title>
<style>
:root {{ --bg: #f8f9fb; --card: #ffffff; --accent: #2563eb; --text: #1e293b; --text2: #64748b; --border: #e2e8f0; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans SC", sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; padding: 24px; }}
.container {{ max-width: 1000px; margin: 0 auto; }}

.header {{ background: linear-gradient(135deg, #1e293b 0%, #334155 100%); color: #fff; border-radius: 12px; padding: 36px 40px; margin-bottom: 24px; }}
.header h1 {{ font-size: 24px; font-weight: 700; margin-bottom: 8px; }}
.header .subtitle {{ font-size: 14px; color: #94a3b8; }}
.header .meta-row {{ display: flex; gap: 32px; margin-top: 16px; flex-wrap: wrap; }}
.header .meta-item {{ font-size: 13px; color: #cbd5e1; }}
.header .meta-item span {{ color: #60a5fa; font-weight: 600; }}

.score-hero {{ display: grid; grid-template-columns: 200px 1fr; gap: 24px; background: var(--card); border-radius: 12px; padding: 32px; margin-bottom: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }}
.score-circle {{ width: 180px; height: 180px; border-radius: 50%; display: flex; align-items: center; justify-content: center; position: relative; }}
.score-inner {{ width: 140px; height: 140px; border-radius: 50%; background: white; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
.score-num {{ font-size: 56px; font-weight: 800; line-height: 1; }}
.score-total {{ font-size: 14px; color: #94a3b8; margin-top: 2px; }}
.score-grade {{ font-size: 28px; font-weight: 800; margin-top: -4px; }}
.score-info {{ display: flex; flex-direction: column; justify-content: center; }}
.score-info .position {{ font-size: 15px; color: var(--text2); margin-bottom: 8px; }}
.score-info .oneliner {{ font-size: 18px; font-weight: 600; color: var(--text); line-height: 1.5; margin-bottom: 12px; }}

.section {{ background: var(--card); border-radius: 12px; padding: 28px 32px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }}
.section h2 {{ font-size: 18px; font-weight: 700; margin-bottom: 20px; }}

.dim-table {{ width: 100%; border-collapse: collapse; }}
.dim-table th {{ text-align: left; padding: 10px 14px; font-size: 12px; font-weight: 600; color: var(--text2); border-bottom: 2px solid var(--border); }}
.dim-table td {{ padding: 12px 14px; font-size: 14px; border-bottom: 1px solid var(--border); }}
.dim-bar-bg {{ width: 100%; height: 8px; background: #f1f5f9; border-radius: 4px; margin-top: 6px; overflow: hidden; }}
.dim-bar-fill {{ height: 100%; border-radius: 4px; }}

.kw-table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
.kw-table th {{ text-align: left; padding: 8px 12px; font-size: 11px; font-weight: 600; color: var(--text2); border-bottom: 2px solid var(--border); background: #f8fafc; }}
.kw-table td {{ padding: 8px 12px; border-bottom: 1px solid var(--border); }}
.badge {{ display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; }}
.badge-hit {{ background: #dcfce7; color: #16a34a; }}
.badge-partial {{ background: #fef9c3; color: #a16207; }}
.badge-miss {{ background: #fee2e2; color: #dc2626; }}
.badge-extra {{ background: #e0e7ff; color: #4338ca; }}

.detail-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
.detail-card {{ border: 1px solid var(--border); border-radius: 8px; padding: 16px; }}
.detail-card h4 {{ font-size: 14px; font-weight: 700; margin-bottom: 10px; }}
.detail-card .gain {{ color: #16a34a; font-size: 13px; margin-bottom: 4px; }}
.detail-card .loss {{ color: #dc2626; font-size: 13px; margin-bottom: 4px; }}
.detail-card .gain::before {{ content: '+ '; font-weight: 700; }}
.detail-card .loss::before {{ content: '− '; font-weight: 700; }}

.advice-list {{ list-style: none; }}
.advice-item {{ border-left: 3px solid var(--border); padding: 12px 16px; margin-bottom: 12px; border-radius: 0 8px 8px 0; background: #f8fafc; }}
.advice-item.roi-1 {{ border-left-color: #dc2626; }}
.advice-item.roi-2 {{ border-left-color: #ea580c; }}
.advice-item.roi-3 {{ border-left-color: #ca8a04; }}
.roi-badge {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700; margin-right: 8px; }}
.roi-1 .roi-badge {{ background: #fee2e2; color: #dc2626; }}
.roi-2 .roi-badge {{ background: #ffedd5; color: #ea580c; }}
.roi-3 .roi-badge {{ background: #fef9c3; color: #a16207; }}
.action-tag {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; margin-left: 8px; }}
.tag-rewrite {{ background: #e0e7ff; color: #4338ca; }}
.tag-new {{ background: #fce7f3; color: #be185d; }}
.advice-item p {{ font-size: 14px; margin: 6px 0 0 0; }}

.comp-table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
.comp-table th {{ text-align: left; padding: 10px 14px; font-size: 12px; font-weight: 600; color: var(--text2); border-bottom: 2px solid var(--border); }}
.comp-table td {{ padding: 10px 14px; border-bottom: 1px solid var(--border); }}
.comp-bar {{ height: 20px; border-radius: 4px; display: flex; align-items: center; padding-left: 8px; font-size: 11px; font-weight: 700; color: #fff; min-width: 40px; }}

.radar-wrap {{ display: flex; justify-content: center; padding: 16px; }}

.footer {{ text-align: center; padding: 20px; color: var(--text2); font-size: 12px; }}
.highlight {{ background: #fef3c7; border-radius: 8px; padding: 14px; font-size: 13px; }}
.highlight-blue {{ background: #e0e7ff; border-radius: 8px; padding: 14px; font-size: 14px; }}

@media (max-width: 768px) {{
  .score-hero {{ grid-template-columns: 1fr; justify-items: center; text-align: center; }}
  .detail-grid {{ grid-template-columns: 1fr; }}
  .header .meta-row {{ flex-direction: column; gap: 8px; }}
}}
</style>
</head>
<body>
<div class="container">
<div class="header">
  <h1>简历-JD 匹配度评分报告</h1>
  <div class="subtitle">5 维度 × 100 分评分体系 | {date}</div>
  <div class="meta-row">
    <div class="meta-item">目标岗位：<span>{target_job}</span></div>
    <div class="meta-item">候选人角色：<span>{candidate_role}</span></div>
    <div class="meta-item">评分日期：<span>{date}</span></div>
  </div>
</div>

{score_hero}

{radar_section}

{dimension_table}

{keyword_table}

{detail_cards}

{recommendations}

{cross_job}

<div class="footer">
  <p>评分引擎：resume-jd-scorer v1.0 · 5 维度 × 100 分 · 基于简历已声明的事实</p>
  <p>⚠️ 评分仅供求职策略参考，不构成录用建议。</p>
</div>
</div>
</body>
</html>'''


def generate_score_hero(result: dict) -> str:
    """生成总分Hero区域HTML"""
    total = result["total_score"]
    grade = result["grade"]
    grade_text = result["grade_text"]
    oneliner = result["oneliner"]

    # 颜色映射
    if grade == "A":
        color = "#16a34a"
    elif grade == "B":
        color = "#2563eb"
    elif grade == "C":
        color = "#ca8a04"
    else:
        color = "#dc2626"

    # 圆环角度
    angle = total / 100 * 360

    return f'''<div class="score-hero">
  <div class="score-circle" style="background: conic-gradient({color} 0deg {angle}deg, #f1f5f9 {angle}deg 360deg);">
    <div class="score-inner">
      <div class="score-num" style="color:{color};">{total}</div>
      <div class="score-total">/ 100</div>
    </div>
  </div>
  <div class="score-info">
    <div class="position">匹配评级：<strong style="color:{color};font-size:22px;">{grade} 级 — {grade_text}</strong></div>
    <div class="oneliner">{oneliner}</div>
  </div>
</div>'''


def generate_radar(result: dict) -> str:
    """生成SVG雷达图"""
    dims = result["dimensions"]
    rates = [
        dims["hard_skills"]["rate"],
        dims["experience"]["rate"],
        dims["academic"]["rate"],
        dims["ats"]["rate"],
        dims["bonus"]["rate"],
    ]
    labels = ["硬技能", "经历", "学术", "ATS", "加分"]
    scores = [
        f"{dims['hard_skills']['score']}/30",
        f"{dims['experience']['score']}/25",
        f"{dims['academic']['score']}/20",
        f"{dims['ats']['score']}/15",
        f"{dims['bonus']['score']}/10",
    ]
    colors = ["#dc2626", "#ea580c", "#dc2626", "#dc2626", "#ca8a04"]

    # 五边形顶点计算
    import math
    cx, cy, r = 210, 170, 130
    points = []
    grid_lines = []
    for level in range(1, 6):
        lr = r * level / 5
        lps = []
        for i in range(5):
            angle = -math.pi / 2 + 2 * math.pi * i / 5
            x = cx + lr * math.cos(angle)
            y = cy + lr * math.sin(angle)
            lps.append(f"{x:.0f},{y:.0f}")
        grid_lines.append(f'<polygon points="{" ".join(lps)}" fill="none" stroke="#e2e8f0" stroke-width="1"/>')

    # 轴线
    axes = []
    for i in range(5):
        angle = -math.pi / 2 + 2 * math.pi * i / 5
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        axes.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.0f}" y2="{y:.0f}" stroke="#e2e8f0" stroke-width="1"/>')

    # 数据点
    data_ps = []
    data_dots = []
    for i, rate in enumerate(rates):
        angle = -math.pi / 2 + 2 * math.pi * i / 5
        x = cx + r * rate * math.cos(angle)
        y = cy + r * rate * math.sin(angle)
        data_ps.append(f"{x:.0f},{y:.0f}")
        data_dots.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="4" fill="{colors[i]}"/>')

    # 标签
    label_tags = []
    label_offsets = [(0, -20), (10, 5), (5, 18), (-5, 18), (-10, 5)]
    for i, (label, score, (dx, dy)) in enumerate(zip(labels, scores, label_offsets)):
        angle = -math.pi / 2 + 2 * math.pi * i / 5
        x = cx + (r + 20) * math.cos(angle)
        y = cy + (r + 20) * math.sin(angle)
        anchor = "middle" if abs(dx) < 5 else ("start" if dx > 0 else "end")
        label_tags.append(f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="{anchor}" font-size="12" font-weight="600" fill="#334155">{label} {score}</text>')

    return f'''<div class="section">
  <h2>📊 能力雷达图</h2>
  <div class="radar-wrap">
    <svg width="440" height="380" viewBox="0 0 440 380">
      <defs>
        <radialGradient id="gradData" cx="50%" cy="50%"><stop offset="0%" stop-color="#dc2626" stop-opacity="0.2"/><stop offset="100%" stop-color="#dc2626" stop-opacity="0.05"/></radialGradient>
      </defs>
      {"".join(grid_lines)}
      {"".join(axes)}
      <polygon points="{" ".join(data_ps)}" fill="url(#gradData)" stroke="#dc2626" stroke-width="2" stroke-linejoin="round"/>
      {"".join(data_dots)}
      {"".join(label_tags)}
    </svg>
  </div>
</div>'''


def generate_dimension_table(result: dict) -> str:
    """生成5维度分数表"""
    dims = result["dimensions"]
    dim_names = [
        ("1. 硬技能匹配", "hard_skills", 30),
        ("2. 经历相关性", "experience", 25),
        ("3. 学术产出", "academic", 20),
        ("4. ATS 关键词覆盖率", "ats", 15),
        ("5. 加分项", "bonus", 10),
    ]

    colors_rate = {
        "hard_skills": "#dc2626",
        "experience": "#ea580c",
        "academic": "#dc2626",
        "ats": "#dc2626",
        "bonus": "#ca8a04",
    }

    rows = []
    total_score = 0
    total_max = 0

    for name, key, max_s in dim_names:
        s = dims[key]["score"]
        rate = dims[key]["rate"]
        color = colors_rate[key]
        total_score += s
        total_max += max_s
        rows.append(f'''<tr>
        <td style="font-weight:600;">{name}</td>
        <td style="color:var(--text2);">{max_s}</td>
        <td style="font-weight:700;font-size:16px;color:{color};">{s}<span style="color:var(--text2);font-weight:400;">/{max_s}</span></td>
        <td style="font-weight:700;color:{color};">{int(rate*100)}%</td>
        <td><div class="dim-bar-bg"><div class="dim-bar-fill" style="width:{int(rate*100)}%;background:{color};"></div></div></td>
      </tr>''')

    total_rate = round(total_score / total_max, 2)
    rows.append(f'''<tr style="background:#f1f5f9;font-weight:700;">
        <td>合计</td><td>100</td>
        <td style="font-size:16px;color:#dc2626;">{total_score}<span style="color:var(--text2);font-weight:400;">/100</span></td>
        <td style="color:#dc2626;">{int(total_rate*100)}%</td>
        <td><div class="dim-bar-bg"><div class="dim-bar-fill" style="width:{int(total_rate*100)}%;background:#dc2626;"></div></div></td>
      </tr>''')

    return f'''<div class="section">
  <h2>📊 5 维度分数表</h2>
  <table class="dim-table">
    <thead><tr><th>评分维度</th><th>满分</th><th>得分</th><th>得分率</th><th style="width:50%;">得分分布</th></tr></thead>
    <tbody>{"".join(rows)}</tbody>
  </table>
</div>'''


def generate_keyword_table(kw_matches: list, extra_hits: list) -> str:
    """生成关键词命中明细表"""
    rows = []
    for i, kw in enumerate(kw_matches, 1):
        status = kw["match_status"]
        if status == "full":
            badge = '<span class="badge badge-hit">✅ 完整命中</span>'
        elif status == "partial":
            badge = '<span class="badge badge-partial">⚠️ 部分命中</span>'
        else:
            badge = '<span class="badge badge-miss">❌ 未命中</span>'

        evidence = kw.get("evidence", "—")
        weight_label = {"critical": "极高", "high": "高", "medium": "中", "low": "低"}.get(kw["weight"], kw["weight"])

        rows.append(f'''<tr>
        <td>{i}</td>
        <td><strong>{kw["keyword"]}</strong></td>
        <td>{kw["category"]}</td>
        <td>{weight_label}</td>
        <td>{badge}</td>
        <td style="font-size:12px;color:var(--text2);">{evidence}</td>
      </tr>''')

    # 额外命中
    for i, eh in enumerate(extra_hits, len(kw_matches) + 1):
        rows.append(f'''<tr>
        <td>{i}</td>
        <td><strong>{eh["keyword"]}</strong></td>
        <td>{eh["category"]}</td>
        <td>—</td>
        <td><span class="badge badge-extra">🔵 简历独有</span></td>
        <td style="font-size:12px;color:var(--text2);">JD未要求但简历体现的加分技能</td>
      </tr>''')

    full = sum(1 for k in kw_matches if k["match_status"] == "full")
    partial = sum(1 for k in kw_matches if k["match_status"] == "partial")
    miss = sum(1 for k in kw_matches if k["match_status"] == "miss")

    return f'''<div class="section">
  <h2>🔑 关键词命中明细表</h2>
  <p style="font-size:13px;color:var(--text2);margin-bottom:16px;">
    JD 共提取 <strong>{len(kw_matches)}</strong> 个核心关键词 | 
    ✅ 完整命中 {full} | ⚠️ 部分命中 {partial} | ❌ 未命中 {miss} | 🔵 简历独有 {len(extra_hits)}
  </p>
  <table class="kw-table">
    <thead><tr><th>#</th><th>JD 关键词</th><th>类别</th><th>JD权重</th><th>命中状态</th><th>简历对应证据</th></tr></thead>
    <tbody>{"".join(rows)}</tbody>
  </table>
</div>'''


def generate_detail_cards(result: dict) -> str:
    """生成每维度得分项与扣分项"""
    dims = result["dimensions"]
    dim_config = [
        ("1️⃣ 硬技能匹配", "hard_skills"),
        ("2️⃣ 经历相关性", "experience"),
        ("3️⃣ 学术产出", "academic"),
        ("4️⃣ ATS 关键词覆盖率", "ats"),
    ]

    cards = []
    for title, key in dim_config:
        d = dims[key]
        score = d["score"]
        max_s = d["max"]
        color = "#dc2626" if key != "bonus" and d["rate"] < 0.5 else "#ca8a04"

        gains_html = "".join(f'<div class="gain">{g}</div>' for g in d.get("gains", []))
        losses_html = "".join(f'<div class="loss">{l}</div>' for l in d.get("losses", []))

        cards.append(f'''<div class="detail-card">
      <h4>{title} <span style="color:{color};">{score}/{max_s}</span></h4>
      {gains_html}
      {losses_html}
    </div>''')

    # 加分项卡片（整行）
    bonus = dims["bonus"]
    bonus_gains = "".join(f'<div class="gain">{g}</div>' for g in bonus.get("gains", []))
    bonus_losses = "".join(f'<div class="loss">{l}</div>' for l in bonus.get("losses", []))

    cards.append(f'''<div class="detail-card" style="grid-column: 1 / -1;">
      <h4>5️⃣ 加分项 <span style="color:#ca8a04;">{bonus["score"]}/10</span></h4>
      {bonus_gains}
      {bonus_losses}
    </div>''')

    return f'<div class="section"><h2>🔍 每维度得分项与扣分项</h2><div class="detail-grid">{"".join(cards)}</div></div>'


def generate_recommendations(recommendations: list) -> str:
    """生成TOP 3建议"""
    items = []
    for rec in recommendations:
        p = rec["priority"]
        action_type = rec.get("action_type", "建议优化")
        tag_class = "tag-rewrite" if action_type == "改写已有" else "tag-new"

        items.append(f'''<li class="advice-item roi-{p}">
      <strong><span class="roi-badge">ROI #{p} · {rec["roi"]}</span></strong>
      <span class="action-tag {tag_class}">{action_type}</span>
      <p><strong>{rec["title"]}</strong></p>
      <p style="font-size:13px;color:var(--text2);margin-top:4px;">{rec.get("detail", "")}</p>
      <p style="font-size:12px;color:var(--text2);margin-top:2px;">预估匹配度提升：{rec.get("estimated_improvement", "未知")}</p>
    </li>''')

    total_improvement = "+15~30分" if len(recommendations) >= 3 else "+10~20分"

    return f'''<div class="section">
  <h2>💡 TOP 3 修改建议（按 ROI 排序）</h2>
  <ul class="advice-list">{"".join(items)}</ul>
  <div class="highlight" style="margin-top:16px;color:#92400e;background:#fef3c7;">
    <strong>⚡ 如果全部建议执行到位：</strong> 预估总分可提升 {total_improvement}。但结构性差距（如角色转换、学术产出）可能仍需长期补课。
  </div>
</div>'''


def generate_cross_job(comparisons: list) -> str:
    """生成跨岗位匹配度对比表"""
    rows = []
    for cj in comparisons:
        score = cj["score"]
        grade = cj["grade"]
        if grade == "A":
            bg = "#dcfce7"; bar_color = "#16a34a"; grade_badge = '<span class="badge badge-hit">A</span>'
        elif grade.startswith("B"):
            bg = "#fef9c3"; bar_color = "#ca8a04"; grade_badge = f'<span class="badge badge-partial">{grade}</span>'
        elif grade == "C":
            bg = "#fff1f2"; bar_color = "#ea580c"; grade_badge = '<span class="badge badge-miss">C</span>'
        else:
            bg = "#fee2e2"; bar_color = "#dc2626"; grade_badge = f'<span class="badge badge-miss">{grade}</span>'

        is_current = cj.get("is_current", False)
        is_best = cj.get("is_best_match", False)
        job_name = cj["job"]
        if is_best:
            job_name += " 🎯 最佳匹配"
        if is_current:
            job_name += " ← 当前"
            bg = "#fee2e2"

        match_pts = " / ".join(cj.get("match_points", []))
        rows.append(f'''<tr style="background:{bg};">
        <td><strong>{job_name}</strong></td>
        <td style="font-weight:700;color:{bar_color};">{score}</td>
        <td>{grade_badge}</td>
        <td><div class="comp-bar" style="width:{max(score,15)}%;background:{bar_color};">{score}/100</div></td>
        <td style="font-size:13px;">{match_pts}</td>
      </tr>''')

    return f'''<div class="section">
  <h2>🔄 跨岗位匹配度对比</h2>
  <table class="comp-table">
    <thead><tr><th>目标岗位</th><th>评分</th><th>评级</th><th>可视化</th><th>核心匹配点</th></tr></thead>
    <tbody>{"".join(rows)}</tbody>
  </table>
  <div class="highlight-blue" style="margin-top:16px;color:#3730a3;">
    <strong>🎯 岗位建议：</strong> 当前简历的最佳匹配为列表中评分最高的A/B级岗位。如目标岗位评分低于C级，建议优先投递高匹配度岗位作为过渡。
  </div>
</div>'''


def generate_report(score_json_path: str, output_html_path: str,
                    candidate_name: str = "候选人", target_job: str = "目标岗位") -> str:
    """从评分JSON生成完整HTML报告"""
    with open(score_json_path, "r", encoding="utf-8") as f:
        result = json.load(f)

    date_str = datetime.now().strftime("%Y-%m-%d")

    # 生成各模块
    score_hero_html = generate_score_hero(result)
    radar_html = generate_radar(result)
    dim_table_html = generate_dimension_table(result)
    kw_table_html = generate_keyword_table(
        result.get("keyword_matches", []),
        result.get("extra_hits", [])
    )
    detail_html = generate_detail_cards(result)
    rec_html = generate_recommendations(result.get("recommendations", []))
    cross_html = generate_cross_job(result.get("cross_job_comparison", []))

    # 填充模板
    html = REPORT_TEMPLATE.format(
        candidate=candidate_name,
        target_job=target_job,
        date=date_str,
        candidate_role=result["meta"].get("candidate_role", "未知"),
        score_hero=score_hero_html,
        radar_section=radar_html,
        dimension_table=dim_table_html,
        keyword_table=kw_table_html,
        detail_cards=detail_html,
        recommendations=rec_html,
        cross_job=cross_html,
    )

    output_path = Path(output_html_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    return str(output_path)


# ─── CLI 入口 ──────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="简历-JD评分HTML报告生成器")
    parser.add_argument("--score-json", required=True, help="评分JSON文件路径")
    parser.add_argument("--output", required=True, help="输出HTML文件路径")
    parser.add_argument("--candidate", default="候选人", help="候选人名称")
    parser.add_argument("--target-job", default="目标岗位", help="目标岗位名称")

    args = parser.parse_args()

    output_path = generate_report(
        args.score_json, args.output,
        candidate_name=args.candidate,
        target_job=args.target_job,
    )

    print(f"✅ 报告生成完成: {output_path}")


if __name__ == "__main__":
    main()
