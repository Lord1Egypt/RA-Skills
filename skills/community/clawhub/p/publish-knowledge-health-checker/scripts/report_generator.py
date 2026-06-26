#!/usr/bin/env python3
"""
知识库健康报告生成器
生成可视化HTML报告卡片
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict
import html  # 用于HTML转义


def escape_html(text: str) -> str:
    """HTML转义，防止XSS"""
    return html.escape(str(text))


def generate_report(results: Dict, output_path: str = None) -> str:
    """生成HTML健康报告"""

    if output_path is None:
        timestamp = datetime.now().strftime('%Y%m%d-%H%M')
        output_path = f'health-report-{timestamp}.html'

    scores = results['scores']
    stats = results['graph_stats']

    # 生成HTML报告
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>知识库健康报告</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }}

        .card {{
            background: white;
            border-radius: 24px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            max-width: 960px;
            width: 100%;
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 28px;
            margin-bottom: 8px;
        }}

        .header .path {{
            opacity: 0.8;
            font-size: 14px;
        }}

        .score-section {{
            display: flex;
            justify-content: space-around;
            padding: 40px 20px;
            background: #f8fafc;
        }}

        .main-score {{
            text-align: center;
        }}

        .main-score .score {{
            font-size: 72px;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            line-height: 1;
        }}

        .main-score .label {{
            color: #64748b;
            font-size: 16px;
            margin-top: 8px;
        }}

        .sub-scores {{
            display: flex;
            gap: 20px;
        }}

        .sub-score {{
            text-align: center;
            padding: 20px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            min-width: 100px;
        }}

        .sub-score .value {{
            font-size: 28px;
            font-weight: 600;
            color: #334155;
        }}

        .sub-score .label {{
            font-size: 12px;
            color: #94a3b8;
            margin-top: 4px;
        }}

        .metrics {{
            padding: 30px 40px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }}

        .metric {{
            padding: 20px;
            background: #f8fafc;
            border-radius: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .metric .name {{
            color: #64748b;
            font-size: 14px;
        }}

        .metric .value {{
            font-size: 24px;
            font-weight: 600;
            color: #334155;
        }}

        .metric .trend {{
            font-size: 12px;
            padding: 4px 8px;
            border-radius: 4px;
            margin-left: 8px;
        }}

        .trend.good {{
            background: #dcfce7;
            color: #16a34a;
        }}

        .trend.bad {{
            background: #fee2e2;
            color: #dc2626;
        }}

        .issues {{
            padding: 30px 40px;
            border-top: 1px solid #e2e8f0;
        }}

        .issues h2 {{
            font-size: 20px;
            color: #334155;
            margin-bottom: 20px;
        }}

        .issue-list {{
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}

        .issue-item {{
            display: flex;
            align-items: center;
            padding: 16px;
            background: #fef2f2;
            border-radius: 8px;
            border-left: 4px solid #dc2626;
        }}

        .issue-item.warning {{
            background: #fffbeb;
            border-left-color: #f59e0b;
        }}

        .issue-icon {{
            font-size: 24px;
            margin-right: 12px;
        }}

        .issue-content {{
            flex: 1;
        }}

        .issue-title {{
            font-weight: 500;
            color: #334155;
            margin-bottom: 4px;
        }}

        .issue-desc {{
            font-size: 14px;
            color: #64748b;
        }}

        .footer {{
            padding: 30px 40px;
            background: #f8fafc;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .timestamp {{
            color: #94a3b8;
            font-size: 14px;
        }}

        .actions {{
            display: flex;
            gap: 12px;
        }}

        .btn {{
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            border: none;
            transition: all 0.2s;
        }}

        .btn-primary {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}

        .btn-primary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 20px -10px rgba(102, 126, 234, 0.5);
        }}

        .btn-secondary {{
            background: white;
            color: #334155;
            border: 1px solid #e2e8f0;
        }}

        .btn-secondary:hover {{
            background: #f8fafc;
        }}

        @media (max-width: 640px) {{
            .score-section {{
                flex-direction: column;
                gap: 30px;
            }}

            .sub-scores {{
                justify-content: center;
            }}

            .metrics {{
                grid-template-columns: 1fr;
            }}

            .footer {{
                flex-direction: column;
                gap: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="card">
        <div class="header">
            <h1>知识库健康报告</h1>
            <div class="path">{results['scan_path']}</div>
        </div>

        <div class="score-section">
            <div class="main-score">
                <div class="score">{scores['total_score']}</div>
                <div class="label">健康分</div>
            </div>

            <div class="sub-scores">
                <div class="sub-score">
                    <div class="value">{scores['empty_score']}</div>
                    <div class="label">空壳检测</div>
                </div>
                <div class="sub-score">
                    <div class="value">{scores['broken_score']}</div>
                    <div class="label">断链检测</div>
                </div>
                <div class="sub-score">
                    <div class="value">{scores['density_score']}</div>
                    <div class="label">内容密度</div>
                </div>
                <div class="sub-score">
                    <div class="value">{scores['network_score']}</div>
                    <div class="label">网络完整</div>
                </div>
            </div>
        </div>

        <div class="metrics">
            <div class="metric">
                <span class="name">总文件数</span>
                <span class="value">{results['total_files']}</span>
            </div>
            <div class="metric">
                <span class="name">空壳文件</span>
                <span class="value">{len(results['empty_files'])}
                    <span class="trend {'good' if len(results['empty_files']) == 0 else 'bad'}">
                        {'✓' if len(results['empty_files']) == 0 else '需处理'}
                    </span>
                </span>
            </div>
            <div class="metric">
                <span class="name">断链数量</span>
                <span class="value">{len(results['broken_links'])}
                    <span class="trend {'good' if len(results['broken_links']) == 0 else 'bad'}">
                        {'✓' if len(results['broken_links']) == 0 else '需处理'}
                    </span>
                </span>
            </div>
            <div class="metric">
                <span class="name">孤立节点</span>
                <span class="value">{len(results['isolated_nodes'])}
                    <span class="trend {'good' if len(results['isolated_nodes']) < 5 else 'bad'}">
                        {'✓' if len(results['isolated_nodes']) < 5 else '需处理'}
                    </span>
                </span>
            </div>
            <div class="metric">
                <span class="name">中心节点</span>
                <span class="value">{len(results['central_nodes'])}</span>
            </div>
            <div class="metric">
                <span class="name">连接总数</span>
                <span class="value">{stats['edge_count']}</span>
            </div>
        </div>

        <div class="issues">
            <h2>待处理问题</h2>
            <div class="issue-list">
                {generate_issues_html(results)}
            </div>
        </div>

        <div class="footer">
            <div class="timestamp">生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
            <div class="actions">
                <button class="btn btn-secondary" onclick="exportPDF()">导出PDF</button>
                <button class="btn btn-primary" onclick="generateFix()">生成修复脚本</button>
            </div>
        </div>
    </div>

    <script>
        function exportPDF() {{
            window.print();
        }}

        function generateFix() {{
            alert('修复脚本生成功能需要运行 auto_fix.py');
        }}
    </script>
</body>
</html>'''

    # 写入文件
    Path(output_path).write_text(html, encoding='utf-8')
    print(f"报告已生成：{output_path}")

    return output_path


def generate_issues_html(results: Dict) -> str:
    """生成问题列表HTML"""
    issues_html = []

    # 空壳文件
    if results['empty_files']:
        for item in results['empty_files'][:5]:  # 只显示前5个
            file_name = escape_html(item['file'])
            issues_text = escape_html(', '.join(item['issues']))
            size_text = escape_html(str(item['size']))
            issues_html.append(f'''
                <div class="issue-item">
                    <span class="issue-icon">📄</span>
                    <div class="issue-content">
                        <div class="issue-title">{file_name}</div>
                        <div class="issue-desc">{issues_text}（{size_text}字符）</div>
                    </div>
                </div>''')

    # 断链
    if results['broken_links']:
        for item in results['broken_links'][:5]:
            source_name = escape_html(item['source'])
            target_name = escape_html(item['target'])
            error_type = escape_html(item['type'])
            error_text = escape_html(item['error'])
            issues_html.append(f'''
                <div class="issue-item warning">
                    <span class="issue-icon">🔗</span>
                    <div class="issue-content">
                        <div class="issue-title">{source_name} → {target_name}</div>
                        <div class="issue-desc">{error_type}：{error_text}</div>
                    </div>
                </div>''')

    # 孤立节点
    if len(results['isolated_nodes']) > 5:
        issues_html.append(f'''
            <div class="issue-item warning">
                <span class="issue-icon">🏝️</span>
                <div class="issue-content">
                    <div class="issue-title">发现 {len(results['isolated_nodes'])} 个孤立节点</div>
                    <div class="issue-desc">这些文件没有内链连接，建议添加到相关主题</div>
                </div>
            </div>''')

    if not issues_html:
        return '<div class="issue-item" style="background: #f0fdf4; border-left-color: #16a34a;"><span class="issue-icon">✅</span><div class="issue-content"><div class="issue-title">知识库健康状态良好</div><div class="issue-desc">未发现需要处理的问题</div></div></div>'

    return '\n'.join(issues_html)


if __name__ == '__main__':
    import sys

    # 从JSON文件读取结果
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
        results = json.loads(Path(json_file).read_text(encoding='utf-8'))
        generate_report(results)
    else:
        print("Usage: python report_generator.py <results.json>")
