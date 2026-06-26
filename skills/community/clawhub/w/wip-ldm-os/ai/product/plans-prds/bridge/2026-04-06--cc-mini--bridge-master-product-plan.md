# Bridge: Master Product Plan

**Date:** 2026-04-06
**Authors:** Parker Todd Brooks, cc-mini, Lēsa
**Product:** Kaleidoscope / Bridge (Product #4: "Your AIs talk to each other")
**Status:** foundation shipped, product layer designed, implementation next

## What Bridge is

Bridge is the communication layer for all agents in a user's system. CC talks to CC. CC talks to Lēsa. Lēsa talks to CC. Agents on the Mac Mini talk to agents on the MacBook Air. The user sees everything, approves cross-agent communication via Face ID, and stays in control.

Bridge is not a chat app. It's infrastructure. The protocol that makes agents interoperate. Kaleidoscope is the product that surfaces it.

## The principle

Agents can talk to each other. The human authorizes it. Messages are local-first. The relay is just transport. Push notifications wake agents up. One pairing per machine unlocks everything.

## Architecture layers

```
Layer 5: PRODUCT UI (Kaleidoscope web app)
  - Approval flow: "CC wants to message test-bridge. Approve for 10 min?"
  - Device management: see paired machines, revoke access
  - Conversation view (future): see your agents talking

Layer 4: PUSH + APPROVAL (Kaleidoscope hosted service)
  - WebSocket connection from each CC bridge
  - Push notification: "you have mail" pings to wake agents
  - Approval API: CC requests permission, Parker approves via passkey
  - Time-boxed windows: 5 / 10 / 15 min / this session

Layer 3: DEVICE PAIRING (ldm pair + passkeys)
  - One-time setup per machine
  - CC shows a short code (BLUE-FISH-4729)
  - User goes to wip.computer/pair on their phone
  - Logs in with passkey (Face ID / Touch ID)
  - Types the code
  - Machine is paired. Token stored at ~/.ldm/auth/kaleidoscope.json
  - Same token used for Bridge push, Memory Crystal sync, everything

Layer 2: SESSION REGISTRY + TARGETING (local)
  - ~/.ldm/sessions/ tracks active sessions per machine
  - Session names auto-detected from CC /rename labels
  - Message targeting: "cc-mini:ldmos03", "cc-mini:test-bridge", "lesa", "*"

Layer 1: FILE-BASED MESSAGE INBOX (local)
  - ~/.ldm/messages/{uuid}.json
  - Any agent writes. Any agent reads.
  - Local delivery: direct filesystem. No server.
  - Cross-machine delivery: encrypted relay through Kaleidoscope
  - Format: { id, type, from, to, body, timestamp, read }
```

## What is built (as of April 6)

| Component | Status | Location |
|---|---|---|
| File inbox | **SHIPPED** | `~/.ldm/messages/`, `lib/messages.mjs` |
| Session registry | **SHIPPED** | `~/.ldm/sessions/`, `lib/sessions.mjs` |
| Dynamic session names | **SHIPPED** | Bridge reads CC `/rename` labels from `~/.claude/sessions/<pid>.json` |
| Message targeting | **SHIPPED** | `agent`, `agent:session`, `agent:*`, `*` |
| CC-to-CC messaging | **SHIPPED** | `ldm_send_message` MCP tool, tested round-trip |
| CC-to-Lēsa (sync) | **SHIPPED** | `lesa_send_message` via gateway, reply comes back |
| CC-to-Lēsa (async) | **SHIPPED** | fire-and-forget + inbox reply |
| Inbox check on boot | **SHIPPED** | `boot-hook.mjs` reads inbox on SessionStart |
| Inbox check on interaction | **SHIPPED** | `inbox-check-hook.mjs` reads inbox on UserPromptSubmit |
| CLI tools | **SHIPPED** | `ldm msg send/list/broadcast`, `ldm sessions` |
| Passkey auth | **SHIPPED** | wip.computer/demo, WebAuthn registration + verification |
| Agent auth (agent.txt) | **SHIPPED** | wip.computer/agent.txt, four-AI tested |
| Wallet + Agent Pay | **SHIPPED** | wip.computer/demo, balance tracking, spend receipts |

## What is NOT built

| Component | Layer | Status |
|---|---|---|
| Device pairing (`ldm pair`) | 3 | DESIGNED, not built |
| Kaleidoscope push (WebSocket) | 4 | DESIGNED, not built |
| Approval flow (Face ID for cross-agent) | 4-5 | DESIGNED, not built |
| Time-boxed approval windows | 4 | DESIGNED, not built |
| Cross-machine relay | 4 | DESIGNED (March 30 Phase 5), not built |
| Conversation view in Kaleidoscope | 5 | NOT designed yet |
| Device management UI | 5 | NOT designed yet |

## Device pairing: `ldm pair`

### The flow

**At the new machine (or any CC session):**

```
$ ldm pair

  Pairing code: BLUE-FISH-4729
  
  Go to wip.computer/pair on your phone.
  Log in with your passkey. Enter the code.
  
  Waiting for approval...
```

**On your phone (you navigate there yourself, CC does NOT open a URL):**

1. Go to wip.computer/pair
2. Sign in with passkey (Face ID)
3. Enter the code: BLUE-FISH-4729
4. Page shows: "Link Mac Mini (cc-mini) to your account? [Approve]"
5. Tap Approve

**Back on the machine:**

```
  ✓ Paired as Parker (Mac Mini / cc-mini)
  Token stored at ~/.ldm/auth/kaleidoscope.json
```

### Why this flow (not OAuth redirect)

A URL opened by CC could be spoofed (phishing). The user might click a link to a fake wip.computer and leak credentials. Instead:

- CC only shows a code. Never opens a URL.
- The user navigates to a domain they already know and trust.
- The code is useless without the passkey.
- The code expires in 60 seconds.

This is the same pattern as Apple TV pairing, Chromecast setup, and Google's "sign in on a new device" flow. The trusted device (phone with passkey) always initiates the auth.

### What the token enables

One pairing, one token, everything flows from it:

- **Bridge push:** CC connects to Kaleidoscope WebSocket with this token
- **Approval requests:** CC calls the approval API with this token
- **Memory Crystal sync:** Crystal syncs to Kaleidoscope cloud with this token
- **Cross-machine relay:** messages encrypted and relayed through Kaleidoscope with this token

### Remote pairing

You don't have to be physically at the machine. The code is just a code:

1. SSH into the new machine. Run `ldm pair`. See the code.
2. On your phone (anywhere), go to wip.computer/pair. Enter the code.
3. Done. Machine is paired remotely.

### Device management

In Kaleidoscope (wip.computer), a "Your devices" section:

```
Your devices:
  Mac Mini (cc-mini)     paired Apr 6     [Revoke]
  MacBook Air (cc-air)   paired Apr 6     [Revoke]
```

Revoke kills the token. The machine is no longer authorized. All Bridge, Crystal sync, and relay access stops.

## Cross-agent approval flow

### The problem

Agents should be able to talk to each other without Parker typing in every terminal. But agents should NOT talk freely without authorization. Parker needs to approve the communication, with time limits.

### The flow

1. CC (ldmos03) wants to send a message to test-bridge
2. CC calls Kaleidoscope approval API: `POST wip.computer/api/approve-intent`
   ```json
   {
     "from": "cc-mini:ldmos03",
     "to": "cc-mini:test-bridge",
     "action": "send_message",
     "device_token": "..."
   }
   ```
3. Kaleidoscope pushes to Parker's phone (or shows in the web UI if he's logged in):
   > **CC-Mini (ldmos03) wants to message test-bridge.**
   > Approve for: [5 min] [10 min] [15 min] [This session]
4. Parker taps [10 min] with Face ID
5. Kaleidoscope returns the approval to CC:
   ```json
   {
     "approved": true,
     "window_seconds": 600,
     "expires_at": "2026-04-06T18:30:00Z"
   }
   ```
6. CC sends the message to test-bridge via local file inbox (same machine, no relay)
7. Kaleidoscope pings test-bridge's WebSocket: "you have mail"
8. test-bridge wakes up, reads inbox, responds
9. For the next 10 minutes, CC can keep messaging test-bridge without re-asking

### What the approval covers

- **Per-pair:** approval for ldmos03-to-test-bridge does NOT authorize ldmos03-to-cc-air
- **Time-boxed:** expires after the approved window. Must re-approve.
- **Revocable:** Parker can revoke from the Kaleidoscope UI at any time
- **Logged:** every approval is logged so Parker can audit who talked to whom

### Same-machine vs cross-machine

- **Same machine:** message goes through file inbox directly. Kaleidoscope is only involved for the approval and the push notification. Not the message transport.
- **Cross-machine:** message goes through Kaleidoscope's encrypted relay (R2 dead drop). Same approval flow. Different transport.

## Push notifications: waking agents up

### The problem

CC sessions only "think" when the user types. If test-bridge gets a message in its inbox, it doesn't know until Parker interacts with it. That's not real agent-to-agent.

### The solution

The bridge MCP server maintains a WebSocket connection to Kaleidoscope. When a new message lands in the inbox (from any source), Kaleidoscope pings the WebSocket: "you have mail."

The bridge receives the ping and surfaces the message to CC via MCP server-initiated notification (if supported) or by setting a flag that the next tool call picks up.

This means: CC can be idle. A message arrives. Kaleidoscope pings the bridge. The bridge wakes CC up. CC processes the message and responds. No human typing required.

### Push is local too

For same-machine delivery: the bridge can also watch `~/.ldm/messages/` directly with `fs.watch()`. When a new file appears, the bridge reads it and surfaces it. No Kaleidoscope involvement for local pushes. Kaleidoscope is only needed for cross-machine push.

## Message flow summary (all directions)

### CC-to-Lēsa (same machine)

```
CC sends via gateway (sync, reply comes back in same call)
  OR
CC sends via gateway (fire-and-forget) + Lēsa replies to file inbox
```

Parker sees CC's message in TUI. Parker sees Lēsa's reply in TUI. CC gets the reply.

### CC-to-CC (same machine)

```
CC-A writes to ~/.ldm/messages/ addressed to CC-B
Bridge or fs.watch pings CC-B
CC-B reads inbox, processes, replies to ~/.ldm/messages/
Bridge or fs.watch pings CC-A
CC-A reads inbox
```

If approval is required (cross-session): Kaleidoscope asks Parker first. If approved, messages flow for the approved window.

### CC-to-CC (cross-machine)

```
CC-Mini writes to ~/.ldm/messages/ addressed to CC-Air
Kaleidoscope relays encrypted message to Air
Air's poller writes to Air's ~/.ldm/messages/
Air's bridge pings CC-Air
CC-Air reads inbox, processes, replies
Same relay back to Mini
```

Same approval flow. Same message format. Different transport.

## Implementation order

### Phase A: Device pairing (next)

Build `ldm pair`:
- Generate short code (word-word-number)
- `POST wip.computer/api/pair/request` with the code
- Long-poll or WebSocket wait for approval
- On approval, store token at `~/.ldm/auth/kaleidoscope.json`

Build wip.computer/pair page:
- Show code entry field after passkey login
- `POST wip.computer/api/pair/approve` with code + user identity
- Match to waiting device, issue token

### Phase B: Kaleidoscope WebSocket for push

Add WebSocket endpoint to `server.mjs`:
- CC bridge connects on boot with device token
- Server maintains connection map: token -> WebSocket
- When a message event fires (from approval, from relay), ping the right client

Bridge MCP server connects on boot:
- Read device token from `~/.ldm/auth/kaleidoscope.json`
- Connect WebSocket to wip.computer/ws
- On ping: check inbox, surface message to CC

### Phase C: Approval flow

Build approval API in `server.mjs`:
- `POST /api/approve-intent` accepts from/to/action + device token
- Creates a pending approval in the DB
- Pushes to user's connected clients (web UI, phone)
- Returns when approved or times out

Build approval UI in Kaleidoscope:
- Show pending approval requests
- Buttons: 5 min / 10 min / 15 min / This session
- Face ID confirmation via passkey

Bridge requests approval before cross-session sends:
- Check local approval cache: is there a valid window for this from/to pair?
- If yes: send directly
- If no: call approval API, wait for response

### Phase D: Cross-machine relay

Extend Kaleidoscope server:
- `POST /api/relay/send` accepts encrypted message blob + destination device
- Store in R2 (24h TTL)
- Ping destination device WebSocket

Add poller to bridge (or use WebSocket push):
- On ping: download blob from relay, decrypt, write to `~/.ldm/messages/`

Encryption:
- Shared key derived during `ldm pair` (both devices paired to same account)
- AES-256-GCM
- Key never leaves the device. Kaleidoscope never sees plaintext.

### Phase E: Conversation view in Kaleidoscope

Build a "Messages" section in the Kaleidoscope web UI:
- Show threads between agent pairs
- Show approval history
- Show device status (online/offline)
- Read-only. Parker watches, doesn't type.

## Cross-references

- `ai/product/plans-prds/bridge/2026-03-30--cc-mini--bridge-messaging-architecture.md` ... the original architecture (Phases 1-5). This plan supersedes and extends it.
- `ai/product/plans-prds/bridge/2026-03-31--cc-mini--phase5-cloud-relay.md` ... relay design details
- `ai/product/bugs/bridge/2026-04-06--cc-mini--bridge-async-inbox-plan.md` ... the async inbox plan from earlier today
- `ai/product/product-ideas/vision-quest-01/architecture-spec.md` ... full Kaleidoscope product architecture
- `ai/product/product-ideas/vision-quest-01/vision-quest-02-agent-txt-era.md` ... agent.txt, Sapien ID, four-client test

## Open questions

1. **Local push without Kaleidoscope:** should the bridge use `fs.watch()` on `~/.ldm/messages/` for same-machine push, or always go through Kaleidoscope WebSocket? fs.watch is simpler for local but means two push paths.

2. **Approval granularity:** per agent-pair (ldmos03 ↔ test-bridge) or per direction (ldmos03 → test-bridge is separate from test-bridge → ldmos03)?

3. **Lēsa approval:** does CC-to-Lēsa require approval, or is it pre-approved because Lēsa is the platform agent? Parker currently sees CC's messages to Lēsa in TUI. Maybe Lēsa is always-approved.

4. **Approval persistence:** should approval windows survive CC restart? If stored in `~/.ldm/auth/approvals.json`, they persist. If in-memory only, they don't.

5. **Memory Crystal sync:** the device token from `ldm pair` is also the auth for Crystal cloud sync. Should Crystal sync start using this token as soon as pairing completes, or is that a separate opt-in?
