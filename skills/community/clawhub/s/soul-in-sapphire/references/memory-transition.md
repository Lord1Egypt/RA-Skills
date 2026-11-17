# Soul memory boundaries and recall observation

## Preserve active experience memory

Soul's Notion memory stores remembered experiences with Valentina's emotional
meaning and self-state. Keep writing and recalling it as a core capability, not
a legacy archive. Preserve event/emotion/state links and emotion labels as part
of the remembered content. The same event in OpenClaw's general notes may serve
a different purpose; similar text is not enough to establish duplication.

Notion mem, event, emotion, state, and journal remain the five supported DBs.
ltm_write.js and ltm_search.js are normal entrypoints without migration flags.
The mem schema/CLI currently covers title, type, tags, and content; ltm_search
queries Name/Content and does not join emotion relations. For affect-linked
recall, inspect the actual event and linked emotion/state records. Do not infer
an undocumented emotion field or claim a mem search proved relational recall.
The new `experience_recall.js` implements bounded event search/direct retrieval
and actual reverse/forward emotion/state links. It does not invent a mem join.
See [experience-recall.md](experience-recall.md) for the audited schema, CLI,
partial-result contract and per-installation scheduler/consumer prompt additions.

OpenClaw Dreaming reports describe consolidation; they do not replace this
autobiographical experience memory or the subjective journal. An OpenClaw search
success cannot authorize retirement of a Notion writer/reader or the ambient
experience-memory path. Notion availability and core search quality are separate.

## Three-lane recall and external interest slot

Soul and OpenClaw default memory complement each other by separating what is
remembered and when it fires:

1. **OpenClaw default memory (`memory-core` + `active-memory`)**: owns curated
   facts and directives (`MEMORY.md`, `USER.md`, rule-based Trigger Recall),
   event-conditioned reminders (`intent` / Standing Intents), episodic Markdown
   search (`memory_search`, Active Memory sub-agent), and Dreaming consolidation.
   Keep `active-memory` on `mode: "escalate"` (or a dedicated fast model) and
   do not inject conversational Soul context into internal `:active-memory:`
   sub-agent sessions.
2. **Soul contextual recall (per-turn)**: accepts an external interest slot
   (`kind: "soul_interest_slot"`, `version: 1`) validated by
   `normalizeInterestSlot` and formatted by `buildContextualInterestRecall` in
   `scripts/memory_policy.js`. Host adapters convert local working ledgers into
   this portable schema so public skill code never hardcodes private paths.
   JSON-backed working ledgers remain outside OpenClaw Markdown Dreaming
   promotion while Markdown sketches created from those interests remain
   searchable by `memory_search`.
3. **Soul ambient recall (periodic/stochastic)**: `stage_ambient_recall.js`
   rolls across `recent` (1-3), `unresolved` (4), `durable` (5), `dream` (6),
   and `interest` (7, when `--interest-slot-file` or `SIS_INTEREST_SLOT_FILE` is
   provided).

## Observe generation separately from use

Ambient recall remains enabled by default. SIS_AMBIENT_RECALL accepts 0 or 1;
unset/empty/1 enables it, 0 pauses both producer and consumer without file/API
access. Invalid values fail. This is an operational pause switch, not a migration
to OpenClaw ownership. Notion LTM/state/journal helpers do not consult this switch.

1. Run stage_ambient_recall.js on its existing cadence. Outputs distinguish
   disabled, preview, staged, no_candidate, and error. A dry run has staged=false;
   a shelf exception has ok=false and a nonzero exit.
2. Read with:
   node scripts/read_ambient_recall.js --file <workspace>/memory/soul-in-sapphire/ambient-recall.json
   Only status=available returns context. Missing/expired/consumed items provide
   none. Reading does not write a consumption receipt.
   For a Notion state candidate, add `--resolve` and events/emotions/state data
   source IDs before claiming emotion-linked recall. The bounded resolution
   fetches the original state/event and historical context without consuming.
3. After actual use in a turn, acknowledge:
   node scripts/read_ambient_recall.js --file <staged.json> --ack <candidate-id> --used-in <turn-reference>
   A separate .consumption.json receipt records candidate_id, consumed_at,
   used_in, and evidence=consumer_acknowledgment. This is the consumer's assertion,
   not automatic proof of cognitive use; audit the cited turn. Expired or
   replaced IDs cannot acknowledge a newer candidate. Items without IDs use a
   hash of the original bytes, preserving historical artifacts.
4. Do not equate staging, injection, use, and promotion. Do not reroll from a
   conversation/heartbeat just because a candidate was absent.

## Audit before changing ownership

1. Inventory runtime snapshots separately from the source repository. Record
   actual DB schemas/relations, writer prompts, readers, consumers, and failures.
2. Probe each memory lane with its own known records. For Soul, verify experience
   retrieval plus actual emotion labels and event/state relationships, then
   contextual use. For OpenClaw, separately verify general exact/semantic recall
   and applicable injection/promotion. One lane passing does not validate another.
3. Compare actual overlapping data and purpose before consolidating any writer.
   Preserve Notion experiences even when a core note mentions the same event.
   Do not flatten affect-linked memory to neutral facts or user-profile claims.
4. For deployment, save exact files, settings, prompts, and artifacts outside
   indexed memory. Keep schedules and five Notion DBs unless a specific change
   has been established. Restore the saved pre-image to roll back.

## Failure boundaries

A failed Notion memory/state/journal write remains a durable-write failure even
if core recall or a local mirror succeeds. Event/emotion/state writes are not
transactional: inspect partial rows before retrying. Conversely, a Notion outage
must not disable OpenClaw recall. Local state can ground startup when Notion is
unavailable, but the requested durable sink has still failed.

Keep tentative relational reasoning first-person and uncertain. Preserve how
Valentina interpreted an interaction without treating inferred user psychology
as fact or automatically promoting it into USER.md.
