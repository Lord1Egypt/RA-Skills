# Codex Remote Control ... Master Plan

**Authors:** cc-mini, Cody (security + continuity review merged in)
**Started:** 2026-04-27
**Last touched:** 2026-04-28
**Status:** Relay/UI prototype live; secure dogfood blocked. The transport prototype (Phase 1 daemon + Phase 2c relay endpoints + Phase 2e Kaleidoscope page) is deployed, but the product is **not ready for real dogfood** until the two P0 blockers below are closed: end-to-end encryption (so the WIP relay never sees prompts/events/output) and real session attach (so the URL's thread id is the thread that actually runs). Do not ship the install spec or publish a user-facing alpha that implies privacy or same-session control until those land.

## Vision

Drive your local Codex session from your phone.

You're at your laptop with a Codex CLI session running. You step away. You want to keep going from your phone. Same session, same context, same files, same agent. Codex Remote Control bridges the two: streamed events, prompt input, and a stop button, on the phone.

The product manifests as three pieces:

1. A local daemon on the Mac that wraps the Codex SDK and dials out to wip.computer.
2. A relay API on wip.computer that pairs the daemon with a Sapien-ID-authed phone.
3. A web driver at kaleidoscope.wip.computer that the phone uses to interact with the live session.

## Why this exists

OpenAI shipped Codex CLI; Anthropic ships remote control of Claude Code via claude.ai/code. We want feature parity for Codex, on Kaleidoscope, on terms that match the rest of the WIP stack: passkey auth, Sapien-ID-bound, no third-party hosting beyond wip.computer, **and the relay does not see the user's work**.

Kaleidoscope is the right surface (phone-first AI experience). wip.computer's hosted MCP server already has WebAuthn passkey + Bearer ck-API-key auth, so daemon registration + phone auth bolt on cleanly. No new auth system. The work payload is end-to-end encrypted between phone and daemon; the relay only sees route metadata.

## Positioning

> "Codex should already do this. Until it does, WIP does."

The pitch is parity plus privacy:

- **Parity.** Claude Code has Remote Control: continue a local session from phone, tablet, browser, claude.ai/code, or the Claude mobile app. The session still runs on the user's machine; the web/mobile UI is a remote window into it. Source: [code.claude.com/docs/en/remote-control](https://code.claude.com/docs/en/remote-control). Codex does not currently have a first-party equivalent. That's the opening.
- **Privacy.** Claude's transport is TLS to Anthropic API; not E2EE between phone and local Claude Code. WIP's transport is E2EE end-to-end between phone and local daemon. WIP routes the bytes; WIP does not read them.
- **Local-first.** Same laptop, same files, same local Codex permissions, sandbox, and approval flow. The phone is a UI; the work stays local.

### What we mirror from Claude Code Remote Control

These are proven UX primitives. Copy them.

- `codex-daemon start` / `codex remote-control` ... start a local server that exposes the session to the phone.
- `--remote-control` flag on existing sessions ... opt in without restarting.
- `/remote-control` (or `/rc`) MCP/slash command from inside a Codex session ... triggers the URL/QR handoff.
- URL + QR for phone handoff. Local filesystem, MCP servers, tools, project config preserved.
- Conversation syncs across terminal, browser, phone. Reconnect after network sleep.
- Outbound-only connections. No inbound ports. Short-lived scoped credentials.
- `--spawn` modes (`same-dir`, `worktree`, `session`) ... worktree mode in particular handles multiple parallel remote tasks without file conflicts. Add to roadmap (Phase 5+).

### Where we go further than Claude

- **End-to-end encrypted** between phone and local daemon. WIP relays it; WIP cannot read it.
- **Short-lived single-use relay tickets** for the browser WebSocket. No long-lived API keys in URL query params.
- **Real session attach**, not silent new-session-with-the-same-id. If the SDK can't resume a thread, the UI says so explicitly.
- **LDM OS substrate.** Pairing, identity, presence, and key registration use the same WebAuthn/passkey infra as the rest of the WIP stack.

### Promotion plan

1. **Position as parity + privacy.** "Claude Code has Remote Control. Codex should too. WIP brings it to Codex, local-first and end-to-end encrypted."
2. **Demo dead simple in 20 seconds.** Laptop running Codex. Phone opens Kaleidoscope. Send a prompt from phone. Watch Codex edit/run locally. Hit Stop from phone. That's the whole pitch.
3. **LDM OS showcase.** This is what LDM OS is for: local agent runtime + hosted identity/relay + mobile UI. Bridge + Kaleidoscope + agent control as one coherent system, not a pile of tools.
4. **Hold marketing until the two P0 blockers close.** Real same-session attach/resume (or honest "new remote session" UX), and E2EE through the relay.
5. **The provocative line.** "Codex should already do this. Until it does, WIP does."

Treat this as a flagship Kaleidoscope feature once privacy and continuity ship.

## Reality check (P0 blockers)

The current architecture is not ready for real work yet. It has two product blockers that must be fixed before dogfooding:

### B1. Session continuity is not actually implemented

The product promises "same session, same context, same files." The daemon can only send prompts to in-memory Codex SDK threads it started itself. `session.list` advertises persisted threads from `~/.codex/session_index.jsonl`, but if the phone opens a URL for one of those thread ids and calls `session.start`, the daemon creates a *different* thread and the original is never controlled.

Not acceptable: list a thread, open the phone UI for it, call `session.start`, ignore the temp id, send prompts to the original id, fail with `unknown session`.

Acceptable outcomes:
- Best: daemon resumes the existing Codex thread id and streams from it.
- Acceptable fallback: if the SDK can't resume, the UI clearly says "start a new remote session" and uses the daemon-returned thread id from that point on.

### B2. The relay is not end-to-end encrypted

Traffic is TLS to WIP, but WIP relay code currently sees normal WebSocket JSON frames. WIP can inspect prompts, Codex events, command output, reasoning items, and errors. This violates the product expectation for private local work.

WIP can provide:
- passkey auth, pairing and device ownership, relay routing, daemon presence
- route-level metadata: handle, daemon id, thread id, timestamps, ciphertext byte counts

WIP must not read:
- prompts, Codex streamed events, command text or output, reasoning items, errors, transcript content

Design target: the relay forwards opaque ciphertext envelopes after an initial E2EE handshake. TLS remains necessary, but it is not the privacy boundary.

### B3. Browser WebSocket auth uses long-lived API key in URL (P1)

The current browser path puts the reusable `ck-` key into a WebSocket query parameter. Replace with single-use, short-lived relay tickets.

### B4. Codex's local safety model must stay intact (P0)

Remote control must not bypass local Codex approval, sandbox, writable-root, or repo-guard behavior. The phone gets `session.send` and `session.interrupt`. It must not gain a privilege path local Codex does not have.

For private alpha:
- restrict `workingDirectory` to an allowlisted root or omit
- **remove caller control over `skipGitRepoCheck`** from remote web traffic; force the daemon's safe default
- surface approval-needed and blocked-command states in the phone UI
- document that the remote phone controls the local Codex process under its existing policy

### B5. Relay must enforce ownership server-side (P0)

The current relay routes by client-provided `sessionId` payload + agent_id from the auth token. The agent_id check is server-enforced; the per-thread routing is client-trusted. That's not enough once E2EE is in: the relay needs to validate that the (handle, daemon_id, thread_id) triple in the route URL corresponds to a daemon paired with the authenticated user, and bind the E2EE handshake to that triple.

The browser ticket (P1, B3) must be issued for a specific `(handle, daemon_id, thread_id)` route and not be reusable for any other route, even by the same authenticated user.

## Source-of-truth findings

### Existing Kaleidoscope behavior to reuse

Kaleidoscope is already the app layer for LDM OS:

- `apps/kaleidoscope-private/README.md` says Kaleidoscope owns browser/mobile UI, pairing, approval, device management, conversation views.
- `web/src/app/login/page.tsx` is the Next.js passkey signup/signin surface.
- `web/src/app/pair/page.tsx` is the phone-side pairing approval with passkey verify.
- `web/src/app/kaleidoscope.css` is the product visual system.

Do not build a parallel auth product for Codex Remote Control. Reuse the Kaleidoscope passkey + pair model. Add Codex-specific remote-control state on top.

### Existing LDM OS hosted behavior to reuse

LDM OS owns hosted infrastructure:

- `src/hosted-mcp/server.mjs` stores passkeys + API keys.
- `/webauthn/register-options|verify`, `/webauthn/auth-options|verify` are the account + passkey primitives.
- `/login?next=...` supports the QR/login flow with redirect-back.
- `/api/codex-relay/*` exists today as the first relay skeleton.

Keep LDM OS as relay, presence, auth, routing. Change what it is *allowed to see*.

### Existing daemon behavior to fix

`apps/wip-codex-remote-control-private` has the right local shape: `codex-daemon start|stop|status|link`, local WS, outbound relay client, MCP wrapper, Codex SDK around `startThread()` and `runStreamed()`.

The gap is `session.list` shows persisted threads, but `session.send` only works for in-memory thread handles. No `session.attach`/resume.

## Architecture (target, with E2EE)

```
[Kaleidoscope phone UI]                           [Mac codex-daemon]
       |                                                  |
       | wss://wip.computer                              | wss://wip.computer
       | relay ticket, route metadata only                | daemon API key
       |                                                  |
       | ciphertext frames                                | ciphertext frames
       v                                                  v
                       [WIP relay / LDM OS]
                       - authenticates both sides
                       - routes by user + daemon + thread/session id
                       - tracks presence
                       - never decrypts Codex payloads
```

The relay remains operationally central. It is not trusted with content.

## Repos involved

| Piece | Repo (private) | Public twin |
|-------|----------------|-------------|
| Local daemon (TS + ws + @openai/codex-sdk) | wipcomputer/wip-codex-remote-control-private | wipcomputer/wip-codex-remote-control |
| Codex MCP wrapper (stdio) | (same repo) | (same) |
| Hosted relay API | wipcomputer/wip-ldm-os-private | wipcomputer/wip-ldm-os |
| Phone driver (Next.js, kaleidoscope.wip.computer) | wipcomputer/kaleidoscope-private | n/a |

### Build order: web first, native later

We're building the Kaleidoscope **web** client first. Native iOS/macOS apps come later. The web client is the **reference client** for the future native app, not a throwaway prototype.

That means the web client defines the contract. Native must reuse:

- passkey/auth identity model
- relay ticket endpoint (`POST /api/codex-relay/ws-ticket`)
- daemon bootstrap endpoint (`GET /api/codex-relay/bootstrap/:threadId`)
- E2EE handshake + frame format
- `session.attach` / `session.send` / `session.interrupt` protocol
- presence + reconnect state machine
- event rendering semantics (agent_message, command_execution, reasoning, turn.completed, turn.failed)

Native gets to add what's only possible there: push notifications, background reconnect, biometric affordances, deeper mobile polish. **The protocol must not change when we go from web to app.**

This sharpens the pitch: web proves the control plane; the Kaleidoscope app makes it feel native.

## WebSocket surface

After E2EE handshake, every Codex control payload below is ciphertext inside an `e2ee.frame`. The relay never sees the JSON.

### Existing protocol (kept)

- `session.start { name?, workingDirectory? }` ... opens a new Codex SDK thread. Returns `{ sessionId }` immediately (a temp UUID); `thread_id` arrives in `thread.started` and the daemon re-keys.
- `session.send { sessionId | name, prompt }` ... forwards via `runStreamed`.
- `session.events` (server-pushed) ... pass-through SDK events (`thread.started`, `item.completed`, `turn.completed`, `turn.failed`).
- `session.interrupt { sessionId }` ... `AbortController.abort()`.
- `session.close { sessionId }` ... drops the in-memory thread handle.
- `session.list` ... reads `~/.codex/session_index.jsonl`.

### New protocol (added in Phase 3)

- `session.attach { id?, threadId, workingDirectory? }`
- `session.attached { id?, sessionId, threadId, resumed: boolean }`
- `session.attach.failed { id?, threadId, reason: "unknown_thread" | "resume_unavailable" | "auth_required" | "codex_error", message? }`

Once E2EE is required for a paired daemon, the relay rejects plaintext `session.*` messages.

## E2EE design

Use audited browser + Node primitives. No custom cipher.

MVP path:
- ECDH P-256, HKDF-SHA-256, AES-GCM (Web Crypto + Node `crypto.subtle`).
- Daemon remote-control identity key at `~/.codex-daemon/e2ee-key.json` on first pair.
- Only the daemon public key + metadata stored on WIP.
- Browser ephemeral keypair per phone session.
- Per-session keys = ECDH(daemon priv, browser ephemeral pub) || HKDF || AES-GCM keys.
- Monotonic send/receive counters in authenticated data → replay + ordering protection.

Envelope:

```json
{
  "type": "e2ee.frame",
  "version": 1,
  "session": "route-session-id",
  "sender": "web|daemon",
  "seq": 42,
  "nonce": "base64url",
  "ciphertext": "base64url"
}
```

Plaintext inside ciphertext is the existing protocol:

```json
{ "type": "session.send", "id": "send-1", "sessionId": "...", "prompt": "..." }
```

### Pairing + key registration

Extend the existing pair flow, do not replace it:

1. `codex-daemon link` creates or loads the daemon E2EE keypair.
2. `POST /api/codex-relay/pair-init` includes daemon public key + hostname + platform + crypto capabilities.
3. WIP returns the existing 6-char code and `/pair` URL.
4. Kaleidoscope pair UI authenticates with passkey using the existing WebAuthn flow.
5. Pair completion stores the daemon public key + daemon_id against the authenticated handle. The (handle, daemon_id, daemon_pubkey) tuple is the unit of trust.
6. Daemon receives only relay credentials and non-secret confirmation from `pair-status`.

### Key revocation + rotation

- **Unpair daemon.** User can revoke a paired daemon from the Kaleidoscope device-management surface. Revocation invalidates the daemon's relay credentials, drops any active relay socket, and removes the stored daemon public key. Subsequent connect attempts fail with `pair_revoked`.
- **Rotate daemon key.** `codex-daemon rotate-key` (or equivalent) generates a new keypair, re-runs `pair-init` to register the new pubkey against the same handle, and prompts the user to re-confirm via passkey. Old key is removed.
- **Expire browser tickets.** Single-use, short TTL (suggest 60s), bound to the (handle, daemon_id, thread_id) route. Used tickets are evicted; expired tickets fail with `ticket_invalid`.
- **Invalidate stale relay sessions.** Server tracks per-route sessions; on revocation or rotation, server actively closes any relay socket bound to the old credential and marks the session id used.
- **Audit log.** Pair, unpair, rotate, ticket-issue, attach-success, attach-fail events recorded against the user's handle for the device-management UI to surface.

### Session handshake

1. Browser opens `/{handle}/codex-remote-control/{threadId}` through `/login?next=...`.
2. Browser calls `GET /api/codex-relay/state` (or new `GET /api/codex-relay/bootstrap/:threadId`) for daemon presence + daemon public key + crypto version.
3. Browser creates an ephemeral keypair.
4. Browser connects with a one-use relay ticket (no `ck-` in URL).
5. Browser sends `e2ee.hello` with its ephemeral public key.
6. Daemon derives the shared key, sends `e2ee.ready`.
7. All Codex control traffic after that is encrypted.

## Session continuity design

### Daemon

```ts
ensureSession({ threadId, workingDirectory? }): Promise<{ sessionId, attached: boolean }>
```

Behavior:
1. If thread id is already in the in-memory map, return it.
2. If Codex SDK exposes `resumeThread(id)` or equivalent, resume and store.
3. If resume unavailable, return structured error: `resume_unavailable`.
4. **Never silently call `startThread()` for a URL thread id unless the UI explicitly asks for a new remote session.**

### Phone UI

On remote-control page load:
1. Parse `{handle}` and `{threadId}` from the route.
2. Authenticate via Kaleidoscope passkey login if no session.
3. Establish E2EE.
4. Send encrypted `session.attach { threadId }`.
5. Enable prompt input only after **all four gates pass**: signed in, daemon online, E2EE ready, and `session.attached` succeeded. If any gate fails or regresses, the composer disables and surfaces the specific gate that failed.
6. On `resume_unavailable`, show clear "Start new remote session" action. If accepted, send `session.start`; replace route/state with the daemon-returned thread id when `thread.started` arrives.

## Build phases

### Phase 1: Local daemon (DONE)

ws server on `127.0.0.1:7777`, Bearer-token auth. Shared secret in `~/.codex-daemon/token` (chmod 600). CLI: `codex-daemon start|stop|status`. `codex-daemon-mcp` MCP wrapper with `remote_control` + `list_sessions`. Reference test client smoke-tested end-to-end with a real Codex turn (85K tokens in / 395 out).

### Phase 2: Phone surface skeleton (DONE on server + UI; MISLEADING UNTIL Phase 0/3 LAND)

- 2a: MCP wrapper with `remote_control` ... done.
- 2b: Outbound relay client + `codex-daemon link` pairing ... done.
- 2c: Hosted relay API in `wip-ldm-os-private/src/hosted-mcp/server.mjs` ... done; **deployed** to wip.computer.
- 2d: Naming write-back ... skipped (Codex SDK has no rename API; URL uses `thread_id`).
- 2e: Phone driver at `kaleidoscope-private/web/src/app/codex-remote-control/[threadId]/page.tsx` ... done; **auto-deployed** to kaleidoscope.wip.computer.

**Caveat:** Phase 2 ships the wire shape without Phase 3's `session.attach` and without Phase 2.5's E2EE. Phone UI must be flagged as "not E2EE, not real attach" until those land.

### Phase 0 (NEW): Stop misleading product surfaces

Owner: `apps/wip-codex-remote-control-private`.

- README + MCP `remote_control` output state explicitly: current alpha is **not E2EE** and does **not yet attach to arbitrary existing Codex sessions**. The phone surface starts a fresh daemon-owned thread.
- Mark phone dogfooding as blocked until Phase 2.5 + Phase 3 pass.
- Remove or hide "same session" copy until `session.attach` works.

Done when:
- Docs match current behavior.
- No install prompt implies WIP cannot read relay payloads.
- No page implies an existing Codex thread is controllable until attach succeeds.

### Phase 1.5 (NEW): Align with Kaleidoscope auth + pairing

Owners: `wip-ldm-os-private`, `apps/kaleidoscope-private`.

- Kaleidoscope's Next.js login + pair flows are the canonical product UI.
- LDM OS hosted MCP is API + relay backend.
- Reuse passkey endpoints. No Codex-specific passkey registration.
- Reuse `/login?next=...` pattern for remote-control URLs.
- Add Codex-specific pair variant only for daemon public-key registration + relay capabilities.

Done when:
- `/login?next=/{handle}/codex-remote-control/{threadId}` works with existing passkey flow.
- Pairing a daemon uses the same UX as Kaleidoscope pairing.
- LDM OS owns API state; Kaleidoscope owns UI.

### Phase 2.5 (NEW): Relay tickets + E2EE

Owners: all three repos.

Daemon:
- Generate + persist daemon E2EE keypair, file mode 0600.
- Send daemon public key + crypto capabilities during `pair-init`.
- Implement E2EE handshake on relay connection.
- Decrypt incoming frames before dispatch; encrypt outgoing `session.event`/`ack`/error.

LDM OS relay:
- Store daemon public key + protocol version per paired handle.
- Add `POST /api/codex-relay/ws-ticket`.
- Replace browser `?token=ck-...` with single-use `?ticket=...`.
- Route `e2ee.hello`/`e2ee.ready`/`e2ee.frame` opaquely.
- Reject plaintext `session.*` for E2EE-capable daemon pairs.
- Never log ciphertext bodies, token values, or decrypted content.

Kaleidoscope:
- Fetch relay bootstrap metadata.
- Generate browser ephemeral keypair.
- Establish E2EE before enabling the composer.
- Send encrypted protocol payloads.
- Internal diagnostics show: `encrypted: yes`, `relay: wip.computer`, `daemon: online/offline`.

Done when:
- Relay unit test proves no plaintext prompts pass through relay handlers.
- Browser-to-daemon integration test proves daemon decrypts a prompt and browser decrypts an event.
- Logs contain route metadata only.

### Phase 3: Real session attach/resume

Owner: `apps/wip-codex-remote-control-private`.

- Investigate current `@openai/codex-sdk` thread-resume support.
- Add `CodexManager.ensureSession`.
- Add `session.attach` protocol handling.
- `session.send` refuses unknown ids with attach-required error.
- Remove caller control over `skipGitRepoCheck` from remote web traffic.
- Allowlist or default-root policy for `workingDirectory`.

Kaleidoscope:
- Send encrypted `session.attach` on page load.
- Disable composer until attached.
- On `resume_unavailable`, show "Start new remote session"; on accept, send `session.start` and update route to real thread id when `thread.started` arrives.

Done when:
- Opening a URL for an existing Codex thread + first prompt uses that same thread.
- If attach unimplementable in SDK, UX makes it explicit; no silent `unknown session` failures.

### Phase 4 (NEW): Remote safety + approval UX

Owners: daemon + Kaleidoscope.

- Forward local Codex approval-needed states to phone if SDK exposes them.
- If approvals can't complete from phone, show "action needed on Mac" with context.
- Interrupt always available during a running turn.
- Local audit events for remote prompts, interrupts, attach attempts, approval handoffs.
- Remote sessions visibly tagged in daemon logs + Codex session metadata where possible.

Done when:
- Blocked command or approval prompt does not hang silently on phone.
- User can distinguish remote-controlled turns from local turns in local diagnostics.

### Phase 5 (NEW): Multi-device hardening

Owners: LDM OS relay + Kaleidoscope.

- Multiple paired daemons per user.
- Daemon labels in phone UI.
- Multiple web viewers can receive events; only one active controller can submit prompts.
- Reconnect redoes E2EE session handshake.
- Stale-daemon and offline states surfaced.

Done when:
- Two phones can watch the same remote session, only the active controller submits.
- Wi-Fi blip recovers without exposing plaintext fallback.

### Phase 6 (was Phase 3): Install path

Goal: paste-the-prompt-into-Codex installs and runs end-to-end.

**Hard gate:** do not author or deploy the install spec, and do not publish a user-facing alpha that implies privacy or same-session control, until Phases 2.5 + 3 have landed and all four test gates above pass. Otherwise we ship product copy that contradicts current behavior.

- Install spec at `wip.computer/install/wip-codex-remote-control.txt` ... NOT YET AUTHORED.
- Repo enrolled in `wipcomputerinc/repos-manifest.json` ... NOT YET DONE.
- Daemon published to npm @alpha ... pre-requisite landed today (see "Pre-req fix").

#### Pre-req fix landed today (2026-04-28)

`wip-release alpha` had a first-publish bug: `npm view <pkg> dist-tags` errors with E404 when a package has never been published, and the dist-tag safety check treated that as a hard failure. Every brand-new wip-* package would refuse to publish on the first run.

- wipcomputer/wip-ai-devops-toolbox-private PR #390: fix in `tools/wip-release/core.mjs`.
- Toolbox v1.9.73-alpha.4 published.
- `@wipcomputer/wip-release@1.9.78` (with the fix) installed locally via `ldm install --alpha`.

So `wip-release alpha` on `wip-codex-remote-control-private` should now succeed on first-publish.

Sequencing note: Phase 6 (publish + install) ships the *current* wire shape. Per Phase 0 above, that ship must clearly say "not E2EE, not real attach" until 2.5 + 3 land. Otherwise we publish a misleading product surface to npm.

## End-to-end UX (target, post Phase 0/2.5/3)

```
1. User opens Codex CLI, pastes:
     Read https://wip.computer/install/wip-codex-remote-control.txt

2. Codex (the AI) reads the spec. Checks "is wip-codex-remote-control installed?"
     If yes: show version. Optionally `ldm install --alpha --dry-run`.
     If no: walk through what it does, show dry-run, install on confirm.

3. After install:
     - codex-daemon link  -> creates/loads E2EE keypair, prints 6-char code +
       https://wip.computer/pair, sends daemon pubkey on pair-init.
     - User opens URL on phone -> passkey signin -> types code; pair-complete
       binds the daemon pubkey to the user's handle.
     - codex-daemon start -> daemon binds 127.0.0.1:7777 + dials wip.computer
       relay over E2EE-capable channel.
     - codex mcp add wip-codex-remote-control --command 'npx codex-daemon-mcp'

4. Inside Codex CLI session, agent calls `remote_control` tool:
     -> Returns https://kaleidoscope.wip.computer/codex-remote-control/<thread-id>
     - User opens URL on phone (already signed in via passkey).
     - Phone fetches relay ticket, generates ephemeral keypair, establishes E2EE
       with the daemon, then sends encrypted `session.attach { threadId }`.
     - On `session.attached`, the phone enables the composer. On
       `resume_unavailable`, the phone offers "Start new remote session."

5. Phone drives the Codex turn:
     - Encrypted prompt -> relay (opaque) -> daemon -> Codex SDK.
     - Codex events -> daemon -> encrypted -> relay (opaque) -> phone (renders live).
     - Stop button -> encrypted session.interrupt -> AbortController on daemon.
     - Approval-needed states surface to phone with "action needed on Mac" if
       the SDK can't satisfy them remotely.
```

## Test plan

### Unit tests
- E2EE frame encrypt/decrypt round trip.
- Wrong key fails decrypt.
- Replayed sequence fails.
- Relay ticket is single-use + expires.
- Relay rejects plaintext `session.send` after E2EE required.
- `ensureSession` returns existing in-memory session.
- `ensureSession` resumes persisted thread when supported.
- `ensureSession` returns `resume_unavailable` instead of starting an unrelated thread.

### Integration tests
- Pair daemon through Kaleidoscope passkey flow.
- Browser opens `/login?next=/{handle}/codex-remote-control/{threadId}` and returns to the route after sign-in.
- Browser gets a relay ticket without putting `ck-` in the WS URL.
- Browser + daemon complete E2EE handshake through WIP relay.
- Browser sends encrypted prompt; daemon decrypts + runs Codex; browser decrypts streamed event.
- Existing thread attach works or returns clear fallback.
- Interrupt aborts a running turn.

### Manual alpha checks
- Phone on cellular, Mac on Wi-Fi.
- Confirm relay logs never show prompt text.
- Confirm remote prompt follows local Codex sandbox + approval behavior.
- Confirm UI never accepts prompt input before attach + encryption ready.

### Test gates required before any user dogfood

These four gates must all pass on a build before that build is offered to a user via the install spec:

1. **Privacy gate.** Relay logs never contain prompt text or decrypted Codex events. Verify on a freshly captured log of a real turn.
2. **Plaintext rejection gate.** Plaintext `session.send` (or any `session.*` other than `e2ee.hello`) is rejected by the relay for E2EE-capable daemon pairs. Connection closes with a clear reason.
3. **Attach gate.** Opening a URL for an existing Codex thread either (a) attaches successfully and the first prompt runs against that thread, or (b) shows the "start new remote session" fallback and never silently runs against a different thread.
4. **Interrupt gate.** Stop button aborts a running turn end-to-end (encrypted session.interrupt → daemon AbortController → SDK turn cancels → phone shows turn.failed or turn.completed cleanly).

If any gate fails, the build is not eligible for the install spec / npm @alpha tag.

### Test results (2026-04-28, code-level audit)

Status legend: **PASS** ... code path enforces the gate. **NEEDS-LIVE** ... code path is correct, but the gate also requires a live integration smoke test (paired daemon + browser + real Codex turn) before the install spec ships.

1. **Privacy gate: PASS / NEEDS-LIVE.**
   - Relay (`wip-ldm-os-private/src/hosted-mcp/server.mjs:2419..2475`): codex-relay WS handler logs only metadata (`agentId`, key prefix, online/offline, ws error names). Frame bodies are forwarded as opaque strings; never inspected, never logged.
   - Daemon (`wip-codex-remote-control-private/src/dispatch.ts`, `codex-manager.ts`): no `console.*` calls in the data path. `relay-client.ts` logs only connection-level metadata (URL, close code, e2ee session id prefix), never frame contents.
   - Live step that remains: capture a relay log of one real encrypted turn and grep for prompt text. Expected: nothing.

2. **Plaintext rejection gate: PASS** (closed by PR #11 in wip-codex-remote-control-private).
   - When the daemon has an E2EE identity loaded (`this.identity`), the relay-client onmessage handler now rejects any non-`e2ee.hello` / non-`e2ee.frame` envelope with a `{type:"error", message:"plaintext rejected..."}` frame and `ws.close(4002, ...)`.
   - Pre-E2EE legacy daemons (no identity loaded) still accept plaintext for back-compat; such daemons should be upgraded.
   - The local Mac WS server (`server.ts`) is unchanged; loopback + bearer token, never crosses a relay.
   - Live step that remains: connect a WS to a paired E2EE daemon, send `{"type":"session.send",...}`, expect one error frame + close 4002.

3. **Attach gate: PASS** at code level.
   - Daemon (`codex-manager.ts`): `attach(threadId)` looks up the threadId in `~/.codex/session_index.jsonl`. If absent, throws `SessionAttachError("unknown_thread")`. If found, calls `codex.resumeThread()`. SDK errors classify as `resume_unavailable` (heuristic: `/resume/` + `/not (?:a function|defined|available)/`) or `codex_error`. Never silently calls `startThread()` for the URL thread id (that was B1).
   - Daemon (`dispatch.ts`): `session.attach` -> `session.attached` (with `resumed: true|false`) or `session.attach.failed { reason }`.
   - Web (`kaleidoscope-private/web/src/app/codex-remote-control/[threadId]/page.tsx`, PR #12): on `e2ee.ready`, sends `session.attach { threadId }` (was `session.start`). Composer is four-gated on `signed-in + daemon-online + e2ee-ready + attached`. On `session.attach.failed { unknown_thread | resume_unavailable }`, renders a yellow banner with a "Start new remote session" button that sends `session.start` and re-attaches when `session.started` arrives.
   - Live step that remains: open `/codex-remote-control/<known-threadId>`, verify "attached to thread ..." + composer enables; open `/codex-remote-control/<bogus-threadId>`, verify yellow banner + button + new-session path.

4. **Interrupt gate: PASS** at code level.
   - Daemon (`codex-manager.ts:runStreamed`): allocates an `AbortController`, passes `signal` to `thread.runStreamed(prompt, { signal })`, clears it in the `finally`. `interrupt(sessionId)` calls `record.abortController.abort()`.
   - Daemon (`dispatch.ts:session.interrupt`): resolves the session, calls `manager.interrupt(sid)`, returns `ack` or `error{"no active turn"}`.
   - Web (`page.tsx`): Stop button calls `interrupt()`, gated on `encrypted && attached`, sends `session.interrupt` over the encrypted channel.
   - Live step that remains: kick off a long turn, hit Stop, expect daemon AbortController fires and phone shows `turn.failed`/`turn.completed` cleanly.

**Net status:** Gates 1-4 close at the code level. The build is eligible for the install spec and `npm @alpha` tag once one live integration pass confirms each gate end-to-end on a paired daemon + phone session.

## Merged PRs

### wipcomputer/wip-codex-remote-control-private (formerly wip-codex-daemon-private)

- #1 Phase 1 daemon scaffold + plan + package metadata
- #2 Phase 2 plan
- #3 Phase 2a: MCP wrapper
- #4 Phase 2b: outbound relay client + `codex-daemon link`
- #5 release-prep: license-guard scaffold + standard MIT+AGPL README block
- #6 docs: WIP standard README format + TECHNICAL.md split
- #7 rename: package + MCP server name to wip-codex-remote-control

Tags: `v0.0.2-alpha.1` (tagged + GitHub release with notes; not yet on npm). The interrupted second `wip-release alpha` left `package.json` bumped to `0.0.2-alpha.2` (uncommitted). Once we re-run `wip-release alpha` after picking up the toolbox fix, that becomes the published version.

### wipcomputer/wip-ldm-os-private

- #694 codex-relay API endpoints + WSS upgrade in `src/hosted-mcp/server.mjs`. Deployed to wip.computer.
- #695 (superseded by #696)
- #696 simplified login.html + `/api/qr` endpoint. (Superseded by Kaleidoscope login; `app/*` HTML in this repo is now stale ... see "Cleanup".)
- #698 (this plan, v1)
- #699 cody secure-session-continuity-plan

### wipcomputer/kaleidoscope-private

- #9 codex-remote-control session driver + `?next=` redirect on `/login`. Auto-deployed to kaleidoscope.wip.computer.

### wipcomputer/wip-ai-devops-toolbox-private

- #390 fix(wip-release): handle first-publish E404. Published as toolbox v1.9.73-alpha.4 / wip-release v1.9.78.

## Live infrastructure

- `wip.computer/api/codex-relay/pair-init` ... daemon initiates pairing. Verified live.
- `wip.computer/api/codex-relay/pair-status/:id` ... daemon polls. Verified live.
- `wip.computer/api/codex-relay/pair-complete` ... web side, passkey-authed. Verified live.
- `wss://wip.computer/api/codex-relay/daemon` ... daemon presence + message pump. Verified 401 without auth.
- `wss://wip.computer/api/codex-relay/web/:threadId` ... phone side, ck-token via `?token=` (to be replaced by ticket in Phase 2.5).
- `wip.computer/api/qr?url=<encoded>` ... generic QR PNG. Verified live.
- `kaleidoscope.wip.computer/codex-remote-control/[threadId]` ... session driver. Live.
- `kaleidoscope.wip.computer/login?next=...` ... passkey signin with redirect. Live.

## Decisions

- **Phone is the canonical surface.** Desktop is fallback only.
- **Single front door at /login** ... Apple/Google `?next=` pattern.
- **The relay never reads payload content.** It routes opaque ciphertext after E2EE handshake. (Supersedes the earlier "transparent passthrough" decision; the relay is still topologically a passthrough but content is opaque.)
- **Relay enforces ownership server-side.** The (handle, daemon_id, thread_id) triple in the route URL must correspond to a daemon paired with the authenticated user. Don't trust client-provided `sessionId` payload routing alone.
- **Codex `thread_id` (UUID) is the canonical identifier in URLs.** `thread_name` is cosmetic display.
- **`session.attach` is the entry verb for an existing thread**, not `session.start`. `session.start` is reserved for the explicit "new remote session" action.
- **Browser WS auth uses single-use relay tickets**, not the `ck-` API key in the URL.
- **npm @alpha is the canonical publish target for alphas** per `library/documentation/how-releases-work.md`.
- **Cross-platform passkey on the phone uses the OS's native WebAuthn.** No custom QR-on-phone flow.
- **Local Codex safety model is the floor.** Remote control inherits it; never bypasses it.

## Open questions

- Does the current `@openai/codex-sdk` expose a supported thread resume API? If yes, use it. If no, decide whether to wait for SDK support or ship "new remote session" as an explicit alpha limitation.
- E2EE key scoping: per paired daemon, per browser device, or both? Recommended: daemon identity key + browser ephemeral keys per session.
- Does the remote-control UI live fully in Kaleidoscope Next.js now, or can the LDM OS static app stay temporarily? Recommended: move UI to Kaleidoscope; keep LDM OS as backend.
- What metadata is acceptable for WIP to retain? Recommended: handle, daemon id, route id, connection times, byte counts, error categories. Not prompts, outputs, or decrypted events.

## Open work + cleanup

1. **Phase 0 docs pass** ... README + MCP `remote_control` output add explicit "not E2EE, not real attach" disclaimers until Phase 2.5 + 3 land.
2. **Author + deploy `wip.computer/install/wip-codex-remote-control.txt`** modeled on `wip-markdown-viewer.txt`. Same disclaimers as Phase 0.
3. **Enroll `wip-codex-remote-control-private` in `wipcomputerinc/repos-manifest.json`** with release block.
4. **Re-run `wip-release alpha`** ... should succeed now that the first-publish fix is installed.
5. **Cleanup stale `wip-ldm-os-private/src/hosted-mcp/app/`** HTML pages (the early mistake before redirected to Kaleidoscope).
6. **Revert `/login` route override in `server.mjs`** to fall back to legacy `demo/login.html`, or remove once Kaleidoscope is canonical.
7. **Bin name alignment (optional).** Package is `wip-codex-remote-control` but bins are `codex-daemon` + `codex-daemon-mcp`. Aligning to `codex-remote-control` + `codex-remote-control-mcp` is cleaner.
8. **`~/.codex-daemon/` data dir.** Old name. Migrate to `~/.codex-remote-control/` for consistency, or leave (no users yet).
9. **Local clone leftover** at `~/wipcomputerinc/.worktrees/wipcomputerinc--cc-mini--codex-daemon-init/repos/ldm-os/apps/wip-codex-daemon-private/`. Canonical clone is at `~/wipcomputerinc/repos/ldm-os/apps/wip-codex-remote-control-private/`. Temp can be removed.
10. **Phase 2.5 work** ... E2EE handshake + relay tickets across all three repos. Largest unbuilt piece.
11. **Phase 3 work** ... `session.attach` + `ensureSession` + `workingDirectory` allowlist + drop `skipGitRepoCheck` from remote callers.
12. **Phase 4 work** ... approval-needed handoff UX.
13. **Phase 5 work** ... multi-daemon, multi-viewer, reconnect-with-rehandshake.

## Naming history

- 2026-04-27: Repo created as `wip-codex-daemon-private`.
- 2026-04-28: User correction: "daemon" is implementation; this is "Codex Remote Control."
- GitHub repo renamed to `wip-codex-remote-control-private` (redirects from old URL).
- Public repo `wipcomputer/wip-codex-remote-control` created (empty placeholder; populated via `deploy-public` on first stable).
- Local directory renamed to `wip-codex-remote-control-private/` (Parker did the `mv`; guard refused agent).
- Package + MCP server name renamed to `wip-codex-remote-control` (PR #7).

## Recommendation (from Cody's review, adopted)

Proceed with this architecture, but change the trust boundary:

- WIP Computer remains the relay + identity provider.
- Kaleidoscope remains the phone UI + passkey product layer.
- LDM OS remains the hosted API + local daemon substrate.
- Codex work payloads are end-to-end encrypted between phone and daemon.
- Existing Codex sessions are advertised as controllable only once the daemon can actually attach or resume them.

This keeps the product aligned with LDM OS: local-first, user-owned, private, and reachable from anywhere without giving the hosted relay the user's work.

## Coordinates for future-me

If you're picking up this thread cold:

- Daemon code: `~/wipcomputerinc/repos/ldm-os/apps/wip-codex-remote-control-private/`.
- Server-side relay: `wip-ldm-os-private/src/hosted-mcp/server.mjs` (search `codex-relay`).
- Phone UI: `kaleidoscope-private/web/src/app/codex-remote-control/[threadId]/page.tsx`.
- Phase 1 detailed plan: `wip-codex-remote-control-private/ai/product/plans-prds/current/2026-04-27--cc-mini--codex-daemon-phase1.md`.
- Phase 2 detailed plan: `wip-codex-remote-control-private/ai/product/plans-prds/current/2026-04-27--cc-mini--codex-daemon-phase2.md`.
- Cody's full continuity + E2EE plan (companion doc): `ai/product/plans-prds/codex-remote-control/2026-04-28--cody--secure-session-continuity-plan.md`.
- Architecture spec (parent context): `wip-ldm-os-private/ai/product/product-ideas/vision-quest-01/architecture-spec.md`.

To resume:

1. **Phase 0 first.** Update README + MCP output to say "not E2EE, not real attach" until 2.5 + 3 land. Otherwise the install spec ships misleading product copy.
2. `cd ~/wipcomputerinc/repos/ldm-os/apps/wip-codex-remote-control-private`. Check `git status` ... expect dirty tree from interrupted bump (package.json at 0.0.2-alpha.2). Restore via `git restore` (needs guard allowance) or roll forward.
3. Run `wip-release alpha`. First-publish fix is installed; should bump + publish to npm @alpha cleanly.
4. Author install spec at `wip-websites-private/wip.computer/install/wip-codex-remote-control.txt` (model on `wip-markdown-viewer.txt`, with Phase 0 disclaimers).
5. Deploy `wip-websites-private` (`bash deploy.sh` from primary tree).
6. Enroll the repo in `repos/repos-manifest.json` (PR in wipcomputerinc).
7. Test top-to-bottom by pasting the install prompt into a fresh Codex CLI session.
8. Cleanup pass: stale `wip-ldm-os-private/src/hosted-mcp/app/` + `/login` route override.
9. **Then start Phase 2.5 (E2EE + ticket).** The largest unbuilt piece. Start by spec'ing keys, envelopes, and the bootstrap endpoint.
10. **Then Phase 3 (`session.attach`).** Investigate Codex SDK resume API first.
