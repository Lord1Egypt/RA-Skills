# Vercel Web Analytics API: verified ground truth

Everything here was read from the live Vercel docs on 2026-08-14. Where this file
disagrees with memory, folklore, or a blog post, this file wins. Re-verify against
the sources below before changing request or response handling.

Sources:

- <https://vercel.com/docs/analytics/web-analytics-api> (concepts, worked examples)
- <https://vercel.com/docs/rest-api/web-analytics/counts-page-views>
- <https://vercel.com/docs/rest-api/web-analytics/aggregates-page-views>
- <https://vercel.com/docs/rest-api/web-analytics/counts-custom-events>
- <https://vercel.com/docs/rest-api/web-analytics/aggregates-custom-events>
- <https://vercel.com/docs/rest-api/errors> (error envelope, rate limiting)
- <https://vercel.com/docs/analytics/limits-and-pricing> (reporting window)

## Endpoints

Base: `https://api.vercel.com/v1/query/web-analytics`

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/visits/count` | One total of page views. Production only. |
| GET | `/visits/aggregate` | Page view rows grouped by time and/or one dimension. |
| GET | `/events/count` | One total of custom events. Production only. |
| GET | `/events/aggregate` | Custom event rows grouped by time and/or one dimension. |

All four are GET. There is no write surface in this API.

## Authentication

`Authorization: Bearer <token>` using a Vercel access token. Project and team are
passed as query parameters, not headers.

## Query parameters

### count endpoints (`/visits/count`, `/events/count`)

| Name | Required | Notes |
| --- | --- | --- |
| `projectId` | yes | Project ID or project name. |
| `since` | no | Timestamp in milliseconds, or a valid Date string. |
| `until` | no | Timestamp in milliseconds, or a valid Date string. |
| `filter` | no | OData filter. URL-encode the value. |
| `teamId` | no | Team ID. Omit for personal-account projects. |
| `slug` | no | Team slug. Alternative to `teamId`. |

The docs describe count as counting "on a project (production only), since Web
Analytics was enabled". There is no `by` and no `limit`.

### aggregate endpoints (`/visits/aggregate`, `/events/aggregate`)

| Name | Required | Notes |
| --- | --- | --- |
| `projectId` | yes | Project ID or project name. |
| `by` | **yes** | Up to two dimensions. At most one time granularity. |
| `since` | **yes** | Timestamp in milliseconds, or a valid Date string. |
| `until` | **yes** | Timestamp in milliseconds, or a valid Date string. |
| `limit` | no | Integer, min 1, max 100, default 10. |
| `filter` | no | OData filter. URL-encode the value. |
| `teamId` | no | Team ID. |
| `slug` | no | Team slug. |

`by` is required. There is no such thing as an ungrouped aggregate query. An
ungrouped total must use a count endpoint, or must group by a time granularity.

`limit` bounds the number of distinct groups. Remaining groups are collapsed into
a single row named `Others`, which still contributes to the represented total.

### How `by` is serialized on the wire

Confirmed against the machine-readable OpenAPI document at
<https://openapi.vercel.sh/>. The `by` parameter is:

```json
{
  "name": "by",
  "in": "query",
  "required": true,
  "schema": {
    "type": "array",
    "minItems": 1,
    "maxItems": 2,
    "uniqueItems": true,
    "example": ["day", "country"]
  }
}
```

The document is OpenAPI 3.0.3 and sets neither `style` nor `explode` on this
parameter, so the specification defaults apply: `style: form` with
`explode: true`. Array values are therefore sent as **repeated query parameters**,
not as one comma-joined value:

```
?by=day&by=country
```

`uniqueItems: true` means the same dimension must not appear twice, and
`maxItems: 2` is the hard ceiling. Both are rejected client-side before any
request goes out.

The schema also pins the accepted JSON dimension syntax as a regular expression,
`^(flags)(/([0-9A-Za-z_]+|'([^']|'')*'))+$` on the visits dataset, which confirms
that keys may be bare when they are alphanumeric-plus-underscore and must
otherwise be single-quoted with embedded quotes doubled.

## Dimensions

Time granularities, at most one per query: `hour`, `day`, `week`, `month`, `year`.

Plain dimensions, valid on both datasets:

`country`, `deviceType`, `environment`, `requestPath`, `referrerHostname`,
`osName`, `browserName`, `route`, `utmSource`, `utmMedium`, `utmCampaign`,
`utmContent`, `utmTerm`

Events-only additional dimension: `eventName`

JSON dimensions:

- `flags` (both datasets). Bare, it groups by flag name. With a key, `flags/beta_banner`, it groups by that flag's value.
- `eventData` (events dataset only). Bare, it groups by property name. With a key, `eventData/plan`, it groups by that property's value.

Keys containing anything other than letters, digits, and underscores must be
wrapped in single quotes: `flags/'my-flag'`, `eventData/'signup-source'`.

`requestPath` is the exact URL path without query parameters, for example
`/blog/my-post`. `route` is the framework route pattern, for example
`/blog/[slug]`, so many URLs roll up into one row.

## Filters

OData syntax. Quote string values with single quotes and URL-encode the whole
expression.

Supported: `eq`, `ne`, `in`, the logical operators `and`, `or`, `not`,
parentheses, and functions such as `startswith` that the OData parser accepts.

**There are no comparison operators** (`gt`, `lt`, `ge`, `le`) documented for this
API. Do not emit them.

Filterable dimensions match the grouping dimensions above, including
`flags/<name> eq 'true'` and, on events, `eventData/<property> eq 'pro'`.

Example: `requestPath eq '/pricing' and country eq 'US'`

Aggregate endpoints document that the filter "by default, filters for production
environment only". Pass `environment eq 'preview'` to reach preview data.

## Response shapes

Every response is `{ "version": <number>, "query": {...}, "data": ... }`.

`query` echoes the interpreted request. On aggregate it always contains `since`,
`until`, and `limit`, and may contain `groupBy` (an array) and `filter`. On count
it always contains `since` and `until`, and may contain `filter`.

### count

`data` is a single object.

- `/visits/count`: `{ "pageviews": number, "visitors": number }`
- `/events/count`: `{ "count": number, "visitors": number }`

```json
{
  "version": 1,
  "query": { "filter": "requestPath eq '/blog/my-post'" },
  "data": { "pageviews": 1250, "visitors": 980 }
}
```

### aggregate

`data` is an array of row objects.

Grouped by a time granularity, each row carries a `timestamp` plus the metrics:

```json
{
  "version": 1,
  "query": {
    "since": "2024-10-01",
    "until": "2024-10-07",
    "groupBy": ["day"],
    "filter": "requestPath eq '/blog/my-post'"
  },
  "data": [
    { "timestamp": "2024-10-01T00:00:00.000Z", "pageviews": 220, "visitors": 180 },
    { "timestamp": "2024-10-02T00:00:00.000Z", "pageviews": 245, "visitors": 201 }
  ]
}
```

Grouped by a plain dimension, each row carries that dimension as a key:

```json
{
  "data": [
    { "country": "US", "pageviews": 640, "visitors": 510 },
    { "country": "DE", "pageviews": 180, "visitors": 150 }
  ]
}
```

### Parsing trap: JSON dimension row keys

Grouping by `eventData/plan` returns rows keyed **`eventData`**, not
`eventData/plan`:

```json
{
  "query": { "groupBy": ["eventData/plan"] },
  "data": [
    { "eventData": "pro", "count": 42, "visitors": 36 },
    { "eventData": "enterprise", "count": 12, "visitors": 10 }
  ]
}
```

The same applies to `flags/<name>`, which returns rows keyed `flags`. Normalization
must map the returned base key back to the requested dimension so output labels
read correctly.

### Metric names differ per dataset

- visits: `pageviews`, `visitors`
- events: `count`, `visitors`

Code must not assume `pageviews` exists on an events response.

### A note on the published JSON Schema

The REST reference pages publish a generated `oneOf` schema whose row variant
lists roughly 300 field names as `required` (every telemetry column Vercel has,
including AI gateway and workflow fields). That is a schema-generation artifact of
a shared internal row type, not a description of real responses. Real rows contain
only the grouped dimension plus the dataset's metrics, as the worked examples
above show. Parse defensively: read known metric keys, treat everything else as
the group key, and never require fields the examples do not show.

## Errors

Documented statuses on these endpoints: `400` (invalid query value), `401` (not
authorized), `402`, `403` (no permission), `410`.

The envelope is consistent across the REST API:

```json
{ "error": { "code": "bad_request", "message": "An english description of the error that just occurred" } }
```

Rate limiting returns code `rate_limited` and carries a `limit` object:

```json
{
  "error": {
    "code": "rate_limited",
    "message": "The rate limit of 6 exceeded for 'api-www-user-update-username'. Try again in 7 days",
    "limit": { "remaining": 0, "reset": 1571432075, "resetMs": 1571432075563, "total": 6 }
  }
}
```

`reset` is Unix seconds; `resetMs` is Unix milliseconds. Rate limits are documented
as per-endpoint, so one throttled endpoint does not block the others.

Surface `error.message` verbatim to the user. It is the most specific diagnostic
available and is written for humans. This client escapes every control character
in it and scrubs its own token out of it first, so what reaches a screen is
Vercel's sentence and nothing that can forge a line of output around it.

**Show it to whoever asked, and stop there.** The wording is Vercel's choice
rather than this tool's, so it can carry operational context alongside the
diagnosis: an internal identifier, a team or account name, a project id, a rate
limit budget together with the endpoint key it belongs to, or which add-on a plan
is missing. That is precisely why it is worth putting in front of the operator
debugging the problem, and precisely why it should not travel any further.
Nothing here rewrites it into a general-audience string, so it should not be
forwarded onward or pasted into an issue tracker, a chat channel, a status page
or another service without being read first. Quoting it to the person who asked
is deliberate; passing it along is not.

## Reporting window

The reporting window is how long analytics data is guaranteed to be queryable.

| Plan | Reporting window |
| --- | --- |
| Hobby | 1 month |
| Pro | 12 months |
| Pro with Web Analytics Plus | 24 months |
| Enterprise | 24 months |

Plan tier is not discoverable from this API, so a `--since` older than the window
should warn rather than block: the query is still legal and may return data, since
Vercel may retain beyond the guarantee.

Other plan-gated behavior worth knowing: custom events require Pro or above, and
UTM parameters require Web Analytics Plus or Enterprise. A query for those on a
lower plan is expected to come back empty rather than to fail.

# Vercel Speed Insights: verified ground truth

Read from the live docs and the OpenAPI document on 2026-08-14. Speed Insights
does not have a dedicated query API. It is exposed through Vercel's general
Observability query surface, which is a different shape from Web Analytics.

Sources:

- <https://vercel.com/docs/speed-insights/accessing-metrics-with-vercel-cli> (metric ids, worked queries)
- <https://vercel.com/docs/cli/metrics> (the full option surface `vercel metrics` exposes)
- <https://vercel.com/docs/query/reference> (aggregations, filter operators, group-by fields)
- <https://vercel.com/docs/speed-insights/metrics> (metric definitions, targets, percentile semantics)
- <https://openapi.vercel.sh/> (the three observability endpoints)

## Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| POST | `/v2/observability/query` | Run one metric query. This is the only way to read Speed Insights data. |
| GET | `/v2/observability/schema` | List queryable metrics for the current scope. |
| GET | `/v2/observability/schema/{metricId}` | Describe one metric: dimensions, unit, aggregations. |

There is no GET query endpoint. `POST` here is a read: the body carries the
query, and nothing is created or mutated. The `/speed-insights/toggle` and
`/web/insights/toggle` endpoints in the same API are writes that enable or
disable the feature, and this project never calls them.

## Metric ids

Confirmed verbatim from the CLI documentation. Every value metric has a matching
count metric giving the number of collected data points behind the value.

| Web Vital | Value metric | Data point count metric | Unit |
| --- | --- | --- | --- |
| Largest Contentful Paint | `vercel.speed_insights.lcp_ms` | `vercel.speed_insights.lcp_count` | milliseconds |
| Interaction to Next Paint | `vercel.speed_insights.inp_ms` | `vercel.speed_insights.inp_count` | milliseconds |
| Cumulative Layout Shift | `vercel.speed_insights.cls` | `vercel.speed_insights.cls_count` | unitless score |
| First Contentful Paint | `vercel.speed_insights.fcp_ms` | `vercel.speed_insights.fcp_count` | milliseconds |
| Time to First Byte | `vercel.speed_insights.ttfb_ms` | `vercel.speed_insights.ttfb_count` | milliseconds |

`vercel.speed_insights` is also valid as a prefix for the schema endpoint.

**Real Experience Score is not queryable.** The docs state plainly: "Real
Experience Score is not available through `vercel metrics`; use the Speed
Insights dashboard to view Real Experience Score." The same applies here, since
both go through the same query surface. Do not invent an RES metric id.

## Request body

`POST /v2/observability/query`, `Authorization: Bearer <token>`, JSON body.
Required: `metric` and `scope`.

| Field | Type | Notes |
| --- | --- | --- |
| `metric` | string | Metric id, required. |
| `scope` | object | Owner or project scope, required. |
| `aggregation` | string | Defaults to the metric's `defaultAggregation` from the schema. Some aggregations take a dimension as `<agg>/<dimension>`, for example `unique/visitor_id`. |
| `groupBy` | string[] | Dimensions to group by. Repeatable, same JSON-dimension and quoting rules as Web Analytics. |
| `filter` | string | OData filter. |
| `limit` | number | Maximum grouped results per time bucket. The CLI documents a default of 10. |
| `orderBy` | string | Rollup column for grouped results. The CLI exposes this as `count` or `value`, defaulting to count. |
| `orderDirection` | string | `asc` or `desc`, default `desc`. |
| `granularity` | object | Time bucket size. |
| `startTime` | string | Start timestamp. |
| `endTime` | string | End timestamp. |
| `bucketTimezone` | string | IANA zone, for example `Europe/Paris`. Aligns calendar buckets (`1d`, `1mo`) only. `startTime`, `endTime` and all output timestamps stay UTC. No effect below daily granularity. |

Documented responses: 200, 400, 401, 402, 403, 408, 410. Note the 408, which
Web Analytics does not have: a query can time out server-side, and that is worth
retrying.

### The scope object: VERIFIED in two steps

The published OpenAPI document declares `scope` as a bare `{"type": "object"}`
with no inner properties, so the shape had to be learned from the API itself.
Two 400s were needed, and each named one half of the answer.

**First**, sending `{"type": "project", "projectId": "..."}`:

```json
[{"expected": "string", "code": "invalid_type",
  "path": ["scope", "ownerId"],
  "message": "Invalid input: expected string, received undefined"},
 {"expected": "array", "code": "invalid_type",
  "path": ["scope", "projectIds"],
  "message": "Invalid input: expected array, received undefined"}]
```

**Then**, dropping `type` and sending `{"ownerId": ..., "projectIds": [...]}`:

```json
[{"code": "invalid_union", "errors": [], "note": "No matching discriminator",
  "discriminator": "type", "path": ["scope", "type"], "message": "Invalid input"}]
```

Put together: **`scope` is a union discriminated on `type`, and the `project`
variant carries both `ownerId` and `projectIds`.**

```json
{"type": "project", "ownerId": "<account id>", "projectIds": ["prj_..."]}
```

The first response is what confirms `project` is a real discriminator value: a
request carrying it got past the union and was judged on its fields instead.

For `--all` this client sends `{"type": "owner", "ownerId": "..."}`, on the
reading that a whole-owner scope names no projects. **That variant name is the
one remaining guess** in the scope; the `project` variant is verified.

**The owner is the account that owns the project.** For a team owned project
that is the team id, so a team is simply its own owner. For a personal project
it is not knowable locally at all, so this client reads it once per run unless
`--owner-id` or `VERCEL_OWNER_ID` supplies it. That is why the operation
allowlist carries a fourth, read-only entry.

**Where the owner is read from, and why not the obvious place.** The first
attempt used `GET /v2/user`, which answered `404 User not found.` against a real
token: a team scoped token has no personal user to return. The right source is
the project's own record, `GET /v9/projects/{idOrName}`, whose `accountId` is a
required top-level string. It answers the same way for a team owned and a
personal project, and the token must already be able to read it, since it is the
project being queried. `--all` has no single project to ask about, so it
requires an explicit owner.

A team **slug** is a name, not an account id, so it cannot fill `ownerId`. A slug
given alone on this surface is refused rather than quietly falling back to the
personal account, which would answer confidently about the wrong account.

`projectIds` is a list of project **ids**. The Web Analytics endpoints document
their `projectId` parameter as "the project identifier or the project name", but
this field asks for ids, and a name is likely to return an empty result rather
than an error, so a value that does not look like `prj_...` is warned about.

### The response body: VERIFIED

A successful query returns:

```json
{
  "query": { ... echo of the interpreted query ... },
  "data":    [ {"timestamp": "...", "<rollup key>": 3868}, ... ],
  "summary": [ {"<rollup key>": 2908} ],
  "orderBy": "<rollup key>",
  "orderDirection": "desc",
  "queryId": "1048351860",
  "statistics": {"bytesRead": 2452137, "rowsRead": 50284, "dbTimeSeconds": 0.067}
}
```

**The rollup key is computable**, not something to probe for: it is the metric
id with dots replaced by underscores, then the aggregation. So
`vercel.speed_insights.lcp_ms` at `p75` is `vercel_speed_insights_lcp_ms_p75`,
and that key names the value in both `data` rows and `summary`.

**`summary` is the window aggregate and the only correct ungrouped answer.** It
cannot be derived from `data`: a percentile does not average, so the P75 of 168
hourly P75s is not the P75 of the week. On a real project the first bucket read
6708 ms while the true window figure was 2908 ms, which is the difference
between "over target" by a lot and "over target" by a little.

An ungrouped query still comes back as a time series, because the server picks a
granularity when none is given (hourly over a week). `summaryOnly: true` in the
request is **ignored**: it appears in the echoed query as `false` regardless, so
it is an output field rather than an input.

### Granularity: VERIFIED

The earlier `{"interval": "1d"}` was refused outright:

> Granularity `{"interval":"1d"}` is not valid. It must divide a day evenly or
> be a single week, month or year.

The real shape is a unit and a count. Confirmed by live probes over a 7 day
range:

| Sent | Result |
| --- | --- |
| nothing | 168 rows, server echoes `{"hours": 1}` |
| `{"hours": 1}` | 168 rows |
| `{"hours": 24}` | 7 rows |
| `{"days": 1}` | 7 rows |
| `{"weeks": 1}` | refused, but on a **plan** limit, not a shape error |

This client sends `{"hours": 1}`, `{"days": 1}`, `{"weeks": 1}`,
`{"months": 1}` and `{"years": 1}`.

### Plan limits on this surface differ from Web Analytics

A live Hobby account answered:

> Invalid request: the hobby plan only grants access to the latest 7 days of
> data.

So observability on Hobby is **7 days**, not the 1 month Web Analytics allows.
The reporting-window warning in this client is calibrated to the Web Analytics
figures and will not catch this.

### Still not pinned down

Two things remain inferred, both marked ASSUMPTION in the code:

- **`granularity`.** Sent as `{"interval": "1d"}`. Never yet exercised by a
  successful live call.
- **The 200 response body.** Declared as a bare object, so `normalize` probes
  for each plausible shape and reports a clear `invalid_response` rather than
  raising on anything unexpected.
- **`--all`.** Sends an empty `projectIds` list, on the reading that naming no
  project means every project the owner has. Not confirmed.

## Aggregations

From the Query Reference: Count, Count per Second, Sum, Sum per Second, Minimum,
Maximum, Percentiles (75th, 90th, 95th, 99th), and Percentages. The CLI spells
percentiles `p75`, `p90`, `p95`, `p99`. P75 is the dashboard default and the
right default here.

Aggregations are computed both within each time bucket and across the whole
query window.

## Dimensions

Confirmed in worked CLI examples: `route`, `request_path`, `device_type`,
`country`, `project_id`, `environment`.

The Query Reference lists a wider set for the observability surface generally
(request hostname, deployment id, HTTP status, cache result, request method,
referrer, client IP and country, user agent, ASN, CDN region, WAF action and
rule id, skew protection, sandbox name and session id). Not all of these are
meaningful for a Speed Insights metric, so treat the six confirmed ones as the
supported set and let the schema endpoint be the source of truth for the rest.

Note the naming difference from Web Analytics: this API uses `snake_case`
(`device_type`, `request_path`, `project_id`) where Web Analytics uses
`camelCase` (`deviceType`, `requestPath`). A dimension name is not portable
between the two surfaces.

## Filters

OData, same family as Web Analytics. `vercel metrics` accepts `--filter`
repeatedly and joins the expressions with `and`.

Confirmed operators: `eq`, `ne`, `in`, `startswith()`, and, unlike Web
Analytics, the numeric comparisons `>`, `>=`, `<`, `<=`. The Query Reference
also lists `endsWith`.

Worked examples, verbatim from the docs:

```text
route eq '/dashboard'
startswith(request_path, '/docs') or startswith(request_path, '/guides')
country ne 'US'
```

`--prod` in the CLI is documented as exactly equivalent to
`--filter "environment eq 'production'"`.

## Granularity mapping

The two surfaces spell time buckets differently, and there is no single
vocabulary that satisfies both:

| Meaning | Web Analytics (`by=`) | Observability (`granularity`) |
| --- | --- | --- |
| hourly | `hour` | `1h` |
| daily | `day` | `1d` |
| weekly | `week` | no documented equivalent |
| monthly | `month` | `1mo` |
| yearly | `year` | no documented equivalent |

Accept both spellings from the user and translate per target. Reject a
granularity that has no equivalent on the selected surface with a specific
error, rather than sending something the API will refuse.

## Targets for interpreting values

Vercel publishes a single "good" target per metric. It does **not** publish the
upper boundary between "needs improvement" and "poor", so do not render a
three-tier rating as though Vercel defined it.

| Metric | Vercel's stated good target |
| --- | --- |
| LCP | 2.5 seconds or less |
| CLS | 0.1 or less |
| INP | 200 milliseconds or less |
| FCP | 1.8 seconds or less |
| TTFB | under 800 milliseconds |
| FID | 100 milliseconds or less |
| TBT | under 800 milliseconds |

Lower is better for every one of them. The dashboard's 0 to 100 colour bands
(0 to 49 poor, 50 to 89 needs improvement, 90 to 100 good) apply to *scores*
derived from a log-normal distribution of HTTP Archive data, not to raw metric
values, so they cannot be applied to a raw millisecond figure.

## Percentile semantics

P75 means the fastest 75% of users, excluding the slowest 25%. A P75 LCP of
1 second means 75% of users saw LCP faster than 1 second. Same pattern for P90,
P95 and P99.

A data point is one measurement of one Web Vital during one visit, collected on
hard navigations. Up to 6 per visit are possible, typically 3 to 6. This is why
the `*_count` metrics matter: a P75 over a handful of data points is not
comparable to one over thousands, and grouped queries default to ordering by
count for exactly that reason.

## Token scope: the two APIs scope differently

VERIFIED against the live API on 2026-08-15, by comparing the same account under
two credentials.

| API | Scoped by | Project scoped token |
| --- | --- | --- |
| Web Analytics `/v1/query/web-analytics/...` | `projectId` query parameter | **200** |
| Observability `/v2/observability/*` | `scope.ownerId` in the body | **404** |

A token bound to a single project has no account context, and the observability
API is account-level, so Vercel answers `404 Observability Data not found.` The
same account with an account-scoped credential returns 96 metrics from
`/v2/observability/schema`, Speed Insights among them, which is what isolates
this to credential scope rather than entitlement or missing data.

The request logs surface, added later, scopes by an account too, through an
`ownerId` query parameter. It is expected to refuse a project scoped token for
the same reason, with a `403` rather than a `404`, but that has never been tested:
the request logs chapter below records it as an assumption rather than adding a
row to the table above, which is verified.

Three things this rules out, each of which looked plausible on the way:

- **Not Observability Plus.** The docs' exemption for Speed Insights holds.
- **Not a disabled feature.** The project reported `speedInsights.hasData: true`.
- **Not the request shape.** The query endpoint validated the body first, and
  only then answered 404.

Note also that `/v2/user` answers `404 User not found.` for a project scoped
token, which is why the owner is read from the project record instead. Vercel's
own CLI hits the same wall, and prefers `VERCEL_TOKEN` over its own OAuth
session, so `vercel whoami` fails the same way when that variable is set. That
is worth knowing before concluding anything from a CLI comparison.

## Plan access

Speed Insights metrics are available through this query surface **without**
Observability Plus. The docs state it twice, on both the CLI reference and the
Speed Insights CLI page. Metrics other than Web Analytics and Speed Insights do
require Observability Plus, so a query for anything outside those two families
may fail on plan grounds.

Speed Insights collects data on all deployed environments, preview included, so
unlike the Web Analytics count endpoints there is no production-only
restriction to work around. Filter by `environment` to narrow it.

# Vercel request logs: verified ground truth

Probed against the live API on **2026-08-17** with a team scoped token, or read
from the live docs the same day. This is the surface behind the `logs`, `errors`
and `error-summary` presets. Where this chapter disagrees with memory, folklore
or a blog post, this chapter wins.

Read this before anything else here: **this endpoint is not in Vercel's published
OpenAPI document.** <https://openapi.vercel.sh/> does not list it, so there is no
schema to check a claim against and no versioning promise to rely on. Its ground
truth is the Vercel CLI's own source, `packages/cli/src/util/logs-v2.ts`,
function `fetchRequestLogs`, which is what `vercel logs` calls in its
non-streaming mode, plus the live probes recorded below. It can change without
notice, which is exactly why every claim in this chapter says how it was learned.

And read this before quoting anything this surface returns: **a request log row
is free text that somebody else's application wrote.** It can hold that
application's own API keys, connection strings, session identifiers or customer
data, and this client can recognise and redact exactly one secret, its own Vercel
token. There is no general redaction here, and there cannot be a useful one, so
the rule is to quote the minimum that answers the question and never to forward
log output to another service. *This client scrubs its own token out of log rows*,
below, states exactly what is covered and what is not.

Sources:

- Vercel CLI source, `packages/cli/src/util/logs-v2.ts`, function `fetchRequestLogs` (the endpoint, its parameters, and the `logs[]` item shape)
- <https://vercel.com/docs/runtime-logs> (retention, volume limits)
- <https://openapi.vercel.sh/> (which does not carry this endpoint, and does carry the two alternatives that turn out not to work)
- Live probes against a real production project, on a team scoped token, 2026-08-17

## Endpoint

```
GET https://vercel.com/api/logs/request-logs
Authorization: Bearer <the same Vercel access token>
```

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `https://vercel.com/api/logs/request-logs` | One page of runtime request logs, newest first. |

Note the host: **`vercel.com`, not `api.vercel.com`**. It is the only operation in
the allowlist that is not on the API host, which is why `__init__.py` carries a
second base URL (`LOGS_BASE_URL`) and why `tests/test_security.py` asserts an
explicit two-host set rather than one host: a third host is still a test failure.

Latency observed: 1.4s to 6.0s per call. The 30 second default timeout is per
request, so it is comfortable for one page, and it should not be lowered for this
surface. Latency is also why `logs.collect` stops after four pages: at the top of
that range four pages is 24 seconds of waiting, and since the timeout is per
request rather than per run, nothing else would cut a longer walk short.

## Authentication and scope

`Authorization: Bearer <token>`, the same kind of Vercel access token the other
two surfaces use. Scope travels in the query string as `projectId` and `ownerId`,
and both are required.

`teamId` is **not** accepted as a substitute for `ownerId`: verified, and the
reason this client never sends one. So the Web Analytics "name your team" hint
would point a reader at a parameter that does not help here. A team is its own
owner, so a team id is the right value for `ownerId`.

**When the owner has to be looked up.** Only when nothing supplies it:
`--owner-id`, `VERCEL_OWNER_ID`, `VERCEL_ORG_ID` or the team id. For a personal
account none of those may be set, and then the owner is read once per run from
`GET /v9/projects/{idOrName}` as `accountId`, the same lookup Speed Insights
already needed. A project **name** does not force that lookup on this surface:
this endpoint accepts a name as happily as an id (see the parameter table), so
resolving one would buy nothing, and the header line showing the name the user
actually typed is more honest than showing an id they never did. Speed Insights
differs, because its scope matches on `projectIds`, where a name comes back empty
rather than as an error.

ASSUMPTION, marked as one in `cli.py::_explain_request_logs_403`: a
**project scoped** token probably cannot read this endpoint, by analogy with
Speed Insights, since this call also carries an `ownerId` and a project scoped
token has no account to act for. Only a team scoped token was available to test
with. Omitting `ownerId` is a 400 and a value the token cannot reach is a 403,
which is why a 403 here gets the token-scope explanation rather than a team one.

## Query parameters

Required. Omitting either of the first two is a `400`:

| Name | Notes |
| --- | --- |
| `projectId` | Project id or project **name**; both verified working. |
| `ownerId` | Account id owning the project. Missing: `400 Validation error: Required at "ownerId"`. Wrong value: `403 You don't have permission to access this resource.` |
| `page` | Zero based page index. |
| `startDate`, `endDate` | Unix **milliseconds**, not seconds and not ISO-8601. |

Optional, all verified to filter:

| Name | Accepted values | Notes |
| --- | --- | --- |
| `level` | `error`, `warning`, `info`, `fatal`, comma separated | Matches **application log lines only**; see below. |
| `statusCode` | integers, `Nxx` classes, or the literal `None`, comma separated | Server-side rule quoted below. |
| `source` | `serverless`, `edge-function`, `edge-middleware`, `static`, comma separated | The display vocabulary differs; see below. |
| `environment` | `production`, `preview` | |
| `requestPath` | exact path | **Exact match**: `/api` returned nothing, `/api/me` returned only that path. |
| `route` | exact route pattern | `/api/documents/[slug]` returned 23 rows across 14 distinct paths. |
| `requestMethod` | `GET`, `POST`, ... | Recorded in upper case on every row seen. Whether the filter is case sensitive was never probed; this client upper-cases the value, which cannot be wrong either way. |
| `branch` | git branch name | |
| `deploymentId` | `dpl_...` | |
| `requestId` | one request | |
| `search` | free text | Not a query syntax; see below. |

Silently ignored, verified to have no effect: `limit`, `path`, `method`,
`domain`, `host`. **`limit` being ignored is the reason a row limit is enforced
in this client** rather than asked of the server: `logs.collect` counts rows as
they arrive and stops.

## Response shape

```json
{"rows": [ ... ], "hasMoreRows": true}
```

A page is **50 rows**, fixed. `hasMoreRows` is the only pagination signal. Rows
arrive newest first, which was observed rather than documented, so
`logs.merge` sorts anyway: ordering is then a property of this client rather than
an assumption about a server.

One real row, trimmed, from a live production project. Every field name,
every type and every empty string is exactly as the API returned them. The
identifiers are not: the request id, deployment id, domains, invocation id and
route name below were replaced with fictional values of the same shape, because
this file is published and a real account's identifiers are not documentation.

```json
{
  "requestId": "abcde-1786964768933-0123456789ab",
  "timestamp": "2026-08-17T11:06:08.933Z",
  "deploymentId": "dpl_ExampleDeploymentId000000000",
  "environment": "production",
  "deploymentDomain": "acme-docs-1a2b3c4d5-...vercel.app",
  "branch": "main",
  "domain": "acme-docs-1a2b3c4d5-...vercel.app",
  "requestMethod": "GET",
  "requestPath": "/api/me",
  "statusCode": 401,
  "errorCode": "",
  "route": "/api/me",
  "cache": "MISS",
  "wafAction": "",
  "traceId": "",
  "logs": [],
  "requestDurationMs": 54,
  "clientRegion": "fra1",
  "hasFunctionCrashed": false,
  "events": [
    {
      "source": "serverless",
      "route": "/api/me",
      "httpStatus": 401,
      "region": "fra1",
      "durationMs": 9,
      "functionRuntime": "nodejs24.x",
      "functionStartType": "hot",
      "functionMaxMemoryUsed": 329,
      "invocationId": "01EXAMPLEINVOCATION0000000"
    }
  ],
  "requestTags": ["ssr", "rsc"]
}
```

`source` is read off the first event that carries one, because the row itself has
no such field, so a row with no event has no source and the table prints `-`.
`region` is read the same way and falls back to the row's own `clientRegion`.

Other fields present on real rows and not used by this client, listed so nobody
has to re-probe: `service`, `callingService`, `resolvedDynamicPath`,
`cacheReason`, `pprState`, `workflowRunId`, `workflowStepId`, `sessionId`,
`proxyEvents`, `functionEvents`, `clientUserAgent`, `requestSearchParams`,
`requestReferer`, `microfrontendsResponseReason`, `microfrontendsMatchedPath`,
`microfrontendsDefaultAppDeploymentId`, `isPrefetchRequest`, `isVercelTrace`.
None of them is thrown away: `--json` prints the whole row under each entry's
`raw` key.

**`logs[]` item shape is `{level, message, messageTruncated}`. ASSUMPTION.**
Taken from the CLI's own mapping code, and **never observed populated**: neither
live project had produced an error or fatal log line in any window probed, so
every row seen carried `logs: []`. Parse it defensively and treat a missing field
as absent, exactly as this file already prescribes for Web Analytics rows. This
is the one shape in the surface resting on the CLI source rather than on
observation, and it is marked ASSUMPTION in `logs.py::_lines`.

INFERRED, not probed: that a request with no status recorded carries
`statusCode: 0` rather than omitting the field. `logs.py::_status` reads both a
missing field and a value of 0 or less as "no status", which is safe either way,
but the 0 spelling itself was reasoned from `statusCode=None` returning rows at
all rather than seen in a payload.

## `level` matches log lines, not responses

The single most important semantic on this surface.

`level=info` returned **zero** rows on a project that returns 50 rows
unfiltered, because every one of those rows carried `logs: []`. The filter
matches rows whose `logs[]` contains an entry of that level, not rows whose
response looked a certain way. So a request that returned `500` without printing
anything is invisible to `level=error`, and a request that returned `200` while
its handler logged a stack trace is invisible to `statusCode=5xx`.

Neither filter alone answers "what is broken". That is why the `errors` and
`error-summary` presets issue two calls, one for `statusCode=5xx` and one for
`level=error,fatal`, and merge them by request id.

## `statusCode` validation

Verbatim from the API:

```
400 Validation error: statusCode must contain only comma-separated integers,
status code classes like 4xx or 5xx, or "None" at "statusCode"
```

Accepted, verified: `500`, `401`, `500,502`, `5xx`, `4xx,5xx`, `40x`,
`401,4xx`, `None`. Rejected, verified: `>=500`, `xxx`. There are no comparison
operators here any more than in Web Analytics OData. `None` returns rows with no
status recorded: 28 of them in a 6 hour window on the test project.

`logs.validate_status_code` mirrors that rule client-side and quotes the API's
own sentence in its error, since that sentence is the authority. It is marginally
stricter: an item must be three characters, the first a digit 1 to 9 and the rest
digits or `x`, so a hypothetical two-digit status is refused locally. Every real
HTTP status is three digits, and every value the probes accepted still passes.

## Neither `level` nor `source` is validated server-side

`level=bogus` and `source=bogus` both return **`200` with zero rows**. A typo
therefore reads as "your site is fine", which is the most damaging failure
available to this tool. **Both vocabularies are validated client-side**, before
the request is built, the way `--granularity` and `--metric` already are.

### The display vocabulary and the filter vocabulary differ for `source`

Probed live on 2026-08-17. A row's `source` column can read
`serverless-middleware`, and that spelling matches nothing as a filter:

| Sent | Result |
| --- | --- |
| `source=edge-middleware` | 50 rows, **every one** carrying a `serverless-middleware` event |
| `source=serverless-middleware` | zero rows, HTTP 200 |

So the filter spelling for a middleware row is `edge-middleware`, and the
displayed spelling is `serverless-middleware`. This client records the mapping in
`logs.SOURCE_ALIASES` and accepts the displayed spelling, rewriting it before the
request is built, so a value copied out of this tool's own table works. A refused
`--source` value names the mapping too.

Do not assume the two vocabularies line up in general. Only this one pair has
been probed.

### Unverified: whether `source=serverless` narrows anything

In the same run, `source=serverless` returned a row set indistinguishable from
the unfiltered one, including rows whose only event source was `static`, while
`source=edge-middleware` filtered as expected. It has not been probed a second
time, so **neither conclusion is available**: do not present a
`source=serverless` result as a strict subset, and do not claim the filter is
broken. Read the `source` column of the rows that came back. This sits alongside
the other open questions in this file: it is recorded so nobody re-derives it,
not because it is settled.

### `search` is free text

`search=/api/me` filtered to that path, and `search=error` returned zero rows on
a project whose rows carried no log lines. The `field:value` syntax the CLI help
advertises does **not** work here in general: `search=path:/api/me` returned
mixed paths (no filtering at all), and `search=level:error` and
`search=method:POST` both returned zero. Document it as free text and nothing
more. That it also searches log text is Vercel's documented behaviour and is
unprobed here, because no test project had logged a line.

## Retention

From <https://vercel.com/docs/runtime-logs>, read 2026-08-17:

| Plan | Retention |
| --- | --- |
| Hobby | 1 hour |
| Pro | 1 day |
| Pro with Observability Plus | 30 days |
| Enterprise | 3 days |
| Enterprise with Observability Plus | 30 days |

With Observability Plus, up to 14 consecutive days may be viewed within a 30 day
window. Volume limits from the same page: each log output up to 256KB, up to 1MB
per request, and at most **256 log lines per request**.

Retention is far shorter than either analytics reporting window, and it drives
two behaviours. The logs presets default to a 1 hour window (`error-summary` to
6 hours) rather than the global 7 days, and an empty result over a window wider
than an hour prints the retention figures instead of implying health. Plan tier
is not discoverable from this API, so the note is printed rather than the query
being blocked.

## This client scrubs its own token out of log rows

This is the first surface in the tool that prints arbitrary remote text, so it is
the first that could break the promise that the access token never appears in any
output. A log line is whatever an application wrote, and applications do print
their own environment; if one logged the token this tool is holding, the API would
hand it straight back on a successful response.

An earlier draft of the design claimed the existing `scrub_credentials` already
covered that. **It did not**, and it was proved false during implementation by
driving the CLI with a response whose log message contained the token:
`scrub_credentials` ran only on strings heading into an `ApiError`, so a token
echoed back on a 200 printed verbatim.

What happens now: `logs.normalize` takes a `scrub` callable and applies it to
**every string in every row**, keys as well as values, before the row becomes a
`LogEntry`. `cli.py::_collect_logs` supplies it, bound to the prepared request's
own headers, because those headers are the authority on what the credential
actually is. That is the single boundary at which a payload becomes typed rows,
so it covers the otherwise unaltered copy kept in `LogEntry.raw` that `--json`
prints, and no rendering path can bypass it. The replacement is the same `<redacted>` used
everywhere else, and the bare credential is substring-matched only when it is at
least 8 characters, so a pathologically short value cannot turn every message
into confetti (the whole header value is always replaced regardless of length).

**The limit, stated precisely.** The tool can recognise exactly one secret: the
one it holds. Nothing can distinguish a user's own API key, connection string or
customer record from ordinary log text, so **no general redaction is possible or
claimed**. What the application logged is what a reader will see. That is why the
guidance in `SKILL.md` is to quote only the lines needed to answer the question
and never to forward log output to another service, and why `README.md` carries
the same warning where it introduces the feature rather than only in its security
section.

The covered half has a regression test:
`tests/test_security.py::test_a_response_echoing_the_token_never_reaches_any_logs_output`
drives the CLI with a **successful** response whose log message contains the
token and asserts the token appears in no output format, checking the table,
`--expand`, `--json`, `--csv` and `error-summary` separately, because each
renders a row differently. A 200 is the case that matters: an error path was
always scrubbed, and a success was not until this surface existed.

## The two alternatives that do not work

Recorded so this is never re-litigated.

**The documented runtime-logs endpoint is a stream that never answers.**
`GET /v1/projects/{projectId}/deployments/{deploymentId}/runtime-logs` is in the
OpenAPI document, tagged `logs`, declared `application/stream+json`. Live probes
against a READY production deployment never received **response headers** at all:
three attempts (plain, `format=lines`, `follow=0`) each timed out at 10 seconds,
and an earlier attempt at 20 seconds. It is a live tail, not a query, and a
request-and-response client cannot use it. There is therefore no follow mode
here, by construction rather than by omission.

**The metrics route is blocked by entitlement, not by shape.**
`POST /v2/observability/query` with `vercel.request.count` grouped by
`http_status` answers:

```
402 payment_required: Observability Plus is required to run this query for team
<team> and is available on Pro and Enterprise plans.
```

`GET /v2/observability/schema` returns 96 metrics for the same token, and
`vercel.request.count` does carry `http_status`, `error_code`, `route` and
`environment` dimensions, so the query is well formed and simply not paid for.
Request logs work on the same account **without** Observability Plus, which is
what makes them the right surface for an error question. Reaching for
`--metric vercel.request.count` instead answers 402 and no flag fixes it.

**Build logs do work, and are out of scope.**
`GET /v3/deployments/{idOrUrl}/events` returns a JSON array promptly
(`direction=backward`, `limit`, `since`, `until`, `statusCode`), carrying
`type: stdout|stderr|fatal|...` build events. Noted for a possible future change;
this surface is runtime request logs only.

## Still not pinned down

Three things are inferred rather than observed here, and one observation is
unresolved. The first two are marked ASSUMPTION in the code:

- **The `logs[]` item shape.** `{level, message, messageTruncated}` from the CLI
  source, never observed populated, so normalization skips anything unexpected
  rather than trusting it.
- **Project scoped tokens.** Reasoned from the `ownerId` requirement rather than
  observed, because only a team scoped token was available.
- **How "no status recorded" is spelled.** Read as `statusCode: 0` or an absent
  field, either of which this client treats as no status.
- **`source=serverless`.** One probe, two readings, no second probe. See above.
