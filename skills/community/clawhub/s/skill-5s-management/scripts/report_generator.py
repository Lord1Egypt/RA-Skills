#!/usr/bin/env python3
"""
5S管理可视化报告生成器
功能：根据检查数据生成HTML格式的5S管理报告
输入：JSON格式的检查数据
输出：HTML可视化报告
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm
    import numpy as np
except ImportError:
    print(json.dumps({
        "status": "error",
        "message": "缺少依赖库，请运行: pip install matplotlib numpy"
    }))
    sys.exit(1)


def load_data(input_path):
    """加载JSON格式的检查数据"""
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(json.dumps({
            "status": "error",
            "message": f"文件不存在: {input_path}"
        }))
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(json.dumps({
            "status": "error",
            "message": f"JSON格式错误: {str(e)}"
        }))
        sys.exit(1)


def create_radar_chart(scores):
    """生成5S得分雷达图"""
    categories = ['整理\n(Seiri)', '整顿\n(Seiton)', '清扫\n(Seiso)', 
                  '清洁\n(Seiketsu)', '素养\n(Shitsuke)']
    
    # 数据映射
    score_values = [
        scores.get('sorting', 0),
        scores.get('set_in_order', 0),
        scores.get('shining', 0),
        scores.get('standardizing', 0),
        scores.get('sustaining', 0)
    ]
    
    # 确保5分制
    score_values = [min(v, 5) for v in score_values]
    
    # 计算角度
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    score_values_plot = score_values + [score_values[0]]
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    
    # 绘制雷达图
    ax.fill(angles, score_values_plot, color='#3498db', alpha=0.25)
    ax.plot(angles, score_values_plot, color='#3498db', linewidth=2, marker='o')
    
    # 设置标签
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10)
    ax.set_ylim(0, 5)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(['1', '2', '3', '4', '5'], fontsize=8)
    
    # 添加分数标注
    for i, (angle, val) in enumerate(zip(angles[:-1], score_values)):
        ax.annotate(f'{val:.1f}', xy=(angle, val), xytext=(angle, val + 0.3),
                   fontsize=10, ha='center', fontweight='bold')
    
    plt.title('5S得分雷达图', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    
    # 保存为base64
    import base64
    from io import BytesIO
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    img_data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return img_data


def create_trend_chart(trend_data):
    """生成分数趋势图"""
    if not trend_data or len(trend_data) < 2:
        return None
    
    periods = [d['period'] for d in trend_data]
    scores = [d['total_score'] / 25 * 100 for d in trend_data]  # 转换为百分制
    
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(periods, scores, marker='o', linewidth=2, color='#3498db', markersize=8)
    ax.fill_between(periods, scores, alpha=0.3, color='#3498db')
    
    ax.set_xlabel('周期', fontsize=11)
    ax.set_ylabel('得分率 (%)', fontsize=11)
    ax.set_ylim(0, 100)
    ax.grid(True, alpha=0.3)
    
    # 添加数据标签
    for x, y in zip(periods, scores):
        ax.annotate(f'{y:.1f}%', (x, y), textcoords="offset points", 
                   xytext=(0, 10), ha='center', fontsize=9)
    
    plt.title('5S得分趋势', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    import base64
    from io import BytesIO
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    img_data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return img_data


def create_issue_pie(issues):
    """生成问题类型分布饼图"""
    if not issues:
        return None
    
    # 统计各类型问题数量
    type_count = {}
    for issue in issues:
        issue_type = issue.get('type', '其他')
        type_count[issue_type] = type_count.get(issue_type, 0) + 1
    
    labels = list(type_count.keys())
    sizes = list(type_count.values())
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6']
    
    fig, ax = plt.subplots(figsize=(5, 5))
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.0f%%',
                                       colors=colors[:len(labels)], startangle=90)
    
    for autotext in autotexts:
        autotext.set_fontsize(9)
        autotext.set_fontweight('bold')
    
    plt.title('问题类型分布', fontsize=12, fontweight='bold')
    plt.tight_layout()
    
    import base64
    from io import BytesIO
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    img_data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return img_data


def get_score_level(score):
    """根据分数返回评价等级"""
    if score >= 4.5:
        return ('优秀', '#27ae60')
    elif score >= 4.0:
        return ('良好', '#3498db')
    elif score >= 3.0:
        return ('合格', '#f39c12')
    else:
        return ('不合格', '#e74c3c')


def generate_html_report(data, radar_chart, trend_chart=None, issue_pie=None):
    """生成HTML报告"""
    
    scores = data.get('scores', {})
    avg_score = sum(scores.values()) / len(scores) if scores else 0
    level, level_color = get_score_level(avg_score)
    
    # 问题状态统计
    issues = data.get('issues', [])
    resolved = sum(1 for i in issues if i.get('status') == 'resolved')
    pending = len(issues) - resolved
    
    # 改进效果统计
    improvements = data.get('improvements', [])
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>5S管理报告 - {data.get('period', 'N/A')}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: "Microsoft YaHei", "PingFang SC", sans-serif; 
               background: #f5f7fa; color: #333; line-height: 1.6; }}
        .container {{ max-width: 1000px; margin: 0 auto; padding: 20px; }}
        
        /* 头部 */
        .header {{ background: linear-gradient(135deg, #2c3e50, #3498db); 
                   color: white; padding: 30px; border-radius: 10px;
                   margin-bottom: 20px; text-align: center; }}
        .header h1 {{ font-size: 28px; margin-bottom: 10px; }}
        .header .meta {{ opacity: 0.9; font-size: 14px; }}
        
        /* 统计卡片 */
        .stats-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); 
                       gap: 15px; margin-bottom: 20px; }}
        .stat-card {{ background: white; padding: 20px; border-radius: 8px;
                      box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }}
        .stat-card .value {{ font-size: 32px; font-weight: bold; 
                             color: #2c3e50; }}
        .stat-card .label {{ color: #7f8c8d; font-size: 14px; margin-top: 5px; }}
        
        /* 等级标签 */
        .level-badge {{ display: inline-block; padding: 5px 20px; 
                       border-radius: 20px; color: white; font-weight: bold; }}
        
        /* 内容区块 */
        .section {{ background: white; border-radius: 10px; padding: 25px; 
                    margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .section h2 {{ color: #2c3e50; border-bottom: 2px solid #3498db; 
                       padding-bottom: 10px; margin-bottom: 20px; font-size: 18px; }}
        
        /* 图表区域 */
        .chart-row {{ display: flex; gap: 20px; flex-wrap: wrap; }}
        .chart-item {{ flex: 1; min-width: 300px; text-align: center; }}
        .chart-item img {{ max-width: 100%; border-radius: 8px; }}
        .chart-title {{ font-weight: bold; color: #555; margin: 10px 0; }}
        
        /* 得分表格 */
        .score-table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
        .score-table th, .score-table td {{ padding: 12px; text-align: center; 
                                            border-bottom: 1px solid #eee; }}
        .score-table th {{ background: #f8f9fa; color: #2c3e50; font-weight: 600; }}
        .score-table tr:hover {{ background: #f8f9fa; }}
        .score-high {{ color: #27ae60; font-weight: bold; }}
        .score-low {{ color: #e74c3c; font-weight: bold; }}
        
        /* 问题列表 */
        .issue-list {{ list-style: none; }}
        .issue-item {{ padding: 15px; border-left: 4px solid; margin-bottom: 10px;
                       background: #f8f9fa; border-radius: 0 5px 5px 0; }}
        .issue-item.resolved {{ border-color: #27ae60; }}
        .issue-item.pending {{ border-color: #f39c12; }}
        .issue-item .issue-header {{ display: flex; justify-content: space-between;
                                      margin-bottom: 5px; }}
        .issue-item .issue-type {{ font-weight: bold; color: #2c3e50; }}
        .issue-item .issue-status {{ font-size: 12px; padding: 2px 8px; 
                                     border-radius: 3px; color: white; }}
        .issue-status.resolved {{ background: #27ae60; }}
        .issue-status.pending {{ background: #f39c12; }}
        .issue-item .issue-desc {{ color: #555; font-size: 14px; }}
        
        /* 改进列表 */
        .improvement-item {{ display: flex; align-items: center; gap: 15px;
                            padding: 15px; background: #f8f9fa; border-radius: 8px;
                            margin-bottom: 10px; }}
        .improvement-arrow {{ color: #27ae60; font-weight: bold; font-size: 18px; }}
        .improvement-scores {{ display: flex; align-items: center; gap: 10px; }}
        .score-before {{ color: #e74c3c; }}
        .score-after {{ color: #27ae60; }}
        .improvement-change {{ background: #27ae60; color: white; 
                               padding: 2px 8px; border-radius: 3px; font-size: 12px; }}
        
        /* 改进建议 */
        .suggestion-box {{ background: #e8f6f3; border-left: 4px solid #1abc9c; 
                          padding: 15px; border-radius: 0 5px 5px 0; }}
        .suggestion-box h4 {{ color: #16a085; margin-bottom: 10px; }}
        .suggestion-box ul {{ margin-left: 20px; color: #2c3e50; }}
        .suggestion-box li {{ margin-bottom: 5px; }}
        
        /* 页脚 */
        .footer {{ text-align: center; color: #7f8c8d; font-size: 12px; 
                   padding: 20px; }}
        
        @media print {{ 
            .section {{ break-inside: avoid; }} 
            body {{ background: white; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 头部 -->
        <div class="header">
            <h1>5S管理执行报告</h1>
            <div class="meta">
                <span>报告周期：{data.get('period', 'N/A')}</span> | 
                <span>区域：{data.get('region', 'N/A')}</span> | 
                <span>生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}</span>
            </div>
        </div>
        
        <!-- 统计卡片 -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="value">{avg_score:.1f}</div>
                <div class="label">综合得分 <span class="level-badge" style="background:{level_color}">{level}</span></div>
            </div>
            <div class="stat-card">
                <div class="value">{len(issues)}</div>
                <div class="label">发现问题数</div>
            </div>
            <div class="stat-card">
                <div class="value" style="color:#27ae60">{resolved}</div>
                <div class="label">已整改</div>
            </div>
            <div class="stat-card">
                <div class="value" style="color:#f39c12">{pending}</div>
                <div class="label">待整改</div>
            </div>
        </div>
        
        <!-- 得分分析 -->
        <div class="section">
            <h2>5S各维度得分分析</h2>
            <div class="chart-row">
                <div class="chart-item">
                    <div class="chart-title">雷达图</div>
                    <img src="data:image/png;base64,{radar_chart}" alt="雷达图">
                </div>
                {f'''
                <div class="chart-item">
                    <div class="chart-title">趋势图</div>
                    <img src="data:image/png;base64,{trend_chart}" alt="趋势图">
                </div>
                ''' if trend_chart else ''}
            </div>
            
            <table class="score-table">
                <thead>
                    <tr>
                        <th>维度</th>
                        <th>得分</th>
                        <th>评价</th>
                        <th>建议</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>整理 (Seiri)</td>
                        <td class="{'score-high' if scores.get('sorting',0)>=4 else 'score-low'}">{scores.get('sorting', 0):.1f}</td>
                        <td>{get_score_level(scores.get('sorting',0))[0]}</td>
                        <td>{'保持良好' if scores.get('sorting',0)>=4 else '需加强非必需品清理'}</td>
                    </tr>
                    <tr>
                        <td>整顿 (Seiton)</td>
                        <td class="{'score-high' if scores.get('set_in_order',0)>=4 else 'score-low'}">{scores.get('set_in_order', 0):.1f}</td>
                        <td>{get_score_level(scores.get('set_in_order',0))[0]}</td>
                        <td>{'保持良好' if scores.get('set_in_order',0)>=4 else '完善定置管理与标识'}</td>
                    </tr>
                    <tr>
                        <td>清扫 (Seiso)</td>
                        <td class="{'score-high' if scores.get('shining',0)>=4 else 'score-low'}">{scores.get('shining', 0):.1f}</td>
                        <td>{get_score_level(scores.get('shining',0))[0]}</td>
                        <td>{'保持良好' if scores.get('shining',0)>=4 else '加强日常清扫频次'}</td>
                    </tr>
                    <tr>
                        <td>清洁 (Seiketsu)</td>
                        <td class="{'score-high' if scores.get('standardizing',0)>=4 else 'score-low'}">{scores.get('standardizing', 0):.1f}</td>
                        <td>{get_score_level(scores.get('standardizing',0))[0]}</td>
                        <td>{'保持良好' if scores.get('standardizing',0)>=4 else '完善检查标准与制度'}</td>
                    </tr>
                    <tr>
                        <td>素养 (Shitsuke)</td>
                        <td class="{'score-high' if scores.get('sustaining',0)>=4 else 'score-low'}">{scores.get('sustaining', 0):.1f}</td>
                        <td>{get_score_level(scores.get('sustaining',0))[0]}</td>
                        <td>{'保持良好' if scores.get('sustaining',0)>=4 else '加强培训与习惯养成'}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <!-- 问题分布 -->
        {f'''
        <div class="section">
            <h2>问题分布分析</h2>
            <div class="chart-row">
                <div class="chart-item">
                    <img src="data:image/png;base64,{issue_pie}" alt="问题分布">
                </div>
            </div>
        </div>
        ''' if issue_pie else ''}
        
        <!-- 问题详情 -->
        {f'''
        <div class="section">
            <h2>问题详情记录</h2>
            <ul class="issue-list">
                {''.join([f'''
                <li class="issue-item {'resolved' if i.get('status')=='resolved' else 'pending'}">
                    <div class="issue-header">
                        <span class="issue-type">{i.get('type', '未知类型')}</span>
                        <span class="issue-status {'resolved' if i.get('status')=='resolved' else 'pending'}">
                            {'已整改' if i.get('status')=='resolved' else '待整改'}
                        </span>
                    </div>
                    <div class="issue-desc">{i.get('description', '')}</div>
                    {'''<div style="color:#7f8c8d;font-size:12px;margin-top:5px;">整改期限：{deadline}</div>'''.format(deadline=i.get("deadline", "未设置")) if i.get('status')!='resolved' else ''}
                </li>
                ''' for i in issues])}
            </ul>
        </div>
        ''' if issues else ''}
        
        <!-- 改进效果 -->
        {f'''
        <div class="section">
            <h2>改进效果展示</h2>
            {''.join([f'''
            <div class="improvement-item">
                <div style="flex:1;font-weight:bold;">{imp.get('item', '')}</div>
                <div class="improvement-scores">
                    <span class="score-before">{imp.get('before', 0):.1f}</span>
                    <span class="improvement-arrow">→</span>
                    <span class="score-after">{imp.get('after', 0):.1f}</span>
                    <span class="improvement-change">+{imp.get('after', 0) - imp.get('before', 0):.1f}</span>
                </div>
                <div style="color:#7f8c8d;font-size:12px;">{imp.get('date', '')}</div>
            </div>
            ''' for imp in improvements])}
        </div>
        ''' if improvements else ''}
        
        <!-- 改进建议 -->
        <div class="section">
            <h2>持续改进建议</h2>
            <div class="suggestion-box">
                <h4>基于本次检查结果的改进建议：</h4>
                <ul>
                    {f'<li>针对得分较低的"{min(scores, key=scores.get)}"维度，需制定专项改进计划</li>' if avg_score < 4 else ''}
                    {f'<li>当前有{pending}项问题待整改，请督促责任人在期限内完成</li>' if pending > 0 else '<li>继续保持当前良好态势，向优秀等级迈进</li>'}
                    <li>建议每周开展1次5S自查，形成问题台账并跟踪整改</li>
                    <li>加强员工5S培训，提高全员意识与参与度</li>
                    <li>建立目视化管理标准，提升现场管理水平</li>
                </ul>
            </div>
        </div>
        
        <!-- 页脚 -->
        <div class="footer">
            本报告由5S目视化管理辅助工具自动生成 | 数据仅供参考，请以实际检查为准
        </div>
    </div>
</body>
</html>'''
    
    return html


def main():
    parser = argparse.ArgumentParser(description='5S管理可视化报告生成器')
    parser.add_argument('--input', '-i', required=True, help='输入JSON数据文件路径')
    parser.add_argument('--output', '-o', required=True, help='输出HTML报告路径')
    parser.add_argument('--period', '-p', default='monthly', help='报告周期类型')
    parser.add_argument('--trend-data', '-t', help='趋势数据JSON文件路径(可选)')
    
    args = parser.parse_args()
    
    # 加载数据
    data = load_data(args.input)
    
    # 加载趋势数据(如果有)
    trend_data = None
    if args.trend_data:
        try:
            with open(args.trend_data, 'r', encoding='utf-8') as f:
                trend_data = json.load(f)
        except Exception:
            pass
    
    # 生成图表
    radar_chart = create_radar_chart(data.get('scores', {}))
    trend_chart = create_trend_chart(trend_data) if trend_data else None
    issue_pie = create_issue_pie(data.get('issues', []))
    
    # 生成HTML报告
    html_report = generate_html_report(data, radar_chart, trend_chart, issue_pie)
    
    # 写入文件
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_report)
    
    # 输出结果JSON
    result = {
        "status": "success",
        "report_path": str(output_path.absolute()),
        "report_size": output_path.stat().st_size,
        "summary": {
            "period": data.get('period', 'N/A'),
            "region": data.get('region', 'N/A'),
            "total_score": sum(data.get('scores', {}).values()) / 5 if data.get('scores') else 0,
            "issues_count": len(data.get('issues', [])),
            "resolved_count": sum(1 for i in data.get('issues', []) if i.get('status') == 'resolved')
        }
    }
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
