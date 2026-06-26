---
name: semrush-seo
description: Semrush SEO integration with API key authentication. Analyze backlinks, keyword rankings, competitor domains, traffic metrics, and SEO data across organic and paid search channels.
---

# Semrush

![Semrush](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/semrush.svg?v=2)

Access Semrush's SEO and digital marketing analytics platform to analyze backlinks, keyword rankings, competitor domains, traffic metrics, and search performance data across organic and paid search channels.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=semrush-seo) for hosted connection flows and credentials so you do not need to configure Semrush API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Semrush |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Semrush |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│   Semrush API    │
│   (User Chat)   │     │   (Proxy)    │     │  (SEO Analytics) │
│                 │     │              │     │                  │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                    │                      │
         │  1. Install Plugin │                      │
         │  2. Pair Device    │                      │
         │  3. Connect Semrush │                      │
         │                    │  4. API Key Proxy    │
         │                    │  5. Request Forward   │
         │                    │                      │
         ▼                    ▼                      ▼
   ┌──────────┐        ┌──────────┐         ┌──────────┐
   │   SKILL  │        │ Dashboard│         │  Semrush │
   │   File   │        │   Auth   │         │  Cloud   │
   └──────────┘        └──────────┘         └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Semrush again."

## Quick Start

```bash
# Check account API units balance
clawlink_call_tool --tool "semrush_account_units_balance"

# Get keyword overview for a phrase
clawlink_call_tool --tool "semrush_keyword_overview_one_database" --params '{"phrase": "content marketing", "database": "us"}'

# Get backlinks overview for a domain
clawlink_call_tool --tool "semrush_backlinks_overview" --params '{"target": "example.com"}'
```

## Authentication

All Semrush tool calls are authenticated automatically by ClawLink using your Semrush API key stored securely in the dashboard.

**No API key is required in chat.** ClawLink injects your API key into every Semrush API request on your behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=semrush and connect Semrush with your API key.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `semrush` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration semrush
```

**Response:** Returns the live tool catalog for Semrush.

### Reconnect

If Semrush tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=semrush
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration semrush`

## Security & Permissions

- Access is scoped to the Semrush account associated with the connected API key.
- **All operations are read-only** — Semrush tools do not modify any data in your Semrush account.
- API units are consumed per request — monitor `semrush_account_units_balance` before launching large batches.
- Responses are CSV-like strings (not JSON) — parse with delimiter-aware splitting before structured use.

## Tool Reference

### Account & Billing

| Tool | Description | Mode |
|------|-------------|------|
| `semrush_account_units_balance` | Fetch remaining Semrush Standard API units for the authenticated account | Read |

### Keyword Research

| Tool | Description | Mode |
|------|-------------|------|
| `semrush_batch_keyword_overview` | Fetch keyword overview reports for up to 100 keywords (volume, CPC, difficulty) | Read |
| `semrush_broad_match_keyword` | Fetch broad match keywords for a given phrase | Read |
| `semrush_keyword_difficulty` | Determine Keyword Difficulty (KD) score for a phrase (0-100) | Read |
| `semrush_keyword_overview_all_databases` | Fetch keyword overview across all Semrush regional databases | Read |
| `semrush_keyword_overview_one_database` | Fetch keyword summary for a phrase from a specific regional database | Read |
| `semrush_keywords_ads_history` | Fetch 12-month historical ad data for a keyword (domains advertising on it) | Read |
| `semrush_organic_results` | Retrieve domains and URLs from Google's top 100 organic results for a keyword | Read |
| `semrush_paid_results` | Fetch domains ranking in Google's paid search results for a keyword | Read |
| `semrush_phrase_questions` | Fetch question-format keywords semantically related to a query phrase | Read |
| `semrush_related_keywords` | Find related keywords (synonyms, variations) for a target phrase | Read |

### Backlink Analysis

| Tool | Description | Mode |
|------|-------------|------|
| `semrush_anchors` | Get CSV report of anchor texts for backlinks pointing to a target domain/URL | Read |
| `semrush_authority_score_profile` | Get Authority Score (AS) distribution for a target (referring domains per AS 0-100) | Read |
| `semrush_backlinks` | Fetch backlinks for a domain or URL as semicolon-delimited CSV | Read |
| `semrush_backlinks_overview` | Get CSV summary of backlinks including Authority Score and link type breakdowns | Read |
| `semrush_categories` | Retrieve content categories and confidence ratings for a domain | Read |
| `semrush_categories_profile` | Get content categories profile from referring domains (top 10,000) | Read |
| `semrush_historical_data` | Retrieve monthly historical backlink and referring domain time series | Read |
| `semrush_indexed_pages` | Get list of indexed pages for a target from Semrush | Read |
| `semrush_referring_domains` | Get semicolon-delimited report of domains linking to a target | Read |
| `semrush_referring_domains_by_country` | Get geographic distribution of referring domains by country | Read |
| `semrush_referring_i_ps` | Fetch IP addresses that are sources of backlinks for a target | Read |
| `semrush_tld_distribution` | Get Top-Level Domain (TLD) distribution of referring domains | Read |

### Domain & Competitor Analysis

| Tool | Description | Mode |
|------|-------------|------|
| `semrush_ads_copies` | Get unique ad copies observed for a domain in Google's paid search results | Read |
| `semrush_batch_comparison` | Compare backlink profiles across multiple targets | Read |
| `semrush_competitors` | Get CSV report of organic search competitors (shared backlinks or referring domains) | Read |
| `semrush_competitors_in_organic_search` | Get domain's organic search competitors from Semrush | Read |
| `semrush_competitors_in_paid_search` | Get list of a domain's paid search competitors from a regional database | Read |
| `semrush_domain_ad_history` | Retrieve 12-month advertising history for a domain (keywords, ad positions, copies) | Read |
| `semrush_domain_organic_pages` | Get report on domain's unique organic pages ranking in Google's top 100 | Read |
| `semrush_domain_organic_search_keywords` | Get organic search keywords for a domain from a regional database | Read |
| `semrush_domain_organic_subdomains` | Get subdomains of a domain ranking in Google's top 100 organic results | Read |
| `semrush_domain_paid_search_keywords` | Fetch keywords driving paid search traffic to a domain | Read |
| `semrush_domain_pla_search_keywords` | Retrieve Product Listing Ad (PLA) search keywords for a domain | Read |
| `semrush_domain_vs_domain` | Compare up to 5 domains to find common, unique, or gap keywords | Read |
| `semrush_pla_competitors` | Get domains competing in Google's Product Listing Ads for a domain | Read |
| `semrush_pla_copies` | Fetch PLA copies observed for a domain in Google's paid search results | Read |

## Code Examples

### Check API units before a large batch

```bash
clawlink_call_tool --tool "semrush_account_units_balance"
```

### Get keyword difficulty and overview

```bash
clawlink_call_tool --tool "semrush_keyword_difficulty" \
  --params '{"phrase": "digital marketing tools", "database": "us"}'

clawlink_call_tool --tool "semrush_keyword_overview_one_database" \
  --params '{"phrase": "content marketing strategy", "database": "us"}'
```

### Analyze backlinks for a competitor

```bash
clawlink_call_tool --tool "semrush_backlinks_overview" \
  --params '{"target": "competitor.com"}'

clawlink_call_tool --tool "semrush_competitors" \
  --params '{"target": "competitor.com"}'
```

### Get organic keywords for a domain

```bash
clawlink_call_tool --tool "semrush_domain_organic_search_keywords" \
  --params '{"target": "example.com", "database": "us"}'
```

### Compare multiple domains

```bash
clawlink_call_tool --tool "semrush_domain_vs_domain" \
  --params '{"domains": "site1.com,site2.com,site3.com", "database": "us"}'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Semrush is connected.
2. Call `clawlink_list_tools --integration semrush` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `semrush`.
5. If no Semrush tools appear, direct the user to https://claw-link.dev/dashboard?add=semrush.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  SEMRUSH OPERATIONS (All Read-Only)                         │
│  list → get → describe → call                                │
│                                                             │
│  Example: Check units → Get keyword overview → Parse results │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools or ambiguous requests, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. All Semrush tools are read-only — no confirmation is required for data retrieval.
4. Parse CSV-formatted responses before structured use. Use `sep=';'` and cast numeric columns before aggregation.
5. A response of `ERROR 50 :: NOTHING FOUND` is a valid zero-result — not a system error.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- All Semrush tools are **read-only** — no write or destructive operations exist in this skill.
- Responses are CSV-like text strings (not JSON) — parse by splitting on newlines and delimiters before extracting structured rows.
- The literal response `ERROR 50 :: NOTHING FOUND` means zero results for that domain/keyword in the selected database — treat as a valid zero-result, not an error.
- Traffic metrics (e.g., `Tr`) are modeled estimates — incompatible with first-party analytics data.
- API units are consumed per request — preflight with `semrush_account_units_balance` before launching large batches.
- `display_date` for historical data must be in `'YYYYMM15'` format (day must be '15').
- `display_limit` must surpass `display_offset` when pagination is used.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration semrush`. |
| Missing connection | Semrush is not connected. Direct the user to https://claw-link.dev/dashboard?add=semrush. |
| `ERROR 50 :: NOTHING FOUND` | Zero results for the target in the selected database — treat as a valid empty response. |
| `Insufficient units` | API units exhausted — check `semrush_account_units_balance` and wait for replenishment. |
| `Invalid database` | The specified regional database is not supported. Check available databases in the tool schema. |

### Troubleshooting: Tools Not Visible

1. Check that the ClawLink plugin is installed:
   ```bash
   openclaw plugins list
   ```
2. If the plugin is installed but tools are missing, tell the user to send `/new` as a standalone message to reload the catalog.
3. If a fresh chat does not help, run:
   ```bash
   openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
   openclaw gateway restart
   ```
4. After restart, tell the user to send `/new` again and retry.

### Troubleshooting: Parsing CSV Responses

1. All Semrush responses are CSV-like strings — use delimiter splitting (semicolon `;` for most tools) to parse rows.
2. Cast numeric columns (backlinks_num, domain_ascore, etc.) before aggregation.
3. Headers match `export_columns` codes (e.g., 'Ph', 'Nq', 'Kd') — parse headers into a structured table first.
4. Use `sep=';'` when calling tools that support the `display_separate` parameter.

## Resources

- [Semrush API Documentation](https://developers.semrush.com/api/)
- [Semrush Domain Analytics](https://www.semrush.com/domain-analytics/)
- [Semrush Keyword Research](https://www.semrush.com/keyword-research/)
- [Semrush Backlink Analytics](https://www.semrush.com/backlinks/)
- [Semrush Projects](https://www.semrush.com/projects/)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=semrush-seo
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [Google Search Console](https://clawhub.ai/hith3sh/google-search-console) — For search performance data from Google
- [Ahrefs SEO](https://clawhub.ai/hith3sh/ahrefs-seo) — For alternative backlink and keyword analysis

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=semrush-seo)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)