# Markdown → 中文 PDF 配方 v3（克制优雅版 · 仿企鹅出版社风格）

适用于纵向/横向/时空智能分析类报告（10–50KB / 14–30 页）。

## v3 设计哲学：**克制 = 优雅**

> **原则**：3 种字号 / 2 种颜色 / 1 处底色 / 大留白 / 优雅字体

| 维度 | v3 取舍 |
|------|---------|
| 字号 | 仅 3 种：14pt（章节） / 12pt（小节） / 11pt（正文） |
| 颜色 | 仅 2 色：主蓝 `#1548A0` + 中灰 `#44545F`（+ 文字黑） |
| 底色 | 仅 1 处：引用框 4% 浅蓝底 |
| 留白 | 段间 12pt（弹性 ±2pt），行高 1.5 |
| 章节比 | 章节与正文比 = 14:11 ≈ 1.27（不夸张） |

## 设计灵感

参考的优雅克制风格：
- **Penguin Random House** 非虚构书
- **Stripe Press** 白皮书
- **Notion** 官方文档
- **Apple HIG** typography 章节

共同点：**少字号 / 少颜色 / 多留白 / 一致性**。

---

## 工具链

| 工具 | 用途 |
|------|------|
| **pandoc ≥ 3.0** | Markdown → LaTeX |
| **MacTeX / TinyTeX** | xelatex + ctex |
| **PingFang SC** | macOS 自带中文 |
| **Menlo** | macOS 自带等宽 |

---

## 一键配置（v3 实测配方）

### 步骤 1：保存 `preamble_v3.tex`

```latex
\usepackage{ctex}
\usepackage{xcolor}
\usepackage{titlesec}
\usepackage{fancyhdr}
\usepackage{booktabs}
\usepackage{array}
\usepackage{colortbl}
\usepackage{enumitem}
\usepackage{tcolorbox}
\usepackage{hyperref}
\usepackage{caption}
\usepackage{tocloft}

% ===== 颜色：仅 2 色 =====
\definecolor{primary}{HTML}{1548A0}    % 主蓝
\definecolor{ink}{HTML}{182430}         % 主文字
\definecolor{ink2}{HTML}{44545F}        % 次文字
\definecolor{rule}{HTML}{C0C6CC}        % 极浅灰（仅用于细线）

% ===== PDF 链接 =====
\hypersetup{
    colorlinks=true,
    linkcolor=primary,
    citecolor=primary,
    urlcolor=primary,
    bookmarksopen=true,
    bookmarksnumbered=true,
    pdfborder={0 0 0}
}

% ===== 章节样式：3 种字号克制 =====
\titleformat{\section}
    {\color{primary}\fontsize{14pt}{18pt}\bfseries\sffamily}
    {\thesection}{1em}{}
\titlespacing*{\section}{0pt}{28pt}{14pt}

\titleformat{\subsection}
    {\color{primary}\fontsize{12pt}{16pt}\bfseries\sffamily}
    {\thesubsection}{1em}{}
\titlespacing*{\subsection}{0pt}{20pt}{10pt}

\titleformat{\subsubsection}
    {\color{ink2}\fontsize{11pt}{17pt}\bfseries\sffamily}
    {\thesubsubsection}{1em}{}
\titlespacing*{\subsubsection}{0pt}{14pt}{8pt}

% ===== 页眉页脚：极简 =====
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\color{ink2}\fontsize{9pt}{12pt}\sffamily 时空智能分析法研究报告}
\fancyhead[R]{\color{ink2}\fontsize{9pt}{12pt}\sffamily 2026-09-08}
\fancyfoot[C]{\color{ink2}\fontsize{9pt}{12pt}\sffamily \thepage}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0pt}

% ===== 行距与段落：宽呼吸 =====
\renewcommand{\arraystretch}{1.5}
\setlength{\parskip}{12pt plus 2pt minus 1pt}
\setlength{\parindent}{0pt}

% ===== 列表：紧凑但不拥挤 =====
\setlist[itemize]{leftmargin=1.4em, itemsep=6pt, topsep=6pt, parsep=2pt}
\setlist[enumerate]{leftmargin=1.8em, itemsep=6pt, topsep=6pt, parsep=2pt}

% ===== 表格：优雅三线 =====
\renewcommand{\arrayrulewidth}{0.4pt}
\arrayrulecolor{rule}

% ===== 引用框：温和的左色带 =====
\tcbuselibrary{skins}
\newtcolorbox{quotebar}{
    enhanced,
    colback=primary!4,
    colframe=primary,
    boxrule=0pt,
    leftrule=3pt,
    arc=0pt,
    outer arc=0pt,
    left=14pt, right=14pt, top=10pt, bottom=10pt,
    fontupper=\color{ink}\fontsize{11pt}{17pt}
}

% ===== 高亮：极轻量的灰底蓝字（不要彩底）=====
\newcommand{\hl}[1]{\colorbox{primary!10}{\textcolor{primary}{#1}}}
\newcommand{\warn}[1]{\textbf{\textcolor{primary}{#1}}}

% ===== 图表题注：优雅灰色 =====
\captionsetup{
    font={small, color=ink2},
    labelfont={bf, color=primary},
    textfont={it}
}
```

### 步骤 2：编译脚本 `build_pdf_v3.sh`

```bash
#!/bin/bash
INPUT="$1"
OUTPUT="$2"

pandoc "$INPUT" \
    -o "$OUTPUT" \
    --pdf-engine=xelatex \
    --include-in-header=preamble_v3.tex \
    -V mainfont="PingFang SC" \
    -V monofont="Menlo" \
    -V CJKmainfont="PingFang SC" \
    -V geometry:margin=2.2cm \
    -V colorlinks=true \
    --toc \
    --toc-depth=2 \
    --number-sections \
    -V title="<标题>" \
    -V subtitle="<副标题>" \
    -V author="<作者>" \
    -V date="\\today"

echo "✅ PDF: $OUTPUT"
```

### 步骤 3：执行

```bash
chmod +x build_pdf_v3.sh
./build_pdf_v3.sh report.md report.pdf
```

---

## 一行命令（终极版 v3）

```bash
pandoc <INPUT>.md \
    -o <OUTPUT>.pdf \
    --pdf-engine=xelatex \
    --include-in-header=preamble_v3.tex \
    -V mainfont="PingFang SC" \
    -V monofont="Menlo" \
    -V CJKmainfont="PingFang SC" \
    -V geometry:margin=2.2cm \
    -V colorlinks=true \
    --toc \
    --toc-depth=2 \
    --number-sections \
    -V title="<标题>" \
    -V subtitle="<副标题>" \
    -V author="<作者>" \
    -V date="\\today"
```

---

## v1 → v2 → v3 演进对照

| 维度 | v1（HTML） | v2（LaTeX 复杂） | **v3（LaTeX 克制）** |
|------|----------|----------------|---------------------|
| 字号种类 | 8+ | 6 | **3** |
| 颜色种类 | 6 | 6 | **2** |
| 底色 | 4 处 | 3 处 | **1 处** |
| 段间留白 | 12pt | 10pt | **12pt（弹性）** |
| 行高 | 1.4 | 1.5 | **1.5（统一）** |
| 章节比 | 14:11 | 16:11 | **14:11 ≈ 1.27** |
| 风格 | 略业余 | 略繁复 | **优雅克制** |
| 适用场景 | 草稿 | 内部报告 | **正式发布 / 客户交付** |

## 何时不用 v3 配方

- 报告需要**像素级控制**（特定封面、签名栏、特定字体）→ 用 `productivity/pdf` skill 的 `pdf_create.py` + reportlab
- 报告含**大量复杂图表**（matplotlib / plotly）→ 用 LaTeX 模板（如 neurips2025）
- 报告**纯英文** → 去掉 `ctex`，换 `mainfont="Times New Roman"`
- 报告**5 页以下短文** → 用 v1 简单配方即可

## 已知瑕疵 + 修复

| 瑕疵 | 原因 | 修复 |
|------|------|------|
| ⚡ ✅ 等 emoji 空框 | PingFang SC 不含 emoji | 用"否 / 是"代替；或装 Noto Sans CJK SC |
| 中文标点间距偏大 | xelatex 默认 CJK | 加 `-V CJKoptions="AutoFakeBold,Scale=0.95"` |
| 长 URL 截断 | 默认 break 策略 | preamble 加 `\usepackage{xurl}` |
| 表格行高过宽 | 默认行距 | preamble `\arraystretch{1.5}` |

## 排版守则（v3 写作时遵守）

| 守则 | 说明 |
|------|------|
| **3 种字号** | 14 / 12 / 11 + 页眉 9，不引入其他字号 |
| **2 种颜色** | 主蓝 + 中灰（除文字黑），不引入其他颜色 |
| **1 处底色** | 引用框，不在正文里加底色块 |
| **大留白** | 段间 12pt，行高 1.5，章节前 28pt |
| **避免 emoji** | 用"否 / 是""高 / 中 / 低"代替 ✅❌⚡ |
| **避免彩虹** | 不在同一段用蓝 / 红 / 金三色高亮 |
| **避免堆砌** | 一个表格不超过 6 列，一个章节不超过 5 个标题 |

## 实证记录

- **2026-09-08 数字媒体艺术 AIGC 教育报告**：v3 输出 `/Users/neocross/Desktop/数字媒体艺术AIGC教育_时空分析报告_v3.pdf`（314 KB / 13 页）
- 实证优势：13 页内容阅读舒适度比 v2 13 页更高（更少的视觉噪音）
- 验证松哥反馈："v3 排版优雅了"

---

**v3 配方生效时间**：2026-09-08
**下一步**：v3.1 增加"自适应主题色"（按客户品牌自动替换 primary 颜色）
