---
name: resend-mail
description: Manage Resend email campaigns, contacts, audiences, domains, templates, and transactional sends via the Resend API. Use when users want to inspect email activity, manage audiences, create and send emails, or automate email workflows.
---

# Resend Email

![Resend Email](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/resend.svg?v=2)

Manage Resend from chat — email campaigns, contacts, audiences, domains, templates, and transactional sends via the Resend API.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=resend-mail) for hosted connection flows and credentials so you do not need to configure Resend API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Resend |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Resend |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ Resend           │
│   (User Chat)   │     │   (OAuth)    │     │ (Email API)       │
└─────────────────┘     └──────────────┘     └──────────────────┘
          │                       │                       │
          │  1. Install Plugin    │                       │
          │  2. Pair Device      │                       │
          │  3. Connect Resend   │                       │
          │                      │  4. Secure Token       │
          │                      │  5. Proxy Requests    │
          │                      │                       │
          ▼                      ▼                       ▼
    ┌──────────┐          ┌──────────┐          ┌──────────┐
    │  SKILL   │          │ Dashboard│          │ Resend   │
    │  File    │          │ Auth     │          │ Dashboard│
    └──────────┘          └──────────┘          └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Resend again."

## Quick Start

```bash
# List all contacts
clawlink_call_tool --tool "resend_list_all_contacts" --params '{"limit": 20}'

# List audiences
clawlink_call_tool --tool "resend_list_audiences" --params '{}'

# Send an email
clawlink_call_tool --tool "resend_send_email" --params '{"from": "team@example.com", "to": ["recipient@example.com"], "subject": "Hello", "html": "<p>Hello world</p>"}'
```

## Authentication

All Resend tool calls are authenticated automatically by ClawLink using the user's connected Resend account.

**No API key is required in chat.** ClawLink stores the credentials securely and injects them into every Resend API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=resend and connect Resend.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `resend` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration resend
```

**Response:** Returns the live tool catalog for Resend.

### Reconnect

If Resend tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=resend
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration resend`

## Security & Permissions

- Access is scoped to the Resend account accessible via the connected account.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (delete contact, delete audience, delete domain) are marked as high-impact and must be confirmed.
- Confirm before sending emails or making broad contact changes — sends are irreversible.

## Tool Reference

### Audiences & Contacts

| Tool | Description | Mode |
|------|-------------|------|
| `resend_list_audiences` | List all audiences | Read |
| `resend_retrieve_audience` | Get audience details | Read |
| `resend_create_audience` | Create a new audience | Write |
| `resend_delete_audience` | Delete an audience | Write |
| `resend_list_all_contacts` | List all contacts | Read |
| `resend_list_contacts` | List contacts in an audience | Read |
| `resend_get_contact` | Get contact details | Read |
| `resend_create_contact` | Create a contact | Write |
| `resend_create_contact_v2` | Create a contact (v2) | Write |
| `resend_update_contact` | Update contact details | Write |
| `resend_delete_contact` | Delete a contact | Write |
| `resend_delete_contact_by_id` | Delete contact by ID | Write |
| `resend_add_contact_to_segment` | Add contact to segment | Write |
| `resend_remove_contact_from_segment` | Remove contact from segment | Write |
| `resend_list_contact_segments` | List segments for a contact | Read |
| `resend_list_contact_topics` | List topics for a contact | Read |

### Segments & Topics

| Tool | Description | Mode |
|------|-------------|------|
| `resend_list_segments` | List all segments | Read |
| `resend_get_segment` | Get segment details | Read |
| `resend_create_topic` | Create a topic | Write |
| `resend_list_topics` | List all topics | Read |
| `resend_get_topic` | Get topic details | Read |
| `resend_update_topic` | Update a topic | Write |
| `resend_delete_segment` | Delete a segment | Write |
| `resend_delete_topic` | Delete a topic | Write |

### Domains

| Tool | Description | Mode |
|------|-------------|------|
| `resend_list_domains` | List all domains | Read |
| `resend_retrieve_domain` | Get domain details | Read |
| `resend_create_domain` | Create and verify a domain | Write |
| `resend_verify_domain` | Verify domain DNS records | Write |
| `resend_update_domain` | Update domain settings | Write |
| `resend_delete_domain` | Delete a domain | Write |

### Templates

| Tool | Description | Mode |
|------|-------------|------|
| `resend_list_templates` | List all templates | Read |
| `resend_get_template` | Get template details | Read |
| `resend_create_template` | Create a template | Write |
| `resend_update_template` | Update a template | Write |
| `resend_delete_template` | Delete a template | Write |
| `resend_duplicate_template` | Duplicate a template | Write |
| `resend_publish_template` | Publish a template | Write |

### Emails

| Tool | Description | Mode |
|------|-------------|------|
| `resend_list_emails` | List sent emails | Read |
| `resend_retrieve_email` | Get email details | Read |
| `resend_send_email` | Send a single email | Write |
| `resend_send_batch_emails` | Send up to 100 emails | Write |
| `resend_cancel_email` | Cancel a scheduled email | Write |
| `resend_update_email` | Update a scheduled email | Write |
| `resend_list_email_attachments` | List attachments on an email | Read |
| `resend_get_email_attachment` | Get attachment details | Read |
| `resend_list_received_emails` | List received emails | Read |

### Webhooks

| Tool | Description | Mode |
|------|-------------|------|
| `resend_list_webhooks` | List all webhooks | Read |
| `resend_get_webhook` | Get webhook details | Read |
| `resend_create_webhook` | Create a webhook | Write |
| `resend_update_webhook` | Update a webhook | Write |
| `resend_delete_webhook` | Delete a webhook | Write |

### Broadcasts

| Tool | Description | Mode |
|------|-------------|------|
| `resend_list_broadcasts` | List all broadcasts | Read |
| `resend_update_broadcast` | Update a broadcast | Write |

### Contact Properties

| Tool | Description | Mode |
|------|-------------|------|
| `resend_list_contact_properties` | List contact property definitions | Read |
| `resend_get_contact_property` | Get contact property details | Read |
| `resend_create_contact_property` | Create a contact property | Write |
| `resend_update_contact_property` | Update a contact property | Write |
| `resend_delete_contact_property` | Delete a contact property | Write |

### API Keys

| Tool | Description | Mode |
|------|-------------|------|
| `resend_list_api_keys` | List all API keys | Read |
| `resend_create_api_key` | Create a new API key | Write |
| `resend_delete_api_key` | Revoke an API key | Write |

## Code Examples

### List all contacts

```bash
clawlink_call_tool --tool "resend_list_all_contacts" \
  --params '{
    "limit": 20
  }'
```

### Create an audience

```bash
clawlink_call_tool --tool "resend_create_audience" \
  --params '{
    "name": "Newsletter Subscribers"
  }'
```

### Send an email

```bash
clawlink_call_tool --tool "resend_send_email" \
  --params '{
    "from": "team@company.com",
    "to": ["recipient@example.com"],
    "subject": "Welcome to our newsletter",
    "html": "<p>Hello! Thanks for subscribing.</p>"
  }'
```

### Create a contact

```bash
clawlink_call_tool --tool "resend_create_contact" \
  --params '{
    "audience_id": "AUDIENCE_ID",
    "email": "newcontact@example.com",
    "first_name": "Jane",
    "last_name": "Doe"
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Resend is connected.
2. Call `clawlink_list_tools --integration resend` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `resend`.
5. If no Resend tools appear, direct the user to https://claw-link.dev/dashboard?add=resend.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                      │
│  list → get → retrieve → call                               │
│                                                             │
│  Example: List contacts → Get details → Show results         │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                     │
│  list → describe → preview → confirm → call                 │
│                                                             │
│  Example: Describe tool → Preview changes → User approves    │
│           → Execute send                                     │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Domain verification requires adding DNS records — allow time for propagation before verifying.
- Emails must have explicit `to`, `cc`, or `bcc` recipients — audience-based sending is not supported.
- Scheduled emails can be cancelled or updated before their scheduled time.
- Batch emails support up to 100 recipients per request.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration resend`. |
| Missing connection | Resend is not connected. Direct the user to https://claw-link.dev/dashboard?add=resend. |
| `DOMAIN_NOT_VERIFIED` | Domain DNS records have not propagated. Wait and retry verification. |
| `CONTACT_ALREADY_EXISTS` | The contact email is already in the audience. |
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

### Troubleshooting: Invalid Tool Call

1. Ensure the integration slug is exactly `resend`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Resend API Documentation](https://resend.com/docs/api-reference/introduction)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=resend-mail
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [SendGrid](https://clawhub.ai/hith3sh/sendgrid-email) — For Twilio SendGrid email operations

---

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
