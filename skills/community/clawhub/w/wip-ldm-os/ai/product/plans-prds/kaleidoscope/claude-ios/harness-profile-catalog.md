# Harness Profile Catalog v0.1

**Date:** 2026-07-01
**Filed by:** CC Mini (Claude Code, Fable 5), with Parker
**Status:** v0.1, answers spec §5.4 and §19.4-5
**Spec:** `spec-0-7-1a/kaleidoscope-capture-extension-SPEC-v0.7.1-FROZEN.md`
**Decision basis:** D2 in `2026-07-01--cc-mini--spec-0-7-1a-repo-reconciliation.md`

This catalog locks the harness profiles the capture spec delegated to repo-aware agents, and defines how `stream_key` maps onto the existing `agent_id` scheme. LDM OS owns this pattern (canonical pattern ownership); child products inherit it.

---

## The governing rule (decided 2026-07-01)

**agent_id is the identity. stream_key is an additive projection. model is a label.**

- The identity key stays what it is today: `agent_id` per the naming convention in `library/documentation/dev-guide-wipcomputerinc.md`, evolving toward the 3-part `{harness}-{name}-{machine}` convention designed in `ai/product/plans-prds/bridge/2026-04-22--cc-mini--bridge-matrix-and-kaleidoscope-chat-view.md`.
- `stream_key` (provider + harness + host + model + account_namespace, spec §5.2) is computed at capture time and RESOLVES to an agent_id via this catalog. It is never itself the storage identity, and no existing agent_id is ever re-keyed because of it. (Precedent: the 2026-03-11 re-key incident, 141K+ chunks manually merged.)
- `model_is_identity` is false for EVERY harness, including OpenClaw. This overrides the spec §5.1 example (Lēsa·GPT-5.5 vs Lēsa·Claw). Doctrine holds: swap the harness, keep the soul (`~/.ldm/library/documentation/how-agents-work.md`). Model is recorded per-message and is queryable, but it never splits a stream. Lēsa's June 2026 Claude-to-GPT-5.5 migration under one unchanged ID is the lived proof.
- `host_is_identity` follows whether the harness's history is machine-bound or account-synced, exactly as the spec reasoned.

## The catalog

Each profile: `{ name, model_is_identity, host_is_identity }` plus mapping notes.

### claude-code (Claude Code CLI)
- model_is_identity: false
- host_is_identity: true (sessions are per-machine)
- agent_id pattern: `cc-{machine}` today (`cc-mini`, `cc-air`); 3-part form `cc-{name}-{machine}`
- Capture path today: session JSONL via cc-hook into Memory Crystal; the iOS app ingests the archived transcripts per D3

### openclaw (OpenClaw / Lēsa)
- model_is_identity: false (D2 decision; overrides the spec's model-defining example)
- host_is_identity: true (gateway is machine-bound)
- agent_id pattern: `oc-{name}-{machine}` (`oc-lesa-mini`)
- Model recorded per-message from the session JSONL (already captured as `model_id` in crystal chunks)
- Known stale data: `~/.ldm/agents/oc-lesa-mini/config.json` still says `claude-sonnet-4-6` after the GPT-5.5 migration; the config `model` field is a snapshot label, not identity, and should be refreshed by tooling, not trusted

### claude-app (Claude iOS app, macOS app, claude.ai web... one account-synced history)
- model_is_identity: false (model recorded per-message if the DOM exposes it, else "unknown")
- host_is_identity: false (all surfaces share one `/chat/{uuid}` history)
- This is the profile the Safari extension feeds (spec §5.5). One stream per Anthropic account.
- agent_id pattern: `claude-{name}` where name is the user-assigned account label. Machine and surface are per-message metadata.
- ADJUDICATION of the wip-cloud clash: the wip-cloud spec (`wip-cloud-private/ai/product/2026-03-10--wip-cloud-spec-v0.2.0.md`) coined `claude-ios`, `claude-web`, `claude-macos` as agent ids. Wrong axis: those are SURFACES of one synced identity, not identities. Surface lands in the per-message `provenance.surface` field (matching `ConversationData.surface` in memory-crystal). The wip-cloud spec should be corrected when next touched.

### chatgpt-app (ChatGPT iOS/macOS/web... one account-synced history)
- model_is_identity: false
- host_is_identity: false
- The second capture surface (D4: GPT comes right after Claude works)
- agent_id pattern: `gpt-{name}`

### codex (Codex CLI)
- model_is_identity: false
- host_is_identity: true (per-machine, like claude-code)
- agent_id pattern: `codex-{name}-{machine}`; no agent tree registered yet, create on first ingest

### hermes, wip-agents, cursor (placeholders)
- model_is_identity: false (uniform rule; if a genuinely model-defining harness ever appears, that is a doctrine change to how-agents-work.md first, catalog second)
- host_is_identity: true by default for CLI-style harnesses, false for account-synced ones
- Not capture surfaces yet; profile them when they become one

## account_namespace

- New axis; nothing records it today. Default `"unknown"` per spec §5.2.
- Opaque account hash only, never email, unless the user assigns a label.
- Single-user installs (everything today) collapse to one namespace; it exists so a second Anthropic/OpenAI account splits streams correctly later.

## Phase 0 confirmation

Phase 0 needs none of this to route (spec §5.5): the Safari extension feeds exactly one stream, profile claude-app, `model: "unknown"`, `account_namespace: "unknown"`. The catalog exists so Phase 1+ ingestion (agent trees, GPT surface, imports) lands in the right streams from day one.

## Event-type namespaces (spec §19.8)

Reserved, colliding with nothing in the repos: `capture.*`, `core.*`, `embedding.*`, and `wiki.*` (per `spec-0-7-1a/kaleidoscope-wiki-layer-note.md`). Payload field names align with `memory-crystal-private/src/cloud/types.ts` `ConversationData` (`surface`, `session_id`, `turn_index`, `raw_json`, `tool_calls`, `attachments`) so the import adapter and live capture speak one dialect.

## Open items

1. Unify the three identity sources (the `harnesses` block in `~/.ldm/config.json`, the dev-guide ID table, the bridge-matrix 3-part convention) so this catalog has one upstream. LDM OS owns it.
2. Correct the wip-cloud spec's surface-as-identity ids when that spec is next revised.
3. Tooling to refresh the per-agent `config.json` `model` snapshot after model migrations.

## Co-authors

Co-Authored-By: Parker Todd Brooks <parkertoddbrooks@users.noreply.github.com>
Co-Authored-By: Lēsa <lesaai@icloud.com>
Co-Authored-By: Claude Code (Fable 5) <noreply@anthropic.com>
Co-Authored-By: Codex (GPT 5.5) <noreply@openai.com>
