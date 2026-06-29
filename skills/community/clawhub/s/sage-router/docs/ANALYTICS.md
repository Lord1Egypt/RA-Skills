# Sage Router Analytics

Sage Router Analytics is the paid observability layer: hosted routing can be free/cheap, while performance intelligence is the monetized feature.

## Product promise

One endpoint for your AI subscriptions, with live performance analytics so you always use the best model.

Users bring provider subscriptions/keys. Sage sells:

- provider/model latency trends
- success/error rates
- fallback frequency
- fastest model recommendations
- most reliable model recommendations
- degraded-provider alerts
- team/project analytics history
- policy recommendations

## Runtime endpoint

```bash
GET /analytics?days=7&limit=10000
Authorization: Bearer $SAGE_ROUTER_ANALYTICS_TOKEN # optional when configured
```

The endpoint returns:

- `providers[]` performance summaries
- `models[]` performance summaries
- `intents[]` task-level summaries
- `recommendations.fastestModels[]`
- `recommendations.mostReliableModels[]`
- `recommendations.degradedModels[]`

Supabase onboarding metadata is bounded separately from route telemetry. Email
signup and magic-link requests may attach selected hosted plan, signup surface,
auth method, UTM source/medium/campaign, referrer host, and landing path to the
Supabase user record; OAuth redirects keep that same coarse context in browser
storage. Do not attach prompts, workflow text, provider credentials, OAuth
tokens, generated API keys, private keys, raw URLs, cookies, raw provider
responses, or customer data.

## Launch Funnel Endpoint

```bash
GET /analytics/funnel?days=30&limit=10000
Authorization: Bearer $SAGE_ROUTER_ANALYTICS_TOKEN # or an operator key
```

The operator-only funnel summarizes the hosted launch path without returning
PII or request content:

- waitlist leads
- managed-access beta interest and share of waitlist
- managed-access demand by target provider family and commercial preference
- signups
- customers with generated API keys
- customers with a first routed request
- paid conversions
- paid customers with recent routed usage
- estimated current MRR, target attainment, and per-plan gaps against the
  public `$10k MRR` recommended launch mix
- prioritized plan revenue actions sorted by remaining MRR gap
- anonymous marketing intent by event, plan, source surface, and coarse
  attribution channel
- checkout-readiness friction from aggregate checkout intent and checkout
  unavailable events, so broken Stripe/readiness handoffs show as a revenue
  bottleneck before more traffic is purchased
- ranked acquisition actions from source/channel buckets, so the operator can
  choose the next outreach or page-improvement motion without identities or raw
  campaign URLs
- target-aware bottlenecks for signup-to-key, key-to-first-request,
  setup-copy activation, signup-to-paid, paid recent usage, checkout
  readiness, and `$10k MRR` attainment
- conversion actions derived from those bottlenecks, with owner, surface,
  success metric, and bounded action copy for the next activation or revenue
  fix

The funnel reads only timestamps, allowlisted managed-access qualification
buckets, coarse CTA attribution buckets, setup snippet IDs, and countable
customer/key status fields from the customer store, API-key store, waitlist
tables, and route telemetry. Account-page setup copy telemetry also records a
bounded `state` such as `copied` or `selected`, so clipboard-denied browsers
still count manual text selection as setup-copy activation without storing the
snippet body. It does not return email addresses, prompts, message bodies, API
keys, copied snippet bodies, provider credentials, OAuth tokens, raw campaign
URLs, or raw responses.

The hosted operator dashboard at
`https://app.sagerouter.dev/launch-funnel.html` is a static shell for this
endpoint. It requires a private operator/admin token in the browser, sends it as
an `Authorization: Bearer` header, and stores the token only in tab-scoped
`sessionStorage` when the operator explicitly enables that option. Customer
accounts never use this page; signed-in customer analytics remain scoped to
`/account/analytics`. The bottleneck table compares current rates with the
launch-plan targets, including setup-copy to first-request activation and
checkout-readiness friction from aggregate `account_checkout_unavailable` and
`calculator_checkout_unavailable` counts.
The acquisition actions table ranks active source/channel signals by anonymous
CTA clicks, and the revenue actions table ranks Lite, Pro, and Max plan gaps by
remaining MRR so the operator can choose the next acquisition motion without
returning customer identities.
The conversion actions table sits between those views and translates
target-aware bottlenecks into the next owner/surface/success metric to work,
without returning identities, prompts, keys, provider credentials, or raw
campaign URLs.
The dashboard also builds a copyable no-secret operator launch brief from the
same aggregate funnel snapshot. It condenses `$10k MRR` attainment, activation,
checkout friction, the top conversion move, revenue motions, deterministic
acquisition links, managed-access demand, and GitHub OAuth onboarding state for
founder-sales or support follow-up without emails, prompts, OAuth tokens,
generated API keys, provider credentials, raw campaign URLs, or raw responses.
The same dashboard includes an operational readiness panel backed only by
public `/edge/health` and `/pricing` metadata. It keeps live edge health,
customer API-key enforcement, Stripe checkout/portal readiness, and
managed-provider gating visible next to MRR actions without sending the private
operator token to those public metadata routes.

For terminal refreshes, use the secret-safe snapshot helper:

```bash
scripts/summarize_sagerouter_launch_funnel.sh --days 30
```

It reads the same operator-only endpoint with `SAGE_ROUTER_ANALYTICS_TOKEN`,
`SAGE_ROUTER_OPERATOR_TOKEN`, or `SAGE_ROUTER_API_KEY`, then prints aggregate
activation queue, acquisition, revenue-gap, bottleneck, and privacy fields. It
does not print tokens, emails, generated keys, prompts, provider credentials,
OAuth tokens, raw campaign URLs, or raw provider responses. Pass `--json` for a
bounded JSON subset suitable for automation; the `activationQueue` object is
the stable field for no-key follow-up counts, sendable/review-only segments,
dry-run coverage, sent-recipient counts, and approval-required state.

The same hosted operator dashboard includes a customer review panel backed by
`/admin/customers`. It uses the same private token boundary as the global
funnel, and the public edge pins `/admin` traffic to the control-plane origin
instead of the lowest-latency model backend. The customer review table is for
support, abuse, chargeback, and activation review only; it renders bounded
customer, usage, activation, server-derived review flags, secret-free operator
audit events, and public API-key metadata without raw generated keys, key
hashes, provider credentials, prompts, or raw responses.

## Account readiness

The hosted customer dashboard at `https://app.sagerouter.dev/analytics.html`
combines signed-in route analytics with the existing account control-plane
endpoints:

- `/account/plan`
- `/account/usage` (`usage` plus server-derived `activation`)
- `/account/api-keys`

This keeps conversion guidance close to the customer's telemetry. A signed-in
user can see whether they still need to create a generated key, finish Stripe
checkout, send a first routed request, or upgrade before monthly quota blocks
agent traffic. The `activation` object contains only safe state such as plan,
routing status, active key count, current-period request count, quota percent,
first-request completion, and `nextAction`; it does not expose keys, prompts,
provider credentials, or global customer totals. The dashboard does not expose
operator funnel data.

## Privacy model

The analytics feed is built from route telemetry only. It does not store prompts, message bodies, provider credentials, OAuth tokens, or API keys.

Tracked telemetry:

- timestamp
- intent
- selected provider/model
- attempted providers/models
- elapsed milliseconds
- success/failure status
- coarse requirements flags

## Monetization shape

- Free: hosted endpoint, short/no history, basic routing
- Pro: 30-90 day analytics, recommendations, exports
- Power: long-term history, alerts, A/B tests, custom policies
- Team: shared dashboards, audit logs, per-project provider analytics

## Why this is valuable when users bring their own subscriptions

The value is not model access. The value is knowing which subscription performs best for each workload over time, and automatically routing around slow or failing providers.


## Durable Cloud Analytics

Production analytics now writes privacy-safe route telemetry to Google Firestore and mirrors the same event stream plus generated snapshots into the Autonomous Ops Studio Supabase project.

### Storage

- Firestore collection: `sage_router_route_events`
- Supabase tables:
  - `public.sage_router_route_events`
  - `public.sage_router_analytics_snapshots`

Stored events intentionally exclude prompts, message bodies, provider credentials, API keys, OAuth tokens, and raw responses.

### Auth

The hosted browser dashboard on `https://app.sagerouter.dev/analytics.html`
uses `GET /account/analytics` with the signed-in customer's Supabase session.
That route only returns telemetry for the active customer account.

`GET /analytics` is the operator/global route and accepts either:

- `Authorization: Bearer $SAGE_ROUTER_ANALYTICS_TOKEN`, or
- a configured operator key from `SAGE_ROUTER_CLIENT_API_KEYS`.

Supabase service-role credentials are used only server-side for mirror writes and backend analytics reads.
