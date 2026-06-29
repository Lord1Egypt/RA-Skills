[English](README_EN.md) | [中文](README.md)
# gugu-gaga · Regulatory Guidance Analysis Tool

[![Version](https://img.shields.io/badge/version-2.5.2-blue)](SKILL.md)
[![Python](https://img.shields.io/badge/python-3.10+-blue)](scripts/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**Pharmaceutical Regulation & Guidance Structured Analysis Tool**

Automatically transforms PDF / DOCX / TXT regulatory documents into structured analysis reports, delivered as **training presentation PPTX** or **study-sharing PDF**.

---

## Table of Contents

- [Features](#features)
- [Workflow](#workflow)
- [Analysis Content](#analysis-content)
- [Output Formats](#output-formats)
- [Quick Start](#quick-start)
- [Directory Structure](#directory-structure)
- [Requirements](#requirements)
- [About](#about)

---

## Features

| Feature | Description |
|---------|-------------|
| **Multi-format Input** | Supports PDF, DOCX, DOC, and TXT |
| **Automatic Format Conversion** | Built-in Microsoft MarkItDown — no external OCR needed |
| **5-Dimensional Structured Analysis** | Element Collection → Characterization → Key Content → Lifecycle Diagram → Traffic-light Statistics |
| **Dual Output Formats** | Training presentation: 16:9 PPTX · Study sharing: 3:4 PDF |
| **Red-Yellow-Green-Blue Light System** | 🔴 Must/Shall · 🟡 Should/Recommended · 🟢 For Reference · 🔵 At Discretion |
| **Resumable Execution** | Step 4 five-phase analysis supports pause-and-resume; tasks auto-numbered |
| **HTML-driven Preview** | Generates HTML Deck for review and approval before converting to final output |
| **Rich Template Library** | 31 single-page layouts + 2 full Deck templates + 22 animation effects |

---

## Workflow

```
Input File (PDF/DOCX/TXT)
  │
  ├─ Step 0  Startup Check: format validation + output mode (A. Training / B. Study)
  │
  ├─ Step 1  Input Conversion: markitdown → Markdown
  │
  ├─ Step 2  Reading: understand document structure
  │
  ├─ Step 3  Domain Check: is this a pharmaceutical document? (abort if not)
  │
  ├─ Step 4  Regulatory Analysis: 5-phase progressive analysis + validation loop
  │
  ├─ Step 5  HTML Generation: page planning → layout assignment → HTML Deck + user review loop
  │
  └─ Step 6  Output Conversion: HTML → PPTX (Playwright screenshot) or PDF (Playwright native engine)
```

---

## Analysis Content

Step 4 performs five independent analysis tasks, progressing phase by phase:

| # | Analysis Item | Prompt File | Description |
|---|--------------|-------------|-------------|
| 4.1 | Element Collection | `resources/prompts/4.1_元素采集.md` | Title, issuing body, legal force level, date, basis |
| 4.2 | Characterization | `resources/prompts/4.2_定性.md` | Why was it issued? Scope? Target audience? |
| 4.3 | Key Content | `resources/prompts/4.3_重点内容.md` | High-risk/high-difficulty areas? How to control? How to check? |
| 4.4 | Lifecycle Diagram | `resources/prompts/4.4_生命周期图.md` | Flowchart of the document's lifecycle process |
| 4.5 | R-Y-G-B Lights | `resources/prompts/4.5_红黄绿蓝灯.md` | Clause-by-clause compliance level classification |

**Traffic-light Rules:**

| Color | Keywords | Meaning |
|-------|----------|---------|
| 🔴 **Red** | must, shall, shall not, prohibited | Mandatory / prohibited |
| 🟡 **Yellow** | should, recommended, encouraged | Recommended practice |
| 🟢 **Green** | for reference, may | Optional / informative |
| 🔵 **Blue** | at discretion, as appropriate | Flexible / case-by-case |

---

## Output Formats

### A. Training Presentation → PPTX (16:9)

- **Template:** `templates/full-decks/pptx-model/`
- **Style:** Alert / risk-control / incident-report style — red-black diagonal stripes, three-tier color system
- **Conversion:** Playwright screenshot method (1920×1080) → `python-pptx` slide-by-slide embedding
- **Artifacts:** `{original_stem}_4.N_*.md` + `{original_stem}.pptx`

### B. Study Sharing → PDF (3:4 Portrait)

- **Template:** `templates/full-decks/pdf-model/`
- **Style:** MUJI / journal style — sticky notes + stickers + rounded thick borders
- **Conversion:** Playwright native PDF engine (810×1080), searchable, vector-sharp
- **Artifacts:** `{original_stem}_4.N_*.md` + `{original_stem}.pdf`

---

## Quick Start

### 1. First-time Setup

```bash
python scripts/setup.py
```

This installs required dependencies via Alibaba Cloud mirror:

- `markitdown` (local source `packages/markitdown/`, with `[docx,pdf]` optional dependencies)
- `playwright`
- `python-pptx`
- `Pillow`

### 2. Using the Skill

In WorkBuddy, load a regulatory document and invoke:

```
@skill:gugu-gaga analyze this document: /path/to/regulation.pdf
```

Select output format (A or B) when prompted. The 6-step workflow then runs automatically.

### 3. Validate Output

```bash
# Validate Step 4 analysis results
python scripts/validate.py --step 4 --dir outputs/

# Validate Step 5 HTML artifacts
python scripts/validate.py --step 5 --html outputs/xxx.html
```

---

## Directory Structure

```
gugu-gaga/
├── SKILL.md                      # Skill definition & workflow entry
├── README.md                     # This file
│
├── scripts/                      # Utility scripts (5)
│   ├── setup.py                  # Environment initialization
│   ├── validate.py               # Output validation (multi-mode)
│   ├── check_assets.py           # Asset integrity check
│   ├── convert_pptx_model.py     # HTML → PPTX conversion
│   └── convert_pdf_model.py      # HTML → PDF conversion
│
├── resources/                    # Resources & specifications
│   ├── html_spec.md              # HTML generation spec (class whitelist, color vars)
│   ├── layouts.md                # Layout catalog & mapping table
│   ├── prompts/                  # Analysis prompts (6)
│   │   ├── 4.1_元素采集.md        # Element Collection
│   │   ├── 4.2_定性.md            # Characterization
│   │   ├── 4.3_重点内容.md         # Key Content
│   │   ├── 4.4_生命周期图.md       # Lifecycle Diagram
│   │   ├── 4.5_红黄绿蓝灯.md       # R-Y-G-B Light System
│   │   └── 5.0_内容映射.md         # Content Mapping
│   └── steps/                    # Step instructions (6)
│       ├── step_1.md ~ step_6.md
│
├── assets/                       # Frontend resources
│   ├── base.css                  # CSS reset & shared tokens
│   ├── fonts.css                 # Google Fonts loader
│   ├── runtime.js                # Keyboard-driven deck runtime
│   ├── themes/                   # Themes
│   │   └── midcentury.css
│   └── animations/               # Animation system (22 effects)
│       ├── animations.css
│       ├── fx-runtime.js
│       └── fx/                   # 20 independent animation effects
│
├── templates/                    # HTML templates
│   ├── full-decks/               # Full deck templates
│   │   ├── pdf-model/            # PDF output template (3:4)
│   │   └── pptx-model/           # PPTX output template (16:9)
│   └── single-page/              # Single-page layout templates (31)
│
└── packages/                     # Bundled dependencies
    └── markitdown/               # Microsoft MarkItDown (MIT)
```

---

## Requirements

| Component | Requirement |
|-----------|-------------|
| Python | ≥ 3.10 |
| Browser | Microsoft Edge (system) |
| Playwright | For HTML → PPTX / PDF conversion |
| OS | Windows (dev environment) |

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

## About

**gugu-gaga** is a structured analysis tool for pharmaceutical regulatory professionals — turning tedious regulation review into clear training materials or study notes.

- **Author:** Gxpcode-Zhonghe
- **Version:** 2.5.2

> 🔬 "Use the tool to break down regulations first. Use your brain to make decisions."
>
> — GxpCode

---

## Repository

- GitHub: [Gxpcode-hezhong/Regulatory-Guidance-Analysis-Tool](https://github.com/Gxpcode-hezhong/Regulatory-Guidance-Analysis-Tool)
- Author: [@Gxpcode-hezhong](https://github.com/Gxpcode-hezhong)
