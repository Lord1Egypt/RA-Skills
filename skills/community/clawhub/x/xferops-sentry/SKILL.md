---
name: xferops-sentry
description: Query Sentry issues, events, and projects via MCP for XferOps incident investigation and triage. Requires @sentry/mcp-server and a Sentry API token.
---

# Sentry MCP

Error tracking and triage via MCP (Model Context Protocol).

## Setup

Install the MCP server:

```bash
npx -y @sentry/mcp-server --skills=inspect,triage
```

Configure in your MCP client (e.g., `~/.mcporter/mcporter.json`):

```json
{
  "mcpServers": {
    "sentry": {
      "command": "npx",
      "args": ["-y", "@sentry/mcp-server", "--skills=inspect,triage"],
      "env": {
        "SENTRY_ACCESS_TOKEN": "your-token-here"
      }
    }
  }
}
```

Set `SENTRY_ACCESS_TOKEN` to a Sentry User Auth Token with API access.

## Tools (8 total)

### Organizations & Projects
- `list_organizations` — List organizations available to the token
- `list_projects` — List projects in an organization

### Issues
- `list_issues` — List issues in an organization (requires `organizationSlug`)
- `get_issue` — Get details for a specific issue (requires `organizationSlug`, `issueId`)

### Events
- `list_events` — List events for an issue (requires `organizationSlug`, `issueId`)
- `get_event` — Get details for an event (requires `organizationSlug`, `eventId`)

### AI Workflows
- `inspect` — AI-powered issue inspection
- `triage` — AI-powered triage assistance

## Common Patterns

### List organizations

```bash
mcporter call sentry.list_organizations
```

### List projects

```bash
mcporter call sentry.list_projects organizationSlug=xferops
```

### List issues

```bash
mcporter call sentry.list_issues organizationSlug=xferops
```

### Get issue details

```bash
mcporter call sentry.get_issue organizationSlug=xferops issueId=XFEROPS-AUTH-1
```

### List events for an issue

```bash
mcporter call sentry.list_events organizationSlug=xferops issueId=XFEROPS-AUTH-1
```

## XferOps Notes

- Default organization: `xferops`
- Token may be stored in Secrets Manager as `xferops/sentry/api-token`
- This setup is already configured on Adam's machine
