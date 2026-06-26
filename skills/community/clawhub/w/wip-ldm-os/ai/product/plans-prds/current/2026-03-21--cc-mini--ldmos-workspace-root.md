# Plan: LDMOS Workspace Root

**Date:** 2026-03-21
**Author:** cc-mini (with Parker)
**Status:** Active exploration

## The Idea

One folder per organization. Everything lives inside it. Every company that runs LDM OS gets one.

Currently `~/wipcomputer/`. For other companies: `~/LDMOS/` or whatever they choose. The name is configurable. The structure is standard.

## What It Is

Not just a working directory. The entire operational surface:

- **Config:** Who you are, how you work, what your conventions are
- **Staff:** Everyone's working dirs (humans + agents)
- **Repos:** All code, organized by category
- **Templates:** License, README, CLAUDE.md, install prompts
- **Docs:** Human-readable system documentation (not API docs... operational docs)
- **Agents:** Registry of who exists, what prefix, what harness
- **Secrets:** References to 1Password or other secret stores
- **Backups:** Central backup config and status

## Proposed Structure

```
~/LDMOS/                             <- or ~/wipcomputer/, ~/acme-corp/, etc.
  config.json                        <- the one config: org, people, agents, conventions

  docs/                              <- human-readable operational docs
    how-backup-works.md              <- what gets backed up, when, where, how to restore
    what-is-ldm.md                   <- ~/.ldm/ explained
    what-is-icloud.md                <- what syncs, what doesn't, why
    what-is-openclaw.md              <- ~/.openclaw/ explained
    how-releases-work.md             <- the full pipeline
    how-install-works.md             <- ldm install, the prompt, dogfooding
    how-agents-work.md               <- agents, sessions, bridge, communication
    how-worktrees-work.md            <- _worktrees/, guard, convention
    directory-map.md                 <- what lives where and why

  staff/                             <- everyone's working dirs
    parker/                          <- human
      documents/
      repos/                         <- Parker's repo clones (if separate from shared)
    cc-mini/                         <- Claude Code on Mac mini
      documents/
        journals/                    <- human-forced journals (Parker says "write a journal")
        automated/                   <- system-generated human-readable output (summaries, daily digests)
        sessions/                    <- legacy (moved to ~/.ldm/agents/cc-mini/memory/sessions/)
        sessions/
    cc-air/                          <- Claude Code on MacBook Air
    lesa/                            <- Lesa (OpenClaw agent)

  repos/                             <- all code repos
    ldm-os/                          <- organizational folder (NOT a monorepo)
      components/
      devops/
      utilities/
      apis/
      apps/
      identity/
    _worktrees/                      <- centralized worktrees
    _sort/                           <- uncategorized
    _sunsetted/                      <- deprecated
    _trash/                          <- deleted (never truly delete)

  templates/                         <- org-specific overrides (checked first)
    claude-md/                       <- org's CLAUDE.md customizations
    license/                         <- org's license text (MIT+AGPL, CLA)
    readme/                          <- org's badges, footer, built-by line
    install-prompt/                  <- org's install prompt
    dev-guide-private.md             <- org-specific dev conventions (branch prefixes, agents, deploy paths)

  LDMOS/                             <- LDM OS system layer
    system-working-directories/      <- macOS aliases to ~/.ldm, iCloud, etc.
    templates/                       <- system defaults (shipped by ldm install, never edit)
      repo-init/                     <- standard ai/ folder scaffold
      claude-md/                     <- default CLAUDE.md templates
      license/                       <- default license templates
      readme/                        <- default readme templates
    docs/                            <- human-readable operational docs
      how-backup-works.md
      what-is-ldm.md
      how-releases-work.md
      how-install-works.md
      how-agents-work.md
      directory-map.md

  agents/                            <- agent registry
    agents.json                      <- who exists, harness, prefix, machine

  secrets/                           <- secret store references (not actual secrets)
    README.md                        <- how to access secrets, what's where

  backups/                           <- backup config and status
    config.json                      <- what to back up, where, when
    last-run.json                    <- status of last backup
```

## config.json

The one file every tool reads from:

```json
{
  "org": "wipcomputer",
  "name": "WIP Computer",
  "npmScope": "@wipcomputer",
  "github": {
    "org": "wipcomputer",
    "accounts": {
      "parker": "parkertoddbrooks",
      "lesa": "lesaai"
    }
  },
  "coAuthors": [
    "Parker Todd Brooks <parkertoddbrooks@users.noreply.github.com>",
    "Lesa <lesaai@icloud.com>",
    "Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
  ],
  "branchPrefixes": {
    "cc-mini": "Claude Code on Mac mini",
    "cc-air": "Claude Code on MacBook Air",
    "lesa-mini": "Lesa on Mac mini"
  },
  "paths": {
    "ldm": "~/.ldm",
    "openclaw": "~/.openclaw",
    "icloud": "~/Documents/wipcomputer--mac-mini-01"
  },
  "license": "MIT+AGPL",
  "timezone": "America/Los_Angeles"
}
```

## Template Inheritance

Two layers. Tools check org first, fall back to system.

```
~/wipcomputer/templates/          <- org overrides (your co-authors, your license, your conventions)
~/wipcomputer/LDMOS/templates/    <- system defaults (shipped by LDM OS, same for everyone)
```

This solves the private/public dev guide problem:
- `DEV-GUIDE-GENERAL-PUBLIC.md` stays in the toolbox repo. Ships with LDM OS. Same for everyone.
- `DEV-GUIDE-FOR-WIP-ONLY-PRIVATE.md` moves to `~/wipcomputer/templates/dev-guide-private.md`. It's org-specific.

The toolbox repo stops carrying org-specific docs in `ai/`. The `ai/` folder stays clean. Org-specific customizations live in the org workspace where they belong.

## Staff Document Structure

Each agent has a `documents/` folder with a clear split:
- `journals/` ... human-forced (Parker says "write a journal")
- `automated/` ... system-generated, human-readable (summaries, daily digests)
- Raw logs and session exports stay in `~/.ldm/agents/<id>/memory/`

## Relationship to ~/.ldm/

`~/.ldm/` is the runtime. Extensions, memory, state, logs.
`~/wipcomputer/` is the workspace. Repos, staff, templates, docs, config.

Same split as `/usr/` (system) vs `/home/` (user).

`~/.ldm/config.json` points to the workspace: `{ "workspace": "~/wipcomputer" }`. Tools never hardcode the path.

## Relationship to CONSTRUCT

CONSTRUCT (github.com/parkertoddbrooks/CONSTRUCT) was the per-project version of this idea for Swift. Architecture enforcement, AI context, template scaffolding. LDMOS workspace is the per-organization version. Not language-specific. Not project-specific. The whole operation.

## Relationship to iCloud

Currently `~/Documents/wipcomputer--mac-mini-01/` syncs via iCloud. The LDMOS workspace would be local-only (no iCloud sync for repos). iCloud becomes an offsite backup target, not the primary location.

The folder restructure (already in progress) is moving things from iCloud to `~/wipcomputer/`. This plan formalizes that as the LDMOS workspace standard.

## For Other Companies

`ldm init --workspace ~/acme-corp` would scaffold this entire tree. The company fills in config.json. Every tool reads from it. No hardcoded org names, npm scopes, or co-author lines anywhere in the codebase.

The install prompt:
```
Read https://wip.computer/install/wip-ldm-os.txt
```

Would detect if a workspace exists. If not, guide the user through creating one.

## Hardcoded Value Audit

Full audit across all repos, config files, LaunchAgents, and CLAUDE.md files. ~250 hardcoded org-specific values found.

### What needs to read from settings/config.json

| Category | Count | Where | config.json key |
|----------|-------|-------|----------------|
| Agent ID defaults | 15+ | memory-crystal, ldm-os boot hook, poller, cc-hook | `agents.{id}` |
| Timezone | 5 | boot-hook, cc-hook, poller, crystal-serve | `timezone` |
| Co-author lines | 1 set | deploy-public.sh | `coAuthors` |
| Staff directory paths | 5+ | memory-crystal, private-mode, healthcheck, boot-config | `paths.workspace` |
| Branch prefix examples | 3 | guard.mjs error messages | `agents.{id}.prefix` |
| npm scope in installer logic | 10+ | ldm.js, catalog.json, installer.ts | `npmScope` |
| Cloudflare worker URLs | 8 | memory-crystal relay, agent-pay | `deploy.workers` |
| Gateway token | 1 | openclaw.json, LaunchAgent plist | Move to 1Password |

### What stays hardcoded (fine as-is)

| Category | Count | Why |
|----------|-------|-----|
| npm package names in package.json | 40+ | These ARE the official package names |
| GitHub repo URLs in package.json | 30+ | Official locations |
| Type comments with agent ID examples | 2 | Documentation |
| License ledger references | 1 | Tracking data |

### Security issues found

- `OPENCLAW_GATEWAY_TOKEN` hardcoded in `ai.openclaw.gateway.plist` and `openclaw.json`. Should be in 1Password or env var.

### Config file sprawl

| Location | Org-specific? | Notes |
|----------|--------------|-------|
| `~/.ldm/config.json` | Minimal | Agent list only |
| `~/.openclaw/openclaw.json` | High | Gateway token, vault name, extra paths |
| `~/.claude/CLAUDE.md` | Heavy | Entire file is org-specific instructions |
| `~/.openclaw/CLAUDE.md` | Heavy | Near-duplicate of above |
| `~/.claude/settings.json` | Heavy | All hook paths hardcode /Users/lesa/ |
| `~/.openclaw/workspace/TOOLS.md` | Heavy | Lesa's tool reference, all paths hardcoded |
| `~/Library/LaunchAgents/*.plist` | Medium | Script paths, gateway token |

### Implementation: loadOrgConfig()

Every tool needs a function that reads `~/wipcomputer/settings/config.json`. The path to the workspace comes from `~/.ldm/config.json`:

```json
// ~/.ldm/config.json
{ "workspace": "~/wipcomputer" }
```

Tools resolve: `workspace + '/settings/config.json'`. Values cascade:
1. Environment variable (highest priority)
2. settings/config.json (org config)
3. Hardcoded default (lowest priority, for bootstrapping)

### CLAUDE.md Three-Level Split

The current 368-line CLAUDE.md at `~/.openclaw/CLAUDE.md` (duplicated at `~/.claude/CLAUDE.md`) splits into three levels:

**Level 1: `~/.claude/CLAUDE.md` (global, every session, ~30 lines)**
- Writing style (no em dashes, timezone, ellipsis)
- Git merge rules (never squash, never push to main)
- Co-authors on every commit (from config.json)
- 1Password CLI: always use SA token
- Never run tools from repo clones
- Shared file protection

Universal rules. Mostly generated from `settings/config.json`.

**Level 2: `~/wipcomputer/CLAUDE.md` (workspace, when opened here, ~100-150 lines)**
- Merge, deploy, install (three-step pipeline)
- Release pipeline (wip-release details)
- Directory structure (where repos live)
- Config architecture (openclaw.json details)
- Plugin table
- Health monitoring
- Memory system
- Agent architecture (Lesa, CC, bridge, MCP tools)
- Boot sequence / end-of-session
- What NOT to touch

The org's operational manual. Shrinks significantly once per-repo CLAUDE.md exists because repo-specific details move to Level 3.

**Level 3: `<repo>/CLAUDE.md` (per-repo, generated by `wip-repos claude`)**
- What this repo does
- Build/test/lint commands (from package.json)
- Repo-specific landmines and guardrails
- Ecosystem section (related repos, their interfaces)
- Dependencies on sibling repos

Currently doesn't exist in any repo. `wip-repos claude --init` creates them.

Claude Code already supports this cascade. It reads `~/.claude/CLAUDE.md` first, then walks up from CWD for project-level CLAUDE.md files. Three reads and the agent knows the whole system.

## Open Questions

- Should repos-manifest.json move here from the toolbox?
- Should the global ~/.claude/CLAUDE.md be generated from config.json?
- How does this work with multiple machines? Is config.json the same on every machine?
- What's the minimum viable version? Just config.json + docs/?
- Where does the git repo boundary go? Is ~/wipcomputer/ a repo? Just LDMOS/? Neither?

## Resolved Questions

- **Name:** `~/wipcomputer/` (company name at root).
- **Structure:** Three top-level folders: `settings/`, `staff/`, `repos/`. Config and templates live in `settings/`.
- **Settings:** `settings/config.json` (identity), `settings/templates/` (org overrides), `settings/system-working-directories/` (macOS aliases to runtime dirs).
- **Template inheritance:** System defaults come from the LDM OS repo. Org overrides live in `settings/templates/`. Tools check org first, fall back to system.
- **Private dev guide:** Moves from repo ai/ folder to `settings/templates/dev-guide-private.md`. No more org-specific docs in repos. (Ticket #157)
- **Journals vs automated:** `staff/<agent>/documents/journals/` = human-forced. `staff/<agent>/documents/automated/` = system-generated human-readable.
- **LDMOS folder:** Was a subfolder, now trashed. System defaults come from the repo, not a deployed folder. `settings/` replaced it for org config.
- **repo-init template:** Lives in `settings/templates/repo-init/ai/`. It's a setting, not code.
