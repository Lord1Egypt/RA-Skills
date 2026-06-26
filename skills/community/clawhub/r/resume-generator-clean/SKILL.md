---
name: resume-generator
version: 1.1.0
description: Professional resume generator with PDF, Word, and HTML export. Supports multiple templates, auto-layout, Chinese/English bilingual, and Markdown/HTML input. Perfect for academic and professional CVs.
author: 31504254
license: MIT
---

# Resume Generator

A professional resume generator skill for creating beautiful, print-ready resumes with multiple export formats (PDF, Word, HTML) and full Chinese character support.

## Features

- **Multiple Export Formats**: PDF, Word (.docx), and HTML
- **PDF Generation**: 
  - Direct PDF generation using ReportLab
  - HTML-to-PDF conversion (WeasyPrint, pdfkit, ReportLab, FPDF)
- **Word Export**: Generate editable .docx files
- **Chinese Support**: Full Chinese character rendering with system fonts
- **Multiple Templates**: Modern, classic, and minimal styles
- **Auto Layout**: Smart pagination and content organization
- **Professional Design**: Clean typography with visual hierarchy
- **Flexible Input**: Support YAML config, Markdown, and HTML

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/resume-generator.git

# Install dependencies
pip install reportlab pyyaml python-docx beautifulsoup4

# Optional: For better PDF quality from HTML
pip install weasyprint pdfkit

# Register with OpenClaw
openclaw skills install resume-generator
```

## Quick Start

### Method 1: Generate from YAML Config

```bash
# Generate from config file
python generate_resume.py --config resume_config.yaml --output resume.pdf

# Use specific template
python generate_resume.py --config config.yaml --template modern_blue --output resume.pdf
```

### Method 2: Convert HTML to PDF

```bash
# Convert HTML resume to PDF
python scripts/resume_to_pdf.py input.html output.pdf

# Use specific template
python scripts/resume_to_pdf.py input.html output.pdf --template modern
```

### Method 3: Convert HTML/Markdown to Word

```bash
# Convert HTML to Word
python scripts/resume_to_docx.py input.html output.docx

# Convert Markdown to Word
python scripts/resume_to_docx.py input.md output.docx --markdown
```

### Method 4: Python API

```python
from scripts.resume_pdf import ResumePDFGenerator

# Create generator
gen = ResumePDFGenerator(theme='modern_blue')

# Add content
gen.add_header(
    name="张三",
    title="高级工程师",
    phone="138-0000-0000",
    email="example@example.com",
    address="北京市海淀区示例路1号"
)

gen.add_section("工作经历", [
    {
        "title": "高级工程师",
        "org": "某某科技有限公司",
        "period": "2020-至今",
        "detail": "软件开发 · 系统架构设计"
    }
])

# Generate PDF
gen.save("resume.pdf")
```

## Export Methods

### 1. Direct PDF Generation (ReportLab)

Best for programmatic resume creation from Python:

```python
from scripts.resume_pdf import ResumePDFGenerator

gen = ResumePDFGenerator(theme='modern_blue')
gen.add_header(...)
gen.add_section(...)
gen.save("output.pdf")
```

### 2. HTML to PDF Conversion

Best for converting existing HTML resumes:

```bash
# Tries multiple PDF backends automatically
python scripts/resume_to_pdf.py resume.html output.pdf

# Supported backends (auto-detected):
# - WeasyPrint (best quality)
# - pdfkit (requires wkhtmltopdf)
# - ReportLab (fallback)
# - FPDF (fallback)
```

### 3. Markdown/Word Export

Best for creating editable documents:

```bash
# Markdown to Word
python scripts/resume_to_docx.py resume.md output.docx --markdown

# HTML to Word
python scripts/resume_to_docx.py resume.html output.docx
```

## Templates

### modern_blue
- Deep blue color scheme (#1e3a5f)
- Clean header with contact grid
- Blue section dividers
- Professional academic style

### classic
- Traditional black and white
- Conservative layout
- Standard section ordering

### minimal
- Ultra-clean design
- Minimal color usage
- Maximum content density

## Configuration Format

```yaml
name: "张三"
title: "高级工程师 · 某某科技有限公司"
contact:
  phone: "138-0000-0000"
  email: "example@example.com"
  address: "北京市海淀区示例路1号"

sections:
  - title: "工作经历"
    items:
      - title: "高级工程师"
        org: "某某科技有限公司"
        period: "2020-至今"
        detail: "软件开发 · 系统架构设计"
  
  - title: "教育背景"
    items:
      - title: "计算机科学硕士"
        org: "某某大学"
        period: "2010-2013"
        detail: "导师：某某教授"

  - title: "发表论文"
    type: "publications"
    items:
      - "[1] Author et al. Paper title[J]. Journal, Year."
      - "[2] ..."
```

## API Reference

### ResumePDFGenerator Class

```python
class ResumePDFGenerator:
    def __init__(self, theme='modern_blue'):
        """Initialize with theme name."""
    
    def add_header(self, name, title, phone, email, address):
        """Add resume header."""
    
    def add_section(self, title, items):
        """Add a content section."""
    
    def add_publications(self, papers):
        """Add publications section."""
    
    def save(self, output_path):
        """Generate and save PDF."""
```

### HTML to PDF Functions

```python
from scripts.resume_to_pdf import generate_pdf

# Convert HTML file to PDF
generate_pdf('input.html', 'output.pdf', template='modern')

# Convert HTML string to PDF
html_content = "<h1>Name</h1><p>Content...</p>"
generate_pdf(html_content, 'output.pdf', template='classic')
```

### HTML/Markdown to Word

```python
from scripts.resume_to_docx import generate_docx, generate_docx_from_markdown

# HTML to Word
generate_docx('input.html', 'output.docx', template='modern')

# Markdown to Word
generate_docx_from_markdown('input.md', 'output.docx', template='classic')
```

## Examples

See `examples/` directory for complete resume samples:
- `example_resume.yaml` - Academic researcher CV
- `academic_cv.yaml` - Academic CV with publications
- `professional_resume.yaml` - Industry resume
- `minimal_resume.yaml` - One-page minimal design

## Directory Structure

```
resume-generator/
├── SKILL.md              # Skill documentation
├── README.md             # Project readme
├── LICENSE               # MIT License
├── generate_resume.py    # Main CLI entry point
├── requirements.txt      # Python dependencies
├── scripts/
│   ├── resume_pdf.py     # Direct PDF generation (ReportLab)
│   ├── resume_to_pdf.py  # HTML to PDF conversion
│   └── resume_to_docx.py # HTML/Markdown to Word
├── examples/
│   └── example_resume.yaml
└── assets/
    └── templates/        # HTML templates
```

## Advanced Usage

### Custom Styling

```python
from scripts.resume_pdf import ResumePDFGenerator

# Use custom colors
gen = ResumePDFGenerator(
    theme='modern_blue',
    primary_color='#1e3a5f',
    accent_color='#2c5282'
)
```

### Multi-page Layout

The generator automatically handles pagination:
- Header repeats on each page
- Smart section breaks
- Balanced content distribution

### Batch Processing

```bash
# Generate multiple resumes
for file in configs/*.yaml; do
    python generate_resume.py --config "$file" --output "output/$(basename $file .yaml).pdf"
done
```

## Troubleshooting

### Chinese Characters Not Displaying

Ensure you have Chinese fonts installed:
- macOS: `/System/Library/Fonts/STHeiti Medium.ttc`
- Linux: Install `fonts-wqy-microhei`
- Windows: SimHei or Microsoft YaHei

### PDF Generation Fails

The skill will automatically fallback to HTML output if PDF libraries are unavailable. Open the HTML in browser and print to PDF.

### Word Export Issues

Make sure `python-docx` is installed:
```bash
pip install python-docx beautifulsoup4
```

## Dependencies

Required:
- `reportlab` - PDF generation
- `pyyaml` - YAML config parsing
- `python-docx` - Word document generation
- `beautifulsoup4` - HTML parsing

Optional (for better PDF quality):
- `weasyprint` - High-quality HTML to PDF
- `pdfkit` - wkhtmltopdf wrapper

## License

MIT License - See LICENSE file for details.

## Contributing

Pull requests welcome! Please follow the existing code style and add tests for new features.

## Changelog

### v1.1.0
- Added HTML to PDF conversion (multiple backends)
- Added HTML/Markdown to Word export
- Enhanced template system
- Improved Chinese font support

### v1.0.0
- Initial release
- Direct PDF generation with ReportLab
- YAML config support
- Multiple themes
