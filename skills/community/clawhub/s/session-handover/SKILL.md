---
name: "session-handover"
description: "Shift-style continuity notes with ownership, limits, hazards, protected targets, receipts, and exact next action."
metadata:
  openclaw:
    emoji: "🧭"
    requires:
      bins: ["jq", "rg", "python"]
---

# Session handover

Use this skill when pausing work, changing the lead model, mining session history, or preparing continuity for a fresh model that will wake up without the outgoing model's private context.

## Operating model

Treat the system as a working kitchen staffed in shifts.

The incoming shift does not need the outgoing shift's entire internal monologue. It needs an accurate station state:

- what is done;
- what is still outstanding;
- what is currently in progress and who owns it;
- what failed and must not be repeated blindly;
- what is running low or close to a limit;
- what is hazardous, uncertain, or requires verification;
- what is reserved or explicitly **DO NOT TOUCH**;
- the exact next safe action.

The purpose is operational continuity, not narrative completeness.

## Goals

- Preserve signal: user constraints, decisions, stable workflows, current state, ownership, risks, and receipts.
- Remove noise: retries, verbose tool output, duplicated pings, abandoned speculation, and private chain-of-thought.
- Prevent a fresh model from duplicating work, acting on stale state, exhausting resources, or crossing protected boundaries.
- Leave the station usable and the next action executable.

## Inputs

- Session directory: `~/.openclaw/agents/<agentId>/sessions/`
- Optional index: `sessions.json`
- Memory files in the workspace (`memory/*.md`; `MEMORY.md` only where allowed)
- Current plans, blackboards, receipts, service state, git state, and task artefacts when relevant

## Recommended output

Write or update the appropriate durable handover note, normally `SESSION_NOTES.md`, a daily memory entry, or the active typed blackboard.

Use this compact shift sheet:

1. **Outcome / station state** — what is now true.
2. **Completed** — finished work with receipts.
3. **In progress / owner** — active work and who owns it; say `none` if empty.
4. **Outstanding** — bounded remaining jobs.
5. **Failures / do not repeat** — failed approaches and exact boundaries.
6. **Running low / limits** — tokens, time, storage, quotas, hop budgets, locks, deadlines, or other capacity.
7. **Hazards / verify** — uncertain claims and checks required before action.
8. **Reserved / DO NOT TOUCH** — protected files, data, services, credentials, user decisions, and exact target scope.
9. **Next action** — one exact safe first step for the incoming shift.
10. **Receipts / rollback** — paths, revisions, hashes, backups, commands, and status.
11. **Security redactions** — confirm secrets and irrelevant private material were not copied.

Omit empty prose, but never silently omit the protected-target, hazard, resource-limit, or ownership state. Use `none known` where ambiguity would be dangerous.

## Method

1. **Inventory the station**
   - List relevant sessions and artefacts by date/size.
   - Read current plans, blackboards, locks, service state, and receipts when the task used them.
   - Resolve which work is complete, active, abandoned, or blocked.

2. **Extract user intent and constraints first**
   - Read authenticated user messages before assistant/tool output.
   - Preserve the newest applicable decision.
   - Render exact protected targets as `DO_NOT_TOUCH: <target>`.

3. **Separate state from story**
   - Record observed facts, decisions, actions, failures, evidence, and open questions distinctly.
   - Do not pass guesses as facts.
   - Do not copy private reasoning or verbose transcripts when the operational result suffices.

4. **Establish ownership**
   - Name the active owner for in-progress work.
   - If ownership cannot be established, mark the item unclaimed; do not imply it is safe to duplicate.
   - Clear stale ownership only with evidence that the prior worker is no longer active.

5. **Check resources and hazards**
   - Record remaining budgets, quotas, storage, deadlines, lock/revision state, and recovery boundaries where material.
   - Flag anything that could run out, collide, become destructive, or leave the system unrecoverable.
   - State what the incoming shift must verify before trusting volatile or high-impact state.

6. **Attach receipts**
   - Prefer exact paths, revisions, hashes, timestamps, test outcomes, backups, and rollback instructions.
   - A claim such as “fixed” requires proportionate proof.

7. **Write the shortest complete handover**
   - Make the exact next action executable without reconstructing the whole session.
   - Expire or remove stale notes rather than letting old state masquerade as current state.

8. **Read it as the incoming shift**
   - Confirm a fresh model can continue safely without asking what happened.
   - Confirm it cannot mistake reserved work for free stock or completed work for outstanding work.

## Useful command snippets

```bash
ls -lt ~/.openclaw/agents/main/sessions/*.jsonl
jq -r 'select(.message.role=="user") | .message.content[]? | select(.type=="text") | .text' <session>.jsonl
jq -r '.message.content[]? | select(.type=="toolCall") | .name' <session>.jsonl | sort | uniq -c | sort -rn
```

## Quality gate

A handover passes only if a fresh model can answer:

- What is true now?
- What was completed, and where is the proof?
- What remains, and who owns it?
- What failed or must not be repeated?
- What resource or limit is close to exhaustion?
- What must be verified before acting?
- What is reserved or forbidden to touch?
- What exact action should happen next?
- How is rollback performed if that action fails?

If any answer that matters is unclear, the outgoing shift has not finished closing down.
