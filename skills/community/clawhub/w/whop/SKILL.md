---
name: Whop
slug: whop
version: 1.0.1
homepage: https://clawic.com/skills/whop
description: Run and grow a Whop business with better offers, checkout flows, promo strategy, affiliates, ads, tracking, analytics, support operations, and advanced API workflows when needed
changelog: Expanded the skill with practical guidance for offers, checkout flows, promo codes, affiliates, ads, analytics, and Whop business operations.
metadata: {"clawdbot":{"emoji":"🟠","requires":{"bins":[],"config":["~/whop/"],"env.optional":["WHOP_API_KEY","WHOP_WEBHOOK_SECRET","WHOP_COMPANY_ID","WHOP_USER_ID","WHOP_RESOURCE_ID"]},"os":["linux","darwin","win32"],"configPaths":["~/whop/"]}}
---

## When to Use

User is working on Whop in any serious business sense: shaping an offer, pricing a product, creating checkout links, launching promo codes, setting up affiliates, testing ads and tracking, improving conversion, handling member operations, or using the API when the dashboard is not enough.

## Architecture

Memory lives in `~/whop/`. If `~/whop/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/whop/
├── memory.md       # Current business model, priorities, and blockers
├── offers.md       # Products, pricing, trials, waitlists, and checkout notes
├── growth.md       # Promo codes, affiliates, ads, tracking, and channel notes
├── ops.md          # Support, refunds, disputes, retention, and analytics habits
└── tech.md         # API keys, webhooks, app IDs, permissions, and automation notes
```

## Quick Start

Start with the highest-value layer first:

- Offer: what is being sold, to whom, with what pricing, trial, and checkout path
- Growth: which channels drive traffic, which affiliates matter, and how attribution is tracked
- Operations: how members are onboarded, supported, retained, refunded, and analyzed
- Automation: only use API, webhooks, or local app tooling when the native business workflow is too slow or too manual

## Quick Reference

Load the smallest file that matches the current Whop surface instead of reading everything at once.

| Topic | File |
|-------|------|
| Setup guide | `setup.md` |
| Memory template | `memory-template.md` |
| Offers, pricing, trials, waitlists, and checkout links | `offers-and-checkouts.md` |
| Promo codes, affiliates, ads, and attribution | `growth-and-marketing.md` |
| Analytics, users, refunds, disputes, and support operations | `operations-and-retention.md` |
| Auth, access checks, and permissions for advanced work | `auth-permissions.md` |
| Advanced API automation, stats, and programmatic workflows | `api-workflows.md` |
| Local app development with the proxy | `proxy-and-local-dev.md` |
| Webhooks, sandbox, and go-live checks | `webhooks-and-sandbox.md` |

## Requirements

- No API key is required for dashboard-only guidance around offers, affiliates, analytics, or operations
- `WHOP_API_KEY` is optional for advanced REST calls, stats queries, file creation, webhook management, promo-code automation, or access token creation
- `WHOP_WEBHOOK_SECRET` is optional for verifying webhook deliveries
- Optional local proxy CLI: `@whop-apps/dev-proxy` exposes `whop-proxy`
- Optional official packages: `@whop/sdk`, `@whop/embedded-components-react-js`, `@whop/embedded-components-vanilla-js`, `whop-sdk`, `whop_sdk`

## Core Rules

### 1. Start from the business goal, not the API surface
- Decide first whether the user is trying to sell more, launch faster, improve conversion, retain members, or automate a repetitive workflow.
- Default to the native Whop dashboard flow when it already solves the problem cleanly.
- Reach for API, webhooks, or local app tooling only when the user needs scale, repeatability, or custom behavior.

### 2. Optimize the offer before optimizing acquisition
- Use products, pricing, free trials, waitlists, and checkout links to sharpen the core offer first.
- Whop supports free checkout links, one-time payment links, recurring links, and split-payment checkout links in the dashboard.
- Use waitlists when qualification matters more than raw volume.

### 3. Keep attribution clean across every channel
- Use tracking links to compare email, X, Instagram, YouTube, communities, and paid traffic sources.
- Add external tracking integrations before scaling spend so the business can see more than dashboard-native numbers.
- Keep affiliate, ad, and direct traffic paths separate in notes so conversion decisions stay defensible.

### 4. Use the right growth lever for the right traffic source
- Promo codes are for controlled price incentives at checkout.
- Global affiliates expose the business to Whop's affiliate network with a default 30% commission.
- Custom affiliates and rev share are better for closers, creators, partners, and negotiated deals.
- Whop Ads exists as a native paid-growth surface, but the docs currently describe it as a beta product with limited access.

### 5. Read operations and retention as part of the funnel
- Analytics, support chats, user management, refunds, disputes, and payment operations are not back-office trivia; they change retention and reputation.
- When a business problem appears, line up acquisition source, product, checkout path, payment outcome, and member lifecycle before changing strategy.
- Use built-in analytics first, then Whop stats or webhooks if the dashboard view is not enough.

### 6. Treat advanced automation as a separate trust boundary
- Server-to-server work uses `Authorization: Bearer ...` against `https://api.whop.com/api/v1`.
- Embedded app requests inside a Whop iframe identify the current user through `x-whop-user-token`.
- Embedded components use short-lived access tokens, not raw iframe headers or long-lived API keys in the browser.
- Webhooks must be verified before side effects, and sandbox and production assets must stay fully separate.

### 7. Keep Whop IDs and environments explicit
- Preserve Whop prefixes such as `biz_`, `app_`, `prod_`, `plan_`, `user_`, `hook_`, and `file_`.
- Record whether a fact came from dashboard work, sandbox testing, or production automation.
- Handle 403s, access failures, and weird data mismatches as scope or approval problems before blaming payloads.

## Whop Traps

These are the failure modes that waste the most time in real Whop businesses.

| Trap | Consequence | Better Move |
|------|-------------|-------------|
| Scaling traffic before the offer is clear | You buy clicks into a weak checkout or confusing product | Tighten product, pricing, trial, and checkout path before increasing spend |
| Mixing promo codes, affiliates, and direct traffic in one bucket | Attribution gets muddy and decisions become guesswork | Keep one tracking path per channel and compare them cleanly |
| Using global affiliates when you really need negotiated partner terms | Margin and incentives drift out of control | Use custom affiliates or rev share for strategic partners |
| Treating analytics as a last step | Problems are discovered only after revenue drops | Review user, payment, and support signals as part of weekly operations |
| Testing payment or webhook automation directly in production | Real money movement and noisy customer data | Start in sandbox with separate keys, webhooks, and test cards |
| Using a company API key where iframe user context is required | Wrong user identity or missing entitlements | Decide first between bearer auth, `x-whop-user-token`, and short-lived access tokens |

## External Endpoints

Every network touchpoint should map to one of these declared Whop surfaces.

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| `https://api.whop.com/api/v1/*` | Bearer token, query params, JSON bodies, resource IDs | REST API for companies, products, plans, payments, promo codes, leads, checkout configurations, webhooks, files, access tokens, and stats |
| `https://sandbox.whop.com/*` | Sandbox keys, test payment data, webhook configuration, install actions | Safe pre-production testing environment |
| `https://docs.whop.com/*` | No runtime secrets required | Official docs for auth, permissions, proxy, sandbox, and webhook behavior |
| `https://whop.com/apps/*/install` | App and company selection in browser | Install and re-approve app permissions |

No other data is sent externally.

## Security & Privacy

**Data that leaves your machine:**
- Bearer credentials sent to Whop for authenticated API requests
- Business metadata, growth settings, membership data, payment filters, promo-code changes, and stats queries sent to Whop
- Webhook acknowledgements returned from your app back to Whop

**Data that stays local:**
- Offer, growth, operations, and environment notes stored in `~/whop/`
- Local proxy configuration and development URLs
- Secret values kept in environment variables rather than in project files

**This skill does NOT:**
- Store secret literals in repository files
- Skip token or webhook verification
- Push the user into API work when the dashboard path is better
- Assume sandbox parity for apps, messaging, or payouts
- Make undeclared requests outside Whop

## Trust

By using this skill, data is sent to Whop.
Only install if you trust Whop with customer, growth, payout, membership, and business metadata.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `ads` — Paid acquisition strategy, testing discipline, and media-buying tradeoffs
- `api` — General REST API patterns, auth strategies, and HTTP debugging
- `oauth` — OAuth token lifecycles, redirects, and delegated access flows
- `payments` — Payment system patterns, failure handling, and reconciliation habits
- `webhook` — Webhook verification, replay handling, and delivery design

## Feedback

- If useful: `clawhub star whop`
- Stay updated: `clawhub sync`
