#!/usr/bin/env python3
"""
DOE Report Generator
Generates DOE study reports (Full Factorial, Fractional, Taguchi) in PDF format
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
from scipy import stats

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

def create_effects_plot(effects):
    """Create main effects plot"""
    fig, ax = plt.subplots(figsize=(8, 5))
    
    factor_names = list(effects.keys())
    effect_values = [effects[f] for f in factor_names]
    
    y_pos = np.arange(len(factor_names))
    colors_bar = ['red' if abs(e) > 5 else 'orange' if abs(e) > 2 else 'green' for e in effect_values]
    
    bars = ax.barh(y_pos, effect_values, color=colors_bar)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(factor_names)
    ax.set_xlabel('Effect')
    ax.set_title('Main Effects Plot')
    ax.grid(True, alpha=0.3, axis='x')
    ax.axvline(x=0, color='black', linestyle='-', linewidth=1)
    
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    return buf

def create_pareto_chart(effects):
    """Create Pareto chart of effects"""
    fig, ax = plt.subplots(figsize=(8, 5))
    
    factor_names = list(effects.keys())
    effect_values = [abs(effects[f]) for f in factor_names]
    
    # Sort by magnitude
    sorted_idx = np.argsort(effect_values)[::-1]
    sorted_names = [factor_names[i] for i in sorted_idx]
    sorted_values = [effect_values[i] for i in sorted_idx]
    
    y_pos = np.arange(len(sorted_names))
    
    bars = ax.barh(y_pos, sorted_values, color='skyblue', edgecolor='black')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(sorted_names)
    ax.set_xlabel('Absolute Effect')
    ax.set_title('Pareto Chart of Effects')
    ax.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    return buf

def generate_doe_full_factorial_report(output_path, design_info, effects, anova_results, responses):
    """Generate DOE Full Factorial PDF report"""
    
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                           rightMargin=10*mm, leftMargin=10*mm,
                           topMargin=10*mm, bottomMargin=10*mm)
    
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    story.append(Paragraph(f"<b>DOE 2^{design_info['factors']} Full Factorial Study Report</b>", 
                          style=ParagraphStyle('Title', fontSize=14, alignment=1)))
    story.append(Spacer(1, 0.15*inch))
    
    # Design Information
    info_data = [
        ['Design Type:', f"2^{design_info['factors']} Full Factorial"],
        ['Number of Factors:', str(design_info['factors'])],
        ['Number of Runs:', str(design_info['runs'])],
        ['Center Points:', str(design_info.get('center_points', 0))],
        ['Date:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
    ]
    
    info_table = Table(info_data, colWidths=[5*cm, 8*cm])
    info_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Effects Table
    story.append(Paragraph("<b>Main Effects and Interactions</b>", 
                          style=ParagraphStyle('Heading', fontSize=11)))
    story.append(Spacer(1, 0.1*inch))
    
    effects_data = [['Factor/Interaction', 'Effect', 'Significance']]
    for name, effect in effects.items():
        sig = '**' if abs(effect) > 5 else '*' if abs(effect) > 2 else ''
        effects_data.append([name, f"{effect:.4f} {sig}", 'Significant' if sig else 'Not Significant'])
    
    effects_table = Table(effects_data, colWidths=[5*cm, 4*cm, 4*cm])
    effects_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ]))
    story.append(effects_table)
    story.append(Spacer(1, 0.2*inch))
    
    # ANOVA Results
    if anova_results:
        story.append(Paragraph("<b>ANOVA Results</b>", 
                              style=ParagraphStyle('Heading', fontSize=11)))
        story.append(Spacer(1, 0.1*inch))
        
        anova_data = [['Source', 'SS', 'MS', 'F', 'p-value']]
        for name, result in anova_results['effects'].items():
            sig = '**' if result['significant'] else ''
            anova_data.append([name, f"{result['ss']:.4f}", f"{result['ms']:.4f}", 
                              f"{result['f']:.2f}", f"{result['p']:.4f} {sig}"])
        
        anova_table = Table(anova_data, colWidths=[4*cm, 2.5*cm, 2.5*cm, 2*cm, 2.5*cm])
        anova_table.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))
        story.append(anova_table)
        story.append(Spacer(1, 0.2*inch))
    
    # Charts
    story.append(Paragraph("<b>Analysis Charts</b>", 
                          style=ParagraphStyle('Heading', fontSize=11)))
    story.append(Spacer(1, 0.1*inch))
    
    effects_buf = create_effects_plot(effects)
    effects_buf.seek(0)
    effects_img = Image(effects_buf, width=14*cm, height=9*cm)
    story.append(effects_img)
    story.append(Spacer(1, 0.15*inch))
    
    pareto_buf = create_pareto_chart(effects)
    pareto_buf.seek(0)
    pareto_img = Image(pareto_buf, width=14*cm, height=9*cm)
    story.append(pareto_img)
    story.append(Spacer(1, 0.2*inch))
    
    # Conclusions
    significant_factors = [name for name, effect in effects.items() if abs(effect) > 2]
    
    if significant_factors:
        conclusion = f"<b>Significant Factors:</b> {', '.join(significant_factors)}<br/><br/>"
        conclusion += "<b>Recommendations:</b><br/>"
        conclusion += "1. Focus on optimizing the significant factors identified above<br/>"
        conclusion += "2. Consider conducting response surface methodology for further optimization<br/>"
        conclusion += "3. Validate results with confirmation runs"
    else:
        conclusion = "<b>No significant factors identified at current screening level.</b><br/><br/>"
        conclusion += "<b>Recommendations:</b><br/>"
        conclusion += "1. Consider increasing sample size or reducing noise<br/>"
        conclusion += "2. Review measurement system capability (MSA)<br/>"
        conclusion += "3. Consider additional factors or interactions"
    
    story.append(Paragraph(conclusion, style=ParagraphStyle('Conclusion', fontSize=10)))
    
    # Footer
    story.append(Spacer(1, 0.3*inch))
    footer = Paragraph(
        f"<i>Generated by Rohoon Six Sigma Skill | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>",
        style=ParagraphStyle('Footer', fontSize=8, textColor=colors.gray)
    )
    story.append(footer)
    
    doc.build(story)
    print(f"✅ DOE Full Factorial Report generated: {output_path}")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', '-o', default='/tmp/doe_report.pdf')
    args = parser.parse_args()
    
    # Test data
    design_info = {'factors': 2, 'runs': 4, 'center_points': 0}
    effects = {'A1': 5.0, 'A2': 10.0, 'A1A2': 0.0}
    anova_results = {
        'effects': {
            'A1': {'ss': 100, 'ms': 100, 'f': 25, 'p': 0.001, 'significant': True},
            'A2': {'ss': 400, 'ms': 400, 'f': 100, 'p': 0.0001, 'significant': True},
            'A1A2': {'ss': 0, 'ms': 0, 'f': 0, 'p': 1.0, 'significant': False},
        }
    }
    responses = np.array([40, 50, 45, 55])
    
    generate_doe_full_factorial_report(args.output, design_info, effects, anova_results, responses)
