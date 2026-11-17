# Sync — Keeping Something Else in Step With the Org

**Before changing or debugging a sync**, read `## Integrations` in `~/Clawic/data/salesforce-api-integration/memory.md` and open the design in `artifacts/` if the `## Boxes` index names one: direction, mechanism, objects, watermark and failure handling are written there.

**Contents:** [Pick the Mechanism](#pick-the-mechanism) · [Polling on SystemModstamp](#polling-on-systemmodstamp) · [The Replication API](#the-replication-api) · [Deletes, the Hard Part](#deletes-the-hard-part) · [Change Data Capture](#change-data-capture) · [Platform Events](#platform-events) · [Outbound Messages](#outbound-messages) · [Reconciliation](#reconciliation) · [Sync Traps](#sync-traps)

## Pick the Mechanism

| Need | Mechanism | Latency | Costs |
|---|---|---|---|
| A warehouse that can be minutes behind | **Poll on `SystemModstamp`** | Your interval | API calls per poll |
| Near-real-time replication of record changes | **Change Data Capture** via the Pub/Sub API | Seconds | Event allocation; a subscriber you must keep up |
| The org wants to tell you something that is not a record change | **Platform Events** | Seconds | Event allocation; a custom event definition |
| A legacy endpoint that already exists and works | **Outbound Messages** | Seconds to minutes | SOAP, and a retry model you do not control |
| Full refresh of everything, nightly | **Bulk query** (`bulk.md`) | Hours | Almost no API allocation |
| Anything else | Poll. It is boring, cheap to reason about, and recovers from any outage by widening the window | | |

Default when nothing is stated: polling. Streaming is the better answer only when someone is on call for the subscriber.

## Polling on SystemModstamp

`LastModifiedDate` does not move for every system-level change. `SystemModstamp` does, and it is indexed. Filtering on the wrong one produces a sync that works for months and then silently stops carrying a class of updates.

```sql
SELECT Id, Name, SystemModstamp
FROM Account
WHERE SystemModstamp > 2026-07-26T02:00:00Z AND SystemModstamp <= 2026-07-26T02:15:00Z
ORDER BY SystemModstamp
```

The pattern that survives contact with production:

1. **Store a watermark**, the high-water `SystemModstamp` you have fully processed — not "now minus the interval". A run that fails must not advance it.
2. **Bound both ends.** An open-ended `>` window against a busy object returns a moving target; a closed window is reproducible and re-runnable.
3. **Overlap by a minute or two.** Clock skew and transaction commit times mean a record can be committed with a timestamp slightly behind the query you already ran. Overlap costs duplicate rows, which upsert absorbs for free; a gap costs data.
4. **Order by `SystemModstamp`** and page with a key-set filter, not `OFFSET` (`soql.md`).
5. **Make the downstream write idempotent** on the Salesforce id or your external id — the overlap in step 3 guarantees repeats.
6. Advance the watermark to the window's *end*, only after the batch is committed downstream.

Interval: the shortest that finishes comfortably before the next one starts. A poll that takes 12 minutes on a 15-minute schedule has no headroom for a busy day, and overlapping runs of the same sync are how the same records get processed twice in parallel.

## The Replication API

Purpose-built for "what changed", and cheaper than a query on high-volume objects:

```bash
curl -G "$SF_INSTANCE_URL/services/data/v62.0/sobjects/Account/updated/" \
  --data-urlencode "start=2026-07-26T02:00:00Z" \
  --data-urlencode "end=2026-07-26T02:15:00Z" \
  -H "Authorization: Bearer $SF_ACCESS_TOKEN"
```

- Returns `ids[]` plus **`latestDateCovered`** — use that value as your next watermark rather than your own `end`, because it is the point Salesforce guarantees it has fully processed.
- The window is limited to roughly the last 30 days and start/end must be at least a minute apart. A subscriber down for longer than the window cannot catch up this way and needs a full re-extract.
- It returns ids only: you still fetch the records, so it pays off when the change rate is a small fraction of the object.

## Deletes, the Hard Part

A polled query cannot see what is gone. Three options, in order of reliability:

1. **`getDeleted`** — the same shape as `getUpdated`, returning `deletedRecords[]` with their deletion dates and `earliestDateAvailable`. Same ~30-day ceiling.
2. **CDC delete events** — real-time, but bounded by 72-hour replay retention.
3. **Periodic reconciliation** — compare id sets between systems and treat the difference as deletions. Slow, expensive, and the only method that catches everything, including records deleted while every mechanism was down.

A record deleted longer ago than the replication window is invisible to every API. If nothing was watching, the only recovery is reconciliation.

Soft signals matter too: a record removed from the integration user's *sharing* looks exactly like a delete from the outside. Before deleting downstream, confirm with `queryAll` — if the record comes back with `IsDeleted = false`, you lost access, you did not lose the record.

## Change Data Capture

Salesforce publishes create, update, delete and undelete events for objects the admin has enabled, and you subscribe through the **Pub/Sub API** (gRPC). The older CometD/Streaming path is legacy; new work goes to Pub/Sub.

- **Replay id** is the cursor: `-1` for new events only, `-2` to start from the earliest retained event, or a stored replay id to resume exactly where you stopped. Persist it with the same discipline as a watermark.
- **72-hour retention.** A subscriber down over a long weekend cannot resume — it must fall back to a `SystemModstamp` catch-up query for the gap and then re-subscribe with `-1`. Write that fallback *before* going live; it is the procedure everyone discovers at the worst moment.
- **Gap events** arrive when Salesforce could not include the full change payload. They carry the record id and the change type but not the fields: treat one as "re-fetch this record", not as an error.
- Update events carry **only the changed fields** plus the header. Downstream code that expects a whole record will write nulls over everything else.
- Events are per-object channels; ordering is guaranteed within a channel, never across two. A Contact event can arrive before the Account event that created its parent — the consumer must tolerate it, usually by re-fetching or by deferring.
- Enablement is per object and is a Setup change, not an API call. Ask before designing around it.

## Platform Events

For messages the org wants to emit that are not record changes: "order shipped", "credit check finished".

- Publish from Apex, Flow, or the API by inserting into the event object (`Order_Shipped__e`); subscribe through Pub/Sub the same way as CDC.
- **Publish behaviour matters**: publish-after-commit only fires if the transaction commits, publish-immediately fires even if it later rolls back. The second produces events for records that do not exist — pick deliberately.
- Delivery and publishing allocations are separate from the API request limit and are consumed by every subscriber, so three consumers of one event cost three deliveries (`limits.md`).
- Same 72-hour replay retention as CDC.

## Outbound Messages

Workflow-era, still everywhere: the org POSTs a SOAP envelope to your endpoint when a record meets criteria.

- Retries for about a day with backoff, then the message is dropped. Your endpoint must return the expected acknowledgement or the org will keep resending.
- Messages may arrive out of order and more than once. Idempotent handling is mandatory, not a nicety.
- The envelope carries a session id scoped to the integration user, which is a credential — never log the raw envelope.
- Fine to keep if it works. Not the choice for anything new: CDC gives ordering, replay and a supported client.

## Reconciliation

Whatever the mechanism, schedule a comparison. It is the only thing that catches the class of bug where the sync reports success and carries nothing.

- Cheap version: `SELECT COUNT() FROM <Object> WHERE SystemModstamp = LAST_N_DAYS:7` on both sides, compared weekly.
- Real version: Bulk-export ids plus `SystemModstamp` and diff against the target monthly. A few API calls for a full answer.
- Put the cadence in the `## Due` table of `memory.md`, with the last run date. An unscheduled reconciliation happens once, during the incident it would have prevented.

## Sync Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| `LastModifiedDate` as the watermark | Misses system-level updates, silently | `SystemModstamp` |
| Watermark = "now minus interval" | A failed run loses its window forever | Store the high-water mark, advance only on success |
| No overlap between windows | Commit-time skew drops records at the boundary | Overlap a minute or two; upsert absorbs the repeats |
| Advancing the watermark before the downstream commit | A crash between the two loses the batch | Advance last |
| Ignoring deletes | The target grows forever and diverges quietly | `getDeleted`, CDC deletes, or reconciliation |
| Treating a CDC update as a full record | Only changed fields are present | Merge by field, or re-fetch |
| Assuming cross-object event ordering | Guaranteed per channel only | Tolerate out-of-order; re-fetch parents |
| No plan for a subscriber down past 72 hours | Replay is gone and the resume silently starts from "now" | Written catch-up procedure, rehearsed once |
| Polling every minute "to be safe" | Burns the daily allocation on empty results | Match the interval to how fast anyone actually needs it |

**When a sync is designed, changed or repaired**: write the row in `## Integrations` (name, direction, mechanism, objects, owner) and keep the full design — watermark, window, failure handling, catch-up procedure, first limit it meets — in `artifacts/<kebab-name>.md`, with its `## Boxes` line added in the same turn. Put the reconciliation cadence in `## Due`. A gap whose cause you found goes in `## Gotchas`.
