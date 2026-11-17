# Kaleidoscope Capture — Phase 0 Build Plan

**Companion to:** `kaleidoscope-capture-extension-SPEC-v0.7.1-FROZEN.md`
**Scope:** Phase 0 MVP only. The heartbeat: **Claude Safari → Kaleidoscope queue → canonical JSONL event log → deterministic projection → chat UI.**
**Phone is the Core** (fast path). **No** embedding, search, BYO keys, import, RRF, multi-device, or image/artifact capture. Text loop first.

> **Definition of MVP done:** I chat in claude.ai in Safari, I **open Kaleidoscope**, and the conversation is there — rendered from a deterministic projection of an append-only event log that survives app kills and page refreshes, with no duplicates.

---

## Ticket breakdown

### T1 — Safari extension: content-script detector (read-only)
- Inject content script on `claude.ai` only (host permission scoped to claude.ai; no `<all_urls>`).
- Detect assistant-turn completion via `MutationObserver` + quiescence debounce (placeholder until **Spike 1** resolves the real stream-stop affordance).
- Extract the paired turn (preceding user message + completed assistant message): `text_raw` + normalized `text_md`. **Read-only — never mutate the DOM.**
- Read `vendor_conversation_id` from `/chat/{uuid}` (**Spike 2**: confirm it's readable + survives SPA nav).
- Compute an **ephemeral in-session hash** to avoid double-sends within one page session (not persisted).
- Respect the capture on/off state (T8): off → read nothing.
- **Out:** images, artifacts, model label (record `"unknown"`), branch/edit detection.
- **Done when:** a completed turn produces one in-memory capture object with stable conversation id, sent once per session.

### T2 — Background worker: message / chunk / ack path
- Receive `sendMessage` from the content script (content scripts **cannot** call native directly).
- Batch, assign `idempotency_key`, chunk per the `sendNativeMessage` ceiling (**Spike 4**), apply backpressure, retry-while-alive.
- Call `browser.runtime.sendNativeMessage`; on ack, mark delivered (idempotent — safe to retry).
- **Explicitly non-durable:** worker holds nothing across suspension; durability begins at T3.
- **Done when:** capture objects cross to native exactly once each under retry, with chunking for large payloads.

### T3 — Native handler: App Group queue writer
- `SFSafariWebExtensionHandler` receives the message in the extension process.
- Wrap as a `capture.turn_observed` **event envelope** (`event_id` = UUIDv7/ULID, `event_type`, `schema_version`, `captured_by_device`, `core_epoch_seen`, `idempotency_key`, `captured_at`, `payload`).
- Append the event to the **App Group durable queue** (iOS Data Protection file class). **Boring: write + ack + exit.** No network, no embedding, no key.
- **Done when:** every delivered capture becomes a durable queued event; handler returns ack; app-killed-after-this-point still has the event (test M3).

### T4 — Core queue ingester (idempotent)
- App (= Core, fast path) drains the App Group queue **when active** (document: app must be foreground to drain; see T9 indicator).
- Idempotent by `event_id` (skip already-processed); apply **salted content dedup** (T9) to skip already-seen content.
- Stamp acceptance metadata (`accepted_by_core`, `accepted_at`, `accepted_core_epoch`, `source_event_id`).
- **Done when:** draining is idempotent; duplicates (same event or same content) are dropped; ingestion is resumable after relaunch.

### T5 — JSONL event envelope + segment writer
- Append accepted events to the **active segment**: `/CaptureLog/core_epoch=<n>/<yyyy>/<mm>/<dd>/events-<seq>.jsonl`.
- **Atomic writes:** temp file → fsync → atomic rename → update manifest. Never write into a visible final file directly.
- On rotation, **seal** the segment and write its manifest (`sha256`, `event_count`, first/last `event_id`, `sealed_at`). Sealed segments are immutable.
- **Done when:** events land in segmented append-only logs; sealed segments are verifiable by manifest; a mid-write kill leaves prior sealed state intact.

### T6 — Projection generator: event log → chat JSON/MD
- Deterministically fold the event log into per-conversation **structured JSON** + **human-readable Markdown** projections, written to `/Transcripts/<opaque_stream>/chat_<opaque>.{json,md}` (**opaque filenames**).
- Tag projections with projection-code version + schema version; rebuildable from the log alone.
- Atomic writes (as T5).
- **Done when:** projection is a pure function of (event log + versions); deleting projections and rebuilding from the log yields identical output (test M5).

### T7 — Chat UI: render from projection
- Kaleidoscope opens into a chat-style view; render conversations from the **projection** (not from live capture, not from the queue).
- This is the "magic moment" — your claude.ai conversations, local, instantly, in your app.
- **Done when:** a captured conversation appears in Kaleidoscope's chat box, reading only from projections.

### T8 — Capture on/off consent state
- First-run consent before any capture; persistent per-site "capture on" indicator; one-tap pause.
- Capture off until consent; **temporary/incognito unknown → do not capture.**
- **Done when:** no DOM is read before consent; toggling off stops all reading (test M8).

### T9 — Idempotency + salted content dedup + pending indicator
- Per-store random salt; content dedup = `SHA256(salt || "kaleidoscope.capture.v1" || source || vendor_conversation_id || role_order || normalization_version || normalized_turn_text)`, computed Core-side on acceptance.
- Maintain the per-conversation watermark.
- **"N captures pending" indicator** in the Kaleidoscope UI (and optional extension badge) for durably-queued-but-not-yet-ingested, so background queueing reads as status, not a bug.
- **Done when:** re-renders/refreshes never double-store; pending count is visible and accurate.

### T10 — Crash / restart recovery tests
- Implement the **test matrix** below as automated/repeatable checks.
- **Done when:** all matrix rows pass.

---

## Phase 0 test matrix (binary acceptance)

| # | Scenario | Pass condition |
|---|---|---|
| M1 | Capture one completed Claude turn | Exactly one `capture.turn_observed` event in the log; renders in UI |
| M2 | Refresh the claude.ai page | No duplicate event/turn (dedup + watermark hold) |
| M3 | App killed **after** native queue write, **before** ingest | Event survives in the App Group queue |
| M4 | App relaunched after M3 | Queue drains; event appended to canonical log |
| M5 | Delete projections, rebuild from log | Byte-identical projection output (determinism) |
| M6 | Delete local working DB/read model, rebuild from log | Full state recovered from canonical log |
| M7 | Malformed / unparseable inbox event | Rejected or quarantined; does not corrupt the log |
| M8 | Capture toggle OFF | No DOM read, no events produced |
| M9 | Native ack received | Means *durably queued*, **not** *log-appended* (states distinct in UI) |
| M10 | Mid-write kill during segment/projection write | Prior sealed state intact; temp discarded on recovery (atomic-write proof) |
| M11 | Same turn delivered twice (retry) | Single stored event (idempotency by `event_id`) |
| M12 | Sealed segment manifest check | `sha256` + `event_count` + first/last `event_id` verify |

### Cross-surface backfill tests (§9.1 of the spec — primary scenario to test against)
These prove the "started on iOS, reopened in Safari, reconstruct the whole thread" capability. Turn-level dedup (M13–M14) is testable from Phase 1; the full sweep-driven backfill (M15–M17) is testable once the reconciliation sweep ships (consider pulling it earlier than Phase 5).

| # | Scenario | Pass condition |
|---|---|---|
| M13 | Re-render a conversation with turns 1–5 already captured | Turns 1–5 recognized as duplicates (per-turn hash), not re-stored |
| M14 | Same conversation now shows turns 1–12 (6–12 authored elsewhere) | 6–12 ingested as new; 1–5 still skipped; **no full-conversation re-dup** |
| M15 | Scroll top→bottom through a partially-captured thread | Sweep backfills exactly the missing turns (the gap), nothing duplicated |
| M16 | Backfilled middle ordering | Turns 6–12 slot **between** 5 and 13 by `turn_index`/`parent_turn_hash`, not appended at the end |
| M17 | Continue chatting after backfill | New turns (13+) append live; final thread is complete + correctly ordered |
| M18 | Very long thread, jump to bottom (virtualization) | System captures what rendered; **does not** claim/false-record turns never in the DOM (completeness honestly bounded) |

---

## What is explicitly NOT in Phase 0
Embeddings (Apple or BYO) · search/RRF · vector DB/indexes · import of existing corpora · multi-device Core/Node sync · Core promotion/epoch transitions beyond a single fixed epoch · image capture · readable-artifact capture · model-label attribution · branch/edit detection · usage/metering · Bridge.

(These are Phases 1–7 in the frozen spec. Do not let them leak into Phase 0.)

---

## Phase 0 spikes (resolve in parallel; some gate tickets)
| Spike | Gates | Question |
|---|---|---|
| **S1 turn-finish signal** | T1 | Real claude.ai stream-stop affordance (vs. debounce placeholder) |
| **S2 stable session id** | T1 | `/chat/{uuid}` content-script-readable + survives SPA nav |
| **S4 payload ceiling** | T2/T3 | Practical `sendNativeMessage` size limit; chunking threshold |
| **S(iOS-drain)** | T4/T9 | Confirm foreground-drain behavior; size the pending-indicator UX |

(Spikes 3/5/6 — tainted-canvas, model label, branch/edit — gate *later* phases, not Phase 0. Spike 7, Apple-embedding benchmark, is the highest-leverage **Phase 1** gate and should be run early in parallel but does not block the Phase 0 text loop.)

---

## Repo-side dependency (NOT resolvable without the private repos)
Two external reviews and the spec all flag the same top non-ticket action, and it requires `agents/{agent_id}/` context this build plan doesn't have:

- **Lock the harness-profile catalog** (which harnesses are model-defining vs model-transparent, host-bound vs synced).
- **Map `stream_key` → existing `agent_id`** (`cc-mini`, `lesa-mini`, the `agents/{agent_id}/` trees).
- **Finalize the canonical event-type catalog** against repo conventions.

→ **Owner: repo-aware agents (Claude Code / on-machine GPT-5.5).** Phase 0 can proceed using a single `Anthropic → Claude app` stream with `model:"unknown"` while this is finalized, because the Safari extension feeds a model-transparent harness and never needs the full catalog to route.

---

## Suggested build order
1. **T8 + T9 scaffolding** (consent gate + dedup/pending infra) — so nothing captures before consent and dedup exists from turn one.
2. **T1 → T2 → T3** (the capture→queue path) with **S1/S2/S4** running alongside.
3. **T4 → T5** (ingest → canonical log) — the durability core.
4. **T6 → T7** (projection → chat UI) — the visible payoff.
5. **T10** (recovery/test matrix) continuously, not at the end.

The moment T7 renders a real captured conversation from a projection — with M1–M6 green — Phase 0 is proven and the broader Kaleidoscope vision has its first working organ.
