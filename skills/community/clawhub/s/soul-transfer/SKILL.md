---
name: soul-transfer
description: "Backup and restore an OpenClaw agent's full workspace (memory, config, credentials, skills, cron jobs) to/from a Git repository. Use when: migrating to a new instance, disaster recovery, setting up a fresh machine, the user says 'backup', 'restore', 'migrate', 'transfer', '夺舍', '还魂', or 'soul transfer'. Also use for periodic backup setup and backup verification."
---

# Soul Transfer (夺舍)

Agent workspace migration between OpenClaw instances via Git.

## Concepts

- **Soul** = workspace files (memory, identity, skills, frameworks)
- **Body** = OpenClaw instance (runtime, config, cron jobs)
- **Backup repo** = Git repository holding the soul
- **Transfer** = clone soul into new body, restore config, rebuild runtime state
- **`$WORKSPACE`** = the agent's workspace directory (resolve via repo path in system prompt, or `~/.openclaw/workspace` as fallback)
- **`openclaw-config-backup.json`** = exported OpenClaw config snapshot (channel tokens, API keys, runtime settings). Name it whatever you like — just keep it in the workspace and committed to the backup repo.

## Backup Procedure

### 1. Ensure Git remote is configured

```bash
cd $WORKSPACE
git remote get-url origin || git remote add origin https://<token>@github.com/<owner>/<repo>.git
```

### 2. Export current OpenClaw config

Save a copy of the live config for future restoration. This file contains channel tokens, API keys, and guild settings that are NOT in the workspace markdown files.

Use `gateway config.get` tool → extract the `parsed` object → write to a JSON file in the workspace (e.g. `openclaw-config-backup.json`).

This step is critical — without this file, channel connections cannot be restored on a new instance.

### 3. Commit and push

```bash
git add -A
git commit -m "backup: $(date +%Y-%m-%d_%H%M)"
git push origin master
```

### 4. Verify backup

```bash
git log --oneline -1
git diff --stat HEAD~1
```

### Backup cron (automated)

Set up a recurring cron job for automatic backups. See references/cron-templates.md for ready-to-use definitions.

## Restore Procedure (夺舍 Checklist)

Execute these steps in order. Do not skip step 5 — it is the most commonly forgotten step.

### Step 1: Clone the backup repo

```bash
git clone https://<token>@github.com/<owner>/<repo>.git /tmp/soul-backup
```

### Step 2: Audit contents

Before restoring, review what's in the repo:

```bash
find /tmp/soul-backup -type f | wc -l
cat /tmp/soul-backup/IDENTITY.md
```

Identify sensitive files that should NOT be copied to markdown: standalone credential files (API tokens, key files, etc.)

### Step 3: Restore workspace files

Copy core files from the backup into `$WORKSPACE`:

- Identity files: `IDENTITY.md`, `USER.md`, `SOUL.md`
- Memory files: `MEMORY.md`, `AGENTS.md`, `HEARTBEAT.md`, `NOW.md`, `SESSION-STATE.md`
- State files: `heartbeat-state.json`
- Daily logs: `memory/*.md` (all of them)
- Skills: `skills/` directory
- Framework files: any `.md` or `.json` strategy/framework files
- **Config backup**: the exported OpenClaw config JSON file

### Step 4: Scrub hardcoded credentials from markdown files

```bash
# Scan for credential patterns
grep -rl 'ghp_\|AKIA[0-9A-Z]\|sk-[a-zA-Z0-9]' $WORKSPACE/ \
  --include='*.md' 2>/dev/null
```

Replace found credentials with `[REDACTED]` in markdown and log files.

Do NOT scrub the config backup JSON — it contains credentials needed for step 5.

### Step 5: Restore OpenClaw config (⚠️ CRITICAL — do not skip)

This is the step that connects channels, API keys, and runtime settings. Without it, all channels remain disconnected.

Read the config backup JSON from the workspace. Extract:

- **Channel tokens** (Discord bot token, Telegram token, etc.)
- **Channel settings** (guilds, allowlists, DM policies, actions)
- **API keys** (web search, etc.)
- **Tool settings** (exec security level)
- **Environment variables**

Apply via `gateway config.patch`:

```json
{
  "channels": {
    "discord": {
      "enabled": true,
      "token": "<from config backup>",
      "groupPolicy": "allowlist",
      "guilds": { "..." },
      "dm": { "..." },
      "actions": { "..." }
    }
  },
  "tools": {
    "web": { "search": { "apiKey": "<from config backup>" } },
    "exec": { "security": "full" }
  }
}
```

After patching, OpenClaw restarts automatically. Verify with `openclaw status` — channels should show connected.

Use `config.schema.lookup` to check field names if the OpenClaw version differs from the backup.

### Step 6: Rebuild cron jobs

Cron jobs are runtime state, NOT stored in git. Rebuild from documented list or references/cron-templates.md.

Use `cron add` for each job. Only restore jobs that are still needed.

### Step 7: Verify and clean up

```bash
# Verify channel connectivity
openclaw status

# Delete temp clone
rm -rf /tmp/soul-backup

# Delete BOOTSTRAP.md if present (no longer a fresh instance)
rm -f $WORKSPACE/BOOTSTRAP.md

# Commit restored state
cd $WORKSPACE
git add -A && git commit -m "夺舍完成: $(date +%Y-%m-%d_%H%M)"
```

### Step 8: Log the event

Record the transfer in today's daily log with timestamp, file count, and any issues encountered.

## Common Pitfalls

1. **Skipping config restore** — Workspace files restore memory but NOT channel connections. The config backup JSON → `config.patch` is mandatory.
2. **Over-scrubbing credentials** — Don't scrub the config backup JSON; it's needed for config.patch. Only scrub credentials embedded in markdown/log files.
3. **Forgetting cron rebuild** — Cron is runtime state, not in git.
4. **Old vs new config schema** — Use `config.schema.lookup` to verify field names before patching. OpenClaw versions may rename fields.
5. **Git remote not configured** — New instance has no remote; configure before first backup push.

## Backup Health Check

Run periodically to verify backup integrity:

```bash
cd $WORKSPACE
# Check remote is configured
git remote -v
# Check last push time
git log --oneline -1
# Check for uncommitted changes
git status --short
# Verify config backup exists and has channel tokens
grep -c '"token"' openclaw-config-backup.json 2>/dev/null || echo "⚠️ No config backup found"
```
