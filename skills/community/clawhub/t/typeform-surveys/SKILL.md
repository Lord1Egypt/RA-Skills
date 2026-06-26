---
name: typeform-surveys
description: Manage Typeform forms, responses, themes, workspaces, and webhooks via the Typeform API. Use this skill when users want to list forms, inspect responses, create forms, manage themes, or automate Typeform survey workflows.
---

# Typeform

![Typeform](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/typeform-dark.svg)

Manage Typeform forms, responses, themes, workspaces, and webhooks from chat via the Typeform API.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=typeform-surveys) for hosted connection flows and credentials so you do not need to configure Typeform API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Typeform |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Typeform |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│  Typeform API   │
│   (User Chat)   │     │   (OAuth)    │     │                  │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect Typeform   │                       │
         │                       │  4. Secure Token      │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │ Typeform │
   │  File    │           │ Auth     │           │ Account  │
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Typeform again."

## Quick Start

```bash
# List all forms
clawlink_call_tool --tool "typeform_list_forms" --params '{}'

# Get form details
clawlink_call_tool --tool "typeform_get_form" --params '{"form_id": "FORM_ID"}'

# List responses
clawlink_call_tool --tool "typeform_list_responses" --params '{"form_id": "FORM_ID"}'
```

## Authentication

All Typeform tool calls are authenticated automatically by ClawLink using the user's connected Typeform account OAuth token.

**No API token is required in chat.** ClawLink stores the OAuth token securely and injects it into every Typeform API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=typeform and connect Typeform.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `typeform` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration typeform
```

**Response:** Returns the live tool catalog for Typeform.

### Reconnect

If Typeform tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=typeform
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration typeform`

## Security & Permissions

- Access is scoped to forms and data accessible to the connected Typeform account.
- **Write operations (create form, update settings, delete responses) require explicit user confirmation.**
- Response data may contain personal information — handle in accordance with privacy best practices.
- Workspace operations may be restricted by Typeform plan level.

## Tool Reference

### Forms

| Tool | Description | Mode |
|------|-------------|------|
| `typeform_list_forms` | List all forms accessible to the account | Read |
| `typeform_get_form` | Get form details including fields and settings | Read |
| `typeform_create_form` | Create a new form | Write |
| `typeform_update_form` | Update a form's title, fields, or settings | Write |
| `typeform_delete_form` | Permanently delete a form | Write |
| `typeform_archive_form` | Archive a form | Write |

### Responses

| Tool | Description | Mode |
|------|-------------|------|
| `typeform_list_responses` | List responses for a form with pagination | Read |
| `typeform_get_response` | Get a specific response with all answers | Read |
| `typeform_delete_response` | Permanently delete a single response | Write |
| `typeform_delete_responses` | Delete multiple responses by ID | Write |
| `typeform_get_response_count` | Get the number of responses for a form | Read |

### Questions & Fields

| Tool | Description | Mode |
|------|-------------|------|
| `typeform_list_form_fields` | List all fields/questions in a form | Read |
| `typeform_create_form_field` | Add a new field to a form | Write |
| `typeform_update_form_field` | Update a field's label, type, or options | Write |
| `typeform_delete_form_field` | Remove a field from a form | Write |
| `typeform_reorder_form_fields` | Reorder fields in a form | Write |

### Logic & Settings

| Tool | Description | Mode |
|------|-------------|------|
| `typeform_get_form_logic` | Get the logic rules configured for a form | Read |
| `typeform_update_form_logic` | Add or update logic rules for a form | Write |
| `typeform_get_form_settings` | Get form settings (language, progress bar, etc.) | Read |
| `typeform_update_form_settings` | Update form settings | Write |

### Themes

| Tool | Description | Mode |
|------|-------------|------|
| `typeform_list_themes` | List all themes | Read |
| `typeform_get_theme` | Get a specific theme's design settings | Read |
| `typeform_create_theme` | Create a new theme | Write |
| `typeform_update_theme` | Update a theme's colors, fonts, or background | Write |
| `typeform_delete_theme` | Delete a theme | Write |

### Workspaces

| Tool | Description | Mode |
|------|-------------|------|
| `typeform_list_workspaces` | List all workspaces | Read |
| `typeform_get_workspace` | Get a workspace's details | Read |
| `typeform_create_workspace` | Create a new workspace | Write |
| `typeform_update_workspace` | Update a workspace's name | Write |
| `typeform_delete_workspace` | Delete an empty workspace | Write |

### Webhooks

| Tool | Description | Mode |
|------|-------------|------|
| `typeform_list_webhooks` | List all webhooks for a form | Read |
| `typeform_register_webhook` | Register a new webhook for a form | Write |
| `typeform_delete_webhook` | Remove a webhook from a form | Write |
| `typeform_get_webhook` | Get webhook details and recent deliveries | Read |

## Code Examples

### List all forms

```bash
clawlink_call_tool --tool "typeform_list_forms" \
  --params '{
    "page_size": 20
  }'
```

### Get form with fields

```bash
clawlink_call_tool --tool "typeform_get_form" \
  --params '{
    "form_id": "FORM_ID"
  }'
```

### List responses for a form

```bash
clawlink_call_tool --tool "typeform_list_responses" \
  --params '{
    "form_id": "FORM_ID",
    "page_size": 20,
    "completed": true
  }'
```

### Get a specific response

```bash
clawlink_call_tool --tool "typeform_get_response" \
  --params '{
    "form_id": "FORM_ID",
    "response_id": "RESPONSE_ID"
  }'
```

### Register a webhook

```bash
clawlink_call_tool --tool "typeform_register_webhook" \
  --params '{
    "form_id": "FORM_ID",
    "url": "https://example.com/webhook/typeform",
    "enabled": true
  }'
```

### Create a new workspace

```bash
clawlink_call_tool --tool "typeform_create_workspace" \
  --params '{
    "name": "Research Team"
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Typeform is connected.
2. Call `clawlink_list_tools --integration typeform` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `typeform`.
5. If no Typeform tools appear, direct the user to https://claw-link.dev/dashboard?add=typeform.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → describe                                      │
│                                                             │
│  Example: List forms → Get form fields → Review responses  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  describe → preview → confirm → call                         │
│                                                             │
│  Example: Preview form creation → User approves → Create   │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Form IDs are required for most operations — use `typeform_list_forms` to discover form IDs.
- Response IDs and field IDs are different — use `typeform_list_responses` and `typeform_list_form_fields` respectively.
- Deleted forms and responses cannot be recovered — always confirm before deleting.
- Webhooks require a publicly accessible HTTPS URL — they will not work with localhost.
- Typeform API has rate limits — the tool response will indicate if backoff is needed.
- Workspace operations (create, delete) may be restricted by the Typeform plan.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration typeform`. |
| Missing connection | Typeform is not connected. Direct the user to https://claw-link.dev/dashboard?add=typeform. |
| `Form not found` | The form ID does not exist or is not accessible. |
| `Response not found` | The response ID does not exist for this form. |
| `Field not found` | The field ID does not exist in the form. |
| `Webhook not found` | The webhook ID does not exist for this form. |
| `Workspace not found` | The workspace ID does not exist or is inaccessible. |
| `not_enough_permissions` | The connected account lacks permission for this operation. |
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

- [Typeform Developer Documentation](https://www.typeform.com/developers/)
- [Typeform API Reference](https://www.typeform.com/developers/get-started)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=typeform-surveys
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=typeform-surveys)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)