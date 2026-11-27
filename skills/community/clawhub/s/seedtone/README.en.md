# seedtone

[![skills.sh](https://skills.sh/b/shxuk/seedtone)](https://skills.sh/shxuk/seedtone)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Node](https://img.shields.io/badge/node-%3E%3D18-green.svg)](./package.json)

[简体中文](./README.md) | English

When building websites, apps, or doing Vibe Coding, colors easily drift into a messy, clashing palette.

`seedtone` glues together **GitHub Primer** semantic roles, **Adobe Leonardo** contrast math, **OKLCH** tinted neutrals, **W3C DTCG / Style Dictionary**, and **APCA** contrast checks. **Give it 1 primary hex color**, and it outputs a stable light/dark UI color matrix that needs almost zero manual tweaking:

1. **A human-readable HTML report** (`dist/color-report.html`): preview web & mobile mockups, toggle light/dark mode, and click to copy variables.
2. **Constraint tooling for AI & code**: CSS variables, Tailwind v4/v3 configs, and a linter to stop AI or teammates from hardcoding random hex values.

## Quick Start

```bash
# Install as an Agent Skill (Claude Code / Cursor / Trae / Antigravity)
npx skills add shxuk/seedtone

# Or run via CLI
git clone https://github.com/shxuk/seedtone.git && cd seedtone
pnpm install
pnpm generate -- --seed "#2563eb"
```

Outputs in `dist/`:
- **Preview**: open `dist/color-report.html`
- **Code**: import `dist/tokens.css`, `dist/tailwind.theme.css` (Tailwind v4 `@theme`), or `dist/tailwind.preset.cjs` (Tailwind v3)

Options: `--tint subtle|pure|warm|cool` (default `subtle`), `--no-semantic`, `--out ./my-theme`.

## Constraint Checks for AI / CI

```bash
pnpm tokens:build                # Rebuild CSS from tokens/
pnpm tokens:check --scan ./src   # Verify contrast & catch hardcoded hex values
```

## How It Works

1. **Lock paper & neutral grays (OKLCH)**: takes the seed hue at ultra-low chroma (`C ≤ 0.012`) and solves lightness for light/dark surfaces.
2. **Solve accent scales (Adobe Leonardo)**: computes text, button, and hover steps against the locked surfaces; dark mode solves from an independent bright seed instead of naive inversion.
3. **Shift clashing status hues**: generates `danger`, `success`, `warning`, and `info`; shifts any status hue away if it lands within `35°` of your seed.
4. **Verify roles (Primer + WCAG / APCA)**: maps to `fgColor` / `bgColor` / `borderColor` / `focus` and checks every pair with WCAG 2.1 and APCA (`apca-w3`).

## Scope

Built for UI color systems and code guardrails—not for brand logo illustration or CMYK print workflows.

## License

[MIT](./LICENSE)
