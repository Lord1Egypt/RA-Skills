# Plan: Universal Installer Toolbox + README Standard + Full Dogfood

**Date:** 2026-03-10
**Author:** cc-mini
**Source:** Parker's instructions + ai/notes/2026-03-10--cc-mini--readme-standard-and-universal-installer-vision.md
**Depends on:** v1.4.0 MCP unlock (done), LDM deployment rewrite (done, PR #43)

## Two problems

### 1. The universal installer doesn't handle toolboxes

The installer handles single repos. But wip-dev-tools is a toolbox: 7 sub-tools under `tools/`, 2 scripts under `scripts/`. Running `wip-install /path/to/wip-dev-tools-private` needs to walk all sub-tools and install each one to the correct interfaces (CLI, MCP, LDM extension, CC Hook, etc).

### 2. READMEs don't follow the standard

Every repo needs two documents:
- **README.md** ... human-facing, follows the standard pattern (see below)
- **TECHNICAL.md** ... developer-facing, all the architecture/source/build details

The README standard (from Parker, non-negotiable):

```
# Tool Name

Tagline. What it solves in human words. Not what it is technically.

## Teach Your AI to [verb]

Copy-paste prompt block. The AI reads the SKILL.md, explains itself,
asks if you want to install, runs the installer. That's onboarding.

## [Tool Name] Features

Human-readable feature list. Each feature has: name, plain description,
stability tag (Stable, Beta, etc). No technical jargon. No architecture
diagrams. No config references. Just what it does for you.

## More Info

- Technical Documentation ... link to TECHNICAL.md
- Other relevant docs ... links

## License
```

Rules:
- Tagline is NOT "a tool that does X". It's what it solves.
- "Teach Your AI" is the install section. User copies a prompt. AI reads SKILL.md, explains, asks questions, offers to install.
- Features are human-readable. Name, plain-English description, stability tag.
- "More Info" links to technical docs. Architecture, API, config, design decisions do NOT go in README.
- License at bottom. That's it. Nothing else.
- Reference implementation: https://github.com/wipcomputer/memory-crystal

## What's done (from previous plan)

- MCP servers added to 4 tools
- SKILL.md added to 3 tools that were missing them
- install.js rewritten with LDM deploy, MCP registration, registry (PR #43, merged)
- All 6 CLIs installed globally

## Steps

### Phase 1: Toolbox detection in detect.mjs [DONE]

Add `detectToolbox(repoPath)` that:
- Checks if `tools/` directory exists with sub-dirs containing `package.json`
- Returns list of sub-tool paths
- Falls back to single-repo mode if no `tools/` found

### Phase 2: Toolbox install mode in install.js [DONE]

Update `main()` to:
- Detect toolbox mode
- For each sub-tool: run the full install flow (CLI, MCP, LDM deploy, CC Hook, etc)
- Aggregate results across all sub-tools
- Single registry entry per sub-tool (not one for the whole toolbox)
- Fix: strip npm scope from names for `claude mcp add`
- Fix: correct arg order for `-e` flag
- Fix: add OPENCLAW_HOME env var to MCP registrations
- Fix: clean deploy (remove existing dirs before copy)
- Fix: only update .mcp.json if it already exists

### Phase 3: Reinstall wip-install [DONE]

- `npm install -g .` from `tools/wip-universal-installer/`
- Verified `wip-install --help` shows new LDM paths and toolbox mode

### Phase 4: Dogfood [DONE]

- Ran `wip-install /path/to/wip-dev-tools-private` (the toolbox itself)
- All 6 sub-tools installed to LDM, 4 MCP servers registered at user scope, registry populated
- Dry run shows all 6 sub-tools, 26 interfaces detected

### Phase 5: README standard for wip-dev-tools [DONE]

- Move current README.md to TECHNICAL.md (it's the developer docs)
- Write new README.md following the standard pattern
- Sections: tagline, Teach Your AI to Dev, Features, More Info, License
- Features: Universal Installer, Release Pipeline, License Detection, Repo Guard, File Guard, Repo Manifest, Private-to-Public Sync, Post-Merge Naming, Dev Guide

### Phase 6: PR + merge + deploy [IN PROGRESS]

- Add README changes to the existing PR branch (cc-mini/universal-installer-toolbox)
- PR to wip-dev-tools-private main
- Merge, deploy to public
- Rename branch with --merged convention

### Phase 7: Address scripts/ folder tools [DONE]

Moved deploy-public and post-merge-rename into `tools/` with package.json wrappers, shell scripts, and SKILL.md files. Dry run now detects 8 sub-tools, 30 interfaces.

### Phase 8: Update the note's "Current State" section [DONE]

Updated ai/notes/2026-03-10--cc-mini--readme-standard-and-universal-installer-vision.md to reflect all installed tools, MCP servers, registry, and README standard applied.

## Not in scope

- ldm-jobs: shell scripts, no package.json, no interfaces yet
- README formatter tool: noted for future, not building it now
- Applying README standard to other repos: wip-dev-tools first, others follow

## Success criteria

1. `wip-install /path/to/wip-dev-tools-private --dry-run` detects all 8 sub-tools and 30 interfaces
2. `wip-install /path/to/wip-dev-tools-private` installs everything, all MCP servers at user scope
3. README.md follows the standard pattern (tagline, Teach Your AI, Features, More Info, License)
4. TECHNICAL.md has all the developer/architecture content
5. PR merged, deployed to public repo
