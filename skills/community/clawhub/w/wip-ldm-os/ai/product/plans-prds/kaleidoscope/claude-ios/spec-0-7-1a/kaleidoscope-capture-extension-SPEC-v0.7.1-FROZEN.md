# Kaleidoscope Capture Extension — Technical Spec v0.7.1 (FROZEN for Phase 0)

**Owner:** Parker Todd Brooks · WIP Computer, Inc.
**Status:** 🧊 **FROZEN (errata applied — v0.7.1a)** — architecture locked; Phase 0 implementation begins. v0.7.1 folded in implementation-hardening edits from external review (GPT-5 / Grok). The **v0.7.1a errata pass** (fresh self-review) corrects four substantive items — sweep phasing, backfill-ordering signals, deletion/erasure, canonical-log location — without changing the architecture. See §0a.
**Surface:** Safari Web Extension shipped inside the Kaleidoscope iOS app

> **Freeze note:** Stop architecture rewrites here. Remaining work is implementation. Changes beyond this point should be code + tickets, not spec revisions, unless a spike returns a blocking surprise. The one item that genuinely requires the private repos — locking the harness-profile catalog and `stream_key → agent_id` mapping against the real `agents/{agent_id}/` trees — is delegated to repo-aware agents (Claude Code / on-machine GPT-5.5), not resolved here.

**Reading note for repo-aware agents:** Written **without access to the private Kaleidoscope/Memory Crystal repos or prior specs.** §5 (Identity), §7 (Storage/event-sourcing), §8 (Embedding) encode design-conversation decisions to be **reconciled against actual repo code** (`agent_id` scheme, `agents/{agent_id}/` trees, Core/Node logic, CloudKit schema, existing OpenAI vector stores). Repo + prior specs are authoritative where they conflict.

---

## 0a. Errata — v0.7.1a (fresh-review pass; corrections, no architecture change)

1. **Sweep reframed for iOS + pulled to Phase 0 (minimal form)** (§6, §9, §18). On iOS, Safari suspends the content script whenever the tab backgrounds; a turn that completes while suspended never fires the live signal. So on this platform the sweep is **the primary recovery path, not redundancy.** A **minimal on-load/on-focus sweep** (rescan rendered turns against the watermark; reuses the T1 extraction path + T9 dedup) is now **Phase 0**; the exhaustive scroll-driven backfill remains later.
2. **Backfill ordering signals corrected** (§9.1, §17.6). `parent_turn_hash` is **uncomputable at a backfill window head** (the parent is evicted from the DOM), and DOM order is *relative*, not absolute. Spike 6 is therefore load-bearing for ordering: it must identify an **absolute** ordering signal (stable `vendor_message_id`, DOM ordinals, or equivalent).
3. **Canonical-log location decided** (§7.4): canonical logs write to the **local app container as truth**; the user-inspectable **iCloud Drive copy is a mirrored export.** This answers the long-dropped "iCloud off/full" question (local-only = fully functional degraded mode; mirror resumes when iCloud returns) and sidesteps ubiquity-container write-coordination (NSFileCoordinator, dataless files) on the hot path.
4. **Deletion vs. immutability resolved** (§7.8 new): tombstone = hide (immediate); **compaction = erase** — a named Core operation that rewrites affected segments dropping tombstoned payloads, reseals with new manifests, and emits `core.segment_compacted`. The one sanctioned exception to segment immutability.
5. Small precision items: normalization-version bump triggers Core-side re-hash of existing turns so re-observed old turns still dedup (§9); `core_epoch_seen` is optional at the handler — Core stamps epoch authoritatively on acceptance (§10); App Group queue uses `NSFileProtectionCompleteUntilFirstUserAuthentication` (§6); cross-session re-sends are expected behavior — the script re-ships rendered turns after a refresh and Core drops duplicates (§9); projection determinism (M5) requires **canonical serialization** (stable key order, fixed timestamp/float formats).

---

## 0. Changelog from v0.7 (hardening only — no architecture change)

- **Segment integrity manifest** (§7.4): sealed JSONL segments carry a manifest (`sha256`, `event_count`, first/last `event_id`, `sealed_at`); projections checkpoint against `segment_id + byte_offset + event_id`.
- **Atomic writes** (§7.4): every segment/projection write is temp-file → fsync → atomic rename → manifest update. The Core never writes directly into a visible final file (iOS can kill mid-write).
- **Acceptance metadata** (§7.3, §10): when the Core appends an inbox observation, it stamps `accepted_by_core`, `accepted_at`, `accepted_core_epoch`, `source_event_id` — resolving the "same event in /Inbox and /CaptureLog" ambiguity.
- **Opaque filenames by default** (§7.4): `/Transcripts/stream_9f3a/chat_01HY….md`, not human-readable content in paths. Filenames leak via sync metadata, backups, screenshots, support flows.
- **iOS lifecycle note** (§6): the containing app does **not** reliably wake just because the extension wrote to the App Group; the queue is durable but **draining requires the app to be active** (Background Tasks/silent push is a later phase). MVP shows a "captures pending" indicator.
- **Stale-epoch policy decided** (§7.6): default = **rewrite-under-current-epoch**, emitting a `core.stale_epoch_rewritten` event for auditability (over quarantine, which feels like data loss).
- **Spike 7 success criteria made concrete** (§17): Recall@K / nDCG on the user's own queries, chunking/pooling strategy, on-device throughput/memory, language/code/math edge cases, and a decision rule.
- **Cross-surface backfill documented** (§9.1, post-freeze clarification — no architecture change): the iOS-app-history-via-Safari reconstruction scenario, named as an explicit test target, with the virtualization caveat and ordering-spike dependency.

---

## 0b. Changelog from v0.6 (carried — event-sourcing model)

- Generic event envelope with `event_type`; observation (`capture.*`) vs canonical (`core.*`/`embedding.*`) taxonomy; inbox-vs-canonical-log boundary with same-device-Core fast path; segmented sealed logs; canonical-commit = event-log append; projection determinism; phone-as-Core MVP. (See §7–§10.)

---

## 1. MVP

1. **An app that opens and looks like a chat.**
2. **Install the plugin**; chat on claude.ai in Safari.
3. **That chat appears inside Kaleidoscope's chat box.**

Heartbeat: **Claude Safari → Kaleidoscope queue → canonical event log → Kaleidoscope chat UI.** Phase 0 has **no** embedding, search, BYO keys, import, RRF, or Core/Node promotion. Phone **is** the Core (fast path, §7.3).

---

## 2. Summary

A Safari Web Extension (inside the app) reads each completed claude.ai turn + in-DOM media/readable artifacts **read-only**, routed content script → background worker → native handler → App Group queue. The **app** (always co-resident, sole egress, **Core** by default) ingests the **event**, appends it to the **canonical JSONL event log**, produces deterministic JSON/MD + read-model projections, embeds the text **on-device (Apple, spike-gated)**, optionally **also** into a **BYO** space, and renders the chat. WIP sees nothing. Protection is Apple's.

---

## 3. Scope / Non-Goals

**In scope (v1):** read-only claude.ai capture; Core/Node event-sourced iCloud storage; on-device + optional BYO embedding with multi-space search; in-app chat rendering; agent/stream identity model.

**Out of scope (v1):** Bridge / agent-to-agent; DOM mutation; interactive-iframe artifacts; non-claude.ai surfaces; native Claude iOS capture (sandbox-impossible); non-Apple device reach; WIP-managed cloud embedding (dropped).

---

## 4. Two Planes

| Plane | Carries | Transport | This doc |
| --- | --- | --- | --- |
| **Memory sync** | The user's memory store between their own devices | iCloud/CloudKit; WIP relay only as deferred non-Apple bridge | **In scope** |
| **Bridge** | Agent-to-agent messages | WIP architecture | **Out of scope** |

---

## 5. Agent / Stream Identity Model

### 5.1 The harness decides what splits a stream
```
harness_profile = { name, model_is_identity: bool, host_is_identity: bool }
```
- **Model-transparent** (Claude app, Claude Code CLI, Open Code): model recorded per-message, doesn't split.
- **Model-defining** (OpenClaw, Hermes): model **is** identity (Lēsa·GPT-5.5 ≠ Lēsa·Claw-4.8).
- **Host**: identity-bearing only where machine-bound (Claude app synced → no; Claude Code CLI per-machine → yes).

### 5.2 Stream key
```
stream_key = provider + harness + (host if host_is_identity) + (model if model_is_identity) + account_namespace
```
`account_namespace = "anthropic:<opaque_account_hash>|unknown"`; never expose email unless user-labeled. Model/host always recorded; split only per profile.

### 5.3 Browse tree
`provider → harness → [host] → [model] → chats`; non-identity model/host are labels; collapse non-disambiguating levels.

### 5.4 Handoff
Finalize harness-profile catalog; reconcile with `agent_id` (`cc-mini`, `lesa-mini`) / `agents/{agent_id}/` → `agent_id` becomes `stream_key`.

### 5.5 Safari extension
Feeds **Anthropic → Claude app** (`model_is_identity:false`) → never needs model to route; records per-message model label if DOM exposes it, else `unknown`.

---

## 6. Message Pipeline

```
content script (claude.ai)  — reads PLAINTEXT read-only; ephemeral in-session hash
   │ browser.runtime.sendMessage   (content scripts CANNOT call native directly)
extension background/service worker  — coordination only, NOT durable
   batching, chunking, idempotency labels, retry-while-alive, backpressure
   │ browser.runtime.sendNativeMessage
SFSafariWebExtensionHandler (extension process)  ← FIRST DURABLE BOUNDARY
   writes capture.* EVENT to App Group queue
   (NSFileProtectionCompleteUntilFirstUserAuthentication — readable for future background drain); acks
   │
App Group container (durable queue)
   │
Kaleidoscope app  (Core by default; else Node → inbox)
   Core fast path: ingest event (idempotent by event_id) → append to canonical log
                   → deterministic projections + read model → embed → render
   Node path:      submit event to /Inbox/<device_id>/ → (Core consumes)
```

**Invariants:** content scripts route via the background worker; the worker is **not** durable (durability begins at the native-handler queue append); the handler is boring (write event, ack, exit); ingestion idempotent by `event_id`; **real-time into the queue, lifecycle-gated into iCloud.**

**iOS lifecycle reality (document, don't fight):** the containing app does **not** reliably wake from suspension just because the extension handler wrote to the App Group. The queue is durable, but **draining/ingestion requires the app to be active** (foreground, or Background Tasks/silent push in a later phase). For the phone-as-Core MVP this is fine — the user is actively in Kaleidoscope — but the literal loop is "chat in Safari, **open Kaleidoscope**, it's there," not background magic. Surface a persistent **"N captures pending"** indicator (and optionally an extension badge) so durably-queued-but-not-yet-ingested is visible, not a perceived bug. The native handler stays boring: write + ack + exit.

---

## 7. Storage Model — Core/Node, Event-Sourced

**Principle:** a designated **Core device owns canonical state and is the only actor that appends canonical events.** Nodes submit **observation events** to an inbox. iCloud/CloudKit is **transport, inbox, backup, distribution — not authority.**

### 7.1 The canonical paragraph (the rule)
> Only the active Core epoch appends to the canonical event log. Nodes never mutate canonical logs directly; they submit capture events to an inbox. The Core validates inbox events, applies idempotency and content dedup, then appends accepted events to segmented JSONL log files. Log segments are append-only while active and immutable once sealed. JSON conversation files, Markdown transcripts, read models, and local SQLite/vector/BM25 indexes are deterministic projections from the canonical event log plus projection/schema versions. Same-device capture on the phone-as-Core MVP is a fast path through the same model: the app consumes its local queue and appends as the active Core.

### 7.2 Observation vs. canonical events
- **Observation events — `capture.*`** (e.g. `capture.turn_observed`, `capture.artifact_observed`): submitted by **Nodes**, *untrusted until Core-accepted*. A Node may only ever emit these.
- **Canonical / derivation events — `core.*`, `embedding.*`** (e.g. `core.turn_normalized`, `core.stream_assigned`, `core.message_deleted`, `core.branch_detected`, `core.schema_migrated`, `core.projection_checkpointed`, `embedding.space_backfilled`): emitted **only by the active Core.**

This taxonomy *is* the inbox/canonical boundary at the event level: inbox = `capture.*` observations; canonical log = Core-accepted events of any type.

### 7.3 Inbox vs. canonical log
```
/Inbox/<device_id>/...          ← Node-submitted capture.* events, awaiting Core
/CaptureLog/...                 ← Core-accepted canonical events only
```
Only the active Core epoch appends to `/CaptureLog`. **Phone-as-Core MVP** = the app consumes its own local queue and appends as the active Core (the fast path); the general Node→inbox→Core flow is the same model with the inbox hop added when the Core is a *different* device.

**Acceptance metadata:** when the Core accepts an inbox observation and appends it to the canonical log, it stamps acceptance fields so the same `event_id` appearing in both `/Inbox` and `/CaptureLog` is unambiguous:
```jsonc
{ "accepted_by_core": "<core_device_id>", "accepted_at": "<ISO-8601>",
  "accepted_core_epoch": 3, "source_event_id": "<original inbox event_id>" }
```
(Equivalently, model this as a `core.capture_accepted` event wrapping the observation — repo-aware agents pick the representation; the fields are the requirement.)

### 7.4 Segmented, sealed logs + integrity + atomic writes
**Location (v0.7.1a decision):** canonical segments are written to the **local app container as truth**; the user-inspectable **iCloud Drive folder holds a mirrored export** of segments + projections, synced opportunistically. Consequences: (a) **iCloud off/full/unsigned = fully functional local-only mode** — the mirror resumes when iCloud returns (surface mirror status in UI, never block capture on it); (b) hot-path atomic writes run against the local filesystem with ordinary POSIX semantics, avoiding ubiquity-container write-coordination (NSFileCoordinator, dataless/evicted files) except in the mirror step.
```
local:  <app container>/CaptureLog/core_epoch=3/2026/06/29/events-000001.jsonl   ← truth
mirror: iCloud Drive/Kaleidoscope/CaptureLog/...                                 ← inspectable export
```
No single endlessly-appended file (avoids iCloud conflict on the mirror). The Core appends only to the **active segment**; **sealed segments are immutable** (sole exception: §7.8 compaction).

**Sealed-segment manifest** (verifiability + replay safety):
```jsonc
{
  "segment_id": "core_epoch=3/2026/06/29/events-000001.jsonl",
  "core_epoch": 3, "event_count": 412,
  "first_event_id": "...", "last_event_id": "...",
  "sha256": "...", "sealed_at": "<ISO-8601>"
}
```
Projections checkpoint against **`segment_id + byte_offset + event_id`** (`core.projection_checkpointed`), giving corruption detection, replay safety, and migration confidence.

**Atomic writes (mandatory — iOS will kill mid-write):** every segment and projection write is **temp file → fsync/close → atomic rename → update manifest.** The Core never writes directly into a visible final segment/projection file. A crash mid-write leaves the prior sealed state intact; the in-flight temp is discarded on recovery.

**Opaque filenames by default:** paths use opaque IDs, not content —
```
good:   /Transcripts/stream_9f3a/chat_01HY....md
risky:  /Transcripts/Claude/therapy-session-about-bloodwork.md
```
The folder is user-inspectable, but filenames still leak through sync metadata, backups, screenshots, and support flows. Human-readable names only where the user explicitly assigns them.

### 7.5 Projection determinism
JSON/MD transcripts, read models, and local indexes are **deterministic projections** reproducible from *event log + projection-code version + schema version*. If projection logic changes, Core emits `core.projection_migrated` / a checkpoint event and **regenerates affected projections.** This is what makes the event log *actually* canonical — projections can always be rebuilt and can never silently drift from the log.

### 7.6 Core-published read model + stale-epoch policy
```
Core master state (internal):        Core-published read model (Nodes consume):
  canonical event log                  conversations / messages / stream tree
  normalization / dedup state          artifact refs
  stream assignment                    embedding-space manifests + coverage status
  tombstones / conflict markers        snapshot / delta versions
  schema migrations
```
**Stale `core_epoch_seen` (decided):** default = **rewrite-under-current-epoch** — the Core accepts a stale-epoch *observation*, appends it under the current epoch, and emits a `core.stale_epoch_rewritten` event for auditability. Stale epoch affects routing/idempotency, not content validity. (Rationale: quarantine feels like data loss to a user whose device was merely offline; rewrite keeps memories from "disappearing.") Stricter quarantine remains available for strict-consistency deployments; the chosen policy is recorded in the read model.

### 7.7 CloudKit / local / posture
- **CloudKit** = coordination: event inbox transport, manifests, sync cursors, device/Core leases, embedding-job status, tombstones.
- **Local per-device** = live SQLite + vector + BM25, rebuilt from the log / read model — never a synced live DB file.
- **Split-brain:** Core lease + epoch; only current epoch publishes; **manual promotion, never auto-election.**
- **Protection (honest):** no separate WIP encryption envelope; data in the user's iCloud under **Apple's account/device/iCloud security** (+ ADP if enabled). "Your iCloud, Apple-secured, WIP-blind." Opaque CloudKit record IDs, generic zones, no titles/provider/plaintext session IDs in queryable metadata.

### 7.8 Deletion: tombstone (hide) vs. compaction (erase)
Append-only immutable segments and "user can delete" are in tension: a `core.message_deleted` tombstone hides content from projections, but the plaintext would persist in sealed segments forever. Resolution — **two distinct user-facing operations:**
- **Delete (tombstone):** immediate; `core.message_deleted` removes the content from all projections/indexes. Content persists in sealed segments (recoverable, audit-preserving).
- **Erase (compaction):** the **one sanctioned exception to segment immutability.** A named Core operation rewrites affected segments **dropping tombstoned payloads**, reseals them with **new manifests** (new `sha256`, adjusted `event_count`), updates projection checkpoints, and emits **`core.segment_compacted`** (recording old→new segment ids and the tombstone ids elided — never the content). Erased content is then also purged from the iCloud mirror, projections, and indexes.
UX must say which one it's doing ("Remove from Kaleidoscope" vs "Erase permanently"). Compaction may be batched/scheduled; export tooling must respect tombstones either way. This closes the "delete that doesn't delete" gap for a privacy-first product.

---

## 8. Embedding & Search

**Invariant — canonical text is the source of truth; every embedding space is derived and rebuildable by re-embedding the text.** You cannot convert a vector between spaces; you never need to. Losing a vector index is never data loss.

### 8.1 Tiers
- **Default — Apple on-device embedding (Natural Language framework / `NLContextualEmbedding`), SPIKE-GATED:** local, keyless, private, network-free. **Benchmark quality, language coverage, chunking/pooling, dimensions, throughput on real captured conversations before treating it as the complete default index.** It is the privacy *floor*; whether it's also good enough as the default *search experience* is an open benchmark question (§17.7), not assumed.
- **Optional — BYO key (OpenAI / Voyage / …):** when present and enabled, **dual-write** — canonical text *also* embedded into the BYO space.
- **WIP-managed cloud embedding: dropped.**

### 8.2 Commit boundary + dual-write
- **Canonical commit = `capture.*` event appended to the JSONL log.** Memory is saved at the append; nothing about memory capture depends on embedding.
- **Apple embedding/indexing = committed local-index update when available** (not a precondition for the memory existing).
- **BYO embedding = best-effort secondary**, independent retry; failure leaves the turn Apple-only + in the log, caught up later.
- **User control:** BYO dual-write toggleable **globally and per-stream**; default on when a key is present **except sensitive/health streams default Apple-only**. Disclose per-memory cloud cost; offer a global pause.

### 8.3 Convergence / coverage status
- Any space made **complete** by re-embedding all logs into it (on key-add/restore/import); default trigger = re-embed-all.
- **Per-space coverage status** tracked + surfaced: `complete | partial(%) | stale | unavailable` ("Apple: complete · OpenAI: 72% · Voyage: unavailable"). Lives in the read model's embedding-space manifest.

### 8.4 Import existing corpora
- **Transcript-bearing import (e.g. OpenAI Memory Crystal with recoverable text):** synthesize `capture.*` **events** from its transcripts so they enter the canonical log like any capture; tag existing vectors as a pre-populated space `openai:text-embedding-3-{model}` (capture source model + dimensions); can also be Apple-embedded → both spaces. Querying the OpenAI space needs the user's BYO key live; escape hatch = re-embed to Apple to go fully local.
- **Vector-only import (no recoverable transcript):** **not canonical.** Attach as a **legacy search space** — searchable while its key/model is available, but **not canonical, not mirrorable, not re-embeddable** (no text to re-embed). Marked legacy. *No transcript, no canonical import.*

### 8.5 Multi-space search
- Each space tagged `embedding_space = model + version + dimensions`.
- Query: embed **once per live space with that space's own model**; search each independently; **fuse ranked lists via RRF** — by rank, never raw score. **Never cross-compare vectors across spaces.** Unavailable space skipped; graceful degradation; coverage status tells the user what was searched.

### 8.6 Apple PCC embeddings — parked spike
PCC / iOS 27 Foundation Models routing expose **generative** models only; Apple embeddings are on-device (Natural Language framework), not PCC; routing to OpenAI/Claude via Apple's framework is generative-only **and** still exposes text to the third party. **Don't build a tier on PCC embeddings.** Spike whether any iOS 27 / WWDC 2026 beta SDK surface exposes embeddings via PCC; if so (private + possibly free under Small Business Program), a candidate high-quality private tier. Pure upside.

---

## 9. Capture (read-only)

- **Trigger — commit-on-finish (primary while foregrounded):** `MutationObserver` on assistant-turn completion (stream-stop affordance / quiescence debounce — spike). Emit a `capture.turn_observed` event.
- **Minimal sweep (Phase 0 — iOS-primary recovery, not redundancy):** on load / route-change / **tab focus**, rescan rendered turns against the watermark and backfill any missing. On iOS, Safari suspends the content script whenever the tab backgrounds; a turn completing while suspended never fires the live signal — the focus-sweep is what recovers it. Reuses the same extraction + dedup path (~small). The **exhaustive scroll-driven backfill** (long-thread reconstruction) remains a later phase.
- **Dedup (two distinct mechanisms):**
  - **Content dedup (salted):** `SHA256(per_store_salt || "kaleidoscope.capture.v1" || source || vendor_conversation_id || role_order || normalization_version || normalized_turn_text)` — per-store salt (not portable), domain-separated. *"Seen this memory content?"* **Normalization-bump rule:** when `normalization_version` changes, the Core **re-derives hashes for existing turns from canonical raw text** so re-observed old turns still dedup (otherwise a version bump + re-observation double-stores history).
  - **Event idempotency:** `event_id` (ULID/UUIDv7). *"Processed this submitted event?"* Both needed.
- **Cross-session re-sends are expected:** after a refresh/new session, the script re-observes rendered turns and re-submits them; the Core drops known content. Duplicate *submissions* are by design; duplicate *storage* is the bug. (A watermark handshake between background worker and native handler is a later optimization, not Phase 0.)
- **Captured:** turn text (raw + normalized markdown); in-DOM images (canvas pixels, local — tainted-canvas spike); readable artifacts (code/md/svg source). Read-only.
- **Branch/edit — spike:** `vendor_conversation_id`, `vendor_message_id` (if present), `parent_turn_hash`, `revision`, `branch_id:unknown|detected`, expressed as events.
- **Model — per-message label**, never identity-blocking on the Claude-app branch.
- **Private mode:** capture on/off; **temporary/incognito unknown → do not capture.**

### 9.1 Cross-surface backfill (named capability + test target)
A conversation can be authored across surfaces that share one account-synced history (Claude **iOS app**, **Mac app**, **web**) — all one harness, one `/chat/{uuid}` (§5, `model_is_identity:false, host_is_identity:false`). Kaleidoscope can only directly observe the **Safari** surface (native apps are sandbox-impossible, §3), but it reconstructs the full thread when the user reopens it in Safari.

**Canonical scenario (must be tested):** turns 1–5 captured in Safari → user continues in the iOS app (turns 6–12, never seen by Safari) → user returns to Safari, scrolls to the top, scrolls all the way down (turns 1–12 render) → keeps chatting (13+). Expected result: **one complete, correctly-ordered conversation** — 1–5 recognized as already-held, 6–12 backfilled, 13+ appended live, **no duplicates.**

**How it works (existing mechanisms, no new architecture):**
- **Conversation-id spine:** all turns share one `vendor_conversation_id`, so the iOS-authored middle is understood as *the same thread continued*, not a new conversation — even though it arrives in two batches from two surfaces.
- **Turn-level dedup (not conversation-level):** the salted content hash is evaluated **per turn**. Scrolling back through 1–12, turns 1–5 hash to known values → skipped; 6–12 are unknown → ingested as new `capture.turn_observed` events. A partially-captured conversation gets *completed*, never re-duplicated or skipped wholesale.
- **Reconciliation sweep is the trigger:** scrolling brings the iOS-authored turns into the DOM so the sweep can hash and backfill them.
- **Event-log ordering:** `turn_index` + `parent_turn_hash` slot the backfilled middle into its correct position by index/parent, regardless of the wall-clock order in which batches were captured.

**Honest limits (document, don't hide):**
- **DOM virtualization caps completeness.** claude.ai evicts off-screen turns from the DOM in long threads; the sweep can only hash what's actually rendered at some moment. A deliberate slow scroll captures more reliably than a jump to the bottom, but completeness on very long backfilled threads is **not guaranteed** — this is inherent to DOM observation (live capture + focus-sweep are primary; scroll-backfill is best-effort).
- **Ordering signals can be unavailable exactly here (v0.7.1a correction).** `parent_turn_hash` is **uncomputable at a backfill window head** — the parent turn is evicted from the DOM, so there is nothing to hash. And DOM order is *relative* order of rendered turns, not absolute position. Both mechanisms this section previously leaned on can fail in the virtualized-middle case. **Spike 6 is therefore load-bearing for backfill ordering:** it must identify an **absolute** ordering signal in the DOM (stable `vendor_message_id`, per-message ordinals, or equivalent). If none exists, backfilled middles order by best-effort (relative order within the window + boundary anchoring against known turns) and the spec must not promise exact interleaving.

**Phasing note (v0.7.1a):** the **minimal on-focus sweep is Phase 0** (it's the iOS reliability path, §9). What lands later is the **exhaustive scroll-driven backfill** for long-thread reconstruction. Building blocks (conversation-id spine, turn-level dedup, event-log ordering) are Phase 0/1; the full §9.1 scenario becomes fully testable once scroll-backfill ships.

---

## 10. Data Model — Event Envelope

**Generic envelope (all canonical objects are events):**
```jsonc
{
  "event_id": "uuidv7-or-ulid",        // idempotency: "processed this event?"
  "event_type": "capture.turn_observed",
  "schema_version": "1.0",
  "captured_by_device": "device_id",
  "core_epoch_seen": 3,                // OPTIONAL at the handler (it may not know); Core stamps epoch authoritatively on acceptance
  "idempotency_key": "...",
  "captured_at": "<ISO-8601>",
  // acceptance metadata — added by Core when an inbox observation is appended to /CaptureLog:
  "accepted_by_core": "<core_device_id>",
  "accepted_at": "<ISO-8601>",
  "accepted_core_epoch": 3,
  "source_event_id": "<original inbox event_id, if rewritten/accepted>",
  "payload": { /* type-specific */ }
}
```

**Event types (illustrative, not exhaustive):**
```
capture.turn_observed      capture.artifact_observed        ← Node observations (inbox)
core.capture_accepted      core.turn_normalized             ← Core-only (canonical)
core.stream_assigned       core.message_deleted
core.branch_detected       core.schema_migrated
core.projection_checkpointed  core.projection_migrated
core.stale_epoch_rewritten    core.segment_compacted
embedding.space_backfilled
```

**`capture.turn_observed` payload:**
```jsonc
{
  "adapter_version": "claude-web-ios-0.1",
  "normalization_version": "md-normalizer-0.1",
  "stream_key": {
    "provider": "Anthropic", "harness": "Claude app",
    "host": null, "model": "unknown",
    "account_namespace": "anthropic:<opaque>|unknown"
  },
  "vendor_conversation_id": "<claude.ai /chat/{uuid}>",
  "vendor_message_id": "<if available, else null>",
  "turn_index": 42, "parent_turn_hash": "...", "revision": 1, "branch_id": "unknown",
  "provenance": {
    "source": "claude.ai", "surface": "safari-ios-web",
    "capture_method": "safari-web-extension",
    "trust_level": "rendered-dom-observation", "provider_signed": false
  },
  "turn": {
    "user":      { "text_raw": "...", "text_md": "..." },
    "assistant": { "text_raw": "...", "text_md": "...", "model_label": "unknown" }
  },
  "media": [ ... ], "artifacts": [ ... ]
  // content dedup hash (salted) added Core-side on acceptance
}
```
Canonical persistence = **append the event to the JSONL log**; JSON/MD transcripts + read model are deterministic Core projections.

---

## 11. Queue States & UX

```
observed_in_dom → sent_to_background → native_queued → (inbox_submitted if Node)
  → core_accepted → log_appended → projected → embedded_local → (embedded_byo) → indexed
```
Labels: `native_queued → "Captured"` · `core_accepted → "Pending sync"` · `log_appended → "Saved"` · `indexed → "Searchable."` Native ack = durably queued, not Core-accepted.

---

## 12. Threat Model (honest)

| Boundary | Sees | Notes |
| --- | --- | --- |
| claude.ai DOM | — | untrusted; `rendered-dom-observation`, unsigned |
| content/background JS | plaintext (transient) | in-memory; no key |
| native handler | plaintext → queued event | first durable boundary; iOS Data Protection |
| app (Core) | plaintext | appends log; projects; embeds; searches |
| **WIP infrastructure** | **nothing — no content, no usage** | WIP-managed embedding dropped |
| Apple model (on-device) | plaintext **locally only** | never leaves device |
| BYO provider | plaintext **at embed time** | only on the user's own key, only if enabled; absent on local-only/sensitive streams |
| iCloud/CloudKit | user's data under **Apple** security | "your iCloud, Apple-secured, WIP-blind" |

**Diagnostics rule (hard):** crash logs, telemetry, analytics, support bundles **never** contain captured text, request bodies, vector contents, titles, raw URLs, or content-revealing filenames. Content-free counts/timings/error-codes only.

---

## 13. Consent / Pairing / Status UX

- **First-run consent:** what's captured; stored in **your iCloud** under Apple security; embeddings **on-device by default (nothing leaves your phone)**; if you add a cloud key, your text is sent to that provider to embed (your choice, toggleable, off for sensitive streams); **WIP never sees your content.**
- **Product language:** *"Maximum privacy (on-device)"* vs *"Better search (your cloud key)."*
- **Persistent per-site "capture on" indicator; one-tap pause; capture off until consent.**

---

## 14. Privacy Review Package (App Store / Notarization)

- Host permissions: **claude.ai only**.
- Capture off until consent; persistent indicator; one-tap pause; incognito-unknown → no capture.
- **Privacy Nutrition Labels / policy:** user's own conversation content; stored in user's iCloud; **on-device embedding by default**; **if BYO embedding is enabled, text goes from the device to the user's selected third-party provider — disclose this optional third-party path** per Apple's App Privacy Details; WIP never sees it.
- **Functionality description:** "user-directed local archival of the user's own displayed conversations into the user's own iCloud memory."
- Content-free telemetry; user deletion/export.

---

## 15. Distribution & Review

- **Now, no review:** Xcode on-device + Ad Hoc (100 devices).
- **Alpha: TestFlight** — up to 10,000 external testers, **first external build requires Beta App Review.**
- **GA:** App Store + §14 package (extension + app, one submission).
- **EU/Japan hedge:** alt-marketplace / web distribution → Notarization; geographically boxed, in flux — hedge, not primary.

---

## 16. ToS Posture

**Anthropic §3 clarification = rollout/marketing gate, not a code dependency.** Development proceeds without confirmation; **external rollout, marketing language, and broad TestFlight distribution stay gated on counsel review and/or Anthropic clarification.** Framing: *Kaleidoscope does not automate Claude usage, send prompts, bypass limits, share credentials, generate in the background, or resell access — it provides user-directed local archival of the user's own rendered conversations, with visible consent.*

---

## 17. Spikes

1. **Turn-finish signal** — real claude.ai stream-stop affordance.
2. **Stable session id** — `/chat/{uuid}` content-script-readable + survives SPA nav.
3. **Tainted-canvas** — cross-origin images without CORS.
4. **`sendNativeMessage` payload ceiling** — chunking threshold; image bytes.
5. **Model signal in claude.ai DOM** — per-message label.
6. **Branch/edit + absolute ordering (LOAD-BEARING for backfill)** — what stable identifiers exist in the DOM: stable `vendor_message_id`, per-message ordinals, or equivalent **absolute** ordering signal. `parent_turn_hash` is unavailable at backfill-window heads (parent evicted) and DOM order is only relative — without an absolute signal, backfilled-middle ordering (M16) is best-effort only.
7. **Apple embedding quality (HIGH PRIORITY)** — benchmark `NLContextualEmbedding` on **real captured conversations** vs. a strong BYO model on the **user's own historical queries.** Concrete success criteria:
   - **Retrieval metric:** Recall@K and/or nDCG on the user's own queries against their own captured turns (not a generic benchmark).
   - **Chunking/pooling strategy:** whole-turn vs. sentence vs. semantic-paragraph; measure which wins on conversation data with code/markdown/tool-use blocks.
   - **Throughput + memory** on-device for typical conversation length, on the oldest supported device; watch thermal throttling on long indexing runs.
   - **Edge cases:** code snippets, mixed-language, math.
   - **Decision rule:** if Apple is within **~10–15%** of the BYO model on the user's own data → **default to Apple** + one-tap "also embed to my OpenAI/Voyage space"; if there's a **noticeable retrieval gap** → make the hybrid explicit in UX ("Maximum privacy" vs "Better search"). This decides whether Apple-local is merely the private floor or the default search experience.
8. **Apple PCC embeddings availability** (§8.6) — parked; pure upside.
9. **Multi-device embedding coordination** — reconcile with Memory Crystal Core/Node embedder logic.

---

## 18. Phased Rollout

- **Phase 0 — MVP:** chat-shell app + capture plugin; `capture.turn_observed` event → canonical JSONL log (local truth, iCloud mirror) → projections → render. **Includes the minimal on-focus sweep** (iOS recovery path, §9). Phone = Core (fast path). **No embedding/search/import/multi-device.**
- **Phase 1** — Apple on-device embedding (post-benchmark) + local hybrid search (RRF over the local space); salted dedup + event idempotency; queue states surfaced.
- **Phase 2** — BYO-key dual-write (with toggles) + multi-space RRF + import of transcript-bearing corpora; per-space coverage status; convergence/backfill.
- **Phase 3** — image + readable-artifact capture.
- **Phase 4** — multi-device Core/Node sync (inbox + manual promotion) + read-model distribution + identity tree in browse UI.
- **Phase 5** — **exhaustive scroll-driven backfill** (long-thread reconstruction, §9.1) + offline inbox + content-free telemetry + compaction (erase) tooling.
- **Phase 6** — non-Apple data bridge.
- **Phase 7** — additional surfaces (ChatGPT/Gemini) via adapters.

---

## 19. Open Questions

**Decisions (defaulted; override anytime):**
1. **Health/sensitive content** — default health-flagged/user-marked-sensitive streams to **Apple on-device only**; explicit per-stream opt-in for cloud. Counsel before GA.
2. **Convergence trigger** — re-embed-all on key-add/import (full mirrors; **default**) vs forward-only.
3. ~~Stale `core_epoch_seen`~~ **DECIDED** (§7.6): rewrite-under-current-epoch + `core.stale_epoch_rewritten` audit event.
4. ~~iCloud off/full~~ **DECIDED** (§7.4, v0.7.1a): local container is truth; iCloud Drive is a mirrored export; local-only is a fully functional degraded mode.
5. ~~Deletion vs. immutability~~ **DECIDED** (§7.8, v0.7.1a): tombstone = hide; compaction = erase (`core.segment_compacted`), the sole immutability exception.

**Repo reconciliation (for Claude Code / repo-aware agents):**
4. Finalize harness-profile catalog (§5.4).
5. Map `stream_key` onto existing `agent_id`.
6. Multi-device embedding coordination vs Core/Node embedder logic.
7. Import adapter (event synthesis from transcripts; vector-only → legacy space; tagging; dedup against canonical log).
8. Finalize the canonical **event-type catalog** (§7.2/§10) against repo conventions.

**Product:**
9. Capture thinking/tool-use steps? (parity vs sensitivity)
10. Offline inbox cap + retention.

**Parallel/external:**
11. Anthropic §3 note (send now).
12. App Store reviewable-by-design package finalization.
