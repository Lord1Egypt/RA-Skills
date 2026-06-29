---
name: run-workflow-weaver
description: "API documentation generator and diagram creator. Turn OpenAPI specs, API endpoints, and code snippets into visual workflows, process diagrams, and step-by-step guides. Export to Markdown, SVG, PNG, PDF, or JSON. Built on Workflow Weaver (weaver.vibingfun.com). Drive via CLI or 23 MCP tools. Use when asked to create API docs, generate diagrams, build process guides, or turn code into visual workflows."
tags:
  - api-documentation
  - openapi
  - diagram
  - workflow
  - mcp
  - process-documentation
  - generator
  - markdown
  - svg
  - pdf
  - png
  - json
  - cli
  - agent
  - byok
  - dev-tools
  - visualization
---

# run-workflow-weaver

Agent skill for driving the [workflow-weaver](https://www.npmjs.com/package/workflow-weaver) CLI and MCP server headlessly. Works from any agent runtime that can invoke subprocesses or connect to an MCP host.

## Prerequisites

- Node.js ≥ 20
- Global install:
  ```bash
  npm install -g workflow-weaver @workflow-weaver/mcp
  ```

## Authentication

**Interactive (recommended for first-time setup):**

```bash
workflow-weaver auth login --email you@example.com
# Password is prompted interactively — omit --password to avoid exposing it in shell history
***

**Non-interactive (agents / CI):**

Export the token after interactive login:

```bash
node -e "process.stdout.write(require(require('os').homedir()+'/.workflow-weaver/config.json').refreshToken)"
```

Then set it in the agent's environment:

```bash
export WORKFLOW_WEAVER_REFRESH_TOKEN=***
```

The CLI automatically reads `WORKFLOW_WEAVER_REFRESH_TOKEN` from the environment. No prefix mapping is needed.

## Security

| Rule | Detail |
|------|--------|
| No hardcoded credentials | Never embed tokens, passwords, or keys in scripts, logs, or skill files |
| Refresh token via env var only | `WORKFLOW_WEAVER_REFRESH_TOKEN` — never interpolate into log lines or `echo` |
| Supabase credentials via env var only | `WORKFLOW_WEAVER_SUPABASE_URL` and `WORKFLOW_WEAVER_SUPABASE_KEY` — never in scripts |
| Config file path | `~/.workflow-weaver/config.json` (chmod 600) — document but never read directly in automation scripts; one-time setup extraction is acceptable |
| Stripe/billing URLs | Present to the user to open in a browser — never open programmatically |
| Smoke placeholder | Use clearly-named placeholders like `smoke-test-invalid-token`, never real-looking values |

## Run (Agent Path)

### CLI subprocess pattern

All commands support `--json` for machine-readable NDJSON output:

```bash
workflow-weaver <command> [args] --json
```

### Exit codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | Domain error (`WorkflowWeaverError`) — check stderr for JSON |
| `2` | Unexpected error |

### Core 6-step sequence

```bash
# 1. Verify credentials
workflow-weaver auth status --json

# 2. Check quota before generating
workflow-weaver billing status --json

# 3. Create a project
PROJECT=$(workflow-weaver projects create \
  --title "Stripe Guide" \
  --use-case "Payment integration" \
  --json)
PROJECT_ID=$(echo "$PROJECT" | jq -r '.id')

# 4. Add a source
workflow-weaver sources add "$PROJECT_ID" \
  --type snippet \
  --content "GET /users" \
  --json

# 5. Generate (streams progress events as NDJSON, final line is the completed version)
GENERATE_OUTPUT=$(workflow-weaver generate "$PROJECT_ID" --json)
echo "$GENERATE_OUTPUT" | tail -1
VERSION_ID=$(echo "$GENERATE_OUTPUT" | tail -1 | jq -r '.versionId // .id')

# 6. Export
workflow-weaver export "$PROJECT_ID" "$VERSION_ID" --format md
```

### Error handling for agents

On any `WorkflowWeaverError` (exit code 1), stderr contains JSON:

```json
{ "error": "Project has no sources", "code": "PRECONDITION_FAILED", "statusCode": 400 }
```

### Quota exhaustion / BYOK

When `billing status --json` returns `canGenerate: false`:

| Resolution | Action |
|------------|--------|
| Subscribe | `workflow-weaver billing subscribe` → present Stripe URL to user |
| Buy credits | `workflow-weaver billing buy-credits` → present Stripe URL to user |
| BYOK | `workflow-weaver providers set-key <provider>` — bypasses quota entirely |

If `byok_active: true`, generation is unlimited regardless of plan or credits.

### Token rotation gotcha

The refresh token in `~/.workflow-weaver/config.json` may be rotated (invalidated and replaced) by the server. **Never cache the token by reading the config file directly.**

- Always pass the token via `WORKFLOW_WEAVER_REFRESH_TOKEN` env var
- If you must read from config, re-read before every operation — do not cache
- The CLI handles token refresh internally; let it read from its config file
- When using the env var, each CLI call may rotate the token server-side. The CLI writes the new token to `~/.workflow-weaver/config.json`, but the env var still holds the old value. For long-running agent sessions, prefer letting the CLI read from its config file rather than setting the env var persistently

## MCP Server Configuration

The MCP server requires **three** env vars: `WORKFLOW_WEAVER_REFRESH_TOKEN`, `WORKFLOW_WEAVER_SUPABASE_URL`, and `WORKFLOW_WEAVER_SUPABASE_KEY`.

### Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "workflow-weaver": {
      "command": "npx",
      "args": ["@workflow-weaver/mcp@latest"],
      "env": {
        "WORKFLOW_WEAVER_REFRESH_TOKEN": "***",
        "WORKFLOW_WEAVER_SUPABASE_URL": "***",
        "WORKFLOW_WEAVER_SUPABASE_KEY": "***"
      }
    }
  }
}
```

### Cursor

Edit `.cursor/mcp.json` in your project root (or `~/.cursor/mcp.json` globally):

```json
{
  "mcpServers": {
    "workflow-weaver": {
      "command": "npx",
      "args": ["@workflow-weaver/mcp@latest"],
      "env": {
        "WORKFLOW_WEAVER_REFRESH_TOKEN": "***",
        "WORKFLOW_WEAVER_SUPABASE_URL": "***",
        "WORKFLOW_WEAVER_SUPABASE_KEY": "***"
      }
    }
  }
}
```

### Kiro

Edit `.kiro/settings/mcp.json` in your workspace:

```json
{
  "mcpServers": {
    "workflow-weaver": {
      "command": "npx",
      "args": ["@workflow-weaver/mcp@latest"],
      "env": {
        "WORKFLOW_WEAVER_REFRESH_TOKEN": "***",
        "WORKFLOW_WEAVER_SUPABASE_URL": "***",
        "WORKFLOW_WEAVER_SUPABASE_KEY": "***"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

> **Note:** If you installed `@workflow-weaver/mcp` globally, you can also use the `workflow-weaver-mcp` binary directly instead of `npx`.

## MCP Tools (23)

| # | Tool | Description |
|---|------|-------------|
| 1 | `get_auth_status` | Verify the configured token |
| 2 | `list_projects` | List all projects |
| 3 | `create_project` | Create a new project |
| 4 | `get_project` | Get a project by ID |
| 5 | `delete_project` | Delete a project |
| 6 | `add_source` | Add an API doc source to a project |
| 7 | `list_sources` | List sources for a project |
| 8 | `remove_source` | Remove a source from a project |
| 9 | `list_providers` | List AI providers and key status |
| 10 | `set_provider_key` | Store a BYOK provider key |
| 11 | `remove_provider_key` | Remove a provider key |
| 12 | `generate_workflow` | Generate a workflow from sources |
| 13 | `list_versions` | List workflow versions |
| 14 | `get_version` | Get a specific version |
| 15 | `patch_version` | Apply a JSON Patch (RFC 6902) to a version |
| 16 | `chat_edit` | Edit a version via natural language |
| 17 | `export_version` | Export a version (svg/png/pdf/md/json) |
| 18 | `create_share_link` | Create a public share link |
| 19 | `list_share_links` | List share links |
| 20 | `revoke_share_link` | Revoke a share link |
| 21 | `get_billing_status` | Check plan, usage, and quota |
| 22 | `get_checkout_url` | Get a Stripe checkout URL |
| 23 | `get_portal_url` | Get a Stripe customer portal URL |

### MCP error handling

All tool errors return `isError: true` with JSON in `content[0].text`:

```json
{ "code": "INVALID_PARAMS", "message": "project_id is required" }
{ "code": "QUOTA_EXCEEDED", "message": "...", "resolution_paths": [...] }
{ "code": "AUTH_FAILED", "message": "Token is not authenticated" }
```

## Smoke Test

Run offline checks (no token required):

```bash
bash .claude/skills/run-workflow-weaver/smoke.sh
```

Run with live credentials:

```bash
WORKFLOW_WEAVER_REFRESH_TOKEN=*** bash .claude/skills/run-workflow-weaver/smoke.sh
```

## Global Flags

| Flag | Description |
|------|-------------|
| `--json` | Output as newline-delimited JSON (NDJSON) |
| `--quiet` | Suppress all non-error output |
| `--api-url <url>` | Override the Supabase URL |
| `--version` | Print CLI version |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `WORKFLOW_WEAVER_REFRESH_TOKEN` | Refresh token (read by CLI and MCP automatically) |
| `WORKFLOW_WEAVER_SUPABASE_URL` | Supabase project URL (required by MCP) |
| `WORKFLOW_WEAVER_SUPABASE_KEY` | Supabase anon key (required by MCP) |
| `WORKFLOW_WEAVER_CLI` | Override CLI binary path (default: `workflow-weaver`) |
| `WORKFLOW_WEAVER_MCP` | Override MCP binary path (default: `workflow-weaver-mcp`) |
