---
name: ui-design-optimizer
description: Generate practical UI design systems and starter pages using local style/color/typography datasets. Use for landing page or dashboard UI planning and implementation.
---

# UI Design Optimizer

## Goal

Produce a concrete, buildable UI output instead of generic design advice.

## Inputs

- Product/domain description (for example: SaaS dashboard, hiring tool, beauty SPA)
- Page type (landing page or dashboard)
- Preferred stack (HTML/CSS by default)

## Data Sources

- `data/styles.csv`
- `data/colors.csv`
- `data/typography.csv`
- `data/patterns.csv`
- `data/rules.json`

## Required Workflow

1. Read relevant rows from style/color/typography data.
2. Choose one style, one palette, and one typography pair with rationale.
3. Output a compact design spec:
   - layout pattern
   - color tokens
   - typography tokens
   - interaction rules
4. If user asks for implementation, generate runnable files (at minimum `index.html` + `styles.css`).
5. Return evidence with file paths and the selected dataset rows/slugs.

## Quality Rules

- Prioritize readability and accessibility (target WCAG AA contrast).
- Use consistent spacing, type scale, and component states.
- Avoid placeholder-only output when implementation is requested.
- Keep generated text UTF-8 clean (no mojibake).

## Verification

When files are generated, verify:

- files exist on disk;
- HTML references stylesheet correctly;
- selected style/palette/typography are reflected in CSS variables.

## Script Helper

Use `scripts/search.ps1` when quick lookup is useful:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/search.ps1 -Query "saas dashboard" -DesignSystem -ProjectName "Demo"
```
