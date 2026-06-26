---
title: Codex Remote Control: live test runbook
date: 2026-04-28
author: cc-mini
status: ready-to-run
related:
  - 2026-04-28--cc-mini--codex-remote-control-master-plan.md
  - 2026-04-28--cody--secure-session-continuity-plan.md
---

# Codex Remote Control: live test runbook

Goal: do one live integration pass that confirms each of the four pre-dogfood gates end-to-end on a paired daemon + phone session. After this pass, the build is eligible for the install spec and `npm @alpha` tag.

Time: ~25 minutes if everything works. Most of that is pairing + opening the phone.

## Prereqs (one time)

1. **Build the daemon you'll test against.**
   ```bash
   cd ~/wipcomputerinc/repos/ldm-os/apps/wip-codex-remote-control-private
   git pull --ff-only origin main
   npm install
   npm run build
   ```
   This is the validation path, not the install path. You'll point a local daemon at `dist/cli.js`. Don't `npm link`. Don't deploy to `~/.ldm/extensions/`. Per the master plan, stable/latest install for our own packages waits on Parker's "install."

2. **Confirm relay is deployed.** Run on this Mac:
   ```bash
   curl -s https://wip.computer/health
   ```
   Expect `200 OK` with version. If not, redeploy `wip-ldm-os-private/src/hosted-mcp/server.mjs` first.

3. **Have a phone ready** with Face ID + a Sapien-ID-authenticated browser session for `wipcomputer`. The `/login?next=...` flow on `wip.computer` puts an `apiKey` and `handle` into `sessionStorage`.

4. **Have a relay-log shell open** on the VPS. Keep this open the whole test:
   ```bash
   ssh wip-vps 'pm2 logs mcp-server --lines 0 --nostream' \
     | tee ~/wipcomputerinc/screenshots/codex-remote-control-live-test.log
   ```
   Everything the relay logs during the test lands in that file. We grep it after gate 1.

## Pair the daemon (one time)

```bash
cd ~/wipcomputerinc/repos/ldm-os/apps/wip-codex-remote-control-private
node dist/cli.js link
```

The CLI prints a 6-char code + a `/pair` URL. Open the URL on the phone, sign in with passkey, enter the code. The CLI ends with:

```
codex-daemon: paired as <handle>
codex-daemon: relay key saved to ~/.codex-daemon/relay-key.json
codex-daemon: run 'codex-daemon start' to bring the daemon online.
```

Verify the E2EE keypair landed:

```bash
ls -l ~/.codex-daemon/e2ee-key.json   # should be -rw-------
```

## Bring the daemon online

In a dedicated terminal (so its stderr stays visible):

```bash
cd ~/wipcomputerinc/repos/ldm-os/apps/wip-codex-remote-control-private
node dist/cli.js start
```

Expect, in order:

```
codex-daemon: listening on ws://127.0.0.1:<port>
codex-daemon: token <local-loopback-token>
codex-daemon: pidfile <path>
codex-daemon: relay enabled (wss://wip.computer/api/codex-relay/daemon)
codex-daemon: stop with 'codex-daemon stop' or SIGINT
relay-client: connected to wss://wip.computer/api/codex-relay/daemon
```

In the relay-log shell, you should see:

```
codex-relay: daemon online for <agentId>
```

Leave the daemon running for the rest of the runbook.

## Stage one known thread (for gate 3)

The attach gate needs a real, resumable Codex thread. Easiest path: run one local Codex turn so it lands in the index.

```bash
codex --help    # confirms the CLI is present
codex           # in a fresh shell. Type one short prompt: "what file am i in?"
                # Wait for the response. Quit.
```

Capture the most recent thread id:

```bash
KNOWN_TID=$(tail -1 ~/.codex/session_index.jsonl | jq -r .id)
echo "$KNOWN_TID"
```

Save that string. You'll paste it into a phone URL.

---

## Gate 1: Privacy

**What we're verifying.** Relay logs never contain prompt text or decrypted Codex events.

**Steps:**

1. On the phone, open:
   ```
   https://wip.computer/codex-remote-control/<KNOWN_TID>
   ```
2. Wait for the system events:
   - `connected. running e2ee handshake...`
   - `encrypted channel ready (e2ee-v1).`
   - `attached to thread <prefix>... (resumed).`
3. Send a prompt with a unique probe token:
   ```
   PROBE-PRIVACY-2026-04-28-XJ7Q list files in cwd, do nothing else
   ```
4. Wait for `turn complete (...)`.
5. In the relay-log shell, stop the tail (Ctrl+C). Grep:
   ```bash
   grep -F "PROBE-PRIVACY-2026-04-28-XJ7Q" ~/wipcomputerinc/screenshots/codex-remote-control-live-test.log
   grep -iE "agent_message|command_execution|reasoning" ~/wipcomputerinc/screenshots/codex-remote-control-live-test.log
   ```

**Pass criteria:**
- First grep returns **nothing**.
- Second grep returns **nothing** (or only matches inside the test log path itself, never inside a quoted relay log line).
- The relay log contains only metadata lines like `codex-relay: daemon online for <agentId>`, `codex-relay: web online <agentId>:<threadId>`, `Session created: ...`, etc.

**Fail signals:** any prompt text, file path from `aggregated_output`, or Codex event JSON appears in the relay log. If it does, stop and file a bug under `wip-ldm-os-private/ai/product/bugs/codex-remote-control/`.

---

## Gate 2: Plaintext rejection

**What we're verifying.** A web client that tries to send plaintext `session.*` against an E2EE-capable daemon is rejected with a clear error and `ws.close(4002, ...)`.

**Steps:**

1. With the daemon still online, mint a fresh ws-ticket. From the phone you used in gate 1, open the JS console and run:
   ```javascript
   const apiKey = sessionStorage.getItem('wip_api_key');
   const r = await fetch('https://wip.computer/api/codex-relay/ws-ticket', {
     method: 'POST',
     headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + apiKey },
     body: JSON.stringify({ thread_id: 'PASTE_KNOWN_TID' }),
   });
   const { ticket } = await r.json();
   console.log('TICKET=' + ticket);
   ```
   Copy the printed ticket.

2. On this Mac, run the plaintext probe (single-file Node, no install):
   ```bash
   THREAD_ID=$KNOWN_TID
   TICKET=<paste-ticket-here>
   node -e '
     const WebSocket = require("ws");
     const url = "wss://wip.computer/api/codex-relay/web/" +
       encodeURIComponent(process.env.THREAD_ID) +
       "?ticket=" + encodeURIComponent(process.env.TICKET);
     const ws = new WebSocket(url);
     ws.on("open", () => {
       console.log("[probe] connected, sending plaintext session.send");
       ws.send(JSON.stringify({
         type: "session.send",
         id: "probe-1",
         sessionId: process.env.THREAD_ID,
         prompt: "PROBE-PLAINTEXT should be rejected",
       }));
     });
     ws.on("message", (data) => console.log("[probe] msg:", data.toString()));
     ws.on("close", (code, reason) => {
       console.log("[probe] close:", code, reason && reason.toString());
       process.exit(0);
     });
     ws.on("error", (err) => console.log("[probe] error:", err.message));
   '
   ```
   You'll need to run this with `ws` available. From the daemon's worktree, that's:
   ```bash
   cd ~/wipcomputerinc/repos/ldm-os/apps/wip-codex-remote-control-private
   THREAD_ID=$KNOWN_TID TICKET=<paste-ticket> node -e '<paste script>'
   ```

**Pass criteria:**
- One inbound message: `{"type":"error","message":"plaintext rejected: this daemon requires e2ee-v1. Send e2ee.hello first."}`.
- Close: `code 4002, reason "plaintext rejected on e2ee-capable daemon"`.
- The `PROBE-PLAINTEXT` token does **not** appear in the relay log (gate 1 also covers this; check anyway).

**Fail signals:** the probe gets an `ack`, an `unknown session` error, or any other behavior. That means the legacy plaintext path is still reachable and gate 2 isn't actually closed.

---

## Gate 3: Attach

**What we're verifying.** Opening a URL for a known thread attaches; opening a URL for an unknown thread shows the fallback and never silently runs against a different thread.

**Steps:**

1. **Known-thread case** (already done in gate 1). On the phone you opened for gate 1, you should have seen:
   ```
   attached to thread <prefix>... (resumed).
   ```
   Send a follow-up prompt that depends on context from the local Codex turn you ran in "stage one known thread":
   ```
   what was my previous question in this thread?
   ```
   Verify the response references the earlier `what file am i in?` content. That confirms `codex.resumeThread()` actually resumed and didn't allocate a new thread silently.

2. **Unknown-thread case.** Close that tab. Open:
   ```
   https://wip.computer/codex-remote-control/bogus-tid-12345-not-real
   ```
3. Wait for `connected. running e2ee handshake...` and `encrypted channel ready (e2ee-v1).`
4. Expect an error event:
   ```
   attach failed: unknown_thread thread bogus-tid-12345-not-real not found in ~/.codex/session_index.jsonl
   ```
5. Expect a yellow banner above the composer: "this thread is not on the daemon. start a fresh remote session?" with a `Start new remote session` button.
6. Click the button. Expect `new remote session started.` and the composer enables.
7. Send a probe prompt: `PROBE-ATTACH-FALLBACK what is 2+2`. Verify response is `4` (or similar) and the turn completes cleanly.

**Pass criteria:**
- Known thread: composer enables only after `attached`, follow-up prompt clearly references earlier turn.
- Unknown thread: composer stays disabled, banner appears, click runs a fresh thread, composer enables only after `session.started`.
- Composer is **never** enabled before either `session.attached` or `session.started`.

**Fail signals:** prompt sent on unknown-thread URL silently runs in a fresh thread without the fallback button being clicked. That's the B1 regression we just fixed.

---

## Gate 4: Interrupt

**What we're verifying.** Stop button aborts a running turn end-to-end.

**Steps:**

1. From the gate-3 known-thread tab (or a fresh attached session), send a prompt that takes a while:
   ```
   PROBE-INTERRUPT write a 2000-word essay about the history of the printing press, slowly
   ```
2. Wait for the first agent_message or command_execution event to appear (so a turn is actually running).
3. Tap **Stop**.
4. Watch the daemon stderr in the dedicated terminal. There should not be a crash; the abort flows back through the SDK.
5. The phone should show one of:
   - `turn failed: <reason>` (most likely; AbortController throws an aborted error)
   - or a clean `turn complete (... in / ... out)` with no further output
6. Send another prompt: `say ok`. Verify it gets a clean response. The session must still be usable after Stop.

**Pass criteria:**
- Stop visibly halts the streaming events on the phone within ~2 seconds.
- Daemon does not crash.
- Next prompt in the same session works.

**Fail signals:** the turn keeps streaming after Stop, or the session is wedged (no response to next prompt), or daemon crashes.

---

## After all four pass

Update the master plan's "Test results" section: change each `PASS / NEEDS-LIVE` to `PASS` and append the date.

Then, in order:
1. Author `wip.computer/install/wip-codex-remote-control.txt` per the LDM install spec.
2. Enroll `wip-codex-remote-control-private` in `repos-manifest.json`.
3. Run `wip-release alpha` for `@openclaw/wip-codex-remote-control@alpha`.
4. Tell Parker the version is published. Wait for the install prompt. Do not `ldm install` for our own stable/latest packages without his go-ahead.

## Cleanup

```bash
node dist/cli.js stop          # daemon
ssh wip-vps 'pm2 logs mcp-server --lines 0 --nostream'   # close the tail in the log shell
```

The relay log file at `~/wipcomputerinc/screenshots/codex-remote-control-live-test.log` is your evidence of the privacy gate. Keep it on disk for a release-or-two as audit trail; archive (don't delete) if you need to clean up.
