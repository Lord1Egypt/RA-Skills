# Apex Endpoints, Actions and Flows — Calling the Org's Own Logic

**Before calling a custom endpoint**, read `## Integrations` in `~/Clawic/data/salesforce-api-integration/memory.md` and any `artifacts/` entry the `## Boxes` index names for it: the contract of a custom endpoint exists nowhere else, because Salesforce publishes no schema for it.

**Contents:** [When the Standard API Is Not Enough](#when-the-standard-api-is-not-enough) · [Apex REST](#apex-rest) · [Invocable Actions](#invocable-actions) · [Flows](#flows) · [Anonymous Apex](#anonymous-apex) · [Async Jobs](#async-jobs) · [Governor Limits Inside Your Call](#governor-limits-inside-your-call) · [Callouts and Named Credentials](#callouts-and-named-credentials) · [Traps](#traps)

## When the Standard API Is Not Enough

Reach for org-side logic only for these; everything else is cheaper as standard REST.

| Situation | Why the standard API loses |
|---|---|
| An operation with no REST verb — undelete, merge, `Database.` options | There is no endpoint to call |
| A business transaction spanning more than 25 dependent steps | Composite's ceiling (`composite.md`) |
| Logic that must be identical for the UI and the integration | Duplicating it in your client guarantees drift |
| A payload shaped like the caller's domain, not Salesforce's | Otherwise the caller learns the Salesforce data model |
| Work that must survive the caller disconnecting | Queueable or Batch Apex, returning a job id |

The cost is real: an Apex endpoint is code somebody must test, deploy, version and own. A five-call composite that works is better than a custom endpoint nobody maintains.

## Apex REST

A class annotated as a REST resource is served at `"$SF_INSTANCE_URL/services/apexrest/<urlMapping>"` — a different base path from `/services/data/`, and it carries **no API version segment**.

```bash
curl -X POST "$SF_INSTANCE_URL/services/apexrest/orders/v1" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"customerKey":"EXT-4471","lines":[{"sku":"A-1","qty":2}]}'
```

- Same OAuth, same daily API allocation, same session rules as everything else. It is not a bypass.
- **Bulkify the contract.** An endpoint that accepts one record forces the caller into a per-record loop, which is the allocation problem from `SKILL.md` Rule 3 wearing a custom URL. Accept a list, return a per-item result array.
- Errors surface as an HTTP 500 with the exception message unless the class catches them and returns a structured body. An endpoint that returns 500 with a stack trace is an endpoint whose failures nobody can act on.
- The URL mapping is the version. There is no content negotiation, so `/orders/v1` and `/orders/v2` are two classes, and the old one stays until every caller has moved.
- Record the endpoint's contract — path, method, request shape, response shape, error shape, owner — in `artifacts/<kebab-name>.md`. It is the only documentation that will exist.

## Invocable Actions

The Actions API exposes standard operations, Flows and invocable Apex through one uniform shape, and it is the correct answer more often than people expect.

```bash
# Discover what this org exposes
curl "$SF_INSTANCE_URL/services/data/v62.0/actions/standard" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN"

# Describe one action's inputs before calling it
curl "$SF_INSTANCE_URL/services/data/v62.0/actions/standard/convertLead" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN"

# Invoke it
curl -X POST "$SF_INSTANCE_URL/services/data/v62.0/actions/standard/convertLead" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN" -H "Content-Type: application/json" \
  -d '{"inputs":[{"leadId":"00Qxx0000012345","convertedStatus":"Closed - Converted"}]}'
```

- `inputs` is always an array, and the response is an array of results in the same order — the API is bulk-shaped by design.
- Discover, then describe, then call. Action names and their input parameters vary by org and by release; the GET is one call and it removes all the guessing.
- Standard actions cover operations with no sObject verb (lead conversion, sending email, posting to Chatter). `.../actions/custom/apex/<ClassName>` and `.../actions/custom/flow/<FlowApiName>` cover what the org built.

## Flows

Only **autolaunched** flows can be invoked through the API — screen flows need a UI and will not appear in the actions list.

- Inputs are the flow's declared input variables; outputs come back only for variables marked available for output. A flow that "does nothing" through the API is usually a flow whose outputs were never exposed.
- A flow runs in the calling user's context and consumes the same per-transaction governor budget as everything else in that transaction.
- Flow versions are independent: invoking by API name runs the **active** version, which an admin can change without telling you. Record the flow's API name and owner in `## Integrations`, and treat a behaviour change with no code change on your side as a version change on theirs.

## Anonymous Apex

`POST /services/data/vXX.0/tooling/executeAnonymous/?anonymousBody=<url-encoded apex>` runs a block of Apex as the current user. It is the right tool for a genuine one-off — fixing 40 records, backfilling one field, kicking a stuck job.

It is the wrong tool for anything recurring: no test coverage, no version control, no review, and no record of what ran except what you write down. When an anonymous block changes data, paste the block into `loads/<year>.md` with the date and the row count it touched, with any credential replaced by its pointer.

## Async Jobs

Work started from the API that runs asynchronously — Batch Apex, Queueable, `@future` — returns a job id immediately. Poll `AsyncApexJob` for `Status`, `JobItemsProcessed`, `TotalJobItems` and `NumberOfErrors`:

```sql
SELECT Id, Status, JobItemsProcessed, TotalJobItems, NumberOfErrors, ExtendedStatus
FROM AsyncApexJob WHERE Id = '707xx0000012345'
```

Async executions have their own daily allocation, separate from API requests (`limits.md`). A job that "never starts" is often queued behind the org's own scheduled work, not broken.

## Governor Limits Inside Your Call

When you POST to an Apex endpoint or invoke an action, **your request becomes an Apex transaction** and inherits the whole budget: 100 SOQL queries, 150 DML statements, 50,000 rows retrieved, 10 seconds of CPU synchronously.

Consequences for the caller:

- The endpoint's maximum safe payload is a property of its code, not of the API. Ask for it, or discover it in a sandbox with a realistic batch, and record it in `## Integrations`.
- A `System.LimitException` comes back as a 500 or as a wrapped `CANNOT_INSERT_UPDATE_ACTIVATE_ENTITY`; halving the batch size is the diagnostic that confirms it (`errors.md`).
- Splitting the payload is the caller's fix; bulkifying the code is the org's. Both are usually needed.

## Callouts and Named Credentials

When the org's Apex calls **out** to your system:

- Up to 100 callouts per transaction, with a cumulative timeout around 120 seconds. A per-record callout inside a trigger is the classic design that dies at volume.
- Callouts cannot follow uncommitted DML in the same transaction — the org's code must go asynchronous, which is why so many integrations arrive minutes later than expected.
- **Named Credentials are where the endpoint and its secret belong.** They keep the URL and the credential out of the code and out of custom settings, and they are the answer whenever someone proposes storing an API key in a custom setting or a hardcoded string. Referencing one from your notes is safe; the credential itself never appears anywhere under `~/Clawic/data/`.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Single-record Apex endpoint | Forces callers into per-record loops | Accept and return arrays |
| Calling an action without describing it first | Input names and requiredness vary by org and release | One GET on the action, then call |
| Assuming `/services/apexrest/` is versioned | It is not; the URL mapping is the only version | Version in the path, retire deliberately |
| Treating a flow as stable | Admins activate new versions silently | Record the flow name and owner in `## Integrations`; suspect version changes first |
| Anonymous Apex as a recurring job | No tests, no history, no review | A deployed class, or a scheduled job |
| Retrying a 500 from an Apex endpoint | It may have committed part of its work | Make the endpoint idempotent on an external key, then retry freely |
| Expecting an async job's result in the response | You get a job id | Poll `AsyncApexJob` |

**When a custom endpoint, action or flow enters the picture**: add its row to `## Integrations` in `memory.md` (name, direction, mechanism, objects, owner) and put its contract — path, payload, error shape, safe batch size, owner — in `artifacts/<kebab-name>.md` with its `## Boxes` line in the same turn. A destructive or data-changing anonymous Apex block goes in `loads/<year>.md`.
