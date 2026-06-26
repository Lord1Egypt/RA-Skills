---
name: reddit-communities
description: Manage Reddit posts, comments, subreddits, users, moderation, and community workflows via the Reddit API. Use when users want to search subreddits, inspect posts, submit content, manage comments, or automate moderation actions.
---

# Reddit

![Reddit](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/reddit.svg?v=2)

Manage Reddit from chat — posts, comments, subreddits, users, moderation, and community workflows via the Reddit API.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=reddit-communities) for hosted connection flows and credentials so you do not need to configure Reddit API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Reddit |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Reddit |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ Reddit │
│   (User Chat)   │     │   (OAuth)    │     │ (Reddit API)      │
└─────────────────┘     └──────────────┘     └──────────────────┘
          │                       │                       │
          │  1. Install Plugin    │                       │
          │  2. Pair Device      │                       │
          │  3. Connect Reddit   │                       │
          │                      │  4. Secure Token      │
          │                      │  5. Proxy Requests    │
          │                      │                       │
          ▼                      ▼                       ▼
    ┌──────────┐          ┌──────────┐          ┌──────────┐
    │  SKILL   │          │ Dashboard│          │ Reddit │
    │  File    │          │ Auth     │          │ Community│
    └──────────┘          └──────────┘          └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Reddit again."

## Quick Start

```bash
# List available Reddit tools
clawlink_list_tools --integration reddit

# Search subreddits
clawlink_call_tool --tool "reddit_search_subreddits" --params '{"query": "machinelearning"}'
```

## Authentication

All Reddit tool calls are authenticated automatically by ClawLink using the user's connected Reddit account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Reddit API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=reddit and connect Reddit.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `reddit` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration reddit
```

**Response:** Returns the live tool catalog for Reddit.

### Reconnect

If Reddit tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=reddit
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration reddit`

## Security & Permissions

- Access is scoped to the Reddit account's accessible data via the connected OAuth scopes.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (delete post, remove comment, ban user) are marked as high-impact and must be confirmed.
- Moderation actions affect community members — confirm before executing bulk or automated moderation.

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Reddit is connected.
2. Call `clawlink_list_tools --integration reddit` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `reddit`.
5. If no Reddit tools appear, direct the user to https://claw-link.dev/dashboard?add=reddit.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: Search subreddits → Get posts → Show results      │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                     │
│  list → get → describe → preview → confirm → call            │
│                                                             │
│  Example: Describe tool → Preview changes → User approves   │
│           → Execute write                                    │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Reddit API rate limits apply — avoid bulk operations without throttling.
- Moderation tools require moderator permissions on the target subreddit.
- Some actions (like cross-posting or modmail) require specific OAuth scopes.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration reddit`. |
| Missing connection | Reddit is not connected. Direct the user to https://claw-link.dev/dashboard?add=reddit. |
| `RATELIMIT` | Too many requests — wait before retrying. |
| `INSUFFICIENT_PERMISSIONS` | The account lacks moderator permissions for this subreddit. |
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

1. Ensure the integration slug is exactly `reddit`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Reddit API](https://www.reddit.com/dev/api/)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=reddit-communities
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [Reddit Ads](https://clawhub.ai/hith3sh/reddit-ads-campaigns) — For Reddit advertising campaigns

---

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
