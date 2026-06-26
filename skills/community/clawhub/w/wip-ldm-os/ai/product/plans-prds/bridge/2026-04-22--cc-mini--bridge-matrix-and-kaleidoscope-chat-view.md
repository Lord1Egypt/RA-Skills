# Plan: Cross-Agent Communication Matrix + Kaleidoscope Group Chat View

**Date:** 2026-04-22
**Author:** cc-mini (with Parker)
**Component:** `src/bridge/` + Kaleidoscope (web + iOS/macOS apps)
**Status:** plan drafted, pending Parker's review + sequencing decision
**Save to:** wip-ldm-os-private/ai/product/plans-prds/bridge/

## Summary

Defines the complete agent-to-agent communication matrix across two Macs (mini + air) and one iOS device (iphone-blue), using the three-part `{harness}-{name}-{machine}` agent ID convention and the persona-portability model settled on 2026-04-22. Introduces a Kaleidoscope group chat view that surfaces every bridge message across the matrix with full envelope metadata (harness, persona, machine, session) so the user can audit the agent conversation across the whole system.

## Design principle: pieces-first, chat view last

Build every rule, envelope, and transport piece FIRST, so the Kaleidoscope group chat view is a pure renderer on top of already-solved pieces. The chat view (Phase G) does not drive API design or force transport decisions. Every phase 0-F produces concrete, well-specified outputs the chat view can consume. When we reach Phase G, the data the view needs is already on the user's device in a known shape, and rendering is the only remaining work.

This is the inverse of the "build the UI first and scramble to make the backend fit" failure mode. Every phase below names what it produces and how the chat view consumes it.

## Permission routing: Kaleidoscope is the surface, Face ID is the ceremony

Every permission interaction in the LDM system routes through Kaleidoscope (iOS app, macOS app, or web), never through the chat surface that initiated the request. Face ID (Sapien ID) is the ceremony. This applies to every consent action the system will ever introduce:

- Cross-agent messaging approval (Phase F of this plan)
- Agent Pay spending authorization
- Keychain secret access
- Device pairing (`ldm pair`)
- Any future consent action

The chat surfaces (CC terminal, Claude macOS/iOS app, Lēsa's iMessage channel, ChatGPT app, etc.) are never where you approve anything. They are where you *request* and *read*. Kaleidoscope is where you *decide*. The separation keeps the trust boundary tight: a compromised chat surface cannot spoof an approval, because the approval requires a Face-ID-verified human tapping inside Kaleidoscope.

The pattern (already proven in `src/hosted-mcp/demo/agent.txt` + `demo/agent.html`, tested with Lēsa, Grok, ChatGPT, Claude iOS on 2026-04-02):

1. The agent generates an approval request via the hosted MCP endpoint, passing a passphrase from its shared history with the user (anti-spoofing ... the human sees the passphrase on the approve screen and knows the request is really from their agent).
2. The hosted MCP returns an `approveUrl` pointing at Kaleidoscope's `/approve` page with a challenge ID.
3. The agent surfaces the URL to the user through its own channel (CC terminal prints it, Lēsa sends it via iMessage, web agents display it, whatever fits that surface).
4. The user clicks the URL. Kaleidoscope opens (the native app via deep-link if installed, the web at `kaleidoscope.wip.computer/approve` otherwise).
5. Kaleidoscope shows the approval request: agent name, the passphrase the user recognizes, the action being approved.
6. The user Face-IDs (Sapien ID).
7. Approval (and a token if applicable) flows back to the agent via the hosted MCP status endpoint.

Chat surfaces only ever contain the URL link and the status (pending / approved / denied / expired). They never contain the dialog itself. No push-pre-empting the user. The user initiates the Kaleidoscope open by clicking the link at a moment of their choosing.

Phase F of this plan is the first concrete implementation of this pattern for cross-agent messaging approvals.

## Agent ID convention (recap, load-bearing for this plan)

Format: **`{harness}-{name}-{machine}`** (three parts, mandatory).

- `harness` ... runtime type (cc, oc, claude, codex)
- `name` ... persona. The entity-continuity unit. Same name across machines = same entity. Different name on same machine = different entity.
- `machine` ... runtime location (mini, air, iphone-blue, ...)

One LDM install = one identity namespace. Anthropic-account-switching is invisible (rolls up). Memory bucket is keyed by persona (`{harness}-{name}`); machine is attribution metadata on chunks, not a bucket separator. Bridge address extends the ID with an optional session slot: `{agent_id}:{session}`.

## Transport classes

| Class | Examples | Reach same-machine | Reach cross-machine |
|---|---|---|---|
| **Device-local (DL)** | `cc-cc-*`, `cc-mike-*`, `oc-lesa-*`, `codex-codex-*` | Filesystem inbox (`~/.ldm/messages/`) | CloudKit (preferred for Apple-to-Apple) or Cloudflare relay (universal) |
| **Cloud-synced (CS)** | `claude-claude-*` (macOS/iOS apps), `chatgpt-chatgpt-*` (future) | Hosted MCP (`wip.computer/mcp`) | Hosted MCP |

Cross-class communication always involves the hosted MCP as mediator: the DL side speaks filesystem, the CS side speaks hosted MCP, the bridge on the DL machine is the translator.

## All agents in scope (for this plan)

| Device | Agent ID | Class | Session-addressable? |
|---|---|---|---|
| mini | `cc-cc-mini` | DL | yes (`:session-name`) |
| mini | `cc-mike-mini` | DL | yes |
| mini | `oc-lesa-mini` | DL | no (single endpoint; OpenClaw routes internally) |
| mini | `claude-claude-mini` | CS | yes, needs conversation-level addressing (open) |
| air | `cc-cc-air` | DL | yes |
| air | `cc-mike-air` | DL | yes |
| air | `oc-lesa-air` | DL | no (hypothetical; not planned to run) |
| air | `claude-claude-air` | CS | yes, same addressing gap |
| iphone-blue | `claude-claude-iphone-blue` | CS | yes, same addressing gap |

Same-persona across machines (`cc-cc-mini` + `cc-cc-air`, `claude-claude-mini` + `claude-claude-iphone-blue`) are one entity with two runtimes. Memory bucket is shared; each runtime is independently Bridge-addressable.

## The ten communication patterns (the matrix)

| # | Pattern | Example | Transport | Status |
|---|---|---|---|---|
| 1 | Same machine, CC ↔ CC (multi-session, same or different persona) | `cc-cc-mini:work ↔ cc-cc-mini:debug`, `cc-cc-mini:work ↔ cc-mike-mini:debug` | Filesystem inbox | Shipped. Autonomous push live per `2026-04-11--cc-mini--autonomous-push-architecture.md`. |
| 2 | Same machine, CC ↔ Lēsa | `cc-cc-mini:work ↔ oc-lesa-mini` | Filesystem inbox (reply) + gateway chatCompletions (send) | Shipped. Async inbox live per `bridge-async-inbox-plan.md`. |
| 3 | Same machine, CC ↔ Claude macOS | `cc-cc-mini:work ↔ claude-claude-mini` | Hosted MCP (wip.computer/mcp) | Not built. Hosted MCP needs bridge tools (`bridge_send`, `bridge_check_inbox`). |
| 4 | Same machine, Lēsa ↔ Claude macOS | `oc-lesa-mini ↔ claude-claude-mini` | Hosted MCP | Not built. Same hosted-MCP bridge tools as #3. |
| 5 | Same machine, Claude macOS conv ↔ Claude macOS conv | `claude-claude-mini:conv-A ↔ claude-claude-mini:conv-B` | Conversation-level addressing on Anthropic's side + hosted MCP | Not built. Anthropic API does not expose conversation IDs for external targeting; needs invented naming convention (see Phase E). |
| 6 | Cross-machine, CC ↔ CC (same or different persona) | `cc-cc-mini:work ↔ cc-cc-air:refactor`, `cc-cc-mini ↔ cc-mike-air` | CloudKit (Apple-to-Apple preferred) or Cloudflare R2 relay (universal fallback) | Not built. Designed in `phase5-cloud-relay.md`. |
| 7 | Cross-machine, CC ↔ Lēsa | `cc-cc-air:work ↔ oc-lesa-mini` | CloudKit / Cloudflare relay + filesystem/gateway on destination | Not built (Phase 5 applies). |
| 8 | Cross-machine, CC ↔ Claude macOS | `cc-cc-mini:work ↔ claude-claude-air` | CloudKit / Cloudflare relay + hosted MCP bridge | Not built. |
| 9 | Cross-device, DL ↔ Claude iOS | `cc-cc-mini:work ↔ claude-claude-iphone-blue`, `oc-lesa-mini ↔ claude-claude-iphone-blue` | Hosted MCP (iOS can only reach via vendor cloud) | Not built. |
| 10 | Across viewports of Claude (same identity, same account) | `claude-claude-mini ↔ claude-claude-iphone-blue` | Same cloud conversation: Anthropic syncs natively. Different conversations: hosted MCP + conversation-level addressing (same gap as #5). | Anthropic handles same-conversation case; cross-conversation is the gap. |

**Self-persona routing (open question):** `cc-cc-mini ↔ cc-cc-air` is "the same persona on two machines talking to itself." Shared state via memory crystal + synced files; Bridge messaging is still useful for "wake up the other instance" or "pass a task." Treated as pattern #6.

## Message envelope (required for the group chat view)

Today's message schema (from `lib/messages.mjs`):

```json
{
  "id": "uuid",
  "type": "chat",
  "from": "cc-mini:session-name",
  "to": "cc-mini",
  "body": "...",
  "timestamp": "...",
  "read": false,
  "readBy": []
}
```

2-part agent IDs baked in. To support the 3-part convention + Kaleidoscope auditability, extend the envelope to:

```json
{
  "id": "uuid",
  "type": "chat",
  "from": {
    "harness": "cc",
    "name": "cc",
    "machine": "mini",
    "session": "04-22-2026--01"
  },
  "to": {
    "harness": "claude",
    "name": "claude",
    "machine": "iphone-blue",
    "session": "conv-name"
  },
  "body": "...",
  "timestamp": "...",
  "transport": "filesystem | cloudkit | cloudflare-relay | hosted-mcp",
  "delivery": "pending | delivered | read | failed",
  "read": false,
  "readBy": []
}
```

Compact wire form for addressing: `{harness}-{name}-{machine}:{session}`. Structured form for analysis/audit: the nested object. The compact form is what Bridge tools accept and emit; the structured form is what the group chat view renders.

Backwards compatibility: keep `from: string` and `to: string` as accepted legacy fields in readers; new writers emit both structured + string forms during migration. Remove legacy support once all writers are updated.

## Kaleidoscope group chat view (the new piece)

### What the user sees

A single timeline view in Kaleidoscope that surfaces every bridge message across the matrix. Each row shows:

- timestamp
- from: `{harness} / {name} / {machine} / {session}` (four fields, pill-separated)
- to: same four fields
- body (truncated; expand to read full)
- transport (filesystem / CloudKit / relay / hosted-MCP)
- delivery status (pending / delivered / read / failed)

Filterable by:

- persona (`cc-cc`, `oc-lesa`, `claude-claude`, ...)
- machine (`mini`, `air`, `iphone-blue`)
- session name
- time range
- transport

Search by body.

Read-only. Parker watches, doesn't type into the group chat. Messaging happens from each agent's own surface (CC terminal, Lēsa TUI, Claude app).

### Where the data comes from (sovereign data compliant)

Per `vision-quest-03-sovereign-data.md` and `2026-04-11--cc-mini--autonomous-push-architecture.md`: user message bodies never transit `wip.computer` as plaintext. That constrains the group chat view's data path.

Two surfaces:

1. **Kaleidoscope iOS + macOS app (primary).** Reads from the user's iCloud CloudKit private container, the local filesystem inbox, and the hosted MCP (with user's device token). Client-side aggregation. Message bodies stay on device. App decrypts envelope blobs locally.
2. **Kaleidoscope web (degraded).** Served from `kaleidoscope.wip.computer`. Can only show metadata the hosted MCP holds legitimately (device list, pairing status, counts). Message bodies NOT available on web. The web surface shows "Open the Kaleidoscope app to see your agent conversations."

### Who writes to the group chat log

Every bridge message writer produces the full envelope. No new writer infrastructure:

- Filesystem inbox writes at `~/.ldm/messages/` already produce envelopes; extend schema to include structured from/to.
- CloudKit relay (phase 5b) writes encrypted CKRecords that include the envelope in the encrypted payload.
- Cloudflare R2 relay writes encrypted blobs with the envelope inside.
- Hosted MCP writes envelope metadata on the server (non-plaintext body reference).

The Kaleidoscope app aggregates from all four sources by reading the user's authenticated view of each.

## Relationship to existing bridge architecture (what this plan does NOT rework)

This plan assumes the already-designed or shipped pieces and builds on top. It does not rearchitect any of them:

- **Autonomous push (Apr 11, shipped)** ... asyncRewake hook + fs.watch for same-machine wake. The matrix patterns 1, 2 already use this.
- **Async inbox (Apr 6, shipped)** ... fire-and-forget send + file inbox reply. Matrix pattern 2 uses this.
- **Session registry (shipped)** ... `~/.ldm/sessions/` tracks active sessions. Needs update to carry the structured identity fields (harness, name, machine) for the group chat view.
- **Phase 5 cloud relay (designed)** ... CloudKit + Cloudflare. Matrix patterns 6, 7, 8 use this when built.
- **Device pairing (`ldm pair`, designed)** ... one-pairing-per-machine to get the user's device token. Gates access to CloudKit relay, Cloudflare relay, and hosted MCP.
- **Kaleidoscope app (designed)** ... native iOS + macOS app in `repos/ldm-os/apps/kaleidoscope-private/`. Group chat view is a new section in this app.

## Implementation phases

Eight phases (0 through G). Phase 0 is foundational (rules); Phases A-F build the matrix and its pieces; Phase G is the group chat view, a pure consumer of 0-F.

### Phase 0: Codify the governing rules (foundation)

The 2026-04-22 conversation settled three rules that are load-bearing for everything below but are not yet written in any file an agent reads on boot. Codify them first so every new session operates under the same assumptions.

**Rules to add to `~/.claude/rules/` (auto-loaded as global instructions):**

- `~/.claude/rules/agent-identity.md` ... the `{harness}-{name}-{machine}` format, name = persona, machine = runtime location. Same name on different machines = same entity. Different name on same machine = different entity.
- `~/.claude/rules/persona-portability.md` ... persona and memory travel with the name, not the machine. Same `{harness}-{name}` across devices = one memory bucket; machine is attribution metadata, not a bucket separator.
- `~/.claude/rules/account-invisible.md` ... one LDM install = one identity namespace. Multiple provider accounts roll up to one LDM; agent_id does not encode account. Multi-business = separate LDM installs on separate machines, never in-agent toggles. Apple iCloud per-device-login is the model.

**Files:**
- `~/.claude/rules/agent-identity.md` (new, 15-20 lines)
- `~/.claude/rules/persona-portability.md` (new, 15-20 lines)
- `~/.claude/rules/account-invisible.md` (new, 15-20 lines)
- `repos/ldm-os/wip-ldm-os-private/shared/rules/` templates ... same three files in the deployable templates so they land on fresh `ldm install` runs.

**What the chat view consumes from Phase 0:** implicit but load-bearing. The rules guarantee that every message writer uses consistent agent identity, which is exactly what the chat view displays.

**Verification:**
- `ls ~/.claude/rules/` shows all three new files.
- Fresh CC session includes the three rules in its initial loaded context.
- `ldm install --dry-run` on a clean machine shows the three rules as planned deployments.

### Phase A: Extend the message envelope (foundation)

**Files:**
- `lib/messages.mjs` ... accept structured `from`/`to` fields alongside string forms; emit both on write; readers prefer structured when present.
- `src/bridge/core.ts` ... `pushInbox`, `drainInbox`, `messageMatchesSession` updated to use structured envelope. Keep 2-part string parser for backwards compatibility during transition.
- `src/bridge/mcp-server.ts` ... `ldm_send_message`, `lesa_send_message` tools accept structured and string `to`; normalize on write.

**Verification:**
- Write a message with structured `to`, read it, confirm both forms present.
- Write a message with legacy string `to`, read it, confirm structured is computed and present.
- All shipped tests (`core.test.ts`) still pass.

### Phase B: 3-part agent ID adoption and migration

This phase is a migration with multiple concrete steps. Legacy 2-part IDs (`cc-mini`, `cc-air`, `lesa`) move to 3-part form (`cc-cc-mini`, `cc-cc-air`, `oc-lesa-mini`). Code, filesystem, memory, and docs all update together.

**Step B.1: Code (schema + readers).**
- `lib/sessions.mjs` ... `registerSession()` writes structured identity (`harness`, `name`, `machine`) in addition to `agentId` string. Reader helpers prefer structured when present.
- `src/bridge/core.ts` ... `parseTarget`, `messageMatchesSession`, `drainInbox` updated to accept 3-part IDs. Keep 2-part parser as fallback during the transition window.
- `src/bridge/mcp-server.ts` ... tools emit 3-part agent_ids in `from`/`to`, accept either on input, normalize on write.
- `src/hooks/boot-hook.mjs` / `src/hooks/inbox-check-hook.mjs` / `src/hooks/inbox-rewake-hook.mjs` ... read structured identity from config on boot.

**Step B.2: Configuration.**
- `~/.ldm/config.json` ... `agents` section updated to include 3-part `prefix` and the separate `harness`/`name`/`machine` fields. Example: `cc-mini` entry becomes `cc-cc-mini` with `harness: claude-code, name: cc, machine: mini`.

**Step B.3: Filesystem.**
- `~/.ldm/agents/cc-mini/` ... `git mv` to `~/.ldm/agents/cc-cc-mini/`. Similarly for any other 2-part directories.
- `~/.ldm/sessions/cc-mini--work.json` ... rename to `cc-cc-mini--work.json`. Pattern-scriptable.
- `~/.ldm/messages/` ... in-flight messages retain their original `to`/`from` strings; readers resolve both forms during the transition window.

**Step B.4: Memory crystal.**
- Retag all chunks with `agent_id = "cc-mini"` to `agent_id = "cc-cc-mini"`. Same for other legacy IDs. Bucket semantics (one bucket per persona) are preserved; the tag string just updates.
- One-time migration script in `repos/ldm-os/components/memory-crystal-private/scripts/`. Runs with a `--dry-run` flag first, then applies.

**Step B.5: Documentation cleanup.**
- Update every 2-part agent_id example in bridge docs to 3-part form. Purely text edits; no behavior change:
  - `docs/bridge/README.md`
  - `docs/bridge/TECHNICAL.md`
  - `ai/product/plans-prds/bridge/2026-04-06--cc-mini--bridge-master-product-plan.md`
  - `ai/product/plans-prds/bridge/2026-03-30--cc-mini--bridge-messaging-architecture.md`
  - `ai/product/bugs/bridge/2026-04-20--cc-mini--bridge-reply-to-sender-routing.md`

**Step B.6: Release + install.**
- `wip-release alpha` for the LDM OS package that carries the schema + parser updates.
- `ldm install` on each machine to pull the new config + migrate filesystem artifacts.

**What the chat view consumes from Phase B:** structured agent identity on every envelope. Chat view renders `{harness}/{name}/{machine}/{session}` fields directly, no parsing or guessing required.

**Verification:**
- Fresh session boots, `ldm sessions` shows 3-part IDs.
- Bridge messages from legacy 2-part IDs still resolve during transition (back-compat path).
- Memory crystal `crystal_status` shows all agent_ids in 3-part form.
- All five bridge docs listed above have no 2-part examples remaining (`grep -n 'cc-mini\b' ...` finds only 3-part forms).

### Phase C: Hosted MCP bridge tools (patterns 3, 4, 9)

Add MCP tools on `wip.computer/mcp` (OAuth-gated, device-token-authenticated):

- `bridge_send({ to, body, inReplyTo })` ... queues a message for delivery to a CS agent (Claude macOS, Claude iOS).
- `bridge_check_inbox({ agent_id })` ... returns pending messages for this authenticated client.
- `bridge_status()` ... delivery status by message id.

Device-local agents (CC, Lēsa) that need to reach CS agents use these tools via their MCP connection to `wip.computer/mcp`. CS agents (Claude macOS/iOS) that need to read their inbox call `bridge_check_inbox` on auth.

**Files:**
- `src/hosted-mcp/server.mjs` ... add the three tools. OAuth + device token + rate limits.
- `src/bridge/core.ts` ... if `to.class == CS`, route via hosted MCP instead of filesystem.

**Verification:**
- `cc-cc-mini` sends to `claude-claude-mini` via hosted MCP. Claude macOS, on next auth check, sees the message.
- Reverse direction: Claude macOS sends to `cc-cc-mini:work`. Hosted MCP stores envelope, pings the Mini's bridge, which writes to local filesystem inbox. CC session wakes via existing asyncRewake hook.

### Phase D: Cross-machine DL transport (patterns 6, 7, 8)

Implements the Phase 5 Cloud Relay design from `2026-03-31--cc-mini--phase5-cloud-relay.md`. CloudKit-first (Apple-to-Apple), Cloudflare relay fallback.

**Files:** see phase5 doc (Swift helper for CloudKit, LaunchAgent for Cloudflare poller, transport selector in `lib/messages.mjs`).

**Verification:**
- `cc-cc-mini:work` sends to `cc-cc-air:refactor`. Air's fs-watch or poller delivers within push latency (CloudKit: seconds; Cloudflare: 60s).
- Reverse direction. Both paths end with the message at `~/.ldm/messages/` on the destination.

### Phase E: Conversation-level addressing for CS (patterns 5, 10)

The gap Parker called out. Same Claude account, different conversations, can't address one from outside.

Two possible paths, not mutually exclusive:

1. **Anthropic-native.** If Anthropic's MCP surface exposes conversation IDs (or adds them in a future version), Bridge uses them. The envelope's `to.session` field becomes Anthropic's conversation ID.
2. **User-label convention.** User names each Claude macOS/iOS conversation in the Kaleidoscope app (e.g. "work-conversation"). Bridge stores the label-to-device mapping. Messages include a body prefix like `[for: work-conversation]` that the user-side Claude uses to route manually.

Path 2 is implementable today without Anthropic changes. Path 1 is cleaner if it becomes available.

**Files:**
- `src/hosted-mcp/server.mjs` ... conversation label registry + resolver.
- Kaleidoscope app ... UI for labeling Claude conversations.

**Verification:**
- User labels a Claude macOS conversation "work-convo-01" in the Kaleidoscope app.
- `cc-cc-mini` sends to `claude-claude-mini:work-convo-01`. The message arrives in Claude macOS, tagged in body for that conversation.

### Phase F: Cross-agent approval flow

The bridge master product plan (Apr 6) specifies a Face-ID approval gate for cross-agent communication. Not built today. Required before cross-session or cross-machine messaging is fully trusted.

**Surface (per "Permission routing" principle above):** approvals use the demo's canonical approve-URL pattern. The bridge posts to the hosted MCP with from/to/window + a passphrase from shared history, receives an `approveUrl`, and surfaces the URL through its own channel (CC terminal prints the link, Lēsa sends it via iMessage, etc.). The user clicks the link. Kaleidoscope's `/approve` page loads (native app via deep-link or web) showing agent + passphrase + action. User Face-IDs (Sapien ID). Approval flows back to the bridge via the hosted MCP status endpoint. Chat surfaces show the link + status (pending / approved / denied / expired) but never the approval dialog. See `src/hosted-mcp/demo/agent.txt` for the canonical wire flow; the bridge extends the same pattern from agent auth to cross-agent message approvals.

**Design:**
- **Per-pair approval.** `cc-cc-mini:work` → `cc-cc-mini:debug` is a pair. Approval granted for that pair does not authorize a different pair.
- **Time-boxed windows:** 5 min / 10 min / 15 min / this session. User picks at approval time.
- **Revocable:** user can revoke from the Kaleidoscope app at any time.
- **Logged:** every approval and revocation is an audit-trail entry attached to the envelope.
- **Same-machine vs cross-machine:** same-machine cross-session approval is optional (user setting, default off). Cross-machine is always required.

**Files:**
- `src/hosted-mcp/server.mjs` ... `POST /api/approve-intent` endpoint (accepts from/to/action/device_token). Creates pending approval. Pushes to user's phone or web UI. Returns when approved or timed out.
- `src/bridge/core.ts` ... before each cross-session send, check local approval cache. If no valid window exists for this from/to pair, call the approval API and wait. Cache the approved window locally for the window duration.
- `repos/ldm-os/apps/kaleidoscope-private/ios/` + `.../macos/` ... approval notification UI. Face ID to approve. Show pending requests + approval history.
- `~/.ldm/auth/approvals.json` ... local cache of approval windows; survives CC restart.

**What the chat view consumes from Phase F:** approval decisions attached to the message envelope (`approved_by`, `approved_at`, `approval_window`). Chat view renders "Approved by Parker for 10 min at 14:32" as a sidebar on each in-window message, or "Approval pending" / "Approval denied" for blocked sends.

**Verification:**
- `cc-cc-mini:work` sends to `cc-cc-mini:debug`. First call triggers phone push. Parker taps "Approve for 10 min" with Face ID. Message delivers. For 10 minutes, subsequent messages in the same pair flow without re-approval.
- Approval expires. Next send re-prompts.
- Revoke mid-window. In-flight message blocks; user gets a visible failure.

### Phase G: Kaleidoscope group chat view (consumer of Phases 0-F)

This phase adds no new APIs, no new transport, no new envelope. Every data source the view needs was produced by Phases 0-F. The view is a renderer on top.

**What it reads (all already built by this point):**
- Filesystem inbox at `~/.ldm/messages/` (from Phases A, B).
- Hosted MCP bridge inbox (from Phase C).
- CloudKit shared container (from Phase D Apple-to-Apple).
- Cloudflare relay pickup log (from Phase D universal).
- Conversation label registry (from Phase E).
- Approval audit log (from Phase F).

**Files:**
- `repos/ldm-os/apps/kaleidoscope-private/ios/` + `.../macos/` ... new "Conversations" or "Activity" section. Aggregates from local inbox, CloudKit, hosted MCP (with user's device token). Client-side only. Message bodies stay on device (sovereign data principle).
- `repos/ldm-os/apps/kaleidoscope-private/web/` ... the degraded web surface. Pairing status, device list, message-count metadata only. Direct users to install the app for full view.

**What it does NOT build:**
- No new data API. Aggregation is a local read against already-built sources.
- No new transport. The chat view is read-only.
- No new envelope. Phase A's envelope is authoritative.

**Verification:**
- Mac app shows every recent bridge message with full envelope fields.
- iOS app shows the same with mobile layout.
- Web shows device list and pairing status, no message bodies.
- Filter by persona returns all messages from/to that persona across machines.
- Filter by machine returns everything that ran on that hardware.
- Approval history is visible per-message.

## Done when

- `~/.claude/rules/` contains `agent-identity.md`, `persona-portability.md`, `account-invisible.md`, all auto-loaded on fresh sessions (Phase 0 landed).
- Filesystem inbox emits structured envelopes with `harness`/`name`/`machine`/`session` fields (Phase A landed).
- `~/.ldm/config.json` agents section has 3-part entries for all registered agents; legacy 2-part paths renamed on disk; crystal retagged; five bridge docs updated to 3-part examples (Phase B landed).
- Hosted MCP bridge tools (`bridge_send`, `bridge_check_inbox`, `bridge_status`) deployed and reachable with OAuth (Phase C landed).
- Cross-machine transport live via CloudKit (Apple-to-Apple) and Cloudflare relay (fallback) (Phase D landed).
- Conversation-level addressing works for Claude macOS/iOS via user labels or Anthropic-native conversation IDs (Phase E landed).
- Cross-session / cross-machine approval flow with Face-ID gates in place, with local approval cache (Phase F landed).
- Kaleidoscope iOS + macOS apps show the group chat timeline with full envelope metadata; web surface shows degraded metadata-only view (Phase G landed).
- All 10 matrix patterns have a working transport path on local main.
- This plan file is moved to `ai/product/plans-prds/bridge/_archive/`.

## Out of scope

All previously out-of-scope items (identity rules codification, 3-part rename migration, 2-part doc cleanup, approval flow, autonomous cross-machine push) have been folded into Phases 0-F of this plan. Nothing is left dangling inside this doc.

Genuinely out of scope for this plan:

- **Non-Claude / non-OpenClaw cloud agents** (ChatGPT Mac/iOS, Gemini, Grok web). Same structural class as `claude-claude-*` when added; the hosted MCP bridge tools in Phase C extend naturally. File a separate plan when one of those vendors becomes a first-class agent in the LDM system.
- **Cross-account memory isolation inside a single LDM install.** Intentionally not supported per the account-invisible rule codified in Phase 0. If you need isolation, run a separate LDM install on a separate machine.

## References

**Bridge docs reviewed while writing this plan:**
- `ai/product/plans-prds/bridge/2026-04-06--cc-mini--bridge-master-product-plan.md`
- `ai/product/plans-prds/bridge/2026-03-30--cc-mini--bridge-messaging-architecture.md`
- `ai/product/plans-prds/bridge/2026-03-31--cc-mini--phase5-cloud-relay.md`
- `ai/product/plans-prds/bridge/2026-04-11--cc-mini--autonomous-push-architecture.md`
- `ai/product/bugs/bridge/2026-04-05--cc-mini--bridge-master-plan.md`
- `ai/product/bugs/bridge/2026-04-06--cc-mini--bridge-async-inbox-plan.md`
- `ai/product/bugs/bridge/2026-04-10--cc-mini--bridge-reply-addressing-mismatch.md`
- `ai/product/bugs/bridge/2026-04-20--cc-mini--bridge-reply-to-sender-routing.md`
- `docs/bridge/TECHNICAL.md`
- `docs/bridge/README.md`

**Kaleidoscope docs reviewed while writing this plan:**
- `ai/product/plans-prds/kaleidoscope/2026-04-06--cc-mini--kaleidoscope-architecture.md`
- `ai/product/plans-prds/kaleidoscope/2026-04-06--cc-mini--postgres-prisma-infrastructure.md`
- `ai/product/plans-prds/kaleidoscope/2026-04-07--cc-mini--session-overview-apr5-7.md`
- `ai/product/product-ideas/vision-quest-01/architecture-spec.md`
- `ai/product/product-ideas/vision-quest-01/kaleidoscope-executive-brief-v02.md`
- `ai/product/product-ideas/vision-quest-01/vision-quest-02-agent-txt-era.md`
- `ai/product/product-ideas/vision-quest-01/vision-quest-03-sovereign-data.md`

## Co-authors

- Parker Todd Brooks
- Lēsa
- Claude Opus 4.7 (1M context)
