# Bulk API 2.0 — Volume Loads and Exports

**Before running a load**, read `loads/<year>.md` if the `## Boxes` index names it — a load of the same object has probably run before, and its row counts, mapping and failure list are the fastest way to predict this one. Read `## Gotchas` too: lock contention and validation-rule surprises are recorded there.

**Contents:** [When Bulk Is the Right Answer](#when-bulk-is-the-right-answer) · [2.0 vs 1.0](#20-vs-10) · [The Job Lifecycle](#the-job-lifecycle) · [CSV Rules That Decide Success](#csv-rules-that-decide-success) · [Lookups Without Salesforce Ids](#lookups-without-salesforce-ids) · [Lock Contention](#lock-contention-the-signature-bulk-failure) · [Reading the Results](#reading-the-results) · [Bulk Query](#bulk-query-export) · [Hard Delete](#hard-delete) · [Limits](#limits) · [Bulk Traps](#bulk-traps)

## When Bulk Is the Right Answer

| Records | Path | API calls |
|---|---|---|
| 1 | sObject REST (`records.md`) | 1 |
| 2 – 200 | sObject Collections (`composite.md`) | 1 |
| 200 – `bulk_threshold` (default 5,000) | Collections in a loop | `ceil(n ÷ 200)` |
| Above `bulk_threshold`, or the source is already a CSV | **Bulk 2.0** | ~5-10 regardless of volume |
| Anything a human is waiting on, under ~2,000 | Collections | Synchronous errors beat a results file |

Bulk trades immediacy for allocation: the job runs asynchronously, you poll, and the errors arrive as a file. That is the correct trade above a few thousand records and the wrong one below it.

## 2.0 vs 1.0

Use 2.0 unless a named 1.0 feature is required.

| | Bulk 2.0 | Bulk 1.0 |
|---|---|---|
| Batching | Automatic — upload one file, Salesforce splits it | Manual, you create and track batches |
| Retries | Salesforce retries transient failures | Yours to implement |
| Processing mode | Parallel only | Parallel **or serial** |
| Query chunking | Automatic | Manual, via the PK chunking header |
| Hard delete | Supported (`hardDelete` operation) | Supported |

The one reason to reach back for 1.0 is **serial mode**, when parallel chunks keep colliding on the same parent records and sorting the file has not fixed it.

## The Job Lifecycle

Four calls, always in this order.

```bash
# 1. Create the job
curl -X POST "$SF_INSTANCE_URL/services/data/v62.0/jobs/ingest" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN" -H "Content-Type: application/json" \
  -d '{"operation":"upsert","object":"Account","externalIdFieldName":"ERP_Id__c",
       "contentType":"CSV","lineEnding":"LF"}'

# 2. Upload the data (the whole file, one PUT)
curl -X PUT "$SF_INSTANCE_URL/services/data/v62.0/jobs/ingest/750xx000000JOBID/batches" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN" -H "Content-Type: text/csv" \
  --data-binary @accounts.csv

# 3. Close it — this is what starts processing
curl -X PATCH "$SF_INSTANCE_URL/services/data/v62.0/jobs/ingest/750xx000000JOBID" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN" -H "Content-Type: application/json" \
  -d '{"state":"UploadComplete"}'

# 4. Poll until terminal
curl "$SF_INSTANCE_URL/services/data/v62.0/jobs/ingest/750xx000000JOBID" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN"
```

Operations: `insert`, `update`, `upsert` (with `externalIdFieldName`), `delete`, `hardDelete`.

States: `Open` → `UploadComplete` → `InProgress` → `JobComplete`, with `Failed` and `Aborted` as the other terminals. **`JobComplete` does not mean every record succeeded** — it means the job finished. The counts are in `numberRecordsProcessed` and `numberRecordsFailed`, and the failures are a separate download.

A job left `Open` holds its data and never processes. A polling loop that forgets step 3 waits forever on a job nobody started.

Poll with backoff — every few seconds at first, then slower. Polling a long job every 500 ms spends more API calls on the poll than on the load.

## CSV Rules That Decide Success

- **Column headers are field API names**, not labels. `Account Name` fails; `Name` works; a custom field is `Region__c`.
- **`lineEnding` must match the file**: `LF` for Unix, `CRLF` for anything produced on Windows or by Excel. A mismatch corrupts the last column of every row, which shows up as a validation error on a field you never touched.
- **Empty cell = leave unchanged. `#N/A` = set to null.** This is the single most consequential convention in the API, and it is the opposite of what most loaders assume.
- **Compound fields are not supported.** `BillingAddress`, `MailingAddress` and geolocation fields must be sent as their components: `BillingStreet`, `BillingCity`, `BillingState`, `BillingPostalCode`, `BillingCountry`.
- Quote any value containing a comma, quote or newline, doubling internal quotes (`"He said ""no"""`). A single unescaped newline shifts every subsequent row.
- Dates: `YYYY-MM-DD`; date-times: ISO 8601 with an explicit offset (`2026-06-15T14:30:00.000+0000`). A date-time without an offset is interpreted in the org's timezone, which moves records across day boundaries in reports.
- Booleans are `true`/`false`; picklists take the API value, not the label.
- UTF-8, no BOM. A BOM turns the first column header into an unrecognized field.
- The file must include the fields required by the object *and* by the org's validation rules — the API applies no page-layout defaults (`records.md`).

## Lookups Without Salesforce Ids

A Bulk CSV can resolve a relationship through the parent's external id, which removes the entire "query for parent ids first" step:

```csv
LastName,Email,Account.ERP_Id__c
Ruiz,dana@acme.example,EXT-4471
```

The column is `<RelationshipName>.<ExternalIdField>` — the relationship name, not the object name (`Account` for the standard lookup, `Shipment__r` for a custom one). Every parent must already exist; unresolved keys fail those rows with `INVALID_CROSS_REFERENCE_KEY` and leave the rest loaded.

## Lock Contention (the signature Bulk failure)

Parallel chunks that touch the same parent record fight for its lock and lose: `UNABLE_TO_LOCK_ROW` on a fraction of rows, different rows each run.

Causes, in order of frequency: child records sharing a parent (Contacts under one Account), master-detail rollups recalculating, ownership changes cascading sharing recalculation, and two jobs against related objects running at once.

Fixes, in order to try:

1. **Sort the file by the parent id or parent external id.** Chunks are cut sequentially, so sorting puts one parent's children in one chunk and the contention disappears. This fixes most cases and costs one `sort`.
2. Run related jobs one at a time instead of in parallel.
3. Fall back to Bulk 1.0 serial mode.
4. For mass ownership changes, ask the admin to enable deferred sharing calculation for the window (`migration.md`).

Record the fix in `## Gotchas`: the same load will run again next quarter.

## Reading the Results

```bash
curl "$SF_INSTANCE_URL/services/data/v62.0/jobs/ingest/750xx000000JOBID/failedResults" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN"
```

Three downloads: `successfulResults`, `failedResults`, `unprocessedrecords`. Each is a CSV echoing your original columns plus `sf__Id` and, for failures, `sf__Error`.

- **Always download `failedResults`.** A job reported as complete with 4% failures is a silent data-quality incident otherwise.
- The failure file is a valid input file: fix the offending columns and re-upload it as a new job. With upsert this is safe to repeat.
- `unprocessedrecords` appears when a job was aborted or hit a limit mid-flight — those records were never attempted.
- Result files are retained for a limited window and then deleted with the job; download before you close the ticket.

## Bulk Query (export)

```bash
curl -X POST "$SF_INSTANCE_URL/services/data/v62.0/jobs/query" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN" -H "Content-Type: application/json" \
  -d '{"operation":"query","query":"SELECT Id, Name, ERP_Id__c FROM Account"}'

curl "$SF_INSTANCE_URL/services/data/v62.0/jobs/query/750xx000000JOBID/results?maxRecords=50000" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN"
```

- `operation: queryAll` includes deleted and archived records.
- Results paginate through the `Sforce-Locator` response header; pass it back as the `locator` parameter until the header comes back empty. Missing this is why an export "only returned the first chunk".
- Bulk 2.0 chunks large exports itself. The manual PK-chunking header belongs to Bulk 1.0 and is only needed there.
- A Bulk export of ten million rows still runs the SOQL: an unselective filter times out here too (`soql.md`).

## Hard Delete

`operation: "hardDelete"` bypasses the recycle bin. It requires the "Bulk API Hard Delete" user permission, cannot be undone, and is the only way to free storage immediately.

Gate it: state the exact record count, confirm explicitly, and refuse entirely when `safety_posture.hard_delete` is `forbidden`. Export the ids to `loads/<year>.md` first — after a hard delete, the only record that those rows existed is the one you wrote.

## Limits

- 150 MB per upload. Split larger files; the job accepts one PUT.
- Records are processed in chunks, so **Apex governor limits still apply per chunk** (≤200 records, 100 SOQL, 150 DML, 10s CPU). A trigger that is fine for one record can fail an entire load (`SKILL.md` Rule 5).
- Daily record ceilings for ingest are large but finite and vary by edition — read `/limits` rather than trusting a number in a document (`limits.md`).
- Concurrent query jobs are capped in the low tens per org; queued jobs wait rather than fail.

## Bulk Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Testing with 10 rows | Never crosses a 200-record chunk boundary, so governor and lock failures cannot appear | Rehearse with ≥1,000 rows in a sandbox (`SKILL.md` Rule 8) |
| Empty cells to clear fields | Means "unchanged"; the old values stay | `#N/A` |
| Excel-exported CSV with `lineEnding: LF` | Excel writes CRLF; the last column carries a stray `\r` | Set `lineEnding: CRLF`, or normalize the file |
| Assuming `JobComplete` means success | It means finished | Read `numberRecordsFailed`, download `failedResults` |
| Re-running the whole file after partial failure | Re-processes everything and duplicates on insert jobs | Re-upload the failure file, and use upsert so repeats are safe |
| Bulk-loading during business hours | Locks, sharing recalculation and trigger load hit real users | Off-hours window, agreed in advance |
| One giant job for related objects | Parents and children in flight together maximizes contention | One job per object, in dependency order (`migration.md`) |
| Leaving the job `Open` | Nothing processes and nothing errors | PATCH to `UploadComplete` |

**After every job**, append a row to `~/Clawic/data/salesforce-api-integration/loads/<year>.md`: date, object, operation, rows in, succeeded, failed, job id, and the one-line cause of the failures. Create the file and its `## Boxes` line in the same turn if it does not exist. If the failure taught you something about the org, add it to `## Gotchas`; if the mapping is one that will be reused, it belongs in `artifacts/mapping-<source>.md`.
