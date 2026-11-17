# KPIs

The operating numbers that move stocks: deliveries, subscribers, same-store sales, nights booked, store counts, and weekly numbers published on the web. Every value comes with its source and the line it was read from, and each reported value is confirmed by a second, independent read of its filing before it is served.

## KPIs

`GET /kpis` (scope `research`, cursor-paged)

One company's KPI values, newest first: each fiscal quarter's numbers from its results release, 10-Q or 10-K, and the weekly numbers tracked for it.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | Ticker, e.g. `TSLA`. Required. |
| `kpi` | query | string | KPI ids, comma separated, e.g. `vehicle_deliveries,vehicle_production`. Default every KPI. |
| `kind` | query | string | `reported` or `tracked`. Reported values come from filings. Tracked values come from the web. |
| `from` | query | string | Periods ending on or after, `YYYY-MM-DD`. |
| `to` | query | string | Periods ending on or before, `YYYY-MM-DD`. |
| `limit` | query | integer | Rows per page, up to 1000. Default `100`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `symbol` | string | Ticker. |
| `kpi` | string | KPI id, e.g. `vehicle_deliveries`. |
| `name` | string | Its name, e.g. `Vehicle deliveries`. |
| `period` | string | Fiscal quarter `2026-Q3`, ISO week `2026-W44` or day `2026-11-04`. |
| `period_end` | string | Last day of the period, `YYYY-MM-DD`. |
| `value` | number | As first reported, in whole units: `486532` vehicles, `59800000000` dollars, `3.1` for 3.1%. |
| `restated_value` | number | The figure a filing a year later printed for this period, when it differs from `value`; else null. |
| `unit` | string | `usd`, `percent`, `basis_points`, or what is counted, e.g. `vehicles`, `members`, `nights`. |
| `kind` | string | `reported` or `tracked`. Reported values come from filings. Tracked values come from the web. |
| `source_url` | string | The document or page it was read from. |
| `accession` | string | The SEC filing, null for tracked. |
| `quote` | string | The sentence or table row holding the number, as printed. |

Request: `GET https://tradytics.com/api/public/v1/kpis?symbol=TSLA&kpi=vehicle_deliveries&apiKey=YOUR_API_KEY`

## KPI definitions

`GET /kpis/definitions` (scope `research`, cursor-paged)

The KPIs covered for each company, the periods they span, and whether the company still reports them. A KPI is never removed: one the company stops reporting is `stopped`, one it redefines is `replaced` by a new id from that quarter on.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | Ticker, e.g. `TSLA`. Default every company covered. |
| `limit` | query | integer | Rows per page, up to 1000. Default `100`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `kpi` | string | KPI id. |
| `symbol` | string | Ticker. |
| `name` | string | Its name. |
| `unit` | string | `usd`, `percent`, `basis_points`, or what is counted, e.g. `vehicles`, `members`, `nights`. |
| `frequency` | string | `quarterly`, `weekly` or `daily`. |
| `kind` | string | `reported` or `tracked`. Reported values come from filings. Tracked values come from the web. |
| `description` | string | What it counts. |
| `status` | string | `active`, `stopped` (not reported in the company's last two quarters, or dropped by the company) or `replaced` (redefined). |
| `replaced_by` | string | For `replaced`: the KPI id that carries on. Else null. |
| `added_period` | string | The quarter it was first tracked. |
| `first_period` | string | The earliest period with a value. |
| `last_period` | string | The latest. |

Request: `GET https://tradytics.com/api/public/v1/kpis/definitions?symbol=TSLA&apiKey=YOUR_API_KEY`
