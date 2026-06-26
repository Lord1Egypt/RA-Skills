---
name: vibe-ui
description: Use when choosing a DESIGN.md style, applying a style to a web project, generating page prompts or template recipes, browsing bundled source systems, or checking UI code against a selected visual style.
---

# Vibe UI

Vibe UI is a DESIGN.md workflow skill for web UI work. It helps choose an inspired visual style, apply its `DESIGN.md`, generate page-specific build prompts, and review generated code for design consistency.

Vibe Gate 2.0 is the default loop for visual work: read the brief, lock the style and recipe, generate with hidden design constraints, then report/critique/polish after implementation.

Included styles are inspired by publicly visible UI patterns. Do not describe them as official brand systems.

Naming rule: Vibe UI-owned workflow features should use Vibe UI names such as Vibe Gate. Upstream names are used only for attribution, source filters, and resource ids.

## Commands

Run commands from `skills/vibe-ui` or call `node /absolute/path/to/skills/vibe-ui/scripts/design.mjs ...`.

```bash
node scripts/design.mjs list [--source built-in|open-design|all]
node scripts/design.mjs search <keyword> [--source built-in|open-design|all]
node scripts/design.mjs recommend "<user goal>" [--source built-in|open-design|all]
node scripts/design.mjs read <brief> [--page page_type] [--design design_id] [--template template_id] [--source built-in|open-design|all]
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
```

Supported page types: `landing`, `dashboard`, `pricing`, `login`, `docs`, `settings`, `profile`, `chrome-extension-landing`.

## Workflow

- For user-facing UI work, run `read "<brief>"` before implementation. It writes `.vibe-ui/brief-read.json` and `.vibe-ui/product-context.json` with audience, buyer anxiety, register, dials, proof strategy, and section strategy.
- If the user names a style, run `use <design_id>` in the project root to write `DESIGN.md`, `DESIGN.generated.md`, and `.vibe-ui/current-design.json`.
- If the user has not chosen a style, run `recommend "<goal>"` or use the recommendation from `read`. Use built-in curated styles by default; add `--source open-design` when they want the broader bundled source library.
- Use namespaced source ids such as `open-design:linear-app`, `open-design:revolut`, or `open-design:airbnb`.
- If the user asks for a page pattern, run `template <template_id>` or `generate <page_type> --template <template_id>`.
- If the user asks for a page that should feel "like" a known style, run `like <design_id> [page_type]` for a brand-safe prompt.
- If the user wants to browse or compare styles visually, run `browse --source all` to generate a local static browser.
- Before generating or editing a page, run `workflow <page_type> --design <design_id> --template <template_id>` for the recommended Vibe UI execution chain.
- Run `invariants <design_id>` and `brief-check <page_type> --design <design_id>` when the task is visual or user-facing. `brief-check` writes `.vibe-ui/vibe-gate-contract.json` with Design Read, dials, page preflight, and anti-pattern watchlist.
- Run `generate <page_type>` and follow the output together with the project's existing stack and components.
- After implementation, run `check <file_or_directory>` or `report <file_or_directory>`. If the report is not Ready or the UI still feels generic, run `critique <target>` and then use `polish <target>` to produce a repair prompt.

## Design Library

- `registry.json` contains 18 high-confidence curated built-in styles.
- `resource/open-design-systems.json` bundles 150 upstream `DESIGN.md` systems as one offline resource.
- `resource/open-design-template-index.json` indexes 111 upstream `design-templates` mirrored through `Liuwei1125/vibe-ui-resources`.
- `resource/open-design-template-recipes.json` contains Vibe UI template recipes distilled from upstream source patterns, including commerce, launch, pricing, waitlist, docs, dashboard, kanban, mobile, onboarding, portfolio, and SaaS recipes.
- `resource/open-design-template-sources.json` contains the full template source bundle for offline-full packaging.
- `resource/resources-sync-manifest.json` records the resource mirror source commit, counts, and hashes.
- `resource/open-design-attribution.md` records upstream license and provenance notes.
- `resource/ui-anti-patterns.json` contains the Vibe Gate 2.0 watchlist used by `brief-check`, `check`, `report`, `critique`, and `polish`.

Default curated styles include `linear`, `vercel`, `stripe`, `apple`, `cursor`, `openai`, `notion`, `raycast`, `mintlify`, `framer`, `airbnb`, `shopify`, `feishu`, `doubao`, `xiaohongshu`, `wechat-reading`, `slack`, and `figma`.

## Guardrails

- Treat `DESIGN.md` as the source of truth for colors, typography, spacing, radius, shadows, layout rhythm, density, and interaction style.
- Do not copy real logos, trademarks, proprietary assets, or official brand claims from inspiration sources.
- Keep Design Read, dials, and internal scaffold text in `.vibe-ui` JSON, reports, prompts, or comments; do not render them in production UI.
- Add stable `data-od-id` values to top-level generated sections when using source-backed recipes.
- Avoid default LLM indigo, emoji-as-icon decoration, invented metrics, filler copy, arbitrary gradients, heavy glass, and unsupported shadows unless the selected `DESIGN.md` explicitly allows them.
- Use Vibe Gate as the default execution contract: `read` interprets the brief, `workflow` shows the full chain, `invariants` states what must not drift, `brief-check` records materials and anti-patterns before implementation, `generate` carries the hidden Design Read constraints, and `report`/`critique`/`polish` close the revision loop after implementation.
- The static checker is a first-pass review. Still run the project tests and inspect the rendered UI for frontend work.
