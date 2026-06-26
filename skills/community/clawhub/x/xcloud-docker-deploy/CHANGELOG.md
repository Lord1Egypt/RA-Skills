# Changelog

## v1.4.1 — 2026-06-23

### Fixed
- Addressed ClawHub security review concerns from the LLM audit.
- Replaced over-broad security claims (`no_network_calls`, `local_only`, and sandbox wording) with accurate package-level claims: templates only, no runtime execution, and explicit user confirmation before impactful operations.
- Constrained the manifest language so project inspection, file generation, credential collection, and live API routing require confirmation gates.
- Added least-privilege, short-lived token guidance and a separate consent step before any `XCLOUD_API_TOKEN` use.
- Added production safety guidance for branches, backups, staging, deployment webhooks, migrations, and live xCloud API mutations.
- Regenerated `.clawhubsafe` checksums.

## v1.4.0 — 2026-06-23

### Changed
- Reworked the first screen to start with human-friendly deployment prompts instead of platform internals.
- Added a simple "This is my project. I want to deploy it on xCloud" usage flow for agents and users.
- Added explicit guidance for pairing this Docker deploy skill with official xCloud API skills for live account/server/site actions.
- Added private `XCLOUD_API_TOKEN` handling guidance: ask only when live API access is needed, never print/store/commit tokens.

## v1.3.2 — 2026-06-23

### Changed
- Modernized the ClawHub listing format to match the newer Token Optimizer card style.
- Added top metadata links for GitHub, latest GitHub release, xCloud Agent Skills, xCloud API docs, and security notes.
- Updated the public summary to lead with `xCloud Docker Deploy v1.3.2` and the xCloud-safe `80:80` to `3080:80` port rewrite.

## v1.3.1 — 2026-06-23

### Changed
- Updated the ClawHub-facing summary so the listing highlights xCloud-safe host port handling and current API-skill-aware deployment guidance.

## v1.3.0 — 2026-06-23

### Fixed
- Added a hard xCloud rule that final compose output must never bind host port `80` or `443`.
- Added explicit rewrite guidance for `80:80` to `3080:80`, with xCloud exposed/primary port `3080`.
- Updated Laravel nginx compose template from `8080:80` to the standard `3080:80` mapping.

### Added
- Documented the xCloud traffic path: user → xCloud Nginx `80/443` → Docker host port `>=1024` → container port.
- Added current xCloud API/agent-skill context so agents know when to use this Docker deploy skill versus official live-operation skills.

## v1.2.0 — 2026-03-03

### Added
- `skill.json` — machine-readable metadata for SkillsMP, ClawHub, and all AI agent indexers (name, version, author, tags, capabilities, supported stacks, install commands, platforms, security flags)
- `.github/skillsmp.yml` — SkillsMP indexing config (category, tags, platforms, featured examples)
- `.github/FUNDING.yml` — GitHub Sponsors maintenance signal
- `CONTRIBUTING.md` — community contribution guide (how to add stacks, fix bugs, submit PRs)

### Changed
- `SKILL.md` frontmatter enriched: YAML tags array (14 tags), `category`, `author`, `platforms` list, `version`, `homepage`, `repository`
- `README.md` rewritten: cleaner structure, usage examples, supported stacks table, full compatibility table, all install paths
- All version references bumped to 1.2.0

## v1.1.1 — 2026-03-03

### Changed
- README rewrite for SkillsMP/Claude Code/Codex CLI discoverability — SkillsMP badge, Codex CLI install path, full compatibility table

## v1.1.0 — 2026-03-03

### Added
- `DETECT.md`: Stack fingerprinting — auto-detects WordPress, Laravel, PHP, Node.js, Next.js, NestJS, Nuxt, Python, Go, Rust
- **Phase 0 routing table** in `SKILL.md` — project type detection before any Docker work
- **5 production Dockerfiles**: Laravel (PHP 8.3-fpm), Next.js (standalone), Node.js (multi-stage), PHP generic (Apache), Python/FastAPI
- **4 compose templates**: Laravel+MySQL+Redis+Queue, Next.js+Postgres, Node.js API+Postgres, FastAPI+Postgres+Celery+Redis
- **4 native deploy guides**: WordPress (one-click + Git), Laravel (composer+artisan), PHP, Node.js
- **Decision matrix** (`references/xcloud-deploy-paths.md`): Native vs Docker by stack + DB + background jobs
- **2 new examples**: Laravel native end-to-end, Next.js Docker end-to-end

### Changed
- `SKILL.md` description updated to reflect full project-aware deployment capability
- README rewritten for SkillsMP/Claude Code/Codex CLI discoverability

## v1.0.0 — 2026-03-03

### Initial Release
- Scenario A: Build-from-source (generate GitHub Actions → GHCR)
- Scenario B: Proxy conflict (remove Caddy/Traefik, add nginx-router)
- Scenario C: Multi-service build (matrix GitHub Actions workflow)
- External config file embedding via Docker `configs:` block
- References: xCloud constraints, scenario deep-dives
- Examples: Rybbit Analytics, custom Dockerfile, fullstack monorepo
