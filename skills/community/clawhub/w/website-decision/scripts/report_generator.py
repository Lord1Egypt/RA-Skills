#!/usr/bin/env python3
"""
网站开发辅助决策报告生成器
Generate professional feasibility decision report for Website Development.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# ============================================================
# Scoring Engine
# ============================================================

DIMENSIONS = {
    "search_heat": {"name": "搜索热度", "weight": 0.25, "icon": "🔍"},
    "competition": {"name": "竞争格局", "weight": 0.20, "icon": "⚔️"},
    "market": {"name": "市场前景", "weight": 0.20, "icon": "📈"},
    "monetization": {"name": "变现能力", "weight": 0.15, "icon": "💰"},
    "dev_feasibility": {"name": "开发可行性", "weight": 0.10, "icon": "🔧"},
    "traffic": {"name": "流量获取", "weight": 0.10, "icon": "🚀"},
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
        rating_desc = "市场机会明确，竞争格局有利，建议尽快立项推进"
        color = "#10B981"
        bg = "#ECFDF5"
        icon = "🚀"
    elif total >= 65:
        rating = "🟡 谨慎推进"
        rating_desc = "有一定市场机会，但需要差异化策略和更深入的需求验证"
        color = "#F59E0B"
        bg = "#FFFBEB"
        icon = "🔍"
    elif total >= 50:
        rating = "⚠️ 暂缓观望"
        rating_desc = "市场风险较高，建议先验证核心假设后再决定是否投入"
        color = "#F97316"
        bg = "#FFF7ED"
        icon = "⏸️"
    else:
        rating = "❌ 不建议做"
        rating_desc = "当前市场条件下风险过高，建议调整方向或等待时机"
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
# Data processing helpers
# ============================================================

def safe_get(d, key, default=""):
    """Safely get nested dict value."""
    if isinstance(d, dict):
        return d.get(key, default)
    return default


def make_score_bar(score, max_score=100):
    """Generate an HTML score bar."""
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
    """Generate a colored tag."""
    return f'<span style="display:inline-block;padding:3px 10px;background:{color}15;color:{color};border-radius:12px;font-size:12px;font-weight:600;margin:2px;">{text}</span>'


def level_badge(level):
    """Generate a colored level badge."""
    colors = {
        "高": ("#EF4444", "#FEE2E2"),
        "中高": ("#F97316", "#FFF7ED"),
        "中等": ("#F59E0B", "#FEF3C7"),
        "中低": ("#3B82F6", "#DBEAFE"),
        "低": ("#10B981", "#D1FAE5"),
        "困难": ("#EF4444", "#FEE2E2"),
        "容易": ("#10B981", "#D1FAE5"),
    }
    c, bg = colors.get(level, ("#6B7280", "#F3F4F6"))
    return f'<span style="display:inline-block;padding:2px 8px;background:{bg};color:{c};border-radius:8px;font-size:12px;font-weight:600;">{level}</span>'


# ============================================================
# HTML Report Generator
# ============================================================

def generate_report(data: dict) -> str:
    """Generate the complete HTML decision report for website development."""

    name = safe_get(data, "name", "未命名产品")
    category = safe_get(data, "category", "未指定类型")
    now = datetime.now().strftime("%Y年%m月%d日 %H:%M")

    # Extract scores
    scores = safe_get(data, "scores", {})
    score_result = calculate_total_score(scores)

    # Extract sections
    search_heat = safe_get(data, "search_heat", {})
    competitors = safe_get(data, "competitors", {})
    industry = safe_get(data, "industry", {})
    traffic = safe_get(data, "traffic", {})
    user_analysis = safe_get(data, "user_analysis", {})
    business_model = safe_get(data, "business_model", {})
    cost = safe_get(data, "cost", {})
    promotion = safe_get(data, "promotion", {})
    development = safe_get(data, "development", {})
    risks = safe_get(data, "risks", {})

    # ============================================================
    # HTML Template
    # ============================================================
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>网站开发可行性决策报告 - {name}</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif; background: #F3F4F6; color: #1F2937; line-height:1.7; }}
  .container {{ max-width: 960px; margin: 0 auto; padding: 20px; }}

  /* Cover */
  .cover {{ background: linear-gradient(135deg, #0F172A 0%, #1E3A5F 50%, #2563EB 100%); color: white; padding: 60px 40px; border-radius: 16px; text-align: center; margin-bottom: 24px; position: relative; overflow: hidden; }}
  .cover::before {{ content: ''; position: absolute; top: -50%; right: -20%; width: 500px; height: 500px; background: radial-gradient(circle, rgba(59,130,246,0.3) 0%, transparent 70%); border-radius: 50%; }}
  .cover::after {{ content: ''; position: absolute; bottom: -30%; left: -10%; width: 400px; height: 400px; background: radial-gradient(circle, rgba(16,185,129,0.2) 0%, transparent 70%); border-radius: 50%; }}
  .cover h1 {{ font-size: 34px; font-weight: 800; margin-bottom: 8px; position: relative; }}
  .cover .subtitle {{ font-size: 18px; opacity: 0.7; position: relative; }}
  .cover .date {{ font-size: 13px; opacity: 0.5; margin-top: 12px; position: relative; }}

  /* Score Card */
  .score-card {{ background: {score_result['bg']}; border: 2px solid {score_result['color']}; border-radius: 16px; padding: 32px; text-align: center; margin-bottom: 24px; }}
  .score-card .big-score {{ font-size: 72px; font-weight: 900; color: {score_result['color']}; line-height: 1; }}
  .score-card .rating {{ font-size: 24px; font-weight: 700; color: {score_result['color']}; margin: 8px 0; }}
  .score-card .rating-desc {{ font-size: 14px; color: #6B7280; max-width: 500px; margin: 0 auto; }}

  /* Section */
  .section {{ background: white; border-radius: 16px; padding: 32px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }}
  .section h2 {{ font-size: 22px; font-weight: 700; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }}
  .section h3 {{ font-size: 16px; font-weight: 600; color: #374151; margin: 16px 0 8px; }}
  .section p {{ margin-bottom: 10px; color: #4B5563; font-size: 14px; }}
  .section ul {{ padding-left: 20px; margin: 8px 0; }}
  .section li {{ color: #4B5563; font-size: 14px; margin: 4px 0; }}

  /* Dimension grid */
  .dim-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin: 16px 0; }}
  @media (max-width: 600px) {{ .dim-grid {{ grid-template-columns: 1fr; }} }}
  .dim-card {{ background: #F9FAFB; border-radius: 12px; padding: 20px; text-align: center; transition: transform 0.2s; }}
  .dim-card:hover {{ transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.08); }}
  .dim-card .dim-icon {{ font-size: 28px; margin-bottom: 8px; }}
  .dim-card .dim-name {{ font-size: 13px; color: #6B7280; margin-bottom: 4px; }}
  .dim-card .dim-score {{ font-size: 28px; font-weight: 800; }}
  .dim-card .dim-weight {{ font-size: 11px; color: #9CA3AF; }}

  /* Info card */
  .info-card {{ background: #F0F9FF; border-left: 4px solid #3B82F6; border-radius: 0 8px 8px 0; padding: 16px 20px; margin: 12px 0; }}
  .info-card.warn {{ background: #FFFBEB; border-color: #F59E0B; }}
  .info-card.success {{ background: #ECFDF5; border-color: #10B981; }}
  .info-card.danger {{ background: #FEF2F2; border-color: #EF4444; }}
  .info-card.purple {{ background: #F5F3FF; border-color: #8B5CF6; }}

  /* Table */
  table {{ width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 13px; }}
  th {{ background: #F9FAFB; padding: 10px 14px; text-align: left; font-weight: 600; color: #374151; border-bottom: 2px solid #E5E7EB; }}
  td {{ padding: 10px 14px; border-bottom: 1px solid #F3F4F6; color: #4B5563; }}
  tr:hover td {{ background: #F9FAFB; }}

  /* Tags */
  .tag {{ display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; margin: 2px; }}
  .tag-blue {{ background: #DBEAFE; color: #1D4ED8; }}
  .tag-green {{ background: #D1FAE5; color: #065F46; }}
  .tag-yellow {{ background: #FEF3C7; color: #92400E; }}
  .tag-red {{ background: #FEE2E2; color: #991B1B; }}
  .tag-purple {{ background: #EDE9FE; color: #5B21B6; }}

  /* Cost grid */
  .cost-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }}
  @media (max-width: 600px) {{ .cost-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
  .cost-item {{ background: #F9FAFB; border-radius: 10px; padding: 16px; text-align: center; }}
  .cost-item .cost-label {{ font-size: 12px; color: #6B7280; margin-bottom: 4px; }}
  .cost-item .cost-value {{ font-size: 18px; font-weight: 700; color: #1F2937; }}

  /* Strategy cards */
  .strategy-card {{ background: #F9FAFB; border-radius: 12px; padding: 20px; margin: 8px 0; border: 1px solid #E5E7EB; }}
  .strategy-card .strategy-num {{ display: inline-block; width: 28px; height: 28px; background: #3B82F6; color: white; border-radius: 50%; text-align: center; line-height: 28px; font-size: 14px; font-weight: 700; margin-right: 8px; }}

  /* Risk grid */
  .risk-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }}
  @media (max-width: 600px) {{ .risk-grid {{ grid-template-columns: 1fr; }} }}
  .risk-item {{ background: #F9FAFB; border-radius: 10px; padding: 16px; }}
  .risk-item .risk-level {{ font-size: 12px; font-weight: 600; margin-bottom: 4px; }}

  /* User persona */
  .persona-card {{ background: linear-gradient(135deg, #F0F9FF, #ECFDF5); border-radius: 12px; padding: 20px; margin: 8px 0; }}

  /* Timeline */
  .timeline {{ position: relative; padding-left: 24px; margin: 16px 0; }}
  .timeline::before {{ content: ''; position: absolute; left: 8px; top: 0; bottom: 0; width: 2px; background: #E5E7EB; }}
  .timeline-item {{ position: relative; margin-bottom: 16px; }}
  .timeline-item::before {{ content: ''; position: absolute; left: -20px; top: 4px; width: 12px; height: 12px; border-radius: 50%; border: 2px solid #3B82F6; background: white; }}
  .timeline-item .tl-time {{ font-size: 12px; color: #9CA3AF; }}
  .timeline-item .tl-title {{ font-weight: 600; color: #1F2937; }}

  /* Footer */
  .footer {{ text-align: center; padding: 24px; color: #9CA3AF; font-size: 12px; }}

  /* Print */
  @media print {{ body {{ background: white; }} .section {{ box-shadow: none; break-inside: avoid; }} }}
</style>
</head>
<body>
<div class="container">

  <!-- Cover -->
  <div class="cover">
    <h1>🌐 {name}</h1>
    <div class="subtitle">{category}</div>
    <div class="date">网站开发可行性决策报告 · {now}</div>
  </div>

  <!-- Score Card -->
  <div class="score-card">
    <div class="big-score">{score_result['total']}</div>
    <div class="rating">{score_result['icon']} {score_result['rating']}</div>
    <div class="rating-desc">{score_result['rating_desc']}</div>
  </div>

  <!-- Dimension Scores -->
  <div class="section">
    <h2>📊 多维度评分矩阵</h2>
    <div class="dim-grid">
"""

    # Dimension cards
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
    # 1. Search Heat Section
    # ============================================================
    sh_score = safe_get(search_heat, "score", 50)
    sh_trend = safe_get(search_heat, "trend", "平稳")
    sh_volume = safe_get(search_heat, "volume", "暂无数据")
    sh_detail = safe_get(search_heat, "detail", "暂无详细数据")
    sh_keywords = safe_get(search_heat, "keywords", [])

    trend_icon = "📈" if "上升" in str(sh_trend) else ("📉" if "下降" in str(sh_trend) else "➡️")
    trend_color = "#10B981" if "上升" in str(sh_trend) else ("#EF4444" if "下降" in str(sh_trend) else "#6B7280")

    html += f"""
  <!-- 1. Search Heat -->
  <div class="section">
    <h2>🔍 一、搜索热度分析</h2>
    {make_score_bar(sh_score)}
    <div style="display:flex;gap:16px;flex-wrap:wrap;">
      <div style="flex:1;min-width:150px;background:#F0F9FF;border-radius:12px;padding:20px;text-align:center;">
        <div style="font-size:13px;color:#6B7280;margin-bottom:4px;">搜索趋势</div>
        <div style="font-size:22px;font-weight:800;color:{trend_color};">{trend_icon} {sh_trend}</div>
      </div>
      <div style="flex:1;min-width:150px;background:#ECFDF5;border-radius:12px;padding:20px;text-align:center;">
        <div style="font-size:13px;color:#6B7280;margin-bottom:4px;">月搜索量</div>
        <div style="font-size:22px;font-weight:800;color:#065F46;">{sh_volume}</div>
      </div>
    </div>
    <p style="margin-top:12px;">{sh_detail}</p>
"""

    if sh_keywords:
        html += '<div style="margin-top:8px;"><strong>关联关键词：</strong> '
        for kw in sh_keywords:
            html += f'<span class="tag tag-blue">{kw}</span> '
        html += '</div>'

    html += """
    <div class="info-card">
      <strong>💡 搜索热度解读：</strong>搜索量反映用户主动需求强度。上升趋势+高搜索量=强市场需求信号；下降趋势需要警惕市场萎缩风险。
    </div>
  </div>
"""

    # ============================================================
    # 2. Competitors Section
    # ============================================================
    comp_count = safe_get(competitors, "count", "未知")
    comp_top3 = safe_get(competitors, "top3", [])
    comp_detail = safe_get(competitors, "detail", "暂无详细数据")
    comp_saturation = safe_get(competitors, "saturation", "中等")
    comp_opportunity = safe_get(competitors, "opportunity", "暂无分析")

    sat_color = "#10B981" if "低" in str(comp_saturation) else ("#F59E0B" if "中" in str(comp_saturation) else "#EF4444")

    html += f"""
  <!-- 2. Competitors -->
  <div class="section">
    <h2>⚔️ 二、竞品格局分析</h2>
    <div class="info-card">
      <strong>同类网站数量：</strong>约 <span style="font-size:20px;font-weight:800;color:#3B82F6;">{comp_count}</span> 个 &nbsp;&nbsp;
      <strong>市场饱和度：</strong><span style="color:{sat_color};font-weight:700;">{comp_saturation}</span>
    </div>
    <p>{comp_detail}</p>
"""

    if comp_top3:
        html += """
    <h3>头部竞品</h3>
    <table>
      <tr><th>排名</th><th>网站名称</th><th>核心功能</th><th>月访问量</th><th>优势</th></tr>"""
        for i, c in enumerate(comp_top3):
            html += f"""
      <tr>
        <td>#{i+1}</td>
        <td><strong>{safe_get(c, 'name', '未知')}</strong></td>
        <td>{safe_get(c, 'feature', '-')}</td>
        <td>{safe_get(c, 'traffic', '-')}</td>
        <td>{safe_get(c, 'advantage', '-')}</td>
      </tr>"""
        html += """
    </table>"""

    html += f"""
    <div class="info-card success">
      <strong>🎯 差异化机会：</strong>{comp_opportunity}
    </div>
  </div>
"""

    # ============================================================
    # 3. Industry Market
    # ============================================================
    market_size = safe_get(industry, "market_size", "暂无数据")
    growth = safe_get(industry, "growth", "暂无数据")
    ind_detail = safe_get(industry, "detail", "暂无详细数据")
    policy = safe_get(industry, "policy", "暂无特殊政策风险")
    trend_desc = safe_get(industry, "trend_desc", "")

    html += f"""
  <!-- 3. Industry -->
  <div class="section">
    <h2>📈 三、行业市场分析</h2>
    <div style="display:flex;gap:16px;flex-wrap:wrap;">
      <div style="flex:1;min-width:180px;background:#F0F9FF;border-radius:12px;padding:20px;text-align:center;">
        <div style="font-size:13px;color:#6B7280;margin-bottom:4px;">市场规模</div>
        <div style="font-size:24px;font-weight:800;color:#1D4ED8;">{market_size}</div>
      </div>
      <div style="flex:1;min-width:180px;background:#ECFDF5;border-radius:12px;padding:20px;text-align:center;">
        <div style="font-size:13px;color:#6B7280;margin-bottom:4px;">年增长率</div>
        <div style="font-size:24px;font-weight:800;color:#065F46;">{growth}</div>
      </div>
    </div>
    <p style="margin-top:12px;">{ind_detail}</p>
"""

    if trend_desc:
        html += f"""
    <div class="info-card purple">
      <strong>📊 行业趋势：</strong>{trend_desc}
    </div>"""

    html += f"""
    <div class="info-card">
      <strong>📋 政策环境：</strong>{policy}
    </div>
  </div>
"""

    # ============================================================
    # 4. User Analysis
    # ============================================================
    ua_target = safe_get(user_analysis, "target_users", "暂无数据")
    ua_pain_points = safe_get(user_analysis, "pain_points", [])
    ua_scenarios = safe_get(user_analysis, "scenarios", [])
    ua_detail = safe_get(user_analysis, "detail", "暂无详细数据")

    html += f"""
  <!-- 4. User Analysis -->
  <div class="section">
    <h2>👥 四、用户画像分析</h2>
    <div class="persona-card">
      <h3>目标用户</h3>
      <p>{ua_target}</p>
    </div>
    <p>{ua_detail}</p>
"""

    if ua_pain_points:
        html += '<h3>核心需求痛点</h3><ul>'
        for pp in ua_pain_points:
            html += f'<li><strong>{safe_get(pp, "title", "") if isinstance(pp, dict) else pp}</strong>{": " + safe_get(pp, "desc", "") if isinstance(pp, dict) else ""}</li>'
        html += '</ul>'

    if ua_scenarios:
        html += '<h3>典型使用场景</h3><ul>'
        for sc in ua_scenarios:
            html += f'<li>{sc if isinstance(sc, str) else safe_get(sc, "desc", str(sc))}</li>'
        html += '</ul>'

    html += """
    <div class="info-card success">
      <strong>💡 用户洞察：</strong>明确目标用户的"谁、什么场景、解决什么问题"三要素，是产品成功的基石。
    </div>
  </div>
"""

    # ============================================================
    # 5. Traffic Potential
    # ============================================================
    traf_search_volume = safe_get(traffic, "search_volume", "中等")
    traf_seo = safe_get(traffic, "seo_difficulty", "中等")
    traf_social = safe_get(traffic, "social_potential", "中等")
    traf_content = safe_get(traffic, "content_potential", "中等")
    traf_detail = safe_get(traffic, "detail", "暂无详细数据")

    html += f"""
  <!-- 5. Traffic -->
  <div class="section">
    <h2>🚀 五、流量潜力评估</h2>
    <table>
      <tr><th>流量渠道</th><th>潜力评级</th><th>获取难度</th><th>转化率预估</th></tr>
      <tr>
        <td>搜索引擎(SEO)</td>
        <td>{level_badge(traf_search_volume)}</td>
        <td>{level_badge(traf_seo)}</td>
        <td>⭐⭐⭐⭐ 高</td>
      </tr>
      <tr>
        <td>社交媒体</td>
        <td>{level_badge(traf_social)}</td>
        <td>中等</td>
        <td>⭐⭐⭐ 中高</td>
      </tr>
      <tr>
        <td>内容营销</td>
        <td>{level_badge(traf_content)}</td>
        <td>中等</td>
        <td>⭐⭐⭐⭐ 高</td>
      </tr>
      <tr>
        <td>付费广告(SEM)</td>
        <td>中等</td>
        <td>低（需预算）</td>
        <td>⭐⭐⭐ 中高</td>
      </tr>
      <tr>
        <td>直接访问/口碑</td>
        <td>中低</td>
        <td>高（需品牌积累）</td>
        <td>⭐⭐⭐⭐⭐ 极高</td>
      </tr>
    </table>
    <p>{traf_detail}</p>
    <div class="info-card success">
      <strong>💡 流量策略优先级：</strong>网站初期以SEO内容营销为主力（免费、可持续），逐步叠加社交媒体分发和付费广告精准投放。
    </div>
  </div>
"""

    # ============================================================
    # 6. Business Model
    # ============================================================
    bm_recommend = safe_get(business_model, "recommend", [])
    bm_detail = safe_get(business_model, "detail", "暂无详细数据")
    bm_arpu = safe_get(business_model, "arpu_estimate", "暂无数据")

    html += f"""
  <!-- 6. Business Model -->
  <div class="section">
    <h2>💰 六、商业模式建议</h2>
    <p>{bm_detail}</p>
    <div class="info-card">
      <strong>预估ARPU：</strong>{bm_arpu}
    </div>
"""

    if bm_recommend:
        html += '<div style="display:flex;flex-wrap:wrap;gap:12px;margin:12px 0;">'
        model_colors = ["#1D4ED8", "#065F46", "#92400E", "#7C3AED", "#BE185D", "#0E7490"]
        model_bgs = ["#DBEAFE", "#D1FAE5", "#FEF3C7", "#EDE9FE", "#FCE7F3", "#CFFAFE"]
        for i, bm in enumerate(bm_recommend):
            color = model_colors[i % len(model_colors)]
            bg = model_bgs[i % len(model_bgs)]
            priority = "⭐" * (3 - i) if i < 3 else ""
            html += f"""
        <div style="flex:1;min-width:160px;background:{bg};border-radius:12px;padding:16px;text-align:center;">
          <div style="font-size:20px;margin-bottom:4px;">{priority}</div>
          <div style="font-weight:700;color:{color};margin-bottom:4px;">{safe_get(bm, 'name', '')}</div>
          <div style="font-size:12px;color:#6B7280;">{safe_get(bm, 'desc', '')}</div>
        </div>"""
        html += '</div>'

    html += """
    <h3>网站主流变现模式参考</h3>
    <table>
      <tr><th>模式</th><th>适用场景</th><th>收入潜力</th><th>实现难度</th></tr>
      <tr><td>广告联盟(AdSense等)</td><td>内容/工具类</td><td>⭐~⭐⭐⭐</td><td>低</td></tr>
      <tr><td>电商直销</td><td>实物/虚拟商品</td><td>⭐⭐~⭐⭐⭐⭐⭐</td><td>中</td></tr>
      <tr><td>会员订阅(SaaS)</td><td>工具/社区/知识付费</td><td>⭐⭐⭐~⭐⭐⭐⭐⭐</td><td>中</td></tr>
      <tr><td>佣金/联盟营销</td><td>导购/比价/推荐类</td><td>⭐⭐~⭐⭐⭐⭐</td><td>低</td></tr>
      <tr><td>付费内容/课程</td><td>教育/知识/媒体</td><td>⭐⭐⭐~⭐⭐⭐⭐</td><td>中</td></tr>
      <tr><td>API/SaaS服务</td><td>技术工具/B端服务</td><td>⭐⭐⭐⭐~⭐⭐⭐⭐⭐</td><td>高</td></tr>
      <tr><td>赞助/品牌合作</td><td>垂直社区/评测类</td><td>⭐⭐~⭐⭐⭐</td><td>低</td></tr>
    </table>
  </div>
"""

    # ============================================================
    # 7. Cost Estimation
    # ============================================================
    cost_domain = safe_get(cost, "domain", "50-100元/年")
    cost_hosting = safe_get(cost, "hosting", "300-3000元/月")
    cost_dev = safe_get(cost, "development", "5-30万")
    cost_ops = safe_get(cost, "ops", "1000-5000元/月")
    cost_promotion = safe_get(cost, "promotion", "1-10万/月")
    cost_total = safe_get(cost, "total_first_year", "10-50万")
    cost_detail = safe_get(cost, "detail", "暂无详细数据")

    html += f"""
  <!-- 7. Cost -->
  <div class="section">
    <h2>💸 七、成本估算</h2>
    <div class="cost-grid">
      <div class="cost-item">
        <div class="cost-label">🌐 域名</div>
        <div class="cost-value">{cost_domain}</div>
      </div>
      <div class="cost-item">
        <div class="cost-label">🖥️ 服务器</div>
        <div class="cost-value">{cost_hosting}</div>
      </div>
      <div class="cost-item">
        <div class="cost-label">💻 开发</div>
        <div class="cost-value">{cost_dev}</div>
      </div>
      <div class="cost-item">
        <div class="cost-label">🔧 运维</div>
        <div class="cost-value">{cost_ops}</div>
      </div>
      <div class="cost-item">
        <div class="cost-label">📣 推广</div>
        <div class="cost-value">{cost_promotion}</div>
      </div>
      <div class="cost-item" style="background:#F0F9FF;border:2px solid #3B82F6;">
        <div class="cost-label">📊 首年总预算</div>
        <div class="cost-value" style="color:#1D4ED8;">{cost_total}</div>
      </div>
    </div>
    <p style="margin-top:12px;">{cost_detail}</p>
    <div class="info-card warn">
      <strong>⚠️ 成本提示：</strong>网站开发成本弹性极大，SaaS模板方案可低至几千元，定制开发可能数十万。建议MVP阶段控制预算在5万以内。
    </div>
  </div>
"""

    # ============================================================
    # 8. Promotion Strategy
    # ============================================================
    promo_strategies = safe_get(promotion, "strategies", [])
    promo_detail = safe_get(promotion, "detail", "暂无详细数据")

    html += f"""
  <!-- 8. Promotion -->
  <div class="section">
    <h2>📢 八、推广策略建议</h2>
    <p>{promo_detail}</p>
"""

    if promo_strategies:
        html += '<div style="display:flex;flex-direction:column;gap:10px;">'
        for i, st in enumerate(promo_strategies):
            labels = ['一','二','三','四','五','六','七','八']
            html += f"""
        <div class="strategy-card">
          <div style="display:flex;align-items:flex-start;gap:12px;">
            <span class="strategy-num">{labels[i] if i < len(labels) else i+1}</span>
            <div>
              <strong>{safe_get(st, 'title', '')}</strong>
              <p style="font-size:13px;color:#6B7280;margin-top:4px;">{safe_get(st, 'desc', '')}</p>
            </div>
          </div>
        </div>"""
        html += '</div>'

    html += """
    <h3>网站推广阶段规划</h3>
    <div class="timeline">
      <div class="timeline-item">
        <div class="tl-time">第1-2个月 · 冷启动</div>
        <div class="tl-title">SEO基础建设 + 内容营销起步</div>
        <p style="font-size:13px;color:#6B7280;">技术SEO优化、关键词布局、开始发布高质量内容</p>
      </div>
      <div class="timeline-item">
        <div class="tl-time">第3-4个月 · 增长期</div>
        <div class="tl-title">社交媒体分发 + 外链建设</div>
        <p style="font-size:13px;color:#6B7280;">知乎/小红书/公众号同步分发、行业网站投稿、友情链接</p>
      </div>
      <div class="timeline-item">
        <div class="tl-time">第5-6个月 · 加速期</div>
        <div class="tl-title">付费广告测试 + 口碑裂变</div>
        <p style="font-size:13px;color:#6B7280;">SEM精准投放测试、用户推荐激励机制、KOL合作</p>
      </div>
      <div class="timeline-item">
        <div class="tl-time">第7-12个月 · 规模化</div>
        <div class="tl-title">品牌建设 + 多渠道矩阵</div>
        <p style="font-size:13px;color:#6B7280;">品牌词搜索量积累、多语言/多站点矩阵、数据驱动优化</p>
      </div>
    </div>
  </div>
"""

    # ============================================================
    # 9. Development Guide
    # ============================================================
    dev_tech = safe_get(development, "tech_stack", "前端React/Vue + 后端Python/Node.js/Java + 数据库MySQL/PostgreSQL")
    dev_tips = safe_get(development, "tips", [])
    dev_detail = safe_get(development, "detail", "暂无详细数据")
    dev_time = safe_get(development, "time_estimate", "MVP 4-8周，完整版 12-24周")

    html += f"""
  <!-- 9. Development -->
  <div class="section">
    <h2>🔧 九、技术选型指南</h2>
    <div class="info-card">
      <strong>推荐技术栈：</strong>{dev_tech}
    </div>
    <div class="info-card warn">
      <strong>预估开发周期：</strong>{dev_time}
    </div>
    <p>{dev_detail}</p>
"""

    if dev_tips:
        html += '<h3>关键避坑要点</h3><ul>'
        for tip in dev_tips:
            html += f'<li>⚠️ {tip}</li>'
        html += '</ul>'

    html += """
    <h3>主流技术方案对比</h3>
    <table>
      <tr><th>方案</th><th>适用场景</th><th>开发效率</th><th>性能</th><th>成本</th></tr>
      <tr><td>WordPress/SaaS模板</td><td>内容站、企业站、博客</td><td>⭐⭐⭐⭐⭐</td><td>⭐⭐⭐</td><td>低</td></tr>
      <tr><td>Next.js/Nuxt.js(SSR)</td><td>SEO要求高的内容/电商站</td><td>⭐⭐⭐⭐</td><td>⭐⭐⭐⭐⭐</td><td>中</td></tr>
      <tr><td>React/Vue SPA</td><td>SaaS工具、后台管理系统</td><td>⭐⭐⭐⭐</td><td>⭐⭐⭐⭐</td><td>中</td></tr>
      <tr><td>Python(Django/FastAPI)</td><td>AI/数据驱动型产品</td><td>⭐⭐⭐</td><td>⭐⭐⭐</td><td>中</td></tr>
      <tr><td>Java(Spring Boot)</td><td>大型企业级应用</td><td>⭐⭐</td><td>⭐⭐⭐⭐⭐</td><td>高</td></tr>
    </table>

    <h3>开发检查清单</h3>
    <table>
      <tr><th>阶段</th><th>关键事项</th><th>常见坑</th></tr>
      <tr><td>域名注册</td><td>选.com/.cn域名，简短易记</td><td>域名过长或含特殊字符</td></tr>
      <tr><td>ICP备案</td><td>国内服务器必须备案（约20工作日）</td><td>未备案导致无法上线</td></tr>
      <tr><td>服务器选型</td><td>初期云服务器2C4G足够，按需扩容</td><td>过度配置导致成本浪费</td></tr>
      <tr><td>SSL证书</td><td>必须HTTPS，推荐Let's Encrypt免费</td><td>HTTP导致浏览器警告</td></tr>
      <tr><td>SEO基础</td><td>TDK优化、sitemap、结构化数据</td><td>忽视SEO导致长期无自然流量</td></tr>
      <tr><td>移动适配</td><td>响应式设计，移动端流量占比>50%</td><td>移动端体验差导致高跳出率</td></tr>
      <tr><td>性能优化</td><td>CDN、图片压缩、懒加载、缓存</td><td>加载慢导致用户流失</td></tr>
      <tr><td>数据安全</td><td>SQL注入防护、XSS/CSRF、数据备份</td><td>安全漏洞导致数据泄露</td></tr>
      <tr><td>隐私合规</td><td>隐私政策页面、Cookie同意弹窗</td><td>违规收集信息面临处罚</td></tr>
    </table>
  </div>
"""

    # ============================================================
    # 10. Risk Assessment
    # ============================================================
    risk_items = safe_get(risks, "items", [])
    if not risk_items:
        risk_items = [
            {"name": "政策合规风险", "level": "中", "desc": "ICP备案、内容审核、数据安全法规变化可能影响运营"},
            {"name": "竞争加剧风险", "level": "高", "desc": "互联网行业进入门槛低，同类产品快速涌现"},
            {"name": "流量获取风险", "level": "高", "desc": "SEO见效慢，付费广告成本持续上升"},
            {"name": "变现困难风险", "level": "中", "desc": "用户付费习惯培养需要时间，广告收入需要规模支撑"},
            {"name": "技术迭代风险", "level": "中", "desc": "前端框架更新快，技术栈可能需要频繁升级"},
            {"name": "安全攻击风险", "level": "中", "desc": "DDoS、SQL注入、爬虫等安全威胁持续存在"},
        ]

    html += """
  <!-- 10. Risks -->
  <div class="section">
    <h2>⚠️ 十、风险提示</h2>
    <div class="risk-grid">
"""
    level_colors = {"高": "#EF4444", "中高": "#F97316", "中": "#F59E0B", "中低": "#3B82F6", "低": "#10B981"}
    level_bgs = {"高": "#FEE2E2", "中高": "#FFF7ED", "中": "#FEF3C7", "中低": "#DBEAFE", "低": "#D1FAE5"}
    for risk in risk_items:
        r_level = safe_get(risk, "level", "中")
        r_color = level_colors.get(r_level, "#F59E0B")
        r_bg = level_bgs.get(r_level, "#FEF3C7")
        html += f"""
      <div class="risk-item" style="border-left:3px solid {r_color};">
        <div class="risk-level" style="color:{r_color};">⚠️ {r_level}风险</div>
        <strong>{safe_get(risk, 'name', '')}</strong>
        <p style="font-size:13px;margin-top:4px;">{safe_get(risk, 'desc', '')}</p>
      </div>"""
    html += """
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

    <h3>核心优势</h3>
    <ul>
      <li>网站独立运营，不受平台规则限制，用户和数据完全自主可控</li>
      <li>SEO长尾效应显著，优质内容可持续获取免费流量</li>
      <li>变现模式灵活，可组合广告+订阅+电商多种模式</li>
    </ul>

    <h3>核心劣势</h3>
    <ul>
      <li>冷启动难度大，无平台流量扶持，完全依赖自主获客</li>
      <li>SEO见效周期长（通常3-6个月），前期流量增长缓慢</li>
      <li>开发和运维成本高于小程序/APP轻量方案</li>
    </ul>

    <h3>下一步行动建议</h3>
    <table>
      <tr><th>优先级</th><th>行动项</th><th>建议时间</th></tr>
      <tr><td>P0</td><td>完成详细需求调研与目标用户访谈（10+目标用户）</td><td>第1-2周</td></tr>
      <tr><td>P0</td><td>深入体验3-5款头部竞品，输出竞品分析文档</td><td>第1-2周</td></tr>
      <tr><td>P0</td><td>验证核心商业模式假设（用户付费意愿调研）</td><td>第2周</td></tr>
      <tr><td>P1</td><td>设计MVP功能范围，制作产品原型</td><td>第2-3周</td></tr>
      <tr><td>P1</td><td>注册域名、购买服务器、完成ICP备案</td><td>第3周</td></tr>
      <tr><td>P2</td><td>启动MVP开发（4-8周内完成）</td><td>第4-12周</td></tr>
      <tr><td>P2</td><td>SEO基础建设+内容策略制定</td><td>第4周起持续</td></tr>
      <tr><td>P3</td><td>灰度发布+种子用户招募</td><td>第8-12周</td></tr>
      <tr><td>P3</td><td>数据埋点+用户反馈收集体系建立</td><td>第12周</td></tr>
    </table>
  </div>

  <!-- Footer -->
  <div class="footer">
    <p>🌐 本报告由 AI 辅助生成 · 数据来源：公开信息搜索 · 仅供参考，不构成投资建议</p>
    <p>报告生成时间：{now} | 网站开发辅助决策系统 v1.0</p>
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

    parser = argparse.ArgumentParser(description="网站开发可行性决策报告生成器")
    parser.add_argument("--name", required=True, help="产品名称")
    parser.add_argument("--category", required=True, help="产品类型/方向")
    parser.add_argument("--output", required=True, help="输出HTML文件路径")
    parser.add_argument("--scores", default="{}", help="评分JSON")
    parser.add_argument("--search-heat", default="{}", help="搜索热度数据JSON")
    parser.add_argument("--competitors", default="{}", help="竞品数据JSON")
    parser.add_argument("--industry", default="{}", help="行业数据JSON")
    parser.add_argument("--traffic", default="{}", help="流量数据JSON")
    parser.add_argument("--user-analysis", default="{}", help="用户分析数据JSON")
    parser.add_argument("--business-model", default="{}", help="商业模式数据JSON")
    parser.add_argument("--cost", default="{}", help="成本数据JSON")
    parser.add_argument("--promotion", default="{}", help="推广策略数据JSON")
    parser.add_argument("--development", default="{}", help="开发指南数据JSON")
    parser.add_argument("--risks", default="{}", help="风险数据JSON")

    args = parser.parse_args()

    data = {
        "name": args.name,
        "category": args.category,
        "scores": json.loads(args.scores),
        "search_heat": json.loads(args.search_heat),
        "competitors": json.loads(args.competitors),
        "industry": json.loads(args.industry),
        "traffic": json.loads(args.traffic),
        "user_analysis": json.loads(args.user_analysis),
        "business_model": json.loads(args.business_model),
        "cost": json.loads(args.cost),
        "promotion": json.loads(args.promotion),
        "development": json.loads(args.development),
        "risks": json.loads(args.risks),
    }

    html = generate_report(data)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")

    print(f"✅ 报告已生成: {output_path}")


if __name__ == "__main__":
    main()
