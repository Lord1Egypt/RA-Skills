---
name: slidev-ppt-generator
description: Generate and export presentations using Slidev. Use only when the user explicitly asks for Slidev, Markdown slides, a previewable slides.md, or needs to export PDF/PPTX/HTML. Do NOT use for Jobs-style vertical HTML presentations.
metadata:
  openclaw:
    emoji: "📊"
    tags: ["slidev", "ppt", "presentation", "markdown", "slides"]
    requires:
      bins: ["node", "npm"]
    platform: ["macos", "linux"]
---

# Slidev PPT Generator

Generate `slides.md` using the standard Slidev workflow, then preview, build, and export within an existing or new Slidev project.

## When to Use

- User explicitly mentions `Slidev`
- User wants `slides.md`, Markdown slides, or a locally previewable presentation
- User wants to turn a Markdown outline into a previewable or exportable Slidev presentation
- User wants to export `PDF`, `PPTX`, or build static HTML

## When NOT to Use

- User wants an editable native PPTX and does not accept image-based Slidev PPTX export
- User wants a Jobs-style, minimalist tech-feel, 9:16 vertical, single-HTML presentation
- User only needs a single HTML landing page or long-form article, not the Slidev workflow
- User has no local Node/npm environment, and the current task does not allow installing dependencies

## Directory Structure

- `scripts/generate.js` — Generate a basic `slides.md` from a given topic
- `scripts/export.js` — Export `pdf` / `pptx` / `png` from within a Slidev project directory
- `templates/tech-share.md` — Tech-share template reference
- `examples/demo-slides.md` — Example slides
- `references/presentation-design.md` — Presentation design and layout rules; must be consulted when generating a formal deck

## Standard Workflow

### 1. Confirm Output Target

Confirm the following information first. If the user has not provided everything, fill in the minimum necessary defaults:

1. Topic
2. Style: `tech` / `product` / `report`
3. Page count range
4. Language: `auto` / `zh` / `en`
5. Final deliverable: preview, HTML, PDF, PPTX
6. Tone: `formal` / `executive` / `technical` / `launch`
7. Official theme preference: auto-detect, or user-specified `default` / `seriph` / `apple-basic`

If the user just says "make a PPT", use these defaults:

- Style: `tech`, Pages: `10`, Language: `auto`
- Output: Generate `slides.md` first, then ask whether to export
- Tone: `formal`, Theme: auto-detect

Language rules:

- If the user explicitly requests English, the entire deck should be in English
- If the user explicitly requests Chinese, the entire deck should be in Chinese
- If the user does not specify, default to the primary language of the user's current message
- Keep titles, body text in the same language; avoid mixing languages
- Do not generate bilingual pages unless the user explicitly requests it

### 2. Check or Initialize Slidev Project

Prefer reusing an existing Slidev project. If the user does not specify a directory, default to `~/slidev-ppt`.

```bash
ls ~/slidev-ppt/package.json ~/slidev-ppt/slides.md
```

If it does not exist, initialize:

```bash
node scripts/init-project.js --dir ~/slidev-ppt
```

If the user needs PDF/PPTX export, initialize with export dependencies:

```bash
node scripts/init-project.js --dir ~/slidev-ppt --with-export-deps
```

The init script installs these official themes: `@slidev/theme-default`, `@slidev/theme-seriph`, `@slidev/theme-apple-basic`, `@slidev/theme-bricks`, `@slidev/theme-shibainu`.

### 3. Generate slides.md — The Core Step

**Do NOT just produce a bullet-point outline.** You are writing a complete, visually designed presentation. Before writing any slide, decide:

1. **Visual direction** — Pick a color mood and image style (dark tech, clean white, warm earth tones)
2. **Theme** — Select based on tone (see Theme Selection below)
3. **Background images** — Select 3-5 Unsplash images that match the topic (see Visual Recipes below)
4. **Layout variety** — Plan which layouts to use; never use `default` for every page

Then write the complete `slides.md` directly. The `generate.js` script only produces a bare skeleton; for any real presentation you should write the file yourself with proper frontmatter, backgrounds, layouts, and styled content.

If the user provides an existing outline, read the existing `slides.md` first, then modify on top of it.

### 4. Preview

```bash
npx slidev slides.md
```

### 5. Export

```bash
node /path/to/slidev-ppt-generator/scripts/export.js --format pdf --output presentation.pdf
```

Or directly: `npx slidev export --format pdf --output presentation.pdf`

## Visual Design Recipes

**This is the most important section.** A deck without visual design is just a document. Follow these recipes.

### Cover Page

The cover page MUST have a background image. Use `layout: cover` with a `background` field. The theme automatically applies a dark overlay for text readability.

```markdown
---
theme: seriph
background: https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1920
class: text-center
---

# Building the Future of AI Agents

Autonomous, local-first, and always available

<div class="abs-br m-6 text-sm opacity-50">
Author Name — March 2026
</div>
```

### How to Choose Background Images

Use Unsplash direct URLs. Pick images by topic keyword:

- **Tech/AI**: server rooms, circuit boards, abstract networks, code on screen
- **Business**: modern offices, skylines, handshakes, conference rooms
- **Nature/Growth**: forests, mountains, sunrise, green fields
- **Data/Analytics**: dashboards, charts, abstract data visualization

URL format: `https://images.unsplash.com/photo-{ID}?auto=format&fit=crop&w=1920&q=80`

Find image IDs at unsplash.com. Use specific photo IDs, not the old `source.unsplash.com` API (deprecated). Pick 3-5 images per deck and reuse them for visual consistency.

For slides that need a background but not a photo, use CSS gradients:

```markdown
---
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)
class: text-center text-white
---
```

Or solid colors:

```markdown
---
background: '#1a1a2e'
class: text-white
---
```

### Section Dividers

Use `layout: section` or `layout: cover` with a background for chapter transitions. Never leave a section page as plain white text.

```markdown
---
layout: section
background: linear-gradient(135deg, #0c3547 0%, #1a6b8a 100%)
class: text-white
---

# Architecture Deep Dive
```

### Content Pages with Visual Structure

**Two-column with image** (apple-basic theme):

```markdown
---
layout: image-right
image: https://images.unsplash.com/photo-xxx?w=960
---

# Why Local-First Matters

- Your data never leaves your machine
- Full control over configuration
- Works offline once set up
- No recurring service fees
```

**Fact/statistic highlight**:

```markdown
---
layout: fact
---

# 7 Agents
Running simultaneously on a single gateway

<br>

# 5 Channels
WhatsApp, Telegram, Discord, Feishu, DingTalk
```

**Quote page**:

```markdown
---
layout: quote
---

# "The best AI assistant is the one you fully control."

— Local-first design philosophy
```

**Statement page** (big idea, minimal text):

```markdown
---
layout: statement
---

# Self-hosted means self-sovereign
```

### Card Grids with UnoCSS

For feature lists, comparisons, or multi-item layouts, use HTML grid with UnoCSS classes instead of plain bullet lists:

```markdown
---
---

# Key Capabilities

<div class="grid grid-cols-2 gap-6 mt-8">
<div class="p-6 bg-gray-100 rounded-lg">
  <h3 class="text-lg font-bold mb-2">Multi-Agent</h3>
  <p class="text-sm opacity-75">Run multiple isolated AI personas on one server</p>
</div>
<div class="p-6 bg-gray-100 rounded-lg">
  <h3 class="text-lg font-bold mb-2">Multi-Channel</h3>
  <p class="text-sm opacity-75">WhatsApp, Telegram, Discord simultaneously</p>
</div>
<div class="p-6 bg-gray-100 rounded-lg">
  <h3 class="text-lg font-bold mb-2">Local-First</h3>
  <p class="text-sm opacity-75">All data stays on your hardware</p>
</div>
<div class="p-6 bg-gray-100 rounded-lg">
  <h3 class="text-lg font-bold mb-2">Open Source</h3>
  <p class="text-sm opacity-75">MIT licensed, community-driven</p>
</div>
</div>
```

For dark themes, use `bg-white/10` or `bg-gray-800` instead of `bg-gray-100`.

### Architecture / Flow Diagrams

**Mermaid diagrams may have rendering issues in PDF/PPTX export** (timing-dependent). Keep Mermaid to under ~15 nodes. For complex diagrams or maximum reliability, use card grids instead:

- Use ASCII-style text diagrams in code blocks
- Use a card-grid layout to represent components
- Use a visual flow with arrows (→) in styled HTML

Example component architecture without Mermaid:

```markdown
---
---

# System Architecture

<div class="grid grid-cols-3 gap-4 mt-6 text-center">
<div class="p-4 bg-blue-100 rounded-lg border-2 border-blue-300">
  <div class="text-xs opacity-50 mb-1">INPUT</div>
  <div class="font-bold">Chat Channels</div>
  <div class="text-xs mt-1">WhatsApp · Telegram · Discord</div>
</div>
<div class="p-4 bg-green-100 rounded-lg border-2 border-green-300">
  <div class="text-xs opacity-50 mb-1">CORE</div>
  <div class="font-bold">Gateway</div>
  <div class="text-xs mt-1">Routing · Sessions · Auth</div>
</div>
<div class="p-4 bg-purple-100 rounded-lg border-2 border-purple-300">
  <div class="text-xs opacity-50 mb-1">EXECUTION</div>
  <div class="font-bold">AI Agents</div>
  <div class="text-xs mt-1">Tools · Skills · Memory</div>
</div>
</div>

<div class="text-center mt-4 text-2xl opacity-30">→ → →</div>
```

### Closing Page

The closing page should have a background (same as cover or complementary). Never end with plain white.

```markdown
---
layout: cover
background: https://images.unsplash.com/photo-xxx?w=1920
class: text-center
---

# Thank You

Questions?

<div class="abs-br m-6 text-sm opacity-50">
author@email.com · github.com/username
</div>
```

## Theme Selection

Prefer official themes. Recommended mapping:

- `technical` → `default` (dark code-friendly, good for tech shares)
- `formal` → `seriph` (elegant serif fonts, good for business)
- `executive` → `seriph` (same, emphasize conclusions)
- `launch` → `apple-basic` (clean, image-heavy layouts)

### Global Frontmatter Template

Always include these fields in the first slide's frontmatter:

```yaml
---
theme: seriph
background: https://images.unsplash.com/photo-{ID}?w=1920
highlighter: shiki
lineNumbers: false
colorSchema: light
title: Your Presentation Title
---
```

- `colorSchema`: use `light` for most business/formal decks; `dark` only for technical/code-heavy decks
- `lineNumbers: false` unless the deck is specifically about code
- Always set a `background` on the first slide

## Design Requirements

- **Every cover and section page MUST have a background** (image, gradient, or color). No plain white covers.
- **At least 3 slides should use a non-default layout** (cover, section, fact, quote, statement, image-right, two-cols)
- **At least 2 slides should have background images** from Unsplash
- One page, one main conclusion. Prefer a compact 8-14 page deck
- The cover page must include title, subtitle, and author/date
- Include at least 1 architecture/structure page, 1 scenario page, 1 value page
- Avoid consecutive bullet-list-only pages; alternate with visual layouts (fact, quote, image-right, card grid)
- Copy should be specific — use real nouns, platform names, module names
- Prefer Markdown tables over HTML tables
- If HTML tables are necessary, always include `<thead>` and `<tbody>`
- For comparisons, prefer card grids or two-column layouts over dense tables

Before generating a formal presentation, you must read [references/presentation-design.md](references/presentation-design.md).

## PDF/PPTX Export Caveats

When the user needs PDF or PPTX output:

- **Mermaid diagrams**: work but may have timing issues with complex diagrams (>15 nodes). Keep them simple or use card grids.
- **Click animations**: each `v-click` step becomes a separate PDF page. Use `--per-slide` flag to get one page per slide: `npx slidev export --format pdf --per-slide`
- **External images must be accessible** at export time — use full Unsplash URLs with `?auto=format&fit=crop&w=1920&q=80`
- **PPTX is image-based** — each slide is a screenshot, not editable PowerPoint. Warn the user.
- **Test with PDF first** before exporting PPTX — PDF is more reliable
- `export.js` will auto-install `playwright-chromium` if missing

## Style Parameters

Determined by the current task, not hard-coded:

- `formal` — Restrained, stable structure, minimal decoration. Use `seriph` theme, light color scheme, 1-2 Unsplash backgrounds.
- `executive` — Emphasizes conclusions, comparisons, action items. Use `seriph`, light, fact/statement layouts for key numbers.
- `technical` — Higher information density, code blocks OK. Use `default` theme, dark color scheme, more code examples.
- `launch` — Stronger visual impact, more background images. Use `apple-basic`, light, image-heavy layouts (image-right, intro-image, 3-images).

Default: `formal`. Switch based on user's explicit request.

## Language Parameter

- `auto` — Follow the primary language of the user's current message
- `zh` — Chinese deck
- `en` — English deck

Do not force English if user does not specify.

## Post-Generation Checklist

After completing `slides.md`, verify:

1. Does the cover page have a background image?
2. Are there at least 2-3 non-default layouts used?
3. Are there any plain-white section divider pages? (Fix: add gradient or image background)
4. Are there more than 3 consecutive bullet-list pages? (Fix: insert a fact, quote, or image-right page)
5. If targeting PDF export: are there any Mermaid diagrams? (Fix: replace with card grids)
6. Does the closing page have a background?
7. Does any single page have more than 6 main blocks?
8. Is there overflow risk on the last page, architecture page, or two-column pages?

## Common Errors

### Slidev Not Found

Run `npx slidev --version` in the project directory. If it fails, run `node scripts/init-project.js --dir ~/slidev-ppt`.

### Export Failure

Check: (1) current directory is a Slidev project, (2) `playwright-chromium` is installed, (3) `slides.md` can start in preview mode.

### Ugly Output

If the exported deck looks like a plain text document: you forgot backgrounds, used only default layout, and didn't apply visual recipes. Go back to the Visual Design Recipes section and redo the slides.

## Expected Behavior After Triggering

When the user says "help me make a PPT about X":

1. Confirm topic, style, page count, output target
2. Check/initialize Slidev project
3. **Write a complete, visually designed `slides.md`** with backgrounds, varied layouts, and styled content — NOT a bullet-point outline
4. Provide preview method
5. When the user requests export, execute export

Do not just return a list of commands; actually write the slides.md file.
