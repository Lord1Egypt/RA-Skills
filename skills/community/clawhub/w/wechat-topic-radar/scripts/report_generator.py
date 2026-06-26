#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
报告生成和可视化模块
生成美观的HTML/图表报告
"""

import json
import os
from typing import List, Dict, Optional
from datetime import datetime
from dataclasses import asdict

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from data_collector import HotTopic
from heat_algorithm import HeatScore
from topic_analyzer import TopicAnalysis


class ReportGenerator:
    """报告生成器"""
    
    def __init__(self, output_dir: str = "./data/reports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_full_report(self, 
                           scores: List[HeatScore],
                           analyses: List[TopicAnalysis],
                           trends: Dict,
                           keywords: List[tuple],
                           recommendations: Dict) -> str:
        """
        生成完整分析报告
        
        Returns:
            HTML报告文件路径
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join(self.output_dir, f"topic_radar_report_{timestamp}.html")
        
        # 生成图表
        charts = self._generate_charts(scores, trends, keywords)
        
        # 生成HTML
        html_content = self._build_html_report(
            scores, analyses, trends, keywords, recommendations, charts
        )
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return report_file
    
    def _generate_charts(self, scores: List[HeatScore], trends: Dict, 
                        keywords: List[tuple]) -> Dict[str, str]:
        """生成可视化图表"""
        charts = {}
        
        # 1. 热度分布饼图
        platform_data = trends.get('platform_distribution', {})
        if platform_data:
            fig = go.Figure(data=[go.Pie(
                labels=list(platform_data.keys()),
                values=[d['count'] for d in platform_data.values()],
                hole=0.4,
                marker=dict(colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'])
            )])
            fig.update_layout(
                title="热点平台分布",
                template="plotly_white",
                height=400
            )
            charts['platform_pie'] = fig.to_html(full_html=False, include_plotlyjs=False)
        
        # 2. TOP10热度条形图
        top10 = scores[:10]
        fig = go.Figure(data=[go.Bar(
            x=[s.total_score for s in top10],
            y=[s.topic.title[:20] + '...' for s in top10],
            orientation='h',
            marker=dict(
                color=[s.total_score for s in top10],
                colorscale='Viridis'
            )
        )])
        fig.update_layout(
            title="TOP 10 热门选题",
            xaxis_title="综合热度分",
            yaxis_title="",
            template="plotly_white",
            height=500,
            yaxis=dict(autorange="reversed")
        )
        charts['top10_bar'] = fig.to_html(full_html=False, include_plotlyjs=False)
        
        # 3. 热度维度雷达图（TOP5）
        if scores:
            top5 = scores[:5]
            categories = ['平台热度', '互动热度', '趋势热度', '内容质量', '爆款潜力']
            
            fig = go.Figure()
            for score in top5:
                fig.add_trace(go.Scatterpolar(
                    r=[
                        score.platform_score,
                        score.interaction_score,
                        score.trend_score,
                        score.quality_score,
                        score.potential_score
                    ],
                    theta=categories,
                    fill='toself',
                    name=score.topic.title[:10]
                ))
            
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=True,
                title="TOP 5 选题热度维度分析",
                height=500
            )
            charts['radar'] = fig.to_html(full_html=False, include_plotlyjs=False)
        
        # 4. 关键词词云图（使用条形图代替）
        if keywords:
            words, weights = zip(*keywords[:15])
            fig = go.Figure(data=[go.Bar(
                x=list(words),
                y=list(weights),
                marker=dict(color=weights, colorscale='Plasma')
            )])
            fig.update_layout(
                title="热门关键词 TOP 15",
                xaxis_title="",
                yaxis_title="权重",
                template="plotly_white",
                height=400
            )
            charts['keywords'] = fig.to_html(full_html=False, include_plotlyjs=False)
        
        # 5. 分类分布图
        category_dist = trends.get('category_distribution', {})
        if category_dist:
            fig = px.treemap(
                names=list(category_dist.keys()),
                parents=[""] * len(category_dist),
                values=list(category_dist.values()),
                title="热点分类分布"
            )
            fig.update_layout(height=400)
            charts['category_tree'] = fig.to_html(full_html=False, include_plotlyjs=False)
        
        return charts
    
    def _build_html_report(self, scores, analyses, trends, keywords, 
                          recommendations, charts) -> str:
        """构建HTML报告"""
        
        # 生成选题推荐HTML
        rec_html = self._generate_recommendations_html(recommendations, analyses)
        
        # 生成详细分析HTML
        detail_html = self._generate_detail_html(analyses[:5])
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>公众号爆款选题雷达报告</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        :root {{
            --primary: #667eea;
            --secondary: #764ba2;
            --success: #48bb78;
            --warning: #ed8936;
            --danger: #f56565;
            --dark: #2d3748;
            --light: #f7fafc;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}
        
        .header .subtitle {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .header .time {{
            margin-top: 15px;
            font-size: 0.9em;
            opacity: 0.8;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        .section-title {{
            font-size: 1.8em;
            color: var(--dark);
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid var(--primary);
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .section-title::before {{
            content: '';
            width: 6px;
            height: 30px;
            background: var(--primary);
            border-radius: 3px;
        }}
        
        .chart-container {{
            background: var(--light);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }}
        
        .stat-card .number {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .stat-card .label {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        
        .topic-card {{
            background: white;
            border: 2px solid #e2e8f0;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            transition: all 0.3s ease;
        }}
        
        .topic-card:hover {{
            border-color: var(--primary);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.2);
            transform: translateY(-2px);
        }}
        
        .topic-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 15px;
        }}
        
        .topic-title {{
            font-size: 1.3em;
            font-weight: bold;
            color: var(--dark);
            flex: 1;
        }}
        
        .topic-score {{
            background: linear-gradient(135deg, var(--success), #38a169);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 1.1em;
        }}
        
        .topic-meta {{
            display: flex;
            gap: 15px;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }}
        
        .meta-tag {{
            background: #edf2f7;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.85em;
            color: #4a5568;
        }}
        
        .angle-section {{
            background: #f7fafc;
            border-radius: 10px;
            padding: 15px;
            margin-top: 15px;
        }}
        
        .angle-title {{
            font-weight: bold;
            color: var(--primary);
            margin-bottom: 10px;
        }}
        
        .angle-item {{
            background: white;
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 8px;
            border-left: 4px solid var(--primary);
        }}
        
        .recommendation-box {{
            background: linear-gradient(135deg, #fff5f5, #fed7d7);
            border: 2px solid var(--danger);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
        }}
        
        .recommendation-box.success {{
            background: linear-gradient(135deg, #f0fff4, #c6f6d5);
            border-color: var(--success);
        }}
        
        .recommendation-box.warning {{
            background: linear-gradient(135deg, #fffaf0, #feebc8);
            border-color: var(--warning);
        }}
        
        .tag {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.8em;
            margin-right: 5px;
            margin-bottom: 5px;
        }}
        
        .tag-hot {{ background: #fed7d7; color: #c53030; }}
        .tag-potential {{ background: #c6f6d5; color: #276749; }}
        .tag-undervalued {{ background: #bee3f8; color: #2c5282; }}
        
        .footer {{
            background: var(--dark);
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 0.9em;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 1.8em; }}
            .content {{ padding: 20px; }}
            .stats-grid {{ grid-template-columns: repeat(2, 1fr); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔥 公众号爆款选题雷达</h1>
            <p class="subtitle">全网热点聚合 · 智能选题分析 · 爆款潜力预测</p>
            <p class="time">生成时间：{datetime.now().strftime("%Y年%m月%d日 %H:%M")}</p>
        </div>
        
        <div class="content">
            <!-- 数据概览 -->
            <div class="section">
                <h2 class="section-title">📊 数据概览</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="number">{len(scores)}</div>
                        <div class="label">采集热点数</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">{len(trends.get('platform_distribution', {}))}</div>
                        <div class="label">覆盖平台</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">{round(sum(s.total_score for s in scores) / len(scores), 1) if scores else 0}</div>
                        <div class="label">平均热度分</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">{len(keywords)}</div>
                        <div class="label">关键词</div>
                    </div>
                </div>
            </div>
            
            <!-- 可视化图表 -->
            <div class="section">
                <h2 class="section-title">📈 可视化分析</h2>
                
                <div class="chart-container">
                    {charts.get('top10_bar', '')}
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div class="chart-container">
                        {charts.get('platform_pie', '')}
                    </div>
                    <div class="chart-container">
                        {charts.get('radar', '')}
                    </div>
                </div>
                
                <div class="chart-container">
                    {charts.get('keywords', '')}
                </div>
            </div>
            
            <!-- 选题推荐 -->
            <div class="section">
                <h2 class="section-title">⭐ 精选选题推荐</h2>
                {rec_html}
            </div>
            
            <!-- 详细分析 -->
            <div class="section">
                <h2 class="section-title">🔍 TOP 5 选题深度分析</h2>
                {detail_html}
            </div>
        </div>
        
        <div class="footer">
            <p>公众号爆款选题雷达 · 智能内容创作助手</p>
            <p>报告生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
    </div>
</body>
</html>"""
        
        return html
    
    def _generate_recommendations_html(self, recommendations: Dict, 
                                     analyses: List[TopicAnalysis]) -> str:
        """生成选题推荐HTML"""
        html = ""
        
        # 当下最热
        hot_now = recommendations.get('hot_now', [])
        if hot_now:
            html += '<div class="recommendation-box">'
            html += '<h3>🔥 当下最热（立即跟进）</h3>'
            for score in hot_now[:3]:
                analysis = next((a for a in analyses if a.original_topic.title == score.topic.title), None)
                angle_title = analysis.angles[0]['suggested_title'] if analysis and analysis.angles else score.topic.title
                
                html += f'''
                <div style="margin: 15px 0; padding: 15px; background: white; border-radius: 10px;">
                    <div style="font-weight: bold; margin-bottom: 8px;">{angle_title}</div>
                    <div style="font-size: 0.9em; color: #666;">
                        来源: {score.topic.platform} | 热度: {score.total_score} | 潜力: {score.potential_score}
                    </div>
                </div>
                '''
            html += '</div>'
        
        # 高潜力
        high_potential = recommendations.get('high_potential', [])
        if high_potential:
            html += '<div class="recommendation-box success">'
            html += '<h3>💎 高潜力选题（提前布局）</h3>'
            for score in high_potential[:3]:
                html += f'''
                <div style="margin: 10px 0;">
                    <span class="tag tag-potential">潜力{score.potential_score}</span>
                    {score.topic.title[:30]}
                </div>
                '''
            html += '</div>'
        
        # 被低估
        undervalued = recommendations.get('undervalued', [])
        if undervalued:
            html += '<div class="recommendation-box warning">'
            html += '<h3>💡 被低估选题（差异化机会）</h3>'
            for score in undervalued[:3]:
                html += f'''
                <div style="margin: 10px 0;">
                    <span class="tag tag-undervalued">互动高</span>
                    {score.topic.title[:30]}
                </div>
                '''
            html += '</div>'
        
        return html
    
    def _generate_detail_html(self, analyses: List[TopicAnalysis]) -> str:
        """生成详细分析HTML"""
        html = ""
        
        for i, analysis in enumerate(analyses, 1):
            topic = analysis.original_topic
            score = analysis.heat_score
            
            html += f'''
            <div class="topic-card">
                <div class="topic-header">
                    <div class="topic-title">{i}. {topic.title}</div>
                    <div class="topic-score">{score.total_score}分</div>
                </div>
                
                <div class="topic-meta">
                    <span class="meta-tag">📱 {topic.platform}</span>
                    <span class="meta-tag">🔥 {topic.hot_score:.0f} 热度</span>
                    {f'<span class="meta-tag">👁 {topic.read_count} 阅读</span>' if topic.read_count else ''}
                    {f'<span class="meta-tag">❤️ {topic.like_count} 点赞</span>' if topic.like_count else ''}
                    {f'<span class="meta-tag">📂 {topic.category}</span>' if topic.category else ''}
                </div>
            '''
            
            # 切入角度
            if analysis.angles:
                html += '<div class="angle-section">'
                html += '<div class="angle-title">🎯 推荐切入角度</div>'
                for angle in analysis.angles[:2]:
                    html += f'''
                    <div class="angle-item">
                        <strong>{angle['type']}</strong> - {angle['suggested_title']}
                        <div style="margin-top: 8px; font-size: 0.9em; color: #666;">
                            💡 {angle['hook'][:50]}... | 目标情绪: {angle['target_emotion']}
                        </div>
                    </div>
                    '''
                html += '</div>'
            
            # 差异化建议
            if analysis.differentiation:
                diff = analysis.differentiation
                html += '<div style="margin-top: 15px; padding: 15px; background: #fffaf0; border-radius: 10px;">'
                html += '<div style="font-weight: bold; color: #c05621; margin-bottom: 10px;">💡 差异化建议</div>'
                for rec in diff.get('recommendations', [])[:2]:
                    html += f'<div style="margin: 5px 0; font-size: 0.9em;">• <strong>{rec["type"]}</strong>: {rec["suggestion"]}</div>'
                html += '</div>'
            
            html += '</div>'
        
        return html
    
    def export_json(self, scores: List[HeatScore], 
                   analyses: List[TopicAnalysis],
                   filepath: str = None) -> str:
        """导出JSON数据"""
        if filepath is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(self.output_dir, f"topic_data_{timestamp}.json")
        
        data = {
            'generated_at': datetime.now().isoformat(),
            'topics_count': len(scores),
            'scores': [
                {
                    'title': s.topic.title,
                    'platform': s.topic.platform,
                    'total_score': s.total_score,
                    'platform_score': s.platform_score,
                    'interaction_score': s.interaction_score,
                    'trend_score': s.trend_score,
                    'quality_score': s.quality_score,
                    'potential_score': s.potential_score,
                }
                for s in scores
            ],
            'analyses': [
                {
                    'title': a.original_topic.title,
                    'angles': a.angles,
                    'differentiation': a.differentiation,
                }
                for a in analyses
            ]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return filepath


if __name__ == "__main__":
    # 测试
    from data_collector import collect_hot_topics
    from heat_algorithm import HeatAlgorithm, analyze_topics
    from topic_analyzer import TopicAnalyzer
    
    print("正在生成测试报告...")
    
    # 采集数据
    topics = collect_hot_topics(limit=20)
    
    # 分析热度
    result = analyze_topics(topics)
    scores = result['scores']
    
    # 详细分析
    analyzer = TopicAnalyzer()
    analyses = [analyzer.analyze(s.topic, s, topics) for s in scores[:10]]
    
    # 生成报告
    generator = ReportGenerator()
    report_file = generator.generate_full_report(
        scores, analyses, result['trends'], 
        result['keywords'], result['recommendations']
    )
    
    print(f"\n✅ 报告已生成: {report_file}")
