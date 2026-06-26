---
name: timeplus-design
description: >
  Build user interfaces that match the Timeplus Console look and feel. Use this
  skill when generating, styling, or reviewing UI for a Timeplus product or
  console-aligned app — buttons, inputs, toggles, tables, cards, layouts — and
  when you need the exact Timeplus colors, Inter typography scale, 4px-radius
  flat-surface shapes, spacing scale, and component states. Provides a
  DESIGN.md (google-labs-code/design.md token format) plus ready-to-adapt CSS,
  Tailwind, and React implementations.
license: Apache-2.0
compatibility: >
  Documentation only — no runtime dependencies. The design system targets web UI
  (CSS / Tailwind / React) and uses the Inter font (loadable from Google Fonts).
  Optional: validate DESIGN.md with `npx @google/design.md lint DESIGN.md`
  (requires Node.js).
metadata:
  author: timeplus-io
  version: "1.0.0"
  docs: https://docs.timeplus.com
  tags:
    - design-system
    - ui
    - frontend
    - design-tokens
    - tailwind
    - react
    - branding
---

# Timeplus Design System

Generate UI that looks like the **Timeplus Console**: clean, professional, and
flat, built on a neutral gray scale with a single pink accent (`#D53F8C`) for
primary actions, the Inter typeface, and a consistent 4px corner radius.

The normative source of truth is [`DESIGN.md`](DESIGN.md) — a
[google-labs-code/design.md](https://github.com/google-labs-code/design.md)
token file. Its YAML front matter holds the exact color, typography, spacing,
radius, and component tokens; its prose explains how to apply them. **Use the
token values verbatim.**

## Quick Reference

| Need | Read |
|------|------|
| Design tokens + rationale (colors, type, layout, shapes, components, do's/don'ts) | [`DESIGN.md`](DESIGN.md) |
| Copy-paste CSS, Tailwind config, and React components | [`references/components.md`](references/components.md) |

## When to Read Reference Files

- **`DESIGN.md`** — Read first for any Timeplus UI task. Provides the exact
  palette (gray-100…gray-900, pink-400/500, red-400/500), the Inter type scale,
  the 4px radius rule, the flat/no-shadow elevation model, the 4px-based spacing
  scale, per-component tokens and states, and the do's & don'ts.
- **`references/components.md`** — Read when implementing. Full CSS,
  `tailwind.config.js` color/font extension, CSS custom properties, and React
  components for buttons (primary/secondary/destructive), text inputs, toggle
  switches, cards, tables, links, dividers, and icons, plus accessibility
  (WCAG AA contrast, focus states, touch targets) and asset guidance.

## Core Rules (at a glance)

- **Font:** Inter only — Regular (400) for content, Semi-Bold (600) for headings/controls. Never below 12px.
- **Color:** Neutral grays carry the UI; pink-500 marks the single primary action; red-500 is for destructive/error only.
- **Surfaces:** Page background is warm off-white `#F7F6F6`; content sits on white cards with a 1px `#DAD9DB` border.
- **Shape:** 4px radius everywhere (pill only for toggles). No shadows — separate with borders.
- **Spacing:** 4px-based scale; 24px container padding, 16px between form fields.
- **Buttons:** 32px tall. **Inputs:** 40px tall. Always provide a visible 2px pink focus ring.

## Validating changes

After editing `DESIGN.md`, optionally lint it against the format spec:

```bash
npx @google/design.md lint DESIGN.md
```

You can also export the tokens to Tailwind or W3C DTCG format:

```bash
npx @google/design.md export --format css-tailwind DESIGN.md > theme.css
```
