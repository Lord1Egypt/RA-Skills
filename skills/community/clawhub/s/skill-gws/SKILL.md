---
name: gws
description: Google Workspace CLI (official Google release) for Drive, Gmail, Calendar, Sheets, Docs, Chat, Admin, and every Workspace API. Includes native MCP server mode for AI agents. Use when you need to manage Google Workspace services via CLI or expose them as MCP tools.
license: MIT
homepage: https://github.com/googleworkspace/cli
metadata:
  {
    "openclaw":
      {
        "emoji": "🏢",
        "requires": { "bins": ["gws"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "npm",
              "package": "@googleworkspace/cli",
              "global": true,
              "bins": ["gws"],
              "label": "Install gws (npm)",
            },
          ],
      },
  }
---

# gws — Google Workspace CLI

Official Google-published CLI for all Workspace APIs. Dynamically built from Google Discovery Service — covers every API endpoint automatically as Google adds them.

**Note:** This is the official Google-org CLI (`googleworkspace/cli`), distinct from third-party alternatives. Prefer `gws` for new integrations — it has native MCP mode and active development from Google.

---

## APIs Covered
- **Drive** — files, folders, sharing, permissions
- **Gmail** — messages, labels, drafts, send
- **Calendar** — events, calendars, invites
- **Sheets** — spreadsheets, values, formatting
- **Docs** — documents read/write
- **Chat** — spaces, messages
- **Admin** — users, groups, org units
- **Tasks** — task lists, tasks
- **Meet** — meeting resources
- *...and every other Workspace API via Discovery Service*

---

## Installation

```bash
npm install -g @googleworkspace/cli
# or: cargo install --git https://github.com/googleworkspace/cli --locked
# or: nix run github:googleworkspace/cli
```

Verify:
```bash
gws --version
```

---

## Authentication (One-time Setup Required)

⚠️ **Auth requires manual action** — OAuth credentials must be set up once per account.

### Option A: With gcloud (fastest)
```bash
gws auth setup   # creates GCP project, enables APIs, logs in
gws auth login   # subsequent logins / scope changes
```

### Option B: Without gcloud (manual GCP console)
1. Go to console.cloud.google.com → create project
2. Enable Workspace APIs (Drive, Gmail, Calendar, etc.)
3. Create OAuth 2.0 Client ID (Desktop app type)
4. Download credentials JSON
5. Set: `export GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=/path/to/credentials.json`
6. Run: `gws auth login`

### Option C: Service Account (server/headless)
```bash
export GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=/path/to/service-account.json
```

Credentials are encrypted at rest (AES-256-GCM) with OS keyring.

---

## Basic Usage

```bash
# List 10 most recent Drive files
gws drive files list --params '{"pageSize": 10}'

# Create a spreadsheet
gws sheets spreadsheets create --json '{"properties": {"title": "Q1 Budget"}}'

# List Gmail messages
gws gmail users messages list --params '{"userId": "me", "maxResults": 5}'

# Send a Gmail message
gws gmail users messages send --params '{"userId": "me"}' --json '{"raw": "<base64>"}'

# Inspect any method schema
gws schema drive.files.list

# Stream paginated results
gws drive files list --params '{"pageSize": 100}' --page-all | jq -r '.files[].name'

# Dry-run (preview request without executing)
gws chat spaces messages create --params '{"parent": "spaces/xyz"}' --json '{"text": "test"}' --dry-run
```

---

## MCP Server Mode (AI Agent Use)

`gws` can act as an MCP server, exposing all Workspace APIs as structured tools for Claude, Cursor, VS Code, etc.

```bash
# Start MCP server (all services)
gws mcp

# Start MCP server (specific services only — recommended)
gws mcp -s drive,gmail,calendar

# Compact mode — reduces from 200-400 tools to ~26 meta-tools (saves context)
gws mcp -s drive,gmail,calendar --tool-mode compact
```

### Add to your agent config (e.g. OpenClaw / mcporter):
```json
{
  "mcpServers": {
    "google-workspace": {
      "command": "gws",
      "args": ["mcp", "-s", "drive,gmail,calendar,sheets,docs", "--tool-mode", "compact"]
    }
  }
}
```

---

## OpenClaw Agent Usage

After auth setup, the agent can:
- Read/send Gmail → automate email workflows
- Read/write Calendar → schedule meetings, parse availability
- Read/write Sheets → log data, pull reports
- Manage Drive → organize files, share docs
- Chat → send notifications to Google Chat spaces

Example — list recent emails:
```bash
gws gmail users messages list --params '{"userId": "me", "maxResults": 10, "q": "is:unread"}'
```

---

## Notes
- **Auth is manual (one-time)** — must complete `gws auth setup` before first use
- **Active development** — pre-v1.0, expect breaking changes; check GitHub for latest
- **Official Google org** — published by `googleworkspace` on GitHub, not a third-party
- **No boilerplate** — structured JSON output, works with `jq` and scripts
- **MCP-native** — expose any Workspace API as an MCP tool with a single command

---

## Status
- **Viability:** ✅ HIGH — official Google org, MCP-native, npm installable
- **Auth blocker:** ⚠️ Manual one-time `gws auth setup` required (GCP project needed)
- **Replacement:** Better long-term choice vs. gcloud scripting — auto-updates with Google API surface
