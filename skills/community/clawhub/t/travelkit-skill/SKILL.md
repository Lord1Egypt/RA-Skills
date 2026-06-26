---
name: travelkit
description: TravelKit flight booking and management skill. Use for flight search, pricing, real-time price verification, order creation, payment, cancellation, refund, change, itinerary download, and TravelKit MCP integration policy. Always use this skill for TravelKit flight lifecycle tasks.
version: 1.1.0
---

# TravelKit Flight Skill

Keep consumer replies in Simplified Chinese unless the user requests another language. Load only the smallest reference needed for the current step; do not preload shared references unless the active workflow points to them.

## Tool Routing

When this skill applies, always follow this skill workflow first. TravelKit MCP tools are execution primitives inside the workflow, not standalone business entry points.

- Use the Fast Routing table to choose the workflow reference before calling any MCP tool.
- Call MCP tools only when the active workflow explicitly instructs the call and all required preconditions are met.
- Do not bypass skill rules because a tool description appears to match the user's request.
- Keep business decisions, safety checks, user confirmations, passenger-data timing, and output formatting in the skill workflow.
- Treat MCP tool results as raw capability results; summarize and continue through the skill rules instead of exposing raw tool behavior to users.
- Before search, lightweight requirement parsing may normalize user intent into internal query parameters. Do not output JSON or a full parsed-field list to normal users unless they explicitly ask for that format.

## Version Notice

If the host platform or SkillHub injects daily version-check facts, consume them without trying to verify versions independently.

- If `skillVersionStatus` is `outdated`, briefly tell the user the installed TravelKit Skill version is not the latest and recommend updating through SkillHub or the host platform. Include `installedVersion`, `latestVersion`, and `updateUrl` only when provided.
- If `skillVersionStatus` is `latest`, do not mention version status.
- If `skillVersionStatus` is `unknown`, do not claim the installed skill is outdated. Only suggest checking SkillHub or the project release page when the user asks about installation, configuration, version, updates, missing tools, API key setup, or unexpected behavior.
- Version notices must not block or derail normal flight search, booking, payment, refund, change, order lookup, or itinerary workflows.
- Do not create timers, background jobs, or version polling from the skill. Daily check frequency and per-user/per-workspace state belong to the host platform.

## Fast Routing

| User intent | Read | Tool(s) |
|---|---|---|
| Search or compare flights | [flight-search](references/flight-search.md) | `flight_search` |
| Price a known flight number | [flight-pricing](references/flight-pricing.md) | `flight_pricing` |
| User selects a search option | [flight-verify](references/flight-verify.md) | `flight_verify_solution` |
| Create an order after verified price | [flight-create-order](references/flight-create-order.md) | `flight_create_order` |
| Pay an order | [flight-pay-order](references/flight-pay-order.md) | `flight_pay_order` |
| Look up orders | [flight-order-lookup](references/flight-order-lookup.md) | `flight_order_detail`, `flight_order_detail_by_external_id`, `flight_order_list` |
| Invoice application | [flight-invoice](references/flight-invoice.md) | `flight_get_order_invoice_application`, `flight_create_order_invoice_application` |
| Cancel an order | [flight-cancel](references/flight-cancel.md) | `flight_cancel_order` |
| Refund | [flight-refund](references/flight-refund.md) | `flight_refund_quote`, `flight_refund_money_search`, `flight_refund_request`, `flight_refund_confirm` |
| Change flight | [flight-change](references/flight-change.md) | `flight_change_search`, `flight_change_request` |
| Download itinerary | [flight-itinerary](references/flight-itinerary.md) | `flight_download_itinerary` |
| API key / credential issues | [mcp-connection](references/mcp-connection.md) | N/A |

## Core Rules

- Search before booking; verify real-time price before collecting passenger information or creating an order.
- Never expose internal fields such as `solutionId`, `orderKey`, confirmation flags, raw MCP JSON, API keys, `passengerIds`, `segmentIds`, or idempotency keys to normal users.
- Normal user-visible replies must never contain `PNR`, `airlinePnr`, airline PNR, `票号/PNR`, or `票号 / PNR`; omit or rewrite those fields even if returned, empty, or present in an error message.
- If `TRAVELKIT_API_KEY` is missing or invalid, treat it only as a platform-managed credential issue. Never invent or output local MCP configuration snippets such as `mcpServers`, `npx`, stdio server setup, or local config JSON.
- Never invent missing tool data. If baggage, refund/change policy, ticketing, deadline, fees, or status data is absent, say it was not returned.
- For order creation, order lookup, and post-payment checks, use [output-rules](references/output-rules.md): total price = fare + tax.
- Search/pricing/verify/order lookup/invoice lookup/itinerary/change-search/refund quote are read operations and can be called as needed.
- Create order, pay, cancel, create invoice application, refund request/confirm, and change request are write operations; get explicit user confirmation for the exact action first.
- Search stage collects only route, dates, passenger counts, cabin, and preferences. Collect ID/passport/phone/email only after price verification succeeds and the user confirms they want to proceed.

## Write Confirmation

Before any write tool, summarize the business action and wait for explicit confirmation. After confirmation, set required internal confirmation fields without asking users about production or technical flags. Read [confirmation-rules](references/confirmation-rules.md) only when preparing a write operation.
