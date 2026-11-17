#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
制造业质量现场数据分析 - HTML 图表生成脚本
生成可视化图表，输出 HTML 文件
"""

import argparse
import json
import sys
import os
from typing import Dict, List, Any
from datetime import datetime

try:
    import pandas as pd
except ImportError as e:
    print(json.dumps({"status": "error", "message": f"缺少必要依赖库: {e}"}))
    sys.exit(1)


# HTML 模板
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>质量现场数据分析报告 - {{report_time}}</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: "Noto Sans SC", "PingFang SC", "Microsoft YaHei", "微软雅黑", "Hiragino Sans GB", Arial, sans-serif;
            background-color: #f5f7fa;
            padding: 20px;
            color: #333;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
        }}

        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #409EFF;
        }}

        .header h1 {{
            font-size: 28px;
            color: #303133;
            margin-bottom: 10px;
        }}

        .header .time {{
            font-size: 14px;
            color: #909399;
        }}

        .section {{
            margin-bottom: 30px;
        }}

        .section-title {{
            font-size: 20px;
            color: #409EFF;
            margin-bottom: 15px;
            padding-left: 10px;
            border-left: 4px solid #409EFF;
        }}

        .overview-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-bottom: 20px;
        }}

        .overview-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}

        .overview-card.warning {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }}

        .overview-card.success {{
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        }}

        .overview-card .label {{
            font-size: 14px;
            opacity: 0.9;
            margin-bottom: 10px;
        }}

        .overview-card .value {{
            font-size: 32px;
            font-weight: bold;
        }}

        .table-container {{
            overflow-x: auto;
            margin-bottom: 20px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            background-color: white;
        }}

        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #EBEEF5;
        }}

        th {{
            background-color: #F5F7FA;
            font-weight: 600;
            color: #606266;
        }}

        tr:hover {{
            background-color: #F5F7FA;
        }}

        .top-rank {{
            color: #F56C6C;
            font-weight: bold;
        }}

        .chart-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}

        .chart-card {{
            background-color: #FAFAFA;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #EBEEF5;
        }}

        .chart-card h3 {{
            font-size: 16px;
            color: #606266;
            margin-bottom: 15px;
            text-align: center;
        }}

        .bar-chart {{
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}

        .bar-item {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .bar-label {{
            width: 150px;
            font-size: 13px;
            text-align: right;
            color: #606266;
        }}

        .bar-track {{
            flex: 1;
            height: 30px;
            background-color: #E4E7ED;
            border-radius: 4px;
            overflow: hidden;
            position: relative;
        }}

        .bar-fill {{
            height: 100%;
            background: linear-gradient(90deg, #409EFF 0%, #66B1FF 100%);
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 10px;
            color: white;
            font-size: 12px;
            transition: width 0.3s ease;
        }}

        .bar-fill.warning {{
            background: linear-gradient(90deg, #E6A23C 0%, #EEBE77 100%);
        }}

        .bar-fill.danger {{
            background: linear-gradient(90deg, #F56C6C 0%, #F89898 100%);
        }}

        .bar-value {{
            font-weight: bold;
        }}

        .recommendation-list {{
            list-style: none;
        }}

        .recommendation-item {{
            background-color: #F0F9FF;
            border-left: 4px solid #409EFF;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 4px;
        }}

        .recommendation-item.priority-high {{
            background-color: #FEF0F0;
            border-left-color: #F56C6C;
        }}

        .recommendation-item.priority-medium {{
            background-color: #FDF6EC;
            border-left-color: #E6A23C;
        }}

        .recommendation-item.priority-low {{
            background-color: #F0F9FF;
            border-left-color: #409EFF;
        }}

        .recommendation-item .rank {{
            display: inline-block;
            width: 24px;
            height: 24px;
            background-color: #409EFF;
            color: white;
            text-align: center;
            line-height: 24px;
            border-radius: 50%;
            font-size: 12px;
            margin-right: 10px;
        }}

        .recommendation-item.priority-high .rank {{
            background-color: #F56C6C;
        }}

        .recommendation-item.priority-medium .rank {{
            background-color: #E6A23C;
        }}

        .recommendation-item .content {{
            display: inline-block;
            vertical-align: middle;
        }}

        .recommendation-item .defect-name {{
            font-weight: bold;
            color: #303133;
        }}

        .recommendation-item .defect-info {{
            font-size: 13px;
            color: #909399;
            margin-top: 5px;
        }}

        @media (max-width: 768px) {{
            .overview-grid {{
                grid-template-columns: 1fr;
            }}

            .chart-container {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>质量现场数据分析报告</h1>
            <div class="time">报告时间: {{report_time}}</div>
        </div>

        {{content}}
    </div>
</body>
</html>
"""


def generate_overview_section(overview: Dict[str, Any]) -> str:
    """
    生成数据概览 HTML
    """
    defect_rate_class = 'success' if overview['overall_defect_rate'] < 5 else ('warning' if overview['overall_defect_rate'] < 10 else 'warning')

    html = f"""
        <div class="section">
            <div class="section-title">数据概览</div>
            <div class="overview-grid">
                <div class="overview-card">
                    <div class="label">总检验量</div>
                    <div class="value">{overview['total_inspection_count']}</div>
                </div>
                <div class="overview-card {defect_rate_class}">
                    <div class="label">整体不良率</div>
                    <div class="value">{overview['overall_defect_rate']}%</div>
                </div>
                <div class="overview-card">
                    <div class="label">不良总数</div>
                    <div class="value">{overview['total_defect_count']}</div>
                </div>
            </div>
        </div>
    """
    return html


def generate_defect_table(defect_type_stats: List[Dict[str, Any]]) -> str:
    """
    生成不良类型统计表格 HTML
    """
    html = """
        <div class="section">
            <div class="section-title">不良类型分类统计</div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>排名</th>
                            <th>不良类型</th>
                            <th>不良数量</th>
                            <th>占比</th>
                        </tr>
                    </thead>
                    <tbody>
    """

    for idx, item in enumerate(defect_type_stats):
        rank_class = 'top-rank' if idx < 3 else ''
        html += f"""
                        <tr>
                            <td class="{rank_class}">{idx + 1}</td>
                            <td>{item['defect_type']}</td>
                            <td>{item['total_count']}</td>
                            <td>{item['percentage']}%</td>
                        </tr>
        """

    html += """
                    </tbody>
                </table>
            </div>
        </div>
    """
    return html


def generate_bar_chart(data: List[Dict[str, Any]], title: str, label_key: str, value_key: str) -> str:
    """
    生成条形图 HTML
    """
    if not data:
        return ''

    max_value = max(item[value_key] for item in data)

    html = f"""
        <div class="chart-card">
            <h3>{title}</h3>
            <div class="bar-chart">
    """

    for idx, item in enumerate(data):
        percentage = item[value_key] / max_value * 100 if max_value > 0 else 0
        bar_class = 'danger' if idx == 0 else ('warning' if idx == 1 else '')

        html += f"""
                <div class="bar-item">
                    <div class="bar-label">{item[label_key]}</div>
                    <div class="bar-track">
                        <div class="bar-fill {bar_class}" style="width: {percentage}%;">
                            {item[value_key]}
                        </div>
                    </div>
                </div>
        """

    html += """
            </div>
        </div>
    """
    return html


def generate_recommendations(recommendations: List[Dict[str, Any]]) -> str:
    """
    生成整改优先级建议 HTML
    """
    if not recommendations:
        return ''

    html = """
        <div class="section">
            <div class="section-title">整改优先级建议</div>
            <ul class="recommendation-list">
    """

    for item in recommendations:
        priority_class = f"priority-{item['priority'].lower()}"

        html += f"""
                <li class="recommendation-item {priority_class}">
                    <span class="rank">{item['rank']}</span>
                    <span class="content">
                        <span class="defect-name">{item['defect_type']}</span>
                        <div class="defect-info">
                            不良数: {item['defect_count']} | 占比: {item['percentage']}% | 优先级: {item['priority']}
                        </div>
                    </span>
                </li>
        """

    html += """
            </ul>
        </div>
    """
    return html


def generate_analysis_conclusion(analysis_result: Dict[str, Any]) -> str:
    """
    生成质量分析结论 HTML
    """
    overview = analysis_result.get('summary', {}).get('overview', {})
    top3 = analysis_result.get('summary', {}).get('top3_defects', {})
    defect_analysis = analysis_result.get('analysis_result', {}).get('defect_type_analysis', {})
    process_analysis = analysis_result.get('analysis_result', {}).get('process_analysis', [])

    # 提取关键数据
    total_inspection = overview.get('total_inspection_count', 0)
    total_defect = overview.get('total_defect_count', 0)
    defect_rate = overview.get('overall_defect_rate', 0)
    top3_items = top3.get('top3', [])
    accumulated_pct = top3.get('accumulated_percentage', 0)
    unique_defect_types = defect_analysis.get('unique_defect_types', 0)

    # 生成整体质量状况评估
    if defect_rate < 2:
        quality_status = "整体质量状况良好，不良率处于较低水平"
    elif defect_rate < 5:
        quality_status = "整体质量状况基本可控，需持续关注重点问题"
    elif defect_rate < 10:
        quality_status = "整体质量状况需要改进，存在较多不良问题"
    else:
        quality_status = "整体质量状况较差，不良率偏高，需要立即采取整改措施"

    # 生成主要问题点总结
    problem_summary = []
    if top3_items:
        top1 = top3_items[0]
        problem_summary.append(f"主要不良问题为「{top1['defect_type']}」，不良数{top1['total_count']}，占比{top1['percentage']}%")

    if accumulated_pct >= 80:
        problem_summary.append(f"TOP3不良累计占比达{accumulated_pct}%，符合二八原则，优先解决这3类问题可大幅降低不良率")
    elif accumulated_pct >= 60:
        problem_summary.append(f"TOP3不良累计占比{accumulated_pct}%，问题较为集中，需重点关注")
    else:
        problem_summary.append(f"不良问题较为分散（TOP3累计占比仅{accumulated_pct}%），需要系统性排查")

    # 生成工序分析结论
    process_conclusion = ""
    if process_analysis:
        top_process = process_analysis[0]
        process_conclusion = f"工序层面，「{top_process['process']}」不良数最多（{top_process['total_defect_count']}），需重点管控"

    # 组合结论内容
    conclusion_lines = [
        f"本次分析共检验{total_inspection}件，发现不良{total_defect}件，整体不良率{defect_rate}%。",
        quality_status + "。",
    ]
    conclusion_lines.extend(problem_summary)
    if process_conclusion:
        conclusion_lines.append(process_conclusion + "。")

    # 生成最终结论
    html = """
        <div class="section">
            <div class="section-title">质量分析结论</div>
            <div style="background-color: #F0F9FF; padding: 20px; border-radius: 8px; border-left: 4px solid #409EFF; line-height: 2;">
    """

    for line in conclusion_lines:
        html += f'                <p style="margin: 0; padding: 5px 0;">{line}</p>\n'

    html += """
            </div>
        </div>
    """
    return html


def generate_html_report(analysis_result: Dict[str, Any], output_file: str) -> None:
    """
    生成完整的 HTML 报告（包含数据概览、统计表格、图表、分析结论、整改建议）
    """
    content_parts = []

    # 1. 数据概览
    overview = analysis_result.get('summary', {}).get('overview', {})
    if overview:
        content_parts.append(generate_overview_section(overview))

    # 2. 不良类型统计表格
    defect_stats = analysis_result.get('analysis_result', {}).get('defect_type_analysis', {}).get('defect_type_stats', [])
    if defect_stats:
        content_parts.append(generate_defect_table(defect_stats))

    # 3. 图表部分
    chart_content_parts = []

    # TOP3 不良类型图表
    if defect_stats:
        top3 = defect_stats[:3]
        chart_content_parts.append(generate_bar_chart(top3, 'TOP3 不良类型分布', 'defect_type', 'total_count'))

    # 按工序分布图表
    process_analysis = analysis_result.get('analysis_result', {}).get('process_analysis', [])
    if process_analysis:
        chart_content_parts.append(generate_bar_chart(process_analysis[:5], '按工序不良分布（Top5）', 'process', 'total_defect_count'))

    # 按班次分布图表
    shift_analysis = analysis_result.get('analysis_result', {}).get('shift_analysis', [])
    if shift_analysis:
        chart_content_parts.append(generate_bar_chart(shift_analysis, '按班次不良分布', 'shift', 'total_defect_count'))

    if chart_content_parts:
        html = """
            <div class="section">
                <div class="section-title">可视化图表</div>
                <div class="chart-container">
        """
        html += '\n'.join(chart_content_parts)
        html += """
                </div>
            </div>
        """
        content_parts.append(html)

    # 4. 质量分析结论
    content_parts.append(generate_analysis_conclusion(analysis_result))

    # 5. 整改建议
    recommendations = analysis_result.get('summary', {}).get('recommendation_priority', [])
    if recommendations:
        content_parts.append(generate_recommendations(recommendations))

    # 组合完整内容
    full_content = '\n'.join(content_parts)

    # 填充模板
    report_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    html = HTML_TEMPLATE.replace('{{report_time}}', report_time).replace('{{content}}', full_content)

    # 写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)


def main():
    parser = argparse.ArgumentParser(description='制造业质量现场数据分析 - 生成完整 HTML 报告')
    parser.add_argument('--input_file', required=True, help='分析后的 JSON 数据文件路径')
    parser.add_argument('--output_file', required=True, help='输出的 HTML 文件路径')
    args = parser.parse_args()

    # 读取输入文件
    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            analysis_result = json.load(f)
    except Exception as e:
        print(json.dumps({
            "status": "error",
            "message": f"读取输入文件失败: {str(e)}"
        }, ensure_ascii=False))
        sys.exit(1)

    if analysis_result.get('status') != 'success':
        print(json.dumps({
            "status": "error",
            "message": f"输入数据状态异常: {analysis_result.get('message', '未知错误')}"
        }, ensure_ascii=False))
        sys.exit(1)

    # 生成 HTML 报告
    try:
        generate_html_report(analysis_result, args.output_file)

        print(json.dumps({
            "status": "success",
            "message": "HTML 报告生成成功",
            "output_file": args.output_file
        }, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({
            "status": "error",
            "message": f"生成 HTML 报告失败: {str(e)}"
        }, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
