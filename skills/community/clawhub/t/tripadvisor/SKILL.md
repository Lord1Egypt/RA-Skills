---
name: Tripadvisor
slug: tripadvisor
version: 1.0.0
homepage: https://clawic.com/skills/tripadvisor
description: Find and compare Tripadvisor hotels, restaurants, and attractions with official API workflows, URL-first navigation, and policy-safe data handling.
changelog: Added official API workflows, UI navigation playbook, and clear compliance guardrails for Tripadvisor interactions.
metadata: {"clawdbot":{"emoji":"🧭","requires":{"bins":["curl","jq","sed"],"env":["TRIPADVISOR_API_KEY"],"config":["~/tripadvisor/"]},"primaryEnv":"TRIPADVISOR_API_KEY","os":["linux","darwin","win32"],"configPaths":["~/tripadvisor/"]}}
---

## Setup

If `~/tripadvisor/` does not exist or is empty, read `setup.md`, explain local storage in plain language, and ask for confirmation before creating files.

## When to Use

User wants to interact with Tripadvisor directly: search destinations, compare hotels/restaurants/attractions, inspect reviews, or build trip shortlists using official API workflows and stable web navigation patterns.

## Architecture

Memory lives in `~/tripadvisor/`. See `memory-template.md` for setup.

```text
~/tripadvisor/
├── memory.md                 # Preferences and recurring constraints
├── sessions/
│   └── YYYY-MM-DD.md         # Search context and selected candidates
├── api/
│   ├── location-cache.md     # query -> location_id mappings
│   └── request-log.md        # redacted endpoint, params, status, timestamp
├── shortlists/
│   └── {city}-{topic}.md     # ranked options with reasons
└── archive/
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup flow | `setup.md` |
| Memory schema | `memory-template.md` |
| Official API workflows | `api-workflows.md` |
| UI navigation playbook | `web-navigation.md` |
| Terms and compliance boundaries | `compliance.md` |

## Core Rules

### 1. Use official Tripadvisor interfaces only
Use official Tripadvisor API endpoints and normal browser navigation. Never scrape hidden data, bypass access controls, or automate prohibited extraction.

### 2. Choose mode explicitly at start
Pick one mode per task:
- API mode: structured lookup and machine-friendly fields
- UI mode: interactive browsing and shortlist guidance
- Hybrid mode: API for discovery, UI for final verification

### 3. Resolve `location_id` before deep queries
For API mode, first map user query to a valid `location_id`, then fetch detail/review/photo endpoints. Cache successful mappings in `~/tripadvisor/api/location-cache.md`.

### 4. Prefer URL-driven navigation over fragile clicks
In UI mode, rely on stable Tripadvisor URLs when possible (city vertical pages and entity detail URLs) before complex click chains.

### 5. Handle consent and anti-bot states safely
If cookie dialogs or anti-bot interstitials appear, ask for user confirmation, document the blocker, and continue with API mode or direct URLs. Do not attempt bypass techniques.

### 6. Produce decision-ready outputs
Always return a ranked shortlist with explicit tradeoffs:
- fit to user goal
- price/quality signal
- uncertainty or missing data

### 7. Keep storage minimal and transparent
Store only reusable trip preferences and selected options under `~/tripadvisor/`. Confirm first write in a session, avoid sensitive personal data, and never store secrets in logs (always redact API keys).

## Common Traps

- Starting with deep detail calls before resolving `location_id` -> API responses become noisy or unusable.
- Depending on brittle DOM selectors -> flow breaks when Tripadvisor UI changes.
- Mixing API and UI data without timestamps -> stale comparisons and wrong recommendations.
- Ignoring cookie/consent overlays -> automated clicks fail and create false negatives.
- Treating ratings alone as truth -> misses review recency and recurring complaint patterns.
- Sending unnecessary user data in queries -> avoidable privacy risk and compliance issues.

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| `https://api.tripadvisor.com/api/partner/2.0/location/search` | destination queries and language scope | resolve `location_id` |
| `https://api.tripadvisor.com/api/partner/2.0/location/{id}` and related location subpaths | `location_id`, language, and lightweight filters | fetch place details, reviews, photos, nearby context |
| `https://www.tripadvisor.com/*` | standard browser navigation signals and user search terms | inspect public pages and verify shortlist candidates |

No other data is sent externally.

## Security & Privacy

**Data that leaves your machine:**
- Destination names, optional date windows, and lightweight filters sent to Tripadvisor API or web pages.

**Data that stays local:**
- Preferences, shortlist decisions, and request logs in `~/tripadvisor/`.

**This skill does NOT:**
- Access files outside `~/tripadvisor/`
- Store payment or passport data by default
- Use scraping bypasses, CAPTCHA evasion, or anti-bot circumvention

## Trust

By using this skill, query data is sent to Tripadvisor services.
Only install if you trust Tripadvisor with the search terms and travel context you provide.

## Scope

This skill ONLY:
- Operates Tripadvisor discovery and comparison workflows
- Uses official API-first calls and policy-safe web navigation
- Produces ranked shortlists with transparent tradeoffs

This skill NEVER:
- Claim guaranteed booking outcomes
- Present uncertain data as verified facts
- Execute purchases or account actions without explicit user instruction

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `booking` — compare accommodation options and total cost breakdowns
- `travel` — manage broader trip planning workflows
- `apple-maps` — validate route friction and area accessibility on macOS
- `search-engine` — improve query iteration and source triangulation
- `expenses` — track trip spending after shortlist decisions

## Feedback

- If useful: `clawhub star tripadvisor`
- Stay updated: `clawhub sync`
