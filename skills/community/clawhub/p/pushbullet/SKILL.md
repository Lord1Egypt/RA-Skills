---
name: pushbullet
description: Pushbullet API integration with managed OAuth for cross-device notification automation. Send pushes, manage devices, create chats, and handle cross-device messaging. Use this skill when users want to send notifications to devices, share links or notes across devices, manage Pushbullet chats, or register and manage connected devices.
---

# Pushbullet

![Pushbullet](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/pushbullet.svg)

Pushbullet connects your devices for instant notifications, file sharing, and cross-device messaging. This integration uses managed OAuth through ClawLink to send pushes, manage devices, chats, and handle all Pushbullet operations without managing API keys manually.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Pushbullet |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Pushbullet |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│  Pushbullet API  │
│   (User Chat)   │     │   (OAuth)    │     │                  │
└─────────────────┘     └──────────────┘     └──────────────────┘
```

## Install

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

## Quick Start

Send a link push to a device:

```
clawlink_execute_tool --integration pushbullet --tool pushbullet_create_push --args '{"type": "link", "title": "Check this out", "url": "https://example.com", "device_iden": "device-iden-here"}'
```

List your registered devices:

```
clawlink_execute_tool --integration pushbullet --tool pushbullet_list_devices
```

View your push history:

```
clawlink_execute_tool --integration pushbullet --tool pushbullet_list_pushes
```

## Authentication

Pushbullet uses OAuth 2.0 managed by ClawLink. No API keys are needed. Authorize access through the ClawLink dashboard. Your access token is stored securely and refreshed automatically.

Connect at: **https://claw-link.dev/dashboard?add=pushbullet**

## Connection Management

**List connections:**
```
clawlink_list_integrations
```

**Verify connection:**
```
clawlink_execute_tool --integration pushbullet --tool pushbullet_get_user
```

**Reconnect:** If a connection expires, visit the dashboard URL above and reconnect Pushbullet.

## Security & Permissions

- **Read** operations (listing devices, pushes, chats, user profile) are safe and require no confirmation.
- **Write** operations (creating pushes, chats, devices, updating settings) modify data and require confirmation.
- **Destructive** operations (deleting pushes, chats, devices, or clearing all pushes) are high-impact and irreversible.

## Tool Reference

### User Operations

| Tool | Description | Mode |
|------|-------------|------|
| `pushbullet_get_user` | Retrieve the authenticated user's profile | Read |

### Push Operations

| Tool | Description | Mode |
|------|-------------|------|
| `pushbullet_list_pushes` | List pushes with optional filtering and pagination | Read |
| `pushbullet_create_push` | Send a push (note, link, or file) to a device, user, or channel | Write |
| `pushbullet_update_push` | Dismiss or modify a push by its identifier | Write |
| `pushbullet_delete_push` | Delete a specific push by its identifier | Write (Destructive) |
| `pushbullet_delete_all_pushes` | Delete all pushes for the current user | Write (Destructive) |
| `pushbullet_upload_request` | Obtain a signed upload URL for file pushes | Write |

### Device Operations

| Tool | Description | Mode |
|------|-------------|------|
| `pushbullet_list_devices` | List all registered devices for the current user | Read |
| `pushbullet_create_device` | Register a new device under the current user's account | Write |
| `pushbullet_update_device` | Update device metadata (nickname, model, etc.) | Write |
| `pushbullet_delete_device` | Remove a device from the account | Write (Destructive) |

### Chat Operations

| Tool | Description | Mode |
|------|-------------|------|
| `pushbullet_list_chats` | List all chat objects for the current user | Read |
| `pushbullet_create_chat` | Create a new chat with a specified email address | Write |
| `pushbullet_update_chat` | Mute or unmute an existing chat | Write |
| `pushbullet_delete_chat` | Delete a chat by its identifier | Write (Destructive) |

## Code Examples

Send a note push to all devices:

```json
{
  "tool": "pushbullet_create_push",
  "args": {
    "type": "note",
    "title": "Reminder",
    "body": "Team standup in 15 minutes"
  }
}
```

Send a link to a specific device:

```json
{
  "tool": "pushbullet_create_push",
  "args": {
    "type": "link",
    "title": "Design Review",
    "url": "https://figma.com/file/abc123",
    "device_iden": "ujCvR2hKfhZSFzJ"
  }
}
```

List pushes after a specific timestamp:

```json
{
  "tool": "pushbullet_list_pushes",
  "args": {
    "modified_after": 1685500000
  }
}
```

Register a new device:

```json
{
  "tool": "pushbullet_create_device",
  "args": {
    "nickname": "Office Laptop",
    "type": "computer",
    "model": "MacBook Pro"
  }
}
```

Mute a chat:

```json
{
  "tool": "pushbullet_update_chat",
  "args": {
    "iden": "chat-iden-here",
    "muted": true
  }
}
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm pushbullet is connected.
2. Call `clawlink_list_tools --integration pushbullet` to see the live catalog.
3. Start with `pushbullet_get_user` to verify the connection.
4. Use `pushbullet_list_devices` to discover available target devices.
5. Use `pushbullet_list_pushes` to view push history.

## Execution Workflow

```
Read Flow:
  get_user → list_devices / list_pushes / list_chats

Write Flow:
  create_push (confirm) → target device receives notification

Manage Flow:
  list_devices → update_device / delete_device (confirm)
  list_chats → update_chat (mute/unmute) / delete_chat (confirm)
```

## Notes

- Pushes can target specific devices, users by email, channels, or all of the user's devices (when no target is specified).
- File pushes require a two-step process: first call `pushbullet_upload_request` to get a signed S3 URL, upload the file, then create the push with the file URL.
- Deleting all pushes is asynchronous -- it may take a moment to complete.
- Chat deletion is permanent; there is no undo.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| 401 Unauthorized | OAuth token expired; reconnect Pushbullet from the dashboard |
| 403 Forbidden | Access denied; check token scopes |
| 404 Not Found | Invalid push, device, or chat identifier |
| 429 Too Many Requests | Rate limit exceeded; Pushbullet limits API calls per minute |

## Troubleshooting

### Tools Not Visible
Run `clawlink_list_tools --integration pushbullet` to verify the integration is active. If empty, reconnect at https://claw-link.dev/dashboard?add=pushbullet.

### Push Not Delivered
Verify the target device is still registered by calling `pushbullet_list_devices`. Ensure the `device_iden` matches a valid device.

### File Upload Fails
Use `pushbullet_upload_request` first to get the signed S3 form data. The file must be uploaded to the returned URL before creating the push.

## Resources

- Pushbullet API Docs: https://docs.pushbullet.com
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=pushbullet
- ClawLink Docs: https://docs.claw-link.dev/openclaw

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=pushbullet)** -- an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
