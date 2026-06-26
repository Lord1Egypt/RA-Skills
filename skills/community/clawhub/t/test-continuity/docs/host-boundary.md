# Host Boundary — Skill/Shared vs Host/Live

## Purpose

This document clarifies what belongs to the **public skill** (shared, portable)
and what belongs to the **host gateway / adapter** (private, instance-specific).
A public skill cannot claim it automatically guarantees channel frontstage
safety; the host must wire its own adapter hooks. See also
[`channel-boundary-stopgap.md`](channel-boundary-stopgap.md) for the minimal
channel-boundary stopgap used to suppress `<final>` leakage and weird heartbeat
text, and [`host-operator-settings.md`](host-operator-settings.md) for the
operator knobs that should be configured at the host/runtime level.

---

## Layer 1 — Skill / Shared (A-class)

These files ship with the skill and contain **no host-specific references**.

| Path | Role |
|------|------|
| `scripts/personal_hooks.py` | Frontstage guard: strips narration, enforces HEARTBEAT.md |
| `scripts/followup_skill_harness.py` | Follow-up scheduling harness |
| `scripts/web_live_runner.mjs` | Web live-check runner |
| `HEARTBEAT.md` (workspace optional) | Model-facing heartbeat instructions when the host keeps a heartbeat checklist |
| `config.schema.json` | Skill configuration schema |
| `docs/*` | Documentation |

**Rule**: No host-specific IDs, no gateway port numbers, no channel destination IDs, no agent IDs
in this layer. Temp-dir prefixes use `ph-` (personal-hooks).

---

## Layer 2 — Host / Adapter (B-class)

These files live **outside** the skill directory, in the gateway's plugin tree.
They are instance-specific and NOT part of the public skill.

| Path (relative to stateDir) | Role |
|------------------------------|------|
| `workspace/plugins/personal-hooks-host-adapter/index.ts` | Adapter: wires `message_sending` + `before_message_write` hooks |
| `openclaw.json` | Gateway config incl. `agents.defaults.heartbeat` |

**What the adapter does that the skill cannot**:

1. **`message_sending` hook** — intercepts ALL outbound (including heartbeat)
   inside `deliverOutboundPayloads`. This is the last line of defense against
   dirty narration reaching the outbound channel adapter. The skill's `personal_hooks.py` only
   runs during model generation; it cannot intercept the delivery pipeline.

2. **`before_message_write` hook** — strips session content for persistence.
   This does NOT affect outbound delivery (they are independent paths).

3. **`agents.defaults.heartbeat`** — gateway-level config required for the
   heartbeat outbound adapter to resolve. Without it, heartbeat delivery
   fails with "Outbound not configured for the selected channel".

4. **`heartbeat.isolatedSession = true`** — gateway-level config that keeps
   background heartbeat runs out of the main direct-conversation session.
   Without it, heartbeat prompts / dispatch context / internal narration can
   re-enter the same continuity store used by ordinary user replies.

5. **new-session startup bootstrap** — when a host starts a fresh `/new` or
   `/reset` session and no real human text exists yet, the host must not
   synthesize a fake user utterance just to drive startup logic. The safe
   startup path is:
   - run `runtime-context --user-text "/new" --is-new-session`
   - use trusted carryover/pending-topic state for internal bootstrap only
   - if the runtime injects a startup bootstrap block as a pseudo-`user` turn,
     treat it as internal control context, not as real human text
   - wait for the first actual human message before any `preagent-sync`
   - do **not** turn bootstrap text into fake user input
   - `/new` may still open from trusted carryover / pending-topic / tracked-followup / schedule context when the timing/safety context justifies it
   - do **not** resume pending topics on the user's behalf from fabricated user text

If a host fabricates text such as a greeting or rest phrase and feeds it into
`preagent-sync`, the skill will treat that text as real user input. This can
misfire sleep/rest suppression, erase the true continuity anchor, and distort
new-session behavior.

## Simple host/operator summary

If someone installs the public skill package, they get the shared continuity
mechanism. They do **not** automatically get every host/live integration.

The missing host pieces are usually:

- **Channel adapter / outbound last-defense**
  - the final outbound interception layer before channel delivery
- **gateway hook wiring**
  - the lifecycle hookup that makes the skill run at the right reply stages
- **live heartbeat host glue**
  - heartbeat scheduling/isolation/delivery wiring for reliable background
    follow-up

This is intentional. The public package stays portable; host/runtime integration
remains opt-in.

---

## Why the skill alone is not enough

```
Model generates reply
       │
       ▼
personal_hooks.py strips narration  ← Skill layer (A)
       │
       ▼
before_message_write persists       ← Adapter layer (B), session only
       │
       ▼
resolveHeartbeatReplyPayload        ← Gateway internal, uses RAW replyResult
       │
       ▼
deliverOutboundPayloads             ← Gateway internal
       │
       ▼
message_sending hook intercepts     ← Adapter layer (B), last defense
       │
       ▼
Channel adapter send
```

The gateway's `resolveHeartbeatReplyPayload` reads from the **raw** model
result, not the hooked session content. So even if the skill's Python guard
strips narration perfectly, a dirty heartbeat reply can still leak through
unless the adapter's `message_sending` hook catches it.

Also: if heartbeat shares the same session key as the direct user thread,
background heartbeat text can pollute carryover / staging / continuity even
when the visible outbound message is clean. The correct host fix is to set
`heartbeat.isolatedSession=true`, which moves heartbeat runs to
`<sessionKey>:heartbeat` while still allowing outbound delivery to the same user.

---

## Deployment checklist for a new host

1. Install skill to `workspace/skills/personal-hooks/`
2. Wire a host adapter at `workspace/plugins/personal-hooks-host-adapter/`
3. Configure `agents.defaults.heartbeat` in `openclaw.json`
4. Set `heartbeat.isolatedSession=true` for any host that uses background heartbeat pushes
5. Verify `message_sending` hook fires: look for `message_sending MODIFY` in gateway logs
6. Verify heartbeat delivery: check channel-delivery ACK entries after first tick
7. Verify heartbeat runs are using `:heartbeat` isolated sessions instead of the main direct session
8. Verify `<final>` tags and heartbeat narration are stripped from final outbound text
9. Verify `/new` startup does **not** invent fake user text before the first
   real human message
