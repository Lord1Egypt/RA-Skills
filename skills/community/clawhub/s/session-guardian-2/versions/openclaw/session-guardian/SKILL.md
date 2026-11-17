---
name: session-guardian
description: Detect natural session boundaries, minimize unnecessary context carryover, and produce concise handoff summaries. Use when a task is completed, a new user request may be unrelated, or context pressure makes session continuation costly; do not use to split active work prematurely.
metadata:
  openclaw:
    emoji: "🧭"
---

# Session Guardian

Manage a conversation's lifecycle without disrupting useful work. The desired outcome is one coherent work topic per session where practical, with a small, accurate handoff when a boundary is worthwhile.

## Operating principles

- Prefer continuity while the user is actively advancing the same project, dataset, incident, document, or decision.
- Treat a completed topic followed by a substantially unrelated request as a boundary candidate.
- Context size alone is not a reason to interrupt work. Use it to strengthen a recommendation at a natural stopping point.
- Never create, close, or switch a session yourself unless the host explicitly supports and authorizes that action. Recommend a boundary and prepare the handoff instead.
- Do not repeatedly recommend the same boundary. If the user continues in the current conversation, accept that choice and continue normally.
- Preserve verified decisions, required next actions, relevant files/paths, commands/parameters, constraints, and unresolved blockers. Omit routine tool output, superseded hypotheses, and failed experiments unless they remain relevant.

## When to assess

Assess session continuity only at a meaningful event:

- a requested task has been completed or reached a clear stopping point;
- the user explicitly says they are changing topic, project, or dataset;
- a new message appears unrelated after the prior topic is complete;
- reliable context-usage telemetry is available and shows elevated pressure; or
- the user asks whether to continue, compact, summarize, or start fresh.

Do not run a visible assessment after every message or while the user is in the middle of a tightly coupled troubleshooting sequence. A brief aside inside unfinished work - small talk, scheduling, a quick tangential question - is not an assessment event: answer it and keep working.

## Decide: continue, defer, or recommend a new session

First identify the **active work unit**: its objective, project/dataset, current state, outstanding work, and decisions the next reply needs.

Then estimate these signals qualitatively:

| Signal | Continue when | Boundary when |
| --- | --- | --- |
| Topic relation | The new request refines, debugs, interprets, reports on, or follows from the active work unit. | It starts an independent domain, project, dataset, or deliverable. |
| History value | Earlier decisions, files, constraints, or results are needed for a good next answer. | Most prior history would not improve the next answer. |
| Work state | Material work remains or the user is still exploring the same issue. | The prior objective is complete or parked with a clear handoff. |
| Context pressure | There is room, or the historical context is still high-value. | Telemetry is high and the work has reached a natural stopping point. |

Use these outcomes:

1. **Continue silently** when the same-topic evidence is strong. Related subtasks are not new sessions.
2. **Defer** when topic relation is uncertain or the earlier work is incomplete. Continue and reassess after a natural checkpoint.
3. **Recommend a new session** only when the old work is complete or safely parked *and* the new work has low dependence on that history; or when high context pressure coincides with a natural stopping point.

If a rough score helps, weight topic continuity most heavily (0–40), then history value (0–30), unfinished work (0–20), and context pressure (0–10). A low total supports a boundary, but the judgment and user intent override arithmetic.

## Context pressure

Use only host-provided, reliable usage information. If none is available, do not invent a percentage or claim the context is near a limit.

- Below roughly 50%: continue normally.
- Around 50–70%: keep working; prepare to hand off at the next natural completion if appropriate.
- Around 70–80%: prefer finishing the current unit and then offering a handoff.
- Above roughly 80%: strongly favor a handoff at the first safe stopping point.

Never force a split during a critical, ongoing task solely because of a threshold.

## Recommendation and handoff

When recommending a boundary, make one concise user-facing note in the user's language. Say why in practical terms; do not present a speculative token-cost claim as fact. For English, use:

> The previous topic has reached a natural stopping point, and this new request is an independent topic. I suggest starting a new session so unrelated history does not weigh on follow-up work. I have prepared a handoff summary you can copy over.

For Chinese, use:

> 前一主题已处理到可收尾状态，而当前问题属于独立主题。建议新开一个会话，避免无关历史影响后续处理。我已整理好可复制的交接信息。

Immediately provide a handoff only if it contains useful carry-forward state. Follow [the handoff template](templates/handoff.md). Include only facts established in the conversation or workspace, mark uncertainty explicitly, and state `None` for empty sections. Do not imply that the handoff transfers automatically.

For detailed boundary examples and edge cases, read [topic-boundaries.md](references/topic-boundaries.md).

## Host notes: OpenClaw

- Install this folder at `<workspace>/skills/session-guardian/` (per-workspace), `~/.agents/skills/session-guardian/` (personal, shared across agents), or the managed `~/.openclaw/skills/session-guardian/` directory. Eligible skills are snapshotted when a session starts, so a freshly installed skill becomes visible in the next session or after a gateway restart.
- OpenClaw follows the AgentSkills spec. The `metadata.openclaw` block (emoji) is optional display metadata; remove it if your OpenClaw version rejects it.
- Users can reference the skill with `$session-guardian` in the composer or invoke it as a `/session-guardian` command.
- Resetting or starting a session is a user action from the chat interface. Recommend the boundary and give the user copy-ready handoff text to paste into the new session; do not attempt to reset the session yourself.
