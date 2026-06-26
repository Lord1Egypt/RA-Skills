---
name: vercel-deployments
description: Manage Vercel projects, deployments, domains, environment variables, and team resources via the Vercel REST API. Use this skill when users want to inspect deployments, manage projects, configure domains, or automate Vercel DevOps workflows.
---

# Vercel

![Vercel](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/vercel-dark.svg)

Manage Vercel projects, deployments, domains, environment variables, and team resources from chat via the Vercel REST API.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=vercel-deployments) for hosted connection flows and credentials so you do not need to configure Vercel API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Vercel |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Vercel |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│  Vercel REST     │
│   (User Chat)   │     │   (OAuth)    │     │      API         │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect Vercel    │                       │
         │                       │  4. Secure Token       │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │  Vercel │
   │  File    │           │ Auth     │           │ Account │
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Vercel again."

## Quick Start

```bash
# List projects
clawlink_call_tool --tool "vercel_list_projects" --params '{}'

# Get deployment details
clawlink_call_tool --tool "vercel_get_deployment" --params '{"deployment_id": "DEPLOYMENT_ID"}'

# List deployments
clawlink_call_tool --tool "vercel_list_deployments" --params '{"project_name": "my-project"}'
```

## Authentication

All Vercel tool calls are authenticated automatically by ClawLink using the user's connected Vercel account token.

**No API token is required in chat.** ClawLink stores the token securely and injects it into every Vercel API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=vercel and connect Vercel.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `vercel` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration vercel
```

**Response:** Returns the live tool catalog for Vercel.

### Reconnect

If Vercel tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=vercel
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration vercel`

## Security & Permissions

- Access is scoped to the Vercel account connected during OAuth setup and the scopes granted.
- **All write operations (deploy, create project, update settings, add domains) require explicit user confirmation.**
- Destructive operations (delete deployment, remove domain) are high-impact and must be confirmed.
- Environment variable changes can affect running deployments — confirm before modifying.

## Tool Reference

### Projects

| Tool | Description | Mode |
|------|-------------|------|
| `vercel_list_projects` | List all projects in the account/team | Read |
| `vercel_get_project` | Get project configuration and settings | Read |
| `vercel_create_project` | Create a new project | Write |
| `vercel_update_project` | Update project name, framework, or settings | Write |
| `vercel_delete_project` | Delete a project and its deployments | Write |

### Deployments

| Tool | Description | Mode |
|------|-------------|------|
| `vercel_list_deployments` | List deployments with pagination and filters | Read |
| `vercel_get_deployment` | Get deployment details including status and URLs | Read |
| `vercel_create_deployment` | Create a new deployment | Write |
| `vercel_cancel_deployment` | Cancel an in-progress deployment | Write |
| `vercel_delete_deployment` | Delete a deployment | Write |

### Domains

| Tool | Description | Mode |
|------|-------------|------|
| `vercel_list_domains` | List all domains in the account | Read |
| `vercel_get_domain` | Get domain details and DNS records | Read |
| `vercel_add_domain` | Add a domain to a project | Write |
| `vercel_remove_domain` | Remove a domain from a project | Write |
| `vercel_verify_domain` | Verify domain ownership | Write |

### Environment Variables

| Tool | Description | Mode |
|------|-------------|------|
| `vercel_list_env` | List environment variables for a project | Read |
| `vercel_add_env` | Add an environment variable to a project | Write |
| `vercel_update_env` | Update an environment variable's value or scope | Write |
| `vercel_delete_env` | Remove an environment variable | Write |

### Teams & Members

| Tool | Description | Mode |
|------|-------------|------|
| `vercel_list_team_members` | List all members of a team | Read |
| `vercel_invite_team_member` | Invite a new member to the team | Write |
| `vercel_remove_team_member` | Remove a member from the team | Write |
| `vercel_update_team_member_role` | Change a member's role | Write |

### Secrets

| Tool | Description | Mode |
|------|-------------|------|
| `vercel_list_secrets` | List all secrets in the account | Read |
| `vercel_create_secret` | Create a secret for use in environment variables | Write |
| `vercel_delete_secret` | Delete a secret | Write |

### Logs & Events

| Tool | Description | Mode |
|------|-------------|------|
| `vercel_get_deployment_events` | Get deployment event log | Read |
| `vercel_get_audit_logs` | Get team audit logs | Read |

## Code Examples

### List all projects

```bash
clawlink_call_tool --tool "vercel_list_projects" \
  --params '{
    "team_id": "team_id"
  }'
```

### Get deployment details

```bash
clawlink_call_tool --tool "vercel_get_deployment" \
  --params '{
    "deployment_id": "dpl_1234567890"
  }'
```

### List deployments for a project

```bash
clawlink_call_tool --tool "vercel_list_deployments" \
  --params '{
    "project_name": "my-nextjs-app",
    "limit": 10
  }'
```

### Add an environment variable

```bash
clawlink_call_tool --tool "vercel_add_env" \
  --params '{
    "project_name": "my-nextjs-app",
    "key": "DATABASE_URL",
    "value": "postgres://...",
    "environment": "production"
  }'
```

### Verify a domain

```bash
clawlink_call_tool --tool "vercel_verify_domain" \
  --params '{
    "domain": "example.com"
  }'
```

### Cancel a deployment

```bash
clawlink_call_tool --tool "vercel_cancel_deployment" \
  --params '{
    "deployment_id": "dpl_1234567890"
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Vercel is connected.
2. Call `clawlink_list_tools --integration vercel` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `vercel`.
5. If no Vercel tools appear, direct the user to https://claw-link.dev/dashboard?add=vercel.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → describe                                      │
│                                                             │
│  Example: List projects → Get deployments → Show status     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  describe → preview → confirm → call                        │
│                                                             │
│  Example: Preview env var change → User approves → Update   │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Deployment IDs start with `dpl_` and project names are used in deployment URLs.
- Environment variables can be scoped to `development`, `preview`, or `production` environments.
- Domain verification requires adding DNS records — check the verification status with `vercel_get_domain`.
- Deleted deployments cannot be restored.
- Team operations require the authenticated user to be a team owner or admin.
- Vercel uses a specific deployment URL format: `https://project.vercel.app`.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration vercel`. |
| Missing connection | Vercel is not connected. Direct the user to https://claw-link.dev/dashboard?add=vercel. |
| `Project not found` | The project name does not exist in the account. |
| `Deployment not found` | The deployment ID does not exist. |
| `Domain not found` | The domain is not registered with the account. |
| `Domain not verified` | Domain ownership has not been verified. Add DNS records first. |
| `Env not found` | The environment variable does not exist in the project. |
| `Forbidden` | The account lacks permission for this operation. |
| Write rejected | User did not confirm a write action. Always confirm before executing writes. |

### Troubleshooting: Tools Not Visible

1. Check that the ClawLink plugin is installed:
   ```bash
   openclaw plugins list
   ```
2. If the plugin is installed but tools are missing, tell the user to send `/new` as a standalone message to reload the catalog.
3. If a fresh chat does not help, run:
   ```bash
   openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
   openclaw gateway restart
   ```
4. After restart, tell the user to send `/new` again and retry.

## Resources

- [Vercel REST API Documentation](https://vercel.com/docs/rest-api)
- [Vercel API Reference](https://vercel.com/docs/rest-api)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=vercel-deployments
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=vercel-deployments)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)