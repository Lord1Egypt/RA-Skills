#!/usr/bin/env python3
"""
简历优化脚本
功能：读取 PDF 简历，调用 Claude API 评估内容，生成精美的 HTML 报告
"""

import os
import sys
import json
import argparse
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    print("请安装必要的依赖：pip install pdfplumber")
    sys.exit(1)


# Claude API 配置
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_AUTH_TOKEN", "")
ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "MiniMax-M2.5")


def extract_text_from_pdf(pdf_path: str) -> str:
    """从 PDF 文件中提取文本内容"""
    text_content = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            if text:
                text_content.append(f"--- 第 {page_num} 页 ---\n{text}")

    return "\n\n".join(text_content)


def evaluate_resume_with_claude(text: str, resume_type: str) -> str:
    """调用 Claude API 评估简历并生成 HTML 报告"""
    if not ANTHROPIC_API_KEY:
        print("错误：未设置 ANTHROPIC_AUTH_TOKEN 环境变量")
        sys.exit(1)

    try:
        import anthropic
    except ImportError:
        print("请安装 anthropic 库：pip install anthropic")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    # 根据简历类型设置系统提示
    if resume_type == "前端":
        system_prompt = """你是一名前端架构师，负责对用户上传的简历进行专业分析和优化。

## 评估步骤

1. **全面阅读简历**：深入了解求职者的基本信息、工作经历、教育背景、项目经验等，不放过任何一个细节。

2. **整体质量评估**：
   - 格式：排版、信息层级、字体统一、段落间距
   - 内容完整性：必要模块是否齐全
   - 语言表达：用词专业性、描述简洁度

3. **项目详细分析**：
   - 分析项目描述是否清晰、成果是否突出
   - 为每个项目提炼详细亮点描述，包含解决方案、关键技术、实施步骤
   - 分析成果是否量化（如：首屏加载时间从4s降至1.5s）

4. **优化建议**：针对每个问题，解释为什么提出建议以及如何提升简历质量

5. **评分标准（满分100分）**：
   - 技术深度（30分）：技术栈深度和广度、项目复杂度、解决方案专业性
   - 业务价值（25分）：项目成果量化程度、对业务影响程度
   - 表达专业度（20分）：描述清晰度、用词准确性、逻辑连贯性
   - 整体结构（15分）：模块完整性、排版美观度、信息有序性
   - 亮点突出度（10分）：是否有吸睛亮点、亮点是否具体可衡量

## 输出要求

请用中文输出，返回 JSON 格式，包含以下字段：

- overall_score: 整体评分（1-100的具体分数）
- summary: 整体概述（100字以内）

- format_assessment: 格式评估
  - score: 分数（满分15）
  - pros: 优点数组
  - issues: 问题数组

- content_assessment: 内容评估
  - score: 分数（满分30）
  - pros: 优点数组
  - issues: 问题数组

- skill_assessment: 技能栈评估
  - score: 分数（满分15）
  - analysis: 分析内容

- project_evaluations: 项目评估数组，每个包含：
  - project_name: 项目名称
  - original_description: 原始描述
  - highlights: 亮点数组，每个包含：
    - description: 亮点描述
    - solution: 解决方案（具体到每个步骤和关键技术）
    - value: 价值体现
  - suggestions: 优化建议数组

- strengths: 优点数组（整体层面）
- weaknesses: 不足数组（整体层面）
- overall_advice: 整体建议总结（200字以内）

只返回 JSON，不要添加任何解释。"""
    else:
        system_prompt = """你是一位资深后端架构师，负责对用户上传的简历进行专业分析和优化。

## 评估步骤

1. **全面阅读简历**：深入了解求职者的基本信息、工作经历、教育背景、项目经验等，不放过任何一个细节。

2. **整体质量评估**：
   - 格式：排版、信息层级、字体统一、段落间距
   - 内容完整性：必要模块是否齐全
   - 语言表达：用词专业性、描述简洁度

3. **项目详细分析**：
   - 分析项目描述是否清晰、成果是否突出
   - 为每个项目提炼详细亮点描述，包含解决方案、关键技术、实施步骤
   - 分析成果是否量化（如：QPS从1000提升到5000，系统可用性从99.9%提升到99.99%）

4. **优化建议**：针对每个问题，解释为什么提出建议以及如何提升简历质量

5. **评分标准（满分100分）**：
   - 系统设计能力（30分）：架构设计深度、系统复杂度、解决方案专业性
   - 高并发处理经验（25分）：大流量处理能力、性能优化成果、稳定性保障能力
   - 业务价值（20分）：项目成果量化程度、对业务影响程度
   - 表达专业度（15分）：描述清晰度、用词准确性、逻辑连贯性
   - 整体结构（10分）：模块完整性、排版美观度、信息有序性

## 输出要求

请用中文输出，返回 JSON 格式，包含以下字段：

- overall_score: 整体评分（1-100的具体分数）
- summary: 整体概述（100字以内）

- format_assessment: 格式评估
  - score: 分数（满分10）
  - pros: 优点数组
  - issues: 问题数组

- skill_assessment: 技能栈评估
  - score: 分数（满分15）
  - analysis: 分析内容

- project_evaluations: 项目评估数组，每个包含：
  - project_name: 项目名称
  - original_description: 原始描述
  - highlights: 亮点数组，每个包含：
    - description: 亮点描述
    - solution: 解决方案（具体到每个步骤和关键技术）
    - value: 价值体现
  - suggestions: 优化建议数组

- strengths: 优点数组（整体层面）
- weaknesses: 不足数组（整体层面）
- overall_advice: 整体建议总结（200字以内）

只返回 JSON，不要添加任何解释。"""

    message = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=8000,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": f"请评估以下简历：\n\n{text}"
            }
        ]
    )

    # 遍历内容块，找到文本内容
    for block in message.content:
        if hasattr(block, 'text'):
            return block.text

    return ""


def escape_html(text: str) -> str:
    """转义 HTML 特殊字符"""
    if not text:
        return ""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#39;'))


def generate_html_report(evaluation_json: str, output_path: str, resume_type: str):
    """生成精美的 HTML 报告"""

    # 解析 JSON
    try:
        data = json.loads(evaluation_json)
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {e}")
        print("原始返回内容:", evaluation_json[:500])
        sys.exit(1)

    # 确定评分颜色
    score = data.get('overall_score', 0)
    if score >= 80:
        score_color = "#52c41a"
        score_label = "优秀"
    elif score >= 60:
        score_color = "#faad14"
        score_label = "良好"
    else:
        score_color = "#ff4d4f"
        score_label = "待提升"

    # 解析各项数据
    summary = data.get('summary', '')
    strengths = data.get('strengths', [])
    weaknesses = data.get('weaknesses', [])
    overall_advice = data.get('overall_advice', '')

    # 格式评估
    format_assessment = data.get('format_assessment', {})
    format_score = format_assessment.get('score', 0)
    format_pros = format_assessment.get('pros', [])
    format_issues = format_assessment.get('issues', [])

    # 内容评估
    content_assessment = data.get('content_assessment', {})
    content_score = content_assessment.get('score', 0)
    content_pros = content_assessment.get('pros', [])
    content_issues = content_assessment.get('issues', [])

    # 技能评估
    skill_assessment = data.get('skill_assessment', {})
    skill_score = skill_assessment.get('score', 0)
    skill_analysis = skill_assessment.get('analysis', '')

    # 项目评估
    project_evaluations = data.get('project_evaluations', [])

    # 生成格式评估 HTML
    format_pros_html = ""
    if format_pros:
        for p in format_pros:
            format_pros_html += f'<div class="mini-item"><span class="plus">+</span> {escape_html(p)}</div>'
    else:
        format_pros_html = '<p style="color: #999; font-size: 14px;">暂无优点</p>'

    format_issues_html = ""
    if format_issues:
        for i in format_issues:
            format_issues_html += f'<div class="mini-item"><span class="minus">-</span> {escape_html(i)}</div>'
    else:
        format_issues_html = '<p style="color: #999; font-size: 14px;">暂无问题</p>'

    # 生成内容评估 HTML
    content_pros_html = ""
    if content_pros:
        for p in content_pros:
            content_pros_html += f'<div class="mini-item"><span class="plus">+</span> {escape_html(p)}</div>'
    else:
        content_pros_html = '<p style="color: #999; font-size: 14px;">暂无优点</p>'

    content_issues_html = ""
    if content_issues:
        for i in content_issues:
            content_issues_html += f'<div class="mini-item"><span class="minus">-</span> {escape_html(i)}</div>'
    else:
        content_issues_html = '<p style="color: #999; font-size: 14px;">暂无问题</p>'

    # 生成优点列表 HTML
    strengths_html = ""
    if strengths:
        for s in strengths:
            strengths_html += f'''
                <div class="item">
                    <div class="item-icon">✓</div>
                    <div class="item-content">
                        <p>{escape_html(s)}</p>
                    </div>
                </div>'''
    else:
        strengths_html = '<p style="color: #999;">暂无优点</p>'

    # 生成不足列表 HTML
    weaknesses_html = ""
    if weaknesses:
        for w in weaknesses:
            weaknesses_html += f'''
                <div class="item">
                    <div class="item-icon">!</div>
                    <div class="item-content">
                        <p>{escape_html(w)}</p>
                    </div>
                </div>'''
    else:
        weaknesses_html = '<p style="color: #999;">暂无不足</p>'

    # 生成项目评估 HTML
    projects_html = ""
    if project_evaluations:
        for proj in project_evaluations:
            project_name = escape_html(proj.get('project_name', '未命名项目'))
            original_desc = escape_html(proj.get('original_description', ''))

            # 亮点
            highlights = proj.get('highlights', [])
            highlights_html = ""
            if highlights:
                for h in highlights:
                    desc = escape_html(h.get('description', ''))
                    solution = escape_html(h.get('solution', ''))
                    value = escape_html(h.get('value', ''))
                    highlights_html += f'''
                    <div class="highlight-item">
                        <div class="highlight-desc">{desc}</div>
                        <div class="highlight-detail">
                            <div><strong>解决方案：</strong>{solution}</div>
                            <div><strong>价值体现：</strong>{value}</div>
                        </div>
                    </div>'''

            # 建议
            suggestions = proj.get('suggestions', [])
            suggestions_html = ""
            if suggestions:
                for sug in suggestions:
                    suggestions_html += f'<div class="project-suggestion">• {escape_html(sug)}</div>'

            projects_html += f'''
            <div class="project-card">
                <div class="project-name">{project_name}</div>
                <div class="project-original">
                    <div class="section-label">原始描述</div>
                    <p>{original_desc}</p>
                </div>
                {f'<div class="project-highlights"><div class="section-label">亮点提炼</div>{highlights_html}</div>' if highlights else ''}
                {f'<div class="project-suggestions"><div class="section-label">优化建议</div>{suggestions_html}</div>' if suggestions else ''}
            </div>'''

    # 生成 HTML
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>简历评估报告 - {resume_type}工程师</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}

        .header {{
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }}

        .header h1 {{
            font-size: 36px;
            font-weight: 700;
            margin-bottom: 10px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        .header p {{
            font-size: 18px;
            opacity: 0.9;
        }}

        .score-card {{
            background: white;
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        }}

        .score-circle {{
            width: 180px;
            height: 180px;
            border-radius: 50%;
            background: conic-gradient({score_color} {score * 3.6}deg, #f0f0f0 0deg);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 20px;
            position: relative;
        }}

        .score-circle::before {{
            content: '';
            position: absolute;
            width: 150px;
            height: 150px;
            background: white;
            border-radius: 50%;
        }}

        .score-value {{
            position: relative;
            z-index: 1;
            font-size: 48px;
            font-weight: 800;
            color: {score_color};
        }}

        .score-label {{
            font-size: 20px;
            color: #666;
            font-weight: 500;
        }}

        .summary {{
            background: #f8f9fa;
            border-radius: 12px;
            padding: 24px;
            margin-top: 30px;
            text-align: left;
        }}

        .summary h3 {{
            color: #333;
            font-size: 18px;
            margin-bottom: 12px;
        }}

        .summary p {{
            color: #666;
            line-height: 1.8;
            font-size: 15px;
        }}

        .card {{
            background: white;
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 24px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.08);
        }}

        .card-title {{
            font-size: 22px;
            font-weight: 700;
            color: #1a1a1a;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
        }}

        .card-title::before {{
            content: '';
            width: 4px;
            height: 24px;
            background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
            border-radius: 2px;
            margin-right: 12px;
        }}

        .score-breakdown {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }}

        .score-item {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 16px;
            text-align: center;
        }}

        .score-item-label {{
            font-size: 14px;
            color: #666;
            margin-bottom: 8px;
        }}

        .score-item-value {{
            font-size: 28px;
            font-weight: 700;
            color: #667eea;
        }}

        .mini-item {{
            padding: 8px 12px;
            margin-bottom: 8px;
            background: #f8f9fa;
            border-radius: 6px;
            font-size: 14px;
            color: #444;
        }}

        .mini-item .plus {{
            color: #52c41a;
            font-weight: bold;
            margin-right: 8px;
        }}

        .mini-item .minus {{
            color: #ff4d4f;
            font-weight: bold;
            margin-right: 8px;
        }}

        .item {{
            display: flex;
            align-items: flex-start;
            padding: 16px 20px;
            border-radius: 10px;
            background: #f8f9fa;
            margin-bottom: 12px;
        }}

        .item-icon {{
            width: 28px;
            height: 28px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 14px;
            flex-shrink: 0;
            font-size: 14px;
        }}

        .strengths-list .item-icon {{
            background: #e6f7ff;
            color: #1890ff;
        }}

        .weaknesses-list .item-icon {{
            background: #fff2f0;
            color: #ff4d4f;
        }}

        .item-content {{
            flex: 1;
        }}

        .item-content p {{
            color: #444;
            line-height: 1.6;
            font-size: 15px;
        }}

        .project-card {{
            background: #f8f9fa;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            border-left: 4px solid #667eea;
        }}

        .project-name {{
            font-size: 18px;
            font-weight: 700;
            color: #1a1a1a;
            margin-bottom: 16px;
        }}

        .project-original {{
            margin-bottom: 16px;
        }}

        .section-label {{
            font-size: 13px;
            font-weight: 600;
            color: #667eea;
            margin-bottom: 8px;
            text-transform: uppercase;
        }}

        .project-original p {{
            color: #666;
            font-size: 14px;
            line-height: 1.6;
        }}

        .project-highlights {{
            margin-bottom: 16px;
        }}

        .highlight-item {{
            background: white;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 12px;
        }}

        .highlight-desc {{
            font-weight: 600;
            color: #1a1a1a;
            margin-bottom: 10px;
        }}

        .highlight-detail {{
            font-size: 13px;
            color: #666;
            line-height: 1.6;
        }}

        .highlight-detail div {{
            margin-bottom: 4px;
        }}

        .highlight-detail strong {{
            color: #333;
        }}

        .project-suggestions {{
            background: white;
            border-radius: 8px;
            padding: 16px;
        }}

        .project-suggestion {{
            color: #666;
            font-size: 14px;
            margin-bottom: 8px;
            line-height: 1.6;
        }}

        .skill-analysis {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            color: #444;
            line-height: 1.8;
            font-size: 14px;
        }}

        .overall-advice {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            padding: 24px;
            color: white;
        }}

        .overall-advice h4 {{
            font-size: 18px;
            margin-bottom: 12px;
        }}

        .overall-advice p {{
            font-size: 15px;
            line-height: 1.8;
            opacity: 0.95;
        }}

        .footer {{
            text-align: center;
            margin-top: 40px;
            color: white;
            opacity: 0.8;
            font-size: 14px;
        }}

        @media (max-width: 600px) {{
            body {{
                padding: 20px 16px;
            }}

            .score-card, .card {{
                padding: 20px;
            }}

            .header h1 {{
                font-size: 28px;
            }}

            .score-breakdown {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>简历优化评估报告</h1>
            <p>基于 {resume_type}架构师视角的专业评估</p>
        </div>

        <div class="score-card">
            <div class="score-circle">
                <span class="score-value">{score}</span>
            </div>
            <div class="score-label">{score_label}</div>
            <div class="summary">
                <h3>整体概述</h3>
                <p>{escape_html(summary)}</p>
            </div>
        </div>

        <div class="card">
            <h2 class="card-title">评分明细</h2>
            <div class="score-breakdown">
                <div class="score-item">
                    <div class="score-item-label">格式评估</div>
                    <div class="score-item-value">{format_score}/15</div>
                </div>
                <div class="score-item">
                    <div class="score-item-label">内容评估</div>
                    <div class="score-item-value">{content_score}/30</div>
                </div>
                <div class="score-item">
                    <div class="score-item-label">技能栈</div>
                    <div class="score-item-value">{skill_score}/15</div>
                </div>
            </div>
        </div>

        <div class="card">
            <h2 class="card-title">格式评估</h2>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <h4 style="font-size: 14px; color: #52c41a; margin-bottom: 12px;">优点</h4>
                    {format_pros_html}
                </div>
                <div>
                    <h4 style="font-size: 14px; color: #ff4d4f; margin-bottom: 12px;">问题</h4>
                    {format_issues_html}
                </div>
            </div>
        </div>

        <div class="card">
            <h2 class="card-title">内容评估</h2>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <h4 style="font-size: 14px; color: #52c41a; margin-bottom: 12px;">优点</h4>
                    {content_pros_html}
                </div>
                <div>
                    <h4 style="font-size: 14px; color: #ff4d4f; margin-bottom: 12px;">问题</h4>
                    {content_issues_html}
                </div>
            </div>
        </div>

        <div class="card">
            <h2 class="card-title">技能栈评估 ({skill_score}/15)</h2>
            <div class="skill-analysis">
                {escape_html(skill_analysis)}
            </div>
        </div>

        <div class="card">
            <h2 class="card-title">项目亮点与优化建议</h2>
            {projects_html if projects_html else '<p style="color: #999;">暂无项目评估</p>'}
        </div>

        <div class="card">
            <h2 class="card-title">整体优点</h2>
            <div class="strengths-list">
                {strengths_html}
            </div>
        </div>

        <div class="card">
            <h2 class="card-title">整体不足</h2>
            <div class="weaknesses-list">
                {weaknesses_html}
            </div>
        </div>

        <div class="card">
            <div class="overall-advice">
                <h4>整体优化建议</h4>
                <p>{escape_html(overall_advice)}</p>
            </div>
        </div>

        <div class="footer">
            <p>此报告由 AI 生成，仅供参考</p>
        </div>
    </div>
</body>
</html>"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"评估报告已保存至: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="简历评估工具")
    parser.add_argument("input_pdf", help="输入的 PDF 简历文件路径")
    parser.add_argument("resume_type", choices=["前端", "后端"], help="简历类型")
    parser.add_argument("-o", "--output", help="输出的 HTML 文件路径（默认在原文件名前加 _评估报告.html）")

    args = parser.parse_args()

    input_path = args.input_pdf
    resume_type = args.resume_type
    output_path = args.output

    # 验证输入文件
    if not os.path.exists(input_path):
        print(f"错误：文件不存在: {input_path}")
        sys.exit(1)

    if not input_path.lower().endswith('.pdf'):
        print("错误：只支持 PDF 文件")
        sys.exit(1)

    # 设置输出路径
    if not output_path:
        input_name = Path(input_path).stem
        output_path = f"{input_name}_评估报告.html"

    print(f"正在读取简历: {input_path}")

    # 步骤 1: 提取 PDF 文本
    print("步骤 1/3: 提取 PDF 文本内容...")
    text_content = extract_text_from_pdf(input_path)
    print(f"提取完成，共 {len(text_content)} 字符")

    # 步骤 2: 调用 Claude 评估
    print("步骤 2/3: 正在评估简历（模拟 {resume_type}架构师视角）...")
    evaluation_result = evaluate_resume_with_claude(text_content, resume_type)
    print("评估完成")

    # 步骤 3: 生成 HTML 报告
    print("步骤 3/3: 生成 HTML 评估报告...")
    generate_html_report(evaluation_result, output_path, resume_type)

    print("\n✅ 简历评估完成！请在浏览器中打开生成的 HTML 文件查看报告。")


if __name__ == "__main__":
    main()