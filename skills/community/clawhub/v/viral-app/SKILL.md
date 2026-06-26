---
name: viral-app
description: Use the viral.app API from an agent with a local CLI for account analytics, tracked videos/accounts, projects, creator hub, and live data operations.
homepage: https://github.com/fmd-labs/viral-app-skills/tree/main/viral-app
metadata: {"openclaw":{"homepage":"https://github.com/fmd-labs/viral-app-skills/tree/main/viral-app","requires":{"bins":["viral-app"],"env":["VIRAL_API_KEY"]},"primaryEnv":"VIRAL_API_KEY"}}
---

# viral-app

Use this skill when you need to read or manage data through the viral.app API.

## When to use

- Query analytics (accounts, videos, KPIs, exports).
- Manage tracked entities (accounts, videos, exclusions, refresh runs).
- Manage projects and creator hub resources.
- Pull live platform data (Facebook, TikTok, Instagram, YouTube).

## Quick start

1. Ensure `viral-app` CLI is installed and available in `PATH`.

```bash
viral-app --help
```

2. Set API key:

```bash
export VIRAL_API_KEY="..."
```

Get this key from viral.app dashboard at `Settings -> API Keys`.

3. Verify access:

```bash
viral-app accounts-list --per-page 1
```

The wrapper injects `x-api-key` automatically from `VIRAL_API_KEY` unless a header is already passed.

## Inputs to collect first

- Task type: read/report or mutate/manage resources.
- Org-scoped IDs: `orgacc_*`, `orgproj_*`, creator/campaign/payout IDs when relevant.
- Platform and entity identifiers (`facebook|tiktok|instagram|youtube`, platform account/video IDs).
- Time bounds (`--date-range[from]`, `--date-range[to]`) for analytics tasks.
- Pagination/scope (`--per-page`, filters) to keep output focused.

## Command cookbook

Discover available operations:

```bash
viral-app --help
viral-app <command> --help
```

Common reads:

```bash
viral-app accounts-list --per-page 10
viral-app videos-list --per-page 10
viral-app analytics-get-kpis
viral-app analytics-top-videos --per-page 10
viral-app integrations-apps-list
```

Common mutations:

```bash
viral-app projects-create --body '{"name":"My Project"}'
viral-app accounts-tracked-refresh --body '{"accounts":["orgacc_..."]}'
viral-app projects-add-to-account --body '{"projectId":"orgproj_...","accountId":"orgacc_..."}'
```

Payout mutation flow:

```bash
viral-app payouts-calculate --body '{"campaignId":"orgcamp_...","creatorId":"orgcre_...","billingPeriodStart":"2026-03-01T00:00:00.000Z","billingPeriodEnd":"2026-03-31T00:00:00.000Z"}'
viral-app payouts-initiate --body '{"campaignId":"orgcamp_...","creatorId":"orgcre_...","billingPeriodStart":"2026-03-01T00:00:00.000Z","billingPeriodEnd":"2026-03-31T00:00:00.000Z","lineItems":[{"title":"Creator payout","amount":1496.62}],"calculation":{...},"integrityToken":"..."}'
```

Rules for payout mutations:

- Always call `payouts-calculate` immediately before `payouts-initiate`.
- Pass the returned `calculation` payload and `integrityToken` into `payouts-initiate` unchanged.
- Do not invent or recompute `integrityToken`.
- If using `autoApproveTalentir=true`, also set `acknowledgeFullPayoutLiability=true` and explain the risk before executing.
- Prefer review-first behavior for payout mutations unless the user explicitly asks to initiate or approve payouts.

## Report templates

Use the bundled report templates when the user asks for Slack-ready summaries or ranking reports:

- Leaderboard template: [assets/templates/leaderboard.md](assets/templates/leaderboard.md)
- Leaderboard example: [assets/examples/leaderboard-sample.md](assets/examples/leaderboard-sample.md)
- Viral Video Library template: [assets/templates/viral-video-library-report.md](assets/templates/viral-video-library-report.md)
- Viral Video Library example: [assets/examples/viral-video-library-report-sample.md](assets/examples/viral-video-library-report-sample.md)
- Creator payments + CPM template: [assets/templates/creator-payments-cpm-report.md](assets/templates/creator-payments-cpm-report.md)
- Creator payments + CPM example: [assets/examples/creator-payments-cpm-report-sample.md](assets/examples/creator-payments-cpm-report-sample.md)

Rules for leaderboard-style outputs:

- Follow the template structure unless the user explicitly asks for a different format.
- Use analytics account links for account-level leaderboard sections.
- Use tracked video detail links for video leaderboard sections.
- Keep numbers compact, for example `1.4M` or `180K`.
- Use period-over-period trend markers where the comparison window is available.
- Prefer returning the rendered report plus the source viral.app links when useful.

Rules for Viral Video Library reports:

- Use linked titles that point to the Viral Video Library detail page.
- Use abbreviated metrics, for example `473K` or `18.2%`.
- Include a hashtags line for every entry.
- Use a single hook line in the form `Hook (<archetype>): text + visual + audio`.
- Do not use "Audio not surfaced" phrasing.
- Do not invent fields when insights are missing; use `not confidently detected`.

Rules for creator payments + CPM reports:

- Use current in-progress upcoming payouts from Creator Hub for the ranking section.
- Use Creator Hub payout links filtered by both `creatorIds` and `campaigns`.
- Compare each payout row against the most recent completed payout window for the same creator and campaign when available.
- Use current vs previous equal-length periods for org-wide KPI deltas.
- Keep payout amounts exact, view totals compact, Effective CPM to 4 decimals, and spend per video to 2 decimals.

## Linking Back Into viral.app

When a user would benefit from opening the data in the product UI, include a direct viral.app app link in your response.

Default production base:

```text
https://viral.app/app
```

Rules:

- Prefer linking to the most specific page the app actually supports.
- For tracked videos and library videos, use dedicated detail pages.
- For accounts and creators, prefer filtered list/dashboard views. The app does not currently expose a dedicated account detail page or creator detail page route.
- For multi-value filters, use comma-separated values in a single query param.
- For date ranges on analytics and creator-hub overview pages, use `df` and `dt` with `YYYY-MM-DD`.
- Preserve `viewMode` when linking account or creator-related analytics:
  - `internal`
  - `competitors`
  - `all`

Common routes:

- Analytics overview filtered by tracked account:

```text
https://viral.app/app/analytics/overview?accounts=<orgAccountId>&viewMode=internal
```

- Analytics accounts filtered by tracked account:

```text
https://viral.app/app/analytics/accounts?accounts=<orgAccountId>&viewMode=internal
```

- Analytics videos filtered by tracked account:

```text
https://viral.app/app/analytics/videos?accounts=<orgAccountId>&viewMode=internal
```

- Analytics videos filtered by tracked account and date range:

```text
https://viral.app/app/analytics/videos?accounts=<orgAccountId>&viewMode=internal&df=2026-03-01&dt=2026-03-18
```

- Tracked video detail page:

```text
https://viral.app/app/analytics/videos/tiktok/7491234567890123456
```

- Analytics overview filtered by creator-owned tracked accounts:

```text
https://viral.app/app/analytics/overview?accounts=<orgAccountId1>,<orgAccountId2>&viewMode=all
```

- Creator Hub creators filtered by campaign:

```text
https://viral.app/app/creator-hub/creators?campaigns=<campaignId>
```

- Creator Hub creators filtered by search and include archived/inactive creators:

```text
https://viral.app/app/creator-hub/creators?search=alex%40example.com&status=all
```

- Creator Hub campaigns filtered by creator:

```text
https://viral.app/app/creator-hub/campaigns?creatorIds=<orgCreatorId>
```

- Creator Hub campaign detail page:

```text
https://viral.app/app/creator-hub/campaigns/<campaignId>
```

- Creator Hub payouts filtered by creator:

```text
https://viral.app/app/creator-hub/payouts/due?creatorIds=<orgCreatorId>
```

- Creator Hub payouts filtered by campaign:

```text
https://viral.app/app/creator-hub/payouts/due?campaigns=<campaignId>
```

- Creator Hub upcoming payouts filtered by creator and campaign:

```text
https://viral.app/app/creator-hub/payouts/upcoming?creatorIds=<orgCreatorId>&campaigns=<campaignId>
```

- Other payout tabs preserve the same filters:

```text
https://viral.app/app/creator-hub/payouts/upcoming?creatorIds=<orgCreatorId>
https://viral.app/app/creator-hub/payouts/canceled?campaigns=<campaignId>
https://viral.app/app/creator-hub/payouts/paid?creatorIds=<orgCreatorId>
```

- Viral video library filtered list:

```text
https://viral.app/app/library/viral-videos?search=notion&dateRange=30d&sort=views
```

- Viral video library filtered by brand/region/minimum views:

```text
https://viral.app/app/library/viral-videos?brandId=<brandId>&regions=US,GB&minViews=100000&sort=outlier
```

- Viral video library detail page:

```text
https://viral.app/app/library/viral-videos/tiktok/7491234567890123456
```

Supported filter keys you can safely use:

- Analytics overview/accounts/videos:
  - `accounts`
  - `platforms`
  - `projects`
  - `contentTypes`
  - `viewMode`
  - `df`
  - `dt`
- Analytics overview only:
  - `publicationMode`
  - `topVideosBy`
  - `topAccountsBy`
  - `topCreatorsBy`
  - `topEntity`
  - `topListsPerPage`
- Creator Hub creators:
  - `search`
  - `campaigns`
  - `status`
- Creator Hub campaigns:
  - `search`
  - `status`
  - `creatorIds`
- Creator Hub overview / campaign overview:
  - `campaigns`
  - `creatorIds`
  - `scope`
  - `publicationMode`
  - `df`
  - `dt`
- Creator Hub payouts:
  - `creatorIds`
  - `campaigns`
- Viral video library:
  - `search`
  - `brandId`
  - `dateRange`
  - `sort`
  - `minViews`
  - `minOutlierFactor`
  - `regions`
  - `productTypes`
  - `verticals`
  - `formats`
  - `hookArchetypes`
  - `productDetected`
  - `brandDetected`
  - `matchedTerms`

If you do not know the correct org-scoped IDs yet:

- link to the closest filtered list you can build confidently
- say what the link shows
- avoid inventing unknown IDs or unsupported paths

## Safety rules

- Confirm intent before `POST`, `PUT`, `PATCH`, or `DELETE` unless the user explicitly asked for that mutation.
- Run `<command> --help` before mutations to verify required flags and body schema.
- Prefer narrow queries first (`--per-page`, filters, date ranges) before broad exports.
- Keep output machine-readable by default; only switch format when requested.

## Troubleshooting

- `401 UNAUTHORIZED`: missing/invalid API key; verify `VIRAL_API_KEY` or `-H "x-api-key: ..."` value.
- `401` can also happen with expired/revoked keys or wrong org context.
- `429` or retry hints: back off and retry later; inspect response headers such as `Retry-After`.
- Empty `data` arrays: validate filters, project/account IDs, and date range constraints.
- Never expose API keys in commits; rotate keys after sharing for tests.

## Agent defaults

- Output defaults to JSON (`RSH_OUTPUT_FORMAT=json` unless overridden).
- Auto-pagination defaults to disabled (`RSH_NO_PAGINATE=true`) for predictable scripted behavior.
- Summarize key metrics after reads and explicitly call out write-side effects after mutations.
