# Example output

Every fenced block below is **captured output from the real code**, not written
by hand. Almost all of the data behind it is synthetic and anonymised: one
fictional docs and marketing site, one dataset, so the numbers agree across
sections.

Three blocks are the exception, and say so where they appear: the first three in
[Errors: request logs](#errors-request-logs) were captured against a **live
Vercel account and then redacted**, which is not the same as synthetic. The
shape, the columns, the counts and every note in them are exactly what the tool
printed. The project id, the route names and the timestamps were replaced
afterwards with fictional equivalents of the same shape, because a real
account's ids and internal route naming do not belong in a published file. That
project happened to have no errors at all: the third block asks for 4xx
responses by name, which is why it has rows to show. The rest of that section is
stub-driven like everything else, with data invented to show what a failing
project looks like.

**Read your own output before you share it.** The blocks here are safe because
they were redacted; a real run is not. Request logs carry your project id, your
route names, your deployment ids and whatever your application chose to log,
which can include secrets or personal data. Quote the part that answers the
question, leave out the rest, and do not forward it to a service that did not
already have access to it.

`vercel-insights` is shorthand for `python3 -m vercel_insights`.

## Getting started

### Which projects do I have?

One Vercel account holds many projects and every query names exactly one, so this is usually the first command to run. Pass either the name or the project id to `--project`.

```console
$ vercel-insights --list-projects
Projects

name            project id                    traffic  speed
--------------  ----------------------------  -------  -----
acme-docs       prj_9RkQm2vT7xLpN4dWbYcF3sJz  data     data
acme-marketing  prj_2LbGf5yUvA8qEr1oPtNm      data     empty
acme-internal   prj_7WsDj4kXzC9nBv6hRlYq      off      off

traffic and speed are Web Analytics and Speed Insights: 'data' means collected, 'empty' means enabled but nothing yet, 'off' means not enabled.
Query one with --project, using either the name or the project id.
[exit code 0]
```

### Forgetting to name a project

The error answers the question behind it rather than only naming a missing flag.

```console
$ vercel-insights vitals --since 2026-08-08 --until 2026-08-15
error: no project configured; pass --project with a project id or name, or set VERCEL_PROJECT_ID in the environment, or pass --all to query every project in the team

This account has:

name            project id                    traffic  speed
--------------  ----------------------------  -------  -----
acme-docs       prj_9RkQm2vT7xLpN4dWbYcF3sJz  data     data
acme-marketing  prj_2LbGf5yUvA8qEr1oPtNm      data     empty
acme-internal   prj_7WsDj4kXzC9nBv6hRlYq      off      off

traffic and speed are Web Analytics and Speed Insights: 'data' means collected, 'empty' means enabled but nothing yet, 'off' means not enabled.
Query one with --project, using either the name or the project id.
[exit code 2]
```

## Traffic: Web Analytics

### The 7 day overview, which is the default

Bare `vercel-insights` runs this.

```console
$ vercel-insights --since 7d
Vercel Web Analytics: prj_9RkQm2vT7xLpN4dWbYcF3sJz
Range: 2026-08-09T05:22:01Z to 2026-08-16T05:22:01Z (UTC)

  pageviews  48,072
  visitors   32,280
  visitors is a sum of the buckets below, so someone who came on two days counts twice;
  run the total preset for distinct visitors over the window

By day
  2026-08-08  6,120  ██████████████████
  2026-08-09  4,980  ██████████████
  2026-08-10  7,840  ███████████████████████
  2026-08-11  8,310  ████████████████████████
  2026-08-12  7,905  ███████████████████████
  2026-08-13  7,402  █████████████████████
  2026-08-14  5,515  ████████████████

Top pages (top 5)
requestPath            pageviews  visitors  % pageviews
---------------------  ---------  --------  -----------
/                         18,420    11,930        38.3%
/docs/getting-started      9,310     6,845        19.4%
/pricing                   7,204     5,588        15.0%
/blog/shipping-faster      4,126     3,390         8.6%
/changelog                 2,870     2,115         6.0%
Others                     6,142     4,102        12.8%
---------------------  ---------  --------  -----------
TOTAL                     48,072    33,970       100.0%

Others is not a real value: it is every group beyond --limit 5, collapsed by the API into one bucket.

Top referrers (top 5)
referrerHostname      pageviews  visitors  % pageviews
--------------------  ---------  --------  -----------
(none)                   21,044    13,980        43.8%
google.com               14,310     9,720        29.8%
news.ycombinator.com      6,890     6,012        14.3%
github.com                3,402     2,560         7.1%
x.com                     2,426     1,798         5.0%
--------------------  ---------  --------  -----------
TOTAL                    48,072    34,070       100.0%
[exit code 0]
```

### Top pages

```console
$ vercel-insights top-pages --since 2026-08-08 --until 2026-08-15
Vercel Web Analytics: prj_9RkQm2vT7xLpN4dWbYcF3sJz (top-pages)
Range: 2026-08-08T00:00:00Z to 2026-08-15T00:00:00Z (UTC)

requestPath            pageviews  visitors  % pageviews
---------------------  ---------  --------  -----------
/                         18,420    11,930        38.3%
/docs/getting-started      9,310     6,845        19.4%
/pricing                   7,204     5,588        15.0%
/blog/shipping-faster      4,126     3,390         8.6%
/changelog                 2,870     2,115         6.0%
Others                     6,142     4,102        12.8%
---------------------  ---------  --------  -----------
TOTAL                     48,072    33,970       100.0%

Others is not a real value: it is every group beyond --limit 10, collapsed by the API into one bucket.
[exit code 0]
```

### Top framework routes

```console
$ vercel-insights top-routes --since 2026-08-08 --until 2026-08-15
Vercel Web Analytics: prj_9RkQm2vT7xLpN4dWbYcF3sJz (top-routes)
Range: 2026-08-08T00:00:00Z to 2026-08-15T00:00:00Z (UTC)

route         pageviews  visitors  % pageviews
------------  ---------  --------  -----------
/                18,420    11,930        46.3%
/docs/[slug]     14,980     9,860        37.6%
/blog/[slug]      6,415     5,104        16.1%
------------  ---------  --------  -----------
TOTAL            39,815    26,894       100.0%
[exit code 0]
```

### Where the traffic came from

```console
$ vercel-insights referrers --since 2026-08-08 --until 2026-08-15
Vercel Web Analytics: prj_9RkQm2vT7xLpN4dWbYcF3sJz (referrers)
Range: 2026-08-08T00:00:00Z to 2026-08-15T00:00:00Z (UTC)

referrerHostname      pageviews  visitors  % pageviews
--------------------  ---------  --------  -----------
(none)                   21,044    13,980        43.8%
google.com               14,310     9,720        29.8%
news.ycombinator.com      6,890     6,012        14.3%
github.com                3,402     2,560         7.1%
x.com                     2,426     1,798         5.0%
--------------------  ---------  --------  -----------
TOTAL                    48,072    34,070       100.0%
[exit code 0]
```

### Traffic by country

```console
$ vercel-insights countries --since 2026-08-08 --until 2026-08-15
Vercel Web Analytics: prj_9RkQm2vT7xLpN4dWbYcF3sJz (countries)
Range: 2026-08-08T00:00:00Z to 2026-08-15T00:00:00Z (UTC)

country  pageviews  visitors  % pageviews
-------  ---------  --------  -----------
US          19,840    12,905        47.0%
DE           8,120     5,644        19.3%
GB           6,310     4,288        15.0%
IN           5,470     3,902        13.0%
BR           2,432     1,801         5.8%
-------  ---------  --------  -----------
TOTAL       42,172    28,540       100.0%
[exit code 0]
```

### Mobile against desktop

```console
$ vercel-insights devices --since 2026-08-08 --until 2026-08-15
Vercel Web Analytics: prj_9RkQm2vT7xLpN4dWbYcF3sJz (devices)
Range: 2026-08-08T00:00:00Z to 2026-08-15T00:00:00Z (UTC)

deviceType  pageviews  visitors  % pageviews
----------  ---------  --------  -----------
desktop        29,140    18,770        60.6%
mobile         17,402    11,960        36.2%
tablet          1,530     1,140         3.2%
----------  ---------  --------  -----------
TOTAL          48,072    31,870       100.0%
[exit code 0]
```

### Browsers

```console
$ vercel-insights browsers --since 2026-08-08 --until 2026-08-15
Vercel Web Analytics: prj_9RkQm2vT7xLpN4dWbYcF3sJz (browsers)
Range: 2026-08-08T00:00:00Z to 2026-08-15T00:00:00Z (UTC)

browserName  pageviews  visitors  % pageviews
-----------  ---------  --------  -----------
Chrome          26,310    17,020        54.7%
Safari          13,480     9,140        28.0%
Firefox          5,220     3,690        10.9%
Edge             3,062     2,020         6.4%
-----------  ---------  --------  -----------
TOTAL           48,072    31,870       100.0%
[exit code 0]
```

### Operating systems

```console
$ vercel-insights operating-systems --since 2026-08-08 --until 2026-08-15
Vercel Web Analytics: prj_9RkQm2vT7xLpN4dWbYcF3sJz (operating-systems)
Range: 2026-08-08T00:00:00Z to 2026-08-15T00:00:00Z (UTC)

osName   pageviews  visitors  % pageviews
-------  ---------  --------  -----------
macOS       19,840    12,610        41.3%
Windows     14,120     9,440        29.4%
iOS          8,930     6,210        18.6%
Android      5,182     3,610        10.8%
-------  ---------  --------  -----------
TOTAL       48,072    31,870       100.0%
[exit code 0]
```

### UTM campaigns

```console
$ vercel-insights campaigns --since 2026-08-08 --until 2026-08-15
Vercel Web Analytics: prj_9RkQm2vT7xLpN4dWbYcF3sJz (campaigns)
Range: 2026-08-08T00:00:00Z to 2026-08-15T00:00:00Z (UTC)

utmCampaign        pageviews  visitors  % pageviews
-----------------  ---------  --------  -----------
launch-week            4,820     3,610        59.0%
newsletter-august      2,140     1,780        26.2%
product-hunt           1,206     1,094        14.8%
-----------------  ---------  --------  -----------
TOTAL                  8,166     6,484       100.0%
[exit code 0]
```

### Custom events

```console
$ vercel-insights events --since 2026-08-08 --until 2026-08-15
Vercel Web Analytics: prj_9RkQm2vT7xLpN4dWbYcF3sJz (events)
Range: 2026-08-08T00:00:00Z to 2026-08-15T00:00:00Z (UTC)

eventName      count  visitors  % count
-------------  -----  --------  -------
signup           412       388    54.6%
subscribe        268       251    35.5%
contact_sales     74        71     9.8%
-------------  -----  --------  -------
TOTAL            754       710   100.0%
[exit code 0]
```

### Which plan did signups choose

```console
$ vercel-insights events --event-property plan --since 2026-08-08 --until 2026-08-15
Vercel Web Analytics: prj_9RkQm2vT7xLpN4dWbYcF3sJz (events)
Range: 2026-08-08T00:00:00Z to 2026-08-15T00:00:00Z (UTC)

eventName  eventData/plan  count  visitors  % count
---------  --------------  -----  --------  -------
signup     free              291       274    70.6%
signup     pro                98        92    23.8%
signup     enterprise         23        22     5.6%
---------  --------------  -----  --------  -------
TOTAL                        412       388   100.0%
[exit code 0]
```

### A daily trend

```console
$ vercel-insights trend --since 2026-08-08 --until 2026-08-15
Vercel Web Analytics: prj_9RkQm2vT7xLpN4dWbYcF3sJz (trend)
Range: 2026-08-08T00:00:00Z to 2026-08-15T00:00:00Z (UTC)

day         pageviews  visitors  % pageviews
----------  ---------  --------  -----------
2026-08-08      6,120     4,180        12.7%
2026-08-09      4,980     3,410        10.4%
2026-08-10      7,840     5,220        16.3%
2026-08-11      8,310     5,560        17.3%
2026-08-12      7,905     5,240        16.4%
2026-08-13      7,402     4,980        15.4%
2026-08-14      5,515     3,690        11.5%
----------  ---------  --------  -----------
TOTAL          48,072    32,280       100.0%
[exit code 0]
```

### One ungrouped total

```console
$ vercel-insights total --since 2026-08-08 --until 2026-08-15
Vercel Web Analytics: prj_9RkQm2vT7xLpN4dWbYcF3sJz (total)
Range: 2026-08-08T00:00:00Z to 2026-08-15T00:00:00Z (UTC)

  pageviews  148,072
  visitors    61,904
[exit code 0]
```

## Speed: Core Web Vitals

### All five vitals against Vercel's published targets

The value is the aggregate for the whole window, taken from the server's own summary. It is not derived from the buckets: a percentile does not average, so the P75 of 168 hourly P75s is not the P75 of the week.

```console
$ vercel-insights vitals --since 2026-08-08 --until 2026-08-15
Vercel Speed Insights: prj_9RkQm2vT7xLpN4dWbYcF3sJz
Range: 2026-08-08T00:00:00Z to 2026-08-15T00:00:00Z (UTC)

metric                        p75  target  verdict
-------------------------  ------  ------  ------------
Largest Contentful Paint    2.9 s   2.5 s  over target
Interaction to Next Paint  184 ms  200 ms  meets target
Cumulative Layout Shift     0.128   0.100  over target
First Contentful Paint      1.6 s   1.8 s  meets target
Time to First Byte         412 ms  800 ms  meets target

Lower is better for all five metrics.
The target is Vercel's published 'good' threshold, so the verdict is two tier: meets target or over target.
Real Experience Score is not queryable through this API; read it on the Speed Insights dashboard.
[exit code 0]
```

### The slowest routes

```console
$ vercel-insights slowest-pages --since 2026-08-08 --until 2026-08-15
Vercel Speed Insights: prj_9RkQm2vT7xLpN4dWbYcF3sJz (slowest-pages, p75)
Range: 2026-08-08T00:00:00Z to 2026-08-15T00:00:00Z (UTC)

route         p75_lcp
------------  -------
/blog/[slug]    5.0 s
/docs/[slug]    3.2 s
/pricing        2.7 s
/               2.2 s

Metric: vercel.speed_insights.lcp_ms (Largest Contentful Paint)
Target: 2.5 s or less
Lower is better for all five metrics.
The target is Vercel's published 'good' threshold, so the verdict is two tier: meets target or over target.
[exit code 0]
```

### The fastest routes

```console
$ vercel-insights fastest-pages --since 2026-08-08 --until 2026-08-15
Vercel Speed Insights: prj_9RkQm2vT7xLpN4dWbYcF3sJz (fastest-pages, p75)
Range: 2026-08-08T00:00:00Z to 2026-08-15T00:00:00Z (UTC)

route         p75_lcp
------------  -------
/blog/[slug]    5.0 s
/docs/[slug]    3.2 s
/pricing        2.7 s
/               2.2 s

Metric: vercel.speed_insights.lcp_ms (Largest Contentful Paint)
Target: 2.5 s or less
Lower is better for all five metrics.
The target is Vercel's published 'good' threshold, so the verdict is two tier: meets target or over target.
[exit code 0]
```

### Speed by country

```console
$ vercel-insights vitals-by-country --since 2026-08-08 --until 2026-08-15
Vercel Speed Insights: prj_9RkQm2vT7xLpN4dWbYcF3sJz (vitals-by-country, p75)
Range: 2026-08-08T00:00:00Z to 2026-08-15T00:00:00Z (UTC)

country  p75_lcp
-------  -------
BR         5.4 s
IN         5.0 s
DE         2.8 s
GB         2.6 s
US         2.2 s

Metric: vercel.speed_insights.lcp_ms (Largest Contentful Paint)
Target: 2.5 s or less
Lower is better for all five metrics.
The target is Vercel's published 'good' threshold, so the verdict is two tier: meets target or over target.
[exit code 0]
```

### Speed by device

The usual explanation for a poor field score.

```console
$ vercel-insights vitals-by-device --since 2026-08-08 --until 2026-08-15
Vercel Speed Insights: prj_9RkQm2vT7xLpN4dWbYcF3sJz (vitals-by-device, p75)
Range: 2026-08-08T00:00:00Z to 2026-08-15T00:00:00Z (UTC)

device_type  p75_lcp
-----------  -------
mobile         4.1 s
tablet         3.0 s
desktop        2.1 s

Metric: vercel.speed_insights.lcp_ms (Largest Contentful Paint)
Target: 2.5 s or less
Lower is better for all five metrics.
The target is Vercel's published 'good' threshold, so the verdict is two tier: meets target or over target.
[exit code 0]
```

### Is it getting better or worse

A granularity is requested here, so the buckets are kept rather than collapsed into one number.

```console
$ vercel-insights vitals-trend --since 2026-08-08 --until 2026-08-15
Vercel Speed Insights: prj_9RkQm2vT7xLpN4dWbYcF3sJz (vitals-trend, p75)
Range: 2026-08-08T00:00:00Z to 2026-08-15T00:00:00Z (UTC)

day         p75_lcp
----------  -------
2026-08-08    3.4 s
2026-08-09    3.2 s
2026-08-10    3.0 s
2026-08-11    2.9 s
2026-08-12    2.8 s
2026-08-13    2.7 s
2026-08-14    2.6 s

Metric: vercel.speed_insights.lcp_ms (Largest Contentful Paint)
Target: 2.5 s or less
Lower is better for all five metrics.
The target is Vercel's published 'good' threshold, so the verdict is two tier: meets target or over target.
[exit code 0]
```

### How much data is behind those percentiles

A percentile over few measurements is not comparable to one over many.

```console
$ vercel-insights data-points --since 2026-08-08 --until 2026-08-15
Vercel Speed Insights: prj_9RkQm2vT7xLpN4dWbYcF3sJz (data-points, sum)
Range: 2026-08-08T00:00:00Z to 2026-08-15T00:00:00Z (UTC)

route         sum_lcp_count  % sum_lcp_count
------------  -------------  ---------------
/blog/[slug]          5,120            12.2%
/docs/[slug]         18,640            44.4%
/pricing              7,180            17.1%
/                    11,020            26.3%
------------  -------------  ---------------
TOTAL                41,960           100.0%

Metric: vercel.speed_insights.lcp_count (Largest Contentful Paint data points)
These are data point counts, not metric values: one data point is one measurement of one web vital during one visit, and a visit produces up to six.
They are what makes a percentile trustworthy, so a group with few of them is not comparable to one with many.
[exit code 0]
```

## Errors: request logs

### Recent requests, captured live and redacted

Real output from a real project, with its identifiers replaced as described at
the top of this file. The `level` column is `-` on every row because none of
these requests printed a log line, which is the ordinary case: a filter like
`--level error` would have matched none of them.

`--limit 5` cut the table, and the footer describes what is on screen rather than
the half hour: *showing the most recent 5 of more requests that matched*, with the
remedy on the line after it. Nothing is called a "most affected route" here,
because all five routes are distinct and tied at one occurrence, and a ranking
with no winner is not a finding. The last route is wider than its column, so it is
truncated with an ellipsis, and its `source` reads `serverless-middleware`: that
is the display spelling, whose filter form is `edge-middleware`, which the last
block in this section shows being resolved.

```console
$ vercel-insights logs --since 30m --limit 5
Vercel request logs: prj_ExampleRedactedProjectId0000 (logs, last 30 minutes)
Range: 2026-08-17T09:18:19Z to 2026-08-17T09:48:19Z (UTC)

time      level  status  method  route                             source                 message
--------  -----  ------  ------  --------------------------------  ---------------------  -------
09:47:59  -         200  GET     /api/teams/[teamId]               serverless
09:47:59  -         401  GET     /api/me                           serverless
09:47:59  -         200  GET     /api/documents/[slug]             serverless
09:47:59  -         200  GET     /robots.txt                       serverless
09:47:59  -         200  GET     /[locale]/t/[teamId]/[documentS…  serverless-middleware

Showing the most recent 5 of more requests that matched in 30 minutes: 4 x 200, 1 x 401.
More rows matched than were shown. Raise --limit (up to 200) or narrow the window.
Add --expand for full messages, or --request-id to pull one request apart.
[exit code 0]
```

### What a healthy project looks like

Also captured live and redacted, and the case most worth recognising: nothing
failed. Exit code 0, because "no errors" is an answer rather than a failure. The
last line is the honest part. Runtime logs are kept for far less time than analytics data, so
over 24 hours an empty result can mean "nothing broke" or "most of that window
has already aged out", and the tool refuses to imply the first.

```console
$ vercel-insights errors --since 24h
Vercel request logs: prj_ExampleRedactedProjectId0000 (errors, last 24 hours)
Range: 2026-08-16T06:34:31Z to 2026-08-17T06:34:31Z (UTC)
Counted as an error: a 5xx response, a crashed function, or a request that logged an error or fatal line.

No request logs for project prj_ExampleRedactedProjectId0000 between 2026-08-16T06:34:31Z and 2026-08-17T06:34:31Z.

Runtime log retention is 1 hour on Hobby, 1 day on Pro, 3 days on Enterprise and 30 days with Observability Plus, so an empty result over a longer window can mean the logs aged out rather than that nothing failed.
[exit code 0]
```

### Asking for 4xx, which are not errors

Live and redacted too, and the one case worth showing on purpose: `errors`
normally decides for itself what an error is, and an explicit `--level` or
`--status-code` takes that decision away from it. The preset then issues a single query carrying
your filter, so the rows are whatever it matched. `--status-code 4xx` matches
401s, and a 401 on `/api/me` is the application turning away an unauthenticated
request, so the header says the filter replaced the error definition rather than
narrowing it, and the footer counts "requests" instead of "errors". Nothing here
claims those three rows are faults.

```console
$ vercel-insights errors --status-code 4xx --since 1h --limit 3
Vercel request logs: prj_ExampleRedactedProjectId0000 (errors, last 1 hour)
Range: 2026-08-17T08:48:40Z to 2026-08-17T09:48:40Z (UTC)
Filter: statusCode 4xx
These rows are what statusCode 4xx matched: your filter chose them, not this tool's own error query. An explicit --level or --status-code replaces the error definition rather than narrowing it.

time      level  status  method  route    source      message
--------  -----  ------  ------  -------  ----------  -------
09:47:59  -         401  GET     /api/me  serverless
09:47:52  -         401  GET     /api/me  serverless
09:47:52  -         401  GET     /api/me  serverless

Showing the most recent 3 of more requests that matched in 1 hour: 3 x 401.
More rows matched than were shown. Raise --limit (up to 200) or narrow the window.
Add --expand for full messages, or --request-id to pull one request apart.
[exit code 0]
```

Compare it with the block above: there the header line reads "Counted as an
error: a 5xx response, a crashed function, or a request that logged an error or
fatal line", because that run applied the definition itself.

### Errors, when there are some

Illustrative from here on: the live account had nothing failing, so these rows
are invented and served to the real renderer through a stub session.

`errors` issues two queries, one for `5xx` responses and one for `error` and
`fatal` log lines, and merges them by request id. All four rows below are errors,
for three different reasons: two 500s that logged a stack trace, a 200 whose
handler logged a fatal line, and a 502 that failed before anything printed. That
last one is why the message column says so rather than leaving a blank cell.

```console
$ vercel-insights errors --since 2026-08-17T10:36:00Z --until 2026-08-17T11:06:00Z
Vercel request logs: prj_9RkQm2vT7xLpN4dWbYcF3sJz (errors, last 30 minutes)
Range: 2026-08-17T10:36:00Z to 2026-08-17T11:06:00Z (UTC)
Counted as an error: a 5xx response, a crashed function, or a request that logged an error or fatal line.

time      level  status  method  route                  source      message
--------  -----  ------  ------  ---------------------  ----------  ----------------------------------
11:04:52  error     500  POST    /api/checkout          serverless  TypeError: Cannot read properties…
11:03:19  error     500  POST    /api/checkout          serverless  TypeError: Cannot read properties…
11:02:41  fatal     200  GET     /api/cron/sync         serverless  FATAL: connection pool exhausted
10:58:03  -         502  GET     /api/documents/[slug]  serverless  (no log line: the response failed)

4 errors in 30 minutes: 2 x 500, 1 x 200, 1 x 502.
Most affected route: /api/checkout (2).
1 of them returned a non-5xx status and count as errors only because they logged an error or fatal line.
Add --expand for full messages, or --request-id to pull one request apart.
[exit code 0]
```

### Where the errors are concentrated

`error-summary` runs the same two queries and tallies the merged rows three ways.
The `200` row in the status table is not a bug: it is the request that counts as
an error only because it logged a fatal line, and the footer says how many rows
qualify that way. Messages are grouped by exact text, never by a guessed pattern,
so two different bugs can never be merged into one row.

```console
$ vercel-insights error-summary --since 2026-08-17T05:06:00Z --until 2026-08-17T11:06:00Z
Vercel request logs: prj_9RkQm2vT7xLpN4dWbYcF3sJz (error-summary, last 6 hours)
Range: 2026-08-17T05:06:00Z to 2026-08-17T11:06:00Z (UTC)

status  count   share
------  -----  ------
500        41   74.5%
502        12   21.8%
200         2    3.6%
------  -----  ------
TOTAL      55  100.0%

route                  count  worst status  first seen  last seen
---------------------  -----  ------------  ----------  ---------
/api/checkout             38           500  05:11:02    10:44:41
/api/documents/[slug]     12           502  06:40:19    10:42:19
/api/cron/sync             5           500  06:30:00    11:02:41

message                                         count  first seen  last seen
----------------------------------------------  -----  ----------  ---------
TypeError: Cannot read properties of undefined     38  05:11:02    10:44:41
(no log line)                                      15  06:30:00    10:42:19
FATAL: connection pool exhausted                    2  07:15:44    11:02:41

55 errors in 6 hours: 41 x 500, 12 x 502, 2 x 200.
Most affected route: /api/checkout (38).
2 of them returned a non-5xx status and count as errors only because they logged an error or fatal line.
[exit code 0]
```

### One request, pulled apart

`--request-id` with `--expand` prints every line that request logged, worst level
first, in full, and marks any line Vercel itself truncated. A message that spans
several lines keeps its shape, indented, so a stack trace never steps back to
column zero and cannot forge a line of this tool's own output.

```console
$ vercel-insights logs --request-id abcde-1786964768933-0123456789ab --expand --since 2026-08-17T10:36:00Z --until 2026-08-17T11:06:00Z
Vercel request logs: prj_9RkQm2vT7xLpN4dWbYcF3sJz (logs, last 30 minutes)
Range: 2026-08-17T10:36:00Z to 2026-08-17T11:06:00Z (UTC)
Filter: requestId abcde-1786964768933-0123456789ab

time      level  status  method  route          source      message
--------  -----  ------  ------  -------------  ----------  ----------------------------------
11:04:52  error     500  POST    /api/checkout  serverless  TypeError: Cannot read properties…
    error: TypeError: Cannot read properties of undefined
          at handler (/var/task/checkout.js:42:19)
    warning: retrying payment provider call (attempt 2 of 3)
    info: cart 4192 for customer 88213 has 3 items and a coupon code that is [truncated by Vercel]
    request abcde-1786964768933-0123456789ab

1 request in 30 minutes: 1 x 500.
[exit code 0]
```

### Logs as JSON

Nothing the API sent is thrown away: each entry carries the tabulated columns
plus the whole original row under `raw`, so a field this tool has no column for
is still there for `jq`. `notes` carries the same sentences the text output
prints, so a script can quote the caveats rather than reinventing them.

```console
$ vercel-insights logs --request-id err-3 --json --since 2026-08-17T10:36:00Z --until 2026-08-17T11:06:00Z
{
  "query": {
    "project": "prj_9RkQm2vT7xLpN4dWbYcF3sJz",
    "preset": "logs",
    "since": "2026-08-17T10:36:00Z",
    "until": "2026-08-17T11:06:00Z",
    "filters": {
      "requestId": "err-3"
    },
    "limit": 50
  },
  "entries": [
    {
      "requestId": "err-3",
      "timestamp": "2026-08-17T11:02:41+00:00",
      "status": 200,
      "method": "GET",
      "path": "/api/cron/sync",
      "route": "/api/cron/sync",
      "source": "serverless",
      "environment": "production",
      "deploymentId": "dpl_ExampleDeploymentId000000000",
      "durationMs": 54.0,
      "region": "fra1",
      "errorCode": "",
      "branch": "main",
      "domain": "demo.vercel.app",
      "traceId": "",
      "crashed": false,
      "isError": true,
      "level": "fatal",
      "message": "FATAL: connection pool exhausted",
      "lines": [
        {
          "level": "fatal",
          "message": "FATAL: connection pool exhausted",
          "truncated": false
        }
      ],
      "raw": {
        "requestId": "err-3",
        "timestamp": "2026-08-17T11:02:41.000Z",
        "deploymentId": "dpl_ExampleDeploymentId000000000",
        "environment": "production",
        "deploymentDomain": "demo.vercel.app",
        "branch": "main",
        "domain": "demo.vercel.app",
        "requestMethod": "GET",
        "requestPath": "/api/cron/sync",
        "statusCode": 200,
        "errorCode": "",
        "route": "/api/cron/sync",
        "cache": "MISS",
        "wafAction": "",
        "traceId": "",
        "logs": [
          {
            "level": "fatal",
            "message": "FATAL: connection pool exhausted",
            "messageTruncated": false
          }
        ],
        "requestDurationMs": 54,
        "clientRegion": "fra1",
        "hasFunctionCrashed": false,
        "events": [
          {
            "source": "serverless",
            "httpStatus": 200,
            "region": "fra1"
          }
        ],
        "requestTags": [
          "ssr",
          "rsc"
        ]
      }
    }
  ],
  "truncated": false,
  "pagesFetched": 1,
  "notes": [
    "1 request in 30 minutes: 1 x 200."
  ]
}
[exit code 0]
```

### Logs as CSV

One row per request. A message containing a newline stays inside its cell,
because `csv.writer` quotes any field holding the line terminator.

The `note:` lines below are on **stderr**, which is why they can be here at all:
CSV has nowhere to carry a caveat, and a consumer piping it is exactly the one
who could not otherwise tell a table cut at its limit from a complete one. So
`errors --csv > errors.csv` writes only the four data rows to the file and still
prints the three notes to the terminal.

```console
$ vercel-insights errors --csv --since 2026-08-17T10:36:00Z --until 2026-08-17T11:06:00Z
time,level,status,method,route,path,source,requestId,message
2026-08-17T11:04:52.100000+00:00,error,500,POST,/api/checkout,/api/checkout,serverless,err-1,TypeError: Cannot read properties of undefined
2026-08-17T11:03:19.400000+00:00,error,500,POST,/api/checkout,/api/checkout,serverless,err-2,TypeError: Cannot read properties of undefined
2026-08-17T11:02:41+00:00,fatal,200,GET,/api/cron/sync,/api/cron/sync,serverless,err-3,FATAL: connection pool exhausted
2026-08-17T10:58:03+00:00,,502,GET,/api/documents/[slug],/api/documents/summer,serverless,err-4,
note: 4 errors in 30 minutes: 2 x 500, 1 x 200, 1 x 502.
note: Most affected route: /api/checkout (2).
note: 1 of them returned a non-5xx status and count as errors only because they logged an error or fatal line.
[exit code 0]
```

`error-summary` has no CSV form, on purpose: it prints three tables, and one file
cannot be three tables. `errors --csv` is the flat version of the same rows.

### The source column and the source filter do not share a vocabulary

A row can display `serverless-middleware` in its `source` column, and the API
matches nothing when that spelling is sent back as a filter: the spelling that
matches those rows is `edge-middleware`. So the value this tool showed is accepted
and rewritten, which the dry run makes visible.

```console
$ vercel-insights logs --source serverless-middleware --since 2026-08-17T10:36:00Z --until 2026-08-17T11:06:00Z --dry-run
GET https://vercel.com/api/logs/request-logs

Query parameters:
  projectId  prj_9RkQm2vT7xLpN4dWbYcF3sJz
  ownerId    own_demo
  page       0
  startDate  1786962960000
  endDate    1786964760000
  source     edge-middleware

Headers:
  Accept         application/json
  Authorization  Bearer <redacted>
  User-Agent     vercel-insights-skill/1.1.1

Encoded URL (never contains the token):
  https://vercel.com/api/logs/request-logs?projectId=prj_9RkQm2vT7xLpN4dWbYcF3sJz&ownerId=own_demo&page=0&startDate=1786962960000&endDate=1786964760000&source=edge-middleware

Nothing was sent. No credential is printed above.
[exit code 0]
```

## Failing a build on a regression

### Every budget met

Exit code 0.

```console
$ vercel-insights vitals --since 2026-08-08 --until 2026-08-15 --budget inp=200 --budget ttfb=800
Vercel Speed Insights: prj_9RkQm2vT7xLpN4dWbYcF3sJz
Range: 2026-08-08T00:00:00Z to 2026-08-15T00:00:00Z (UTC)

metric                        p75  target  verdict
-------------------------  ------  ------  ------------
Largest Contentful Paint    2.9 s   2.5 s  over target
Interaction to Next Paint  184 ms  200 ms  meets target
Cumulative Layout Shift     0.128   0.100  over target
First Contentful Paint      1.6 s   1.8 s  meets target
Time to First Byte         412 ms  800 ms  meets target

Lower is better for all five metrics.
The target is Vercel's published 'good' threshold, so the verdict is two tier: meets target or over target.
Real Experience Score is not queryable through this API; read it on the Speed Insights dashboard.

Budgets
  pass    Interaction to Next Paint    184 ms against 200 ms
  pass    Time to First Byte           412 ms against 800 ms
[exit code 0]
```

### A budget exceeded

Exit code **3**, deliberately not 1: the run succeeded and is reporting bad news, which a CI step usually wants to tell apart from the API being down. A copyable workflow is in [`github-action-budget.yml`](github-action-budget.yml).

```console
$ vercel-insights vitals --since 2026-08-08 --until 2026-08-15 --budget lcp=2500 --budget cls=0.1
Vercel Speed Insights: prj_9RkQm2vT7xLpN4dWbYcF3sJz
Range: 2026-08-08T00:00:00Z to 2026-08-15T00:00:00Z (UTC)

metric                        p75  target  verdict
-------------------------  ------  ------  ------------
Largest Contentful Paint    2.9 s   2.5 s  over target
Interaction to Next Paint  184 ms  200 ms  meets target
Cumulative Layout Shift     0.128   0.100  over target
First Contentful Paint      1.6 s   1.8 s  meets target
Time to First Byte         412 ms  800 ms  meets target

Lower is better for all five metrics.
The target is Vercel's published 'good' threshold, so the verdict is two tier: meets target or over target.
Real Experience Score is not queryable through this API; read it on the Speed Insights dashboard.

Budgets
  fail    Largest Contentful Paint      2.9 s against 2.5 s
  fail    Cumulative Layout Shift       0.128 against 0.100
at least one budget was exceeded, so this run exits 3
[exit code 3]
```

## Beyond web vitals

### What can this account query?

The schema is the source of truth for what an account can reach. Everything outside Web Analytics and Speed Insights needs Observability Plus.

```console
$ vercel-insights --list-metrics vercel
Queryable metrics

7 queryable metric(s):

vercel.function_invocation.count
    unit          count
    aggregations  sum
    default       sum
    dimensions    route, function_region
    Function Invocations Count

vercel.request.count
    unit          count
    aggregations  sum
    default       sum
    dimensions    route, http_status
    Requests Count

vercel.speed_insights.cls
    unit          score
    aggregations  p75, p90, p95, p99
    default       p75
    dimensions    route, request_path, country, device_type
    Speed Insights Cumulative Layout Shift

vercel.speed_insights.fcp_ms
    unit          ms
    aggregations  p75, p90, p95, p99
    default       p75
    dimensions    route, request_path, country, device_type
    Speed Insights First Contentful Paint

vercel.speed_insights.inp_ms
    unit          ms
    aggregations  p75, p90, p95, p99
    default       p75
    dimensions    route, request_path, country, device_type
    Speed Insights Interaction to Next Paint

vercel.speed_insights.lcp_ms
    unit          ms
    aggregations  p75, p90, p95, p99
    default       p75
    dimensions    route, request_path, country, device_type
    Speed Insights Largest Contentful Paint

vercel.speed_insights.ttfb_ms
    unit          ms
    aggregations  p75, p90, p95, p99
    default       p75
    dimensions    route, request_path, country, device_type
    Speed Insights Time to First Byte
[exit code 0]
```

### Any metric, by id

No unit and no target are claimed for a metric outside the five web vitals, so the value is reported rather than judged.

```console
$ vercel-insights --metric vercel.function_invocation.count --aggregation sum --group-by route --since 2026-08-08 --until 2026-08-15
Vercel Speed Insights: prj_9RkQm2vT7xLpN4dWbYcF3sJz (metric, sum)
Range: 2026-08-08T00:00:00Z to 2026-08-15T00:00:00Z (UTC)

route         sum_count  % sum_count
------------  ---------  -----------
/api/search      48,210        63.3%
/api/auth        21,840        28.7%
/api/webhook      6,120         8.0%
------------  ---------  -----------
TOTAL            76,170       100.0%
[exit code 0]
```

## Machine readable output

### As JSON, for jq

```console
$ vercel-insights devices --since 2026-08-08 --until 2026-08-15 --json
{
  "query": {
    "groupBy": [
      "deviceType"
    ]
  },
  "range": {
    "since": "2026-08-08T00:00:00Z",
    "until": "2026-08-15T00:00:00Z"
  },
  "dataset": "visits",
  "groupBy": [
    "deviceType"
  ],
  "isCount": false,
  "metrics": [
    "pageviews",
    "visitors"
  ],
  "rows": [
    {
      "key": "desktop",
      "groups": {
        "deviceType": "desktop"
      },
      "timestamp": null,
      "metrics": {
        "pageviews": 29140,
        "visitors": 18770
      }
    },
    {
      "key": "mobile",
      "groups": {
        "deviceType": "mobile"
      },
      "timestamp": null,
      "metrics": {
        "pageviews": 17402,
        "visitors": 11960
      }
    },
    {
      "key": "tablet",
      "groups": {
        "deviceType": "tablet"
      },
      "timestamp": null,
      "metrics": {
        "pageviews": 1530,
        "visitors": 1140
      }
    }
  ],
  "totals": {
    "pageviews": 48072,
    "visitors": 31870
  },
  "raw": {
    "version": 1,
    "query": {
      "groupBy": [
        "deviceType"
      ]
    },
    "data": [
      {
        "deviceType": "desktop",
        "pageviews": 29140,
        "visitors": 18770
      },
      {
        "deviceType": "mobile",
        "pageviews": 17402,
        "visitors": 11960
      },
      {
        "deviceType": "tablet",
        "pageviews": 1530,
        "visitors": 1140
      }
    ]
  }
}
[exit code 0]
```

### As CSV, for a spreadsheet

```console
$ vercel-insights devices --since 2026-08-08 --until 2026-08-15 --csv
deviceType,pageviews,visitors
desktop,29140,18770
mobile,17402,11960
tablet,1530,1140
[exit code 0]
```

## Seeing the request without sending it

### A Web Analytics request

`--dry-run` needs no token and sends nothing.

```console
$ vercel-insights top-pages --since 2026-08-08 --until 2026-08-15 --country US --dry-run
GET https://api.vercel.com/v1/query/web-analytics/visits/aggregate

Query parameters:
  projectId  prj_9RkQm2vT7xLpN4dWbYcF3sJz
  by         requestPath
  since      2026-08-08T00:00:00Z
  until      2026-08-15T00:00:00Z
  limit      10
  filter     country eq 'US'

Headers:
  Accept         application/json
  Authorization  Bearer <redacted>
  User-Agent     vercel-insights-skill/1.1.1

Encoded URL (never contains the token):
  https://api.vercel.com/v1/query/web-analytics/visits/aggregate?projectId=prj_9RkQm2vT7xLpN4dWbYcF3sJz&by=requestPath&since=2026-08-08T00%3A00%3A00Z&until=2026-08-15T00%3A00%3A00Z&limit=10&filter=country+eq+%27US%27

Nothing was sent. No credential is printed above.
[exit code 0]
```

### A request logs dry run, which is two requests

`errors` is the one preset whose dry run shows why it queries twice: one call
filters on the response status, the other on the log level, and the merge happens
here rather than at the API. Note the host, `vercel.com` rather than
`api.vercel.com`, and the timestamps in Unix milliseconds, which is what this
endpoint takes.

```console
$ vercel-insights errors --since 2026-08-17T10:36:00Z --until 2026-08-17T11:06:00Z --dry-run
GET https://vercel.com/api/logs/request-logs

Query parameters:
  projectId   prj_9RkQm2vT7xLpN4dWbYcF3sJz
  ownerId     team_8mHvK3nQpR6tXwZa
  page        0
  startDate   1786962960000
  endDate     1786964760000
  statusCode  5xx

Headers:
  Accept         application/json
  Authorization  Bearer <redacted>
  User-Agent     vercel-insights-skill/1.1.1

Encoded URL (never contains the token):
  https://vercel.com/api/logs/request-logs?projectId=prj_9RkQm2vT7xLpN4dWbYcF3sJz&ownerId=team_8mHvK3nQpR6tXwZa&page=0&startDate=1786962960000&endDate=1786964760000&statusCode=5xx

Nothing was sent. No credential is printed above.

GET https://vercel.com/api/logs/request-logs

Query parameters:
  projectId  prj_9RkQm2vT7xLpN4dWbYcF3sJz
  ownerId    team_8mHvK3nQpR6tXwZa
  page       0
  startDate  1786962960000
  endDate    1786964760000
  level      error,fatal

Headers:
  Accept         application/json
  Authorization  Bearer <redacted>
  User-Agent     vercel-insights-skill/1.1.1

Encoded URL (never contains the token):
  https://vercel.com/api/logs/request-logs?projectId=prj_9RkQm2vT7xLpN4dWbYcF3sJz&ownerId=team_8mHvK3nQpR6tXwZa&page=0&startDate=1786962960000&endDate=1786964760000&level=error%2Cfatal

Nothing was sent. No credential is printed above.
[exit code 0]
```

### A Speed Insights request, with its JSON body

```console
$ vercel-insights vitals-trend --metric inp --granularity 1d --since 2026-08-08 --until 2026-08-15 --dry-run
POST https://api.vercel.com/v2/observability/query

Query parameters:
  (none)

Headers:
  Accept         application/json
  Authorization  Bearer <redacted>
  User-Agent     vercel-insights-skill/1.1.1

JSON body:
  {
    "metric": "vercel.speed_insights.inp_ms",
    "scope": {
      "type": "project",
      "ownerId": "team_8mHvK3nQpR6tXwZa",
      "projectIds": [
        "prj_9RkQm2vT7xLpN4dWbYcF3sJz"
      ]
    },
    "aggregation": "p75",
    "granularity": {
      "days": 1
    },
    "startTime": "2026-08-08T00:00:00Z",
    "endTime": "2026-08-15T00:00:00Z"
  }

Encoded URL (never contains the token):
  https://api.vercel.com/v2/observability/query

Nothing was sent. No credential is printed above.
[exit code 0]
```

## When something is wrong

### Nothing collected in the window

Exit code 0. An empty result is an answer, not a failure.

```console
$ vercel-insights top-pages --since 2026-01-01 --until 2026-01-02
No visits data for project prj_9RkQm2vT7xLpN4dWbYcF3sJz (grouped by requestPath) between 2026-01-01T00:00:00Z and 2026-01-02T00:00:00Z with no filter. Try a wider --since, or relax the filter.
[exit code 0]
```

### A token that cannot reach Speed Insights

Vercel answers `404 Observability Data not found.`, which reads as "your project has no data" but means "this token cannot ask".

```console
$ vercel-insights vitals --since 2026-08-08 --until 2026-08-15
error: HTTP 404 (not_found): Observability Data not found.
This usually means the access token is scoped to a single project. Speed Insights is served by Vercel's observability API, which scopes by account rather than by project, so it needs a token with account (or team) scope. Web Analytics presets keep working with a project scoped token. Create an account scoped token at https://vercel.com/account/tokens, or confirm the scope of the current one with: npx vercel@latest metrics schema
[exit code 1]
```

### A token that cannot reach request logs

The logs endpoint is scoped by the owning account too, through an `ownerId`
parameter it requires and cannot infer, so a project scoped token is refused with
a `403`. The hint names that rather than pointing at `--team`: a team id is
verified not to work in place of an `ownerId` here, and the client never sends one.

```console
$ vercel-insights errors --since 30m
error: HTTP 403 (forbidden): You don't have permission to access this resource.
Request logs are scoped by the owning account (the ownerId parameter), so a token scoped to a single project cannot read them: it cannot act for the account that owns the project. Create an account or team scoped token at https://vercel.com/account/tokens, and set VERCEL_TEAM_ID for a team owned project, since a team is its own owner.
[exit code 1]
```

### A mistyped log level

Refused rather than sent. This API answers an unknown `level` or `source` with
HTTP 200 and zero rows, so a typo would read as "your site is fine", which is the
worst answer available. The same applies to `--status-code`, where the error quotes
the API's own rule.

```console
$ vercel-insights errors --level erro
error: --level 'erro' is not a log level this API knows; it accepts error, warning, info, fatal, comma separated. This is checked here because the API answers an unknown value with HTTP 200 and zero rows rather than an error, which would read as 'nothing is broken'
[exit code 2]
```
```console
$ vercel-insights errors --status-code '>=500'
error: --status-code '>=500' is not a status this API accepts. It says: "statusCode must contain only comma-separated integers, status code classes like 4xx or 5xx, or \"None\"". So --status-code 500, --status-code 5xx, --status-code 4xx,5xx and --status-code None all work; a comparison such as >=500 does not
[exit code 2]
```

### No permission

Vercel's own message is kept verbatim.

```console
$ vercel-insights top-pages --since 2026-08-08 --until 2026-08-15
error: HTTP 403 (forbidden): Not authorized
[exit code 1]
```

### Rate limited, after retries are used up

```console
$ vercel-insights top-pages --since 2026-08-08 --until 2026-08-15 --max-retries 1
error: HTTP 429 (rate_limited): Too many requests [gave up after 2 attempts]
hint: rate limits are per endpoint; wait for the reset above or raise --max-retries so the client waits for you
[exit code 1]
```

### A mistyped dimension

Caught before any request is sent.

```console
$ vercel-insights top-pages --group-by contry --since 2026-08-08 --until 2026-08-15 --dry-run
error: unknown dimension 'contry' for the visits dataset. Did you mean 'country'? Valid dimensions: hour, day, week, month, year, country, deviceType, environment, requestPath, referrerHostname, osName, browserName, route, utmSource, utmMedium, utmCampaign, utmContent, utmTerm, flags, plus flags/<name>
[exit code 2]
```
