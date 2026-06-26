# AI DevOps Toolbox ... Read Me First

**Last updated:** 2026-04-21
**Status:** Living document. Read this before any plan, build, or PR.

---

## What This File Is

This is the product bible for this repo. It answers: what is this thing, why does it exist, how does it work, and what's the current state. Every person and agent working on this repo reads this first.

**Keep it current.** Update it when the architecture changes, when major features ship, when the mental model shifts. If this file is stale, the team is working from bad context.

**Keep it honest.** Don't describe the aspirational version. Describe what's built and what's missing. Plans go in `plans-prds/`. This file is ground truth.

---

## This Folder

```
product/
  readme-first-product.md   <- you're here (the product bible)
  _trash/
  notes/                    <- freeform notes, research, observations
    feedback/               <- external reviews (GPT, Grok, etc.)
  plans-prds/               <- plans with lifecycle stages
    roadmap.md              <- the prioritized roadmap
    current/                <- plans being built right now
    upcoming/               <- plans that are next
    archive-complete/       <- plans that shipped
    todos/                  <- per-agent task lists
    _sort/                  <- plans that need categorizing
    _trash/
  product-ideas/            <- ideas that aren't plans yet
```

**Navigate:**
- **Want to know what's planned?** Read `plans-prds/roadmap.md`.
- **Want to know what's being built right now?** Look in `plans-prds/current/`.
- **Have an idea?** Write it up in `product-ideas/`.
- **Ready to turn an idea into a plan?** Move it from `product-ideas/` to `plans-prds/upcoming/` (or `current/` if starting now).

**Plan lifecycle:**
```
product-ideas/  ->  upcoming/  ->  current/  ->  archive-complete/
   (idea)          (planned)     (building)       (shipped)
```

---

## What AI DevOps Toolbox Is

Your AI writes code. But does it know how to release it? Check license compliance? Protect your identity files? Sync private repos to public? Follow a real development process?

AI DevOps Toolbox is 17 tools that teach your AI how to do all of this. You don't run them manually. Your AI knows how to use them. Built by a team of humans and AIs shipping real software together at WIP Computer.

---

## Core Concepts

**Six interfaces, one tool.** Every tool can ship up to six interfaces: CLI, Module, MCP, OC Plugin, Skill, CC Hook. Universal Installer detects which ones a repo supports and deploys them all. One command.

**SKILL.md is the real interface.** The README is the front door for humans. SKILL.md is the documentation your AI reads. It works in both Claude Code (reads it as a prompt) and OpenClaw (loaded from `~/.openclaw/skills/`). Same file, both systems.

**README standard.** Every repo follows the same pattern: badges, tagline, "Teach Your AI" onboarding block, features, interface coverage table, more info, license. Technical details go to TECHNICAL.md. The README is for deciding whether to use it.

**Toolbox, not monorepo.** Each tool in `tools/` is self-contained with its own package.json. Versioning is collective. One release covers everything.

**Never delete, always trash.** Files move to `_trash/`. Nothing is ever removed from the repo. Completed plans move to `archive-complete/`. Superseded files move to `_trash/`.

---

## How It Works

```
tools/
  wip-universal-installer/     <- installs everything else (CLI, bootstraps LDM OS)
  wip-release/                 <- release pipeline (CLI + MCP)
  wip-license-hook/            <- dependency license scanning (CLI + MCP)
  wip-license-guard/           <- repo license compliance (CLI + CC Hook)
  wip-file-guard/              <- identity file protection (CLI + OC Plugin + CC Hook)
  wip-branch-guard/            <- blocks writes on main, --no-verify, --force (CC Hook)
  wip-repo-permissions-hook/   <- repo visibility guard (CLI + MCP + OC Plugin + CC Hook)
  wip-repos/                   <- repo manifest reconciler (CLI + MCP)
  wip-repo-init/               <- repo scaffolding (CLI)
  wip-readme-format/           <- README formatter (CLI)
  deploy-public/               <- private-to-public sync (CLI)
  post-merge-rename/           <- branch cleanup (CLI)
  ldm-jobs/                    <- scheduled automation (macOS app)
```

**Install flow:** `ldm install wipcomputer/wip-ai-devops-toolbox` (or `wip-install`, which bootstraps LDM OS automatically). Clones the repo, scans each tool for interface signals (bin, mcp-server.mjs, openclaw.plugin.json, SKILL.md, guard.mjs), then deploys each to the right location. CLI goes to PATH, MCP registers at user scope, plugins deploy to `~/.ldm/extensions/` and `~/.openclaw/extensions/`, skills deploy to `~/.openclaw/skills/<tool>/`, hooks wire into `~/.claude/settings.json`.

**Release flow:** Work on a branch, PR to main, merge, run `wip-release patch|minor|major`. It bumps version, syncs SKILL.md, updates CHANGELOG.md, auto-detects dev updates as release notes, commits, tags, pushes, publishes to npm + GitHub Packages + GitHub Releases, renames merged branches. Then `deploy-public.sh` syncs to the public repo.

**State lives in:**
- `~/.ldm/extensions/registry.json` ... what's installed
- `~/.claude/settings.json` ... CC Hooks
- `~/.claude/.mcp.json` ... MCP registrations (CC)
- `~/.openclaw/.mcp.json` ... MCP registrations (OpenClaw)
- `~/.openclaw/skills/<tool>/SKILL.md` ... deployed skills
- `~/.openclaw/extensions/<name>/` ... deployed plugins

---

## Key Source Files

| File | What It Does |
|------|-------------|
| `tools/wip-universal-installer/install.js` | The installer. Detects interfaces, deploys everything |
| `tools/wip-universal-installer/detect.mjs` | Interface detection logic (scans for signals) |
| `tools/wip-release/core.mjs` | Release pipeline core (version bump through GitHub release) |
| `tools/wip-release/mcp-server.mjs` | MCP server for release + release_status |
| `tools/wip-license-hook/mcp-server.mjs` | MCP server for license scan/audit/gate/ledger |
| `tools/wip-repo-permissions-hook/guard.mjs` | CC Hook + OC Plugin for visibility guard |
| `tools/wip-file-guard/guard.mjs` | CC Hook + OC Plugin for identity file protection |
| `tools/wip-branch-guard/guard.mjs` | CC Hook: blocks writes on main, --no-verify, --force |
| `tools/wip-license-guard/guard.mjs` | CC Hook: blocks commit/push on license failures |
| `tools/wip-repos/mcp-server.mjs` | MCP server for manifest reconciliation |
| `tools/wip-repo-init/init.mjs` | Repo init tool (scaffolds ai/ structure) |
| `tools/wip-readme-format/format.mjs` | README formatter (section-based staging + deploy) |
| `SKILL.md` | The toolbox-level skill file (all tools documented here) |
| `README.md` | The public README (follows the standard) |
| `TECHNICAL.md` | Architecture, build steps, dev setup |

---

## What's Built (as of v1.9.72)

- Universal Installer with toolbox mode, EEXIST handling, skill deployment, LDM OS auto-bootstrap
- Release pipeline with license gate, product docs gate, release notes file requirement, issue reference requirement, auto-close issues, dev update auto-detection, skill publish to website, ClawHub publish
- License rug-pull detection with MCP, ledger, daily cron scan
- License guard with CC Hook, `--from-standard`, and wip-release integration
- Branch guard (CC Hook: blocks writes on main, blocks --no-verify and --force)
- Global git pre-commit hook (blocks commits on main/master across all repos)
- Identity file protection (CC Hook + OC Plugin)
- Repo visibility guard (CC Hook + OC Plugin + MCP)
- Repo manifest reconciler with MCP
- Repo init (ai/ directory scaffolding with templates/)
- README formatter (section-based staging, --deploy, --check, toolbox mode)
- Private-to-public sync with --dry-run, GitHub Packages from public, co-author lines
- Post-merge branch naming and pruning
- LDM Dev Tools.app (macOS scheduled automation)
- README standard and "Teach Your AI" onboarding pattern
- Dual MIT+AGPL licensing with CLA
- Dev Guide with release notes workflow documented in both public and private guides
- --version flag on all 12 CLI tools
- SKILL.md conversational install flow (ldm install, Memory Crystal pattern)
- .publish-skill.json for auto-publishing SKILL.md to website on release

---

## What's Missing

- No GitHub Actions pack
- No security scanning (SBOM, CVE)
- No multi-language publishing (npm only)
- No org-wide dashboard
- No demo video of wip-release in action
- No example template repo for people to clone and test
- wip-release should auto-update roadmap.md and readme-first-product.md before deploy
- Plans in current/ should auto-move to archive-complete/ when all items checked

---

## Key Documents

| Document | Location |
|----------|----------|
| **This file** | `readme-first-product.md` |
| **Roadmap** | `plans-prds/roadmap.md` |
| **Interface system + README standard** | `../notes/2026-03-10--cc-mini--readme-standard-and-universal-installer-vision.md` |
| **Dev guide (private)** | `../../DEV-GUIDE-FOR-WIP-ONLY-PRIVATE.md` |
| **GPT/Grok feedback** | `notes/feedback/` |
| **Product ideas** | `product-ideas/` |

---

## Principles

1. **Agent-first.** The AI is the primary user. READMEs onboard humans. SKILL.md onboards agents.
2. **One command.** Install, release, deploy, audit. Each workflow is one command. No multi-step manual processes.
3. **Never delete.** Move to `_trash/`. Everything stays in git history.
4. **Dry-run first.** Every destructive operation has `--dry-run`. Show what will change before changing it.
5. **Dual-license.** MIT for using the tools. AGPL for reselling them. Free for everyone except commercial resellers.
6. **Private by default.** Working repos are private. Public repos are clean mirrors. The `ai/` folder never ships.
7. **Co-authored.** Every commit has all three contributors. Parker, Lesa, Claude Code. That's how we work.

---

## How to Update This File

- **New major feature shipped?** Update "What's Built" and "What's Missing."
- **Architecture changed?** Update "How It Works" and "Key Source Files."
- **New mental model?** Update "Core Concepts."
- **New principle?** Add to "Principles."
- **Always update** the "Last updated" date at the top.
- **Never delete sections.** If a section is empty, leave the heading. It reminds the team to fill it in.
