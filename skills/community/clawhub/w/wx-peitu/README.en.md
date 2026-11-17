# wx-peitu · WeChat Article Illustration Generator

🇨🇳 中文版: [README.md](README.md)

[![Stars](https://img.shields.io/github/stars/EdwardWason/wx-peitu?style=flat-square)](https://github.com/EdwardWason/wx-peitu)
[![License](https://img.shields.io/badge/license-MIT--0-green?style=flat-square)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-wx--peitu-orange?style=flat-square)](https://clawhub.ai/skills/wx-peitu)
[![Skill](https://img.shields.io/badge/Claude%20Code-Skill-blue?style=flat-square)](SKILL.md)

[See it in action](#features) · [Get started](#30-second-start) · [Core mechanism](#core-mechanism) · [Limitations](#limitations) · [License](#license)

---

_"Say one sentence, get a full set of WeChat illustrations."_

---

**wx-peitu** is not another Markdown typesetting tool — it's a complete content-to-image illustration system. It doesn't do full-article layout — it extracts visualizable units from your long-form articles and generates a set of **density-qualified, style-consistent, publish-ready** PNG illustration packs, auto-synced to Lark Drive for instant mobile download and publishing.

---

## Features

- 🎨 **Dual visual system**: Editorial for atmosphere & narrative, Swiss for facts & structure, sharing one workflow
- 📐 **5 canvas sizes**: Cover 900×383, body 640×auto, quote 640×272, divider 640×200, back cover 900×383
- 🧩 **20 illustration types**: Cover/back cover, quote cards, data charts, logic chains, process pipelines, version timelines, decision cards, cognitive corrections, manifesto cards, case cards, and more
- 🏗 **24 layout recipes**: E01-E14 Editorial + S01-S10 Swiss, no 3 consecutive same-recipe cards
- 🎯 **4-Purpose framework**: Each illustration tagged with purpose (attention/readability/memorability/conversion), driving design parameters
- 🖼 **3 image sources**: Pexels / Unsplash / Wallhaven, user images always prioritized
- ✅ **Density gate**: 3-dimension 15-point scoring, ≥9 threshold, 8 categories 53 anti-patterns + AI decontamination
- 📱 **Lark Drive sync**: Auto-upload after screenshot, mobile download and publish instantly
- 🔧 **Tweak mode**: Only regenerate specified illustrations, not the entire set

## When to Use / When Not To

✅ **Use when**
- WeChat long-form article illustrations (cover + body + quote + back cover)
- Data visualization cards, logic flow diagrams, knowledge cards
- Article cover and back cover design
- Comparison charts, funnel diagrams, decision trees
- Magazine-grade illustrations without design software

❌ **Don't use when**
- Full article typesetting (use md2wechat-skill or Kami)
- Video/motion graphics
- Pure image editing with no content extraction or layout
- Fan/celebrity content (visual language mismatch)
- Hard-sell advertising (violates content-first philosophy)
- Articles exceeding 15 illustrations (consider splitting the article)

## ⚠️ User Warnings

This skill automatically performs the following operations when running:
1. **Auto-uploads to Feishu Cloud Drive**: Generated illustrations are automatically uploaded to a specified Feishu cloud folder
2. **Auto-saves to Desktop**: PNG illustrations are automatically saved to `C:\Users\<user>\Desktop\<project-name>公众号配图\` directory
3. **Auto-calls external APIs**: Calls Pexels/Pixabay APIs to search for illustration photos (requires API Key)
4. **Auto-opens File Explorer**: May invoke `explorer.exe` to open the output directory after generation

To disable certain side effects, you can remove the `lark-cli` upload step or `explorer.exe` invocation from the generation script.

## 30-Second Start

```bash
# ClawHub install (recommended)
clawhub install wx-peitu

# Or npx install
npx skills add https://github.com/EdwardWason/wx-peitu --skill wx-peitu

# Or manual install
git clone https://github.com/EdwardWason/wx-peitu.git ~/.claude/skills/wx-peitu
```

After installation, just tell your Agent:

```
Generate a set of WeChat illustrations for this article
```

```
Surprise me, just do it
```

```
Swiss style illustrations for this tech article, IKB Blue
```

## 10 Category Auto-Detection

| Category | Detection Signals | Default Style | Default Palette |
|----------|------------------|---------------|-----------------|
| Deep observation / Business | "IPO"/"valuation"/"earnings" | Swiss | IKB Blue |
| Tech / Product | "AI"/"launch"/"feature" | Swiss | IKB Blue / Safety Orange |
| Humanities / Culture | "history"/"literature"/"art" | Editorial | Kraft Paper / Forest Ink |
| Career / How-to | "method"/"steps"/"checklist" | Swiss | Lemon Green |
| Travel / Lifestyle | "travel"/"city"/"food" | Editorial | Warm earth |
| Books / Notes | "review"/"reading"/"excerpt" | Editorial | Ink Classic |
| People / Interviews | "exclusive"/"dialogue"/"profile" | Editorial | Dune / Forest Ink |
| Data / Research | "research"/"report"/"statistics" | Swiss | IKB Blue |
| Opinion / Commentary | "I think"/"actually"/"truth" | Editorial | Ink Classic |
| Tutorial / Guide | "tutorial"/"guide"/"how to" | Swiss | Lemon Green |

## Common Use Cases

| Scenario | Recommended Mode | Trigger |
|----------|-----------------|---------|
| Long article → WeChat illustrations | Multi-Illustration | "Generate illustrations for this article" |
| Master mode full automation | Master Mode | "Surprise me, just do it" |
| Tech product review | Swiss + IKB Blue | "Swiss style, IKB Blue" |
| Human interest / Profiles | Editorial + Ink Classic | "Editorial style, Ink Classic" |
| Tweak a specific card | Tweak Mode | "Card 3 is too dark, adjust it" |

## Usage

### Three Modes

```
User input
    │
    ├── Says "surprise me"/"you decide"/"just do it"?
    │   → Master Mode (fully automated, zero confirmations)
    │
    ├── Contains "illustration"/"article illustrations"/"WeChat"?
    │   → Multi-Illustration Mode (6-step flow, 2 confirmation points)
    │
    └── "Card N..."?
        → Tweak Mode (only regenerate specified card)
```

### Workflow

```
MD article → Parse → Plan (confirm 1) → Style (confirm 2) → Generate HTML → Usage guide → Screenshot + Lark sync
```

1. **Step A Parse** — Extract 20 visualizable units, tag with Purpose
2. **Step B Plan** — Show illustration plan (emoji + one-liner), user confirms
3. **Step C Style** — 3 questions + category auto-detect + visual rhythm planning
4. **Step D Generate HTML** — Independent HTML per illustration, layout diversity check
5. **Step E Usage guide** — Article section ↔ illustration mapping + quick edit commands
6. **Step F Screenshot & Deliver** — Puppeteer → PNG → desktop folder → Lark Drive sync

## Example Requests

```
User: "Generate WeChat illustrations for this Tencent AI analysis article"

Agent: Parsed 8 visualizable units. Recommended plan:
- Cover: Swiss IKB Blue — tech-forward cover
- Core data: Data billboard — 3 key metrics
- Logic chain: Process pipeline — AI strategy in 3 steps
- Quote card: Manifesto — core judgment
- Back cover: Swiss IKB Blue — summary closure
Confirm to generate?
```

```
User: "Surprise me, generate full illustrations for this product postmortem"

Agent: [Auto-parse → Auto-match → Batch generate → Screenshot → Lark sync]
Generated 6 illustrations: cover + 3 infographics + quote card + back cover
Saved to desktop, synced to Lark Drive
```

## Core Mechanism

### Why HTML → Puppeteer → PNG

- **Agent-friendly**: HTML + CSS is text; Agents can write, read, modify, and verify directly
- **Layout precision**: CSS Grid + strict font sizes / whitespace / grid, far beyond Markdown layout capabilities
- **Open image sources**: Unsplash / Pexels / Wallhaven or any web resource
- **Simple delivery**: PNG ready to send, no deployment or export tools needed
- **Mobile accessible**: After Lark Drive sync, open Lark App on phone → download → publish

### Dual Style System

| Dimension | Editorial Magazine | Swiss International |
|-----------|-------------------|---------------------|
| **Font** | Serif, locked at 500 | Sans-serif |
| **Color** | Warm tones, paper base | Gray-white + 4 accent palettes |
| **Layout** | Atmospheric, magazine composition | Grid system, minimal precision |
| **Gray scale** | 7-step warm gray (no cool blue-grays) | 5-step calibrated premium gray |

### Three Aesthetic Constraints

- **Restraint**: Brand color ≤ 5% area, single accent principle
- **Breathing**: Whisper shadows, 0.5pt borders, 8pt border-radius
- **Warmth**: Warm gray system replaces all cool blue-grays, no pure white backgrounds

### Density Gate

3-dimension 15-point scoring, ≥9/15 threshold per card:

| Dimension | Max | Core Question |
|-----------|-----|---------------|
| Information density | 5 | How many actionable information points does this card convey? |
| Visual hierarchy | 5 | Can the reader find the visual entry point within 3 seconds? |
| Information completeness | 5 | Can this be understood when viewed independently? |

## Directory Structure

```
wx-peitu/
├── SKILL.md                    # Agent workflow (6 steps + 14 rules)
├── README.md                   # Chinese docs
├── README.en.md                # English docs
├── CHANGELOG.md                # Version history (v4.0.0 → v7.0.0)
├── LICENSE                     # MIT-0
├── .claude-plugin/
│   └── plugin.json             # Claude Code metadata
├── .github/                    # Community templates
│   └── ISSUE_TEMPLATE/         # Issue templates
└── references/                 # Reference docs
    ├── workflow.md             # 6-step workflow + tweak mode + screenshot + Lark sync
    ├── design-system.md        # Dual style + CSS vars + 3-tier typography + title mapping
    ├── quality-gates.md        # Density scoring + 53 anti-patterns + AI decontamination
    └── assets.md               # 24 Recipes + HTML skeletons + image sources + chart system
```

## Theme Presets

### Editorial (5 sets)

| Theme | Ink / Paper | Use Case |
|-------|-----------|----------|
| 🖋 Ink Classic | `#141413` / `#f5f4ed` | Default, business topics |
| 🌿 Forest Ink | `#1a2e1f` / `#f5f1e8` | Nature, sustainability, non-fiction |
| 🍂 Kraft Paper | `#2a1e13` / `#eedfc7` | Nostalgia, humanities, literature |
| 🌙 Dune | `#1f1a14` / `#f0e6d2` | Art, design, creative, fashion |
| 🏺 Morandi | `#3D3529` / `#F5F0E8` | Elegant, restrained, lifestyle |

### Swiss (4 sets)

| Accent | Hex | Use Case |
|--------|-----|----------|
| 🔵 IKB Blue | `#002FA7` | Default, business, AI products |
| 🟡 Lemon Yellow | `#FFD500` | Youth, sports, retail, consumer |
| 🟢 Lemon Green | `#C5E803` | Eco, health, Gen Z |
| 🟠 Safety Orange | `#FF6B35` | Warning, news, industrial, energy |

## Typography Scale

### Body Illustrations (640px canvas)

| Role | Size | Weight | Notes |
|------|------|--------|-------|
| Display / Hero | 36-44px | 300-400 | Confident, not oppressive |
| Section Title | 24-32px | 400-500 | Hierarchy anchor |
| Body | 14-16px | 400-500 | Comfortable mobile reading |
| Captions / Meta | 10-12px | 500-600 | Small text, heavier weight |
| Data Numbers | 28-36px | 300-400 | Data cards, larger than body, smaller than title |

### Cover / Back Cover (900×383)

| Role | Size | Weight | Notes |
|------|------|--------|-------|
| Cover Title | 44-52px | 300-400 | Readable in thumbnail within 1 second |
| Cover Subtitle | 15-18px | 400 | Supporting info |
| Cover Meta | 11-13px | 500 | Source / Author / Date |

## Limitations

- **Requires an Agent platform**: No GUI — runs in TRAE / Claude Code / Codex or similar Agent environments
- **Puppeteer depends on system Chrome**: Screenshot functionality requires Chrome or Chromium installed locally
- **Lark Drive requires lark-cli**: Cloud sync requires pre-installed and authenticated lark-cli
- **Cover/back cover must have photo backgrounds**: Solid-color covers can't stop readers from scrolling — this is a design decision, not a limitation
- **No custom colors allowed**: Only preset palettes — free color selection breaks overall style consistency
- **Windows path hardcoding**: Desktop save path and `explorer.exe` are Windows-only; macOS/Linux users need manual adjustment

## Core Design Principles

1. **Restraint over shouting** — Brand color ≤ 5% area, single accent principle; restraint stands out in the feed
2. **Structure over decoration** — Font size + type contrast + grid whitespace build information hierarchy, not shadows and cards
3. **Layout over freedom** — 24 layout recipes, choose then refine; don't invent non-existent pages
4. **The larger, the lighter** — 44px+ titles use weight ≤ 400, small text uses heavier weights; this is the core of "premium feel"
5. **Warmth over coldness** — All grays must be warm (R ≈ G > B), no cool blue-grays, no pure white backgrounds
6. **Content drives quantity** — Illustration count determined by content analysis, not fixed templates
7. **User images first** — User-provided images always prioritized over stock libraries, no repeated asking
8. **Density gate is non-negotiable** — Each illustration independently passes density scoring (≥9/15); if it doesn't pass, it doesn't generate

## Visual References

- *The Economist* / *Monocle* / *Kinfolk* — layout and letter-spacing
- Massimo Vignelli / Helvetica Forever / Swiss International grid system
- Xiaohongshu / WeChat feed — "restraint wins attention" content samples
- Guizang's illustration card practice and "make magazines, not web pages" methodology

## FAQ

**Can I batch generate?**
Yes. A typical article generates 5-10 illustrations. screenshot.js captures all to a desktop folder in one click.

**Why must covers/back covers have photo backgrounds?**
Solid-color covers can't stop readers from scrolling. The hero page's job is to "stop the scroll" — photo background + text overlay is the most effective approach.

**Why no custom colors?**
This Skill's core value is consistent output. Free color selection breaks overall style — only preset palettes are allowed.

**How to sync to phone?**
Auto-upload to Lark Drive after screenshot. Open Lark App on phone → Drive → find the folder → download → publish.

**How to modify a specific illustration?**
Just say "Card N is too dark" or "Change Card N's layout" to enter tweak mode — only the target card is regenerated.

**Does it support English content?**
Yes. The font system covers both Chinese and English; layout recipes are language-agnostic.

---

## License

MIT-0 © 2026