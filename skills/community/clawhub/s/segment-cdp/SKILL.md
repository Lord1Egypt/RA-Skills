---
name: segment-cdp
description: Segment CDP integration with API key authentication. Manage sources, destinations, contacts, segments, and tracking events for customer data platform operations.
---

# Segment

![Segment](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/segment.png)

Connect to Segment's Customer Data Platform to manage sources, destinations, contacts, segments, and track user events. Send identity and event data, manage suppression lists, and configure marketing integrations.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=segment-cdp) for hosted connection flows and credentials so you do not need to configure Segment API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Segment |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Segment |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│  Segment API     │
│   (User Chat)   │     │   (Proxy)    │     │  (Sources,       │
│                 │     │              │     │  Destinations)   │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                    │                      │
         │  1. Install Plugin │                      │
         │  2. Pair Device    │                      │
         │  3. Connect Segment │                      │
         │                    │  4. API Key Proxy    │
         │                    │  5. Request Forward  │
         │                    │                      │
         ▼                    ▼                      ▼
   ┌──────────┐        ┌──────────┐         ┌──────────┐
   │   SKILL  │        │ Dashboard│         │  Segment │
   │   File   │        │   Auth   │         │   CDP    │
   └──────────┘        └──────────┘         └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Segment again."

## Quick Start

```bash
# Get destination details
clawlink_call_tool --tool "segment_get_destination" --params '{"destination_id": "YOUR_DESTINATION_ID"}'

# List warehouses connected to a source
clawlink_call_tool --tool "segment_list_connected_warehouses_from_source" --params '{"source_id": "YOUR_SOURCE_ID"}'

# Identify a user with traits
clawlink_call_tool --tool "segment_identify" --params '{"user_id": "USER123", "traits": {"email": "user@example.com", "name": "Alice"}}'
```

## Authentication

All Segment tool calls are authenticated automatically by ClawLink using your Segment API key stored securely in the dashboard.

**No API key is required in chat.** ClawLink injects your API key into every Segment API request on your behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=segment and connect Segment with your API key.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `segment` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration segment
```

**Response:** Returns the live tool catalog for Segment.

### Reconnect

If Segment tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=segment
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration segment`

## Security & Permissions

- Access is scoped to the Segment workspace and sources associated with the connected API key.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (delete source, remove write key) are marked as high-impact and must be confirmed.
- Write keys for sources should be kept secure — revoke and rotate them if compromised.

## Tool Reference

### Source Management

| Tool | Description | Mode |
|------|-------------|------|
| `segment_add_labels_to_source` | Add existing labels to a Source for metadata tagging | Write |
| `segment_delete_source` | Permanently delete a Segment Source by ID | Write |
| `segment_list_connected_warehouses_from_source` | List warehouses connected to a Source | Read |
| `segment_list_schema_settings_in_source` | Retrieve schema configuration settings for a Source | Read |
| `segment_update_source` | Update a Source's metadata and settings | Write |

### Destination Operations

| Tool | Description | Mode |
|------|-------------|------|
| `segment_get_destination` | Retrieve a Destination's full configuration by ID | Read |
| `segment_list_delivery_metrics_summary_from_destination` | Get event delivery metrics summary from a Destination | Read |

### User Identification & Tracking

| Tool | Description | Mode |
|------|-------------|------|
| `segment_alias` | Alias a previous user ID to a new user ID (merge anonymous and known identities) | Write |
| `segment_group` | Associate an identified user with a group via Segment HTTP Tracking API | Write |
| `segment_identify` | Identify a user and set/update traits via Segment HTTP Tracking API | Write |
| `segment_page` | Record a page view via Segment HTTP Tracking API | Write |
| `segment_screen` | Record a mobile app screen view via Segment HTTP Tracking API | Write |
| `segment_track` | Record a custom user event via Segment HTTP Tracking API | Write |

### Data Import

| Tool | Description | Mode |
|------|-------------|------|
| `segment_batch` | Send multiple analytics calls (Identify/Track/Page/Screen/Group) in a single batch request | Write |
| `segment_import_historical_data` | Import historical data in bulk with support for original timestamps | Write |

### Keys & Access

| Tool | Description | Mode |
|------|-------------|------|
| `segment_remove_source_write_key` | Revoke an existing write key for a Source (security rotation) | Write |

### Usage & Monitoring

| Tool | Description | Mode |
|------|-------------|------|
| `segment_get_daily_per_source_api_calls_usage` | Fetch daily API call counts per source for a given period | Read |

## Code Examples

### Identify a user with traits

```bash
clawlink_call_tool --tool "segment_identify" \
  --params '{
    "user_id": "USER123",
    "traits": {
      "email": "alice@example.com",
      "name": "Alice Smith",
      "plan": "pro"
    }
  }'
```

### Track a custom event

```bash
clawlink_call_tool --tool "segment_track" \
  --params '{
    "user_id": "USER123",
    "event": "Purchased",
    "properties": {
      "product": "Widget",
      "price": 29.99,
      "currency": "USD"
    }
  }'
```

### Add labels to a source

```bash
clawlink_call_tool --tool "segment_add_labels_to_source" \
  --params '{"source_id": "YOUR_SOURCE_ID", "labels": ["production", "web"]}'
```

### Batch multiple calls

```bash
clawlink_call_tool --tool "segment_batch" \
  --params '{
    "batch": [
      {"type": "identify", "traits": {"email": "bob@example.com"}},
      {"type": "track", "event": "Signed Up", "properties": {"source": "landing-page"}}
    ]
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Segment is connected.
2. Call `clawlink_list_tools --integration segment` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `segment`.
5. If no Segment tools appear, direct the user to https://claw-link.dev/dashboard?add=segment.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → describe → call                                │
│                                                             │
│  Example: List destinations → Get metrics → Show results    │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  describe → preview → confirm → call                        │
│                                                             │
│  Example: Describe tool → Preview changes → User approves   │
│           → Execute track/identify                          │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Identify and Track calls require a valid identity (`user_id` or `anonymous_id`) — without one, events cannot be associated with users.
- Batch operations reduce HTTP overhead when sending multiple events — use them for efficiency when tracking several events at once.
- Historical data imports must include the original timestamp (`timestamp` field) to maintain accurate event chronology.
- Source write keys are sensitive — only revoke them when rotating or decommissioning a source.
- Delivery metrics provide event-level delivery status to destinations — use them to diagnose destination-level issues.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration segment`. |
| Missing connection | Segment is not connected. Direct the user to https://claw-link.dev/dashboard?add=segment. |
| `invalid_source_id` | The specified source does not exist or is not accessible with the current API key. |
| `invalid_destination_id` | The specified destination does not exist or is not accessible. |
| `missing_identity` | Track/Page/Screen calls require at least `user_id` or `anonymous_id`. |
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

1. Ensure the integration slug is exactly `segment`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Segment API Documentation](https://docs.segment.io/apis)
- [Segment Sources](https://docs.segment.io/connections/sources)
- [Segment Destinations](https://docs.segment.io/connections/destinations)
- [Segment Identify API](https://docs.segment.io/connections/sources/catalog/libraries/server/http-api/#identify)
- [Segment Track API](https://docs.segment.io/connections/sources/catalog/libraries/server/http-api/#track)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=segment-cdp
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [HubSpot CRM](https://clawhub.ai/hith3sh/hubspot-crm) — For CRM and marketing automation
- [Salesforce CRM](https://clawhub.ai/hith3sh/salesforce-ops) — For enterprise CRM operations

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=segment-cdp)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)