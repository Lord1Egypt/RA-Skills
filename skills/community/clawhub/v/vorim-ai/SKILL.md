---
name: vorim
description: AI agent identity, permissions, trust scores, and audit trails via Vorim AI. Gives your OpenClaw agent a cryptographic identity so every action is verified, permissioned, and logged.
license: MIT-0
metadata:
  openclaw:
    primaryEnv: VORIM_API_KEY
    requires:
      bins: [mcporter]
      env: [VORIM_API_KEY]
    tags:
      - security
      - identity
      - trust
      - audit
      - permissions
    homepage: https://vorim.ai
    repository: https://github.com/Kzino/vorim-openclaw-skill
---

# Vorim AI — Agent Identity & Trust

You have access to Vorim AI for agent identity, permissions, and audit trails. Use these capabilities to verify your identity, check permissions before taking actions, and log what you do.

## Setup

1. **Create a free account** at https://vorim.ai (no credit card required)
2. **Get your API key** from Settings → API Keys
3. **Set the environment variable:**
```
VORIM_API_KEY=agid_sk_live_...
```

The free tier includes 3 agents with full access.

## When to Use Vorim

### Before Taking Sensitive Actions
Before performing any action that modifies data, sends messages, executes code, makes payments, or accesses external services, check if you have permission:

Use the MCP tool `vorim_check_permission` with:
- `agent_id`: your registered Vorim agent ID
- `scope`: the permission level needed

Available scopes (least to most privileged):
- `agent:read` — browsing, searching, reading data
- `agent:write` — creating files, sending messages, editing data
- `agent:execute` — running shell commands, scripts, automations
- `agent:transact` — making purchases, payments, financial actions
- `agent:communicate` — sending emails, posting to social media
- `agent:delegate` — granting permissions to other agents
- `agent:elevate` — escalating privileges

If permission is denied, inform the user and do not proceed.

### After Every Action
Log what you did by emitting an audit event using `vorim_emit_event`:
- `agent_id`: your Vorim agent ID
- `event_type`: one of `tool_call`, `api_request`, `message_sent`, `permission_change`, `status_change`
- `action`: what you did (e.g., `send_email`, `run_script`, `read_file`)
- `result`: `success`, `denied`, or `error`

### To Verify Your Identity
When interacting with external services or other agents, you can prove your identity using `vorim_verify_trust`. This returns your trust score (0-100), active permissions, and cryptographic fingerprint.

### To Register (First Run)
On first use, register this OpenClaw instance as a Vorim agent using `vorim_register_agent`:
- `name`: a descriptive name (e.g., "kwame-openclaw-macbook")
- `capabilities`: what this agent can do (e.g., ["browse", "email", "shell", "calendar"])
- `scopes`: permissions to request (e.g., ["agent:read", "agent:write", "agent:execute"])

Save the returned `agent_id` — you'll need it for all subsequent operations.

## MCP Integration

Vorim tools are available via the `@vorim/mcp-server` MCP server. The following tools are available:

| Tool | Purpose |
|------|---------|
| `vorim_ping` | Check API connectivity |
| `vorim_register_agent` | Register this agent (first run) |
| `vorim_get_agent` | Get agent details |
| `vorim_list_agents` | List all agents |
| `vorim_update_agent` | Update agent metadata |
| `vorim_revoke_agent` | Permanently revoke an agent |
| `vorim_check_permission` | Check if action is allowed (do this before sensitive actions) |
| `vorim_grant_permission` | Grant a permission scope |
| `vorim_list_permissions` | List active permissions |
| `vorim_revoke_permission` | Revoke a permission |
| `vorim_emit_event` | Log an audit event (do this after every action) |
| `vorim_export_audit` | Export signed audit bundle |
| `vorim_verify_trust` | Verify identity and trust score |
| `vorim_register_ephemeral` | Create a short-lived agent |
| `vorim_delegate_credential` | Delegate credentials to another agent |
| `vorim_request_token` | Request a short-lived access token |
| `vorim_list_delegations` | List credential delegations |

## Behavioral Guidelines

1. **Always check permission before destructive or external actions** — this protects the user
2. **Always log actions** — the audit trail is the user's proof of what happened
3. **Be transparent about your identity** — when asked, share your Vorim agent ID and trust score
4. **Respect denied permissions** — if a permission check returns denied, do not attempt the action
5. **Register once, reuse forever** — save your agent_id after first registration

## Links

- Website: https://vorim.ai
- Documentation: https://vorim.ai/docs
- npm: https://www.npmjs.com/package/@vorim/mcp-server
- IETF Draft: draft-vorim-vaip-00
