# CLI and module contract

Authoritative interface for the `vercel-insights` skill. Tests, documentation and
examples are written against it. Read `docs/api-notes.md` first: it holds the
verified facts for all three APIs this contract is built on.

Target: Python 3.10+. Runtime dependency: `requests`. Everything else is stdlib.

## Package layout

The tool is a package at the repository root, not a single script. It covers
three different Vercel APIs with different request shapes, so one file no longer
earns its keep.

```
vercel_insights/
  __init__.py        VERSION, exceptions, sanitizers, shared constants
  __main__.py        entry point, path-robust so it runs from anywhere
  timerange.py       time parsing, range resolution, granularity translation
  odata.py           OData quoting, clause building, JSON dimension keys
  http.py            operation allowlist, request prep, redaction, retries
  webanalytics.py    Web Analytics request building and response normalization
  speedinsights.py   Speed Insights request building and response normalization
  logs.py            request logs: request building, vocabulary validation,
                     response normalization, paging, merge, local aggregation
  projects.py        project listing and the one project record lookup
  budgets.py         budget parsing and evaluation, and the exit code 3 constant
  render.py          table, JSON, CSV, overview, vitals and logs renderers
  presets.py         the preset table
  cli.py             argument parsing and main()
```

Both of these must work:

```bash
python3 -m vercel_insights --help              # from the repository root
python3 /abs/path/vercel_insights/__main__.py  # from anywhere
```

`__main__.py` puts the package's parent directory on `sys.path` before importing,
so the second form works without installation. `pip install -e .` additionally
provides a `vercel-insights` console script.

## Three surfaces, one CLI

| | Web Analytics | Speed Insights | Request logs |
| --- | --- | --- | --- |
| Endpoints | `GET /v1/query/web-analytics/{visits,events}/{count,aggregate}` | `POST /v2/observability/query`, `GET /v2/observability/schema[/{metricId}]` | `GET https://vercel.com/api/logs/request-logs` |
| Selected by | `--dataset visits\|events` | `--metric lcp\|inp\|cls\|fcp\|ttfb` | picking a logs preset; there is no flag for it |
| Dimension case | camelCase (`requestPath`) | snake_case (`request_path`) | camelCase query parameters, no OData at all |
| Time buckets | `by=day` | `granularity: 1d` | none; rows, not buckets |
| Metrics | `pageviews`/`visitors`, `count`/`visitors` | one value per metric, plus `*_count` data points | none; one row per request, carrying status, level, route and log lines |
| Scoped by | `projectId` (+ `teamId` or `slug`) | `scope.ownerId` and `scope.projectIds` | `projectId` and `ownerId`; `teamId` is not accepted in place of `ownerId`, and is never sent |

A preset determines which surface is used. `--dataset` and `--metric` are
mutually exclusive: passing both is a config error naming the conflict, and
neither means anything on a logs preset.

The request logs endpoint is the only one not on `api.vercel.com` and the only
one absent from Vercel's published OpenAPI document. Its ground truth is the
Vercel CLI source plus the live probes recorded in `docs/api-notes.md`, so it can
change without notice.

## Presets

| Preset | Surface | Query | Default limit |
| --- | --- | --- | --- |
| `overview` (default) | web analytics | 3 aggregate calls: `day`, `requestPath`, `referrerHostname` | 5 |
| `trend` | web analytics | aggregate by `day` | 100 |
| `top-pages` | web analytics | aggregate by `requestPath` | 10 |
| `top-routes` | web analytics | aggregate by `route` | 10 |
| `referrers` | web analytics | aggregate by `referrerHostname` | 10 |
| `countries` | web analytics | aggregate by `country` | 10 |
| `devices` | web analytics | aggregate by `deviceType` | 10 |
| `browsers` | web analytics | aggregate by `browserName` | 10 |
| `operating-systems` | web analytics | aggregate by `osName` | 10 |
| `campaigns` | web analytics | aggregate by `utmCampaign` | 10 |
| `events` | web analytics | aggregate by `eventName` (+ `eventData/<p>`) | 10 |
| `total` | web analytics | count | n/a |
| `vitals` | speed insights | 5 queries, P75 of each metric, ungrouped | n/a |
| `slowest-pages` | speed insights | P75 `lcp_ms` by `route`, `orderBy value`, `desc` | 10 |
| `fastest-pages` | speed insights | P75 `lcp_ms` by `route`, `orderBy value`, `asc` | 10 |
| `vitals-by-country` | speed insights | P75 of `--metric` by `country` | 10 |
| `vitals-by-device` | speed insights | P75 of `--metric` by `device_type` | 10 |
| `vitals-trend` | speed insights | P75 of `--metric` over time, `granularity` default `1d` | n/a |
| `data-points` | speed insights | `sum` of `<metric>_count` by `route` | 10 |
| `logs` | request logs | 1 call, one row per request, newest first | 50 rows |
| `errors` | request logs | 2 calls merged: `statusCode=5xx` and `level=error,fatal` | 50 rows |
| `error-summary` | request logs | the same 2 calls, tallied locally by status, route and message (3 tables) | 200 rows |

`vitals` is the Speed Insights counterpart of `overview`: it issues one query per
metric because the API returns one metric per request. Like `overview`, it
rejects `--group-by`, `--csv` and `--metric` with a message naming the preset to
use instead. `error-summary` is the logs counterpart, and rejects `--csv` for the
same reason: three tables do not fit one file.

`errors` issues two calls because `level` matches what a request logged while
`statusCode` matches what it answered, and neither question answers the other.
The results are merged and deduplicated by request id, the copy carrying more log
lines winning, then sorted newest first and truncated to the limit. An explicit
`--level` or `--status-code` collapses it to a single call with the user's filter,
which is the usual "an explicit flag overrides a preset value" rule.

### Per-preset window defaults

`--since` defaults to `7d`, except where a preset owns a default. Runtime log
retention is one hour on Hobby and one day on Pro, so a 7 day default on the logs
surface would report nothing and read as a healthy site.

| Preset | Default `--since` |
| --- | --- |
| `logs`, `errors` | `1h` |
| `error-summary` | `6h` |
| every other preset | `7d` |

An explicit `--since` always wins, including `--since ""`, which still reaches the
time parser and is still refused rather than being replaced by a default.

`--list-presets` prints the preset table and exits 0 without touching the network.

## Options

Configuration: `--token`/`VERCEL_TOKEN`, `--project`/`VERCEL_PROJECT_ID`,
`--team`/`VERCEL_TEAM_ID`, `--team-slug`/`VERCEL_TEAM_SLUG`, and
`--owner-id`/`VERCEL_OWNER_ID` or `VERCEL_ORG_ID`.

The owner is needed by the two scoped surfaces: Speed Insights sends it as
`scope.ownerId`, request logs as the `ownerId` parameter. A team is its own owner,
so `--team` covers it. With none of those set, the owner is read once per run from
`GET /v9/projects/{project}` as `accountId`. On the logs surface a missing owner is
the only trigger for that lookup, since the endpoint accepts a project name as
happily as an id; Speed Insights also resolves a name, because its scope matches
on `projectIds`.

### Speed Insights options

| Flag | Default | Notes |
| --- | --- | --- |
| `--metric lcp\|inp\|cls\|fcp\|ttfb` | preset | Selects the Speed Insights surface. |
| `--percentile 75\|90\|95\|99` | `75` | Sugar for `--aggregation p75` and friends. |
| `--aggregation NAME` | metric default | Raw passthrough, for example `sum`, `p90`, `max`. |
| `--order-by count\|value` | `count` | Grouped results only. |
| `--order asc\|desc` | `desc` | Grouped results only. |
| `--bucket-timezone IANA` | none | Aligns `1d`/`1mo` buckets only. |
| `--all` | off | Query every project in the team. Mutually exclusive with `--project`. |
| `--data-points` | off | Query the `*_count` metric instead of the value metric. |
| `--budget NAME=VALUE` | none | Repeatable. Exit 3 when a measured vital exceeds VALUE. A metric with no data does not fail. |

### Request logs options

Every flag here is meaningful only on a logs preset (`logs`, `errors`,
`error-summary`); on any other preset each one exits 2 naming the three presets
that accept it. Each value is validated locally, before a request exists, because
this API answers an unknown `level` or `source` with **HTTP 200 and zero rows**:
an unchecked typo would read as "nothing is broken".

| Flag | Default | Validation, and the wire parameter it becomes |
| --- | --- | --- |
| `--level LEVEL` | none | `error`, `warning`, `info`, `fatal`, comma separated, any case. Anything else is a config error naming all four. Becomes `level`. Matches **application log lines, not responses**. |
| `--status-code CODE` | none | Comma separated. Each item is either three characters whose first is a digit 1 to 9 and whose rest are digits or `x` (`500`, `5xx`, `40x`), or the literal `None` for a request with no status recorded. A comparison such as `>=500` is a config error quoting the API's own rule. Becomes `statusCode`. |
| `--source SOURCE` | none | `serverless`, `edge-function`, `edge-middleware`, `static`, comma separated. `serverless-middleware` is accepted as a display alias and rewritten to `edge-middleware`, which is the spelling that matches those rows. Anything else is a config error naming the vocabulary and the alias. Becomes `source`. |
| `--method METHOD` | none | Upper-cased for the wire. Becomes `requestMethod`. A method outside the standard set (`GET`, `HEAD`, `POST`, `PUT`, `PATCH`, `DELETE`, `OPTIONS`, `TRACE`, `CONNECT`) is **warned about on stderr and still sent**, because a custom method is legal HTTP: refusing would remove capability, and saying nothing would leave the same zero-rows trap `--level` and `--source` are validated against. |
| `--search TEXT` | none | Free text and nothing more: not a query syntax, so do not expect `status:500` to filter by status. Probed forms either returned unfiltered rows or nothing. Becomes `search`. |
| `--request-id ID` | none | One request. Becomes `requestId`. |
| `--branch NAME` | none | Becomes `branch`. |
| `--deployment ID` | none | A `dpl_` id, passed through with no lookup. Becomes `deploymentId`. |
| `--expand` | off | Rendering only, no wire effect: prints every full log line under its row instead of truncating the message to its column. |

On this surface `--path`, `--route` and `--environment` become the query
parameters `requestPath`, `route` and `environment` rather than OData clauses, and
`--path` and `--route` are **exact match**. `--search` is the substring tool here.

`--limit` counts **rows**, not groups: 1 to 200, default 50 (`error-summary`
defaults to 200). The API pages 50 rows at a time and ignores a `limit` of its
own, so the budget is enforced client-side and paging stops after 4 pages. Nothing
rolls up into an `Others` row here; rows past the limit are left out, and the
footer says so.

### Shared options

`--group-by` (repeatable), `--granularity`, `--since`, `--until`, `--limit`,
`--filter` (repeatable), `--json`, `--csv`, `--dry-run`, `--timeout`,
`--max-retries`, `--no-color`, `--verbose`, `--version`, `--list-presets`.

Filter shorthands compile to the correct dimension spelling for the active
surface: `--path` becomes `requestPath eq '...'` on Web Analytics and
`request_path eq '...'` on Speed Insights. Shorthands valid on all three:
`--path`, `--route`, `--environment`. `--country` and `--device` work on the two
analytics surfaces. Shorthands that exist only on Web Analytics (`--browser`,
`--os`, `--referrer`, the UTM flags, `--event-name`, `--flag`,
`--event-property`) are a config error when another surface is active, and the
message names the reason and where the flag does work.

### Granularity

`--granularity` accepts both vocabularies and translates per surface:

| Accepted input | Web Analytics | Speed Insights |
| --- | --- | --- |
| `hour`, `1h` | `hour` | `1h` |
| `day`, `1d` | `day` | `1d` |
| `week` | `week` | config error, no equivalent |
| `month`, `1mo` | `month` | `1mo` |
| `year` | `year` | config error, no equivalent |

An unsupported combination is rejected before any network call, and the error
names both the granularity and the surface. On a logs preset **any** granularity
is a config error, because that API answers with rows rather than time buckets;
the `--group-by` refusal there points at `error-summary`, which groups.

## Validation rules, all enforced before any network call

Rules 1 to 13 from the previous contract still apply (missing project, missing
token unless `--dry-run`, `--team` with `--team-slug`, more than 2 grouping
dimensions, more than one time granularity, unknown dimension, events-only
dimension on visits, `--limit` out of bounds, `--environment preview` on a count
query, `--json` with `--csv`, `--since` not before `--until`, reporting-window
warning, `--flag` without `=`). Added:

14. `--dataset` together with `--metric`: config error naming the conflict.
15. A Web-Analytics-only shorthand or grouping dimension used on the Speed Insights surface, and the reverse.
16. `--granularity week` or `year` on Speed Insights: config error listing what that surface supports.
17. `--all` together with `--project`: config error.
18. `--percentile` outside 75, 90, 95, 99: config error listing the four.
19. `--metric` with an unknown name: config error listing the five, with a did-you-mean suggestion.
20. `--order-by` or `--order` without a grouping: config error explaining they apply to grouped results only.
21. `--bucket-timezone` with a sub-daily granularity: warning on stderr, not an error, since the API ignores it there.
22. Any option used on a surface it means nothing on: config error. One table in `cli.py` (`SURFACE_OPTIONS`) maps each option to the surfaces it is meaningful on, and the check runs in every direction rather than pairwise. Every refusal names the flag, the value passed, the surface the preset queries, why the flag means nothing there, and the presets where it does work. This covers `--budget`, which is Speed Insights only and was previously accepted and ignored elsewhere.

Added with the request logs surface:

23. Any logs-only option (`--level`, `--status-code`, `--source`, `--method`, `--search`, `--request-id`, `--branch`, `--deployment`, `--expand`) on a Web Analytics or Speed Insights preset: config error naming `logs`, `errors` and `error-summary`.
24. `--group-by` or `--granularity` on a logs preset: config error. Logs are rows, not buckets; the `--group-by` message names `error-summary`.
25. `--filter` on a logs preset: config error. That API takes no OData, and the message lists the flags that do filter there.
26. `--level` or `--source` with a value outside its vocabulary: config error naming every accepted value, and, for `--source`, the `serverless-middleware` to `edge-middleware` alias. Checked locally because the API answers 200 with zero rows.
27. `--status-code` that is neither `Nxx`-shaped nor `None`: config error quoting the API's own validation sentence.
28. `--limit` outside 1 to 200 on a logs preset: config error saying that the limit counts rows there, that the API pages 50 at a time, and that this client stops after 4 pages.
29. `--csv` with `error-summary`: config error naming `errors --csv`, which is one row per request.
30. `--team-slug` alone on a logs preset: config error. That endpoint needs the account id, and a slug is a name; the same rule already applied to Speed Insights.
31. `--method` outside the standard HTTP set: **warning on stderr, not an error**, and the value is still sent. A custom method is legal HTTP, so refusing would remove capability the API may have; silence is what is not acceptable, since an unrecorded method comes back as 200 with zero rows. The warning names the standard set and that outcome.

Every message names the offending value and the fix. No traceback reaches the user.

## Exit codes

`0` success including an empty result, `1` API or network failure, `2`
configuration or usage error, `3` a `--budget` was exceeded, `130` interrupted.

Exit 3 is exclusive to `--budget`, which is a Speed Insights option, so no other
surface can produce it. An empty result is a success everywhere, request logs
included: "nothing failed in this window" is an answer, and exiting non-zero for
it would fail a caller's pipeline over good news.

## Security invariants

Restated for three surfaces. These are testable properties. The table below is
where `tests/test_security.py` gets its own copy of the allowlist: it transcribes
these entries by hand rather than reading them back from the code, because a test
that iterates the table it is checking cannot notice a seventh entry appearing in
it. So an operation added to `http.py` without updating that transcription fails
the suite, and updating the transcription without updating this table leaves the
two out of step, which is the thing to avoid.

1. **Operation allowlist.** `http.py` holds one module-level table mapping each allowed operation to a fixed `(method, url)` pair. There are exactly **six** entries:

   | Operation | Method | URL |
   | --- | --- | --- |
   | `web_analytics` | GET | `https://api.vercel.com/v1/query/web-analytics/{dataset}/{endpoint}` |
   | `observability_query` | POST | `https://api.vercel.com/v2/observability/query` |
   | `observability_schema` | GET | `https://api.vercel.com/v2/observability/schema` |
   | `project` | GET | `https://api.vercel.com/v9/projects/{project}` |
   | `projects` | GET | `https://api.vercel.com/v10/projects` |
   | `request_logs` | GET | `https://vercel.com/api/logs/request-logs` |

   The dispatcher takes an operation key, never a method or a host. No user input can select, extend or override an entry, and only `{...}` placeholders are substituted, each with a validated value.
2. **Two hosts, and only two.** Five entries are on `api.vercel.com`; `request_logs` is on the dashboard host `vercel.com`, because that is where Vercel serves historical request logs. The host set is asserted explicitly, so a third host is a test failure rather than a silent widening.
3. The only HTTP calls in the package are `session.get` and `session.post`, each appearing exactly once, both inside that dispatcher. Neither follows redirects: `allow_redirects=False`, and a 3xx becomes an error naming the location it refused, so the allowlist binds every hop rather than only the first.
4. The token appears only in the `Authorization` header: never in a URL, query parameter, request body, log line, exception message, `__repr__`, or formatter output. It is validated at config time as header-safe and scrubbed from every error path.
5. **On the logs surface the scrub also runs on responses.** Log rows are free text an application wrote, so a response can echo the very token that fetched it. `logs.normalize` applies the credential scrub to every string in every row, keys included, before the row becomes a `LogEntry`, which covers the verbatim copy `--json` prints under `raw`. It rewrites the one secret this tool holds and claims nothing about the user's own: no code can tell an API key from ordinary log text.
6. `--dry-run` constructs no session and sends nothing, and succeeds with no token present. For a POST operation it prints the full JSON body it would have sent.
7. `redact_headers` is applied everywhere headers are rendered.
8. Every string from a response passes a sanitizer at the one normalization boundary: `sanitize_label` for a field, `sanitize_message` for a log message, which keeps newlines because a stack trace's line structure carries meaning. Nothing downstream re-sanitizes and nothing downstream may skip it.
9. No `eval`, no `exec`, no `subprocess`, no filesystem writes.

The project's public claim is "read-only against a six-endpoint allowlist", not
"GET-only". Documentation must state why one endpoint is POST: Vercel exposes no
GET equivalent for observability queries, and a query body is still a read. It
must also state that `request_logs` is absent from Vercel's published OpenAPI
document, since a reader cannot verify that one against a schema.

## Speed Insights rendering

`Result` gains what the renderer needs to interpret a value: the metric id, its
unit (`ms` or a unitless score), and the number of data points when available.

- Millisecond values render as milliseconds under 1000 and as seconds with one decimal above, for example `1.4 s`.
- CLS renders as a bare number with three decimals.
- The `vitals` preset prints one row per metric: metric name, P75 value, Vercel's published target, and whether the value meets it.
- Targets come from `docs/api-notes.md`: LCP 2500 ms, INP 200 ms, CLS 0.1, FCP 1800 ms, TTFB 800 ms. Render a two-tier verdict, meets target or over target. **Do not render a three-tier good / needs improvement / poor scale**: Vercel publishes only the good target, and the dashboard's three colour bands apply to derived 0-100 scores, not to raw values.
- Lower is better for all five metrics. Say so in the output legend so a reader does not misread an ordering.
- When a data point count is available, show it, and note that a percentile over few data points is not comparable to one over many.
- Real Experience Score is not queryable. If a user asks for it by name, fail with a config error that says so and points at the dashboard, rather than silently substituting another metric.

## Request logs rendering

`logs` and `errors` print one row per request, newest first, with the columns
`time`, `level`, `status`, `method`, `route`, `source`, `message`.

- `time` is `HH:MM:SS` UTC for a window of 24 hours or less and `MM-DD HH:MM:SS` for a longer one, so a row is never ambiguous about which day it belongs to. Exactly 24 hours takes the short form. `(no time)` when the row carried no timestamp.
- `level` is the worst level among the request's own log lines (`fatal` over `error` over `warning` over `info`), or `-` when it logged nothing.
- `status` shows `(none)` when no status was recorded, which is what `--status-code None` selects.
- `route` falls back to the request path, then to `(unknown)`.
- `message` is the worst line's text, truncated to its column. An error that logged nothing prints `(no log line: the response failed)`, because an empty cell there would read as a rendering fault rather than as the fact that nothing was printed; an ordinary row that logged nothing leaves the cell empty.
- `--expand` prints every line of the request in full underneath its row, marks any line Vercel itself truncated, and names the request id.
- The most-affected route line is printed only when one route outnumbers the next. A tie has no winner, so printing the row that happened to sort first as "most affected" would report the tiebreak as a finding, and a single route leads nothing.
- Every sentence beyond the table is composed in `logs.py` and carried on the report as data, so `render.py` states no API fact of its own.

`error-summary` prints the same title, range and filter lines and then three
tables over the same merged rows: by status with a share column and a total, by
route with the worst status and a first and last seen, and by exact message.
Messages are grouped by **exact text**, never clustered by a guessed pattern,
because merging two different bugs into one row is a worse answer than two rows. `(no log line)` is its own group. A request that
counts as an error only because it logged an error or fatal line appears under its
real status, so a `200` row in a table of errors is not a bug, and a footer line
says how many rows qualify that way.

The honesty rules are part of the contract, not presentation:

1. **An empty result over a window wider than one hour prints the retention figures** (1 hour Hobby, 1 day Pro, 3 days Enterprise, 30 days with Observability Plus) and says an empty answer may mean the logs aged out rather than that nothing failed. Below an hour there is nothing to warn about, and warning every time would train the reader to skip it.
2. **4xx is excluded from `errors` deliberately**: a 401 on `/api/me` is the application working. `--status-code 4xx` asks for them by name.
3. **`--level` only sees requests that logged**, stated in `--help`, in `SKILL.md` and in the `errors` header line.
4. **Truncation is always visible, and a truncated report describes its sample.** When more rows matched than were shown, the count sentence says so of itself ("showing the most recent N of more that matched in the window") rather than counting the sample as if it were the window, a following line repeats that more matched and says what to do, and the most-affected route line is scoped to the rows shown. When a two-call `errors` run truncated, it adds that the result is the most recent N of each kind rather than a global top N. This holds in every format: `--json` carries the notes in the document and `--csv` prints them to stderr, because a consumer piping CSV is precisely the one who cannot tell otherwise.
5. **The header line describes the query that actually ran.** The `errors` preset prints what counted as an error above the table (a 5xx response, a crashed function, or a request that logged an error or fatal line) while it applied that definition itself. An explicit `--level` or `--status-code` collapses it to a single call carrying the user's filter, so the rows become whatever that filter matched: the header then names that filter and says it replaced the definition rather than narrowing it, and the footer counts "requests" rather than "errors", because `--status-code 4xx` returns 401s and a 401 is not an error by any definition this tool holds. `error-summary` prints no header note at all, because the note is carried on the report but only the row renderer prints it; it prints the filter line and its `logged_only` footer instead.
6. **No sentence outruns its own table.** `logged_only` counts a row only when it is a non-5xx that did not crash *and* carries an error or fatal log line, all three checked, so the "count as errors only because they logged an error or fatal line" footer can never appear beside a message table whose every group reads `(no log line)`.

`--json` emits `{"query", "entries", "truncated", "pagesFetched", "notes"}`, each
entry carrying the tabulated columns plus the whole original row under `raw`, so
nothing the API sent is discarded. `--csv` emits one row per request with the
columns `time`, `level`, `status`, `method`, `route`, `path`, `source`,
`requestId`, `message`; a message containing a newline stays in one cell because
`csv.writer` quotes it. **A `--csv` run prints the report's notes to stderr**,
one per line and prefixed `note: `, so the data stream stays machine readable
while truncation and the retention caveat stay visible: `--json` carries them
inside the document, and CSV has nowhere to put them.

## Module surface

Exceptions, sanitizers and constants live in `__init__.py`: `ConfigError`,
`ApiError`, `RateLimitError`, `sanitize_label`, `sanitize_message`, `VERSION`,
`BASE_URL`, `LOGS_BASE_URL`, `OTHERS_LABEL`.

| Module | Public surface |
| --- | --- |
| `timerange` | `parse_time_value`, `resolve_range`, `to_api_timestamp`, `to_unix_ms`, `normalize_granularity(value, surface)`, `WEB_ANALYTICS`, `SPEED_INSIGHTS`, `LOGS`, `SURFACES`, `SURFACE_LABELS` |
| `odata` | `quote_odata`, `build_clause`, `combine_filters`, `json_dimension`, `validate_key_segments` |
| `http` | `OPERATIONS`, `PreparedRequest`, `redact_headers`, `format_dry_run`, `retry_delay`, `execute`, `scrub_credentials` |
| `webanalytics` | `VISIT_DIMENSIONS`, `EVENT_DIMENSIONS`, `select_endpoint`, `validate_group_by`, `build_request`, `normalize` |
| `speedinsights` | `METRICS`, `TARGETS`, `SPEED_DIMENSIONS`, `validate_metric`, `build_request`, `normalize` |
| `logs` | `LEVELS`, `SOURCES`, `SOURCE_ALIASES`, `SOURCE_ALIAS_NOTE`, `METHODS`, `FILTER_PARAMS`, `PAGE_SIZE`, `MAX_PAGES`, `MIN_LIMIT`, `MAX_LIMIT`, `DEFAULT_LIMIT`, `validate_levels`, `validate_sources`, `validate_status_code`, `validate_limit`, `normalize_method`, `method_warning`, `build_request`, `normalize`, `collect`, `merge`, `error_filter_sets`, `summarize`, `build_report`, `RETENTION_NOTE`, `ERROR_DEFINITION` |
| `projects` | `looks_like_project_id`, `build_list_request`, `build_one_request`, `extract_projects`, `format_projects`, `resolve_project_id`, `owner_from_project` |
| `budgets` | `BUDGET_EXCEEDED`, `Budget`, `parse_budgets`, `evaluate`, `any_failed` |
| `render` | `Row`, `Result`, `LogLine`, `LogEntry`, `RouteTally`, `MessageTally`, `LogSummary`, `LogReport`, `ERROR_LEVELS`, `format_table`, `format_json`, `format_csv`, `render_overview`, `render_vitals`, `render_logs`, `render_error_summary`, `format_logs_json`, `format_logs_csv`, `verdict` |
| `presets` | `PRESETS`, `Preset`, `format_presets` |
| `cli` | `build_parser`, `main` |

`logs.py` performs no I/O: `collect` takes an injected page fetcher, which is
what lets the paging loop, the 4 page cap and the merge be tested with no HTTP at
all. The log containers live in `render.py` beside `Row` and `Result` because
`render.py` must not import a surface module; `logs.py` builds them, the way
`webanalytics.py` builds `Result`.

`execute` keeps its injected `session`, `sleep` and `jitter` callables so retry
behavior stays deterministic under test. `retry_delay` stays pure. Retryable
statuses now include **408**, which the observability API documents and Web
Analytics does not.

## Output expectations

Unchanged for Web Analytics: grouped tables carry one column per grouped
dimension, a share-of-total percent for the primary metric, a totals row, and a
labelled `Others` bucket with its explanatory note. Empty results print one
explanatory line and exit 0. JSON carries `query`, `range`, `rows`, `totals` and
the untouched payload under `raw`. CSV is written with `csv.writer`.

Speed Insights output follows the same conventions, with the value column
formatted per its unit and, for `vitals`, the target and verdict columns
described above.

Request logs share the title and range lines and the "one explanatory line, exit
0" rule for an empty answer, and otherwise follow *Request logs rendering* above:
rows rather than groups, no totals row on a table whose columns do not add up, and
every caveat printed rather than implied.
