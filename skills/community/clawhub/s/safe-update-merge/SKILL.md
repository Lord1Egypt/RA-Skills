---
name: safe-merge-update
description: "Safely merge upstream OpenClaw updates without destroying plugin/skill injections, custom UI tabs, or workspace features. Two-phase: Phase 1 (automated) merges, builds, and restarts the gateway from a safe-merge branch — without touching local-desktop-main. Phase 2 (user-confirmed) promotes to local-desktop-main and pushes to the fork remote only after the user verifies the gateway is healthy."
metadata:
  openclaw:
    emoji: "🔄"
    requires:
      bins: ["git"]
      anyPkgMgr: ["npm", "pnpm"]
      optionalBins:
        - name: "claude"
          description: "Claude Code CLI — only required for --auto-resolve conflict resolution. Install: npm i -g @anthropic-ai/claude-code"
        - name: "python3"
          description: "Used by preflight.sh to write the JSON report. Available by default on most Linux/macOS systems."
        - name: "systemctl"
          description: "Used to restart the gateway after a successful merge (systemctl --user restart openclaw-gateway). Required only on systemd-based Linux hosts."
      env:
        - REPO_DIR
      optionalEnv:
        - name: ANTHROPIC_API_KEY
          description: "Required by the claude CLI for conflict resolution. May already be set in your shell environment or claude config (~/.claude/)."
        - name: UPSTREAM_REMOTE
          description: "Git remote name for openclaw/openclaw (default: upstream)"
        - name: TARGET_REMOTE
          description: "Git remote to push result to (default: myfork)"
        - name: TARGET_BRANCH
          description: "Branch to promote on success (default: local-desktop-main)"
        - name: PACKAGE_MGR
          description: "npm or pnpm — auto-detected from lockfile if unset"
      gitRemotes:
        - name: "upstream"
          description: "OpenClaw upstream repo (github.com/openclaw/openclaw)"
          envOverride: "UPSTREAM_REMOTE"
        - name: "myfork"
          description: "Your fork remote to push to"
          envOverride: "TARGET_REMOTE"
      gitBranches:
        - name: "local-desktop-main"
          description: "Branch to promote merged result to"
          envOverride: "TARGET_BRANCH"
---

# Safe Merge Update

Merges upstream OpenClaw changes into your fork while preserving all custom code:
plugin registrations, custom UI tabs, workspace skills, controllers, and state extensions.

## ⚠️ Operator Warnings — Read Before Running

This skill performs **high-impact, partially irreversible operations**. Understand what it does before executing in a production environment:

| Operation | Phase | Impact |
|-----------|-------|--------|
| `git merge upstream/main` | Phase 1 | Creates `safe-merge-YYYY-MM-DD` branch and merges — **no changes to `local-desktop-main`** |
| `npm run build` / `pnpm run build` | Phase 1 | Downloads packages if lockfile changed (network); builds in place |
| `systemctl --user restart openclaw-gateway` | Phase 1 | **Restarts the live gateway** — brief downtime; gateway now runs from safe-merge build |
| Conflict resolution via `claude` CLI | Phase 1 (optional) | Passes **redacted** file content to the Claude API; `Edit`+`Read` tools only — **`Bash` explicitly excluded** |
| `git push --force` to `TARGET_REMOTE/TARGET_BRANCH` | **Phase 2 only** (`--promote`) | **Overwrites remote branch** — only runs after user confirms gateway is healthy |
| `git branch -D safe-merge-*` | **Phase 2 only** (`--promote`) | Deletes temp branch after successful promotion |

### Prerequisites

Before running, verify:
- `git remote -v` shows **`upstream`** pointing to `github.com/openclaw/openclaw` (or set `UPSTREAM_REMOTE`)
- `git remote -v` shows **`myfork`** pointing to your fork (or set `TARGET_REMOTE`)  
- Branch **`local-desktop-main`** exists locally (or set `TARGET_BRANCH`)
- `claude` CLI is installed and authenticated (`claude --version`)
- `npm` or `pnpm` is available for builds
- You are OK with the gateway restarting automatically on success

### Conflict Resolution & Secret Redaction

When merge conflicts occur, the script:
1. Runs `scripts/redact-secrets.sh` on each conflicted file — replaces secrets with `[REDACTED_N]` placeholders, writes the redaction map to a per-file temp file in a mode-700 directory
2. Invokes the **`claude` CLI** with `--allowedTools Edit,Read` (no `Bash`) to resolve conflict markers in the redacted files — the model cannot execute shell commands
3. After claude exits, the script runs `git add -A && git commit --no-edit` itself
4. Restores secrets from the redaction map, then deletes the map files immediately

If you prefer manual resolution, skip claude entirely: fix conflicts yourself and run `--resume`.

### Flags

| Flag | Description |
|------|-------------|
| `--dry-run` | Fetch remotes, show divergence and estimated conflict count, then exit — **no changes made** |
| `--no-auto-resolve` | Stop on conflicts instead of invoking claude — leaves the safe-merge branch for manual resolution, then use `--resume` |
| `--resume <branch>` | Skip the merge; run build → restart on an existing safe-merge branch (use after manual conflict resolution) |
| `--promote <branch>` | **Phase 2** — run after user confirms the gateway is healthy. Force-pushes the safe-merge branch to `TARGET_REMOTE/TARGET_BRANCH`, switches local branch, deletes temp branch. This is the only step that modifies `local-desktop-main`. |

### All Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `REPO_DIR` | *(required)* | Path to your OpenClaw repository |
| `UPSTREAM_REMOTE` | `upstream` | Remote name for openclaw/openclaw |
| `UPSTREAM_BRANCH` | `main` | Branch to pull from upstream |
| `TARGET_REMOTE` | `myfork` | Remote to force-push result to |
| `TARGET_BRANCH` | `local-desktop-main` | Branch to promote on success |
| `LOCAL_BRANCH` | current branch | The branch being merged from (used by preflight.sh for divergence stats) |
| `PACKAGE_MGR` | auto-detect | `npm` or `pnpm` (auto-detected from lockfile) |

## How It Works

1. **Pre-flight**: Fetch upstream, compute divergence, detect conflicts
2. **AI Merge**: The agent resolves each conflict using the merge manifest as intent context
3. **Validate**: Build check, tab verification, protected pattern scan
4. **Report**: Announce results back to the requesting session

## Security & Privacy

### Model Usage
This skill uses the **`claude` CLI** (the Anthropic Claude Code CLI, not the OpenClaw agent model) for conflict resolution. The CLI must be installed separately and authenticated with an Anthropic API key in your environment. It is invoked with `--allowedTools Edit,Read` — the `Bash` tool is explicitly excluded, so the model can only read and edit files, not execute shell commands.

The model sees only the **redacted content** of conflicted files (see Secret Redaction below) — not the entire repository.

To control which Claude model is used, configure it in your `~/.claude/config.json` or set the model via claude CLI flags.

### Secret Redaction

Before any file content is sent to the claude CLI for conflict resolution, it passes through `scripts/redact-secrets.sh` which detects and replaces:
- API keys (OpenAI `sk-`, GitHub `ghp_`, Slack `xoxb-`, AWS `AKIA`, etc.)
- Bearer/Basic auth tokens
- Private keys (RSA, EC, OPENSSH)
- Connection strings with embedded passwords
- Config values for `password`, `secret`, `token`, `apiKey` fields

Detected secrets are replaced with `[REDACTED_N]` placeholders.

**How the map is stored:** `redact-secrets.sh` requires fd 3 to be open and writes the redaction map to whatever file fd 3 points to. In `safe-merge-update.sh`, fd 3 is wired to a per-file temp file inside a mode-700 temp directory (`mktemp -d`). So **the map is written to disk** — in a private, process-owned temp directory — and deleted immediately after secret restoration. It is never written to stdout, stderr, or any shared/world-readable path.

If your security policy requires no disk writes, mount the temp dir on a tmpfs:
```bash
REDACT_MAP_DIR=$(mktemp -d)
mount -t tmpfs -o size=1m,mode=700 tmpfs "$REDACT_MAP_DIR"
# ... run safe-merge-update.sh with REDACT_MAP_DIR set ...
umount "$REDACT_MAP_DIR" && rmdir "$REDACT_MAP_DIR"
```

**What is sent to the claude CLI:** Only the redacted content of conflicted files. Claude resolves conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) using only the `Edit` and `Read` tools — **`Bash` is not granted**, so the model cannot execute shell commands. The script itself runs `git add -A && git commit --no-edit` after claude finishes.

Backups in `/tmp/safe-merge/backups/` contain only **redacted content** — they are created after redaction and never contain plaintext secrets.

### What Gets Sent to the Model
- Only **conflicting file diffs** are sent (not the entire repository)
- All secrets are **redacted before transmission** (see above)
- The merge manifest describes file intents and protected patterns
- `.env` files are never included in merge prompts

### Build Execution
The validation phase runs `pnpm install --ignore-scripts`, `pnpm build`, and `pnpm ui:build` to verify the merge compiles.

**`pnpm install` will download packages from the npm registry.** This is network activity. `--ignore-scripts` is always passed to suppress `preinstall`/`postinstall` lifecycle hooks from running untrusted code.

**Before proceeding past pre-flight:**
- Review upstream `package.json` diffs in the pre-flight report
- Check for new dependencies you don't recognize before running install
- For maximum safety, run the full merge in an isolated environment (container, VM, or disposable clone)

**SKILL.md says "No Network Installs" — this refers to the skill package itself (no curl/wget/npm install in the skill's own setup). It does NOT mean the merge workflow avoids network; `git fetch upstream` and `pnpm install` both require network access.**

### Backups (Non-Negotiable)
Before ANY file edits, the skill creates a full backup of every conflicting file at `/tmp/safe-merge/backups/` preserving directory structure. **Backups are created after secret redaction** — they never contain plaintext secrets. If the merge goes wrong, restore from backups and re-run secret restoration.

### No Network Installs
This skill contains no install scripts that download from external URLs. All files are local to the skill package. The only network activity is `git fetch upstream` and your normal model API calls.

## Invocation

### Via UI
Click the **↑ Update** button in the topbar (right of Health pill).

### Via Chat
```
/update — or ask: "run a safe merge update"
```

## Architecture

### Fully Automated Pipeline (`scripts/safe-merge-update.sh`)

The primary entry point. Run this directly — it handles the entire workflow end-to-end:

```bash
cd /path/to/openclaw

# Safe first step — shows divergence, makes no changes
REPO_DIR=. ./scripts/safe-merge-update.sh --dry-run

# Phase 1 — merge, build, restart gateway from safe-merge branch
# local-desktop-main is NOT touched; no remote push yet
REPO_DIR=. ./scripts/safe-merge-update.sh

# Manual mode — stop on conflicts for review instead of invoking claude
REPO_DIR=. ./scripts/safe-merge-update.sh --no-auto-resolve

# Resume after fixing conflicts manually (still Phase 1)
REPO_DIR=. ./scripts/safe-merge-update.sh --resume safe-merge-2026-03-02

# Phase 2 — after verifying the gateway is healthy, promote to local-desktop-main
REPO_DIR=. ./scripts/safe-merge-update.sh --promote safe-merge-2026-03-02
```

**Two-phase design — `local-desktop-main` is never touched until the user confirms:**

**Phase 1 (automated):**
1. Checks you're on `local-desktop-main` with a clean working tree
2. `--dry-run`: fetches, shows upstream divergence + estimated conflict count, exits — no changes
3. `git fetch --all`
4. Prunes any stale `safe-merge-*` branches (prevents accumulation)
5. Creates `safe-merge-YYYY-MM-DD` branch
6. Runs `git merge upstream/main --no-edit`
7. **If conflicts** → redacts secrets (maps written to mode-700 temp dir via fd 3, deleted after restore), invokes `claude --allowedTools Edit,Read` (Bash excluded), restores secrets, runs `git commit` — use `--no-auto-resolve` to stop for manual review
8. `pnpm build` + `pnpm ui:build`
9. Restarts gateway from current working tree (safe-merge branch build)
10. **Exits with confirmation prompt** — `local-desktop-main` is unchanged, no remote push yet
11. On build failure: leaves safe-merge branch intact for investigation

**Phase 2 (user-confirmed via `--promote`):**
1. User verifies gateway is healthy
2. `git push myfork safe-merge-YYYY-MM-DD:local-desktop-main --force`
3. `git checkout local-desktop-main && git reset --hard safe-merge-YYYY-MM-DD`
4. `git branch -D safe-merge-YYYY-MM-DD`

**Rollback before confirming:** gateway restart reverts to previous build; `local-desktop-main` was never touched.

**Claude conflict resolution strategy (baked into the script):**
- local-desktop-main UI/vault/navigation customizations → prefer HEAD (ours)
- Upstream security and bug fixes → prefer incoming (theirs)
- Additive changes on both sides → keep both
- TypeScript type unions → union both sides
- Genuinely ambiguous → prefer HEAD

**Resume mode** — for cases where Claude's auto-resolution needs a manual touch:
```bash
# Fix conflicts manually, then:
./scripts/safe-merge-update.sh --resume safe-merge-2026-03-02
# Skips merge, runs build → push → cleanup
```

### Supporting Scripts (for advanced / manual use)
- `scripts/preflight.sh` — read-only analysis, produces JSON report at `/tmp/safe-merge/preflight-report.json`
- `scripts/validate.sh` — post-merge build + `mustPreserve` pattern checks
- `scripts/merge-agent-prompt.md` — prompt template for per-file conflict resolution (used when invoking Claude manually)
- `scripts/redact-secrets.sh` — secret detection and redaction before model transmission

### Branch Strategy
- **Working branch**: `local-desktop-main` (your fork's primary branch)
- **Temp merge branch**: `safe-merge-YYYY-MM-DD` (created and destroyed per run)
- **Upstream source**: `upstream/main` (`openclaw/openclaw` official repo)
- **Push target**: `myfork/local-desktop-main`
- Stale safe-merge branches are auto-pruned at the start of each run — no accumulation

## Phases

### Phase 1: Pre-flight (`scripts/preflight.sh`)

Run automatically when invoked. Produces a report at `/tmp/safe-merge/preflight-report.json`.

**What it does:**
- Fetches upstream (`git fetch upstream`)
- Computes commit divergence (ahead/behind counts)
- Lists conflicting files via `git merge-tree`
- Checks each conflict against the merge manifest for protection status
- Creates a temporary worktree for dry-run merge (avoids touching your working tree)

**Pre-flight report includes:**
- Divergence stats
- List of conflicting files with protection status
- Recommended strategy per file (keep-ours, ai-merge, accept-upstream)

**Environment variables:**
- `REPO_DIR` — Path to your OpenClaw repo (must be set explicitly)
- `UPSTREAM_REMOTE` — Upstream remote name (default: `upstream`)
- `UPSTREAM_BRANCH` — Upstream branch (default: `main`)

### Phase 2: Merge & Conflict Resolution

The agent performs the actual merge and resolves conflicts:

1. **Create merge branch** — `git checkout -b safe-merge-YYYY-MM-DD`
2. **Examine conflicts before merging** — read both our version and upstream's version of each conflicting file to understand what each side changed
3. **Run the merge** — `git merge upstream/main --no-commit --no-ff`
4. **For each conflicting file:**
   a. Read the conflict markers to understand the exact diff
   b. Check `MERGE_MANIFEST.json` for intent and strategy (`keep-ours`, `accept-upstream`, `ai-merge`)
   c. Resolve: write the clean merged file preserving our customizations + upstream improvements
   d. `git add` the resolved file
5. **Verify auto-merged protected files** — even files that auto-merge need checking: grep for `mustPreserve` patterns to confirm our custom code survived
6. **Secret redaction** (for complex conflicts requiring prompt-based resolution):
   - `scripts/redact-secrets.sh` replaces secrets with `[REDACTED_N]` placeholders
   - Redaction map is written to a per-file temp file in a mode-700 directory via fd 3; it is never written to stdout, stderr, or any shared path, and is deleted immediately after secret restoration
   - After resolution, restore secrets from map, then delete the temp directory

**Key principle:** Always examine both sides of a conflict BEFORE attempting resolution. Understanding what upstream changed and what we customized is essential for correct merges.

### Phase 3: Validation (`scripts/validate.sh`)

After all conflicts are resolved:
- `pnpm install --ignore-scripts` — install any new dependencies (lifecycle scripts suppressed)
- `pnpm build` — compile the gateway
- `pnpm ui:build` — compile the Control UI
- Protected pattern scan — verify `mustPreserve` patterns from the manifest still exist
- Tab verification — check that custom UI tabs are still registered

### Phase 4: Commit & Report

- Commits on the merge branch (`safe-merge-YYYY-MM-DD`) — never directly on `main`
- Commit message includes: upstream version, commit count, conflict resolution summary, file counts
- Reports to user: files resolved, strategies used, build status, any warnings
- User decides whether to merge the branch into `main` and push:
  ```bash
  git checkout main
  git merge safe-merge-YYYY-MM-DD
  git push origin main
  ```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `REPO_DIR` | *(required, declared in metadata)* | Path to your OpenClaw repository |
| `SAFE_MERGE_MODEL` | *(agent's current model)* | Model override for conflict resolution |
| `UPSTREAM_REMOTE` | `upstream` | Git remote name for upstream |
| `UPSTREAM_BRANCH` | `main` | Upstream branch to merge from |

### Merge Model Selection

The model used for AI conflict resolution can be configured in two ways:

1. **Via the UI modal** — The update modal includes a "Merge Model" dropdown that lists all available models (same catalog as Agents → Model Selection). The selection is persisted in `localStorage` under the key `openclaw-merge-model` and survives page reloads. When a model is selected and "Run Safe Merge" is clicked, the merge prompt includes `SAFE_MERGE_MODEL=<selected-model>`.

2. **Via environment variable** — Set `SAFE_MERGE_MODEL` before invoking the skill (e.g., in the agent's env config or inline).

If neither is set, the skill uses the agent's currently configured primary model.

The dropdown appears on both the initial "Check for Updates" screen and the results screen, so you can change it at any point before starting the merge.

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | This file — skill instructions |
| `MERGE_MANIFEST.json` | Protected files, intents, `mustPreserve` patterns |
| `scripts/preflight.sh` | Pre-flight analysis (read-only, no modifications) |
| `scripts/validate.sh` | Post-merge build and pattern validation |
| `scripts/merge-agent-prompt.md` | Prompt template for per-file conflict resolution |
| `scripts/redact-secrets.sh` | Secret detection and redaction before model transmission |
| `update-modal.ts` | Reference copy of the UI update modal component (source of truth: `ui/src/ui/views/update-modal.ts`) |
| `references/bg-sessions-backend.ts` | Reference: `src/gateway/server-methods/bg-sessions.ts` |
| `references/bg-sessions-controller.ts` | Reference: `ui/src/ui/controllers/bg-sessions.ts` |
| `references/bg-sessions-views.ts` | Reference: `ui/src/ui/views/bg-sessions.ts` |

## Background Sessions Panel

A right-side drawer panel that lets you **watch and talk to background/cron subagents** in real-time, without leaving the Control UI.

### How to Open
- **Click the updates badge** (e.g. "148 Updates") in the status bar — opens the update modal *and* slides in the background sessions panel simultaneously
- Can also be opened programmatically: `openBgSessionsPanel(client, state)`

### What It Shows
- **Session list dropdown** — all isolated/cron sessions, with 🟢 running / ⚪ idle indicator and a human-readable label extracted from the cron job name
- **Live transcript** — scrollable, role-colored messages:
  - 🟣 `You` (user injections)
  - 🟢 `Agent` (assistant responses)
  - 🟡 `→ tool` (tool calls with args)
  - ⚪ `← result` (tool results, truncated)
  - 🔴 `system` (compaction events)
- **Auto-refresh** — polls `bgSessions.history` every 3 seconds while panel is open
- **Send messages** — text area at the bottom; Enter sends, Shift+Enter newlines. Routes through `chat.send` RPC using the selected `sessionKey`

### Architecture

**Backend** (`src/gateway/server-methods/bg-sessions.ts`):
- `bgSessions.list` — reads `sessions.json` for the default agent, filters for isolated/cron session keys (UUID format: `agent:main:<uuid>`), returns label, updatedAt, running status (lock file presence)
- `bgSessions.history` — loads the `.jsonl` transcript file via `readSessionMessages()`, simplifies to `{ role, text, timestamp, toolName }` array
- `bgSessions.send` is intentionally omitted — the UI calls `chat.send` directly with the target `sessionKey`

**Controller** (`ui/src/ui/controllers/bg-sessions.ts`):
- `openBgSessionsPanel(client, state)` — sets panel open, fetches sessions, starts 3s poll
- `closeBgSessionsPanel(state)` — clears panel open flag, stops poll
- `loadBgSessions(client, state)` — fetches session list via RPC
- `loadBgSessionHistory(client, state, key)` — fetches transcript via RPC
- `selectBgSession(client, state, key)` — changes selected session, reloads history
- `sendBgMessage(client, state)` — calls `chat.send` RPC with session key + message, refreshes history
- `startBgSessionsPolling(client, state)` / `stopBgSessionsPolling()` — manage setInterval

**View** (`ui/src/ui/views/bg-sessions.ts`):
- `renderBgSessionsPanel(state, client)` — full Lit HTML panel, rendered as overlay in `app-render.ts`
- `bgSessionsPanelStyles` — exported CSS (for reference; styles are embedded in the view's html template)
- Panel is an overlay div (fixed inset-0, z-index 9000) with a right-anchored 520px panel; click outside to close

**State fields** (added to `AppViewState` and `OpenClawApp`):
```typescript
bgSessionsPanelOpen: boolean;
bgSessionsList: BgSession[] | null;
bgSessionsLoading: boolean;
bgSessionsSelectedKey: string | null;
bgSessionsHistory: BgMessage[] | null;
bgSessionsHistoryLoading: boolean;
bgSessionsInput: string;
bgSessionsSending: boolean;
```

### Wiring in app-render.ts
The panel is rendered as the last overlay before the closing `</div>`:
```typescript
${state.bgSessionsPanelOpen && state.client ? renderBgSessionsPanel(state, state.client) : nothing}
```

The update badge click handler also calls `openBgSessionsPanel`:
```typescript
@click=${() => {
  // ...existing update modal logic...
  if ((state as any).client) { openBgSessionsPanel((state as any).client, state as any); }
}}
```

### MERGE_MANIFEST.json — Add These Entries
When merging future upstream changes, protect these new files:
```json
"src/gateway/server-methods/bg-sessions.ts": {
  "intent": "New RPC handlers for background session listing and history (bgSessions.list, bgSessions.history)",
  "strategy": "keep-ours"
},
"ui/src/ui/controllers/bg-sessions.ts": {
  "intent": "Controller for the background sessions panel — load, poll, send, select",
  "strategy": "keep-ours"
},
"ui/src/ui/views/bg-sessions.ts": {
  "intent": "Right-side drawer panel for viewing/talking to cron subagents",
  "strategy": "keep-ours"
}
```

Also add these `mustPreserve` patterns to the relevant existing protected files:
- `ui/src/ui/app-render.ts`: `renderBgSessionsPanel`, `openBgSessionsPanel`, `bgSessionsPanelOpen`
- `ui/src/ui/app.ts`: `bgSessionsPanelOpen`, `bgSessionsList`, `bgSessionsSelectedKey`
- `ui/src/ui/app-view-state.ts`: `bgSessionsPanelOpen`, `bgSessionsList`

## UI Update Modal

Clicking the topbar update button (in **any** state) opens an update modal with a guided flow:

1. **Check for Updates** — asks the user to confirm, then calls `update.checkUpstream` RPC with `force: true` (bypasses cache)
2. **Status Result** — shows upstream divergence: commits behind, commits ahead, or "Up to date"
3. **Action Buttons** — "⚡ Run Safe Merge" (if behind) or "🔄 Run Merge Anyway" (if up to date) — both send the merge prompt to the chat session

The modal is rendered by `ui/src/ui/views/update-modal.ts` and uses state properties `updateModalState` (closed/confirm/checking/result), `upstreamDivergence`, and `mergeModel` on the app component. A reference copy of the modal source is kept at `skills/safe-merge-update/update-modal.ts`.

### Button States

- **N Updates** (accent-colored): Git upstream has N newer commits
- **Updates Available** (accent-colored): npm registry has a newer version (non-fork workflows)
- **✓ Up to Date** (muted pill, clickable): Up to date — click still opens the modal to re-check
- **Merging…** (spinner, disabled): Merge in progress

### How Update Detection Works

The gateway runs two parallel checks:

1. **npm registry** (`update-startup.ts`): Compares `VERSION` against npm latest. Used for standard installs.
2. **Git upstream** (`update.checkUpstream` RPC): Runs `git fetch upstream && git rev-list --count HEAD..upstream/main`. Used for fork workflows. Result is cached for 5 minutes.

For forks, the git check is authoritative — your local `package.json` version will often be ahead of npm (since you're building from source), so the npm check would incorrectly say "up to date."

## Post-Merge Checklist

After a successful merge, always:
1. Run `pnpm ui:build` — the Control UI is served from `dist/control-ui/`
2. **Update systemd service version** — the UI header reads `OPENCLAW_SERVICE_VERSION` from the service unit:
   ```bash
   NEW_VERSION=$(node -e "console.log(require('./package.json').version)")
   sed -i "s/OPENCLAW_SERVICE_VERSION=.*/OPENCLAW_SERVICE_VERSION=$NEW_VERSION/" ~/.config/systemd/user/openclaw-gateway.service
   systemctl --user daemon-reload
   ```
3. Run `openclaw gateway restart` — pick up the new build
4. Check config schema compatibility — upstream may add `.strict()` to schemas
5. Clean up backups: `rm -rf /tmp/safe-merge/` — while backups are redacted, remove them when no longer needed

## Changelog

### 2026-03-02 — Fully Automated Pipeline
- Added `scripts/safe-merge-update.sh` — end-to-end automated merge pipeline
- Source changed from `origin/main` → `upstream/main` (now pulls real OpenClaw updates)
- Fork branch updated to `local-desktop-main` (was `main`)
- Conflicts auto-resolved by Claude using baked-in strategy (no human needed for happy path)
- Auto-prunes stale `safe-merge-*` branches on each run (prevents infinite accumulation)
- On success: pushes to `myfork/local-desktop-main`, deletes temp branch, restarts gateway
- On build failure: leaves safe-merge branch intact, exits cleanly for investigation
- `--resume` flag: skip merge, jump straight to build → push → cleanup (for post-manual-fix)
- MERGE_MANIFEST.json v1.2.0: added `hostinger.ts`, `plugins-ui.ts`, `memory.ts` as protected files
- Memory tab now shows spinner on first load (no more flash of empty content)

### 2026-03-01 — Background Sessions Panel
- Added `bgSessions.list` and `bgSessions.history` RPC handlers
- Added Background Sessions Panel UI (right-side drawer, session selector, live transcript, send input)
- Clicking the updates badge now opens the panel alongside the update modal
- State fields: `bgSessionsPanelOpen`, `bgSessionsList`, `bgSessionsSelectedKey`, `bgSessionsHistory`, `bgSessionsInput`, `bgSessionsSending`, `bgSessionsHistoryLoading`, `bgSessionsLoading`
- MERGE_MANIFEST.json updated with 3 new protected files and `mustPreserve` patterns

### 2026-03-01 — Merge of 148 upstream commits
Conflicts resolved in: `app-render.helpers.ts`, `app-render.ts`, `app-view-state.ts`, `app.ts`. Key resolutions:
- `app-render.helpers.ts`: kept `renderContextGauge`, merged `hideCron` + `sessionsHideCron` from upstream, merged `countHiddenCronSessions`, preserved `renderRecentArchivedOptions`
- `app-render.ts`: kept our nav imports (`getDynamicTabGroups`, Jarvis/mode/usage); added upstream's `resolveConfiguredCronModelSuggestions`
- `app-view-state.ts`: kept `sessionsAgentFilter` + added `sessionsHideCron` from upstream
- `app.ts`: kept session history fields + added `sessionsHideCron = true` default from upstream

## Known Issues / Lessons Learned

### Discord Voice Schema (2026-02-27)
Upstream added `.strict()` to `DiscordVoiceSchema`, rejecting keys our fork previously supported. Fix: remove unsupported keys from config, or add them back to the schema.

### Control UI Assets Missing (2026-02-27)
`pnpm build` builds the gateway but NOT the Control UI. UI needs separate `pnpm ui:build`. The validate script now includes this.

### Duplicate Schema Properties (2026-02-27)
Git auto-merge kept both our extracted const AND upstream's inline block. Fix: manual dedup during AI conflict resolution.

### CSP connect-src Extensions (2026-03-01)
Our fork adds `http://localhost:*` (Jarvis voice agent) and `https://api.openai.com` (Realtime API) to the CSP `connect-src` directive in `control-ui-csp.ts`. Upstream only has `ws: wss:`. On merge, always keep our extensions — they're required for voice features.

### Branch Naming Convention (2026-03-01)
Merge branches should be date-stamped: `safe-merge-YYYY-MM-DD`. This makes it easy to identify merge attempts and clean up old branches.

### Auto-Merged Protected Files Need Verification (2026-03-01)
Even files that auto-merge without conflicts can lose custom code if upstream refactors the surrounding context. After merge, always verify `mustPreserve` patterns exist in auto-merged protected files — don't just trust git's auto-merge.

### pnpm install May Add Packages (2026-03-01)
Upstream may add new dependencies. When 162 commits are merged, `pnpm install` downloaded 51 new packages. This is expected but worth noting in the merge report.

## Safety Summary

- ✅ **Backups before any edits** — `/tmp/safe-merge/backups/`
- ✅ **New branch** — never merges directly into current branch
- ✅ **Validation must pass** before committing
- ✅ **No external downloads in skill setup** — skill files are all local; merge workflow does use network for `git fetch` and `pnpm install`
- ✅ **No credential requirements** — uses your existing agent model
- ✅ **Secrets redacted before model transmission** — API keys, tokens, passwords, private keys
- ✅ **Only conflict diffs sent to model** — not the entire repo
- ✅ **User controls merge** — agent reports results, user decides to push
- ✅ **Dry-run in worktree** — pre-flight uses a temp worktree, not your working tree
- ✅ **Stops on failure** — if validation fails, reports and stops rather than pushing broken code
