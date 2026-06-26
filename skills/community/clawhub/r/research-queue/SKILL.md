---
name: research-queue
description: Structured background research queue for unresolved technical, product, algorithmic, mathematical, and workflow questions. Use when the user wants to capture open questions in `QUESTIONS.md`, investigate them over time, run bounded web/local experiments, update queue state, or build an autonomous cron-driven research loop with strict evidence and completion tracking.
---

# Research Queue

Use this skill when work produces unresolved questions that deserve deliberate investigation instead of ad-hoc guessing.

## Core workflow

1. Read `QUESTIONS.md`.
2. If the file is missing, initialize it using the format in `references/queue-format.md`.
3. Select at most one question unless the user explicitly asks for batch processing.
4. Prefer the highest-priority `open` question with the strongest practical value.
5. Investigate using only the minimum tools needed.
6. Update the question entry in place with:
   - status
   - startedAt / completedAt when applicable
   - evidence summary
   - conclusion or blocked reason
   - memory note path if something durable was learned
7. If the final status is `done` or `wontfix`, move the entire question block from `## Active Questions` to `## Completed Questions` in the same edit pass.
8. Write durable findings to `memory/YYYY-MM-DD.md` when they are worth remembering.

## Allowed investigation methods

Choose the lightest method that can answer the question:

- `web_search` for fast grounded search
- `web_fetch` for reading specific pages
- `browser` only when a real browser is needed
- `read` for local docs/config/code
- `exec` for bounded local experiments, scripts, benchmarks, math checks, and repro steps

Allowed local coding includes short Python, Rust, JavaScript, or shell experiments when they directly help answer the selected question.

## Hard rules

- Investigate one question at a time by default.
- Do not silently delete old questions.
- Do not mark a question `done` without a concrete conclusion or result.
- Distinguish clearly between verified findings, hypotheses, and blocked work.
- When a question becomes `done` or `wontfix`, move it out of `## Active Questions` immediately; do not leave completed items in the active section.
- Use plausible real timestamps only; never write a `completedAt` in the future relative to the current run.
- Do not modify production code or config unless the user explicitly asks for implementation work; research mode may create bounded scratch experiments or propose diffs instead.
- Do not let the queue turn into vague brainstorming sludge; rewrite unclear entries into concrete answerable questions.

## Status model

Use only these statuses in `QUESTIONS.md`:

- `open` — not started yet
- `investigating` — currently being worked
- `blocked` — cannot finish without missing input/access/time
- `done` — answered well enough for now
- `wontfix` — intentionally dropped

## First-use initialization

If `QUESTIONS.md` does not exist:

1. Read `references/queue-format.md`.
2. Create `QUESTIONS.md` from the canonical template.
3. Keep the initial headings and status conventions intact.
4. Add only the starter examples or the user’s real questions; do not pad it with fake research tasks.

## Automation

Prefer **OpenClaw cron** when the user wants this queue processed automatically.

- Default to cron, not HEARTBEAT.
- Use HEARTBEAT only if the user explicitly wants main-session, drift-tolerant background attention.
- Be explicit that this means the OpenClaw `cron` tool, **not** Unix `crontab`.
- Prefer isolated cron runs so research work does not pollute the main conversation.
- For scheduling details and the minimal run prompt, read `references/automation.md`.

## What good completion looks like

A finished question should leave behind:

- a stable answer or a bounded partial answer
- the evidence source or experiment basis
- completion time that matches the actual run window
- relocation of finished work into `## Completed Questions`
- durable memory only if the result is likely to matter later

## References

- Queue structure and canonical template: `references/queue-format.md`
- Automation and OpenClaw cron guidance: `references/automation.md`
