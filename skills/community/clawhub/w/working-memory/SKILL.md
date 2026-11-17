---
name: working-memory
description: Maintain a project's mid-term working memory — a WORKING.md file in the repo holding the current stage's state (decision log, what was tried and failed, what's next) so it survives context compaction and new sessions. Use to set up WORKING.md in a project, to read it at the start of a session, to checkpoint progress into it after a meaningful step or before /compact, and to consolidate settled conclusions into long-term assistant memory (then reset WORKING.md) when a stage completes. Triggers: "set up working memory", "checkpoint", "save state", "resume where we left off", "consolidate memory", "end of stage", or a mention of WORKING.md.
---

# Working Memory

## Why

A long session runs out of context and gets **compacted** — the transcript is squeezed into a summary, and the details drop out: decisions, edge-cases, what was already tried and failed. Work quality falls, and the next session starts blind — the user feels "didn't we already do this?".

Root cause: the important state lived **only in the conversation** — volatile memory that dies on compaction and never crosses into a new session. The fix is to stage that state onto a medium that survives: a `WORKING.md` file in the repo.

## The three levels

| Level | Medium | Lifespan |
|---|---|---|
| **Short-term** | session context | hours — dies on compaction |
| **Mid-term** | `WORKING.md` in the repo | days–weeks — while a stage runs |
| **Long-term** | the assistant's memory (e.g. Claude Code memory files) | months — survives everything |

This skill owns the mid-term level and the bridge up to long-term. Flow: **context → WORKING.md → (distill at stage end) → long-term memory.** WORKING.md is a *staging area* for memory, not a parallel store.

## The file

`WORKING.md` lives at the repo root (a working thread in a subfolder may have its own, e.g. `docs/research/WORKING.md`). Four sections:

- **Current stage** — one or two lines: where we are right now.
- **Decision log** — datestamped entries (absolute dates), newest-relevant on top: what was decided/done and *why*.
- **Tried / didn't work** — dead ends, so they aren't re-attempted.
- **Next** — open tails, TODOs, the obvious next step.

Copy `assets/WORKING.template.md` as the starting point.

## Operations

### Setup (once per project)
When a project has no WORKING.md and the work is non-trivial: copy the template to the repo root, fill **Current stage** from what's known, and add a pointer to the project's `CLAUDE.md` so it's read on every future session (snippet in `assets/CLAUDE-snippet.md`). If there is no `CLAUDE.md`, create one with just that pointer.

### Start / resume (every session)
At the start of work on a project, **read WORKING.md before acting** — it restores the stage state that context loss erased. Check subfolders for thread-specific WORKING.md too. If asked to "resume", this is the anchor.

### Checkpoint (often — the core habit)
After any meaningful decision or step — and **before a planned `/compact`, and whenever the user says "checkpoint / save state"** — append to WORKING.md: update **Current stage**, add 1–3 lines to the **Decision log**, record any new dead end, refresh **Next**. Do it *during* the work, not at session end — compaction can strike first. Keep entries terse; the quality bar is that a fresh session could resume from them.

### Consolidate (at stage end)
When a stage closes: **distill** the settled conclusions from WORKING.md up into long-term assistant memory, then **reset** WORKING.md to a clean slate for the next stage. Decide what rises with the belonging test below. This is the "sleep" step — without it, WORKING.md grows into an unreadable log and nothing reaches durable memory.

## The belonging test

For any line, ask: **"When this stage ends and WORKING.md is reset — should this survive?"**
- **Yes** → it's a settled conclusion (architecture, an infra fact, a hard-won gotcha, who-knows-what). → long-term memory.
- **No** → it's operational state (progress, an open tail, a TODO). → stays in WORKING.md, dies with the stage.

One event splits across levels: the *investigation* stays as a decision-log entry; the *lesson* rises to memory. Example — log: "spent a day chasing 87% 5xx, turned out to be bots on missing paths"; memory: "the catch-all handler must return 404 for unknown routes, not 500".

## Rules

- **Don't duplicate what code or git already show.** WORKING.md holds decisions and reasons, not a changelog you could `git log`.
- **Procedural knowledge** (how to deploy, how to test) belongs in `CLAUDE.md` or `docs/`, not WORKING.md — it's not stage state.
- **Absolute dates.** Resolve "tomorrow / next week" to a real date, so the log stays readable later.
- **Don't wait for stage end to write.** Mid-term memory only helps if it's written before context is lost.
