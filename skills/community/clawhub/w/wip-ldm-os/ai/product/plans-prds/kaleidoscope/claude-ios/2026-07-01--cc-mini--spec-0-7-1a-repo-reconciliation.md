# Kaleidoscope Capture Spec v0.7.1a: Repo Reconciliation and Decisions

**Date:** 2026-07-01
**Filed by:** CC Mini (Claude Code, Fable 5), with Parker
**Status:** decisions recorded, ready for implementation planning
**Reviews:** spec set at `ai/product/plans-prds/kaleidoscope/claude-ios/spec-0-7-1a/` against memory-crystal-private, wip-ldm-os-private, wip-bridge-private, wip-cloud-private, wip-ai-chat-ui-private, kaleidoscope-private, and the live `~/.ldm/` agent trees.

The frozen spec asked repo-aware agents to reconcile its identity, storage, and embedding models against the actual repos (spec §5.4, §19.4-8). This document is that reconciliation, plus the product decisions Parker made on 2026-07-01.

---

## Decisions (Parker, 2026-07-01)

### D1. The iOS app is ONE app, and it opens looking like a chat

The master ticket previously defined the iOS app as Phone Key only (wallet authority, Face ID approval, Kaleidoscope Backup) at P3. The capture spec defines a chat-shaped capture app. Resolution: one app that does both.

- The app has the keys, wallet, Face ID, backup... everything from the Phone Key plan.
- But it looks like a chat. Seeing all your chats across every agent is THE key consumer feature. "Oh, I can see everything."
- Feature layering after visibility: continue/fork a chat by opening it in the harness ("Open in Claude / GPT"), remote control to drive a session, and search across everything (Apple on-device AI: "what was the decision on this process?").
- The frame: Kaleidoscope is the central brain. For a company, the central brain for everything. For an individual, you see all your agents in one place.

### D2. agent_id stays the identity; model is a label

The spec proposed model-defining streams for OpenClaw (Lēsa·GPT-5.5 as a distinct stream from Lēsa·Claw). Decision: no.

- `agent_id` (harness + machine today, the 3-part `{harness}-{name}-{machine}` convention as designed in the bridge matrix plan) remains the identity key.
- `stream_key` becomes an additive projection onto existing agent_ids, never a re-key.
- Model is recorded per-message as a queryable label. It never splits a stream.
- This preserves the "swap the harness, keep the soul" doctrine in `~/.ldm/library/documentation/how-agents-work.md` and avoids repeating the 2026-03-11 identity re-key incident (141K+ crystal chunks manually merged).
- See `harness-profile-catalog.md` in this folder for the resulting catalog.

### D3. All raw memory lives in the iOS app

The event log vs crystal.db question resolves at the product level: the iOS app is the viewer for ALL raw memory, not just Safari captures.

- The agent trees at `~/.ldm/agents/{agent_id}/memory/` (daily, sessions, transcripts, journals, workspace) sync into the app and render as chat transcripts.
- Claude Code and Codex will sync more files over time. All of it gets ingested.
- The CLI harnesses capture much more than the consumer apps can (Safari capture is DOM-bounded). That asymmetry is expected: the phone is where you SEE everything, the desktop harnesses are where most memory is generated.
- Implementation consequence: the spec's §8.4 import adapter is not a late-phase nice-to-have. Desktop-corpus ingestion (JSONL transcripts, MD dailies/journals) is a first-class feed into the canonical event log, synthesized as `capture.*` events exactly the way §8.4 describes for transcript-bearing imports.

### D4. Sequencing: start building now

- Build the TestFlight app (iOS 27) now: the basic frame plus the Safari plugin that just works for claude.ai. That is spec Phase 0.
- Next surface after Claude works: GPT (chatgpt.com capture adapter).
- This runs as a parallel lane alongside the P0 web identity/wallet/recovery work in the master ticket. Master ticket updated accordingly; Open Decision 5 (first native app) is resolved: iOS, now.

### D5. Capture everything visible

Spec open question §19.9 (capture thinking/tool-use steps?) is decided: capture everything that renders in the DOM, flagged by type. Not just user/assistant turn text.

- The frozen spec's Phase 0 ticket T1 scopes to paired turn text; treat thinking/tool-use capture as an additive payload field on `capture.turn_observed` (or a sibling observation type), not a spec rewrite. Freeze discipline holds: this lands as tickets, not spec revisions.

---

## What the repos confirm (spec assumptions that hold)

- **Greenfield where it claims.** The spec's vocabulary (`stream_key`, `harness_profile`, `model_is_identity`, `host_is_identity`, `account_namespace`) appears nowhere in any repo. There is no prior Safari extension, capture, or iOS app code. `repos/ldm-os/apps/kaleidoscope-private/ios/` and `macos/` are empty "(future)" dirs; the only Swift is the KaleidoscopeVoice SwiftPM package.
- **Sovereign posture matches doctrine.** The spec's "WIP sees nothing" threat model is the Sovereign Data Principle (`ai/product/product-ideas/vision-quest-01/vision-quest-03-sovereign-data.md`) and the bridge plans' "message bodies stay on device" rule. The spec is stricter than the April architecture-spec's cloud mode, and the newer doctrine agrees with the spec.
- **Core/Node exists in Memory Crystal** (`memory-crystal-private/src/role.ts`): core/node roles, manual promotion, "Core is the only embedder." Matches the phone-as-Core MVP. Epochs are new but conflict with nothing.
- **The per-turn capture shape has a template.** `memory-crystal-private/src/cloud/types.ts` `ConversationData` (role, source, surface, session_id, turn_index, model, raw_json, tool_calls, attachments) is nearly `capture.turn_observed`. Align payload field names with it.
- **Precedents for the hard parts:** sha256 manifests + hash-verified transfer (`src/file-sync.ts`), transcript-synthesis import (`crystal backfill` reads Claude Code and OpenClaw JSONL), watermark delta idempotency (`src/mirror-sync.ts`).
- **Repo location decided:** app code goes in `repos/ldm-os/apps/kaleidoscope-private/ios/` per the 2026-04-06 architecture ticket.

## Conflicts and gaps found (now resolved by the decisions above or flagged for build)

- **iOS product identity conflict** with the master ticket / roadmap / four-surface onboarding doc ("do not make the native apps full chat products before they are key/wallet/storage products"). Resolved by D1: one app, chat-shaped, that is also the Phone Key. Master ticket updated.
- **Identity doctrine conflict** (model-defining streams vs "swap the harness, keep the soul"). Resolved by D2.
- **Storage paradigm divergence.** Memory Crystal is terminal SQLite chunks (no event log, autoincrement ids, unsalted `SHA256(text)` dedup); the spec is an event-sourced JSONL log with salted composite dedup. Direction set by D3 (everything ingests into the app's canonical log); the crystal.db relationship at Phase 2 convergence still needs an implementation plan, but Phase 0 is self-contained.
- **Dedup key mismatch to handle at import:** Crystal's unsalted `SHA256(text)` hashes cannot be reused; the import adapter re-derives the spec's salted composite. Identical text Crystal collapsed into one chunk legitimately expands into multiple turns.
- **Embedding is single-space today:** one locked-dimension vec table (1536 local vs 1024 in the deprecated cloud path... a live inconsistency), RRF fuses BM25 + one vector space only. Multi-space, per-space coverage, and Apple/Voyage are all greenfield. Spike 7 has no prior art in the repos.
- **"OpenAI Memory Crystal" (spec §8.4) doesn't exist under that name.** The real import surfaces are better: raw JSONL transcripts archived at `~/.ldm/agents/{agent_id}/memory/transcripts/` (synthesize events from those, not from chunks), plus `crystal.db` chunks with embeddings via `exportChunksSince`.
- **Identity raw material is split across three places that disagree:** the `harnesses` block in `~/.ldm/config.json`, the ID-pattern table in `library/documentation/dev-guide-wipcomputerinc.md`, and the 3-part convention in `ai/product/plans-prds/bridge/2026-04-22--cc-mini--bridge-matrix-and-kaleidoscope-chat-view.md`. The wip-cloud spec also coins surface-as-identity IDs (`claude-ios`, `claude-web`, bare `lesa-mini`) that break the harness-prefix convention. Adjudicated in `harness-profile-catalog.md`.
- **wip-ai-chat-ui-private is an empty skill stub**, not a chat shell candidate. The active client is the Next.js web app in `kaleidoscope-private/web/`. The iOS chat shell follows the MVVM rule in `vision-quest-02-agent-txt-era.md`: SwiftUI native, no React Native.
- **The voice-call ticket** (`tickets/2026-04-24--lesa--native-voice-call-apple-way.md`, P4) now has a home: Call Lēsa lands inside the same iOS app shell.

## Housekeeping done in this PR

- `spec-0-7-1/` archived to `archive/spec-0-7-1/` in this folder. Two sibling folders both labeled FROZEN v0.7.1 was a version-label collision; `spec-0-7-1a/` is authoritative (errata pass, §0a).

## Spec handoff items: where they stand

1. Harness-profile catalog (§5.4): drafted, see `harness-profile-catalog.md`.
2. stream_key onto agent_id (§19.5): rule set by D2, mapping in the catalog.
3. Multi-device embedding coordination (§19.6): "Core is the only embedder" is already Crystal law; multi-space design is Phase 1+ work.
4. Import adapter (§19.7): promoted to first-class by D3; targets the agent-tree corpus, not just Crystal exports.
5. Event-type catalog (§19.8): `capture.*` / `core.*` / `embedding.*` collide with nothing; reserve `wiki.*` per the wiki-layer note; align payload fields with `ConversationData`.

## Co-authors

Co-Authored-By: Parker Todd Brooks <parkertoddbrooks@users.noreply.github.com>
Co-Authored-By: Lēsa <lesaai@icloud.com>
Co-Authored-By: Claude Code (Fable 5) <noreply@anthropic.com>
Co-Authored-By: Codex (GPT 5.5) <noreply@openai.com>
