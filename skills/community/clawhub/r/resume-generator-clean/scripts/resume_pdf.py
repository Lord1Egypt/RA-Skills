#!/usr/bin/env python3
"""
Resume PDF Generator
Professional resume generator with Chinese character support.
Based on ReportLab for reliable PDF generation.
"""

import os
import sys
import yaml
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm


class ResumePDFGenerator:
    """Generate professional PDF resumes with Chinese support."""
    
    # Color schemes
    THEMES = {
        'modern_blue': {
            'primary': colors.HexColor('#1e3a5f'),
            'accent': colors.HexColor('#2c5282'),
            'light': colors.HexColor('#4a7ab8'),
            'divider': colors.HexColor('#3182ce'),
            'dark_text': colors.HexColor('#1a202c'),
            'medium_text': colors.HexColor('#4a5568'),
            'light_text': colors.HexColor('#718096'),
            'bg_light': colors.HexColor('#f7fafc'),
        },
        'classic': {
            'primary': colors.HexColor('#000000'),
            'accent': colors.HexColor('#333333'),
            'light': colors.HexColor('#666666'),
            'divider': colors.HexColor('#999999'),
            'dark_text': colors.HexColor('#000000'),
            'medium_text': colors.HexColor('#333333'),
            'light_text': colors.HexColor('#666666'),
            'bg_light': colors.HexColor('#f5f5f5'),
        }
    }
    
    def __init__(self, theme='modern_blue', font_path=None):
        """
        Initialize the generator.
        
        Args:
            theme: Color theme name ('modern_blue' or 'classic')
            font_path: Path to Chinese font file (auto-detected if None)
        """
        self.theme = self.THEMES.get(theme, self.THEMES['modern_blue'])
        self.font_path = font_path or self._find_chinese_font()
        self._register_fonts()
        self.story = []
        
    def _find_chinese_font(self):
        """Find system Chinese font."""
        possible_paths = [
            '/System/Library/Fonts/STHeiti Medium.ttc',  # macOS
            '/System/Library/Fonts/PingFang.ttc',  # macOS alternative
            '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',  # Linux
            'C:/Windows/Fonts/simhei.ttf',  # Windows
            'C:/Windows/Fonts/msyh.ttc',  # Windows alternative
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
        raise RuntimeError("No Chinese font found. Please install Chinese fonts or specify font_path.")
    
    def _register_fonts(self):
        """Register Chinese fonts with ReportLab."""
        try:
            pdfmetrics.registerFont(TTFont('ChineseFont', self.font_path))
        except Exception as e:
            print(f"Warning: Could not register font: {e}")
            pdfmetrics.registerFont(TTFont('ChineseFont', 'Helvetica'))
    
    def _create_styles(self):
        """Create paragraph styles."""
        t = self.theme
        return {
            'title': ParagraphStyle(
                'ResumeTitle',
                fontName='ChineseFont',
                fontSize=34,
                textColor=t['primary'],
                spaceAfter=10,
                leading=38
            ),
            'subtitle': ParagraphStyle(
                'ResumeSubtitle',
                fontName='ChineseFont',
                fontSize=13,
                textColor=t['accent'],
                spaceAfter=6,
                leading=16
            ),
            'contact': ParagraphStyle(
                'ResumeContact',
                fontName='ChineseFont',
                fontSize=10,
                textColor=t['medium_text'],
                spaceAfter=12,
                leading=14
            ),
            'heading': ParagraphStyle(
                'ResumeHeading',
                fontName='ChineseFont',
                fontSize=12,
                textColor=t['primary'],
                spaceAfter=2,
                spaceBefore=14,
                leading=14
            ),
            'normal': ParagraphStyle(
                'ResumeNormal',
                fontName='ChineseFont',
                fontSize=9.5,
                leading=13,
                textColor=t['dark_text']
            ),
            'small': ParagraphStyle(
                'ResumeSmall',
                fontName='ChineseFont',
                fontSize=8.5,
                leading=11,
                textColor=t['medium_text']
            ),
            'emphasis': ParagraphStyle(
                'ResumeEmphasis',
                fontName='ChineseFont',
                fontSize=9.5,
                leading=13,
                textColor=t['accent']
            ),
        }
    
    def _blue_divider(self):
        """Create a blue divider line."""
        return Table([['']], colWidths=[18*cm], style=TableStyle([
            ('LINEBELOW', (0, 0), (-1, 0), 1.5, self.theme['divider']),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 1),
        ]))
    
    def add_header(self, name, title, phone, email, address):
        """Add resume header with contact information."""
        styles = self._create_styles()
        t = self.theme
        
        header_data = [
            [Paragraph(name, styles['title'])],
            [Paragraph(title, styles['subtitle'])],
            [Paragraph(f'{phone} · {email} · {address}', styles['contact'])],
        ]
        
        header_table = Table(header_data, colWidths=[18*cm])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), t['bg_light']),
            ('TOPPADDING', (0, 0), (-1, -1), 18),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('BOX', (0, 0), (-1, -1), 0.5, t['light']),
        ]))
        
        self.story.append(header_table)
        self.story.append(Spacer(1, 0.4*cm))
    
    def add_section(self, title, items):
        """
        Add a content section.
        
        Args:
            title: Section title (e.g., "工作经历")
            items: List of dicts with keys: title, org, period, detail
        """
        styles = self._create_styles()
        t = self.theme
        
        self.story.append(Paragraph(title, styles['heading']))
        self.story.append(self._blue_divider())
        self.story.append(Spacer(1, 0.06*cm))
        
        for i, item in enumerate(items):
            primary = f"<b>{item['title']}</b> · {item['org']} · <span color='{t['accent'].hexval()}'>{item['period']}</span>"
            
            item_data = [
                ['•', Paragraph(primary, styles['normal'])],
            ]
            
            if item.get('detail'):
                item_data.append(['', Paragraph(item['detail'], styles['small'])])
            
            self.story.append(Table(
                item_data,
                colWidths=[0.4*cm, 17.6*cm],
                style=TableStyle([
                    ('ALIGN', (0, 0), (0, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (0, -1), 'TOP'),
                    ('TOPPADDING', (0, 0), (-1, -1), 0),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ])
            ))
            
            if i < len(items) - 1:
                self.story.append(Spacer(1, 0.08*cm))
        
        self.story.append(Spacer(1, 0.2*cm))
    
    def add_publications(self, papers):
        """
        Add publications section.
        
        Args:
            papers: List of paper strings
        """
        styles = self._create_styles()
        
        self.story.append(Paragraph('发表论文', styles['heading']))
        self.story.append(self._blue_divider())
        self.story.append(Spacer(1, 0.06*cm))
        
        for paper in papers:
            self.story.append(Paragraph(paper, styles['small']))
            self.story.append(Spacer(1, 0.06*cm))
        
        self.story.append(Spacer(1, 0.15*cm))
    
    def add_software(self, software_list):
        """
        Add software/copyrights section.
        
        Args:
            software_list: List of software strings
        """
        styles = self._create_styles()
        t = self.theme
        
        self.story.append(Paragraph('软件著作权', styles['heading']))
        self.story.append(self._blue_divider())
        self.story.append(Spacer(1, 0.08*cm))
        
        for sw in software_list:
            self.story.append(Paragraph(sw, styles['small']))
            self.story.append(Spacer(1, 0.06*cm))
    
    def save(self, output_path):
        """Generate and save PDF."""
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=1.5*cm,
            leftMargin=1.5*cm,
            topMargin=1.2*cm,
            bottomMargin=1.2*cm
        )
        doc.build(self.story)
        print(f"✓ Resume PDF created: {output_path}")


def generate_from_yaml(config_path, output_path, theme='modern_blue'):
    """Generate resume from YAML config file."""
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    gen = ResumePDFGenerator(theme=theme)
    
    # Add header
    gen.add_header(
        name=config['name'],
        title=config['title'],
        phone=config['contact']['phone'],
        email=config['contact']['email'],
        address=config['contact']['address']
    )
    
    # Add sections
    for section in config.get('sections', []):
        if section.get('type') == 'publications':
            gen.add_publications(section['items'])
        elif section.get('type') == 'software':
            gen.add_software(section['items'])
        else:
            gen.add_section(section['title'], section['items'])
    
    gen.save(output_path)


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate professional resume PDF')
    parser.add_argument('--config', '-c', required=True, help='Path to YAML config file')
    parser.add_argument('--output', '-o', required=True, help='Output PDF path')
    parser.add_argument('--theme', '-t', default='modern_blue', choices=['modern_blue', 'classic'],
                       help='Color theme')
    
    args = parser.parse_args()
    
    generate_from_yaml(args.config, args.output, args.theme)
