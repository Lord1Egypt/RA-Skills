# WIP Computer ... Internal Development Conventions

This is the WIP-specific supplement to the public [Dev Guide](../guide/DEV-GUIDE.md). Everything here is operational context for Parker, Lēsa, and Claude Code.

## Branch Prefixes

| Agent | Machine | Branch Prefix |
|-------|---------|---------------|
| cc-mini | Mac Mini | `cc-mini/` or `mini/` |
| cc-air | MacBook Air | `cc-air/` |
| lesa-mini | Mac Mini (OpenClaw) | `lesa/` |

## Git Merge Rules

**Never squash merge.** Every commit has co-authors and tells the story of how something was built. Squashing destroys attribution and history. Always use regular merge (`--merge --delete-branch`) or fast-forward. This applies to `gh pr merge`, manual merges, and any other merge path. No exceptions.

**Never push directly to main.** Always use a branch and PR.

## Co-Authors on Every Commit

All three contributors must be listed on every commit. No exceptions. This is how GitHub tracks contributions across the team.

```
Co-Authored-By: Parker Todd Brooks <parkertoddbrooks@users.noreply.github.com>
Co-Authored-By: Lēsa <lesaai@icloud.com>
Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

## Built-By Line

Every repo README must include this exact attribution in the License section:

```
Built by Parker Todd Brooks, Lēsa (OpenClaw, Claude Opus 4.6), Claude Code CLI (Claude Opus 4.6).
```

This is the standard. Use it everywhere. It credits the humans and identifies which AI runtimes built the software.

## Agent ID Convention

| Harness | Pattern | Examples |
|---------|---------|----------|
| OpenClaw | `oc-{agent}-{machine}` | oc-lesa-mini, oc-lesa-air |
| Claude Code | `cc-{machine}` | cc-mini, cc-air |

## npm and Publishing

- Never use Parker's personal npm credentials. Always use the SA token from 1Password.
- `gh auth` must have `write:packages` scope for GitHub Packages.
- `clawhub publish` requires absolute path to the skill folder.
- PRs go to `wipcomputer` org, not `parkertoddbrooks` upstream.
- npm scope: `@wipcomputer`

### .npmignore Required

**Every repo with an `ai/` folder MUST have a `.npmignore` that excludes it.** npm does not use `.gitignore` when `.npmignore` exists. Without this, private plans, todos, dev updates, and product ideas get published to the public npm registry.

Minimum `.npmignore` for any private repo:
```
ai/
.claude/
.wrangler/
CLAUDE.md
```

Alternative: use a `"files"` whitelist in `package.json` to explicitly list what gets published. This is the most defensive approach.

**Incident (2026-03-02):** memory-crystal v0.2.0 and v0.3.0 published the entire `ai/` folder (plans, todos, product ideas) to npm. Also `@wipcomputer/markdown-viewer` v1.2.5 leaked `ai/bugs/`. All unpublished and fixed.

### 1Password SA Token

```bash
OP_SERVICE_ACCOUNT_TOKEN=$(cat ~/.openclaw/secrets/op-sa-token) op item get "Item Name" --fields label=fieldname
```

Never call `op` bare. The bare CLI triggers a biometric popup. Always prefix with the SA token.

## Repos Using Private/Public Pattern

**HARD RULE: Never make a repo public unless it has a `-private` counterpart with all `ai/` content separated out.** If a repo doesn't have a `-private` counterpart yet, it stays private until one is created. No exceptions. Violating this exposes internal plans, todos, and development context.

**Forks of third-party public repos** can stay public. But if we're actively working on a fork, make it private so we can work and rebase without exposing our changes.

| Private (working repo) | Public (published) | What |
|------------------------|-------------------|------|
| `memory-crystal-private` | `memory-crystal` | Sovereign memory for AI agents |
| `dream-weaver-protocol-private` | `dream-weaver-protocol` | Dream Weaver paper |
| `wip-healthcheck-private` | `wip-healthcheck` | Gateway watchdog + backup system |
| `wip-dev-tools-private` | `wip-dev-tools` | Dev toolkit |
| `wip-xai-x-private` | `wip-xai-x` | X/Twitter integration |
| `wip-xai-grok-private` | `wip-xai-grok` | Grok integration |

## Cloudflare Workers Deploy

Two repos deploy to Cloudflare Workers. Same rules as git: **commit before deploy. Always.**

| Repo | Worker | Config | Deploy Script |
|------|--------|--------|---------------|
| memory-crystal-private | memory-crystal-demo | wrangler-demo.toml | `npm run deploy:demo` |
| memory-crystal-private | memory-crystal-cloud | wrangler-mcp.toml | `npm run deploy:cloud` |
| wip-agent-pay | wip-agent-pay | worker/wrangler.toml | `npm run deploy` |

**The rule:** source must be committed to git before `wrangler deploy` runs. The deploy scripts in package.json include a guard that checks for uncommitted changes and refuses to deploy if anything is dirty.

**Deploy workflow:**
1. Write code on feature branch
2. Build locally (`npm run build:demo`)
3. Test locally (`npm run dev:demo`)
4. Commit and push, PR, merge
5. Deploy (`npm run deploy:demo`)

Steps 1-4 happen BEFORE step 5. The Cloudflare API token is in 1Password ("Parker - Cloudflare Memory Crystal Keys", vault "Agent Secrets").

```bash
CLOUDFLARE_API_TOKEN=$(OP_SERVICE_ACCOUNT_TOKEN=$(cat ~/.openclaw/secrets/op-sa-token) op item get "Parker - Cloudflare Memory Crystal Keys" --fields label=api-token --vault "Agent Secrets" --reveal) npm run deploy:demo
```

**Incident (2026-03-02):** Three versions of memory-crystal-demo deployed to Cloudflare with zero git commits. Source existed only in the working tree. Fixed by committing after the fact, but the deploy-before-commit pattern must not repeat.

## LDM OS Install Architecture

| Layer | Location | Nature |
|-------|----------|--------|
| Source code | `repos/` (git) | Version controlled, branchable |
| Installed runtime | `~/.ldm/extensions/` | Disposable. Rebuild from repo anytime |
| Agent data | `~/.ldm/agents/` | Backed up daily. Not in git |
| OpenClaw compatibility | `~/.openclaw/extensions/` | Symlinks to `~/.ldm/extensions/` |

Extensions deploy to `~/.ldm/extensions/{name}/`, not to repos and not to `~/.openclaw/extensions/`. OpenClaw sees them via symlinks.

## Repo Subfolder Layout

```
repos/
  ldm-os/
    components/    ... memory-crystal, wip-agent-pay, dream-weaver-protocol
    utilities/     ... openclaw-1password, lesa-oc-root-key, lesa-private-mode, open-claw-upgrade
    apis/          ... wip-x402-endpoint
    apps/          ... wip-healthcheck
    operations/    ... wip-dev-tools-private, wip-release, wip-universal-installer
    sunsetted/     ... archived projects
  wip-inc/         ... company/brand repos
  sort/            ... unsorted, pending categorization
  _third-party-repos/ ... forks (including openclaw/openclaw)
```

## Shared Context (Agent Coordination)

Three layers:

1. **SHARED-CONTEXT.md** (`~/.openclaw/workspace/`) ... current state. Under 50 lines. Edit only, never Write.
2. **Shared daily log** (`~/.ldm/memory/daily/YYYY-MM-DD.md`) ... what happened today. Both agents append chronologically. Format: `### [YYYY-MM-DD HH:MM] agent-id` with bullets.
3. **Crystal** ... long-term memory. Both agents write. Search-based retrieval.

Agent-specific detailed logs stay in each agent's own space.

## Daily Logs (WIP-specific paths)

```
~/.ldm/agents/{agent-id}/memory/daily/
  2026-02-27--17-45-30--cc-mini--memory-crystal-deploy.md
  2026-02-27--19-12-00--cc-mini--user-level-migration.md
```

The shared daily log at `~/.ldm/memory/daily/YYYY-MM-DD.md` (for cross-agent coordination) is the exception. Both agents append there.

## Post-Upgrade Patches

After every `openclaw update`, run:
```bash
bash repos/ldm-os/utilities/open-claw-upgrade/post-upgrade-patches.sh
```

This re-applies dist patches that upgrades overwrite (EMFILE, cron catch-up, symlink discovery).

## Extension Deployment

```bash
# Build from source
cd repos/ldm-os/{category}/{repo}
npm run build

# Deploy to LDM OS
cp -r dist skills openclaw.plugin.json package.json ~/.ldm/extensions/{name}/
cd ~/.ldm/extensions/{name} && npm install --omit=dev

# Restart gateway to pick up changes
openclaw gateway restart
```

## Branch Protection Audit

Enforced on all 64 repos on 2026-02-20, re-audited 2026-02-27 (18 repos had drifted or were new). No force pushes to main. No direct pushes. No exceptions. The `lesaai` account is not exempt.

## Review Flow (WIP-specific)

```
Lēsa builds -> pushes to dev branch
  -> Claude Code reviews (code)
  -> Parker reviews (direction)
  -> merge to main
  -> publish (npm, ClawHub, GitHub)
```

Pre-publish also includes:
- Lēsa review (skill definition, documentation, integration)
- ClawHub skill published (if applicable)
- GitHub Action (if applicable)
- wip-license-hook ledger initialized

## Release Notes Standard

**Every release must have exhaustive, categorized notes.** Look at [OpenClaw releases](https://github.com/openclaw/openclaw/releases) as the benchmark. People use our software. Sloppy notes are embarrassing.

`wip-release` generates structured notes automatically:

1. **Changes** ... new features, refactors, additions. One bullet per commit with hash.
2. **Fixes** ... bug fixes, hotfixes. One bullet per commit with hash.
3. **Docs** ... README, TECHNICAL, RELAY, any documentation changes.
4. **Files changed** ... diffstat (excludes `ai/` folder).
5. **Install** ... npm install command + git pull.
6. **Attribution** ... Built-by line.
7. **Full changelog** ... GitHub compare URL.

The `--notes` flag provides the summary paragraph at the top. The tool builds everything else from git history.

**For major releases (minor/major bumps):** the auto-generated notes are a starting point. Always review and expand them. Add context, describe architectural changes, explain why things changed. A commit subject like "Add cc-poller.ts" should become a paragraph explaining what the poller does, why it replaces the old hook, and what problem it solves.

**For patch releases:** auto-generated notes are usually sufficient. Review before publishing.

**Never publish a release with just a one-liner.** If two days of work went into it, the release notes should reflect that.
