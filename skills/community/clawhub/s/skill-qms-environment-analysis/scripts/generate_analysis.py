#!/usr/bin/env python3
"""
QMS环境因素分析脚本
功能：生成SWOT矩阵图、PESTEL雷达图、风险矩阵图及PDF分析报告
用法：
  python generate_analysis.py visualize --data <json_file> --output <output_dir>
  python generate_analysis.py report --data <json_file> --output <output_dir>
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# 图表生成
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 配置中文字体
chinese_fonts = [f.name for f in fm.fontManager.ttflist if 'CJK' in f.name or 'Noto' in f.name or 'SimHei' in f.name or 'WenQuanYi' in f.name or 'Droid' in f.name]
if chinese_fonts:
    plt.rcParams['font.sans-serif'] = chinese_fonts[:1] + ['DejaVu Sans']
else:
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

import matplotlib.patches as mpatches
import numpy as np
from matplotlib.patches import FancyBboxPatch
import matplotlib.patheffects as path_effects

# PDF报告生成
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY


class QMSAnalyzer:
    """QMS环境因素分析器"""
    
    def __init__(self, data_path: str):
        with open(data_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        self.org_name = self.data.get('org_name', '未知组织')
        self.analysis_date = self.data.get('analysis_date', datetime.now().strftime('%Y-%m-%d'))
        self.swot = self.data.get('swot', {})
        self.pestel = self.data.get('pestel', {})
        self.internal_issues = self.data.get('internal_issues', [])
        self.external_issues = self.data.get('external_issues', [])
        
        # 颜色配置
        self.colors = {
            'strengths': '#2E7D32',    # 绿色
            'weaknesses': '#C62828',   # 红色
            'opportunities': '#1565C0', # 蓝色
            'threats': '#EF6C00',      # 橙色
            'background': '#FAFAFA',
            'text': '#212121',
            'grid': '#E0E0E0'
        }
        
        # PESTEL维度颜色
        self.pestel_colors = {
            'political': '#7B1FA2',    # 紫色
            'economic': '#1976D2',     # 蓝色
            'social': '#388E3C',       # 绿色
            'technological': '#F57C00', # 橙色
            'environmental': '#00796B', # 青色
            'legal': '#5D4037'         # 棕色
        }
        
        self.pestel_labels = {
            'political': 'Political\n政治',
            'economic': 'Economic\n经济',
            'social': 'Social\n社会',
            'technological': 'Technological\n技术',
            'environmental': 'Environmental\n环境',
            'legal': 'Legal\n法律'
        }

    def generate_swot_matrix(self, output_path: str):
        """生成SWOT四象限矩阵图"""
        fig, ax = plt.subplots(figsize=(14, 12))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # 标题
        title = f'{self.org_name} SWOT分析矩阵'
        ax.text(5, 9.7, title, fontsize=18, fontweight='bold', ha='center', va='top',
                color=self.colors['text'])
        ax.text(5, 9.3, f'分析日期: {self.analysis_date}', fontsize=10, ha='center', va='top',
                color='#757575')
        
        # 定义象限
        quadrants = [
            {'name': 'Strengths\n优势', 'x': 0.5, 'y': 5.2, 'width': 4.5, 'height': 4.3,
             'color': self.colors['strengths'], 'items': self.swot.get('strengths', []), 'abbr': 'S'},
            {'name': 'Weaknesses\n劣势', 'x': 5.0, 'y': 5.2, 'width': 4.5, 'height': 4.3,
             'color': self.colors['weaknesses'], 'items': self.swot.get('weaknesses', []), 'abbr': 'W'},
            {'name': 'Opportunities\n机遇', 'x': 0.5, 'y': 0.5, 'width': 4.5, 'height': 4.3,
             'color': self.colors['opportunities'], 'items': self.swot.get('opportunities', []), 'abbr': 'O'},
            {'name': 'Threats\n威胁', 'x': 5.0, 'y': 0.5, 'width': 4.5, 'height': 4.3,
             'color': self.colors['threats'], 'items': self.swot.get('threats', []), 'abbr': 'T'}
        ]
        
        # 绘制象限
        for q in quadrants:
            # 背景框
            rect = FancyBboxPatch((q['x'], q['y']), q['width'], q['height'],
                                  boxstyle="round,pad=0.02,rounding_size=0.3",
                                  facecolor=q['color'], alpha=0.15,
                                  edgecolor=q['color'], linewidth=3)
            ax.add_patch(rect)
            
            # 象限标题
            ax.text(q['x'] + q['width']/2, q['y'] + q['height'] - 0.4, q['name'],
                   fontsize=14, fontweight='bold', ha='center', va='top',
                   color=q['color'])
            
            # 编号标签
            ax.text(q['x'] + 0.3, q['y'] + q['height'] - 0.5, q['abbr'],
                   fontsize=24, fontweight='bold', ha='left', va='top',
                   color=q['color'], alpha=0.4)
            
            # 内容列表
            items = q['items'] if q['items'] else ['（待补充）']
            y_pos = q['y'] + q['height'] - 1.3
            for i, item in enumerate(items[:6], 1):  # 最多显示6条
                # 截断过长文本
                display_text = item if len(item) <= 35 else item[:32] + '...'
                ax.text(q['x'] + 0.4, y_pos - i * 0.55, f'{i}. {display_text}',
                       fontsize=9, ha='left', va='top', color=self.colors['text'])
        
        # 中心标签
        ax.text(5, 5, 'SWOT', fontsize=28, fontweight='bold', ha='center', va='center',
               color='#BDBDBD')
        
        # 横纵轴标签
        ax.text(5, 0.1, '内部因素 ← → 外部因素', fontsize=10, ha='center', va='bottom',
               color='#757575', style='italic')
        ax.text(0.1, 5, '积极因素\n↑\n消极因素', fontsize=9, ha='left', va='center',
               color='#757575', style='italic', rotation=90)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        plt.close()
        print(f"[OK] SWOT矩阵图已生成: {output_path}")
        return output_path

    def generate_pestel_radar(self, output_path: str):
        """生成PESTEL雷达图"""
        categories = list(self.pestel.keys())
        N = len(categories)
        
        # 计算每个维度的得分（基于因素数量，标准化到1-10）
        values = []
        for cat in categories:
            items = self.pestel.get(cat, [])
            score = min(len(items) * 2, 10) if items else 1
            values.append(score)
        
        # 计算角度
        angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
        values = values + values[:1]
        angles = angles + angles[:1]
        
        fig, ax = plt.subplots(figsize=(12, 10), subplot_kw=dict(polar=True))
        
        # 背景圆
        ax.set_facecolor(self.colors['background'])
        
        # 绘制网格
        for level in [2, 4, 6, 8, 10]:
            ax.plot(angles, [level] * (N + 1), '--', color='#E0E0E0', linewidth=0.8)
        
        # 绘制数据
        ax.plot(angles, values, 'o-', linewidth=2.5, color='#1565C0', markersize=8)
        ax.fill(angles, values, alpha=0.25, color='#1565C0')
        
        # 设置维度标签
        labels = [self.pestel_labels.get(cat, cat) for cat in categories]
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, fontsize=10)
        
        # 设置Y轴
        ax.set_ylim(0, 10)
        ax.set_yticks([2, 4, 6, 8, 10])
        ax.set_yticklabels(['2', '4', '6', '8', '10'], fontsize=8, color='#9E9E9E')
        
        # 标题
        ax.set_title(f'{self.org_name}\nPESTEL外部环境分析', 
                    fontsize=16, fontweight='bold', pad=20, color=self.colors['text'])
        
        # 添加图例说明
        legend_text = "注：得分基于各维度因素数量，反映关注程度"
        ax.text(0.5, -0.15, legend_text, transform=ax.transAxes,
               fontsize=8, ha='center', color='#757575', style='italic')
        
        # 在雷达图外侧显示各维度详细数量
        for i, (cat, val) in enumerate(zip(categories, values[:-1])):
            count = len(self.pestel.get(cat, []))
            ax.annotate(f'({count})', xy=(angles[i], val),
                       xytext=(angles[i], val + 0.8),
                       fontsize=9, ha='center', color='#616161',
                       fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close()
        print(f"[OK] PESTEL雷达图已生成: {output_path}")
        return output_path

    def generate_risk_matrix(self, output_path: str):
        """生成外部风险评估矩阵图"""
        if not self.external_issues:
            print("[SKIP] 无外部风险数据，跳过风险矩阵生成")
            return None
            
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # 定义风险等级颜色
        risk_colors = {
            '重大风险': '#D32F2F',
            '高风险': '#F57C00',
            '中风险': '#FBC02D',
            '低风险': '#388E3C',
            '可接受': '#7B1FA2'
        }
        
        # 绘制背景格子
        colors_grid = [
            ['#FFCDD2', '#FFCDD2', '#FFF9C4'],  # 高可能性行
            ['#FFCDD2', '#FFF9C4', '#C8E6C9'],  # 中可能性行
            ['#FFF9C4', '#C8E6C9', '#C8E6C9']   # 低可能性行
        ]
        
        likelihoods = ['高', '中', '低']
        impacts = ['低', '中', '高']
        
        for i, likelihood in enumerate(likelihoods):
            for j, impact in enumerate(impacts):
                rect = plt.Rectangle((j, 2-i), 1, 1, 
                                     facecolor=colors_grid[i][j],
                                     edgecolor='white', linewidth=2)
                ax.add_patch(rect)
        
        # 绘制风险点
        for issue in self.external_issues:
            likelihood = issue.get('likelihood', '中')
            impact = issue.get('impact', '中')
            
            x_map = {'低': 0.3, '中': 1.3, '高': 2.3}
            y_map = {'高': 2.3, '中': 1.3, '低': 0.3}
            
            if likelihood in x_map and impact in y_map:
                circle = plt.Circle((x_map[likelihood], y_map[impact]), 0.2,
                                    facecolor=self.pestel_colors.get('economic', '#1976D2'),
                                    edgecolor='white', linewidth=2, alpha=0.8)
                ax.add_patch(circle)
                
                # 添加标签（截断过长文本）
                issue_text = issue.get('issue', '')[:15] + '...' if len(issue.get('issue', '')) > 15 else issue.get('issue', '')
                ax.text(x_map[likelihood], y_map[impact], f'{len(issue_text)//5}',
                       fontsize=8, ha='center', va='center', color='white', fontweight='bold')
        
        # 设置轴
        ax.set_xlim(-0.2, 3.2)
        ax.set_ylim(-0.2, 3.2)
        ax.set_xticks([0.5, 1.5, 2.5])
        ax.set_xticklabels(['低', '中', '高'], fontsize=12)
        ax.set_yticks([0.5, 1.5, 2.5])
        ax.set_yticklabels(['低', '中', '高'], fontsize=12)
        
        ax.set_xlabel('影响程度 (Impact)', fontsize=12, fontweight='bold', labelpad=10)
        ax.set_ylabel('可能性 (Likelihood)', fontsize=12, fontweight='bold', labelpad=10)
        
        # 标题
        ax.set_title(f'{self.org_name}\n外部风险评估矩阵', 
                    fontsize=16, fontweight='bold', pad=15)
        
        # 添加图例
        legend_elements = [mpatches.Patch(facecolor=color, label=risk)
                          for risk, color in risk_colors.items()]
        ax.legend(handles=legend_elements, loc='upper right', 
                 bbox_to_anchor=(1.35, 1.0), fontsize=9, title='风险等级')
        
        # 添加网格线
        ax.grid(True, linestyle='--', alpha=0.3)
        ax.set_axisbelow(True)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close()
        print(f"[OK] 风险矩阵图已生成: {output_path}")
        return output_path

    def generate_report(self, output_path: str, charts_dir: str):
        """生成PDF分析报告"""
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=2*cm, leftMargin=2*cm,
            topMargin=2*cm, bottomMargin=2*cm
        )
        
        styles = getSampleStyleSheet()
        
        # 自定义样式
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=22,
            textColor=colors.HexColor('#1565C0'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#424242'),
            spaceBefore=15,
            spaceAfter=10,
            fontName='Helvetica-Bold'
        )
        
        subheading_style = ParagraphStyle(
            'CustomSubHeading',
            parent=styles['Heading3'],
            fontSize=11,
            textColor=colors.HexColor('#616161'),
            spaceBefore=10,
            spaceAfter=6,
            fontName='Helvetica-Bold'
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#424242'),
            spaceBefore=4,
            spaceAfter=4,
            leading=14,
            alignment=TA_JUSTIFY
        )
        
        story = []
        
        # 封面
        story.append(Spacer(1, 5*cm))
        story.append(Paragraph(self.org_name, title_style))
        story.append(Paragraph("QMS环境因素分析报告", title_style))
        story.append(Spacer(1, 2*cm))
        story.append(Paragraph(f"分析日期: {self.analysis_date}", body_style))
        story.append(Paragraph(f"报告类型: 年度环境因素分析", body_style))
        story.append(Paragraph("适用标准: ISO 9001:2015 第4.1条", body_style))
        story.append(PageBreak())
        
        # 目录提示
        story.append(Paragraph("目录", heading_style))
        story.append(Paragraph("1. 执行摘要", body_style))
        story.append(Paragraph("2. SWOT分析", body_style))
        story.append(Paragraph("3. PESTEL分析", body_style))
        story.append(Paragraph("4. 关键问题与风险", body_style))
        story.append(Paragraph("5. 改进建议", body_style))
        story.append(PageBreak())
        
        # 1. 执行摘要
        story.append(Paragraph("1. 执行摘要", heading_style))
        summary = f"""
        本报告对{self.org_name}的内部和外部环境因素进行了系统分析，
        旨在支持质量管理体系（QMS）的战略决策与持续改进。
        """
        story.append(Paragraph(summary.strip(), body_style))
        
        # 统计摘要
        s_count = len(self.swot.get('strengths', []))
        w_count = len(self.swot.get('weaknesses', []))
        o_count = len(self.swot.get('opportunities', []))
        t_count = len(self.swot.get('threats', []))
        story.append(Spacer(1, 0.3*cm))
        
        stats_data = [
            ['SWOT维度', '因素数量', 'PESTEL维度', '因素数量'],
            [f'Strengths(优势)', s_count, 'Political(政治)', len(self.pestel.get('political', []))],
            [f'Weaknesses(劣势)', w_count, 'Economic(经济)', len(self.pestel.get('economic', []))],
            [f'Opportunities(机遇)', o_count, 'Social(社会)', len(self.pestel.get('social', []))],
            [f'Threats(威胁)', t_count, 'Technological(技术)', len(self.pestel.get('technological', []))],
            ['', '', 'Environmental(环境)', len(self.pestel.get('environmental', []))],
            ['', '', 'Legal(法律)', len(self.pestel.get('legal', []))],
        ]
        
        stats_table = Table(stats_data, colWidths=[4*cm, 2.5*cm, 4*cm, 2.5*cm])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1565C0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F5F5F5')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDBDBD')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#EEEEEE')]),
        ]))
        story.append(stats_table)
        story.append(PageBreak())
        
        # 2. SWOT分析
        story.append(Paragraph("2. SWOT分析", heading_style))
        
        # 插入SWOT图
        swot_chart_path = os.path.join(charts_dir, 'swot_matrix.png')
        if os.path.exists(swot_chart_path):
            story.append(Image(swot_chart_path, width=15*cm, height=13*cm))
            story.append(Spacer(1, 0.5*cm))
        
        # SWOT详细列表
        story.append(Paragraph("2.1 优势 (Strengths)", subheading_style))
        for i, item in enumerate(self.swot.get('strengths', []), 1):
            story.append(Paragraph(f"{i}. {item}", body_style))
        
        story.append(Paragraph("2.2 劣势 (Weaknesses)", subheading_style))
        for i, item in enumerate(self.swot.get('weaknesses', []), 1):
            story.append(Paragraph(f"{i}. {item}", body_style))
        
        story.append(Paragraph("2.3 机遇 (Opportunities)", subheading_style))
        for i, item in enumerate(self.swot.get('opportunities', []), 1):
            story.append(Paragraph(f"{i}. {item}", body_style))
        
        story.append(Paragraph("2.4 威胁 (Threats)", subheading_style))
        for i, item in enumerate(self.swot.get('threats', []), 1):
            story.append(Paragraph(f"{i}. {item}", body_style))
        
        story.append(PageBreak())
        
        # 3. PESTEL分析
        story.append(Paragraph("3. PESTEL外部环境分析", heading_style))
        
        # 插入PESTEL雷达图
        pestel_chart_path = os.path.join(charts_dir, 'pestel_radar.png')
        if os.path.exists(pestel_chart_path):
            story.append(Image(pestel_chart_path, width=13*cm, height=11*cm))
            story.append(Spacer(1, 0.5*cm))
        
        pestel_dimensions = [
            ('political', 'Political - 政治因素'),
            ('economic', 'Economic - 经济因素'),
            ('social', 'Social - 社会因素'),
            ('technological', 'Technological - 技术因素'),
            ('environmental', 'Environmental - 环境因素'),
            ('legal', 'Legal - 法律因素'),
        ]
        
        for key, title in pestel_dimensions:
            story.append(Paragraph(title, subheading_style))
            items = self.pestel.get(key, [])
            if items:
                for i, item in enumerate(items, 1):
                    story.append(Paragraph(f"{i}. {item}", body_style))
            else:
                story.append(Paragraph("（待分析补充）", body_style))
        
        story.append(PageBreak())
        
        # 4. 关键问题与风险
        story.append(Paragraph("4. 关键问题与风险", heading_style))
        
        # 内部问题
        if self.internal_issues:
            story.append(Paragraph("4.1 内部关键问题", subheading_style))
            
            internal_data = [['维度', '问题描述', '严重程度', '改进建议']]
            for issue in self.internal_issues:
                internal_data.append([
                    issue.get('dimension', ''),
                    issue.get('issue', ''),
                    issue.get('severity', ''),
                    issue.get('suggestion', '')
                ])
            
            internal_table = Table(internal_data, colWidths=[2.5*cm, 5*cm, 2*cm, 4.5*cm])
            internal_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E7D32')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDBDBD')),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
            ]))
            story.append(internal_table)
            story.append(Spacer(1, 0.5*cm))
        
        # 外部风险
        if self.external_issues:
            story.append(Paragraph("4.2 外部风险评估", subheading_style))
            
            # 插入风险矩阵
            risk_chart_path = os.path.join(charts_dir, 'risk_matrix.png')
            if os.path.exists(risk_chart_path):
                story.append(Image(risk_chart_path, width=12*cm, height=10*cm))
                story.append(Spacer(1, 0.3*cm))
            
            external_data = [['维度', '风险描述', '可能性', '影响', '应对措施']]
            for issue in self.external_issues:
                external_data.append([
                    issue.get('dimension', ''),
                    issue.get('issue', ''),
                    issue.get('likelihood', ''),
                    issue.get('impact', ''),
                    issue.get('suggestion', '')
                ])
            
            external_table = Table(external_data, colWidths=[2*cm, 4*cm, 1.5*cm, 1.5*cm, 5*cm])
            external_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#EF6C00')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDBDBD')),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
            ]))
            story.append(external_table)
        
        story.append(PageBreak())
        
        # 5. 改进建议
        story.append(Paragraph("5. 改进建议与行动计划", heading_style))
        story.append(Paragraph("5.1 战略建议", subheading_style))
        
        # 基于分析生成建议
        if self.swot.get('weaknesses'):
            story.append(Paragraph("针对劣势的改进方向：", body_style))
            for i, w in enumerate(self.swot.get('weaknesses', [])[:3], 1):
                story.append(Paragraph(f"  • 建立{w}的改进机制", body_style))
        
        if self.swot.get('threats'):
            story.append(Paragraph("应对威胁的策略：", body_style))
            for i, t in enumerate(self.swot.get('threats', [])[:3], 1):
                story.append(Paragraph(f"  • 制定应对{t}的风险预案", body_style))
        
        if self.swot.get('opportunities'):
            story.append(Paragraph("把握机遇的行动：", body_style))
            for i, o in enumerate(self.swot.get('opportunities', [])[:3], 1):
                story.append(Paragraph(f"  • 制定利用{o}的发展计划", body_style))
        
        story.append(Paragraph("5.2 下一步工作", subheading_style))
        next_steps = [
            "将本报告提交管理评审会议审议",
            "根据审议意见更新质量目标和改进计划",
            "在内审中重点关注内部问题项的改进效果",
            "定期跟踪外部环境变化，及时更新风险清单"
        ]
        for step in next_steps:
            story.append(Paragraph(f"• {step}", body_style))
        
        # 页脚
        story.append(Spacer(1, 1*cm))
        story.append(Paragraph(f"-- 报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')} --", 
                              ParagraphStyle('Footer', parent=body_style, 
                                           alignment=TA_CENTER, fontSize=8,
                                           textColor=colors.HexColor('#9E9E9E'))))
        
        # 生成PDF
        doc.build(story)
        print(f"[OK] 分析报告已生成: {output_path}")
        return output_path


def main():
    parser = argparse.ArgumentParser(
        description='QMS环境因素分析工具 - 生成可视化图表和PDF报告'
    )
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    # 可视化命令
    visualize_parser = subparsers.add_parser('visualize', help='生成可视化图表')
    visualize_parser.add_argument('--data', required=True, help='JSON数据文件路径')
    visualize_parser.add_argument('--output', default='./output', help='输出目录')
    
    # 报告命令
    report_parser = subparsers.add_parser('report', help='生成PDF分析报告')
    report_parser.add_argument('--data', required=True, help='JSON数据文件路径')
    report_parser.add_argument('--output', default='./output', help='输出目录')
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    # 确保输出目录存在
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    analyzer = QMSAnalyzer(args.data)
    
    if args.command == 'visualize':
        swot_path = output_dir / 'swot_matrix.png'
        pestel_path = output_dir / 'pestel_radar.png'
        risk_path = output_dir / 'risk_matrix.png'
        
        analyzer.generate_swot_matrix(str(swot_path))
        analyzer.generate_pestel_radar(str(pestel_path))
        analyzer.generate_risk_matrix(str(risk_path))
        
        print(f"\n[SUCCESS] 可视化图表已生成到: {output_dir}")
        
    elif args.command == 'report':
        report_path = output_dir / 'qms_environment_report.pdf'
        
        # 先生成图表
        charts_dir = output_dir / 'charts'
        charts_dir.mkdir(parents=True, exist_ok=True)
        
        analyzer.generate_swot_matrix(str(charts_dir / 'swot_matrix.png'))
        analyzer.generate_pestel_radar(str(charts_dir / 'pestel_radar.png'))
        analyzer.generate_risk_matrix(str(charts_dir / 'risk_matrix.png'))
        
        # 生成报告
        analyzer.generate_report(str(report_path), str(charts_dir))
        
        print(f"\n[SUCCESS] 分析报告已生成: {report_path}")


if __name__ == '__main__':
    main()
