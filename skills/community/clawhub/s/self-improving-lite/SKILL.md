---
name: self-improving-lite
description: "Capture errors, corrections, and better approaches as short learnings, and promote broadly useful ones to persistent workspace files. Use when a command fails, the user corrects you, you find a better approach, or before starting a major task."
version: "1.0.0"
---

# Self-Improving Lite

Turn mistakes and discoveries into durable improvements. Log events as short
learnings, review them at natural breakpoints, and promote the broadly useful
ones to the workspace files that every session loads.

## When to Use

- A command, tool, or API call fails or returns an unexpected result.
- The user corrects you or rejects your approach.
- You find a better approach than the one you used or planned.
- Before a major task: review existing learnings relevant to the task.

Do not log ordinary one-off instructions, hypotheticals, or context-specific
details that will not matter later.

## Learning Log

Keep learnings in `.learnings/LEARNINGS.md` in the workspace root. Create it
if missing:

```bash
mkdir -p .learnings
[ -f .learnings/LEARNINGS.md ] || printf "# Learnings\n\nCorrections, insights, and better approaches captured during work.\n\n---\n" > .learnings/LEARNINGS.md
```

Never overwrite existing entries; append only. Do not log secrets, tokens,
private keys, or full file contents; use short sanitized summaries.

Entry format:

```markdown
## LRN-YYYYMMDD-NNN
- Category: correction | insight | better_approach
- Context: what you were doing (one line)
- Observation: what happened (one or two lines)
- Rule: the reusable lesson, one sentence, scoped
- Status: pending
```

Example:

```markdown
## LRN-20261113-001
- Category: better_approach
- Context: Reviewed a colleague's API design before implementing it.
- Observation: Asking two questions up front avoided a rewrite of the endpoint schema.
- Rule: Before implementing a colleague's interface design, confirm the error semantics first.
- Status: pending
```

## Promoting to Persistent Workspace Files

When a learning is broadly useful — it applies across tasks, prevents a
recurring mistake, or records knowledge any teammate (human or AI) should
have — promote it so every future session inherits it.

Promotion targets:

| Learning type | Target file |
|---------------|-------------|
| Workspace conventions and collaboration rules | Project instruction file (`.hermes.md` in Hermes workspaces, `AGENTS.md` elsewhere) |
| Behavioral patterns and communication style | `SOUL.md` |
| Tool capabilities and gotchas | `TOOLS.md` |

How to promote:

1. Check the learning is supported by evidence (a resolved incident, a
   verified result), not a guess.
2. Append the rule to the target file as one or two lines, with a source link
   back to the learning entry. Create the target file if it does not exist;
   never overwrite or rewrite existing content.
3. Mark the learning entry `Status: promoted` with the target file and date.

Promoted rules are short and actionable, for example:

```markdown
- Before implementing a colleague's interface design, confirm error semantics first. Source: .learnings/LEARNINGS.md#LRN-20261113-001
```

Keep each promoted rule self-contained and scoped. If a rule stops being
useful, annotate it as outdated rather than deleting history.

## Sharing Learnings with Teammates

Useful learnings are worth sharing, not just storing. When you collaborate
with other agents or teammates:

- Offer a short sanitized summary of the relevant learning and its source
  path, not raw transcripts or logs.
- When a learning would help a teammate's current work, offer it directly;
  avoid dumping the whole log.
- When a teammate shares a learning with you, log it and evaluate it for
  promotion like one of your own.

Only share in trusted environments, and never include secrets or private file
contents in what you send.

## Maintenance Basics

- Review relevant learnings at natural breakpoints: before a major task,
  after completing a feature, after fixing a bug.
- Resolve entries when fixed (`Status: resolved` with a one-line note).
- Do not delete old entries; they are the evidence behind promoted rules.
- Keep the log useful: promote or resolve entries rather than letting them
  accumulate indefinitely.
