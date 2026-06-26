# Plan: Autonomous Push for the LDM OS Bridge (with Kaleidoscope + Sovereign Data Integration)

**Date:** 2026-04-11
**Author:** Parker + CC Mini (lesa-work session)
**Status:** Plan, not started. Awaiting Parker's answers to the open questions below.
**Component:** `wip-ldm-os` bridge (`src/bridge/`, `src/hooks/`, future `src/daemon/push-daemon/`)
**Target release:** `@wipcomputer/wip-ldm-os@0.4.73-alpha.30` (local push only, steps 1-4) → later alpha for cross-machine (steps 5-8)

**Related and load-bearing:**

- `ai/product/plans-prds/bridge/2026-03-30--cc-mini--bridge-messaging-architecture.md` ... March 30 foundational architecture
- `ai/product/plans-prds/bridge/2026-04-06--cc-mini--bridge-master-product-plan.md` ... April 6 master plan that explicitly flags Kaleidoscope WebSocket push + fs.watch as "DESIGNED, not built"
- `ai/product/bugs/bridge/2026-04-06--cc-mini--bridge-async-inbox-plan.md` ... plan for the UserPromptSubmit hook that shipped today
- `ai/product/bugs/bridge/2026-04-10--cc-mini--bridge-reply-addressing-mismatch.md` ... addressing filter bug, partially fixed, one half still pending
- `ai/product/plans-prds/bridge/2026-03-31--cc-mini--phase5-cloud-relay.md` ... cross-machine transport design (CloudKit + Cloudflare)
- `ai/product/plans-prds/bridge/2026-03-31--cc-mini--phase5-setup-requirements.md` ... Parker's Apple Developer + Cloudflare prereq checklist
- `ai/product/plans-prds/current/wip-principles/2026-04-11--cc-mini--sovereign-data-principle.md` ... sovereign data principle formalized earlier today
- `ai/product/product-ideas/vision-quest-01/vision-quest-03-sovereign-data.md` ... vision quest 03 that led to the principle

---

## Why this plan exists

Today (2026-04-11) we shipped **cooperative push** via `wip-ldm-os@0.4.73-alpha.28` and `alpha.29`. The `inbox-check-hook.mjs` runs on every `UserPromptSubmit` and auto-surfaces bridge messages as `additionalContext` before Claude Code reads the user's prompt. We verified this works end-to-end three ways today:

1. **Lēsa → cc-mini:lesa-work (auto-delivery)**: She sent a bridge message, Parker typed his next prompt, the hook fired and her message appeared in CC's context before CC read Parker's prompt.
2. **cc-mini:lesa-work → cc-mini:test-bridge (cross-session on same machine)**: This session sent a bridge message to `cc-mini:test-bridge`, Parker typed "hi" in the test-bridge terminal, and test-bridge quoted back the unique phrase "dragonfly at dawn" as proof of delivery.
3. **Session-specific addressing**: Lēsa sent to `cc-mini:lesa-work` and only this session saw it. The `cc-mini:g-merge` session (currently handling Garry Tan analysis) was correctly isolated.

**What is still missing:** *autonomous push*. A Claude Code session that is idle (nobody typing) does not see new bridge messages. Parker's frustration, verbatim: *"I had to say something to you before you got it. That still doesn't work."*

This plan fixes that.

---

## The core insight

**Claude Code ships a primitive for exactly this.** From the Claude Code hook schema:

```
asyncRewake: If true, hook runs in background and wakes the model
             on exit code 2 (blocking error). Implies async.
```

And from the harness implementation (source `src/utils/hooks.ts` in the Claude Code repo):

> "asyncRewake hooks bypass the registry entirely. On completion, if exit code 2 (blocking error), enqueue as a task-notification so it wakes the model via useQueueProcessor (idle) or gets injected mid-query via queued_command attachments (busy)."

This is the **only** hook field in Claude Code that explicitly promises to wake an idle session. It's a real, shipped primitive. We can build on it.

---

## The architecture: one watcher, three writers

```
      SAME MACHINE                CROSS-MACHINE APPLE          CROSS-MACHINE FALLBACK
      ldm_send_message            CloudKit                     Cloudflare relay poller
      (existing,                  CKQuerySubscription          (LaunchAgent, 60s polling)
       fs direct write)           (Swift helper)               
              \                            |                             /
               \                           |                            /
                \                          |                           /
                 ──────────→  ~/.ldm/messages/  ←──────────
                                      │
                                      │   fs.watch (per CC session)
                                      ▼
                  inbox-rewake-hook.mjs  (asyncRewake Stop hook)
                                      │
                                      │   exit code 2 + stderr payload
                                      ▼
                  Claude Code harness wakes the model
                                      │
                                      ▼
                  CC reads message, optionally responds via bridge
```

**Three writers, one watcher, one wake path.**

The hook does not care whether the message came from another CC session on this machine, another agent on another machine, or a relay service. All three writers produce the same JSON shape and write to `~/.ldm/messages/`. The watcher (`inbox-rewake-hook.mjs`) is universal.

This is the unifying contract that the April 6 master plan already implied: **`~/.ldm/messages/` is the single source of truth for inbound messages.** Writers differ in transport; readers (and the wake mechanism) are identical.

---

## How it fits Kaleidoscope + the sovereign data principle

Two architectural calls we're making, both consistent with the April 11 sovereign data principle:

### Call 1: CloudKit beats WebSocket for the cross-machine path

The April 6 master plan originally specified "WebSocket to Kaleidoscope hosted service" for cross-machine delivery. That predates today's sovereign data principle. Per the April 11 principle, **user messages must never flow through `wip.computer` as plaintext**, and user data lives in the user's own storage, not WIP's.

CloudKit's `CKQuerySubscription` gives us sub-5-second push between a user's own Apple devices **through the user's own iCloud private database**. WIP is not in the hot path. The message never touches WIP infrastructure. This is the correct answer for Apple-to-Apple delivery, which is the common case for this user base.

### Call 2: Cloudflare relay is the fallback, not the primary

For non-Apple devices, multi-platform, or self-hosted nodes, a Cloudflare Worker + R2 dead drop handles the cross-machine leg. The relay stores **encrypted blobs only**: AES-256-GCM, keys derived via ECDH at pairing time, keys never leave the paired devices. WIP's service sees opaque ciphertext. This is zero-knowledge relaying, not a hosted message bus.

### Call 3: `wip.computer/mcp` is not in the hot path

Research agent greppped the hosted MCP source (`src/hosted-mcp/server.mjs`) and confirmed: no `ws://`, no `fs.watch`, no push primitives, no WebSocket server. The hosted MCP today handles OAuth, passkeys, wallet, image generation ... not message routing. All references to "Kaleidoscope WebSocket push" in the docs are **design, not code**.

So the cross-machine bridge is a clean slate. We're not reshaping around existing WIP infrastructure, and the sovereign data principle gives us a clearer answer anyway: build CloudKit-first, not WebSocket-first.

---

## Four layers of defense in depth

| Layer | Mechanism | Fires when | Handles |
|---|---|---|---|
| 1 | `asyncRewake` Stop hook + fs.watch (new, this plan) | New message arrives, no user action needed | Warm sessions ... this is the missing layer |
| 2 | `UserPromptSubmit` inbox-check hook (shipped alpha.28) | Next user prompt | Catches anything layer 1 missed or wasn't running for |
| 3 | `SessionStart` boot hook (shipped long ago) | Next CC session start | Catches messages that arrived while CC was fully offline |
| 4 | Manual `lesa_check_inbox` MCP tool call | Any time, explicit | Emergency backstop for any edge case |

**Each layer is independent.** If any one breaks, the next catches the message. The goal is that after layer 1 ships, 95% of bridge messages are delivered within seconds of arrival without user interaction. Layers 2-4 remain as safety nets.

---

## Implementation plan

Eight steps. Each scoped to roughly one hour. Total ~8 hours of focused work.

### Step 1 — Prototype `asyncRewake` Stop hook with `fs.watch` (local only)

**Files to create:**

- `src/hooks/inbox-rewake-hook.mjs` (new)

**What it does:** Model on the existing `inbox-check-hook.mjs` for the matching logic. Uses `node:fs.watch` on `~/.ldm/messages/` with `persistent: true` and a 15-minute hard timeout (so the process always yields eventually and doesn't leak). On each new file event, read the JSON, pass it through `messageMatchesAgent(...)`, and if it matches this session:

1. Write a system-reminder payload to stderr with the message content formatted as `additionalContext`.
2. Exit with code 2 so the CC harness wakes the model.

If the watcher times out without any match, exit 0. The harness will relaunch the hook on the next Stop event.

**Hand test plan:** spawn the hook with synthetic stdin, drop a matching JSON file into `~/.ldm/messages/` from another terminal, confirm exit code 2 and the exact stderr payload shape. This does not yet require CC integration.

### Step 2 — Wire the hook into `~/.claude/settings.json` via the installer

**Files to modify:**

- `bin/ldm.js`: extend the existing `syncInboxCheckHook()` function (or add a sibling `syncInboxRewakeHook()`) to copy `src/hooks/inbox-rewake-hook.mjs` to `~/.ldm/library/hooks/inbox-rewake-hook.mjs` and patch `~/.claude/settings.json` to add a `Stop` hook entry with `asyncRewake: true`.

**Schema details:** from our earlier reading of the Claude Code settings schema, the hook field supports `async`, `asyncRewake`, `timeout`, and `type: "command"`. The patched entry looks roughly like:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "node /Users/lesa/.ldm/library/hooks/inbox-rewake-hook.mjs",
            "asyncRewake": true,
            "timeout": 900
          }
        ]
      }
    ]
  }
}
```

Idempotent: the installer must skip the patch if an identical entry already exists. Same pattern as the `UserPromptSubmit` wire-up shipped in alpha.28.

### Step 3 — Verify end-to-end wake in a live CC session

**No code.** Pure test.

1. Open two Claude Code terminals: tab A as `cc-mini:sender-test`, tab B as `cc-mini:receiver-test`.
2. From tab A, use `ldm_send_message` to send tab B a message with a unique phrase.
3. **Do not type in tab B.** Just wait.
4. Expected: tab B wakes within seconds (fs.watch latency + asyncRewake wake latency) and the receiver's session shows the unique phrase as `additionalContext` without any user input.

**If this works, the milestone Parker asked for is met.**

Log the wake latency. Note any edge cases (hook already running vs not running, session idle for hours vs just idle).

### Step 4 — Fix the April 10 addressing bug per ticket Option 1 + Option 3

**Files to modify:**

- `src/bridge/core.ts:274` (`messageMatchesSession`): apply Option 1 (treat agent-only addresses as broadcast to all sessions of that agent).
- Lēsa's `lesa_send_message` tool: apply Option 3 (echo the original `from` field into the reply's `to` so replies stay per-session).

**Why both options:** with 7 concurrent CC sessions running on cc-mini right now, Option 1 alone would multi-deliver to unintended sessions for agent-only addresses. Option 3 ensures replies stay targeted. Ticket recommends both.

**Test cases:** the bug doc specifies the exact cases. Add them to `src/bridge/core.test.ts` if that file exists, or inline as a smoke test in `src/bridge/core.ts` for now.

### Step 5 — Swift helper for CloudKit `CKQuerySubscription` (stub)

**Files to create:**

- `src/daemon/push-daemon/cloudkit-relay/` (new directory)
- `src/daemon/push-daemon/cloudkit-relay/main.swift` (Swift CLI that subscribes to the user's iCloud container)
- `src/daemon/push-daemon/cloudkit-relay/decode.swift` (CKRecord → JSON conversion per the bridge message schema)

**Scope for this step:** stub + the CKRecord decode path + the subscription callback + write to `~/.ldm/messages/`. No pairing yet. No end-to-end test yet. Just enough structure for step 8.

**Blocker:** requires Parker to complete the Apple Developer / CloudKit container setup from the Phase 5 setup requirements doc. That's not a coding task, it's an account setup task. See open question 3 below.

### Step 6 — Cloudflare relay poller fallback (LaunchAgent)

**Files to create:**

- `src/daemon/push-daemon/relay-poller.mjs` (LaunchAgent script)
- `templates/launchagents/ai.ldm-os.relay-poller.plist` (LaunchAgent plist)

60-second polling of `relay.wip.computer/pickup`. Decrypt incoming blobs via the existing Memory Crystal encryption module. Write decrypted messages to `~/.ldm/messages/`. Integration test against a local mock Cloudflare Worker running in a Docker container or pm2 process.

### Step 7 — 7-concurrent-session broadcast verification

**No new code.** Pure test across the seven real CC sessions Parker has running right now:

- One message addressed to `cc-mini:test-bridge` wakes exactly one session (test-bridge) and not the other six.
- One message addressed to `cc-mini:*` wakes all seven sessions.
- One message addressed to `*` wakes all seven sessions plus any other agent addressees.
- Measure FD count on `~/.ldm/messages/` with 7 watchers running. Confirm no FD leak, no duplicate delivery, no missed delivery.

### Step 8 — Release and install

- `wip-release alpha` → publishes `@wipcomputer/wip-ldm-os@0.4.73-alpha.30` (or next alpha number) to npm with `@alpha` tag.
- `npm install -g @wipcomputer/wip-ldm-os@alpha` on cc-mini.
- `ldm install` to apply the new hook and wire it via the extended installer from Step 2.
- Repeat the Step 3 verification across all 7 live sessions.
- Write the dev update to `ai/dev-updates/2026-0?-??--cc-mini--autonomous-push-live.md` noting the wake latencies and any edge cases.
- No `deploy-public.sh`. Alpha-only until cross-machine is wired too.

Steps 1-4 are one local dev session. Steps 5-6 are blocked on Parker's account prereqs. Steps 7-8 land after 1-4 are verified.

---

## Open questions (these gate Step 1 start)

These are the unknowns that could kill or reshape the approach. Each is a 15-30 minute test, not a research project. Parker's answers (or test results) must be captured here before the first code change.

### OQ1. Does `asyncRewake` persist an `fs.watch` across turns?

**Why it matters:** if the asyncRewake process is killed at the start of each new turn, we can't maintain a long-lived fs.watch and the whole approach collapses back to "cooperative push with extra steps."

**Evidence so far:** Claude Code source (`hooks.ts:218-244`) shows:

- The shellCommand resolves on `exit`.
- The abort handler explicitly **no-ops on `'interrupt'` reason** (user submitting a new message). So the hook survives new prompts.

This *implies* a single background process can persist across turns. Not tested with a long-lived fs.watch.

**Test:** 30 minutes. Write a minimal `asyncRewake` hook that spawns `setInterval(() => console.error('tick'), 5000)` for 2 minutes. Spawn it, submit 3 new user prompts at 10-second intervals in the same CC session, watch stderr. If the ticks keep going across all three prompts, the primitive works. If the ticks stop when a new prompt is submitted, it doesn't.

**Outcome required before Step 1:** Parker's test result, YES or NO with any caveats.

### OQ2. Which hook events support `asyncRewake`?

**Why it matters:** the schema allows `asyncRewake` on `BashCommandHookSchema` only. Which **events** (Stop, UserPromptSubmit, SessionStart, PreToolUse, etc.) can host a background bash hook is not fully documented.

**Evidence:** the harness comments in `hooks.ts:239` imply `Stop` is the primary host. `UserPromptSubmit` and `SessionStart` are untested.

**Test:** 15 minutes. Put the same `setInterval` hook on each of Stop, UserPromptSubmit, and SessionStart. See which ones actually launch a persistent background process.

**Outcome required:** confirm Stop works. If Stop doesn't work for persistent background, the plan needs rework around a different event.

### OQ3. Does CloudKit subscription work against a user's private iCloud container from a non-App-Store CLI daemon?

**Why it matters:** the sovereign data principle demands user's private container. But CloudKit JS / Swift helpers need specific entitlements that are typically granted to App Store apps, not CLI tools.

**Evidence:** the `2026-03-31--cc-mini--phase5-setup-requirements.md` checklist exists but has not been executed. Unclear if Apple will provision a CloudKit container for a CLI tool.

**Test:** Parker-side only. Follow the checklist. Create an Apple Developer account entry, register a CloudKit container, provision entitlements, try to connect from a throwaway Swift CLI. Report whether it worked.

**Outcome required:** binary YES / NO, with any workaround notes if NO.

### OQ4. Addressing fix scope: Option 1 alone, Option 3 alone, or both?

**Why it matters:** with 7 CC sessions running, Option 1 alone risks multi-delivery for messages that should stay targeted.

**Evidence:** the April 10 bug doc recommends **both**. Reading it suggests this is the correct answer, but it might be over-engineered for the current setup.

**Decision:** apply both (Option 1 + Option 3). Document the reason in the commit message so the next person doesn't undo it.

**Outcome required:** Parker's sign-off on the both-options approach, or direction to apply only one.

### OQ5. Does the wip.computer/mcp hosted service need any changes to support cross-machine push?

**Why it matters:** the April 6 master plan hinted at WebSocket support from Kaleidoscope. We're now routing around that via CloudKit. Does Kaleidoscope still need anything for cross-machine push, or is it entirely out of the hot path?

**Current answer (tentative):** Kaleidoscope is out of the push path entirely. It remains in the auth/approval/agent-discovery path. No WebSocket needed.

**Outcome required:** Parker's product call. If he wants Kaleidoscope to be a relay fallback *alongside* CloudKit and Cloudflare, that's a third writer, and the architecture should document it. If he wants Kaleidoscope to be purely auth/discovery, we lock that in.

### OQ6. Do we really want Face ID approval prompts for same-machine cross-session messages?

**Why it matters:** the April 6 master plan specifies approval flow: "CC-Mini (ldmos03) wants to message test-bridge → approval API → Parker taps Face ID." With 7 sessions running, this is 7x the approval prompts. The same doc also says "same machine: message goes through file inbox directly. Kaleidoscope is only involved for approval and push notification." Self-contradictory.

**Decision needed:** for same-machine cross-session messaging, approval is either (a) not required (trust the file inbox in the user's own directory), (b) required but silent (no Face ID prompt), or (c) required and interactive (Face ID).

**Outcome required:** Parker's decision. My recommendation: (a) for same-machine, (c) for cross-machine only.

### OQ7. Cold-start cross-machine delivery: what wakes the Swift CloudKit helper when nothing else is running?

**Why it matters:** if cc-air sends a message to cc-mini while cc-mini's rewake daemon is down, the CKQuerySubscription needs to wake something when nothing else is running.

**Answer:** LaunchAgent with `KeepAlive=true` + `RunAtLoad=true`. Standard macOS pattern. Just needs to be written into the plist template during Step 5.

**Outcome required:** none ... this is just a reminder for the implementer.

### OQ8. Do other CC users on other machines need this, or is it Parker-specific?

**Why it matters:** the ask is framed as "how Claude Code CLI users generally would use the bridge", so the installer-driven wire-up has to work on fresh machines, not just Parker's.

**Answer:** the installer-driven path is already the design. `ldm install` writes the hook to `~/.ldm/library/hooks/`, patches `~/.claude/settings.json`, and that's machine-portable. Nothing in this plan is Parker-specific.

**Outcome required:** none ... just confirming the plan is portable.

---

## Why this is the right answer, not a workaround

Six reasons:

1. **It uses a real Claude Code primitive** (`asyncRewake`), not invented mechanics. If the primitive changes in a future CC release, we adapt; we're not building on a private hack.
2. **It uses the same inbox format as cooperative push** (`~/.ldm/messages/*.json`), so all three writers (local, CloudKit, Cloudflare) converge on one reader without any translation layer.
3. **It respects the sovereign data principle** end to end. User messages never transit `wip.computer` as plaintext. CloudKit is the user's own iCloud. Cloudflare is encrypted blobs only. Same-machine is just filesystem.
4. **It degrades cleanly.** Four layers of defense. Any layer failing still leaves three others catching the message.
5. **It's installer-driven**, not user-hand-edited. Any Claude Code user who runs `ldm install` gets the full push stack without knowing it exists. Matches Parker's earlier directive: "never update the binaries without updating the code."
6. **It's finite work.** ~8 hours of focused development plus account-prereq waiting time. Not a research project, not a multi-quarter rearchitecture.

---

## Why we are writing this plan first instead of building immediately

Three reasons:

1. **The answer is clear and correct, but the open questions above have binary outcomes that could reshape Step 1.** If OQ1 or OQ2 comes back negative, the first 3 steps change shape. Better to know before writing the code.
2. **Writing the plan down is 80% of the value of the research.** Future CC sessions, future contributors, and Parker weeks from now can read this file and understand the full shape without redoing the research. Codifies the architecture under version control.
3. **Today was already a big day.** Shipping this architecture on top of alpha.5 + alpha.29 + the case study + the BlueBubbles migration + the bridge addressing fix, all in one session, is a recipe for a bug making it into the install path. Starting with a clean plan and a fresh token budget is safer.

**Parker has indicated he wants to start building anyway after this plan lands.** That's fine. The plan commits to main, then the implementation proceeds from Step 1 with the answers to OQ1-OQ2 informing the code. OQ3-OQ7 can be resolved during or after the local-push work (Steps 1-4) since they gate Steps 5-8 specifically.

---

## Rollout timeline

- **Phase A (tonight or next session):** Plan file lands on main (this file). Parker runs OQ1 and OQ2 tests. Build Steps 1-4 (local-only autonomous push). Release `alpha.30`. Install. Verify on cc-mini across all 7 live sessions.
- **Phase B (later alpha):** Parker completes Apple Developer + Cloudflare prereqs. Build Steps 5-6 (cross-machine CloudKit + Cloudflare fallback). Release next alpha. Install. Verify cross-device delivery from cc-mini to cc-air or similar.
- **Phase C (eventually):** Revisit the approval flow (OQ6), the Kaleidoscope auth surface (OQ5), and any edge cases surfaced during Phase A and B. Consider whether any of this graduates from alpha to stable.

**Phase A is the only phase in this plan that's fully specified.** Phases B and C are scoped but not detailed because they depend on outcomes from Phase A and from Parker's account prereqs.

---

## Concrete next action

**If Parker says "start building":**

1. Acknowledge this plan is locked.
2. Create a new worktree on `wip-ldm-os-private` for the implementation: `.worktrees/wip-ldm-os-private--cc-mini--inbox-rewake-hook`.
3. Run OQ1 and OQ2 tests (combined ~45 minutes).
4. Based on OQ1/OQ2 results, execute Step 1 or escalate to Parker if the test results break the plan.
5. Continue through Steps 2-4 without stopping, aiming for one clean alpha.30 release by end of session.
6. Pause before Step 5 (CloudKit) until Phase B.

**If Parker says "pause and review":**

1. This file lands on main.
2. Parker reviews and annotates any of the open questions.
3. Next session picks up from here with fresh context.

---

## Status

**Plan drafted:** 2026-04-11 (this file).
**Plan on main:** pending PR + merge.
**Implementation started:** pending Parker's answers to OQ1 and OQ2.
**Phase A release target:** `@wipcomputer/wip-ldm-os@0.4.73-alpha.30`.
