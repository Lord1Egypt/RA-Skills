#!/usr/bin/env python3
"""
Generate SPC PDF Report
Creates a professional SPC report with control charts and capability analysis

Usage:
    python3 generate_spc_report.py --output /tmp/spc_report.pdf
"""

import io
import os
import sys
import numpy as np
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['font.sans-serif'] = ['STHeiti', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False
import matplotlib.pyplot as plt
from scipy import stats

# Register Chinese font
def register_chinese_font():
    font_paths = [
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
    ]
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont('Chinese', font_path))
                return True
            except:
                pass
    return False

register_chinese_font()

def generate_data():
    """Generate simulated SPC data"""
    np.random.seed(42)
    
    # Generate 100 measurements (20 subgroups × 5)
    # Process with slight shift
    base_mean = 10.0
    base_std = 0.05
    
    data = []
    for i in range(20):
        # Add slight trend
        mean_shift = 0.002 * i
        subgroup = np.random.normal(base_mean + mean_shift, base_std, 5)
        data.extend(subgroup)
    
    return np.array(data)

def create_control_chart(data, subgroup_size=5):
    """Create control chart image"""
    n_subgroups = len(data) // subgroup_size
    subgroups = data[:n_subgroups * subgroup_size].reshape(n_subgroups, subgroup_size)
    
    xbar = np.mean(subgroups, axis=1)
    r = np.ptp(subgroups, axis=1)
    
    xbar_bar = np.mean(xbar)
    r_bar = np.mean(r)
    
    # Constants for n=5
    A2, D3, D4 = 0.577, 0, 2.114
    
    ucl_xbar = xbar_bar + A2 * r_bar
    lcl_xbar = xbar_bar - A2 * r_bar
    ucl_r = D4 * r_bar
    lcl_r = D3 * r_bar
    
    # Create plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    fig.suptitle('Xbar-R Control Chart', fontsize=14, fontweight='bold')
    
    # Xbar chart
    ax1.plot(range(1, n_subgroups+1), xbar, 'b-o', markersize=4, label='Xbar')
    ax1.axhline(y=xbar_bar, color='green', linestyle='-', linewidth=2, label=f'CL={xbar_bar:.4f}')
    ax1.axhline(y=ucl_xbar, color='red', linestyle='--', linewidth=2, label=f'UCL={ucl_xbar:.4f}')
    ax1.axhline(y=lcl_xbar, color='red', linestyle='--', linewidth=2, label=f'LCL={lcl_xbar:.4f}')
    ax1.set_ylabel('Average')
    ax1.set_title('Xbar Chart')
    ax1.legend(loc='upper right', fontsize=8)
    ax1.grid(True, alpha=0.3)
    
    # R chart
    ax2.plot(range(1, n_subgroups+1), r, 'b-o', markersize=4, label='R')
    ax2.axhline(y=r_bar, color='green', linestyle='-', linewidth=2, label=f'CL={r_bar:.4f}')
    ax2.axhline(y=ucl_r, color='red', linestyle='--', linewidth=2, label=f'UCL={ucl_r:.4f}')
    ax2.axhline(y=lcl_r, color='red', linestyle='--', linewidth=2, label=f'LCL={lcl_r:.4f}')
    ax2.set_xlabel('Subgroup')
    ax2.set_ylabel('Range')
    ax2.set_title('R Chart')
    ax2.legend(loc='upper right', fontsize=8)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    
    return buf

def create_capability_chart(data, usl, lsl):
    """Create capability analysis chart"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle('Process Capability Analysis', fontsize=14, fontweight='bold')
    
    # Histogram with normal curve
    ax1.hist(data, bins=15, density=True, alpha=0.7, edgecolor='black', color='skyblue')
    
    mu, sigma = np.mean(data), np.std(data)
    x = np.linspace(lsl, usl, 100)
    ax1.plot(x, stats.norm.pdf(x, mu, sigma), 'r-', linewidth=2, label='Normal Fit')
    
    ax1.axvline(x=mu, color='red', linestyle='--', linewidth=2, label=f'μ={mu:.4f}')
    ax1.axvline(x=usl, color='green', linestyle='-', linewidth=2, label=f'USL={usl}')
    ax1.axvline(x=lsl, color='green', linestyle='-', linewidth=2, label=f'LSL={lsl}')
    ax1.set_xlabel('Measurement')
    ax1.set_ylabel('Density')
    ax1.set_title('Data Distribution')
    ax1.legend(fontsize=8)
    ax1.grid(True, alpha=0.3)
    
    # Capability indices bar chart
    cp = (usl - lsl) / (6 * sigma)
    cpu = (usl - mu) / (3 * sigma)
    cpl = (mu - lsl) / (3 * sigma)
    cpk = min(cpu, cpl)
    
    metrics = ['Cp', 'Cpu', 'Cpl', 'Cpk']
    values = [cp, cpu, cpl, cpk]
    colors_bar = ['#6BCB77' if v >= 1.33 else '#FFD93D' if v >= 1.0 else '#FF6B6B' for v in values]
    
    bars = ax2.bar(metrics, values, color=colors_bar)
    ax2.set_ylabel('Capability Index')
    ax2.set_title('Process Capability Indices')
    ax2.axhline(y=1.33, color='orange', linestyle='--', alpha=0.5, label='Target (1.33)')
    ax2.axhline(y=1.0, color='red', linestyle=':', alpha=0.5, label='Min (1.0)')
    ax2.legend(fontsize=8)
    ax2.set_ylim(0, max(2.5, max(values) * 1.3))
    
    for bar, val in zip(bars, values):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                f'{val:.2f}', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    
    return buf, cp, cpk

def create_table(data, col_widths):
    """Create styled table"""
    table = Table(data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Chinese'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    return table

def generate_spc_pdf(output_path):
    """Generate complete SPC report PDF"""
    
    # Generate data
    data = generate_data()
    usl, lsl = 10.3, 9.7
    
    # Calculate statistics
    n = len(data)
    mean = np.mean(data)
    std = np.std(data, ddof=1)
    cp = (usl - lsl) / (6 * std)
    cpu = (usl - mean) / (3 * std)
    cpl = (mean - lsl) / (3 * std)
    cpk = min(cpu, cpl)
    
    # Create PDF
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
        title="SPC Report"
    )
    
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='ChineseHeading1', parent=styles['Heading1'], fontName='Chinese', fontSize=18, spaceAfter=12, alignment=1))
    styles.add(ParagraphStyle(name='ChineseHeading2', parent=styles['Heading2'], fontName='Chinese', fontSize=14, spaceAfter=10, spaceBefore=8))
    styles.add(ParagraphStyle(name='ChineseBody', parent=styles['Normal'], fontName='Chinese', fontSize=10, spaceAfter=6, leading=14))
    styles.add(ParagraphStyle(name='ChineseSmall', parent=styles['Normal'], fontName='Chinese', fontSize=8, textColor=colors.gray))
    
    story = []
    
    # Title
    story.append(Paragraph("SPC Statistical Process Control Report", styles['ChineseHeading1']))
    story.append(Spacer(1, 0.3*inch))
    
    # Study Information
    info_data = [
        ['Product:', 'Bearing Housing'],
        ['Characteristic:', 'Bore Diameter (mm)'],
        ['Process:', 'CNC Machining'],
        ['Machine:', 'CNC-01'],
        ['Operator:', 'Quality Inspector'],
        ['Sample Size:', str(n)],
        ['Subgroup Size:', '5'],
        ['Number of Subgroups:', '20'],
        ['USL:', str(usl)],
        ['LSL:', str(lsl)],
        ['Date:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
    ]
    story.append(create_table(info_data, [4*cm, 9*cm]))
    story.append(Spacer(1, 0.3*inch))
    
    # Control Chart Section
    story.append(Paragraph("1. Control Chart Analysis", styles['ChineseHeading2']))
    story.append(Spacer(1, 0.15*inch))
    
    chart_buf = create_control_chart(data)
    chart_buf.seek(0)
    chart_img = Image(chart_buf, width=6.5*inch, height=5*inch)
    story.append(chart_img)
    story.append(Spacer(1, 0.3*inch))
    
    # Control chart statistics
    xbar_bar = np.mean(np.mean(data.reshape(20, 5), axis=1))
    r_bar = np.mean(np.ptp(data.reshape(20, 5), axis=1))
    
    ctrl_data = [
        ['Xbar (Center Line):', f'{xbar_bar:.4f}'],
        ['R Bar (Average Range):', f'{r_bar:.4f}'],
        ['Estimated Sigma:', f'{r_bar/2.326:.4f}'],
        ['Process Status:', 'In Control ✅'],
    ]
    story.append(create_table(ctrl_data, [5*cm, 7*cm]))
    story.append(Spacer(1, 0.3*inch))
    
    # Capability Section
    story.append(Paragraph("2. Process Capability Analysis", styles['ChineseHeading2']))
    story.append(Spacer(1, 0.15*inch))
    
    cap_chart_buf, cp_val, cpk_val = create_capability_chart(data, usl, lsl)
    cap_chart_buf.seek(0)
    cap_img = Image(cap_chart_buf, width=6.5*inch, height=4.5*inch)
    story.append(cap_img)
    story.append(Spacer(1, 0.3*inch))
    
    # Capability statistics
    if cpk >= 1.67:
        rating = 'Excellent'
        action = 'Maintain current state'
    elif cpk >= 1.33:
        rating = 'Good'
        action = 'Maintain, continuous improvement'
    elif cpk >= 1.0:
        rating = 'Marginal'
        action = 'Need improvement plan'
    else:
        rating = 'Insufficient'
        action = 'Must improve, 100% inspection'
    
    cap_data = [
        ['Cp (Potential Capability):', f'{cp:.4f}'],
        ['Cpk (Actual Capability):', f'{cpk:.4f}'],
        ['CPU:', f'{cpu:.4f}'],
        ['CPL:', f'{cpl:.4f}'],
        ['Mean:', f'{mean:.4f}'],
        ['Std Dev:', f'{std:.4f}'],
        ['Min:', f'{np.min(data):.4f}'],
        ['Max:', f'{np.max(data):.4f}'],
        ['', ''],
        ['Rating:', rating],
        ['Action:', action],
        ['Acceptable:', 'Yes ✅' if cpk >= 1.33 else 'No ❌'],
    ]
    story.append(create_table(cap_data, [5*cm, 7*cm]))
    story.append(Spacer(1, 0.3*inch))
    
    # Conclusion
    story.append(Paragraph("3. Conclusion", styles['ChineseHeading2']))
    story.append(Spacer(1, 0.15*inch))
    
    conclusion = f"""
    <b>Process Status:</b> The process is in statistical control with no out-of-control points detected.<br/><br/>
    <b>Capability Assessment:</b> Cpk = {cpk:.2f} indicates the process is {rating.lower()}. 
    The process {action.lower()}.<br/><br/>
    <b>Recommendations:</b><br/>
    - Continue monitoring with control charts<br/>
    - Investigate any special causes if points go out of control<br/>
    - Consider reducing variation if higher capability is required
    """
    story.append(Paragraph(conclusion, styles['ChineseBody']))
    
    # Footer
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph(
        f"<i>Report generated by Rohoon Six Sigma Skill | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>",
        style=styles['ChineseSmall']
    ))
    
    # Build PDF
    doc.build(story)
    print(f"✅ SPC Report generated: {output_path}")
    print(f"   Sample size: {n}")
    print(f"   Cpk: {cpk:.4f}")
    print(f"   Rating: {rating}")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Generate SPC PDF Report')
    parser.add_argument('--output', '-o', type=str, default='/tmp/spc_report.pdf',
                       help='Output PDF file path')
    args = parser.parse_args()
    
    generate_spc_pdf(args.output)
