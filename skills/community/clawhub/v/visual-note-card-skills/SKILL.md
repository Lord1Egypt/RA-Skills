---
name: visual-note-card
description: Generate professional Chinese visual note cards (视觉笔记卡片/信息图) as single-page HTML infographics with automatic PNG export. Use this skill whenever the user asks to create a visual note, knowledge card, infographic, one-pager summary, visual summary, 知识卡片, 视觉笔记, 信息图, 一页纸总结, or any poster-style knowledge visualization. Also trigger when the user wants to summarize an article, blog post, book chapter, or concept into a structured visual card format, or when they reference an existing visual note and ask to create one in the same style. This skill produces both a self-contained HTML file and a high-quality PNG image, ready for sharing on social media or printing.
---

# Visual Note Card Generator

Create professional, information-dense visual note cards (视觉笔记/信息图) as self-contained HTML files with automatic PNG export via Playwright. The output is a structured, poster-style infographic with modular card layout, suitable for social media sharing or printing.

## Design System

Before writing any code, read the reference template at `assets/template.html` for the canonical HTML/CSS structure. Then adapt the content to the user's topic.

### Core Visual Identity

The design follows an **editorial knowledge card** aesthetic — high information density with clear visual hierarchy, inspired by premium magazine layouts and structured note-taking.

**Color Palette (CSS Variables):**
- `--primary`: Deep teal `#1a7a6d` — headers, badges, accent elements
- `--primary-dark`: `#145f54` — bottom highlight bar
- `--primary-deep`: `#0d3d36` — deep accent
- `--accent`: Orange `#e8713a` — emphasis, secondary badges, important labels
- `--bg`: Warm gray `#f0ebe4` — page background
- `--bg-light`: `#f5f1ec` — light panel background
- `--bg-card`: `#e8e3dc` — framework card background
- `--black`: `#1a1a1a` — dark panel, primary text
- `--white`: `#ffffff`

Users may request alternate color schemes. If so, maintain the same structural contrast ratios: one warm neutral background, one strong primary color, one accent color, and black for dark panels.

**Typography:**
- English display: `Playfair Display` (serif, 700/900) — main title
- Chinese body: `Noto Sans SC` (400/500/700/900) — all Chinese text
- Monospace: `JetBrains Mono` (500/700) — labels, URLs, tags
- Import via Google Fonts in the `<style>` block

**Layout — Fixed Poster Dimensions:**
- Container width: `1200px`
- Padding: `36px 40px 28px`
- Background: `var(--bg)`

### Mandatory Layout Sections (Top to Bottom)

Every visual note card MUST include these sections in order:

#### 1. Top Bar
A single-line flex row with:
- Left: Topic label in uppercase monospace (e.g., `AI PRODUCT ARCHITECTURE · SYSTEM DESIGN`)
- Right: Source label (e.g., `OPENAI ENGINEERING BLOG`)

#### 2. Main Title Area
Two-column flex layout:
- Left: Large bilingual title — English line in `Playfair Display 38px`, Chinese line in `Noto Sans SC 40px` colored with `var(--primary)`
- Right: A 2–3 line **thesis statement** (核心观点) summarizing the card's argument, with the key phrase in `<strong>`. Optionally include a source URL below.

#### 3. Framework Row (Flexible Grid, Recommended 4 Columns)

A row of equal-width cards representing the core framework/model of the topic. The number of columns is flexible — choose based on the actual content:

- **2 columns** — binary concepts, comparisons (e.g., Before vs After, Input vs Output)
- **3 columns** — triads, triangular models (e.g., People-Process-Technology)
- **4 columns** — **recommended default**, most common for frameworks (e.g., E-K-C-F, M-P-D-G)
- **5 columns** — five-element models (e.g., HEART metrics, Five Forces)
- **6 columns** — extended taxonomies (use sparingly, keep descriptions very short)

Analyze the topic and choose the column count that best fits the natural structure. Don't force 4 columns if the concept has 3 or 5 natural parts.

**CSS implementation:** Use `grid-template-columns: repeat(N, 1fr)` where N is the chosen column count.

**Card structure (same regardless of column count):**
- Each card has a colored square **letter badge** (first letter of the concept) + Chinese name
- Below the badge: 1–2 lines of description with one `<strong>` keyword
- For 5–6 columns, keep descriptions to 1 line to avoid overflow

**Badge color rotation** (cycles through these in order):
1. `--primary` (teal)
2. `--primary` (teal)
3. `--accent` (orange)
4. `--primary-deep` (deep teal)
5. `--accent` (orange) — if 5th column exists
6. `--primary` (teal) — if 6th column exists

The framework should be a **memorable acronym** (e.g., E-K-C-F, M-P-D-G). Invent one if the source doesn't provide it.

#### 4. Two-Column Content Area
A `grid-template-columns: 1fr 1fr` layout:

**Left: Dark Panel** (`background: var(--black)`, white text)
- Section title with emoji icon (⚡, 🔥, 🛠, etc.)
- 2 sub-blocks, each with an orange title (`var(--accent)`) and a bulleted list (custom `■` bullets in teal)
- List items use `<strong>` for key phrases (white color)
- A bottom "conclusion" block with a divider line and a memorable quote/insight (key phrase in `#5ee6d0` mint color)

**Right: Light Panel** (`background: var(--bg-light)`)
- Section title with star icon (★)
- 3–4 numbered insight items, each with:
  - A large serif number (`Playfair Display 36px`, teal)
  - Bold title line
  - 1–2 lines of description with `<strong>` keywords

#### 5. Bottom Highlight Bar
Full-width bar with `background: var(--primary-dark)`:
- Left: The framework formula (e.g., `Architecture = M × P × D × G`) in mint highlight color `#5ee6d0`
- Right: A closing thought in lighter text

#### 6. Footer
Flex row:
- Left: Framework label in monospace
- Right: Brand / framework name with a small teal dot separator

## Content Strategy

When the user provides a topic (or an article URL/text):

1. **Extract or synthesize a 4-part framework** — find the core structural model. If one doesn't exist, create a meaningful decomposition with a memorable acronym.
2. **Write a provocative thesis** — the right-side subtitle should be a strong, opinionated claim, not a bland description.
3. **Dark panel = "Story + Transformation"** — use this for narrative content: problems, transitions, role changes, paradigm shifts.
4. **Light panel = "Pitfalls or Insights"** — use this for actionable numbered takeaways.
5. **Bottom formula** — distill the entire card into one equation-style summary.
6. **All text is Chinese** except for: the main English title line, technical terms, framework acronyms, and footer labels.

## Output

### Default: HTML + PNG

By default, generate **both** an HTML file and a PNG image:

1. **Generate the HTML** — single self-contained `.html` file with all CSS inline. No external dependencies except Google Fonts and html2canvas CDN. Save to `/mnt/user-data/outputs/`.
2. **Generate the PNG** — run the bundled `scripts/html2png.py` script to render the HTML into a high-quality PNG image.

```bash
python <skill-path>/scripts/html2png.py /mnt/user-data/outputs/card.html /mnt/user-data/outputs/card.png --scale=1.5
```

Present **both** files to the user (PNG first, then HTML). The PNG is the primary deliverable for sharing; the HTML enables further browser-based export or editing.

If the user explicitly asks for "只要 HTML" or "HTML only", skip the PNG step.

### PNG Generation Script: `scripts/html2png.py`

A Playwright-based headless renderer. It opens the HTML in Chromium, waits for Google Fonts to load, hides the FAB button, then screenshots the `.poster` element.

**Usage:**
```bash
python html2png.py <input.html> [output.png] [--scale=N]
```

**Scale options:**
- `--scale=1` — standard (1200px wide), smallest file
- `--scale=1.5` — **default**, recommended for social media (1800px wide)
- `--scale=2` — print quality (2400px wide)

**Dependencies:** `playwright` (pip install playwright && playwright install chromium). Pre-installed on Claude's compute environment.

### Download Button (Mandatory in HTML)

Every generated HTML card MUST include a **floating action button (FAB)** in the bottom-right corner with a dropdown menu for export options:

- **标准 PNG** — 1× scale, quick sharing
- **高清 PNG** — 1.5× scale, social media recommended
- **超清 PNG** — 2× scale, for printing
- **JPEG** — 1.5× scale, smaller file size

Implementation:
1. Add `<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>` before `</body>`
2. The FAB (`div.fab-wrap`) is placed OUTSIDE `.poster` so it won't appear in the exported image
3. Clicking the FAB toggles a dropdown menu upward; clicking outside closes it
4. During capture, the FAB is hidden and a toast spinner ("正在导出…") is shown
5. The FAB icon toggles between a download arrow and a close ×
6. The exported filename is derived from `document.title` + scale suffix

See `assets/template.html` for the complete FAB HTML, CSS, and JS.

### Copyright (Mandatory)

Every card MUST include a copyright bar **inside** the `.poster` div (below the footer, separated by a thin border-top), so it appears in both the HTML page and the exported PNG:

```html
<div class="copyright-bar">
  <svg><!-- GitHub icon --></svg>
  <span>Generated by <a href="https://github.com/beilunyang/visual-note-card-skills">https://github.com/beilunyang/visual-note-card-skills</a></span>
</div>
```

## Example Prompts → Expected Behavior

| User Says | Action |
|-----------|--------|
| "帮我做一张关于 RAG 架构的视觉笔记" | Generate HTML + PNG about RAG architecture |
| "把这篇文章做成信息图" + article text | Extract key ideas, synthesize framework, generate HTML + PNG |
| "生成一张同风格的卡片，主题是微服务" | Generate HTML + PNG about microservices |
| "Create a visual note about product-market fit" | Generate bilingual HTML + PNG about PMF |
| "只要 HTML，不要图片" | Generate HTML only, skip PNG |
| "生成一张 2x 高清的 PNG" | Generate HTML + PNG with `--scale=2` |
