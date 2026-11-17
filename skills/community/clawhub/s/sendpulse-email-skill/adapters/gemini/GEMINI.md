# SendPulse Email Service — project rules for Gemini

> Copy this file into your project root as `GEMINI.md` (or merge into an existing
> one). Keep the full skill folder in the repo — paths below assume
> `docs/sendpulse-email-skill/`; adjust if cloned elsewhere.

When the task involves SendPulse email campaigns (address books, subscribers,
segments, campaign creation/scheduling, A/B tests, campaign analytics, bulk-email
API), read `docs/sendpulse-email-skill/SKILL.md` first and follow it. References:

- `references/quickstart.md` — key → book → subscribers → first campaign
- `references/address-books.md` — books, import, variables, tags, blacklist
- `references/segmentation.md` — presets, conditions, dynamic lists
- `references/campaigns.md` — create/schedule, statuses, review, A/B, resend to unopened
- `references/analytics.md` — reading stats + metric→action playbook
- `references/api-reference.md` — full endpoint catalog
- `references/errors.md` — troubleshooting order, status decoder
- `references/webhooks.md` — real-time events incl. task_status_update
- `references/list-building.md` — opt-in, double opt-in, hygiene
- `examples/` — curl, PHP, Python, Node.js

Hard rules (apply even without reading the references):

1. Routing: email HTML → `sendpulse-template-skill`; transactional sends →
   `sendpulse-smtp-skill`; never loop a send endpoint over a list — use campaigns.
2. Auth: prefer the Single API Key (*Settings → API*); OAuth (1 h TTL) as
   alternative; credentials from env vars.
3. `POST /campaigns`: `body` Base64-encoded (or `template_id`); verified
   `sender_email` on a corporate domain; max 4 campaigns/hour; ≤10 books.
4. Blacklist `emails` = Base64 of a comma-separated string. Date variables
   `YYYY-MM-DD`.
5. Campaign held for review = normal (especially first sends) — read the status
   before debugging; never speculate about or help evade moderation.
6. Drive the pre-flight: segment (not "everyone") → test send → cost check →
   tracking + UTM → schedule; afterwards read the stats and recommend changes.
7. Opt-in lists only; mirror opt-outs immediately; never re-import unsubscribed or
   bounced addresses.
8. Backoff-retry on 429/5xx only.
