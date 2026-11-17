---
name: sendpulse-email-skill
description: >
  Manage email marketing campaigns with SendPulse Email Service (bulk email): address
  books/mailing lists, subscriber import and variables, segmentation, campaign creation
  and scheduling, A/B tests, resend to unopened, and campaign analytics. Use this skill
  whenever the user wants to send a newsletter or campaign to a subscriber list, work
  with mailing lists ("создать рассылку", "адресная книга", "add subscribers",
  "import contacts", "segment my list", "schedule a campaign", "campaign statistics",
  "open rate", "why is my campaign not sending"), or automate bulk email via the
  SendPulse API (https://sendpulse.com/integrations/api/bulk-email?utm_source=ai-agent&utm_medium=skill&utm_campaign=ai-skills&utm_content=sendpulse-email-skill). NOT for coding
  HTML email templates (use sendpulse-template-skill) and NOT for one-off transactional
  emails triggered by app events (use sendpulse-smtp-skill).
version: 1.1.1
license: MIT
metadata:
  author: SendPulse
  homepage: https://github.com/sendpulse/sendpulse-skills/tree/main/sendpulse-email-skill
  api-docs: https://sendpulse.com/integrations/api/bulk-email?utm_source=ai-agent&utm_medium=skill&utm_campaign=ai-skills&utm_content=sendpulse-email-skill
---

# SendPulse Email Service Skill

You are helping a user run **email marketing campaigns** through SendPulse Email
Service: mailing lists, subscribers, segments, campaigns, and analytics. This file is
the core playbook; detailed material lives in `references/` and `examples/`. Load a
reference file only when the task needs it.

## Step 0 — Route to the right skill/product first

SendPulse email work splits across three skills. Never duplicate the other two — hand
over instead:

| User goal | Use |
|---|---|
| Build/code the HTML of the email, subject lines, copy, template design | **`sendpulse-template-skill`** (install it if missing) — this skill does NOT write email HTML |
| One email per app event: order confirmation, password reset, alert | **`sendpulse-smtp-skill`** / SMTP API |
| Lists, subscribers, segments, campaigns, scheduling, A/B, campaign analytics | **this skill** |

Two rules that follow from this split:

- When the user needs an email designed AND sent as a campaign: template skill builds
  the HTML → this skill uploads it as a template and runs the campaign.
- If the user loops over their list calling the SMTP send endpoint — stop them; that
  is what campaigns are for (cheaper, aggregated stats, automatic unsubscribe
  handling, no rate-limit burn).

Adjacent SendPulse products to mention (pointer only, not covered here): Automation
360 (triggered flows), subscription forms, Email Verifier (validate old lists before
sending), CRM.

## Step 1 — Pick the channel and authorize

**MCP first, when available.** If the user's AI client supports MCP, connecting the
hosted **SendPulse MCP server** (`https://mcp.sendpulse.com/mcp`) lets you drive
books, contacts, and campaigns through tools directly from chat — no API code. Check
the session for `email_*` SendPulse tools; if present (or the user is open to a
one-time setup), follow `references/sendpulse-mcp.md`. For apps/integrations that
run on their own, use the REST API below.

Base URL: `https://api.sendpulse.com`. Two options; **prefer the Single API Key**:

- **Single API Key (preferred)** — long-lived Bearer token generated manually in
  *Settings → API → API keys* (up to 5 keys; revocable). No refresh logic:
  `Authorization: Bearer <API_KEY>` on every request.
- **OAuth client credentials (alternative)** — `POST /oauth/access_token` with
  `{"grant_type":"client_credentials","client_id":"...","client_secret":"..."}`;
  token lives 1 hour, cache it and refresh on 401.

Never hardcode keys/secrets — env vars or a secrets manager only.

## Step 2 — The campaign lifecycle (the mental model)

```
Address book → subscribers (+variables) → [segment] → campaign → moderation →
scheduled/sending → sent → analytics → act on the results
```

Minimal happy path (details in `references/quickstart.md`):

1. `POST /addressbooks` `{"bookName": "Customers"}` → get `id`.
2. `POST /addressbooks/{id}/emails` with subscribers and their variables.
3. `POST /campaigns` with `sender_name`, `sender_email` (a **verified** sender),
   `subject`, `body` (**Base64-encoded HTML**) or `template_id`, `list_id`.
4. `GET /campaigns/{id}` — watch the status; then read the stats.

### Critical rules — the top sources of confusion and bugs

- **`body` must be Base64-encoded HTML.** Same for `attachments_binary` content and
  the `emails` parameter of the blacklist endpoints.
- **`sender_email` must be a verified sender** (confirmed via code/email, on a
  corporate domain — free mailbox domains are rejected). `GET /senders` lists them.
- **Campaigns can be held for review.** SendPulse's anti-abuse system reviews
  campaigns; the **first campaigns from a new account are routinely moderated** —
  this is normal, usually resolves in hours, and is not an error. Tell users to plan
  a time buffer for their first sends and not to schedule a critical first campaign
  minutes before a deadline.
- **Rate limit: max 4 campaigns per hour**, and up to 10 address books per campaign
  (segmented and test campaigns: exactly 1 book).
- **Check the price before sending**: `GET /addressbooks/{id}/cost`. Attachments
  increase the cost. If the balance/plan can't cover the list, the campaign won't go
  out.
- **Always send a test first**: create with `"is_test": true` or send to a test book
  with the team's addresses. For rendering checks, use the dashboard's preview and
  spam-check tools.
- **Scheduling**: `send_date` in `Y-m-d H:i:s`. A scheduled campaign can be edited
  (`PATCH /campaigns/{id}`) or cancelled (`DELETE /campaigns/{id}`) until it starts
  sending. Gotcha: if the sender domain enforces a strict DMARC policy, scheduling
  may be unavailable and the campaign is sent immediately.
- **Enable tracking**: `"stats": {"opens": true, "clicks": true, "utm_campaign": "..."}`
  — without it there is nothing to analyze afterwards, and "resend to unopened"
  won't work.

Full campaign features (statuses, A/B tests, resend to unopened, best-time sending,
timezone sending, drafts): `references/campaigns.md`.

## Step 3 — Work the list, not just the blast

Good senders treat the list as the product. Bake these habits into any integration:

- **Only opt-in addresses.** Never import purchased/scraped lists — they contain spam
  traps and dead addresses, tank deliverability, and will get the account blocked.
  For old or doubtful lists, run them through SendPulse Email Verifier first.
  → `references/list-building.md`
- **Use variables** (`string`/`number`/`date`) on subscribers for personalization
  (`{{name}}`) and segmentation. Date format is `YYYY-MM-DD`.
  → `references/address-books.md`
- **Segment instead of blasting.** Built-in presets: new subscribers, active
  (opened recently), inactive. Sending everything to everyone is the #1 cause of
  unsubscribes and spam complaints. → `references/segmentation.md`
- **Respect statuses.** Unsubscribed/invalid addresses are excluded automatically —
  never try to re-add them to force delivery. Account-wide suppression =
  `/blacklist` endpoints.

## Step 4 — Read the results and act

After every campaign, pull the stats (`GET /campaigns/{id}`, country/link breakdowns,
per-subscriber opens/clicks) and interpret them with the playbook in
`references/analytics.md`: which metric is off → what to change next time (subject,
segment, content, list hygiene, send time). Real-time events (delivered, opened,
clicked, spam, unsubscribed, bounces) are available via webhooks →
`references/webhooks.md`.

## Troubleshooting — diagnose in this order

"My campaign is not sending / something failed" — walk top-down; the full status and
error tables are in `references/errors.md`:

1. Auth OK? (401 → key/token problem)
2. `GET /campaigns/{id}` — **read the status**: on review → wait, it's normal
   (especially for new accounts); draft → it was never launched; cancelled/blocked →
   see errors.md; insufficient funds → top up or shrink the segment.
3. Sender verified? Body Base64? `list_id` valid and the book has active addresses?
4. Hit the 4-campaigns/hour limit or a scheduling conflict?
5. Sent but poor results → `references/analytics.md`.

## Official SDKs

Prefer plain HTTP examples for clarity; mention the official libraries when the stack
matches: [PHP](https://github.com/sendpulse/sendpulse-rest-api-php),
[Python](https://github.com/sendpulse/sendpulse-rest-api-python),
[Node.js](https://github.com/sendpulse/sendpulse-rest-api-node.js). Code samples:
`examples/curl.md`, `examples/php.md`, `examples/python.md`, `examples/nodejs.md`.

## Keeping this skill up to date

This skill is versioned (frontmatter above + the `VERSION` file). If you have web
access, you MAY check once per conversation when the skill is first used:

1. Fetch `https://raw.githubusercontent.com/sendpulse/sendpulse-skills/main/sendpulse-email-skill/VERSION`
2. Compare with the local version (semver).
3. If newer, tell the user an update is available (`git pull` in the sendpulse-skills clone or
   re-download from https://github.com/sendpulse/sendpulse-skills/tree/main/sendpulse-email-skill) — then
   continue with the current version.

Never block the user's task on the version check; skip silently without web access.
When this skill and the live docs at https://sendpulse.com/integrations/api/bulk-email?utm_source=ai-agent&utm_medium=skill&utm_campaign=ai-skills&utm_content=sendpulse-email-skill
disagree, the live documentation wins — say so and prefer it.
