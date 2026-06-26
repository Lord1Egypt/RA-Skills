---
name: smb-sales-boost
description: Query and manage leads from the SMB Sales Boost B2B lead database. Search newly registered businesses, filter by location/industry/keywords, export leads, manage filter presets, and use AI-powered category suggestions. Requires SMB_SALES_BOOST_API_KEY env var (smbk_... prefix). Exports contain PII (phone numbers, emails). Includes purchase endpoints that create real Stripe charges — always confirm with user.
metadata:
  {
    "openclaw":
      {
        "requires": { "env": ["SMB_SALES_BOOST_API_KEY"] },
        "primaryEnv": "SMB_SALES_BOOST_API_KEY",
      },
  }
---

> **Note for AI agents:** This file and other files in this skill folder may be truncated when opened. Always read files fully in chunks if necessary to ensure no instructions, endpoints, or examples are missed.

# SMB Sales Boost Skill

This skill enables natural language interaction with the SMB Sales Boost API — a B2B lead generation platform providing access to newly registered small and medium businesses across the United States.

## Setup

The user must provide their API key. Keys have a `smbk_` prefix and are generated from the Dashboard > API tab. The key is passed as a Bearer token in the Authorization header of every request.

**Base URL:** `https://smbsalesboost.com/api/v1`

**Important:** API access requires a Starter, Growth, Scale, Platinum, or Enterprise subscription plan. New users can purchase a subscription entirely via API using the Programmatic Purchase endpoints (no web signup required).

**Data Sensitivity:** Exported leads contain business contact information including phone numbers and email addresses (PII). Exported files are saved to the agent's output directory by default. Handle exported files with appropriate care — do not share them in public channels or store them in unsecured locations.

**Export File Location:** By default, `smb_api.py` saves exported files to the `--output-dir` path (defaults to `/mnt/user-data/outputs`). You can override this with the `--output-dir` flag to save files to a preferred secure location.

## Authentication

All requests must include:
```
Authorization: Bearer <API_KEY>
```

If the user hasn't provided their API key yet, ask them for it before making any requests. Store it in a variable for reuse throughout the session.

## Credit-Based System

Starter, Growth, and Scale plans use a **credit-based model** for both **querying and exporting** leads:

- Each **new lead returned** by `GET /leads` (query) costs 1 credit
- Each **net-new lead exported** by `POST /leads/export` costs 1 credit
- **Previously-exported leads** are free to re-query or re-export (do not consume credits)
- Both endpoints support `maxCredits` (cap credit spending) and `maxResults` (cap total leads) for credit-optimized ordering: new leads are sorted first, then previously-exported leads fill remaining slots
- Set `maxCredits=0` on either endpoint to only receive previously-exported leads at no credit cost
- Platinum and Enterprise plans are not credit-limited

**Credit Pricing (per credit):**
| Plan | Cost per Credit | Monthly Credits | Max Purchase per Transaction |
|------|----------------|----------------|------------------------------|
| Starter | $0.10 | 500 | 2,500 |
| Growth | $0.075 | 2,000 | 10,000 |
| Scale | $0.05 | 10,000 | 50,000 |
| Platinum | $0.03 | 100,000 | 500,000 |
| Enterprise | $0.02 | 250,000 | 1,250,000 |

**Credit balance fields** (from `GET /me`): `monthlyCredits`, `monthlyCreditsUsed`, `monthlyCreditsRemaining`, `permanentCredits`, `totalCreditsRemaining`, `creditOverageRate`

**Additional profile fields** (from `GET /me`): `totalLeadsExported` (all-time count), `monthlyLeadsExported` (current billing cycle), `autoTopUp` (nested object with `enabled`, `triggerType`, `triggerAmount`, `purchaseType`, `purchaseAmount`, `capType`, `capAmount`)

Users can purchase additional permanent credits via `POST /purchase-credits` or configure automatic top-ups via `GET/PATCH /auto-top-up`.

## Rate Limits

- General endpoints: 60 requests per minute
- Export endpoints: 1 per 5 minutes
- AI endpoints: 5 per minute
- Programmatic purchase: 5 per hour per IP
- Claim key: 30 per hour per IP

Rate limit headers are returned on every response: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`. If rate limited, check the `Retry-After` header for seconds to wait.

## Two Database Types

SMB Sales Boost has two separate databases with different contact information available:

1. **`home_improvement`** — Home improvement/contractor businesses with **phone numbers**, star ratings, review counts, review snippets, profile URLs, and categories
2. **`other`** — General newly registered businesses with **phone numbers and email addresses**, registered URLs, crawled URLs, short/long descriptions, redirect status, and AI-enriched category estimations

The Home Improvement database provides phone numbers as the primary contact method. The Other database provides both phone numbers and email addresses, making it ideal for cold email and multi-channel outreach campaigns.

Some filter parameters only work with one database type. The user's account has a default database setting. Always check which database the user wants to query.

---

## Core Endpoints

### 1. Search Leads — `GET /leads`

The primary endpoint. Translates natural language queries into filtered lead searches. **Each new lead returned costs 1 credit** (previously-exported leads are free to re-query). Supports `maxCredits` and `maxResults` parameters for credit-optimized ordering.

**Key Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `page` | integer | Page number (default: 1) |
| `limit` | integer | Results per page (max 1000, default 100) |
| `database` | string | `home_improvement` or `other` |
| `positiveKeywords` | JSON array string | Keywords to include (OR logic). Supports `*` wildcard for pattern matching (e.g., `["*dental*", "*ortho*"]`). Without wildcards, performs substring matching by default. |
| `negativeKeywords` | JSON array string | Keywords to exclude (AND logic). Also supports `*` wildcard (e.g., `["*franchise*"]`). |
| `orColumns` | JSON array string | Column names to search keywords against |
| `search` | string | Full-text search across all fields |
| `stateInclude` | string | Comma-separated state codes: `CA,NY,TX` |
| `stateExclude` | string | Comma-separated state codes to exclude |
| `cityInclude` | JSON array string | Cities to include |
| `cityExclude` | JSON array string | Cities to exclude |
| `zipInclude` | JSON array string | ZIP codes to include |
| `zipExclude` | JSON array string | ZIP codes to exclude |
| `nameIncludeTerms` | JSON array string | Business name include terms |
| `nameExcludeTerms` | JSON array string | Business name exclude terms |
| `lastUpdatedFrom` | date string | Filter by Last Updated date (after this date). Supports ISO 8601 or relative format (e.g., `rel:7d`, `rel:6m`). |
| `lastUpdatedTo` | date string | Filter by Last Updated date (before this date) |
| `updateReasonFilter` | string | Comma-separated update reasons to filter by (e.g., "Newly Added", "Phone Primary") |

**Understanding "Last Updated" — this is critical for finding the freshest leads:**
- **Home Improvement leads:** Last Updated means a new phone number was detected
- **Other leads:** Last Updated means any of the 5 contact/address fields changed: primary phone, secondary phone, primary email, secondary email, or full address
- Both databases also include newly added records in this date
- Many businesses launch a website before adding contact info, so the Last Updated date captures when that information first becomes available — making it the primary way to identify the most actionable leads

| Parameter | Type | Description |
|-----------|------|-------------|
| `countryInclude` | JSON array string | Countries to include |
| `countryExclude` | JSON array string | Countries to exclude |
| `sortBy` | string | Field to sort by |
| `sortOrder` | string | `asc` or `desc` (default: `desc`) |

**Wildcard Keyword Tips:**
- Use `*` to match any characters: `"*dental*"` matches "dental clinic", "pediatric dentistry", etc.
- Combine wildcards for compound terms: `"*auto*repair*"` matches "auto body repair", "automotive repair shop", etc.
- Use multiple keyword variations for broader coverage: `["*dental*", "*dentist*", "*orthodont*"]`
- Keywords without wildcards still perform substring matching by default
- **URL Space-to-Wildcard:** For URL columns (registered URL, crawled URL, profile URL), spaces in search terms are automatically replaced with `%` wildcards. For example, "dental clinic" becomes `%dental%clinic%` to match URLs like `example.com/dental-clinic`

**Home Improvement Only:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `minStars` / `maxStars` | number | Star rating range |
| `minReviewCount` / `maxReviewCount` | integer | Review count range |
| `categoriesIncludeTerms` / `categoriesExcludeTerms` | JSON array string | Category filters |
| `reviewSnippetIncludeTerms` / `reviewSnippetExcludeTerms` | JSON array string | Review text filters |
| `profileUrlIncludeTerms` / `profileUrlExcludeTerms` | JSON array string | Profile URL filters |

**Other Database Only:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `urlIncludeTerms` / `urlExcludeTerms` | JSON array string | Registered URL filters |
| `crawledUrlIncludeTerms` / `crawledUrlExcludeTerms` | JSON array string | Crawled URL filters |
| `descriptionIncludeTerms` / `descriptionExcludeTerms` | JSON array string | Short description filters |
| `descriptionLongIncludeTerms` / `descriptionLongExcludeTerms` | JSON array string | Long description filters |
| `emailPrimaryInclude` / `emailPrimaryExclude` | JSON array string | Primary email filters |
| `emailSecondaryInclude` / `emailSecondaryExclude` | JSON array string | Secondary email filters |
| `phonePrimaryInclude` / `phonePrimaryExclude` | JSON array string | Primary phone filters |
| `phoneSecondaryInclude` / `phoneSecondaryExclude` | JSON array string | Secondary phone filters |
| `redirectFilter` | string | `yes` or `no` — filter by redirect status |
| `registrationDateFrom` / `registrationDateTo` | date string | Filter by domain registration date (ISO 8601 or relative format e.g., `rel:6m`) |
| `timeScrapedFrom` / `timeScrapedTo` | date string | Filter by when leads were scraped (ISO 8601 or relative format e.g., `rel:30d`) |
| `websiteSchemaFilter` | string | Comma-separated website schema types (e.g., `LocalBusiness,Organization`). Use `GET /leads/other/schema-types` for available values. |

**Credit Control Parameters (also available on export):**

| Parameter | Type | Description |
|-----------|------|-------------|
| `maxResults` | integer | Cap total leads returned (new + previously-exported). New leads prioritized first, then previously-exported fill remaining slots. |
| `maxCredits` | integer | Cap credits spent on this query. Set to `0` to only receive previously-exported leads at no cost. |

When `maxCredits` or `maxResults` is specified, credit-optimized ordering is applied: new (credit-consuming) leads sorted first, then previously-exported leads, each group sorted by lastUpdated descending (or your custom sort).

**Important:** At least one positive filter is required (positiveKeywords or any column-specific include terms).

**Response includes:** `leads` array, `totalCount`, `page`, `limit`, `databaseType`, `creditsUsed`, `creditsRemaining` (credit-plan users only), `maxResults`, `maxCredits` (echoed when specified)

**Error 402 Payment Required:** Returned when credit-plan users have insufficient credits. Use `maxCredits` or `maxResults` to limit credit usage, or purchase more credits.

**Lead fields use display-name keys (with spaces).** The two databases return different schemas:

- **HomeImprovementLead:** `id`, `Company Name`, `Phone`, `Stars`, `Review Count`, `Categories`, `Profile URL`, `Review Snippet`, `Address Full`, `Street`, `Address City`, `Address State`, `Address Zip`, `Address Country`, `Last Updated`, `Time Scraped`
- **OtherLead:** `id`, `Company Name`, `Phone Primary`, `Phone Secondary`, `Email Primary`, `Email Secondary`, `Registered URL`, `Registration Date`, `Redirect`, `Crawled URL`, `AI Categories`, `Website Schema`, `Description Short`, `Description Long`, `Address Full`, `Street`, `City`, `State`, `Zip`, `Country`, `Last Updated`, `Time Scraped`

Contact fields (phone/email) are masked for free users. The `Last Updated` field indicates when contact information was last detected or updated — the best indicator of lead freshness and actionability.

**AI Categories (Other Database):** Leads in the Other database may include an `AI Categories` field containing an array of 1-3 AI-estimated category names, or null if not yet classified. This progressive enrichment classifies businesses into 957+ categories.

### 2. Preview Leads — `GET /leads/preview`

Preview leads matching your filters with **masked contact information** — does **NOT** consume any credits. Use this to test filters and evaluate result quality before committing credits on the full `GET /leads` endpoint.

**How it differs from `GET /leads`:**
- Contact fields are returned in masked format (e.g., `(5**) ***-**89`, `j***@***.com`)
- No credits are consumed regardless of plan
- No `maxCredits` or `maxResults` parameters (not needed since preview is free)
- Contact-field filters are not available: `emailPrimaryInclude`, `emailPrimaryExclude`, `emailSecondaryInclude`, `emailSecondaryExclude`, `phonePrimaryInclude`, `phonePrimaryExclude`, `phoneSecondaryInclude`, `phoneSecondaryExclude`
- All other filters are identical to `GET /leads` (keywords, location, company name, URLs, descriptions, ratings, dates, etc.)

**Response includes:** `leads` array (with masked contacts), `pagination` (page, limit, total, pages), `databaseType`, `preview: true` flag

**When to use preview:**
- User wants to check how many results match before spending credits
- User wants to evaluate filter quality
- User says "preview", "test my filters", "how many leads match", or similar

### 3. Website Schema Types — `GET /leads/other/schema-types`

Returns a sorted list of all distinct website schema types found in the Other leads database. Use these values with the `websiteSchemaFilter` parameter on `GET /leads`.

### 4. Export Leads — `POST /leads/export`

Export filtered leads as CSV, JSON, or XLSX files.

**Request body:**
```json
{
  "database": "home_improvement" | "other",
  "filters": { /* same filter params as GET /leads */ },
  "selectedIds": [1, 2, 3],  // alternative to filters
  "formatId": 123,  // optional export format template ID
  "maxLeads": 500,  // optional: cap leads per export, overflow stored in reservoir
  "maxResults": 1000,  // optional: total leads (new + previously-exported)
  "maxCredits": 100  // optional: credit spending cap (0 = only previously-exported leads)
}
```

**Credit system (Starter/Growth/Scale plans):**
- Each net-new lead exported deducts 1 credit
- Previously-exported leads are included for free
- Use `maxCredits` to control spending, `maxLeads` to limit volume
- Set `maxCredits: 0` to only receive previously-exported leads at no cost

**Response:** `files` array (with base64-encoded data), `leadCount`, `exportId`, `databaseType`, `creditsUsed`, `creditsRemaining`, `overflowCount`

**Error 402 Payment Required:** Returned when credit-plan users have insufficient credits.

Rate limited: 1 export per 5 minutes, max 10,000 leads per export.

### 5. Filter Presets — `/filter-presets`

- `GET /filter-presets` — List all saved presets
- `POST /filter-presets` — Create a preset (requires `name` and `filters` object)
- `DELETE /filter-presets/{id}` — Delete a preset

### 6. Keyword Lists — `/keyword-lists`

Keyword lists now support typed lists (positive or negative) with paired list management and source categories.

- `GET /keyword-lists` — List all keyword lists
- `POST /keyword-lists` — Create (requires `name`, optional `keywords` array, `sourceCategories` array max 3)
- `PUT /keyword-lists/{id}` — Update
- `DELETE /keyword-lists/{id}` — Delete

**Keyword list properties:** `name`, `keywords` (wildcard patterns e.g., `*dentist*`), `type` (positive/negative), `pairedListId` (linked positive/negative pair), `sourceCategories` (max 3), `autoRefineEnabled`, `refinementStatus` (running/completed/paused)

### 7. Email Schedules — `/email-schedules`

Email schedules now support distribution modes and lead reservoirs.

- `GET /email-schedules` — List schedules
- `POST /email-schedules` — Create (requires `name`, `filterPresetId`, `intervalValue`, `intervalUnit`, `recipients` min 1)
- `PATCH /email-schedules/{id}` — Update (supports `isActive` toggle)
- `DELETE /email-schedules/{id}` — Delete
- `POST /email-schedules/{id}/trigger` — Manually trigger an active schedule to send immediately (rate limited: 1 per 5 minutes)

**Distribution modes:**
- `full_copy` (default): All leads sent to every recipient
- `split_evenly`: Leads divided evenly among recipients. Optional `fullCopyRecipients` array for people who should receive the full list (e.g., managers)

**Lead reservoir:** Set `maxLeadsPerEmail` to cap leads per delivery. Overflow is stored and included in the next scheduled email.

**Schedule pause reasons:** The `pauseReason` field indicates why a schedule is paused: `null` (not paused), `"user"` (manually paused), or `"insufficient_credits"` (auto-paused due to low credits).

**Combined File Feature:** When file splitting is enabled, you can configure a combined file that includes an assignee column and file name column, sent to dedicated combined recipients. Use `combinedAssigneeColumnName` and `combinedFileNameColumnName` on export formats.

### 8. Export Formats — `/export-formats`

- `GET /export-formats` — List custom export formats
- `POST /export-formats` — Create (requires `name`, supports `fileType`, `fieldMappings`, split settings, `databaseType`, `combinedAssigneeColumnName`, `combinedFileNameColumnName`)
- `GET /export-formats/{id}` — Get specific format
- `PATCH /export-formats/{id}` — Update
- `DELETE /export-formats/{id}` — Delete
- `POST /export-formats/{id}/set-default` — Set as default

### 9. Export History — `/export-history`

- `GET /export-history` — List past exports (optional `limit` param, default 50)
- `GET /export-history/{id}/download` — Re-download (expires after 7 days)

### 10. AI Features

**`POST /ai/suggest-categories`** — Get AI category suggestions based on company profile.

Required: `companyName`, `companyDescription`, `productService`
Optional: `companyWebsite`, `smbType`, `excludeCategories`

**`POST /ai/generate-keywords`** — Trigger async keyword generation based on your company profile and target categories (up to 3 per list). Keywords are generated as wildcard patterns and saved to keyword lists with auto-refine enabled by default. Use `/ai/keyword-status` to check progress.

**`GET /ai/keyword-status`** — Check the status of keyword generation jobs. Use this to poll for completion after triggering keyword generation.

**AI Auto-Refine** — Single-pass 4-phase optimization that automatically refines keyword lists using AI:

- Phase 1: Validates positive keywords (50% threshold, up to 2 variation attempts)
- Phase 1B: Discovers up to 15 new positive keywords in a single AI call
- Phase 2: Validates negative keywords (40% threshold)
- Phase 2B: Discovers up to 5 new negative keywords from ~80 sample leads
- Final quality score (1-10, median of 3) determines if a retry pass is needed
- Auto-refine turns off when complete
- Uses `sourceCategories` (max 3 per list) for accurate AI scoring

Endpoints:

- `POST /ai/auto-refine/enable` — Enable auto-refine for a keyword list (requires `listId`)
- `POST /ai/auto-refine/disable` — Disable auto-refine for a keyword list (requires `listId`)
- `GET /ai/auto-refine/status` — Check auto-refine status (optional `listId` query param to filter by specific list)

### 11. Export Blacklist — `/export-blacklist`

- `GET /export-blacklist` — List blacklisted entries
- `POST /export-blacklist` — Add entry (single or batch via `entries` array)
- `DELETE /export-blacklist/{id}` — Remove entry

### 12. Account

- `GET /me` — Get user profile (subscription plan, settings, onboarding status, credit balance)
- `PATCH /me` — Update profile (firstName, lastName, companyName, companyWebsite)
- `GET /settings/database` — Check current database type and switch availability. Returns: `currentDatabase`, `canSwitch` (boolean), `daysRemaining` (days until switch allowed), `lastSwitchedAt` (ISO timestamp or null)
- `POST /settings/switch-database` — Switch between databases (has cooldown). Requires `smbType` field with value `home_improvement` or `other`. Incompatible email schedules are auto-paused; the response includes a `pausedSchedules` count.

### 13. Programmatic Purchase — Buy a subscription via API

**⚠ Purchase Confirmation Required:** Always confirm with the user before calling `POST /purchase`, `POST /purchase-credits`, or `POST /subscription/change-plan`. These endpoints create real Stripe charges. Never execute a purchase action without explicit user confirmation.

**⚠ Unauthenticated Endpoints:** `POST /purchase` and `POST /claim-key` do **not** require an API key. This means they can be called without any credentials. Because they initiate real Stripe checkout sessions and retrieve API keys, **never call these endpoints autonomously** — always present the action to the user and wait for explicit approval before executing.

No web signup required. New users can purchase and get an API key entirely via API:

1. `POST /purchase` **(unauthenticated)** — Create a Stripe Checkout session. Provide `email` and `plan` (starter, growth, scale, platinum, or enterprise). Returns a `checkoutUrl` and `claimToken`.
2. Direct the user to complete payment at the checkout URL.
3. `POST /claim-key` **(unauthenticated)** — After payment, provide `email` and `claimToken` to retrieve the API key. If payment is still pending, returns status `pending` — poll every 5-10 seconds.

### 14. Credits & Subscription Management

**⚠ All purchase/plan-change endpoints create real charges — always confirm with the user first.**

- `POST /purchase-credits` — Purchase additional permanent credits. Provide either `creditCount` (min 100, max 5x your plan's monthly credits) or `dollarAmount` (min $1). Max per purchase: Starter 2,500, Growth 10,000, Scale 50,000, Platinum 500,000, Enterprise 1,250,000. Uses saved payment method (Stripe off-session charge). Pricing: Starter 10¢, Growth 7.5¢, Scale 5¢, Platinum 3¢, Enterprise 2¢ per credit.
- `GET /auto-top-up` — Get auto top-up configuration (trigger threshold, purchase amount, monthly cap, current usage).
- `PATCH /auto-top-up` — Configure automatic credit purchases. When enabled, credits are purchased automatically when permanent credit balance falls below the trigger threshold. Parameters: `enabled` (required, boolean), `triggerType` ("credits" or "dollars"), `triggerAmount`, `purchaseType` ("credits" or "dollars"), `purchaseAmount`, `capType` ("credits", "dollars", or null), `capAmount` (nullable).
- `POST /subscription/change-plan` — Upgrade or downgrade between starter, growth, and scale. On upgrade, unused monthly credits convert to permanent credits (capped at current plan's standard allocation). Downgrades take effect at renewal.
- `POST /subscription/cancel` — Cancel subscription at end of current billing period. Access continues until period ends.

---

## Natural Language Translation Guide

When users make natural language requests, translate them into API calls. Use multiple wildcard keyword variations to cast a wider net — keywords are matched via OR logic so more variations means better coverage:

| User Says | API Call |
|-----------|---------|
| "Find new dental practices in Texas" | `GET /leads?positiveKeywords=["*dental*","*dentist*","*orthodont*"]&stateInclude=TX` |
| "Search for med spas and aesthetics businesses in Florida" | `GET /leads?positiveKeywords=["*med*spa*","*medical*spa*","*aesthet*","*botox*","*medspa*"]&stateInclude=FL` |
| "Show me auto repair shops in Chicago updated this week" | `GET /leads?positiveKeywords=["*auto*repair*","*body*shop*","*mechanic*","*oil*change*","*brake*"]&cityInclude=["Chicago"]&lastUpdatedFrom=rel:7d` |
| "Find pet grooming businesses in California, exclude boarding" | `GET /leads?positiveKeywords=["*pet*groom*","*dog*groom*","*pet*salon*"]&negativeKeywords=["*boarding*","*kennel*"]&stateInclude=CA` |
| "Get bakeries and catering companies in New York" | `GET /leads?positiveKeywords=["*bakery*","*bake*shop*","*cater*","*pastry*","*cake*"]&stateInclude=NY` |
| "Find fitness studios in Georgia and North Carolina" | `GET /leads?positiveKeywords=["*fitness*","*gym*","*yoga*","*pilates*","*crossfit*"]&stateInclude=GA,NC` |
| "Get 50 leads with high ratings" | `GET /leads?limit=50&minStars=4` (home_improvement only) |
| "Find businesses with LocalBusiness schema type" | `GET /leads?websiteSchemaFilter=LocalBusiness` (other only) |
| "Show leads registered in the last 6 months" | `GET /leads?registrationDateFrom=rel:6m` (other only) |
| "Preview leads before spending credits" | `GET /leads/preview` with same filters |
| "How many dental leads are in Texas?" | `GET /leads/preview` with dental keywords + stateInclude=TX (check totalCount) |
| "Test my filters without using credits" | `GET /leads/preview` with current filters |
| "Export all my filtered results" | `POST /leads/export` with current filters |
| "Export but only spend 50 credits max" | `POST /leads/export` with `maxCredits: 50` |
| "Export only previously-exported leads (free)" | `POST /leads/export` with `maxCredits: 0` |
| "What categories should I target?" | `POST /ai/suggest-categories` |
| "Save this search as 'FL Med Spas'" | `POST /filter-presets` |
| "Show my recent exports" | `GET /export-history` |
| "What plan am I on?" | `GET /me` |
| "How many credits do I have left?" | `GET /me` |
| "Buy 500 more credits" | `POST /purchase-credits` with `creditCount: 500` |
| "Upgrade to the Growth plan" | `POST /subscription/change-plan` with `targetPlan: "growth"` |
| "Cancel my subscription" | `POST /subscription/cancel` |
| "Exclude these domains from exports" | `POST /export-blacklist` |
| "Enable auto-refine on my keyword list" | `POST /ai/auto-refine/enable` with `listId` |
| "Check on my keyword generation" | `GET /ai/keyword-status` |
| "Send my scheduled email now" | `POST /email-schedules/{id}/trigger` |
| "Split leads evenly among my sales team" | `POST /email-schedules` with `distributionMode: "split_evenly"` |
| "Search but only spend 10 credits" | `GET /leads` with `maxCredits=10` |
| "Show me only leads I've already exported" | `GET /leads` with `maxCredits=0` |
| "Set up auto top-up for credits" | `PATCH /auto-top-up` with `enabled: true` and thresholds |
| "Check my auto top-up settings" | `GET /auto-top-up` |
| "I want to sign up for a Starter plan" | `POST /purchase` with `plan: "starter"` |

## Building API Requests

Use the included `smb_api.py` script for all API calls. It handles authentication, URL encoding, response parsing, and safe file export in a single reusable file. **Do not use shell commands like `curl`** — constructing shell commands from user-provided input risks shell injection vulnerabilities.

### Usage

```bash
python smb_api.py <API_KEY> <METHOD> <ENDPOINT> [--params '{"key":"value"}'] [--body '{"key":"value"}'] [--output-dir /path/to/dir]
```

### Examples

```bash
# Search for med spas in Florida using wildcard keywords (OR logic)
python smb_api.py smbk_xxx GET /leads --params '{"positiveKeywords":"[\"*med*spa*\",\"*medical*spa*\",\"*aesthet*\",\"*botox*\",\"*medspa*\"]","stateInclude":"FL","limit":"25"}'

# Find auto shops in multiple states, exclude franchises
python smb_api.py smbk_xxx GET /leads --params '{"positiveKeywords":"[\"*auto*repair*\",\"*body*shop*\",\"*mechanic*\",\"*tire*\",\"*oil*change*\"]","negativeKeywords":"[\"*franchise*\",\"*jiffy*\"]","stateInclude":"GA,FL,NC,SC,TN","limit":"50"}'

# Search for recently updated dental leads in Texas
python smb_api.py smbk_xxx GET /leads --params '{"positiveKeywords":"[\"*dental*\",\"*dentist*\",\"*orthodont*\",\"*oral*surg*\"]","stateInclude":"TX","lastUpdatedFrom":"rel:7d"}'

# Full-text search across all fields
python smb_api.py smbk_xxx GET /leads --params '{"search":"organic coffee","limit":"25"}'

# Filter by website schema type (other database only)
python smb_api.py smbk_xxx GET /leads --params '{"websiteSchemaFilter":"LocalBusiness","stateInclude":"CA","limit":"25"}'

# Preview leads with masked contacts (no credits consumed)
python smb_api.py smbk_xxx GET /leads/preview --params '{"positiveKeywords":"[\"*dental*\",\"*dentist*\"]","stateInclude":"TX","limit":"25"}'

# Preview to check result count before committing credits
python smb_api.py smbk_xxx GET /leads/preview --params '{"positiveKeywords":"[\"*med*spa*\",\"*aesthet*\"]","stateInclude":"FL"}'

# Get available website schema types
python smb_api.py smbk_xxx GET /leads/other/schema-types

# Get account info (includes credit balance)
python smb_api.py smbk_xxx GET /me

# Export with credit controls
python smb_api.py smbk_xxx POST /leads/export --body '{"database":"other","filters":{"positiveKeywords":["*pet*groom*","*veterinar*","*dog*train*"],"stateInclude":"CA,OR,WA"},"maxCredits":100}'

# Export only previously-exported leads (free, no credits used)
python smb_api.py smbk_xxx POST /leads/export --body '{"database":"other","filters":{"positiveKeywords":["*dental*"],"stateInclude":"TX"},"maxCredits":0}'

# Purchase additional credits
python smb_api.py smbk_xxx POST /purchase-credits --body '{"creditCount":500}'

# Purchase credits by dollar amount
python smb_api.py smbk_xxx POST /purchase-credits --body '{"dollarAmount":50}'

# Change subscription plan
python smb_api.py smbk_xxx POST /subscription/change-plan --body '{"targetPlan":"growth"}'

# Cancel subscription
python smb_api.py smbk_xxx POST /subscription/cancel

# Search leads with credit controls (cap at 10 credits)
python smb_api.py smbk_xxx GET /leads --params '{"positiveKeywords":"[\"*dental*\"]","stateInclude":"TX","maxCredits":"10","maxResults":"50"}'

# Search only previously-exported leads (free, no credits used)
python smb_api.py smbk_xxx GET /leads --params '{"positiveKeywords":"[\"*dental*\"]","stateInclude":"TX","maxCredits":"0"}'

# Get auto top-up configuration
python smb_api.py smbk_xxx GET /auto-top-up

# Configure auto top-up (buy 500 credits when balance drops below 100)
python smb_api.py smbk_xxx PATCH /auto-top-up --body '{"enabled":true,"triggerType":"credits","triggerAmount":100,"purchaseType":"credits","purchaseAmount":500}'

# Disable auto top-up
python smb_api.py smbk_xxx PATCH /auto-top-up --body '{"enabled":false}'

# Start a programmatic purchase (no auth needed, but script still requires a placeholder key)
python smb_api.py none POST /purchase --body '{"email":"user@example.com","plan":"starter"}'

# Claim API key after payment
python smb_api.py none POST /claim-key --body '{"email":"user@example.com","claimToken":"tok_abc123"}'

# AI category suggestions
python smb_api.py smbk_xxx POST /ai/suggest-categories --body '{"companyName":"FitPro Supply","companyDescription":"Commercial fitness equipment distributor","productService":"Gym equipment, treadmills, weight systems"}'

# Create a filter preset
python smb_api.py smbk_xxx POST /filter-presets --body '{"name":"NY Bakeries","filters":{"positiveKeywords":["*bakery*","*bake*shop*","*cater*","*pastry*"],"stateInclude":"NY"}}'

# Create email schedule with split distribution
python smb_api.py smbk_xxx POST /email-schedules --body '{"name":"Daily TX Leads","filterPresetId":5,"intervalValue":1,"intervalUnit":"days","recipients":[{"email":"rep1@co.com"},{"email":"rep2@co.com"}],"distributionMode":"split_evenly","fullCopyRecipients":["manager@co.com"],"maxLeadsPerEmail":50}'

# Enable AI auto-refine on a keyword list
python smb_api.py smbk_xxx POST /ai/auto-refine/enable --body '{"listId":42}'

# Check auto-refine status for a specific list
python smb_api.py smbk_xxx GET /ai/auto-refine/status --params '{"listId":"42"}'

# Check keyword generation job status
python smb_api.py smbk_xxx GET /ai/keyword-status

# Manually trigger an email schedule
python smb_api.py smbk_xxx POST /email-schedules/15/trigger

# Delete a filter preset
python smb_api.py smbk_xxx DELETE /filter-presets/42
```

The script outputs JSON to stdout and rate limit headers to stderr. For export requests, files are automatically saved with sanitized filenames.

**Remember:**
- Use multiple wildcard keyword variations to cast a wider net (e.g., `["*dental*", "*dentist*", "*orthodont*"]` not just `["dental"]`) — keywords are matched via OR logic
- Use `*` for flexible pattern matching: `"*auto*repair*"` matches "auto body repair", "automotive repair shop", etc.
- JSON array parameters should be serialized as strings inside the `--params` JSON
- At least one positive filter is required for lead searches
- Use `GET /leads/preview` when the user wants to test filters or check counts without spending credits — contacts are returned masked and no credits are consumed
- Check which database the user needs before applying database-specific filters
- Home Improvement database provides phone numbers; Other database provides phone numbers and email addresses
- Lead field keys use display names with spaces (e.g., `Company Name`, `Phone Primary`, `AI Categories`)
- Phone and email are masked for free-tier users and always masked in preview responses
- Present results in a clean, readable table format
- For credit-plan users, mention credits used/remaining after both queries and exports (both consume credits for new leads)
- The `POST /purchase` and `POST /claim-key` endpoints do not require authentication (no API key needed)

## Security

This skill addresses two specific agent execution risks: **shell injection** from constructing CLI commands with user input, and **arbitrary file writes** from unsanitized API-provided filenames.

**Shell injection prevention:** The `smb_api.py` script uses Python's `requests` library for all HTTP calls. User-provided search terms, locations, and other inputs are passed as structured function arguments — never interpolated into shell command strings. This eliminates the shell injection vector that exists when agents construct `curl` commands from user input.

**Path traversal prevention in exports:** The `/leads/export` endpoint returns base64-encoded files with an API-provided `fileName` field. A malicious or corrupted filename (e.g., `../../etc/passwd`) could write files to arbitrary locations. The script enforces three safeguards:
1. **Basename extraction:** `os.path.basename()` strips all directory components — `../../etc/passwd` becomes `passwd`
2. **Extension validation:** Only `.csv`, `.json`, and `.xlsx` extensions are allowed; anything else defaults to `.csv`
3. **Scoped output directory:** Files are written only to the designated output directory (`/mnt/user-data/outputs/` by default), never to user-specified or API-specified paths

**API key handling:** The key is passed as a CLI argument and sent only in the Authorization header. It is never logged, written to files, or included in error output.

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Bad request — check parameters |
| 401 | Invalid or missing API key |
| 402 | Insufficient credits (credit-plan users) — check credit balance with `GET /me` |
| 403 | Active subscription required |
| 404 | Resource not found |
| 429 | Rate limited — check `Retry-After` header |
| 500 | Server error |

All errors return: `{ "error": "error_code", "message": "Human-readable message" }`
