# Plan: wip-privatize + Template Unification + Full Pipeline

**Date:** 2026-03-27
**Author:** cc-mini (with Parker)
**Tickets:** #190, #225, #228, #239
**Save to:** wip-ldm-os-private/ai/product/plans-prds/current/

## Update: config-from-home.json merged into config.json (2026-03-29)

`config-from-home.json` has been merged into `config.json` as of PR cc-mini/merge-config. The installer (`ldm init`) now handles the one-time migration: if `config-from-home.json` exists at `~/.ldm/`, it merges it into `config.json` and renames it to `config-from-home.json.migrated`. All code that previously read from `settings/config.json` or `config-from-home.json` now reads from `~/.ldm/config.json`.

## Context

26 repos sit in `_to-privatize/` queues. The privatization workflow is 7 manual steps. We have tools (wip-repo-init, deploy-public.sh) but no orchestration. Parker wants a single command that connects everything:

- `settings/templates/` (source of truth for all scaffolding)
- `settings/docs/` (personalized docs deployed by ldm install)
- `settings/config.json` (org identity, agents, paths)
- `settings/config-dependencies.json` (what files need updating when things change)
- `settings/docs/change-dependencies.json` (what docs need updating when code changes)
- `docs.wip.computer` (public docs site via Mintlify)
- The 5 questions as gates on every release
- ALL repo docs (README.md, TECHNICAL.md, SKILL.md, CLAUDE.md)

This plan connects all of these into one flow.

## Relationship to v0.3.0 Master Plan

This plan is the INFRASTRUCTURE companion to the v0.3.0 product master plan at:
`/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/plans-prds/current/ldm-os-v030-master-plan.md`

The master plan is the PRODUCT roadmap (what LDM OS becomes): bridge absorption, agent register, message bus, update checker, ACP awareness, cloud relay.

This plan is the INFRASTRUCTURE roadmap (how the system manages itself): templates, docs, releases, quality gates, privatization, onboarding.

**Shipped from master plan (as of 2026-03-27):**
- Phase 1: Bridge absorption (done, bridge is in LDM OS core)
- Phase 2: Agent Register (done, session files + ldm sessions)
- Phase 3: Message Bus (done, file-based messaging)
- Phase 4: Update Checker (done, cron + boot notification)
- Phase 5: ACP-Client (research done, documented)
- Phase 6: Init + Doctor (partially done, this plan extends it)

**Not yet shipped from master plan:**
- Phase 7: Cloud Relay (encrypted ephemeral storage)

**Where they overlap:**
- Phase 6 (Init + Doctor): master plan adds session/message dirs. This plan extends init with template deployment, system repo creation, harness detection, working directories, onboarding (ldm setup).
- Doc standard: master plan says README.md + TECHNICAL.md. This plan extends with SKILL.md + references/ + CLAUDE.md per repo + settings/templates/ pipeline.

Don't merge these plans. They serve different audiences. Update the master plan when its next revision is due.

## Directory Structure (CURRENT, as of 2026-03-28)

### Workspace (user-facing)
```
~/wipcomputerinc/                          USER'S ORG HOME
  repos/                                   All code repos
  team/                                    People and agent documents
  operations/                              Org operations
  library/                                 System stuff (like macOS ~/Library/)
    documentation/                         Personalized system docs (14 files)
    system-directories/                    Finder aliases (harnesses, backups, ldm)
    _trash/
```

### LDM OS Runtime (system, managed by installer)
```
~/.ldm/                                    THE OS
  config.json                              LDM config (workspace, harnesses)
  config-from-home.json                    Org config (agents, paths, npm scope, co-authors)
  config-dependencies.json                 What files reference what paths
  change-dependencies.json                 What docs update when code changes
  doc-dependencies.json                    Crosslinks between docs
  shared/
    rules/                                 Instruction files deployed to harnesses
    boot/                                  Boot config
    prompts/                               Shared prompts
    dev-guide-wipcomputerinc.md            Org-specific dev conventions
  templates/                               All templates (.tmpl + rendered)
    repo-init/ai/...                       ai/ scaffold for new repos
    license/LICENSE.md                     License template
    license/CLA.md                         CLA template
    release-notes/release-notes.md         Release notes scaffold
    install-prompt/install-prompt.md       Install prompt template (var-driven)
    claude-md/                             CLAUDE.md level templates (placeholders)
    _trash/                                Trashed templates
  extensions/                              Installed skills and tools
  agents/                                  Agent identity + memory
  memory/                                  crystal.db (shared memory)
  bin/                                     Deployed scripts
  hooks/                                   Claude Code hooks
  state/                                   Runtime state
  templates/                               All templates
  logs/                                    All logs
  backups/                                 Local backups
  tmp/                                     Install staging
```

### Harness Directories (deployment targets)
```
~/.claude/                                 Claude Code harness
  CLAUDE.md, settings.json, .mcp.json      Config (tracked in git)
  rules/                                   Deployed from ~/.ldm/shared/rules/
  skills/                                  Deployed from ~/.ldm/extensions/ (not tracked)
  plans/                                   Active session plans (tracked in git)
  projects/                                Per-project memory (backed up daily)

~/.openclaw/                               OpenClaw harness
  CLAUDE.md, SYSTEM.md, openclaw.json      Config (tracked in git)
  workspace/                               Lesa's workspace
  extensions/                              Plugins (symlinked from ~/.ldm/extensions/)
```

### Path Migration (old -> new)

| Old path | New path | Status |
|----------|----------|--------|
| `~/wipcomputerinc/settings/` | DELETED | Replaced by library/ + ~/.ldm/ |
| `~/wipcomputerinc/settings/config.json` | `~/.ldm/config-from-home.json` | MOVED |
| `~/wipcomputerinc/settings/config-dependencies.json` | `~/.ldm/config-dependencies.json` | MOVED |
| `~/wipcomputerinc/settings/docs/` | `~/wipcomputerinc/library/documentation/` | MOVED |
| `~/wipcomputerinc/settings/docs/change-dependencies.json` | `~/.ldm/change-dependencies.json` | MOVED |
| `~/wipcomputerinc/settings/docs/doc-dependencies.json` | `~/.ldm/doc-dependencies.json` | MOVED |
| `~/wipcomputerinc/settings/templates/` | `~/.ldm/templates/` | MOVED |
| `~/wipcomputerinc/settings/templates/dev-guide-private.md` | `~/.ldm/shared/dev-guide-wipcomputerinc.md` | MOVED + RENAMED |
| `~/wipcomputerinc/settings/system-working-directories/` | `~/wipcomputerinc/library/system-directories/` | MOVED + RENAMED |

### Dev Guide References (FIX NOW)

Both dev guides must be referenced in ALL three CLAUDE.md files:

**Public dev guide:** `/Users/lesa/wipcomputerinc/repos/ldm-os/devops/wip-ai-devops-toolbox-private/DEV-GUIDE-GENERAL-PUBLIC.md`
**Private dev guide:** `/Users/lesa/.ldm/shared/dev-guide-wipcomputerinc.md`

Add to:
1. `~/.claude/CLAUDE.md` (global, read from everywhere)
2. `~/.openclaw/CLAUDE.md` (project, read from ~/.openclaw/)
3. Home folder CLAUDE.md if one exists

The private dev guide should be in the BOOT SEQUENCE (`~/.ldm/shared/boot/boot-config.json`). Read on every session start. 378 lines of org conventions is worth the tokens because NOT reading it causes cascading failures (proven 2026-03-26/27).

**Hook (ticket needed):** PreToolUse hook that fires before `git commit`, `git push`, `wip-release`, `gh pr create`. The hook forces the agent to confirm it has read the dev guide for this session. Not "read the file every time" but "have you read it this session? If not, read it now."

**Ticket:** #242 (filed) - Hook: force agent to read dev guide before git operations.

### CRITICAL: 27+ broken references to update

Files that reference the old `settings/` path and need updating:
- `~/.claude/CLAUDE.md` (1 reference)
- `~/.openclaw/CLAUDE.md` (1 reference)
- `~/.ldm/config-dependencies.json` (references old paths)
- `~/.ldm/change-dependencies.json` (references old paths)
- `~/.claude/plans/*.md` (86 references in active plan)
- `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/bin/ldm.js` (3 references, installer code)
- `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/shared/docs/*.tmpl` (template paths)
- `/Users/lesa/wipcomputerinc/repos/ldm-os/devops/wip-ai-devops-toolbox-private/ai/DEV-GUIDE-FOR-WIP-ONLY-PRIVATE.md` (pointer)
- `/Users/lesa/wipcomputerinc/repos/ldm-os/devops/wip-ai-devops-toolbox-private/DEV-GUIDE-GENERAL-PUBLIC.md` (dependency map)
- `/Users/lesa/.claude/projects/-Users-lesa--openclaw/memory/repo-locations.md` (auto-memory)
- `/Users/lesa/wipcomputerinc/library/documentation/*.md` (self-references)

ALL of these must be updated in one batch. Not piecemeal. One PR per repo that touches all references.

## The Full Pipeline

```
OS repo (source of truth)
  /Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/shared/templates/
      |
      v  ldm install deploys
~/.ldm/templates/                          Rendered templates on user's machine
      |
      v  tools read from here (wip-repo-init, wip-release, wip-privatize)
Each repo gets scaffolded files (LICENSE, ai/, CLAUDE.md, etc.)
      |
      v  wip-release publishes, deploy-public.sh syncs
Public repos
      |
      v  ldm install reads + deploys to harnesses
~/.claude/ and ~/.openclaw/                Rules, skills, config
      |
      v  wip-docs repo (when ready)
docs.wip.computer                          Public docs via Mintlify
```

## Template System Architecture

### Two-way flow

```
OS repo (source of truth)
  /Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/shared/templates/
      |
      v  ldm install (renders vars from config, deploys)
User's machine
  /Users/lesa/.ldm/templates/                 <- deployed templates (user can edit)
      |
      v  tools read from here (wip-repo-init, wip-release, wip-privatize)
Repos get scaffolded
      |
      v  ldm templates push (FUTURE)
User chooses: push to OS repo (everyone benefits) OR push to company repo (just my org)
```

One location: `~/.ldm/templates/`. No three-tier split. The installer deploys here. Tools read from here. User edits here. Checksum tracking detects user edits vs installer updates.

### V1: Seed + notify
- First `ldm install`: deploys templates to both locations
- Later `ldm install`: updates OS defaults at `~/.ldm/shared/templates/`. Does NOT touch user's copy at `settings/templates/`. Shows "2 new templates available" in status.
- `ldm templates update`: interactive. Shows new/changed templates. User picks what to adopt.
- User customizations at `settings/templates/` are never overwritten.

### Future: Two-way push
- `ldm templates push` diffs user's copy against OS defaults
- User chooses: "Push to WIP Computer (the OS)" or "Push to my company repo"
- Push to OS: creates PR on wipcomputer/wip-ldm-os-private. If merged, ships in next release. Every user gets it.
- Push to company: pushes to the company's own template/config repo. Only that org's installs get it.
- Self-aware: if a user fixes a bug in a template, the system notices the diff and suggests "This looks like a fix. Push it upstream?" No manual rebase needed. The system sees the delta and offers to contribute it back.
- This is the open source contribution model applied to AI infrastructure. Users customize. Improvements flow back to the OS. The OS gets better from usage.

### Template diff detection (at release time, in wip-release)

When `wip-release` runs on ANY repo, it scans that repo's `ai/` structure and compares it to `/Users/lesa/wipcomputerinc/settings/templates/repo-init/`. If the repo has folders or files in `ai/` that the template doesn't have:

```
wip-release patch
  ...
  Template diff detected:
    + ai/product/bugs/triage/          (not in template)
    + ai/product/org-updates/          (not in template)
  Add these to the OS template? [y/n]
  > y
  Updated: /Users/lesa/wipcomputerinc/settings/templates/repo-init/

  Push to installer? [y/n]
  > y
  Created PR on wipcomputer/wip-ldm-os-private: "Add triage/ and org-updates/ to repo-init template"
```

No per-repo hooks. No per-commit checks. One scan at release time, piggybacks on wip-release which already scans for release notes, product docs, and roadmap updates.

For external users (no private repo access):
- Same scan happens on their machine
- Instead of PR on private repo, it creates an issue on the PUBLIC repo (wipcomputer/wip-ldm-os)
- The issue includes the diff and a description of what they added
- Parker reviews and merges manually

### Company/org enforcement (future)
```json
// In settings/config.json
"templates": {
  "enforce": true,     // company mode: overwrite user templates on every install
  "source": "org"      // read from org config, not OS defaults
}
```
When enforce is true, the installer overwrites without asking. The company controls the templates.

## Cross-Harness Extension Deployment (ADDED 2026-03-30)

### The problem

Extensions and plugins are siloed by harness. wip-release, branch-guard, file-guard are Claude Code hooks and skills. Lesa can't use them. Private-mode, compaction-indicator, memory-crystal are OpenClaw plugins. Claude Code can't toggle private mode. When the bridge was fixed on Mar 30, the installer deployed to `~/.ldm/extensions/` but the MCP ran from `~/.openclaw/extensions/`. Three separate systems, no coordination.

### The principle

Each harness gets its own copy of every extension it can use. Not symlinks. Real copies. Because:
- iOS won't let you write to arbitrary paths
- macOS sandboxes apps
- A future agent on a VPS has its own filesystem
- You can't force all harnesses to read from one location
- Each harness should be self-contained and independently deployable

The installer is the glue. It knows what each harness needs and deploys copies to each one's expected location.

### How it should work

Every extension declares its interfaces in its package manifest:

```json
{
  "interfaces": {
    "cli": { "bin": "cli.mjs" },
    "mcp": { "server": "mcp-server.mjs" },
    "ocPlugin": { "entry": "dist/openclaw.js" },
    "ccHook": { "event": "PreToolUse", "command": "guard.mjs" },
    "skill": { "dir": "skills/" }
  }
}
```

When `ldm install` processes an extension:

1. **Detect interfaces** from the manifest (the universal installer already does this)
2. **For each detected harness on this machine:**
   - CLI: `npm install -g` (goes to `/opt/homebrew/bin/`)
   - MCP server: register with `claude mcp add` for Claude Code, deploy to `~/.openclaw/extensions/` for OpenClaw
   - OpenClaw plugin: deploy to `~/.openclaw/extensions/`
   - Claude Code hook: register in `~/.claude/settings.json`
   - Skill: deploy to `~/.claude/skills/` AND `~/.openclaw/skills/`
3. **Update the registry** at `~/.ldm/extensions/registry.json` with what was deployed where

### What this enables

- Lesa can run `wip-release` (deployed as OpenClaw skill, not just Claude Code skill)
- Claude Code can toggle private mode (exposed as MCP tool, not just OpenClaw plugin)
- Any new extension installed once is available in every harness
- Adding a new harness (Cursor, Codex, etc.) means adding a deploy target, not rewriting extensions

### Current state (as of 2026-03-30)

The universal installer detects interfaces and deploys to multiple targets. But it's inconsistent:
- Some extensions deploy to both `~/.ldm/extensions/` and `~/.openclaw/extensions/` (bridge, file-guard)
- Some only deploy to `~/.ldm/extensions/` and register as Claude Code MCP/hooks
- Skills deploy to both Claude Code and OpenClaw
- But OpenClaw plugins are NOT exposed to Claude Code as MCP tools
- And Claude Code hooks are NOT deployed as OpenClaw skills

### What needs to change

1. **Audit all extensions:** For each one, list which interfaces it has and which harnesses it's deployed to. Find the gaps.
2. **Universal deploy in the installer:** When an extension has an OpenClaw plugin interface, also register it as a Claude Code MCP server. When it has a Claude Code hook, also deploy it as an OpenClaw skill (where possible).
3. **Two-way bridge for plugin types that can't cross directly:** Some OpenClaw plugins (HTTP routes, hooks) can't be directly exposed to Claude Code. For those, create thin MCP wrappers that call the OpenClaw gateway.

### Relationship to Agent Skills Spec

See: `ai/product/plans-prds/current/skills/2026-03-25--cc-mini--adopt-agent-skills-spec.md`

The skills spec defines the FORMAT: every product ships `SKILL.md` (under 150 lines, pure instructions) + `references/` (context files). Cross-harness deployment defines the DISTRIBUTION: `ldm install` deploys skills to every harness (`~/.claude/skills/`, `~/.openclaw/skills/`, `~/.ldm/skills/`). Same architecture, two concerns.

The three-layer model (Source -> Runtime -> Home) from the skills spec maps directly:
- **Source**: `SKILL.md` + `references/` in the repo
- **Runtime**: deployed to `~/.ldm/skills/{product}/` by `ldm install`
- **Home**: deployed to each harness's skill directory

On iOS (future): App Intents expose the same skills as MCP tools. The skill format is the same. The delivery mechanism is different (App Intents instead of file deploy).

### Relationship to agent-to-agent communication

See: `ai/product/plans-prds/bridge/2026-03-30--cc-mini--bridge-messaging-architecture.md`

The bridge plan covers: file-based inbox (replacing broken in-memory queue), session targeting (multiple Claude Code sessions per agent), cross-agent messaging, and the relationship between the 18789 gateway, 18790 HTTP inbox, and tmux.

Key insight from Mar 30: Parker wants multiple Claude Code sessions running simultaneously. Same agent (cc-mini), same memory (crystal, daily logs), different conversations. A working session, a brainstorm session, a task session. Lesa targets which one she's talking to. Messages to the brainstorm don't interrupt the working session.

## Onboarding: ldm setup (guided first-run)

After `ldm install`, first-time users run `ldm setup`. The AI walks them through configuration:

1. Org name, GitHub org, npm scope -> `settings/config.json`
2. Team members, co-authors -> `settings/config.json`
3. License preference (MIT, AGPL, dual) -> `settings/config.json`
4. README footer ("Built by" line) -> `settings/config.json` under `branding`
5. Review templates (release notes, repo scaffold) -> show and customize `settings/templates/`
6. Connect 1Password (if applicable) -> `settings/config.json`

The LLM is the interface. No Mac app needed for V1. The setup skill reads settings/ and walks the user through conversationally.

`ldm setup` only runs once (or when user asks). After that, `ldm install` uses the config.

## What belongs where (UPDATED 2026-03-28)

| Thing | Where it lives | Why |
|-------|---------------|-----|
| Org name, co-authors, GitHub org | `~/.ldm/config-from-home.json` | Identity. Config value. Merges with config.json eventually. |
| README footer ("Built by") | Derived from `coAuthors` in `~/.ldm/config-from-home.json` | Generated from config, not hardcoded. |
| Tagline | `~/.ldm/config-from-home.json` under `tagline` | Config value. |
| README badges | Computed by `wip-readme-format` from detected interfaces | Generated output. Not config or template. |
| Release notes scaffold | `~/.ldm/templates/release-notes/` | Template. Scaffolded per release. |
| Repo init (ai/ structure) | `~/.ldm/templates/repo-init/` | Template. Scaffolded per repo. |
| CLAUDE.md levels | `~/.ldm/templates/claude-md/` | Template. Deployed to different locations. |
| LICENSE + CLA text | `~/.ldm/templates/license/` | Template. Scaffolded per repo. |
| Install prompt | `~/.ldm/templates/install-prompt/` | Template. Var-driven. Published to website. |
| Dev guide (private) | `~/.ldm/shared/dev-guide-wipcomputerinc.md` | Document. Read by agents. Not a template. |
| Personalized docs | `~/wipcomputerinc/library/documentation/` | Human-readable docs. Agents don't read from here. |
| System directory aliases | `~/wipcomputerinc/library/system-directories/` | Finder navigation. |
| Config dependencies | `~/.ldm/config-dependencies.json` | Tracks what files reference paths. |
| Change dependencies | `~/.ldm/change-dependencies.json` | Tracks what docs update when code changes. |
| Doc dependencies | `~/.ldm/doc-dependencies.json` | Tracks crosslinks between docs. |

**Rule:** `settings/templates/` is for things that get SCAFFOLDED into repos or DEPLOYED to the machine. Config values go in `settings/config.json`. Computed output is generated by tools. Documents that agents read are docs, not templates.

**_trash/ handling:** The installer (ldm install) and all tools IGNORE `_trash/` folders. Never read, never deploy, never scan. But the installer tracks what templates SHOULD exist. If a template is missing (user moved it to _trash/ or deleted it), the installer notices and asks: "Template X was removed. Restore from defaults?" It detects absence, not presence in trash.

**No placeholders in production.** All template files must have REAL content before the installer hooks up. The placeholder naming convention (`-placeholder`) was a design phase artifact. Before any of this ships:
1. Replace every placeholder with real content (from existing sources in the toolbox repo's `ai/wip-templates/` or from the hardcoded values in tool source code)
2. Rename files: drop `-placeholder` from all filenames
3. Settings/templates/ should look exactly like a fully installed system
4. The installer compares what's on your machine to what the OS ships. Same: skip. OS has new: "New template available." User customized: keep theirs.

**Cleanup:** Delete `/Users/lesa/wipcomputerinc/settings/templates/readme/` entirely.
- Badges: computed by wip-readme-format. Not a template.
- License block: moves to `/Users/lesa/wipcomputerinc/settings/templates/license/` (already has a placeholder there)
- "Built by" line: derived from `coAuthors` in `/Users/lesa/wipcomputerinc/settings/config.json`
- Tagline: add `"tagline": "WIP.computer. Learning Dreaming Machines."` to `/Users/lesa/wipcomputerinc/settings/config.json`

## System Repos + Working Directories

### System repos created by ldm install

Every important directory gets a git repo for version control. `ldm install` checks each one and creates it if missing.

| Directory | Repo naming | Created by | Status |
|-----------|------------|-----------|--------|
| `~/wipcomputerinc/` | `wipcomputer/wipcomputer-ldmos-{orgname}-home-private` | ldm install | EXISTS |
| `~/.ldm/` | `wipcomputer/wipcomputer-ldmos-{orgname}-system-private` | ldm install | EXISTS |
| `~/.openclaw/` | `wipcomputer/dot-openclaw` (kept as-is, harness created it) | OpenClaw harness | EXISTS |
| `~/.claude/` | `wipcomputer/wipcomputer-ldmos-{orgname}-dot-claude-private` | ldm install | **MISSING, needs creating** |

**Naming convention:**
- Repos WE create: `wipcomputer-ldmos-{orgname}-{purpose}-private`
- Repos the HARNESS created: keep their name. Don't rename what the harness made.

**`ldm install` behavior:**
1. For each detected harness, check: does the harness directory have a `.git/`?
2. If yes (like `.openclaw/`): leave it alone. The harness manages its own repo.
3. If no (like `.claude/`): create `wipcomputer-ldmos-{orgname}-dot-{harness}-private`, init, first commit.
4. For `~/.ldm/` and `~/wipcomputerinc/`: check they exist. If not, create during `ldm init`.

### System working directories

`/Users/lesa/wipcomputerinc/settings/system-working-directories/` is the Finder navigation map. Aliases (not symlinks) to every important directory.

```
system-working-directories/
  integrated--harnesses/         <- aliases to harness dirs
    .claude alias                -> ~/.claude/
    .openclaw alias              -> ~/.openclaw/
  ldmos-system/                  <- alias to the OS runtime
    .ldm alias                   -> ~/.ldm/
  ldmos-backup-location/
    local/                       <- alias to local backups (~/.ldm/backups/)
    off-site/                    <- alias to iCloud backups
  _trash/
```

**`ldm install` behavior:**
- For each detected harness, create a Finder alias in `integrated--harnesses/`
- Create `ldmos-system/` alias to `~/.ldm/`
- Create `ldmos-backup-location/` aliases to local and offsite backup paths

### How ldm install creates all of this (step by step)

During `ldm init` or `ldm install`, the installer runs these steps for system repos and working directories:

```
1. CHECK SYSTEM REPOS
   For each system directory (~/.ldm/, ~/wipcomputerinc/):
     - Does it have a .git/?
     - If no: create repo on GitHub (wipcomputer-ldmos-{orgname}-{purpose}-private)
     - git init, add remote, initial commit, push

2. CHECK HARNESS REPOS
   For each detected harness (~/.claude/, ~/.openclaw/, etc.):
     - Does it have a .git/?
     - If yes (harness created it): leave it alone
     - If no (like ~/.claude/): create repo (wipcomputer-ldmos-{orgname}-dot-{harness}-private)
     - git init, .gitignore, README, initial commit, push

3. CREATE WORKING DIRECTORIES STRUCTURE
   At ~/wipcomputerinc/settings/system-working-directories/:
     - integrated--harnesses/
       For each detected harness: create Finder alias -> harness directory
     - ldmos-system/
       Create Finder alias -> ~/.ldm/
     - ldmos-backup-location/
       local/ -> alias to ~/.ldm/backups/
       off-site/ -> alias to iCloud backup path (from config.json paths.icloudBackup)

4. UPDATE README
   At ~/wipcomputerinc/settings/system-working-directories/README.md:
     - List all aliases and what they point to
     - List all system repos and their GitHub URLs
```

**After deploying, ldm install commits to system repos.** Every file it deploys (templates, docs, LaunchAgents, rules, skills) gets committed to the appropriate system repo (~/.claude/, ~/.ldm/, ~/wipcomputerinc/). This way the git repos always reflect what's actually installed. No uncommitted drift.

```
ldm install
  + 14 docs deployed to settings/docs/
  + 18 templates deployed to settings/templates/
  + 1 LaunchAgent deployed
  + Committed to wipcomputerinc repo: "ldm install v0.4.59: templates, docs, LaunchAgents"
  + Committed to .claude repo: "ldm install v0.4.59: rules, skills, settings"
  + Committed to .ldm repo: "ldm install v0.4.59: extensions, shared, agents"
```

Finder alias creation uses osascript:
```bash
osascript -e 'tell application "Finder" to make alias file to POSIX file "/target" at POSIX file "/dest"'
```

Files to change: `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/bin/ldm.js` (cmdInit)

### Docs update (DONE)

Updated `/Users/lesa/wipcomputerinc/settings/docs/system-directories.md` with:
- System Repos table (all directories, their repos, who created them)
- Harness Comparison table (what's tracked where: LDM vs OpenClaw vs Claude Code)
- System Working Directories section (aliases structure)
- Naming convention for new repos

## Code quality + deploy quality (both required)

Our 5 questions are DEPLOY gates (what does the installer touch?). They don't cover CODE quality. gstack (https://github.com/garrytan/gstack) checks code quality: SQL safety, LLM trust boundaries, security (OWASP/STRIDE), conditional side effects, N+1 queries, adversarial multi-model review, design review (catches AI slop), test coverage.

We need both. The release pipeline should check:

**Code quality (gstack-style, during /review):**
- Security: SQL injection, LLM trust boundaries, OWASP
- Tests pass
- No AI slop in code or UI
- Adversarial review (second opinion)

**Deploy quality (our 5 questions, during wip-release):**
1. What source files changed?
2. What does ldm install deploy?
3. Fresh vs existing install?
4. What docs need updating?
5. What files does the installer touch?

**Product quality (our enforcement, during wip-release):**
- Roadmap updated
- Product bible updated
- Bug docs have issues + plans
- Release notes have the story

All three layers. Code, deploy, product. None optional.

### Existing research (already done, connect to this plan)

These files contain the full analysis. Don't redo this work:

- `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/product-ideas/gstack-integration.md`
  Full 1:1 mapping of gstack vs WIP skills. 13 NEW, 5 OVERLAP, 3 infrastructure.
  Architecture options: vendored wrappers (recommended), fork, or side-by-side.
  Biggest gaps: /office-hours, /plan-*-review, /review, /qa, /investigate, /retro, /document-release.
  Where our tools are better: wip-release, wip-file-guard, universal-installer, wip-repos, license compliance.

- `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/plans-prds/current/skills/2026-03-25--cc-mini--adopt-agent-skills-spec.md`
  SKILL.md format: < 150 lines, pure process, context in reference files.
  Our SKILL.md was 390 lines mixing pitch with instructions. Restructured to references/ pattern.

- `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/plans-prds/current/skills/ref--gstack-patterns.md`
  gstack architecture: template system, preamble, auto-generated from .tmpl files.
  Key insight: no product pitch in SKILL.md. Pure behavioral instruction.

- `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/plans-prds/current/skills/ref--agent-skills-spec.md`
  Agent Skills Spec (agentskills.io): frontmatter, body < 500 lines, progressive disclosure.

- `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/plans-prds/current/skills/ref--agentcard-analysis.md`
  AgentCard pattern: no pitch, when/when NOT to use, exact params, typical flow.

### How gstack connects to this plan

1. **wip-privatize** should suggest /office-hours before scaffolding (scope the product first)
2. **wip-release** should run gstack-style /review checks before publishing (code quality gate)
3. **Per-repo SKILL.md** follows the Agent Skills Spec (< 150 lines, references/ for context)
4. **Templates** for SKILL.md live at settings/templates/ (same pattern as everything else)
5. **Architecture decision:** Option A (vendored wrappers) is recommended. gstack installed as dependency, thin LDM OS wrappers add our context (boot sequence, memory crystal, workspace conventions).

Ticket: #(TBD) evaluate and integrate gstack skills into LDM OS.

## License Change: MIT + AGPLv3 -> Apache 2.0 + AGPLv3

**Decision:** Change permissive tier from MIT to Apache 2.0 for patent protection.

**NEEDS LEGAL REVIEW before executing.** Unsettled question: does old git history on public repos count as "distributed" under MIT? Can someone cherry-pick a pre-change commit and claim MIT license? As sole copyright holder, Parker can relicense going forward. But the retroactive question on public git history needs a lawyer.

**When ready to execute:**
1. Update template at `/Users/lesa/wipcomputerinc/settings/templates/license/LICENSE.md`
2. Update CLA if needed
3. Update every repo's LICENSE file (batch operation across all repos)
4. Update every repo's README license section
5. Update `wip-license-guard` and `wip-license-hook` (check for Apache headers, not MIT)
6. Update Dev Guide license section
7. Tag the change commit in every repo

**5 Questions for this change:**
1. Source: LICENSE.md and README.md in every repo + license template + license guard config
2. ldm install: deploys updated template. wip-repo-init scaffolds Apache. wip-license-guard validates Apache.
3. Fresh vs existing: fresh gets Apache. Existing repos need batch LICENSE update.
4. Docs: Dev Guide, settings/docs/, every repo README, docs.wip.computer license page
5. Files touched: every repo's LICENSE + README, template, guard config, hook config

## OS vs Apps Architecture

LDM OS is the operating system. Products are apps that run on it. Don't bundle apps into the OS.

**The OS (ships with LDM OS, free):**
- Boot sequence, agent identity, shared workspace
- Installer (ldm install), Bridge (communication), System Pulse (health), Recall (boot context)
- Templates, rules, docs, settings
- LUME

**Apps (install separately through the OS, independently priceable):**
- Memory Crystal (memory)
- Code / AI DevOps Toolkit (dev tools)
- 1Password integration
- xAI Grok, X Platform
- Markdown Viewer, Healthcheck
- Dream Weaver Protocol
- Third-party apps (via SKILL.md + ldm install)

**Each app has:**
- Its own SKILL.md (independently discoverable)
- Its own install prompt at wip.computer/install/{name}.txt
- Its own repo (public + private)
- Its own pricing (free, paid, subscription)
- "Part of the LDM OS ecosystem. Install via: ldm install {name}"

**LDM OS SKILL.md is the hub:**
- Lists available apps
- "Install all: ldm install --all" or "Install one: ldm install memory-crystal"
- Does NOT auto-install apps. The OS installs the OS. Apps install separately.

**For now:** ldm install installs everything (OS + all apps). This doesn't change. But the architecture keeps each app independent (own SKILL.md, own install prompt, own repo) so that when pricing or unbundling is needed, the structure is already there. Build for the future, ship for today.

**Install prompt template** at `/Users/lesa/wipcomputerinc/settings/templates/install-prompt/install-prompt.md`:

The template is fully variable-driven. wip-release reads it, fills in vars from config.json + repo package.json, publishes to the website.

Variables from two sources:

**Org config** (`/Users/lesa/wipcomputerinc/settings/config.json`):
| Variable | Field | Example |
|----------|-------|---------|
| `{{deploy.website}}` | deploy.website | "wip.computer" |
| `{{npmScope}}` | npmScope | "@wipcomputer" |
| `{{package-manager}}` | (default or config) | "npm" (future: bun) |

**App config** (each repo's package.json or .publish-skill.json):
| Variable | Field | Example |
|----------|-------|---------|
| `{{app-name}}` | displayName or SKILL.md name | "Memory Crystal" |
| `{{app-slug}}` | package.json name | "wip-memory-crystal" |
| `{{app-package}}` | package.json name | "wip-memory-crystal" |
| `{{not-ldmos}}` | computed: is this LDM OS? | true/false |

**Rendered template:**
```
# Install {{app-name}}

Open your AI and paste this:

---

Read https://{{deploy.website}}/install/{{app-slug}}.txt

Check if {{app-name}} is already installed. If it is, run ldm install --dry-run and show me what I have and what's new.

If not, walk me through setup and explain:

1. What is {{app-name}}?
{{#if not-ldmos}}
2. What is LDM OS?
{{/if}}
3. What does it install on my system?
4. What changes for us? (this AI)
5. What changes across all my AIs?

Then ask:
- Do you have questions?
- Want to see a dry run?

If I say yes: Install the CLI first ({{package-manager}} install -g {{npmScope}}/{{app-package}}) and then run ldm install --dry-run.

Show me exactly what will change. Don't install anything until I say "install".
```

Conditional: if app IS LDM OS, skip "What is LDM OS?" question (would be redundant).

**Hardcoded values that STAY hardcoded:**
- `ldm install` (it's the OS command, always the same)
- "Open your AI and paste this" (the user instruction, always the same)
- The 5 questions structure (standard across all apps)

Install paths:
- `ldm install` ... installs everything (OS + all apps)
- `ldm install {app-name}` ... installs one app through the OS
- `crystal init` ... legacy, kept for Memory Crystal only. New apps only use ldm install.
- Each app's SKILL.md at wip.computer/install/{app-slug}.txt describes that specific app
- LDM OS SKILL.md is the hub listing all available apps

The LDM OS and Memory Crystal examples in the template file are OUTPUT examples showing what the filled-in template looks like. They're not separate templates.

## Doc cascade (EVERY phase must update all three)

Every phase in this plan must update three places. No exceptions.

| Layer | Location | How it gets updated |
|-------|----------|-------------------|
| Repo docs | Each repo's README.md, TECHNICAL.md | Updated in the repo, deployed via deploy-public.sh |
| Settings docs | `/Users/lesa/wipcomputerinc/settings/docs/` | Templates at `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/shared/docs/` deployed by ldm install |
| Public docs site | `docs.wip.computer` via `/Users/lesa/wipcomputerinc/repos/wip-docs/` | Push to wip-docs repo, Mintlify auto-deploys |

**Specific docs that must update as we build this plan:**
- `/Users/lesa/wipcomputerinc/settings/docs/how-install-works.md` (template deployment, ldm setup, seed + notify)
- `/Users/lesa/wipcomputerinc/settings/docs/how-releases-work.md` (5-question gate, bug enforcement, roadmap/product-bible blocks)
- `/Users/lesa/wipcomputerinc/settings/docs/what-is-ldm-os.md` (new commands: ldm setup, ldm backup, ldm templates)
- `/Users/lesa/wipcomputerinc/settings/docs/system-directories.md` (settings/templates/ explained)
- `/Users/lesa/wipcomputerinc/repos/wip-docs/guides/how-install-works.mdx` (public version)
- `/Users/lesa/wipcomputerinc/repos/wip-docs/guides/how-releases-work.mdx` (public version)
- `/Users/lesa/wipcomputerinc/repos/wip-docs/ldm-os/commands.mdx` (new commands)

**The rule:** If a phase changes how something works, the settings/docs template gets updated in the same PR. Not later. Not "we'll do docs after." Same PR.

**Exception: docs.wip.computer updates happen LAST.** Parker is still organizing the public docs site. Don't push to `wipcomputer/wip-docs` until Parker says it's ready. Settings/docs and repo docs update immediately. Public site waits.

## What to build (in order)

### Phase 1: Template unification (#190)

**Problem:** Two template systems exist. `settings/templates/repo-init/` has 28 files. `wip-repo-init/templates/` has 9 files. They're not in sync.

**Fix:**
1. Make `settings/templates/` the single source of truth
2. Update `wip-repo-init` to read from `settings/templates/repo-init/` instead of its own `templates/` dir
3. Fall back to bundled templates if settings/templates/ doesn't exist (fresh install)

**Files to change:**
- `/Users/lesa/wipcomputerinc/repos/ldm-os/devops/wip-ai-devops-toolbox-private/tools/wip-repo-init/init.mjs` (read from settings/templates/)
- Delete or mark deprecated: `wip-repo-init/templates/` (replaced by settings/templates/repo-init/)

**5 Questions:**
1. Source: wip-repo-init/init.mjs
2. ldm install: deploys settings/templates/ to workspace (already working)
3. Fresh vs existing: fresh has no settings/templates/, tool falls back to bundled. Existing: reads from settings/templates/.
4. Docs: Dev Guide (document template source), settings/docs/how-install-works.md
5. Files touched: settings/templates/repo-init/ (source), wip-repo-init reads from there

### Phase 2: wip-privatize command

**New tool at:**
```
/Users/lesa/wipcomputerinc/repos/ldm-os/devops/wip-ai-devops-toolbox-private/tools/wip-privatize/
  cli.mjs       CLI entry point
  core.mjs      Core logic
  package.json
  SKILL.md      Skill definition
```

**What it does (one command):**
```bash
wip-privatize /path/to/repo              # full privatization
wip-privatize /path/to/repo --dry-run    # preview
```

Steps:
1. Validate: repo exists, has git remote, not already -private
2. Read org from settings/config.json
3. Rename on GitHub: `gh api repos/{org}/{name} -X PATCH -f name={name}-private`
4. Update local remote: `git remote set-url origin ...`
5. Rename local folder: `{name}` -> `{name}-private`
6. Create public mirror: `gh repo create {org}/{name} --public`
7. Scaffold ai/: run `wip-repo-init` (reads from settings/templates/repo-init/)
8. Generate CLAUDE.md: from settings/templates/claude-md/repo-claude-md template
9. Verify LICENSE: check against settings/templates/license/
10. Verify README: check structure against settings/templates/readme/
11. Commit scaffold
12. Move out of `_to-privatize/` into parent category folder
13. Update repos-manifest.json (via wip-repos)
14. First deploy-public.sh to populate public mirror
15. Print summary: what was done, what's next (release, docs update)

**5 Questions:**
1. Source: new tool at devops/wip-ai-devops-toolbox-private/tools/wip-privatize/
2. ldm install: deploys CLI + skill
3. Fresh vs existing: new tool, no migration
4. Docs: Dev Guide (replace manual steps with wip-privatize), docs.wip.computer (add wip-privatize page)
5. Files touched: /opt/homebrew/bin/wip-privatize, ~/.claude/skills/wip-privatize/, ~/.ldm/extensions/wip-privatize/

### Phase 2b: Bug workflow enforcement

**Problem:** Agents find bugs, sometimes write docs, sometimes file issues, sometimes neither. No enforcement. Bugs get noted in session transcripts and forgotten.

**Fix:** Three layers of enforcement.

**Layer 1: Template.** Update `/Users/lesa/wipcomputerinc/settings/templates/repo-init/ai /product/bugs/README.md` with:
- The full workflow (plan mode, write doc, file issue, connect them)
- Required sections in every bug doc
- A bug doc template with REQUIRED markers

Bug doc required sections:
```markdown
# Bug: <description>

**Date:** YYYY-MM-DD
**Filed by:** <agent-id>
**GitHub Issue:** <org>/<repo>#<number> <!-- REQUIRED -->
**Priority:** critical / high / medium / low

## What happened

## Root cause

## Fix plan

### 5 Questions
1. **Source files:**
2. **ldm install deploys:**
3. **Fresh vs existing:**
4. **Docs to update:**
5. **Files touched:**

## Files to change

## How to test

## Status
- [ ] Bug doc written
- [ ] GitHub issue filed
- [ ] Fix implemented
- [ ] Fix tested
- [ ] Fix released
- [ ] Bug doc moved to archive/
```

**Layer 2: wip-release gate.** When `wip-release` runs, scan `ai/product/bugs/` for:
- Bug docs without `GitHub Issue:` filled in -> BLOCK
- Bug docs with empty `Fix plan` section -> BLOCK ("Bug filed without a fix plan. The plan goes in the bug doc, not a separate file.")
- Bug docs with empty required sections -> WARN

**Layer 3: Stop hook (future).** When a session ends, check if any new files in `ai/product/bugs/` were created without a corresponding `gh issue create`. Warn the agent on next session boot.

**The workflow (what agents must do):**
1. Find a bug
2. Enter plan mode
3. Write bug doc at `ai/product/bugs/YYYY-MM-DD--<agent>--<description>.md`
4. File GitHub issue on the public repo (issues always on public repo)
5. Add the issue number to the bug doc's `GitHub Issue:` field
6. Add the bug doc path to the GitHub issue body
7. Fix the bug (following the plan in the doc)
8. Move bug doc to `ai/product/bugs/archive/` when fix ships

### Phase 2c: Fix repo-init template structure

**Problems found:**

| Issue | Fix |
|-------|-----|
| `archive-complete/` in docs, `archive/` in template | Standardize on `archive/`. Update docs. |
| `plans-prds/_sort/` documented but not scaffolded | Add the folder + README |
| `product/_trash/` documented but not scaffolded | Add the folder + README |
| `bugs/` not mentioned in `read-me-first.md` or `readme-first-product.md` | Add to both structure sections |
| `notes/feedback/` not mentioned in either README | Add to both structure sections |
| `todos/_trash/README 2.md` iCloud duplicate | Delete |
| Every folder should have a `_trash/` subfolder | Audit and add where missing |

**Files to update in `/Users/lesa/wipcomputerinc/settings/templates/repo-init/`:**

**1. `ai/read-me-first.md`** ... structure section must match actual template. Corrected structure:
```
ai/
  read-me-first.md
  _sort/
  _trash/
  dev-updates/
    product-updates/
    _trash/
  product/
    readme-first-product.md
    _trash/
    bugs/                               <- ADD (missing from current doc)
      archive/
      _trash/
    notes/
      feedback/                         <- ADD (missing from current doc)
      _trash/
    plans-prds/
      roadmap.md
      README.md
      _sort/                            <- ADD (missing from current template)
      _trash/
      upcoming/
      current/
      archive/                          <- FIX (was archive-complete/)
      todos/
    product-ideas/
      _trash/
```
Also update the table in "What's In Each Section" to include bugs/ and feedback/.

**2. `ai/product/readme-first-product.md`** ... fix "This Folder" section to match the same corrected structure above. Add bugs/ and feedback/ to the folder listing. Rename archive-complete/ to archive/.

**3. `ai/product/plans-prds/README.md`** ... update to mention `_sort/` and use `archive/` (not `archive-complete/`).

**4. `ai/product/plans-prds/roadmap.md`** ... no structural changes needed (content template is good).

**5. `ai/product/bugs/README.md`** ... full rewrite with bug workflow:
- The workflow (plan mode, write doc, file issue, connect)
- Required sections in every bug doc (Issue #, Root cause, Fix plan, 5 questions, Files to change, How to test)
- Bug doc template with REQUIRED markers
- How bugs connect to wip-release gates

**Folders to add:**
- `ai/product/_trash/README.md`
- `ai/product/plans-prds/_sort/README.md`
- Every subfolder that doesn't have `_trash/` gets one

**Delete:**
- `ai/product/plans-prds/todos/_trash/README 2.md`

### Phase 2d: Release notes template

**What it is:** `/Users/lesa/wipcomputerinc/settings/templates/release-notes/release-notes-placeholder.md` is the spec for what the release notes scaffold should look like.

**Current state:**
- Placeholder at settings/templates/ says "currently hardcoded"
- Actual template is HARDCODED in `/Users/lesa/wipcomputerinc/repos/ldm-os/devops/wip-ai-devops-toolbox-private/tools/wip-release/core.mjs` line 297 (`scaffoldReleaseNotes()`)
- `ldm install` doesn't deploy it. `wip-release` doesn't read it. Nothing connects them.

**What should happen:**

1. Source: real template lives in LDM OS repo at `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/shared/templates/release-notes/release-notes.md`
2. Install: `ldm install` deploys to `/Users/lesa/wipcomputerinc/settings/templates/release-notes/release-notes.md` (rename from placeholder)
3. Run: `wip-release` reads from `/Users/lesa/wipcomputerinc/settings/templates/release-notes/release-notes.md` instead of hardcoding. Falls back to bundled if settings/templates/ doesn't exist.
4. Update: user edits their copy at settings/templates/. OS updates show as "new template available" via `ldm templates update`.

**Template content must include:**
- Title with repo name + version (auto-filled by wip-release)
- One-line summary
- "The story" section (prose required, wip-release blocks if empty)
- Issues closed (auto-detected from git log)
- The 5 questions as required sections:
  1. What source files changed?
  2. What does ldm install deploy?
  3. Fresh vs existing install?
  4. What docs need updating?
  5. What files does the installer touch?
- How to verify

**Files to change:**
- `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/shared/templates/release-notes/release-notes.md` (NEW: the real template)
- `/Users/lesa/wipcomputerinc/repos/ldm-os/devops/wip-ai-devops-toolbox-private/tools/wip-release/core.mjs` (read from settings/templates/ instead of hardcoding)
- `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/bin/ldm.js` (deploy release-notes template in ldm install)
- Delete: `/Users/lesa/wipcomputerinc/settings/templates/release-notes/release-notes-placeholder.md` (replaced by real template)

**5 Questions for this change:**
1. Source: wip-ldm-os-private/shared/templates/release-notes/release-notes.md + wip-release/core.mjs
2. ldm install deploys: template to settings/templates/release-notes/
3. Fresh vs existing: fresh gets template. Existing: seed only, never overwrite.
4. Docs: Dev Guide (document that wip-release reads from settings/templates/), settings/docs/how-releases-work.md
5. Files touched: settings/templates/release-notes/release-notes.md, wip-release behavior changes

### Phase 2e: Hook up per-repo ai/ docs to the publish flow

**Problem:** Four files in every repo's ai/ folder should stay current:
1. `ai/read-me-first.md` ... the structure guide
2. `ai/product/readme-first-product.md` ... the product bible
3. `ai/product/plans-prds/roadmap.md` ... the roadmap
4. `ai/product/plans-prds/README.md` ... plans index

Right now these are scaffolded once by `wip-repo-init` and never touched again. They drift. The roadmap doesn't get updated when features ship. The product bible doesn't reflect what's built.

**When they should update:**

| File | When | How |
|------|------|-----|
| `roadmap.md` | Every PR merge + every release | wip-release already checks: "roadmap not updated since last release" and warns. Make this a BLOCK, not a warning. |
| `readme-first-product.md` | Every release | wip-release checks: "product bible not updated since last release." BLOCK. The "What's Built" and "What's Missing" sections must reflect the release. |
| `read-me-first.md` | Only when structure changes | Template diff at release time (Phase 2 template detection). If the OS template changed, warn: "read-me-first.md may need updating." |
| `plans-prds/README.md` | Only when structure changes | Same as read-me-first.md |

**Implementation in wip-release (`/Users/lesa/wipcomputerinc/repos/ldm-os/devops/wip-ai-devops-toolbox-private/tools/wip-release/core.mjs`):**

wip-release already has a "product docs check" that warns. Upgrade it:

```
Before publishing, check:
1. ai/product/plans-prds/roadmap.md ... modified since last tag? If not -> BLOCK
2. ai/product/readme-first-product.md ... modified since last tag? If not -> BLOCK
3. ai/product/bugs/ ... any bug docs without GitHub Issue field? -> BLOCK
4. ai/product/bugs/ ... any bug docs with empty Fix plan? -> BLOCK
5. RELEASE-NOTES ... has 5 questions answered? -> WARN (BLOCK later)
```

This means: you can't release without updating the roadmap and product bible. Period. Not a suggestion. A gate.

**PR checklist (already in Dev Guide, enforce via wip-release):**
The Dev Guide at `/Users/lesa/wipcomputerinc/repos/ldm-os/devops/wip-ai-devops-toolbox-private/DEV-GUIDE-GENERAL-PUBLIC.md` lines 623-649 already says every PR must update roadmap and readme-first. wip-release is the enforcement.

### Phase 3: Per-repo docs standard (#228)

After privatization, every repo needs:

| File | Source | Required |
|------|--------|----------|
| CLAUDE.md | settings/templates/claude-md/repo-claude-md | Yes |
| README.md | settings/templates/readme/ (badges + footer) | Yes |
| TECHNICAL.md | Written per repo | Yes |
| SKILL.md | Written per repo (if agent-facing) | If applicable |
| LICENSE | settings/templates/license/ | Yes |
| ai/ | settings/templates/repo-init/ | Yes |

wip-privatize scaffolds all of these. CLAUDE.md and LICENSE come from templates. README gets validated against the template. TECHNICAL.md and SKILL.md are flagged as "needs writing" in the summary.

**5 Questions:**
1. Source: each repo's own files
2. ldm install: doesn't deploy these (they're in git)
3. Fresh vs existing: no difference
4. Docs: docs.wip.computer (every repo's README + TECHNICAL feeds the docs site)
5. Files touched: CLAUDE.md, README.md, TECHNICAL.md, SKILL.md, LICENSE, ai/ in each repo

### Phase 4: docs.wip.computer sync

After repos are privatized and documented, the public docs site needs updating.

**Current state:** 40 pages on docs.wip.computer (wip-docs repo). Content was bulk-generated from repo READMEs. Needs to be kept in sync.

**Future state:** When a repo's README or TECHNICAL changes, the corresponding page in wip-docs should update. This is manual for now. The change-dependencies.json maps it:

```json
"README.md (any repo)": ["public repo README (via deploy-public.sh)"]
```

But there's no mapping from public repo -> wip-docs page. That's a gap.

**Add to change-dependencies.json:**
```json
"<repo>/README.md": ["wip-docs/<section>/<page>.mdx"],
"<repo>/TECHNICAL.md": ["wip-docs/<section>/<page>.mdx"]
```

**5 Questions:**
1. Source: wip-docs repo (wipcomputer/wip-docs)
2. ldm install: doesn't deploy (Mintlify auto-deploys from GitHub)
3. Fresh vs existing: no difference
4. Docs: the docs site IS the docs
5. Files touched: wip-docs/*.mdx

### Phase 5: 5-question gates in wip-release (#239)

**What:** wip-release checks RELEASE-NOTES for the 5 questions. If missing, release is blocked.

**Implementation:** In `wip-ai-devops-toolbox-private/tools/wip-release/core.mjs`, after finding the RELEASE-NOTES file, scan for the 5 headings or keywords:
- "source files" or "what changed"
- "ldm install" or "deploy"
- "fresh" or "existing"
- "docs" or "documentation"
- "files touched" or "installer"

If fewer than 3 are found, print a WARNING (not blocking yet). If fewer than 1, BLOCK.

Gradual enforcement: warn first, block later once the team is used to it.

**5 Questions:**
1. Source: wip-release/core.mjs
2. ldm install: deploys CLI (wip-release is part of toolbox)
3. Fresh vs existing: no difference
4. Docs: Dev Guide (document the gate), RELEASE-NOTES template (add 5 questions as sections)
5. Files touched: /opt/homebrew/bin/wip-release

## Test: openclaw-tavily is the first run

```bash
# Phase 1 already done (templates exist)

# Phase 2: privatize tavily
wip-privatize /Users/lesa/wipcomputerinc/repos/ldm-os/utilities/_to-privatize/openclaw-tavily --dry-run
wip-privatize /Users/lesa/wipcomputerinc/repos/ldm-os/utilities/_to-privatize/openclaw-tavily

# Verify:
gh repo view wipcomputer/openclaw-tavily-private  # private, with ai/
gh repo view wipcomputer/openclaw-tavily           # public mirror, no ai/
ls .../utilities/openclaw-tavily-private/ai/       # scaffold exists
ls .../utilities/openclaw-tavily-private/CLAUDE.md # from template

# Then: bump version, release, deploy
cd .../utilities/openclaw-tavily-private
# bump package.json 1.0.0 -> 1.0.2
wip-release patch
deploy-public.sh ... wipcomputer/openclaw-tavily

# Verify installer:
ldm install --dry-run  # tavily should NOT show as update available

# Then: second repo to confirm repeatable
wip-privatize /Users/lesa/wipcomputerinc/repos/ldm-os/utilities/_to-privatize/wip-healthcheck
```

## The 26 repos in _to-privatize (batch after tavily works)

```
utilities/_to-privatize/ (10): imessage-reply-context, imessage-rich, lesa-voice-call,
  md-to-x, openclaw-tavily, security-audit-skill, wip-healthcheck, wip-obsidian,
  wip-understand-video

components/_to-privatize/ (8): agent-identity-builder, cc-session-export,
  fading-heartbeat, lesa-agreements, lesa-openclaw-context-embeddings,
  voice-training-plugin, wip-enterprise-agents, wip-total-recall

apps/_to-privatize/ (6): wip-exec-brief, wip-field-notes-papers, wip-ldm-scrapbook,
  wip-scrapbook, wip-todo, x-bookmarks-reviewer

devops/_to-privatize/ (1): wip-heartbeat
apis/_to-privatize/ (1): wip-music-api
```

## Files to create/modify

### New files
| File | What |
|------|------|
| `devops/.../tools/wip-privatize/cli.mjs` | CLI entry point |
| `devops/.../tools/wip-privatize/core.mjs` | Core logic |
| `devops/.../tools/wip-privatize/package.json` | Package config |
| `devops/.../tools/wip-privatize/SKILL.md` | Skill definition |

### Modified files
| File | What |
|------|------|
| `devops/.../tools/wip-repo-init/init.mjs` | Read from settings/templates/ (#190) |
| `devops/.../tools/wip-release/core.mjs` | 5-question gate (#239) |
| `devops/.../DEV-GUIDE-GENERAL-PUBLIC.md` | Add wip-privatize, document template source |
| `wip-ldm-os-private/catalog.json` | Update tavily repo field |
| `settings/docs/change-dependencies.json` | Add repo -> wip-docs mappings |
| `settings/templates/release-notes/release-notes-placeholder.md` | Add 5 questions as sections |
| `wipcomputer/wip-docs` | Add wip-privatize page to docs.wip.computer |
