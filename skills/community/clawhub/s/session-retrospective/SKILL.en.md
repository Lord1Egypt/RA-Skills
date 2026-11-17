---
name: session-retrospective
slug: yumingtao-session-retrospective
displayName: Session Retrospective
version: 1.0.5
summary: Review the session at its end, log workflow issues as structured JSONL signals; recurrence escalates priority, and one phrase enters fix mode to close the loop.
license: MIT
tags:
  - session review
  - workflow improvement
  - feedback log
  - developer tools
description: >
  A read-only retro of your development session at its end: extract only
  systemic issues that actually happened — wrong answers that needed
  correction, skipped gates, wrong routing, MCP errors, skill/doc gaps,
  multi-turn corrections — and append them as enum-validated JSONL entries
  to a local feedback log: a recurring issue is a rule gap and its priority
  escalates automatically; when nothing went wrong, log one success entry
  and never fabricate. Say "start fixing" to enter Fix Mode: items ordered
  by recurrence and priority, one fix proposal per item, one confirmation
  per item, every fix closing the loop with an append-only audit entry —
  and Fix Mode runs from the log alone, across sessions. Ships a
  zero-dependency validation script (Node 18+) that machine-checks log
  health and recurrence groups after each append and before fixing.
  Complementary to
  report-style retro skills: this skill is the machine-aggregable
  signal-data layer, not a report for humans. Smoke-tested on a real
  session across both the main path and the corrupted-line exception.
  Triggers on "session review", "log session feedback", "retrospective",
  "fix from the feedback log", "start fixing", "回顾一下这个会话",
  "记录会话反馈", "会话复盘", "开始修复".
---

# Session Retrospective

Use this skill to review the current session and append structured feedback
entries to the project's workflow feedback log.

## Quick TOC

- **Session over, want to log now**: What to Analyze → How to Write Feedback (JSONL field table) → Quick Reference
- **Unsure whether something gets logged**: Quick Reference (includes the two "do not log" cases) and Anti-Patterns
- **Something went wrong**: Exception quick reference (SR-E01 ~ SR-E05)
- **Want to fix**: Fix Mode (optional second phase)
- **Want a full example**: references/retrospective-example.en.md

Other sections on demand: Iron Laws / Where feedback goes / When to Use / When NOT to use / Automatic Self-Checks / Rules / Completion Checklist / FAQ.

## Retrospective Iron Laws

Three inviolable rules — breaking any one makes the feedback log worthless:

1. **No fabricating conversation facts.** Every entry must point at a turn that actually happened — the AI really got it wrong, a gate really was skipped, a tool really errored. If you cannot recall it, do not write it; less is better.
2. **Only systemic signals.** An entry's value is that it points at a fixable skill/doc/rule gap. Pure execution slips (a forgotten parameter, a typo) have no fix target — skip them.
3. **No secrets.** No tokens, keys, passwords, internal addresses, or full raw transcripts in notes. The log is read by future improvement decisions, not leaked from.

## Where feedback goes

Default location: `metrics/workflow-feedback.jsonl` in the current project
root. If the project establishes a different log location (check the project
docs or an existing log file), use that. Create the file on first write; it is
append-only local state and never committed to git — if `metrics/` is not
git-ignored on first write, remind the engineer to add it.

## When to Use

- Engineer says "review this session", "log session feedback", or "session review"
- End of a working session on any workflow task
- After resolving a problem that took multiple back-and-forth exchanges
- Engineer says "fix from the feedback log", "process the feedback", or "start fixing" → go straight to [Fix Mode](#fix-mode-optional-second-phase)

## When NOT to use

- The session just started and there is nothing substantive to review → say so; do not generate empty entries
- The whole session was trivial clarifications with no workflow issues → write one `success` entry and stop
- The engineer only wants a conversation summary, not workflow feedback → that is a summarization task, not this skill

## What to Analyze

Review the conversation and identify:

1. **Wrong answers that needed correction** — AI gave incorrect output and the engineer had to correct it
2. **Gate-skipped** — a required workflow phase or confirmation was skipped
3. **Wrong routing** — the AI used the wrong skill, workflow, or approach
4. **MCP errors** — a tool call failed or blocked the workflow
5. **Skill/doc gaps** — repeated clarifications needed because a rule was missing or unclear
6. **Multi-turn corrections** — 2+ exchanges needed to reach a correct answer (merge all turns of one issue into a single entry, noting the turn count)
7. **Successful completions** — worth recording as positive signal

Write one feedback entry per distinct issue. If nothing went wrong, write one `success` entry.

## How to Write Feedback

Append one JSON object per line to the feedback log:

```json
{"timestamp": "2026-11-13T14:30:00+08:00", "platform": "claude", "area": "review", "result": "corrected", "issue_type": "wrong-routing", "priority": "medium", "notes": "<what went wrong and what the correct behavior should be>", "ref": "PR-123"}
```

| Field | Values |
|---|---|
| `timestamp` | ISO-8601 local time |
| `platform` | `claude`, `codex`, `codebuddy`, `cursor`, `trae`, `github-copilot`, `intellij-copilot`, `gemini`, `opencode`, `other` |
| `area` | `planning`, `implementation`, `review`, `git-pr`, `mcp`, `environment`, `docs`, `other` |
| `result` | `success`, `blocked`, `corrected`, `failed` |
| `issue_type` | `none`, `gate-skipped`, `wrong-routing`, `mcp-error`, `skill-sync-missing`, `generated-code-hygiene`, `logging-convention`, `utility-reuse`, `title-format`, `ticket-field`, `auth`, `tool-error`, `other` |
| `priority` | optional: `low`, `medium`, `high` — impact scope × recurrence frequency; omitted means `low`, and `success` entries usually omit it |
| `notes` | what went wrong and what the correct behavior should be |
| `ref` | optional ticket / PR number |

Infer `platform` from the current AI tool unless the engineer specifies otherwise.

**Recurrence marking:** before appending, scan the existing log — the same
`area` + `issue_type` **and substantively the same issue** counts as a
recurrence: append `recurring (occurrence N)` to notes and set `priority` to
at least `medium`. Same enum pair but a substantively different issue is
recorded as a new issue — false escalation pollutes the signal. Recurrence is
the strongest signal of a rule gap. Operational meaning of "substantively the
same issue": the same kind of rule gap acting on the **same target** — the
same skill, the same doc, or the same workflow step; a different target or a
different gap type is a new issue.

## Automatic Self-Checks

A reliable log is built on validation, not good intentions. When Node ≥ 18 is
available, prefer the bundled script for machine validation; without Node,
perform the three checks below entry by entry — equivalent in effect:

- **Pre-append validation**: after assembling entries and before appending, verify every entry of this turn — parses as JSON, platform/area/result/issue_type/priority all pass their enums, notes ≤ 200 characters with no secrets; fix first if any check fails.
- **Post-append confirmation**: after appending, re-read the log and confirm the new line actually landed and parses; if it got corrupted by encoding or truncation, do not rewrite the original line (append-only) — report it and append a correction entry per SR-E05.
- **Fix-mode full-log validation**: when Fix Mode loads the log, first run a line-by-line JSON parse + enum + notes-length check, tally corrupted lines (SR-E04) and recurrence counts per `area` + `issue_type` — those counts drive the fix ordering, not impressions.

**Machine validation script (zero dependencies, Node ≥ 18)**:

```bash
node scripts/validate-feedback.mjs metrics/workflow-feedback.jsonl
```

Performs all three checks in one run: line-by-line JSON parse + field enums +
notes length, **secret scanning** (common key/token patterns are hard errors
— the machine-enforced version of Iron Law 3), **full ISO-8601 validation**
(timezone offset and a real calendar date required), corrupted-line tally,
enum-pair recurrence candidate grouping (the script pairs on `area` +
`issue_type`; **same pair ≠ substantively the same issue** — you confirm per
the operational rule before marking recurring), and a fix-ordering suggestion
by count. Exit code 0 = log healthy (candidate notices do not affect it),
non-zero = hard errors — run it once after each append and once when Fix Mode
loads the log.

## Quick Reference

| Situation | Action |
|---|---|
| AI got it wrong, engineer corrected | One `result=corrected` entry per distinct issue |
| Required phase/confirmation skipped | One `gate-skipped` entry |
| Wrong skill, workflow, or approach used | One `wrong-routing` entry |
| MCP/tool call failed | One `mcp-error` or `tool-error` entry |
| Repeated clarifications from a missing rule | One entry with the gap's `issue_type` |
| 2+ turns to reach a correct answer | Merge into one entry, note the turn count |
| Task completed smoothly | One `success` entry |
| User forgot a parameter, made a typo | **Do not log** (no fix target) |
| User simply complimented the work | **Do not log** (unless it reveals a missing rule) |

## Rules

- Keep `notes` under 200 characters, focused on what should change in the workflow
- Do NOT log trivial clarifications (e.g., missing parameters the user simply forgot to provide)
- Focus on systemic issues: things indicating a skill, doc, or workflow rule needs updating
- Do NOT commit the feedback log — it is append-only local state

## Exception Quick Reference

| Code | Scenario | Action |
|------|----------|--------|
| SR-E01 | Log file/directory not writable | Create the `metrics/` directory on first write; retry once on transient failure; if still unwritable, report the cause and print the entries in the conversation for the engineer to save manually; never write to a different location |
| SR-E02 | No conversation to review (invoked right after session start) | Say "no session history to review"; do not generate empty or fabricated entries |
| SR-E03 | Invoked mid-session | Review only up to the current turn, state "review truncated at current turn", suggest another retrospective at session end; record entries normally |
| SR-E04 | JSONL file exists but some lines are corrupted | Do not rewrite or delete corrupted lines; skip them, report "N corrupted line(s) found" in the summary table, append starting from a new line |
| SR-E05 | Engineer disputes a recorded entry | Do not delete it (append-only); append a correction entry whose notes point at the disputed entry's timestamp |

## Retrospective Anti-Patterns

When you catch yourself doing or thinking these, **stop immediately**:

| What you're doing / thinking | What it really means | Correct action |
|---|---|---|
| Logging "user forgot the parameter" | No fix target | Skip per the Quick Reference |
| Logging a user compliment as feedback | Not a workflow issue | Log only if it reveals a missing rule |
| Writing an essay in notes | Over 200 characters, unusable | One sentence problem + one sentence correct behavior |
| Putting tokens/keys/raw transcripts in notes | Leak risk (Iron Law 3) | Redact before logging |
| One entry per turn of the same issue | Noise that hides the recurrence signal | Merge into one entry with a recurring mark |
| Inventing an entry that "should have happened" | The log loses credibility (Iron Law 1) | Delete it; less is better |

## Retrospective Completion Checklist

Before emitting the summary, confirm each item:

- [ ] Every entry points at a conversation turn that actually happened (traceable, no fabrication)
- [ ] No trivial clarifications, no compliment entries
- [ ] notes ≤ 200 characters and contain no secrets/raw transcripts
- [ ] Multi-turn corrections of one issue merged (recurrence marked where applicable)
- [ ] Each JSON line passes the field enum validation (platform/area/result/issue_type/priority)
- [ ] Log re-read after appending; new line confirmed on disk and passing validation (or `validate-feedback.mjs` exits 0)
- [ ] Feedback log not committed to git (metrics/ ignored or engineer reminded)
- [ ] Doc works standalone: no cross-skill relative paths, in-skill references (references/) verified to exist
- [ ] A `success` entry written when nothing went wrong

## After Writing Feedback

Print a brief summary table:

| Area | Issue Type | Priority | Notes |
|------|-----------|----------|-------|
| ...  | ...       | ...      | ...   |

Then suggest which files in the current project likely need updating based
on the issues found — this is the lower half of the feedback loop: **the log
records the signal; the file suggestions turn it into action**. The engineer
can say "start fixing" to enter Fix Mode and turn those suggestions into
confirmed changes (see below).

A full real-session worked example lives in
[`references/retrospective-example.en.md`](references/retrospective-example.en.md).

## Fix Mode (Optional Second Phase)

The review phase stays read-only + append-to-log; fixing is an explicit
second step. Enter when the engineer says "fix from the feedback log",
"process the feedback", or "start fixing" right after a review.

### Why a Separate Phase

If review mixes with fixing, measurement gets polluted by modification —
the log's credibility depends on the review phase never touching any rule.
Keeping them separate has an extra payoff: **Fix Mode works from the log
alone, no original conversation needed** — it can run in a brand-new session,
across sessions.

### Fix Workflow

1. **Load the log and validate fully**: read the feedback log, run the line-by-line validation from "Automatic Self-Checks" and tally recurrence counts; skip corrupted lines per SR-E04 and report them. `node scripts/validate-feedback.mjs <log-path>` does it in one step (includes fix-ordering suggestion).
2. **Order**: entries marked `recurring` first, then by `priority` (high → medium → low); within the same level, newest first.
3. **Propose per item**: for each entry, present a fix proposal — target file, concrete change, why this change — **one confirmation per item**; never batch-apply. When notes are too terse to ground a proposal, confirm the missing background with the engineer first — never guess.
4. **Execute**: apply the change after the engineer confirms; skip without pushing if not confirmed.
5. **Close the loop**: after each fix, append a `result=success` closure entry whose notes say "fixed: <original entry timestamp>" — the log stays append-only and the fix history stays auditable.

### Fix Guardrails

| Situation | Action |
|---|---|
| Entry has no fix target (`success`, pure observation) | Skip and state so in the summary |
| Single low-priority, non-recurring observation | Do not change rules directly; ask the engineer whether to escalate |
| Fix touches a skill itself or a team-level rule | Must propose a revertible change (e.g., a separate commit) and prompt for review |
| Recurring entries sharing the same `area`+`issue_type` | Check that group's full history and confirm the root cause matches before fixing |

### Fix Completion

Emit a summary: N item(s) fixed (mapped to which log entries), M item(s) skipped and why, and a priority list of remaining items.

## Recommended Pairings

All pairings are optional; this skill has no hard dependency on any of them:

- **Scheduler/automation tools** (platform cron, schedule-style automations): this skill does not self-trigger — reviews run when the engineer or a workflow invokes it at session end; for scheduled retrospectives, have the scheduler call this skill's triggers at fixed times.
- **workflow-skill-designer** (same-repo meta-skill): when the log keeps surfacing "a workflow/skill is missing" gaps, combine it with Fix Mode's confirmed needs to design an orchestrator + phases structured workflow skill.
- **Experience-promotion/memory skills** (the kind that promote general lessons to workspace files like AGENTS.md): this skill's log is their input — they consume structured signals for lesson promotion and continuous improvement; this skill only keeps the signals accurate.
- **Report-style retrospective skills** (structured templates, retros with facilitation guides): when they need traceable turn evidence or signal statistics, this skill's log serves directly as the data source.

## FAQ

**Q: Why not commit the feedback log to git?**
A: It is local working state containing trial-and-error detail; committing would push personal workflow noise into the team repo. Archiving is the engineer's call.

**Q: What if an entry turns out to be wrong?**
A: The log is append-only — never delete. Append a correction entry whose notes point at the disputed entry's timestamp (see SR-E05). A wrong record plus its correction is itself a workflow signal.

**Q: The log keeps growing — what then?**
A: This skill only appends. When size hurts readability, the engineer decides an archiving/cleanup strategy; the recurring marks help identify which patterns have already been absorbed into rules and can be archived.

**Q: Will Fix Mode touch my files without confirmation?**
A: No. It proposes a fix per item and applies one confirmation at a time; every fix appends a closure entry pointing at the original entry's timestamp, keeping the log append-only and auditable. Fix Mode runs from the log alone, across sessions.

**Q: How does this relate to experience-promotion or self-improvement skills?**
A: Complementary: they target continuous learning and promote general lessons to workspace files like AGENTS.md; this skill focuses on structured extraction of session-level workflow issues. Its log output can be consumed directly by them as input.

## Language Support

This skill supports both Chinese and English interaction. Triggers include "session review", "log session feedback", "retrospective", "start fixing", "fix from the feedback log", "回顾一下这个会话", "记录会话反馈", "会话复盘", "开始修复". Write notes in the session's primary language.
