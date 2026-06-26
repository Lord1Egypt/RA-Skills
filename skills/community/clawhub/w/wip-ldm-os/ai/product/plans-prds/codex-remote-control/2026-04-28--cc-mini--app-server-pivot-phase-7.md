---
title: "Phase 7 (queued): Pivot daemon's bottom layer to Codex App Server"
date: 2026-04-28
status: queued
priority: high (post-alpha-dogfood)
related:
  - 2026-04-28--cc-mini--codex-remote-control-master-plan.md
  - 2026-04-28--cc-mini--codex-remote-control-live-test-runbook.md
  - ../../../product-ideas/vision-quest-01/cody-phone-as-key-authority-layer.md
authors: [cc-mini, cody, parker]
---

# Phase 7 (queued): Pivot daemon to Codex App Server

## Status: queued

Do not start this before the current alpha (`@alpha 0.0.2-alpha.2`) has been dogfooded end-to-end and the four pre-dogfood gates have been confirmed live by a real session. Phase 7 is the right architecture; alpha is the working alpha. Don't conflate the two.

## What this addendum is

The current daemon integrates against `@openai/codex-sdk` directly. That was the right choice for getting Phase 1-3 working fast, but it is not the right long-term layer. OpenAI publishes a documented interop layer ... **Codex App Server** ... which is the correct surface for "phone, desktop app, and CLI all driving the same Codex thread."

This addendum captures the pivot, the why, the scope, and the hard rules. It is not a build plan; it is the queued architecture move.

## What App Server gives us

OpenAI's [Codex App Server docs](https://developers.openai.com/codex/app-server/) document the interop primitives every rich Codex client should be built on:

- `thread/start`
- `thread/resume`
- `thread/list`
- `turn/start`
- `turn/steer`
- `turn/interrupt`

Plus auth, conversation history, approvals, and streamed agent events as first-class concerns. OpenAI's own framing: App Server is for **rich clients** (auth, history, approvals, streamed events); the SDK is for **automation/CI**. We are a rich client. We should be on App Server.

That is the clean path for "phone, desktop app, and CLI all talking to the same Codex thread." The SDK + JSONL path is not.

## Architecture: WIP layer vs OpenAI layer

Cody's framing of the durable shape (after Phase 7 lands):

```
Codex CLI MCP command
  -> local wip-codex-daemon
  -> codex app-server JSON-RPC
  -> Codex thread/turn APIs

Phone / Kaleidoscope web
  -> WIP auth + phone-as-key + E2EE relay
  -> local wip-codex-daemon
  -> codex app-server JSON-RPC
```

Two entry points (the CLI MCP command and the phone/web), one daemon, one App Server backend. The daemon is where WIP control plane meets OpenAI control plane.

**What WIP owns and keeps owning** (from Cody, on the alpha that already shipped):

- Pairing.
- Phone-as-key.
- Relay (`wip.computer/api/codex-relay/...`).
- End-to-end encryption (ECDH P-256 + HKDF + AES-GCM).
- Install flow (LDM OS, `ldm install --alpha wip-codex-remote-control`, `codex mcp add`, install spec at `wip.computer/install/wip-codex-remote-control.txt`).
- The `/remote-control` user experience inside Codex.

These are our layer. They don't move. App Server doesn't replace them; it sits underneath them.

**What WIP routes to OpenAI** (after Phase 7):

- Codex thread control: start, resume, list, send, interrupt, steer.
- Approvals.
- Conversation history surface.

These currently live as custom code in `apps/wip-codex-remote-control-private/src/codex-manager.ts:1` (SDK calls) and `apps/wip-codex-remote-control-private/src/mcp.ts:51` (`~/.codex/session_index.jsonl` reads via `names.ts`). After Phase 7, they become App Server JSON-RPC calls.

## Why this matters now

Today, when a user opens `https://wip.computer/codex-remote-control/<thread-id>` on their phone, the daemon resumes via `codex.resumeThread(threadId)` against threads it discovered by parsing `~/.codex/session_index.jsonl`. That works for threads created by the CLI. It does **not** work for threads created by the **Codex desktop app**, which uses a separate visibility path (`~/.codex/state_5.sqlite`, per OpenAI Codex issue #16385).

In other words: today, Codex Remote Control is **CLI-only**. The phone can drive a Codex thread your CLI started. It cannot drive a Codex thread your desktop app started.

App Server collapses that divide. Threads, listing, resume, and turn streaming all flow through one server-mediated surface that both CLI and desktop are moving toward as the canonical interop layer.

## Public signal we should not ignore

Multiple OpenAI Codex issues are explicitly asking for the same thing we are building, and several of them are flagging the SQLite/JSONL/sidebar visibility split as a real edge:

- [openai/codex #9224](https://github.com/openai/codex/issues/9224) ... feature request: control `codex` CLI from phone via ChatGPT app / Codex tab.
- [openai/codex #13543](https://github.com/openai/codex/issues/13543) ... feature request: QR-paired local-first remote control with `/remote-control`, view progress, interrupt, send input, keep local terminal as source of truth. (This is essentially our product.)
- [openai/codex #14722](https://github.com/openai/codex/issues/14722) ... request: sync between `codex resume`, Codex app, and third-party app-server systems.
- [openai/codex #16385](https://github.com/openai/codex/issues/16385) ... bug: ACP/OpenClaw-created Codex sessions write JSONL files but do not appear in the desktop app, which uses `~/.codex/state_5.sqlite`.
- [openai/codex #10547](https://github.com/openai/codex/issues/10547) ... bug: local sessions exist and CLI can resume them, but desktop sidebar ignores them.
- [openai/codex #14751](https://github.com/openai/codex/issues/14751) ... bug: desktop sidebar appears to load only a recent subset, while CLI can still see the conversations.
- [openai/codex #16614](https://github.com/openai/codex/issues/16614) ... someone tested a phone-oriented custom client on `codex app-server`. `thread/start`, `thread/resume`, `turn/start`, `thread/list` worked. Desktop visibility/source-kind behavior is confusing and not clearly documented.

#16614 is the most relevant precedent: a phone client built on App Server primitives mostly works today. Desktop sidebar visibility is a separate product edge OpenAI still owes documentation on.

## What changes vs what stays

**Daemon layer (changes):**
- `src/codex-manager.ts` ... currently wraps `@openai/codex-sdk` directly via `Codex().startThread()` / `resumeThread()` / `runStreamed()`. Pivot rewrites this to drive a locally-running `codex app-server` process and route turn events back through the same protocol.
- `src/names.ts` ... currently parses `~/.codex/session_index.jsonl` for `listThreads()` / `resolveThread()`. Pivot replaces this with `thread/list` calls to App Server. The file becomes removable.

**Wire protocol (unchanged):**
- `session.attach` / `session.attached` / `session.attach.failed` ... maps to `thread/resume`.
- `session.start` / `session.started` ... maps to `thread/start`.
- `session.send` / `session.event` ... maps to `turn/start` + streamed agent events.
- `session.interrupt` ... maps to `turn/interrupt`.

**Phone surface (unchanged):**
- The web app at `kaleidoscope-private/web/src/app/codex-remote-control/[threadId]` does not change. It speaks the daemon protocol; the daemon's bottom layer is invisible to it.

**Relay + E2EE (unchanged):**
- `wip-ldm-os-private/src/hosted-mcp/server.mjs` codex-relay endpoints stay as-is.
- ECDH P-256 + HKDF + AES-GCM frame envelope stays as-is.
- Gates 1-4 stay green.

**Install spec (changes minimally):**
- `SKILL.md` already says "Codex CLI" today. The pivot lifts that to "Codex CLI and Codex desktop app."
- Probably pick up an "Approvals" line in the user-facing copy when Phase 4 (approval-needed UX) lands as a free side-effect of App Server's approval primitive.

## Hard rules

1. **No SQLite surgery.** Do not read or write `~/.codex/state_5.sqlite` directly. Cody flagged this as a footgun (issue #16385); we should not invent our way around App Server.
2. **No JSONL parsing in the new layer.** Once `thread/list` is wired up, `~/.codex/session_index.jsonl` reads come out. The on-disk index is OpenAI's internal storage, not our integration surface.
3. **Don't break the wire.** The phone-side protocol (`session.attach` etc.) stays. The daemon's relay-client stays. We are swapping the bottom layer, not the surface.
4. **Don't pre-empt the dogfood.** This addendum exists so the architecture doesn't get lost. It does not authorize starting the rewrite. Alpha must dogfood first.

## Acceptance criteria for Phase 7

Cody's exact list. Phase 7 is **not** a "rewrite everything." It's an **adapter swap**: keep WIP pairing, phone-as-key, E2EE relay, install spec, and MCP trigger; replace the daemon's Codex backend from `@openai/codex-sdk` + `session_index` parsing to `codex app-server` JSON-RPC. The cut lands when **all** of these are true:

- [ ] `/remote-control` still works from Codex CLI.
- [ ] Existing thread attach uses `thread/resume`.
- [ ] Session list uses `thread/list`, not `~/.codex/session_index.jsonl`.
- [ ] Sending input uses `turn/start` or `turn/steer` as appropriate.
- [ ] Interrupt uses `turn/interrupt`.
- [ ] Approval/waiting state is surfaced from app-server status/events.
- [ ] No direct writes to Codex SQLite or JSONL indexes.
- [ ] Desktop/sidebar behavior is **tested and documented**, not assumed.

Do not block alpha dogfood on this unless current SDK / `session_index` behavior prevents the test from working. The clean separation: alpha validates the **product experience**; Phase 7 aligns with **OpenAI's real architecture**.

## Build plan (skeleton)

When Parker greenlights Phase 7 (adapter swap):

1. Probe `codex app-server` locally on the dogfood Mac. Confirm `thread/list`, `thread/resume`, `turn/start`, `turn/interrupt` work as documented.
2. Worktree on `wip-codex-remote-control-private`. New branch `cc-mini/phase-7-app-server`.
3. New module `src/app-server-client.ts` ... starts a managed `codex app-server` process (or connects to one), exposes the JSON-RPC primitives.
4. Rewrite `src/codex-manager.ts` to delegate to `app-server-client.ts`. Keep the same exported shape (`start`, `attach`, `runStreamed`, `interrupt`, etc.) so `dispatch.ts` does not change.
5. Delete `src/names.ts`. `listThreads()` and `resolveThread()` callers move to `app-server-client.ts`.
6. Re-run `npm test`. All 20 gate assertions must still pass.
7. Live: walk the acceptance-criteria list above end-to-end, including a desktop-app-created thread URL opened on phone.
8. Cut beta or stable, deploy SKILL.md update lifting "Codex CLI" to "Codex CLI and Codex desktop app."

## Open questions for the pivot itself

1. Does `codex app-server` self-bootstrap, or do we need a managed-child-process supervisor in the daemon?
2. What's the auth path? Does App Server inherit the user's `~/.codex/auth.json`, or does the daemon need to forward credentials?
3. Approval UX (Phase 4): does App Server's approval primitive route to a streamed event the daemon can lift to the phone, or does it require an inline callback the daemon implements?
4. Multi-thread: can App Server handle multiple concurrent thread/resume sessions, or do we need one App Server child per session?
5. Versioning: which App Server protocol version does the daemon target, and how do we declare the SDK dependency?
6. Local-only daemon mode: does App Server require any inbound port, or is it stdio-only? Affects the loopback-only contract.

These are not blockers; they are what gets investigated in step 1 of the build plan.

## Reference

- [OpenAI Codex App Server docs](https://developers.openai.com/codex/app-server/)
- Cody's "Phone as Key, Apple as Authority Layer": `wip-ldm-os-private/ai/product/product-ideas/vision-quest-01/cody-phone-as-key-authority-layer.md`
- Codex Remote Control master plan: `wip-ldm-os-private/ai/product/plans-prds/codex-remote-control/2026-04-28--cc-mini--codex-remote-control-master-plan.md`
- OpenAI Codex issues: #9224, #10547, #13543, #14722, #14751, #16385, #16614

## TL;DR

The CLI build was the right wedge. App Server is the right next layer. Phase 7 is an adapter swap, not a rewrite ... pairing, phone-as-key, E2EE, install flow, and MCP trigger all stay; the daemon's Codex backend swaps from SDK + JSONL to `codex app-server` JSON-RPC. Desktop app and approvals come along for the ride. Not now ... alpha validates the product experience, then Phase 7 aligns with OpenAI's real architecture.
