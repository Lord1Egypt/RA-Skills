# Plan: Repo-Based Install ... The Participation Layer

## Context

LDM OS currently treats install like npm: download, deploy, discard the source. The user gets binaries and extensions but never sees the code, the history, or the ai/ folder.

Parker's insight: these aren't repos for the human. These are the AGENTS' repos. When an agent runs `ldm install memory-crystal`, that clone becomes the agent's working copy. The agent reads the code, finds bugs, fixes them, submits PRs. The human reviews and merges. The fix flows back to everyone.

This transforms LDM OS from a package manager into a recursive contribution loop:

```
install -> use -> find bugs -> fix -> PR -> merge -> release -> update -> repeat
```

Every LDM OS installation becomes a development node. Every agent becomes a potential contributor.

## Architecture

### New directory: ~/.ldm/repos/

```
~/.ldm/repos/
  wipcomputer/
    memory-crystal/           <- cloned from public repo
      ai/                     <- scaffolded on install (wip-repo-init)
        products/
          bugs/               <- agent writes bug reports here
          plans-prds/
            current/
            upcoming/
        dev-updates/          <- agent writes dev updates here
        notes/
      src/
      dist/
      package.json
      .git/                   <- remote origin: wipcomputer/memory-crystal
    wip-ai-devops-toolbox/
      ai/                     <- same scaffold
      tools/
      ...
```

### The private/public inversion

Parker's system today:
- `memory-crystal-private` (private repo, has ai/, plans, bugs)
- `memory-crystal` (public repo, clean, no ai/)

User's system after install:
- `~/.ldm/repos/wipcomputer/memory-crystal/` (cloned from public)
- LDM auto-scaffolds the ai/ folder
- It becomes the user's private working copy OF the public repo
- Their ai/ folder is theirs. Their bugs, their plans, their notes.
- Code changes they make can PR back to the public repo

The public repo is the upstream. The local clone is the user's private fork. No GitHub fork needed unless they want to push.

### Install flow (replaces /tmp/ clone)

```
ldm install memory-crystal

1. Resolve via catalog -> wipcomputer/memory-crystal
2. Clone to ~/.ldm/repos/wipcomputer/memory-crystal/
   - If already exists: git pull instead of re-clone
   - Use gh repo clone (respects auth, handles SSH/HTTPS)
3. Scaffold ai/ folder if missing
   - Run wip-repo-init logic (template copy, no-overwrite)
   - .gitignore ai/ so it doesn't conflict with upstream pulls
4. Build if needed (npm run build)
5. Install interfaces from local clone
   - CLI: npm install -g @scope/pkg (from registry, not local)
   - Extensions: copy dist/ to ~/.ldm/extensions/
   - MCP: register via claude mcp add
   - Hooks: update ~/.claude/settings.json
6. Update registry.json with localPath field
```

### Update flow

```
ldm update (or ldm install bare)

For each repo in ~/.ldm/repos/:
1. Check for local changes (git status)
   - If dirty: stash, pull, unstash (or warn and skip)
2. git pull origin main
3. Rebuild if needed
4. Reinstall interfaces
5. Report what changed
```

### Bug submission

```
ldm bug memory-crystal "trashReleaseNotes crashes on untracked files"

1. Creates ~/.ldm/repos/wipcomputer/memory-crystal/ai/products/bugs/YYYY-MM-DD--description.md
2. Opens issue on upstream: gh issue create --repo wipcomputer/memory-crystal
3. Links the local file to the issue number
4. Agent can later fix the bug in the local clone and submit a PR
```

### Contribution flow

```
ldm contribute memory-crystal

1. Detect changes: git diff (code changes, ai/ changes)
2. Create branch: cc-mini/fix-description (or user-configured prefix)
3. Commit changes with co-authors
4. If no fork exists and user wants to push:
   - gh repo fork --remote-only (creates fork on GitHub, no re-clone)
   - Push to fork
5. Open PR: gh pr create (auto-routes fork -> upstream)
6. Report: "PR #42 opened on wipcomputer/memory-crystal"
```

### Change detection (the recursive awareness)

```
ldm status

Local repos: 3
  memory-crystal    clean     (v0.7.26, up to date)
  wip-ai-devops     modified  (2 files changed in tools/wip-release/)
  wip-xai-grok      behind    (v1.0.2, v1.0.3 available)

Suggestions:
  wip-ai-devops: You have local changes. Run: ldm contribute wip-ai-devops
  wip-xai-grok:  Update available. Run: ldm update wip-xai-grok
```

The system sees that the agent modified code in a public repo's clone. It doesn't just sit there. It says: "you should submit this."

## Implementation Phases

### Phase 1: Local repo home (foundation)
- Create ~/.ldm/repos/ structure
- Change clone target from /tmp/ to ~/.ldm/repos/{org}/{name}/
- Don't delete after install
- Update registry.json with localPath
- `ldm install` re-uses existing clone (git pull) instead of re-clone

### Phase 2: ai/ scaffold on install
- Run wip-repo-init logic after clone
- Add ai/ to .gitignore in the local clone (so git pull doesn't conflict)
- Agent can immediately write bugs, plans, dev-updates

### Phase 3: ldm bug
- New command: `ldm bug <component> "description"`
- Writes structured bug file to ai/products/bugs/
- Opens issue on upstream via gh issue create
- Links local file to issue number

### Phase 4: ldm contribute
- New command: `ldm contribute <component>`
- Detects local changes
- Creates branch, commits, forks if needed, opens PR
- Agent-native: the agent fixes the bug and submits

### Phase 5: Change detection in ldm status
- Scan ~/.ldm/repos/ for dirty repos
- Show suggestions: contribute, update, etc.
- The recursive awareness loop

## What already exists (reuse)

| Component | Location | Reuse for |
|-----------|----------|-----------|
| wip-repo-init | devops-toolbox tools/wip-repo-init/ | Phase 2: ai/ scaffold |
| catalog.json | wip-ldm-os-private/catalog.json | Phase 1: repo URL resolution |
| registry.json | ~/.ldm/extensions/registry.json | Phase 1: add localPath field |
| installFromPath() | lib/deploy.mjs | Phase 1: install from local clone |
| gh repo fork | GitHub CLI | Phase 4: fork for PR |
| gh pr create | GitHub CLI | Phase 4: submit PR |
| gh issue create | GitHub CLI | Phase 3: file bugs |
| deploy-public.sh | devops-toolbox scripts/ | Pattern reference for sync logic |

## Key design decisions

1. **Clone, not fork.** Fork only when contributing. Most agents just need the local copy.
2. **ai/ in .gitignore.** The user's ai/ folder is local-only. git pull never conflicts with it.
3. **npm for CLIs, local for extensions.** CLIs still come from npm registry (no /tmp/ symlinks). Extensions install from the local clone.
4. **Agents get branch prefixes.** cc-mini/ for CC, lesa-mini/ for Lesa. Same convention we use today.
5. **PRs over issues.** The bug file is documentation. The PR is the contribution. `ldm bug` files the issue. `ldm contribute` submits the fix.

## Files to modify

### Phase 1 (minimal)
| File | Change |
|------|--------|
| `bin/ldm.js` cmdInstall() | Clone to ~/.ldm/repos/ instead of /tmp/ |
| `bin/ldm.js` cmdInstallCatalog() | git pull existing repos instead of re-clone |
| `lib/deploy.mjs` | installFromPath accepts permanent repo path |
| `lib/state.mjs` | Add localPath to reconciliation |
| `catalog.json` | No change needed (repo URLs already there) |

### Phase 2
| File | Change |
|------|--------|
| `bin/ldm.js` | Add scaffold step after clone |
| Copy wip-repo-init templates into LDM OS | Or import from devops-toolbox |

### Phase 3-5
| File | Change |
|------|--------|
| `bin/ldm.js` | New commands: bug, contribute |
| `lib/contribute.mjs` | New file: git branch, commit, fork, PR logic |

## Verification

```bash
# Phase 1: repos persist
ldm install memory-crystal
ls ~/.ldm/repos/wipcomputer/memory-crystal/   # exists
ldm install   # bare: git pulls, doesn't re-clone

# Phase 2: ai/ scaffold
ls ~/.ldm/repos/wipcomputer/memory-crystal/ai/  # exists
cat .gitignore | grep ai/                        # ignored

# Phase 3: bug submission
ldm bug memory-crystal "test bug"
ls ~/.ldm/repos/wipcomputer/memory-crystal/ai/products/bugs/  # file exists
gh issue list --repo wipcomputer/memory-crystal                # issue created

# Phase 4: contribution
# (modify a file in the local clone)
ldm contribute memory-crystal
# PR opened on upstream

# Phase 5: awareness
ldm status
# Shows: "wip-ai-devops: modified (2 files). Run: ldm contribute"
```
