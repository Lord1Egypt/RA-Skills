# AGENTS.md — skill-data-intelligence

> 本文件遵循 AGENTS.md 规范，供任意 AI Agent（OpenClaw、Claude、GPT、Gemini 等）直接学习并使用本 Skill。

---

## 🧠 Skill 身份

你是一个拥有三大能力的数据智能助手：

| 能力 | 支持 |
|---|---|
| 🔧 系统文件操作 | Windows COM / macOS xlwings / Linux openpyxl |
| 📊 数据深度分析 | pandas / numpy / scipy / statsmodels |
| 🎨 专业可视化 | Plotly（交互）/ Matplotlib（报告级） |

**支持所有三大操作系统：Windows / macOS / Linux**

---

## 🎯 需要强制触发本 Skill 的场景

- 用户要操作任何文件：`.xlsx` `.xls` `.csv` `.docx` `.doc` `.wps` `.txt` `.md` `.rtz` `.json`
- 用户要对数据进行分析、建模、预测、异常检测
- 用户要生成图表、仪表盘、可视化报告
- 用户说「帮我分析」「读取这个文件」「做个图表」等

---

## 🔄 框架内应遵循的工作流程

### Step 1 — 判断操作系统

```python
import platform
OS = platform.system()  # 'Windows' | 'Darwin' | 'Linux'
```

### Step 2 — 选择最优文件读取策略

| 操作系统 | Excel/WPS | Word/WPS | 老格式 (.xls/.doc) |
|---|---|---|---|
| **Windows** | `win32com` → `openpyxl` 降级 | `win32com` → `python-docx` 降级 | COM 直接读取 |
| **macOS** | `xlwings` → `openpyxl` 降级 | `python-docx` | LibreOffice 转换 |
| **Linux** | `openpyxl` | `python-docx` | LibreOffice headless 转换 |

### Step 3 — 分析 → 可视化流水线

```python
# 1. 读数据
from scripts.doc_parser import detect_and_load
data = detect_and_load(filepath)

# 2. 分析
from scripts.deep_analyzer import DeepAnalyzer
report = DeepAnalyzer(df).run_full_analysis()

# 3. 可视化
from scripts.viz_engine import create_dashboard, export_viz
fig = create_dashboard(report)
export_viz(fig, 'outputs/report')
```

---

## 📊 分析层次框架

```
Level 1: 描述性   → 数据现状是什么？
Level 2: 诊断性   → 为什么会这样？
Level 3: 预测性   → 未来会怎样？
Level 4: 规范性   → 应该怎么做？
```

---

## 📤 输出要求

每次分析任务必须输出：

```
outputs/
├── report_YYYYMMDD_HHMMSS.html   ← Plotly 交互报告
├── report_YYYYMMDD_HHMMSS.png    ← Matplotlib 静态图
├── analysis_result.json          ← 结构化分析数据
└── summary.md                    ← 不超过5行的关键洞察
```

---

## 🛠️ 可用脚本列表

| 脚本 | 功能 | 调用方式 |
|---|---|---|
| `scripts/doc_parser.py` | 自动检测并加载任意文件 | `python scripts/doc_parser.py <file>` |
| `scripts/deep_analyzer.py` | 4级数据分析 | `python scripts/deep_analyzer.py <file> [date_col] [value_col]` |
| `scripts/viz_engine.py` | 生成交互式仪表盘 | `python scripts/viz_engine.py <analysis.json> <output_dir>` |
| `scripts/win_excel_reader.py` | Windows COM 读取 Excel | `python scripts/win_excel_reader.py <file> [sheet]` |
| `scripts/mac_excel_reader.py` | macOS xlwings 读取 Excel | `python scripts/mac_excel_reader.py <file> [sheet]` |
| `scripts/wps_extractor.py` | WPS 文件提取 | `python scripts/wps_extractor.py <file>` |

---

## 💻 安装依赖

```bash
# 全平台通用
pip install pandas numpy scipy statsmodels plotly matplotlib openpyxl python-docx chardet

# Windows 额外
pip install pywin32

# macOS 额外
pip install xlwings

# Linux 额外
pip install pdfplumber           # PDF 支持
sudo apt install libreoffice-nogui fonts-noto-cjk  # LibreOffice + 中文字体
```

---

## 🔧 关键避坑指南

| 场景 | 注意点 |
|---|---|
| Windows COM | 必须调用 `Quit()` 防止进程残留 |
| macOS AppleScript | 首次需要开启「辅助功能」权限 |
| Linux 可视化 | 无头服务器需要设置 `matplotlib.use('Agg')` |
| WPS COM | 名称与 Office 不同：`KET.Application`（表格）/ `KWPS.Application`（文字）|
| 大文件 >50MB | `openpyxl` 使用 `read_only=True` 模式 |
| 中文 CSV | 指定 `encoding='utf-8-sig'` 处理 Windows BOM |

---

## 📚 参考文件

| 文件 | 内容 |
|---|---|
| [SKILL.md](SKILL.md) | Cursor 专用 Skill 入口，含决策树 |
| [references/windows-api.md](references/windows-api.md) | Windows COM / PowerShell 详细手册 |
| [references/macos-api.md](references/macos-api.md) | macOS xlwings / AppleScript 详细手册 |
| [references/linux-api.md](references/linux-api.md) | Linux openpyxl / LibreOffice 详细手册 |
| [references/file-formats.md](references/file-formats.md) | 文件格式解析指南 |
| [references/viz-patterns.md](references/viz-patterns.md) | 图表选型与样式指南 |
