---
name: tempo-api-mcp
description: Access Tempo time-tracking data via MCP. Use when the user asks about Tempo worklogs, plans, teams, accounts, or wants to log time, check resource allocations, or manage timesheet approvals. Triggers on phrases like "log my time in Tempo", "how many hours did I log this week", "check my team's worklogs", "what's the resource plan for this sprint", or any request involving Jira/Tempo time tracking. Requires tempo-api-mcp installed and the tempo server registered (see Setup below).
---

# tempo-api-mcp

MCP server for Tempo — natural-language time-tracking and resource planning via the Tempo API.

- **npm:** [npmjs.com/package/tempo-api-mcp](https://www.npmjs.com/package/tempo-api-mcp)
- **Source:** [github.com/chrischall/tempo-api-mcp](https://github.com/chrischall/tempo-api-mcp)

## Setup

### Option A — npx (recommended)

Add to `.mcp.json` in your project or `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "tempo": {
      "command": "npx",
      "args": ["-y", "tempo-api-mcp"],
      "env": {
        "TEMPO_API_TOKEN": "your-api-token-here"
      }
    }
  }
}
```

### Option B — from source

```bash
git clone https://github.com/chrischall/tempo-api-mcp
cd tempo-api-mcp
npm install && npm run build
```

Then add to `.mcp.json`:

```json
{
  "mcpServers": {
    "tempo": {
      "command": "node",
      "args": ["/path/to/tempo-api-mcp/dist/index.js"],
      "env": {
        "TEMPO_API_TOKEN": "your-api-token-here"
      }
    }
  }
}
```

Or use a `.env` file in the project directory with `TEMPO_API_TOKEN=<value>`.

### Getting your API token

1. Log in to your Tempo workspace
2. Go to **Settings → API integration**
3. Create a new token and copy it

## Authentication

Bearer token auth — attached to every request as `Authorization: Bearer <token>`.

## Tools

### Worklogs
| Tool | Description |
|------|-------------|
| `tempo_get_worklogs` | List worklogs with optional filters (project, issue, date range) |
| `tempo_get_worklog(id)` | Get a single worklog by id |
| `tempo_create_worklog(authorAccountId, issueId, startDate, timeSpentSeconds, ...)` | Log time against a Jira issue |
| `tempo_update_worklog(id, authorAccountId, startDate, timeSpentSeconds, ...)` | Update an existing worklog |
| `tempo_delete_worklog(id)` | Delete a worklog |
| `tempo_search_worklogs(authorIds?, issueIds?, projectIds?, from?, to?, ...)` | Advanced search via POST |
| `tempo_get_worklogs_by_user(accountId, from?, to?)` | All worklogs for a user |
| `tempo_get_worklogs_by_project(projectId, from?, to?)` | All worklogs for a Jira project |
| `tempo_get_worklogs_by_issue(issueId, from?, to?)` | All worklogs for a Jira issue |
| `tempo_get_worklogs_by_team(teamId, from?, to?)` | All worklogs for a Tempo team |
| `tempo_get_worklogs_by_account(accountKey, from?, to?)` | All worklogs for a Tempo account |

### Plans (Resource Allocations)
| Tool | Description |
|------|-------------|
| `tempo_get_plans(from, to, ...)` | List plans for a date range |
| `tempo_get_plan(id)` | Get a single plan by id |
| `tempo_create_plan(assigneeId, assigneeType, planItemId, planItemType, startDate, endDate, ...)` | Create a resource allocation plan |
| `tempo_update_plan(id, ...)` | Update an existing plan |
| `tempo_delete_plan(id)` | Delete a plan |

### Teams
| Tool | Description |
|------|-------------|
| `tempo_get_teams(...)` | List teams with optional filters |
| `tempo_get_team(id)` | Get a single team by id |
| `tempo_create_team(name, ...)` | Create a new team |
| `tempo_update_team(id, name, ...)` | Update a team |
| `tempo_delete_team(id)` | Delete a team |
| `tempo_get_team_memberships(...)` | List team memberships |
| `tempo_search_team_memberships(...)` | Advanced membership search via POST |

### Accounts
| Tool | Description |
|------|-------------|
| `tempo_get_accounts()` | List all accounts (OPEN and CLOSED) |
| `tempo_get_account(key)` | Get a single account by key |
| `tempo_search_accounts(...)` | Search accounts by status, category, or project |
| `tempo_create_account(key, name, ...)` | Create a new account |
| `tempo_update_account(key, name, ...)` | Update an account |
| `tempo_delete_account(key)` | Delete an account |
| `tempo_get_account_categories()` | List all account categories |

### Projects & Timesheets
| Tool | Description |
|------|-------------|
| `tempo_get_projects()` | List Tempo Financial Manager projects |
| `tempo_get_project(id)` | Get a project by id |
| `tempo_get_timesheet_approval_status(accountId, from?, to?)` | Get timesheet approval status for a user |
| `tempo_get_timesheet_approvals_waiting()` | List timesheets waiting for approval |
| `tempo_search_timesheet_approval_logs(...)` | Search approval audit logs |
| `tempo_get_periods(from?, to?)` | Get Tempo period definitions |
| `tempo_get_user_schedule(accountId, from, to)` | Get a user's work schedule |
| `tempo_get_global_configuration()` | Get global Tempo settings |
| `tempo_get_work_attributes()` | List custom worklog attributes |
| `tempo_get_roles()` | List all Tempo roles |

## Workflows

**Log time for today:**
```
tempo_create_worklog(authorAccountId, issueId, startDate: "today", timeSpentSeconds: 3600)
```

**See this week's time for a user:**
```
tempo_get_worklogs_by_user(accountId, from: "2026-03-16", to: "2026-03-20")
```

**Check resource plan for a project:**
```
tempo_get_plans(from: "2026-03-01", to: "2026-03-31", projectIds: [123])
```

**Find all worklogs for an issue:**
```
tempo_get_worklogs_by_issue(issueId: 456, from: "2026-01-01")
```

**Review pending timesheet approvals:**
```
tempo_get_timesheet_approvals_waiting()
tempo_get_timesheet_approval_status(accountId, from: "2026-03-01", to: "2026-03-31")
```

## Notes

- `timeSpentSeconds` is always an integer (e.g. `3600` = 1 hour, `1800` = 30 min)
- `authorAccountId` is the Atlassian account id (not a username) — required for all worklog operations
- `tempo_get_plans` requires both `from` and `to` — no other filter is mandatory
- Default pagination limit is 50 for most endpoints; use `offset` + `limit` to page through results
- `tempo_delete_worklog` is a hard delete — there is no restore

## Acknowledgement of Terms

By using this MCP server, you acknowledge and agree to the following:

**1. This server accesses your own Tempo account via Tempo's official API.** Auth happens via your own per-user OAuth/API token, issued by your Tempo/Jira instance. It does not — and cannot — access anyone else's worklogs or your colleagues' time entries.

**2. [Tempo's Terms of Use](https://www.tempo.io/terms-of-use) govern your use of this server**. The clauses most relevant here:

> Your registration is solely for your personal use, and you shall not authorize others to use your account.

And: users must not "automate the use of the Service, such as by using scripts" — *except* via documented APIs (Section 5.3.2(v)). API tokens are the sanctioned automation mechanism — that's what this server uses.

You are agreeing to those terms — read by the maintainer 2026-05-23 — every time you invoke a tool in this server.

**3. Personal, single-user use only.** This project is not affiliated with, endorsed by, sponsored by, or in partnership with Tempo Software ehf or Atlassian. It is a personal automation tool for one Tempo-licensed user to drive their own worklogs and reports. Do not use it to log time on behalf of colleagues, to bulk-export reports across an org for resale, or to share your token with anyone else.

**4. Your token is yours alone.** Tempo issues per-user OAuth/API tokens; **do not commit `TEMPO_API_TOKEN` to git**, do not paste it in shared chats, and rotate it if it's ever exposed.

**5. Your employer's policy may add restrictions.** Tempo is typically licensed via Jira to an organization. Your employer may have IT/security/acceptable-use policies that further restrict scripted automation against Jira/Tempo — even when Tempo's own ToU allows it. **Check with your employer's IT/Jira admin** before automating against a corporate Tempo instance.

**6. You accept full responsibility** for any consequences of using this server in connection with your Tempo account — rate limiting, token revocation, account warnings, your IT admin emailing you, or any enforcement action. If Tempo or your employer objects to your use, stop using this server.

This section is the maintainer's good-faith summary of the terms — it is not legal advice and does not modify or supersede Tempo's actual ToU or your employer's policies.
