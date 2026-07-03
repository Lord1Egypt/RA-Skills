# 📊 Score Analysis Skill

AI-powered class score analysis tool for OpenClaw. Generates visualized charts and professional reports with school branding support.

[![OpenClaw Skills](https://img.shields.io/badge/OpenClaw-Skills-blue)](https://clawhub.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**[中文文档](README_CN.md)**

## ✨ Features

- 📊 **Auto-detect headers** - Supports Excel/CSV with merged cells, Chinese/English mixed headers
- 📈 **Multi-dimensional analysis** - Horizontal (peer classes) & vertical (time) comparison
- 🎯 **Critical student identification** - Near pass line analysis with radar charts
- 📉 **Subject imbalance diagnosis** - Identify students with severe subject imbalance
- 📋 **Grouped radar charts** - By student type (critical, imbalanced)
- 📄 **Professional reports** - Word format with three-line tables, embedded charts
- 🎨 **Customizable branding** - School colors, logo, header/footer

## 🚀 Quick Start

### Installation

```bash
# Via OpenClaw
openclaw skills install score-analysis

# Or manually copy to your skills directory
cp -r score-analysis ~/.openclaw/workspace/skills/
```

### Dependencies

```bash
pip install python-docx matplotlib pandas numpy openpyxl
```

### Usage

1. Provide score data (Excel/CSV)
2. Skill auto-detects headers and validates data
3. User confirms data accuracy
4. Analysis runs with charts and report generation

## 📋 Workflow

```
Data Input → Header Detection → Data Validation → Analysis → Charts → Report → PPT (optional)
                ↓                    ↓              ↓          ↓         ↓
           Auto-detect         User confirms    Multi-dim   Radar    Word doc
           format              accuracy         analysis    charts   with branding
```

## 📊 Analysis Dimensions

### Horizontal Comparison
- Total score average
- Subject averages
- Score segment distribution
- Pass line rates
- Top student distribution

### Vertical Comparison
- Average score trends
- Pass count changes
- Ranking fluctuations
- Subject score changes

### Individual Analysis
- Score stability
- Subject imbalance
- Progress/regression
- Critical student identification

## 🎨 Chart Types

| Chart | Description |
|-------|-------------|
| Subject Average Bar | Compare subject averages |
| Class Comparison | Compare with peer classes |
| Score Distribution | Score segment distribution |
| Radar (Critical) | Near pass line students |
| Radar (Imbalanced) | Subject-imbalanced students |

## 📄 Report Output

Professional Word report with:
- School logo & branding
- Three-line tables (research style)
- Embedded charts
- Highlight boxes for key conclusions
- Header/footer with page numbers

## ⚙️ Configuration

### Subject Score Rules

| Subject | Default Score Type |
|---------|-------------------|
| Chinese, Math, English, Physics | Raw score |
| Chemistry, Biology, Politics, Geography | Adjusted score |
| Total | Adjusted total |

### Customization

Edit `scripts/generate_report.py` to customize:
- School colors (line 12-19)
- Report layout
- Chart styles

## 📁 Directory Structure

```
score-analysis/
├── SKILL.md                 # Skill description
├── README.md                # This file
├── LICENSE                  # MIT License
├── scripts/
│   ├── create_template.py           # Template generator
│   ├── generate_report_from_template.py  # Report from template
│   ├── generate_radar_charts.py     # Radar chart generator
│   └── generate_report.py           # Direct report generator
├── references/
│   └── analysis_framework.md        # Analysis framework
├── assets/
│   └── report_template.docx         # Word template
└── examples/
    └── sample_data.json             # Sample data
```

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING](CONTRIBUTING.md) first.

## 📝 License

MIT License - see [LICENSE](LICENSE)

## 🙏 Acknowledgments

- Built for [OpenClaw](https://openclaw.ai) ecosystem
- Chart generation via [matplotlib](https://matplotlib.org/)
- Document generation via [python-docx](https://python-docx.readthedocs.io/)
