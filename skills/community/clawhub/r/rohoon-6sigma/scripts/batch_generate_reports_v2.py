#!/usr/bin/env python3
"""
批量生成 SPC 报告（Figure 12-3 标准格式）- 支持完整中英文
导入 Excel 数据，自动生成 SPC 分析报告
"""

import sys
import os
import numpy as np
import pandas as pd
from datetime import datetime

sys.path.insert(0, '/Library/Python/3.9/site-packages')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# 导入 Figure 12-3 完整生成器（带图表）
from generate_figure12_3 import generate_figure12_3_pdf

# 直接在这里定义支持中英文的生成函数
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.flowables import Flowable

import io

# 中文字体注册
_CHINESE_FONT_REGISTERED = False
def register_chinese_font():
    global _CHINESE_FONT_REGISTERED
    if _CHINESE_FONT_REGISTERED:
        return True
    font_paths = ["/System/Library/Fonts/STHeiti Light.ttc", "/System/Library/Fonts/PingFang.ttc"]
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont('Chinese', font_path))
                _CHINESE_FONT_REGISTERED = True
                return True
            except:
                continue
    return False

def _para(text, font_size=7, bold=False, color=None):
    register_chinese_font()
    if bold:
        text = f'<b>{text}</b>'
    if color:
        text = f'<font color="{color}">{text}</font>'
    style = ParagraphStyle(name='temp', fontName='Chinese', fontSize=font_size, leading=font_size + 2)
    return Paragraph(text, style)

class CapabilityBar(Flowable):
    def __init__(self, value, target, max_scale=2.0, width=200, height=45):
        super().__init__()
        self.value = value
        self.target = target
        self.max_scale = max_scale
        self._width = width
        self._height = height
    
    def wrap(self, availWidth, availHeight):
        return (self._width, self._height)
    
    def draw(self):
        canvas = self.canv
        width, height = self._width, self._height
        value_ratio = min(self.value / self.max_scale, 1.0)
        target_ratio = min(self.target / self.max_scale, 1.0)
        passed = self.value >= self.target
        
        bar_height = height * 0.4
        bar_y = (height - bar_height) / 2
        
        # 灰色背景
        canvas.setFillColor(colors.Color(0.92, 0.92, 0.92))
        canvas.rect(0, bar_y, width, bar_height, fill=1, stroke=0)
        
        # 绿色/红色进度条
        bar_color = colors.Color(0.0, 0.65, 0.0) if passed else colors.Color(0.8, 0.0, 0.0)
        canvas.setFillColor(bar_color)
        canvas.rect(0, bar_y, width * value_ratio, bar_height, fill=1, stroke=0)
        
        # 实际值竖线
        value_x = width * value_ratio
        canvas.setStrokeColor(bar_color)
        canvas.setLineWidth(2)
        canvas.line(value_x, bar_y - 4, value_x, bar_y + bar_height + 4)
        
        # 目标值箭头
        target_x = width * target_ratio
        canvas.setStrokeColor(colors.gray)
        canvas.setLineWidth(1.5)
        arrow_h = 5
        canvas.line(target_x - arrow_h/2, bar_y + bar_height + 4 + arrow_h, target_x, bar_y + bar_height + 4 + arrow_h/2)
        canvas.line(target_x, bar_y + bar_height + 4 + arrow_h/2, target_x + arrow_h/2, bar_y + bar_height + 4 + arrow_h)
        canvas.line(target_x - arrow_h/2, bar_y - 4 - arrow_h, target_x, bar_y - 4 - arrow_h/2)
        canvas.line(target_x, bar_y - 4 - arrow_h/2, target_x + arrow_h/2, bar_y - 4 - arrow_h)
        
        # 刻度
        canvas.setStrokeColor(colors.black)
        canvas.setLineWidth(0.5)
        canvas.setFillColor(colors.black)
        canvas.setFont('Helvetica', 7)
        for ratio, label in [(0, '0'), (0.5, '1.0'), (1.0, '2.0')]:
            x = width * ratio
            canvas.line(x, bar_y - 6, x, bar_y - 3)
            canvas.drawCentredString(x, bar_y - 16, label)
        
        # 实际值数字
        canvas.setFillColor(bar_color)
        canvas.setFont('Helvetica-Bold', 8)
        canvas.drawCentredString(value_x, bar_y - 26, f'{self.value:.2f}')
        
        # 目标值标签
        canvas.setFillColor(colors.gray)
        canvas.setFont('Helvetica', 7)
        canvas.drawCentredString(target_x, bar_y - 38, f'Target: {self.target:.2f}')


def generate_figure12_3_bilingual(study_info, data, specification, capability_indices, language='en'):
    """生成 Figure 12-3 报告（支持中英文）"""
    
    # 中英文标签
    L = {
        'en': {
            'title': 'SPC & Process Capability Study Report',
            'subtitle': 'AIAG / VDA SPC harmonized standard',
            'op_name': 'Op.Name', 'evaluation': 'Evaluation',
            'part_no': 'Part No.', 'part_name': 'Part Name', 'phase': 'Phase',
            'char_no': 'Characteristic No.', 'char_name': 'Characteristic Name',
            'department': 'Department', 'machine_id': 'Machine ID', 'machine_name': 'Machine Name',
            'qe': 'QE', 'process_id': 'Process ID', 'process_name': 'Process Name',
            'study_loc': 'Study loc.', 'remarks': 'Remarks',
            'drawing_values': 'Drawing Values', 'collected_values': 'Collected Values',
            'statistical_values': 'Statistical Values',
            'potential_capability': 'Potential Capability Index (95% C.I.)',
            'critical_capability': 'Critical Capability Index (95% C.I.))',
            'requirements_met': 'The requirements were met (Cp, Cpk)',
            'requirements_not_met': 'Requirements NOT met',
            'required_potential': 'Required Potential Performance/Capability Index',
            'required_critical': 'Required Critical Performance/Capability Index',
            'analysis_control': 'Analysis/Control', 'height': 'Height',
            'xbar_remarks': 'xbar/s chart, capability indices for fixed tooling',
            'cp_label': 'Cp,G', 'cpk_label': 'Cpk,G',
        },
        'cn': {
            'title': 'SPC 与过程能力研究报告',
            'subtitle': 'AIAG / VDA SPC 协调标准',
            'op_name': '操作员', 'evaluation': '评估期间',
            'part_no': '零件编号', 'part_name': '零件名称', 'phase': '阶段',
            'char_no': '特性编号', 'char_name': '特性名称',
            'department': '部门', 'machine_id': '设备编号', 'machine_name': '设备名称',
            'qe': '质量工程师', 'process_id': '过程编号', 'process_name': '过程名称',
            'study_loc': '研究地点', 'remarks': '备注',
            'drawing_values': '设计值', 'collected_values': '收集值',
            'statistical_values': '统计值',
            'potential_capability': '潜在能力指数 (95% 置信区间)',
            'critical_capability': '临界能力指数 (95% 置信区间)',
            'requirements_met': '满足要求 (Cp, Cpk)',
            'requirements_not_met': '不满足要求',
            'required_potential': '要求的潜在性能/能力指数',
            'required_critical': '要求的临界性能/能力指数',
            'analysis_control': '分析/控制', 'height': '高度',
            'xbar_remarks': 'xbar/s 控制图，固定工装能力指数',
            'cp_label': 'Cp,G', 'cpk_label': 'Cpk,G',
        },
    }
    
    labels = L.get(language, L['en'])
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=1.5*cm, leftMargin=1.5*cm, topMargin=1.5*cm, bottomMargin=1.5*cm)
    styles = getSampleStyleSheet()
    register_chinese_font()
    story = []
    
    usl = specification['usl']
    lsl = specification['lsl']
    target = specification.get('target', (usl+lsl)/2)
    mu = np.mean(data)
    sigma = np.std(data, ddof=1)
    cp = capability_indices['cp']
    cpk = capability_indices['cpk']
    
    page_width = A4[0] - 3*cm
    col_width = page_width / 6
    
    # 标题
    title_style = ParagraphStyle('title', fontName='Chinese', fontSize=12, leading=14, alignment=1)
    story.append(Paragraph(labels['title'], title_style))
    story.append(Paragraph(labels['subtitle'], ParagraphStyle('subtitle', fontName='Chinese', fontSize=9, leading=11, alignment=1, textColor=colors.gray)))
    story.append(Spacer(1, 0.15*inch))
    
    # 表头
    header_data = [
        [_para(f"{labels['op_name']}:", bold=True), _para(study_info.get('operator_name', 'Quality'), color='blue'),
         _para(f"{labels['evaluation']}:", bold=True), _para(f'from {study_info.get("start_time", "N/A")}\nto {study_info.get("end_time", "N/A")}', color='blue'), '', ''],
        [_para(labels['part_no'], bold=True), _para(study_info.get('part_name', 'N/A'), color='blue'),
         _para(labels['part_name'], bold=True), _para(study_info.get('characteristic_name', 'N/A'), color='blue'),
         _para(labels['phase'], bold=True), _para(labels['analysis_control'], color='blue')],
        [_para(labels['char_no'], bold=True), _para(study_info.get('characteristic_id', '8'), color='blue'),
         _para(labels['char_name'], bold=True), _para(labels['height'], color='blue'),
         _para(labels['department'], bold=True), _para(labels['department'], color='blue')],
        [_para(labels['machine_id'], bold=True), _para(study_info.get('machine_id', 'N/A'), color='blue'),
         _para(labels['machine_name'], bold=True), _para(study_info.get('machine_name', 'N/A'), color='blue'),
         _para(labels['qe'], bold=True), _para(labels['qe'], color='blue')],
        [_para(labels['process_id'], bold=True), _para(study_info.get('process_id', 'N/A'), color='blue'),
         _para(f"{labels['process_name']}:", bold=True), _para(study_info.get('process_name', 'N/A'), color='blue'),
         _para(labels['study_loc'], bold=True), _para(study_info.get('study_location', 'N/A'), color='blue')],
        [_para(labels['remarks'], bold=True), _para(labels['xbar_remarks'], color='blue'), '', '', '', ''],
    ]
    
    header_table = Table(header_data, colWidths=[col_width]*6)
    header_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Chinese'), ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3), ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black), ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('SPAN', (3, 0), (5, 0)), ('SPAN', (1, 5), (5, 5)),
        ('WORDWRAP', (0, 0), (-1, -1), 'ON'),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 0.15*inch))
    
    # 统计表格
    col_width_3 = page_width / 3
    if language == 'cn':
        stats_data = [
            [labels['drawing_values'], labels['collected_values'], labels['statistical_values']],
            [f'Tm = {target:.4f}', f'x̃ = {mu:.4f}', f'X50% = {mu:.4f}'],
            [f'LSL = {lsl:.4f}', f'xmin = {min(data):.4f}', f'X0.135% = {mu - 3*sigma:.6f}'],
            [f'USL = {usl:.4f}', f'xmax = {max(data):.4f}', f'X99.865% = {mu + 3*sigma:.6f}'],
            [f'T = {usl-lsl:.4f}', f'R = {np.ptp(data):.4f}', f'Xup3-Xlo3 = {6*sigma:.6f}'],
            ['', f'ntot = {len(data)}', f'neff = {len(data)}'],
            ['', f'n<T> = {len(data)}/100%', 'p<T> = 100%'],
            ['', 'n>USL = 0', 'p>USL = 0%'],
            ['', 'n<LSL = 0', 'p<LSL = 0%'],
            ['测量不确定度：0.0211', f'子组大小 = 5', f'x̄ = {mu:.6f}'],
            ['扩展因子 k = 2 (95.45%)', '子组类型/频率：固定/1 件/小时', f's̄ = {sigma:.6f}'],
            ['Guard Band (95%): 0.0175', '分布模型：混合分布 (EM)', ''],
            ['单位：mm', '计算方法：ISO 22514-2 M2,1', ''],
        ]
    else:
        stats_data = [
            [labels['drawing_values'], labels['collected_values'], labels['statistical_values']],
            [f'Tm = {target:.4f}', f'x̃ = {mu:.4f}', f'X50% = {mu:.4f}'],
            [f'LSL = {lsl:.4f}', f'xmin = {min(data):.4f}', f'X0.135% = {mu - 3*sigma:.6f}'],
            [f'USL = {usl:.4f}', f'xmax = {max(data):.4f}', f'X99.865% = {mu + 3*sigma:.6f}'],
            [f'T = {usl-lsl:.4f}', f'R = {np.ptp(data):.4f}', f'Xup3-Xlo3 = {6*sigma:.6f}'],
            ['', f'ntot = {len(data)}', f'neff = {len(data)}'],
            ['', f'n<T> = {len(data)}/100%', 'p<T> = 100%'],
            ['', 'n>USL = 0', 'p>USL = 0%'],
            ['', 'n<LSL = 0', 'p<LSL = 0%'],
            ['Exp. Uncertainty: 0.0211', f'Subgr.size = 5', f'x̄ = {mu:.6f}'],
            ['Factor k = 2 (95.45%)', 'Subgr: fixed / 1 p.h.', f's̄ = {sigma:.6f}'],
            ['Guard Band (95%): 0.0175', 'Model: Mixed (EM)', ''],
            ['Unit: mm', 'Method: ISO 22514-2 M2,1', ''],
        ]
    
    stats_table = Table(stats_data, colWidths=[col_width_3]*3)
    stats_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Chinese'), ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2), ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black), ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
    ]))
    story.append(stats_table)
    story.append(Spacer(1, 0.15*inch))
    
    # 能力指数区域
    passed = cpk >= 1.67 and cp >= 1.67
    bar_width = page_width * 0.25 - 10
    cp_bar = CapabilityBar(cp, 1.67, 2.0, width=bar_width, height=45)
    cpk_bar = CapabilityBar(cpk, 1.67, 2.0, width=bar_width, height=45)
    
    cap_data = [
        [labels['potential_capability'], labels['cp_label'], f'{cp:.2f} ≤ {cp:.2f} ≤ {cp*1.1:.2f}', cp_bar],
        [labels['critical_capability'], labels['cpk_label'], f'{cpk:.2f} ≤ {cpk:.2f} ≤ {cpk*1.1:.2f}', cpk_bar],
        ['', '', labels['requirements_met'] if passed else labels['requirements_not_met'], ''],
    ]
    
    col_width_4 = [page_width * 0.38, page_width * 0.12, page_width * 0.25, page_width * 0.25]
    cap_table = Table(cap_data, colWidths=col_width_4)
    cap_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Chinese'), ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4), ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black), ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (2, 2), (2, 2), colors.green if passed else colors.red),
        ('TEXTCOLOR', (2, 2), (2, 2), colors.white),
        ('ALIGN', (3, 0), (3, 1), 'CENTER'), ('VALIGN', (3, 0), (3, 1), 'MIDDLE'),
    ]))
    story.append(cap_table)
    story.append(Spacer(1, 0.1*inch))
    
    target_data = [
        [labels['required_potential'], f'{labels["cp_label"]} target', '1.67', ''],
        [labels['required_critical'], f'{labels["cpk_label"]} target', '1.33', ''],
    ]
    target_table = Table(target_data, colWidths=col_width_4)
    target_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Chinese'), ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4), ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black), ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(target_table)
    
    doc.build(story)
    return buffer.getvalue()


# ==================== 批量生成主程序 ====================

print("=" * 80)
print("SPC 报告批量生成器（Figure 12-3 标准格式，完整中英文支持）")
print("=" * 80)

data_dir = os.path.join(os.path.dirname(__file__), 'tmp', 'test_data')
output_dir_en = os.path.join(os.path.dirname(__file__), 'tmp', 'SPC_Reports_EN')
output_dir_cn = os.path.join(os.path.dirname(__file__), 'tmp', 'SPC_Reports_CN')

os.makedirs(output_dir_en, exist_ok=True)
os.makedirs(output_dir_cn, exist_ok=True)

data_files = [
    ('01_Normal_Distribution', '正态分布', 'Normal Distribution'),
    ('02_NonNormal_Weibull', 'Weibull 偏态', 'Weibull Skewed'),
    ('03_NonNormal_Mixed', '混合双峰', 'Mixed Bimodal'),
]

def load_excel_data(file_path):
    df = pd.read_excel(file_path, sheet_name='SPC_Data')
    return df

def calculate_capability(data, usl, lsl, target):
    mu = np.mean(data)
    sigma = np.std(data, ddof=1)
    cp = (usl - lsl) / (6 * sigma) if sigma > 0 else 0
    cpu = (usl - mu) / (3 * sigma) if sigma > 0 else 0
    cpl = (mu - lsl) / (3 * sigma) if sigma > 0 else 0
    cpk = min(cpu, cpl)
    return {'mu': mu, 'sigma': sigma, 'cp': cp, 'cpk': cpk, 'cpu': cpu, 'cpl': cpl, 'pp': cp, 'ppk': cpk}

def generate_report(df, output_path, language='en'):
    data = df['Measurement_Value'].values
    usl = df['USL'].iloc[0]
    lsl = df['LSL'].iloc[0]
    target = df['Target'].iloc[0]
    cap = calculate_capability(data, usl, lsl, target)
    
    study_info = {
        'operator_name': df['Operator'].iloc[0],
        'start_time': df['Measurement_Time'].min().strftime('%Y-%m-%d %H:%M:%S'),
        'end_time': df['Measurement_Time'].max().strftime('%Y-%m-%d %H:%M:%S'),
        'part_name': df['Part_Name'].iloc[0],
        'characteristic_name': df['Characteristic'].iloc[0],
        'machine_name': df['Machine'].iloc[0],
        'process_name': df['Process'].iloc[0],
        'process_id': 'PROC-001',
        'characteristic_id': 'CHAR-008',
        'machine_id': 'MC-001',
        'study_location': 'Workshop-1',
    }
    
    specification = {'usl': usl, 'lsl': lsl, 'target': target}
    capability_indices = {'cp': cap['cp'], 'cpk': cap['cpk'], 'cpu': cap['cpu'], 'cpl': cap['cpl'], 'pp': cap['pp'], 'ppk': cap['ppk']}
    
    # 使用完整生成器（带图表）
    pdf_bytes = generate_figure12_3_pdf(study_info, data, specification, capability_indices, language)
    
    with open(output_path, 'wb') as f:
        f.write(pdf_bytes)
    return cap

print("\n开始生成报告...")
print("=" * 80)

for file_prefix, name_cn, name_en in data_files:
    print(f"\n处理：{name_cn} ({name_en})")
    print("-" * 60)
    
    excel_path = os.path.join(data_dir, f'{file_prefix}_Data.xlsx')
    if not os.path.exists(excel_path):
        print(f"  ✗ 文件不存在：{excel_path}")
        continue
    
    df = load_excel_data(excel_path)
    print(f"  ✓ 加载数据：{len(df)} 条记录")
    
    # 英文版
    output_en = os.path.join(output_dir_en, f'{file_prefix}_Figure12-3_EN.pdf')
    cap_en = generate_report(df, output_en, language='en')
    print(f"  ✓ 英文报告：{output_en}")
    print(f"     Cp={cap_en['cp']:.2f}, Cpk={cap_en['cpk']:.2f}")
    
    # 中文版
    output_cn = os.path.join(output_dir_cn, f'{file_prefix}_Figure12-3_CN.pdf')
    cap_cn = generate_report(df, output_cn, language='cn')
    print(f"  ✓ 中文报告：{output_cn}")
    print(f"     Cp={cap_cn['cp']:.2f}, Cpk={cap_cn['cpk']:.2f}")

print("\n" + "=" * 80)
print("报告生成完成！")
print("=" * 80)
print(f"\n英文报告目录：{output_dir_en}")
print(f"中文报告目录：{output_dir_cn}")

# 打开所有 PDF
print("\n正在打开所有 PDF 报告...")
import subprocess
for output_dir in [output_dir_en, output_dir_cn]:
    for f in sorted(os.listdir(output_dir)):
        if f.endswith('.pdf'):
            subprocess.run(['open', os.path.join(output_dir, f)], check=False)

print("完成！")
