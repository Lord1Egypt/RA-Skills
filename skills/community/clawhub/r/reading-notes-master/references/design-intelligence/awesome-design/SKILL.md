---
name: awesome-design
description: |
  Use when user asks about design skills, UI skills, design tools,
  "what design skills are available", "help me design",
  "recommend a design skill", "UI/UX skill", "design workflow",
  "設計技能", "UI 技能", "設計工具推薦",
  or when the user needs guidance on which design skill to use for a specific task.
version: 0.1.1
allowed-tools: Bash, Read, WebSearch
---

# Awesome Design Skills: A Curated Guide

A verified, curated directory of design skills for AI coding agents. Helps you pick the right skill for logos, UI components, animations, presentations, icons, and full design systems.

## Skill Directory

### Visual Design & UI Systems

| Skill | What It Does | Install | Source |
|-------|-------------|---------|--------|
| **UI/UX Pro Max** | 67 UI styles, 161 industry rules, 161 color palettes, 57 font pairings, 25 chart types. Most comprehensive UI system. | `git clone https://github.com/nextlevelbuilder/ui-ux-pro-max-skill ~/.claude/skills/ui-ux-pro-max` | [GitHub](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) |
| **Taste** | Senior UI/UX engineering with metric-based rules. 7 variants: core taste + soft (premium), minimalist (editorial), brutalist, stitch (Google Stitch), output (anti-truncation), redesign. | `git clone https://github.com/Leonxlnx/taste-skill ~/.claude/skills/taste` | [GitHub](https://github.com/Leonxlnx/taste-skill) |
| **Impeccable** | 18 design sub-skills (/polish, /audit, /typeset, /overdrive, /colorize, /layout, etc.). Anti-pattern detection. CLI scanner with 24 design quality checks. | `git clone https://github.com/pbakaus/impeccable ~/.claude/skills/impeccable` | [GitHub](https://github.com/pbakaus/impeccable) |
| **Design & Refine** | Generates multiple distinct UI variations with side-by-side comparison at `/__design_lab`. Figma-style commenting. Next.js, Vite, Remix, Astro. | `git clone https://github.com/0xdesign/design-plugin ~/.claude/skills/design-plugin` | [GitHub](https://github.com/0xdesign/design-plugin) |
| **Interface Design** | Design engineering with craft, memory, and enforcement. 6 design directions (precision, warmth, sophistication, etc.) for consistent UI across projects. | `git clone https://github.com/Dammyjay93/interface-design ~/.claude/skills/interface-design` | [GitHub](https://github.com/Dammyjay93/interface-design) |

### Components & Icons

| Skill | What It Does | Install | Source |
|-------|-------------|---------|--------|
| **Shadcnblocks** | Expert knowledge of 1,338 blocks and 1,189 shadcn/ui components. Intelligent component selection and composition. | `git clone https://github.com/masonjames/Shadcnblocks-Skill ~/.claude/skills/shadcnblocks` | [GitHub](https://github.com/masonjames/Shadcnblocks-Skill) |
| **Better Icons** | Search 200,000+ icons from 150+ collections (Lucide, Material, Heroicons, Tabler). Auto-learns your preferred icon sets. React/Vue/Svelte/SVG export. | `git clone https://github.com/better-auth/better-icons ~/.claude/skills/better-icons` | [GitHub](https://github.com/better-auth/better-icons) |

### SVG & Logo Design

| Skill | What It Does | Install | Source |
|-------|-------------|---------|--------|
| **SVG Logo Designer** | Professional vector logos with 3-5 concepts per project. Horizontal, vertical, square, icon-only layouts. Clean semantic SVG. | `git clone https://github.com/rknall/claude-skills ~/.claude/skills/rknall-claude-skills` | [GitHub](https://github.com/rknall/claude-skills) |
| **Algorithmic Art** | Parametric geometry, custom color theory, and interactive visualizations. Generative art with SVG. | Part of [Anthropic Skills](https://github.com/anthropics/skills) | [GitHub](https://github.com/anthropics/skills) |

### Image Generation

| Skill | What It Does | Install | Source |
|-------|-------------|---------|--------|
| **Z-Image** | Generate images from text using Alibaba's free Z-Image-Turbo model (ModelScope API). 2,000 free calls/day. Custom dimensions 512-2048px. English + Chinese prompts. | `git clone https://github.com/FuturizeRush/zimage-skill ~/.claude/skills/zimage` | [GitHub](https://github.com/FuturizeRush/zimage-skill) |

### Animation & Motion

| Skill | What It Does | Install | Source |
|-------|-------------|---------|--------|
| **Animate** | Animation patterns for Next.js/React based on Emil Kowalski's course. 8 working examples. | `git clone https://github.com/delphi-ai/animate-skill ~/.claude/skills/animate` | [GitHub](https://github.com/delphi-ai/animate-skill) |
| **CSS Animation** | Self-contained HTML/CSS animations for feature walkthroughs, demos, onboarding. No JS dependencies (uses Google Fonts). | `git clone https://github.com/neonwatty/css-animation-skill ~/.claude/skills/css-animation` | [GitHub](https://github.com/neonwatty/css-animation-skill) |

### Data Visualization

| Skill | What It Does | Install | Source |
|-------|-------------|---------|--------|
| **Visualise** | Inline interactive visuals: SVG diagrams, HTML widgets, Chart.js charts, explainers. Progressive loading. No dependencies. | `git clone https://github.com/bentossell/visualise ~/.claude/skills/visualise` | [GitHub](https://github.com/bentossell/visualise) |

### Presentations & Documents

| Skill | What It Does | Install | Source |
|-------|-------------|---------|--------|
| **PPTX** | Full PowerPoint toolkit: read, edit, create .pptx files. Thumbnail grids, XML access, PDF conversion. | Part of [Anthropic Skills](https://github.com/anthropics/skills). Deps: `pip install "markitdown[pptx]" Pillow` + `npm install -g pptxgenjs` | [GitHub](https://github.com/anthropics/skills) |

### Theming & Branding

| Skill | What It Does | Install | Source |
|-------|-------------|---------|--------|
| **Theme Factory** | 10 pre-set themes with colors/fonts. Apply to any artifact. | Part of [Anthropic Skills](https://github.com/anthropics/skills) | [GitHub](https://github.com/anthropics/skills) |
| **Brand Guidelines** | Apply Anthropic's brand colors and typography. Template for creating brand guideline skills. | Part of [Anthropic Skills](https://github.com/anthropics/skills) | [GitHub](https://github.com/anthropics/skills) |
| **Canvas Design** | Advanced typography with 80+ fonts, color harmony, and text rendering effects. | Part of [Anthropic Skills](https://github.com/anthropics/skills) | [GitHub](https://github.com/anthropics/skills) |
| **Web Artifacts Builder** | Multi-component HTML artifacts using React, Tailwind, shadcn/ui. For claude.ai web artifacts. | Part of [Anthropic Skills](https://github.com/anthropics/skills) | [GitHub](https://github.com/anthropics/skills) |

## Which Skill Should I Use?

### By Task

| Task | Recommended Skill | Why |
|------|-------------------|-----|
| "Design a landing page" | UI/UX Pro Max + Taste (soft) | Pro Max gives structure, Taste gives premium feel |
| "Make a logo" | SVG Logo Designer | Purpose-built for logo workflows |
| "Add animations" | Animate (React/Next.js) or CSS Animation (vanilla) | Animate for frameworks, CSS Animation for zero-dep |
| "Find icons" | Better Icons | 200K+ icons, auto-learns preferences |
| "Build a component library" | Shadcnblocks + Impeccable | Shadcnblocks for components, Impeccable for QA |
| "Create a presentation" | PPTX | Full PowerPoint read/write/create |
| "Redesign my app" | Taste (redesign variant) | Audits and upgrades without breaking functionality |
| "Make a chart/diagram" | Visualise | Inline interactive charts and diagrams |
| "Design review / audit" | Impeccable | 25 deterministic checks + /audit command |
| "Apply a theme" | Theme Factory | 10 pre-built themes, instant application |
| "Generate data art" | Algorithmic Art | Parametric geometry and generative visuals |
| "Generate an image" | Z-Image | Free, 2K calls/day, no OpenAI key needed |
| "Compare UI options" | Design & Refine | Side-by-side variations with commenting |

### By Framework

| Framework | Best Skills |
|-----------|------------|
| Next.js / React | Taste, Animate, Shadcnblocks, Design & Refine |
| Tailwind CSS | UI/UX Pro Max, Impeccable, Shadcnblocks |
| Vanilla HTML/CSS | CSS Animation, Visualise, SVG Logo Designer |
| Vue / Svelte | Better Icons (multi-framework), UI/UX Pro Max |
| PowerPoint | PPTX |

## Security Notes

All skills listed here have been reviewed for safety:
- No `curl | sh` pipes or obfuscated code
- No credential harvesting (env var collection)
- No base64 decoding of hidden payloads
- No raw IP URL connections

Before installing any skill not listed here, check for these patterns:
```bash
# Quick security scan
grep -rn 'curl.*|.*sh\|base64.*decode\|eval(\|exec(' /path/to/skill/ --include="*.md" --include="*.js" --include="*.ts" --include="*.py" --include="*.sh"
```

## Tips

- Start with **one** skill per category. Don't install everything at once.
- **Taste + UI/UX Pro Max** is the most popular combination for general UI work.
- **Impeccable** is the best for design QA and catching anti-patterns.
- Skills that are "Part of Anthropic Skills" come from the official Anthropic collection and are the safest option.
- Check skill GitHub repos for recent activity — abandoned skills may have outdated patterns.
- When skills conflict (different design opinions), the last-installed skill's rules typically take precedence.
