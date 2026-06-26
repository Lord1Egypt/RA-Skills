"""
SPC 报告生成器 - 生成 PDF 格式的 SPC 研究报告
支持控制图报告、能力分析报告
"""

import io
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['font.sans-serif'] = ['STHeiti', 'PingFang SC', 'Arial Unicode MS', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

import matplotlib.pyplot as plt
import numpy as np


# ==================== 中文字体支持 ====================

_CHINESE_FONT_REGISTERED = False

def register_chinese_font():
    """注册中文字体"""
    global _CHINESE_FONT_REGISTERED
    
    if _CHINESE_FONT_REGISTERED:
        return True
    
    font_paths = [
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/PingFang.ttc",
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont('Chinese', font_path))
                _CHINESE_FONT_REGISTERED = True
                return True
            except Exception:
                continue
    
    return False


# ==================== 样式定义 ====================

def create_styles():
    """创建 PDF 样式"""
    register_chinese_font()
    
    styles = getSampleStyleSheet()
    
    styles.add(ParagraphStyle(
        name='ChineseHeading1',
        parent=styles['Heading1'],
        fontName='Chinese',
        fontSize=18,
        spaceAfter=12,
        alignment=1,
    ))
    
    styles.add(ParagraphStyle(
        name='ChineseHeading2',
        parent=styles['Heading2'],
        fontName='Chinese',
        fontSize=14,
        spaceAfter=10,
        spaceBefore=8,
    ))
    
    styles.add(ParagraphStyle(
        name='ChineseBody',
        parent=styles['Normal'],
        fontName='Chinese',
        fontSize=10,
        spaceAfter=6,
        leading=14,
    ))
    
    styles.add(ParagraphStyle(
        name='ChineseSmall',
        parent=styles['Normal'],
        fontName='Chinese',
        fontSize=8,
        spaceAfter=4,
        textColor=colors.gray,
    ))
    
    return styles


# ==================== 控制图图表 ====================

def create_control_chart(
    data: np.ndarray,
    subgroup_size: int = 5,
    chart_type: str = 'Xbar-R'
) -> io.BytesIO:
    """创建控制图"""
    n_subgroups = len(data) // subgroup_size
    subgroups = data[:n_subgroups * subgroup_size].reshape(n_subgroups, subgroup_size)
    
    if chart_type == 'Xbar-R':
        fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
        fig.suptitle(f'{chart_type} 控制图', fontsize=14, fontweight='bold')
        
        # 计算子组统计量
        xbar = np.mean(subgroups, axis=1)
        r = np.ptp(subgroups, axis=1)  # 极差
        
        # 控制限计算
        xbar_bar = np.mean(xbar)
        r_bar = np.mean(r)
        
        # A2, D3, D4 系数（n=5）
        A2, D3, D4 = 0.577, 0, 2.114
        
        ucl_xbar = xbar_bar + A2 * r_bar
        lcl_xbar = xbar_bar - A2 * r_bar
        
        ucl_r = D4 * r_bar
        lcl_r = D3 * r_bar
        
        # Xbar 图
        ax1 = axes[0]
        ax1.plot(range(1, n_subgroups+1), xbar, 'b-o', markersize=4, label='Xbar')
        ax1.axhline(y=xbar_bar, color='green', linestyle='-', linewidth=2, label=f'CL={xbar_bar:.4f}')
        ax1.axhline(y=ucl_xbar, color='red', linestyle='--', linewidth=2, label=f'UCL={ucl_xbar:.4f}')
        ax1.axhline(y=lcl_xbar, color='red', linestyle='--', linewidth=2, label=f'LCL={lcl_xbar:.4f}')
        ax1.set_ylabel('平均值')
        ax1.set_title('Xbar 图 (均值控制图)')
        ax1.legend(loc='upper right', fontsize=8)
        ax1.grid(True, alpha=0.3)
        
        # R 图
        ax2 = axes[1]
        ax2.plot(range(1, n_subgroups+1), r, 'b-o', markersize=4, label='R')
        ax2.axhline(y=r_bar, color='green', linestyle='-', linewidth=2, label=f'CL={r_bar:.4f}')
        ax2.axhline(y=ucl_r, color='red', linestyle='--', linewidth=2, label=f'UCL={ucl_r:.4f}')
        ax2.axhline(y=lcl_r, color='red', linestyle='--', linewidth=2, label=f'LCL={lcl_r:.4f}')
        ax2.set_xlabel('子组编号')
        ax2.set_ylabel('极差')
        ax2.set_title('R 图 (极差控制图)')
        ax2.legend(loc='upper right', fontsize=8)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
    
    elif chart_type == 'I-MR':
        fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
        fig.suptitle(f'{chart_type} 控制图', fontsize=14, fontweight='bold')
        
        # 计算移动极差
        mr = np.abs(np.diff(data))
        
        # 控制限计算
        x_bar = np.mean(data)
        mr_bar = np.mean(mr)
        
        E2, D4 = 2.66, 3.267
        
        ucl_x = x_bar + E2 * mr_bar
        lcl_x = x_bar - E2 * mr_bar
        
        ucl_mr = D4 * mr_bar
        
        # I 图
        ax1 = axes[0]
        ax1.plot(range(1, len(data)+1), data, 'b-o', markersize=3, label='I')
        ax1.axhline(y=x_bar, color='green', linestyle='-', linewidth=2, label=f'CL={x_bar:.4f}')
        ax1.axhline(y=ucl_x, color='red', linestyle='--', linewidth=2, label=f'UCL={ucl_x:.4f}')
        ax1.axhline(y=lcl_x, color='red', linestyle='--', linewidth=2, label=f'LCL={lcl_x:.4f}')
        ax1.set_ylabel('测量值')
        ax1.set_title('I 图 (单值控制图)')
        ax1.legend(loc='upper right', fontsize=8)
        ax1.grid(True, alpha=0.3)
        
        # MR 图
        ax2 = axes[1]
        ax2.plot(range(1, len(mr)+1), mr, 'b-o', markersize=3, label='MR')
        ax2.axhline(y=mr_bar, color='green', linestyle='-', linewidth=2, label=f'CL={mr_bar:.4f}')
        ax2.axhline(y=ucl_mr, color='red', linestyle='--', linewidth=2, label=f'UCL={ucl_mr:.4f}')
        ax2.axhline(y=0, color='red', linestyle='--', linewidth=2, label='LCL=0')
        ax2.set_xlabel('观测值编号')
        ax2.set_ylabel('移动极差')
        ax2.set_title('MR 图 (移动极差控制图)')
        ax2.legend(loc='upper right', fontsize=8)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    
    return buf


# ==================== 能力分析图表 ====================

def create_capability_chart(
    data: np.ndarray,
    usl: float,
    lsl: float,
    cpk: float
) -> io.BytesIO:
    """创建能力分析图表"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('过程能力分析', fontsize=14, fontweight='bold')
    
    # 1. 直方图 + 正态曲线
    ax1 = axes[0]
    n, bins, patches = ax1.hist(data, bins=20, density=True, alpha=0.7, edgecolor='black')
    
    # 正态分布曲线
    mu, sigma = np.mean(data), np.std(data)
    x = np.linspace(lsl, usl, 100)
    from scipy import stats
    ax1.plot(x, stats.norm.pdf(x, mu, sigma), 'r-', linewidth=2, label='正态拟合')
    
    ax1.axvline(x=mu, color='red', linestyle='--', linewidth=2, label=f'μ={mu:.4f}')
    ax1.axvline(x=usl, color='red', linestyle='-', linewidth=2, label=f'USL={usl}')
    ax1.axvline(x=lsl, color='red', linestyle='-', linewidth=2, label=f'LSL={lsl}')
    ax1.set_xlabel('测量值')
    ax1.set_ylabel('密度')
    ax1.set_title('数据分布')
    ax1.legend(fontsize=8)
    ax1.grid(True, alpha=0.3)
    
    # 2. 能力指数对比图
    ax2 = axes[1]
    
    # 计算其他指数
    cpu = (usl - mu) / (3 * sigma)
    cpl = (mu - lsl) / (3 * sigma)
    cp = (usl - lsl) / (6 * sigma)
    
    metrics = ['Cp', 'Cpu', 'Cpl', 'Cpk']
    values = [cp, cpu, cpl, cpk]
    colors_bar = ['#FF6B6B' if v < 1.33 else '#FFD93D' if v < 1.67 else '#6BCB77' for v in values]
    
    bars = ax2.bar(metrics, values, color=colors_bar)
    ax2.set_ylabel('能力指数')
    ax2.set_title('能力指数对比')
    ax2.axhline(y=1.33, color='orange', linestyle='--', alpha=0.5, label='最低要求 (1.33)')
    ax2.axhline(y=1.67, color='green', linestyle='--', alpha=0.5, label='优秀 (1.67)')
    ax2.legend(fontsize=8)
    ax2.set_ylim(0, max(2.5, max(values) * 1.3))
    
    # 添加数值标签
    for bar, val in zip(bars, values):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, 
                f'{val:.2f}', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    
    return buf


# ==================== 表格构建 ====================

def _create_table(data, col_widths, styles):
    """创建表格的辅助函数"""
    table = Table(data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Chinese'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    return table


def create_control_chart_result_table(
    chart_type: str,
    n_subgroups: int,
    subgroup_size: int,
    control_limits: Dict[str, float],
    violations: List[str]
) -> Table:
    """创建控制图结果表"""
    data = [
        ['控制图类型', chart_type],
        ['子组数量', str(n_subgroups)],
        ['子组大小', str(subgroup_size)],
        ['中心线 (CL)', f"{control_limits.get('cl', 0):.4f}"],
        ['上控制限 (UCL)', f"{control_limits.get('ucl', 0):.4f}"],
        ['下控制限 (LCL)', f"{control_limits.get('lcl', 0):.4f}"],
        ['判异规则触发', ', '.join(violations) if violations else '无'],
        ['过程状态', '受控' if not violations else '失控 - 需要调查'],
    ]
    
    return _create_table(data, [5*cm, 7*cm], getSampleStyleSheet())


def create_capability_result_table(
    capability_indices: Dict[str, float],
    specification: Dict[str, float]
) -> Table:
    """创建能力指数结果表"""
    cpk = capability_indices.get('cpk', 0)
    
    if cpk >= 2.0:
        rating = '六西格玛水平'
        action = '保持，可放宽控制'
    elif cpk >= 1.67:
        rating = '优秀'
        action = '维持现状'
    elif cpk >= 1.33:
        rating = '良好'
        action = '维持，持续改进'
    elif cpk >= 1.0:
        rating = '边缘'
        action = '需要改进计划'
    else:
        rating = '不足'
        action = '必须改进，100% 检验'
    
    data = [
        ['规格上限 (USL)', f"{specification.get('usl', 0):.4f}"],
        ['规格下限 (LSL)', f"{specification.get('lsl', 0):.4f}"],
        ['目标值', f"{specification.get('target', 0):.4f}"],
        ['', ''],
        ['Cp', f"{capability_indices.get('cp', 0):.4f}"],
        ['Cpu', f"{capability_indices.get('cpu', 0):.4f}"],
        ['Cpl', f"{capability_indices.get('cpl', 0):.4f}"],
        ['Cpk', f"{cpk:.4f}"],
        ['Pp', f"{capability_indices.get('pp', 0):.4f}"],
        ['Ppk', f"{capability_indices.get('ppk', 0):.4f}"],
        ['', ''],
        ['评级', rating],
        ['行动建议', action],
    ]
    
    return _create_table(data, [5*cm, 7*cm], getSampleStyleSheet())


# ==================== 主生成函数 ====================

def generate_spc_control_chart_pdf(
    study_info: Dict[str, Any],
    data: np.ndarray,
    chart_type: str = 'Xbar-R',
    subgroup_size: int = 5,
    control_limits: Optional[Dict[str, float]] = None,
    violations: Optional[List[str]] = None
) -> bytes:
    """生成控制图 PDF 报告"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
        title=f"SPC Control Chart Report - {study_info.get('characteristic_name', 'N/A')}"
    )
    
    styles = create_styles()
    story = []
    
    # 标题
    story.append(Paragraph("SPC 控制图分析报告", styles['ChineseHeading1']))
    story.append(Spacer(1, 0.3*inch))
    
    # 基本信息
    info_data = [
        ['质量特性', study_info.get('characteristic_name', 'N/A')],
        ['产品', study_info.get('product_name', 'N/A')],
        ['过程', study_info.get('process_name', 'N/A')],
        ['控制图类型', chart_type],
        ['数据量', f"{len(data)} 个测量值 ({len(data)//subgroup_size} 子组 × {subgroup_size})"],
        ['生成日期', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
    ]
    
    info_table = _create_table(info_data, [4*cm, 9*cm], styles)
    story.append(info_table)
    story.append(Spacer(1, 0.3*inch))
    
    # 控制图结果
    story.append(Paragraph("1. 控制图分析结果", styles['ChineseHeading2']))
    story.append(Spacer(1, 0.15*inch))
    
    if control_limits is None:
        control_limits = {'cl': np.mean(data), 'ucl': np.mean(data) + 3*np.std(data), 'lcl': np.mean(data) - 3*np.std(data)}
    if violations is None:
        violations = []
    
    story.append(create_control_chart_result_table(
        chart_type, len(data)//subgroup_size, subgroup_size, control_limits, violations
    ))
    story.append(Spacer(1, 0.3*inch))
    
    # 控制图
    story.append(Paragraph("2. 控制图", styles['ChineseHeading2']))
    story.append(Spacer(1, 0.15*inch))
    
    chart_buf = create_control_chart(data, subgroup_size, chart_type)
    chart_buf.seek(0)
    chart_img = Image(chart_buf, width=6.5*inch, height=5*inch)
    story.append(chart_img)
    story.append(Spacer(1, 0.3*inch))
    
    # 页脚
    story.append(PageBreak())
    story.append(Paragraph(
        f"<i>本报告由 SPC/MSA 系统自动生成 | 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>",
        style=styles['ChineseSmall']
    ))
    
    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes


def generate_spc_capability_pdf(
    study_info: Dict[str, Any],
    data: np.ndarray,
    specification: Dict[str, float],
    capability_indices: Dict[str, float]
) -> bytes:
    """生成过程能力分析报告 PDF"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
        title=f"SPC Capability Report - {study_info.get('characteristic_name', 'N/A')}"
    )
    
    styles = create_styles()
    story = []
    
    # 标题
    story.append(Paragraph("SPC 过程能力分析报告", styles['ChineseHeading1']))
    story.append(Spacer(1, 0.3*inch))
    
    # 基本信息
    info_data = [
        ['质量特性', study_info.get('characteristic_name', 'N/A')],
        ['产品', study_info.get('product_name', 'N/A')],
        ['过程', study_info.get('process_name', 'N/A')],
        ['样本量', str(len(data))],
        ['均值', f"{np.mean(data):.4f}"],
        ['标准差', f"{np.std(data, ddof=1):.4f}"],
        ['生成日期', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
    ]
    
    info_table = _create_table(info_data, [4*cm, 9*cm], styles)
    story.append(info_table)
    story.append(Spacer(1, 0.3*inch))
    
    # 能力分析结果
    story.append(Paragraph("1. 过程能力指数", styles['ChineseHeading2']))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(create_capability_result_table(capability_indices, specification))
    story.append(Spacer(1, 0.3*inch))
    
    # 能力分析图表
    story.append(Paragraph("2. 能力分析图表", styles['ChineseHeading2']))
    story.append(Spacer(1, 0.15*inch))
    
    chart_buf = create_capability_chart(
        data,
        specification.get('usl', np.mean(data) + 3*np.std(data)),
        specification.get('lsl', np.mean(data) - 3*np.std(data)),
        capability_indices.get('cpk', 0)
    )
    chart_buf.seek(0)
    chart_img = Image(chart_buf, width=6.5*inch, height=4.5*inch)
    story.append(chart_img)
    story.append(Spacer(1, 0.3*inch))
    
    # 正态性检验
    from scipy import stats
    shapiro_stat, shapiro_p = stats.shapiro(data[:5000])  # Shapiro 最多 5000 样本
    
    story.append(Paragraph("3. 正态性检验", styles['ChineseHeading2']))
    story.append(Spacer(1, 0.15*inch))
    
    normality_data = [
        ['检验方法', 'Shapiro-Wilk'],
        ['统计量 W', f"{shapiro_stat:.4f}"],
        ['p 值', f"{shapiro_p:.4f}"],
        ['结论', '数据服从正态分布' if shapiro_p > 0.05 else '数据不服从正态分布 (p<0.05)'],
    ]
    
    story.append(_create_table(normality_data, [5*cm, 7*cm], styles))
    story.append(Spacer(1, 0.3*inch))
    
    # 页脚
    story.append(PageBreak())
    story.append(Paragraph(
        f"<i>本报告由 SPC/MSA 系统自动生成 | 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>",
        style=styles['ChineseSmall']
    ))
    
    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes
