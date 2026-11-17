---
name: uberfix-maintenance
description: Create and follow maintenance requests in UberFix using authorized tools.
---

# UberFix Maintenance

Use when the user needs to open a maintenance request, check its status, inspect its details, add a note, cancel a request, or request a quotation in UberFix.

## Connection

This skill **does not** directly authenticate or call UberFix. Use installed UberFix tools exposed by an authorized OpenClaw plugin, or a separately connected MCP client. Current operational endpoint requires a provisioned `x-api-key` and is **not** a user OAuth connector. Never request a shared or administrator credential from the end user.

## Actions

- `uberfix_create_maintenance_request`: collect `client_name`, `client_phone`, `location`, `title`, `description`; optional `service_type`, `priority`, `latitude`, `longitude`.
- `uberfix_check_request_status`: `search_term` is a request number or client phone; optional `search_type`.
- `uberfix_get_request_details`: use `request_number` or `request_id` and `client_phone` if required.
- `uberfix_add_request_note`: requires `request_id`, `note`, `client_phone`.
- `uberfix_cancel_request`: requires `request_id`, `client_phone`, `reason`; explicitly confirm cancellation with the user before calling.
- `uberfix_get_quote`: currently **creates a quotation request record**, not a side-effect-free price lookup. Collect `service_type`, `description`, `client_name`, `client_phone` and obtain the user's explicit approval before calling. Do not present it as a read-only estimate.

## Operating rules

Only use live tool responses as authoritative. Never invent request IDs, prices or statuses. If authentication or tenant authorization fails, explain the failure rather than bypassing it. Treat customer phone number as a lookup input, **not proof of ownership**. Current backend API-consumer authorization is not proven to be tenant-isolated; only use keys restricted to the intended company and do not claim cross-tenant protection has been tested. Do not modify workflows or database records directly.
