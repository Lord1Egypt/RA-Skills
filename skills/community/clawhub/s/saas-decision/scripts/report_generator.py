#!/usr/bin/env python3
"""
SaaS产品辅助决策报告生成器
Generate professional feasibility decision report for SaaS products.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# ============================================================
# Scoring Engine — 9 SaaS-Specific Dimensions
# ============================================================

DIMENSIONS = {
    "market_demand": {"name": "市场需求", "weight": 0.15, "icon": "📊"},
    "user_profile": {"name": "用户画像", "weight": 0.10, "icon": "👥"},
    "pain_points": {"name": "需求痛点", "weight": 0.10, "icon": "🎯"},
    "competition": {"name": "竞品格局", "weight": 0.15, "icon": "⚔️"},
    "monetization": {"name": "变现能力", "weight": 0.15, "icon": "💰"},
    "acquisition": {"name": "获客增长", "weight": 0.10, "icon": "📈"},
    "marketing": {"name": "推广营销", "weight": 0.15, "icon": "📢"},
    "cost_structure": {"name": "成本结构", "weight": 0.05, "icon": "💸"},
    "tech_feasibility": {"name": "技术可行性", "weight": 0.05, "icon": "🔧"},
}


def calculate_total_score(scores: dict) -> dict:
    """Calculate weighted total score and rating."""
    total = 0
    dim_scores = {}
    for key, dim in DIMENSIONS.items():
        s = scores.get(key, 50)
        dim_scores[key] = s
        total += s * dim["weight"]

    total = round(total, 1)

    if total >= 80:
        rating = "✅ 强烈建议做"
        rating_desc = "市场需求强劲，竞争格局有利，SaaS商业模式清晰，建议尽快启动MVP验证"
        color = "#10B981"
        bg = "#ECFDF5"
        icon = "🚀"
    elif total >= 65:
        rating = "🟡 谨慎推进"
        rating_desc = "有一定市场机会，但需要差异化定位和更深入的用户需求验证后再投入"
        color = "#F59E0B"
        bg = "#FFFBEB"
        icon = "🔍"
    elif total >= 50:
        rating = "⚠️ 暂缓观望"
        rating_desc = "市场风险较高或竞争激烈，建议先验证核心假设、小范围试点后再决定"
        color = "#F97316"
        bg = "#FFF7ED"
        icon = "⏸️"
    else:
        rating = "❌ 不建议做"
        rating_desc = "当前市场条件下风险过高，市场需求不明确或竞争过度饱和，建议重新评估方向"
        color = "#EF4444"
        bg = "#FEF2F2"
        icon = "🛑"

    return {
        "total": total,
        "dimensions": dim_scores,
        "rating": rating,
        "rating_desc": rating_desc,
        "color": color,
        "bg": bg,
        "icon": icon,
    }


# ============================================================
# Helpers
# ============================================================

def safe_get(d, key, default=""):
    if isinstance(d, dict):
        return d.get(key, default)
    return default


def make_score_bar(score, max_score=100):
    pct = min(score / max_score, 1.0)
    if score >= 80:
        color = "#10B981"
    elif score >= 65:
        color = "#3B82F6"
    elif score >= 50:
        color = "#F59E0B"
    else:
        color = "#EF4444"
    return f"""<div style="display:flex;align-items:center;gap:10px;margin:6px 0;">
  <div style="flex:1;height:10px;background:#E5E7EB;border-radius:5px;overflow:hidden;">
    <div style="width:{pct*100}%;height:100%;background:{color};border-radius:5px;transition:width 0.6s;"></div>
  </div>
  <span style="font-weight:700;font-size:14px;color:{color};min-width:45px;text-align:right;">{score}分</span>
</div>"""


def make_tag(text, color="#3B82F6"):
    return f'<span style="display:inline-block;padding:3px 10px;background:{color}15;color:{color};border-radius:12px;font-size:12px;font-weight:600;margin:2px;">{text}</span>'


def level_badge(level):
    colors = {
        "高": ("#EF4444", "#FEE2E2"),
        "中高": ("#F97316", "#FFF7ED"),
        "中等": ("#F59E0B", "#FEF3C7"),
        "中低": ("#3B82F6", "#DBEAFE"),
        "低": ("#10B981", "#D1FAE5"),
        "困难": ("#EF4444", "#FEE2E2"),
        "容易": ("#10B981", "#D1FAE5"),
        "强": ("#10B981", "#D1FAE5"),
        "弱": ("#EF4444", "#FEE2E2"),
        "激烈": ("#EF4444", "#FEE2E2"),
        "蓝海": ("#10B981", "#D1FAE5"),
    }
    c, bg = colors.get(level, ("#6B7280", "#F3F4F6"))
    return f'<span style="display:inline-block;padding:2px 8px;background:{bg};color:{c};border-radius:8px;font-size:12px;font-weight:600;">{level}</span>'


# ============================================================
# HTML Report Generator
# ============================================================

def generate_report(data: dict) -> str:
    name = safe_get(data, "name", "未命名产品")
    category = safe_get(data, "category", "未指定行业")
    now = datetime.now().strftime("%Y年%m月%d日 %H:%M")

    scores = safe_get(data, "scores", {})
    score_result = calculate_total_score(scores)

    # Extract sections
    market = safe_get(data, "market_demand", {})
    user = safe_get(data, "user_profile", {})
    pain = safe_get(data, "pain_points", {})
    competitors = safe_get(data, "competition", {})
    monetization = safe_get(data, "monetization", {})
    acquisition = safe_get(data, "acquisition", {})
    marketing = safe_get(data, "marketing", {})
    cost = safe_get(data, "cost_structure", {})
    tech = safe_get(data, "tech_feasibility", {})
    risks = safe_get(data, "risks", {})

    # ============================================================
    # HTML Template
    # ============================================================
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SaaS可行性决策报告 - {name}</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif; background: #F3F4F6; color: #1F2937; line-height:1.7; }}
  .container {{ max-width: 960px; margin: 0 auto; padding: 20px; }}

  .cover {{ background: linear-gradient(135deg, #0C1B33 0%, #1B3A5C 40%, #2563EB 80%, #7C3AED 100%); color: white; padding: 60px 40px; border-radius: 16px; text-align: center; margin-bottom: 24px; position: relative; overflow: hidden; }}
  .cover::before {{ content: ''; position: absolute; top: -30%; right: -15%; width: 500px; height: 500px; background: radial-gradient(circle, rgba(124,58,237,0.25) 0%, transparent 70%); border-radius: 50%; }}
  .cover::after {{ content: ''; position: absolute; bottom: -40%; left: -10%; width: 400px; height: 400px; background: radial-gradient(circle, rgba(16,185,129,0.2) 0%, transparent 70%); border-radius: 50%; }}
  .cover h1 {{ font-size: 36px; font-weight: 800; margin-bottom: 8px; position: relative; }}
  .cover .subtitle {{ font-size: 18px; opacity: 0.75; position: relative; }}
  .cover .badge {{ display: inline-block; background: rgba(255,255,255,0.15); padding: 6px 20px; border-radius: 20px; font-size: 13px; margin-top: 16px; position: relative; backdrop-filter: blur(10px); }}
  .cover .date {{ font-size: 13px; opacity: 0.5; margin-top: 8px; position: relative; }}

  .score-card {{ background: {score_result['bg']}; border: 2px solid {score_result['color']}; border-radius: 16px; padding: 32px; text-align: center; margin-bottom: 24px; }}
  .score-card .big-score {{ font-size: 72px; font-weight: 900; color: {score_result['color']}; line-height: 1; }}
  .score-card .rating {{ font-size: 24px; font-weight: 700; color: {score_result['color']}; margin: 8px 0; }}
  .score-card .rating-desc {{ font-size: 14px; color: #6B7280; max-width: 500px; margin: 0 auto; }}

  .section {{ background: white; border-radius: 16px; padding: 32px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }}
  .section h2 {{ font-size: 22px; font-weight: 700; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }}
  .section h3 {{ font-size: 16px; font-weight: 600; color: #374151; margin: 20px 0 8px; }}
  .section p {{ margin-bottom: 10px; color: #4B5563; font-size: 14px; }}
  .section ul {{ padding-left: 20px; margin: 8px 0; }}
  .section li {{ color: #4B5563; font-size: 14px; margin: 4px 0; }}

  .dim-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin: 16px 0; }}
  @media (max-width: 600px) {{ .dim-grid {{ grid-template-columns: 1fr; }} }}
  .dim-card {{ background: #F9FAFB; border-radius: 12px; padding: 18px; text-align: center; transition: transform 0.2s; }}
  .dim-card:hover {{ transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.08); }}
  .dim-card .dim-icon {{ font-size: 26px; margin-bottom: 6px; }}
  .dim-card .dim-name {{ font-size: 13px; color: #6B7280; margin-bottom: 4px; }}
  .dim-card .dim-score {{ font-size: 26px; font-weight: 800; }}
  .dim-card .dim-weight {{ font-size: 11px; color: #9CA3AF; }}

  .info-card {{ background: #F0F9FF; border-left: 4px solid #3B82F6; border-radius: 0 8px 8px 0; padding: 16px 20px; margin: 12px 0; }}
  .info-card.warn {{ background: #FFFBEB; border-color: #F59E0B; }}
  .info-card.success {{ background: #ECFDF5; border-color: #10B981; }}
  .info-card.danger {{ background: #FEF2F2; border-color: #EF4444; }}
  .info-card.purple {{ background: #F5F3FF; border-color: #8B5CF6; }}

  table {{ width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 13px; }}
  th {{ background: #F9FAFB; padding: 10px 14px; text-align: left; font-weight: 600; color: #374151; border-bottom: 2px solid #E5E7EB; }}
  td {{ padding: 10px 14px; border-bottom: 1px solid #F3F4F6; color: #4B5563; }}
  tr:hover td {{ background: #F9FAFB; }}

  .tag {{ display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; margin: 2px; }}
  .tag-blue {{ background: #DBEAFE; color: #1D4ED8; }}
  .tag-green {{ background: #D1FAE5; color: #065F46; }}
  .tag-yellow {{ background: #FEF3C7; color: #92400E; }}
  .tag-red {{ background: #FEE2E2; color: #991B1B; }}
  .tag-purple {{ background: #EDE9FE; color: #5B21B6; }}

  .stat-row {{ display: flex; gap: 16px; flex-wrap: wrap; }}
  .stat-card {{ flex: 1; min-width: 160px; border-radius: 12px; padding: 20px; text-align: center; }}
  .stat-card .stat-label {{ font-size: 13px; color: #6B7280; margin-bottom: 4px; }}
  .stat-card .stat-value {{ font-size: 24px; font-weight: 800; }}
  .stat-card.blue {{ background: #F0F9FF; }}
  .stat-card.blue .stat-value {{ color: #1D4ED8; }}
  .stat-card.green {{ background: #ECFDF5; }}
  .stat-card.green .stat-value {{ color: #065F46; }}
  .stat-card.amber {{ background: #FFFBEB; }}
  .stat-card.amber .stat-value {{ color: #92400E; }}
  .stat-card.purple {{ background: #F5F3FF; }}
  .stat-card.purple .stat-value {{ color: #5B21B6; }}

  .strategy-card {{ background: #F9FAFB; border-radius: 12px; padding: 18px; margin: 8px 0; border: 1px solid #E5E7EB; }}
  .strategy-card .strategy-num {{ display: inline-flex; align-items: center; justify-content: center; width: 28px; height: 28px; background: #7C3AED; color: white; border-radius: 50%; font-size: 14px; font-weight: 700; margin-right: 10px; flex-shrink: 0; }}

  .persona-card {{ background: linear-gradient(135deg, #F0F9FF, #ECFDF5); border-radius: 12px; padding: 20px; margin: 8px 0; }}
  .pain-card {{ background: #FFFBEB; border-radius: 10px; padding: 16px; margin: 6px 0; border-left: 3px solid #F59E0B; }}

  .pricing-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }}
  @media (max-width: 700px) {{ .pricing-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
  .pricing-model {{ background: #F9FAFB; border-radius: 10px; padding: 16px; text-align: center; border: 1px solid #E5E7EB; }}
  .pricing-model.active {{ border: 2px solid #7C3AED; background: #F5F3FF; }}

  .risk-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }}
  @media (max-width: 600px) {{ .risk-grid {{ grid-template-columns: 1fr; }} }}
  .risk-item {{ background: #F9FAFB; border-radius: 10px; padding: 16px; }}
  .risk-item .risk-level {{ font-size: 12px; font-weight: 600; margin-bottom: 4px; }}

  .timeline {{ position: relative; padding-left: 24px; margin: 16px 0; }}
  .timeline::before {{ content: ''; position: absolute; left: 8px; top: 0; bottom: 0; width: 2px; background: #E5E7EB; }}
  .timeline-item {{ position: relative; margin-bottom: 16px; }}
  .timeline-item::before {{ content: ''; position: absolute; left: -20px; top: 4px; width: 12px; height: 12px; border-radius: 50%; border: 2px solid #7C3AED; background: white; }}
  .timeline-item .tl-time {{ font-size: 12px; color: #9CA3AF; }}
  .timeline-item .tl-title {{ font-weight: 600; color: #1F2937; }}

  .footer {{ text-align: center; padding: 24px; color: #9CA3AF; font-size: 12px; }}

  @media print {{ body {{ background: white; }} .section {{ box-shadow: none; break-inside: avoid; }} }}
</style>
</head>
<body>
<div class="container">

  <!-- Cover -->
  <div class="cover">
    <h1>☁️ {name}</h1>
    <div class="subtitle">{category}</div>
    <div class="badge">SaaS 产品可行性决策报告</div>
    <div class="date">{now}</div>
  </div>

  <!-- Score Card -->
  <div class="score-card">
    <div class="big-score">{score_result['total']}</div>
    <div class="rating">{score_result['icon']} {score_result['rating']}</div>
    <div class="rating-desc">{score_result['rating_desc']}</div>
  </div>

  <!-- Dimension Matrix -->
  <div class="section">
    <h2>📊 多维度评分矩阵</h2>
    <div class="dim-grid">
"""
    for key, dim in DIMENSIONS.items():
        s = score_result["dimensions"].get(key, 50)
        color = "#10B981" if s >= 80 else ("#3B82F6" if s >= 65 else ("#F59E0B" if s >= 50 else "#EF4444"))
        html += f"""
      <div class="dim-card">
        <div class="dim-icon">{dim['icon']}</div>
        <div class="dim-name">{dim['name']}</div>
        <div class="dim-score" style="color:{color}">{s}</div>
        <div class="dim-weight">权重 {int(dim['weight']*100)}%</div>
      </div>"""

    html += """
    </div>
  </div>
"""

    # ============================================================
    # 1. Market Demand
    # ============================================================
    mkt_score = safe_get(market, "score", 50)
    mkt_size = safe_get(market, "market_size", "暂无数据")
    mkt_growth = safe_get(market, "growth", "暂无数据")
    mkt_tam = safe_get(market, "tam", "暂无数据")
    mkt_sam = safe_get(market, "sam", "暂无数据")
    mkt_detail = safe_get(market, "detail", "暂无详细数据")
    mkt_trends = safe_get(market, "trends", [])

    html += f"""
  <!-- 1. Market Demand -->
  <div class="section">
    <h2>📊 一、市场需求分析</h2>
    {make_score_bar(mkt_score)}
    <div class="stat-row">
      <div class="stat-card blue">
        <div class="stat-label">SaaS 市场规模</div>
        <div class="stat-value">{mkt_size}</div>
      </div>
      <div class="stat-card green">
        <div class="stat-label">年增长率</div>
        <div class="stat-value">{mkt_growth}</div>
      </div>
      <div class="stat-card amber">
        <div class="stat-label">总可寻址市场 (TAM)</div>
        <div class="stat-value">{mkt_tam}</div>
      </div>
      <div class="stat-card purple">
        <div class="stat-label">可服务市场 (SAM)</div>
        <div class="stat-value">{mkt_sam}</div>
      </div>
    </div>
    <p style="margin-top:12px;">{mkt_detail}</p>
"""

    if mkt_trends:
        html += '<h3>市场趋势信号</h3><ul>'
        for t in mkt_trends:
            html += f'<li>{"📈 " if isinstance(t, str) and ("增长" in t or "上升" in t) else "📉 " if isinstance(t, str) and ("下降" in t or "萎缩" in t) else "🔹 "}{t if isinstance(t, str) else safe_get(t, "desc", str(t))}</li>'
        html += '</ul>'

    html += """
    <div class="info-card">
      <strong>💡 SaaS市场洞察：</strong>评估TAM→SAM→SOM漏斗。SaaS的魅力在于可规模化——验证PMF后增长近乎线性。优先关注年增速>20%的细分赛道。
    </div>
  </div>
"""

    # ============================================================
    # 2. User Profile & Personas
    # ============================================================
    usr_score = safe_get(user, "score", 50)
    usr_target = safe_get(user, "target", "暂无数据")
    usr_personas = safe_get(user, "personas", [])
    usr_decision = safe_get(user, "decision_chain", "暂无数据")
    usr_wtp = safe_get(user, "willingness_to_pay", "中")
    usr_detail = safe_get(user, "detail", "暂无详细数据")

    html += f"""
  <!-- 2. User Profile -->
  <div class="section">
    <h2>👥 二、用户画像分析</h2>
    {make_score_bar(usr_score)}
    <div class="persona-card">
      <h3>目标用户</h3>
      <p>{usr_target}</p>
    </div>
    <div class="info-card purple">
      <strong>购买决策链：</strong>{usr_decision}
    </div>
    <p>{usr_detail}</p>
"""

    if usr_personas:
        html += '<h3>核心用户画像</h3>'
        persona_colors = ["#DBEAFE", "#D1FAE5", "#FEF3C7", "#EDE9FE"]
        for i, p in enumerate(usr_personas):
            bg = persona_colors[i % len(persona_colors)]
            html += f"""
        <div class="persona-card" style="background:{bg};">
          <strong>{safe_get(p, 'name', '') if isinstance(p, dict) else p}</strong>
          <p style="font-size:13px;margin-top:4px;">{safe_get(p, 'desc', '') if isinstance(p, dict) else ''}</p>
        </div>"""

    html += f"""
    <div class="info-card success">
      <strong>💡 付费意愿：</strong>{level_badge(usr_wtp)} — SaaS用户付费意愿直接影响MRR增长和LTV。B端用户付费意愿通常高于C端。
    </div>
  </div>
"""

    # ============================================================
    # 3. Pain Points & Demand Analysis
    # ============================================================
    pain_score = safe_get(pain, "score", 50)
    pain_items = safe_get(pain, "items", [])
    pain_alternatives = safe_get(pain, "alternatives", [])
    pain_urgency = safe_get(pain, "urgency", "中")
    pain_detail = safe_get(pain, "detail", "暂无详细数据")

    html += f"""
  <!-- 3. Pain Points -->
  <div class="section">
    <h2>🎯 三、需求痛点分析</h2>
    {make_score_bar(pain_score)}
    <p>{pain_detail}</p>
"""

    if pain_items:
        html += '<h3>核心痛点矩阵</h3>'
        for i, pp in enumerate(pain_items):
            severity = safe_get(pp, "severity", "中") if isinstance(pp, dict) else "中"
            sev_colors = {"高": "#EF4444", "中": "#F59E0B", "低": "#10B981"}
            sc = sev_colors.get(severity, "#F59E0B")
            html += f"""
        <div class="pain-card">
          <div style="display:flex;justify-content:space-between;align-items:center;">
            <strong>{safe_get(pp, 'title', '') if isinstance(pp, dict) else pp}</strong>
            <span style="color:{sc};font-size:12px;font-weight:600;">痛点强度：{severity}</span>
          </div>
          <p style="font-size:13px;margin-top:4px;">{safe_get(pp, 'desc', '') if isinstance(pp, dict) else ''}</p>
        </div>"""

    if pain_alternatives:
        html += '<h3>用户当前替代方案</h3><ul>'
        for alt in pain_alternatives:
            html += f'<li>{alt if isinstance(alt, str) else safe_get(alt, "name", "") + " — " + safe_get(alt, "desc", "")}</li>'
        html += '</ul>'

    html += f"""
    <div class="info-card warn">
      <strong>⚠️ 需求迫切度：</strong>{level_badge(pain_urgency)} — {("用户痛点强烈且缺乏好方案，产品切入机会大" if pain_urgency == "高" else "有一定痛点但替代方案较多，需差异化突破" if pain_urgency == "中" else "痛点不显著，需谨慎验证用户是否愿意为此付费")}
    </div>
  </div>
"""

    # ============================================================
    # 4. Competition Landscape
    # ============================================================
    comp_score = safe_get(competitors, "score", 50)
    comp_direct = safe_get(competitors, "direct_count", "未知")
    comp_indirect = safe_get(competitors, "indirect_count", "未知")
    comp_saturation = safe_get(competitors, "saturation", "中等")
    comp_top = safe_get(competitors, "top_products", [])
    comp_diff = safe_get(competitors, "differentiation", "暂无分析")
    comp_detail = safe_get(competitors, "detail", "暂无详细数据")
    comp_moat = safe_get(competitors, "moat", "低")

    sat_color = "#10B981" if comp_saturation in ["低", "蓝海"] else ("#F59E0B" if "中" in str(comp_saturation) else "#EF4444")

    html += f"""
  <!-- 4. Competition -->
  <div class="section">
    <h2>⚔️ 四、竞品格局分析</h2>
    {make_score_bar(comp_score)}
    <div class="stat-row">
      <div class="stat-card blue">
        <div class="stat-label">直接竞品</div>
        <div class="stat-value">{comp_direct}</div>
      </div>
      <div class="stat-card amber">
        <div class="stat-label">间接竞品</div>
        <div class="stat-value">{comp_indirect}</div>
      </div>
      <div class="stat-card green">
        <div class="stat-label">市场饱和度</div>
        <div class="stat-value" style="font-size:18px;color:{sat_color};">{comp_saturation}</div>
      </div>
      <div class="stat-card purple">
        <div class="stat-label">护城河潜力</div>
        <div class="stat-value" style="font-size:18px;">{level_badge(comp_moat)}</div>
      </div>
    </div>
    <p>{comp_detail}</p>
"""

    if comp_top:
        html += """
    <h3>头部竞品对比</h3>
    <table>
      <tr><th>产品</th><th>定价模式</th><th>目标客户</th><th>核心优势</th><th>弱点</th></tr>"""
        for c in comp_top:
            html += f"""
      <tr>
        <td><strong>{safe_get(c, 'name', '-')}</strong></td>
        <td>{safe_get(c, 'pricing', '-')}</td>
        <td>{safe_get(c, 'target', '-')}</td>
        <td>{safe_get(c, 'advantage', '-')}</td>
        <td>{safe_get(c, 'weakness', '-')}</td>
      </tr>"""
        html += """
    </table>"""

    html += f"""
    <div class="info-card success">
      <strong>🎯 差异化机会：</strong>{comp_diff}
    </div>
  </div>
"""

    # ============================================================
    # 5. Monetization & SaaS Pricing
    # ============================================================
    mon_score = safe_get(monetization, "score", 50)
    mon_pricing = safe_get(monetization, "pricing_model", "暂无建议")
    mon_arpu = safe_get(monetization, "arpu_estimate", "暂无数据")
    mon_ltv = safe_get(monetization, "ltv_estimate", "暂无数据")
    mon_mrr_12m = safe_get(monetization, "mrr_12m_estimate", "暂无数据")
    mon_detail = safe_get(monetization, "detail", "暂无详细数据")
    mon_tiers = safe_get(monetization, "tiers", [])

    html += f"""
  <!-- 5. Monetization -->
  <div class="section">
    <h2>💰 五、变现能力与SaaS定价</h2>
    {make_score_bar(mon_score)}
    <p>{mon_detail}</p>

    <h3>SaaS 关键指标预估</h3>
    <div class="stat-row">
      <div class="stat-card blue">
        <div class="stat-label">ARPU (月)</div>
        <div class="stat-value">{mon_arpu}</div>
      </div>
      <div class="stat-card green">
        <div class="stat-label">LTV (客户生命周期价值)</div>
        <div class="stat-value">{mon_ltv}</div>
      </div>
      <div class="stat-card purple">
        <div class="stat-label">12个月 MRR 预估</div>
        <div class="stat-value">{mon_mrr_12m}</div>
      </div>
    </div>

    <h3>SaaS 主流定价模式对比</h3>
    <div class="pricing-grid">
      <div class="pricing-model{' active' if '订阅制' in str(mon_pricing) else ''}">
        <div style="font-size:24px;margin-bottom:4px;">🔄</div>
        <div style="font-weight:700;margin-bottom:4px;">订阅制</div>
        <div style="font-size:11px;color:#6B7280;">按月/年收费<br>收入可预测性高</div>
      </div>
      <div class="pricing-model{' active' if '用量' in str(mon_pricing) else ''}">
        <div style="font-size:24px;margin-bottom:4px;">📊</div>
        <div style="font-weight:700;margin-bottom:4px;">用量计费</div>
        <div style="font-size:11px;color:#6B7280;">按API/存储/用户数<br>与大客户对齐</div>
      </div>
      <div class="pricing-model{' active' if 'Freemium' in str(mon_pricing) or '免费' in str(mon_pricing) else ''}">
        <div style="font-size:24px;margin-bottom:4px;">🆓</div>
        <div style="font-weight:700;margin-bottom:4px;">Freemium</div>
        <div style="font-size:11px;color:#6B7280;">免费基础版+付费升级<br>PLG增长飞轮</div>
      </div>
      <div class="pricing-model{' active' if '混合' in str(mon_pricing) else ''}">
        <div style="font-size:24px;margin-bottom:4px;">🎯</div>
        <div style="font-weight:700;margin-bottom:4px;">混合模式</div>
        <div style="font-size:11px;color:#6B7280;">基础订阅+超量计费<br>兼顾稳定与弹性</div>
      </div>
    </div>
    <div class="info-card" style="margin-top:12px;">
      <strong>推荐定价模式：</strong>{mon_pricing}
    </div>
"""

    if mon_tiers:
        html += '<h3>建议定价梯度</h3><table><tr><th>版本</th><th>月费</th><th>年费</th><th>核心功能</th><th>目标用户</th></tr>'
        tier_colors = ["#DBEAFE", "#D1FAE5", "#FEF3C7", "#EDE9FE"]
        for i, t in enumerate(mon_tiers):
            html += f"""
      <tr style="background:{tier_colors[i % len(tier_colors)]};">
        <td><strong>{safe_get(t, 'name', '-')}</strong></td>
        <td>{safe_get(t, 'monthly', '-')}</td>
        <td>{safe_get(t, 'yearly', '-')}</td>
        <td>{safe_get(t, 'features', '-')}</td>
        <td>{safe_get(t, 'target_user', '-')}</td>
      </tr>"""
        html += '</table>'

    html += """
  </div>
"""

    # ============================================================
    # 6. Customer Acquisition
    # ============================================================
    acq_score = safe_get(acquisition, "score", 50)
    acq_cac = safe_get(acquisition, "cac_estimate", "暂无数据")
    acq_channels = safe_get(acquisition, "channels", [])
    acq_plg = safe_get(acquisition, "plg_potential", "中")
    acq_detail = safe_get(acquisition, "detail", "暂无详细数据")

    html += f"""
  <!-- 6. Acquisition -->
  <div class="section">
    <h2>📈 六、获客增长分析</h2>
    {make_score_bar(acq_score)}
    <p>{acq_detail}</p>

    <div class="stat-row">
      <div class="stat-card amber">
        <div class="stat-label">预估 CAC (客户获取成本)</div>
        <div class="stat-value">{acq_cac}</div>
      </div>
      <div class="stat-card purple">
        <div class="stat-label">PLG 增长潜力</div>
        <div class="stat-value" style="font-size:18px;">{level_badge(acq_plg)}</div>
      </div>
    </div>

    <h3>SaaS 获客渠道效率对比</h3>
    <table>
      <tr><th>渠道</th><th>适用阶段</th><th>CAC</th><th>转化率</th><th>可复制性</th><th>SaaS适配度</th></tr>
      <tr><td>内容营销/SEO</td><td>全阶段</td><td>低</td><td>中高</td><td>⭐⭐⭐⭐⭐</td><td>⭐⭐⭐⭐⭐</td></tr>
      <tr><td>产品驱动增长(PLG)</td><td>冷启动-增长</td><td>极低</td><td>高</td><td>⭐⭐⭐⭐⭐</td><td>⭐⭐⭐⭐⭐</td></tr>
      <tr><td>付费广告(SEM)</td><td>增长-规模化</td><td>中高</td><td>中</td><td>⭐⭐⭐</td><td>⭐⭐⭐⭐</td></tr>
      <tr><td>合作伙伴/渠道</td><td>增长-规模化</td><td>中</td><td>中高</td><td>⭐⭐⭐⭐</td><td>⭐⭐⭐⭐</td></tr>
      <tr><td>社区/口碑</td><td>全阶段</td><td>极低</td><td>极高</td><td>⭐⭐</td><td>⭐⭐⭐⭐⭐</td></tr>
      <tr><td>SDR外呼/销售</td><td>规模化</td><td>极高</td><td>低</td><td>⭐⭐</td><td>⭐⭐⭐</td></tr>
    </table>
"""

    if acq_channels:
        html += '<h3>推荐获客组合</h3>'
        for i, ch in enumerate(acq_channels):
            labels = ['一','二','三','四','五']
            html += f"""
        <div class="strategy-card">
          <div style="display:flex;align-items:flex-start;gap:12px;">
            <span class="strategy-num">{labels[i] if i < len(labels) else i+1}</span>
            <div>
              <strong>{safe_get(ch, 'channel', '') if isinstance(ch, dict) else ch}</strong>
              <p style="font-size:13px;color:#6B7280;margin-top:4px;">{safe_get(ch, 'desc', '') if isinstance(ch, dict) else ''}</p>
            </div>
          </div>
        </div>"""

    html += """
  </div>
"""

    # ============================================================
    # 7. Marketing & Promotion
    # ============================================================
    mar_score = safe_get(marketing, "score", 50)
    mar_strategies = safe_get(marketing, "strategies", [])
    mar_content = safe_get(marketing, "content_strategy", "暂无数据")
    mar_brand = safe_get(marketing, "brand_positioning", "暂无数据")
    mar_detail = safe_get(marketing, "detail", "暂无详细数据")

    html += f"""
  <!-- 7. Marketing -->
  <div class="section">
    <h2>📢 七、推广营销策略</h2>
    {make_score_bar(mar_score)}
    <p>{mar_detail}</p>

    <div class="info-card purple">
      <strong>品牌定位：</strong>{mar_brand}
    </div>

    <div class="info-card">
      <strong>内容策略方向：</strong>{mar_content}
    </div>
"""

    if mar_strategies:
        html += '<h3>核心营销策略</h3>'
        for i, st in enumerate(mar_strategies):
            labels = ['一','二','三','四','五','六','七','八']
            html += f"""
        <div class="strategy-card">
          <div style="display:flex;align-items:flex-start;gap:12px;">
            <span class="strategy-num">{labels[i] if i < len(labels) else i+1}</span>
            <div>
              <strong>{safe_get(st, 'title', '') if isinstance(st, dict) else st}</strong>
              <p style="font-size:13px;color:#6B7280;margin-top:4px;">{safe_get(st, 'desc', '') if isinstance(st, dict) else ''}</p>
            </div>
          </div>
        </div>"""

    html += """
    <h3>SaaS 推广阶段规划</h3>
    <div class="timeline">
      <div class="timeline-item">
        <div class="tl-time">第1-2个月 · 冷启动</div>
        <div class="tl-title">内容基建 + 种子用户招募</div>
        <p style="font-size:13px;color:#6B7280;">搭建官网/文档/博客、SEO关键词布局、招募10-50个种子用户深度共创</p>
      </div>
      <div class="timeline-item">
        <div class="tl-time">第3-4个月 · 验证期</div>
        <div class="tl-title">PMF验证 + 口碑传播</div>
        <p style="font-size:13px;color:#6B7280;">收集NPS反馈、优化转化漏斗、在ProductHunt/少数派等平台发布</p>
      </div>
      <div class="timeline-item">
        <div class="tl-time">第5-8个月 · 增长期</div>
        <div class="tl-title">付费投放测试 + 内容矩阵</div>
        <p style="font-size:13px;color:#6B7280;">SEM精准投放、行业KOL合作、知乎/公众号/视频号多平台内容分发</p>
      </div>
      <div class="timeline-item">
        <div class="tl-time">第9-12个月 · 规模化</div>
        <div class="tl-title">品牌建设 + 渠道拓展</div>
        <p style="font-size:13px;color:#6B7280;">行业会议演讲、合作伙伴计划、案例营销、出海/多语言扩展</p>
      </div>
    </div>
  </div>
"""

    # ============================================================
    # 8. Cost Structure
    # ============================================================
    cost_score = safe_get(cost, "score", 50)
    cost_cloud = safe_get(cost, "cloud", "2000-10000元/月")
    cost_dev = safe_get(cost, "development", "10-50万")
    cost_tools = safe_get(cost, "tools_saas", "1000-5000元/月")
    cost_ops = safe_get(cost, "ops", "1000-5000元/月")
    cost_marketing_year = safe_get(cost, "marketing_year", "5-30万/年")
    cost_total_1y = safe_get(cost, "total_first_year", "30-100万")
    cost_detail = safe_get(cost, "detail", "暂无详细数据")

    html += f"""
  <!-- 8. Cost Structure -->
  <div class="section">
    <h2>💸 八、成本结构分析</h2>
    {make_score_bar(cost_score)}
    <div class="stat-row">
      <div class="stat-card blue">
        <div class="stat-label">☁️ 云基础设施</div>
        <div class="stat-value" style="font-size:16px;">{cost_cloud}</div>
      </div>
      <div class="stat-card green">
        <div class="stat-label">💻 研发人力</div>
        <div class="stat-value" style="font-size:16px;">{cost_dev}</div>
      </div>
      <div class="stat-card amber">
        <div class="stat-label">🔧 第三方工具</div>
        <div class="stat-value" style="font-size:16px;">{cost_tools}</div>
      </div>
      <div class="stat-card purple">
        <div class="stat-label">📢 营销预算/年</div>
        <div class="stat-value" style="font-size:16px;">{cost_marketing_year}</div>
      </div>
    </div>
    <p style="margin-top:12px;">{cost_detail}</p>
    <div class="info-card" style="background:#F0F9FF;border-color:#1D4ED8;">
      <strong>📊 首年总预算预估：</strong><span style="font-size:22px;font-weight:800;color:#1D4ED8;">{cost_total_1y}</span>
    </div>

    <h3>SaaS 典型成本结构参考（ARR占比）</h3>
    <table>
      <tr><th>成本类别</th><th>早期(<10万ARR)</th><th>成长期(10-100万)</th><th>规模化(>100万)</th></tr>
      <tr><td>研发 (R&D)</td><td>40-60%</td><td>30-40%</td><td>20-30%</td></tr>
      <tr><td>销售与市场 (S&M)</td><td>20-30%</td><td>30-50%</td><td>30-40%</td></tr>
      <tr><td>行政 (G&A)</td><td>10-20%</td><td>10-15%</td><td>8-12%</td></tr>
      <tr><td>云基础设施 (COGS)</td><td>5-15%</td><td>10-20%</td><td>15-25%</td></tr>
      <tr><td>利润空间</td><td>0-15%</td><td>10-20%</td><td>15-25%</td></tr>
    </table>
    <div class="info-card warn">
      <strong>⚠️ 成本提示：</strong>SaaS早期最大成本是研发人力。MVP阶段建议用Serverless/低代码降低云成本，3人以内小团队快速验证PMF。
    </div>
  </div>
"""

    # ============================================================
    # 9. Tech Feasibility (SaaS-specific)
    # ============================================================
    tech_score = safe_get(tech, "score", 50)
    tech_stack = safe_get(tech, "recommended_stack", "暂无建议")
    tech_architecture = safe_get(tech, "architecture", "多租户SaaS架构")
    tech_compliance = safe_get(tech, "compliance", "暂无特殊要求")
    tech_time = safe_get(tech, "time_estimate", "MVP 6-12周")
    tech_detail = safe_get(tech, "detail", "暂无详细数据")
    tech_tips = safe_get(tech, "tips", [])

    html += f"""
  <!-- 9. Tech Feasibility -->
  <div class="section">
    <h2>🔧 九、SaaS技术可行性</h2>
    {make_score_bar(tech_score)}
    <div class="info-card">
      <strong>推荐技术栈：</strong>{tech_stack}
    </div>
    <div class="info-card purple">
      <strong>SaaS 架构模式：</strong>{tech_architecture}
    </div>
    <div class="info-card warn">
      <strong>合规要求：</strong>{tech_compliance}
    </div>
    <p>{tech_detail}</p>

    <div class="info-card success">
      <strong>预估开发周期：</strong>{tech_time}
    </div>
"""

    if tech_tips:
        html += '<h3>SaaS 开发关键踩坑指南</h3><ul>'
        for tip in tech_tips:
            html += f'<li>⚠️ {tip if isinstance(tip, str) else safe_get(tip, "desc", str(tip))}</li>'
        html += '</ul>'

    html += """
    <h3>SaaS 技术架构关键决策</h3>
    <table>
      <tr><th>决策点</th><th>选项A（轻量）</th><th>选项B（企业级）</th><th>建议</th></tr>
      <tr>
        <td>租户隔离</td>
        <td>共享数据库+逻辑隔离</td>
        <td>独立数据库/Schema</td>
        <td>MVP用共享DB，大客户用独立实例</td>
      </tr>
      <tr>
        <td>认证授权</td>
        <td>Supabase Auth / Clerk</td>
        <td>Keycloak / Auth0 Enterprise</td>
        <td>早期用第三方SaaS认证，省时省力</td>
      </tr>
      <tr>
        <td>计费系统</td>
        <td>Stripe + 手动管理</td>
        <td>Chargebee / Recurly</td>
        <td>先用Stripe，ARR>50万时上专业计费</td>
      </tr>
      <tr>
        <td>部署方式</td>
        <td>公有云SaaS</td>
        <td>支持私有化部署</td>
        <td>先纯SaaS，大客户需求再考虑私有化</td>
      </tr>
      <tr>
        <td>监控告警</td>
        <td>Sentry + Grafana</td>
        <td>Datadog + PagerDuty</td>
        <td>Sentry免费版足够早期使用</td>
      </tr>
    </table>
  </div>
"""

    # ============================================================
    # 10. Risk Assessment
    # ============================================================
    risk_items = safe_get(risks, "items", [])
    if not risk_items:
        risk_items = [
            {"name": "PMF风险", "level": "高", "desc": "产品与市场需求不匹配是SaaS创业失败的首要原因，35%的SaaS因此死亡"},
            {"name": "获客成本过高", "level": "高", "desc": "CAC持续上升且LTV/CAC<3将导致增长不可持续"},
            {"name": "客户流失风险", "level": "中高", "desc": "SaaS月度流失率>5%意味着年化流失>46%，需强力客户成功体系"},
            {"name": "定价策略失误", "level": "中", "desc": "定价过低无法覆盖成本，定价过高阻碍增长，需持续A/B测试"},
            {"name": "竞争替代风险", "level": "中", "desc": "大厂/开源项目可能免费提供类似功能，削弱付费意愿"},
            {"name": "安全合规风险", "level": "中", "desc": "数据泄露、等保要求、GDPR等合规成本可能超出预期"},
        ]

    html += """
  <!-- 10. Risks -->
  <div class="section">
    <h2>⚠️ 十、风险提示</h2>
    <div class="risk-grid">
"""
    level_colors = {"高": "#EF4444", "中高": "#F97316", "中": "#F59E0B", "中低": "#3B82F6", "低": "#10B981"}
    for risk in risk_items:
        r_level = safe_get(risk, "level", "中")
        r_color = level_colors.get(r_level, "#F59E0B")
        html += f"""
      <div class="risk-item" style="border-left:3px solid {r_color};">
        <div class="risk-level" style="color:{r_color};">⚠️ {r_level}风险</div>
        <strong>{safe_get(risk, 'name', '')}</strong>
        <p style="font-size:13px;margin-top:4px;">{safe_get(risk, 'desc', '')}</p>
      </div>"""
    html += """
    </div>

    <div class="info-card danger" style="margin-top:16px;">
      <strong>🚨 SaaS 创业死亡陷阱 Top 3：</strong>
      <ol style="margin-top:8px;padding-left:20px;">
        <li><strong>没验证PMF就大规模投入</strong> → 先找到10个愿意付费的用户再扩团队</li>
        <li><strong>追求功能大而全</strong> → MVP只做一件事，做到极致再扩展</li>
        <li><strong>忽视客户成功</strong> → 每流失一个客户，需要5个新客户来弥补ARR</li>
      </ol>
    </div>
  </div>
"""

    # ============================================================
    # 11. Final Decision
    # ============================================================
    html += f"""
  <!-- 11. Final Decision -->
  <div class="section" style="background: {score_result['bg']}; border: 2px solid {score_result['color']};">
    <h2>🎯 十一、综合决策建议</h2>
    <div style="text-align:center;padding:20px;">
      <div style="font-size:48px;margin-bottom:8px;">{score_result['icon']}</div>
      <div style="font-size:28px;font-weight:800;color:{score_result['color']};margin-bottom:8px;">{score_result['rating']}</div>
      <div style="font-size:16px;color:#374151;margin-bottom:16px;">综合评分：<span style="font-size:36px;font-weight:900;color:{score_result['color']};">{score_result['total']}</span> / 100</div>
      <p style="max-width:500px;margin:0 auto;color:#6B7280;">{score_result['rating_desc']}</p>
    </div>

    <h3>SaaS 核心优势</h3>
    <ul>
      <li><strong>收入可预测：</strong>订阅制带来稳定的月度经常性收入(MRR)，估值倍数远高于传统软件</li>
      <li><strong>边际成本递减：</strong>服务第1000个客户的成本远低于第1个，规模效应显著</li>
      <li><strong>数据驱动迭代：</strong>产品使用数据实时反馈，可快速迭代优化产品</li>
      <li><strong>全球化潜力：</strong>SaaS天然支持远程交付，不受地域限制</li>
    </ul>

    <h3>SaaS 核心挑战</h3>
    <ul>
      <li><strong>冷启动难度大：</strong>从0到1找到PMF通常需要6-18个月</li>
      <li><strong>客户获取成本高：</strong>B2B SaaS的CAC通常在数百到数千元，需要LTV/CAC>3</li>
      <li><strong>持续投入要求高：</strong>产品迭代、客户成功、安全合规都需要持续投入</li>
      <li><strong>竞争壁垒建立慢：</strong>纯功能优势容易被复制，需构建数据/网络/品牌护城河</li>
    </ul>

    <h3>下一步行动计划（SaaS MVP路径）</h3>
    <table>
      <tr><th>优先级</th><th>行动项</th><th>建议时间</th><th>关键产出</th></tr>
      <tr><td><span class="tag tag-red">P0</span></td><td>完成10-20个目标用户深度访谈，验证痛点假设</td><td>第1-2周</td><td>用户痛点报告 + PMF假设文档</td></tr>
      <tr><td><span class="tag tag-red">P0</span></td><td>深入体验3-5款头部竞品，输出竞品分析矩阵</td><td>第1-2周</td><td>竞品功能对比表 + 差异化定位</td></tr>
      <tr><td><span class="tag tag-red">P0</span></td><td>确定SaaS定价模型，做定价意愿小范围调研</td><td>第2-3周</td><td>定价方案V1 + 用户付费意愿数据</td></tr>
      <tr><td><span class="tag tag-yellow">P1</span></td><td>设计MVP功能范围，制作Figma原型</td><td>第2-3周</td><td>MVP PRD + 交互原型</td></tr>
      <tr><td><span class="tag tag-yellow">P1</span></td><td>搭建技术基础设施（CI/CD、监控、多租户框架）</td><td>第3-4周</td><td>技术架构文档 + 开发环境就绪</td></tr>
      <tr><td><span class="tag tag-yellow">P1</span></td><td>注册域名、搭建官网、SEO基础建设</td><td>第3-4周</td><td>Landing Page上线 + 基础SEO</td></tr>
      <tr><td><span class="tag tag-yellow">P1</span></td><td>启动MVP开发（核心功能+支付集成）</td><td>第4-12周</td><td>可用的MVP产品</td></tr>
      <tr><td><span class="tag tag-green">P2</span></td><td>灰度发布 + 种子用户招募（目标：10个付费用户）</td><td>第8-12周</td><td>10个付费客户 + NPS数据</td></tr>
      <tr><td><span class="tag tag-green">P2</span></td><td>建立客户成功体系（onboarding流程、知识库）</td><td>第12周起</td><td>客户成功SOP + 帮助中心</td></tr>
      <tr><td><span class="tag tag-blue">P3</span></td><td>数据驱动迭代（分析留存、转化漏斗、功能使用率）</td><td>第12周起持续</td><td>月度数据分析报告</td></tr>
      <tr><td><span class="tag tag-blue">P3</span></td><td>A/B测试定价方案，优化转化率</td><td>第16周起</td><td>定价优化方案</td></tr>
    </table>

    <div class="info-card success" style="margin-top:16px;">
      <strong>🎯 SaaS 成功的唯一指标：</strong>找到一群愿意持续付费的用户，且获取他们的成本低于他们带来的价值（LTV/CAC > 3）。在验证这个公式之前，克制扩张冲动。
    </div>
  </div>

  <!-- Footer -->
  <div class="footer">
    <p>☁️ 本报告由 AI 辅助生成 · 数据来源：公开信息搜索 · 仅供参考，不构成投资建议</p>
    <p>报告生成时间：{now} | SaaS辅助决策系统 v1.0</p>
  </div>

</div>
</body>
</html>"""

    return html


# ============================================================
# CLI Entry Point
# ============================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(description="SaaS产品可行性决策报告生成器")
    parser.add_argument("--name", required=True, help="产品名称")
    parser.add_argument("--category", required=True, help="行业/方向")
    parser.add_argument("--output", required=True, help="输出HTML文件路径")
    parser.add_argument("--scores", default="{}", help="评分JSON")
    parser.add_argument("--market-demand", default="{}", help="市场需求数据JSON")
    parser.add_argument("--user-profile", default="{}", help="用户画像数据JSON")
    parser.add_argument("--pain-points", default="{}", help="需求痛点数据JSON")
    parser.add_argument("--competition", default="{}", help="竞品数据JSON")
    parser.add_argument("--monetization", default="{}", help="变现定价数据JSON")
    parser.add_argument("--acquisition", default="{}", help="获客增长数据JSON")
    parser.add_argument("--marketing", default="{}", help="推广营销数据JSON")
    parser.add_argument("--cost-structure", default="{}", help="成本结构数据JSON")
    parser.add_argument("--tech-feasibility", default="{}", help="技术可行性数据JSON")
    parser.add_argument("--risks", default="{}", help="风险数据JSON")

    args = parser.parse_args()

    data = {
        "name": args.name,
        "category": args.category,
        "scores": json.loads(args.scores),
        "market_demand": json.loads(args.market_demand),
        "user_profile": json.loads(args.user_profile),
        "pain_points": json.loads(args.pain_points),
        "competition": json.loads(args.competition),
        "monetization": json.loads(args.monetization),
        "acquisition": json.loads(args.acquisition),
        "marketing": json.loads(args.marketing),
        "cost_structure": json.loads(args.cost_structure),
        "tech_feasibility": json.loads(args.tech_feasibility),
        "risks": json.loads(args.risks),
    }

    html = generate_report(data)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")

    print(f"✅ 报告已生成: {output_path}")


if __name__ == "__main__":
    main()
