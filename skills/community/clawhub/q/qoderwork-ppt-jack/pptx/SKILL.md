---
name: qoderwork-ppt
version: 1.0.0
description: Generate QoderWork-style presentations. Automatically matches 14 templates based on your topic and outputs an editable .pptx file.
description_zh: 生成 QoderWork 风格演示文稿。根据主题自动匹配 14 种模板，输出可编辑的 .pptx 文件。
category: content-creation
---

# QoderWork-PPT

When a user wants to **generate a QoderWork-style presentation**, use this skill. Based on the user's topic and requirements, it automatically generates content, matches suitable templates, and outputs an editable PowerPoint file.

## Execution Flow

### 0. Prepare output directory

Create the output directories if they don't exist:

```bash
mkdir -p output output/images
```

### 1. Understand requirements & generate content document

Read `rules/content-rules.md` (in this skill directory), then convert the user's requirements into a structured content document at `output/content.md`.

- Extract from user input: topic, audience, key points, page count preferences, etc.
- Generate a well-structured plain-text document following content-rules
- Content should be complete, logically clear, and ready for template matching
- **CRITICAL — page budget**: unless the user explicitly requests more, plan for **8–15 slides total** (including cover, TOC, section dividers, and closing). Count your planned slides before proceeding to step 2. If the outline exceeds 15, merge or cut sections.

### 2. Match templates & generate slide sequence

Read `rules/template-matching.md` and `templates/manifest.json`, then generate `output/slides.json` based on content.md.

- **slides.json array length MUST be ≤ 15** (unless the user explicitly requested more). Count before writing the file.
- Format per slide: `{ "templateId": "xxx", "slots": { "slotId": "value", ... } }`
- A **full example** (one slide per template type) is available at `rules/slides-example.json` — copy and adapt it
- Strictly follow template-matching rules; slot values must conform to manifest constraints (type, maxLength, etc.)

**Cover background**：cover 模板的 `coverBackground` 槽位**勿主动填写**，使用模板默认背景。仅当用户明确要求自定义封面图时才填。

**Section-divider 插图**：03 章节分隔页右侧的 `image` 槽位**尽量勿填**，使用模板默认插图。仅当用户明确要求更换章节配图时才填。

**Image slots (type: image)** accept any of:

| Format | Example | When to use |
|--------|---------|-------------|
| `lucide:<icon-name>` | `lucide:shield-check` | Icon-style images (preferred for column cards in 06/07/08) |
| Image URL | `https://example.com/photo.jpg` | Web images |
| Local path | `output/images/slide-03.png` | After generating/saving an image locally |

**When you must generate/search for real images**: slots marked `aiGeneratable: true` that need a **real photograph or illustration** (not an icon) — typically `section-divider` image, `content-left-text-right-image` image, and `full-image` background. Call `generate_image` or `web_search` to obtain them, save to `output/images/`, and fill the path into slots. **These image slots are required** — do NOT leave the default placeholder.

### 3. Fill HTML templates

**Working directory (cwd)**: must be the project root (where `output/` lives).

**Script path**: relative to this skill directory. Replace `SKILL_SCRIPTS` below with the actual path (e.g., `resources/skills-market/qoderwork-ppt/scripts` if using this repo as workspace, or `~/.qoderwork/skills/qoderwork-ppt/scripts` if installed from market).

Optional — validate first:

```bash
node SKILL_SCRIPTS/validate-slides.js output/slides.json
```

Then fill templates (or use the one-click pipeline below):

```bash
node SKILL_SCRIPTS/fill-template.js output/slides.json
```

**Recommended — one-click pipeline (steps 3+4 combined)**:

```bash
node SKILL_SCRIPTS/run-pipeline.js output/slides.json
```

Output file is auto-named with a timestamp (e.g. `output/presentation-2026-03-06-10-30-00.pptx`) to avoid overwriting previous runs.

### 4. Convert to PPTX

If you didn't use the one-click pipeline above, run separately:

```bash
node SKILL_SCRIPTS/html-to-pptx-dom.js output/filled
```

Reads filled HTML from `output/filled/`, renders via Puppeteer, and converts to PPTX using dom-to-pptx — **preserving background images, rounded corners, fonts, and full styling**.

### 5. Inform the user

Tell the user the PPT has been generated at `output/presentation.pptx`, with a brief summary of page count and structure.

## Resumability (Agent checkpoint recovery)

- **Step 1**: If `output/content.md` already exists and the user didn't ask to "regenerate content", skip to step 2.
- **Step 2**: Always (re-)generate `output/slides.json` from content.md.
- **Step 3+4**: If only slides.json changed, just re-run `run-pipeline.js` (overwrites `output/filled/` and `output/presentation.pptx`).

## Key Files (in this skill directory)

| File | Purpose |
|------|---------|
| `rules/content-rules.md` | Content generation rules & document structure |
| `rules/template-matching.md` | Template matching rules & image slot conventions |
| `rules/slides-example.json` | Full slides.json example (one slide per template type) |
| `templates/manifest.json` | 14 template definitions with slot specs |
| `templates/*.html` | 14 HTML template files (1920×1080) |
| `scripts/validate-slides.js` | Pre-validation for slides.json |
| `scripts/fill-template.js` | Fills slot values into HTML templates |
| `scripts/html-to-pptx-dom.js` | High-fidelity HTML → PPTX conversion |
| `scripts/run-pipeline.js` | One-click: validate → fill → convert |

## Output Files (in project root `output/`)

| File | Purpose |
|------|---------|
| `output/content.md` | Intermediate: structured content |
| `output/slides.json` | Intermediate: slide sequence + slot values |
| `output/images/` | Generated/downloaded images for slides |
| `output/filled/*.html` | Filled single-page HTML files |
| `output/presentation.pptx` | Final PowerPoint file |

## Dependencies

Before first use, install dependencies in this skill directory:

```bash
cd <path-to-this-skill-directory> && npm install
```

Required packages: `jsdom`, `puppeteer`, `dom-to-pptx`, `lucide-static`. **Icons are loaded from local `lucide-static` (no network at runtime).**
