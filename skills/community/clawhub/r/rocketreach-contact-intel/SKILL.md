---
name: rocketreach-contact-intel
description: Search people and companies, inspect contact intelligence, and review company signals in RocketReach — funding, growth, size, and tech stack. Use when users want to find decision-maker contact info, research company profiles, or build prospect lists.
---

# RocketReach

![RocketReach](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/rocketreach.png)

Search people and companies, inspect contact intelligence, and review company signals in RocketReach — funding, growth, size, and tech stack via the RocketReach API.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=rocketreach-contact-intel) for hosted connection flows and credentials so you do not need to configure RocketReach API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect RocketReach |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect RocketReach |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ RocketReach      │
│   (User Chat)   │     │   (OAuth)    │     │ (API)             │
└─────────────────┘     └──────────────┘     └──────────────────┘
          │                       │                       │
          │  1. Install Plugin    │                       │
          │  2. Pair Device       │                       │
          │  3. Connect RR       │                       │
          │                      │  4. Secure Token        │
          │                      │  5. Proxy Requests     │
          │                      │                       │
          ▼ ▼                       ▼
    ┌──────────┐          ┌──────────┐          ┌──────────┐
    │  SKILL   │          │ Dashboard│          │ RocketReach│
    │  File    │          │ Auth     │          │ Platform │
    └──────────┘          └──────────┘          └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for RocketReach again."

## Quick Start

```bash
# Look up a person by email
clawlink_call_tool --tool "rocket_reach_lookup_person" --params '{"email": "ceo@company.com"}'

# Look up a company
clawlink_call_tool --tool "rocket_reach_lookup_company" --params '{"company_name": "Acme Corp"}'

# Get company funding
clawlink_call_tool --tool "rocket_reach_get_company_funding" --params '{"domain": "acme.com"}'
```

## Authentication

All RocketReach tool calls are authenticated automatically by ClawLink using the user's connected RocketReach account.

**No API key is required in chat.** ClawLink stores the credentials securely and injects them into every RocketReach API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=rocketreach and connect RocketReach.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `rocketreach` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration rocketreach
```

**Response:** Returns the live tool catalog for RocketReach.

### Reconnect

If RocketReach tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=rocketreach
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration rocketreach`

## Security & Permissions

- Access is scoped to the RocketReach account's accessible data.
- **All operations require explicit user confirmation.** Before executing lookups or searches, confirm the target person or company with the user.
- RocketReach lookups consume API credits — confirm before doing bulk lookups.
- Do not store or log personal data without explicit consent.

## Tool Reference

### Person Lookup

| Tool | Description | Mode |
|------|-------------|------|
| `rocket_reach_lookup_person` | Look up a person by email | Read |
| `rocket_reach_lookup_person_and_company` | Look up person and company in one call | Read |
| `rocket_reach_check_person_status` | Check status of person lookup requests | Read |
| `rocket_reach_search_people` | Search people by name, title, or keywords | Read |

### Company Lookup

| Tool | Description | Mode |
|------|-------------|------|
| `rocket_reach_lookup_company` | Look up a company by name | Read |
| `rocket_reach_search_companies` | Search companies by name or keyword | Read |
| `rocket_reach_get_company_funding` | Get company funding history | Read |
| `rocket_reach_get_company_growth` | Get company growth metrics | Read |
| `rocket_reach_get_company_size` | Get company employee size | Read |
| `rocket_reach_get_company_industries` | Get company industry tags | Read |
| `rocket_reach_get_company_tech_stack` | Get company technology stack | Read |

### Account

| Tool | Description | Mode |
|------|-------------|------|
| `rocket_reach_get_account` | Get account information | Read |

## Code Examples

### Look up a person by email

```bash
clawlink_call_tool --tool "rocket_reach_lookup_person" \
  --params '{
    "email": "founder@startup.com"
  }'
```

### Look up a company by domain

```bash
clawlink_call_tool --tool "rocket_reach_lookup_company" \
  --params '{
    "company_name": "Stripe"
  }'
```

### Get company funding

```bash
clawlink_call_tool --tool "rocket_reach_get_company_funding" \
  --params '{
    "domain": "stripe.com"
  }'
```

### Get company tech stack

```bash
clawlink_call_tool --tool "rocket_reach_get_company_tech_stack" \
  --params '{
    "domain": "stripe.com"
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm RocketReach is connected.
2. Call `clawlink_list_tools --integration rocketreach` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `rocketreach`.
5. If no RocketReach tools appear, direct the user to https://claw-link.dev/dashboard?add=rocketreach.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                      │
│  lookup → search → get → call                                │
│                                                             │
│  Example: Lookup person → Get profile → Show contact info    │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools or ambiguous requests, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer person and company reads before credit-consuming actions.
4. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- RocketReach lookups consume API credits — check account balance before bulk operations.
- Person lookups by email are the most reliable lookup method.
- Company lookups require a confirmed domain for tech stack and funding data.
- Async lookup requests can be checked with `rocket_reach_check_person_status`.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration rocketreach`. |
| Missing connection | RocketReach is not connected. Direct the user to https://claw-link.dev/dashboard?add=rocketreach. |
| `NO_MATCH` | No person or company found for the given criteria. |
| `INSUFFICIENT_CREDITS` | Not enough API credits for this lookup. |
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

1. Ensure the integration slug is exactly `rocketreach`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.

## Resources

- [RocketReach API](https://rocketreach.co/api)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=rocketreach-contact-intel
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [Apollo](https://clawhub.ai/hith3sh/apollo-contact-intel) — For alternative contact intelligence
- [Research to Sheets](https://clawhub.ai/hith3sh/research-to-sheets) — For saving research to spreadsheets

---

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
