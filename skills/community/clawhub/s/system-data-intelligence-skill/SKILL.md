---
name: system-data-intelligence
description: >
  专为需要直接操作系统应用并进行深度数据分析的场景设计。

  【强制触发场景】：
  - 用户提及 Excel、WPS、Word、TXT、Markdown、RTZ 等文件的读取/写入/操控
  - 用户想从任何应用中「抓取」「提取」「获取」数据
  - 用户需要对数据进行「深度分析」「趋势研究」「异常检测」「预测」
  - 用户要求生成「图表」「可视化」「仪表盘」「数据报告」
  - 用户说「帮我看看这个文件里...」「分析一下这份数据...」「做个图表展示..."
  - 任何涉及跨应用数据流转的任务

  【核心能力】：系统接口调用 × 数据深度分析 × 专业可视化

  IMPORTANT: 只要涉及文件操作、数据分析、可视化中的任何一项，必须使用此 skill。
  不要因为任务「看起来简单」就跳过——底层接口调用有很多坑，skill 里有避坑指南。
---

# System Data Intelligence Skill

## 🔍 快速决策树

收到任务时，先判断类型：

```
用户任务
  ├─ 涉及文件/应用操作？
  │    ├─ Windows → 走 [WIN-PATH]
  │    ├─ macOS   → 走 [MAC-PATH]
  │    └─ Linux   → 走 [LINUX-PATH]
  ├─ 纯数据分析（已有数据）？→ 走 [ANALYSIS-PATH]
  └─ 数据可视化？→ 走 [VIZ-PATH]
```

遇到组合型任务（最常见）：**先读文件 → 再分析 → 最后可视化**。

---

## [WIN-PATH] Windows 系统接口调用

### 优先级顺序
1. **Python + win32com**（Excel/Word/WPS 首选，功能最全）
2. **PowerShell + COM**（系统级操作，无需 Python 环境）
3. **openpyxl / python-docx**（离线解析，不依赖应用程序）
4. **pywinauto**（GUI 自动化，万不得已时使用）

### Excel / WPS Spreadsheet
```python
# 执行: python scripts/win_excel_reader.py <filepath> [sheet_name]
```

### Word / WPS Writer
```python
# 执行: python scripts/doc_parser.py <filepath>
```

### 关键注意点
- 操作完成后**必须**调用 `Quit()` 释放 COM 进程
- WPS 的 COM 名称：`"KET.Application"`（表格）/ `"KWPS.Application"`（文字）
- 大文件（>50MB）使用 `openpyxl` 的 `read_only=True` 模式

> 详细 API 手册 → [references/windows-api.md](references/windows-api.md)

---

## [MAC-PATH] macOS 系统接口调用

### 优先级顺序
1. **Python + xlwings**（Excel for Mac 首选）
2. **AppleScript / JXA**（系统原生，稳定可靠）
3. **python-docx / openpyxl**（离线解析）
4. **subprocess + osascript**（调用系统命令）

### Excel for Mac
```python
# 执行: python scripts/mac_excel_reader.py <filepath> [sheet_name]
```

### 关键注意点
- 首次调用 AppleScript 需要「辅助功能」授权
- 提示用户在「系统设置 → 隐私与安全性 → 辅助功能」开启权限

> 详细 API 手册 → [references/macos-api.md](references/macos-api.md)

---

## [LINUX-PATH] Linux 系统接口调用

### 优先级顺序
1. **openpyxl / python-docx**（Excel/Word 首选，无需应用程序）
2. **LibreOffice headless**（老格式 .doc/.xls 转换）
3. **pandas + xlrd**（旧版 Excel 离线解析）
4. **pdfplumber / pymupdf**（PDF 提取）

### Excel / CSV 数据
```python
# 执行: python scripts/doc_parser.py <filepath>
# 支持 .xlsx .xls .xlsm .csv （无需 Office）
```

### 老格式转换（.doc / .xls）
```bash
# LibreOffice headless 转换为现代格式
libreoffice --headless --convert-to xlsx input.xls --outdir /tmp/
libreoffice --headless --convert-to docx input.doc --outdir /tmp/
```

### 关键注意点
- Linux 无 COM/AppleScript，一律用 Python 库离线解析
- 老格式文件先用 LibreOffice headless 转换再读取
- 中文内容需要安装 CJK 字体：`sudo apt install fonts-noto-cjk`

> 详细 API 手册 → [references/linux-api.md](references/linux-api.md)

---

## [ANALYSIS-PATH] 数据深度分析

### 分析层次（从浅到深）

```
Level 1: 描述性分析   → 数据现状是什么？（均值、分布、缺失率）
Level 2: 诊断性分析   → 为什么会这样？（相关性、异常根因）
Level 3: 预测性分析   → 未来会怎样？（趋势、预测模型）
Level 4: 规范性分析   → 应该怎么做？（优化建议、决策支持）
```

### 标准分析流水线
```python
# 执行完整分析
# python scripts/deep_analyzer.py <csv_or_excel_path> [date_col] [value_col]
```

脚本输出：
- `outputs/analysis_result.json` — 结构化分析报告
- `outputs/summary.md` — 文字洞察摘要

> 详细分析模式 → [references/viz-patterns.md](references/viz-patterns.md)

---

## [VIZ-PATH] 数据可视化

### 图表选型

```
数据关系类型
  ├─ 时间趋势        → 折线图 / 面积图
  ├─ 类别比较        → 柱状图 / 条形图 / 雷达图
  ├─ 部分与整体      → 饼图 / 旭日图 / 树状图
  ├─ 分布情况        → 箱线图 / 直方图 / 小提琴图
  ├─ 相关关系        → 散点图 / 热力图
  └─ 多维关系        → 平行坐标 / 桑基图
```

### 可视化执行
```python
# 生成交互式仪表盘
# python scripts/viz_engine.py <analysis_result.json> <output_dir>
```

输出：`report.html`（交互版）+ `charts/*.png`（静态版）

> 图表模板与最佳实践 → [references/viz-patterns.md](references/viz-patterns.md)

---

## ⚡ 自动文件格式检测

不确定文件格式时，使用统一入口：

```python
from scripts.doc_parser import detect_and_load
df = detect_and_load("/path/to/any/file")
```

支持格式：`.xlsx` `.xls` `.xlsm` `.et` `.docx` `.doc` `.wps` `.txt` `.md` `.rtz` `.csv` `.json`

---

## 📤 输出规范

每次任务完成必须输出：

1. **数据摘要卡片**（≤5 行关键洞察，Markdown 格式）
2. **可视化文件**（HTML 交互版 + PNG 静态版）
3. **结构化数据**（JSON / CSV，供后续使用）
4. **操作日志**（记录调用接口与数据量）

输出路径：`outputs/report_YYYYMMDD_HHMMSS/`

---

## 💡 心法

> **不要问用户想要什么格式——直接给最好的那个。**
> 收到文件就分析，分析完就可视化，可视化完就生成报告。
> 每一步都留下日志，每一步都输出可下载文件。
> 用户说「分析一下」，你就给他一份完整的数据故事。
