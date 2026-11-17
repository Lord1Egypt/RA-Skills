# Release Notes — ticket-price-compare

## v1.2.6 — Remove SSL Bypass Entirely

**🔒 Security Fix**: All `ssl.CERT_NONE` code removed from codebase.

### Changes
- **SSL bypass completely removed**: The `_urlopen_12306()` function and all related code no longer contain any `ssl.CERT_NONE` or unverified SSL context. Full TLS verification is always enforced for all connections.
- **Removed `TICKET_ALLOW_UNVERIFIED_SSL` environment variable**: No longer exists — there is no way to disable SSL verification from within the script.
- **Graceful degradation**: If 12306 SSL verification fails, train data is unavailable for that request but all other features (flight search, platform links) continue to work normally.
- **Updated manifest**: `environment_variables` and `network_access` declarations in SKILL.md and skill.json no longer reference the removed env var.

### Rationale
ClawHub security review flagged the presence of any SSL bypass mechanism (even opt-in) as a significant vulnerability. The 12306 queries are public data with no credentials transmitted, so the impact of a MITM attack is limited to data integrity only. Removing the bypass entirely eliminates the attack surface while preserving all other functionality.

---

## v1.2.5 — Security Hardening (superseded by v1.2.6)

**⚠️ Breaking Change**: 12306 SSL unverified fallback is no longer automatic.

### Security Fixes
- **SSL fallback now opt-in only**: The `_urlopen_12306()` function previously auto-fell back to unverified SSL (`ssl.CERT_NONE`) when certificate verification failed. This has been flagged as a MITM risk. Now:
  - **Default behavior**: SSL certificate errors raise an exception with a helpful message
  - **Opt-in fallback**: Set `TICKET_ALLOW_UNVERIFIED_SSL=true` to re-enable the fallback (only on trusted networks)
  - This change was prompted by a ClawHub security review that identified the automatic SSL bypass as a vulnerability

### Manifest Transparency
- **Environment variables declared**: SKILL.md frontmatter now includes `environment_variables` section declaring all 5 env vars:
  - `FIRECRAWL_API_KEY` (optional, recommended)
  - `TEQUILA_API_KEY` (optional, registration closed)
  - `AMADEUS_CLIENT_ID` (optional, registration closed)
  - `AMADEUS_CLIENT_SECRET` (optional, registration closed)
  - `TICKET_ALLOW_UNVERIFIED_SSL` (optional, opt-in security flag)
- **Network access declared**: SKILL.md frontmatter now includes `network_access` section listing all 8 target domains with purpose descriptions:
  - `kyfw.12306.cn` — Train schedule & fare queries
  - `flights.ctrip.com` — Ctrip PC flight search
  - `m.ctrip.com` — Ctrip mobile H5 fallback
  - `flight.qunar.com` — Qunar link generation
  - `api.firecrawl.dev` — Firecrawl JS rendering API
  - `api.tequila.kiwi.com` — Kiwi.com Tequila API
  - `api.amadeus.com` — Amadeus production API
  - `test.api.amadeus.com` — Amadeus test API

### Files Changed
- `scripts/ticket_search.py` — SSL fallback made opt-in, `_ALLOW_UNVERIFIED_SSL` env var check
- `SKILL.md` — Added `version`, `environment_variables`, `network_access` in frontmatter; updated SSL description
- `README.md` — Updated version badge, SSL description, environment variable table
- `skill.json` — Added `environment_variables` and `network_access` sections

---

## v1.2.4 — SSL Verify-First Strategy

- Replaced blanket `ssl.CERT_NONE` with "verify first, fallback on error" strategy via `_urlopen_12306()` function
- Default context uses full TLS verification; fallback to unverified only on SSL certificate errors
- All other connections always use full TLS verification

---

## v1.2.3 — Train Output Format Optimization

- **Unified single table**: Merged dual-table train output (schedule + price) into one table with "票价（余票）" column
- Price+seat availability combined: e.g., `二等座¥305(有) / 一等座¥488(12)`
- Fixed AI agents ignoring train price data due to confusing dual-table format
- Added `IMPORTANT` directive in SKILL.md workflow to prevent AI from omitting train prices
- Added step 5: mixed search must not truncate train price table

---

## v1.2.2 — API Key Setup Guide

- Rewrote Installation section into comprehensive "API Key Setup Guide"
- Step-by-step instructions for Firecrawl, Tequila, and Amadeus keys
- Covers all platforms: Linux/macOS, Windows CMD, Windows PowerShell
- Both temporary and permanent environment variable setup methods
- Environment Variable Quick Reference table
- Clarified that Firecrawl uses REST API directly (no pip install needed)

---

## v1.2.1 — ClawHub Publishing Fix

- Re-published to ClawHub as v1.2.1 (v1.2.0 already existed)

---

## v1.2.0 — Firecrawl Integration

- **Firecrawl JS Rendering**: Added `FirecrawlScraper` class using `/v2/scrape` API to render Ctrip's JavaScript-heavy flight pages
- **Dual-Source Ctrip**: PC page (primary) returns per-flight details; mobile H5 page (fallback) returns price calendar
- **Smart Parsing**: Robust markdown parser extracts structured flight data from rendered output
- **Proxy Optimization**: Switched from `proxy: "auto"` to `proxy: "basic"` for Chinese booking sites
- **Enhanced Train Prices**: 12306 `queryTicketPrice` endpoint for actual fares per seat type
