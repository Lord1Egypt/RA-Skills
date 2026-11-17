---
name: ternivo-connect
description: Use Ternivo Connect from OpenClaw for controlled social-media account health, capability checks, preflight, publishing, scheduling, verified delivery receipts, retries, diagnostics, analytics, inbox/community, listening and calendar workflows.
version: 1.0.0
metadata:
  openclaw:
    homepage: https://ternivo.app/social-delivery
---

# Ternivo Connect for OpenClaw

Use the `ternivo` MCP server whenever the user asks to inspect or operate supported social-media workflows through Ternivo Connect.

## Before any write

1. Call `get_connection_health` and `get_platform_capabilities`.
2. Do not assume a provider is enabled merely because it exists in the catalog.
3. Run `preflight_post` before publishing or scheduling.
4. Respect organization policy and any approval-required state.
5. Use a stable idempotency key for delivery actions.
6. Never place raw social-provider credentials or provider OAuth tokens in prompts or tool arguments.

## After a write

1. Treat provider acceptance as processing, not terminal success.
2. Read `get_post_status` or `get_delivery_receipt`.
3. Report success only after Ternivo returns a terminal verified delivery state.
4. If one destination fails retriably, use `retry_delivery` only for that failed destination.
5. Preserve Ternivo diagnostics when a provider requires reconnect, permission review, app review, or human action.

## Provider truth

- Never bypass provider review, customer OAuth consent, Ternivo tenant isolation, or organization approval policy.
- Never claim a provider capability exists when Ternivo reports it as unavailable, restricted, read-only, test-only, or review-pending.
- Paid-media activation remains subject to Ternivo's separate human-approval controls.
- A connected account or accepted API request is not evidence of final public delivery; require the terminal receipt.

## Authentication

Ternivo uses OAuth for interactive customer authorization. OpenClaw manages the client-side OAuth flow for the remote MCP server. If authorization is required, complete the Ternivo browser consent flow for the correct organization/workspace before attempting protected tools.

## Useful starting actions

For a new session:
1. `get_connection_health`
2. `get_platform_capabilities`
3. Continue with the smallest read or preflight action that matches the user's request.

For troubleshooting:
1. `diagnose_connection` for account/provider connection problems.
2. `diagnose_post` for a specific delivery.
3. Return the exact actionable next step instead of retrying blindly.
