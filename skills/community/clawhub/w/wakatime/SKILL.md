---
name: wakatime
description: WakaTime API integration with managed OAuth. Retrieve coding statistics, track developer productivity, analyze programming languages and editor usage, view daily summaries. Use this skill when users want to check coding activity, review developer metrics, track project time, or analyze productivity patterns.
---

# WakaTime

![WakaTime](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/wakatime.svg)

Developer productivity tracking from chat -- view coding stats, language breakdowns, project time, and daily activity summaries.

Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=wakatime), an integration hub for OpenClaw that handles hosted OAuth flows and credentials so you don't need to configure WakaTime API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect WakaTime |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect WakaTime |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│  WakaTime API    │
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

1. **Get your profile**: `wakatime_get_user` with user param `"current"` -- see your WakaTime profile.
2. **View today's coding**: `wakatime_get_current_user_status_bar_today` -- get today's coding summary.
3. **Check stats by range**: `wakatime_get_user_stats_by_range` -- analyze coding patterns over a specific time period.

## Authentication

WakaTime uses managed OAuth via ClawLink. No API keys needed. Connect your WakaTime account at [claw-link.dev/dashboard?add=wakatime](https://claw-link.dev/dashboard?add=wakatime) and authorize access through the hosted flow.

## Connection Management

**List connections**: `clawlink_list_integrations` -- confirm WakaTime is connected.

**Verify**: Call `wakatime_get_user` with user `"current"` to test access.

**Reconnect**: If you see auth errors, reconnect at [claw-link.dev/dashboard?add=wakatime](https://claw-link.dev/dashboard?add=wakatime).

## Security & Permissions

All WakaTime tools are read-only. No write operations are available. All calls are safe and require no confirmation.

## Tool Reference

### User Operations

| Tool | Description | Mode |
|------|-------------|------|
| `wakatime_get_user` | Get user profile (use `"current"` for authenticated user) | Read |
| `wakatime_get_current_user_status_bar_today` | Get today's coding activity summary | Read |
| `wakatime_get_machine_names` | List user's machines with last seen time | Read |
| `wakatime_list_user_user_agents` | List plugins/editers that have sent data for a user | Read |
| `wakatime_get_users_all_time_since_today` | Get total coding time since account creation | Read |

### Statistics Operations

| Tool | Description | Mode |
|------|-------------|------|
| `wakatime_get_user_stats` | Get coding stats over the default time range | Read |
| `wakatime_get_user_stats_by_range` | Get stats for a specific time range (languages, editors, projects) | Read |
| `wakatime_get_aggregate_stats` | Get aggregate coding stats across all WakaTime users | Read |

### Summary Operations

| Tool | Description | Mode |
|------|-------------|------|
| `wakatime_get_user_summaries` | Get daily coding summaries with breakdowns by project, language, editor | Read |

### Project Operations

| Tool | Description | Mode |
|------|-------------|------|
| `wakatime_list_user_projects` | List WakaTime projects with names, IDs, and last activity | Read |

### Goal / Insight Operations

| Tool | Description | Mode |
|------|-------------|------|
| `wakatime_get_goals` | List user's goals with progress series | Read |
| `wakatime_get_insights` | Retrieve coding insights for a user over a time range | Read |

### Leaderboard Operations

| Tool | Description | Mode |
|------|-------------|------|
| `wakatime_get_leaders` | List public leaders ranked by coding activity | Read |

### Reference / Meta Operations

| Tool | Description | Mode |
|------|-------------|------|
| `wakatime_list_program_languages` | List all verified programming languages tracked by WakaTime | Read |
| `wakatime_get_editors` | List WakaTime IDE plugins with metadata | Read |
| `wakatime_get_meta` | Get API meta info including WakaTime server IPs | Read |
| `wakatime_get_oauth_authorize` | Generate OAuth 2.0 authorization URL | Read |

## Code Examples

**Get your coding profile**

```json
{
  "tool": "wakatime_get_user",
  "args": { "user": "current" }
}
```

**View today's coding activity**

```json
{
  "tool": "wakatime_get_current_user_status_bar_today"
}
```

**Get stats for the last 7 days**

```json
{
  "tool": "wakatime_get_user_stats_by_range",
  "args": { "user": "current", "range": "last_7_days" }
}
```

**List all your projects**

```json
{
  "tool": "wakatime_list_user_projects",
  "args": { "user": "current" }
}
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm `wakatime` is connected.
2. Call `clawlink_list_tools --integration wakatime` to see the live catalog.
3. Call `wakatime_get_user` with user `"current"` to verify your profile.
4. Use stats and summary tools to explore coding activity.

## Execution Workflow

```
Read Flow:  User asks for coding stats → clawlink resolves connection → WakaTime API → metrics displayed
```

## Notes

- All tools are read-only. WakaTime integration does not write any data.
- Use `"current"` as the user parameter to reference the authenticated user.
- `wakatime_get_user_summaries` requires the `read_summaries` scope.
- `wakatime_get_goals` requires the `read_goals` scope.
- Coding time values may differ from dashboard totals due to API vs. web display logic.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| 401 Unauthorized | Token expired; reconnect at the dashboard |
| 403 Forbidden | Insufficient OAuth scope for the requested data |
| 404 Not Found | Invalid user ID or username |

## Troubleshooting

### Tools Not Visible
Run `openclaw gateway restart` after installing the plugin. Start a fresh chat session.

### Missing Summaries or Goals
The OAuth connection may not have the required scopes. Reconnect to grant additional permissions.

## Resources

- WakaTime API Docs: https://wakatime.com/developers
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=wakatime
- ClawLink Docs: https://docs.claw-link.dev/openclaw

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=wakatime)** -- an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
