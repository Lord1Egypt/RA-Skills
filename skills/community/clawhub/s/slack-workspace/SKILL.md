---
name: slack-messaging
description: Send messages, manage channels, handle files, and coordinate team communication in Slack via the Slack API. Use this skill when users want to send messages, search conversations, manage channels, create reminders, or automate Slack workflows from chat.
---

# Slack

Manage Slack workspaces — send messages, manage channels, search conversations, handle files, create reminders, and automate team communication via the Slack API.

This skill uses [ClawLink](https://claw-link.dev) for hosted connection flows and credentials so you do not need to configure Slack API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Slack |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Slack |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│   Slack Web API  │
│   (User Chat)   │     │   (OAuth)    │     │                  │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect Slack     │                       │
         │                       │  4. Secure Token      │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │  Slack   │
   │  File    │           │ Auth     │           │ Workspace│
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Slack again."

## Quick Start

```bash
# List all channels
clawlink_call_tool --tool "slack_list_all_channels" --params '{}'

# Send a message
clawlink_call_tool --tool "slack_send_message" --params '{"channel": "C0123456789", "text": "Hello from OpenClaw!"}'

# Find a user
clawlink_call_tool --tool "slack_find_user_by_email_address" --params '{"email": "colleague@company.com"}'
```

## Authentication

All Slack tool calls are authenticated automatically by ClawLink using the user's connected Slack workspace OAuth token.

**No API token is required in chat.** ClawLink stores the OAuth token securely and injects it into every Slack Web API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=slack and connect Slack.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `slack` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration slack
```

**Response:** Returns the live tool catalog for Slack.

### Reconnect

If Slack tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=slack
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration slack`

## Security & Permissions

- Access is scoped to the Slack workspace connected during OAuth setup and the permissions granted.
- **All write operations require explicit user confirmation.** Before executing any message send, channel create, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (delete channel, delete file, delete message) are marked as high-impact and must be confirmed.
- Message sends to external channels or DMs should be confirmed before posting.

## Tool Reference

### Messages

| Tool | Description | Mode |
|------|-------------|------|
| `slack_send_message` | Send a text message to a channel, DM, or MPDM | Write |
| `slack_send_thread_reply` | Reply to a specific message thread | Write |
| `slack_schedule_message` | Schedule a message for future delivery | Write |
| `slack_delete_scheduled_message` | Delete a pending scheduled message | Write |
| `slack_list_scheduled_messages` | List pending scheduled messages in a channel | Read |
| `slack_deletes_a_message_from_a_chat` | Delete a message from a channel or DM | Write |
| `slack_update_message` | Update an existing message's text | Write |

### Channels

| Tool | Description | Mode |
|------|-------------|------|
| `slack_list_all_channels` | List all channels in the workspace | Read |
| `slack_find_channels` | Search channels by name, topic, or purpose | Read |
| `slack_create_channel` | Create a new public or private channel | Write |
| `slack_archive_conversation` | Archive a channel (makes it read-only) | Write |
| `slack_rename_channel` | Rename an existing channel | Write |
| `slack_set_channel_topic` | Set the topic/description of a channel | Write |
| `slack_set_channel_purpose` | Set the purpose of a channel | Write |
| `slack_invite_users_to_a_slack_channel` | Invite users to a channel | Write |
| `slack_join_an_existing_conversation` | Join a channel you have access to | Write |
| `slack_leave_conversation` | Leave a channel | Write |
| `slack_close_dm` | Close a DM or MPDM conversation | Write |

### Conversations & History

| Tool | Description | Mode |
|------|-------------|------|
| `slack_fetch_conversation_history` | Get messages from a channel (main timeline, not threads) | Read |
| `slack_fetch_message_thread_from_a_conversation` | Get all replies in a specific thread | Read |
| `slack_list_conversations` | List conversations accessible to a user | Read |

### Users

| Tool | Description | Mode |
|------|-------------|------|
| `slack_list_all_users` | List all users in the workspace | Read |
| `slack_find_users` | Search users by name, email, or criteria | Read |
| `slack_find_user_by_email_address` | Look up a user by their email address | Read |
| `slack_get_user_presence` | Get a user's current presence (active/away) | Read |
| `slack_get_user_dnd_status` | Get a user's Do Not Disturb status | Read |

### Files

| Tool | Description | Mode |
|------|-------------|------|
| `slack_list_files_with_filters_in_slack` | List files shared in the workspace | Read |
| `slack_upload_file_to_channel` | Upload a file to a channel | Write |
| `slack_delete_file` | Permanently delete a file | Write |
| `slack_download_slack_file` | Download file content and get a public URL | Read |

### Reactions

| Tool | Description | Mode |
|------|-------------|------|
| `slack_add_reaction_to_an_item` | Add an emoji reaction to a message | Write |
| `slack_remove_reaction_from_item` | Remove a reaction from a message | Write |
| `slack_fetch_item_reactions` | Get all reactions on a message | Read |

### Reminders

| Tool | Description | Mode |
|------|-------------|------|
| `slack_create_a_reminder` | Create a reminder at a specific time | Write |
| `slack_list_reminders` | List all your reminders | Read |
| `slack_get_reminder` | Get details of a specific reminder | Read |
| `slack_complete_reminder` | Mark a reminder as complete | Write |
| `slack_delete_reminder` | Delete a reminder | Write |

### Pins & Stars

| Tool | Description | Mode |
|------|-------------|------|
| `slack_pin_item` | Pin a message to a channel | Write |
| `slack_list_pinned_items` | List all pinned items in a channel | Read |
| `slack_remove_pin` | Unpin an item from a channel | Write |
| `slack_add_star` | Star a channel, file, or message | Write |
| `slack_list_starred_items` | List your starred items | Read |
| `slack_remove_star` | Remove a star from an item | Write |

### Canvases

| Tool | Description | Mode |
|------|-------------|------|
| `slack_create_canvas` | Create a new Slack Canvas document | Write |
| `slack_edit_canvas` | Edit content in a Canvas | Write |
| `slack_delete_canvas` | Delete a Canvas permanently | Write |
| `slack_lookup_canvas_sections` | Get section IDs for targeted editing | Read |

### Team & Admin

| Tool | Description | Mode |
|------|-------------|------|
| `slack_fetch_team_info` | Get workspace metadata and settings | Read |
| `slack_invite_user_to_workspace` | Invite a new user to the workspace | Write |
| `slack_create_user_group` | Create a user group (subteam) | Write |
| `slack_list_user_groups` | List all user groups | Read |
| `slack_disable_user_group` | Disable a user group | Write |
| `slack_enable_user_group` | Re-enable a disabled user group | Write |
| `slack_list_enterprise_teams` | List all teams in an Enterprise Grid org | Read |
| `slack_read_audit_logs` | Read Enterprise Grid audit logs | Read |

### Emoji

| Tool | Description | Mode |
|------|-------------|------|
| `slack_add_emoji` | Add a custom emoji to the workspace | Write |
| `slack_list_custom_emojis` | List all custom emoji | Read |
| `slack_remove_emoji` | Remove a custom emoji (Enterprise Grid) | Write |

### Calls

| Tool | Description | Mode |
|------|-------------|------|
| `slack_get_call_info` | Get details about a Slack call | Read |
| `slack_end_call` | End an ongoing call | Write |
| `slack_add_call_participants` | Add participants to a call | Write |
| `slack_remove_call_participants` | Remove participants from a call | Write |

## Code Examples

### Send a message to a channel

```bash
clawlink_call_tool --tool "slack_send_message" \
  --params '{
    "channel": "C0123456789",
    "text": "Deployment complete! Version 2.1.0 is live."
  }'
```

### Reply to a thread

```bash
clawlink_call_tool --tool "slack_send_thread_reply" \
  --params '{
    "channel": "C0123456789",
    "thread_ts": "1234567890.123456",
    "text": "I will take care of this by end of day."
  }'
```

### Create a channel

```bash
clawlink_call_tool --tool "slack_create_channel" \
  --params '{
    "name": "project-alpha",
    "is_private": false
  }'
```

### Schedule a reminder

```bash
clawlink_call_tool --tool "slack_create_a_reminder" \
  --params '{
    "text": "Weekly team sync",
    "time": "tomorrow at 10am"
  }'
```

### Find a user and send them a DM

```bash
clawlink_call_tool --tool "slack_find_user_by_email_address" \
  --params '{
    "email": "alex@company.com"
  }'
```

### Upload a file to a channel

```bash
clawlink_call_tool --tool "slack_upload_file_to_channel" \
  --params '{
    "channel": "C0123456789",
    "content": "File content here",
    "filename": "report.csv",
    "title": "Q1 Report"
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Slack is connected.
2. Call `clawlink_list_tools --integration slack` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `slack`.
5. If no Slack tools appear, direct the user to https://claw-link.dev/dashboard?add=slack.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → find → call                         │
│                                                             │
│  Example: Find channel → Get history → Show messages       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  describe → preview → confirm → call                        │
│                                                             │
│  Example: Preview message → User approves → Send message    │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- `slack_fetch_conversation_history` returns messages from the main channel timeline only — threaded replies require `slack_fetch_message_thread_from_a_conversation`.
- Channel IDs (C*/G*) are required for most Slack tools — use `slack_find_channels` to resolve display names to IDs.
- Message scheduling accepts natural language times (e.g., "in 15 minutes", "every Thursday at 2pm") or Unix timestamps.
- DMs and MPDMs use channel IDs starting with `D` or `G` respectively.
- File uploads are limited by Slack's constraints; large files may need to be uploaded to a file host first.
- Rate limits apply to many endpoints (~1-2 requests/second for list operations); honor `Retry-After` headers.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration slack`. |
| Missing connection | Slack is not connected. Direct the user to https://claw-link.dev/dashboard?add=slack. |
| `channel_not_found` | The channel ID does not exist or the bot is not a member. |
| `user_not_found` | The user email or ID does not match any workspace member. |
| `not_authed` | The OAuth token is invalid or has been revoked. Reconnect Slack. |
| `missing_scope` | The token lacks the required scope for this operation. |
| `message_not_found` | The message timestamp does not match any message in the channel. |
| `cant_update_message` | Only the message author or workspace admin can edit a message. |
| `is_archived` | The target channel has been archived. |
| `send_as_app` | The message requires a bot token. The user may need to use a different connection method. |
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

1. Ensure the integration slug is exactly `slack`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.
4. Resolve channel names to IDs using `slack_find_channels` before calling tools that require a channel ID.

### Troubleshooting: Empty Results

1. `slack_fetch_conversation_history` returns empty — the tool only fetches the main timeline, not threaded replies. Use `slack_fetch_message_thread_from_a_conversation` with the parent message's `thread_ts`.
2. `slack_find_channels` returns empty — the channel may be private or the bot may not be a member. Use the channel ID directly if known.
3. `slack_list_all_users` returns incomplete results — this may reflect guest account visibility settings, not a real absence.

## Resources

- [Slack API Documentation](https://api.slack.com/)
- [Slack Web API Reference](https://api.slack.com/methods)
- [Slack Rate Limits](https://api.slack.com/docs/rate-limits)
- ClawLink: https://claw-link.dev
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

---

**Powered by [ClawLink](https://claw-link.dev)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)