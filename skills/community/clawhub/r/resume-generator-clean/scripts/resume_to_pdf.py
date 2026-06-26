#!/usr/bin/env python3
"""
Resume to PDF Converter
Generates professional PDF resumes from HTML or text input.
"""

import sys
import os
from pathlib import Path

def generate_pdf(input_file, output_file, template='modern'):
    """
    Convert HTML resume to PDF.
    
    Args:
        input_file: Path to HTML file or raw HTML string
        output_file: Path for output PDF
        template: Template name (modern, classic, minimal)
    """
    # Try multiple methods in order of preference
    methods = [
        _try_weasyprint,
        _try_pdfkit,
        _try_reportlab,
        _try_fpdf
    ]
    
    for method in methods:
        try:
            result = method(input_file, output_file, template)
            if result:
                return True
        except Exception as e:
            print(f"Method {method.__name__} failed: {e}")
            continue
    
    # If all methods fail, create a placeholder with instructions
    _create_fallback(input_file, output_file)
    return False

def _try_weasyprint(input_file, output_file, template):
    """Try using WeasyPrint for PDF generation."""
    try:
        from weasyprint import HTML, CSS
        
        html_content = _get_html_content(input_file)
        css_content = _get_template_css(template)
        
        HTML(string=html_content).write_pdf(
            output_file,
            stylesheets=[CSS(string=css_content)]
        )
        print(f"PDF generated using WeasyPrint: {output_file}")
        return True
    except ImportError:
        return False

def _try_pdfkit(input_file, output_file, template):
    """Try using pdfkit (wkhtmltopdf wrapper)."""
    try:
        import pdfkit
        
        html_content = _get_html_content(input_file)
        options = {
            'page-size': 'A4',
            'margin-top': '20mm',
            'margin-right': '20mm',
            'margin-bottom': '20mm',
            'margin-left': '20mm',
            'encoding': 'UTF-8',
            'enable-local-file-access': None
        }
        
        pdfkit.from_string(html_content, output_file, options=options)
        print(f"PDF generated using pdfkit: {output_file}")
        return True
    except ImportError:
        return False

def _try_reportlab(input_file, output_file, template):
    """Try using ReportLab for PDF generation."""
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        
        doc = SimpleDocTemplate(
            output_file,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        styles = getSampleStyleSheet()
        story = []
        
        # Parse HTML and convert to ReportLab elements
        html_content = _get_html_content(input_file)
        text_content = _html_to_text(html_content)
        
        # Add content as simple paragraphs
        lines = text_content.split('\n')
        for line in lines:
            line = line.strip()
            if line:
                if line.startswith('# '):
                    # Title
                    p = Paragraph(line[2:], styles['Title'])
                elif line.startswith('## '):
                    # Section header
                    p = Paragraph(line[3:], styles['Heading2'])
                else:
                    p = Paragraph(line, styles['Normal'])
                story.append(p)
                story.append(Spacer(1, 0.2*cm))
        
        doc.build(story)
        print(f"PDF generated using ReportLab: {output_file}")
        return True
    except ImportError:
        return False

def _try_fpdf(input_file, output_file, template):
    """Try using FPDF for PDF generation."""
    try:
        from fpdf import FPDF
        
        class ResumePDF(FPDF):
            def header(self):
                pass
            
            def footer(self):
                self.set_y(-15)
                self.set_font('Arial', 'I', 8)
                self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
        
        pdf = ResumePDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        html_content = _get_html_content(input_file)
        text_content = _html_to_text(html_content)
        
        pdf.set_font('Arial', '', 11)
        
        lines = text_content.split('\n')
        for line in lines:
            line = line.strip()
            if line:
                if line.startswith('# '):
                    pdf.set_font('Arial', 'B', 16)
                    pdf.cell(0, 10, line[2:], ln=True)
                    pdf.ln(5)
                elif line.startswith('## '):
                    pdf.set_font('Arial', 'B', 14)
                    pdf.cell(0, 8, line[3:], ln=True)
                    pdf.ln(3)
                else:
                    pdf.set_font('Arial', '', 11)
                    pdf.multi_cell(0, 6, line)
                    pdf.ln(2)
        
        pdf.output(output_file)
        print(f"PDF generated using FPDF: {output_file}")
        return True
    except ImportError:
        return False

def _create_fallback(input_file, output_file):
    """Create a fallback HTML file when PDF generation fails."""
    html_content = _get_html_content(input_file)
    
    # Add print-friendly CSS
    enhanced_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Resume - Print Version</title>
<style>
    @media print {{
        body {{ margin: 0; padding: 20px; }}
        .no-print {{ display: none; }}
    }}
    body {{
        font-family: 'Segoe UI', 'Microsoft YaHei', Arial, sans-serif;
        max-width: 800px;
        margin: 40px auto;
        padding: 30px;
        line-height: 1.6;
        color: #333;
    }}
    h1 {{
        color: #2c3e50;
        border-bottom: 3px solid #3498db;
        padding-bottom: 10px;
    }}
</style>
</head>
<body>
    <div class="no-print" style="background: #fff3cd; padding: 15px; margin-bottom: 20px; border-radius: 5px;">
        <strong>Note:</strong> PDF libraries not available. Please use browser print to save as PDF:<br>
        1. Press Ctrl+P (or Cmd+P on Mac)<br>
        2. Select "Save as PDF" as destination<br>
        3. Click Save
    </div>
    {html_content}
</body>
</html>"""
    
    # Save as HTML instead
    html_output = output_file.replace('.pdf', '_print.html')
    with open(html_output, 'w', encoding='utf-8') as f:
        f.write(enhanced_html)
    
    print(f"\nPDF generation requires additional libraries.")
    print(f"Created print-ready HTML instead: {html_output}")
    print(f"Open this file in browser and press Ctrl+P to save as PDF.\n")

def _get_html_content(input_file):
    """Read HTML content from file or return as-is if it's already HTML."""
    if os.path.isfile(input_file):
        with open(input_file, 'r', encoding='utf-8') as f:
            return f.read()
    return input_file

def _html_to_text(html_content):
    """Simple HTML to text conversion."""
    import re
    
    # Remove style tags and content
    text = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL)
    
    # Convert common tags to text markers
    text = re.sub(r'<h1[^>]*>', '# ', text, flags=re.IGNORECASE)
    text = re.sub(r'<h2[^>]*>', '## ', text, flags=re.IGNORECASE)
    text = re.sub(r'<h3[^>]*>', '### ', text, flags=re.IGNORECASE)
    text = re.sub(r'<li[^>]*>', '- ', text, flags=re.IGNORECASE)
    
    # Remove all remaining HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Clean up whitespace
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'&amp;', '&', text)
    
    return text.strip()

def _get_template_css(template_name):
    """Get CSS for specified template."""
    templates = {
        'modern': '''
            body { font-family: 'Segoe UI', Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 30px; line-height: 1.6; color: #333; }
            h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
            h2 { color: #34495e; margin-top: 25px; border-left: 4px solid #3498db; padding-left: 10px; }
        ''',
        'classic': '''
            body { font-family: 'Times New Roman', serif; max-width: 800px; margin: 40px auto; padding: 30px; line-height: 1.6; }
            h1 { color: #000; border-bottom: 2px solid #000; text-align: center; }
            h2 { color: #333; margin-top: 25px; border-bottom: 1px solid #ccc; }
        ''',
        'minimal': '''
            body { font-family: 'Helvetica Neue', Arial, sans-serif; max-width: 700px; margin: 40px auto; padding: 20px; line-height: 1.5; color: #222; }
            h1 { font-size: 28px; font-weight: 300; border-bottom: 1px solid #ddd; }
            h2 { font-size: 18px; font-weight: 400; color: #555; margin-top: 30px; text-transform: uppercase; }
        '''
    }
    return templates.get(template_name, templates['modern'])

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python resume_to_pdf.py <input.html> <output.pdf> [--template modern|classic|minimal]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    template = 'modern'
    if '--template' in sys.argv:
        idx = sys.argv.index('--template')
        if idx + 1 < len(sys.argv):
            template = sys.argv[idx + 1]
    
    success = generate_pdf(input_file, output_file, template)
    
    if success:
        print(f"\n✓ Resume PDF created: {output_file}\n")
    else:
        print(f"\n⚠ Created print-ready HTML (PDF libraries not available)\n")
