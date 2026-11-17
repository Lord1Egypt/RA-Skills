# Reports and Dashboards — Reading the Numbers the Business Trusts

**Before running one**, check `## Saved Queries` in `~/Clawic/data/salesforce-api-integration/memory.md`: report ids and the SOQL equivalents that replaced them when a report hit its row ceiling are recorded there.

**Contents:** [Report or Query](#report-or-query) · [Find and Describe](#find-and-describe) · [Run It](#run-it) · [Reading the factMap](#reading-the-factmap) · [Runtime Filters](#runtime-filters) · [Async Runs](#async-runs) · [Dashboards](#dashboards) · [Limits](#limits) · [Report Traps](#report-traps)

## Report or Query

| Need | Use | Why |
|---|---|---|
| The exact number the sales meeting quotes | The report | It carries the org's own filters, groupings and currency conversion. A SOQL rebuild that differs by 2% is worse than useless |
| Rows to process, load or export | SOQL or Bulk (`soql.md`, `bulk.md`) | No row ceiling, no factMap to unpick |
| More than a couple of thousand rows | Bulk query | The synchronous report path truncates |
| A recurring extract | SOQL, written once | Reports get edited by whoever owns them, without warning |

The trap in both directions: rebuilding a trusted report in SOQL and quietly getting a different number, or scraping a report for bulk data it was never meant to deliver.

## Find and Describe

```bash
# Recently used reports (a short list, not the catalog)
curl "$SF_INSTANCE_URL/services/data/v62.0/analytics/reports" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN"

# The full catalog, searchable, through ordinary SOQL
curl -G "$SF_INSTANCE_URL/services/data/v62.0/query/" \
  --data-urlencode "q=SELECT Id, Name, DeveloperName, FolderName FROM Report WHERE Name LIKE '%Pipeline%'" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN"

# What this report contains: columns, groupings, filters, format
curl "$SF_INSTANCE_URL/services/data/v62.0/analytics/reports/00Oxx0000012345/describe" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN"
```

Describe before running anything you did not build. `reportMetadata` tells you the report format (`TABULAR`, `SUMMARY`, `MATRIX`), the grouping columns, the aggregates and the existing filters — and the format decides the entire shape of the result you are about to parse.

## Run It

```bash
# Aggregates only — fast, and often all you need
curl "$SF_INSTANCE_URL/services/data/v62.0/analytics/reports/00Oxx0000012345" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN"

# With the detail rows
curl "$SF_INSTANCE_URL/services/data/v62.0/analytics/reports/00Oxx0000012345?includeDetails=true" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN"
```

A synchronous run returns roughly the first couple of thousand detail rows and sets `allData: false` when it truncated. **Check that flag every time** — a truncated report looks exactly like a complete one, and the aggregates are computed over the full data set while the rows are not. Reporting "here are all the deals" from a truncated response is the failure mode this API is famous for.

Running a report consumes an API call and a report-run allocation; it changes nothing in the org.

## Reading the factMap

The response is not a table. It is a `factMap` keyed by grouping coordinates, and understanding the key format is the whole skill:

| Key | Means |
|---|---|
| `T!T` | Grand total — the only key a tabular report has |
| `0!T` | First value of the first grouping, all of the second |
| `0!0`, `0!1` | First grouping value crossed with each second-grouping value (matrix) |

Each entry carries `aggregates[]` (the summary values, with `label` and `value`) and, when `includeDetails=true`, `rows[].dataCells[]` in the column order given by `reportMetadata.detailColumns`.

- `value` is the raw datum; `label` is the formatted, localized string. Sum `value`, display `label`, never the reverse.
- Grouping labels live in `groupingsDown`/`groupingsAcross`, not in the factMap — you join them by the key's index positions.
- For a tabular report you only ever need `factMap["T!T"]`, which is why tabular reports are the ones worth automating.

## Runtime Filters

POST the report id with a modified `reportMetadata` to filter without touching the saved report:

```bash
curl -X POST "$SF_INSTANCE_URL/services/data/v62.0/analytics/reports/00Oxx0000012345?includeDetails=true" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN" -H "Content-Type: application/json" \
  -d '{"reportMetadata":{"reportFilters":[
        {"column":"OPPORTUNITY.STAGE_NAME","operator":"equals","value":"Proposal"}],
      "standardDateFilter":{"column":"CLOSE_DATE","durationValue":"THIS_QUARTER"}}}'
```

- Column names are the report's internal API names from the describe, not the object's field names. Copy them from `reportMetadata`; they cannot be guessed.
- The number of runtime filters is capped in the low tens — enough for parameterizing, not for arbitrary querying.
- `reportBooleanFilter` (`"1 AND (2 OR 3)"`) combines them. Without it, filters are AND'd.
- This is how one saved report serves twelve dashboards' worth of questions without twelve saved reports.

## Async Runs

For a report that is slow or wide:

```bash
curl -X POST "$SF_INSTANCE_URL/services/data/v62.0/analytics/reports/00Oxx0000012345/instances" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN"
# → {"id":"0LGxx0000012345","status":"New"}

curl "$SF_INSTANCE_URL/services/data/v62.0/analytics/reports/00Oxx0000012345/instances/0LGxx0000012345" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN"
```

Poll until `status` is `Success` (or `Error`). Instances are retained for about a day and then discarded, and both the number of concurrent instances and the number retained per report are capped — download the result rather than treating the instance as storage.

## Dashboards

`/analytics/dashboards` lists them, `/analytics/dashboards/<id>` returns the current component data with the timestamp of the last refresh, and a POST to `/analytics/dashboards/<id>` requests a refresh.

Dashboards run as a specific user (the running user, or the viewer for dynamic dashboards), so the numbers you read through the API are that user's numbers — a legitimate reason for the API and the screen to disagree. Refresh allocations are separate and small; scraping dashboards for data instead of reading their source reports exhausts them quickly.

## Limits

- Roughly 2,000 detail rows synchronously, with `allData` marking truncation.
- Hourly caps on report runs and on concurrent async instances, per org and per user; the async report entries in `/limits` are the ones to watch (`limits.md`).
- Every run is an API call against the same daily allocation as everything else.
- A report over an unindexed filter times out for exactly the same reason a SOQL query does (`soql.md`).

## Report Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Ignoring `allData` | Truncated results look complete | Check the flag; above the ceiling, switch to Bulk query |
| Summing `label` values | They are localized, formatted strings | Sum `value` |
| Guessing filter column names | They are report-internal names | Take them from `/describe` |
| Polling an async instance every second | Burns the allocation on status checks | Backoff, and download once |
| Treating a report id as stable forever | Reports get rebuilt in new folders and the id changes | Store the id **and** the developer name in `## Saved Queries` |
| Rebuilding a trusted report in SOQL | Currency conversion, sharing and filter logic differ; the number will not match | Run the report for the number, use SOQL for the rows |
| Scraping dashboards for data | Small refresh allocation, running-user semantics | Read the source reports |

**When a report becomes part of a workflow** — the number someone asks for weekly, or one that hit the row ceiling and had to become a query — record it in `## Saved Queries` in `memory.md`: purpose, kind (report or SOQL), the id or the query, and the note that explains which one to use. That note is what stops the next session from rebuilding the same report in SOQL and getting a different answer.
