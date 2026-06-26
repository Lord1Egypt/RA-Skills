---
name: taku-compact
description: >
  Create a recoverable active-work brief for context-heavy coding, design,
  debugging, review, research, or handoff sessions. Multi-mode context-control
  habit with resume, handoff, debug, review, design, and research policies.
---

# Taku Compact - Context-Control Habit

Use `/taku-compact` to compress active work into a recoverable brief. It is a
bonus utility skill, not a seventh Taku phase.

Rule labels: `[IRON LAW]` means a non-negotiable correctness constraint. `[GUIDANCE]` means a strong default that may adapt when context justifies it.

Compact preserves current task state. Reflect preserves long-term learnings.
Never write `.taku/learnings` from this skill. You may list
`reflect_candidates`, but `/taku-reflect` is the only path that can promote them
after user approval. A `reflect_candidates` entry is not a recorded learning and
must never be worded as one.

## Host Boundary

This skill does not control the host transcript, context window, message
slicing, archive behavior, or clear behavior. It creates a handoff brief from
available evidence. Do not claim that tool calls, tool results, or transcript
events were compacted.

If a future host exposes transcript ranges, record them as retrieval hints only
after verifying they are available. Otherwise use file, diff, command, log,
prior-brief, and current-session anchors.

## Mode Selection

Accept an explicit mode when the user provides one:

| Mode | Use When | Preserve First |
|------|----------|----------------|
| `resume` | The same agent or user will continue later | next step, open todos, blockers, recent decisions |
| `handoff` | Another agent or session needs to continue | background, scope, decisions, files, verification, next step |
| `debug` | Investigation or failed checks are in progress | symptoms, reproduction, evidence, failed hypotheses, next probe |
| `review` | A dirty diff or delivery review is next | diff intent, risk areas, test coverage, scope drift, blockers |
| `design` | Think/Plan/product discussion needs preserving | constraints, tradeoffs, confirmed decisions, open questions |
| `research` | Source reading or technical exploration needs preserving | sources, findings, confidence, unresolved questions, followups |

If no mode is provided, infer it from the request and current state. Record
`mode_selection_reason` in the brief. Prefer `handoff` when multiple modes fit
and the user asked for general compacting.

## State Scan Contract

[IRON LAW] Run an evidence-first state scan before writing the brief. Do not summarize from
memory first.

### 1. Durable Sources

Read or inspect these when present:

- `DESIGN.md`
- `PLAN.md`
- `README.md`
- `AGENTS.md`
- `CLAUDE.md`
- `.taku/context/current.md`
- `.taku/context/compact-*.md`
- `.taku/learnings/*.jsonl` as approved context only

Only include stable-layer details that affect the active task. If a durable
source is missing or irrelevant, record that in `source_coverage`; do not treat
it as a blocker.

### 2. Repo Evidence

Inspect git and file-system evidence when a repo is available:

- `git status --short`
- `git diff --stat`
- `git diff --name-only`
- relevant `git diff` hunks for changed files
- `git log -n 3 --oneline`

Changed files must come from git or the file system, not guesswork. A clean diff
means no durable code changes were observed; it does not mean no progress
occurred.

### 3. Session-Visible State

Treat visible conversation and tool outputs as first-class state:

- recent user decisions and corrections
- explicit constraints and preferences
- command results visible in this session
- tool output, agent findings, review findings, and debug observations
- design/research progress that has not been written to project files

Mark conversation-derived claims as `user` and command/tool-output claims as
`tool`. Do not present them as file-backed project truth unless they were
written to a durable artifact.

### 4. Source Tags and Confidence

Every important claim must carry one of these source categories:

- `file`: project file, Taku context file, approved learning, or file-system inspection
- `git`: status, diff, or commit history
- `tool`: command output or tool result visible in the session
- `user`: explicit user statement, correction, or approval
- `inferred`: agent synthesis from other evidence
- `unknown`: unavailable or unverified evidence

Do not say tests passed unless actual command output or explicit user-provided
evidence shows that.

Include `state_confidence` for goal, changed files, verification, and next step
using `high`, `medium`, `low`, or `unknown`.

## Brief Output

Use `references/compact-brief.md` as the local brief scaffold. Fill every applicable
field. Remove irrelevant mode-specific sections, but keep `unknowns`,
`retrieval_hints`, and `completeness_check`.

Default persistence:

1. Create `.taku/context/` if needed.
2. Write the latest brief to `.taku/context/current.md`.
3. Write the same brief to `.taku/context/compact-YYYYMMDD-HHMMSS.md`.

If files cannot or should not be written in the current host, output the brief in
chat and mark `persistence: chat_only`.

## Mode-Specific Requirements

### Resume

Include:

- the first concrete next action
- unresolved blockers
- open todos
- recent session context needed to avoid rework

### Handoff

Include:

- background and current scope
- decisions and user constraints
- changed files or confirmation that none were observed
- verification state
- exact restart instructions for the next agent

### Debug

Include:

- observed symptoms
- reproduction steps
- evidence collected
- failed hypotheses and why they failed
- next probe

Never describe a fix as verified without evidence.

### Review

Include:

- diff intent
- changed files
- risk areas
- test coverage observed
- scope drift check against `PLAN.md` or user intent when available
- pre-ship blockers

### Design

Include:

- user constraints
- options considered
- tradeoffs
- confirmed decisions
- open questions
- recommended next planning step

### Research

Include:

- sources inspected
- key findings
- confidence by finding
- unresolved questions
- follow-up searches or files to inspect

## Completeness Check

Before finishing, verify the brief includes:

- user constraints or `unknown`
- open todos or `none_observed`
- failed attempts or `none_observed`
- verification state with evidence or `not_established`
- changed files with sources or `none_observed`
- retrieval hints
- unknowns
- mode-specific required fields
- source tags for important claims

If a required item is missing, fix the brief before presenting it.

## Non-Goals

- Do not edit implementation files.
- Do not update `PLAN.md` status.
- Do not run formatters or codegen.
- Do not commit, push, or open a PR.
- Do not fix bugs.
- Do not write `.taku/learnings`.
- Do not add archive or clear semantics.
