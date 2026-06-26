"""
MSA 报告生成器 - 生成 PDF 格式的 MSA 研究报告
支持 GR&R、偏倚、线性研究报告
"""

import io
import os
from datetime import datetime
from typing import Dict, Any, Optional

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
matplotlib.use('Agg')  # 非交互式后端

# 配置 matplotlib 中文字体
matplotlib.rcParams['font.sans-serif'] = ['STHeiti', 'PingFang SC', 'Arial Unicode MS', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

import matplotlib.pyplot as plt
import numpy as np


# ==================== 中文字体支持 ====================

# 全局字体注册标志
_CHINESE_FONT_REGISTERED = False

def register_chinese_font():
    """注册中文字体"""
    global _CHINESE_FONT_REGISTERED
    
    if _CHINESE_FONT_REGISTERED:
        return True
    
    # 尝试使用系统字体
    font_paths = [
        "/System/Library/Fonts/STHeiti Light.ttc",  # macOS
        "/System/Library/Fonts/STHeiti Medium.ttc",  # macOS
        "/System/Library/Fonts/PingFang.ttc",  # macOS
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",  # Linux
        "C:\\Windows\\Fonts\\simhei.ttf",  # Windows
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont('Chinese', font_path))
                _CHINESE_FONT_REGISTERED = True
                return True
            except Exception as e:
                print(f"字体注册失败 {font_path}: {e}")
                continue
    
    return False


# ==================== 样式定义 ====================

def create_styles():
    """创建 PDF 样式"""
    # 注册中文字体
    register_chinese_font()
    
    styles = getSampleStyleSheet()
    
    # 标题样式
    styles.add(ParagraphStyle(
        name='ChineseHeading1',
        parent=styles['Heading1'],
        fontName='Chinese',
        fontSize=18,
        spaceAfter=12,
        alignment=1,  # 居中
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
        name='ChineseHeading3',
        parent=styles['Heading3'],
        fontName='Chinese',
        fontSize=12,
        spaceAfter=6,
        spaceBefore=6,
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


# ==================== 图表生成 ====================

def create_grr_chart(
    data_array: np.ndarray,
    grr_result: Dict[str, float],
    evaluation: Dict[str, Any]
) -> io.BytesIO:
    """创建 GR&R 控制图"""
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    fig.suptitle('GR&R 分析图表', fontsize=14, fontweight='bold')
    
    n_parts, n_operators, n_trials = data_array.shape
    
    # 1. 零件平均值图 (Xbar Chart by Part)
    ax1 = axes[0, 0]
    part_means = data_array.mean(axis=(1, 2))
    part_std = data_array.std(axis=(1, 2))
    x_parts = range(1, n_parts + 1)
    ax1.errorbar(x_parts, part_means, yerr=part_std, fmt='o-', capsize=5)
    ax1.set_xlabel('零件编号')
    ax1.set_ylabel('平均值')
    ax1.set_title('零件平均值')
    ax1.grid(True, alpha=0.3)
    
    # 2. 操作者箱线图
    ax2 = axes[0, 1]
    operator_data = [data_array[:, i, :].flatten() for i in range(n_operators)]
    bp = ax2.boxplot(operator_data, labels=[f'Op{i+1}' for i in range(n_operators)])
    ax2.set_ylabel('测量值')
    ax2.set_title('操作者分布')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # 3. 变差分量饼图
    ax3 = axes[1, 0]
    labels = ['重复性 (EV)', '再现性 (AV)', '零件变差 (PV)']
    sizes = [grr_result['ev'], grr_result['av'], grr_result['pv']]
    colors_pie = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    ax3.pie(sizes, labels=labels, colors=colors_pie, autopct='%1.1f%%')
    ax3.set_title('变差分量分布')
    
    # 4. %GRR 柱状图
    ax4 = axes[1, 1]
    metrics = ['%GRR', '%EV', '%AV', '%PV']
    values = [
        evaluation['percent_grr'],
        evaluation['percent_ev'],
        evaluation['percent_av'],
        evaluation['percent_pv']
    ]
    bar_colors = ['#FF6B6B' if v > 30 else '#FFD93D' if v > 10 else '#6BCB77' for v in values]
    bars = ax4.bar(metrics, values, color=bar_colors)
    ax4.set_ylabel('百分比 (%)')
    ax4.set_title('变差百分比')
    ax4.axhline(y=10, color='green', linestyle='--', alpha=0.5, label='可接受限')
    ax4.axhline(y=30, color='red', linestyle='--', alpha=0.5, label='拒绝限')
    ax4.legend()
    ax4.set_ylim(0, max(100, max(values) * 1.2))
    
    # 添加数值标签
    for bar, val in zip(bars, values):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                f'{val:.1f}%', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    
    return buf


def create_bias_chart(
    measurements: list,
    reference_value: float,
    bias_result: Dict[str, float]
) -> io.BytesIO:
    """创建偏倚分析图表"""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle('偏倚分析图表', fontsize=14, fontweight='bold')
    
    # 1. 测量值分布图
    ax1 = axes[0]
    ax1.hist(measurements, bins=10, edgecolor='black', alpha=0.7)
    ax1.axvline(x=reference_value, color='red', linestyle='--', linewidth=2, 
                label=f'参考值：{reference_value:.4f}')
    ax1.axvline(x=np.mean(measurements), color='blue', linestyle='-', linewidth=2,
                label=f'平均值：{np.mean(measurements):.4f}')
    ax1.set_xlabel('测量值')
    ax1.set_ylabel('频数')
    ax1.set_title('测量值分布')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. 偏倚置信区间图
    ax2 = axes[1]
    bias = bias_result['bias']
    ci = bias_result.get('confidence_interval', [bias - 0.01, bias + 0.01])
    
    y_pos = 1
    ax2.errorbar(bias, y_pos, xerr=[[bias - ci[0]], [ci[1] - bias]], 
                fmt='o', capsize=10, markersize=12)
    ax2.axvline(x=0, color='red', linestyle='--', linewidth=2, label='零偏倚')
    ax2.set_xlabel('偏倚值')
    ax2.set_yticks([])
    ax2.set_title(f'偏倚置信区间 (t={bias_result.get("t_statistic", 0):.3f})')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 添加统计信息文本
    stats_text = f"Bias: {bias:.4f}\nt-statistic: {bias_result.get('t_statistic', 0):.3f}\np-value: {bias_result.get('p_value', 0):.4f}"
    ax2.text(0.05, 0.95, stats_text, transform=ax2.transAxes, fontsize=9,
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    
    return buf


def create_linearity_chart(
    reference_values: np.ndarray,
    measurements: np.ndarray,
    linearity_result: Dict[str, float]
) -> io.BytesIO:
    """创建线性分析图表"""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle('线性分析图表', fontsize=14, fontweight='bold')
    
    # 1. 散点图 + 回归线
    ax1 = axes[0]
    ax1.scatter(reference_values, measurements, s=100, alpha=0.7, label='测量数据')
    
    # 回归线
    x_line = np.linspace(reference_values.min(), reference_values.max(), 100)
    y_line = linearity_result['slope'] * x_line + linearity_result['intercept']
    ax1.plot(x_line, y_line, 'r-', linewidth=2, label='回归线')
    
    # 理想线 (y=x)
    ax1.plot(x_line, x_line, 'g--', alpha=0.5, label='理想线性')
    
    ax1.set_xlabel('参考值')
    ax1.set_ylabel('测量平均值')
    ax1.set_title('线性回归分析')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 添加 R²
    ax1.text(0.05, 0.95, f'R² = {linearity_result["r_squared"]:.4f}', 
             transform=ax1.transAxes, fontsize=11,
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # 2. 残差图
    ax2 = axes[1]
    residuals = measurements - (linearity_result['slope'] * reference_values + linearity_result['intercept'])
    ax2.scatter(reference_values, residuals, s=100, alpha=0.7)
    ax2.axhline(y=0, color='red', linestyle='--', linewidth=2)
    ax2.set_xlabel('参考值')
    ax2.set_ylabel('残差')
    ax2.set_title('残差分析')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    
    return buf


# ==================== PDF 内容构建 ====================

def create_header_table(study_info: Dict[str, Any]) -> Table:
    """创建报告头部信息表"""
    data = [
        ['MSA 研究报告', ''],
        ['报告编号', f"MSA-{study_info.get('id', 'N/A')}-{datetime.now().strftime('%Y%m%d')}"],
        ['研究类型', study_info.get('study_type', 'N/A')],
        ['研究名称', study_info.get('study_name', 'N/A')],
        ['质量特性', study_info.get('quality_characteristic', 'N/A')],
        ['生成日期', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
    ]
    
    table = Table(data, colWidths=[4*cm, 10*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Chinese'),
        ('FONTSIZE', (0, 0), (1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (1, 0), 12),
        ('BACKGROUND', (0, 1), (1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
    ]))
    
    return table


def create_grr_result_table(grr_result: Dict[str, float], evaluation: Dict[str, Any]) -> Table:
    """创建 GR&R 结果表"""
    data = [
        ['变差分量', '数值', '百分比'],
        ['重复性 (EV)', f"{grr_result['ev']:.6f}", f"{evaluation['percent_ev']:.2f}%"],
        ['再现性 (AV)', f"{grr_result['av']:.6f}", f"{evaluation['percent_av']:.2f}%"],
        ['GR&R (RR)', f"{grr_result['rr']:.6f}", f"{evaluation['percent_grr']:.2f}%"],
        ['零件变差 (PV)', f"{grr_result['pv']:.6f}", f"{evaluation['percent_pv']:.2f}%"],
        ['总变差 (TV)', f"{grr_result['tv']:.6f}", '100%'],
        ['', '', ''],
        ['评估指标', '', ''],
        ['ndc (分级数)', f"{evaluation.get('ndc', 'N/A')}", ''],
        ['接受状态', evaluation.get('acceptance', 'N/A'), ''],
    ]
    
    return _create_table(data, [5*cm, 4*cm, 4*cm])


def create_grr_raw_data_table(data_array: np.ndarray) -> Table:
    """创建 GR&R 原始数据表"""
    n_parts, n_operators, n_trials = data_array.shape
    
    # 构建表头
    header = ['零件', '操作者'] + [f'第{i+1}次' for i in range(n_trials)] + ['平均值', '极差']
    data = [header]
    
    # 添加数据行
    for i in range(n_parts):
        for j in range(n_operators):
            row = [f'零件{i+1}', f'操作者{j+1}']
            values = [data_array[i, j, k] for k in range(n_trials)]
            row.extend([f'{v:.4f}' for v in values])
            row.append(f'{np.mean(values):.4f}')
            row.append(f'{max(values) - min(values):.4f}')
            data.append(row)
    
    # 列宽
    col_widths = [2*cm, 2*cm] + [1.5*cm] * n_trials + [1.5*cm, 1.5*cm]
    
    return _create_table(data, col_widths)


def create_bias_raw_data_table(measurements: list, reference_value: float) -> Table:
    """创建偏倚研究原始数据表"""
    data = [
        ['序号', '测量值', '偏倚 (测量值 - 参考值)'],
    ]
    
    for i, val in enumerate(measurements):
        bias = val - reference_value
        data.append([str(i+1), f'{val:.4f}', f'{bias:+.4f}'])
    
    # 添加统计行
    mean_val = np.mean(measurements)
    std_val = np.std(measurements, ddof=1)
    data.append([
        '统计',
        f'平均值={mean_val:.4f}\n标准差={std_val:.4f}',
        f'平均偏倚={mean_val - reference_value:.4f}'
    ])
    
    return _create_table(data, [2*cm, 4*cm, 5*cm])


def create_linearity_raw_data_table(reference_values: np.ndarray, measurements: np.ndarray) -> Table:
    """创建线性研究原始数据表"""
    data = [
        ['零件编号', '参考值', '测量值', '偏倚 (测量值 - 参考值)'],
    ]
    
    for i, (ref, meas) in enumerate(zip(reference_values, measurements)):
        bias = meas - ref
        data.append([str(i+1), f'{ref:.4f}', f'{meas:.4f}', f'{bias:+.4f}'])
    
    return _create_table(data, [2*cm, 3*cm, 3*cm, 4*cm])


def _create_table(data, col_widths):
    """创建表格的辅助函数"""
    table = Table(data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Chinese'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    return table
    
    table = Table(data, colWidths=[5*cm, 4*cm, 4*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Chinese'),
        ('FONTNAME', (0, 1), (-1, -1), 'Chinese'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, 6), colors.beige),
        ('BACKGROUND', (0, 7), (-1, -1), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
    ]))
    
    return table


def create_bias_result_table(bias_result: Dict[str, float]) -> Table:
    """创建偏倚结果表"""
    data = [
        ['统计量', '数值'],
        ['参考值', f"{bias_result.get('reference_value', 'N/A'):.4f}"],
        ['测量次数', str(bias_result.get('n_measurements', 0))],
        ['偏倚 (Bias)', f"{bias_result.get('bias', 0):.6f}"],
        ['偏倚百分比', f"{bias_result.get('bias_percent', 0):.2f}%"],
        ['t 统计量', f"{bias_result.get('t_statistic', 0):.3f}"],
        ['p 值', f"{bias_result.get('p_value', 0):.4f}"],
        ['显著性', '是' if bias_result.get('is_significant', False) else '否'],
        ['置信区间下限', f"{bias_result.get('ci_lower', 0):.6f}"],
        ['置信区间上限', f"{bias_result.get('ci_upper', 0):.6f}"],
    ]
    
    table = Table(data, colWidths=[7*cm, 6*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Chinese'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
    ]))
    
    return table


def create_linearity_result_table(linearity_result: Dict[str, float]) -> Table:
    """创建线性结果表"""
    data = [
        ['统计量', '数值'],
        ['斜率 (Slope)', f"{linearity_result.get('slope', 0):.6f}"],
        ['截距 (Intercept)', f"{linearity_result.get('intercept', 0):.6f}"],
        ['R 平方', f"{linearity_result.get('r_squared', 0):.4f}"],
        ['斜率 p 值', f"{linearity_result.get('p_value_slope', 0):.4f}"],
        ['截距 p 值', f"{linearity_result.get('p_value_intercept', 0):.4f}"],
        ['线性度', f"{linearity_result.get('linearity', 0):.6f}"],
        ['线性度百分比', f"{linearity_result.get('linearity_percent', 0):.2f}%"],
        ['线性接受状态', '接受' if linearity_result.get('is_linear', False) else '拒绝'],
    ]
    
    table = Table(data, colWidths=[7*cm, 6*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Chinese'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
    ]))
    
    return table


def create_footer(styles) -> Paragraph:
    """创建页脚"""
    return Paragraph(
        f"<i>本报告由 SPC/MSA 系统自动生成 | 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>",
        style=styles['ChineseSmall']
    )


# ==================== 主生成函数 ====================

def generate_msa_pdf(
    study_type: str,
    study_info: Dict[str, Any],
    results: Dict[str, Any],
    chart_data: Optional[Dict[str, Any]] = None
) -> bytes:
    """
    生成 MSA PDF 报告
    
    Args:
        study_type: 研究类型 (GRR, BIAS, LINEARITY)
        study_info: 研究基本信息
        results: 分析结果
        chart_data: 图表数据（可选）
    
    Returns:
        PDF 文件的字节数据
    """
    # 创建 PDF 文档
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
        title=f"MSA Report - {study_info.get('study_name', 'N/A')}"
    )
    
    # 创建样式
    styles = create_styles()
    
    # 构建内容
    story = []
    
    # 标题
    story.append(Paragraph("MSA 研究报告", styles['ChineseHeading1']))
    story.append(Spacer(1, 0.3*inch))
    
    # 头部信息表
    story.append(create_header_table(study_info))
    story.append(Spacer(1, 0.3*inch))
    
    # 根据研究类型添加内容
    if study_type == 'GRR':
        story.append(Paragraph("1. GR&R 分析结果", styles['ChineseHeading2']))
        story.append(Spacer(1, 0.2*inch))
        
        grr_result = results.get('grr_error', {})
        evaluation = results.get('evaluation', {})
        
        # 结果表
        story.append(create_grr_result_table(grr_result, evaluation))
        story.append(Spacer(1, 0.3*inch))
        
        # 评估说明
        acceptance = evaluation.get('acceptance', 'N/A')
        ndc = evaluation.get('ndc', 0)
        
        if acceptance == 'acceptable':
            eval_text = "✅ <b>测量系统可接受</b>：%%GRR ≤ 10%，测量系统满足要求。"
        elif acceptance == 'conditionally_acceptable':
            eval_text = "⚠️ <b>测量系统条件接受</b>：10% < %GRR ≤ 30%，可根据应用重要性、量具成本、维修成本等因素决定是否接受。"
        else:
            eval_text = "❌ <b>测量系统不可接受</b>：%GRR > 30%，需要改进测量系统。"
        
        story.append(Paragraph(eval_text, styles['ChineseBody']))
        story.append(Paragraph(f"<b>ndc (分级数):</b> {ndc} - {'≥5，满足要求' if ndc >= 5 else '<5，建议改进'}", styles['ChineseBody']))
        story.append(Spacer(1, 0.3*inch))
        
        # 原始数据
        if chart_data and 'data_array' in chart_data:
            story.append(Paragraph("2. 原始测量数据", styles['ChineseHeading2']))
            story.append(Spacer(1, 0.15*inch))
            story.append(create_grr_raw_data_table(chart_data['data_array']))
            story.append(Spacer(1, 0.3*inch))
        
        # 图表
        if chart_data and 'data_array' in chart_data:
            story.append(Paragraph("3. 分析图表", styles['ChineseHeading2']))
            story.append(Spacer(1, 0.2*inch))
            
            chart_buf = create_grr_chart(
                chart_data['data_array'],
                grr_result,
                evaluation
            )
            chart_buf.seek(0)
            chart_img = Image(chart_buf, width=6*inch, height=4.5*inch)
            story.append(chart_img)
            story.append(Spacer(1, 0.3*inch))
    
    elif study_type == 'BIAS':
        story.append(Paragraph("1. 偏倚分析结果", styles['ChineseHeading2']))
        story.append(Spacer(1, 0.2*inch))
        
        bias_result = results.get('bias_result', {})
        story.append(create_bias_result_table(bias_result))
        story.append(Spacer(1, 0.3*inch))
        
        # 评估说明
        is_significant = bias_result.get('is_significant', False)
        if is_significant:
            eval_text = "⚠️ <b>偏倚显著</b>：p 值 < 0.05，测量系统存在显著偏倚，需要校准或调整。"
        else:
            eval_text = "✅ <b>偏倚不显著</b>：p 值 ≥ 0.05，测量系统偏倚在可接受范围内。"
        
        story.append(Paragraph(eval_text, styles['ChineseBody']))
        story.append(Spacer(1, 0.3*inch))
        
        # 原始数据
        if chart_data and 'measurements' in chart_data:
            story.append(Paragraph("2. 原始测量数据", styles['ChineseHeading2']))
            story.append(Spacer(1, 0.15*inch))
            story.append(create_bias_raw_data_table(chart_data['measurements'], chart_data.get('reference_value', 0)))
            story.append(Spacer(1, 0.3*inch))
        
        # 图表
        if chart_data and 'measurements' in chart_data:
            story.append(Paragraph("3. 分析图表", styles['ChineseHeading2']))
            story.append(Spacer(1, 0.2*inch))
            
            chart_buf = create_bias_chart(
                chart_data['measurements'],
                chart_data.get('reference_value', 0),
                bias_result
            )
            chart_buf.seek(0)
            chart_img = Image(chart_buf, width=6.5*inch, height=4*inch)
            story.append(chart_img)
            story.append(Spacer(1, 0.3*inch))
    
    elif study_type == 'LINEARITY':
        story.append(Paragraph("1. 线性分析结果", styles['ChineseHeading2']))
        story.append(Spacer(1, 0.2*inch))
        
        linearity_result = results.get('linearity_result', {})
        story.append(create_linearity_result_table(linearity_result))
        story.append(Spacer(1, 0.3*inch))
        
        # 评估说明
        is_linear = linearity_result.get('is_linear', False)
        r_squared = linearity_result.get('r_squared', 0)
        
        if is_linear:
            eval_text = f"✅ <b>线性可接受</b>：R² = {r_squared:.4f}，测量系统在量程范围内线性良好。"
        else:
            eval_text = f"⚠️ <b>线性存在问题</b>：R² = {r_squared:.4f}，测量系统可能存在线性问题，需要调查原因。"
        
        story.append(Paragraph(eval_text, styles['ChineseBody']))
        story.append(Spacer(1, 0.3*inch))
        
        # 原始数据
        if chart_data and 'reference_values' in chart_data:
            story.append(Paragraph("2. 原始测量数据", styles['ChineseHeading2']))
            story.append(Spacer(1, 0.15*inch))
            story.append(create_linearity_raw_data_table(chart_data['reference_values'], chart_data['measurements']))
            story.append(Spacer(1, 0.3*inch))
        
        # 图表
        if chart_data and 'reference_values' in chart_data:
            story.append(Paragraph("3. 分析图表", styles['ChineseHeading2']))
            story.append(Spacer(1, 0.2*inch))
            
            chart_buf = create_linearity_chart(
                chart_data['reference_values'],
                chart_data['measurements'],
                linearity_result
            )
            chart_buf.seek(0)
            chart_img = Image(chart_buf, width=6.5*inch, height=4*inch)
            story.append(chart_img)
            story.append(Spacer(1, 0.3*inch))
    
    # 页脚
    story.append(PageBreak())
    story.append(create_footer(styles))
    
    # 构建 PDF
    doc.build(story)
    
    # 获取字节数据
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes
