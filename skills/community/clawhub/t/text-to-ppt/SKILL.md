---
name: text-to-ppt
description: Convert any text input (research reports, summaries, proposals, plans, etc.) into a beautiful HTML-based presentation. Use when the user asks to create a PPT, slides, presentation, deck, or convert text/documents into slides. Also triggers on phrases like "做成PPT", "生成幻灯片", "做个演示文稿", "转成slides", "create presentation", "make slides", "text to presentation". Supports data visualization with Chart.js, Font Awesome icons, and modern design themes.
---

# Text-to-PPT — 文本转 HTML 演示文稿

Convert any text input into a visually stunning, single-file HTML presentation.

## CRITICAL: Two-Phase Generation

**ALWAYS use the two-phase approach. NEVER generate the full HTML in one shot.**

### Phase 1: Plan (fast, single call)

Read the input text, then produce a **slide-by-slide outline** in JSON format:

```json
{
  "title": "Presentation Title",
  "language": "zh-CN",
  "density": "detailed",
  "theme": "dark",
  "slides": [
    {
      "number": 1,
      "type": "title",
      "heading": "Main Title",
      "content": "Subtitle or tagline",
      "layout": "centered",
      "notes": "Visual: large title with accent underline"
    },
    {
      "number": 2,
      "type": "content",
      "heading": "Section Title",
      "points": ["Point 1", "Point 2", "Point 3"],
      "layout": "bullets",
      "hasData": false,
      "notes": "Use numbered badges for each point"
    },
    {
      "number": 3,
      "type": "chart",
      "heading": "Key Metrics",
      "chartType": "bar",
      "chartData": {
        "labels": ["A", "B", "C"],
        "datasets": [{"label": "Sales", "data": [100, 200, 150]}]
      },
      "points": ["Insight 1", "Insight 2"],
      "layout": "split",
      "hasData": true,
      "notes": "Left: chart, Right: insights as stat cards"
    }
  ]
}
```

**Rules for Phase 1:**
- Output ONLY the JSON plan. No HTML. No explanation.
- Identify data points → mark `hasData: true` and provide `chartType` + `chartData`
- Choose layout: `centered`, `bullets`, `split`, `grid`, `timeline`, `cards`, `fullchart`, `quote`
- Target 8-15 slides. Never exceed 20.
- This should take <10 seconds.

### Phase 2: Generate (parallel, page-by-page)

**Read `references/design-system.md`** — this is where the full design spec lives.

Then generate HTML for each slide **independently**. Each slide is a self-contained `<div class="slide">` block.

**For each slide, the agent should:**
1. Take ONE slide from the plan (by number)
2. Read only the design system reference if not already loaded
3. Generate ONLY that one slide's HTML `<div class="slide">...</div>`
4. No `<html>`, no `<head>`, no `<body>` — just the slide div

**BATCHING: Generate slides in parallel using sub-agents.** Spawn up to 5 sub-agents simultaneously, each generating 1-2 slides.

### Phase 3: Assemble

After all slides are generated:
1. Read the shell template from `references/shell-template.html`
2. Insert all slide divs into the shell
3. Ensure chart canvas IDs are unique across all slides
4. Save to Obsidian vault: `~/Documents/longhai/Longhai/`
5. Tell user the file path

## Execution Strategy

### When running as the main agent:
1. Phase 1 yourself (fast, just JSON)
2. Write the plan to a temp file
3. Spawn sub-agents for Phase 2 (parallel slide generation)
4. Collect results and assemble in Phase 3

### Sub-agent task format (for Phase 2):
```
Generate HTML for slide {N} of a presentation.

SLIDE PLAN:
{JSON for this specific slide}

DESIGN SYSTEM: Read references/design-system.md for theme colors, components, and rules.

OUTPUT: Return ONLY a single <div class="slide" style="background-color: #0f172a;">...</div> block.
No <html>, <head>, or <body> tags. Use inline styles. Include <script> for Chart.js if this slide has charts.
Use unique canvas ID: chart-slide{N}-{random}.
```

## Input Sources

- Directly pasted text
- A file path — read it first with `read`
- A URL — fetch it first with `web_fetch`
- An Obsidian note path — read it first

## Output

- Single self-contained HTML file
- File naming: `{topic-slug}.presentation.html`
- Default save location: `~/Documents/longhai/Longhai/`
- Tell the user the file path

## Theme Options

| Theme | Background | Text | Cards | Accent |
|-------|-----------|------|-------|--------|
| dark (default) | slate-900 | slate-50 | slate-800 | blue-500/amber-500 |
| light | slate-50 | slate-900 | white | blue-600/amber-600 |
| tech | gray-950 | emerald-50 | gray-900 | cyan-500/violet-500 |
| warm | stone-900 | amber-50 | stone-800 | orange-500/rose-500 |

User can specify a theme. Default: dark.
