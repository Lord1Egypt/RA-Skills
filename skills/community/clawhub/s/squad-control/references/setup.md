# Squad Control Setup Guide

## Prerequisites
- An OpenClaw instance (VPS, local machine, Windows/WSL, etc.)
- A Squad Control account at https://squadcontrol.ai

---

## Step 1 — Get your API Key

1. Sign in to Squad Control
2. Go to **Settings → OpenClaw Integration**
3. Click **Generate API Key** — copy it now (shown once)
4. Note your workspace slug (shown in the connect snippet)

---

## Step 2 — Add env vars to OpenClaw

Edit `~/.openclaw/openclaw.json` and add:

```json
{
  "env": {
    "SC_API_URL": "https://squadcontrol.ai",
    "SC_API_KEY": "mc_your_api_key_here"
  }
}
```

Then restart: `openclaw gateway restart`

Optional hardening env vars:
- `SC_REVIEWER_AGENT_ID` — deterministic reviewer routing
- `SC_DEFAULT_BRANCH` — default PR/merge base branch (if not `main`)
- `SC_WAKE_DISPATCH_AGENT` — which local OpenClaw agent should issue residual dispatcher handoffs (defaults to `main`)
- `SC_WAKE_DISPATCH_MODE` — `acp` (default) for direct ACP `sessions.spawn`, or `chat` to force the older dispatcher handoff path
- `SC_WAKE_ACP_AGENT` — which ACP harness agent should run direct wake-dispatched work (defaults to `codex`)
- `SC_WAKE_LOCAL_GATEWAY_URL` — override the local authenticated OpenClaw Gateway base URL used for `POST /api/sessions/spawn`
- `SC_WAKE_LOCAL_GATEWAY_TOKEN` — override the local gateway token if you do not want to rely on `~/.openclaw/gateway.token`
- `SC_WAKE_LOCAL_GATEWAY_TOKEN_FILE` — override the token file path (default: `~/.openclaw/gateway.token`)
- `SC_WAKE_ACP_ENDPOINT_CACHE_TTL_SEC` — how long to remember that the local `/api/sessions/spawn` endpoint is unavailable before retrying (default: 3600)

**About SC_API_KEY scopes:**
- **Workspace-scoped key** — bound to a single workspace. `/api/tasks/pending` returns only that workspace's tasks. Good for single-workspace setups.
- **Account-scoped key** — spans all workspaces in your account. `/api/tasks/pending` returns tasks from all workspaces, each with an embedded `workspace` object containing repo URL, GitHub token, and concurrency settings. **Recommended for multi-workspace setups** — no local workspace config needed.

> Both key types are fully supported. If you're only using one workspace, a workspace-scoped key works fine. If you're managing multiple projects from one OpenClaw instance, generate an account-scoped key in Squad Control → Settings → API Keys.

---

## Step 3 — Set up the polling cron job

> **Security note:** `SC_API_URL` and `SC_API_KEY` are already set as env vars in Step 2.
> The cron message below does **not** embed them — OpenClaw injects them from your config automatically.
> Never paste your API key directly into a cron message; it would be stored in plaintext in `~/.openclaw/cron/jobs.json`.

Run this command once in your terminal:

```bash
openclaw cron add \
  --name "squad-control-poll" \
  --every 5m \
  --session isolated \
  --message "Use the squad-control skill to check for and execute pending tasks."
```

Optional and currently experimental on OpenClaw 2026.3.2:

```bash
openclaw cron add \
  --name "squad-control-wake-listener" \
  --every 15m \
  --session isolated \
  --message "Use the squad-control skill to run the wake listener for low-latency dispatch. If the listener spawns a local openclaw agent handoff, wait for that subprocess to finish before ending the cron session."
```

Verify it's scheduled:
```bash
openclaw cron list
```

Test immediately (should return HEARTBEAT_OK if no pending tasks):
```bash
openclaw cron run <jobId>
```

---

## Step 4 — (Optional) Set up GitHub access for private repos

If your workspace repository is private:

1. Go to **Settings → Project Repository → GitHub Personal Access Token**
2. Generate a fine-grained PAT at https://github.com/settings/tokens with:
   - **Contents**: Read and write
   - **Pull requests**: Read and write
   - **Metadata**: Read-only (required)
3. Paste it and click **Save Token**

Agents will automatically receive this token when they pick up tasks and use it to clone and push to your private repo.

---

## Step 5 — Create agents and tasks

1. Go to **Agents → Create Agent** (e.g. a Developer agent)
2. Go to **Tasks → New Task**, assign it to your agent
3. Wait up to 5 min (or click Run on the cron job to test immediately)
4. Watch the agent pick it up and work

With the default polling cron, pickup latency is up to 5 minutes. The optional wake-listener cron is still experimental on current OpenClaw builds: Squad Control first uses an outbound wake relay connection and falls back to the legacy long-poll endpoint if needed, but the final local dispatch step still depends on the host OpenClaw runtime. On older OpenClaw builds that do not expose the local `/api/sessions/spawn` endpoint, the listener caches that capability miss for a while and falls back to chat dispatch.

---

## Architecture

```
Squad Control (cloud)             OpenClaw (your machine)
  ├── Task kanban              ←→   ├── Polls /api/tasks/pending every 5m
  ├── Agent definitions             ├── Parses workspace.repoUrl + githubToken
  ├── Thread history                ├── Clones repo, does work
  └── Review flow                   ├── Creates PRs, posts results to thread
                                    └── Reports success or failure back
```

Pull-based: OpenClaw polls Squad Control. The optional wake listener keeps the connection outbound-only as well, so there is still no public URL or port forwarding requirement, but the recommended production path on current OpenClaw builds is the 5-minute polling cron.
