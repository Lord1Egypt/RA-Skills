# Resume Generator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

A professional resume generator with multiple export formats (PDF, Word, HTML), full Chinese character support, and flexible input options.

## ✨ Features

- **Multiple Export Formats**: PDF, Word (.docx), and HTML
- **PDF Generation Options**:
  - Direct PDF generation using ReportLab
  - HTML-to-PDF conversion (WeasyPrint, pdfkit, ReportLab, FPDF)
- **Word Export**: Generate editable .docx files from Markdown or HTML
- **Chinese Support**: Complete Chinese character rendering
- **Multiple Themes**: Modern blue, classic, and minimal styles
- **Flexible Input**: YAML config, Markdown, or HTML
- **Auto Layout**: Smart pagination and content organization

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/resume-generator.git
cd resume-generator

# Install dependencies
pip install -r requirements.txt

# For OpenClaw users
openclaw skills install resume-generator
```

### Requirements

- Python 3.7+
- reportlab
- pyyaml
- python-docx
- beautifulsoup4

Optional (for better PDF quality from HTML):
- weasyprint
- pdfkit + wkhtmltopdf

## 🚀 Quick Start

### Generate from YAML Config

```bash
python generate_resume.py --config resume.yaml --output resume.pdf
```

### Convert HTML to PDF

```bash
python scripts/resume_to_pdf.py input.html output.pdf --template modern
```

### Convert Markdown to Word

```bash
python scripts/resume_to_docx.py input.md output.docx --markdown
```

### Python API

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

## 📖 Usage Examples

### Example 1: YAML to PDF

Create `resume.yaml`:

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
        period: "2014-2017"
        detail: "导师：某某教授"
```

Generate:
```bash
python generate_resume.py -c resume.yaml -o output.pdf -t modern_blue
```

### Example 2: HTML to PDF

```bash
# Convert existing HTML resume to PDF
python scripts/resume_to_pdf.py my_resume.html my_resume.pdf

# With specific template
python scripts/resume_to_pdf.py my_resume.html my_resume.pdf --template classic
```

### Example 3: Markdown to Word

```bash
# Convert Markdown resume to editable Word document
python scripts/resume_to_docx.py resume.md resume.docx --markdown
```

## 🎨 Themes

### Modern Blue (Default)
- Deep blue color scheme (#1e3a5f)
- Professional academic style
- Clean visual hierarchy

### Classic
- Traditional black and white
- Conservative layout
- Timeless design

### Minimal
- Ultra-clean design
- Minimal color usage
- Maximum content density

## 📂 Directory Structure

```
resume-generator/
├── SKILL.md              # OpenClaw skill documentation
├── README.md             # This file
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

## 🔧 Troubleshooting

### Chinese Characters Not Displaying

Install Chinese fonts:

**macOS:**
```bash
# System already has STHeiti
```

**Linux:**
```bash
sudo apt-get install fonts-wqy-microhei
```

**Windows:**
```bash
# SimHei or Microsoft YaHei should be pre-installed
```

### PDF Generation Fails

The skill will automatically fallback to HTML output if PDF libraries are unavailable. Open the HTML in browser and print to PDF.

### Missing Dependencies

```bash
# Install all required packages
pip install reportlab pyyaml python-docx beautifulsoup4

# Optional: For better HTML to PDF quality
pip install weasyprint pdfkit
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [ReportLab](https://www.reportlab.com/) for PDF generation
- Inspired by professional academic CV templates
- Created for the OpenClaw ecosystem

## 📮 OpenClaw Integration

This skill can be installed via OpenClaw:

```bash
# Install from local directory
openclaw skills install /path/to/resume-generator

# Or via clawhub (once published)
openclaw skills install resume-generator
```
