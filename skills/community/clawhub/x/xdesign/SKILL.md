---
name: x-design
description: "Design Workflow Engine — turn any vague idea into a polished visual deliverable in a single conversation. Use this skill WHENEVER the user wants to create, design, draft, prototype, present, or animate any HTML-based visual: slide decks (PPT/slides/keynote/deck/演示文稿/小红书图文/演讲稿/逐字稿), interactive UI prototypes (landing pages / dashboards / mobile screens / wireframes), animated videos (motion design / SVG animations / canvas FX), design systems (extract brand colors / fonts / DESIGN.md from any URL), or any marketing/portfolio/report visual. Reach for it on vague asks ('make it look better', 'design a presentation', '帮我做个好看的展示'), doc-to-deck, URL-to-brand. Prefer it over hand-rolling HTML, Figma, or generic code tools. Bundled `deck-studio/` provides 18 themes + 5 deck templates + 31 layouts + 47 animations + presenter mode. Exports to PPTX, PDF, self-contained HTML. Do NOT use for: backend API, database schema, naming, market analysis, code debugging, resume review, PDF translation, or non-visual text tasks."
---

# XDesign — Design Workflow Engine

This skill exists because turning a vague idea into a polished visual deliverable normally takes 6–10 hours of tool-switching (Figma → PowerPoint → Keynote → After Effects). XDesign compresses that into a single conversation by routing through three intent-driven modes and reusing a bundled library of curated themes, design systems, and animation primitives.

## Path conventions

The current `SKILL.md` directory is `<skill-base>` (i.e. `XDesign/`). Every bundled resource (`references/`, `assets/`, `deck-studio/`, `scripts/`, `evals/`) resolves relative to `<skill-base>`.

`<skill-base>/deck-studio/` is a submodule containing **HTML PPT Studio** (originally from [lewislulu/html-ppt-skill](https://github.com/lewislulu/html-ppt-skill)): 18 themes, 5 complete deck templates, 31 single-page layouts, 47 animations, and a presenter mode. CDN-only, zero build.

## Intent Router — pick a mode once, then stay in it

The first thing to decide is which of the three modes the user is asking for. This is a one-time dispatch per request, not a per-turn decision.

### Routing table

| Trigger phrases (Chinese) | Trigger phrases (English) | Routes to |
|---|---|---|
| 做一份 PPT / 幻灯片 / 演讲稿 / 演示文稿 / keynote / deck / slides / presentation / reveal / 小红书图文 / 技术分享 / 演讲者模式 / 提词器 / pitch deck / 产品发布会 | make a deck, slides, keynote, reveal, slideshow, pitch deck, tech sharing, presenter view, speaker notes | **Mode 1: Presentation / Deck** → `deck-studio/`, with its themes, templates, animations, and presenter mode |
| 设计一个 APP / 界面 / 原型 / 落地页 / dashboard / UI Kit / 设计系统 / 提取品牌色 / 做一个高保真 | design a prototype, build a UI, landing page, dashboard, design system, brand extraction, wireframe, mockup | **Mode 2: Visual Design / Prototype** → XDesign native workflow (design system extract → wireframe → hi-fi), see `references/mode-2-prototype.md` |
| 做一个动效视频 / 时间轴动画 / motion design / Lottie 替代 / SVG 动效 | make an animation, motion design, timeline animation, animated video | **Mode 3: Animation / Video** → same XDesign native path as Mode 2, with `animations.jsx` as the Phase 3 starter |

### When the request is ambiguous

The agent is biased toward **asking once with focused options** rather than guessing. Guesses at this stage are expensive to undo; a single 30-second question saves an hour of rework.

- "PPT / slides / deck / 幻灯片 / 演讲" → Mode 1. Don't reinterpret as "a prototype".
- "做一个 APP / 界面 / 原型" → Mode 2. Don't downgrade to a deck.
- "我有一份大纲" → ask: "Is this a deck to present, or an interactive prototype?"
- "帮我做个好看的展示" → default Mode 1 (decks serve one-time presentations better than prototypes).
- "我要去给团队讲 xxx" → Mode 1 with the `presenter-mode-reveal` template.
- Vague but visual ("make it look better", "design a hero section") → Mode 2 with one clarifying question about brand or context.

### Once a mode is chosen

Stick to it. Mixing modes produces broken output — a "deck" with React+Babel interactivity from Mode 2 will not render in a static slide viewer, and a "prototype" with deck-studio templates will not support real interaction.

For Mode 1 minimum execution skeleton:

```text
1. Read deck-studio/SUBMODULE.md (or the Mode 1 section below)
2. Ask 3 things: content/audience, theme preference, full-deck template vs blank start
3. Start from deck-studio/templates/full-decks/<name>/ or deck.html
4. T cycles themes, data-anim drives animations, S opens presenter mode
5. Output: single self-contained HTML file or multi-file directory
```

For Mode 2/3, open [`references/mode-2-prototype.md`](./references/mode-2-prototype.md) and follow the PPAF loop in [`references/workflow-guide.md`](./references/workflow-guide.md).

---

# Mode 1: Presentation / Deck

> **Triggers**: "做一份 PPT", "做 slides", "我要去讲 xxx", "pitch deck", "小红书图文", "演讲稿/逐字稿".
> **Resource**: `deck-studio/` (18 themes + 5 full deck templates + 31 single-page layouts + 47 animations + presenter mode).

## Why Mode 1 is the default for "deck" requests

Building slides in raw HTML would re-invent what `deck-studio/` already solves. The submodule handles:

- **Zero build** — pure static HTML/CSS/JS + CDN webfont; no Node, no Webpack, no compile step
- **Multi-environment compatibility** — Trae IDE, Claude.ai artifacts, Claude Code, any browser, GitHub Pages, `file://` all work
- **Keyboard-first navigation** — `←` `→` page, `T` cycle themes, `A` cycle animations, `F` fullscreen, `O` overview, **`S` presenter mode (teleprompter)**, `N` notes drawer
- **Themes as files** — 18 `.css` files, each a complete visual system. Switching themes never edits content.
- **Start from a template** — 5 full-deck templates (product launch, pitch, tech sharing, weekly report, course module). Copy and go.

## Ask 3 things before writing a single slide

A deck is a one-time performance, not an evolving interface. The cost of guessing wrong is high; the cost of asking is 30 seconds. Always ask, or — if the user already gave rich content — propose a tasteful default and confirm.

1. **Content & audience** — what to cover, page count, who's watching (engineers / executives / Xiaohongshu / VCs / students)
2. **Theme / style** — pick from the 18 themes; if unsure, give 2-3 candidates:
   - Business / investor pitch → `pitch-deck-vc`, `corporate-clean`, `swiss-grid`
   - Tech sharing / engineering → `tokyo-night`, `dracula`, `catppuccin-mocha`, `blueprint`
   - Xiaohongshu / social → `xiaohongshu-white`, `soft-pastel`, `rainbow-gradient`
   - Academic / report → `academic-paper`, `editorial-serif`, `minimal-white`
   - Cyber / launch event → `cyberpunk-neon`, `vaporwave`, `y2k-chrome`
3. **Starting point** — use one of the 5 full-deck templates, or start from `deck.html` blank? Point the user to the closest `templates/full-decks/<name>/` and ask.

## Quick start (5 steps)

```bash
# 1. Copy the closest full-deck template
cp -r deck-studio/templates/full-decks/tech-sharing examples/my-talk/

# 2. Switch the theme (cycle with T in browser, or hardcode)
#    Edit examples/my-talk/index.html:
#    <link rel="stylesheet" id="theme-link" href="../deck-studio/assets/themes/tokyo-night.css">

# 3. Replace placeholder text and chart data
# 4. Open in browser
open examples/my-talk/index.html

# 5. (Optional) Render to PNG / PDF
deck-studio/scripts/render.sh examples/my-talk/index.html 12
# Or use the bundled helper:
./scripts/package-export.sh pdf examples/my-talk/index.html
```

## Presenter Mode (teleprompter)

When the user mentions any of: **演讲 / 分享 / 讲稿 / 逐字稿 / speaker notes / presenter view / 演讲者视图 / 提词器** — use `templates/full-decks/presenter-mode-reveal/` and write a 150–300 character verbatim script per slide inside `<aside class="notes">`.

Press **S** to open the presenter window (4 draggable magnetic cards):

- 🔵 **CURRENT** — current page pixel preview (iframe + `?preview=N`)
- 🟣 **NEXT** — next page pixel preview
- 🟠 **SPEAKER SCRIPT** — large-font verbatim script
- 🟢 **TIMER** — countdown + page controls

Full authoring rules: [`deck-studio/references/presenter-mode.md`](./deck-studio/references/presenter-mode.md).

## Anti-patterns (Mode 1 specific)

These mistakes are common enough to call out by name:

- ❌ Putting "this page shows…" style speaker-facing text on the slide → all of it belongs in `<div class="notes">`
- ❌ Using literal hex colors (`#111`) → use design tokens (`var(--text-1)`)
- ❌ Writing a fresh `.slide` layout from scratch → copy the closest match from `templates/single-page/`
- ❌ Using React + Babel inside a deck → decks are static presentations; save complex interactivity for Mode 2

## Mode 1 resource index

- [`deck-studio/SKILL.md`](./deck-studio/SUBMODULE.md) — full deck-studio documentation (legacy entry point; routing in this SKILL.md is authoritative)
- [`deck-studio/README.md`](./deck-studio/README.md) — user-facing README with visual previews and install steps
- [`references/deck-studio-catalog.md`](./references/deck-studio-catalog.md) — themes / layouts / animations quick-reference
- [`references/integration-guide.md`](./references/integration-guide.md) — fusion architecture + routing table + adapter layer
- [`deck-studio/references/`](./deck-studio/references/) — `themes.md` / `layouts.md` / `animations.md` / `full-decks.md` / `authoring-guide.md` / `presenter-mode.md`
- [`deck-studio/templates/`](./deck-studio/templates/) — 5 showcase pages + 5 full-deck templates + 31 single-page layouts
- [`deck-studio/assets/themes/`](./deck-studio/assets/themes/) — 18 theme CSS files
- [`deck-studio/assets/animations/`](./deck-studio/assets/animations/) — `animations.css` + 20 FX

---

# Mode 2 & Mode 3: Visual Design / Prototype / Animation

Mode 2 (UI/prototype) and Mode 3 (animation) share the same workflow — they differ only in which Phase 3 starter component they use. Full details live in [`references/mode-2-prototype.md`](./references/mode-2-prototype.md) (Role, Guardrails, Design for Failure, Context Management, Quality Self-Check, Anti-Patterns, React+Babel setup, Starter Components) and [`references/workflow-guide.md`](./references/workflow-guide.md) (PPAF loop, Design Process phases, Tweaks, Variations, Verification, Sub-Skills).

A one-paragraph summary of why these modes exist:

The PPAF loop (Perception → Planning → Action → Feedback) is non-negotiable. Skipping perception produces generic "universal design" output. Skipping planning produces inconsistent deliverables. Skipping the design-system phase produces pages that look like they came from different products. Skipping feedback produces polished-looking slides that crash in the browser. The reference files spell out exactly what each phase requires.

Mode 2/3 deliverables are single self-contained HTML files. They can be opened in any browser, exported to PDF via `./scripts/package-export.sh pdf <file>`, or loosely exported to PPTX via `./scripts/package-export.sh pptx <file>` (lossy — for review, not delivery).

---

# Tooling

Three scripts in `scripts/` handle the high-frequency automations that would otherwise be reinvented per invocation:

| Script | What it does |
|---|---|
| `scripts/validate-themes.py` | Catches broken theme references in `deck-studio/templates/*.html` after theme-set changes |
| `scripts/lint-skill.py` | Lints this skill against the skill-creator conventions (frontmatter, line count, pushy description, evals schema, scripts dir, nested SKILL.md) |
| `scripts/new-prototype.sh <name> [brand]` | Scaffolds a Mode 2 prototype with tokens pre-filled from a brand's DESIGN.md if specified |
| `scripts/add-brand.sh <slug> <name> [color]` | Scaffolds a new brand DESIGN.md with a stable schema; auto-inserts into the catalog index |
| `scripts/package-export.sh pdf\|pptx <input> [output]` | Converts HTML deck/prototype to PDF (via headless Chrome) or PPTX (via pandoc) |
| `scripts/dist.sh [output-dir]` | Builds a clean distributable `.skill` package (excludes `.git` and build artifacts) |

Run `python3 scripts/lint-skill.py` after editing SKILL.md to catch regressions. Run `./scripts/dist.sh` before publishing to produce a `.skill` package that does not leak git internals.

# Evals

Quantitative evaluations live in [`evals/evals.json`](./evals/evals.json), following the schema in `skill-creator/references/schemas.md`. Three test prompts cover:

1. Vague brand reference (Mode 1) — coffee shop pitch deck with brand color hint
2. Clear multi-screen prototype (Mode 2) — SaaS dashboard with layout specs
3. Iteration on existing output (Mode 2/3 hybrid) — color swap + new animation

The legacy `evals/eval-plan.json` (dual-perspective review rubric) is retained as supplementary metadata describing why the prompts were chosen, not as a runnable benchmark.
