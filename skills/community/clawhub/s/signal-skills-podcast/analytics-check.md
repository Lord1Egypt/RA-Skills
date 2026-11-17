# Cross-checking mined claims against your own product analytics

Optional step, run after Step 4 (synthesis), before Step 5 (report). A
guest claim like "camera-permission-first onboarding drops completion
20-30%" is more useful ranked against what actually happens in *your*
product than left as an anecdote. This step turns a subset of mined
findings into `[verified against our data]` / `[contradicted by our
data]` items instead of `[anecdotal]`.

This is deliberately backend-agnostic — it does not hardcode PostHog,
Amplitude, Mixpanel, or GA4. It defines one contract and detects at
runtime which backend (if any) is actually available in the current
session, the same dependency-gating pattern Step 2 already uses for
cloud ASR (don't offer a backend as a real option if its credentials
aren't present).

## The contract

Every backend answers the same three query shapes. Whatever backend you
use, normalize its response into this shape before handing it to the
report step:

```json
{
  "metric": "funnel_step_rate | event_count | retention_curve",
  "value": 0.58,
  "n": 4200,
  "date_range": "2026-06-01..2026-07-01",
  "source": "<platform name>, <project/board name>"
}
```

- `funnel_step_rate`: completion rate at a named step, e.g. "what fraction
  of users who start onboarding complete the photo-upload step."
- `event_count`: raw count of a named event, optionally filtered
  (platform, date range) — for "did X actually spike."
- `retention_curve`: cohort retention at day N — for claims about
  stickiness/churn.

A claim is "verified" if the observed value is within the claim's stated
range (or same direction, if the claim gave no number). "Contradicted" if
it's outside that range or the opposite direction. Anything you can't map
to one of these three shapes stays anecdotal, unresolved by this step. Do
not force-fit a claim into a query it doesn't actually match.

## Step 0 — Detect what's available (don't ask if you don't have to)

Check the remembered preference first:

```bash
python3 SKILL_DIR/ledger.py config-get analytics_backend
```

If it returns something, use that backend silently. If empty, detect in
this order and stop at the first hit:

1. **PostHog** — an active PostHog MCP connection in this session
   (`ToolSearch` will surface `mcp__*posthog*` tools if one is connected),
   or a `posthog:*` skill available. This is the richest option: HogQL
   queries, no separate API key to manage, and the `posthog:querying-posthog-data`
   skill already knows how to shape a query — delegate to it rather than
   hand-rolling HogQL here.
2. **Amplitude** — `AMPLITUDE_API_KEY` and `AMPLITUDE_SECRET_KEY` in env.
3. **Mixpanel** — `MIXPANEL_SERVICE_ACCOUNT` (or
   `MIXPANEL_API_SECRET` for the older auth) in env.
4. **GA4** — `GA4_PROPERTY_ID` and a service-account credentials path
   (`GOOGLE_APPLICATION_CREDENTIALS`) in env. Flag that this one has the
   most setup friction of the four (OAuth service account, not a bearer
   key) — don't silently attempt it without both present.

If none are available, say so explicitly and skip this step entirely —
don't fabricate a comparison. Offer to remember a choice the same way
Step 2 does: `ledger.py config-set analytics_backend <name>`.

## Per-backend query recipes

Each of these is a mapping from the contract above onto that platform's
actual query mechanism. None of this runs on-device (it's a live API/MCP
call, not a local script) — but it's a single well-shaped call per claim,
not exploratory back-and-forth, so the token/latency cost is small and
bounded.

### PostHog
Prefer the `posthog:querying-posthog-data` skill or a direct MCP
`execute-sql`/`query` call with HogQL. Funnel step rate: a funnel insight
query over the named steps; event count: a trends query with the exact
event name from the claim; retention: PostHog's native retention insight.
Cite as `"PostHog, project <name>, <date range>"`.

### Amplitude
REST API, Basic Auth with `AMPLITUDE_API_KEY:AMPLITUDE_SECRET_KEY`:
- Funnel: `GET /2/funnels` with the step event sequence.
- Event count: `GET /2/events/segmentation` filtered to the event name
  and date range.
- Retention: `GET /2/retention` with the cohort definition.
Cite as `"Amplitude, project <id>, <date range>"`.

### Mixpanel
JQL via `POST /api/2.0/jql` (service account auth) is the most flexible
path for funnel/retention; `/api/2.0/segmentation` covers plain event
counts. Cite as `"Mixpanel, project <id>, <date range>"`.

### GA4
Data API `properties.runReport` (needs the `google-analytics-data`
client or a signed REST call — this is meaningfully more setup than the
other three). Funnel step rate maps to a funnel exploration reproduced as
a report; event count is a straight dimensions/metrics report filtered to
the event name; GA4 has no native retention-curve endpoint as clean as
the others — say so if a retention claim can't be mapped here rather than
approximating it.

## Feeding results back into the report

A cross-checked item's `tag`/`tag_class` in the `render_report.py` payload
upgrades from `anecdotal`/`mid` to `confirmed twice`/`sig` (verified) or
gets a distinct `contradicted`/`alert` tag (this is the single most
valuable output of this whole step: a guest's advice that doesn't hold up
against your own users). Its `reasoning` field should say what was
checked and what came back, its `source` field should carry both
citations (episode + analytics platform), e.g.:

```
"source": "<show> ep 214 (2026-06-30); cross-checked against
PostHog funnel data, <your project>, 2026-06-01..07-01: observed 58%
completion vs. claimed 65-70%, contradicted" (illustrative values)
```
