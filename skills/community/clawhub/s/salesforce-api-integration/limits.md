# Limits — Allocation, Concurrency, and Budgeting a Job

**Before any job that could consume a noticeable share of the day**, read `## Limits Observed` in `~/Clawic/data/salesforce-api-integration/memory.md`: the org's allocation, its typical daily usage and the last storage reading are there, and they turn "is this safe" into arithmetic.

**Contents:** [Read the Org, Not the Documentation](#read-the-org-not-the-documentation) · [What Counts as a Call](#what-counts-as-a-call) · [The Daily Allocation](#the-daily-allocation) · [Concurrency](#concurrency) · [Governor Limits Are a Different Thing](#governor-limits-are-a-different-thing) · [Storage](#storage) · [Budgeting a Job](#budgeting-a-job) · [When the Ceiling Is Hit](#when-the-ceiling-is-hit) · [Watching It](#watching-it)

## Read the Org, Not the Documentation

Allocations depend on edition, license count and add-ons. Every published number is a shape, not a value; the org states its own:

```bash
curl "$SF_INSTANCE_URL/services/data/v62.0/limits/" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN"
```

The response is a map of `{"Max": n, "Remaining": n}` pairs. The ones that decide plans: `DailyApiRequests`, `DataStorageMB`, `FileStorageMB`, the Bulk v2 job and file-storage entries, `DailyAsyncApexExecutions`, and the streaming/event entries when the org uses them.

`Remaining` against a **rolling 24-hour window**, not a midnight reset. An allocation spent by a 3 a.m. load is still spent at 2 a.m. the next night. That single fact changes how loads get scheduled.

## What Counts as a Call

| Operation | Calls |
|---|---|
| One REST create, read, update, delete | 1 |
| A SOQL query | 1 per page — 200,000 records at 2,000 per page is 100 |
| sObject Collections, up to 200 records | **1** |
| sObject Tree, up to 200 records | 1 |
| Composite or Batch with 25 subrequests | Subrequests count individually — it buys latency, not allocation (`composite.md`) |
| A Bulk 2.0 job, any volume | Roughly 5-10: create, upload, close, polls, result downloads |
| A describe | 1, or ~0 with `If-Modified-Since` returning 304 (`metadata.md`) |
| `/limits` itself | 1 — cheap, but not free inside a loop |
| Apex running inside the org | 0 against the API allocation; it has governor limits instead |
| Platform Events and CDC delivered to a subscriber | Counted against event allocations, not the API request limit (`sync.md`) |

The gap between the second row and the fourth is the whole reason Rule 3 exists: the same 50,000 records cost 50,000 calls one way, 250 another, and about 8 a third.

## The Daily Allocation

The shape is *per-license, with a floor*: a per-user-license allotment multiplied by licensed users, plus a minimum that keeps small orgs usable. Developer Edition is a flat 15,000 per day. Professional Edition needs the API add-on before any of this applies at all.

Three consequences that matter more than the number:

- **The allocation is org-wide and shared.** Your job competes with the marketing tool, the ERP sync, the phone system and everything an admin left running. "We have plenty" is only true at the moment you looked.
- **Adding users adds allocation.** An org that lost seats in a layoff lost API budget too — a familiar cause of an integration that suddenly hits the ceiling without changing.
- **It resets by rolling window.** There is no "start of day" to wait for.

## Concurrency

At most 25 concurrent synchronous requests running longer than 20 seconds, org-wide. Beyond that, new long requests are rejected while short ones keep flowing.

- The usual cause is not traffic but *slowness*: unselective queries that each take 30 seconds (`soql.md`). Make them selective and the concurrency problem disappears without touching the client.
- Parallel workers hitting the ceiling all retry at once. Backoff with jitter, and cap the worker count deliberately rather than discovering the cap.
- Bulk jobs are asynchronous and do not consume this budget — one more argument for Bulk at volume.

## Governor Limits Are a Different Thing

Two independent ceilings, constantly confused:

| | API limits | Governor limits |
|---|---|---|
| Scope | The org, per rolling day | One Apex transaction |
| Counts | Requests you send | SOQL (100), DML statements (150), rows retrieved (50,000), CPU (10s sync) inside the org's code |
| You hit it by | Making too many calls | Sending records into an object whose triggers are inefficient |
| Symptom | `REQUEST_LIMIT_EXCEEDED` | `CANNOT_INSERT_UPDATE_ACTIVATE_ENTITY` wrapping a `System.LimitException` |
| Fix | Fewer, bigger calls | Smaller chunks, or the org's code gets fixed |

**Bigger batches help the first and hurt the second.** That tension is the real reason batch size is a decision: your DML reaches the org's triggers in chunks of up to 200 records, and a trigger with a query per record fails at 101. When both pressures are live, the answer is Bulk 2.0 (few API calls) plus a conversation about the trigger.

## Storage

- Most records count as **2 KB** regardless of how many fields they carry — a million skinny rows is about 2 GB, and field count is not the lever.
- Files, attachments and content versions count against a separate file-storage allocation (`files.md`).
- Deleted records still occupy storage while they sit in the recycle bin. Freeing space immediately means hard delete (`bulk.md`), which is irreversible.
- Storage overage does not fail reads — it fails **writes**, which is how a migration dies at 80% completion. Check `DataStorageMB` before a load that adds millions of rows, and write the reading into `## Limits Observed` in `memory.md`.

## Budgeting a Job

State this before running anything large:

```
calls = ceil(records ÷ batch_size) + polls + result_downloads
share = calls ÷ Remaining from /limits
```

- Collections: `batch_size` 200. Bulk: the whole job is a handful of calls. Per-record loops: `batch_size` 1, which is the number that stops the argument.
- Above ~10% of `Remaining`, say so explicitly before starting. Above ~50%, it is a scheduled off-hours job, not something to run mid-conversation.
- Add the export side: a 500,000-record extract paged through SOQL is 250 calls; through Bulk query it is under ten.

## When the Ceiling Is Hit

1. **Stop.** Retrying `REQUEST_LIMIT_EXCEEDED` consumes the allocation you are waiting for and extends the outage for every other integration in the org.
2. Report `Remaining` and the rolling-window nature to the user in one line — the recovery is time, not action.
3. Find the consumer. Salesforce's own API usage reporting, and Event Monitoring where the org has it, attribute calls to Connected Apps and users; the answer is very often a third-party tool polling every minute.
4. Fix the pattern before asking for more: per-record loops → Collections, polling → CDC or a longer interval, repeated describes → caching, repeated queries → one query with `IN`.
5. Only then, a temporary increase through Salesforce Support — which is a request with a business case and a lead time, not a setting.

Notification thresholds are worth setting once: Salesforce can email an admin when API usage crosses a percentage of the allocation. It costs nothing and it is the difference between noticing at 80% and finding out at 100%.

## Watching It

Put a weekly usage check in the `## Due` table of `memory.md`, and a storage check quarterly. Each is one `/limits` call.

**After every check, and after any job that moved the numbers**, overwrite the rows in `## Limits Observed` in `memory.md`: allocation, typical use, peak, storage percentage, each with the date it was read. Overwrite rather than append — a stale allocation from before the last license change is worse than no number, because it will be trusted.
