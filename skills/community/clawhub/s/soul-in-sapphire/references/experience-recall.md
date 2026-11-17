# Bounded emotion-linked experience recall

## Schema and meaning

The September 2026 read-only audit found these actual routes:

```text
mem: Name / Content / Tags / Source; no event relation
events: Name / context / when / source / link
emotions.event -> events       (single_property)
state.event -> events          (single_property)
events.emotions -> emotions    (independent single_property)
events.state -> state          (independent single_property)
journal: body / mood_label / intent; no event relation
```

`emostate_tick.js` writes the reverse edges only. Single-property relations do
not automatically populate the independent event-side properties. Empty
`events.emotions`/`events.state` is not evidence of an unrecorded experience.
Query each child data source with `event relation contains <event-page-id>`.
Merge actual forward-only legacy edges by page ID, preserving edge provenance.

The reader rechecks the configured schemas on each invocation. Wrong relation
targets are not queried; pages outside the configured data source are withheld.
Absent/incompatible old fields, conflicting edges and truncated inline relation
values are reported, not silently upgraded to the current schema. Notion's
integration visibility still limits what any reader can observe.

`ltm_search.js` remains the existing mem Name/Content CLI. Its success says nothing
about emotional joins. Do not join mem or journal to an event by matching dates,
similar prose, or tags. Tags and first-person emotional prose retain their own
meaning, but are not a measured axis/level pair. A new explicit mem relation
would be a separately designed schema/writer change, not a bulk migration needed
for this event reader.

## CLI and output

```bash
node scripts/experience_recall.js --query "remembered experience" \
  --events-dsid <EVENTS_DS_ID> --emotions-dsid <EMOTIONS_DS_ID> --state-dsid <STATE_DS_ID>
```

Replace `--query` with `--event-id <EVENT_PAGE_ID>` for direct retrieval or
`--state-id <STATE_PAGE_ID>` to follow a known state's actual event relation.
Exactly one selector is required. Queries filter Name/context server-side;
no unfiltered database scan is used. A direct known-source lookup is not evidence
that search worked; verify the query route separately.

| Limit | Default | Maximum |
| --- | --- | --- |
| `--limit` events | 3 | 5 |
| `--linked-limit` rows per event/lane | 5 | 10 |
| `--max-requests` API requests | 32 | 64 |
| `--text-limit` characters per field | 2000 | 4000 |
| `--total-text-limit` total field-text characters | 24000 | 48000 |

Each schema/page/query call counts against the same request budget, including
failed calls. No automatic query or property pagination is performed. `has_more`
and clipped content are explicit diagnostics. The total text budget covers field
values, not JSON keys, identifiers, or diagnostics. `state_json` is returned as
bounded recorded text, not recalculated or presented as the current state.

Output contains experience fields, event time and source, actual emotion
axis/level/comment/need/coping, historical state fields, page IDs/URLs, relation
evidence, retrieval time, missing/truncated field lists and diagnostics.
`temporal_scope=recorded_at_experience_not_current` applies to every result.

- `complete`: the bounded result has no detected schema, link, field or budget
  gaps. This is not a full-corpus coverage or cognitive-use claim.
- `no_match`: the bounded filtered query returned no candidates without errors.
- `partial`: some context is available, or a source/link/field gap was detected.
  `ok:true` with `complete:false` is intentional for readable incomplete records.
- `error`: request/schema response failures prevented any event result.
- Request failures or request-budget exhaustion set `ok:false` and CLI exit 1,
  even when another lane succeeded. Failure in emotions is not masked by state.

`no_linked_records` means no rows were observable through the checked edges; it
does not establish whether data was never saved, unlinked, or hidden by access.
`conflicting_relation` preserves the observed forward edge but marks the result
incomplete. No repair writes, automatic retries of writers or invented emotions.

## Ambient producer and consumer

The dice probabilities, cadence and shelf choices stay unchanged. Notion
candidates now carry `affect_context`, bounded recorded fields and a source
locator in addition to the short preview:

- State: recorded mood/intent/reason/state text, event IDs and relation status.
- Journal: recorded mood/intent/body/future, explicitly a journal self-report.
- Mem: recorded Content/Tags/Source/CreatedAt/Confidence, explicitly without a
  verified event join. Do not flatten tags/prose into a generic neutral fact.

Per staged field: 1200 text characters, or 20 list entries of 200 characters;
event references: 5. Truncation/missing fields are labeled. Candidate files are
written owner-readable/writable. Older version-1 candidates remain readable.

Read a live candidate without rolling or consuming:

```bash
node scripts/read_ambient_recall.js --file <staged.json>
node scripts/read_ambient_recall.js --file <staged.json> --resolve \
  --events-dsid <EVENTS_DS_ID> --emotions-dsid <EMOTIONS_DS_ID> --state-dsid <STATE_DS_ID>
```

For `notion_state`, resolution uses the original page and real event edge, not
trust in cached fields. It resolves at most one event with the normal shared
request/text bounds. Other source kinds report `no_verified_event_route`; they
retain their source and context without inventing a join. A partial resolution
must stay partial in the conversation. A replaced/expired candidate is rejected
after a slow resolution. Neither read nor resolve writes a receipt.

After actual use, a separate call records the exact candidate and turn:

```bash
node scripts/read_ambient_recall.js --file <staged.json> \
  --ack <CANDIDATE_ID> --used-in <ACTUAL_TURN_REFERENCE>
```

Do not combine `--resolve` and `--ack`. This is a consumer acknowledgment, not
automatic proof of cognitive use. Cite and inspect the corresponding turn in
audits. Fixture/diagnostic turn receipts are not production conversational proof.

## Scheduler/consumer prompt contract (apply per installation)

When deploying this source, preserve the existing 5DB IDs, schedules and writer
jobs. Resolve `<...>` placeholders from the operator's workspace, never from
shared skill defaults. These are the relevant prompt additions, not commands
to execute during repository development:

**Continuity synthesis / writer**

> Preserve a meaningful event and its historical emotion/state context. When
> there is evidence for an emotional change, include 1-3 accepted emotion axes
> with recorded intensity and first-person reason in emostate_tick's payload;
> do not invent an emotion just to fill the schema. If no emotion was recorded,
> do not later claim the event has an emotion record. For a relevant remembered
> experience, use experience_recall with bounded event query or known source ID,
> and distinguish incomplete context from success. Keep mem write/search active.
> Deduplicate by experience, emotional meaning, provenance and purpose, not
> text alone. Do not promote an inference about user psychology as a fact.
> Report Notion write failure independently of a successful local/core write.

**Subjective journal**

> Keep the existing single-day preflight and local mirror behavior. Synthesize
> first-person meaning, not a scheduler health log or Dreaming report. When
> recalling an earlier event, resolve its real emotion/state relations and
> distinguish then from now. Never let a local mirror hide Notion write failure.

**Ambient staging**

> Run exactly one existing stage_ambient_recall command with the configured
> workspace, timezone, TTL and state/journal/mem IDs. Do not force or reroll in
> production. A dry run is only preview. Report producer errors. Do not mark
> a candidate consumed or claim it was injected/used from successful staging.

**Conversation/heartbeat consumer**

> Read unexpired staged context once without rerolling. For a notion_state
> candidate that matters to an emotion-linked claim, call read_ambient_recall
> with --resolve and the configured events/emotions/state data source IDs.
> Preserve source and historical emotion context, including partial diagnostics.
> Use it only when useful. After actual use, acknowledge the exact candidate ID
> with the real turn reference in a separate call; reading is not use.

The initial September audit found the deployed consumer using direct JSON reading
with no receipt workflow; the continuity prompt did not explicitly require
emotion axes, and ambient staging lacked the new consumer path. Those runtime
prompts/snapshots are separate from this repository. Check the current installation
and saved deployment evidence rather than treating the initial audit as current status.
Do not claim deployment
or a live conversational-consumption pass from source tests alone.

## Verification and rollback

Run `node --test scripts/experience_recall.test.js scripts/memory_boundary.test.js`.
Tests use synthetic text, IDs and relations only. For live verification, keep raw
schema/row snapshots and output outside the repository and indexed memory, with
restricted permissions. Audit all 5 schemas and only a few known rows. Compare
direct event, event query, and state-ID results to actual source IDs and values.
Use an isolated temporary workspace for deterministic ambient tests; never
overwrite or force-roll production candidates. Record no private prose/IDs in
public reports or fixtures.

Before rollout save exact runtime files/prompts/env metadata and candidate/
receipt pre-images outside indexed memory. Roll back by restoring those saved
versions, not by altering Notion rows. This implementation does not migrate,
delete or change any Notion schema/record and does not modify OpenClaw ranking.
