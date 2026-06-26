# 🧠 system-data-Intelligence

> A professional **Cursor Agent Skill** for system-level file operations, deep data analysis, and professional data visualization.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)](#)
[![Cursor Skill](https://img.shields.io/badge/Cursor-Agent%20Skill-purple)](#)
[![Agent Compatible](https://img.shields.io/badge/AGENTS.md-compatible-green)](#)

---

## 📦 What This Skill Does

This skill equips any AI agent with three tightly integrated superpowers:

| Capability | Technologies |
|---|---|
| 🔧 **System File Access** | win32com (Windows), xlwings (macOS), openpyxl/LibreOffice (Linux) |
| 📊 **Deep Data Analysis** | pandas, numpy, scipy, statsmodels |
| 🎨 **Professional Visualization** | Plotly (interactive), Matplotlib (report-quality) |

**Supported file formats:** `.xlsx` `.xls` `.xlsm` `.et` `.docx` `.doc` `.wps` `.txt` `.md` `.rtz` `.csv` `.json`

**Supported OS:** Windows / macOS / Linux

---

## 🤖 AI Agent 兼容性

本项目可供任意 AI Agent 学习和使用：

| Agent | 接入方式 |
|---|---|
| **Cursor** | 将项目复制到 `~/.cursor/skills/` 即可自动加载 |
| **OpenClaw / Claude** | 读取 [AGENTS.md](AGENTS.md) 作为系统提示词 |
| **GPT / 其他** | 将 [AGENTS.md](AGENTS.md) 内容粘贴到 System Prompt |
| **对话模式** | 直接将 [SKILL.md](SKILL.md) 内容作为提示词输入 |

核心规范文件：**[AGENTS.md](AGENTS.md)**

---

## 🗂️ Repository Structure

```
system-data-Intelligence/
├── SKILL.md                     ← Cursor skill entry point (≤500 lines)
├── AGENTS.md                    ← Universal AI agent instructions
├── references/
│   ├── windows-api.md           ← Windows COM / PowerShell reference
│   ├── macos-api.md             ← macOS xlwings / AppleScript reference
│   ├── linux-api.md             ← Linux openpyxl / LibreOffice reference
│   ├── file-formats.md          ← Excel / WPS / Word / RTZ format guide
│   └── viz-patterns.md          ← Chart selection & styling reference
├── scripts/
│   ├── win_excel_reader.py      ← Windows COM Excel reader
│   ├── mac_excel_reader.py      ← macOS xlwings Excel reader
│   ├── wps_extractor.py         ← WPS Spreadsheet & Writer extractor
│   ├── doc_parser.py            ← Universal parser (all platforms)
│   ├── deep_analyzer.py         ← Full data analysis engine
│   └── viz_engine.py            ← Plotly + Matplotlib visualization engine
├── requirements.txt
└── README.md
```

---

## 🚀 Installation

### Cursor (Personal Skill)

```bash
mkdir -p ~/.cursor/skills/system-data-intelligence
git clone https://github.com/zhaojie911272507/system-data-Intelligence.git \
  ~/.cursor/skills/system-data-intelligence
```

### OpenClaw / Claude / Other Agents

将 [AGENTS.md](AGENTS.md) 中的内容作为系统提示词输入到对话界面。

### Python Dependencies

```bash
# 全平台通用
pip install pandas numpy scipy statsmodels plotly matplotlib openpyxl python-docx chardet kaleido

# Windows
pip install pywin32

# macOS
pip install xlwings

# Linux
pip install pdfplumber
sudo apt install libreoffice-nogui fonts-noto-cjk
```

---

## 💡 Trigger Scenarios

The agent will **automatically apply** this skill when you say:

- "帮我分析这个 Excel 文件..."
- "读取 WPS 表格里的数据"
- "生成一份可视化报告"
- "分析这份销售数据的趋势"
- "提取 Word 文档中的表格"
- "解析这个 RTZ 项目文件"
- "做个仪表盘展示数据"

---

## 🔄 Workflow Example

```python
import platform
from scripts.doc_parser import detect_and_load
from scripts.deep_analyzer import DeepAnalyzer
from scripts.viz_engine import create_dashboard, export_viz

# Auto-detect OS and load file
df = detect_and_load("/path/to/sales.xlsx")

# Deep analysis
report = DeepAnalyzer(df).run_full_analysis()

# Visualization
fig = create_dashboard(report, title="Sales Intelligence Dashboard")
export_viz(fig, "outputs/sales_report", formats=["html", "png"])
```

---

## 📤 Output Format

Every analysis produces:

```
outputs/
├── report_YYYYMMDD_HHMMSS.html   ← Interactive full report
├── report_YYYYMMDD_HHMMSS.png    ← Static report image
├── analysis_result.json          ← Structured analysis data
└── summary.md                     ← Key insights (≤5 lines)
```

---

## 📚 References

- [Windows API Reference](references/windows-api.md)
- [macOS API Reference](references/macos-api.md)
- [Linux API Reference](references/linux-api.md)
- [File Formats Guide](references/file-formats.md)
- [Visualization Patterns](references/viz-patterns.md)
- [Universal Agent Instructions](AGENTS.md)

---

## 📄 License

MIT License — feel free to use, modify, and distribute.
