---
name: zyte-api-scraping
description: Extract structured data from websites using Zyte API (formerly Crawlera) with smart proxy rotation and browser rendering. Use this skill when users want to scrape dynamic JavaScript-rendered pages, extract data at scale, or monitor website content.
---

# Zyte API

![Zyte API](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/firecrawl.svg)

Access Zyte API from chat — extract structured data from URLs, inspect service health, and review incidents or maintenance windows.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=zyte-api-scraping) for hosted connection flows and credentials so you do not need to configure Zyte API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Zyte API |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Zyte API |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│    Zyte API       │
│   (User Chat)   │     │   (Credentials)│   │  (Scraping)      │
└─────────────────┘     └──────────────┘     └──────────────────┘
          │                       │                       │
          │  1. Install Plugin    │                       │
          │  2. Pair Device       │                       │
          │  3. Connect Zyte       │                       │
          │                       │  4. Proxy Requests │
          │                       │  5. Route Through │
          │                       │                       │
          ▼                       ▼                       ▼
    ┌──────────┐           ┌──────────┐           ┌──────────┐
    │  SKILL   │           │ Dashboard│           │  Zyte   │
    │  File    │           │ Auth     │           │ Portal │
    └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Zyte API again."

## Quick Start

```bash
# List integrations
clawlink_list_integrations

# List Zyte API tools
clawlink_list_tools --integration zyte-api

# Search for a specific tool
clawlink_search_tools --query "extract" --integration zyte-api
```

## Authentication

All Zyte API tool calls are authenticated automatically by ClawLink using the user's connected Zyte API credentials.

**No API key is required in chat.** ClawLink stores the credentials securely and injects them into every Zyte API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=zyte-api and connect Zyte API.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `zyte-api` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration zyte-api
```

**Response:** Returns the live tool catalog for Zyte API.

### Reconnect

If Zyte API tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=zyte-api
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration zyte-api`

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Zyte API is connected.
2. Call `clawlink_list_tools --integration zyte-api` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `zyte-api`.
5. If no Zyte API tools appear, direct the user to https://claw-link.dev/dashboard?add=zyte-api.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: Check status → Extract data → Return results     │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  list → get → describe → preview → confirm → call           │
│                                                             │
│  Example: Describe tool → Preview changes → User approves   │
│           → Execute extraction │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer targeted extraction and status checks before broad or repeated scraping requests.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Tool Reference

### Extraction

| Tool | Description | Mode |
|------|-------------|------|
| `zyte_api_extract` | Extract structured data from a URL | Read |
| `zyte_api_extract_batch` | Extract data from multiple URLs | Read |
| `zyte_api_scrape` | Scrape a webpage with browser rendering | Read |

### Service Health

| Tool | Description | Mode |
|------|-------------|------|
| `zyte_api_get_status` | Check Zyte API service status | Read |
| `zyte_api_list_incidents` | List active and recent incidents | Read |
| `zyte_api_list_maintenance` | List scheduled maintenance windows | Read |

### Account& Usage

| Tool | Description | Mode |
|------|-------------|------|
| `zyte_api_get_usage` | Get current API usage statistics | Read |
| `zyte_api_get_account` | Get account details and plan info | Read |

## Code Examples

### Extract data from a URL

```bash
clawlink_call_tool --tool "zyte_api_extract" \
  --params '{
    "url": "https://example.com/products",
    "follow_redirects": true,
    "browser_html": true
  }'
```

### Check service status

```bash
clawlink_call_tool --tool "zyte_api_get_status" \
  --params '{}'
```

### List recent incidents

```bash
clawlink_call_tool --tool "zyte_api_list_incidents" \
  --params '{
    "status": "open"
  }'
```

### Batch extraction

```bash
clawlink_call_tool --tool "zyte_api_extract_batch" \
  --params '{
    "urls": [
      "https://example.com/page1",
      "https://example.com/page2",
      "https://example.com/page3"
    ]
  }'
```

## Security & Permissions

- Access is scoped to the connected Zyte API account's subscription.
- **All extraction operations require explicit user confirmation** for high-volume or repeated scraping.
- Respect robots.txt and website terms of service when scraping.
- Do not use Zyte API for illegal scraping or unauthorized data extraction.
- Cost-sensitive operations (large batch jobs) require extra scrutiny before execution.

## Notes

- Zyte API handles JavaScript rendering automatically via smart proxy technology.
- Rate limits and quotas depend on the subscription plan.
- Some websites may block scraping requests; Zyte API's proxy rotation helps but cannot guarantee access.
- When extracting from many URLs, consider batching to reduce API calls.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration zyte-api`. |
| Missing connection | Zyte API is not connected. Direct the user to https://claw-link.dev/dashboard?add=zyte-api. |
| ` extraction_failed` | The URL could not be extracted. Check the URL or try with browser_html enabled. |
| `quota_exceeded` | API quota limit reached. Wait or upgrade the plan. |
| `website_blocked` | The website blocked the request. Try a different approach. |
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

### Troubleshooting: Extraction Failures

1. Verify the URL is publicly accessible.
2. Try enabling `browser_html` for JavaScript-rendered pages.
3. Check if the website blocks scraping and adjust approach accordingly.
4. For persistent failures, check Zyte API service status for outages.

## Resources

- [Zyte API Documentation](https://docs.zyte.com/zyte-api/)
- [Zyte API Overview](https://www.zyte.com/zyte-api/)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=zyte-api-scraping
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=zyte-api-scraping)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
