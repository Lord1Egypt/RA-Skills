# Reports, charts and exports

A report is a saved question about your workspace data. It always has a **table**, and it can
have a **download** (CSV), a **chart** or a **map**. Reports are the answer to "how many", "how
much per week", "which station is short of people", "what changed last month".

**A member can open and read reports. A member cannot build one.** Building is the operator's
job — that is one call in the service-request channel, not a missing right you should work
around. Section 3 is the exact wording that gets it built right the first time.

## 1. What a report can do

| Capability | What it looks like |
|---|---|
| Table | Columns you name, in the order you name them, with your own column titles. Pagination or one long page. |
| CSV download | One click turns the table into a file: header row, semicolon separator, decimal comma — the format spreadsheet users expect in Europe. Optional per report; some reports deliberately have no download. |
| Bar / line / pie / scatter chart | Standard charts over one of the columns, with a title and a legend. The chart and the table always show the same numbers. |
| Multi-series chart | Two or more measures next to each other — for example *planned* against *actual* hours in the same week. |
| Stacked chart | Categories stacked per period — for example absences per month, split by kind. |
| Map / heatmap | Points from latitude/longitude columns, optionally clustered, with up to a few dozen regions in their own colours and a time slider that replays the last days. |
| Filters | Search fields that narrow the table and the chart together. They travel in the session, never in the URL, and they survive a page reload. |
| Favourites | Any report, and the exact view you were in (table, chart or map), can be pinned to your start cards. |
| Who sees it | A report is bound to one scope and to one or more roles. Nobody outside that scope sees it, even with the right role. |

**Cost:** building a report costs nothing (definitions are free). Reading one costs the same as
reading objects in that scope — a pay-per-use account spends a few credits per open.

## 2. What a report cannot do

- **No self-service editing.** No member-facing editor, no "save as" for members.
- **No automatic row filtering by the reader.** The scope and the role decide *whether* you may
  open a report, not *which rows* you get. A report that must show each person only their own
  rows has to be built that way by the operator.
- **No joins across scopes** unless the operator builds them on purpose.
- **No live push.** A report is a snapshot of the moment you open it.

## 3. How to order one (service request template)

Send a request in the service channel (`ontouser_service_request`) with these six lines. Vague
requests come back as questions, and that costs a round trip.

```
Report:       <short title>
Business:     <the question in one sentence, e.g. "are we over or under the planned hours?">
Shows:        <one row per what?>  e.g. per week, per person, per month, per station
Columns:      <the fields you want to see, in order>
Filter:       <what should narrow it, e.g. month, person, station>
Chart:        <bar / line / pie / stacked / map / none>
CSV:          <yes / no>
Who sees it:  <scope and role, e.g. "planning scope, member">
```

If the data for a column does not exist yet in the workspace, say so in the request — a report
cannot invent a field. "We would need a `contractType` on every person first" is a useful
sentence in a request.

## 4. A menu that works for shift-based businesses

These four are built and confirmed against real workspace data. Use them as the shopping list
when a restaurant or a care roster asks for "something with charts".

| Report | One row per | Columns | Chart |
|---|---|---|---|
| Hours per week: planned vs. actual | calendar week | week, planned hours, actual hours | two bars per week |
| Shifts per person | employee | person, number of shifts | bar, sorted by count |
| Absences per month and kind | month and kind | month, kind, count | stacked bars per month |
| Shifts per station | station | station, number of shifts | pie |

Three of them answer the questions a manager actually asks on a Monday: *are we over the plan*,
*who carries the load*, *who is away*, *where are we thin*.

Good next candidates, all buildable from the same data: overtime per person and month (actual
minus planned), sickness rate per month (sick days ÷ planned days), staffing coverage per day
(shifts filled against demand), and the wage forecast per month (planned hours × hourly rate).

## 5. For the operator (what building one needs)

A report is one definition: the query, the column titles, optional search fields, the chart or
map settings, the scope and the roles. The query is written against the workspace data, so the
report shows exactly what the objects contain — nothing is derived behind it. Two rules that save
the most time:

- **Decide who aggregates.** Either the query returns raw rows and the chart counts them, or the
  query aggregates itself and the chart reads the ready numbers. Mixing the two produces bars of
  height 1 — the classic first-day mistake.
- **A stacked chart needs one column per category, not one row per category.** A query that
  returns `month, kind, count` cannot feed a stack of four kinds — the chart asks for a column
  per series and finds none, and the chart stays empty while the table looks perfect. Pivot it in
  the query (`SUM(CASE WHEN kind = '…' THEN 1 ELSE 0 END) AS …`) so every series has its own
  column.
- **Never join a one-to-many table without grouping.** A person with two shifts joined onto
  something that has one row per notification becomes two rows for the same shift, and the
  report silently double-counts.

Verification is not optional: open the report, count the rows against the number of objects you
expect, and check that the table and the chart agree. A report nobody counted is a report that
lies for months.
