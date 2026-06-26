#!/usr/bin/env python3
"""
AIAG-VDA SPC Yellow Volume Unified Report Generator
AIAG-VDA SPC 黄皮书统一报告生成器
"""

import io
import os
import numpy as np
from datetime import datetime
from typing import Dict, Optional
from dataclasses import dataclass

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['axes.unicode_minus'] = False
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import Circle
from scipy import stats

# 注册中文字体
FONT_PATHS = [
    'C:/Windows/Fonts/msyh.ttc',  # 微软雅黑
    'C:/Windows/Fonts/simhei.ttf',  # 黑体
    'C:/Windows/Fonts/simsun.ttc',  # 宋体
    '/System/Library/Fonts/STHeiti Light.ttc',
    '/System/Library/Fonts/PingFang.ttc',
]
_chinese_font_path = None
for fp in FONT_PATHS:
    if os.path.exists(fp):
        _chinese_font_path = fp
        try:
            pdfmetrics.registerFont(TTFont('Chinese', fp, validate=False))
        except:
            pass
        break

_font_prop = fm.FontProperties(fname=_chinese_font_path) if _chinese_font_path else None

# 颜色
COLORS = {
    'primary': '#1F4E79',
    'secondary': '#2E75B6',
    'accent': '#00B050',
    'warning': '#FF0000',
    'light_gray': '#F2F2F2',
}

# 文本
TEXTS = {
    'zh': {
        'title': 'SPC 过程能力研究报告',
        'subtitle': 'AIAG / VDA SPC 统一标准',
        'process_name': '过程名称',
        'machine_name': '设备名称',
        'study_location': '研究地点',
        'study_date': '研究日期',
        'part_name_id': '零件名称及编号',
        'characteristic_name_id': '特性名称及编号',
        'study_remarks': '研究备注',
        'sample_size': '样本量',
        'subgroup_size': '子组大小',
        'histogram': '直方图',
        'raw_value_chart': '原始值图',
        'probability_plot': '概率图',
        'xbar_s_chart': 'Xbar-S 控制图',
        'x50_percent': 'X50%',
        'spread': '展宽',
        'distribution_model': '分布模型',
        'capability_requirement': '能力要求',
        'conclusion': '结论',
        'measurement_value': '测量值',
        'frequency': '频数',
        'subgroup': '子组',
        'expected_normal': '期望正态值',
        'ordered_data': '有序数据',
        'ppm_upper': 'PPM > USL',
        'ppm_lower': 'PPM < LSL',
        'ci_95': '95% 置信区间',
        'geometric_method': '几何法',
        'normal': '正态',
        'non_normal': '非正态',
    },
    'en': {
        'title': 'SPC Process Capability Study Report',
        'subtitle': 'AIAG / VDA SPC Harmonized Standard',
        'process_name': 'Process Name',
        'machine_name': 'Machine Name',
        'study_location': 'Study Location',
        'study_date': 'Study Date',
        'part_name_id': 'Part Name & ID',
        'characteristic_name_id': 'Characteristic Name & ID',
        'study_remarks': 'Study Remarks',
        'sample_size': 'Sample Size',
        'subgroup_size': 'Subgroup Size',
        'histogram': 'Histogram',
        'raw_value_chart': 'Raw Value Chart',
        'probability_plot': 'Probability Plot',
        'xbar_s_chart': 'Xbar-S Chart',
        'x50_percent': 'X50%',
        'spread': 'Spread',
        'distribution_model': 'Distribution Model',
        'capability_requirement': 'Capability Requirement',
        'conclusion': 'Conclusion',
        'measurement_value': 'Measurement Value',
        'frequency': 'Frequency',
        'subgroup': 'Subgroup',
        'expected_normal': 'Expected Normal Value',
        'ordered_data': 'Ordered Data',
        'ppm_upper': 'PPM > USL',
        'ppm_lower': 'PPM < LSL',
        'ci_95': '95% CI',
        'geometric_method': 'Geometric Method',
        'normal': 'Normal',
        'non_normal': 'Non-Normal',
    }
}


@dataclass
class StudyInfo:
    process_name: str = ""
    machine_name: str = ""
    study_location: str = ""
    study_date: str = ""
    part_name: str = ""
    part_id: str = ""
    characteristic_name: str = ""
    study_remarks: str = "Capability Study"
    subgroup_size: int = 5


@dataclass
class Specification:
    usl: float
    lsl: float
    target: Optional[float] = None


def _get_font(lang: str):
    return _font_prop if lang == 'zh' else None


def create_histogram(data, spec, lang):
    fig, ax = plt.subplots(figsize=(5.5, 3.5), dpi=150)
    ax.hist(data, bins=30, color=COLORS['accent'], edgecolor='white', alpha=0.7)
    ax.axvline(x=spec.usl, color=COLORS['warning'], linewidth=1.5, label=f"USL={spec.usl:.4f}")
    ax.axvline(x=spec.lsl, color=COLORS['warning'], linewidth=1.5, label=f"LSL={spec.lsl:.4f}")
    if spec.target:
        ax.axvline(x=spec.target, color=COLORS['secondary'], linestyle='--', linewidth=1)
    ax.axvline(x=np.median(data), color=COLORS['primary'], linestyle=':', linewidth=1.5)
    t = TEXTS[lang]
    ax.set_xlabel(t['measurement_value'], fontsize=8, fontproperties=_get_font(lang))
    ax.set_ylabel(t['frequency'], fontsize=8, fontproperties=_get_font(lang))
    ax.set_title(t['histogram'], fontsize=9, fontweight='bold', fontproperties=_get_font(lang))
    ax.legend(fontsize=6)
    ax.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    return buf


def create_raw_chart(data, spec, lang):
    fig, ax = plt.subplots(figsize=(7, 3), dpi=150)
    ax.scatter(range(len(data)), data, s=4, c=COLORS['accent'], alpha=0.6, marker='.')
    ax.axhline(y=spec.usl, color=COLORS['warning'], linewidth=1, label=f"USL={spec.usl:.4f}")
    ax.axhline(y=spec.lsl, color=COLORS['warning'], linewidth=1, label=f"LSL={spec.lsl:.4f}")
    ax.axhline(y=np.mean(data), color=COLORS['secondary'], linestyle='--', linewidth=1)
    t = TEXTS[lang]
    ax.set_xlabel('Value No.', fontsize=8, fontproperties=_get_font(lang))
    ax.set_ylabel(t['measurement_value'], fontsize=8, fontproperties=_get_font(lang))
    ax.set_title(t['raw_value_chart'], fontsize=9, fontweight='bold', fontproperties=_get_font(lang))
    ax.legend(fontsize=6)
    ax.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    return buf


def create_probability_plot(data, lang):
    fig, ax = plt.subplots(figsize=(4, 3.5), dpi=150)
    (osm, osr), (slope, intercept, r) = stats.probplot(data, dist="norm", fit=True)
    ax.scatter(osm, osr, s=6, c=COLORS['accent'], marker='.')
    ax.plot(osm, slope * osm + intercept, color=COLORS['warning'], linewidth=1.5)
    t = TEXTS[lang]
    ax.set_xlabel(t['expected_normal'], fontsize=8, fontproperties=_get_font(lang))
    ax.set_ylabel(t['ordered_data'], fontsize=8, fontproperties=_get_font(lang))
    ax.set_title(t['probability_plot'], fontsize=9, fontweight='bold', fontproperties=_get_font(lang))
    ax.text(0.05, 0.95, f"R² = {r**2:.4f}", transform=ax.transAxes, fontsize=7)
    ax.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    return buf


def create_xbar_s_chart(data, subgroup_size, lang):
    n_subgroups = len(data) // subgroup_size
    if n_subgroups < 2:
        fig, ax = plt.subplots(figsize=(7, 3))
        ax.text(0.5, 0.5, "Insufficient data", ha='center', va='center')
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close(fig)
        return buf
    
    subgroups = data[:n_subgroups * subgroup_size].reshape(n_subgroups, subgroup_size)
    xbar = np.mean(subgroups, axis=1)
    s = np.std(subgroups, axis=1, ddof=1)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 4.5), sharex=True, dpi=150)
    
    xbar_bar, s_bar = np.mean(xbar), np.mean(s)
    A3, B3, B4 = 1.427, 0, 2.089
    
    ax1.plot(range(len(xbar)), xbar, 'g-', linewidth=0.8, marker='.', markersize=4)
    ax1.axhline(y=xbar_bar, color=COLORS['secondary'], linewidth=1.5, label='CL')
    ax1.axhline(y=xbar_bar + A3 * s_bar, color=COLORS['warning'], linestyle='--', linewidth=1, label='UCL')
    ax1.axhline(y=xbar_bar - A3 * s_bar, color=COLORS['warning'], linestyle='--', linewidth=1, label='LCL')
    ax1.set_ylabel('Xbar', fontsize=8, fontproperties=_get_font(lang))
    ax1.set_title('Xbar-S Chart', fontsize=9, fontweight='bold', fontproperties=_get_font(lang))
    ax1.legend(fontsize=6)
    ax1.grid(True, linestyle='--', alpha=0.3)
    
    ax2.plot(range(len(s)), s, 'g-', linewidth=0.8, marker='.', markersize=4)
    ax2.axhline(y=s_bar, color=COLORS['secondary'], linewidth=1.5, label='CL')
    ax2.axhline(y=B4 * s_bar, color=COLORS['warning'], linestyle='--', linewidth=1, label='UCL')
    ax2.set_xlabel(TEXTS[lang]['subgroup'], fontsize=8, fontproperties=_get_font(lang))
    ax2.set_ylabel('S', fontsize=8, fontproperties=_get_font(lang))
    ax2.legend(fontsize=6)
    ax2.grid(True, linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    return buf


def calculate_stats(data, spec):
    n = len(data)
    mean, std = np.mean(data), np.std(data, ddof=1)
    x_0_135 = np.percentile(data, 0.135)
    x_50 = np.percentile(data, 50)
    x_99_865 = np.percentile(data, 99.865)
    spread = x_99_865 - x_0_135
    
    cp_g = (spec.usl - spec.lsl) / spread if spread > 0 else 999
    cpu_g = (spec.usl - x_50) / (spread / 2) if spread > 0 else 999
    cpl_g = (x_50 - spec.lsl) / (spread / 2) if spread > 0 else 999
    cpk_g = min(cpu_g, cpl_g)
    
    cpk_se = np.sqrt((1 / (9 * n)) * (1 + cpk_g**2 / 2))
    cpk_lcl = max(0, cpk_g - 1.96 * cpk_se)
    cpk_ucl = cpk_g + 1.96 * cpk_se
    
    ppm_upper = (1 - stats.norm.cdf(spec.usl, mean, std)) * 1e6
    ppm_lower = stats.norm.cdf(spec.lsl, mean, std) * 1e6
    
    status = 'PASS' if cpk_g >= 1.33 else 'MARGINAL' if cpk_g >= 1.0 else 'FAIL'
    
    return {
        'n': n, 'mean': mean, 'std': std,
        'x_50': x_50, 'spread': spread,
        'cp_g': cp_g, 'cpk_g': cpk_g,
        'cpk_lcl': cpk_lcl, 'cpk_ucl': cpk_ucl,
        'ppm_upper': ppm_upper, 'ppm_lower': ppm_lower,
        'status': status,
    }


class AIAGVDAReportGenerator:
    def __init__(self, lang='en'):
        self.lang = lang
        self.texts = TEXTS.get(lang, TEXTS['en'])
        self.styles = self._create_styles()
    
    def _create_styles(self):
        styles = getSampleStyleSheet()
        font_name = 'Chinese' if self.lang == 'zh' else 'Helvetica'
        return {
            'title': ParagraphStyle('Title', parent=styles['Heading1'], fontSize=14, fontName=font_name),
            'header': ParagraphStyle('Header', fontSize=9, fontName=font_name, textColor=colors.HexColor(COLORS['primary'])),
            'normal': ParagraphStyle('Normal', fontSize=9, fontName=font_name),
            'small': ParagraphStyle('Small', fontSize=7, textColor=colors.grey, fontName=font_name),
        }
    
    def _p(self, text):
        """创建 Paragraph (支持中文)"""
        return Paragraph(text, self.styles['normal'])
    
    def generate_figure12_1(self, output_path, data, spec, study_info=None):
        if study_info is None:
            study_info = StudyInfo()
        
        stats = calculate_stats(data, spec)
        doc = SimpleDocTemplate(output_path, pagesize=A4, 
                               rightMargin=1*cm, leftMargin=1*cm, topMargin=1*cm, bottomMargin=1*cm)
        story = []
        t = self.texts
        
        # 标题
        story.append(Paragraph(f'<b>{t["title"]}</b>', self.styles['title']))
        story.append(Paragraph(t['subtitle'], self.styles['small']))
        story.append(Spacer(1, 6))
        
        # 行 1-3
        row1 = Table([[self._p(f"{t['process_name']}: {study_info.process_name or 'Process X'}"),
                       self._p(f"{t['machine_name']}: {study_info.machine_name or 'Machine A'}"),
                       self._p(f"{t['study_location']}: {study_info.study_location or 'Site A'}")]], 
                     colWidths=[160, 160, 150])
        row1.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, colors.black), ('FONTSIZE', (0, 0), (-1, -1), 8),
                                  ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(COLORS['light_gray']))]))
        story.append(row1)
        
        # 行 4-6
        row2 = Table([[self._p(f"{t['study_date']}: {study_info.study_date or datetime.now().strftime('%Y-%m-%d')}"),
                       self._p(f"{t['part_name_id']}: {study_info.part_name or 'Part A'}"),
                       self._p(f"{t['characteristic_name_id']}: {study_info.characteristic_name or 'Dim'}")]], 
                     colWidths=[160, 160, 150])
        row2.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, colors.black), ('FONTSIZE', (0, 0), (-1, -1), 8)]))
        story.append(row2)
        
        # 行 7-10
        row3 = Table([[self._p(f"{t['study_remarks']}: {study_info.study_remarks}"),
                       self._p(f"{t['sample_size']} = {stats['n']}, {t['subgroup_size']} = {study_info.subgroup_size}")]], 
                     colWidths=[320, 150])
        row3.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, colors.black), ('FONTSIZE', (0, 0), (-1, -1), 8),
                                  ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(COLORS['light_gray']))]))
        story.append(row3)
        story.append(Spacer(1, 6))
        
        # 图表
        hist_img = Image(create_histogram(data, spec, self.lang), width=230, height=145)
        raw_img = Image(create_raw_chart(data, spec, self.lang), width=240, height=100)
        charts1 = Table([[self._p(f"11. {t['histogram']}"), self._p(f"12. {t['raw_value_chart']}")], [hist_img, raw_img]], 
                        colWidths=[240, 240])
        charts1.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, colors.black), ('FONTSIZE', (0, 0), (-1, 0), 8),
                                     ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(COLORS['light_gray']))]))
        story.append(charts1)
        
        prob_img = Image(create_probability_plot(data, self.lang), width=200, height=145)
        xbar_img = Image(create_xbar_s_chart(data, study_info.subgroup_size, self.lang), width=280, height=180)
        charts2 = Table([[self._p(f"13. {t['probability_plot']}"), self._p(f"14. {t['xbar_s_chart']}")], [prob_img, xbar_img]], 
                        colWidths=[200, 280])
        charts2.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, colors.black), ('FONTSIZE', (0, 0), (-1, 0), 8),
                                     ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(COLORS['light_gray']))]))
        story.append(charts2)
        story.append(Spacer(1, 6))
        
        # 行 15-17
        row4 = Table([[self._p(f"15. {t['x50_percent']} = {stats['x_50']:.6f}"),
                       self._p(f"16. {t['spread']} = {stats['spread']:.6f}"),
                       self._p(f"17. {t['distribution_model']}: {t['normal']}")]], 
                     colWidths=[160, 160, 160])
        row4.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, colors.black), ('FONTSIZE', (0, 0), (-1, -1), 8),
                                  ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(COLORS['light_gray']))]))
        story.append(row4)
        
        # 行 18
        row5 = Table([[self._p(f"18. {t['capability_requirement']}: Cp,G = {stats['cp_g']:.2f}, Cpk,G = {stats['cpk_g']:.2f} [{stats['status']}] ({t['geometric_method']})")]], 
                     colWidths=[480])
        row5.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, colors.black), ('FONTSIZE', (0, 0), (-1, -1), 9)]))
        story.append(row5)
        
        # 行 19
        row6 = Table([[self._p(f"19. Cpk: [{stats['cpk_lcl']:.2f}, {stats['cpk_ucl']:.2f}] {t['ci_95']} | {t['ppm_upper']} = {stats['ppm_upper']:.1f}, {t['ppm_lower']} = {stats['ppm_lower']:.1f}")]], 
                     colWidths=[480])
        row6.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, colors.black), ('FONTSIZE', (0, 0), (-1, -1), 8)]))
        story.append(row6)
        
        # 行 20
        conclusion = "Requirements met" if stats['status'] == 'PASS' else "Process needs improvement"
        row7 = Table([[self._p(f"20. {t['conclusion']}: {conclusion}")]], colWidths=[480])
        row7.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, colors.black), ('FONTSIZE', (0, 0), (-1, -1), 9),
                                  ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(COLORS['light_gray']))]))
        story.append(row7)
        
        doc.build(story)
        return output_path

    def generate_figure12_2(self, output_path, data, spec, study_info=None):
        """Figure 12-2: 非正态/混合分布报告 (22个元素)"""
        if study_info is None:
            study_info = StudyInfo()
        
        stats = calculate_stats(data, spec)
        doc = SimpleDocTemplate(output_path, pagesize=A4, 
                               rightMargin=1*cm, leftMargin=1*cm, topMargin=1*cm, bottomMargin=1*cm)
        story = []
        t = self.texts
        
        story.append(Paragraph(f'<b>{t["title"]} - {t["non_normal"]}</b>', self.styles['title']))
        story.append(Paragraph(t['subtitle'], self.styles['small']))
        story.append(Spacer(1, 6))
        
        row1 = Table([[self._p(f"{t['process_name']}: {study_info.process_name or 'Process X'}"),
                       self._p(f"{t['machine_name']}: {study_info.machine_name or 'Machine A'}"),
                       self._p(f"{t['study_location']}: {study_info.study_location or 'Site A'}")]], colWidths=[160, 160, 150])
        row1.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, colors.black), ('FONTSIZE', (0, 0), (-1, -1), 8), ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(COLORS['light_gray']))]))
        story.append(row1)
        
        row2 = Table([[self._p(f"{t['study_date']}: {study_info.study_date or datetime.now().strftime('%Y-%m-%d')}"),
                       self._p(f"{t['part_name_id']}: {study_info.part_name or 'Part A'}"),
                       self._p(f"{t['characteristic_name_id']}: {study_info.characteristic_name or 'Dim'}")]], colWidths=[160, 160, 150])
        row2.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, colors.black), ('FONTSIZE', (0, 0), (-1, -1), 8)]))
        story.append(row2)
        
        row3 = Table([[self._p(f"{t['study_remarks']}: {study_info.study_remarks} (Non-Normal)"),
                       self._p(f"{t['sample_size']} = {stats['n']}, {t['subgroup_size']} = {study_info.subgroup_size}")]], colWidths=[320, 150])
        row3.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, colors.black), ('FONTSIZE', (0, 0), (-1, -1), 8), ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(COLORS['light_gray']))]))
        story.append(row3)
        story.append(Spacer(1, 6))
        
        hist_img = Image(create_histogram(data, spec, self.lang), width=230, height=145)
        raw_img = Image(create_raw_chart(data, spec, self.lang), width=240, height=100)
        charts1 = Table([[self._p(f"11. {t['histogram']}"), self._p(f"12. {t['raw_value_chart']}")], [hist_img, raw_img]], colWidths=[240, 240])
        charts1.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, colors.black), ('FONTSIZE', (0, 0), (-1, 0), 8), ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(COLORS['light_gray']))]))
        story.append(charts1)
        
        prob_img = Image(create_probability_plot(data, self.lang), width=200, height=145)
        xbar_img = Image(create_xbar_s_chart(data, study_info.subgroup_size, self.lang), width=280, height=180)
        charts2 = Table([[self._p(f"13. {t['probability_plot']}"), self._p(f"14. {t['xbar_s_chart']}")], [prob_img, xbar_img]], colWidths=[200, 280])
        charts2.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, colors.black), ('FONTSIZE', (0, 0), (-1, 0), 8), ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(COLORS['light_gray']))]))
        story.append(charts2)
        story.append(Spacer(1, 6))
        
        row4 = Table([[self._p(f"15. {t['x50_percent']} = {stats['x_50']:.6f}"),
                       self._p(f"16. {t['spread']} = {stats['spread']:.6f}"),
                       self._p(f"17. {t['distribution_model']}: Mixed (C4)")]], colWidths=[160, 160, 160])
        row4.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, colors.black), ('FONTSIZE', (0, 0), (-1, -1), 8), ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(COLORS['light_gray']))]))
        story.append(row4)
        
        row5 = Table([[self._p(f"18. {t['capability_requirement']}: Cp,G = {stats['cp_g']:.2f}, Cpk,G = {stats['cpk_g']:.2f} [{stats['status']}] ({t['geometric_method']})")]], colWidths=[480])
        row5.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, colors.black), ('FONTSIZE', (0, 0), (-1, -1), 9)]))
        story.append(row5)
        
        row6 = Table([[self._p(f"19. Cpk: [{stats['cpk_lcl']:.2f}, {stats['cpk_ucl']:.2f}] {t['ci_95']} | {t['ppm_upper']} = {stats['ppm_upper']:.1f}, {t['ppm_lower']} = {stats['ppm_lower']:.1f}")]], colWidths=[480])
        row6.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, colors.black), ('FONTSIZE', (0, 0), (-1, -1), 8)]))
        story.append(row6)
        
        conclusion = "Requirements met" if stats['status'] == 'PASS' else "Process needs improvement"
        row7 = Table([[self._p(f"20. {t['conclusion']}: {conclusion}")]], colWidths=[480])
        row7.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, colors.black), ('FONTSIZE', (0, 0), (-1, -1), 9), ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(COLORS['light_gray']))]))
        story.append(row7)
        
        row8 = Table([[self._p(f"21. Time Dependent Distribution Model: Mixed Distribution (C4)")]], colWidths=[480])
        row8.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, colors.black), ('FONTSIZE', (0, 0), (-1, -1), 8)]))
        story.append(row8)
        
        guard_band = stats['std'] * 0.1
        row9 = Table([[self._p(f"22. Measurement Uncertainty: ±{guard_band:.4f} | Guard Band: {guard_band:.4f}")]], colWidths=[480])
        row9.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, colors.black), ('FONTSIZE', (0, 0), (-1, -1), 8), ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(COLORS['light_gray']))]))
        story.append(row9)
        
        doc.build(story)
        return output_path

    def generate_figure12_3(self, output_path, data, spec, study_info=None):
        """Figure 12-3: 标准统计表格格式"""
        if study_info is None:
            study_info = StudyInfo()
        
        stats = calculate_stats(data, spec)
        doc = SimpleDocTemplate(output_path, pagesize=A4, 
                               rightMargin=1*cm, leftMargin=1*cm, topMargin=1*cm, bottomMargin=1*cm)
        story = []
        t = self.texts
        
        story.append(Paragraph(f'<b>{t["title"]} - Standard Format</b>', self.styles['title']))
        story.append(Paragraph(t['subtitle'], self.styles['small']))
        story.append(Spacer(1, 6))
        
        row1 = Table([[self._p(f"1. {t['process_name']}: {study_info.process_name or 'Process X'}"),
                       self._p(f"2. {t['machine_name']}: {study_info.machine_name or 'Machine A'}"),
                       self._p(f"3. {t['study_location']}: {study_info.study_location or 'Site A'}")]], colWidths=[160, 160, 150])
        row1.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, colors.black), ('FONTSIZE', (0, 0), (-1, -1), 8)]))
        story.append(row1)
        
        row2 = Table([[self._p(f"4. {t['study_date']}: {study_info.study_date or datetime.now().strftime('%Y-%m-%d')}"),
                       self._p(f"5. {t['part_name_id']}: {study_info.part_name or 'Part A'}"),
                       self._p(f"6. {t['characteristic_name_id']}: {study_info.characteristic_name or 'Dim'}")]], colWidths=[160, 160, 150])
        row2.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, colors.black), ('FONTSIZE', (0, 0), (-1, -1), 8)]))
        story.append(row2)
        
        row3 = Table([[self._p(f"7-10. {t['sample_size']}={stats['n']}, {t['subgroup_size']}={study_info.subgroup_size}, {study_info.study_remarks}")]], colWidths=[470])
        row3.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, colors.black), ('FONTSIZE', (0, 0), (-1, -1), 8)]))
        story.append(row3)
        story.append(Spacer(1, 6))
        
        stat_header = [self._p('<b>Drawing Values</b>'), self._p('<b>Collected Values</b>'), self._p('<b>Statistical Values</b>')]
        stat_data = [
            [self._p('USL'), self._p(f'{spec.usl:.6f}'), self._p(f'Mean (X̄): {stats["mean"]:.6f}')],
            [self._p('LSL'), self._p(f'{spec.lsl:.6f}'), self._p(f'Std Dev (σ): {stats["std"]:.6f}')],
            [self._p('Target'), self._p(f'{spec.target:.6f}' if spec.target else 'N/A'), self._p(f'Median: {stats["x_50"]:.6f}')],
            [self._p('Tolerance'), self._p(f'{spec.usl - spec.lsl:.6f}'), self._p(f'Range: {np.max(data) - np.min(data):.6f}')],
            [self._p('Unit'), self._p('mm'), self._p(f'n: {stats["n"]}')],
        ]
        stat_table = Table([stat_header] + stat_data, colWidths=[150, 150, 170])
        stat_table.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, colors.black), ('FONTSIZE', (0, 0), (-1, -1), 8), ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(COLORS['primary'])), ('TEXTCOLOR', (0, 0), (-1, 0), colors.white), ('ALIGN', (0, 0), (-1, -1), 'CENTER')]))
        story.append(stat_table)
        story.append(Spacer(1, 6))
        
        hist_img = Image(create_histogram(data, spec, self.lang), width=230, height=145)
        raw_img = Image(create_raw_chart(data, spec, self.lang), width=240, height=100)
        charts1 = Table([[self._p(f"11. {t['histogram']}"), self._p(f"12. {t['raw_value_chart']}")], [hist_img, raw_img]], colWidths=[240, 240])
        charts1.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, colors.black), ('FONTSIZE', (0, 0), (-1, 0), 8), ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(COLORS['light_gray']))]))
        story.append(charts1)
        
        prob_img = Image(create_probability_plot(data, self.lang), width=200, height=145)
        xbar_img = Image(create_xbar_s_chart(data, study_info.subgroup_size, self.lang), width=280, height=180)
        charts2 = Table([[self._p(f"13. {t['probability_plot']}"), self._p(f"14. {t['xbar_s_chart']}")], [prob_img, xbar_img]], colWidths=[200, 280])
        charts2.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, colors.black), ('FONTSIZE', (0, 0), (-1, 0), 8), ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(COLORS['light_gray']))]))
        story.append(charts2)
        story.append(Spacer(1, 6))
        
        cap_header = [self._p('<b>Index</b>'), self._p('<b>Value</b>'), self._p('<b>95% CI</b>'), self._p('<b>Status</b>')]
        cap_data = [
            [self._p('Cp,G'), self._p(f'{stats["cp_g"]:.3f}'), self._p('-'), self._p('PASS' if stats['cp_g'] >= 1.33 else 'FAIL')],
            [self._p('Cpk,G'), self._p(f'{stats["cpk_g"]:.3f}'), self._p(f'[{stats["cpk_lcl"]:.2f}, {stats["cpk_ucl"]:.2f}]'), self._p(stats['status'])],
        ]
        cap_table = Table([cap_header] + cap_data, colWidths=[100, 100, 150, 120])
        cap_table.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, colors.black), ('FONTSIZE', (0, 0), (-1, -1), 8), ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(COLORS['primary'])), ('TEXTCOLOR', (0, 0), (-1, 0), colors.white), ('ALIGN', (0, 0), (-1, -1), 'CENTER')]))
        story.append(cap_table)
        story.append(Spacer(1, 6))
        
        ppm_row = Table([[self._p(f"{t['ppm_upper']}: {stats['ppm_upper']:.1f}"), self._p(f"{t['ppm_lower']}: {stats['ppm_lower']:.1f}"), self._p(f"PPM Total: {stats['ppm_upper'] + stats['ppm_lower']:.1f}")]], colWidths=[160, 160, 150])
        ppm_row.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, colors.black), ('FONTSIZE', (0, 0), (-1, -1), 8)]))
        story.append(ppm_row)
        
        conclusion = "Requirements met" if stats['status'] == 'PASS' else "Process needs improvement"
        conc_row = Table([[self._p(f"{t['conclusion']}: {conclusion}")]], colWidths=[470])
        conc_row.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, colors.black), ('FONTSIZE', (0, 0), (-1, -1), 9), ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(COLORS['light_gray']))]))
        story.append(conc_row)
        
        doc.build(story)
        return output_path


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='AIAG-VDA Report Generator')
    parser.add_argument('-o', '--output', default='report.pdf')
    parser.add_argument('-l', '--lang', choices=['zh', 'en'], default='zh')
    parser.add_argument('-f', '--figure', choices=['12-1', '12-2', '12-3'], default='12-1')
    args = parser.parse_args()
    
    np.random.seed(42)
    data = np.random.normal(130.0392, 0.033, 875)
    spec = Specification(usl=130.15, lsl=129.95, target=130.05)
    
    gen = AIAGVDAReportGenerator(lang=args.lang)
    if args.figure == '12-1':
        gen.generate_figure12_1(args.output, data, spec)
    elif args.figure == '12-2':
        gen.generate_figure12_2(args.output, data, spec)
    elif args.figure == '12-3':
        gen.generate_figure12_3(args.output, data, spec)
    print(f'Generated: {args.output}')