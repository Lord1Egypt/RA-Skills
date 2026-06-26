# Create Template Guide

Use this workflow when the user wants a new scaffold from a screenshot,
description, or rough idea.

## Goal

Create a reusable blueprint file that describes structure and generation rules,
not a prefilled final page.

## Steps

1. Identify output format (`markdown`, `html`, or `jsx`)
2. Pick destination path:
   - `templates/markdowns/{name}.md`
   - `templates/htmls/{name}.md`
   - `templates/jsx/{name}.md`
3. Extract and document:
   - core sections and order
   - required vs optional blocks
   - data and component interactions
   - style constraints
   - validation checklist
4. Add a scaffold skeleton with placeholders
5. Avoid fake brand stories and fabricated business claims
6. Update `templates/INDEX.md`

## Naming

- Use kebab-case file names
- Prefer intent-based names (`product-launch-page`, `analytics-explorer`)

## Definition of Done

- Template is actionable without reading source artifacts
- Scaffold is complete enough to generate a publishable first draft
- Sections can be omitted safely when user data is missing
