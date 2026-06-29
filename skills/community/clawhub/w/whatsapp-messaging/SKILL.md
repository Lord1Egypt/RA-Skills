---
name: whatsapp-messaging
description: Send WhatsApp messages, manage templates, handle media, and automate WhatsApp Business messaging workflows via the WhatsApp Business API. Use this skill when users want to send messages, manage templates, or automate customer communication on WhatsApp.
---

# WhatsApp

![WhatsApp](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/whatsapp.svg?v=2)

Send WhatsApp messages, manage templates, handle media, and automate WhatsApp Business messaging workflows via the WhatsApp Business API.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=whatsapp-messaging) for hosted connection flows and credentials so you do not need to configure WhatsApp API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect WhatsApp |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect WhatsApp |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│  WhatsApp Cloud  │
│   (User Chat)   │     │   (OAuth)    │     │      API         │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect WhatsApp  │                       │
         │                       │  4. Secure Token      │
         │                       │  5. Proxy Requests   │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │ WhatsApp│
   │  File    │           │ Auth     │           │ Business │
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for WhatsApp again."

## Quick Start

```bash
# List phone numbers
clawlink_call_tool --tool "whatsapp_get_phone_numbers" --params '{}'

# Send a text message
clawlink_call_tool --tool "whatsapp_send_message" --params '{"phone_number": "+15551234567", "message": "Hello from OpenClaw!"}'

# List message templates
clawlink_call_tool --tool "whatsapp_get_message_templates" --params '{}'
```

## Authentication

All WhatsApp tool calls are authenticated automatically by ClawLink using the user's connected WhatsApp Business account token.

**No API token is required in chat.** ClawLink stores the token securely and injects it into every WhatsApp Business API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=whatsapp and connect WhatsApp.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `whatsapp` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration whatsapp
```

**Response:** Returns the live tool catalog for WhatsApp.

### Reconnect

If WhatsApp tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=whatsapp
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration whatsapp`

## Security & Permissions

- Access is scoped to the WhatsApp Business account connected during OAuth setup.
- **All message send operations require explicit user confirmation.** WhatsApp messages reach real users — confirm recipients and content.
- Message templates must be pre-approved by WhatsApp before they can be used.
- The 24-hour customer service window applies to free-form messages — outside this window, only approved templates can be sent.
- Confirm recipient phone numbers before sending — messages cannot be recalled.

## Tool Reference

### Phone Numbers

| Tool | Description | Mode |
|------|-------------|------|
| `whatsapp_get_phone_numbers` | List all phone numbers on the WhatsApp Business account | Read |
| `whatsapp_get_phone_number` | Get details for a specific phone number | Read |

### Messages

| Tool | Description | Mode |
|------|-------------|------|
| `whatsapp_send_message` | Send a text message to a WhatsApp number | Write |
| `whatsapp_send_media` | Send an image, video, audio, or document | Write |
| `whatsapp_send_media_by_id` | Send media using a previously uploaded media ID | Write |
| `whatsapp_send_location` | Send a location message with coordinates | Write |
| `whatsapp_send_contacts` | Send contact card(s) to a WhatsApp user | Write |
| `whatsapp_send_interactive_buttons` | Send a message with up to 3 reply buttons | Write |
| `whatsapp_send_interactive_list` | Send a list message with up to 10 options | Write |
| `whatsapp_send_template_message` | Send an approved message template | Write |

### Media

| Tool | Description | Mode |
|------|-------------|------|
| `whatsapp_upload_media` | Upload media (image, video, audio, document) to WhatsApp servers | Write |
| `whatsapp_get_media_info` | Get metadata and download URL for uploaded media | Read |

### Message Templates

| Tool | Description | Mode |
|------|-------------|------|
| `whatsapp_get_message_templates` | List all message templates | Read |
| `whatsapp_get_template_status` | Get approval status of a specific template | Read |
| `whatsapp_create_message_template` | Create a new message template | Write |
| `whatsapp_delete_message_template` | Delete a message template | Write |

### Business Profile

| Tool | Description | Mode |
|------|-------------|------|
| `whatsapp_get_business_profile` | Get the business profile information | Read |

## Code Examples

### List phone numbers

```bash
clawlink_call_tool --tool "whatsapp_get_phone_numbers" \
  --params '{}'
```

### Send a text message

```bash
clawlink_call_tool --tool "whatsapp_send_message" \
  --params '{
    "phone_number_id": "PHONE_NUMBER_ID",
    "recipient_phone": "+15551234567",
    "message": "Hi! Your order #12345 has shipped and is on its way."
  }'
```

### Send an image

```bash
clawlink_call_tool --tool "whatsapp_send_media" \
  --params '{
    "phone_number_id": "PHONE_NUMBER_ID",
    "recipient_phone": "+15551234567",
    "media_url": "https://example.com/receipt.png",
    "caption": "Here is your receipt for order #12345"
  }'
```

### Send interactive buttons

```bash
clawlink_call_tool --tool "whatsapp_send_interactive_buttons" \
  --params '{
    "phone_number_id": "PHONE_NUMBER_ID",
    "recipient_phone": "+15551234567",
    "header": "Order Update",
    "body": "Has your package arrived?",
    "buttons": [
      {"id": "yes", "title": "Yes"},
      {"id": "no", "title": "No"}
    ]
  }'
```

### Send a template message

```bash
clawlink_call_tool --tool "whatsapp_send_template_message" \
  --params '{
    "phone_number_id": "PHONE_NUMBER_ID",
    "recipient_phone": "+15551234567",
    "template_name": "shipping_confirmation",
    "language_code": "en",
    "components": [
      {
        "type": "body",
        "parameters": [
          {"type": "text", "text": "John"},
          {"type": "text", "text": "#12345"}
        ]
      }
    ]
  }'
```

### Upload media

```bash
clawlink_call_tool --tool "whatsapp_upload_media" \
  --params '{
    "phone_number_id": "PHONE_NUMBER_ID",
    "media_url": "https://example.com/image.png",
    "media_type": "image/png"
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm WhatsApp is connected.
2. Call `clawlink_list_tools --integration whatsapp` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `whatsapp`.
5. If no WhatsApp tools appear, direct the user to https://claw-link.dev/dashboard?add=whatsapp.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → describe                                     │
│                                                             │
│  Example: List templates → Get template status → Report     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  describe → preview → confirm → call                       │
│                                                             │
│  Example: Preview message → User approves → Send message    │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- You need a `phone_number_id` from `whatsapp_get_phone_numbers` to send messages.
- The 24-hour customer service window: free-form messages can only be sent to users who have messaged you within the past 24 hours.
- Outside the 24-hour window, you must use approved message templates.
- Template deletion has a 30-day cooldown before the name can be reused.
- Media downloads expire — use `whatsapp_get_media_info` to get a fresh download URL.
- Recipient phone numbers must include country code (e.g., `+1` for US).

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration whatsapp`. |
| Missing connection | WhatsApp is not connected. Direct the user to https://claw-link.dev/dashboard?add=whatsapp. |
| `131026` — Message undeliverable | The recipient's phone number is not a valid WhatsApp account. |
| `133010` — Phone number not on WhatsApp | The recipient has not registered on WhatsApp. |
| `131047` — Outside 24-hour window | Must use a template message. Send a template instead. |
| `Template not found` | The template name does not exist or hasn't been approved. |
| `Template rejected` | The template is pending review or was rejected by WhatsApp. |
| `Media upload failed` | The media URL is inaccessible or the format is unsupported. |
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

### Troubleshooting: Message Send Fails

1. Confirm the recipient phone number is correct and includes the country code.
2. Check if the 24-hour window has expired — use a template message instead.
3. Verify the template is approved before trying to send it.
4. Check the phone number ID is correct for the business account.

## Resources

- [WhatsApp Business API Documentation](https://developers.facebook.com/docs/whatsapp/cloud-api)
- [WhatsApp Business API Reference](https://developers.facebook.com/docs/whatsapp/api/messages)
- [Message Templates Guidelines](https://developers.facebook.com/docs/whatsapp/message-templates)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=whatsapp-messaging
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=whatsapp-messaging)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)