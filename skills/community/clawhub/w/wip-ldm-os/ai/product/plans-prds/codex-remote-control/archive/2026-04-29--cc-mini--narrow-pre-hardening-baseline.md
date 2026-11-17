---
title: "Narrow pre-hardening baseline test for Codex Remote Control"
date: 2026-04-29
status: ready-to-run
owner: Codex Remote Control pair (Claude Code implements; Cody/Codex reviews)
reviewer: Overall Security Codex (validates the gate after the run)
related:
  - 2026-04-28--cc-mini--codex-remote-control-master-plan.md
  - 2026-04-28--cc-mini--codex-remote-control-live-test-runbook.md
  - 2026-04-29--codex--relay-auth-security-ticket.md
---

# Narrow pre-hardening baseline

## Purpose

Validate that the install / pair / UI shell of Codex Remote Control works **as deployed today**, before the VPS Security pair lands its hardening train (#727, #729, #731, #732, #733). This baseline answers one question: does the user get from `Read https://wip.computer/install/wip-codex-remote-control.txt` to a fully-rendered, key-paired phone surface ... without exposing prompt or output content through the still-un-hardened relay?

## Constraint (the "narrow" part)

**Do not type a prompt.** Do not let any Codex prompt or output flow through the relay during this test. The relay does not yet enforce:

- WS Origin allowlist (#731)
- Production rejection of `?token=ck-...` (#727)
- Per-thread daemon response routing (#733)
- Hardcoded-key removal + rotation (#727)
- Log audit / redaction (#729)

Until those land, the relay is a credentialed but not fully hardened path. The phone-side code already encrypts via E2EE (page.tsx + codex-relay-e2ee.ts), so any frame that does cross the wire is ciphertext ... but we do not need to test that here. Phase 7 / dogfood post-hardening tests it.

The baseline runs everything **up to** the point where the user would type a prompt, then stops.

## Owner / reviewer / output shape

- **Implementer:** Remote Control Claude Code (this agent).
- **Reviewer:** Remote Control Cody/Codex.
- **Gate validator:** Overall Security Codex.
- **Output:** one line, exactly: `baseline reached install/pair/UI only; no prompt/output through relay`. Or: a precise failure description with the step that broke and the observed vs expected behavior.

## Prerequisite: VPS Security pair confirms

Before the baseline runs, the VPS Security pair must report back on item #1 (Postgres token check or rotation). Output expected from them: `suffix present` (the testing daemon's existing `ck-` token is in Postgres `ApiKey` and survives the future hardening cut) or `rotated and inserted` (a fresh key was generated, inserted into Postgres, and the test daemon rebuilt with it). Without that confirmation, the baseline test could pass against a token that's about to be revoked, which is meaningless data.

## Steps

Run from a fresh terminal session. Treat each step as a checkpoint with a yes/no result.

### Step 1: AI reads install spec

Paste the install prompt into a fresh Codex CLI session:

```
Read https://wip.computer/install/wip-codex-remote-control.txt

Use the install document and live local checks as the source of truth. Do not search memory or prior notes for this install.

Check if it's installed. If yes, show me what version I have.

If not, walk me through setup and explain:

1. What is Codex Remote Control?
2. What does it install on my system?
3. How does my phone drive my Codex session?

Then ask:
- Do you have questions?
- Want to see a dry run?

If I say yes, install via `ldm install --alpha wip-codex-remote-control` and walk me through pairing my phone.

Don't install anything until I say "install".
```

**Expected:** AI fetches the spec, reports "not installed" with live-check evidence, names the three install pieces (npm package + binaries, Codex MCP registration, daemon state dir), names the license/sovereignty paragraph, recommends a dry run.

**Pass criteria:** AI's summary mentions MIT/AGPLv3 + `https://github.com/wipcomputer` (the license/sovereignty paragraph must not be paraphrased away). AI explicitly calls out the MCP server registration even if the dry-run output lists only `cli, module`.

### Step 2: Dry-run

Say "yes, dry run."

**Expected:** AI runs `ldm install --alpha --dry-run wip-codex-remote-control`. Approve the network-out prompt. Output names the package, binaries, and where they would land. AI summarizes in plain English and explicitly mentions the MCP server registration even though `Interfaces detected:` lists only `cli, module`.

**Pass criteria:** "Dry run completed. No changes were made." line appears. AI summary names MCP.

### Step 3: Real install

Say "install."

**Expected:** AI runs the three commands in order:

```bash
ldm install --alpha wip-codex-remote-control
codex mcp add wip-codex-remote-control -- codex-daemon-mcp
codex-daemon start
```

Approve each sandbox prompt.

**Pass criteria:**

- `which codex-daemon` prints a path.
- `which codex-daemon-mcp` prints a path.
- `grep wip-codex-remote-control ~/.codex/config.toml` returns the MCP entry.
- `codex-daemon status` shows pid + relay state.
- `~/.codex-daemon/` exists and has a `token` file.

### Step 4: Pair the phone

In the Codex session, the AI will tell you to run `codex-daemon link`. Run it.

**Expected:** Terminal prints a 6-char code and a `/pair` URL on `wip.computer`. Open the URL on your phone, sign in with Face ID / Touch ID, type the code.

**Pass criteria:**

- Pair completes within 5 minutes.
- `~/.codex-daemon/relay-key.json` exists (chmod 600).
- `~/.codex-daemon/e2ee-key.json` exists (chmod 600).
- Daemon log shows `relay-client: connected to wss://wip.computer/api/codex-relay/daemon`.

### Step 5: Invoke `/remote-control`

In the Codex session, type `/remote-control`.

**Expected:** The MCP tool returns a URL of the shape:

```
https://wip.computer/login?next=%2Fcodex-remote-control%2F<thread-id>
```

**Pass criteria:**

- URL is returned, not an error.
- URL is on `wip.computer` (not a different host).
- The URL's `next=` parameter points to `/codex-remote-control/<thread-id>` for an actual thread id (not a placeholder).

### Step 6: Open the URL on phone, render the shell

Open the URL on your phone.

**Expected:**

- `wip.computer/login` authenticates (the phone is already signed in from step 4 if same browser session; otherwise Face ID prompts).
- Browser redirects to `wip.computer/codex-remote-control/<thread-id>`.
- The Next.js phone page renders.
- The page calls `GET /api/codex-relay/bootstrap/<thread-id>` (returns 200 JSON with `daemon_online: true`, `daemon_public_key`, `e2ee_available: true`).
- The page calls `POST /api/codex-relay/ws-ticket` (returns 200 JSON with a ticket).
- The page generates an ephemeral browser keypair, opens WSS with `?ticket=...`, sends `e2ee.hello`.
- The daemon responds with `e2ee.ready`.
- The phone page sends `session.attach { threadId }` (encrypted as `e2ee.frame`).
- The daemon responds with `session.attached` or `session.attach.failed { unknown_thread }`.
- If `session.attached`: composer enables but is empty. **STOP HERE.**
- If `session.attach.failed`: yellow "start new remote session" banner appears. **STOP HERE.**

**Pass criteria:**

- DevTools Network panel shows `/bootstrap` and `/ws-ticket` calls returning JSON 200.
- DevTools Network panel WS URL is `wss://wip.computer/api/codex-relay/web/<tid>?ticket=<short-string>`. **No `ck-` substring anywhere in the URL.**
- DevTools Console shows no errors.
- The page reaches one of: composer-enabled-empty, or the yellow fallback banner. Either is a pass.

### Step 7: STOP

**Do not type a prompt. Do not click "Start new remote session". Do not press any control that would cause a `session.send` or `session.start` to flow through the relay.**

Close the browser tab. `codex-daemon stop` to stop the daemon.

## Recovery if the baseline fails

Each step has a clear pass criterion. If a step fails:

1. Capture: AI output, terminal output, daemon stderr, browser console, Network panel screenshot.
2. Stop the test. Do not advance past the failed step.
3. Report failure with: which step, what was expected, what happened, captured evidence.

Specifically:

- **Step 1-3 failure** → Codex Remote Control pair owns the fix (install spec, install commands, dialog).
- **Step 4 failure** (pair flow) → Could be either pair: the daemon's pair flow (Codex Remote Control) or the relay's `/api/codex-relay/pair-*` endpoints (VPS Security). Triage by error message.
- **Step 5 failure** (`/remote-control`) → Codex Remote Control pair (MCP tool returns).
- **Step 6 failure** (phone shell render) → Triage. Bootstrap / ws-ticket failures are VPS Security territory. Phone-page rendering failures are Codex Remote Control territory. The DevTools Network panel will say which.

## Output (when baseline passes)

Report exactly:

> baseline reached install/pair/UI only; no prompt/output through relay

Plus a one-line breadcrumb naming the test thread id used (so the VPS Security pair can confirm the same daemon-pair survives the hardening cut).

## What this baseline does NOT cover

- Actual prompt-and-stream behavior (the four pre-dogfood gates: privacy, plaintext rejection, attach happy-path, interrupt). Those run post-hardening.
- WS Origin allowlist (#731) ... not yet active.
- Production token-fallback rejection (#727) ... not yet active.
- Per-thread daemon response routing (#733) ... not yet active.
- Hardcoded-key cleanup + rotation (#727) ... not yet active.
- Log audit / redaction (#729) ... not yet active.

When all five P0 hardening items land + deploy + smoke-test, the post-hardening dogfood (`live-test-runbook.md` + `npm test`) is the next gate.
