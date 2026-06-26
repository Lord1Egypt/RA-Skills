---
name: sendgrid-email
description: SendGrid email integration with API key authentication. Manage marketing campaigns, transactional templates, contacts, suppression lists, sender identities, IP pools, and event webhooks via the SendGrid API.
---

# SendGrid

![SendGrid](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/sendgrid.svg?v=2)

Connect to Twilio SendGrid to manage email marketing campaigns, transactional templates, contacts, suppression lists, sender identities, IP address pools, and event webhooks.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=sendgrid-email) for hosted connection flows and credentials so you do not need to configure SendGrid API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect SendGrid |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect SendGrid |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│   SendGrid API   │
│   (User Chat)   │     │   (Proxy)    │     │  (Email, Marketing│
│                 │     │              │     │   Campaigns)      │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                    │                      │
         │  1. Install Plugin │                      │
         │  2. Pair Device    │                      │
         │  3. Connect SendGrid │                   │
         │                    │  4. API Key Proxy   │
         │                    │  5. Request Forward │
         │                    │                     │
         ▼                    ▼                     ▼
   ┌──────────┐        ┌──────────┐         ┌──────────┐
   │   SKILL  │        │ Dashboard│         │  SendGrid│
   │   File   │        │   Auth   │         │   Cloud  │
   └──────────┘        └──────────┘         └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for SendGrid again."

## Quick Start

```bash
# Check account verification status
clawlink_call_tool --tool "sendgrid_completed_steps"

# Create a new contact
clawlink_call_tool --tool "sendgrid_add_or_update_a_contact" --params '{"contacts": [{"email": "alice@example.com", "first_name": "Alice", "last_name": "Smith"}]}'

# Create a transactional template
clawlink_call_tool --tool "sendgrid_create_a_transactional_template" --params '{"name": "Welcome Email Template"}'
```

## Authentication

All SendGrid tool calls are authenticated automatically by ClawLink using your SendGrid API key stored securely in the dashboard.

**No API key is required in chat.** ClawLink injects your API key into every SendGrid API request on your behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=sendgrid and connect SendGrid with your API key.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `sendgrid` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration sendgrid
```

**Response:** Returns the live tool catalog for SendGrid.

### Reconnect

If SendGrid tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=sendgrid
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration sendgrid`

## Security & Permissions

- Access is scoped to the SendGrid account associated with the connected API key.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (delete campaign, delete suppression, remove write key) are marked as high-impact and must be confirmed.
- IP address management and account provisioning require Pro or Premier plans — check your plan before attempting these operations.

## Tool Reference

### Account & Verification

| Tool | Description | Mode |
|------|-------------|------|
| `sendgrid_completed_steps` | Retrieve verification status of Domain Authentication and Single Sender Verification | Read |

### Contacts & Lists

| Tool | Description | Mode |
|------|-------------|------|
| `sendgrid_add_or_update_a_contact` | Add or update contacts asynchronously (matched by email, phone, external_id; returns job_id) | Write |
| `sendgrid_create_a_list` | Create a new contact list in Marketing Campaigns | Write |
| `sendgrid_create_list` | Create a new contact list (up to 1000 lists per account; names must be unique) | Write |
| `sendgrid_create_a_segment` | Create a segment using SQL-like conditions for targeted campaigns | Write |
| `sendgrid_create_segment` | Create a contact segment using Segmentation V2 API | Write |

### Campaigns & Single Sends

| Tool | Description | Mode |
|------|-------------|------|
| `sendgrid_create_a_campaign` | Create a marketing campaign with subject, sender, content, and list/segment | Write |
| `sendgrid_create_single_send` | Create a Single Send draft (uses `email_config`; scheduling requires separate endpoint) | Write |
| `sendgrid_bulk_delete_single_sends` | Permanently delete multiple Single Sends by ID (up to 1000 per request) | Write |
| `sendgrid_cancel_or_pause_a_scheduled_send` | Cancel or pause scheduled email sends by batch_id | Write |

### Transactional Templates

| Tool | Description | Mode |
|------|-------------|------|
| `sendgrid_create_a_transactional_template` | Create a transactional email template (up to 300 per account) | Write |
| `sendgrid_create_a_new_transactional_template_version` | Create a new version of a transactional template | Write |
| `sendgrid_activate_template_version` | Activate a specific version as the default for a template | Write |

### Sender Identities

| Tool | Description | Mode |
|------|-------------|------|
| `sendgrid_create_a_sender` | Create a sender identity for Marketing Campaigns (up to 100 unique senders) | Write |
| `sendgrid_create_a_sender_identity` | Create a new sender identity with from address and identity details | Write |
| `sendgrid_create_verified_sender_request` | Create a sender identity via POST and send a verification email | Write |

### Suppressions & Bounces

| Tool | Description | Mode |
|------|-------------|------|
| `sendgrid_add_suppressions_to_a_suppression_group` | Add email addresses to an unsubscribe group | Write |
| `sendgrid_add_to_global_suppressions_group` | Add email addresses to the global suppression group (idempotent) | Write |
| `sendgrid_delete_a_bounce` | Remove an email from the bounce suppression list | Write |
| `sendgrid_delete_a_global_suppression` | Remove an email from suppressions to allow future delivery | Write |

### IP Address Management

| Tool | Description | Mode |
|------|-------------|------|
| `sendgrid_add_a_twilio_send_grid_ip_address` | Provision a new dedicated IP address (Pro/Premier plans only; additional cost) | Write |
| `sendgrid_add_ips` | Add dedicated IP addresses to the account | Write |
| `sendgrid_create_an_ip_pool` | Create a new IP pool to group dedicated IPs | Write |
| `sendgrid_create_an_ip_pool_with_a_name_and_ip_assignments` | Create an IP pool and assign IPs in a single atomic operation | Write |
| `sendgrid_add_an_ip_address_to_a_pool` | Add a dedicated IP address to an existing pool | Write |
| `sendgrid_assign_a_batch_of_subusers_to_an_ip` | Assign multiple subusers to a specified IP address | Write |
| `sendgrid_delete_a_batch_of_ips_from_an_ip_pool` | Remove IPs from a pool (IPs remain in account, not deleted) | Write |

### Domain Authentication

| Tool | Description | Mode |
|------|-------------|------|
| `sendgrid_authenticate_a_domain` | Enable domain authentication for users or subusers | Write |
| `sendgrid_associate_an_authenticated_domain_with_a_given_user` | Associate an authenticated domain with a subuser | Write |
| `sendgrid_add_an_ip_to_an_authenticated_domain` | Add an IP address to an authenticated domain for custom SPF | Write |
| `sendgrid_bind_authenticated_domains_to_user` | Associate additional authenticated domains with a subuser (up to 5) | Write |

### Branded Links & Tracking

| Tool | Description | Mode |
|------|-------------|------|
| `sendgrid_create_a_branded_link` | Create a new branded link for link tracking | Write |
| `sendgrid_associate_a_branded_link_with_a_subuser` | Associate a branded link with a subuser for link tracking | Write |
| `sendgrid_delete_a_branded_link` | Permanently delete a branded link | Write |

### Alerts & Webhooks

| Tool | Description | Mode |
|------|-------------|------|
| `sendgrid_create_a_new_alert` | Create an alert (usage_limit or stats_notification type) | Write |
| `sendgrid_create_a_new_event_webhook` | Set up an Event Webhook with URL, events, and OAuth/signature verification | Write |

### Parse Webhook

| Tool | Description | Mode |
|------|-------------|------|
| `sendgrid_create_a_parse_setting` | Create an Inbound Parse Webhook setting to receive and parse incoming emails | Write |
| `sendgrid_delete_a_parse_setting` | Delete a specific inbound parse webhook setting by hostname | Write |

### Custom Fields

| Tool | Description | Mode |
|------|-------------|------|
| `sendgrid_create_a_custom_field` | Create a custom field for storing additional contact information (up to 120 per account) | Write |
| `sendgrid_create_custom_field_definition` | Create a unique case-insensitive custom field definition | Write |

### Designs

| Tool | Description | Mode |
|------|-------------|------|
| `sendgrid_create_design` | Create a new email design in the SendGrid Design Library | Write |

### External Integrations

| Tool | Description | Mode |
|------|-------------|------|
| `sendgrid_create_integration` | Create a SendGrid Marketing Integration for forwarding events to Segment | Write |

### API Keys & Access Management

| Tool | Description | Mode |
|------|-------------|------|
| `sendgrid_create_api_keys` | Create a new SendGrid API key with specified permissions (up to 100 keys) | Write |
| `sendgrid_add_one_or_more_ips_to_the_allow_list` | Add IPv4 addresses to IP access management allow list (max 1000 total) | Write |

### SSO & Teammates

| Tool | Description | Mode |
|------|-------------|------|
| `sendgrid_create_an_sso_integration` | Create a SAML 2.0 SSO integration with an Identity Provider | Write |
| `sendgrid_create_an_sso_certificate` | Create an SSO certificate for SAML 2.0 authentication | Write |
| `sendgrid_create_an_sso_teammate` | Create an SSO Teammate (requires Enterprise account with SSO enabled) | Write |
| `sendgrid_approve_access_request` | Approve a teammate's access request (admin only) | Write |

### Account Provisioning (Partners)

| Tool | Description | Mode |
|------|-------------|------|
| `sendgrid_create_an_account` | Create a new customer account (reseller partners only) | Write |
| `sendgrid_authenticate_an_account_with_single_sign_on` | Generate a one-time SSO URL for a customer's Twilio SendGrid account (reseller partners only) | Write |

### Subusers

| Tool | Description | Mode |
|------|-------------|------|
| `sendgrid_create_subuser` | Create a new subuser account | Write |

### Batch & Mail Operations

| Tool | Description | Mode |
|------|-------------|------|
| `sendgrid_create_a_batch_id` | Generate a new mail batch ID to group multiple email sends | Write |

## Code Examples

### Add or update a contact

```bash
clawlink_call_tool --tool "sendgrid_add_or_update_a_contact" \
  --params '{
    "contacts": [
      {"email": "alice@example.com", "first_name": "Alice", "last_name": "Smith", "custom_fields": {"industry": "tech"}}
    ]
  }'
```

### Create a transactional template version

```bash
clawlink_call_tool --tool "sendgrid_create_a_new_transactional_template_version" \
  --params '{
    "template_id": "YOUR_TEMPLATE_ID",
    "active": 1,
    "name": "Version 2",
    "html_content": "<html><body><h1>Welcome {{name}}!</h1></body></html>"
  }'
```

### Create a suppression group

```bash
clawlink_call_tool --tool "sendgrid_create_a_new_suppression_group" \
  --params '{
    "name": "Newsletter Unsubscribes",
    "description": "Recipients who opted out of newsletter emails"
  }'
```

### Add IPs to an allow list

```bash
clawlink_call_tool --tool "sendgrid_add_one_or_more_ips_to_the_allow_list" \
  --params '{"ips": ["192.168.1.0/24", "10.0.0.1"]}'
```

### Create an event webhook

```bash
clawlink_call_tool --tool "sendgrid_create_a_new_event_webhook" \
  --params '{
    "url": "https://your-app.com/webhook/sendgrid",
    "events": ["delivered", "open", "click", "bounce", "dropped"]
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm SendGrid is connected.
2. Call `clawlink_list_tools --integration sendgrid` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `sendgrid`.
5. If no SendGrid tools appear, direct the user to https://claw-link.dev/dashboard?add=sendgrid.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → describe → call                                │
│                                                             │
│  Example: Check verification status → List contacts          │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  describe → preview → confirm → call                        │
│                                                             │
│  Example: Describe tool → Preview changes → User approves   │
│           → Execute create                                   │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- IP address management tools (add, create pools, assign subusers) require Pro or Premier plans — Essential/Free plans will receive errors.
- Reseller-only endpoints (`create_an_account`, `authenticate_an_account_with_single_sign_on`) return 403 for non-partner accounts.
- Contact operations are asynchronous — `add_or_update_a_contact` returns a `job_id` for tracking import status.
- Custom field names must be unique and cannot use reserved names (first_name, last_name, email, created_at, etc.).
- Suppression group names and descriptions are visible to recipients when they manage email preferences.
- Date fields for custom fields use MM/DD/YYYY format or epoch timestamp.
- Branded links require domain authentication — authenticate the domain first before creating branded links.
- SSO features require Enterprise plan or higher.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration sendgrid`. |
| Missing connection | SendGrid is not connected. Direct the user to https://claw-link.dev/dashboard?add=sendgrid. |
| `403 Forbidden` | The API key lacks permissions for this operation, or the feature requires a higher plan (Pro/Premier/Enterprise). |
| `400 Bad Request` | Invalid parameters — check the tool schema with `clawlink_describe_tool`. |
| `404 Not Found` | The referenced resource (campaign, template, IP) does not exist. |
| `429 Too Many Requests` | Rate limit exceeded — wait and retry with exponential backoff. |
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

1. Ensure the integration slug is exactly `sendgrid`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.
4. Verify plan requirements — IP management and SSO require Pro/Enterprise plans.

## Resources

- [SendGrid API Documentation](https://docs.sendgrid.com/api-reference)
- [SendGrid Marketing Campaigns API](https://docs.sendgrid.com/api-reference/campaigns-api)
- [SendGrid Transactional Email](https://docs.sendgrid.com/ui/sending-email/how-to-send-email-with-transactional-templates)
- [SendGrid IP Management](https://docs.sendgrid.com/ui/sending-email/ip-access-management)
- [SendGrid Inbound Parse](https://docs.sendgrid.com/for-developers/parsing-email/setting-up-the-inbound-parse-webhook)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=sendgrid-email
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [Mailchimp](https://clawhub.ai/hith3sh/mailchimp-email) — For Mailchimp email marketing
- [Postmark](https://clawhub.ai/hith3sh/postmark-email) — For transactional email delivery

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=sendgrid-email)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)