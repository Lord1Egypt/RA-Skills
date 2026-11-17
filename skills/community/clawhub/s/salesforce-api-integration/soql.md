# SOQL — Querying Without Table Scans

**Before writing a query against an object you have not queried here before**, read `## Schema Map` in `~/Clawic/data/salesforce-api-integration/memory.md` and `schema/<object>.md` if `## Boxes` names one, plus `## Saved Queries` — the query may already exist, with a note on whether its filter is selective.

**Contents:** [Selectivity Decides Everything](#selectivity-decides-everything) · [The Call](#the-call) · [Filters](#filters) · [Date Literals](#date-literals) · [Relationships](#relationships) · [Aggregates](#aggregates) · [Field Shortcuts](#field-shortcuts) · [Pagination](#pagination) · [SOSL](#sosl-text-search) · [Deleted and Archived](#deleted-and-archived) · [Building Queries Safely](#building-queries-safely) · [Query Traps](#query-traps)

## Selectivity Decides Everything

A SOQL query either uses an index or reads the whole object. On a 50,000-row object nobody notices; on a five-million-row Task table the same query times out at 120 seconds and there is no tuning to be done afterwards.

- **Indexed by default**: `Id`, `Name`, `OwnerId`, `CreatedDate`, `SystemModstamp`, `RecordTypeId`, `Email` on Contact and Lead, every lookup and master-detail field, and any field marked External Id or Unique. Everything else is unindexed until an admin (or Salesforce Support) adds a custom index.
- **The threshold is a fraction, not a row count.** A filter is selective only when it matches a small share of the object — roughly the first million rows at ~30% for a standard index, ~10% for a custom one, with the share tightening as the object grows. A filter matching half the object is never selective, however indexed the field.
- **What silently kills the index**: `!=`, `NOT`, `LIKE '%x%'` with a leading wildcard, `OR` across two different fields, comparing a field to `null` on some field types, and any function wrapped around the filtered field.
- **`OR` across fields is the quiet one.** `WHERE Email = :e OR Phone = :p` can force a scan even though both fields are indexed. Two selective queries and a union in your own code beat one unselective query.
- Diagnose before optimizing: append `&explain=true` to the query call and read back the plan, the leading operation type (`Index` vs `TableScan`) and the estimated row count.

```bash
curl -G "$SF_INSTANCE_URL/services/data/v62.0/query/" \
  --data-urlencode "q=SELECT Id FROM Task WHERE WhatId = '006xx0000012345'" \
  --data-urlencode "explain=true" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN"
```

## The Call

```bash
curl -G "$SF_INSTANCE_URL/services/data/v62.0/query/" \
  --data-urlencode "q=SELECT Id, Name, Industry FROM Account WHERE Industry = 'Technology' LIMIT 200" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN"
```

`--data-urlencode` over hand-rolled `+` substitution: a query with a space, an apostrophe or a `%` in a literal breaks the manual version in ways that surface as `MALFORMED_QUERY` on a query that reads fine.

Response shape: `totalSize` (the count of matching records, not of records returned), `done` (false means there is more), `records[]`, and `nextRecordsUrl` when `done` is false. `attributes.type` on each record is how you tell objects apart in a polymorphic result.

## Filters

```sql
SELECT Id, Name, Amount FROM Opportunity WHERE StageName = 'Proposal' AND Amount > 10000
SELECT Id FROM Account WHERE Industry IN ('Technology','Finance')
SELECT Id FROM Lead WHERE Status NOT IN ('Closed - Converted','Closed - Not Converted')
SELECT Id FROM Account WHERE Website != null
SELECT Id FROM Contact WHERE Name LIKE 'Smi%'          -- indexed: prefix match
SELECT Id FROM Contact WHERE Name LIKE '%smith%'        -- table scan: use SOSL instead
```

- Escape a literal apostrophe with a backslash: `WHERE Name = 'O\'Brien'`.
- Semi-join and anti-join: `WHERE Id IN (SELECT AccountId FROM Opportunity WHERE Amount > 50000)`. Salesforce caps how many of these one query may contain, and each one is a separate pass — two round trips are usually faster and always easier to debug.
- Picklist filters compare against the **API value**, which is not always the label the user sees. `toLabel(StageName)` returns the label in the results; it cannot be filtered on.

## Date Literals

Date literals evaluate in the **user's timezone**, not UTC — the same query run by two users can return different rows across a midnight boundary. Pin the timezone in `config.yaml` under output format if that matters.

| Literal | Window |
|---|---|
| `TODAY`, `YESTERDAY`, `TOMORROW` | The day |
| `THIS_WEEK`, `LAST_WEEK`, `NEXT_WEEK` | Week per the user's locale start day |
| `THIS_MONTH`, `LAST_MONTH`, `THIS_QUARTER`, `THIS_FISCAL_QUARTER`, `THIS_YEAR` | Calendar, or fiscal where the literal says so |
| `LAST_N_DAYS:30`, `NEXT_N_DAYS:7`, `LAST_N_MONTHS:6` | Rolling window ending today |
| `LAST_90_DAYS` | Fixed shorthand |

Absolute forms: a Date field takes `2026-06-15` unquoted; a DateTime field takes `2026-06-15T00:00:00Z` unquoted. Quoting either is `MALFORMED_QUERY`.

For incremental work, filter on `SystemModstamp`, not `LastModifiedDate` — the reason is in `sync.md`.

## Relationships

```sql
-- Child to parent: dot notation, up to 5 levels
SELECT Id, Name, Account.Name, Account.Owner.Name FROM Contact

-- Parent to child: a subquery using the child relationship name (plural)
SELECT Id, Name, (SELECT Id, LastName FROM Contacts) FROM Account

-- Custom relationships end in __r, the field ends in __c
SELECT Id, Shipment__r.Tracking_No__c FROM Invoice__c
SELECT Id, (SELECT Id FROM Shipments__r) FROM Account

-- Polymorphic fields (Task.WhatId, Event.WhoId): branch on type
SELECT Id, TYPEOF What WHEN Account THEN Name WHEN Opportunity THEN StageName ELSE Id END FROM Task
```

- One level of parent-to-child subquery only; a subquery inside a subquery is not valid SOQL. Two queries, joined in your code.
- The child relationship name is not the object name. `describe` returns it under `childRelationships[].relationshipName`, and a custom one is whatever the admin typed — check before guessing the plural.
- A subquery's records come back nested with their own `done`/`nextRecordsUrl`. More than 200 children per parent means the nested set is truncated: query the child object directly with a parent filter instead.
- Traversing a lookup that is null yields null, not an error. A report of "missing account names" is often just orphaned records.

## Aggregates

```sql
SELECT COUNT() FROM Account
SELECT Industry, COUNT(Id) total FROM Account GROUP BY Industry
SELECT StageName, SUM(Amount) amt, AVG(Amount) avg FROM Opportunity GROUP BY StageName
SELECT AccountId, COUNT(Id) c FROM Contact GROUP BY AccountId HAVING COUNT(Id) > 5
SELECT CALENDAR_MONTH(CloseDate) m, SUM(Amount) FROM Opportunity WHERE CloseDate = THIS_YEAR GROUP BY CALENDAR_MONTH(CloseDate)
SELECT Type, StageName, SUM(Amount) FROM Opportunity GROUP BY ROLLUP(Type, StageName)
```

- `COUNT()` with no argument returns only `totalSize`; `COUNT(Id)` returns a row you can group and alias. Ask for the one you actually want.
- Aliases are how you read the result: without `total`, the value comes back as `expr0`.
- Grouped results do not paginate like record results. If a grouping produces more rows than one response carries, narrow the grouping or filter the window — do not reach for `OFFSET`.
- Aggregates respect sharing and FLS like any query: two users can legitimately get two different totals.

## Field Shortcuts

- `FIELDS(ALL)`, `FIELDS(STANDARD)`, `FIELDS(CUSTOM)` expand to the fields the running user can see. `FIELDS(ALL)` requires a `LIMIT` of 200 or less, which makes it a debugging tool, not a production query.
- `FORMAT(Amount)` returns the locale-formatted string; `convertCurrency(Amount)` converts to the user's currency in a multi-currency org — without it, `SUM(Amount)` across currencies adds numbers that are not comparable.
- `ORDER BY ... NULLS LAST` — Salesforce sorts nulls first by default on ascending sorts, which puts empty records at the top of every report nobody asked for.

## Pagination

```bash
# Ask for smaller pages when each record is wide
curl -G "$SF_INSTANCE_URL/services/data/v62.0/query/" \
  --data-urlencode "q=SELECT Id, Name FROM Account" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN" \
  -H "Sforce-Query-Options: batchSize=500"

# Then follow the cursor until done
curl "$SF_INSTANCE_URL/services/data/v62.0/query/01gxx000000MYzz-2000" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN"
```

- Pages hold up to 2,000 records; `batchSize` accepts 200–2,000 and is a request, not a guarantee.
- **Every page is one API call.** 200,000 records at the default page size is 100 calls; the same export through Bulk 2.0 is a handful (`bulk.md`). Count before you loop.
- `OFFSET` maxes out at 2,000 and is not a pagination strategy — it re-executes the query each time. Page with `nextRecordsUrl`, or key-set paginate on `Id` (`WHERE Id > :lastId ORDER BY Id LIMIT 2000`), which stays correct even while records are being inserted.
- Query locators expire. A loop that pauses for a long batch job comes back to an invalid `nextRecordsUrl`; restart from a key-set filter instead.

## SOSL (Text Search)

SOQL scans; SOSL searches the index. When the user says "find anything mentioning Acme", it is SOSL.

```bash
curl -G "$SF_INSTANCE_URL/services/data/v62.0/search/" \
  --data-urlencode "q=FIND {Acme*} IN NAME FIELDS RETURNING Account(Id,Name), Lead(Id,Company)" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN"
```

- Search groups: `ALL FIELDS`, `NAME FIELDS`, `EMAIL FIELDS`, `PHONE FIELDS`, `SIDEBAR FIELDS`. Narrow the group and the search gets both faster and more precise.
- Trailing wildcard `*` and single-character `?` are supported; a **leading** wildcard is not — which is the whole reason SOSL is fast.
- Quoted phrases match exactly: `FIND {"John Smith"}`. Unquoted terms are OR'd.
- Reserved characters (`? & | ! { } [ ] ( ) ^ ~ * : \ " ' + -`) must be escaped with a backslash inside the braces.
- SOSL returns a capped set per object and is not a bulk export tool; use it to find the ids, then SOQL for the fields.

## Deleted and Archived

- `queryAll/` sees records in the recycle bin and archived activities: `SELECT Id, IsDeleted FROM Account WHERE IsDeleted = true`. Plain `query/` never returns them.
- The recycle bin holds deleted records for a limited retention window, after which they are gone and only `getDeleted` (within its 30-day window) can tell you they existed (`sync.md`).
- Old Tasks and Events get archived and stop appearing in normal queries — a "missing activity history" bug that is not a bug.

## Building Queries Safely

Concatenating user input into a SOQL string is injectable the same way SQL is. A value of `' OR Name != '` turns a filter into a full export.

- Bind parameters where the client supports them; otherwise escape single quotes and backslashes in every interpolated value.
- Whitelist field and object names against `describe` output — they cannot be escaped, only validated.
- Cap every generated query with a `LIMIT`. An unbounded query against a large object is how one bad filter becomes a 120-second timeout and a chunk of the day's API allocation.

## Query Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| `SELECT *` | Not valid SOQL; `FIELDS(ALL)` is capped at 200 records | Name the fields you need — narrower rows also page faster |
| Filtering on a formula field | Some formula fields are not filterable, and none are indexed | Filter on the underlying fields, or ask the admin for a real field |
| `WHERE OwnerId = 'name'` | Owner is an id, not a name | Sub-select the User by name, or store the id |
| Counting with `totalSize` after a `LIMIT` | `totalSize` reflects the limited set once a LIMIT is applied | Run `SELECT COUNT()` separately for a true count |
| Paginating a live table with `OFFSET` | Inserts shift the window, so rows are skipped or repeated | Key-set pagination on `Id` |
| Assuming a missing field means empty | Nulls are omitted from JSON, and so are fields the user cannot read | Check `describe` and FLS before writing "no data" |
| One query per parent record | 500 parents is 500 API calls | One query with `WHERE ParentId IN (...)`, then group in your code |

**When a query proves worth keeping** — it took work to make selective, it is one the user asks for repeatedly, or it replaces a report that hit its row ceiling — add a row to `## Saved Queries` in `~/Clawic/data/salesforce-api-integration/memory.md` with its purpose and whether the filter is selective. If a query's failure taught you something about the org (an unindexed field, a formula that cannot be filtered), that belongs in `## Gotchas` instead.
