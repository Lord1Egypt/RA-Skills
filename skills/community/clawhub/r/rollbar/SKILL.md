---
name: rollbar
version: 1.5.0
description: "Monitor and manage Rollbar error tracking. List recent items, get item details, resolve/mute issues, track deployments, and manage project access tokens via the Rollbar API."
homepage: https://github.com/vittor1o/rollbar-openclaw-skill
metadata:
  openclaw:
    emoji: "🐛"
    requires:
      bins:
        - curl
        - python3
    permissions:
      shell: exec
      env:
        read:
          - ROLLBAR_ACCESS_TOKEN
          - ROLLBAR_CONFIG_FILE
      network:
        outbound:
          - https://api.rollbar.com
      files:
        read:
          - .rollbar-mcp.json
          - secrets/rollbar
          - .env
        write:
          - .rollbar-mcp.json
    safety:
      destructive_commands:
        - resolve
        - mute
        - activate
        - project-token-create
        - project-token-update
      interlock: "--yes or --dry-run required for state-changing commands"
---

# Rollbar Skill

Monitor and manage Rollbar errors directly from OpenClaw.

## Setup

The script resolves your Rollbar token from the first matching source:

| Priority | Method | How |
|---|---|---|
| 1 | `$PWD/secrets/rollbar` | One-line file in your agent workspace containing the token |
| 2 | `.rollbar-mcp.json` | MCP-compatible JSON config (cwd, `~/.rollbar-mcp.json`, or `$ROLLBAR_CONFIG_FILE`) |
| 3 | `$PWD/.env` | File in your agent workspace with `ROLLBAR_ACCESS_TOKEN=your-token` |
| 4 | `ROLLBAR_ACCESS_TOKEN` | Environment variable (injected or shell) |

### MCP-Compatible Config (Recommended for multi-project setups)

Create `.rollbar-mcp.json` in your agent workspace:

```json
// Single project
{ "token": "tok_abc123" }

// Multiple projects
{
  "projects": [
    { "name": "linkz-api",       "token": "tok_abc123" },
    { "name": "linkz-dashboard", "token": "tok_xyz789" },
    { "name": "linkz-php",       "token": "tok_def456" }
  ]
}
```

Use `--project-name <name>` to select a specific project's token when running commands.

> **Tip:** Use `project-token-create --save` to have the agent auto-create and persist tokens to `.rollbar-mcp.json`.

### Single-project .env

```bash
# workspace-myagent/.env
ROLLBAR_ACCESS_TOKEN=your-token-here
```

### Token types

- **Project-level token** — from Rollbar → Project → Settings → Project Access Tokens. Use `read` scope for monitoring; add `write` scope to resolve/mute. Best for single-project use.
- **Account-level token** — from Rollbar → Account Settings → Account Access Tokens. Required for `projects`, `project-tokens`, and `project-token-create`. Use `--project-id` to target specific projects.

## Commands

All commands use the helper script `rollbar.sh` in this skill directory.

### List projects (account token only)

```bash
./skills/rollbar/rollbar.sh projects
```

### List recent items (errors/warnings)

```bash
./skills/rollbar/rollbar.sh items [--project-id <id>] [--project-name <name>] [--status active|resolved|muted] [--level critical|error|warning|info] [--limit 20]
```

### Get item details

```bash
./skills/rollbar/rollbar.sh item <item_id>
```

### Get occurrences for an item

```bash
./skills/rollbar/rollbar.sh occurrences <item_id> [--limit 5]
```

### Resolve an item

```bash
./skills/rollbar/rollbar.sh resolve <item_id> --yes
# or preview without making changes:
./skills/rollbar/rollbar.sh resolve <item_id> --dry-run
```

### Mute an item

```bash
./skills/rollbar/rollbar.sh mute <item_id> --yes
```

### Activate (reopen) an item

```bash
./skills/rollbar/rollbar.sh activate <item_id> --yes
```

> **Safety interlock:** `resolve`, `mute`, `activate`, `project-token-create`, and `project-token-update`
> require `--yes` to execute or `--dry-run` to preview. Omitting both prints a warning and exits with
> an error — preventing silent state changes from mistaken or manipulated invocations.

### List deploys

```bash
./skills/rollbar/rollbar.sh deploys [--limit 10]
```

### Get project info

```bash
./skills/rollbar/rollbar.sh project
```

### Top active items (summary)

```bash
./skills/rollbar/rollbar.sh top [--limit 10] [--hours 24]
```

---

## Project Access Token Management

These commands require an **account-level token with `write` scope**.

### List project access tokens

```bash
./skills/rollbar/rollbar.sh project-tokens --project-id <id>
```

Token values are truncated in output (first 8 chars + `...`) for safety.

### Create a project access token

```bash
./skills/rollbar/rollbar.sh project-token-create \
  --project-id <id> \
  --name "openclaw-agent" \
  --scopes read,write \
  [--project-name <name>] \
  [--save]
```

- `--scopes` — comma-separated, e.g. `read` or `read,write` (default: `read,write`)
- `--save` — automatically saves the new token to `.rollbar-mcp.json` using `--project-name` (or `--name`) as the key
- `--project-name` — name used as the key in `.rollbar-mcp.json` when `--save` is set

**Bootstrap workflow** — let the agent provision its own project tokens:

```bash
# Set account token first
export ROLLBAR_ACCESS_TOKEN=your-account-token

# Create tokens for each project and save to MCP config
./rollbar.sh project-token-create --project-id 378962  --name "linkz-api-agent"       --scopes read,write --project-name linkz-api       --save --yes
./rollbar.sh project-token-create --project-id 462118  --name "linkz-dashboard-agent"  --scopes read,write --project-name linkz-dashboard  --save --yes
./rollbar.sh project-token-create --project-id 755542  --name "linkz-php-agent"        --scopes read,write --project-name linkz-php        --save --yes

# Now use per-project tokens directly from config
./rollbar.sh items --project-name linkz-api
```

### Update a project access token

```bash
./skills/rollbar/rollbar.sh project-token-update <token_id> \
  --project-id <id> \
  --token-status enabled|disabled
```

---

## Proactive Monitoring

To get automatic alerts for new critical/error items, set up a cron job in OpenClaw:

> "Check Rollbar for new critical or error-level items in the last hour. If any new items appeared, summarize them and alert me."

Recommended schedule: every 30–60 minutes during work hours.

## Notes

- All output is JSON for easy parsing.
- The `top` command sorts active items by occurrence count — useful for daily triage.
- Token values in `project-tokens` output are truncated for safety; full values are only returned on creation.
- Rollbar API docs: https://docs.rollbar.com/reference
