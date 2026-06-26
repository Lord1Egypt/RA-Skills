---
name: reddit-ads-campaigns
description: Inspect Reddit Ads campaigns, ad groups, creatives, and reporting data via the Reddit Ads API. Use when users want to review campaign performance, audit ad group settings, check creative status, or analyze advertising metrics.
---

# Reddit Ads

![Reddit Ads](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/reddit.svg?v=2)

Inspect Reddit Ads from chat — campaigns, ad groups, creatives, and reporting data via the Reddit Ads API.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=reddit-ads-campaigns) for hosted connection flows and credentials so you do not need to configure Reddit Ads API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Reddit Ads |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Reddit Ads |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ Reddit Ads │
│   (User Chat)   │     │   (OAuth)    │     │ (Ads API)        │
└─────────────────┘     └──────────────┘     └──────────────────┘
          │                       │                       │
          │  1. Install Plugin    │                       │
          │  2. Pair Device       │                       │
          │  3. Connect Reddit    │                       │
          │                       │  4. Secure Token       │
          │                       │  5. Proxy Requests     │
          │                       │                       │
          ▼                       ▼                       ▼
    ┌──────────┐ ┌──────────┐           ┌──────────┐
    │  SKILL   │           │ Dashboard│           │ Reddit │
    │  File    │           │ Auth     │           │ Ads UI   │
    └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Reddit Ads again."

## Quick Start

```bash
# List campaigns
clawlink_list_tools --integration reddit-ads

# Inspect campaign structure
clawlink_call_tool --tool "redditads_list_campaigns" --params '{}'
```

## Authentication

All Reddit Ads tool calls are authenticated automatically by ClawLink using the user's connected Reddit account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Reddit Ads API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=reddit-ads and connect Reddit Ads.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `reddit-ads` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration reddit-ads
```

**Response:** Returns the live tool catalog for Reddit Ads.

### Reconnect

If Reddit Ads tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=reddit-ads
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration reddit-ads`

## Security & Permissions

- Access is scoped to the Reddit Ads account accessible via the connected OAuth app.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (pause campaign, delete ad group) are marked as high-impact and must be confirmed.
- Confirm before launching, pausing, or editing live ads — changes affect real campaign spend.

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Reddit Ads is connected.
2. Call `clawlink_list_tools --integration reddit-ads` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `reddit-ads`.
5. If no Reddit Ads tools appear, direct the user to https://claw-link.dev/dashboard?add=reddit-ads.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → describe → call                               │
│                                                             │
│  Example: List campaigns → Inspect structure → Show results │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  list → get → describe → preview → confirm → call            │
│                                                             │
│  Example: Describe tool → Preview changes → User approves   │
│           → Execute update                                   │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Reddit Ads API requires an approved Reddit Ads account — self-serve accounts need sufficient spend history.
- This is a hybrid skill — tool availability depends on the specific Reddit Ads API scopes granted during connection.
- Campaign changes affect live spend — always confirm before editing active campaigns.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration reddit-ads`. |
| Missing connection | Reddit Ads is not connected. Direct the user to https://claw-link.dev/dashboard?add=reddit-ads. |
| `AD_ACCOUNT_NOT_FOUND` | The connected account does not have an active Reddit Ads account. |
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

1. Ensure the integration slug is exactly `reddit-ads`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Reddit Ads API](https://ads-api.reddit.com/docs/)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=reddit-ads-campaigns
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [Reddit Communities](https://clawhub.ai/hith3sh/reddit-communities) — For Reddit community and content management

---

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
