---
name: zoom-meetings
description: Manage Zoom meetings, webinars, registrants, cloud recordings, and event workflows via the Zoom API. Use this skill when users want to schedule meetings, manage webinar participants, access recordings, or automate Zoom event workflows.
---

# Zoom

![Zoom](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/zoom.svg?v=2)

Access Zoom via the Zoom API with managed OAuth authentication. Manage meetings, webinars, registrants, collaborators, and event workflows from chat.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=zoom-meetings) for hosted connection flows and credentials so you do not need to configure Zoom API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Zoom |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Zoom |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│    Zoom API       │
│   (User Chat)   │     │   (OAuth)    │     │   (Meetings)     │
└─────────────────┘     └──────────────┘     └──────────────────┘
          │                       │                       │
          │  1. Install Plugin    │                       │
          │  2. Pair Device       │                       │
          │  3. Connect Zoom      │                       │
          │                       │  4. Secure Token      │
          │                       │  5. Proxy Requests    │
          │                       │                       │
          ▼                       ▼                       ▼
    ┌──────────┐           ┌──────────┐           ┌──────────┐
    │  SKILL   │           │ Dashboard│           │  Zoom    │
    │  File    │           │ Auth     │           │ Web Portal│
    └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Zoom again."

## Quick Start

```bash
# List integrations
clawlink_list_integrations

# List Zoom tools
clawlink_list_tools --integration zoom

# Search for a specific tool
clawlink_search_tools --query "meeting" --integration zoom
```

## Authentication

All Zoom tool calls are authenticated automatically by ClawLink using the user's connected Zoom account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Zoom API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=zoom and connect Zoom.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `zoom` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration zoom
```

**Response:** Returns the live tool catalog for Zoom.

### Reconnect

If Zoom tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=zoom
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration zoom`

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Zoom is connected.
2. Call `clawlink_list_tools --integration zoom` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `zoom`.
5. If no Zoom tools appear, direct the user to https://claw-link.dev/dashboard?add=zoom.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: List meetings → Get details → Show results        │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  list → get → describe → preview → confirm → call           │
│                                                             │
│  Example: Describe tool → Preview changes → User approves   │
│           → Execute update                                  │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Tool Reference

### Meetings

| Tool | Description | Mode |
|------|-------------|------|
| `zoom_list_meetings` | List scheduled meetings for a user | Read |
| `zoom_get_a_meeting` | Get meeting details by ID | Read |
| `zoom_create_a_meeting` | Create a new meeting | Write |
| `zoom_update_a_meeting` | Update an existing meeting | Write |
| `zoom_delete_a_meeting` | Delete a meeting | Write |
| `zoom_get_meeting_recordings` | Get cloud recordings for a meeting | Read |

### Webinars

| Tool | Description | Mode |
|------|-------------|------|
| `zoom_list_webinars` | List scheduled webinars | Read |
| `zoom_get_a_webinar` | Get webinar details by ID | Read |
| `zoom_list_webinar_registrants` | List webinar registrants | Read |
| `zoom_add_a_webinar_registrant` | Register a participant for a webinar | Write |

### Users& Settings

| Tool | Description | Mode |
|------|-------------|------|
| `zoom_get_user` | Get user details by ID or email | Read |
| `zoom_list_users_settings` | Get user settings including preferences | Read |
| `zoom_list_users_collaboration_devices` | List user's collaboration devices | Read |

### Registrants & Participants

| Tool | Description | Mode |
|------|-------------|------|
| `zoom_add_a_meeting_registrant` | Register a participant for a meeting | Write |
| `zoom_get_past_meeting_participants` | List participants from a past meeting | Read |
| `zoom_list_webinar_participants` | List webinar participants | Read |

### ZRA (Revenue Accelerator)

| Tool | Description | Mode |
|------|-------------|------|
| `zoom_list_zra_conversations` | List ZRA conversations | Read |
| `zoom_get_zra_conversation_scorecards` | Get conversation scorecards | Read |
| `zoom_create_zra_conversation` | Create a ZRA conversation | Write |

### Cloud Recordings

| Tool | Description | Mode |
|------|-------------|------|
| `zoom_list_all_recordings` | List all cloud recordings | Read |
| `zoom_list_archived_files` | List archived meeting files | Read |

## Code Examples

### List upcoming meetings

```bash
clawlink_call_tool --tool "zoom_list_meetings" \
  --params '{
    "user_id": "me",
    "page_size": 10
  }'
```

### Create a meeting

```bash
clawlink_call_tool --tool "zoom_create_a_meeting" \
  --params '{
    "topic": "Team Standup",
    "start_time": "2025-01-15T09:00:00Z",
    "duration": 30,
    "timezone": "America/Los_Angeles"
  }'
```

### Get meeting recordings

```bash
clawlink_call_tool --tool "zoom_get_meeting_recordings" \
  --params '{
    "meeting_id": "123456789"
  }'
```

### Register a webinar attendee

```bash
clawlink_call_tool --tool "zoom_add_a_webinar_registrant" \
  --params '{
    "webinar_id": "123456789",
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane.doe@example.com"
  }'
```

## Security & Permissions

- Access is scoped to the connected Zoom account's data and permissions.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (deleting meetings, recordings) are marked as high-impact and must be confirmed.
- Webinar operations may require a Pro or higher Zoom plan with webinar add-on.
- Cloud recording access depends on the account's recording settings.

## Notes

- Meeting IDs may exceed 32-bit integer range; treat them as full-length numeric or string identifiers.
- Start URLs for hosts expire in 2 hours for standard accounts.
- Registrant operations require the meeting/webinar to have registration enabled.
- Some tools require specific Zoom plans (Pro, Business, Enterprise) or add-ons.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration zoom`. |
| Missing connection | Zoom is not connected. Direct the user to https://claw-link.dev/dashboard?add=zoom. |
| `Meeting not found` | The meeting ID does not exist or the meeting has ended. |
| `Registration has not been enabled` | Enable registration on the meeting before adding registrants. |
| `Webinar plan is missing` | The account does not have a webinar plan/license. |
| `Only available for paid users` | The operation requires a licensed (paid) Zoom account. |
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

1. Ensure the integration slug is exactly `zoom`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Zoom API Documentation](https://developers.zoom.us/docs/api/)
- [Zoom Meeting API Reference](https://developers.zoom.us/docs/api-reference/zoom-api/)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=zoom-meetings
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=zoom-meetings)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
