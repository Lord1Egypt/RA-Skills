---
name: Yelp
slug: yelp
version: 1.0.0
homepage: https://clawic.com/skills/yelp
description: Search Yelp businesses and reviews, compare local options, and audit listing quality with official APIs, public pages, and safe action boundaries.
changelog: Initial release with local business discovery, review signal interpretation, shortlist guidance, and listing audit support.
metadata: {"clawdbot":{"emoji":"⭐","requires":{"bins":["curl","jq"],"config":["~/yelp/"]},"os":["linux","darwin","win32"],"configPaths":["~/yelp/"]}}
---

## When to Use

User wants to work on Yelp directly: find restaurants or local services, compare businesses, inspect reviews, check delivery or takeout signals, or audit a Yelp listing with source-aware workflows.

Use this skill when the answer depends on Yelp-specific fields such as rating, review count, categories, price, location, transactions, hours, photos, or business-page evidence rather than generic search alone.

## Architecture

Memory lives in `~/yelp/`. If `~/yelp/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/yelp/
├── memory.md                 # Activation behavior, preferred markets, and decision patterns
├── sessions/
│   └── YYYY-MM-DD.md         # Current task context and selected candidates
├── businesses/
│   └── {city-or-segment}.md  # Saved shortlists, business aliases, and notes
├── api/
│   ├── alias-cache.md        # name+location -> Yelp alias or business ID
│   └── request-log.md        # Redacted endpoint, params, status, timestamp
└── audits/
    └── {business}.md         # Listing-quality findings and next actions
```

## Quick Reference

Load only the file needed for the current Yelp task.

| Topic | File |
|-------|------|
| Setup and activation behavior | `setup.md` |
| Memory schema and status model | `memory-template.md` |
| Official API request patterns | `api-workflows.md` |
| Search, compare, and shortlist workflow | `search-playbook.md` |
| Review interpretation and signal weighting | `review-analysis.md` |
| Listing QA and owner-side audit workflow | `listing-audit.md` |
| Access limits and safe operating boundaries | `access-boundaries.md` |

## Requirements

- No credentials required for public-page verification and manual comparison.
- `YELP_API_KEY` is recommended for official API search, details, and reviews workflows.
- Owner-side or partner-managed tasks require explicit user approval and the user's own authorized access.
- Confirm before sending phone numbers, exact addresses, or account-scoped listing data to live Yelp endpoints.

## Coverage

This skill is designed for Yelp-specific work that usually breaks when an agent treats it like generic local search:
- restaurant and local-service discovery
- head-to-head business comparison in one market
- review signal analysis and complaint clustering
- delivery or takeout eligibility checks where Yelp exposes those signals
- business listing audits for owners, operators, or agencies

## Core Rules

### 1. Choose the operating mode before querying
- Use page mode for visible public research, API mode for structured fields, and audit mode for listing-quality reviews.
- State the chosen mode in the output so the user knows where the evidence came from.
- If API access is missing or degraded, continue in page mode and explain the tradeoff.

### 2. Resolve the exact business before analysis
- Use location, category, alias, and phone match when possible before comparing or quoting review signals.
- Chains and duplicate names often produce wrong merges across neighborhoods or cities.
- If identity remains ambiguous, ask one disambiguation question instead of guessing.

### 3. Separate consumer research from owner actions
- Default to read-first workflows: search, compare, summarize, and audit.
- Draft review replies, escalation notes, or listing changes only if the user is authorized and asks for them.
- Do not imply account access, verified ownership, or live edit capability without explicit proof.

### 4. Rank with decision signals, not stars alone
- Weight rating, review volume, review recency, complaint themes, price fit, and category match together.
- Recent negative clusters often matter more than a legacy 4.5 average.
- Flag low-sample or stale-review situations clearly.

### 5. Treat Yelp fields as platform-specific, not universal truth
- `price`, `transactions`, `hours`, `attributes`, and delivery or takeout flags are useful but not guaranteed to be current everywhere.
- Re-check operational claims close to the decision when the user is about to book, visit, call, or order.
- Do not convert Yelp metadata into hard promises.

### 6. Keep storage minimal and redacted
- Store reusable filters, accepted or rejected shortlist reasons, and verified aliases in `~/yelp/`.
- Never store secrets, raw API keys, or unredacted signed request URLs.
- In logs, keep only endpoint path, safe params, outcome, and timestamp.

### 7. Return outcome-ready outputs
- For discovery: give a shortlist with why each option is in, what the tradeoffs are, and what should be verified next.
- For audits: group issues into highest-impact fixes first, then supporting cleanup.
- For review analysis: separate evidence, inference, and uncertainty.

## Common Traps

- Comparing businesses from different neighborhoods without distance or market normalization -> the shortlist looks better on paper than in real life.
- Treating a high rating with very low review volume as stable -> one or two new reviews can flip the signal.
- Ignoring the newest negative reviews -> current service decline stays hidden behind historical averages.
- Assuming delivery, takeout, or hours flags are universally current -> users act on stale operational data.
- Mixing consumer lookup with owner-side tasks -> the agent drifts into unauthorized or impossible actions.
- Logging raw API request headers or URLs -> secrets leak into local notes.

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| `https://api.yelp.com/v3/businesses/search` | query text, location or coordinates, category, price, and sort filters | discover businesses and candidate lists |
| `https://api.yelp.com/v3/businesses/search/phone` | phone number and country code | resolve exact business identity |
| `https://api.yelp.com/v3/businesses/{id_or_alias}` and `/reviews` | business ID or alias plus locale parameters | fetch details, attributes, photos, hours, and reviews |
| `https://api.yelp.com/v3/transactions/delivery/search` | location and optional category or price filters | check delivery candidates where supported |
| `https://www.yelp.com/*` | standard browser navigation signals and user search terms | verify visible public-page evidence |

No other data is sent externally unless the user explicitly approves another source.

## Security & Privacy

Data that may leave your machine:
- business names, search terms, location hints, phone numbers, and optional filter parameters sent to Yelp

Data that stays local:
- shortlist decisions, recurring filters, alias cache, and audit notes in `~/yelp/`

This skill does NOT:
- store API keys in markdown files
- claim listing ownership or edit access without proof
- use CAPTCHA bypass, anti-bot evasion, or undeclared scraping flows
- modify its own `SKILL.md`

## Trust

This skill can send business search terms, locations, and optional identifiers to Yelp services.
Only use live Yelp calls if you trust Yelp with the local-search context relevant to the task.

## Scope

This skill ONLY:
- searches and compares Yelp businesses with explicit evidence
- analyzes review signals, listing quality, and operational flags
- prepares drafts or audit recommendations when the user is authorized

This skill NEVER:
- fabricate ratings, reviews, or business availability
- imply owner access or post live changes without explicit instruction
- hide missing data, stale signals, or unsupported market coverage

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `google-reviews` - Compare Yelp signals against Google review patterns and reputation drift.
- `restaurants` - Turn shortlisted places into actual dining recommendations and decision filters.
- `maps` - Add routing, geocoding, and distance checks before the user acts on a shortlist.
- `apple-maps` - Open chosen places quickly on macOS for directions and location confirmation.
- `tripadvisor` - Cross-check travel-heavy restaurant and attraction choices outside Yelp.

## Feedback

- If useful: `clawhub star yelp`
- Stay updated: `clawhub sync`
