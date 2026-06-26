---
name: vizboard
description: Generate beautiful, self-contained HTML dashboards and visual pages — architecture diagrams, flowcharts, KPI dashboards, data tables, diff reviews, plan reviews, and project recaps. Use when the user asks for a diagram, architecture overview, diff review, plan review, project recap, comparison table, or any visual explanation of technical concepts. Also use proactively when you are about to render a complex ASCII table (4+ rows or 3+ columns) — present it as a styled HTML page instead.
license: MIT
metadata:
  author: nicobailon
  version: "1.0.0"
---

# Vizboard

## Goal
Generate self-contained HTML pages for visual explanations of architectures, plans, diffs, data tables, and KPI dashboards.

## Hard Rules
- Never use ASCII-art when this skill is active.
- Tables with `4+ rows` or `3+ columns` must always be rendered as HTML (proactively).
- HTML must be fully self-contained (inline CSS/JS, no external assets).
- Always deliver the generated file to the user after generation.

## Workflow
1. Determine visualization type: architecture, flowchart, sequence, table, dashboard.
2. Pick a template:
   - `templates/architecture.html`
   - `templates/mermaid-flowchart.html`
   - `templates/data-table.html`
3. For large/complex diagrams use Mermaid + themeVariables.
4. For tabular data use semantic `<table>`.
5. Apply styling via CSS variables (intentional palette, not defaults).
6. Verify responsive layout and no overflow.

## Rendering Guidance
- Architecture (text-heavy): CSS grid + cards.
- Topology/flow/state/sequence: Mermaid.
- Data tables/audits/comparisons: HTML table with sticky header.
- KPI/dashboard: grid + optional chart libs from `references/libraries.md`.

## Output & Delivery
Save to:
- `~/.agent/diagrams/<descriptive-name>.html`

**After generation, ALWAYS deliver the file to the user:**
1. Copy to workspace: `cp ~/.agent/diagrams/<file>.html ./<file>.html`
2. Send: `message(action="send", filePath="./<file>.html", message="<brief description of the dashboard>")`
3. Cleanup: `rm ./<file>.html`
4. Reply `NO_REPLY` after sending

**Do NOT skip step 2** — the user expects to receive the file in chat, not just a file path.
**Do NOT skip step 3** — files in workspace accumulate.

## Quality Gate
- Clear visual hierarchy.
- No clipped text or containers.
- Light/dark mode support.
- Mermaid blocks are readable; large diagrams have zoom/pan.
- Content reflects the user's actual request — no filler or boilerplate.

## References
- `references/css-patterns.md` — layout, overflow, zoom controls.
- `references/libraries.md` — Mermaid/Chart.js/anime.js usage.
- `references/responsive-nav.md` — navigation for long pages.
- `prompts/*.md` — ready-made scenarios (diff-review, plan-review, fact-check, project-recap).
