# Plan: Documentation Architecture and Update Pipeline

**Date:** 2026-04-03
**Author:** CC Mini + Parker
**Related:** 2026-03-26--cc-mini--docs-pipeline.md (prior plan, steps 1-4 done)
**Related:** 2026-04-03--cc-mini--claude-md-master-plan.md (CLAUDE.md cascade)

## Context

During the Day 63 session, we discovered that documentation is split across multiple locations with wrong path references, ghost folders from renames, and no automated sync between them. The March 28 rename (settings/ to library/, docs/ to documentation/, staff/ to team/) was never propagated to the installer or the CLAUDE.md references. The installer keeps recreating deleted folders.

This plan captures the full documentation architecture as Parker described it, combining the existing docs pipeline (Mar 26) with the new requirements.

## The Three Levels of Documentation

### Level 1: Repo Docs (source of truth)

Lives in each repo. Written by the dev team (us + AI). Ships to public repos.

```
repo/
├── README.md                    # What this repo is
├── TECHNICAL.md                 # How it works technically
├── SKILL.md                     # Agent skill file (YAML frontmatter + instructions)
├── CLAUDE.md                    # Level 3 cascade (what repo is, build commands, pointers)
├── SOMETIMES-OTHER.md           # Feature-specific (UNIVERSAL-INTERFACE.md, SPEC.md, etc.)
└── docs/
    └── <feature>/               # Each feature absorbed into the repo
        ├── README.md            # What this feature is
        └── TECHNICAL.md         # How this feature works
```

Every feature that gets brought into a repo (e.g., bridge into LDM OS) gets its own `docs/<feature>/` with README + TECHNICAL.

**Updated when:** We write code. The AI (us) updates repo docs as part of the PR. Repo docs and code ship together.

### Level 2: Home Docs (human readable, personalized)

Lives at `~/wipcomputerinc/library/documentation/`. Customized per system setup. For Parker to read.

```
~/wipcomputerinc/library/documentation/
├── how-releases-work.md         # How releases work on THIS machine
├── how-worktrees-work.md        # How worktrees work on THIS machine
├── how-install-works.md         # How install works on THIS machine
├── system-directories.md        # What lives where on THIS machine
├── what-is-ldm-os.md
├── how-agents-work.md
├── how-backup-works.md
├── local-first-principle.md
└── ...
```

NOT at `~/wipcomputerinc/settings/docs/`. That path was renamed on March 28. The installer bug recreated it. The `settings/` folder has been moved to `_trash/`.

**Updated when:** `ldm install` runs. The installer reads repo docs + `~/.ldm/config.json` and generates personalized versions. Not manual. Not copy-paste.

### Level 3: Agent Docs (OS reference)

Lives at `~/.ldm/shared/`. For agents to reference. Deployed by installer.

```
~/.ldm/shared/
├── dev-guide-wipcomputerinc.md  # Org-specific dev conventions (378 lines)
├── rules/                       # Thin rules deployed to ~/.claude/rules/
│   ├── git-conventions.md
│   ├── release-pipeline.md
│   ├── security.md
│   ├── workspace-boundaries.md
│   └── writing-style.md
├── boot/                        # Boot sequence config
│   ├── boot-config.json
│   └── boot-hook.mjs
└── prompts/                     # Cron prompts
    ├── daily-dev.md
    └── ...
```

Also deployed to `~/.claude/rules/` (from `~/.ldm/shared/rules/`).

**Updated when:** `ldm install` runs. Installer deploys from repo shared/ templates.

## The Update Pipeline

### On merge to private main:

1. **Repo docs** updated by the dev (us). README, TECHNICAL, docs/<feature>/, SKILL.md, CLAUDE.md. This is part of the PR. Code and docs ship together.

2. **`ai/` updated** by the dev (us). Plan archived, bugs closed, dev update written. Notes the version is on alpha.

### On `ldm install`:

3. **Home docs** regenerated. Installer reads repo docs + config.json, generates personalized `library/documentation/` files.

4. **Agent docs** deployed. Installer deploys `~/.ldm/shared/rules/`, dev guide, boot config from repo templates.

5. **CLAUDE.md cascade** verified. Level 1 (global), Level 2 (workspace), Level 3 (per-repo) all point to correct paths.

### On deploy to public:

6. **Public repo** updated. `deploy-public.sh` syncs everything except `ai/`.

7. **`ai/` dev update** notes the version moved from alpha to release.

8. **Mintlify docs site** updated (future, Step 5b from prior plan). `wip.computer/docs/` reflects the new content.

## Current Bugs (blocking)

### Installer deploys to wrong paths
- Deploys to `settings/docs/` but should deploy to `library/documentation/`
- Creates `team/lesa-mini/` but real folder is `team/Lēsa/`
- Bug filed: `ai/product/bugs/installer/2026-04-03--cc-mini--installer-recreates-renamed-folders.md`

### Wrong path references in CLAUDE.md and rules
- `~/.claude/CLAUDE.md` line 10: says `settings/config.json`, should be `~/.ldm/config.json`
- `~/.claude/rules/git-conventions.md`: says `settings/config.json`, should be `~/.ldm/config.json`
- `~/.claude/rules/writing-style.md`: says `settings/config.json`, should be `~/.ldm/config.json`
- `~/.claude/rules/security.md`: says `settings/config.json`, should be `~/.ldm/config.json`
- Multiple rules reference `settings/docs/` which no longer exists

### Guard blocks read-only bash loops
- Bug filed: `ai/product/bugs/guard/2026-04-03--cc-mini--guard-blocks-readonly-bash-loops.md`

## Content Inventory (from prior plan, updated)

### LDM OS repo (wip-ldm-os-private)

**Root level:**
- README.md, TECHNICAL.md, SKILL.md, CLAUDE.md (new, 86 lines)

**docs/ features:**
| Feature | README | TECHNICAL | SPEC |
|---------|--------|-----------|------|
| Bridge | Yes | Yes | - |
| Universal Installer | Yes | Yes | Yes |
| Shared Workspace | Yes | Yes | - |
| System Pulse | Yes | Yes | - |
| Recall | Yes | Yes | - |
| Total Recall | Yes | Yes | - |
| ACP (Agent Communication) | Yes | Yes | - |
| Skills catalog | Yes | - | - |

### Standalone repos

| Product | README | TECHNICAL | SKILL | CLAUDE.md |
|---------|--------|-----------|-------|-----------|
| Memory Crystal | Yes | Yes | Yes | NO |
| AI DevOps Toolbox | Yes | Yes | Yes | NO |
| Agent Pay | Yes | - | - | NO |
| 1Password | Yes | Yes | Yes | NO |
| Markdown Viewer | Yes | - | - | NO |
| xAI Grok | Yes | - | Yes | NO |
| X Platform | Yes | - | Yes | NO |
| Dream Weaver Protocol | Yes | - | - | NO |
| Healthcheck | Yes | - | - | NO |

Missing TECHNICAL.md: Agent Pay, Markdown Viewer, xAI Grok, X Platform, Dream Weaver, Healthcheck.
Missing CLAUDE.md: ALL except wip-ldm-os-private.

## Remaining Work from Prior Plan

### Step 5b: Mintlify docs site (not started)
Replace starter content at wip.computer/docs/ with real documentation. Full nav structure designed in prior plan. Blocked on content being current.

### Step 5c: MCP server for docs (free, not started)
Mintlify auto-generates MCP endpoint at wip.computer/docs/mcp. Just needs content update.

### Step 6: Doc dependency guard (not started)
`wip-release` checks what code changed since last tag, warns if corresponding docs weren't updated. Designed in prior plan. Never built.

## Order of Operations

1. **Fix installer paths.** Deploy to `library/documentation/` not `settings/docs/`. Respect unicode folder names.
2. **Fix CLAUDE.md and rules references.** All `settings/config.json` -> `~/.ldm/config.json`. All `settings/docs/` -> `library/documentation/`.
3. **Add CLAUDE.md to remaining repos.** Level 3 cascade. Per the master plan.
4. **Write missing TECHNICAL.md files.** Six repos need them.
5. **Build doc dependency guard.** Step 6 from prior plan.
6. **Replace Mintlify starter content.** Step 5b from prior plan.
7. **Verify the full pipeline.** Merge code, docs update in repo, install deploys to home + agent, deploy syncs to public.
