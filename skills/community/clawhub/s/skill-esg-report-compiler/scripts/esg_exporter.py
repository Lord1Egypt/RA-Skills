#!/usr/bin/env python3
"""
ESG Exporter - ESG报告导出工具
支持生成PDF/HTML格式的ESG报告
"""

import argparse
import json
from datetime import datetime
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY


# 报告配置
REPORT_CONFIG = {
    "title": "ESG可持续发展报告",
    "subtitle": "环境、社会与治理绩效报告",
    "company_name": "示例企业",
    "report_period": ""
}


def create_pdf_report(data, output_file, config=None):
    """
    生成PDF格式ESG报告
    
    Args:
        data: ESG数据字典
        output_file: 输出PDF文件路径
        config: 报告配置
    """
    config = config or REPORT_CONFIG
    
    # 创建文档
    doc = SimpleDocTemplate(
        output_file,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    # 样式定义
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='Title_CN',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=24,
        alignment=TA_CENTER,
        spaceAfter=12
    ))
    styles.add(ParagraphStyle(
        name='Subtitle_CN',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=14,
        alignment=TA_CENTER,
        spaceAfter=30
    ))
    styles.add(ParagraphStyle(
        name='Section_CN',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        spaceBefore=20,
        spaceAfter=12,
        textColor=colors.HexColor('#1a237e')
    ))
    styles.add(ParagraphStyle(
        name='Body_CN',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
        leading=16
    ))
    
    story = []
    
    # 封面
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph(config.get('company_name', ''), styles['Title_CN']))
    story.append(Paragraph(config.get('title', 'ESG报告'), styles['Title_CN']))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph(config.get('subtitle', ''), styles['Subtitle_CN']))
    story.append(Spacer(1, 2*cm))
    
    # 报告信息
    story.append(Paragraph(f"<b>报告期:</b> {data.get('dimensions', {}).get('environmental', {}).get('E1', {}).get('period', config.get('report_period', ''))}", styles['Body_CN']))
    story.append(Paragraph(f"<b>编制日期:</b> {datetime.now().strftime('%Y年%m月%d日')}", styles['Body_CN']))
    story.append(Paragraph(f"<b>报告版本:</b> 1.0", styles['Body_CN']))
    
    story.append(PageBreak())
    
    # 目录
    story.append(Paragraph("目 录", styles['Section_CN']))
    toc_items = [
        "1. 执行摘要",
        "2. ESG绩效概览",
        "3. 环境维度绩效",
        "4. 社会维度绩效",
        "5. 治理维度绩效",
        "6. 关键指标汇总表"
    ]
    for item in toc_items:
        story.append(Paragraph(item, styles['Body_CN']))
    
    story.append(PageBreak())
    
    # 执行摘要
    story.append(Paragraph("1. 执行摘要", styles['Section_CN']))
    summary_text = """
    本报告全面披露了公司在环境、社会与治理（ESG）三个维度的可持续发展绩效。
    报告编制遵循GRI（全球报告倡议组织）标准框架，确保信息的完整性、可靠性和可比性。
    """
    story.append(Paragraph(summary_text.strip(), styles['Body_CN']))
    story.append(Spacer(1, 0.5*cm))
    
    # 数据汇总
    completeness = data.get('completeness_score', 0)
    total_metrics = sum(len(v) for v in data.get('dimensions', {}).values())
    story.append(Paragraph(f"<b>数据完整性:</b> 本次报告涵盖 {total_metrics} 项关键ESG指标，数据完整度达 {completeness:.1f}%", styles['Body_CN']))
    
    # ESG绩效概览
    story.append(Paragraph("2. ESG绩效概览", styles['Section_CN']))
    
    # 雷达图说明
    if Path('esg_radar.png').exists():
        story.append(Paragraph("<b>ESG综合评分:</b>", styles['Body_CN']))
        story.append(Image('esg_radar.png', width=10*cm, height=10*cm))
        story.append(Spacer(1, 0.5*cm))
    
    # 各维度汇总
    for dim, dim_name in [('environmental', '环境'), ('social', '社会'), ('governance', '治理')]:
        dim_data = data.get('dimensions', {}).get(dim, {})
        if dim_data:
            valid_count = sum(1 for v in dim_data.values() if v.get('value') is not None)
            story.append(Paragraph(f"<b>{dim_name}维度:</b> 已收集 {valid_count}/{len(dim_data)} 项指标", styles['Body_CN']))
    
    story.append(PageBreak())
    
    # 环境维度
    story.append(Paragraph("3. 环境维度绩效", styles['Section_CN']))
    story.append(Paragraph("本章节披露公司在环境保护、资源利用和气候变化应对方面的绩效数据。", styles['Body_CN']))
    
    env_data = data.get('dimensions', {}).get('environmental', {})
    if env_data:
        for metric_id, info in env_data.items():
            if info.get('value') is not None:
                story.append(Paragraph(f"<b>{info.get('name', metric_id)}:</b> {info.get('value')} {info.get('unit', '')}", styles['Body_CN']))
    
    # 社会维度
    story.append(Paragraph("4. 社会维度绩效", styles['Section_CN']))
    story.append(Paragraph("本章节披露公司在员工发展、社区参与和社会责任方面的绩效数据。", styles['Body_CN']))
    
    soc_data = data.get('dimensions', {}).get('social', {})
    if soc_data:
        for metric_id, info in soc_data.items():
            if info.get('value') is not None:
                story.append(Paragraph(f"<b>{info.get('name', metric_id)}:</b> {info.get('value')} {info.get('unit', '')}", styles['Body_CN']))
    
    story.append(PageBreak())
    
    # 治理维度
    story.append(Paragraph("5. 治理维度绩效", styles['Section_CN']))
    story.append(Paragraph("本章节披露公司在公司治理、合规经营和风险管理方面的绩效数据。", styles['Body_CN']))
    
    gov_data = data.get('dimensions', {}).get('governance', {})
    if gov_data:
        for metric_id, info in gov_data.items():
            if info.get('value') is not None:
                story.append(Paragraph(f"<b>{info.get('name', metric_id)}:</b> {info.get('value')} {info.get('unit', '')}", styles['Body_CN']))
    
    # 关键指标汇总表
    story.append(Paragraph("6. 关键指标汇总表", styles['Section_CN']))
    
    table_data = [['指标ID', '指标名称', '数值', '单位', '报告期']]
    
    for dim_data in data.get('dimensions', {}).values():
        for metric_id, info in dim_data.items():
            if info.get('value') is not None:
                table_data.append([
                    metric_id,
                    info.get('name', ''),
                    str(info.get('value', '')),
                    info.get('unit', ''),
                    str(info.get('period', ''))
                ])
    
    table = Table(table_data, colWidths=[2*cm, 4*cm, 3*cm, 2*cm, 3*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f5f5')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cccccc')),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))
    
    story.append(table)
    
    # 附录
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("<b>附录: 数据来源与说明</b>", styles['Body_CN']))
    story.append(Paragraph("本报告数据来源于公司内部管理信息系统及各部门统计数据。数据截止日期为报告期末。", styles['Body_CN']))
    story.append(Paragraph("报告编制联系人: ESG管理委员会 | 联系方式: esg@example.com", styles['Body_CN']))
    
    # 生成PDF
    doc.build(story)
    
    return output_file


def export_html_report(data, output_file, config=None):
    """导出HTML格式报告"""
    config = config or REPORT_CONFIG
    
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{config.get('title', 'ESG报告')}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: "Microsoft YaHei", Arial, sans-serif; line-height: 1.8; color: #333; }}
        .container {{ max-width: 1000px; margin: 0 auto; padding: 40px 20px; }}
        .header {{ text-align: center; padding: 60px 0; border-bottom: 3px solid #1a237e; margin-bottom: 40px; }}
        .header h1 {{ font-size: 36px; color: #1a237e; margin-bottom: 10px; }}
        .header h2 {{ font-size: 24px; color: #666; font-weight: normal; }}
        .section {{ margin-bottom: 50px; }}
        .section h2 {{ font-size: 24px; color: #1a237e; border-left: 5px solid #1a237e; padding-left: 15px; margin-bottom: 20px; }}
        .metric-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }}
        .metric-card {{ background: #f8f9fa; padding: 20px; border-radius: 8px; border-left: 4px solid #2196F3; }}
        .metric-card .label {{ font-size: 14px; color: #666; }}
        .metric-card .value {{ font-size: 28px; font-weight: bold; color: #1a237e; }}
        .metric-card .unit {{ font-size: 14px; color: #999; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px 15px; text-align: left; border: 1px solid #ddd; }}
        th {{ background: #1a237e; color: white; }}
        tr:nth-child(even) {{ background: #f8f9fa; }}
        .footer {{ text-align: center; padding: 30px; color: #666; font-size: 14px; border-top: 1px solid #ddd; margin-top: 50px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{config.get('company_name', '')}</h1>
            <h2>{config.get('title', 'ESG可持续发展报告')}</h2>
            <p style="margin-top: 20px; color: #666;">报告期: {data.get('dimensions', {}).get('environmental', {}).get('E1', {}).get('period', '')}</p>
        </div>
        
        <div class="section">
            <h2>执行摘要</h2>
            <p>本报告全面披露了公司在环境、社会与治理（ESG）三个维度的可持续发展绩效。</p>
            <p style="margin-top: 15px;"><strong>数据完整性:</strong> 本次报告涵盖 {sum(len(v) for v in data.get('dimensions', {}).values())} 项关键ESG指标。</p>
        </div>
        
        <div class="section">
            <h2>ESG绩效概览</h2>
            <div class="metric-grid">
"""
    
    # 添加各维度汇总
    for dim, dim_name, color in [
        ('environmental', '环境维度', '#2E7D32'),
        ('social', '社会维度', '#1565C0'),
        ('governance', '治理维度', '#7B1FA2')
    ]:
        dim_data = data.get('dimensions', {}).get(dim, {})
        if dim_data:
            valid = sum(1 for v in dim_data.values() if v.get('value') is not None)
            total = len(dim_data)
            html_content += f"""
                <div class="metric-card" style="border-left-color: {color};">
                    <div class="label">{dim_name}</div>
                    <div class="value">{valid}/{total}</div>
                    <div class="unit">已收集指标数</div>
                </div>
"""
    
    html_content += """
            </div>
        </div>
        
        <div class="section">
            <h2>环境维度</h2>
            <table>
                <tr><th>指标</th><th>数值</th><th>单位</th><th>报告期</th></tr>
"""
    
    for metric_id, info in data.get('dimensions', {}).get('environmental', {}).items():
        if info.get('value') is not None:
            html_content += f"""
                <tr>
                    <td>{info.get('name', metric_id)}</td>
                    <td>{info.get('value')}</td>
                    <td>{info.get('unit', '')}</td>
                    <td>{info.get('period', '')}</td>
                </tr>
"""
    
    html_content += """
            </table>
        </div>
        
        <div class="section">
            <h2>社会维度</h2>
            <table>
                <tr><th>指标</th><th>数值</th><th>单位</th><th>报告期</th></tr>
"""
    
    for metric_id, info in data.get('dimensions', {}).get('social', {}).items():
        if info.get('value') is not None:
            html_content += f"""
                <tr>
                    <td>{info.get('name', metric_id)}</td>
                    <td>{info.get('value')}</td>
                    <td>{info.get('unit', '')}</td>
                    <td>{info.get('period', '')}</td>
                </tr>
"""
    
    html_content += """
            </table>
        </div>
        
        <div class="section">
            <h2>治理维度</h2>
            <table>
                <tr><th>指标</th><th>数值</th><th>单位</th><th>报告期</th></tr>
"""
    
    for metric_id, info in data.get('dimensions', {}).get('governance', {}).items():
        if info.get('value') is not None:
            html_content += f"""
                <tr>
                    <td>{info.get('name', metric_id)}</td>
                    <td>{info.get('value')}</td>
                    <td>{info.get('unit', '')}</td>
                    <td>{info.get('period', '')}</td>
                </tr>
"""
    
    html_content += f"""
            </table>
        </div>
        
        <div class="footer">
            <p>编制单位: ESG管理委员会 | 编制日期: {datetime.now().strftime('%Y年%m月%d日')}</p>
            <p>联系方式: esg@example.com</p>
        </div>
    </div>
</body>
</html>
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return output_file


def main():
    parser = argparse.ArgumentParser(description='ESG报告导出工具')
    parser.add_argument('--input', '-i', required=True, help='ESG数据文件(JSON)')
    parser.add_argument('--output', '-o', required=True, help='输出文件路径')
    parser.add_argument('--format', '-f', choices=['pdf', 'html'], default='pdf', help='输出格式')
    parser.add_argument('--company', '-c', default='示例企业', help='公司名称')
    parser.add_argument('--title', '-t', default='ESG可持续发展报告', help='报告标题')
    
    args = parser.parse_args()
    
    # 读取数据
    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    config = {
        "company_name": args.company,
        "title": args.title,
        "report_period": data.get('dimensions', {}).get('environmental', {}).get('E1', {}).get('period', '')
    }
    
    # 生成报告
    if args.format == 'pdf':
        output_file = create_pdf_report(data, args.output, config)
    else:
        output_file = export_html_report(data, args.output, config)
    
    result = {
        "status": "success",
        "format": args.format,
        "output_file": output_file
    }
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
