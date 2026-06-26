# UI Design Optimizer

Implementation-first UI/UX skill for OpenClaw. It helps select style, color, and typography from local datasets, then produce a practical design spec and starter files.

## What This Version Improves (v1.1.0)

- Removes corrupted trigger patterns and metadata mojibake.
- Normalizes trigger patterns for stable matching.
- Keeps guidance focused on output quality and accessibility.
- Works with runtime path `skills/ui-design-optimizer`.

## Core Capabilities

- Design-system generation
- Style recommendation
- Color palette selection
- Typography pairing
- Industry-oriented guidance
- Accessibility checks (WCAG-oriented)

## Data Files

- `data/styles.csv`
- `data/colors.csv`
- `data/typography.csv`
- `data/patterns.csv`
- `data/rules.json`

## Typical Prompts

- `Design a landing page for a fintech product.`
- `Generate a dashboard design system for a hiring tool.`
- `Recommend color palette and typography for a wellness app.`

## Script Usage

```powershell
powershell -ExecutionPolicy Bypass -File scripts/search.ps1 -Query "saas dashboard" -DesignSystem -ProjectName "Demo"
```

## Validation

1. Check skill availability:

```powershell
openclaw skills check | findstr /I "ui-design-optimizer"
```

2. If available, generate a demo and verify file output in your target directory.

## Credits

Adapted from UI-UX Pro Max:
- https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
