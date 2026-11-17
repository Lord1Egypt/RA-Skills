# SMB Sales Boost API reference (for the smb-sales-boost skill)

> **Note for AI agents:** This file may be truncated when opened. Read it fully, in chunks if necessary. `SKILL.md` has the rules and workflows; this file has the complete details. Base URL: `https://smbsalesboost.com/api/v1`. Every endpoint needs `Authorization: Bearer smbk_...` except `POST /purchase` and `POST /claim-key`.

Contents: 1. Endpoints, 2. Lead search parameters, 3. Lead fields, 4. Exports, 5. Export history, 6. Lead export history, 7. Export formats, 8. Export blacklist, 9. Filter presets, 10. Keyword lists, 11. Email schedules, 12. AI endpoints, 13. Enrichments, 14. Account and billing, 15. Signing up, 16. Errors and headers, 17. Integrations.

## 1. Endpoints

Cost: "credits" means it spends credits; "money" means it charges or authorizes charges to the card; "sends data out" means lead data (business contact details) goes to a system outside SMB Sales Boost. Limiter: every endpoint counts toward 600 requests per minute per key; "export" and "AI" are the extra shared 5-per-minute buckets; "integrations" is 60 requests per minute per account, shared with the dashboard and the MCP server (connect also 30 per minute). The long-running calls (`POST /leads/export`, `POST /email-schedules/{id}/trigger`, `POST /ai/suggest-categories` and the three `POST /lead-export-history/...` calls) can answer `202` with a `jobId` instead; `GET /jobs/{jobId}` then returns their answer (section 16).

| Method and path | Purpose | Cost | Limiter |
|---|---|---|---|
| `GET /me` | Profile, plan, credit balance, trial, auto top-up and overage settings | | |
| `PATCH /me` | Update name, company name, company website | | |
| `GET /settings/database` | Always reports the Main database (`other`) | | |
| `GET /leads` | Search leads, full contact details | credits | |
| `GET /leads/preview` | Search leads, contacts masked | free | |
| `GET /leads/other/schema-types` | List website schema types for `websiteSchemaFilter` (`503 schema_types_warming` right after a server restart) | | |
| `POST /leads/export` | Export leads to a CSV, JSON or XLSX file | credits | export |
| `GET /export-history` | List export files (90-day window) | | |
| `GET /export-history/{id}/download` | Download an export file | | |
| `GET /export-history/{id}/download-url` | Short-lived direct download link for an export file | | |
| `GET /lead-export-history` | Every lead you received, with tracking ids | | |
| `GET /lead-export-history/ids` | All matching tracking ids | | |
| `POST /lead-export-history/refresh` | Replace stored copies with current data | free; sends `lead.updated` to your integrations for leads with newer data | export |
| `POST /lead-export-history/re-export` | Rebuild a file from stored copies | free | export |
| `POST /lead-export-history/refresh-and-export` | Refresh, then rebuild a file | free; sends `lead.updated` like refresh | export |
| `GET /export-formats`, `GET /export-formats/{id}` | List or get export formats | | |
| `POST /export-formats`, `PATCH /export-formats/{id}`, `DELETE /export-formats/{id}` | Create, update, delete | | |
| `POST /export-formats/{id}/set-default` | Make a format the default | | |
| `GET /export-blacklist`, `POST /export-blacklist`, `DELETE /export-blacklist/{id}` | Domains to keep out of exports | | |
| `GET /filter-presets`, `POST /filter-presets`, `DELETE /filter-presets/{id}` | Saved searches for email schedules | | |
| `GET /keyword-lists`, `POST /keyword-lists`, `PUT /keyword-lists/{id}`, `DELETE /keyword-lists/{id}` | Keyword lists | | |
| `GET /email-schedules`, `POST /email-schedules`, `PATCH /email-schedules/{id}`, `DELETE /email-schedules/{id}` | Scheduled lead emails | credits, sends email (an active schedule, the default on create, sends its first email within about 15 minutes) | |
| `POST /email-schedules/{id}/trigger` | Send a schedule now | credits, sends email | export |
| `POST /ai/suggest-categories` | Suggest customer categories | | AI |
| `POST /ai/generate-keywords` | Delete all keyword lists and regenerate them | | AI |
| `GET /ai/keyword-status` | Keyword generation jobs (last 24 hours) | | |
| `GET /ai/auto-refine/status` | Refinement progress | | |
| `POST /ai/auto-refine/enable`, `POST /ai/auto-refine/disable` | Start or stop refinement of a list | | AI (enable only) |
| `POST /enrichments` | Start a URL enrichment run | credits | |
| `GET /enrichments`, `GET /enrichments/{id}` | List runs, get one run | | |
| `GET /enrichments/{id}/download` | Short-lived link to the result CSV | | |
| `POST /purchase-credits` | Buy permanent credits with the card on file | money | |
| `GET /auto-top-up`, `PATCH /auto-top-up` | Automatic credit purchases | money (when enabled) | |
| `GET /overage-budget`, `PATCH /overage-budget` | Spend past zero, billed daily | money (when enabled) | |
| `POST /subscription/change-plan` | Upgrade, downgrade, trial switch or activation | money | |
| `POST /subscription/cancel` | Cancel at period end | | |
| `POST /purchase` | Subscription checkout, no API key needed | money | 5 per hour per IP |
| `POST /claim-key` | Older flow that cannot succeed; the key is emailed instead | | 30 per hour per IP |
| `GET /jobs/{jobId}` | The answer of a long-running call that answered `202` (section 16) | | |
| `GET /integrations/providers` | Integration providers and whether each is available now | | integrations |
| `GET /integrations`, `GET /integrations/{id}` | List integrations, get one | | integrations |
| `POST /integrations/webhook` | Create a webhook integration (returns the signing secret once) | sends data out (from then on, automatically) | integrations |
| `PATCH /integrations/{id}` | Rename, pause, re-enable, change events, destination or header `apiKey`, Pipedrive deals | sends data out (when re-pointed, re-enabled or events added) | integrations |
| `DELETE /integrations/{id}` | Delete an integration | | integrations |
| `GET /integrations/{id}/deliveries` | Newest 50 delivery attempts | | integrations |
| `POST /integrations/{id}/deliveries/{deliveryId}/retry` | Re-send one delivery | sends data out | integrations |
| `POST /integrations/{id}/test` | Send a synthetic test event | sends data out | integrations |
| `POST /integrations/{id}/push-lead` | Send one lead now | credits (new lead), sends data out | integrations |
| `POST /integrations/{provider}/connect` | Start a HubSpot, Salesforce or Pipedrive connection, or reconnect one (returns a link) | sends data out (after the user approves) | integrations, plus 30 per minute |
| `GET /integrations/{id}/field-mapping`, `PATCH`, `DELETE` | CRM field mapping: read, change, reset | | integrations |
| `POST /integrations/{id}/field-mapping/test` | Dry run: creates and deletes test records in the CRM | sends data out | integrations |
| `GET /integrations/{id}/pipedrive/pipelines`, `GET /integrations/{id}/pipedrive/deal-fields` | Pipedrive pipelines and deal fields | | integrations |

## 2. Lead search parameters

Used by `GET /leads` and `GET /leads/preview` as query parameters, and inside the `filters` object of `POST /leads/export`, except `maxCredits`, `maxResults` and `excludePurchased`: in an export these go at the top level of the body, next to `filters` (inside `filters` they are silently ignored and the export is not capped). `page`, `limit` and `search` are not used by the export. Unknown parameters are ignored silently.

**Formats.** In a query string, list parameters are JSON-array strings (`["a","b"]`) except the comma-separated ones marked CS. In the export `filters` object, use real JSON arrays for every list (the export ignores JSON-array strings for most of them). The `smb_api.py` script converts both automatically when you pass real arrays.

### Paging, sorting and credit control

| Parameter | Format | Notes |
|---|---|---|
| `page` | integer | Default 1. |
| `limit` | integer | Default 100, clamped to 1-1000 (the API reads `0` or a non-number as 100). On `GET /leads` this is also the most credits one call can spend, so `smb_api.py` accepts only one whole number from 1 to 1000 there and refuses `0`, negative, decimal or text values and a `limit` given twice before anything is sent. |
| `sortBy` | string | Default `lastBuyingSignal` (old name `lastUpdated` still accepted). Others: `wCompanyName`, `wOgrequestedUrl`, `wSimpleCrawledUrl`, `wProfileDate`, `wRedirectYn`, `wAddressCity`, `wAddressState`, `wAddressZip`, `wPhonePrimary`, `wEmailPrimary`, `wTimeScraped`, `wEmployeeCount`, `wFoundingDate`, `wIsChain`, `wPriceRange`, `wLegalName`, `wIndustryNaics`, `wDuns`, `wSlogan`, `wEmailPrimaryMx`, `wEmailDomainMx`, `wEmailSecurity`, `wAddressSource`, and the numeric `wNumLocations`, `wOpenPositions`, `wRatingValue`, `wReviewCount`. Unknown values fall back to the default. |
| `sortOrder` | `asc` or `desc` | Default `desc`. |
| `maxCredits` | integer, 0 or more | `GET /leads` (query; applies to that one call) and export (top-level body field, a JSON number). Most credits that call may spend. `0` returns only leads you already have. On `GET /leads` a non-number or negative value is ignored (no cap) and a decimal is cut to a whole number, so validate it. The export rejects a non-integer or negative value with `400`, but treats `null` as no cap. `smb_api.py` refuses `null`, negative, decimal, `true`/`false` and text values before sending, and refuses `GET /leads` and `POST /leads/export` without `maxCredits` unless `--confirm` is added. |
| `maxResults` | integer, 1 or more | `GET /leads` (query) and export (top-level body field). Most leads to return in this call: on `GET /leads` it trims the current page only, and trimmed leads are not carried to the next page; on export it caps the file. |
| `excludePurchased` | `true` | Preview (query) and export (top-level body boolean). Leaves out leads flagged `contactExported` (see section 3). On preview it is applied after paging, so a page can hold fewer than `limit` leads and `pagination.total` still counts them. `GET /leads` ignores it. |
| `database` | string | Ignored; always the Main database (`other`). |

### Keyword and text filters (these can start a search)

At least one of `positiveKeywords`, `nameIncludeTerms`, `urlIncludeTerms`, `crawledUrlIncludeTerms`, `descriptionIncludeTerms` must be present. Otherwise `GET /leads` and preview return no leads with `requiresKeywords: true`, and export returns `400`.

| Parameter | Matches | Notes |
|---|---|---|
| `positiveKeywords` | `orColumns` | OR across keywords and columns. Case-insensitive substring. `*` is a wildcard; on URL columns spaces are wildcards too. |
| `negativeKeywords` | `orColumns` | Drops a lead when any keyword matches any column (empty values are kept). |
| `orColumns` | | Columns for both keyword lists. Default `wOgrequestedUrl`, `wSimpleCrawledUrl`, `wCompanyName`, `aiCategoryEstimation`. Allowed: those plus `wProfileDescriptionShort`, `wAddressCity`, `wAddressState`, `wAddressZip`, `wPhonePrimary`, `wPhoneTotal`, `wEmailPrimary`, `wEmailTier1` to `wEmailTier6`. Searches stay fast only with the four defaults. |
| `nameIncludeTerms`, `nameExcludeTerms` | Company name | Include terms join the keyword OR group when `wCompanyName` is in `orColumns` (default); otherwise each is required. |
| `urlIncludeTerms`, `urlExcludeTerms` | Registered URL | Same rules. |
| `crawledUrlIncludeTerms`, `crawledUrlExcludeTerms` | Crawled URL | Same rules. |
| `descriptionIncludeTerms`, `descriptionExcludeTerms` | Short description | Not in the default `orColumns`, so each include term is required unless you add `wProfileDescriptionShort`. |
| `search` | Company name, both URLs, short description, city, primary phone | Plain substring; `*` is not a wildcard. `GET /leads` and preview only. Does not count as a positive filter. |

### Location

| Parameter | Format | Notes |
|---|---|---|
| `stateInclude`, `stateExclude` | CS | Uppercase two-letter codes, exact match. |
| `cityInclude`, `cityExclude` | list | Case-insensitive substring. |
| `zipInclude`, `zipExclude` | list | Exact match. |
| `streetInclude`, `streetExclude` | list | Substring. |
| `stateEmptyFilter`, `cityEmptyFilter`, `zipEmptyFilter`, `streetEmptyFilter` | `only_empty` / `exclude_empty` | Empty-value filters. |

### Dates and buying signals

Dates accept ISO 8601 (`2026-09-01`, `2026-09-01T12:00:00Z`) or relative `rel:<n><unit>` with units `h`, `d`, `w`, `m` (months), `y`. Only the Last Buying Signal dates are compared as real dates, and an invalid one makes the call fail with `500`, so check the format. `registrationDateFrom/To` and `timeScrapedFrom/To` are compared as text against the stored values (Time Scraped looks like `2026-09-01 14:30:00`), so use a plain `YYYY-MM-DD` date for them: a time of day, including the time a `rel:` value resolves to, is not applied on the boundary day (a `From` bound leaves out that whole day and a `To` bound keeps it), and an invalid value matches the wrong rows instead of failing.

| Parameter | Notes |
|---|---|
| `lastBuyingSignalFrom`, `lastBuyingSignalTo` | Last Buying Signal range (inclusive). Old names `lastUpdatedFrom`, `lastUpdatedTo` still work; the new name wins if both are sent. A date-only `To` means the start of that day. |
| `buyingSignalTypeFilter` | CS. Exact, case-sensitive types: `Newly Added`, `Phone Primary`, `Total Phones`, `Email Primary`, `Tier 1 Emails`, `Tier 2 Emails`, `Address Full`, `Instagram`, `LinkedIn`, `Facebook`, `YouTube`, `TikTok`, `X (Twitter)`, `Google Maps`, `Yelp`, `Pinterest`, `Other Social`. Old name `updateReasonFilter` still works. |
| `registrationDateFrom`, `registrationDateTo` | Domain registration date. |
| `timeScrapedFrom`, `timeScrapedTo` | When the website was last crawled. |

**What moves the Last Buying Signal:** the lead is first added (`Newly Added`), or a new non-empty value differs from the stored one in Phone Primary, Total Phones, Email Primary, Tier 1 Emails, Tier 2 Emails or Address Full, or a social profile is added or changed for a source (Instagram, LinkedIn, Facebook, YouTube, TikTok, X (Twitter), Google Maps, Yelp, Pinterest, Other Social). `Buying Signal Type` lists the reasons for the most recent change. Removing a value, or changes to other fields, do not move it.

### Contact filters

Term filters take a list whose items are strings or `{"v": "text", "m": "contains" | "starts" | "ends"}` (default contains). Matching is case-insensitive; `*` is a literal character here, not a wildcard. Phones are matched against the stored text, so formatting matters (for an area code use `{"v": "(512)", "m": "starts"}`).

| Include / exclude | Empty filter (`only_empty` / `exclude_empty`) |
|---|---|
| `phonePrimaryInclude`, `phonePrimaryExclude` | `phonePrimaryEmptyFilter` |
| `phoneTotalInclude`, `phoneTotalExclude` | `phoneTotalEmptyFilter` |
| `emailPrimaryInclude`, `emailPrimaryExclude` | `emailPrimaryEmptyFilter` |
| `emailTier1Include` ... `emailTier6Include`, `emailTier1Exclude` ... `emailTier6Exclude` | `emailTier1EmptyFilter` ... `emailTier6EmptyFilter` |
| | `descriptionEmptyFilter` (short description) |

### Company detail columns

For each key below: `<key>Include` and `<key>Exclude` (term lists as above) and `<key>EmptyFilter`. Keys: `employeeCount`, `foundingDate`, `isChain`, `priceRange`, `legalName`, `industryNaics`, `duns`, `founder`, `founderEmail`, `founderPhone`, `openingHours`, `areaServed`, `offers`, `brand`, `slogan`, `logoUrl`, `socialProfiles`, `platform`, `bookingOpsCrmSoftware`, `reputationChatSoftware`, `marketingEmailSoftware`, `adPixels`, `paymentFinancingSoftware`.

| Parameter | Format | Notes |
|---|---|---|
| `minNumLocations`, `maxNumLocations` | number | Number of locations. Leads without a value are excluded when a bound is set. |
| `minOpenPositions`, `maxOpenPositions` | number | Job postings found on the website. `openPositionsEmptyFilter`: empty = no careers page found. |
| `minRatingValue`, `maxRatingValue` | number | Review rating. |
| `minReviewCount`, `maxReviewCount` | number | Number of reviews. |
| `emailPrimaryMxValues`, `emailDomainMxValues` | list | Exact email provider domains, for example `["google.com","outlook.com"]`. |
| `emailSecurityValues` | list | Exact values such as `spf`, `dkim`, `dmarc`, `bimi`, `none`. |
| `addressSourceValues` | list | Exact address-source values. |
| `emailPrimaryMxEmptyFilter`, `emailDomainMxEmptyFilter`, `emailSecurityEmptyFilter`, `addressSourceEmptyFilter` | empty filter | |
| `websiteSchemaFilter` | CS | Substring match on website schema types; values from `GET /leads/other/schema-types` (a bare JSON array, kept up to date in the background so it answers at once; right after a server restart it can answer `503 schema_types_warming` with `Retry-After: 60`, so try again about a minute later). |
| `redirectFilter` | `yes` / `no` | `no` includes leads with no value. |

## 3. Lead fields

Leads from `GET /leads` and preview use display-name keys, in this order: `id`, `Last Buying Signal`, `Last Updated` (deprecated duplicate of Last Buying Signal), `Buying Signal Type` (array or null), `Registered URL`, `Registration Date`, `Redirect` (`Yes` / `No`), `Crawled URL`, `Company Name`, `AI Categories` (array or null), `Address Full`, `Street`, `City`, `State`, `Zip`, `Address Source`, `Platform`, `Booking/Ops/CRM Software`, `Reputation/Chat Software`, `Marketing/Email Software`, `Ad Pixels`, `Payment/Financing Software`, `Employees`, `Number of Job Postings`, `Founding Date`, `Number of Locations`, `Is Chain?`, `Rating Value`, `Review Count`, `Price Range`, `Legal Name`, `NAICS Code`, `DUNS Number`, `Founder Name(s)`, `Founder Email(s)`, `Founder Phone(s)`, `Latitude`, `Longitude`, `Opening Hours`, `Area Served`, `Offers`, `Brand`, `Slogan`, `Logo URL`, `Social Profiles`, `Phone Primary`, `Total Phones`, `Email Primary`, `Email Primary Provider`, `Tier 1 Emails`, `Tier 2 Emails`, `Tier 3 Emails`, `Tier 4 Emails`, `Tier 5 Emails`, `Tier 6 Emails`, `Website Email Provider`, `Website Email Security`, `Website Schema`, `Description Short`, `Description Long`, `Time Scraped`.

- Values are strings or null unless noted. `Social Profiles` is a list written as text, like `['https://facebook.com/x']`.
- Preview masks phones and emails (`(512) ***-**42`, `hel*@domain.com`, list fields masked item by item), including founder emails and phones, except on leads you already have, which come back unmasked with `contactExported: true`. `contactExported: true` in a preview does not guarantee the lead is free in `GET /leads`.
- Response: `{"data": {"leads": [...], "pagination": {"page", "limit", "total", "pages"}, "databaseType": "other", "creditsUsed", "creditsRemaining", "maxResults"?, "maxCredits"?}}`. Preview adds `"preview": true` and has no credit fields. With no positive filter: `leads: []`, `requiresKeywords: true` and a `message`.
- Headers: `X-Credits-Capped: true` when your balance cut the results; `X-Lead-Query-Path` is `sidecar` (fast), `cached` (fast, served from a 20-second cache) or `trigram` (slow, up to about 110 seconds).
- Charging (credit plans): on each page, new leads come first and are cut to the smaller of `maxCredits` and your spendable balance; leads you already have fill the rest of the page free; the page is then cut to `maxResults`. Each returned lead counts as received, and connected CRM and webhook integrations receive it (section 17).

## 4. Exports: `POST /leads/export`

| Body field | Type | Notes |
|---|---|---|
| `filters` | object | Any parameters from section 2 except `search`, `page`, `limit`, `database`, `maxCredits`, `maxResults` and `excludePurchased` (send those three as top-level body fields; inside `filters` they are silently ignored, so a `maxCredits` placed there does not cap spending). Lists must be real arrays (`stateInclude` and `stateExclude` also accept a comma string without spaces, such as `"FL,GA"`: the export does not trim the pieces, so `"FL, GA"` silently ignores GA; `buyingSignalTypeFilter` and `websiteSchemaFilter` also accept a comma string; `positiveKeywords`, `negativeKeywords` and `orColumns` also accept a JSON-array string). Needs a positive filter unless `selectedIds` is used. Up to 100,000 leads. |
| `selectedIds` | integer array | Export these lead ids instead of a filter (filters are then ignored). Practical limit about 12,000 ids (100 KB request body). |
| `maxCredits` | integer, 0 or more (a JSON number) | Most credits to spend. Without it the export can use the whole balance plus any overage budget (`smb_api.py` then requires `--confirm`); `null` also means no cap, so the script refuses it. |
| `maxResults` | integer, 1 or more | Most leads in the file. |
| `maxLeads` | integer, 1 or more | Like `maxResults`, but the overflow (`overflowCount` in the response) is kept in your lead reservoir while it has room and merged into your next `maxLeads` export. The reservoir is one pool per account, shared with email schedules, up to your plan's monthly credit allowance; leads that do not fit are not kept. |
| `excludePurchased` | boolean `true` | Only leads you do not have yet. |
| `formatId` | integer | Export format to use (section 7). A wrong id silently uses your default format, or the built-in CSV. |
| `inline` | boolean | Default `true` (file contents in the response). `false` (or `?inline=false`) returns `exportId` and `downloadUrl` per file instead. |

- File type and columns come from the export format: the one named by `formatId`, otherwise your account's default format (section 7; set in the dashboard or with `set-default`), otherwise the built-in CSV with the default columns below. Before a large export without `formatId`, check `GET /export-formats` for a format with `isDefault: true` and `fileType: "xlsx"` (see the next point).
- XLSX: at most 20,000 rows in one file. An export that would put more in any one file (a single file, a split part, or the `includeTotal` file, which holds every lead) returns `400 export_too_large` after the credits were charged. For large XLSX exports the format must keep every file at 20,000 rows or less: `splitFiles: true`, `splitMode: "max_rows"`, `maxRowsPerFile` of 20,000 or less and `includeTotal: false`. To recover, do not simply repeat the request (an export picks new leads first, so a repeat can charge for different leads): re-run it with a CSV or such a split format, `maxCredits: 0` and no `excludePurchased`, which returns the leads you already have at no cost, or re-export them from the lead export history (section 6).
- Response: `{"data": {"files": [{"fileName", "fileType", "data", "size"}], "leadCount", "exportId", "databaseType": "other", "creditsUsed", "creditsRemaining", "maxLeads"?, "overflowCount"?, "maxResults"?, "maxCredits"?}}`. `files[].data` is plain text for CSV and JSON and base64 for XLSX. With `inline: false`, files carry `exportId` and `downloadUrl` (`/api/v1/export-history/{id}/download`, needs the API key) instead of `data`; a file that could not be stored keeps its `data`.
- File names: `leads-main-YYYY-MM-DD.csv` (or `leads-other-...`); split files add `_part1`, `_part2` and an optional `_total`.
- Default columns (59): `Last Buying Signal`, `Buying Signal Type`, `Registered URL`, `Registration Date`, `Redirect`, `Crawled URL`, `Company Name`, `Categories (AI Enrichment)`, `Phone Primary`, `Total Phones`, `Email Primary`, `Email Primary Provider`, `Tier 1 Emails` to `Tier 6 Emails`, `Website Email Provider`, `Website Email Security`, `Website Schema`, `Description Short`, `Description Long`, `Address Full`, `Street`, `City`, `State`, `Zip`, `Address Source`, `Platform`, `Booking/Ops/CRM Software`, `Reputation/Chat Software`, `Marketing/Email Software`, `Ad Pixels`, `Payment/Financing Software`, `Employees`, `Number of Job Postings`, `Founding Date`, `Number of Locations`, `Is Chain?`, `Rating Value`, `Review Count`, `Price Range`, `Legal Name`, `NAICS Code`, `DUNS Number`, `Founder Name(s)`, `Founder Email(s)`, `Founder Phone(s)`, `Latitude`, `Longitude`, `Opening Hours`, `Area Served`, `Offers`, `Brand`, `Slogan`, `Logo URL`, `Social Profiles`, `Time Scraped`.
- Cells are limited to 32,767 characters in CSV and XLSX (Excel's limit); JSON is not limited. Array values are written as text like `['a', 'b']`.
- The export blacklist (section 8) is applied to exports and previews.
- Every file is also saved in export history for 90 days.
- Long-running: an export still running after about 75 seconds answers `202` with a `jobId` and keeps running; the charge, the lead export history and the export history files are written whether or not anyone collects the answer. `GET /jobs/{jobId}` returns the full response (with `X-Credits-Capped`) for up to 60 minutes after the export finishes, then `410 job_result_expired` for about a day, then `404 job_not_found` (the files stay in export history). Use `inline: false` for large exports so that response stays small. Send an `Idempotency-Key` header (`smb_api.py` does): the same key returns the same job instead of exporting again. To get the result of a running export use `GET /jobs/{jobId}`, never the export again: a new export after it finished (or with other arguments) picks new leads first and charges for them; an identical export while it runs returns the same job. If the answer is lost, check export history and lead export history first; a re-run with `maxCredits` 0 returns leads already paid for at no charge. A `402 insufficient_credits` charged nothing and does not use up the key: buy credits, then retry with the same key. `429 charge_in_progress` (`Retry-After: 30`) means another export, lead search or push of the account was still being charged; nothing was charged. `GET /leads` can answer it too, after waiting up to 30 seconds.

## 5. Export history

- `GET /export-history?limit=N` (0-200, default 50; newest 200 files only): items `{id, fileName, fileType, leadCount, fileSize, formatName, databaseType, filters, createdAt, expiresAt, downloadAvailable, unavailableReason}`. `unavailableReason` is `expired`, `not_stored` or null. Stored `filters` use the internal names (`updateReasonFilter`, `lastUpdatedFrom`).
- `GET /export-history/{id}/download`: the raw file (not JSON) with `Content-Disposition: attachment`.
- `GET /export-history/{id}/download-url`: `{"data": {"downloadUrl", "expiresInSeconds", "fileName", "fileType", "fileSize", "leadCount", "fileExpiresAt"}}`. The link works for at most 15 minutes and must be fetched without the `Authorization` header. Treat it like a password.
- Errors for both: `404 not_found`, `410 {"error": "gone", "reason": "expired" | "not_stored"}` (re-export the leads free, section 6), `503` with `Retry-After: 30` (storage temporarily unavailable).

## 6. Lead export history

Every lead you received (dashboard, API, email schedules, CRM pushes, enrichments) has one tracking row, with a stored copy of the lead as you received it.

- `GET /lead-export-history`: query `limit` (1-200, default 50), `offset`, `dateFrom`, `dateTo` (inclusive), `exportMethod` (`dashboard`, `api`, `email_schedule`, `crm_push`, `enrichment`). Response `{"data": [{"id", "leadId", "exportedAt", "exportMethod", "leadSnapshot", "lastChangedFields", "lead", ...}], "totalCount", "limit", "offset"}`. `id` is the tracking id. Snapshots use internal camelCase field names. Receiving the same lead again updates its row.
- `GET /lead-export-history/ids`: same filters, no paging: `{"data": [ids], "totalCount"}`.
- `POST /lead-export-history/re-export` with `{"trackingIds": [...], "formatId"?}`: free; returns one file (raw, not JSON) built from the stored copies. 1-5,000 ids. `formatId` must be a JSON number; split settings are ignored.
- `POST /lead-export-history/refresh` with `{"trackingIds": [...]}` or `{"filters": {"dateFrom", "dateTo", "exportMethod"}}`: free; overwrites the stored copies with current data and reports `changed` and `changedFields` per id. At most 5,000 rows. When `trackingIds` is sent, `filters` is ignored; otherwise a `filters` date that is not a valid date string (year 1-9999), or a `databaseType` or `exportMethod` that is not a string, returns `400 bad_request` and changes nothing (for example "filters.dateFrom must be a valid date (e.g. 2026-08-18)" or "filters.exportMethod must be a string").
- `POST /lead-export-history/refresh-and-export`: refresh, then return one file like re-export; it also clears the change markers once the file is delivered to you. It checks everything before it changes any entry, so a `400` or `404` leaves the entries unchanged (stored copies and change markers).
- A refresh that finds newer data for a lead sends `lead.updated` to your integrations, unless the lead is on your export blacklist (both refresh calls; a plain re-export sends nothing). Because the refresh records that newer data as received, a later export of the same lead does not send `lead.updated` for that change again.
- All three POSTs share the 5-per-minute export limit.
- All three POSTs are long-running calls (section 16): a big selection can answer `202` with a `jobId`. A file that finishes after a `202` is kept for pickup with `GET /jobs/{jobId}` for up to 60 minutes and is never added to export history (re-export again for free after that; refresh-and-export has already refreshed the entries by then, but it clears their change markers only when the file is delivered, so a file nobody collected leaves them set and running refresh-and-export again, also free, clears them). A tracking id listed twice is processed once.

## 7. Export formats

- Create (`POST /export-formats`): `name` (1-100 characters), `fileType` (`csv`, `json`, `xlsx`) and `fieldMappings` (at least one `{"sourceField", "exportName", "type": "field" | "spacer"}`) are required. Optional: `startRow` (1-100), `includeHeaders` (default true), `splitFiles` (default false), `splitMode` (`max_rows`, `equal_parts`, `parts_max_rows`), `maxRowsPerFile` (10-100,000; for XLSX keep it at 20,000 or less), `numberOfParts` (2-100), `includeTotal` (for XLSX it must stay `false` above 20,000 leads, since the total file holds every lead), `combinedAssigneeColumnName`, `combinedFileNameColumnName` (1-50 characters, for email-schedule combined files). Use whole numbers.
- `PATCH` updates any of those fields; `POST /export-formats/{id}/set-default` makes it the default.
- `sourceField` keys: `lastUpdated` (Last Buying Signal), `lastUpdatedReason` (Buying Signal Type), `wOgrequestedUrl`, `wProfileDate`, `wRedirectYn`, `wSimpleCrawledUrl`, `wCompanyName`, `aiCategoryEstimation`, `wPhonePrimary`, `wPhoneTotal`, `wEmailPrimary`, `wEmailPrimaryMx`, `wEmailTier1` to `wEmailTier6`, `wEmailDomainMx`, `wEmailSecurity`, `wProfileCategory`, `wProfileDescriptionShort`, `wProfileDescriptionLong`, `wAddressFull`, `wAddressStreet`, `wAddressCity`, `wAddressState`, `wAddressZip`, `wAddressSource`, `wPlatform`, `wBookingOpsCrmSoftware`, `wReputationChatSoftware`, `wMarketingEmailSoftware`, `wAdPixels`, `wPaymentFinancingSoftware`, `wEmployeeCount`, `wOpenPositions`, `wFoundingDate`, `wNumLocations`, `wIsChain`, `wRatingValue`, `wReviewCount`, `wPriceRange`, `wLegalName`, `wIndustryNaics`, `wDuns`, `wFounder`, `wFounderEmail`, `wFounderPhone`, `wGeoLat`, `wGeoLong`, `wOpeningHours`, `wAreaServed`, `wOffers`, `wBrand`, `wSlogan`, `wLogoUrl`, `wSocialProfiles`, `wTimeScraped`. An unknown key produces an empty column.

## 8. Export blacklist

- `POST /export-blacklist` with `{"value": "example.com", "entryType": "domain"}`, or `{"entries": [...]}` for several (one invalid entry rejects the batch). `value` is 1-500 characters, stored as sent.
- A lead is left out of exports and previews when its registered or crawled URL contains the value (or the value contains the URL), or its primary email's domain equals the value. Because of the second test, once the blacklist has any domain entry, a lead whose Registered URL or Crawled URL is empty is also left out. `GET /leads`, email schedules, re-export and refresh-and-export do not apply the blacklist to the leads they return.
- `POST /integrations/{id}/push-lead` (with `leadId`) and the `lead.updated` events a lead export history refresh sends check each lead on its own: a lead whose registered or crawled URL contains a value (or is contained in it), or whose primary email's domain equals one, is not pushed (`400 bad_request`) or not announced; an empty URL alone does not match there.
- `GET /export-blacklist` lists entries; `DELETE /export-blacklist/{id}` removes one.

## 9. Filter presets

Presets are used only by email schedules. `POST /filter-presets` body: `{"name": "TX dentists", "filters": {"hash": "<search string>"}}`. The search string is URL-query style (a leading `#` is optional). Keys the schedule engine reads:

| Key | Meaning | Format |
|---|---|---|
| `ni` / `ne` | Company name include / exclude | JSON array, URL-encoded |
| `ui` / `ue` | Registered URL include / exclude | JSON array |
| `cli` / `cle` | Crawled URL include / exclude | JSON array |
| `di` / `de` | Short description include / exclude | JSON array |
| `nkl`, `ukl`, `ckl`, `dkl` | Keyword list ids; positive lists become keywords, negative lists become exclusions | comma-separated ids |
| `si` / `se` | States include / exclude | comma-separated codes, no spaces |
| `ci` / `ce`, `zi` / `ze` | City / ZIP include / exclude | JSON array |
| `rf` | Redirect filter | `yes` / `no` |
| `orc` | Keyword columns (as `orColumns`) | comma-separated |
| `q` | Plain substring search | text |
| `urf` | Buying signal types | comma-separated |

A hash has no key for `positiveKeywords`: `ni`, `ui`, `cli` and `di` each match only their own column and none of them searches AI Categories, while keywords from a positive keyword list in `nkl` are searched like `positiveKeywords` (including AI Categories). So to reproduce a `positiveKeywords` search, create a positive keyword list and put its id in `nkl`. A positive filter is required: a non-empty `ni`, `ui`, `cli` or `di`, or the id of one of your own positive keyword lists (with at least one keyword) in `nkl`/`ukl`/`ckl`/`dkl`. A negative list alone does not count, ids that are not yours are dropped, and a preset without a positive filter silently sends nothing. Example in Python: `"#" + urllib.parse.urlencode({"ni": json.dumps(["*dental*", "*dentist*"]), "si": "TX,OK"})`. Other dashboard filters are not applied by schedules. Presets cannot be edited: create a new one, point the schedule at it with `PATCH` (add `"isActive": false` to the same call if the user should review the new search before it sends), then delete the old one (deleting a preset first deletes every schedule that still uses it: check `GET /email-schedules` for its `filterPresetId` and name those schedules to the user before deleting).

## 10. Keyword lists

- `POST /keyword-lists`: `{"name", "type": "positive" | "negative", "keywords": ["*dental*", ...], "sourceCategories"?: ["Dentists"]}`. `name` is trimmed and must be 1-255 characters, `keywords` a non-empty array of strings, `sourceCategories` an array of strings or null. Other fields are ignored; invalid input returns `400 validation_error`.
- `PUT /keyword-lists/{id}`: any of `name`, `type`, `keywords`, `sourceCategories`.
- `GET /keyword-lists` returns every list with its refinement state (`autoRefineEnabled`, `refinementStatus`: null, `running`, `paused`, `completed`, `failed`; `scoresPerRound`, `pairedListId`). `DELETE` does not delete the paired list.
- Lists are not applied to API searches automatically; pass their `keywords` as `positiveKeywords` or `negativeKeywords`.
- A running refinement rewrites the list's `keywords`, and email schedules whose preset names the list in `nkl`/`ukl`/`ckl`/`dkl` use the new keywords on their next send. Deleting a list (or `POST /ai/generate-keywords`, which deletes them all) silently removes it from those presets: a deleted negative list stops excluding leads, so the schedule can send and charge for more leads, and a preset whose only positive filter was a deleted list stops sending. Regenerated lists get new ids, so point the schedule at a new preset that uses them.

## 11. Email schedules

| Field | Required | Notes |
|---|---|---|
| `name` | yes | 1-100 characters |
| `filterPresetId` | yes | JSON number of your preset |
| `intervalValue` | yes | Whole number 1-720 |
| `intervalUnit` | yes | `hours` or `days` |
| `recipients` | yes | `[{"email": "a@b.com", "splitParts"?: [1]}]`, 1-50 |
| `isActive` | no | Default `true`. Create with `false`, then activate with `PATCH`. |
| `exportFormatId` | no | JSON number or null (default format) |
| `maxLeadsPerEmail` | no | 1-100,000 or null. New leads past the cap, and new leads your credits could not cover, are kept in your lead reservoir (one pool per account, shared by your schedules and API exports, up to your plan's monthly credit allowance; when it is full, more leads are not kept) and sent with a later email. On credit plans, leads you already received that do not fit are not kept. |
| `distributionMode` | no | `full_copy` (default) or `split_evenly` |
| `fullCopyRecipients` | no | Plain email strings, up to 50; receive everything in `split_evenly` mode when at least 2 `recipients` are active (with only 1 active recipient the schedule sends as `full_copy` and these addresses get nothing) |
| `combinedFileEnabled`, `combinedRecipients` | no | A merged file for split formats, sent to plain email strings (up to 50) |
| `combinedIncludeAssignee`, `combinedIncludeFileName`, `combinedColumnPosition` (`beginning` / `end`), `combinedAssigneeColumnName`, `combinedFileNameColumnName` | no | Combined-file columns |

- Each run sends leads whose Last Buying Signal is newer than the last send (the first run sends every match, up to 10,000), puts new leads first, caps them at your spendable credits and `maxLeadsPerEmail`, sends the email, then charges 1 credit per new lead. New leads cut by either cap are kept in the lead reservoir (one pool per account, shared by your schedules and API exports, up to your plan's monthly credit allowance; when it is full, more leads are not kept) and are added to a later email of the schedule, where they cost 1 credit each. On credit plans, leads you already received that do not fit are not kept. A lead that shares a primary phone or email with one you already received counts as received and is free. The schedule pauses only when your spendable balance is 0. There is no time-of-day setting: the schedule is checked every 15 minutes and sends once the interval has passed since the previous send.
- `pauseReason`: `null` (running), `user` (paused by the user) or `insufficient_credits` (paused automatically; resumes when credits are added, the overage budget is enabled, or a trial switches to a larger plan). `PATCH {"isActive": true}` with no credits returns `200` but leaves the schedule paused with `insufficient_credits`.
- `POST /email-schedules/{id}/trigger` ignores the interval and sends now. `400` if the schedule is paused. A `200` does not prove an email went out (for example, no new leads); compare `lastSent` and `totalSentCount`. A `500` is not safe to repeat. It is a long-running call (section 16): a big send answers `202` and keeps going. With an `Idempotency-Key` header (`smb_api.py` sends one and prints it), repeating the call with the same key returns the same send instead of sending again (the key is kept with the job for up to about 48 hours; a server restart forgets it, so then check `lastSent` first); triggering a schedule while a trigger of it is still running also returns that job. `409 schedule_run_in_progress` means the schedule's regular run is sending it right now; nothing was sent by this call (check `lastSent` when it finishes).
- Deleting a schedule also deletes its list of recipients who unsubscribed. To stop a schedule, pause it with `PATCH {"isActive": false}` instead: it keeps that list and can be resumed later.

## 12. AI endpoints

- `POST /ai/suggest-categories`: required `companyName`, `companyDescription`, `productService`; optional `companyWebsite` (the server reads the site), `excludeCategories` (up to 50). Each text at most 2,000 characters. Response `{"data": {"categories": [...], "websiteAnalysisFailed": false}}`. Not saved, nothing charged. A long-running call (section 16): with a website to analyse it can answer `202` and finish in the background (the result is kept for up to 60 minutes).
- `POST /ai/generate-keywords`: no body. Cancels pending jobs, deletes ALL keyword lists, then (only when `GET /me` shows non-empty `targetCategories`) generates one positive and one negative list per category with refinement turned on. Answers `{"data": {"message": "Keyword generation started", "status": "pending"}}` even when nothing will be generated.
- `GET /ai/keyword-status`: `{"data": {"hasJobs", "jobs": [{"id", "status": "pending" | "completed" | "failed" | "cancelled", ...}]}}` for the last 24 hours.
- `GET /ai/auto-refine/status` (optional `?listId=`): per list `listId`, `name`, `type`, `autoRefineEnabled`, `refinementStatus`, `currentRound`, `maxRounds`, `scoresPerRound` (`round`, `score` 1-10, `reasoning`), `lastRefinedAt`, `pairedListId`.
- `POST /ai/auto-refine/enable` / `disable` with `{"listId": <number>}`: applies to the list and its pair. Enabling resets the score history; at most 3 refinements run at once across all customers, and a start that could not run is not queued, so check the status and enable again later if `refinementStatus` stays null.

## 13. Enrichments

- `POST /enrichments` body: `urls` (array of strings; up to 100,000 after duplicates are removed), `maxCredits` (whole number of at least 1; when omitted the run can spend up to your current credit balance but never the overage budget, while a `maxCredits` above your balance lets it draw on the overage budget, which is billed to the card), `databaseMatchPercent` (0-100, default 100: the share of `maxCredits` that may go to new database matches; unused budget flows to live fetches, never the reverse), `contactTypes` (`phone`, `email`, `either`; the minimum a result must carry to be delivered and charged), `emailResults` (boolean; default from the account; the email links to the dashboard). Unknown option names are ignored; `null` values are rejected. Response `202 {"data": {"id", "status": "queued", "urlCount", "duplicatesRemoved", "skippedInvalid"}}`. `400 invalid_request` for bad options or no usable URLs.
- URLs are matched by host name (path, `www.` and protocol ignored for matching; the full URL is used for live fetches). Private and local addresses are refused.
- `GET /enrichments?limit=&offset=` (limit 1-100, default 25) and `GET /enrichments/{id}`: `{"id", "status", "createdAt", "deliveredAt", "options", "urls": {"submitted", "duplicatesRemoved", "skippedInvalid"}, "database": {"matched", "delivered", "charged", "free", "skippedOverBudget", "noRequestedContact"}, "live": {"sentToScraper", "delivered", "failed", "noRequestedContact", "skippedOverBudget"}, "credits": {"databaseCharged", "liveCharged", "total", "final"}, "result": {"rowCount", "ready"}, "error"}`. `error` can be set on a delivered run; it is informational.
- Run status: `queued`, `matching`, `scraping`, `merging`, `delivering`, then `completed`, `partial` (delivered, but a credit limit stopped it early) or `failed` (no file).
- Charging: database matches are charged within seconds of submitting; live fetches are charged when the file is published (`credits.final` becomes true). Live fetch tenths of a credit accumulate across runs and are deducted in whole credits.
- `GET /enrichments/{id}/download`: `{"data": {"downloadUrl", "expiresInSeconds": 300}}`, a link to fetch without the API key. `409 not_ready` while the run is in progress. Download within 90 days.
- Result CSV: one row per usable URL (duplicates and unparseable URLs are only counted), columns `Submitted URL`, `Status`, `Source` (`database`, `live_scrape`, `none`), `Credits Charged`, then the 59 lead columns. Status values: `matched_paid` (1 credit), `matched_free`, `scraped` (0.1 credit), `scrape_failed`, `skipped_db_budget`, `skipped_scrape_budget`, `matched_no_contact`, `scraped_no_contact`, `skipped_invalid` (all free except the two noted).

## 14. Account and billing

**`GET /me`** fields: `id`, `email`, `firstName`, `lastName`, `companyName`, `companyWebsite`, `smbType` (always `other`), `subscriptionPlan`, `subscriptionStatus`, `isSubscribed`, `freeTrialEligible`, `trial` (`isTrialing`, `startedAt`, `endsAt`, `plan`, `outcome`, `convertedAt`, `firstChargeAmountCents` (list price), `freeTrialUsedAt`, `daysRemaining`), `freeLeadsUsed`, `totalLeadsExported`, `monthlyLeadsExported`, `onboardingCompleted`, `targetCategories`, `targetLocations`, `monthlyCredits`, `monthlyCreditsUsed`, `monthlyCreditsRemaining`, `permanentCredits`, `temporaryCreditsRemaining`, `totalCreditsRemaining`, `creditOverageRate` (cents per credit), `autoTopUp` (`enabled`, `triggerType`, `triggerAmount`, `purchaseType`, `purchaseAmount`, `capType`, `capAmount`), `overageBudget` (`enabled`, `budgetType`, `budgetAmount`, `creditsUsedThisCycle`, `amountUsedThisCycleCents`, `pendingChargeCents`, `billingSuspended`). During a trial `monthlyCredits` is the trial allowance.

**`PATCH /me`:** `firstName`, `lastName` (50 characters each), `companyName` (100), `companyWebsite` (500, http or https; `acme.com` is stored as `https://acme.com/`). `null` clears a field.

**`POST /purchase-credits`:** `creditCount` (whole number, 100 up to 5x the monthly allowance: Starter 2,500, Growth 10,000, Scale 50,000, Platinum 500,000, Enterprise 1,250,000) or `dollarAmount` (at least 1; can buy fewer than 100 credits). Optional `Idempotency-Key` header or `idempotencyKey` (8-64 letters, digits, `_`, `-`): a retry with the same key within 24 hours is not charged again (Stripe keeps keys for about a day); after that, check `permanentCredits` in `GET /me` before buying again. Response `{"data": {"success", "creditsAdded", "totalPermanentCredits", "amountCharged", "amountChargedCents", "pricePerCredit", "stripePaymentIntentId"}}`. Errors: `400 no_payment_method`, `402 payment_failed` or `authentication_required` (use a new key after the card is fixed), `403`, `409 plan_change_in_progress` (nothing charged; retry shortly). Credits bought while a paid-plan downgrade is pending (not a trial plan switch) expire at the next renewal with the rest of the balance. New credits also restart email schedules paused for insufficient credits.

**Auto top-up (`PATCH /auto-top-up`):** replaces the whole configuration. Enabling needs `triggerType` and `purchaseType` (`credits` or `dollars`), `triggerAmount` and `purchaseAmount` (purchase at least 100 credits or $1, at most the 5x limit), optional `capType` (`credits`, `dollars` or null) with `capAmount` (a rolling 30-day cap). It compares only the permanent balance with the trigger, and does not run during a trial or while a downgrade is pending. `{"enabled": false}` clears it. `GET` adds `monthlyUsage` and `pricePerCredit`.

**Overage budget (`PATCH /overage-budget`):** `{"enabled": true, "budgetType": "dollars" | "credits", "budgetAmount": N}` (`budgetType` defaults to `dollars` when omitted; at most the dollar or credit equivalent of 5x the monthly allowance per billing cycle). Enabling it also restarts email schedules paused for insufficient credits. Usage past zero is charged to the card once a day (amounts under $0.50 roll to the next day); a failed charge pauses overage use, and 5 failures turn it off. `{"enabled": false}` stops new usage; anything already used is still charged. `GET` returns `enabled`, `budgetType`, `budgetAmount`, `cycleUsage`, `pendingCharge`, `headroomCredits`, `billingSuspended`, `pricePerCredit`.

**`POST /subscription/change-plan`:** `{"targetPlan": "starter" | "growth" | "scale", "mode"?: "switch_trial" | "activate_now"}`. Only between Starter, Growth and Scale. While a downgrade is pending, moves are judged against the plan the downgrade came from, not the current plan. `GET /me` does not show a pending downgrade, so ask the user.

| Situation | Result | Response `changeType` |
|---|---|---|
| Upgrade: a plan above the current one or, while a downgrade is pending, the plan the downgrade came from or a higher one | Full new price charged now, billing cycle restarts, all unused credits kept, new allowance granted | `upgrade` (with `newMonthlyCredits`, `permanentCreditsAdded`) |
| Downgrade: a lower plan or, while a downgrade is pending, any plan below the one the downgrade came from (even one above the current plan, for example Scale, then Starter, then Growth) | No charge now; at the next renewal the whole balance expires, then the new plan's allowance is granted | `downgrade` |
| Trial, `switch_trial` (default) | No charge; trial end date unchanged; allowance = 50% of the new plan minus credits already used | `trial_switch` (with `newCredits`, `creditsRemaining`, `trialEndsAt`) |
| Trial, `activate_now` | Trial ends, the target plan's full price is charged now, full allowance granted, the target plan's remaining trial allowance is added to permanent credits | `trial_activated` (with `newCredits`, `permanentCreditsAdded`, `amountChargedCents`; `alreadyProcessed: true` means it was already done) |

Errors: `400` (same plan, `already_active`, Platinum/Enterprise/legacy plan), `402 payment_declined` (trial activation; `trialStillActive: true`, nothing changed) or `payment_failed` (upgrade), and `409` codes where nothing changed: `plan_change_in_progress` (retry in a moment), `plan_state_changed` (re-read `GET /me`, then retry), `trial_conversion_pending` (wait `retryAfterSeconds`, then re-read: the trial will have converted), `trial_state_changed` (re-read state), `trial_purchase_rate_lock` (credits bought during the trial block moving to a plan with a higher per-credit price; keep the plan, activate it, or use those credits first), `renewal_in_progress` (follow the message), `activation_in_progress` (retry after a refresh). A `500` or timeout may have charged: check `GET /me` before retrying.

**`POST /subscription/cancel`:** no body. `{"data": {"message", "cancelAtPeriodEnd": true, "currentPeriodEnd" (Unix seconds), "status", "isTrial", "trialEndsAt"}}`. Calling it again is harmless. There is no API to undo it.

## 15. Signing up: `POST /purchase`

No API key. Body `{"email", "plan": "starter" | "growth" | "scale" | "platinum" | "enterprise", "trial"?: false}`: Starter, Growth and Scale start a 14-day free trial by default when eligible; only the JSON boolean `false` skips it (the plan price is then charged at checkout and `reason` is `not_requested`). Response `201 {"data": {"checkoutUrl", "expiresAt", "plan", "trial": {"eligible", "days", "credits", "endsAt", "note", "reason"?}, "message"}}`. `reason` when not eligible: `not_requested`, `plan_not_eligible`, `trial_already_used`, `currently_subscribed`. Errors: `400 invalid_email` / `invalid_plan`, `403 forbidden` / `disposable_email`, `409 already_subscribed`, `410 plan_retired`. The API key is emailed after checkout (an address that already has an account first gets an email to confirm the purchase). `POST /claim-key` cannot succeed because no claim token is issued; do not use it.

## 16. Errors and headers

Error body: `{"error": "<code>", "message": "..."}`, plus `details` for `validation_error` (also on the integration endpoints) and `invalid_request`, `creditsRemaining` for `insufficient_credits`, `reason` for `gone`, `retryAfterSeconds` for `trial_conversion_pending`, `declineCode` and `trialStillActive` for `payment_declined`. A rate-limit 429 has `"error": "Rate limit exceeded"` and `retryAfter`; the lead-search capacity 429 has `"error": "lead_query_capacity_busy"`. Malformed JSON gives `400 bad_request`; a body over 100 KB (32 MB for enrichments) gives `413 payload_too_large`.

Safe to retry: every `429`, every `503` except `provider_unavailable` (after `Retry-After`), every `GET` except `GET /leads`, `PATCH` calls outside `/integrations`, `POST /subscription/cancel`, `POST /purchase-credits` with the same idempotency key within 24 hours, and a long-running call repeated with the same `Idempotency-Key` (below). `smb_api.py` retries a `429` or `503` by itself (up to 60 seconds of `Retry-After`), except on integration calls other than `GET` (everything under `/integrations` that changes or sends something): it returns those errors with advice, so check `GET /integrations` (or `GET /integrations/{id}/deliveries` for test, retry and push-lead) and repeat the call once only if the change or delivery is not there. Not safe to repeat blindly after a `500`, a timeout or a `524`: `GET /leads`, `POST /leads/export`, `POST /enrichments`, `POST /email-schedules/{id}/trigger`, `POST /subscription/change-plan`, `POST /integrations/webhook` (check `GET /integrations` first: the same provider and `targetUrl` returns `409 integration_exists`, a changed URL creates a second integration with its own secret, and a lost signing secret means delete and create again), `PATCH /integrations/{id}` (check `GET /integrations/{id}`), `POST /integrations/{id}/push-lead` (may have sent and charged; check `GET /integrations/{id}/deliveries`, where every push that was sent is recorded, for a CRM the CRM itself, and `GET /me`), and creating presets, lists or schedules (a retry can create a duplicate; list first). `POST /integrations/{provider}/connect` is safe to repeat (it only issues a new link).

Response headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` (ISO timestamp), `Retry-After` (seconds), `X-Credits-Capped`, `X-Lead-Query-Path`, and on long-running calls `Location`, `X-SMBSB-Job-Id`, `X-SMBSB-Job-Status` (on `202` answers and `GET /jobs/{jobId}` answers only) and `Preference-Applied`.

### Long-running calls

`POST /leads/export`, `POST /email-schedules/{id}/trigger`, `POST /ai/suggest-categories`, `POST /lead-export-history/refresh`, `/refresh-and-export` and `/re-export` run as background jobs. Input errors (4xx) still answer at once. Otherwise:

- **Finished within the wait:** the usual answer (same status, headers and body), plus `Cache-Control: no-store` and `X-SMBSB-Job-Id`. The wait is about 75 seconds; `Prefer: wait=N` (0-75, counted from when the request arrived) shortens it and `Prefer: respond-async` answers at once (`Preference-Applied` echoes what was honored). The answer always starts within about 90 seconds of arrival.
- **Still running:** `202` with `Location: /api/v1/jobs/{jobId}`, `Retry-After: 5`, `X-SMBSB-Job-Status: running` and `{"jobId", "status": "running", "kind", "phase", "progress": {"done", "total", "label"} | null, "elapsedMs", "statusUrl", "retryAfterSeconds", "message"}`.
- **`GET /jobs/{jobId}`** (any API key of the account): `202` again while it runs (`Prefer: wait=N`, 0-60, waits for it first); once finished, exactly the answer the original call would have given (any status, a file included) with `X-SMBSB-Job-Status: completed` or `failed`. Results are normally kept 60 minutes after the job finished (24 hours for a schedule trigger), sooner under heavy load (each account keeps at most 500 finished jobs). Then `410 job_result_expired` (`X-SMBSB-Job-Status: expired`) for about a day, with a `message` that says where to look, and then `404 job_not_found`, also for an unknown id or a job a server restart interrupted. Never repeat an export or a trigger then: check what it already did first (export history and lead export history, where a re-run with `maxCredits` 0 returns leads already paid for at no charge; `lastSent` in `GET /email-schedules`). Polls count only toward the 600-per-minute limit.
- **`Idempotency-Key` header** (8-64 letters, digits, `_`, `-`): repeating the call with the same key never runs it again; it returns the running job, its stored answer, or the `410` once that answer is no longer kept. The key stays with the job for up to about 25 hours after it finished (about 48 hours for a schedule trigger). A `409`, `429` or `503` answer, and a `402 insufficient_credits` from `POST /leads/export`, does not use up the key; any other answer comes back again for the same key, so after an error answer or with changed arguments use a new key. The same key with a different request answers `409 idempotency_key_reused`; a malformed key answers `400` and nothing runs. Without a key, an identical call returns the job that is still running.
- **Capacity:** each account runs at most 3 exports, 5 schedule triggers, 3 category suggestions and 2 of each lead-export-history call at once; more answer `429 job_capacity_busy` with `Retry-After: 30`. The call still counts toward its 5-per-minute limit (a repeat that returns a running job too).
- **Restarts:** a server restart interrupts running jobs and forgets kept results and keys. What a job already saved stays saved (charges, lead export history, export history files, `lastSent`), and leads you already received are never charged twice.
- `smb_api.py` sends a key on every long-running call, prints it, follows a `202` until the final answer (then saves files as usual), and has `--async`, `--no-wait` and `--job-timeout`.

## 17. Integrations

Integrations send lead data to the user's own systems: CRMs (HubSpot, Salesforce, Pipedrive) and automation tools or any HTTPS endpoint (Zapier, n8n, Make, Pipedream, Clay, Generic Webhook). They use the same API key and paid-plan check as every other endpoint. **Every call that creates, connects, re-points, re-enables, tests or pushes sends business contact details outside SMB Sales Boost: describe the destination and get the user's approval first** (SKILL.md Rule 5; `smb_api.py` requires `--confirm` for them).

### How delivery works

- **Events:**
  - `lead.created` - one event per lead the user receives for the first time (dashboard or API export, API search, email schedule or push).
  - `lead.updated` - one event per lead when a lead you already received reaches your account again with a newer Last Buying Signal than when you last received it (an export or email schedule that includes it, a push to another integration, or a `GET /leads` page or MCP `search_leads` call that returns it), or when a Lead Export History refresh finds that newer data. Receiving an unchanged lead again sends nothing. A refresh sends nothing for a lead on your export blacklist (section 8).
  - `GET /leads/preview` and a plain re-export from the lead export history send no lead events. Leads you get through a URL enrichment run send no `lead.created` or `lead.updated`; the next time such a lead reaches your account it sends `lead.updated`.
  - `export.completed` and `email_schedule.sent` carry the lead count and `sampleLeads` (up to 5 leads, each with id, companyName, website, email, phone, city and state). `credit.low_balance` carries the remaining credits.
  - Lead events carry the business contact details. Delivery runs in the background after the search, export, email or refresh that produced the leads.
- **CRM events:** HubSpot, Salesforce and Pipedrive integrations take only `lead.created` and `lead.updated`; a subscription to any other event returns `400 validation_error` (for example "HubSpot integrations accept only lead.created and lead.updated.", with one `details` entry per refused event) and nothing is saved.
- **Webhook format:** a JSON `POST` of `{"id", "type", "occurredAt", "userId", "integrationId", "provider", "data"}`. For live lead events and `leadId` pushes `data` is a flat lead summary (`id`, `databaseType`, `source`, `companyName`, `website`, `email`, `phone`, `address`, `city`, `state`, `zip`, `lastBuyingSignal`, `buyingSignalType` and the other contact fields; see `openapi.json`); a push of your own data and a test event have their own shapes (rows 9 and 10). It carries the headers `X-SMB-Event`, `X-SMB-Timestamp` and `X-SMB-Signature: t=<unix-ts>,v1=<hex>`, where `v1` is HMAC-SHA256 of `"<ts>." + rawBody` keyed with the integration's signing secret (compare with a timing-safe check). Clay integrations created with `apiKey` also send it as `X-SMB-API-Key`, but only to the active destination URLs it was set for, never to another host: it is bound to them when it is set, and a dashboard edit binds it again to the integration's active destinations on the same origin. A URL on a switched-off subscription is never bound, so switching that subscription on later does not send the key there until the owner edits the integration in the dashboard or `apiKey` is sent again. An API key that points the integration at any new destination URL must send `apiKey` again in the same request. It is never returned.
- **Retries and failures:** webhook deliveries make up to 5 attempts, waiting about 1, 2, 4 and 8 seconds (plus up to 1 second) between them; a CRM delivery is attempted once. Deliveries to HubSpot, Salesforce and Pipedrive are sent at most 3 at a time per integration, and HubSpot calls are paced to HubSpot's rate limits, so a large export reaches the CRM gradually. Pausing a CRM integration, or switching an event off, also stops the lead deliveries still waiting in its queue. After 5 failed deliveries in a row the integration becomes `needs_attention` and stops sending until it is re-enabled (`PATCH` with `{"status": "connected"}`, a successful test or delivery retry, or for a CRM, connecting the same CRM account again). One failed delivery is, for example, a live webhook event whose 5 attempts all failed, a failed CRM write, a failed push, a retry that could not reach the destination, or a test the destination rejected. Every push is recorded in the integration's deliveries and counts toward `needs_attention` like any other delivery. A paused (`disabled`) integration gets no new events, and API/MCP tests, retries and pushes on it are refused (a delivery already in progress may finish its remaining attempts; the owner can still send a test from the dashboard). Failures never change a paused integration's status (re-enabling resets its failure count). Live events never use an inactive subscription (`isActive: false`), and webhook tests and pushes do not either (a CRM test or push goes to the connected CRM); a delivery retry re-sends a past delivery to the URL it was first sent to.
- **CRMs:** HubSpot: per-user OAuth. Creates or updates Contacts matched by email (a lead without an email creates no Contact) and Companies matched by website domain, or by exact company name when the lead has no website of its own (none, or a social or listing page such as Facebook or Yelp), and links each Contact to its Company. Salesforce creates or updates Lead records matched by email (a lead without an email always creates a new Lead; Contacts and Accounts are not written). Pipedrive upserts Persons and Organizations (and optionally creates Deals). The CRM providers can be "available when configured": when one is not set up yet, its calls return `503 provider_unavailable`; check `GET /integrations/providers`.
- **Owner safeguards:** each integration records the API key that created it (`createdVia`) and the channel and key of the last change to where it sends data (`lastChangedVia`, `lastChangedAt`); the dashboard shows them. When an API key (REST or MCP) creates a webhook integration, connects a CRM, points an integration at a new destination, adds or re-activates events, or re-enables it, the account owner is emailed for each change. During bursts of more than 10 changes in an hour, further changes are combined into summary emails. The email shows the destination host only, the key prefix and name, and how to undo it. Connecting a CRM account that is already connected emails the owner only when it brings a `needs_attention` integration back to `connected` (as a re-enable). A CRM connect link stops working when the API key that asked for it is revoked (`key_revoked`; nothing is created). When revoking a key in the dashboard, the user can also pause every integration that key set up (off by default). Every such API key change updates `lastChangedVia`; a dashboard change updates it only when it adds a destination URL the integration never had. Pausing, and resuming, switching on more events or switching on a URL it already had in the dashboard, keep `lastChangedVia`, so an integration a key re-pointed still shows that key.
- **Limits:** at most 25 integrations per account (the limit applies only to new connections: re-authorizing a CRM account that is already connected is not refused) and 20 event subscriptions per integration (duplicate events are merged). Every integration call counts toward 60 requests per minute per account, shared with the dashboard and the MCP server; `POST /integrations/{provider}/connect` is also limited to 30 per minute. Over the limit: `429` with `Retry-After`. Every target URL must be a public `http(s)` address (`https` in production) of at most 2,048 characters; private, local and cloud-metadata addresses are refused with `400 bad_request`.

### The Integration object

`{"id", "provider", "providerName", "status": "connected" | "disabled" | "needs_attention" (set by the system), "displayName", "externalAccountId", "authMethod": "oauth2" | "webhook" | "api_key_webhook", "metadata", "consecutiveFailures", "lastFailureAt", "lastSuccessAt", "tokenExpiresAt", "createdAt", "updatedAt", "subscriptions": [{"id", "eventType", "targetUrl", "isActive", "config"}], "createdVia": {"channel": "dashboard" | "api" | "mcp", "apiKey": {"id", "keyPrefix", "name", "revoked"} | null} | null, "lastChangedVia": {...same shape...} | null, "lastChangedAt"}`

- `externalAccountId` is the destination URL (first 200 characters) for webhooks, and the CRM account id or instance for CRMs. Webhook URLs from Zapier or Make often contain a token: do not paste them into public places.
- `createdVia: null` means the integration was created before this was recorded. Secrets, OAuth tokens and the signing secret are never returned (except the signing secret once, at creation).
- `metadata` holds CRM details such as `hubId`, `instanceUrl`, `apiDomain`, cached field lists, the field mapping and Pipedrive deal settings; it is `null` for webhooks.

### Endpoints

| # | Method and path | Body or query | Response (`200`, inside `{"data": ...}`) | Safety |
|---|---|---|---|---|
| 1 | `GET /integrations/providers` | | `[{"id", "name", "tagline", "description", "authMethod", "ownerSetupRequired", "defaultEvents", "supportsPerLeadPush", "setupHelpUrl"?, "helpText", "available", "reason"?}]` | Read only |
| 2 | `GET /integrations` | | `[Integration]`, newest first | Read only |
| 3 | `GET /integrations/{id}` | | `Integration` | Read only |
| 4 | `POST /integrations/webhook` | `provider` (`zapier`, `n8n`, `make`, `pipedream`, `clay`, `generic_webhook`), `targetUrl`, `events` (1 or more event names), optional `displayName` (1-100 characters), optional `apiKey` (up to 500 characters, sent to the destination as `X-SMB-API-Key`; pass the body with `--body-file`) | `{"integration": Integration, "signingSecret"}` | Sends data out from now on; emails the owner; `--confirm`. `signingSecret` is shown only this once: give it to the user, never log or store it (the script does not save this response with `--out`). Not safe to repeat after a timeout: check `GET /integrations` first. The same provider and `targetUrl` again returns `409 integration_exists`; a changed URL (even a trailing slash) creates a second integration with its own secret. If the integration exists but you did not get its `signingSecret`, read it (`GET /integrations/{id}`), show the user its provider, destination URLs and events, and with their yes delete it (row 6) and create it again with the same values (both need `--confirm`; events that went to different URLs are restored with a `PATCH` of `subscriptions`). |
| 5 | `PATCH /integrations/{id}` | Any of `displayName`, `status` (`connected` or `disabled`; `needs_attention` is set only by the system and sending it is a `400 validation_error`, except as a no-op on an integration that already has it), `subscriptions` (replaces the whole list: `[{"eventType", "targetUrl"?, "isActive"?, "config"?}]`, up to 20; on a HubSpot, Salesforce or Pipedrive integration only `lead.created` and `lead.updated`, active or not, else `400 validation_error` and nothing is saved; a subscription without `targetUrl` takes `defaultTargetUrl`, else that event's current URL, else the integration's first URL for a new event), `defaultTargetUrl` (webhook integrations only, `400 bad_request` on a CRM; sent without `subscriptions` it re-points every existing subscription, inactive ones too, to this URL; to change only some events, send `subscriptions`), `apiKey` (string up to 500 characters, or `null` or `""` to stop sending it; the header secret sent as `X-SMB-API-Key`; only for Clay integrations and webhook integrations that already send one, otherwise `400 bad_request` ("apiKey only applies to Clay integrations and to webhook integrations that already send a header API key"; on a CRM "apiKey only applies to webhook integrations"); pass it with `--body-file`), `pipedriveDeals` (Pipedrive only: `{"enabled"?, "pipelineId"?, "stageId"?, "defaultValue"?, "defaultCurrency"?, "expectedCloseDays"?, "fieldMap"?}`; enabling needs a pipeline and a stage) | `Integration` | Renaming and `{"status": "disabled"}` are harmless. `subscriptions`, `defaultTargetUrl`, `apiKey`, `pipedriveDeals` or `{"status": "connected"}` (from `disabled` or `needs_attention`) change where, what or whether data is sent: `--confirm`, and the owner is emailed when the destination changes, events are added or it is re-enabled. Pointing an integration that has a header `apiKey` at any new destination URL (one none of its subscriptions uses yet, even on the same host) needs `apiKey` in the same request (a new value or `null`), else `400 bad_request` ("This integration sends a header API key. Pointing it at a new destination URL requires apiKey in the same request (a new value, or null to stop sending it)."). A new URL already used by another integration of the same provider gives `409 integration_exists` (nothing changed). If the integration changes while the update is being applied, the update is applied again on top of that change; `409 conflict` ("The integration changed while this update was being applied. Read it again and retry.") means it changed again; nothing changed: read it again and retry. `401 unauthorized` ("This API key has been revoked") means the key was revoked in that moment; nothing was applied. The integration and its subscriptions are saved together, but a `500` may come after the change was saved: check `GET /integrations/{id}` before repeating. |
| 6 | `DELETE /integrations/{id}` | | `{"message": "Integration deleted"}` | Permanent (subscriptions and delivery log too, and a webhook's signing secret cannot be recovered); `--confirm`. To stop sending without losing anything, pause it instead (`PATCH` with `{"status": "disabled"}`, no confirmation needed). |
| 7 | `GET /integrations/{id}/deliveries` | | `[{"id", "eventType", "targetUrl", "status", "statusCode", "attemptCount", "latencyMs", "errorMessage", "responseBody", "createdAt", "completedAt"}]`, newest 50 | Read only. `responseBody` is the destination's reply (up to 1,000 characters). |
| 8 | `POST /integrations/{id}/deliveries/{deliveryId}/retry` | | `{"status", "statusCode"?, "latencyMs"?, "error"?}` (`status` is `success` or `failed`) | Sends the stored payload again to the URL it originally went to (not the current one), with the same event data (a webhook gets a new event `id` and `occurredAt`); `--confirm`. No credits. The retry is recorded in the deliveries, and a failed one (also a timeout or an unreachable host) counts toward `needs_attention`. A paused (`disabled`) integration gives `400 bad_request` ("Integration is paused. Re-enable it first (PATCH status connected)."); a success on a `needs_attention` integration switches it back to `connected` and emails the owner. |
| 9 | `POST /integrations/{id}/test` | | same as 8 | Sends a synthetic `lead.created` test event ("Acme Test Co", website `https://example.com`, no email) to the real destination. For a CRM it creates a real test record that is not removed (HubSpot: no Contact, since the test lead has no email, and an "Acme Test Co" Company for `example.com` that later tests update instead of adding another). `--confirm`. Same paused / `needs_attention` rules as 8. |
| 10 | `POST /integrations/{id}/push-lead` | `{"leadId": 123}` (a lead from the database) or `{"lead": {...}}` (the user's own data) | `{"status", "tracked", "creditsUsed", "result"?, "error"?}` (`status` is `success` or `failed`) | Sends one lead now, to this integration only once; `--confirm`. With `leadId`: a lead the user already received is free, even at a zero balance; a new lead costs 1 credit (`402 insufficient_credits` when there are none) and then counts as received, so the user's other integrations subscribed to `lead.created` also get it, while re-pushing a lead the user already received sends `lead.updated` to their other integrations subscribed to `lead.updated` only when the lead changed since the user last received it (a newer Last Buying Signal); this one gets neither: it receives the lead once, from the push. The export blacklist applies (section 8). With `lead` it is free and not tracked. A leadId push to a webhook sends the same flat lead summary as a live lead.created event, with source `crm_push`. A push of your own data sends `{"lead": <your object as sent>, "source": "manual_push"}`. Both arrive as `lead.created`. The integration must be `connected` (`400` otherwise, also once failures have made it `needs_attention`). Every push is recorded in the integration's deliveries and counts toward `needs_attention` like any other delivery; a push refused before anything is sent (for example "No active subscription for this integration", answered with `status: "failed"`, `tracked: false` and `creditsUsed: 0`, or a `4xx` error) is not recorded, not charged and not added to the export history. Not safe to repeat after a timeout: check the deliveries (a push still in progress can take a minute to appear), for a CRM the CRM itself (a repeat can create a duplicate record), and `GET /me`. `503` happens only before any charge; `500 internal_error` may have taken a credit ("Push failed while charging ..."): check `GET /me` and `GET /lead-export-history` before pushing that lead again. |
| 11 | `POST /integrations/{provider}/connect` | `provider` is `hubspot`, `salesforce` or `pipedrive`; optional `{"environment": "sandbox"}` (Salesforce only; the default is `production`) | `{"provider", "authorizationUrl", "expiresAt"}` | The user must open `authorizationUrl` in a browser within 10 minutes and approve; the CRM account they sign in to is the one connected, and the new integration then appears in `GET /integrations` with these events: HubSpot `lead.created` on and `lead.updated` present but off (turn it on with `PATCH`; `GET /integrations` shows each event's real `isActive`, while `defaultEvents` in `GET /integrations/providers` lists both); Salesforce `lead.created`; Pipedrive `lead.created` and `lead.updated`. Emails the owner. Connecting a CRM account that is already connected re-authorizes that integration in place: it gets new access, a `needs_attention` integration becomes `connected` again, a paused one stays paused, and its events, field mapping, Pipedrive deal settings and delivery history are kept (no new integration, and the owner is emailed only when it brings a `needs_attention` integration back). Use this when a CRM integration is `needs_attention` because its access was removed or expired; the user must sign in to the same CRM account, and a Salesforce sandbox integration needs `{"environment": "sandbox"}`. Signing in to a different account of the same CRM connects it as a new integration. If HubSpot does not confirm which account the user signed in to, nothing is connected or changed ("We could not confirm which HubSpot account you signed in to, so nothing was connected or changed. Please try connecting again in a minute."); ask for a new link a minute later. If the API key that asked for the link is revoked before the user approves, the connection fails with `key_revoked` and nothing is created. `--confirm`. Safe to repeat (a new link). `400 bad_request` only for a wrong `environment` (sent for a provider other than Salesforce, or not `production`/`sandbox`); `409 integration_limit` at 25 integrations, unless the account already has an integration of that provider that a sign-in could re-authorize (the 25-integration limit applies only to new connections, so signing in to a new CRM account then fails in the browser and nothing is created); another provider name is `404`; `503 provider_unavailable` when the provider is not set up. |
| 12 | `GET /integrations/{id}/field-mapping` | optional `refresh=true` (re-read the CRM's field list; it is cached for 10 minutes) | HubSpot `{"smbFields", "contactFields", "companyFields", "cachedAt", "mapping"}`; Salesforce `{"smbFields", "leadFields", "contactFields", "accountFields", "cachedAt", "mapping"}`; Pipedrive `{"smbFields", "personFields", "organizationFields", "cachedAt", "mapping"}` | Reads the CRM |
| 13 | `PATCH /integrations/{id}/field-mapping` | HubSpot `{"contact"?, "company"?}`, Salesforce `{"lead"?}`, Pipedrive `{"person"?, "organization"?}`; each an object from an SMB Sales Boost field id (from `smbFields`) to a CRM field key (1-100 characters). Unknown field ids are dropped. The mapping is replaced as a whole: a scope you leave out is cleared. A scope of another provider is a `400 validation_error` (for example "Scope(s) lead do not apply to HubSpot integrations. HubSpot takes: contact, company."), and a body with no scope is a `400` (use `DELETE` to reset). | `{"mapping"}` | Changes which CRM fields receive the data on every future delivery; `--confirm` |
| 14 | `DELETE /integrations/{id}/field-mapping` | | `{"mapping"}` (the defaults) | Resets the mapping; `--confirm` |
| 15 | `POST /integrations/{id}/field-mapping/test` | optional `{"mapping": {...}}` (test a mapping before saving it) | `{"ok", "scopes": [{"scope", "label", "ok", "issues": [{"smbFieldId"?, "targetField"?, "message", "severity"}]}]}` | Dry run that creates and then deletes synthetic records in the CRM; `--confirm` |
| 16 | `GET /integrations/{id}/pipedrive/pipelines` | | `[{"id", "name", "active", "stages": [{"id", "name", "orderNr"}]}]` | Read only (Pipedrive integrations) |
| 17 | `GET /integrations/{id}/pipedrive/deal-fields` | | `{"smbFields", "dealFields", "cachedAt", "fieldMap"}` | Read only (Pipedrive integrations) |

Routes 12-15 work for HubSpot, Salesforce and Pipedrive integrations; 16-17 for Pipedrive only. Calling one on the wrong kind of integration returns `400 bad_request`. Routes 8-17 return `503 provider_unavailable` (no `Retry-After`; do not retry) when that CRM provider is not set up on this deployment.

### Errors

| Status | `error` | When |
|---|---|---|
| 400 | `validation_error` | The body failed validation; `details` lists the problems. Includes `status: "needs_attention"` in a `PATCH` (unless the integration already has it), a `subscriptions` event other than `lead.created` or `lead.updated` on a HubSpot, Salesforce or Pipedrive integration ("<Provider> integrations accept only lead.created and lead.updated."), and a field-mapping scope of another provider or no scope at all |
| 400 | `bad_request` | A bad id, a route for another provider, an unsafe or private URL, `defaultTargetUrl` or `apiKey` on a CRM, pointing an integration with a header `apiKey` at a new destination URL without `apiKey`, pushing to an integration that is not `connected`, testing or retrying a paused one, Pipedrive deals without a pipeline and stage, a wrong `environment` on connect |
| 401 | `unauthorized` | Missing, invalid or revoked API key; also `PATCH /integrations/{id}` when the key is revoked while the update is being applied ("This API key has been revoked"; nothing changed) |
| 402 | `insufficient_credits` | `push-lead` with a new lead and no credits left (a lead already received stays free) |
| 403 | `forbidden` | No active paid plan, or export limits reached on `push-lead` (accounts not on a credit plan) |
| 404 | `not_found` | The integration (or delivery) does not exist or belongs to another account: "Integration not found. Use GET /api/v1/integrations to list your integrations." |
| 409 | `integration_exists` | The same provider and destination already exist (on create, or a `PATCH` re-point onto a URL another integration of the same provider uses); nothing changed |
| 409 | `integration_limit` | The account already has 25 integrations (on connect, only when no integration of that provider could be re-authorized; reconnecting an account that is already connected is never limited) |
| 409 | `conflict` | `PATCH /integrations/{id}` only, when the integration changed twice while the update was being applied (a single change is absorbed: the update is applied again on top of it): "The integration changed while this update was being applied. Read it again and retry." Nothing changed; read it with `GET /integrations/{id}` and retry if the change still makes sense |
| 429 | `Rate limit exceeded` | More than 60 integration requests per minute for the account (all channels), or 30 connects per minute; wait `Retry-After`. `smb_api.py` does not retry it on calls other than `GET` |
| 502 | `provider_error` | The CRM's API failed (field lists, pipelines, mapping test); try again later |
| 503 | `provider_unavailable` | "<Provider> is not available yet." The provider is not set up; no `Retry-After`; do not retry |
| 503 | `service_unavailable` | A temporary failure before anything was written or charged; repeat after `Retry-After` (for integration changes, check `GET /integrations` or the deliveries first) |
| 500 | `internal_error` | Server error; the change or push may have happened (`push-lead` may have taken a credit): check `GET /integrations`, the deliveries and `GET /me` before repeating |

### Typical flows

```bash
# Webhook to Zapier (after the user approved the destination and events)
python3 smb_api.py GET /integrations/providers
python3 smb_api.py POST /integrations/webhook --body-file hook.json --confirm
# hook.json: {"provider": "zapier", "targetUrl": "https://hooks.zapier.com/hooks/catch/123/abc/", "events": ["lead.created"], "displayName": "Zapier leads"}
python3 smb_api.py POST /integrations/41/test --confirm        # synthetic event to the real URL
python3 smb_api.py GET /integrations/41/deliveries             # did it arrive?
python3 smb_api.py PATCH /integrations/41 --body '{"status":"disabled"}'   # pause (no confirmation needed)

# Connect HubSpot: give the user the authorizationUrl, then look for the new integration
python3 smb_api.py POST /integrations/hubspot/connect --confirm
python3 smb_api.py GET /integrations

# Reconnect a CRM integration that is needs_attention (its access was removed or expired):
# the same connect call; the user signs in to the SAME CRM account, and the integration
# becomes connected again with its events, field mapping and delivery history kept
python3 smb_api.py POST /integrations/hubspot/connect --confirm
python3 smb_api.py GET /integrations/41                        # status connected, consecutiveFailures 0
```
