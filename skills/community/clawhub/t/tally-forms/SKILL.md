---
name: tally-forms
description: Manage Tally forms, submissions, respondents, fields, and form workflow data via the Tally API. Use this skill when users want to list forms, inspect submissions, review field data, create forms, or automate Tally form workflows.
---

# Tally

![Tally](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/tally.png)

Manage Tally forms, submissions, respondents, fields, and form workflows from chat via the Tally API.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=tally-forms) for hosted connection flows and credentials so you do not need to configure Tally API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Tally |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Tally |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│   Tally API      │
│   (User Chat)   │     │   (OAuth)    │     │                  │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect Tally     │                       │
         │                       │  4. Secure Token      │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │  Tally   │
   │  File    │           │ Auth     │           │  Account │
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Tally again."

## Quick Start

```bash
# List all forms
clawlink_call_tool --tool "tally_list_forms" --params '{}'

# Get form details
clawlink_call_tool --tool "tally_get_form" --params '{"form_id": "FORM_ID"}'

# List submissions for a form
clawlink_call_tool --tool "tally_list_submissions" --params '{"form_id": "FORM_ID"}'
```

## Authentication

All Tally tool calls are authenticated automatically by ClawLink using the user's connected Tally account OAuth token.

**No API token is required in chat.** ClawLink stores the OAuth token securely and injects it into every Tally API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=tally and connect Tally.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `tally` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration tally
```

**Response:** Returns the live tool catalog for Tally.

### Reconnect

If Tally tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=tally
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration tally`

## Security & Permissions

- Access is scoped to forms and data accessible to the connected Tally account.
- **Write operations (create form, delete submission) require explicit user confirmation.**
- Submission data may contain personal information — handle in accordance with privacy best practices.
- Confirm before making bulk changes to form settings or deleting submissions.

## Tool Reference

### Forms

| Tool | Description | Mode |
|------|-------------|------|
| `tally_list_forms` | List all forms accessible to the account | Read |
| `tally_get_form` | Get form details including fields and settings | Read |
| `tally_create_form` | Create a new form | Write |
| `tally_update_form` | Update a form's name, fields, or settings | Write |
| `tally_delete_form` | Permanently delete a form | Write |
| `tally_duplicate_form` | Duplicate an existing form | Write |
| `tally_archive_form` | Archive a form | Write |
| `tally_unarchive_form` | Unarchive a form | Write |

### Submissions

| Tool | Description | Mode |
|------|-------------|------|
| `tally_list_submissions` | List submissions for a form with pagination | Read |
| `tally_get_submission` | Get a specific submission with all field values | Read |
| `tally_delete_submission` | Permanently delete a submission | Write |
| `tally_mark_submission_as_read` | Mark a submission as read | Write |
| `tally_mark_submission_as_unread` | Mark a submission as unread | Write |
| `tally_get_submission_count` | Get the number of submissions for a form | Read |

### Respondents

| Tool | Description | Mode |
|------|-------------|------|
| `tally_list_respondents` | List all respondents to a form | Read |
| `tally_get_respondent` | Get a specific respondent's information | Read |

### Fields

| Tool | Description | Mode |
|------|-------------|------|
| `tally_list_fields` | List all fields for a form | Read |
| `tally_create_field` | Add a new field to a form | Write |
| `tally_update_field` | Update a field's label, options, or settings | Write |
| `tally_delete_field` | Remove a field from a form | Write |

### Form Workflows

| Tool | Description | Mode |
|------|-------------|------|
| `tally_submit_form` | Submit a response to a form | Write |
| `tally_get_form_workflow` | Get the workflow settings for a form | Read |
| `tally_update_form_workflow` | Update form workflow settings | Write |

### Notifications

| Tool | Description | Mode |
|------|-------------|------|
| `tally_list_notifications` | List notification settings for a form | Read |
| `tally_create_notification` | Create a new notification rule | Write |
| `tally_update_notification` | Update notification settings | Write |
| `tally_delete_notification` | Remove a notification rule | Write |

## Code Examples

### List all forms

```bash
clawlink_call_tool --tool "tally_list_forms" \
  --params '{}'
```

### Get form with fields

```bash
clawlink_call_tool --tool "tally_get_form" \
  --params '{
    "form_id": "FORM_ID"
  }'
```

### List submissions for a form

```bash
clawlink_call_tool --tool "tally_list_submissions" \
  --params '{
    "form_id": "FORM_ID",
    "limit": 20
  }'
```

### Get a specific submission

```bash
clawlink_call_tool --tool "tally_get_submission" \
  --params '{
    "form_id": "FORM_ID",
    "submission_id": "SUBMISSION_ID"
  }'
```

### Submit a form response

```bash
clawlink_call_tool --tool "tally_submit_form" \
  --params '{
    "form_id": "FORM_ID",
    "fields": {
      "EMAIL": "respondent@example.com",
      "MESSAGE": "This is my response"
    }
  }'
```

### Get respondent list

```bash
clawlink_call_tool --tool "tally_list_respondents" \
  --params '{
    "form_id": "FORM_ID",
    "limit": 50
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Tally is connected.
2. Call `clawlink_list_tools --integration tally` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `tally`.
5. If no Tally tools appear, direct the user to https://claw-link.dev/dashboard?add=tally.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → describe                                      │
│                                                             │
│  Example: List forms → Get submissions → Review responses  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  describe → preview → confirm → call                        │
│                                                             │
│  Example: Preview form creation → User approves → Create    │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Form IDs are required for most operations — use `tally_list_forms` to discover form IDs.
- Submissions contain field values mapped by field ID (not field label).
- Deleted forms and submissions cannot be recovered — always confirm before deleting.
- Field IDs in submissions match the internal field identifiers, not visible labels.
- Tally's API is read-focused for submissions — form creation and modification capabilities vary by plan.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration tally`. |
| Missing connection | Tally is not connected. Direct the user to https://claw-link.dev/dashboard?add=tally. |
| `Form not found` | The form ID does not exist or is not accessible. |
| `Submission not found` | The submission ID does not exist for this form. |
| `Field not found` | The field ID does not exist in the form. |
| `Not authorized` | The connected account lacks access to this form or operation. |
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

- [Tally API Documentation](https://tally.so/help/webhooks)
- [Tally Developer Docs](https://tally.so/developers)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=tally-forms
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=tally-forms)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)