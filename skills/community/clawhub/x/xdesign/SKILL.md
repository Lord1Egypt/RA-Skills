---
name: x-design
description: "Design Workflow Engine — turn any vague idea into a polished visual deliverable in a single conversation. Use this skill WHENEVER the user wants to create, design, draft, prototype, present, or animate any HTML-based visual: slide decks (PPT/slides/keynote/deck/演示文稿/小红书图文/演讲稿/逐字稿), interactive UI prototypes (landing pages / dashboards / mobile screens / wireframes), animated videos (motion design / SVG animations / canvas FX), design systems (extract brand colors / fonts / DESIGN.md from any URL), or any marketing/portfolio/report visual. Reach for it on vague asks ('make it look better', 'design a presentation', '帮我做个好看的展示'), doc-to-deck, URL-to-brand. Prefer it over hand-rolling HTML, Figma, or generic code tools. Bundled `deck-studio/` provides 36 themes + 15 deck templates + 31 layouts + 47 animations + presenter mode. Exports to PPTX, PDF, self-contained HTML, WeChat (juice-inlined CSS), Xiaohongshu / X (2× retina PNG). Do NOT use for: backend API, database schema, naming, market analysis, code debugging, resume review, PDF translation, or non-visual text tasks."
---

# XDesign — Design Workflow Engine

This skill exists because turning a vague idea into a polished visual deliverable normally takes 6–10 hours of tool-switching (Figma → PowerPoint → Keynote → After Effects). XDesign compresses that into a single conversation by routing through three intent-driven modes and reusing a bundled library of curated themes, design systems, and animation primitives.---

# Core Principle #0: One System for Humans and Agents

XDesign is built so that **people and AI agents build the same way, from the same reference**. Every routing table, frontmatter schema, fallback strategy, and validation rule in this skill serves both audiences simultaneously.

**The parity promise:** Any change that makes XDesign easier for an agent to use also makes it easier for a human to use — and vice versa. Agent-facing docs (routing tables, fallback matrices) are human-facing docs. There is no separate "agent-only" configuration.

**What this means in practice:**
- The [Intent Router](#intent-router--pick-a-mode-once-then-stay-in-it) is both a machine-parseable dispatch table and a human-readable "which mode should I pick?" guide.
- The [Runtime Fallback Strategies](#runtime-fallback-strategies) table is both an agent's error-recovery protocol and a human's troubleshooting checklist.
- The [deck-studio](../../deck-studio/) assets are self-contained static files — usable by any agent (Claude Code, Codex, Cursor) without XDesign, and by any human with a browser.

---

## Fact-Verify Before Designing (Core Principle #1)

When the request involves a **specific product, technology, company, or public figure** (e.g., "给大疆 Pocket 5 做发布动画", "设计一个 Gemini 4 的 landing page"), `WebSearch` the entity first before starting any design work. Do not rely on training-data memory for existence, version numbers, release dates, or specs.

**Why:** Building a launch animation for a product that released last week — but the model thinks "hasn't launched yet" — wastes the entire session on a wrong assumption. A 10-second search prevents a multi-hour rework.

**Hard rule:** If the search confirms the entity exists and has official assets (logo, product photos, press kit), those become required inputs. See [Brand Asset Protocol](./references/brand-asset-protocol.md).

## 验证第一步必带（Validation-First Step）

无论进入哪个 Mode，在投入完整交付物之前必须先产出一个**最小可验证样本**供用户确认方向。这一步避免"生成完 30 页 deck / 20 屏 prototype 后才发现方向跑偏"的灾难性返工。

| Mode | 最小验证样本 | 确认点 |
|------|-------------|--------|
| Mode 1 Presentation | 1-3 张代表性 slides（封面 + 内容页 + 主题切换各 1） | 主题风格 / 版式节奏 / 字体配色 |
| Mode 2 Prototype | 单个关键页面（首页或核心交互页）的 hi-fi 静态稿 | 视觉风格 / 信息架构 / 品牌还原度 |
| Mode 3 Animation | 关键帧或首尾帧静态图（含 1 段动效预览） | 动效风格 / 节奏 / 视觉语言 |

**执行规则：**
- 用户描述需求后，**先输出最小验证样本**，等用户确认"方向对了"再生成完整交付物
- 用户已给出强约束（"必须用某某主题"、"就按这个模板"、"按上次的风格再做一份"）时可跳过，直接进入完整生成
- 最小样本与最终交付物之间的差异**只允许在量级上**（页数/组件数），不允许在视觉语言上发生根本性变化
- Mode 1 的"Streaming Preview（>8 slides 拆两轮）"是此规则的长 deck 子情况，规则保持一致

## Path conventions

The current `SKILL.md` directory is `<skill-base>` (i.e. `XDesign/`). Every bundled resource (`references/`, `assets/`, `deck-studio/`, `scripts/`, `evals/`) resolves relative to `<skill-base>`.

`<skill-base>/deck-studio/` is a submodule containing **HTML PPT Studio** (originally from [lewislulu/html-ppt-skill](https://github.com/lewislulu/html-ppt-skill)): 36 themes, 15 complete deck templates (each with extended frontmatter for scenario/tags/recommended filtering), 31 single-page layouts, 47 animations, and a presenter mode. CDN-only, zero build.

## Intent Router — pick a mode once, then stay in it

The first thing to decide is which of the three modes the user is asking for. This is a one-time dispatch per request, not a per-turn decision.

### Format Auto-Detect (fast path)

Before routing, check if the user's input is **structured data** rather than a design request. If yes, skip design-system extraction and go straight to visualization.

| Input signal | Detection heuristic | Fast path |
|---|---|---|
| CSV / TSV | Commas/tabs separating rows; first row looks like headers | → Mode 2, skip Perception. Render as interactive table or chart |
| JSON array | `[ {…}, {…} ]` with consistent keys | → Mode 2, skip Perception. Infer chart type from data shape |
| SQL result | Tabular text with `├──` or `│` box-drawing separators | → Mode 2, skip Perception. Render as data grid |
| Markdown table | `| col | col |` with `---` separator | → Mode 2, skip Perception. Render as styled table |

**When auto-detected:** Tell the user "检测到结构化数据，跳过设计系统阶段，直接生成 [table/chart/dashboard]。" Then open `references/mode-2-prototype.md` at the Planning phase (skip Perception). Use a neutral design system (e.g., `corporate-clean` theme tokens) unless the user specifies otherwise.

**When ambiguous:** If the input mixes data with design intent ("把这个 CSV 做成 Stripe 风格的 dashboard"), do not auto-detect — follow the normal routing and run Perception to extract the Stripe design system.

### Routing table

| Trigger phrases (Chinese) | Trigger phrases (English) | Routes to |
|---|---|---|
| 做一份 PPT / 幻灯片 / 演讲稿 / 演示文稿 / keynote / deck / slides / presentation / reveal / 小红书图文 / 技术分享 / 演讲者模式 / 提词器 / pitch deck / 产品发布会 | make a deck, slides, keynote, reveal, slideshow, pitch deck, tech sharing, presenter view, speaker notes | **Mode 1: Presentation / Deck** → `deck-studio/`, with its themes, templates, animations, and presenter mode |
| 设计一个 APP / 界面 / 原型 / 落地页 / dashboard / UI Kit / 设计系统 / 提取品牌色 / 做一个高保真 | design a prototype, build a UI, landing page, dashboard, design system, brand extraction, wireframe, mockup | **Mode 2: Visual Design / Prototype** → XDesign native workflow (design system extract → wireframe → hi-fi), see `references/mode-2-prototype.md` |
| 做一个动效视频 / 时间轴动画 / motion design / Lottie 替代 / SVG 动效 | make an animation, motion design, timeline animation, animated video | **Mode 3: Animation / Video** → same XDesign native path as Mode 2, with `animations.jsx` as the Phase 3 starter |
| 审查 / 检查 / audit / review / 把关 / 无障碍 / accessibility / a11y / WCAG / polish / 上线前检查 / 帮我审一下 | audit this, review for issues, accessibility check, a11y, polish pass, review this page | **Review Mode** → [`references/review-passes.md`](./references/review-passes.md)（4 pass：Accessibility / AI-Slop / Hierarchy & Rhythm / Interaction States；可审任意 HTML，不依赖生产流） |

### When the request is ambiguous

The agent is biased toward **asking once with focused options** rather than guessing. Guesses at this stage are expensive to undo; a single 30-second question saves an hour of rework.

**Template-first fallback:** When the user gives a vague request ("帮我做个 PPT"), check `deck-studio/templates/full-decks/*/README.md` frontmatter `scenario` and `tags` to narrow to 2-3 candidates, then ask "这风格更接近哪种？" rather than "选哪个模板？".

- "PPT / slides / deck / 幻灯片 / 演讲" → Mode 1. Don't reinterpret as "a prototype".
- "做一个 APP / 界面 / 原型" → Mode 2. Don't downgrade to a deck.
- "我有一份大纲" → ask: "Is this a deck to present, or an interactive prototype?"
- "帮我做个好看的展示" → default Mode 1 (decks serve one-time presentations better than prototypes).
- "我要去给团队讲 xxx" → Mode 1 with the `presenter-mode-reveal` template.
- Vague but visual ("make it look better", "design a hero section", "帮我设计个页面") → Mode 2, but check whether the user gave any brand/reference. If none, route to the **Design Direction Advisor** ([references/design-direction-advisor.md](./references/design-direction-advisor.md)) — produce 3 differentiated visual directions before committing to a full build.

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

### Review Mode (cross-cutting)

Review Mode 可在任何 Mode 产出后、或对任意外部 HTML 独立运行。它不是生产模式的替代，而是独立的质检层——4 个 pass（Accessibility / AI-Slop / Hierarchy & Rhythm / Interaction States）可单跑可全跑。生产流内的 CP4 是"出厂自检"，Review Mode 是"独立质检站"。触发词与执行流程见 [`references/review-passes.md`](./references/review-passes.md)。

---

# Mode 1: Presentation / Deck

> **Triggers**: "做一份 PPT", "做 slides", "我要去讲 xxx", "pitch deck", "小红书图文", "演讲稿/逐字稿".
> **Resource**: `deck-studio/` (36 themes + 15 full-deck templates + 31 single-page layouts + 47 animations + presenter mode).
> **Template metadata**: Each template README has extended frontmatter (`mode / scenario / surface / recommended / tags / example_id`) for structured filtering. See [Template Matching](#template-matching-mode-1).

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
3. **Starting point** — use one of the 15 full-deck templates, or start from `deck.html` blank? Filter templates by `scenario` frontmatter; pick the lowest `recommended` score that matches. When in doubt, present 2-3 options sorted by `recommended` ascending.

## Quick start (5 steps)

```bash
# 1. Copy the closest full-deck template (sort by `recommended` in README frontmatter)
cp -r deck-studio/templates/full-decks/tech-sharing/examples/my-talk/

# 2. Switch the theme (cycle with T in browser, or hardcode)
#    Edit examples/my-talk/index.html:
#    <link rel="stylesheet" id="theme-link" href="../deck-studio/assets/themes/tokyo-night.css">

# 3. Replace placeholder text and chart data
# 4. Open in browser
open examples/my-talk/index.html

# 5. (Optional) Render to PNG / PDF / social
deck-studio/scripts/render.sh examples/my-talk/index.html 12
# Or use the bundled helper:
./scripts/package-export.sh pdf examples/my-talk/index.html
# Social export (WeChat / XHS / X):
./scripts/package-export.sh social wechat examples/my-talk/index.html
```

## Template Matching (Mode 1)

Each full-deck template has extended frontmatter for filtering. Use these fields to narrow the picker when the user's intent is specific:

| If user asks for… | Filter by `scenario` | First pick (lowest `recommended`) |
|---|---|---|
| 技术分享 / 开发者分享 | `engineering` | `tech-sharing` (15) |
| 创业融资 / pitch / VC | `marketing` | `pitch-deck` (20) |
| 产品发布 / 新品上线 | `marketing` | `product-launch` (25) |
| 小红书 / 社交图文 | `social` | `xhs-pastel-card` (30) |
| 周报 / 团队同步 | `general` | `weekly-report` (40) |
| 安全告警 / 事故复盘 | `engineering` | `testing-safety-alert` (45) |
| 课程 / 教学 | `education` | `course-module` (60) |
| 工具测评 / 技术Review | `engineering` | `hermes-cyber-terminal` (65) |
| 知识图谱 / 架构图 | `engineering` | `graphify-dark-graph` (70) |
| 极简 / 方向键导航 | `general` | `dir-key-nav-minimal` (75) |
| 个人笔记 / 学习笔记 | `personal` | `obsidian-claude-gradient` (80) |

When none of the above match, fall back to `presenter-mode-reveal` (50) for any presentation with speaker notes, or `weekly-report` (40) for a generic structured deck.

## Presenter Mode (teleprompter)

When the user mentions any of: **演讲 / 分享 / 讲稿 / 逐字稿 / speaker notes / presenter view / 演讲者视图 / 提词器** — use `templates/full-decks/presenter-mode-reveal/` and write a 150–300 character verbatim script per slide inside `<aside class="notes">`.

Press **S** to open the presenter window (4 draggable magnetic cards):

- 🔵 **CURRENT** — current page pixel preview (iframe + `?preview=N`)
- 🟣 **NEXT** — next page pixel preview
- 🟠 **SPEAKER SCRIPT** — large-font verbatim script
- 🟢 **TIMER** — countdown + page controls

Full authoring rules: [`deck-studio/references/presenter-mode.md`](./deck-studio/references/presenter-mode.md).

## Streaming Preview (long decks)

When a deck will exceed **8 slides**, generate in two passes so the user can preview direction before you commit to the full output:

1. **Pass 1** — Write slides 1–5 to `<output>/deck-preview.html` with:
   - `deck-studio/assets/base.css` + `deck-studio/assets/fonts.css` + chosen theme CSS
   - `deck-studio/assets/runtime.js` (so `←` `→` `T` `F` work)
   - A `<div id="partial-banner">` at the top: "部分预览 · 1-N / 总 M 张 · 生成中…" (sticky, dismissible)
   - `data-partial="true"` on `<body>` for CSS targeting
   - Open the file in the browser/artifact panel
1. **Pass 2** — Generate the full deck with all slides. If the user liked the direction, write to the final output file. If they asked for changes, regenerate the full deck with corrections; keep `deck-preview.html` for diffing.
3. **Cleanup** — Delete `deck-preview.html` once the user confirms the final deck, unless they asked to keep it.

**Do NOT split** decks with ≤8 slides — the overhead of two writes outweighs any benefit. Do NOT split at slide boundaries that break narrative flow (a "6-slide problem statement + 10-slide solution" is fine; splitting a 4-slide timeline in half is not).

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

**Format auto-detect fast path:** When the user provides structured data (CSV / JSON / SQL), the [Format Auto-Detect](#format-auto-detect-fast path) entry point routes directly to `references/mode-2-prototype.md` Phase 2 (Planning), skipping Phase 1 (Perception / design system extraction). The output is a data visualization (table, chart, or dashboard) rather than a branded prototype.

A one-paragraph summary of why these modes exist:

The PPAF loop (Perception → Planning → Action → Feedback) is non-negotiable. Skipping perception produces generic "universal design" output. Skipping planning produces inconsistent deliverables. Skipping the design-system phase produces pages that look like they came from different products. Skipping feedback produces polished-looking slides that crash in the browser. The reference files spell out exactly what each phase requires.

Mode 2/3 deliverables are single self-contained HTML files. They can be opened in any browser, exported to PDF via `./scripts/package-export.sh pdf <file>`, or loosely exported to PPTX via `./scripts/package-export.sh pptx <file>` (lossy — for review, not delivery).

## Design Direction Advisor (Mode 2/3 fallback for vague requests)

When Mode 2/3 receives a request with **no brand name, no screenshot, no reference URL**, do not produce a generic "universal design." Instead, route to the [Design Direction Advisor](./references/design-direction-advisor.md): generate **3 differentiated visual directions** (Information-first → Balanced → Concept-led), let the user pick, then enter the normal PPAF loop with the confirmed direction. The Advisor uses the existing 36 themes + 58 brand DESIGN.md files as its ammunition library — no new assets needed.

**Motion-specific additions** (v2.7+): The Advisor now includes `ANIMATION_FREQUENCY` dial (based on usage frequency — high-frequency interactions get reduced/no animation), and a [Motion Vocabulary](./references/design-direction-advisor.md#motion-vocabulary-translate-vague-requests-to-precise-terms) translation table to convert vague descriptions ("弹一下") into precise animation parameters.

**Progressive Intake** (v2.7+): When the user gives a vague request ("做个落地页"), the agent MUST run the [3-round intake interview](./references/mode-2-prototype.md#progressive-intake-interview-for-vague-requests) — structured multiple-choice questions that guide the user to provide useful constraints without forcing them to make design decisions. Max 3 rounds, then proceed with inference.

## Animation Quality Standards (Mode 3)

For Mode 3 (Animation/Video) deliverables, the [Animation Reason Checklist](./references/animation-standards.md#animation-reason-checklist-mode-3-mandatory-before-generating) is **mandatory** — every animation must justify itself with a functional reason (spatial consistency, state indication, relationship explanation, prevent disorientation, or feedback). Animations without a valid reason are removed rather than generated.

Additionally, 7 animation-specific [Pre-flight Checks](./references/animation-standards.md#pre-flight-animation-quality-rules-additive-to-existing-checks) (#11-#17) run after the existing CP4 checklist, covering duration bounds, easing curves, GPU-layer properties, touch device safety, and reduced-motion granularity.

**Physical correctness default:** Entrance animations start from `scale(0.95) + opacity: 0` (elements don't appear from nothing), not `scale(0)`. See `deck-studio/assets/animations/animations.css` for the updated defaults.

---

# Tooling

A unified CLI entry point dispatching to task-specific scripts:

```bash
# Export
./scripts/xdesign export pdf  <input.html> [output.pdf]
./scripts/xdesign export pptx <input.html> [output.pptx]
./scripts/xdesign export social wechat|xhs|x <input.html> [output]

# Theme management
./scripts/xdesign theme list
./scripts/xdesign theme validate

# Brand scaffolding
./scripts/xdesign brand add <slug> <display-name> [hex]

# Prototype scaffolding
./scripts/xdesign proto new <name> [brand-slug]

# Eject (swizzle) a sub-block from a file
./scripts/xdesign eject <input.html> <block-id> [output.html]

# Lint + package
./scripts/xdesign lint
./scripts/xdesign dist [output-dir]
```

All subcommands proxy to the existing `package-export.sh`, `add-brand.sh`, `new-prototype.sh`, `validate-themes.py`, `lint-skill.py`, and `dist.sh` — the CLI adds a consistent interface, not new logic.

Three scripts in `scripts/` handle the high-frequency automations that would otherwise be reinvented per invocation:

| Script | What it does |
|---|---|
| `scripts/validate-themes.py` | Catches broken theme references in `deck-studio/templates/*.html` after theme-set changes |
| `scripts/lint-skill.py` | Lints this skill against the skill-creator conventions (frontmatter, line count, pushy description, evals schema, scripts dir, nested SKILL.md) |
| `scripts/new-prototype.sh <name> [brand]` | Scaffolds a Mode 2 prototype with tokens pre-filled from a brand's DESIGN.md if specified |
| `scripts/add-brand.sh <slug> <name> [color]` | Scaffolds a new brand DESIGN.md with a stable schema; auto-inserts into the catalog index |
| `scripts/package-export.sh pdf <input> [output]` | Converts HTML deck/prototype to PDF (via headless Chrome) |
| `scripts/package-export.sh pptx <input> [output]` | Converts HTML deck/prototype to PPTX (via pandoc, lossy) |
| `scripts/package-export.sh social wechat <input> [output]` | Juice-inlines CSS for WeChat editor paste (dependency: `juice`) |
| `scripts/package-export.sh social xhs <input> [output]` | Renders 2× retina PNG for Xiaohongshu (dependency: `playwright`) |
| `scripts/package-export.sh social x <input> [output]` | Renders 2× retina PNG for X/Twitter (dependency: `playwright`) |
| `scripts/dist.sh [output-dir]` | Builds a clean distributable `.skill` package (excludes `.git` and build artifacts) |

Run `python3 scripts/lint-skill.py` after editing SKILL.md to catch regressions. Run `./scripts/dist.sh` before publishing to produce a `.skill` package that does not leak git internals.

# Evals

Quantitative evaluations live in [`evals/evals.json`](./evals/evals.json), following the schema in `skill-creator/references/schemas.md`. Eight test prompts cover:

1. Vague brand reference (Mode 1) — coffee shop pitch deck with brand color hint
2. Clear multi-screen prototype (Mode 2) — SaaS dashboard with layout specs
3. Iteration on existing output (Mode 2/3 hybrid) — color swap + new animation
4. URL-to-brand extraction + landing page (Mode 2)
5. Animation with brand constraints (Mode 3)
6. **Vibe test** — anti-slop compliance for premium-consumer landing page
7. **Vibe test** — narrative arc and hierarchy for tech talk deck
8. **Vibe test** — animation justification and reduced-motion for logo reveal

**Vibe tests** (evals 6-8) are inspired by Astryx's "earned by measurement" principle: they test visual quality conventions rather than assert them, using a rubric of dimensions (`anti-slop:gradient`, `pattern:narrative-arc`, `animation:valid-reason`, etc.). Results are held loosely — a failed vibe test signals a rule that may need revisiting, not a hard failure.

The legacy `evals/eval-plan.json` (dual-perspective review rubric) is retained as supplementary metadata describing why the prompts were chosen, not as a runnable benchmark.---

# Architecture: Foundations → Components → Patterns

XDesign's visual capability is organized in three layers, each built on the below:

| Layer | What it provides | Where it lives |
|---|---|---|
| **Foundations** | Visual tokens: color palettes, typography scales, spacing systems, shadow elevation | `deck-studio/assets/themes/`, [deck-studio references](../deck-studio/references/themes.md) |
| **Components** | Single-slide building blocks: 31 layouts covering openers, data displays, diagrams, closers | `deck-studio/templates/single-page/`, [layouts.md](../deck-studio/references/layouts.md) |
| **Patterns** | Multi-slide narrative recipes: 8 battle-tested arcs (pitch, landing, dashboard, narrative, comparison, process, report, course) | [patterns.md](./references/patterns.md) |

**How to use:**
- When the user asks for a **deck**, the Intent Router (Mode 1) picks a template. Patterns suggest which sequence of layouts to use.
- When the user asks for a **prototype** (Mode 2), Foundations provide the tokens, Components provide the building blocks.
- When the request matches a known pattern trigger (e.g., "pitch deck", "dashboard"), reference the pattern by name and fill its slots.

Patterns are defaults, not mandates — if the user provides their own structure, respect it.

---

## Agent Decision Guide

For routing logic, fallback matrices, context management, and error recovery specific to AI agents, see [references/agent-playbook.md](./references/agent-playbook.md).

---

# Runtime Fallback Strategies

When a primary operation fails, follow these fallback paths instead of freezing or hallucinating:

| Failure Scenario | Primary Path | Fallback | Log Action |
|---|---|---|---|
| URL-to-brand: WebFetch fails | Fetch URL → extract tokens → write DESIGN.md | Read `references/design-system-catalog.md` for known brands; if not found, ask user for 3-5 brand tokens manually | Log "WebFetch failed for {url}, falling back to catalog" |
| deck-studio theme CSS not found | Load `deck-studio/assets/themes/<name>.css` | Fall back to `corporate-clean.css` (always present); warn user | Log "Theme {name}.css not found, using corporate-clean" |
| deck-studio template directory not found | Reference `templates/full-decks/<name>/` | Fall back to `templates/single-page/` layouts; build a valid deck from parts | Log "Full-deck template {name} not found, using single-page fallback" |
| runtime.js fails to load | Browser loads `assets/runtime.js` | Deck still renders as static HTML slides (no interactivity); nothing breaks | Log "runtime.js failed to load" |
| Headless Chrome export fails | `scripts/package-export.sh pdf` | Offer manual "Print to PDF" instructions instead | Log "PDF export failed, offering manual alternative" |
| brand DESIGN.md has no color palette | Use DESIGN.md tokens | Derive a default palette from the brand name's dominant color | Log "No palette in DESIGN.md, deriving from brand name" |

# Token Budget Guidelines

XDesign operates in HTML-generation mode, which is token-heavy. Follow these budget limits to avoid context overrun:

| Mode | Typical Output Size | Token Budget | Strategy |
|---|---|---|---|
| Mode 1 (deck) | 1 single-file HTML (6-30 slides) | ~4K-8K tokens | Use scoped CSS classes (`tpl-*`, `xw-*`) to avoid class-name bloat; reuse existing theme CSS instead of inlining |
| Mode 2 (prototype/dashboard) | 1 HTML file with JS interactivity | ~6K-12K tokens | Prefer CSS Grid/Flexbox over repetitive div structures; use CSS variables for consistent theming |
| Mode 3 (animation) | 1 HTML file with Canvas/JS | ~4K-10K tokens | Avoid long keyframe definitions; use JS-driven animation with requestAnimationFrame |
| URL-to-brand (extract) | 1 small DESIGN.md | ~500-1K tokens | Only extract essential tokens (6 colors, 2 fonts, 3 radii, 2 spacing); skip verbose descriptions |
| Iteration (edit) | Incremental diff | ~500-2K tokens | Read target file first; output only changed sections; avoid full-file rewrite |

> **Rule**: If token budget for a mode is exceeded, split the output into multiple responses (e.g., generate the CSS file separately from the HTML body).

# Cross-Agent Compatibility

`deck-studio/` is **self-contained**: every file is static HTML + CSS + JS + CDN webfonts. You can use it from any coding agent (Claude Code, Codex, Cursor, etc.) without XDesign.

**From another agent:**

1. Copy or symlink the `deck-studio/` directory into your project:
   ```bash
   ln -s ~/.trae/skills/XDesign/deck-studio ./deck-studio-assets
   ```
2. Reference assets by relative path in your generated HTML:
   ```html
   <link rel="stylesheet" href="./deck-studio-assets/assets/base.css">
   <link rel="stylesheet" href="./deck-studio-assets/assets/themes/tokyo-night.css">
   <script src="./deck-studio-assets/assets/runtime.js"></script>
   ```
3. Use `deck-studio/templates/full-decks/<name>/index.html` as your starting point — copy and edit.

**Why this works:** No build step, no Node, no bundler. The runtime is vanilla JS toggling `<section class="slide">` visibility. All dependencies are CDN (Google Fonts) or local (themes, animations).

**Limitations:** Without XDesign's routing layer, you lose scenario-based template matching and streaming preview. You pick the template manually. The `README.md` frontmatter in each template still lists `scenario` and `tags` to help you choose.

# Changelog

| Version | Date | Changes |
|---|---|---|
| v2.7 | 2026-07 | **Animation Quality System** + **Progressive Intake**: **#1 Animation Reason Checklist** (mandatory for Mode 3): every animation must justify itself with a functional reason. **#2 Animation Frequency Dial**: `ANIMATION_FREQUENCY` in Design Direction Advisor. **#3 Motion Vocabulary**: vague→precise translation table. **#4 Pre-flight Animation Rules (#11-17)**: duration bounds, easing curves, GPU-layer only, touch safety, reduced-motion granularity. **#5 Physical Correctness Defaults**: `kf-zoom` changed from `scale(.6)` to `scale(.96)`. **#6 Reduced-Motion Granularity**: color-only (always) + transform (suppressed). **#7 Progressive Intake Interview**: 3-round max structured questions for vague requests — guides users to provide constraints without forcing design decisions. |
| v2.6 | 2026-06 | **Anti-Slop Deepening** — inspired by taste-skill methodology research (MIT,理念借鉴/文本原创), added 4 improvements: **#1 Design Preference Layer (P1)**: New section in `mode-2-prototype.md` — deeper bias correction across typography (serif-as-creative-tell, Inter-everywhere), color (premium-consumer farmhouse palette, mid-design drift), layout (centered-hero-over-mesh, equal-card-filler), and motion (purposeless marquee, ambient particles). Each rule has WHY + deliberate alternative. **#2 Three Dials (P2)**: New internal config system in `design-direction-advisor.md` — `DESIGN_VARIANCE / MOTION_INTENSITY / VISUAL_DENSITY` (1-10), inferred from user signals, drives layout/motion/density decisions. Invisible to user, recorded in HTML reasoning block. **#3 Brief Inference 6-Signal (P3)**: Upgraded Phase 1 from 3-question dump to 6-dimension signal scan (page kind / vibe words / references / audience / brand assets / quiet constraints) + one-line "Design Read" output. Ask only when genuinely ambiguous. **#4 Pre-flight Check (P4)**: 10-item mechanical checklist in `mode-2-prototype.md` CP4 — color consistency lock, saturation <80%, italic descender clearance, no orphaned placeholders, marquee ≤1, prefers-reduced-motion, mobile hit targets ≥44px, etc. All content originally authored; no external text reproduced. |
| v2.5 | 2026-06 | **Decision-Support Layer upgrade** — inspired by design methodology research, added 5 new mechanisms: **#1 Design Direction Advisor (P0)**: New `references/design-direction-advisor.md` — when Mode 2/3 receives vague requests with no brand/reference, generates 3 differentiated visual directions (Information-first → Balanced → Concept-led) before committing to full build. Uses existing 36 themes + 58 DESIGN.md as ammunition library. **#2 Brand Asset Protocol (P1)**: New `references/brand-asset-protocol.md` — 5-step hard flow (Ask → Search → Download → Verify → Freeze) for acquiring real brand assets. Two trigger types: designing FOR a brand, and designing WITH identifiable brands. **#3 Anti-AI-Slop Rules (P1)**: Expanded `mode-2-prototype.md` with WHY explanations and legitimate-exception boundaries for each slop pattern. **#4 Image Pre-flight Checkpoint (P2)**: New Phase 1.5 in PPAF loop — content-essential designs must fetch real images before designing, never substitute with CSS blocks. **#5 Fact-Verify Principle #0 (P2)**: WebSearch specific products/technologies before designing — prevents building on wrong assumptions. **#6 Tweaks Template (P3)**: Full HTML/JS implementation template for in-design variation controls with localStorage persistence. **#7 Junior Designer Workflow (P3)**: 4-checkpoint rhythm (Assumptions → Wireframe → First hi-fi → Full) with mandatory HTML reasoning block. All content originally authored; no external text reproduced. |
| v2.4 | 2026-06 | **#1 Extended Frontmatter**: Added mode/scenario/surface/recommended/tags/example_id to all 15 deck template READMEs. Added Template Matching table and scenario-based fallback to SKILL.md routing. Updated deck count 5→15 in path conventions. **#2 Streaming Preview**: Added two-pass generation for decks >8 slides with partial HTML preview + dismissible banner. **#3 Social Export**: Added `social wechat|xhs|x` subcommands to package-export.sh. WeChat = juice-inlined CSS; XHS/X = 2× retina PNG via Playwright. Updated Tooling table. **#4 Format Auto-Detect**: Added fast path for CSV/JSON/SQL/Markdown-table input. Structured data skips Perception phase and routes directly to Mode 2 data visualization. **#5 Cross-Agent Compatibility**: Documented deck-studio as self-contained static assets usable from any coding agent (Claude Code / Codex / Cursor). Added symlink + path reference guide. |
| v2.3 | 2026-06 | Synced deck-studio to 36 themes + 15 full-decks from upstream. Added evals for Mode 3 and URL-to-brand. Created automated eval pipeline (`evals/run-evals.sh`). Added Runtime Fallback Strategies & Token Budget Guidelines. Updated all reference docs to match resource counts. |
