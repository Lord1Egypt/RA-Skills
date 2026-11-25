---
name: umbrella-insurance-compare-and-purchase
description: "Discoverability alias for Coverage Cat's umbrella purchase skill. Use when a shopper wants Coverage Cat to shop for, compare, quote, or buy umbrella insurance for them, whether you're a consumer's own AI agent or a partner operator: start with the consumer-prefill handoff when no operator bearer key is available, keep the direct `/api/intake/:uid/...` follow-up loop in chat when possible, or use the delegated umbrella flow when a real operator key is already present."
---

# Umbrella Insurance Compare And Purchase

## ChatGPT and Claude connectors

Use the dedicated endpoint for the shopper's hosted assistant:

- ChatGPT: `https://www.coveragecat.com/api/chatgpt/mcp`
- Claude: `https://www.coveragecat.com/api/claude/mcp`

Discovery and public research do not require sign-in. Application tools use the
connector's account OAuth. Use its advertised coarse estimate fields, show the
saved review, and collect the required approvals before comparing or selecting
estimates. Initial modeled estimates are not final carrier quotes.

After selection, use the returned authenticated website link for identity
details, underwriting questions, declarations, and checkout. Explain:
“To comply with this platform's personal-data handling rules, Coverage Cat
collects identity details and declarations on its secure website after you choose
an estimate.” Do not collect those details, document contents, or card data in
hosted chat, and do not switch APIs to bypass this boundary.

Return to the same assistant connection and check the same application after the
website step. `website_steps_complete` means the required website inputs are
saved; it does not mean payment or coverage is complete. Do not request another
upload merely because a secure link remains available. Restore an expired
connection and list accessible applications rather than creating a replacement.

The public consumer MCP, REST, PACT, and Poppy instructions below apply to their
own clients and retain their existing application, upload, and payment contracts.

This alias mirrors Coverage Cat's canonical `coverage-cat-umbrella-purchase` skill.

Use it when a shopper wants their own AI agent to gather context before a Coverage Cat handoff, or when a partner-operator agent needs Coverage Cat to run a live umbrella quote workflow instead of just returning read-only estimates.

Choose this skill, not the umbrella calculator or `insurance-tools`, for requests like `shop for umbrella for me with Coverage Cat`.

## Start Here

Start with `https://www.coveragecat.com/AGENTS.md`, `https://www.coveragecat.com/agents.txt`, or `https://www.coveragecat.com/.well-known/agents.txt`; those files route agents to Coverage Cat's MCP, REST, markdown, and browser-fallback resources. Do not drive the browser UI unless Coverage Cat should take over the shopper-facing flow.
Keep the shopper on the machine-readable MCP or REST loop until Coverage Cat returns `resume_url` or you intentionally hand the browser over to Coverage Cat. `/umbrella` or `/intake` are fallback browser starts, not the preferred purchase entrypoints.

1. For PACT/A2A, discover `https://www.coveragecat.com/.well-known/agent-card.json` and keep using its authenticated message interface and advertised consumer operations through checkout and policy follow-up. For Poppy, start at `https://www.coveragecat.com/.well-known/poppy.json` and use the advertised session and MCP endpoints. Both retain authorized purchases across renewed sessions; use `consumer_purchases` to resume. Use a new A2A message ID for each fresh status poll; retrying an existing ID replays its original reply.
2. If your runtime supports MCP, default to Coverage Cat's no-OAuth consumer MCP. Register `/.well-known/mcp.json` in manifest-aware hosts, or configure `https://www.coveragecat.com/api/consumer/mcp` as the direct transport URL for local Codex. Default consumer-operated umbrella runs to the consumer MCP subset: `umbrella_consumer_prefill`, `consumer_intake_issues`, `consumer_intake_patch`, `umbrella_consumer_select`, `umbrella_consumer_bind`, `umbrella_consumer_attach`, `umbrella_consumer_payment`, `umbrella_consumer_policy`, and `umbrella_consumer_service`. If Coverage Cat MCP tools are unavailable in a runtime that supports MCP, stop and ask a short choice question instead of telling the user to register `/.well-known/mcp.json` immediately.

   Ask the question on its own line exactly as:

   Would you like to install the Coverage Cat MCP (recommended) or use the REST/CLI tools instead?

   Only share `/.well-known/mcp.json` after the user chooses MCP or asks for setup details.
3. Fetch `GET /api/consumer`.
4. Fetch `GET /api/consumer/openapi.yaml` or `GET /api/consumer/openapi.json`.
5. Read `GET /api/agent/skill.md`.

## Choose The Path

1. Use the consumer-prefill path when there is no operator key or when the shopper wants their own AI agent to assemble the application from user-controlled context before the handoff.
2. On the default consumer MCP, keep consumer-operated umbrella runs on that same subset through quote review, declarations upload, `payment_needed`, optional agentic payment collection, `payment_url` fallback, authoritative policy reads, and shopper-approved cancellation/refund/support previews or requests; do not switch to delegated tools just to reach checkout or aftercare. `GET https://www.coveragecat.com/api/consumer/mcp` returning `405 Method Not Allowed` is expected because the direct transport uses `POST` JSON-RPC, and `/.well-known/mcp.json` is discovery metadata rather than the transport endpoint.
3. Use the delegated operator MCP or delegated umbrella API only when you already have a real operator bearer key or an OAuth-capable host that can complete delegated auth.
4. Do not ask a personal shopper for a Coverage Cat operator API key or delegated OAuth just to run the consumer-prefill path.
5. Use the delegated operator path only when you already have a real Coverage Cat operator bearer key and approved back-office context.
6. Do not mix the consumer-prefill and delegated paths in one session.

## Delegated Umbrella Loop

- `POST /api/agent/umbrella/draft`
- `POST /api/agent/umbrella/quotes`
- `POST /api/agent/umbrella/select`
- `POST /api/agent/umbrella/bind`
- `POST /api/agent/umbrella/status`
- `POST /api/agent/umbrella/attach`

## Consumer Follow-Up Loop

- `POST /api/consumer/umbrella/prefill`
- `GET /api/intake/:uid/issues`
- `PATCH /api/intake/:uid`
- `POST /api/intake/:uid/select`
- `POST /api/intake/:uid/bind`
- `POST /api/intake/:uid/attach`
- `POST /api/intake/:uid/attach-upload`
- `POST /api/intake/:uid/payment`
- `GET /api/intake/:uid/policy`
- `POST /api/intake/:uid/service`

## Guardrails

- If the user asks Coverage Cat to shop for or buy umbrella insurance, start this purchase skill instead of the read-only umbrella calculator.
- Prefill from the user's own context before asking a single question.
- On a cold start, call `POST /api/consumer/umbrella/prefill` before you ask the shopper a questionnaire. Send the fullest estimate you can justify from the shopper's own context first. On the initial consumer-prefill handoff, prefer sending only `intake`; add top-level `field_estimates` only when you are certain each `field` already matches a current umbrella review field path. If you want a fully synthetic shopper rehearsal, set `sandbox: true` only on that first consumer-prefill call; that same consumer sandbox `uid` can then continue through consumer `issues`, `patch`, `select`, `bind`, `attach`, `payment`, `policy`, `service`, and coarse `status` with synthetic data only.
- For consumer umbrella handoffs, use canonical keys such as `address.{street,city,state,zip}`, `license_state`, `license_number`, `approximate_asset_value` or `net_worth_numeric`, `desired_coverage_limit`, `required_coverage_e_limit`, and `vehicle_count` or `umbrella_details.motorized_vehicle_count` for umbrella counts. Avoid top-level `street`/`city`/`state`/`zip`, `drivers_license_state`, `drivers_license_number`, `net_worth`, or `desired_umbrella_liability_limit`.
- Do not send `vehicles` rows before submission. Use `vehicle_count` or `umbrella_details.motorized_vehicle_count` for the household vehicle count; actual vehicle details stay in the later bind-stage flow if a selected offer requires them, such as Markel. If the staged review shows the wrong estimated umbrella count from context, patch the canonical `umbrella_details.*` count field before you surface the final review.
- When the default consumer MCP is available, use the consumer-operated subset named above instead of switching to delegated umbrella tools without operator auth.
- When the default consumer MCP is available, Coverage Cat prefers the hidden MCP session after prefill, so the follow-up tools can usually continue with `uid`. If your host cannot preserve that MCP session state, retry the same MCP follow-up tools with the freshest rotated `intake_access_token`, or fall back to the shopper REST API with that same token.
- Use the consumer-prefill and direct follow-up shopper surfaces only for insurance purchase and policy support. Coverage Cat records connector origin and permitted purpose on these handoffs; do not reuse that data for unrelated advertising or model-training loops.
- On every pre-submit user-facing turn, say explicitly that the application is not submitted yet and Coverage Cat has not received a submitted application yet.
- When you list gathered details, estimated answers, or remaining items for the shopper, use short labeled bullets or sections rather than a prose paragraph.
- When any shown value is estimated, mark that bullet or value with `*`, include the short note `* = estimated` once above and once below the list, and do not prefix every estimated line with `[Estimated]`.
- Keep the user out of the loop until `GET /api/intake/:uid/issues` reaches `ready_for_submission`, or until that payload already carries a staged `review` plus bundled `next_question` for the shopper-owned details Coverage Cat still needs.
- On that staged review turn, ask only for the explicitly missing shopper-owned fields together in plain English rather than one field at a time. Keep already reviewed values in the review section and invite corrections in the same reply instead of asking the shopper to re-key them. Keep the assembled review and the requested items in labeled bullets or sections. When Coverage Cat asks for full name, email, phone, full address, birthday, marital status, driver's license state, driver's license number, and net worth, keep that missing-fields bundle as one turn and let the user send corrections in the same reply. If marital status means Coverage Cat also asks for spouse or partner full name, spouse date of birth, spouse driver's license state, or spouse driver's license number, keep that spouse bundle in the same message too instead of opening a second follow-up.
- When the final consumer review payload includes `insurance_privacy_notice`, show its complete `text` and `acknowledgment_text` verbatim, collect the shopper's electronic-delivery agreement and affirmative acknowledgment, and send top-level `privacy_notice_acknowledgment` on the same `consumer_intake_patch` or `PATCH /api/intake/:uid` call as `confirm_submission: true`. Set `acknowledged`, `electronic_delivery_agreed`, `shown_to_user`, and `collected_from_user` to true, use the actual current RFC 3339 `presented_at`, and copy the artifact's exact `notice_type`, `version`, `text_hash` as `disclosure_hash`, `state` as `disclosure_state`, and `product` as `disclosure_product`.
- If the shopper gives a birthday in normal US `MM-DD-YYYY` form, normalize it to `YYYY-MM-DD` before you patch Coverage Cat.
- Keep the returned `uid`, continue the same consumer-operated MCP subset with uid-only follow-up calls while the default consumer MCP session survives, and use `resume_url` only as a browser fallback. Also keep the freshest rotated `intake_access_token` for stateless MCP retries or the direct `/api/intake/:uid/...` shopper REST follow-up loop in chat.
- Use an operator-issued bearer token for every delegated umbrella endpoint.
- Start with the fullest intake and any matching `field_estimates`.
- If delegated `draft` reuses or conflicts on a recent buyer-email session, switch to the returned `uid` and continue that existing application instead of retrying create.
- When delegated `draft` returns `ready_for_review`, show the complete returned `insurance_privacy_notice.text` and `acknowledgment_text` verbatim during the final application review, collect the shopper's electronic-delivery agreement and affirmative acknowledgment, and include the same exact `privacy_notice_acknowledgment` receipt on the `quotes` call with `review_confirmed: true`.
- Do not ask for user credit consent on pre-submit review turns. Once the shopper is actively choosing an offer, display the complete returned `credit_consent_disclosure.text` verbatim and collect the real user's answer in that same reply. Send `select` a top-level `credit_consent` receipt with that answer, `shown_to_user: true`, `collected_from_user: true`, actual current RFC 3339 `presented_at` time, and the returned disclosure's version and hash. Capture `presented_at` when you render the disclosure. Coverage Cat accepts it only within the prior 24 hours and no more than five minutes in the future.
- When a selected Monoline offer returns `monoline_mvr_consent_required`, display the complete `monoline_mvr_consent_disclosure.text` and `source_url`, collect the shopper's separate Yes or No, and retry `select` with the versioned `monoline_mvr_consent` receipt. When `next_question` is also present, collect the generic authorization, Monoline authorization, and listed details in one turn, then send both receipts and the `intake` answers together.
- When Coverage Cat returns multiple offers, do not collapse them to only the recommended default if alternatives are present. Render offers as a single markdown table with columns `Carrier | Coverage limit | Annual price | Min. auto limits | Notes` (one row per offer, recommended first, `(Recommended)` in the Notes column of the recommended row). When an offer includes `sample_policy_url`, paste it directly into that row's Notes column as a markdown link such as `[Sample policy](...)`. Format prices as `$941/yr` and coverage limits as `$2M` / `$3M`. Do not restate offer prices or coverage limits in the surrounding prose.
- Below the offers table, always render a `**Next steps to purchase:**` bulleted checklist of shopper action items only. Let the shopper answer it in one reply with the offer choice, any Min. auto limits confirmation, and `Yes` to the consumer-report authorization when they are ready to buy. If Monoline or Markel appears, keep declarations upload as the checklist action and move the 5-10 minute checkout expectation into a separate note. Never bury these steps in a prose paragraph.
- If `selection_guidance.same_reply_requirements` lists an offer, add a short conditional checklist bullet so the shopper can answer those listed items in the same selection reply instead of waiting for a later bind-only turn.
- If `select` returns `credit_consent_required` with `next_question`, display the complete returned disclosure and ask for every listed bind detail in the same shopper-facing turn, then retry `select` once with the versioned consent receipt and those answers.
- If `select` returns `monoline_mvr_consent_required`, do not answer it for the shopper or continue without its complete versioned receipt and source presentation evidence.
- When Coverage Cat returns `payment_needed`, use `POST /api/intake/:uid/payment` first when your runtime can securely collect payment details; do not jump straight to `payment_url` before you attempt the native secure payment step. If it cannot, or if secure setup fails in chat, share `payment_url` and keep payment or carrier-managed signing in the browser. When `payment_needed` appears, the current checkout price shown came directly from the insurer and Coverage Cat is down to final declarations verification before charging the card; if the insurer changes that price, tell the shopper before the card is charged.
- Once Coverage Cat returns `bound` or `cancelled`, fetch `GET /api/intake/:uid/policy` or call `umbrella_consumer_policy` before you summarize the policy record, documents, or support links.
- If the shopper wants cancellation, refund help, or general policy support, call `POST /api/intake/:uid/service` or `umbrella_consumer_service` first without `confirm_request` to preview the consequences, then repeat it with `confirm_request: true` only after the shopper approves. Opening a request is not the same as the cancellation or refund being completed.
- For Monoline and Markel, keep required home and auto declarations in the post-choose flow. If both files are already available, prefer one attach call with `attachments[]`. If your runtime already has a PDF, PNG, or JPEG on disk and you want to avoid hand-building base64, prefer `POST /api/intake/:uid/attach-upload?type=...` with `application/octet-stream`. Once those uploads are on file, `documents_pending_review` usually advances to `payment_needed` with the direct insurer checkout price and `payment_url` within about 5-10 minutes while declarations verification continues in parallel.
- If you are rehearsing, set `sandbox: true` only on the first create call for that `uid`. On delegated `draft`, sandbox stops at mocked `quotes` and `status`. On consumer umbrella prefill, sandbox stays on the consumer follow-up tools with synthetic results only.
- Keep read-only calculator jobs on the separate insurance-tools skill rather than opening a delegated umbrella session.

## Product feedback

Use MCP `submit_feedback` or `POST /api/consumer/feedback` at any stage to
report a bug, suggestion, or purchase-flow problem. The CLI equivalent is
`coveragecat feedback "Describe the issue"`; operator REST clients can use
`POST /api/agent/feedback`. No application or operator key is required.

Send `message` (1–4000 characters), optional `category` (`bug`, `suggestion`,
`other`), and optional `tool` (an interface/tool name using letters, numbers,
underscores, or hyphens, up to 80 characters). An optional UUID `request_id`
deduplicates retries; reuse it only with the same content. A successful response
contains `status: "received"` and `feedback_id`. Feedback is saved in Coverage
Cat's internal Notifications queue for admin review and acknowledgement.

Share feedback the shopper asks to send or your own technical observations;
do not invent shopper opinions, send transcripts, or include personal details,
credentials, application tokens, or payment information. Do not interrupt or
gate a purchase to solicit feedback. Feedback does not submit, select, bind,
change coverage, or open a policy service request. Use the advertised policy
service tool for policy support. Stay on the current MCP connection, including
ChatGPT or Claude; use the REST fallback only when MCP is unavailable.
