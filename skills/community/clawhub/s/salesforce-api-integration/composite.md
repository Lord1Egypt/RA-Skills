# Composite — Many Operations, One Round Trip

**Before building a chained payload**, read `## Schema Map` and `## Gotchas` in `~/Clawic/data/salesforce-api-integration/memory.md`, and open any `artifacts/` entry the `## Boxes` index names for this operation — a working chain for the same objects may already be written down.

Five different resources share the word "composite" and they differ on the two things that matter: **what counts as one API call** and **what rolls back together**. Pick on those, not on convenience.

**Contents:** [Pick by Transaction Boundary](#pick-by-transaction-boundary) · [What Actually Saves Allocation](#what-actually-saves-allocation) · [sObject Collections](#sobject-collections) · [Composite](#composite-chained-dependent-calls) · [Batch](#batch-independent-calls) · [sObject Tree](#sobject-tree) · [Composite Graph](#composite-graph) · [Reading Composite Errors](#reading-composite-errors) · [Composite Traps](#composite-traps)

## Pick by Transaction Boundary

| Need | Resource | Ceiling | Rollback unit |
|---|---|---|---|
| Same operation on many records of one object | **sObject Collections** | 200 records | All or per-record, your choice |
| Later calls need ids from earlier ones | **Composite** | 25 subrequests | All 25, or none of them, via `allOrNone` |
| Unrelated calls, just fewer round trips | **Batch** | 25 subrequests | Nothing — each stands alone |
| A parent and its children created together | **sObject Tree** | 200 records total | The whole payload |
| Many independent object graphs in one request | **Composite Graph** | 500 nodes | **Per graph** — the only resource with independent rollback units |
| Anything above 200 records of one object | Bulk 2.0 (`bulk.md`) | — | Per chunk |

## What Actually Saves Allocation

- **Collections and Tree collapse many records into one API call.** 200 Accounts created for the price of one request is the reason Collections exists.
- **Composite and Batch save round trips, not allocation.** Their subrequests count individually against the daily limit — the win is latency and transactional grouping, not budget. A loop of 25 calls rewritten as one composite call is the same allocation cost with a fraction of the wall-clock time.

State which of the two you are buying when you recommend one. Confirm against `/limits` before and after a large run if the number matters (`limits.md`).

## sObject Collections

Up to 200 records, one operation, one call. Mixed object types are allowed in the same payload via `attributes.type`.

```bash
curl -X POST "$SF_INSTANCE_URL/services/data/v62.0/composite/sobjects" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN" -H "Content-Type: application/json" \
  -d '{"allOrNone": false,
       "records":[
         {"attributes":{"type":"Account"},"Name":"Account 1"},
         {"attributes":{"type":"Account"},"Name":"Account 2"}]}'
```

- `PATCH` the same endpoint to update (each record needs `Id`), `DELETE ...?ids=001xxx,001yyy&allOrNone=false` to delete, `POST /composite/sobjects/<Object>` with an `ids` array to read many at once.
- Upsert by external id: `PATCH /composite/sobjects/<Object>/<ExternalIdField>` — the idempotent form, and the right default for anything that might be retried.
- **The response is always HTTP 200**, carrying an array of `{id, success, errors}` in request order. A caller that branches on the HTTP status alone reports total success on a payload where half the records failed.
- `allOrNone: true` rolls the whole batch back on the first error, and every other record reports `PROCESSING_HALTED`. Default it from `config.yaml` (`all_or_none`, default true) and override deliberately: a nightly sync usually wants `false` and a failure file; a financial write usually wants `true`.

## Composite (chained, dependent calls)

```bash
curl -X POST "$SF_INSTANCE_URL/services/data/v62.0/composite" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN" -H "Content-Type: application/json" \
  -d '{"allOrNone": true,
       "compositeRequest":[
         {"method":"POST","url":"/services/data/v62.0/sobjects/Account",
          "referenceId":"newAccount","body":{"Name":"Acme Corp"}},
         {"method":"POST","url":"/services/data/v62.0/sobjects/Contact",
          "referenceId":"newContact","body":{"LastName":"Ruiz","AccountId":"@{newAccount.id}"}},
         {"method":"GET","url":"/services/data/v62.0/sobjects/Contact/@{newContact.id}",
          "referenceId":"readBack"}]}'
```

- `@{referenceId.field}` substitutes any field from an earlier response, including into a URL. That is how you create a parent and use its id without a round trip.
- Subrequests execute **in order**, so an id can only be referenced after it exists.
- `referenceId` values must be unique within the request and are how you find each result in the response.
- Each subrequest may carry its own `httpHeaders`, which is where a per-record `Sforce-Auto-Assign: FALSE` goes.
- 25 subrequests is the ceiling and it is not negotiable: a 30-record dependent chain is two composite calls with the ids carried across.

## Batch (independent calls)

`POST /composite/batch` with a `batchRequests` array of `{method, url}` — note the URLs are version-relative (`v62.0/sobjects/Account/001xxx`), which is the most common copy-paste error between the two resources.

No transaction: each subrequest succeeds or fails alone, `hasErrors` on the response tells you whether to inspect. Use it to fetch several unrelated things in one trip; never use it for a chain, because it cannot reference earlier results.

## sObject Tree

One nested payload creating a parent and its children:

```bash
curl -X POST "$SF_INSTANCE_URL/services/data/v62.0/composite/tree/Account" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN" -H "Content-Type: application/json" \
  -d '{"records":[{"attributes":{"type":"Account","referenceId":"ref1"},"Name":"Parent Account",
        "Contacts":{"records":[
          {"attributes":{"type":"Contact","referenceId":"ref2"},"LastName":"Ruiz"},
          {"attributes":{"type":"Contact","referenceId":"ref3"},"LastName":"Jones"}]}}]}'
```

- 200 records total across the whole nested structure, counted as one API call.
- **Create only** — no update, no upsert. It is the tool for seeding related data, not for syncing it.
- The child key is the child *relationship* name (`Contacts`, `Shipments__r`), and it is the same trap as in SOQL: it is not the object name.
- The response maps every `referenceId` to its new id; keep them, because that mapping is the only link back to your source rows.
- Any failure fails the whole payload, with the errors keyed by `referenceId`.

## Composite Graph

```json
{"graphs":[
  {"graphId":"acme","compositeRequest":[ ...up to 500 nodes... ]},
  {"graphId":"globex","compositeRequest":[ ... ]}]}
```

Each graph commits or rolls back on its own. That makes it the right resource for "load 40 customers, each with their contacts and opportunities, and do not let one bad customer take down the other 39" — the case where composite's single `allOrNone` is too coarse and Collections cannot express the dependencies.

## Reading Composite Errors

Every one of these resources returns HTTP 200 for a request that was well-formed, whatever happened to the records inside it. The rule is the same everywhere: **branch on the per-subrequest `statusCode` / `success` field, never on the outer status.**

| Response detail | Meaning |
|---|---|
| `success: false` with `errors[]` | That record failed; the array carries `statusCode`, `message`, `fields` |
| `PROCESSING_HALTED` | `allOrNone` was true and something else failed — this record is collateral |
| `statusCode: 400` inside `compositeResponse` | That subrequest failed; earlier ones may already be rolled back |
| `hasErrors: true` (batch) | At least one subrequest failed; the rest still happened |

Take the `errorCode` to `errors.md`, never the HTTP status.

## Composite Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Checking only the HTTP status | It is 200 even when every record failed | Inspect `success` per record |
| Using composite to save API allocation | Subrequests count individually | Collections for volume, composite for dependencies |
| Absolute URLs in a batch request | Batch takes version-relative URLs, composite takes absolute ones | Copy the shape from the right example |
| A dependent chain longer than 25 | Hard ceiling | Split, carrying ids forward |
| Tree for updates | Create-only resource | Collections upsert |
| `allOrNone: true` on a nightly sync | One bad row discards the whole batch every night | `false`, plus a failure list you actually read |
| Assuming children come back in order | Results are keyed by `referenceId`, not position | Map by `referenceId` |

**When a composite payload takes real work to get right** — a chained onboarding sequence, a graph that loads a customer and everything under it — save it as `artifacts/<kebab-name>.md` with a line on when to read it, and add its `## Boxes` line in `memory.md` the same turn. Rebuilding a 25-step chain from scratch costs an afternoon; reading one costs a minute.
