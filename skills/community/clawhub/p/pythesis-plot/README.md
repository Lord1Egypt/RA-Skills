# 📊 PyThesisPlot

> **Scientific Plotting Skill for Claude Code** — Transform raw data into publication-ready figures with Nature/Science quality standards.

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/stephenlzc/pythesis-plot)](https://github.com/stephenlzc/pythesis-plot/releases)
[![中文](https://img.shields.io/badge/中文-README-red.svg)](README.zh-CN.md)

---

## 🎯 What is PyThesisPlot?

PyThesisPlot is a **Claude Code Skill** that teaches AI assistants how to create publication-quality scientific figures from raw data. It provides:

- 📊 **Intelligent Workflow**: Data → Analysis → Recommendations → Confirmation → Figures
- 🎨 **Journal-Ready Output**: 300 DPI, Nature/Science style compliance
- 🔬 **Multi-Domain Support**: Biology, Psychology, Economics, Chemistry
- 📁 **Organized Output**: Timestamped directories with reproducible code

**Trigger**: When you upload data files (CSV/Excel/TXT) and ask for plots, charts, or figures.

---

## 📦 Installation

### For Humans

Copy and paste this to your AI assistant (Claude Code, Cursor, etc.):

```
Install PyThesisPlot skill for me:
https://github.com/stephenlzc/pythesis-plot
```

Or if you enjoy YAML-induced headaches, read the [Installation Guide](docs/installation.md). But seriously, let the agent handle it. Humans copy-paste paths wrong.

### For LLM Agents

```bash
git clone https://github.com/stephenlzc/pythesis-plot.git ~/.claude/skills/pythesis-plot
pip install pandas matplotlib seaborn openpyxl numpy scipy
```

**Full instructions**: [docs/installation.md](docs/installation.md)

---

## 🚀 Skip This README

We're past the era of manual plotting. Just paste this into your agent:

```
I have some data and need publication-ready figures for my thesis. 
Use PyThesisPlot skill to help me:
https://github.com/stephenlzc/pythesis-plot
```

---

## 🚀 Quick Start

Once installed, simply upload your data and ask:

> "**Help me create some charts for my thesis**"

> "**Plot this data for my scientific paper**"

> "**Generate publication-ready figures from this Excel file**"

The skill will automatically:
1. **Analyze** your data structure and types
2. **Recommend** appropriate chart types
3. **Wait for your confirmation** on chart selection
4. **Generate** 300 DPI PNG figures + reproducible Python code

---

## 📋 Skill Structure

```
pythesis-plot/
├── SKILL.md                          # Skill definition (trigger conditions)
├── README.md                         # This file
├── README.zh-CN.md                   # Chinese documentation
├── scripts/
│   ├── workflow.py                   # Main orchestrator
│   ├── data_analyzer.py              # Data analysis engine
│   └── plot_generator.py             # Figure generation engine
├── references/
│   ├── workflow_guide.md             # Workflow documentation
│   ├── chart_types.md                # Chart selection guide
│   ├── style_guide.md                # Visual standards
│   └── examples.md                   # Code examples
└── assets/themes/
    ├── academic.mplstyle             # Academic journal style
    ├── nature.mplstyle               # Nature journal style
    └── presentation.mplstyle         # Presentation style
```

---

## 🎨 Supported Chart Types

| Chart Type | Best For | Example Use Case |
|:----------:|:---------|:-----------------|
| 📈 Line Plot | Time series, Trends | Gene expression over time |
| 📊 Bar Chart | Group comparisons | Treatment vs Control |
| 🎯 Box Plot | Distribution, Outliers | qPCR Ct values |
| ⚡ Scatter + Regression | Correlations | Dose-response relationships |
| 🔥 Heatmap | Correlation matrices | Multi-gene expression |
| 📋 Dashboard | Multi-panel figures | Complete study overview |

---

## 💡 Example Use Cases

### Example 1: Biomedical Research (qPCR Data)

```
User: "I have qPCR data for my PCOS study. Help me create figures."

AI: Analyzing Mouse_PCOS_BRAC1_RawData_108.xlsx...
    Detected: 108 samples, 3 groups, gene expression data
    
    Recommended Charts:
    1. Body weight comparison (bar chart)
    2. BRAC1 expression levels (log scale bar chart)
    3. qPCR Ct distributions (box plot)
    4. Comprehensive 2×2 dashboard

User: "Generate all of them"

AI: ✅ Generated 4 publication-ready figures in output/20250312-143052-PCOS/
```

### Example 2: Psychology RCT Study

```
User: "Plot my mental health intervention results"

AI: Analyzing Adolescent_Mental_Health_Intervention_1200.xlsx...
    Detected: 1200 participants, 4-arm RCT, pre/post measurements
    
    Recommended Charts:
    1. CONSORT-style study flow
    2. SDQ pre/post comparison
    3. Responder analysis (stacked bar)
    4. Effect size forest plot

User: "Generate schemes 1, 2, and 3"

AI: ✅ Generated 3 figures with statistical annotations
```

---

## ⚙️ How It Works

### 1. Skill Trigger

The skill activates when the YAML `description` in `SKILL.md` matches your request:

```yaml
---
name: pythesis-plot
description: Python scientific plotting tool... 
  Triggers when users upload data files (txt/md/excel/csv) 
  and mention "help me plot", "create chart", "data visualization", 
  "thesis figure", "scientific plotting"...
---
```

### 2. Workflow Stages

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Data Upload │────▶│  Analysis   │────▶│Recommendations│
└─────────────┘     └─────────────┘     └──────┬──────┘
                                                │
                                                ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Delivery  │◀────│ Generation  │◀────│Confirmation │
│  (PNG+Code) │     │             │     │  (Required) │
└─────────────┘     └─────────────┘     └─────────────┘
```

### 3. Output Organization

All outputs saved to timestamped directory:

```
output/
└── 20250312-143052-your-data/
    ├── 20250312-143052-your-data.csv    # Original data (renamed)
    ├── analysis_report.md               # Data analysis report
    ├── plot_config.json                 # Chart configuration
    ├── 20250312-143052_plot.py          # Reproducible Python code
    └── *.png                            # 300 DPI figures
```

---

## 📖 Documentation

- **[Workflow Guide](references/workflow_guide.md)** — Complete workflow walkthrough
- **[Chart Types](references/chart_types.md)** — When to use which chart
- **[Style Guide](references/style_guide.md)** — Color schemes and visual standards
- **[Examples](references/examples.md)** — Code examples and tutorials

---

## 🔧 Dependencies

```bash
pip install pandas matplotlib seaborn openpyxl numpy scipy
```

---

## 🤝 Contributing

Contributions welcome! This skill follows the standard SKILL.md format:

1. **Fork** this repository
2. **Modify** SKILL.md or add new chart types
3. **Test** with sample data
4. **Submit** a Pull Request

### Skill Format

```yaml
---
name: pythesis-plot
description: | 
  Clear trigger conditions for when AI should load this skill.
  List specific phrases and contexts.
---

# Skill Body

## Quick Start
Brief instructions...

## Features
- Feature 1
- Feature 2
```

---

## 🌐 Languages

- **English**: [README.md](README.md) (this file)
- **中文**: [README.zh-CN.md](README.zh-CN.md)

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- 🎨 Color palettes from [Nature](https://www.nature.com/) and [Science](https://www.science.org/) style guides
- 📊 Visualization practices from [Seaborn](https://seaborn.pydata.org/)
- 🎓 Academic standards from [Matplotlib](https://matplotlib.org/)

---

<div align="center">

**Made with ❤️ for Researchers**

[⬆ Back to Top](#-pythesisplot)

</div>
