# Changelog

All notable changes to this project will be documented in this file.

## 1.1.0 - 2026-06-04

### Added

- Vibe Gate 2.0 `read "<brief>"` command that writes `.vibe-ui/brief-read.json` and `.vibe-ui/product-context.json`.
- Design Read fields for audience, buyer anxiety, register, density/variance/motion dials, proof strategy, section strategy, anti-references, and recommended design/template.
- Read-aware `brief-check` contracts with Design Read, dials, page-specific preflight, and contextual anti-pattern watchlists.
- `critique <target>` command that writes timestamped `.vibe-ui/critique/critique-*.md` reports.
- `polish <target>` command that prints a Vibe Gate 2.0 repair prompt.
- Registry dial metadata for built-in styles and page-specific preflight metadata for template recipes.
- Expanded deterministic anti-pattern library covering AI tells, proof failures, layout repetition, typography risks, accessibility risks, and scaffold leakage.
- `resource/open-design-template-index.json` with 111 indexed OpenDesign `design-templates` from the Vibe UI resources mirror.
- Expanded Vibe UI template recipes for commerce home, product launch, pricing, waitlist, docs home, dashboard, kanban, mobile app, mobile onboarding, portfolio profile, and SaaS landing.
- `resource/open-design-template-sources.json` and `resource/resources-sync-manifest.json` for offline-full packaging and resource provenance.

### Changed

- `generate` now includes hidden Design Read guidance when a brief read is available.
- `report` now includes Vibe Gate 2.0 synthesis for Design Read execution, template completion, buyer anxiety coverage, and proof strategy credibility.
- README, README.zh-CN.md, SKILL.md, and AGENTS.md now describe the full `read -> brief-check -> generate -> report -> critique/polish` loop.
- `read` now recommends domain-specific template recipes such as `vibe:commerce-home` for shopping and retail briefs instead of defaulting every landing page to SaaS.
- `scripts/sync-open-design.mjs` now consumes the `Liuwei1125/vibe-ui-resources` mirror by default and keeps direct upstream sync as a maintainer-only path.

## 1.0.1 - 2026-06-01

### Added

- Marketplace update guidance in English and Chinese README files.
- Release checklist wording for versioned tags and marketplace upload package selection.

### Changed

- Bumped package and registry metadata to `1.0.1`.
- Clarified that `vibe-ui-standard-skill.zip` is the recommended default marketplace upload, while `offline-full` is for full offline bundle requests.

## 1.0.0 - 2026-06-01

### Added

- Initial Vibe UI skill for local-first `DESIGN.md` workflows.
- 18 curated built-in styles for high-confidence style selection.
- 150 bundled upstream `DESIGN.md` systems for offline search and application.
- Vibe UI template recipes for landing pages, dashboards, and docs pages.
- Vibe Gate workflow with `workflow`, `invariants`, `brief-check`, persisted contracts, and report guidance.
- Static browser generation for built-in styles, upstream source systems, and template recipes.
- Design consistency reporting with score, decision, blockers, top fixes, and Bad/Fix/Evidence fields.
- English `README.md` and Chinese `README.zh-CN.md`.
- Publish package modes for `minimal`, `standard`, and `offline-full`.
- Publish preflight checks with `scripts/publish-kit.mjs --check`.
- GitHub-ready repository governance files, issue templates, PR template, and CI workflow.

### Security

- No default network requests in normal Vibe UI CLI usage.
- No model API calls.
- Brand-safety guardrails for inspiration-based visual styles.

### Attribution

- Added upstream provenance and license notes in `resource/open-design-attribution.md`.
