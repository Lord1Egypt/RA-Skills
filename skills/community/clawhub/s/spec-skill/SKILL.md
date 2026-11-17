---
name: spec
description: >-
  Gated requirements, design and tasks spec under docs/plans/, with hash-pinned
  approval receipts and a decision ledger a fresh session can resume from.
  Invoke with /spec (Claude Code) or $spec (Codex).
disable-model-invocation: true
metadata:
  openclaw:
    homepage: https://preuve.ai
---

# Spec-driven change

Requirements, design, tasks. A risk-tiered number of approval gates, a decision
ledger that survives compaction, and every task traced to the requirement that
justifies it.

Before writing anything:

- **Read the overlay.** The consuming repo's `AGENTS.md`, or a file it names,
  lists that repo's tier-3 surfaces, deploy step, hard stops and reviewers. The
  method here is project-agnostic; the overlay is where the risk lives.
- **Read `references/example-spec.md`.** One small tier-3 spec in full. It pins
  the exact shapes, so copy them rather than inferring them from the rules here.
- **Run the validator**, before presenting any gate and again before execution:

  ```bash
  node <this-skill-dir>/scripts/check-spec.mjs docs/plans/<date>-<slug>
  ```

  It recomputes approval hashes, cascades a void approval downstream, and
  reports uncovered criteria, orphan citations, missing `Verify:` lines,
  invented npm scripts and unproven non-regression assertions. Exit 1 means
  fix it before the gate.

## Layout

```
docs/plans/<YYYY-MM-DD>-<slug>/
  requirements.md
  design.md          # feature and bug only, never quick
  tasks.md
  .spec-state.json
```

Older flat single-file plans in `docs/plans/` stay as they are.

## Tier first

Say which tier and why in your first message. Three stops is the top tier, not
the default, and file count is not the signal: four locale files are not riskier
than one line in a checkout path.

- **Three gates**, each document approved separately. Money, access control,
  entitlements, irreversible writes, schema migrations, production data, or the
  user asks for an implementation review. The overlay names the concrete
  surfaces. Only here are the three questions independent: right behaviour,
  safe architecture, safe decomposition.
- **Two gates**, requirements then design; tasks generate and execute without a
  further stop. A new surface, a pipeline change, a cross-subsystem refactor, an
  API route that is not money or auth.
- **One gate**, criteria and approach together. `quick` specs and obvious
  multi-file work. Most of what gets asked for.

At every tier: write one gated file, stop, report the path and what it decided,
and wait. Ungated files may follow in the same turn.

## Spec types

- **feature**: all three files.
- **bug**: `requirements.md` is the investigation: symptoms, reproduction, root
  cause, expected behaviour, what must not change. `tasks.md` is the fix plus
  the regression test that would have caught it.
- **quick**: short `requirements.md` and `tasks.md`, no `design.md`.

## Decisions

Ask only when the answer changes the output, 1 to 3 questions at a time, and
only what the repo cannot tell you. Every real either/or is a structured choice
(`AskUserQuestion` on Claude Code; on Codex a short numbered list, then stop):
one question per decision, your recommended option first and labelled
`(Recommended)`, the trade-off in each option's description. Mirror the
question into the ledger before the gate, and the answer with its `why` in the
same turn it is answered.

## Approval is a receipt

A file's existence says it was written, not approved: an agent interrupted
between writing `design.md` and review leaves a directory indistinguishable from
an approved one. So the phase is derived from the files present, and approval
is a SHA-256 receipt in the ledger, written when the user approves:

```
shasum -a 256 docs/plans/<date>-<slug>/requirements.md
```

Check receipts with the validator, never by eye: a mismatch voids that approval
and every one below it, and the cascade is the part an eyeball skips. Re-open
the voided gates.

## `.spec-state.json`

The decision ledger. Update it in the same turn as whatever it records: a
question asked, an answer, a phase change. Full example in the reference. No
`phase` field: phase is derived from the files.

- `type`: `feature`, `bug` or `quick`. `tier`: 1, 2 or 3, as declared.
- `approved`: one `{file, sha256, at}` per approved document. Drop the entry
  when its approval is voided; never edit a hash to clear a mismatch.
- `decisions[]`: `id` stable and carrying the same question forever (when the
  meaning changes, retire the id with its `why` and add a new one);
  `recommended` mandatory while open; `answer` null while open and kept forever
  once answered; `why` one sentence written at the answer, the reason the file
  beats the chat log.
- `blocking`: one sentence for a human on what you are waiting for. Never
  branch on it.
- `closure`: `implemented`, `merged`, `deployed` or `verified`; absent while
  open.
- `context.template`: the module the work is modelled on. There is almost
  always one.

Update it without narrating it. Show it when the user asks what state a spec is
in: hidden governing state is worse than noisy state.

## requirements.md

Numbered requirements, each a user story then criteria numbered `1.1`, `1.2` so
tasks can cite them. Criteria in EARS form:

```
WHEN <event> THE SYSTEM SHALL <response>
IF <precondition> THEN THE SYSTEM SHALL <response>
```

Observable, not vague: "SHALL return within 2s", not "should be fast".
Behaviour, not implementation: "SHALL cache frequently accessed data", not
"SHALL use Redis". Always an explicit **Out of scope**, and **Open questions**
that is empty or mirrored into the ledger.

For money, access-control, entitlement or shared-contract work, add
**non-regression assertions**: `WHEN <x> THE SYSTEM SHALL CONTINUE TO <y>`, each
with a `Proven by:` line naming a test that exists (verified) or that a task
creates. An assertion with no test behind it is a wish, and a bug spec without
any is incomplete.

### Analyze before the gate

Pass over the finished file once and report what you found, not that you
checked. A contradiction costs a sentence here and a phase in `design.md`.

- **Contradictions**: two criteria that cannot both hold. Name both numbers.
- **Ambiguity**: a criterion two competent readers would build differently.
  Rewrite it, or make it a decision.
- **Gaps**: empty state, external call failing, unauthenticated caller,
  concurrent writers, the unpaid tier, a non-default locale. Systems fail
  silently exactly there.
- **Untestable**: no observable outcome.
- **Unstated coupling**: holds only if another subsystem behaves a certain way.
  Name it, and say whether you verified it.

A few lines for `quick`. For money, access control, entitlements or migrations
it is mandatory, and finding nothing is said out loud.

## design.md

Overview and how it satisfies each requirement, then architecture, data model,
interfaces, error handling, testing strategy. Mermaid only where it helps.

Every non-obvious choice gets a decision block (context, options with
trade-offs, decision, rationale) and the same decision in the ledger. When the
choice is the user's (taste, product direction, spend, anything the repo cannot
decide), ask it at the design gate with options mirroring the block's, instead
of writing it as settled.

Name the co-artifacts here, not at the end: the scoped rules, docs and sibling
surfaces that move with the code. Say plainly when merging does not ship the
change, and name the apply step from the overlay.

## tasks.md

Ordered checkboxes, each one focused step building on the last, with `Files:`,
`Verify:` and `_Requirements:`. Shape in the reference.

- Coding tasks only. "Discuss with the user" is a gate.
- Every criterion cited by at least one task. Report the coverage count.
- A task without a `Verify:` line is not a task. The command exists in
  `package.json` or a CI job the overlay names; when nothing exercises the
  criterion, the task is to write the test.
- A foundation task implementing no user-visible criterion is
  `_Requirements: enabler_`. A fake citation makes the coverage count lie; an
  honest gap does not.
- Sequence foundation first, or risk first when a piece might not work at all,
  and say which in one line at the top.
- A tier-3 spec ships as one PR per task group, each small enough for the
  review bots to cover in full, never one PR for the whole spec.

## Resuming

Read in this order: `.spec-state.json`, `ls` the dir, `requirements.md` and
`design.md` in full, then `tasks.md`. The constraints, exclusions and error
semantics live upstream; a task list read alone is how an executor confidently
builds the wrong thing.

Run the validator and report the receipt state. Then sync: check the codebase
for tasks another session already finished, tick them, say which. An unchecked
box is not proof the work is undone.

**One session per spec.** There is no merge model for the checkboxes or the
ledger. Parallel work means separate specs with non-overlapping files.

## Execution

Work through unchecked tasks in order: tick the box, run that task's `Verify:`,
continue. Stop when all are ticked or on a real blocker, and summarize what
landed and what remains.

Sequentially: `tasks.md` carries no dependency metadata, so guessing at
independence puts two dispatches in one file. When the user asks for
parallelism, dispatch a subagent per task with the task text, `Files:` and
`Verify:` as the whole brief, only for tasks whose `Files:` provably do not
intersect, and merge in the main thread.

Unattended: stop and report after 10 consecutive tasks without a human look;
stop on the first failing verification rather than stacking work behind a red
check; leave tool approvals with the user.

Hard stops always: never mutate production data or secrets, never restart a
shared local service the user owns, plus whatever the overlay adds. Pushing
follows the overlay's rule; with no overlay, confirm before each push.

## Closing: "shipped" is four states

Written is nowhere near live, and merging may not deploy the thing users hit.
Record `closure` and skip nothing:

| `closure`     | Means                                                           |
| ------------- | --------------------------------------------------------------- |
| `implemented` | Tasks ticked, verifications green, local only.                  |
| `merged`      | On the default branch.                                          |
| `deployed`    | The production apply step from the overlay has run, named here. |
| `verified`    | Observed working in production.                                 |

**Archive only at `deployed` or later.** Archiving at `implemented` leaves a
spec that looks finished over a system that never changed. When the deploy is
the user's to run, stop at `merged` and say so.

At closure: report the co-artifact sweep unprompted, follow the overlay's
specialist-review policy for the surfaces you touched, and write the decisions
with their reasoning to the project's durable memory when it has one, retiring
any fact a new decision supersedes.

## Lifecycle: a shipped spec is an archive, not a contract

A spec that disagrees with the code is worse than no spec, because readers still
trust it. Three genres:

| Genre           | Where                                  | Rule                                                                      |
| --------------- | -------------------------------------- | ------------------------------------------------------------------------- |
| In flight       | `docs/plans/<date>-<slug>/`            | Live. Amend freely, gates apply.                                          |
| Archived        | same dir, frozen apart from the header | What was intended on that date. Stale by design, never revised.           |
| Living contract | project rules, `docs/`, agent docs     | Present tense, current behaviour, updated in the same commit as the code. |

On archiving: head each file with `> Archived <date>. Intent as of that date,
not current behaviour. Current: <the rule that owns this area now>.`, then
migrate anything load-bearing out (an env-flag table, an ordering invariant, a
gate order, a money path) into the scoped rule and link it. If nothing is
load-bearing, say so.

An abandoned spec stays, with `requirements.md` headed
`> Abandoned <date>. <one sentence why.>`. The reason it died stops the idea
being re-proposed next quarter.

## Backward flow

Design proving a requirement wrong is normal. It flows backwards instead of
being patched around. Stop, say which document is now wrong and why in one
sentence, then:

1. **Void the receipts first**, before touching prose, so an interruption
   cannot leave a stale approval over changed text.
2. Amend, keeping requirement numbers stable: renumbering breaks every
   citation. When a number's meaning changes, retire it, add a new one, and fix
   the citing tasks.
3. Record the reversal as a decision with its `why`. An approach tried and
   abandoned is the one thing a later session cannot reconstruct.
4. Re-derive downstream and re-open the voided gates. An amended requirement
   means `design.md` gets a look, not a rubber stamp.
5. Re-run the validator.
