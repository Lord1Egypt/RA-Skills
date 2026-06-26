---
name: groove-work-compound
description: "Document lessons, update rules/templates/docs. Use to capture learnings after review."
license: MIT
allowed-tools: Read Write Edit Glob Grep Bash(git:*) AskUserQuestion
metadata:
  author: andreadellacorte
---

# groove-work-compound

## Scope

**"This conversation" means the full chat thread** (all messages in the same chat where the user invoked compound). Lessons and compound actions come from work done or decided anywhere in that thread.

**In scope:**
- Work done earlier in the same chat: other skill runs (e.g. /ppp-weekly-report, /groove-work-plan), file or bean edits, decisions, review or planning discussion.
- Any bean or work item the user or the thread refers to as part of the workflow (e.g. the epic or task this compound stage belongs to). Use those to ground lessons and actions.

**Not in scope unless the user asks:** Daily memory, weekly summaries, or other docs (e.g. "compound on the whole day").

**If no other work is visible** in the context when compound runs (e.g. the turn only shows the compound request): **ask** which session or work to compound on (e.g. "I only see the compound request. Which session should I compound on — e.g. the PPP run above, or something else?") instead of concluding "no work discussed."

## Outcome

Lessons, root causes, and fixes are documented. Relevant project files are updated (rules, templates, docs, task bodies). A checklist of compound actions with done/pending status is produced.

## Acceptance Criteria

- Lessons are documented with root cause analysis (not just what went wrong, but why)
- Relevant project files are updated: rules files, templates, docs, task bodies
- Checklist is produced with each action marked done or pending
- If user frustration patterns were detected, they are specifically captured
- "No new lessons" is an explicit acceptable outcome — capture it rather than skipping

## Constraints

- Read `tasks.backend` from `.groove/index.md`; memory path is always `.groove/memory/`
- **Pending capture**: if `.groove/.cache/pending-capture.md` exists (staged by the `session-capture` Stop hook), read it first and use its commits/working-changes as ground-truth source material for the lessons and the git context — so a forgotten or compacted session is not lost. After the compound stage is recorded, delete `.groove/.cache/pending-capture.md`.
- Before producing the compound actions checklist, check for open mistake incidents via `/groove-utilities-memory-mistakes --list`:
  - If open incidents exist: process each using the log → fix → audit → resolve cycle from `/groove-utilities-memory-mistakes` before moving on
  - Add to compound checklist: "mistakes: N incident(s) resolved → learned/<topic>" (done/pending)
  - If no open incidents: skip silently
- Output goes into existing project files — do not create new files unless necessary
- Always run even if it seems like "nothing to capture" — capture that explicitly
- Compound actions checklist must include why each action matters, not just what it is
- If user showed repeated fixes, confusion, or rework: capture the pattern and its trigger
- Create stage task in backend if `tasks.backend != none` via `/groove-utilities-task-create` with a descriptive title so multiple compounds per day are distinct: `YYYY-MM-DD, Compound — <brief topic>` (topic from the work just closed, e.g. release, feature, or session summary). Do not number stages in task titles.
- After producing the compound actions checklist, identify any lesson that is about AI workflow,
  agent behaviour, tool usage, or engineering process — not specific to the codebase or product
- If any such lesson is found:
  - Propose: "Workflow learning detected — add to .groove/memory/learned/<suggested-topic>.md?"
  - Suggest a topic name based on the content (e.g. `patterns`, `tools`, `anti-patterns`, `hooks`)
  - Wait for user to confirm, pick a different topic, or skip
  - If confirmed: append the lesson as a bullet under a `## <YYYY-MM-DD>` heading in the file;
    create the file with a `# <Topic>` heading if it does not exist; create the dated heading if absent
  - Add to compound checklist: "workflow learning → .groove/memory/learned/<topic>.md" (done/pending)
- If no workflow lessons, skip this step entirely — no prompt, no noise
- If a workflow learning was captured locally AND `groovebook:` is set in `.groove/index.md`: add a one-line suggestion after the checklist: "Learning captured → `.groove/memory/learned/<topic>.md`. Publish to groovebook? Run `/groove-groovebook-publish`." If `groovebook:` is absent: skip silently.
- After a workflow learning is captured, offer graduation: "Is this lesson stable enough to apply to every future session? Run `/groove-utilities-memory-graduate <topic>` to promote it to AGENTS.md permanently." — only suggest if the lesson was just confirmed, not every compound run.
- After the workflow learning step, scan the conversation for deferred items — phrases like "we'll come back to", "do this later", "next time", "TODO", "skip for now", "won't fix today". If any are found: list them and ask "Capture any of these as promises? (numbers, or enter to skip)" — for each confirmed item, run `/groove-utilities-memory-promises <text>`. If none found: skip silently.
- After the workflow learning step, prompt for an optional session rating:
  - Ask: "Rate this session (1–5): how well did the compound loop serve you? (enter to skip)"
  - If the user provides a rating: append to `.groove/memory/learned/signals.md` under a table; create the file with a header and table header row if it does not exist
  - Format: `| YYYY-MM-DD | <rating>/5 | <one-line context from the session topic> |`
  - If the user skips: do not mention it again
