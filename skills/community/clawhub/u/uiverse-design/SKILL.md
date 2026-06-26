---
name: uiverse-design
description: "UI component design learning library with 165 curated CSS/Tailwind components from Uiverse Galaxy (open-source, MIT). Use when: (1) user explicitly asks to browse or search UI component designs from Uiverse, (2) user needs CSS/Tailwind code examples for buttons, cards, loaders, inputs, forms, toggles, tooltips, or notifications, (3) user explicitly mentions 'uiverse', 'uiverse galaxy', or 'UI component library'. Do NOT activate for general UI/UX questions, design advice, or when user just says 'component' or 'style' without requesting specific code."
---

# Uiverse Design — UI Component Design Library

165 curated open-source UI components from Uiverse Galaxy (MIT license). Each component is a self-contained HTML file with inline CSS or Tailwind classes, ready to copy into any project.

---

## About This Skill

**This skill ships with a curated subset (165 components, ~15 per category).**

The full Uiverse Galaxy repository contains 3800+ components. If the user wants access to the complete library, they can run the included setup script to download it from GitHub:

```bash
bash <skill-dir>/scripts/setup.sh
```

> **Note:** The setup script downloads external content from GitHub at runtime. The downloaded content is not reviewed as part of this skill and may change over time. Users should review the script source before running it. Use `--proxy` if a network proxy is needed.

After download completes, the full library replaces the curated subset automatically.

---

## Component Categories

```
assets/galaxy/
├── Buttons/          — CTA, icon, animated, hover effects
├── Cards/            — Info cards, 3D effects, data display
├── loaders/          — Spinners, progress bars, skeletons
├── Inputs/           — Text, search, floating labels
├── Toggle-switches/  — On/off, multi-state, themed
├── Forms/            — Login, signup, contact, search
├── Checkboxes/       — Custom styled, animated
├── Patterns/         — Backgrounds, gradients, textures
├── Radio-buttons/    — Custom styled, animated
├── Tooltips/         — Hover, click, positioned
└── Notifications/    — Toast, alert, badge
```

## Search Components

```bash
bash <skill-dir>/scripts/search.sh <category> [keyword] [--tailwind|--css]
bash <skill-dir>/scripts/search.sh --all [keyword]     # Search all categories
bash <skill-dir>/scripts/search.sh --sample <category>  # Random samples for inspiration
bash <skill-dir>/scripts/search.sh --stats              # Show statistics
bash <skill-dir>/scripts/search.sh --tags               # Popular tags
```

## Design Learning Workflow

### Step 1: Identify Page Type → Choose Components

| Page Type | Focus On | Key Components |
|-----------|----------|----------------|
| **Dashboard** | Card grids, data display, loading states | Cards, Loaders, Notifications |
| **Admin Panel** | Tables, forms, action buttons | Forms, Buttons, Inputs, Checkboxes |
| **Data Panel** | KPI cards, chart placeholders, filters | Cards, Inputs, Radio-buttons |
| **Settings Page** | Toggles, forms, save buttons | Toggle-switches, Forms, Buttons |
| **Landing Page** | Eye-catching buttons, gradients, animations | Buttons, Patterns, Cards |

### Step 2: Extract Design Patterns from Components

Each `.html` file is a design study. Focus on extracting:

**Color System** — Extract `--primary`, `--bg`, `--accent` variables
**Spacing Rhythm** — Observe `padding`, `margin`, `gap` values
**Border Radius** — `4px` (sharp) → `12px` (rounded) → `50px` (pill)
**Shadow Depth** — `box-shadow` offset, blur, and color for layering
**Animation** — `transition` duration, `transform` changes, `@keyframes`
**Typography** — `font-size`, `font-weight`, `letter-spacing` combinations

### Step 3: Combine into Complete Pages

Use `references/patterns.md` for ready-to-use design patterns: card grids, dark themes, KPI displays, status indicators, table styles, and color scheme references.

## Component File Format

- **CSS components** (84%): Contain `<style>` tag, self-contained
- **Tailwind components** (11%): Use Tailwind utility classes
- **Mixed components** (5%): Both `<style>` and Tailwind classes

Header comment identifies source and tags:
```html
<!-- From Uiverse.io by author - Tags: tag1, tag2, tag3 -->
```

## Common Tags

| Tag | Meaning | Use Case |
|-----|---------|----------|
| `animated` / `animation` | Has animations | Attention, feedback |
| `hover` / `hover effect` | Hover interaction | Buttons, links, cards |
| `gradient` | Gradient colors | Backgrounds, buttons, accents |
| `minimalist` | Minimal style | Admin panels, professional products |
| `material design` | Material style | Android/Web universal |
| `dark` / `light&dark` | Dark theme | Dashboards, night mode |
| `modern` / `smooth` | Modern feel | New projects, product pages |
| `loading` / `loader` | Loading state | Data waiting, skeletons |

## License

MIT license from [Uiverse.io](https://uiverse.io/).
