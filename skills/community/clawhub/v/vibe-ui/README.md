# Vibe UI

<p align="center">
  <a href="README.md"><strong>English</strong></a>
  ·
  <a href="README.zh-CN.md">简体中文</a>
</p>

<p align="center">
  <img alt="Version 1.1.0" src="https://img.shields.io/badge/version-1.1.0-2563eb?style=for-the-badge">
  <img alt="Tests passing" src="https://img.shields.io/badge/tests-passing-22c55e?style=for-the-badge">
  <img alt="Node.js" src="https://img.shields.io/badge/runtime-Node.js-475569?style=for-the-badge">
  <img alt="Local first" src="https://img.shields.io/badge/local--first-DESIGN.md-7c3aed?style=for-the-badge">
</p>

Local-first `DESIGN.md` workflow skill for web UI generation, style selection, Design Read, prompt generation, and design consistency checks.

Vibe UI helps AI coding agents choose a visual style, apply design context, generate page prompts, run a pre-build quality gate, and review generated UI code. Vibe UI-owned workflow features use Vibe UI names such as **Vibe Gate** and **Vibe UI template recipes**. Upstream names are used only for source filters, resource ids, provenance, and attribution.

## Features

- 18 curated built-in styles for high-confidence defaults.
- 150 upstream `DESIGN.md` systems bundled in `resource/open-design-systems.json`.
- 111 upstream `design-templates` indexed from `Liuwei1125/vibe-ui-resources`.
- Vibe UI template recipes distilled from upstream source patterns, including commerce, launch, pricing, waitlist, docs, dashboard, kanban, mobile, onboarding, portfolio, and SaaS recipes.
- Vibe Gate 2.0 execution chain: `read`, `workflow`, `invariants`, `brief-check`, `generate`, `report`, `critique`, and `polish`.
- Design Read with audience, buyer anxiety, register, density/variance/motion dials, proof strategy, and section strategy.
- Static style browser with filters and copy-command snippets.
- Design consistency checks with score, blockers, synthesis, and Bad/Fix/Evidence guidance.
- Publish package modes for `minimal`, `standard`, and `offline-full`.

## Quick Start

```bash
cd skills/vibe-ui
npm test
node scripts/design.mjs list
node scripts/design.mjs recommend "AI SaaS landing page for frontend engineers"
```

Apply a design from any project root:

```bash
node /absolute/path/to/skills/vibe-ui/scripts/design.mjs use linear
node /absolute/path/to/skills/vibe-ui/scripts/design.mjs read "AI SaaS landing page for frontend engineers" --page landing --design linear
node /absolute/path/to/skills/vibe-ui/scripts/design.mjs workflow landing --design linear --target src/app/page.tsx
node /absolute/path/to/skills/vibe-ui/scripts/design.mjs brief-check landing --design linear
node /absolute/path/to/skills/vibe-ui/scripts/design.mjs generate landing
node /absolute/path/to/skills/vibe-ui/scripts/design.mjs report src/app/page.tsx
node /absolute/path/to/skills/vibe-ui/scripts/design.mjs critique src/app/page.tsx
node /absolute/path/to/skills/vibe-ui/scripts/design.mjs polish src/app/page.tsx
```

Use the bundled upstream source library when you need broader references:

```bash
node scripts/design.mjs list --source open-design
node scripts/design.mjs use open-design:linear-app
node scripts/design.mjs template vibe:commerce-home
node scripts/design.mjs generate landing --template vibe:commerce-home
```

After `use`, Vibe UI writes:

- `DESIGN.md`
- `DESIGN.generated.md`
- `.vibe-ui/current-design.json`

After `read`, Vibe UI writes:

- `.vibe-ui/brief-read.json`
- `.vibe-ui/product-context.json`

## Commands

```bash
node scripts/design.mjs list [--source built-in|open-design|all]
node scripts/design.mjs search <keyword> [--source built-in|open-design|all]
node scripts/design.mjs recommend "<user goal>" [--source built-in|open-design|all]
node scripts/design.mjs read "<brief>" [--page page_type] [--design design_id] [--template template_id] [--source built-in|open-design|all]
node scripts/design.mjs use <design_id>
node scripts/design.mjs like <design_id> [page_type] [--strength light|medium|bold]
node scripts/design.mjs remix <primary_design_id> <secondary_design_id> [goal]
node scripts/design.mjs workflow <page_type> [--design design_id] [--template template_id] [--target file_or_directory]
node scripts/design.mjs template <template_id>
node scripts/design.mjs generate <page_type> [--template template_id]
node scripts/design.mjs invariants <design_id>
node scripts/design.mjs brief-check <page_type> [--design design_id] [--template template_id]
node scripts/design.mjs check <file_or_directory>
node scripts/design.mjs report <file_or_directory> [--out DESIGN-REPORT.md]
node scripts/design.mjs browse [--source built-in|open-design|all] [--out directory]
node scripts/design.mjs preview [--source built-in|open-design|all] [--out directory]
node scripts/design.mjs submit <design_id> <DESIGN.md> [--name display_name]
node scripts/design.mjs extract-url <url_or_html_file> [--out DESIGN.md]
node scripts/design.mjs import <figma_or_screenshot_notes> [--kind figma|screenshot] [--out DESIGN.md]
node scripts/design.mjs critique <file_or_directory> [--out directory]
node scripts/design.mjs polish <file_or_directory>
node scripts/sync-open-design.mjs
node scripts/publish-kit.mjs --platform all --package minimal|standard|offline-full [--dry-run|--check]
```

Resource sync prefers the companion resource mirror:

```bash
node scripts/sync-open-design.mjs --resources-repo /path/to/vibe-ui-resources
```

Only maintainers should use direct upstream sync:

```bash
node scripts/sync-open-design.mjs --upstream-open-design
```

## Vibe Gate

Run Vibe Gate 2.0 before implementation for visual or user-facing work:

```bash
node scripts/design.mjs read "AI release governance landing for healthcare compliance teams" --page landing --design cursor --template open-design:saas-landing
node scripts/design.mjs workflow landing --design open-design:linear-app --template open-design:saas-landing --target src/app/page.tsx
node scripts/design.mjs invariants open-design:linear-app
node scripts/design.mjs brief-check landing --design open-design:linear-app --template open-design:saas-landing
node scripts/design.mjs generate landing --template open-design:saas-landing
```

`read` writes a hidden Design Read and lightweight product context. `brief-check` writes `.vibe-ui/vibe-gate-contract.json` with dials, proof strategy, page-specific preflight, and read-aware anti-patterns. Do not render Design Read, dials, or internal scaffold text in production UI.

After implementation, run:

```bash
node scripts/design.mjs report src/app/page.tsx
node scripts/design.mjs critique src/app/page.tsx
node scripts/design.mjs polish src/app/page.tsx
```

## Source Modes

- `built-in`: curated Vibe UI registry; default mode.
- `open-design`: 150 local upstream systems, addressed as `open-design:<slug>`.
- `all`: built-in plus bundled upstream source systems.

## Publish Packages

```bash
node scripts/publish-kit.mjs --platform all --package minimal --dry-run
node scripts/publish-kit.mjs --platform all --package standard --dry-run
node scripts/publish-kit.mjs --platform all --package offline-full --dry-run
node scripts/publish-kit.mjs --platform all --package offline-full --check
```

- `minimal`: core skill files, registry, CLI, prompts, icon, and Vibe Gate watchlist.
- `standard`: `minimal` plus attribution, template index, template recipes, resource manifest, and curated source design files.
- `offline-full`: `standard` plus the 150-system upstream offline bundle and full template source bundle.

## Marketplace Updates

For a marketplace update, publish a new GitHub tag and Release, then upload the recommended package to the marketplace form.

1. Update `package.json`, `registry.json`, and `CHANGELOG.md` to the new version.
2. Run `npm run release:check`, `npm run release:dry-run`, `npm run release:smoke`, and `npm run release:zip`.
3. Push `main`, create a new `vX.Y.Z` tag, and create a GitHub Release with the three zip artifacts.
4. Use `vibe-ui-standard-skill.zip` as the default marketplace upload unless the platform requires the smallest package.
5. Use `vibe-ui-offline-full-skill.zip` only when the marketplace or reviewer wants the full offline 150-system bundle and full template source bundle.
6. Copy the version and change summary from `CHANGELOG.md` into the marketplace update notes.

## Repository Notes

For a public GitHub repository, keep generated package artifacts such as `dist/` out of git. Publish zip files through GitHub Releases when needed.

## Attribution

Vibe UI bundles upstream design resources for offline search and application. See `resource/open-design-attribution.md` for provenance and license notes.

## Disclaimer

Included styles are inspired by publicly visible UI patterns. They are not official brand systems. Do not copy logos, trademarks, proprietary assets, screenshots, or official brand claims from inspiration sources.
