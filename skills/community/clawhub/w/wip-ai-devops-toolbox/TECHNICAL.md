###### WIP Computer

# AI DevOps Toolbox

## Want your AI to dev? Here's the full system.

Your AI writes code. But does it know how to release it? Check license compliance? Sync private repos to public ones? Follow a real development process?

**AI DevOps Toolbox** is a collection of battle-tested tools for AI-assisted software development. Built by a team of humans and AIs shipping real software together.

Used internally to manage 100+ repos, 200+ releases, and daily license compliance across the [wipcomputer](https://github.com/wipcomputer) org. These tools run in production every day.

**Real-world example:** [wip-universal-installer](tools/wip-universal-installer/) ships its releases entirely through wip-release. 6 releases, v2.1.5, changelog and GitHub releases all generated automatically.

## Quick Start

```bash
# Install LDM OS (shared infrastructure for all your AI tools)
npm install -g @wipcomputer/wip-ldm-os
ldm init

# Preview what will be installed (12 tools, 39+ interfaces)
ldm install wipcomputer/wip-ai-devops-toolbox --dry-run

# Install everything
ldm install wipcomputer/wip-ai-devops-toolbox

# Verify
ldm doctor
```

## Tools

### Universal Installer (built into [LDM OS](https://github.com/wipcomputer/wip-ldm-os))

The Universal Interface specification for agent-native software. Defines how every tool ships six interfaces: CLI, importable module, MCP Server, OpenClaw Plugin, Skill, Claude Code Hook. The detection engine powers [`ldm install`](https://github.com/wipcomputer/wip-ldm-os).

```bash
# Detect what interfaces a repo supports
ldm install /path/to/repo --dry-run

# Install a tool from GitHub
ldm install wipcomputer/wip-file-guard

# Standalone fallback (bootstraps LDM OS if needed)
wip-install wipcomputer/wip-file-guard
```

**Source:** Pure JavaScript, no build step. [`tools/wip-universal-installer/detect.mjs`](tools/wip-universal-installer/detect.mjs) (detection), [`tools/wip-universal-installer/install.js`](tools/wip-universal-installer/install.js) (standalone installer). Zero dependencies. LDM OS deploy engine at [`lib/deploy.mjs`](https://github.com/wipcomputer/wip-ldm-os/blob/main/lib/deploy.mjs).

[README](tools/wip-universal-installer/README.md) ... [SKILL.md](tools/wip-universal-installer/SKILL.md) ... [Universal Interface Spec](tools/wip-universal-installer/SPEC.md) ... [Reference](tools/wip-universal-installer/REFERENCE.md)

### Dev Guide

Best practices for AI-assisted development teams. Covers release process, repo structure, the `ai/` folder convention, branch protection, private/public repo patterns, post-merge branch renaming, repo directory structure, Cloudflare Workers deploy guards, and more.

[Read the Dev Guide](DEV-GUIDE-GENERAL-PUBLIC.md)

### LDM Dev Tools.app

macOS automation wrapper. A native `.app` bundle that runs scheduled jobs (backup, branch protection audit, etc.) with Full Disk Access. One app to grant permissions to, one place to add new automation.

**Source:** Job scripts are plain shell. The app provides a Full Disk Access wrapper.

| Script | What it does | Source |
|--------|-------------|--------|
| `backup.sh` | Calls `~/.ldm/bin/ldm-backup.sh` (unified backup) | wip-ldm-os-private/scripts/ |
| [`branch-protect.sh`](tools/ldm-jobs/branch-protect.sh) | Audit and enforce branch protection across all org repos | tools/ldm-jobs/ |
| [`visibility-audit.sh`](tools/ldm-jobs/visibility-audit.sh) | Audit public repos for missing -private counterparts | tools/ldm-jobs/ |

The backup script is deployed by `ldm install` to `~/.ldm/bin/`. It backs up ~/.ldm/, ~/.openclaw/, ~/.claude/, and the workspace. See `how-backup-works.md` in the workspace docs.

```bash
# Run standalone
~/.ldm/bin/ldm-backup.sh                # or --dry-run to preview
bash tools/ldm-jobs/branch-protect.sh
bash tools/ldm-jobs/visibility-audit.sh

# Or via the app wrapper
open -W ~/Applications/LDMDevTools.app --args backup
open -W ~/Applications/LDMDevTools.app --args branch-protect
open -W ~/Applications/LDMDevTools.app --args visibility-audit
```

[README](tools/ldm-jobs/README.md)

**Setup:** Drag `LDMDevTools.app` into System Settings > Privacy & Security > Full Disk Access. Then schedule via cron:

```bash
# Daily backup at midnight, branch protection audit at 1 AM, visibility audit at 2 AM
0 0 * * * open -W ~/Applications/LDMDevTools.app --args backup >> ~/.ldm/logs/cron.log 2>&1
0 1 * * * open -W ~/Applications/LDMDevTools.app --args branch-protect >> ~/.ldm/logs/cron.log 2>&1
0 2 * * * open -W ~/Applications/LDMDevTools.app --args visibility-audit >> ~/.ldm/logs/cron.log 2>&1
```

Logs: `~/.ldm/logs/`

### wip-release

One-command release pipeline. Version bump, changelog, SKILL.md sync, npm publish, GitHub release, website skill publish. All in one shot.

```bash
wip-release patch                               # auto-detects RELEASE-NOTES-v{version}.md
wip-release minor --dry-run
wip-release major
```

**Release notes are mandatory.** Write `RELEASE-NOTES-v{version}.md` (dashes, not dots) on your feature branch. Commit it with the code. The PR diff shows both code and notes for review. On release, wip-release auto-detects the file.

**Quality gates (all run before release):**
- **Release notes:** Must come from a file (--notes flag removed). Three sources: RELEASE-NOTES file, ai/dev-updates/, or --notes-file. Blocks changelog-format entries ("fix: ...", "add: ..."). Must reference at least one GitHub issue (#XX).
- **Product docs:** Warns if roadmap, readme-first, or dev-updates are stale. Auto-updates version/date in `ai/product/plans-prds/roadmap.md` and `ai/product/readme-first-product.md` before commit.
- **Technical docs:** When source files (.mjs, .js, .ts) changed since last tag, checks that SKILL.md or TECHNICAL.md was also updated. Warns on patch, blocks on minor/major. Skip: `--skip-tech-docs-check`.
- **Interface coverage (toolbox repos):** Scans `tools/*/` for actual interfaces (CLI, Module, MCP, OC Plugin, Skill, CC Hook). Compares against README.md and SKILL.md coverage table. Reports: missing from table, detected but not marked, marked but not detected. Warns on patch, blocks on minor/major. Skip: `--skip-coverage-check`.
- **Stale branches:** Warns (patch) or blocks (minor/major) if merged branches exist on remote.
- **Worktree guard:** Blocks releases from linked worktrees. Must run from main working tree. Skip: `--skip-worktree-check`.
- **Dogfood cooldown:** Writes `.last-release` marker. Branch guard blocks `npm install -g` for 5 minutes.

**Post-release automation:**
- Post-merge branch rename (--merged-YYYY-MM-DD)
- Stale worktree prune from `_worktrees/`
- Skill publish to wip.computer/install/{name}.txt
- Product docs version sync

**All 7 CLIs support `--version` and `-v`.**

**Source:** Pure JavaScript, no build step. [`tools/wip-release/cli.js`](tools/wip-release/cli.js) (entry point), [`tools/wip-release/core.mjs`](tools/wip-release/core.mjs) (main logic), [`tools/wip-release/mcp-server.mjs`](tools/wip-release/mcp-server.mjs) (MCP server). Zero dependencies.

[README](tools/wip-release/README.md) ... [SKILL.md](tools/wip-release/SKILL.md) ... [Reference](tools/wip-release/REFERENCE.md)

### wip-license-hook

License rug-pull detection. Scans every dependency and fork for license changes. Pre-pull hook blocks merges if a license changed upstream. Pre-push hook alerts. Daily cron scan. Generates a public compliance dashboard.

```bash
wip-license-hook scan
wip-license-hook audit
```

**Source:** TypeScript. All source in [`tools/wip-license-hook/src/`](tools/wip-license-hook/src/):

| File | What it does |
|------|-------------|
| `src/cli/index.ts` | CLI entry point |
| `src/core/scanner.ts` | Dependency scanning (npm, pip, cargo, go, forks) |
| `src/core/detector.ts` | License text fingerprinting |
| `src/core/ledger.ts` | Ledger persistence and snapshots |
| `src/core/reporter.ts` | Reporting and dashboard HTML generation |

[README](tools/wip-license-hook/README.md) ... [SKILL.md](tools/wip-license-hook/SKILL.md)

### wip-repo-permissions-hook

Repo visibility guard. Blocks repos from going public without a `-private` counterpart. Works as a CLI, Claude Code hook, and OpenClaw plugin. Catches accidental exposure of internal plans, todos, and development context.

```bash
# Check a single repo
wip-repo-permissions check wipcomputer/memory-crystal
# -> OK: memory-crystal-private exists

# Audit all public repos in org
wip-repo-permissions audit wipcomputer
# -> Lists violations, exit code 1 if any found
```

**Source:** Pure JavaScript, no build step. [`tools/wip-repo-permissions-hook/core.mjs`](tools/wip-repo-permissions-hook/core.mjs) (logic), [`tools/wip-repo-permissions-hook/cli.js`](tools/wip-repo-permissions-hook/cli.js) (CLI), [`tools/wip-repo-permissions-hook/guard.mjs`](tools/wip-repo-permissions-hook/guard.mjs) (Claude Code hook). Zero dependencies.

[README](tools/wip-repo-permissions-hook/README.md) ... [SKILL.md](tools/wip-repo-permissions-hook/SKILL.md)

### post-merge-rename.sh

Post-merge branch renaming. Scans for merged branches that haven't been renamed, appends `--merged-YYYY-MM-DD` to preserve history. Runs automatically as part of `wip-release`, or standalone.

**Source:** Plain shell. [`scripts/post-merge-rename.sh`](scripts/post-merge-rename.sh)

```bash
bash scripts/post-merge-rename.sh              # scan + rename all
bash scripts/post-merge-rename.sh --dry-run     # preview only
bash scripts/post-merge-rename.sh <branch>      # rename specific branch
```

### wip-file-guard

Hook that blocks destructive edits to protected identity files. Works with Claude Code CLI and OpenClaw. Protects CLAUDE.md, SHARED-CONTEXT.md, SOUL.md, IDENTITY.md, MEMORY.md, and pattern-matched memory/journal files.

Two rules: block `Write` on protected files entirely, block `Edit` when removing more than 2 lines or replacing more than 4 lines.

```bash
# List protected files
wip-file-guard --list
```

**Source:** Pure JavaScript, no build step. [`tools/wip-file-guard/guard.mjs`](tools/wip-file-guard/guard.mjs) (single file, all logic). Zero dependencies.

[README](tools/wip-file-guard/README.md) ... [SKILL.md](tools/wip-file-guard/SKILL.md) ... [Reference](tools/wip-file-guard/REFERENCE.md)

### deploy-public.sh

Private-to-public repo sync. The full pipeline:

1. Rsyncs all files except `ai/` from private to public repo clone
2. Rewrites repository URL from private to public in package.json
3. Creates a branch, commits with co-authors, pushes, creates PR
4. Merges PR (--merge, never squash)
5. Creates matching GitHub release on public repo (pulls notes from private repo's release)
6. Publishes to npm from public repo clone
7. Publishes to GitHub Packages from public repo clone (uses `gh auth token`)
8. Cleans stale branches on public repo

```bash
bash scripts/deploy-public.sh /path/to/private-repo wipcomputer/public-repo
bash scripts/deploy-public.sh /path/to/private-repo wipcomputer/public-repo --dry-run
```

**Source:** Plain shell. [`scripts/deploy-public.sh`](scripts/deploy-public.sh) and [`tools/deploy-public/deploy-public.sh`](tools/deploy-public/deploy-public.sh)

### wip-repos

Repo manifest reconciler. Makes `repos-manifest.json` the single source of truth for repo organization. Like prettier for folder structure. Move folders around all day; on sync, everything snaps back to where the manifest says. Also generates cross-repo CLAUDE.md ecosystem sections.

```bash
# Check for drift
wip-repos check

# Sync filesystem to match manifest
wip-repos sync --dry-run

# Add a repo
wip-repos add ldm-os/utilities/my-tool --remote wipcomputer/my-tool

# Move a repo in the manifest
wip-repos move ldm-os/utilities/my-tool --to ldm-os/devops/my-tool

# Generate directory tree
wip-repos tree

# Generate cross-repo CLAUDE.md ecosystem sections
wip-repos claude                         # all repos
wip-repos claude my-repo                 # one repo
wip-repos claude --init                  # create CLAUDE.md for repos missing one
wip-repos claude --dry-run               # preview
```

**How `wip-repos claude` works:**

Agents can't read sibling repos at runtime. This command solves that by pre-generating cross-repo context into each repo's CLAUDE.md.

1. Reads all repos from `repos-manifest.json`
2. Extracts metadata from each: `package.json` (name, version, bin, exports), `SKILL.md` (interfaces), directory structure
3. For each repo, determines relevant siblings (same category + core repos)
4. Generates an `## Ecosystem` section between `<!-- wip-repos:start -->` / `<!-- wip-repos:end -->` delimiter comments
5. Hand-written CLAUDE.md content outside the delimiters is never touched

Templates at `templates/global-claude-md.md` (for `~/.claude/CLAUDE.md`) and `templates/repo-claude-md.template` (for per-repo starter).

**Source:** Pure JavaScript, no build step. [`tools/wip-repos/core.mjs`](tools/wip-repos/core.mjs) (manifest logic), [`tools/wip-repos/claude.mjs`](tools/wip-repos/claude.mjs) (ecosystem generator), [`tools/wip-repos/cli.mjs`](tools/wip-repos/cli.mjs) (CLI). Zero dependencies.

[README](tools/wip-repos/README.md)

### wip-repo-init

Scaffold the standard `ai/` directory in any repo. Plans, notes, ideas, dev updates, todos. One command.

New repo: creates the full structure. Existing repo: moves old `ai/` contents to `ai/_sort/ai_old/` so you can sort at your own pace. Nothing is deleted.

```bash
wip-repo-init /path/to/repo              # scaffold ai/ in a repo
wip-repo-init /path/to/repo --dry-run    # preview without changes
```

**Source:** Pure JavaScript, no build step. [`tools/wip-repo-init/init.mjs`](tools/wip-repo-init/init.mjs). Zero dependencies.

[README](tools/wip-repo-init/README.md) ... [SKILL.md](tools/wip-repo-init/SKILL.md)

### wip-readme-format

Generate or validate READMEs that follow the WIP Computer standard. Badges, title, tagline, "Teach Your AI" block, features, interface coverage table, license.

```bash
wip-readme-format /path/to/repo              # generate section files
wip-readme-format /path/to/repo --deploy     # assemble into final README
wip-readme-format /path/to/repo --dry-run    # preview without writing
```

**Source:** Pure JavaScript, no build step. [`tools/wip-readme-format/format.mjs`](tools/wip-readme-format/format.mjs). Zero dependencies. Reads templates from `ai/wip-templates/readme/`.

[README](tools/wip-readme-format/README.md) ... [SKILL.md](tools/wip-readme-format/SKILL.md)

### wip-license-guard

License enforcement for your own repos. Checks copyright, dual-license (MIT+AGPL), CLA, README license section. Toolbox-aware: checks every sub-tool. Interactive first-run setup. Auto-fix mode repairs issues.

```bash
wip-license-guard check                  # audit current repo
wip-license-guard check --fix            # audit and auto-fix
wip-license-guard init --from-standard   # apply WIP Computer defaults
wip-license-guard readme-license         # audit/fix license blocks across all repos
```

**Claude Code Hook:** Also wired as a PreToolUse hook (`guard.mjs`). On `ldm install`, registers in `~/.claude/settings.json`. Blocks `git commit` and `git push` when license compliance fails. Only checks repos with `.license-guard.json`. Repos without config silently pass.

**Source:** Pure JavaScript, no build step. [`tools/wip-license-guard/cli.mjs`](tools/wip-license-guard/cli.mjs) (CLI), [`tools/wip-license-guard/core.mjs`](tools/wip-license-guard/core.mjs) (logic), [`tools/wip-license-guard/guard.mjs`](tools/wip-license-guard/guard.mjs) (CC hook). Zero dependencies.

[README](tools/wip-license-guard/README.md) ... [SKILL.md](tools/wip-license-guard/SKILL.md)

### wip-branch-guard

Blocks all writes on main branch. The enforcement layer for required worktrees. PreToolUse hook that catches Write, Edit, and destructive Bash commands. Resolves the repo from the file path, not the CWD. If a file is outside any git repo (e.g. `~/.claude/plans/`), the guard allows edits immediately. Only protects files within git repos.

**Features:**
- **Workflow teaching:** Error messages include the full 8-step dev process (worktree, branch, commit, push, PR, merge, wip-release, deploy-public). Agents learn the workflow from the error, not just that they're blocked.
- **Worktree path warning:** Warns when `git worktree add` creates outside `_worktrees/`. Suggests `ldm worktree add`.
- **Dogfood cooldown:** After `wip-release`, blocks `npm install -g` for 5 minutes. Forces dogfooding via the install prompt.
- **Worktree requirement on branches:** On any non-main branch, edits blocked if not inside a worktree. Separate error message directs agents to create a worktree properly.
- **Dangerous flag blocking:** `--no-verify` and `git push --force` blocked on any branch.
- **Shared state allowlist:** CLAUDE.md, SHARED-CONTEXT.md, daily logs, `~/.ldm/logs/` always writable on main.
- **Non-repo passthrough:** Files outside any git repo allowed immediately.

```bash
wip-branch-guard --check       # report current branch status
```

**Source:** Pure JavaScript, no build step. [`tools/wip-branch-guard/guard.mjs`](tools/wip-branch-guard/guard.mjs). Zero dependencies.

## Source Code

All implementation source is committed in this repo. No closed binaries, no mystery boxes.

| Tool | Language | Source location | Build step? |
|------|----------|----------------|-------------|
| Dev Guide | Markdown | `DEV-GUIDE-GENERAL-PUBLIC.md` | None. |
| LDM Dev Tools jobs | Shell | `tools/ldm-jobs/backup.sh`, `branch-protect.sh`, `visibility-audit.sh` | None. Runnable standalone or via `.app` wrapper. |
| wip-release | JavaScript (ESM) | `tools/wip-release/cli.js`, `core.mjs`, `mcp-server.mjs` | None. What you see is what runs. |
| wip-license-hook | TypeScript | `tools/wip-license-hook/src/**/*.ts`, `mcp-server.mjs` | `cd tools/wip-license-hook && npm install && npm run build` |
| wip-license-guard | JavaScript (ESM) | `tools/wip-license-guard/cli.mjs`, `core.mjs`, `guard.mjs` | None. What you see is what runs. |
| wip-repo-permissions-hook | JavaScript (ESM) | `tools/wip-repo-permissions-hook/core.mjs`, `cli.js`, `guard.mjs`, `mcp-server.mjs` | None. What you see is what runs. |
| post-merge-rename.sh | Shell | `scripts/post-merge-rename.sh` | None. |
| wip-file-guard | JavaScript (ESM) | `tools/wip-file-guard/guard.mjs` | None. What you see is what runs. |
| wip-branch-guard | JavaScript (ESM) | `tools/wip-branch-guard/guard.mjs` | None. What you see is what runs. |
| wip-universal-installer | JavaScript (ESM) | `tools/wip-universal-installer/detect.mjs`, `install.js` | None. What you see is what runs. |
| deploy-public.sh | Shell | `scripts/deploy-public.sh` | None. |
| wip-repos | JavaScript (ESM) | `tools/wip-repos/core.mjs`, `cli.mjs`, `mcp-server.mjs`, `claude.mjs` | None. What you see is what runs. |
| wip-repo-init | JavaScript (ESM) | `tools/wip-repo-init/init.mjs` | None. What you see is what runs. |
| wip-readme-format | JavaScript (ESM) | `tools/wip-readme-format/format.mjs` | None. What you see is what runs. |

Previously standalone tools (wip-release, wip-license-hook, wip-file-guard, wip-universal-installer) were merged here. The standalone repos redirect to this one.

### Private/Public Repo Pattern

Development happens in private repos (with `ai/` folders for internal notes, plans, dev updates). When publishing, `deploy-public.sh` syncs everything except `ai/` to the public repo. Source files are always committed. Compiled output (`dist/`) is gitignored and only published to npm.

## Development

### wip-license-hook (TypeScript)

```bash
cd tools/wip-license-hook
npm install
npm run build          # compiles src/ -> dist/
node dist/cli/index.js scan   # test locally
```

### wip-release (JavaScript)

No build step needed. Edit `cli.js` or `core.mjs` and test directly:

```bash
cd tools/wip-release
node cli.js --dry-run patch --notes="test"
```

## Install

Tell your AI:

```
Read wip.computer/install/wip-ai-devops-toolbox.txt

Then explain what these tools do and help me set them up.
```

Or install via LDM OS:

```bash
npm install -g @wipcomputer/wip-ldm-os
ldm init
ldm install wipcomputer/wip-ai-devops-toolbox --dry-run
ldm install wipcomputer/wip-ai-devops-toolbox
ldm doctor
```

Or install the root package directly:

```bash
npm install -g @wipcomputer/wip-ai-devops-toolbox
```

Or install individual tools:

```bash
npm install -g @wipcomputer/wip-release
npm install -g @wipcomputer/wip-license-hook
npm install -g @wipcomputer/wip-file-guard
npm install -g @wipcomputer/wip-repos
```

## License

Dual-license model designed to keep tools free while preventing commercial resellers.

```
MIT      All CLI tools, MCP servers, skills, and hooks (use anywhere, no restrictions).
AGPLv3   Commercial redistribution, marketplace listings, or bundling into paid services.
```

Built by Parker Todd Brooks, Lēsa (OpenClaw, Claude Opus 4.6), Claude Code (Claude Opus 4.6).
