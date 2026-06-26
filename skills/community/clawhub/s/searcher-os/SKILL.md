---
name: searcher-os
description: Manage deal pipeline, search on-market deals, track brokers, run SBA loan calculations, manage tasks, and review CIM analyses in Searcher OS
version: 1.3.0
homepage: https://searcheros.ai
metadata:
  openclaw:
    primaryEnv: SEARCHER_OS_API_KEY
    emoji: "briefcase"
    homepage: https://searcheros.ai
---

# Searcher OS

Manage the user's M&A deal pipeline, search for businesses on the market, track broker relationships, review inbound emails, run SBA loan calculations, manage deal tasks, and analyze CIM documents via the Searcher OS REST API.

## Setup

Authentication is handled by the Searcher OS plugin. If you haven't signed in yet, run `/searcheros-login`. The user must have a Searcher OS account on the Searcher ($90/mo) or Deal Team ($244/mo) plan.

## API

**Base URL:** `https://searcheros.ai/api/agent`

All tool calls use a single endpoint:

```
POST https://searcheros.ai/api/agent/invoke
Authorization: Bearer $SEARCHER_OS_API_KEY
Content-Type: application/json

{"tool": "<tool_name>", "params": {<params>}}
```

**Responses:**
- Success: `{"ok": true, "result": {...}}`
- Error: `{"ok": false, "error": {"code": "...", "message": "..."}}`
- Confirmation needed: `{"ok": true, "result": {"status": "pending_confirmation", "confirmationId": "...", "message": "...", "expiresAt": "..."}}`

## Tool Discovery

Call `GET https://searcheros.ai/api/agent/tools` with the same Authorization header to get the live list of all available tools with their descriptions and parameter schemas. Use this to stay current as new tools are added.

## Session Start

At the start of every conversation, call `get_context` first. It returns the user's name, buy boxes, pipeline stage counts, and feed stats in a single call. Use this to:
1. Greet the user by name
2. Give a brief pipeline status (e.g., "You have 12 active deals: 5 Interested, 3 NDA Signed, 2 CIM Review, 2 Conversations")
3. Highlight anything notable (e.g., "47 new deals came in this week")
4. Suggest 2-3 next actions:
   - "Want me to check your newest on-market deals?"
   - "Ready to update the stage on any deals?"
   - "Want to search for deals matching your buy box?"

## Available Tools

### Context
- **get_context** — Get session context: user profile, buy boxes, pipeline counts, feed stats. Call FIRST at start of every conversation.
- **ping** — Health check. No params.
- **buy_box_list** — Get user's acquisition criteria (buy boxes). No params.

### Pipeline (My Deals)
- **pipeline_list** — List tracked deals. Params: `stage?` (interested|nda_signed|cim_review|conversations|loi_sent|due_diligence|closed|dead), `search?` (string), `limit?` (default 20, max 100), `offset?`
- **pipeline_get_deal** — Get full deal details. Params: `opportunity_id` (uuid, required)
- **pipeline_stage_counts** — Count deals per stage. No params.
- **pipeline_move_stage** — Move deal to new stage. Needs confirmation. Params: `opportunity_id` (uuid), `new_stage` (enum)
- **pipeline_add_note** — Add note to deal. Params: `opportunity_id` (uuid), `notes` (string)
- **pipeline_kill_deal** — Kill a deal. Needs confirmation. Params: `opportunity_id` (uuid), `kill_reason` (financial_discrepancy|deal_size_insufficient|concentration_risk|industry_mismatch|no_broker_response|overpriced|intuitive_rejection|competition|location|other), `kill_notes?`
- **pipeline_update_deal** — Update deal metadata (star, label, next action, priority). No confirmation needed. Params: `opportunity_id` (uuid), `is_starred?` (boolean), `deal_label?` (green|yellow|red|null), `next_action?` (string|null, max 500), `next_action_due?` (ISO date string|null), `priority?` (0-10)
- **pipeline_log_interaction** — Log an interaction (call, email, meeting, note) directly on a deal without needing a broker. No confirmation needed. Params: `opportunity_id` (uuid), `interaction_type` (call|email_sent|email_received|meeting|note), `subject?` (max 300), `notes?` (max 5000), `broker_id?` (uuid, optional)

### Feed (On-Market Deals)
- **feed_search** — Search on-market deals. Params: `keyword?`, `industry?` (slug), `states?` (string[]), `msas?` (string[], metro areas), `min_price?`, `max_price?`, `min_ebitda?`, `max_ebitda?`, `min_revenue?`, `max_revenue?`, `min_margin?`, `max_margin?` (0-1), `min_multiple?`, `max_multiple?`, `buy_box_id?`, `freshness_hours?`, `sort_by?` (first_seen|asking_price|sde_ebitda|gross_revenue), `sort_order?` (asc|desc), `limit?` (default 20, max 50), `offset?`
- **feed_count** — Count matching deals. Params: `keyword?`, `industry_filter?`, `states?` (string[]), `buy_box_id?`, `freshness_hours?`, `price_dropped?` (boolean), `min_price?`, `max_price?`, `min_ebitda?`, `max_ebitda?`, `min_revenue?`, `max_revenue?`
- **feed_stats** — Feed statistics (price distribution, industry/source breakdown). No params.
- **feed_save_deal** — Save deal to pipeline. Needs confirmation. Params: `staging_listing_id` (uuid), `private_notes?`
- **feed_dismiss_deal** — Dismiss deal from feed. Auto-approved by default. Params: `staging_listing_id` (uuid)

### Inbox (Inbound Emails)
- **inbox_list** — List emails. Params: `status?` (unmatched|matched|ignored), `limit?`, `offset?`
- **inbox_get_email** — Get full email. Params: `email_id` (uuid)
- **inbox_link_to_deal** — Link email to deal. Needs confirmation. Params: `email_id` (uuid), `opportunity_id` (uuid)
- **inbox_ignore** — Ignore email. Params: `email_id` (uuid)

### Brokers
- **broker_list** — List brokers. Params: `search?`, `sort_by?` (name|company|deal_count)
- **broker_get** — Get broker details. Params: `broker_id` (uuid)
- **broker_create** — Add broker. Needs confirmation. Params: `name` (required), `email?`, `phone?`, `company?`
- **broker_log_interaction** — Log interaction. Needs confirmation. Params: `broker_id` (uuid), `interaction_type` (call|email_sent|email_received|meeting|note), `subject?`, `notes?`, `opportunity_id?`

### CIM (Confidential Information Memorandums)
- **cim_list** — List CIM analyses for a deal. Params: `opportunity_id` (uuid)
- **cim_get_analysis** — Get CIM analysis details. Params: `cim_id` (uuid)
- **cim_search** — Search across CIM analyses. Params: `query?`

### Calculator
- **calculator_run** — Run an SBA 7(a) loan calculation. Computes DSCR, monthly payments, cash flow, and deal structure. Returns a verdict (FAIL/RISKY/PASS/GOOD/STRONG). Params: `asking_price` (required), `sde` (required), `down_payment_pct?` (default 0.10), `sba_rate?` (default 0.105), `sba_term_years?` (default 10), `seller_note_pct?` (default 0), `seller_note_rate?` (default 0.06), `seller_note_term_years?` (default 5), `buyer_compensation?` (default 0), `working_capital?` (default 0), `include_working_capital_in_loan?` (default true)

### Tasks
- **task_list** — List tasks for deals. Returns incomplete tasks by default. Params: `opportunity_id?` (uuid, filter to single deal), `stage?` (pipeline stage filter), `include_completed?` (default false), `limit?` (default 50, max 100), `offset?`
- **task_update** — Update a task. Mark complete/incomplete, change priority, set due date, or rename (manual tasks only). Completing the last task in a stage may auto-advance the deal. No confirmation needed. Params: `task_id` (uuid, required), `completed?` (boolean), `title?` (manual tasks only, max 500), `priority?` (1=High, 2=Medium, 3=Normal, manual tasks only), `due_date?` (YYYY-MM-DD|null)

### Confirmations
Write operations may return `"status": "pending_confirmation"`. Use these tools to manage:
- **confirmation_list_pending** — List pending confirmations. No params.
- **confirmation_check_status** — Check status. Params: `confirmation_id` (uuid)
- **confirmation_resolve** — Approve or deny. Params: `confirmation_id` (uuid), `decision` (approved|denied)
- **confirmation_get_auto_approve** — Get auto-approve settings. No params.

## Confirmation Flow

Some tools (marked "Needs confirmation") require user approval before executing:

1. Call the write tool (e.g., `pipeline_move_stage`)
2. If result has `"status": "pending_confirmation"` — tell the user it needs their approval
3. The user can approve in the Searcher OS web app OR tell you "yes, approve it"
4. If user says approve: call `confirmation_resolve` with `{"confirmation_id": "<id>", "decision": "approved"}`
5. The action executes and returns the result
6. Confirmations expire after 30 minutes if not resolved

## Rate Limits

100 requests per minute per API key. On 429 responses, check the `Retry-After` header.
