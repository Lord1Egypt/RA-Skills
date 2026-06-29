[English](README_EN.md) | [中文](README.md)
# gugu-gaga

> 制药法规 & 指南结构化分析工具 | Regulatory & Guidance Analysis Tool

[![Version](https://img.shields.io/badge/version-2.5.2-blue)](./SKILL.md)
[![Author](https://img.shields.io/badge/author-Gxpcode--Zhonghe-orange)](./SKILL.md)

将 PDF / DOCX / TXT 法规文件自动转化为结构化分析报告，输出为**培训演示 PPTX** 或**学习分享 PDF**。

---

## 目录

- [功能特性](#功能特性)
- [工作流](#工作流)
- [分析内容](#分析内容)
- [输出格式](#输出格式)
- [快速开始](#快速开始)
- [目录结构](#目录结构)
- [环境要求](#环境要求)
- [关于](#关于)

---

## 功能特性

| 特性 | 说明 |
|------|------|
| **多格式输入** | 支持 PDF、DOCX、DOC、TXT 四种格式 |
| **自动格式转换** | 内嵌 Microsoft MarkItDown，无需外部 OCR 服务 |
| **五维结构分析** | 元素采集 → 定性 → 重点内容 → 生命周期图 → 灯色统计 |
| **双输出格式** | 培训演示用 16:9 PPTX，学习分享用 3:4 PDF |
| **红黄绿蓝灯体系** | 🔴 必须/应当 · 🟡 宜/建议 · 🟢 参照/参考 · 🔵 酌情/视情况 |
| **断点续跑** | Step 4 五阶段分析支持中断后继续，任务自动编号 |
| **HTML 驱动预览** | 生成 HTML Deck 后先预览审阅，确认后再转换为最终产物 |
| **丰富的模板体系** | 31 个单页布局 + 2 个完整 Deck 模板 + 22 种动画特效 |

---

## 工作流

```
输入文件 (PDF/DOCX/TXT)
  │
  ├─ Step 0  启动检查：格式校验 + 用途选择（A.培训演示 / B.学习分享）
  │
  ├─ Step 1  输入转换：markitdown → Markdown
  │
  ├─ Step 2  阅读：理解目录结构
  │
  ├─ Step 3  领域判断：是否属于制药领域？（非制药则终止）
  │
  ├─ Step 4  法规分析：五阶段渐进式分析 + 校验循环
  │
  ├─ Step 5  生成 HTML：页数规划 → 布局分配 → HTML Deck + 用户审阅循环
  │
  └─ Step 6  转换输出：HTML → PPTX（Playwright 截图法）或 PDF（Playwright 原生引擎）
```

---

## 分析内容

Step 4 执行五项独立分析任务，逐阶段推进：

| 序号 | 分析项 | 文件 | 说明 |
|------|--------|------|------|
| 4.1 | 元素采集 | `resources/prompts/4.1_元素采集.md` | 名称、发布机构、效力级别、日期、编制依据 |
| 4.2 | 定性 | `resources/prompts/4.2_定性.md` | 为什么制订？适用范围？适用对象？ |
| 4.3 | 重点内容 | `resources/prompts/4.3_重点内容.md` | 高风险/高难点在哪？如何管控？如何检查？ |
| 4.4 | 生命周期图 | `resources/prompts/4.4_生命周期图.md` | 以流程图绘制文档中的生命周期流程 |
| 4.5 | 红黄绿蓝灯 | `resources/prompts/4.5_红黄绿蓝灯.md` | 按章节/条款逐条统计法规符合性等级 |

**灯色规则：**

| 灯色 | 关键词 | 含义 |
|------|--------|------|
| 🔴 红灯 | 必须、应当、不得、禁止 | 强制要求 / 禁止行为 |
| 🟡 黄灯 | 宜、建议、鼓励、推荐 | 推荐做法 |
| 🟢 绿灯 | 参照、参考、可 | 可选 / 参考性条款 |
| 🔵 蓝灯 | 酌情、视情况、适当时 | 弹性空间 |

---

## 输出格式

### A. 培训演示 → PPTX（16:9）

- **模板：** `templates/full-decks/pptx-model/`
- **风格：** 警示/风控/事故报告风格，红黑斜条纹、三档色卡
- **转换方式：** Playwright 截图法（1920×1080）→ `python-pptx` 逐页嵌入
- **产物：** `{原文stem}_4.N_*.md` + `{原文stem}.pptx`

### B. 学习分享 → PDF（3:4 竖版）

- **模板：** `templates/full-decks/pdf-model/`
- **风格：** MUJI/手帐风格，便签 + 贴纸 + 圆角厚边框
- **转换方式：** Playwright 原生 PDF 引擎（810×1080），可搜索、矢量清晰
- **产物：** `{原文stem}_4.N_*.md` + `{原文stem}.pdf`

---

## 快速开始

### 1. 首次安装环境

```bash
python scripts/setup.py
```

此命令使用阿里云镜像安装所需依赖：
- `markitdown`（本地源码 `packages/markitdown/`，含 `[docx,pdf]` 可选依赖）
- `playwright`
- `python-pptx`
- `Pillow`

### 2. 使用 Skill

在 WorkBuddy 中输入法规文件并加载 skill：

```
@skill:gugu-gaga 分析这份文件：/path/to/regulation.pdf
```

按提示选择输出格式（A 或 B），后续自动执行 6 步工作流。

### 3. 校验产物

```bash
# 校验 Step 4 分析结果
python scripts/validate.py --step 4 --dir outputs/

# 校验 Step 5 HTML 产物
python scripts/validate.py --step 5 --html outputs/xxx.html
```

---

## 目录结构

```
gugu-gaga/
├── SKILL.md                      # Skill 定义与工作流入口
├── README.md                     # 本文件
│
├── scripts/                      # 工具脚本（5 个）
│   ├── setup.py                  # 环境初始化
│   ├── validate.py               # 产物校验（支持多模式）
│   ├── check_assets.py           # 资源完整性检查
│   ├── convert_pptx_model.py     # HTML → PPTX 转换
│   └── convert_pdf_model.py      # HTML → PDF 转换
│
├── resources/                    # 资源与规范
│   ├── html_spec.md              # HTML 生成规范（class 白名单、颜色变量）
│   ├── layouts.md                # 布局目录 / 映射表
│   ├── prompts/                  # 分析 Prompt（6 个）
│   │   ├── 4.1_元素采集.md
│   │   ├── 4.2_定性.md
│   │   ├── 4.3_重点内容.md
│   │   ├── 4.4_生命周期图.md
│   │   ├── 4.5_红黄绿蓝灯.md
│   │   └── 5.0_内容映射.md
│   └── steps/                    # 步骤指令（6 个）
│       ├── step_1.md ~ step_6.md
│
├── assets/                       # 前端资源
│   ├── base.css                  # CSS 重置 & 共享 Token
│   ├── fonts.css                 # Google Fonts 加载
│   ├── runtime.js                # 键盘驱动 Deck 运行时
│   ├── themes/                   # 主题
│   │   └── midcentury.css
│   └── animations/               # 动画系统（22 个特效）
│       ├── animations.css
│       ├── fx-runtime.js
│       └── fx/                   # 20 个独立动画特效
│
├── templates/                    # HTML 模板
│   ├── full-decks/               # 完整 Deck 模板
│   │   ├── pdf-model/            # PDF 输出模板（3:4）
│   │   └── pptx-model/           # PPTX 输出模板（16:9）
│   └── single-page/              # 单页布局模板（31 个）
│
└── packages/                     # 内嵌依赖
    └── markitdown/               # Microsoft MarkItDown（MIT）
```

---

## 环境要求

| 组件 | 要求 |
|------|------|
| Python | ≥ 3.10 |
| 浏览器 | Microsoft Edge（系统自带） |
| Playwright | 用于 HTML → PPTX/PDF 转换 |
| 操作系统 | Windows（开发环境） |

---

## 关于

**gugu-gaga** 是一个面向制药法规专业人士的结构化分析工具，将繁琐的法规研读过程自动化为清晰的培训材料或学习笔记。

- **作者：** Gxpcode-Zhonghe
- **版本：** 2.5.2
- **协议：** 内部工具

> 🔬 "先用工具把法规拆明白，再用人脑做决策。"
