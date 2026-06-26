# AlphaClaw: Deep Analysis for LDM OS

**Date:** 2026-04-11
**Author:** CC (Claude Code)
**For:** Parker
**Source repo:** `repos/third-party-repos/alphaclaw/` (private fork of `garrytan/alphaclaw` at `wipcomputer/alphaclaw`)
**Companion doc:** `2026-04-11--cc-mini--gbrain-analysis.md`

---

## TL;DR

1. **alphaclaw is a web-UI version of what wip-healthcheck + lesa-bridge + our openclaw install flow are trying to be.** 19 stars. 7 days old. Docker/Linux only (no macOS local dev). Deploy on Railway or Render with one click.

2. **Tagline:** "First deploy to first message in under five minutes." The onboarding experience is 10x better than ours right now.

3. **The watchdog is stronger than wip-healthcheck on observability.** Crash-loop detection, auto-repair via `openclaw doctor --fix`, persistent SQLite event log with correlation IDs, queryable UI. Our healthcheck is solid on detection but weaker on "event log for humans to review."

4. **The Setup UI (Preact + htm + Wouter) is what our install flow should be.** Nine tabs covering Gateway/Browse/Usage/Cron/Nodes/Watchdog/Providers/Envars/Webhooks. We're CLI-only today. Huge UX gap.

5. **The anti-drift AGENTS.md injection pattern is the same we use** but delivered differently: alphaclaw injects the rules **on every message**, not just session start. Solves the "CLAUDE.md gets compressed after 50K tokens" problem.

6. **Multi-channel orchestration is extensive:** Telegram topics, Discord, Slack Socket Mode, Google Workspace OAuth (Gmail + Calendar + Drive + Docs + Sheets + Tasks + Contacts + Meet). lesa-bridge is iMessage-only. Major gap.

7. **Git-backed workspace audit trail** (hourly automatic commits of the `.openclaw` dir to GitHub). We don't do this. Should.

8. **Ejectable by design.** "Remove AlphaClaw and your agent keeps running. Nothing proprietary, nothing to migrate."

---

## 1. What alphaclaw is

alphaclaw is the ops and setup layer around OpenClaw. Explicit positioning: "the ultimate OpenClaw harness."

**Core capabilities:**
- Password-protected Setup UI (Preact + htm + Wouter, bundled with esbuild)
- Gateway manager (spawns, monitors, restarts, proxies OpenClaw gateway as a child process)
- Watchdog (crash-loop detection, auto-repair, multi-channel notifications, SQLite event log)
- Channel orchestration (Telegram topics, Discord, Slack Socket Mode, Google Workspace OAuth)
- Cron jobs UI with run history and cost analytics
- Nodes (guided VPS multi-machine setup)
- Webhooks with per-hook transform modules
- Browser-based file explorer with git-aware sync
- Anti-drift prompt hardening (injected `AGENTS.md` + `TOOLS.md` into every message)
- In-place version management (alphaclaw + openclaw updates with pending markers)
- Codex OAuth PKCE flow

**Tests:** 440. Active development. MIT license.

**Deploy targets:** Railway and Render via one-click templates. Docker/Linux only. No macOS local dev yet.

---

## 2. The runtime model

alphaclaw runs as an Express 4 HTTP server (port 3000 by default, or `$PORT` env var; `bin/alphaclaw.js:469-478`). It manages OpenClaw's Gateway as a child process spawned via `spawn("openclaw", ["gateway", "run"], { ... })` (`lib/server/gateway.js:149`).

### Gateway lifecycle

1. **Port assignment:** Gateway runs on `127.0.0.1:18789`. alphaclaw enforces that it cannot run on 18789 itself.
2. **Child process spawning:** `launchGatewayProcess()` spawns the gateway, captures stderr in a 50-line tail buffer, and emits a launch handler once "listening on" appears in stdout (`lib/server/gateway.js:141-199`).
3. **Exit handling:** When the gateway exits, `gatewayExitHandler` is invoked with `{ code, signal, expectedExit, stderrTail }`. Unexpected exits trigger watchdog recovery.
4. **Proxy:** Express routes inbound requests to the gateway via `http-proxy`.
5. **Restart patterns:**
   - `restartGateway()` calls `openclaw gateway --force` to stop + re-exec
   - `restartGatewayLight()` calls `openclaw gateway restart` for lighter restarts
   - Both mark the exit as expected via `markManagedGatewayExitExpected()` so watchdog doesn't trigger
6. **Auth token flow:** `OPENCLAW_GATEWAY_TOKEN` is auto-generated if unset and injected into the gateway's environment via `gatewayEnv()` (`lib/server/gateway.js:44-49`). Token lives in `.env` on the server.
7. **Signal handling:** On SIGTERM/SIGINT, alphaclaw calls `openclaw gateway stop` and exits gracefully.

---

## 3. The Setup UI (STEAL THIS entire concept)

Nine tabs:

| Tab | Manages |
|-----|---------|
| **General** | Gateway status/restart, channel health, pending pairings, Google Workspace, repo sync schedule, OpenClaw dashboard link |
| **Browse** | File explorer rooted at `.openclaw`, inline edits, diff view, git-aware sync |
| **Usage** | Token summaries, per-session/per-agent cost breakdown |
| **Cron** | Job management, rolling calendar, run history, trend analytics, per-run usage |
| **Nodes** | VPS node setup, browser-attach, routing controls |
| **Watchdog** | Health monitoring, crash-loop status, auto-repair toggle, notifications, event log, live terminal |
| **Providers** | AI provider credentials + model selection + Codex OAuth |
| **Envars** | Edit env vars, gateway restart prompts |
| **Webhooks** | Endpoint visibility, create flow, request history, payload inspection, OAuth callbacks |

### Onboarding wizard

First visit (no `openclaw.json`) shows a step-by-step flow. Model selection → provider credentials → GitHub repo pairing → channel setup (Telegram/Discord/Slack). Each step validates credentials and writes config incrementally.

### Password auth model

- Single `SETUP_PASSWORD` env var (required)
- All Setup UI access gated behind password auth
- Brute-force protection via exponential backoff lockout (`lib/server/login-throttle.js`)
- First CLI device pairing is auto-approved for one-click onboarding
- Subsequent pairing requests appear in the UI

### What our stack looks like by comparison

CLAUDE.md, CLI commands, `openclaw doctor`, 1Password SA token, ops via terminal. Everything works but there's no "show this to a non-engineer" surface.

### What to do about it

**Option A:** Fork alphaclaw's UI and adapt it to our harness. Replace OpenClaw-specific bits with LDM OS equivalents (Dream Weaver tab, Memory Crystal tab, Agent Pay tab, Kaleidoscope tab). Preact + htm + Wouter stack is lightweight and ejectable.

**Option B:** Contribute our LDM OS features upstream as alphaclaw tabs. Then Garry's users get our differentiators and we get his UI.

Both are valid. Option A gives us control; Option B gets wider distribution.

---

## 4. The watchdog (compare to wip-healthcheck)

From `lib/server/watchdog.js` (25KB, real state machine):

```javascript
const state = {
  lifecycle: "stopped" | "running" | "crashed",
  health: "unknown" | "healthy" | "degraded" | "unhealthy",
  uptimeStartedAt,
  repairAttempts,
  crashTimestamps,
  autoRepair,
  notificationsDisabled,
  crashRecoveryActive,
  awaitingAutoRepairRecovery,
  startupConsecutiveHealthFailures,
};
```

### Health check cadence

- **Regular:** 120s default (`WATCHDOG_CHECK_INTERVAL`)
- **Bootstrap (startup only):** 5s until healthy
- **Degraded:** 5s

### Crash-loop detection

3 crashes in 300s triggers the `crash_loop` incident. Configurable thresholds. `probeGatewayHealth()` POSTs to the gateway's health endpoint with a 5s timeout. Response codes: 200 = healthy, 5xx = unhealthy, timeout/network error = degraded.

### Auto-repair sequence

1. Increment `state.repairAttempts`
2. If `WATCHDOG_AUTO_REPAIR=true` and attempts < max (default 3):
3. Run `openclaw doctor --fix --yes` (via `lib/server/doctor/service.js`)
4. Restart gateway
5. Probe health again to confirm recovery
6. Notify via Telegram/Discord/Slack (configurable)

### Persistent event log

Every watchdog event (crash, health check, repair attempt, notification) is logged to SQLite (`lib/server/db/watchdog/`). Schema: `eventType, source, status, details, correlationId`. UI renders the log with timestamps.

API: `GET /api/watchdog/events` returns recent incidents with pagination. UI at `lib/public/js/components/watchdog-tab/` renders the event log.

### Notification format (strict)

```
🐺 *AlphaClaw Watchdog*
🔴 Crash loop detected - [View logs](URL)
Trigger: `crash_loop`
Attempt count: 2
```

Emoji codes: 🟢 healthy, 🟡 awaiting, 🔴 error. Markdown links only (no HTML). Values with underscores wrapped in backticks.

### How we compare

wip-healthcheck has a LaunchAgent running every 3 min, checks gateway process, HTTP probe, file descriptors, token usage, memory health. Auto-restarts gateway (rate-limited). Escalates via chatCompletions, fallback direct iMessage. Writes logs to a daily log file.

### What alphaclaw has that we don't

1. **Persistent SQLite event log with queryable schema.** We log to a file. Queryable log is much better for postmortems.
2. **UI to review incidents.** A tab showing "all crashes in last 7 days with correlation IDs" is much better than grepping log files.
3. **Multi-channel notification abstraction.** We hardcode iMessage.
4. **Explicit auto-repair attempt counter with max.** We have rate limiting but not "max repair attempts before giving up."
5. **Bootstrap mode with faster polling during startup.** Our healthcheck uses a fixed 3-minute interval.

### What we have that alphaclaw doesn't

1. **Token usage monitoring** (75%/90% compaction warnings).
2. **iMessage escalation path** directly to Parker.
3. **File descriptor monitoring.**
4. **Agent-as-first-responder pattern** (agent gets the warning, not just the operator).

### The merge

Port alphaclaw's SQLite event log + UI tab into wip-healthcheck. Keep our token/compaction/FD checks and agent-as-first-responder escalation. Add multi-channel notification abstraction so iMessage + Telegram + Discord can all be targets. Contribute compaction monitoring + agent-first-responder upstream to alphaclaw.

---

## 5. Anti-drift prompt hardening (exact same pattern we use)

alphaclaw injects `lib/setup/core-prompts/AGENTS.md` into the OpenClaw agent's system prompt **on every message**. Not a one-time CLAUDE.md read ... on every message.

### Key content (from lib/setup/core-prompts/AGENTS.md)

```markdown
### ⚠️ No YOLO System Changes!

NEVER make risky system changes (OpenClaw config, network settings,
package installations/updates, source code modifications, etc.)
without the user's explicit approval FIRST.

Always explain:
1. What you want to change
2. Why you want to change it
3. What could go wrong

Then WAIT for the user's approval.

### Plan Before You Build

Before diving into implementation, share your plan when the work
is significant...

### Save and Show Your Work (IMPORTANT)

Your `.openclaw` directory is version-controlled and this is how
work survives container restarts.

Anytime you add, edit, or remove workspace files, openclaw.json,
cron.json, skills, or external resources, commit and push your
changes to git.

End your message with a Changes committed summary.
```

Plus `TOOLS.md`: "Do not deflect actionable requests to the Setup UI. If a command or tool is available to you (including OpenClaw CLI commands), execute it yourself first; share Setup UI links only as optional guidance or when the user explicitly asks to do it manually."

### The delta with our approach

We inject CLAUDE.md via the boot sequence at the **start** of a session. alphaclaw injects it **on every message**. That's the anti-drift part. A CLAUDE.md read once gets compressed away after 50K tokens. An AGENTS.md injected every message stays top-of-mind.

### What to pull

The "per-message injection" pattern. Investigate whether the OpenClaw harness supports this. If so, move our most critical rules (shared file protection, 1Password SA token, no squash merge, merge-deploy-install separation, memory-first rule) into a per-message prompt. The rest stays in CLAUDE.md for session-level grounding.

Also adopt the "end every message with a Changes committed summary" rule for sessions that touch workspace files.

---

## 6. Channel orchestration (compare to lesa-bridge)

alphaclaw wires Telegram, Discord, Slack Socket Mode, and full Google Workspace OAuth.

### Telegram

- Bot token stored in `openclaw.json` → `channels.telegram.botToken`
- **Topic mapping:** `alphaclaw telegram topic add --thread <id> --name <text>` registers Telegram topics (threads within groups) to agent sessions
- **Multi-threaded scaling:** as usage grows, wizard guides splitting messages into topic groups
- `requireMention` config controls whether bot needs @mention to respond

### Discord

- Bot token + per-agent channel bindings
- Simple token-based auth (no Socket Mode)

### Slack

- **Socket Mode** for real-time subscriptions (no HTTP webhooks)
- Bot token + App-Level Token both required
- `createSlackApi()` manages socket connections

### Google Workspace

- OAuth flow: user provides OAuth client credentials from Google Cloud Console
- `gog` CLI (Google Workspace CLI) auto-installed at startup (`bin/alphaclaw.js:509-534`)
- Services: Gmail, Calendar, Drive, Sheets, Docs, Tasks, Contacts, Meet
- **Gmail watch:** creates Google Pub/Sub topic + subscription, registers push endpoint at alphaclaw's webhook URL, on push the transform module extracts email metadata and routes to agent
- Watch expiration tracked; alphaclaw auto-renews before expiry

### Per-agent channel bindings

Each agent (stored in `openclaw.json` → `agents[agentId]`) can have per-channel routes. Example: `destination: { channel: "telegram", to: "-1001234567890", agentId: "ops" }` routes to a Telegram group + ops agent.

### What we have

lesa-bridge for iMessage. agent.txt for Sapien ID auth. Bridge round-trip via tmux to CC. Memory Crystal sync hooks. Kaleidoscope demo at wip.computer/demo.

### What to add

A channel abstraction layer. Right now lesa-bridge is iMessage-specific. alphaclaw's pattern of `destination = { channel, to, agentId }` with per-agent bindings is cleaner. Refactor lesa-bridge to match, add Telegram and Discord behind the same interface. Google Workspace via OAuth is a bigger lift but the Pub/Sub pattern for Gmail is well-documented here.

---

## 7. Webhooks with transforms

Named webhook endpoints allow third-party services to trigger agents via HTTP POST. Each webhook has a transform module for payload normalization.

### Architecture

```
POST /hooks/{webhook-name}?token=<WEBHOOK_TOKEN>
  ↓
webhook-middleware.js validates token
  ↓
transform module (hooks/transforms/{name}/{name}-transform.mjs)
  ↓
agent.wake() or agent.message()
```

### Transform module convention

- **Path:** `hooks/transforms/{hook-name}/{hook-name}-transform.mjs`
- **Signature:** `export default async function transform(payload, context) { ... }`
- **Return:** `{ message, name, wakeMode, channel, to, agentId }`
- **Payload nesting:** webhook data is at `payload.payload` (double-nested by some providers)

### Features

- Custom names: lowercase letters, numbers, hyphens
- Managed webhooks: "gmail" (auto-created for Gmail watch, readonly)
- All webhook requests logged to SQLite (`lib/server/db/webhooks/`)
- API: `GET /api/webhooks/:name/requests` returns paginated request history
- Payload inspection: up to 50KB per request
- Query-string tokens `?token=<WEBHOOK_TOKEN>` for providers without Authorization header support (with warning shown in UI)
- Separate OAuth callback endpoint for providers needing stateful auth flows

### What this solves for us

We don't have a first-class webhook system. Everything is iMessage + MCP. Adding alphaclaw's webhook pattern would let us integrate any third-party service (GitHub events, Linear, Stripe, Twilio, etc.) without writing custom glue each time.

---

## 8. Cron jobs + nodes

### Cron jobs (`lib/server/cron-service.js`)

- Job store: `$ALPHACLAW_ROOT_DIR/cron/jobs.json`
- Each job: `{ id, name, schedule (cron expression), enabled, payload, delivery (destination), state }`
- Run history: `$ALPHACLAW_ROOT_DIR/cron/runs/{jobId}/{timestamp}.json`
- **Per-run usage:** tokens, model, provider, cost (used by Usage tab)
- **Delivery status:** `delivered` flag + `deliveryStatus` (OK/FAILED/SKIPPED)
- **UI features:** rolling calendar (next 30 days), trend view (24h/7d/30d), cost per job

### Nodes (VPS multi-machine setup)

- Setup wizard for connecting a remote node to alphaclaw
- **Browser attach:** node connects + registers itself; browser-based attach confirmation
- **Routing:** assign workloads (cron jobs, agent sessions) to specific nodes
- **Reconnect commands:** copy-paste commands to re-establish dropped connections

We have `wip-schedule` but it's CLI-only. The cron UI and run history is a big UX improvement.

---

## 9. File explorer + Git-sync

### Browser-based workspace explorer (`lib/public/js/components/browse-tab/`)

- Root: `.openclaw` directory
- File tree view, inline edit, markdown preview, diff viewer, git-aware save
- **Inline edits:** edit any text file in the browser → POST to save → git diff preview → commit message prompt → git push

### Git sync

- Hourly automatic commits via system cron entry (`bin/alphaclaw.js:581-600`, `lib/setup/hourly-git-sync.sh`)
- `alphaclaw git-sync -m "message"` CLI command for manual commits
- **Git auth shim:** alphaclaw installs `/usr/local/bin/git` wrapper that uses `GIT_ASKPASS` to inject `GITHUB_TOKEN` for auth (no hardcoding in URLs)
- Headless git operations without terminal interaction
- Every agent action is version-controlled and auditable

### What we do

Lēsa commits manually when asked. No hourly automatic commits.

### What to do

Add a LaunchAgent (on Mac) that runs hourly. Conditionally commit if there are changes. Or do it on every `agent_end` hook. **One afternoon of work.** Cite: `bin/alphaclaw.js:581-600` and `lib/setup/hourly-git-sync.sh`.

---

## 10. Codex OAuth PKCE flow (reusable)

alphaclaw has a full PKCE OAuth flow for OpenAI Codex CLI.

**Constants** (from `constants.js`):
- Client ID: `app_EMoamEEZ73f0CkXaXp7hrann`
- Authorize URL: `https://auth.openai.com/oauth/authorize`
- Redirect URI: `http://localhost:1455/auth/callback`
- Scope: `openid profile email offline_access`

**Flow:**
1. User clicks "Connect Codex" in Providers tab
2. Browser opens Codex auth URL with PKCE `code_challenge`
3. User grants permission on OpenAI's site
4. Redirect back to alphaclaw's callback handler
5. alphaclaw exchanges code for token, stores in auth-profiles.json

**Why this matters:** when we integrate any OAuth-based provider (Claude account login, GitHub OAuth, Google OAuth), we'll need this exact pattern. alphaclaw has working, tested code. Port it.

---

## 11. Design system worth lifting

alphaclaw's frontend: **Preact + htm + Wouter + Tailwind.** Lightweight. No build-time React. Fast.

### Component library

| Component | CSS class / variant | Purpose |
|-----------|---------------------|---------|
| `ActionButton` | `ac-btn-cyan`, `ac-btn-secondary`, `ac-btn-green`, `ac-btn-ghost`, `ac-btn-danger` | Primary/secondary/ghost action buttons |
| `ConfirmDialog` | — | Destructive confirmations |
| `ModalShell` | `fixed inset-0 bg-black/70 flex p-4 z-50` | Custom non-confirm modals |
| `Badge` | — | Status chips (replaces inline status spans) |
| `SecretInput` | — | Password/token fields with show/hide |
| `ToggleSwitch` | — | Boolean controls |
| `Tooltip`, `InfoTooltip` | portal-backed | Hover help (not clipped by scroll containers) |
| `LoadingSpinner` | — | Loading states |
| `PageHeader` | — | Page title + actions |

### Theme tokens (lib/public/css/theme.css)

```css
--bg: #0d121b;
--bg-sidebar: #0f141f;
--accent: #63ebff; /* cyan */
--text: #c9d1d9;
--text-muted: #6e7681;
--text-dim: #424854;
--status-error-bg: rgba(127, 29, 29, 0.95);
--status-warning-bg: rgba(66, 32, 6, 0.95);
--status-success-bg: rgba(5, 46, 22, 0.5);
```

Mapped to Tailwind via `tailwind.config.cjs`. **Semantic tokens only.** No raw palette classes (`text-body` not `text-gray-300`).

### Cache primitives (lib/public/js/lib/api-cache.js)

- `cachedFetch(url)` — imperative one-off fetches
- `useCachedFetch(url, options)` — component data loads
- `usePolling(url, interval, cacheKey)` — recurring refreshes
- `pauseWhenHidden` — tab-inactive optimization

### Shared utilities

- `lib/public/js/lib/format.js` — `formatCost()`, `formatTokens()`, `formatDuration()`, `formatDate()`
- `lib/public/js/lib/session-keys.js` — session key parsing + destination derivation
- `lib/public/js/lib/storage-keys.js` — all localStorage keys centralized (naming: `alphaclaw.<area>.<purpose>`)

### When to use this stack

Kaleidoscope next-gen. Memory Crystal browser. Dream Weaver visualizer. LDM OS installer UI. **Any web UI we build from now on.** It's lightweight enough to ship a mini-UI in any repo and consistent enough to feel unified.

---

## 12. Version management

**In-place updates:** alphaclaw can update itself and OpenClaw without manual downloads or restarts.

### alphaclaw updates

- Endpoint: `POST /api/alphaclaw/update` triggers `npm install @chrysb/alphaclaw@latest`
- Writes pending marker: `$ALPHACLAW_ROOT_DIR/.alphaclaw-update-pending`
- On restart, `bin/alphaclaw.js` detects marker and re-runs install (`:161-187`)
- Release notes displayed in UI before apply

### OpenClaw updates

- Similar flow: detect new version in npm registry, apply with timeout handling
- Fallback for ephemeral filesystems (Railway): pending marker pattern

### Version pinning in templates

- Railway/Render templates pin `@chrysb/alphaclaw` version in `package.json`
- Beta iterations pinned explicitly (e.g., `0.3.2-beta.4`); production uses `latest` tag
- Ensures consistent Docker layer caching (comment in AGENTS.md:85)

### What to learn for wip-release

- **In-app release notes review** before apply. We have wip-release CLI but no in-app confirmation flow.
- **Pending marker pattern** for ephemeral filesystem recovery. Useful for cloud deployments.

---

## 13. Notable patterns

### Express 4 vs 5 guardrails (AGENTS.md:94-113)

A broken npm tree that resolves Express 5 causes body parsing regressions. alphaclaw documents the failure mode and fix:

- Symptom: in-place `/app/node_modules` mutations (emergency package swaps) leave tree inconsistent
- Fix: clean rebuild: `docker compose down && docker compose build --no-cache && docker compose up -d`
- Verify: `node -p "require('express/package.json').version"` should be `4.x`

### Managed internal files

- Hourly git sync script: `$ALPHACLAW_ROOT_DIR/.alphaclaw/hourly-git-sync.sh`
- System cron entry: `/etc/cron.d/openclaw-hourly-sync`
- Reconciled on every startup: if missing or stale, alphaclaw reinstalls it

### Shared formatters

Prevents duplication of `formatCost`, `formatTokens`, `formatDuration` across features. Feature-specific transforms stay local.

### Decomposed components from day one

AGENTS.md:46-48: "Avoid monolithic implementation files. For new UI areas and API areas, start with a decomposed structure (focused components/hooks/utilities; focused route modules/services/helpers)." Prevents drift into god-files.

---

## 14. What's weak or missing

1. **macOS local development** not supported. Docker/Linux only.
2. **No voice integrations** (Twilio, voicebot, phone). Big gap vs gbrain.
3. **No analytics beyond cost.** Usage tab covers tokens/cost but not semantic observability of agent reasoning.
4. **No plugin system.** Integrations are hardcoded (Telegram, Discord, Slack, Google Workspace). Custom channels require forking.
5. **Limited workflow automation.** Cron jobs are simple repeating tasks. No conditional workflows, fan-out/fan-in, or multi-step pipelines.
6. **No draft/staging mode.** All changes are live.
7. **No observability into doctor runs.** Doctor output is logged but not queryable (no trend view, no before/after snapshots).
8. **GitHub-only git sync.** Hardcoded OAuth flow + API endpoints. No GitLab, Gitea, self-hosted.

---

## 15. STEAL LIST (ranked by impact × ease)

### Tier 1: Pull immediately

1. **Hourly git sync LaunchAgent for Lēsa's workspace.** LaunchAgent runs every hour, commits any changes, pushes to GitHub. **1 afternoon of work.** Cite: `bin/alphaclaw.js:581-600`, `lib/setup/hourly-git-sync.sh`.

2. **Per-message AGENTS.md injection for critical rules.** Move the most critical rules (1P SA token, shared file protection, no squash merge) into a per-message prompt. Leave the rest in CLAUDE.md. **1 day.** Requires verifying OpenClaw harness supports per-message injection.

3. **"End every message with a Changes committed summary" rule** for sessions that touch workspace files. One-line CLAUDE.md addition.

### Tier 2: Adapt into our stack

4. **Watchdog SQLite event log + correlation IDs into wip-healthcheck.** Queryable incident history. Bootstrap mode with faster polling. Multi-channel notification abstraction. **3-5 days.** Cite: `lib/server/watchdog.js`, `lib/server/db/watchdog/`.

5. **Channel abstraction layer for lesa-bridge.** Refactor to `destination = { channel, to, agentId }` pattern. Add Telegram as a peer to iMessage. **1 week.**

6. **Webhooks with transform modules.** First-class webhook system. Named endpoints, transform convention, request logging, OAuth callback support. **1 week.**

7. **LDM OS Setup UI forked from alphaclaw.** Preact + htm + Wouter. Replace OpenClaw-specific tabs with Dream Weaver / Memory Crystal / Agent Pay / Kaleidoscope. Keep the watchdog + providers + envars + webhooks tabs. **2-3 weeks.**

8. **Codex OAuth PKCE flow** as a reusable template. Port when we integrate any OAuth provider. Days when needed.

9. **Cron UI with run history** for wip-schedule. Rolling calendar + trend analytics + per-run usage. **1 week.**

### Tier 3: Inspiration

10. **Shared component library lifted wholesale.** ActionButton, ConfirmDialog, ModalShell, Badge, SecretInput, ToggleSwitch, Tooltip, InfoTooltip, LoadingSpinner, PageHeader. Use for any UI we build from now on.

11. **Cache primitives** (cachedFetch, useCachedFetch, usePolling with pauseWhenHidden).

12. **Telegram notice format** for our own notification systems (🟢/🟡/🔴 + markdown links + backticks for special chars).

13. **Decomposed-from-day-one** component rule. Prevents monolithic files.

14. **Express 4 vs 5 guardrails** pattern. Document known failure modes + recovery procedures.

---

## 16. Collisions with our stack

### wip-healthcheck vs alphaclaw watchdog

**The collision:** both are self-healing watchdogs for OpenClaw gateway.

**Resolution:** Port alphaclaw's event log and UI tab patterns into wip-healthcheck. Keep our agent-first-responder escalation (alphaclaw doesn't have this). Contribute our improvements upstream to alphaclaw so everyone benefits.

### lesa-bridge vs alphaclaw channel orchestration

**The collision:** both route messages to agents across channels.

**Resolution:** alphaclaw has multi-channel (Telegram/Discord/Slack/Google). We have iMessage + MCP. Both matter. Port alphaclaw's channel abstraction pattern into lesa-bridge so we can add Telegram as a peer. Then contribute iMessage back upstream to alphaclaw (Garry doesn't have it).

### CLAUDE.md boot sequence vs alphaclaw AGENTS.md per-message injection

**The collision:** both inject rules into the agent's system prompt.

**Resolution:** hybrid. Keep CLAUDE.md as the session-level grounding. Add a shorter per-message prompt re-enforcing the MOST critical rules. Under 500 tokens so it doesn't eat context.

### OpenClaw install via CLI vs alphaclaw Setup UI

**The collision:** both are install/config surfaces.

**Resolution:** use alphaclaw's UI as the "non-engineer" entry point. Keep our CLI + CLAUDE.md flow for agent-to-agent installs. Fork the UI or contribute LDM OS tabs upstream.

---

## 17. What we have that alphaclaw doesn't

1. **Token usage + compaction monitoring** (75%/90% warnings, agent-first escalation).
2. **Agent-first-responder escalation** (agent gets the warning, not just the operator).
3. **iMessage as a channel.** Parker's primary UX.
4. **Four-layer memory stack** mapping to different consolidation windows.
5. **Dream Weaver Protocol** as theory + implementation.
6. **Cross-agent MCP bridge** (Lēsa ↔ CC).
7. **Agent Pay x402 micropayments.**
8. **Sapien ID** (ld+json manifest, discoverable auth).
9. **Private mode** (wipe scan/search/execute).
10. **1Password headless SA token** (zero-interaction secrets).
11. **File descriptor monitoring** in healthcheck.
12. **Lēsa as named persona** with identity files and soul docs.
13. **macOS support** (we live there).

---

## 18. What to contribute back

### Upstream PRs to alphaclaw

1. **Token usage + compaction monitoring** as a new watchdog check. Directly portable. Our compaction-indicator plugin is already modular.

2. **Agent-first-responder escalation.** Our pattern notifies the agent FIRST via chatCompletions. Contribute this escalation path alongside the existing operator notifications.

3. **iMessage channel.** Add iMessage as a supported channel alongside Telegram/Discord/Slack. Lifts lesa-bridge into the upstream codebase. Big deal for Mac users.

4. **macOS local development support.** alphaclaw README explicitly says "macOS local development is not yet supported." We have native Mac integration. Worth contributing a macOS path.

5. **File descriptor monitoring** as a new health check. Simple addition.

6. **Universal installer pattern.** Our wip-universal-installer scaffolds any agent-native repo. Could be alphaclaw's onboarding path for custom plugins.

---

## 19. Key files to read directly

**Architecture:**
- `AGENTS.md` (project-level coding conventions)
- `lib/setup/core-prompts/AGENTS.md` (the runtime prompt injected on every message)
- `lib/server/watchdog.js` (self-healing state machine, 25KB)
- `lib/server/gateway.js` (child-process lifecycle)
- `lib/server/doctor/service.js` (auto-repair logic)

**UI / design system:**
- `lib/public/js/components/` (shared component library)
- `lib/public/css/theme.css` (theme tokens)
- `tailwind.config.cjs` (token mapping)
- `lib/public/js/lib/api-cache.js` (cache primitives)
- `lib/public/js/lib/format.js` (shared formatters)

**Channels:**
- `lib/server/telegram-*.js`
- `lib/server/discord-api.js`
- `lib/server/slack-api.js`
- `lib/server/gmail-watch.js`
- `lib/server/google-state.js`
- `lib/server/gog-skill.js`

**Webhooks + cron:**
- `lib/server/webhooks.js`
- `lib/server/webhook-middleware.js`
- `lib/server/cron-service.js`

**Entrypoints:**
- `bin/alphaclaw.js`
- `lib/server.js`

---

## 20. Quotables

1. "The ultimate OpenClaw harness. Deploy in minutes. Stay running for months. Observability. Reliability. Agent discipline. Zero SSH rescue missions."

2. "First deploy to first message in under five minutes."

3. "No Lock-in. Eject Anytime. AlphaClaw simply wraps OpenClaw, it's not a dependency. Remove AlphaClaw and your agent keeps running. Nothing proprietary, nothing to migrate."

4. "UX over features. Usability matters more than feature count. Every interaction should feel considered."

5. "Reliability is a feature. The watchdog, auto-repair, crash-loop recovery ... these matter as much as any UI improvement."

6. "NEVER make risky system changes without the user's explicit approval FIRST. Always explain: (1) What you want to change, (2) Why you want to change it, (3) What could go wrong. Then WAIT."

7. "Your `.openclaw` directory is version-controlled and this is how work survives container restarts."

8. "Do not deflect actionable requests to the Setup UI. If a command or tool is available to you, execute it yourself first."

9. "AlphaClaw is a convenience wrapper ... it intentionally trades some of OpenClaw's default hardening for ease of setup."

10. "All gateway access is gated behind a single `SETUP_PASSWORD`. Brute-force protection is built in (exponential backoff lockout)."

---

## 21. Closing

alphaclaw is the operational harness we've been half-building. Where gbrain is a "steal the architecture" target, alphaclaw is a "steal the UX" target.

The most impactful single pull is the **hourly git sync** (one afternoon). The most strategically important pull is the **Setup UI pattern** (2-3 weeks) that gives LDM OS a non-engineer entry point. The highest-leverage upstream contribution is the **iMessage channel + macOS support** (plants our flag and onboards Mac users to alphaclaw).

**Everything in alphaclaw accelerates us if we're willing to integrate rather than rebuild.**

**Next actions:**
1. Pull the hourly git sync pattern into a LaunchAgent. This week.
2. Design a per-message prompt injection for critical rules. This week.
3. Spike the SQLite event log + correlation ID pattern in wip-healthcheck. Next week.
4. Scope a forked Setup UI for LDM OS. Next two weeks.
5. First upstream PR: iMessage channel + macOS local-dev support.
