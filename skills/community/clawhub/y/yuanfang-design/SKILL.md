---
name: yuanfang-design
description: |
  Shared design system for yuanfang-skills. Provides token CSS variables, 12+ themes, and reusable layout-type HTML blocks. Used by yuanfang-html-image (and future yuanfang-html-ppt) to render visually consistent output.
  When user asks to "add a new theme", "add a new layout", or "view the design system", use this skill.
---

# yuanfang-design

Shared design library providing:

- **base.css** — 30+ token CSS variables (colors, fonts, sizes, space, radius, shadow, decor, feature flags)
- **themes/** — 12 theme overrides, each as a single CSS file using `[data-theme="..."]` selectors
- **layout-types/** — Reusable HTML blocks (cover.html, future bullets/kpi-grid/etc.)
- **showcase/** — Visual QA tool: 12 themes × 6 platforms = 72 iframes in a grid
- **references/authoring-guide.md** — Rules for adding new themes/layout-types

## When to use

Use this skill when:
- The user wants to add a new visual style → create a new theme file
- The user wants to add a new layout type (e.g., bullets, kpi-grid) → create new HTML block
- The user wants to view all themes/layouts at once → open the showcase
- The user wants to understand the design system → read authoring-guide.md

## Structure

```
yuanfang-design/
├── base.css              # All token defaults (no literals in .cover rules)
├── themes/<name>.css     # Each theme = token override set
├── layout-types/<name>.html
├── animations.css        # Shared animation library (placeholder for now)
├── references/authoring-guide.md
└── showcase/cover-showcase.html
```

## How themes work

A theme is a single CSS file that overrides base.css tokens:

```css
[data-theme="dark-gold"] {
  --bg: #1A1A2E;
  --text: #F5E6D3;
  --accent: #E2B714;
  /* ... */
}
```

The `cover.html` layout-type references tokens only. Swapping the theme = reskinning the entire layout.

## How to add a new theme

1. Copy `themes/_template.css` to `themes/<name>.css`
2. Override tokens for: colors, fonts, sizes, decor, feature flags
3. Test: `npm run render -- --theme <name> --layout cover --platforms xiaohongshu-v`
4. Update showcase/cover-showcase.html to include the new theme

## How to add a new layout-type

1. Create `layout-types/<name>.html` with `{{}}` placeholders for content
2. Add corresponding `.layout-<name>` rules to base.css (or new file)
3. Test: `npm run render -- --theme minimal-white --layout <name> --platforms all`
4. Add to showcase
