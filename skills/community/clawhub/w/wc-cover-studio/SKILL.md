---
name: wc-cover-studio
description: >-
  公众号封面生成（WeChat cover studio）。当用户需要 公众号封面、封面图、文章配图、
  设计封面、单图双用、微信封面、cover image、WeChat cover，或要为文章设计封面时触发。
  工作流：读文章→定风格→选行业意象→生成1:1主图→PIL后处理，一次交付三种版式
  （900×383头条 / 1080×1080方版 / 单图双用），单图双用通吃微信两种裁切比例，
  中文标题100%无错字，内置程序化QA，适用所有公众号/自媒体创作者。
agent_created: true
---

# WeChat Cover Generator（公众号封面生成）

## Overview

Generate production-ready WeChat Official Account article covers from an article file or a topic description. The workflow handles the entire pipeline: reading the article's publish info block (title candidates / summary / cover suggestion), choosing a visual style, generating a 1:1 master image, applying Chinese title overlay with system fonts, producing all three required formats, and running programmatic QA.

**The critical rule this skill encodes**: WeChat's backend accepts only ONE cover image, but automatically crops two displays — the headline card shows the full 2.35:1 image, while the share thumbnail shows the CENTER 1:1 region. Therefore key content must live in the central safe zone. See `references/wechat-cover-rules.md` §1.

## Workflow

### Step 1 · Read the article

Read the article file. Extract the publish-info block at the top (usually quoted lines starting with `>`):

- 标题（候选列表，选最贴合的一个，可浓缩为 4-8 字主标题 + 副标题）
- 摘要（80 字内）
- 封面建议（若有，作为风格参考；用户可要求自由发挥）
- 文章类型（科普/叙事/行业洞察 → 决定风格，见风格库）

### Step 2 · Choose a style and industry imagery

Consult the style library in `references/wechat-cover-rules.md` §3. Quick guide:

| 文章类型 | 风格 |
|---|---|
| 科普、产品机制、技术原理 | 歸藏材质插画（白底 3D + IKB 蓝）或扁平插画 |
| 对比类（新旧、两体系） | 扁平插画 + 材质对比 |
| 叙事、人物、独白、深夜氛围 | 深夜氛围摄影（暖黄灯光 + 深蓝黑背景） |

**Choose industry-specific imagery**（`references/wechat-cover-rules.md` §3.5）— the most important step for cover quality:

- Follow the 意象选择三步法: list 3-5 candidate symbols for the topic's field, verify each is field-exclusive (reject generic symbols like yin-yang, hearts, stars, gears), then prefer material contrast against the counterpart.
- Use the 行业意象速查表 for common fields (中医/金融/教育/科技/西医/电商/农业/法律/建筑/历史), and search references for any niche/unfamiliar symbol before prompting.
- General rule: generic symbols dilute professionalism; field-exclusive tools and artifacts (针灸铜人, 算盘, 芯片, 化验单...) read instantly.

### Step 3 · Generate the 1:1 master image

Use the image generation tool (ImageGen / equivalent) with size **1024x1024**. Follow the prompt template in `references/wechat-cover-rules.md` §4.

Mandatory prompt requirements:
- `square 1:1 composition, subject fills the lower two thirds, centered horizontally`
- `upper third reserved as clean empty background for title overlay`
- `generous safe margins, full subject visible, no crop`
- For short labels (2-5 chars) that the image model renders: list ALL labels with explicit positions and add `ALL N ... MUST appear, no exceptions, no omissions`（多标签防漏技巧，§4）

**Never** ask the image model to render titles longer than ~6 characters — overlay them with PIL instead (§4, §5).

### Step 4 · Run the post-processing script

Run `scripts/make_cover.py` with the generated 1:1 master image:

```bash
python scripts/make_cover.py <input_1x1_image> \
  --title "主标题" \
  --subtitle "副标题" \
  -o <output_dir>
```

The script produces (default modes `square,wide,dual`):
1. `cover_1x1_*.png` — 1080×1080 square share cover
2. `cover_900x383_*.png` — wide headline cover (crops the 2.35:1 band from center; `--crop-center` adjusts, default 0.52)
3. `cover_单图双用.png` — **single-image dual-use** cover: central 383×383 safe zone (subject + title) with blurred ambiance extension on both sides. This is the recommended upload.

Use `--modes square` or `--modes wide` to generate only specific formats.

### Step 5 · Verify with built-in QA

The script runs automatic pixel-sampling QA after each render (title-region pixel counts). Check the output:
- `[QA] ... ✅` for every mode. If a mode shows `⚠️ 偏低`, inspect the title region or re-run with adjusted parameters.
- For extra verification (no image-viewing capability), follow the QA table in `references/wechat-cover-rules.md` §6: background sampling, warm-pixel grid for subject location, title pixel count.

### Step 6 · Deliver

- Present the `cover_单图双用.png` first (recommended upload), then the wide and square versions.
- Also write a short 封面说明 markdown next to the covers recording: design rationale, title scheme, and QA results.
- **File placement convention**: if the article lives in a platform-organized folder structure (e.g. `docs/软文/公众号/02_科普_.../` where each article has its own subfolder holding copy + images), save all generated covers and the 封面说明 into that article's subfolder — never scatter them at the platform root. Platform-level files (e.g. `_发布须知.md`) stay at the platform root.

## Concrete Example

User: "给这篇文章做一个封面" (attaching an article .md)

1. Read article → extract title candidates & cover suggestion.
2. Pick style (article-type → style library) and pick industry imagery (§3.5 意象三步法 + 速查表).
3. ImageGen 1024×1024 with prompt template (subject centered, upper third empty).
4. `python make_cover.py master.png --title "最难的不是技术" --subtitle "做灵素AI 这一年" -o <article_dir>`
5. Confirm 3 QA ✅ lines.
6. Present dual-use + wide + square, write 封面说明.md.

## Resources

- `scripts/make_cover.py` — PIL post-processing: title/subtitle overlay (auto light/dark text color by background), 900×383 crop, 1080×1080 square, 383×383 central safe-zone dual-use layout, programmatic QA. Auto-detects Chinese fonts (Windows 微软雅黑 / macOS 苹方 / Linux Noto).
- `references/wechat-cover-rules.md` — WeChat cover crop mechanics, full workflow, style library (with prompt elements per style), industry-specific imagery library with 意象三步法 + 10-domain quick-reference table (中医/金融/教育/科技/西医/电商/农业/法律/建筑/历史), ImageGen prompt templates, multi-label anti-dropout tricks, PIL title spec, QA table, delivery checklist.
