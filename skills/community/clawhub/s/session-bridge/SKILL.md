---
name: session-bridge
description: Use when context is lost after switching surfaces (Telegram to WhatsApp, TUI to Telegram), when handing off tasks between agents (Jon → Eddie, Cipher → Eddie), when an agent needs to know what was discussed in another session, or when you want to resume a conversation on a new surface. Triggers on "catch me up", "what were we working on", "pass this to Eddie", "context switch", "session handoff", "I'm on TUI now", "continue from where we left off".
---

# Session Bridge

Keep context coherent across surfaces (Telegram / WhatsApp / TUI) and agents (Eddie ↔ Jon ↔ Cipher ↔ Sage ↔ Picasso) using lightweight **topic capsules** — without syncing full transcripts or adding load to the memory system.

## Core Concept

Each active work thread gets a **capsule** — a small JSON file keyed by topic:

```
tasks/bridges/
  looking-glass.json        ← Meta Ray-Ban project
  session-bridge-design.json ← This skill's design thread
  clawhub-skill-build.json  ← Active publishing task
```

Capsules hold only what matters: goal, status, decisions, open questions, next action. They are **transient working state**, not long-term memory. They do not replace `MEMORY.md`, daily logs, or the ontology graph — they sit on top as a coordination layer.

---

## Script

```bash
SCRIPT=~/.openclaw/workspace/skills/session-bridge/scripts/bridge.py
python3 $SCRIPT <command> [options]
```

---

## Commands

### Create a capsule
```bash
python3 $SCRIPT create \
  --topic "looking-glass" \
  --goal "Wire Meta Ray-Bans as Eddie's physical presence" \
  --source "agent:main:telegram:direct:7550791652" \
  --agent main
```

### Update a capsule (after decisions, handoffs, progress)
```bash
python3 $SCRIPT refresh \
  --topic "looking-glass" \
  --status "active" \
  --next-action "Mike to share Ray-Ban SDK access" \
  --add-decision "Use Bluetooth audio bridge, not USB" \
  --add-question "Does Ray-Ban SDK expose camera feed?" \
  --add-fact "Mike's Ray-Bans model: Meta Ray-Ban v2"
```

### Get a briefing for session start (hydrate)
```bash
python3 $SCRIPT hydrate --topic "looking-glass"
```

Output (~150–350 tokens):
```
[Session Bridge] Topic: looking-glass
Status: active
Goal: Wire Meta Ray-Bans as Eddie's physical presence
Decisions: Use Bluetooth audio bridge, not USB
Open: Does Ray-Ban SDK expose camera feed?
Next: Mike to share Ray-Ban SDK access
Sources: agent:main:telegram:direct:7550791652
Updated: 2026-03-20T06:45Z
```

### Cross-agent handoff
```bash
python3 $SCRIPT handoff \
  --topic "session-bridge-design" \
  --to "agent:main:telegram:direct:7550791652"
```
Then pass the output to `sessions_send` so Eddie wakes up informed.

### See all active capsules
```bash
python3 $SCRIPT list
python3 $SCRIPT status --topic "looking-glass"
```

### Clean up stale capsules
```bash
python3 $SCRIPT expire --max-age-hours 48
```

---

## Bridging Surfaces (Telegram ↔ WhatsApp ↔ TUI)

### Option A — Config routing (recommended first step)

Add `identityLinks` to `openclaw.json` to collapse the same human across surfaces into one canonical session per agent:

```json
{
  "session": {
    "dmScope": "per-channel-peer",
    "identityLinks": [
      {
        "canonical": "mike",
        "peers": [
          "telegram:7550791652",
          "whatsapp:+15555550123"
        ]
      }
    ]
  }
}
```

This makes Telegram-Eddie and WhatsApp-Eddie share the **same session** — no bridging needed. TUI uses a different mechanism (main session key).

### Option B — Capsule hydration on surface switch

When the same canonical session is not possible (TUI ↔ Telegram, or different agent entirely):

1. On the outgoing surface, refresh the relevant capsule:
   ```bash
   python3 $SCRIPT refresh --topic <topic> --next-action "..."
   ```
2. On the incoming surface, hydrate at session start:
   ```bash
   python3 $SCRIPT hydrate --topic <topic>
   ```
3. Inject the briefing as context before responding.

---

## Bridging Agents (Jon → Eddie, Cipher → Eddie)

When finishing a delegation task, the completing agent should:

1. Refresh the capsule with results:
   ```bash
   python3 $SCRIPT refresh \
     --topic "<task-topic>" \
     --status "done" \
     --add-decision "Research complete: X is the right approach" \
     --next-action "Eddie to implement"
   ```

2. Generate a handoff and deliver via `sessions_send`:
   ```bash
   python3 $SCRIPT handoff --topic "<task-topic>" --to "agent:main:telegram:direct:7550791652"
   # Copy output → sessions_send(sessionKey="agent:main:...", message=<output>)
   ```

Eddie reads the brief and continues — no re-explaining needed.

---

## What Goes Where

| Information type | Where it lives |
|---|---|
| Current topic, status, next action | Capsule (transient, expires) |
| Decisions worth keeping long-term | `MEMORY.md` (promote manually) |
| Structured facts (people, devices, projects) | Ontology graph |
| Narrative context / observations | Daily memory log |
| Team operating rules | `SHARED_CONTEXT.md` |

Capsules are **not** a replacement for memory — they are short-lived working state that gets discarded when a topic concludes.

---

## Token Cost

| Operation | Approx. tokens | When |
|---|---|---|
| Create/refresh capsule | ~150 | On handoff or decision |
| Hydrate (session start briefing) | ~200–350 | Once per session |
| Handoff message | ~300 | Cross-agent delegation |
| Status/list | ~100 | On demand |

Hydration adds **<0.2% of a 200k context window** per session. Stale capsules add zero cost (they're just files).

---

## Agent Protocol (Team Rules)

- **On delegation:** create or refresh capsule before `sessions_send`-ing a task
- **On completion:** refresh capsule with outcome + next action, then handoff
- **On surface switch:** hydrate the relevant capsule at session start
- **On topic close:** set `--status done`, let expire cleanup handle it
- **Never:** dump full session transcripts into capsules (defeats the point)

---

## Example: Full Cross-Agent Flow

```
Mike asks Eddie about the Looking Glass project.
Eddie doesn't remember details from last session.

1. Eddie runs: bridge.py hydrate --topic looking-glass
   → Gets: "Status: active | Next: Mike to share SDK access"
   → Continues conversation without re-explaining from scratch

Mike tells Eddie: "Let Jon research the Ray-Ban SDK."
Eddie creates a task capsule and delegates to Jon via sessions_send.

Jon finishes research.
2. Jon runs: bridge.py refresh --topic looking-glass \
     --add-decision "SDK exposes camera feed via BLE" \
     --next-action "Eddie to prototype BLE bridge"
3. Jon runs: bridge.py handoff --topic looking-glass \
     --to agent:main:telegram:direct:7550791652
4. Jon sends handoff output to Eddie via sessions_send.

Eddie receives handoff.
5. Eddie reads capsule brief, continues work without Jon re-explaining.
```

---

## Setup

No dependencies beyond Python 3.8+. Works immediately after install:

```bash
openclaw skills install session-bridge
python3 ~/.openclaw/workspace/skills/session-bridge/scripts/bridge.py list
```
