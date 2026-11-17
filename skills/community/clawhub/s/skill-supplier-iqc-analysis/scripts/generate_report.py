#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
报告生成脚本
功能：根据分析结果生成Markdown和HTML格式报告
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from jinja2 import Template


class ReportGenerator:
    """报告生成器"""

    def __init__(self, data_json):
        """初始化报告生成器"""
        self.data = json.loads(data_json) if isinstance(data_json, str) else data_json

    def generate_markdown(self):
        """生成Markdown格式报告"""
        md_lines = []

        # 标题
        md_lines.append("# IQC供应商质量分析报告")
        md_lines.append(f"\n**报告生成时间**: {self.data.get('report_date', '')}\n")

        # 一、数据汇总
        md_lines.append("## 一、数据汇总")
        md_lines.append(f"- **分析供应商数量**: {self.data['summary']['supplier_count']} 家")
        md_lines.append(f"- **总来料批次**: {self.data['summary']['total_batches']} 批次")
        md_lines.append(f"- **总来料数量**: {self.data['summary']['total_quantity']} 件")
        md_lines.append(f"- **总不良数量**: {self.data['summary']['total_defects']} 件\n")

        # 二、关键质量指标
        md_lines.append("## 二、关键质量指标")
        md_lines.append(f"- **批次合格率**: {self.data['summary']['batch_pass_rate']}%")
        md_lines.append(f"- **来料不良PPM**: {self.data['summary']['ppm']} PPM\n")

        # 三、单供应商质量汇总
        if self.data.get('supplier_summary'):
            md_lines.append("## 三、单供应商质量汇总")
            md_lines.append("| 供应商名称 | 来料批次 | 来料数量 | 不良数量 | 批次合格率 | PPM | 风险等级 |")
            md_lines.append("|-----------|---------|---------|---------|-----------|-----|---------|")
            for item in self.data['supplier_summary']:
                md_lines.append(
                    f"| {item['supplier']} | {item['batches']} | {item['quantity']} | "
                    f"{item['defects']} | {item['pass_rate']}% | {item['ppm']} | {item['risk_level']} |"
                )
            md_lines.append("")

        # 四、不良类型TOP分析
        if self.data.get('defect_type_top'):
            md_lines.append("## 四、不良类型TOP分析")
            md_lines.append("| 排名 | 不良类型 | 不良次数 | 占比 |")
            md_lines.append("|-----|---------|---------|------|")
            for idx, item in enumerate(self.data['defect_type_top'], 1):
                md_lines.append(
                    f"| {idx} | {item['defect_type']} | {item['count']} | {item['percentage']}% |"
                )
            md_lines.append("")

        # 五、检验项目TOP分析
        if self.data.get('inspect_item_top'):
            md_lines.append("## 五、检验项目TOP分析")
            md_lines.append("| 排名 | 检验项目 | 不良次数 | 占比 |")
            md_lines.append("|-----|---------|---------|------|")
            for idx, item in enumerate(self.data['inspect_item_top'], 1):
                md_lines.append(
                    f"| {idx} | {item['inspect_item']} | {item['count']} | {item['percentage']}% |"
                )
            md_lines.append("")

        # 六、多供应商横向对标
        if self.data.get('supplier_comparison'):
            md_lines.append("## 六、多供应商横向对标")
            md_lines.append("| 排名 | 供应商名称 | 批次合格率 | PPM | 综合得分 |")
            md_lines.append("|-----|-----------|-----------|-----|---------|")
            for idx, item in enumerate(self.data['supplier_comparison'], 1):
                md_lines.append(
                    f"| {idx} | {item['supplier']} | {item['pass_rate']}% | {item['ppm']} | {item['score']} |"
                )
            md_lines.append("")

        # 七、质量趋势分析
        if self.data.get('trend_data'):
            md_lines.append("## 七、质量趋势分析")
            md_lines.append("| 时间周期 | 批次合格率 |")
            md_lines.append("|---------|-----------|")
            for item in self.data['trend_data']:
                md_lines.append(f"| {item['period']} | {item['pass_rate']}% |")
            md_lines.append("")

        # 八、专项分析结论
        md_lines.append("## 八、专项分析结论")
        for conclusion in self.data.get('conclusions', []):
            # 移除HTML标签（Markdown不支持）
            clean_conclusion = conclusion.replace('<span class=\'highlight\'>', '**').replace('</span>', '**')
            clean_conclusion = clean_conclusion.replace('<span class=\'good-highlight\'>', '**').replace('</span>', '**')
            md_lines.append(f"- {clean_conclusion}")
        md_lines.append("")

        md_lines.append("---")
        md_lines.append("\n*本报告由SQE质量分析系统自动生成，仅供内部质量管理使用*")

        return "\n".join(md_lines)

    def generate_html(self):
        """生成HTML格式报告"""
        template_path = Path(__file__).parent.parent / "assets" / "report-template.html"

        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
        except FileNotFoundError:
            # 如果模板不存在，使用内置模板
            template_content = self._get_builtin_template()

        template = Template(template_content)
        html_content = template.render(**self.data)

        return html_content

    def _get_builtin_template(self):
        """内置HTML模板（备用）"""
        return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>IQC供应商质量分析报告</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
        h1, h2 { color: #333; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        table th, table td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        table th { background-color: #4CAF50; color: white; }
        .summary { background-color: #f5f5f5; padding: 15px; margin: 20px 0; }
        .conclusion { background-color: #fff3cd; padding: 15px; margin: 20px 0; border-left: 4px solid #ffc107; }
    </style>
</head>
<body>
    <h1>IQC供应商质量分析报告</h1>
    <p>报告生成时间：{{report_date}}</p>

    <div class="summary">
        <h2>数据汇总</h2>
        <ul>
            <li>分析供应商数量：{{supplier_count}} 家</li>
            <li>总来料批次：{{total_batches}} 批次</li>
            <li>总来料数量：{{total_quantity}} 件</li>
            <li>总不良数量：{{total_defects}} 件</li>
        </ul>
    </div>

    <h2>关键质量指标</h2>
    <ul>
        <li>批次合格率：{{batch_pass_rate}}%</li>
        <li>来料不良PPM：{{ppm}} PPM</li>
    </ul>

    <div class="conclusion">
        <h2>专项分析结论</h2>
        {% for conclusion in conclusions %}
        <p>{{conclusion|safe}}</p>
        {% endfor %}
    </div>
</body>
</html>'''


def main():
    parser = argparse.ArgumentParser(description='生成IQC质量分析报告')
    parser.add_argument('--data', required=True, help='分析结果JSON字符串或文件路径')
    parser.add_argument('--output_dir', default='.', help='输出目录')
    parser.add_argument('--prefix', default='IQC分析报告', help='输出文件名前缀')

    args = parser.parse_args()

    # 读取数据
    try:
        data_path = Path(args.data)
        if data_path.exists():
            with open(data_path, 'r', encoding='utf-8') as f:
                data_json = f.read()
        else:
            data_json = args.data
    except Exception as e:
        print(f"读取数据失败: {e}", file=sys.stderr)
        sys.exit(1)

    # 生成报告
    generator = ReportGenerator(data_json)

    # 生成Markdown报告
    md_content = generator.generate_markdown()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    md_file = Path(args.output_dir) / f"{args.prefix}_{timestamp}.md"

    try:
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"Markdown报告已生成: {md_file}")
    except Exception as e:
        print(f"生成Markdown报告失败: {e}", file=sys.stderr)
        sys.exit(1)

    # 生成HTML报告
    html_content = generator.generate_html()
    html_file = Path(args.output_dir) / f"{args.prefix}_{timestamp}.html"

    try:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML报告已生成: {html_file}")
    except Exception as e:
        print(f"生成HTML报告失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
