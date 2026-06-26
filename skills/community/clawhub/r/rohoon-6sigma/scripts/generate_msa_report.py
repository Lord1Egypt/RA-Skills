#!/usr/bin/env python3
"""
MSA Report Generator
Generates MSA study reports (GR&R, Bias, Linearity) in PDF format
A4 Portrait layout
"""

import io
import os
import numpy as np
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['font.sans-serif'] = ['STHeiti', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False
import matplotlib.pyplot as plt

def register_chinese_font():
    font_paths = ["/System/Library/Fonts/STHeiti Light.ttc"]
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont('Chinese', font_path))
                return True
            except: pass
    return False

register_chinese_font()

def create_grr_chart(data_array, grr_result, evaluation):
    """Create GR&R analysis chart"""
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    fig.suptitle('GR&R Analysis Charts', fontsize=12, fontweight='bold')
    
    n_parts, n_operators, n_trials = data_array.shape
    
    # 1. Part averages
    ax1 = axes[0, 0]
    part_means = [np.mean(data_array[i, :, :]) for i in range(n_parts)]
    ax1.bar(range(1, n_parts+1), part_means, color='skyblue', edgecolor='black')
    ax1.set_xlabel('Part')
    ax1.set_ylabel('Average')
    ax1.set_title('Part Averages')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # 2. Operator boxplot
    ax2 = axes[0, 1]
    operator_data = [data_array[:, i, :].flatten() for i in range(n_operators)]
    bp = ax2.boxplot(operator_data, labels=[f'Op{i+1}' for i in range(n_operators)])
    ax2.set_ylabel('Measurement')
    ax2.set_title('Operator Distribution')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # 3. Variation pie chart
    ax3 = axes[1, 0]
    labels = ['EV', 'AV', 'PV']
    sizes = [grr_result['ev'], grr_result['av'], grr_result['pv']]
    colors_pie = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    ax3.pie(sizes, labels=labels, colors=colors_pie, autopct='%1.1f%%')
    ax3.set_title('Variation Distribution')
    
    # 4. %GRR bar chart
    ax4 = axes[1, 1]
    metrics = ['%EV', '%AV', '%GRR', '%PV']
    values = [evaluation['percent_ev'], evaluation['percent_av'], 
              evaluation['percent_grr'], evaluation['percent_pv']]
    bar_colors = ['#FF6B6B' if v > 30 else '#FFD93D' if v > 10 else '#6BCB77' for v in values]
    ax4.bar(metrics, values, color=bar_colors)
    ax4.set_ylabel('Percentage (%)')
    ax4.set_title('Variation Percentage')
    ax4.axhline(y=10, color='green', linestyle='--', alpha=0.5)
    ax4.axhline(y=30, color='red', linestyle='--', alpha=0.5)
    ax4.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    return buf

def generate_msa_grr_report(output_path, study_info, grr_result, evaluation, data_array):
    """Generate MSA GR&R PDF report"""
    
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                           rightMargin=10*mm, leftMargin=10*mm,
                           topMargin=10*mm, bottomMargin=10*mm)
    
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    story.append(Paragraph("<b>MSA GR&R Study Report</b>", 
                          style=ParagraphStyle('Title', fontSize=14, alignment=1)))
    story.append(Spacer(1, 0.15*inch))
    
    # Study Information
    info_data = [
        ['Study ID:', str(study_info.get('id', 'N/A'))],
        ['Study Name:', study_info.get('study_name', 'N/A')],
        ['Part Count:', str(study_info.get('n_parts', 'N/A'))],
        ['Operator Count:', str(study_info.get('n_operators', 'N/A'))],
        ['Trial Count:', str(study_info.get('n_trials', 'N/A'))],
        ['Date:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
    ]
    
    info_table = Table(info_data, colWidths=[4*cm, 9*cm])
    info_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Results Table
    results_data = [
        ['Variation Component', 'Value', 'Percentage'],
        ['Repeatability (EV)', f"{grr_result['ev']:.6f}", f"{evaluation['percent_ev']:.2f}%"],
        ['Reproducibility (AV)', f"{grr_result['av']:.6f}", f"{evaluation['percent_av']:.2f}%"],
        ['GR&R (RR)', f"{grr_result['rr']:.6f}", f"{evaluation['percent_grr']:.2f}%"],
        ['Part Variation (PV)', f"{grr_result['pv']:.6f}", f"{evaluation['percent_pv']:.2f}%"],
        ['Total Variation (TV)', f"{grr_result['tv']:.6f}", '100%'],
        ['', '', ''],
        ['Evaluation', '', ''],
        ['ndc (Distinct Categories)', str(evaluation.get('ndc', 'N/A')), ''],
        ['Acceptance', evaluation.get('acceptance', 'N/A'), ''],
    ]
    
    results_table = Table(results_data, colWidths=[5*cm, 4*cm, 4*cm])
    results_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('BACKGROUND', (0, 1), (-1, 6), colors.beige),
        ('BACKGROUND', (0, 8), (-1, -1), colors.lightblue),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    story.append(results_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Charts
    story.append(Paragraph("<b>Analysis Charts</b>", style=ParagraphStyle('Heading', fontSize=11)))
    story.append(Spacer(1, 0.1*inch))
    
    chart_buf = create_grr_chart(data_array, grr_result, evaluation)
    chart_buf.seek(0)
    chart_img = Image(chart_buf, width=14*cm, height=11*cm)
    story.append(chart_img)
    story.append(Spacer(1, 0.2*inch))
    
    # Conclusion
    acceptance = evaluation.get('acceptance', 'N/A')
    if acceptance == 'acceptable':
        conclusion = "✅ <b>Measurement system is ACCEPTABLE</b>: %GRR ≤ 10%"
    elif acceptance == 'conditionally_acceptable':
        conclusion = "⚠️ <b>Measurement system is CONDITIONALLY ACCEPTABLE</b>: 10% < %GRR ≤ 30%"
    else:
        conclusion = "❌ <b>Measurement system is UNACCEPTABLE</b>: %GRR > 30%, improvement required"
    
    story.append(Paragraph(conclusion, style=ParagraphStyle('Conclusion', fontSize=10)))
    
    # Footer
    story.append(Spacer(1, 0.3*inch))
    footer = Paragraph(
        f"<i>Generated by Rohoon Six Sigma Skill | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>",
        style=ParagraphStyle('Footer', fontSize=8, textColor=colors.gray)
    )
    story.append(footer)
    
    doc.build(story)
    print(f"✅ MSA GR&R Report generated: {output_path}")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', '-o', default='/tmp/msa_grr_report.pdf')
    args = parser.parse_args()
    
    # Test data
    study_info = {'id': 1, 'study_name': 'Test GR&R', 'n_parts': 10, 'n_operators': 3, 'n_trials': 3}
    grr_result = {'ev': 0.05, 'av': 0.03, 'rr': 0.06, 'pv': 0.21, 'tv': 0.22}
    evaluation = {'percent_grr': 27.31, 'percent_ev': 23.45, 'percent_av': 13.99, 
                  'percent_pv': 96.19, 'ndc': 5, 'acceptance': 'conditionally_acceptable'}
    np.random.seed(42)
    data_array = np.random.normal(10.0, 0.1, (10, 3, 3))
    
    generate_msa_grr_report(args.output, study_info, grr_result, evaluation, data_array)
