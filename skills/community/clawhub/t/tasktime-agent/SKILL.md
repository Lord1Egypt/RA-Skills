---
name: tasktime
description: >-
  TaskTime Pro is a free, open-source, local-first work manager for freelancers,
  covering tasks, timers, expenses, invoices, and reports. Core use requires no
  TaskTime account or cloud sync, works offline after the PWA is loaded or
  installed, and stores work records in the browser. This first-party TaskTime
  Pro skill lets same-device agents operate the app through scoped access and
  approval controls.
version: 1.3.0
metadata:
  openclaw:
    requires:
      bins:
        - node
    install:
      - kind: node
        package: "@tasktimepro/agent-bridge"
        bins:
          - tasktime-agent-bridge
    skillKey: tasktime
    homepage: https://tasktime.pro/agents/openclaw/
---

# TaskTime Pro

Use this skill when a user asks you to work with TaskTime Pro through its local agent bridge: plan or update work, manage tasks and clients, track time, prepare invoice data, inspect reports, handle expenses, open app review screens, or recover agent setup.

Stay on the supported TaskTime Pro bridge surface. Do not directly edit browser storage, Yjs documents, Google Drive sync files, invoice records, billing state, or other persisted app data outside TaskTime Pro tools.

## Skill Scope

This is the first-party portable ClawHub skill published by TaskTime Pro as `@tasktimepro/tasktime-agent`. It should guide agent clients that need safe TaskTime Pro access through MCP. If a repository or user environment also provides local TaskTime Pro instructions, read those too because they may contain the active app URL, workspace policy, or deployment-specific setup notes.

TaskTime Pro is free and open source. Core use requires no TaskTime account or cloud sync, works offline after the PWA is loaded or installed, and stores work records in browser-local storage. The production app sends limited aggregate usage metrics without project, task, client, invoice, expense, note, or time-entry content.

The paired browser app is the authority for customer data, validation, navigation, downloads, email sends, sync behavior, backups, restore flows, and account deletion. The bridge is a same-device MCP stdio server that forwards approved commands to that visible app session; it is not a remote API.

## Connection

Prefer the MCP server when the client exposes it. For a standalone install, the standard stdio command is:

```json
{
  "mcpServers": {
    "tasktime": {
      "command": "tasktime-agent-bridge",
      "args": ["--app-url", "https://app.tasktime.pro"]
    }
  }
}
```

If the binary is not already installed, install the bridge package or let OpenClaw install it from the skill metadata:

```bash
npm install -g @tasktimepro/agent-bridge
```

For OpenClaw, prefer the complete native plugin installed with `openclaw plugins install @tasktimepro/openclaw`. Its Gateway service owns one vendored bridge across ordinary turns. Do not launch another bridge manually. The bundled `.mcp.json` is a compatibility artifact for non-native hosts; OpenClaw's native format takes precedence.

The user grants first-use access in TaskTime Pro under Account > Agent Access. Require a running, paired browser session before reading or mutating data. After pairing, call `tools/list` because available tools depend on the granted scopes. Default scopes are `read`, `write`, and `navigation`; optional scopes are `billing`, `export`, and `email`. Current TaskTime Pro app builds show scopes after connection; do not tell the user to select scopes in the app unless a future scope picker is visible.

OpenClaw may expose tools with the MCP server prefix, for example `tasktime__list_projects` instead of `list_projects`.

For OpenClaw-managed installs, pair TaskTime Pro only to the Gateway-owned native bridge. Use `tasktime__get_pairing_status` and `tasktime__refresh_pairing` (or the unprefixed names when exposed that way) to obtain the exact endpoint, short-lived launch URL, stable agent identity, pairing expiry, and session state.

The OpenClaw plugin uses the stable display identity `tasktime.agent.openclaw` with the label `OpenClaw on this device`; that string is not authentication. The WebSocket port is dynamic. A refresh resumes from a current-tab session record. Closing and reopening TaskTime in the same browser profile uses a non-exportable proof-of-possession key to receive a fresh session without durably storing a bearer token. Re-pair after a Gateway/bridge restart, explicit disconnect, revoke, disable, expiry, forgotten browser authorization, or definitive reconnect rejection.

If a native tool returns `legacy_mcp_conflict`, an older `mcp.servers.tasktime` owner is still enabled. Ask the user to disable that exact legacy TaskTime entry and restart the Gateway; do not remove config silently and do not start or kill another bridge.

Trusted chat approvals default to until revoked for stable same-device managed agents. Shorter trust durations may be available, but do not tell the user they must re-trust every 30 days unless they chose a 30-day grant.

## Operating Workflow

1. Use MCP tools for TaskTime Pro data work. Use browser UI automation only for visual validation or unsupported workflows.
2. Inspect before changing data. Start with list, preview, or read tools before write, billing, export, email, restore, or delete tools.
3. For invoice and quote work, preview unbilled work before creating drafts, finalizing invoices, exporting PDFs, or sending email. Before canceling an eligible unpaid invoice, inspect it and explain that cancellation is terminal, retains its number, and releases its owned source work.
4. For navigation work, use `open_*` view tools to bring the user to the relevant visible app screen for review.
5. For approval-gated actions, use a valid exact-input TaskTime Pro approval token created through `tasktime/create_approval_token`, or let the browser-visible approval prompt handle the action. Do not reuse tokens for changed inputs.
6. Keep the user in control for invoice finalization or cancellation, email sending, export, account data deletion, restore, sync wiping, and cascade deletes.

## Free and Pro Boundaries

- Free supports one active client at a time. Existing clients remain readable and editable, and archived clients remain restorable when the active-client count permits. If `create_client`, `unarchive_client`, or an archived-to-active `update_client` returns `ENTITLEMENT_REQUIRED`, do not bypass the check, archive another client without explicit user intent, or replay with a different idempotency key.
- `get_report_summary` is Free only with the exact `scope: "basic-current-month"` request and no advanced arguments. That response contains only current-month Received, Expenses, and Tracked time. Omitted scope, `scope: "advanced"`, advanced report sections/ranges/filters/rows, and report exports require Pro.
- Email preview, templates, invoice/quote PDF export, and manual delivery remain Free. TaskTime-hosted `send_invoice_email` and `send_project_quote_email` require a Pro trial or subscription plus fresh confirmation. Returning from trial or Checkout never authorizes an automatic send.
- When a send has an ambiguous outcome, call `get_email_send_status` with the original attempt ID. It is read-only, does not contact the provider, and must never be replaced by an automatic resend. Start a fresh send only after TaskTime reports the prior attempt rejected and the user confirms again.
- Treat `ENTITLEMENT_REQUIRED` and billing-suspension responses as policy results from the paired app. Use the supplied recovery route or `open_account_view` when the user wants to review Pro or billing; do not infer access from tool visibility alone.

## Useful First Tools

- `list_projects`, `list_clients`, and `list_tasks` to understand the current workspace.
- `get_pairing_status` and `refresh_pairing` for setup/recovery before app data tools are available.
- `get_active_timers`, `start_timer`, `pause_timer`, `resume_timer`, and `stop_timer` for time tracking.
- `create_project`, `create_client`, and `create_task` for normal setup and planning.
- `list_expenses` and expense category tools for expense review and entry.
- `find_unbilled_time` and `preview_invoice_from_unbilled_work` before invoice drafting.
- `list_invoices` before `cancel_invoice`; cancel only finalized unpaid invoices with the required reason, exact invoice-number confirmation, billing scope, and TaskTime Pro approval.
- `create_invoice_draft`, `preview_project_quote`, and invoice/quote email tools only within granted scopes and approval rules.
- `open_project_view`, `open_invoice_view`, `open_reports_view`, and other navigation tools to put the user on review screens.

## Recovery

If a tool call returns an unavailable app-session error with `launch_tasktime`, open or guide the user to TaskTime Pro, pair Account > Agent Access, then retry. Do not treat this as a generic MCP failure.

If `get_pairing_status` is available, inspect it before suggesting manual commands. If the status shows no paired app session, use its ephemeral `launchUrl`; if the pairing is expired or consumed, call `refresh_pairing` and use the new URL. Never copy pairing URLs into logs or durable notes. Never pair the app to a separately launched terminal bridge when OpenClaw already owns the integration.

If tool availability does not match the task, call `tools/list` again and check granted scopes. Ask the user to adjust TaskTime Pro Agent Access only when the missing scope is actually needed.

For task-and-time-management workflows, prefer this sequence: inspect projects/tasks, create or choose the task, start the timer, let the user work, later check active timers and stop the matching timer. A timer can reasonably run for hours; do not assume the session should expire after a short chat turn.

## Safety

- Never expose the bridge through public interfaces, tunnels, shared hosts, or remote control channels.
- Never mutate raw IndexedDB, Yjs documents, Google Drive sync files, invoice state, or billing state outside the TaskTime Pro bridge.
- Never ask the user to reset browser data, clear IndexedDB, or wipe Drive sync state as a normal fix.
- Never print pairing codes, approval tokens, authorization headers, exported account data, invoice PDFs, or email payloads unless the user explicitly asks for that artifact.
- Treat destructive, restore, billing, export, and email tools as high-impact operations: read or preview first, explain the intended action, then mutate only with explicit user intent and TaskTime Pro approval.

## Full Documentation

- Agent docs: https://tasktime.pro/agents/
- Quickstart: https://tasktime.pro/agents/quickstart/
- Security model: https://tasktime.pro/agents/security/
- MCP tool reference: https://tasktime.pro/agents/tools/
- Machine-readable MCP tools: https://tasktime.pro/agents/mcp-tools.json
- Bridge discovery manifest: https://tasktime.pro/.well-known/tasktime-agent.json
- Claude setup: https://tasktime.pro/agents/claude/
- OpenClaw setup: https://tasktime.pro/agents/openclaw/
- Debugging guide: https://tasktime.pro/agents/debugging/
