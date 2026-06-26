# Dev Update: DevOps Toolbox Rename + Dual Licensing

**Date:** 2026-03-10 14:00 PST
**Author:** cc-mini
**Repo:** wip-ai-devops-toolbox-private (formerly wip-dev-tools-private)
**PR:** #44 (merged to main)

## What happened

Full-day session covering repo rename, README overhaul, dual licensing across all tools, new license guard tool, and installer dogfood.

### Repo renamed

- `wip-dev-tools` -> `wip-ai-devops-toolbox` (GitHub, both public and private)
- `wip-dev-tools-private` -> `wip-ai-devops-toolbox-private` (GitHub, both public and private)
- Local directory renamed under `ldm-os/devops/`
- All cross-repo references updated: CLAUDE.md, repos-manifest.json, repos/README.md, auto-memory, CC context files, deployed extension package.json files

### README overhaul

- Title changed from "Dev Tools" to "DevOps Toolbox"
- Interface tags added to every feature (CLI, Module, MCP, OpenClaw, Skill, CC Hook)
- Stability tags (Stable/Beta) moved to separate lines
- "Read more about..." links added to every feature
- Bold intro paragraph explaining what interfaces are
- Feature order finalized: Universal Installer, Dev Guide, LDM Dev Tools.app, Release Pipeline, License Rug-Pull Detection, License Guard, Repo Visibility Guard, Identity File Protection, Repo Manifest, Private-to-Public Sync, Post-Merge Branch Naming
- LDM Dev Tools.app added as third feature (was missing from v1.3.0 README)
- Badges added to all tool READMEs that were missing them
- Attribution standardized: "Built by Parker Todd Brooks, Lēsa (OpenClaw, Claude Opus 4.6), Claude Code (Claude Opus 4.6)."

### Dual licensing (MIT+AGPL)

- Applied Memory Crystal's MIT+AGPL pattern to all tools
- MIT for local/personal use, AGPL for cloud/hosted/marketplace distribution
- All 11 LICENSE files updated (root + 10 tools/) to dual format
- GitHub now shows "LICENSE" badge instead of "MIT License" (custom dual text)
- `.license-guard.json` config committed to root: copyright "WIP Computer, Inc.", license "MIT+AGPL", year "2026"

### New tool: wip-license-guard

- `tools/wip-license-guard/` ... CLI tool for license compliance
- Commands: `init` (interactive setup), `check` (audit), `check --fix` (auto-repair)
- Interactive first-run: asks copyright holder, license type, year, attribution
- Toolbox-aware: scans `tools/` subdirectories for sub-tool compliance
- Checks: LICENSE file exists, copyright matches, license type matches, README has license section
- Auto-fix mode repairs issues automatically
- Interfaces: CLI, Module
- Status: Beta

### Installer dogfood

- Full `wip-install` dry run: 9 tools detected, 31 interfaces found
- Full install: 30 interfaces processed successfully
- wip-license-hook CLI install has pre-existing TypeScript build issue (MCP + extension still work)

### Badge standardization

- All tool READMEs now have shields.io badges matching the root README pattern
- Badges show: npm version, CLI/TUI, MCP Server, OpenClaw Plugin, Claude Code Hook, Claude Code Skill, Universal Interface Spec (as applicable per tool)

## Files changed

- `README.md` (root) ... complete overhaul
- `LICENSE` (root + all 10 tools/) ... dual MIT+AGPL
- `tools/wip-license-guard/` (NEW) ... cli.mjs, core.mjs, package.json
- `.license-guard.json` (NEW) ... license config
- All tool READMEs ... badges, attribution, license sections
- Cross-repo refs ... CLAUDE.md, repos-manifest.json, repos/README.md, deployed extensions

## Open items

- Deploy changes to public repo (wip-ai-devops-toolbox)
- Update .github org profile README with new repo name
- Run wip-release after merge
- wip-license-hook TypeScript build issue (pre-existing)
