#!/usr/bin/env python3
"""
选址分析报告生成器
读取 analyze_location.py 输出的JSON数据，生成交互式HTML可视化报告。

Usage:
    python generate_report.py --input analysis_result.json [--output report.html]
"""

import argparse
import json
import sys
import os


def get_grade_color(grade: str) -> str:
    """根据评级返回颜色"""
    if grade.startswith("A"):
        return "#22c55e"
    elif grade.startswith("B"):
        return "#3b82f6"
    elif grade.startswith("C"):
        return "#f59e0b"
    elif grade.startswith("D"):
        return "#ef4444"
    else:
        return "#dc2626"


def get_score_color(score: float) -> str:
    if score >= 85:
        return "#22c55e"
    elif score >= 70:
        return "#3b82f6"
    elif score >= 55:
        return "#f59e0b"
    elif score >= 40:
        return "#ef4444"
    return "#dc2626"


def build_recommendations(scoring: dict, competitors: dict, surroundings: dict) -> list[dict]:
    """生成策略建议"""
    recs = []
    scores = scoring["scores"]

    # 人流量
    if scores["foot_traffic"] < 50:
        recs.append({"priority": "P0", "dimension": "人流量", "icon": "🚶",
                     "advice": "人流量偏低，建议加强线上引流（美团/抖音团购），配合开业促销活动吸引客流。"})
    elif scores["foot_traffic"] >= 80:
        recs.append({"priority": "P1", "dimension": "人流量", "icon": "🚶",
                     "advice": "人流量充足，建议优化店内动线和服务效率，确保高峰期接待能力。"})

    # 竞品
    comp_total = competitors.get("total", 0)
    if scores["competition"] < 50:
        recs.append({"priority": "P0", "dimension": "竞品", "icon": "⚔️",
                     "advice": f"周边{comp_total}家竞品，竞争激烈。建议差异化定位：独特产品、会员体系、场景化营销。"})
    elif scores["competition"] >= 80:
        recs.append({"priority": "P0", "dimension": "竞品", "icon": "⚔️",
                     "advice": "竞品较少，蓝海机会！建议快速铺店抢占市场份额，建立品牌先发优势。"})

    # 用户群体
    if scores["customer_demographics"] < 50:
        recs.append({"priority": "P1", "dimension": "客群", "icon": "👥",
                     "advice": "目标客群密度偏低，建议做详细的市场调研，确认品类与周边人群的匹配度。"})

    # 消费力
    if scores["spending_power"] < 50:
        recs.append({"priority": "P1", "dimension": "消费力", "icon": "💰",
                     "advice": "周边消费配套不足，建议定价策略偏大众化，控制成本结构。"})
    elif scores["spending_power"] >= 80:
        recs.append({"priority": "P2", "dimension": "消费力", "icon": "💰",
                     "advice": "消费配套完善，可考虑中高端定位，提升客单价。"})

    # 交通
    if scores["traffic_pattern"] < 50:
        recs.append({"priority": "P1", "dimension": "交通", "icon": "🚇",
                     "advice": "公共交通不够便利，建议选择靠近地铁口/公交站的位置，或配置充足停车位。"})

    # 通用建议
    recs.append({"priority": "P2", "dimension": "运营", "icon": "📊",
                 "advice": "建议开店后前3个月密切跟踪客流转化率、客单价、复购率等核心指标，持续优化。"})

    return sorted(recs, key=lambda r: {"P0": 0, "P1": 1, "P2": 2}[r["priority"]])


def generate_html(data: dict, output_path: str):
    """生成交互式HTML报告"""
    geo = data.get("geo", {})
    scoring = data.get("scoring", {})
    scores = scoring.get("scores", {})
    competitors = data.get("competitors", {})
    surroundings = data.get("surroundings", {})
    traffic = data.get("traffic", {})
    district = data.get("district", {})
    input_data = data.get("input", {})

    address = geo.get("formatted_address", input_data.get("address", ""))
    store_type = input_data.get("store_type", "")
    radius = input_data.get("radius", 1000)
    grade = scoring.get("grade", "未知")
    overall = scores.get("overall", 0)
    reasons = scoring.get("reasons", {})

    grade_color = get_grade_color(grade)
    score_color = get_score_color(overall)

    recs = build_recommendations(scoring, competitors, surroundings)
    cats = surroundings.get("categories", {})

    # 周边设施详情HTML
    facility_html = ""
    cat_labels = {
        "residential": ("住宅", "🏘️"),
        "office": ("办公", "🏢"),
        "education": ("教育", "🎓"),
        "commercial": ("商业", "🛒"),
        "dining": ("餐饮", "🍽️"),
        "transport": ("交通", "🚇"),
        "medical": ("医疗", "🏥"),
        "entertainment": ("娱乐", "🎬"),
    }
    for key, (label, icon) in cat_labels.items():
        info = cats.get(key, {})
        count = info.get("count", 0)
        density = info.get("density_per_sqkm", 0)
        top5 = info.get("top5", [])
        items = "、".join([t["name"] for t in top5[:3]]) or "无"
        facility_html += f"""
        <div class="facility-card">
            <div class="facility-icon">{icon}</div>
            <div class="facility-info">
                <div class="facility-name">{label}</div>
                <div class="facility-count">{count} 个 <span class="density">密度 {density}/km²</span></div>
                <div class="facility-detail">{items}</div>
            </div>
        </div>"""

    # 竞品列表HTML
    comp_list_html = ""
    for c in competitors.get("top_competitors", [])[:8]:
        comp_list_html += f"""
        <tr>
            <td>{c['name']}</td>
            <td>{c['distance']}m</td>
            <td>{c.get('rating', '-')}</td>
            <td class="address-cell">{c.get('address', '-')}</td>
        </tr>"""

    # 推荐HTML
    rec_html = ""
    for r in recs:
        priority_badge = {"P0": '<span class="badge badge-p0">P0 紧急</span>',
                          "P1": '<span class="badge badge-p1">P1 重要</span>',
                          "P2": '<span class="badge badge-p2">P2 建议</span>'}[r["priority"]]
        rec_html += f"""
        <div class="recommendation">
            <div class="rec-header">{r['icon']} {r['dimension']} {priority_badge}</div>
            <div class="rec-body">{r['advice']}</div>
        </div>"""

    # 竞品距离分布条
    dist_dist = competitors.get("distance_distribution", {})
    near = dist_dist.get("near_0_300m", 0)
    mid = dist_dist.get("mid_300_700m", 0)
    far_pct = dist_dist.get("far_700m_plus", 0)
    total_comp = competitors.get("total", 1)
    if total_comp > 0:
        near_pct = round(near / total_comp * 100)
        mid_pct = round(mid / total_comp * 100)
        farp = 100 - near_pct - mid_pct
    else:
        near_pct = mid_pct = farp = 0

    # 综合评分仪表盘
    circumference = 2 * 3.14159 * 54
    dash_offset = circumference * (1 - overall / 100)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>开店选址分析报告 - {address}</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif; background: #f0f2f5; color: #1a1a2e; line-height: 1.6; }}
.container {{ max-width: 1100px; margin: 0 auto; padding: 20px; }}

/* Header */
.header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 16px; padding: 32px; margin-bottom: 24px; position: relative; overflow: hidden; }}
.header::after {{ content: ''; position: absolute; top: -50%; right: -10%; width: 300px; height: 300px; background: rgba(255,255,255,0.05); border-radius: 50%; }}
.header h1 {{ font-size: 28px; margin-bottom: 8px; }}
.header .subtitle {{ opacity: 0.85; font-size: 15px; }}
.header .meta {{ margin-top: 16px; display: flex; gap: 20px; flex-wrap: wrap; font-size: 13px; opacity: 0.8; }}

/* Score Card */
.score-row {{ display: grid; grid-template-columns: 280px 1fr; gap: 24px; margin-bottom: 24px; }}
@media (max-width: 768px) {{ .score-row {{ grid-template-columns: 1fr; }} }}
.score-card {{ background: white; border-radius: 16px; padding: 32px; text-align: center; box-shadow: 0 2px 12px rgba(0,0,0,0.06); }}
.score-circle {{ position: relative; width: 140px; height: 140px; margin: 0 auto 16px; }}
.score-circle svg {{ transform: rotate(-90deg); }}
.score-value {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 42px; font-weight: 800; color: {score_color}; }}
.score-grade {{ display: inline-block; padding: 6px 20px; border-radius: 20px; font-size: 16px; font-weight: 700; background: {grade_color}15; color: {grade_color}; margin-top: 8px; }}

.radar-card {{ background: white; border-radius: 16px; padding: 24px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); display: flex; align-items: center; justify-content: center; }}

/* Section */
.section {{ background: white; border-radius: 16px; padding: 28px; margin-bottom: 24px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); }}
.section h2 {{ font-size: 20px; margin-bottom: 20px; display: flex; align-items: center; gap: 10px; }}
.section h2 .dot {{ width: 8px; height: 8px; border-radius: 50%; background: #667eea; }}

/* Traffic badge */
.traffic-badge {{ display: inline-flex; align-items: center; gap: 8px; padding: 10px 20px; border-radius: 12px; font-size: 16px; font-weight: 600; }}
.traffic-badge.green {{ background: #dcfce7; color: #166534; }}
.traffic-badge.yellow {{ background: #fef9c3; color: #854d0e; }}
.traffic-badge.orange {{ background: #ffedd5; color: #9a3412; }}
.traffic-badge.red {{ background: #fee2e2; color: #991b1b; }}
.traffic-badge.gray {{ background: #f3f4f6; color: #6b7280; }}

/* Facility Grid */
.facility-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 12px; }}
.facility-card {{ display: flex; gap: 12px; padding: 14px; background: #f8fafc; border-radius: 12px; border: 1px solid #e2e8f0; }}
.facility-icon {{ font-size: 28px; flex-shrink: 0; }}
.facility-info {{ flex: 1; min-width: 0; }}
.facility-name {{ font-weight: 600; font-size: 14px; color: #334155; }}
.facility-count {{ font-size: 20px; font-weight: 700; color: #1e293b; }}
.facility-count .density {{ font-size: 12px; font-weight: 400; color: #94a3b8; }}
.facility-detail {{ font-size: 12px; color: #64748b; margin-top: 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}

/* Table */
.comp-table {{ width: 100%; border-collapse: collapse; }}
.comp-table th {{ background: #f8fafc; padding: 12px 16px; text-align: left; font-size: 13px; color: #64748b; font-weight: 600; border-bottom: 2px solid #e2e8f0; }}
.comp-table td {{ padding: 12px 16px; border-bottom: 1px solid #f1f5f9; font-size: 14px; }}
.comp-table tr:hover td {{ background: #f8fafc; }}
.address-cell {{ max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}

/* Distance Distribution */
.dist-bar {{ height: 24px; border-radius: 12px; display: flex; overflow: hidden; margin: 12px 0; }}
.dist-bar .near {{ background: #ef4444; }}
.dist-bar .mid {{ background: #f59e0b; }}
.dist-bar .far {{ background: #22c55e; }}
.dist-legend {{ display: flex; gap: 16px; font-size: 12px; color: #64748b; }}

/* Recommendations */
.recommendation {{ padding: 16px; background: #f8fafc; border-radius: 12px; margin-bottom: 10px; border-left: 4px solid #667eea; }}
.rec-header {{ font-weight: 600; margin-bottom: 6px; display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }}
.rec-body {{ font-size: 14px; color: #475569; }}

/* Badges */
.badge {{ display: inline-block; padding: 2px 8px; border-radius: 6px; font-size: 11px; font-weight: 600; }}
.badge-p0 {{ background: #fee2e2; color: #991b1b; }}
.badge-p1 {{ background: #ffedd5; color: #9a3412; }}
.badge-p2 {{ background: #dbeafe; color: #1e40af; }}

/* Insight box */
.insight {{ background: linear-gradient(135deg, #667eea10, #764ba210); border: 1px solid #667eea30; border-radius: 12px; padding: 20px; margin: 16px 0; }}
.insight h3 {{ font-size: 15px; color: #667eea; margin-bottom: 8px; }}
.insight p {{ font-size: 14px; color: #475569; }}

/* Info grid */
.info-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 12px; }}
.info-item {{ padding: 12px; background: #f8fafc; border-radius: 10px; }}
.info-label {{ font-size: 11px; color: #94a3b8; text-transform: uppercase; }}
.info-value {{ font-size: 16px; font-weight: 600; color: #1e293b; margin-top: 4px; }}

/* Map placeholders */
.map-placeholder {{ background: #e2e8f0; border-radius: 12px; height: 300px; display: flex; align-items: center; justify-content: center; color: #94a3b8; font-size: 14px; }}

/* Dimension bars */
.dim-bars {{ display: flex; flex-direction: column; gap: 12px; }}
.dim-bar {{ display: grid; grid-template-columns: 100px 1fr 60px; align-items: center; gap: 12px; }}
.dim-bar .dim-label {{ font-size: 13px; color: #475569; font-weight: 500; text-align: right; }}
.dim-bar .dim-track {{ height: 10px; background: #f1f5f9; border-radius: 5px; overflow: hidden; }}
.dim-bar .dim-fill {{ height: 100%; border-radius: 5px; transition: width 1s ease; }}
.dim-bar .dim-value {{ font-size: 14px; font-weight: 700; }}

.footer {{ text-align: center; padding: 24px; color: #94a3b8; font-size: 12px; }}
</style>
</head>
<body>
<div class="container">

<!-- ========== Header ========== -->
<div class="header">
    <h1>📍 开店选址分析报告</h1>
    <div class="subtitle">{address} — {store_type}选址评估</div>
    <div class="meta">
        <span>📅 报告时间: {data.get('timestamp', '')}</span>
        <span>🔍 分析半径: {radius}m</span>
        <span>📌 {district.get('name', geo.get('district', ''))}</span>
    </div>
</div>

<!-- ========== Score Row ========== -->
<div class="score-row">
    <div class="score-card">
        <div style="font-size:13px;color:#94a3b8;margin-bottom:8px;">综合选址评分</div>
        <div class="score-circle">
            <svg width="140" height="140" viewBox="0 0 140 140">
                <circle cx="70" cy="70" r="54" fill="none" stroke="#f1f5f9" stroke-width="12"/>
                <circle cx="70" cy="70" r="54" fill="none" stroke="{score_color}" stroke-width="12"
                    stroke-dasharray="{circumference:.1f}" stroke-dashoffset="{dash_offset:.1f}" stroke-linecap="round"/>
            </svg>
            <div class="score-value">{overall}</div>
        </div>
        <div class="score-grade">{grade}</div>
        <p style="font-size:13px;color:#94a3b8;margin-top:12px;">满分 100 分，基于6维综合评估</p>
    </div>

    <div class="radar-card">
        <canvas id="radarChart" width="480" height="400"></canvas>
    </div>
</div>

<!-- ========== 基本信息 ========== -->
<div class="section">
    <h2><span class="dot"></span>基本信息</h2>
    <div class="info-grid">
        <div class="info-item">
            <div class="info-label">分析地址</div>
            <div class="info-value">{address}</div>
        </div>
        <div class="info-item">
            <div class="info-label">经纬度</div>
            <div class="info-value">{geo.get('lng', '-')}, {geo.get('lat', '-')}</div>
        </div>
        <div class="info-item">
            <div class="info-label">开店类型</div>
            <div class="info-value">{store_type}</div>
        </div>
        <div class="info-item">
            <div class="info-label">所属区域</div>
            <div class="info-value">{geo.get('district', '-')} / {geo.get('city', '-')}</div>
        </div>
        <div class="info-item">
            <div class="info-label">分析半径</div>
            <div class="info-value">{radius}m</div>
        </div>
        <div class="info-item">
            <div class="info-label">实时交通状态</div>
            <div class="info-value">{traffic.get('status_text', '未知')}</div>
        </div>
    </div>
</div>

<!-- ========== 实时人流 & 交通态势 ========== -->
<div class="section">
    <h2><span class="dot"></span>📡 实时人流与交通态势</h2>
    <p style="font-size:14px;color:#64748b;margin-bottom:16px;">
        基于高德地图实时交通态势数据（替代摄像头实时画面），评估区域人流活跃度。
        交通拥堵指数越高，通常意味着区域人流越密集、商业活跃度越高。
    </p>
    {f'''
    <div style="margin-bottom:16px;">
        <span class="traffic-badge {"green" if traffic.get("congestion_index", 0) <= 1 else "yellow" if traffic.get("congestion_index", 0) == 2 else "orange" if traffic.get("congestion_index", 0) == 3 else "red" if traffic.get("congestion_index", 0) >= 4 else "gray"}">
            {traffic.get("status_text", "未知")} · 拥堵指数 {traffic.get("congestion_index", "-")}
        </span>
    </div>
    ''' if traffic.get("available") else '''
    <div class="insight">
        <h3>⚠️ 实时交通数据不可用</h3>
        <p>无法获取该区域的实时交通数据，人流评估依赖周边POI密度推算。</p>
    </div>'''}
    <div class="info-grid">
        <div class="info-item">
            <div class="info-label">畅通路段占比</div>
            <div class="info-value">{traffic.get('expedite_pct', '-')}</div>
        </div>
        <div class="info-item">
            <div class="info-label">缓行路段占比</div>
            <div class="info-value">{traffic.get('congested_pct', '-')}</div>
        </div>
        <div class="info-item">
            <div class="info-label">拥堵路段占比</div>
            <div class="info-value">{traffic.get('blocked_pct', '-')}</div>
        </div>
        <div class="info-item">
            <div class="info-label">区域描述</div>
            <div class="info-value" style="font-size:13px;">{traffic.get('description', '无')}</div>
        </div>
    </div>
</div>

<!-- ========== 多维度详细评分 ========== -->
<div class="section">
    <h2><span class="dot"></span>六维详细评分</h2>
    <div class="dim-bars">
        {''.join(f'''
        <div class="dim-bar">
            <div class="dim-label">{{
                "foot_traffic": "人流量",
                "customer_demographics": "用户群体",
                "traffic_pattern": "客流特点",
                "spending_power": "消费情况",
                "competition": "竞品分析",
                "environment": "商业环境"
            }}.get(k, k)
        }} ({scoring.get("weights", {{}}).get(k, 0) * 100:.0f}%)</div>
            <div class="dim-track"><div class="dim-fill" style="width:{v}%;background:{get_score_color(v)};"></div></div>
            <div class="dim-value" style="color:{get_score_color(v)};">{v}</div>
        </div>
        <div style="font-size:12px;color:#94a3b8;margin-left:112px;margin-bottom:8px;">{reasons.get(k, '')}</div>
        ''' for k, v in scores.items() if k != "overall")}
    </div>
</div>

<!-- ========== 周边设施分析 ========== -->
<div class="section">
    <h2><span class="dot"></span>周边设施全景</h2>
    <p style="font-size:14px;color:#64748b;margin-bottom:16px;">
        分析半径{radius}m内的配套设施分布，反映区域人群结构和消费潜力。
    </p>
    <div class="facility-grid">
        {facility_html}
    </div>
</div>

<!-- ========== 竞品分析 ========== -->
<div class="section">
    <h2><span class="dot"></span>竞品分析 — {store_type}</h2>
    <div class="info-grid" style="margin-bottom:20px;">
        <div class="info-item">
            <div class="info-label">竞品总数</div>
            <div class="info-value">{competitors.get('total', 0)} 家</div>
        </div>
        <div class="info-item">
            <div class="info-label">竞争密度</div>
            <div class="info-value">{competitors.get('density_level', '-')}</div>
        </div>
        <div class="info-item">
            <div class="info-label">竞品均分</div>
            <div class="info-value">{competitors.get('avg_rating', '-')}</div>
        </div>
        <div class="info-item">
            <div class="info-label">300m内竞品</div>
            <div class="info-value">{dist_dist.get('near_0_300m', 0)} 家</div>
        </div>
    </div>

    <div class="insight">
        <h3>💡 战略洞察</h3>
        <p>{competitors.get('strategic_insight', '暂无足够数据进行竞品分析。')}</p>
    </div>

    {f'''
    <div style="margin:16px 0;">
        <div style="font-size:13px;color:#64748b;margin-bottom:8px;">竞品距离分布</div>
        <div class="dist-bar">
            <div class="near" style="width:{near_pct}%;" title="0-300m: {near}家"></div>
            <div class="mid" style="width:{mid_pct}%;" title="300-700m: {mid}家"></div>
            <div class="far" style="width:{farp}%;" title="700m+: {far_pct}家"></div>
        </div>
        <div class="dist-legend">
            <span>🔴 0-300m: {near}家 ({near_pct}%)</span>
            <span>🟡 300-700m: {mid}家 ({mid_pct}%)</span>
            <span>🟢 700m+: {far_pct}家 ({farp}%)</span>
        </div>
    </div>
    ''' if competitors.get('top_competitors') else ''}

    {f'''
    <table class="comp-table">
        <thead><tr><th>竞品名称</th><th>距离</th><th>评分</th><th>地址</th></tr></thead>
        <tbody>{comp_list_html}</tbody>
    </table>
    ''' if comp_list_html else '<p style="color:#94a3b8;">该区域暂未发现同类竞品 — 潜在蓝海市场</p>'}
</div>

<!-- ========== 行动建议 ========== -->
<div class="section">
    <h2><span class="dot"></span>行动建议与策略</h2>
    {rec_html}
</div>

<!-- ========== 数据来源声明 ========== -->
<div class="section" style="font-size:13px;color:#64748b;">
    <h2><span class="dot"></span>数据来源与说明</h2>
    <ul style="padding-left:20px;line-height:2;">
        <li><strong>高德地图API</strong>：地理编码、POI搜索、交通态势、行政区划</li>
        <li><strong>实时人流代理</strong>：通过交通拥堵指数 + POI密度综合推算（公共摄像头数据不可通过API获取）</li>
        <li><strong>用户画像</strong>：基于周边POI类型（住宅/办公/教育/商业密度）推断</li>
        <li><strong>评分算法</strong>：6维度加权评分模型，权重可根据行业调整</li>
        <li><strong>免责声明</strong>：本报告为数据驱动的参考建议，不构成投资决策依据。建议结合实地考察综合判断。</li>
    </ul>
</div>

<div class="footer">
    开店选址分析报告 · 基于高德地图实时数据生成 · 仅供参考
</div>

</div>

<script>
// Radar Chart
const ctx = document.getElementById('radarChart').getContext('2d');
new Chart(ctx, {{
    type: 'radar',
    data: {{
        labels: ['人流量', '用户群体', '客流特点', '消费情况', '竞品分析', '商业环境'],
        datasets: [{{
            label: '{store_type}选址评分',
            data: [
                {scores.get('foot_traffic', 0)},
                {scores.get('customer_demographics', 0)},
                {scores.get('traffic_pattern', 0)},
                {scores.get('spending_power', 0)},
                {scores.get('competition', 0)},
                {scores.get('environment', 0)}
            ],
            backgroundColor: 'rgba(102, 126, 234, 0.2)',
            borderColor: 'rgba(102, 126, 234, 1)',
            borderWidth: 2,
            pointBackgroundColor: 'rgba(102, 126, 234, 1)',
            pointBorderColor: '#fff',
            pointRadius: 5,
            pointHoverRadius: 7,
        }}]
    }},
    options: {{
        responsive: true,
        maintainAspectRatio: false,
        scales: {{
            r: {{
                beginAtZero: true,
                max: 100,
                ticks: {{ stepSize: 20, font: {{ size: 11 }}, backdropColor: 'transparent' }},
                pointLabels: {{ font: {{ size: 13, weight: '600' }}, color: '#475569' }},
                grid: {{ color: '#e2e8f0' }},
            }}
        }},
        plugins: {{
            legend: {{ display: false }},
        }}
    }}
}});
</script>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    return output_path


def main():
    parser = argparse.ArgumentParser(description="选址分析报告生成器")
    parser.add_argument("--input", "-i", required=True, help="分析数据JSON文件路径")
    parser.add_argument("--output", "-o", default="", help="输出HTML报告路径（默认: <input>_report.html）")

    args = parser.parse_args()

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"读取输入文件失败: {e}", file=sys.stderr)
        sys.exit(1)

    if "error" in data:
        print(f"分析数据包含错误: {data['error']}", file=sys.stderr)
        if "hint" in data:
            print(f"提示: {data['hint']}", file=sys.stderr)
        sys.exit(1)

    output_path = args.output or args.input.replace(".json", "_report.html")

    try:
        report_path = generate_html(data, output_path)
        print(f"报告已生成: {report_path}")
    except Exception as e:
        print(f"生成报告失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
