# Dev Update: Memory Crystal v0.7.8 to v0.7.19 (Full Session)

**Date:** 2026-03-13
**Author:** CC-Mini
**Session:** memory-db-fix (memory-crstal01)

---

## Summary

Marathon session. Started with investigating a "FAILING" embeddings report. Ended with 11 patch releases, a new CLI command, scoring fixes, installer overhaul, agent.txt on wip.computer, and three product specs.

## What Shipped (v0.7.8 to v0.7.19)

### Database Cleanup (v0.7.8)
- DELETE trigger on chunks table cascading to chunks_vec and chunks_fts
- `crystal cleanup` CLI command with `--dry-run` (backup, pause cron, clean orphans, rebuild FTS, VACUUM, resume cron)
- `cleanOrphans()` method on Crystal class
- Cleaned 141,651 orphaned vectors + 141,652 orphaned FTS entries
- Database: 1.96 GB -> 1.45 GB (525 MB saved)
- Product rule: Memory Crystal indexes conversations only, not raw directory scans

### Doctor Fixes (v0.7.9)
- `checkOpEmbeddings()` detects 1Password SA token as embedding provider
- Backup check detects LDM Dev Tools.app cron and existing backup files
- Bridge check detects local extension directories
- `crystal init --dry-run` shows full doctor output instead of empty "already up to date"

### Install Prompt + Website (v0.7.10)
- README install prompt URL changed from GitHub to `wip.computer/install/memory-crystal.txt`
- `wip.computer/agent.txt` created (front door for AI agents)
- 8 SKILL.md files published to `wip.computer/install/*.txt`
- `publish-skill.sh` script for auto-publishing SKILL.md to websites

### npm Scoping (v0.7.10-v0.7.11)
- Package renamed from `memory-crystal` to `@wipcomputer/memory-crystal`
- GitHub Packages publish now works (scoping fix)
- LDM OS catalog.json updated

### Installer Fixes (v0.7.12-v0.7.17)
- npm version detection: `crystal init` checks npm for newer versions before proceeding
- Semver comparison: fixed string comparison bug ("0.7.14" > "0.7.8" was false)
- Infinite loop fix: removed recursive `execSync('crystal init')` after npm upgrade
- SKILL.md Step 0 made mandatory: always `npm install -g` before `crystal init`
- Version sync: `package.json` always copied to extensions after ldm install delegation

### Bridge Detection (v0.7.18)
- `isBridgeRegistered()` now checks `claude mcp get` user scope in addition to `.mcp.json` files

### Score Normalization (v0.7.19)
- Removed `* 8` multiplier that clamped all scores to 100%
- Added relative normalization: top result = 95%, others scaled relative
- Scores now show meaningful variation (95%, 90%, 75%) instead of all 100%

## Bugs Filed

| Issue | Repo | Status |
|-------|------|--------|
| #50 | memory-crystal-private | npm link runs from repo clone | Fixed |
| #51 | memory-crystal-private | Doctor false reports (5 issues) | Fixed |
| #55 | memory-crystal-private | Install refs: memory-crystal -> @wipcomputer | Fixed |
| #57 | memory-crystal-private | crystal init doesn't detect scoped npm | Fixed |
| #63 | memory-crystal-private | init doesn't update extension package.json | Fixed |
| #64 | memory-crystal-private | Bridge check fails on user scope | Fixed |
| #149 | wip-ai-devops-toolbox-private | Pre-merge product doc check | Open (plan written) |
| #150 | wip-ai-devops-toolbox-private | Merge/Deploy/Install conflated | Open (rule added to Dev Guide) |
| #1 | wip-root-key-private | Root key gates install (sudo for agents) | Open (plan written) |

## Product Docs Written

- `wip-secrets-ios-private/ai/product/product-ideas/lesa-app-remote-biometrics.md` ... Lesa iOS app with remote biometrics
- `wip-secrets-ios-private/ai/product/bugs/2026-03-13--plaintext-sa-token-on-disk.md` ... plaintext SA token bug
- `wip-ai-devops-toolbox-private/ai/product/plans-prds/upcoming/` ... 3 plans (auto-publish skill, merge-time doc check, install guard hook)
- `wip-ai-devops-toolbox-private/ai/product/bugs/2026-03-13--cc-mini--merge-deploy-install-conflated.md`
- `wip-root-key-private/ai/product/plans-prds/upcoming/2026-03-13--cc-mini--root-key-gates-install.md` ... sudo for agents
- `wip-agent-pay-private/ai/product/plans-prds/upcoming/agent-txt-and-store-discovery--2026-03-13.md` ... agent.txt + store

## Key Decisions

1. **Merge, Deploy, Install are three separate steps.** Never combine. Added to both Dev Guides and CLAUDE.md.
2. **Memory Crystal indexes conversations only.** No raw directory scanning.
3. **Root key gates install.** sudo for agents. Three layers: process, hook, crypto.
4. **agent.txt convention.** Plain text at `yoursite.com/agent.txt` for AI agent discovery.
5. **Step 0 is mandatory.** Always `npm install -g` before `crystal init`.
