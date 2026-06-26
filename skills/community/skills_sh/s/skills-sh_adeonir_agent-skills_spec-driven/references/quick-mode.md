# Quick Mode

Express lane for small changes. Minimal ceremony, minimal artifacts.

## Contents

- [When to Use](#when-to-use)
- [Workflow](#workflow)
- [Scope Escalation](#scope-escalation)
- [Guidelines](#guidelines)
- [Quick Task Template](#quick-task-template)
- [Error Handling](#error-handling)

## When to Use

- Mechanical changes with zero load-bearing decisions
- Outcome obvious from the description (typo, config swap, named bug + line, rename with no behavior change, dep bump with no API change)
- Scope describable in one sentence
- No ambiguity in requirements

File count is not a criterion — a rename touching 40 files is still
Quick mode if the change is mechanical. Conversely, a 3-file change
that requires a novel decision belongs in Specify.

## Workflow

> Before writing artifacts, ensure `.artifacts` is excluded locally: `grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude`

If the user pauses mid-execution and resumes later, re-read `task.md` before
the next edit — branch, status, or scope may have drifted.

### Step 1: Ensure Structure

Check if `.artifacts/specs/` exists. If not:

```bash
mkdir -p .artifacts/specs
```

### Step 2: Derive Directory Name and Ask About Branch

The directory is `{YYYY-MM-DD}-{slug}`: the creation date (the same value
written to `created` in the task frontmatter) plus the slug. No counter,
no scan. If it already exists (same slug, same day), suffix the slug
(`{slug}-2`).

Generate slug from description:
- "Fix login redirect" -> `fix-login-redirect`

Ask about the branch. Default suggestion is a new branch using the slug. Record the user's choice in `task.md` frontmatter only -- the actual `git switch` happens at Step 7, just before editing.

```text
Branch for this quick task?
1. New branch: fix/{slug} (recommended)
2. Current branch ({current-branch})
3. Other (specify name)
```

Create directory:

```bash
mkdir -p .artifacts/specs/{date}-{slug}
```

### Step 3: Detect Quality Gates

Read `package.json` (or equivalent for the stack):
- Lint script
- Typecheck script
- Test script

Record the actual commands for this project -- they go into the task file and
run in Step 8. If a gate doesn't exist, write `n/a` instead of inventing one.

### Step 4: Create Task File

Use the template (below) as the canonical structure — it wins over any
existing task. Do not read sibling specs in `.artifacts/specs/` for shape
or decisions, and never read `.artifacts/archive/`. The only cross-feature
input is `.artifacts/knowledge.md`.

Create `.artifacts/specs/{date}-{slug}/task.md` with:
- Description of what needs to change
- Files to modify (if known)
- Expected outcome
- `sources:` in frontmatter: durable external references the task points to
  instead of duplicating -- input file paths, tracker ticket IDs or URLs.
  One entry per source; leave `[]` when nothing durable defines the change
- Context: anything settled only in this conversation that implement needs
  -- decisions, content/copy, constraints, clarifications -- or "None" when
  a `sources:` pointer covers it (see Handoff Completeness below)
- Quality Gates filled with commands detected in Step 3
- Branch chosen in Step 2 in frontmatter (creation deferred to Step 7)

**Handoff Completeness:** the task file is the only thing a clean session
sees. Before moving on, confirm: could a fresh session implement this from
`task.md` plus its `sources:` alone? If anything that bears on the change
was settled only in chat, capture it in `## Session Context` now. If it lives in a
durable source the project already tracks, record a `sources:` pointer
instead of duplicating. If it is only in chat, it does not exist.

### Step 5: Load Patterns

Even small changes must follow project patterns.

- If `.artifacts/codebase/{area}.md` cache exists for this area: read it.
  Pay attention to Project Abstractions and Custom Hooks -- use these
  instead of primitives
- If not: follow patterns already present in the files being modified
- Read 2-3 files near the target (siblings in the same directory or
  closest peers in the layer being touched) to extract local patterns
  before editing -- naming, imports, error handling

**Inline micro-research (only if needed):**

Trigger (any of these):

- The task touches a tech the codebase has not used (new library call,
  version bump with API change, unfamiliar API).
- The task writes code or config whose correctness depends on a
  version-sensitive fact of an existing dep or runtime (engine
  constraints, runtime version pins, default behaviors that changed
  across versions).

Skip otherwise.

Path: follow Knowledge Verification Chain Steps 1-3 (codebase -> project
docs -> external docs). Cap at 1-2 queries.

Capture findings inline in `task.md` under a `## Notes` section. Do **not**
write to `.artifacts/research/{topic}.md` -- that cache is for the pipeline's
research phase (Medium and up), not quick mode.

If 1-2 queries insufficient (deeper unknowns surface, multiple unfamiliar
APIs, conflicting docs): stop and escalate via Scope Escalation.

### Step 6: Diagnose Root Cause (defect inputs only)

Skip when the task is a feature addition, config tweak, refactor, or
text-level change.

**Trigger signals (apply when any match):**
- Input is a bug/issue ticket artifact (e.g., from an issue tracker)
- Description contains defect keywords: `fix`, `bug`, `error`, `broken`,
  `regression`, `crash`, `falha`, `quebrou`, `não funciona`, "stopped
  working", "throws", "fails"

**Required before Step 7:**

1. **Reproduce or trace the failure**: confirm the symptom from logs,
   stack trace, repro steps, or a failing test. If you cannot observe
   the failure, stop and ask the user for repro before proceeding.
2. **Locate the defect**: identify the file:line where the wrong
   behavior originates -- not where the symptom surfaces. Follow the
   call chain back to the first incorrect decision.
3. **State the hypothesis**: one sentence describing the actual cause
   ("`<` should be `<=` in expiry check at auth.ts:42", not "auth is
   broken").
4. **Capture in `task.md`** under a new `## Diagnosis` section
   (template below): hypothesis, evidence (file:line + repro signal),
   confidence (high / medium / low).

**Root-fix vs workaround:**

The default is fix at the root. A workaround is acceptable only when:
- The root fix is out of scope for this task (different layer, owned
  by another team, requires migration), AND
- The workaround is explicitly labeled in code with a comment naming
  the underlying defect, AND
- The root defect is captured as a follow-up (`follow_up` in
  frontmatter, or a separate ticket)

Never use `try/catch`, default fallback, or silent recovery to hide a
defect whose root cause has not been diagnosed. Suppressing a symptom
without diagnosis is not a fix.

If confidence is **low** after these steps, stop and escalate via
Scope Escalation -- diagnosis needs depth quick-mode cannot give.

### Design is inline, not a phase

Before Step 7, treat `task.md` as a hypothesis, not a contract. The author may
have assumed one approach without weighing alternatives.

Enumerate silently the 2-4 viable approaches. If only one exists, proceed. If
multiple exist with materially different trade-offs (lock contention, deploy
parity, library surface, reversibility, coupling to internal layouts), surface
them to the user as a short trade-off table before writing code. Let the user
pick — do not present a recommendation dressed as analysis.

This is a precondition to Step 7, not a numbered step. Skipping it and
implementing task-as-written is executing a command, not collaborating on a
design.

Trigger signals (enumerate):
- Task touches infrastructure (DB access, build tooling, CI, deploy)
- Task creates reusable tooling (seeds, fixtures, dev routes, mock servers)
- Task integrates a new dependency or runtime
- Task description names a filesystem path, internal API, or binary format

Skip signals (proceed without enumeration):
- Bug fix with file and line named
- Config value swap
- Rename or text-level refactor with no behavioral change
- Dependency version bump with no API change

### Step 7: Implement

Follow [coding-principles.md](coding-principles.md) during implementation.

Before editing, if `branch:` in task.md frontmatter differs from the current git branch and is not `main`/`master`:

```bash
git switch -c {branch} 2>/dev/null || git switch {branch}
```

Skip when frontmatter says `main`/`master`, when empty, or when current branch already matches. Step 2 records intent -- this is where the branch actually moves.

1. Read task.md in full -- including `## Session Context` for decisions,
   content, and constraints settled earlier -- and follow any `sources:`
   pointer to its durable source before editing. On a clean-session resume
   this is the only context the change has
2. Read relevant files
3. Make the change -- match the patterns loaded in Step 5
4. If Step 6 ran: the change must address the diagnosed root cause,
   not the symptom. A defensive `try/catch`, default fallback, or
   silent recovery is acceptable only when labeled as a workaround per
   the rules in Step 6 (root-fix out of scope, comment naming the
   defect, follow-up captured)

**Source of truth:** reproduce every fact (identifiers, tokens, copy, config
values) from task.md `## Session Context`, a `sources:` pointer, or the
codebase. If a fact is in none of these, STOP and ask — never invent or default it.

### Step 8: Run Quality Gates and Verify

Run in order. Static gates first; static failures short-circuit — do not execute
the change until static gates pass. A typecheck or lint failure means the
runtime behavior is moot; running the script or hitting the endpoint just burns
cycles before you have to come back and fix the static issue anyway.

```text
1. {lint command} --fix       (static)
2. {typecheck command}        (static)
3. {test command}             (static, if any)
4. Execute the change end-to-end — run the script, open the UI, hit the endpoint
5. Inspect result against task.md "Expected Outcome"
```

Skip gates marked `n/a` in the task file. Fix errors before proceeding. If the
same gate fails 3 times, stop and ask the user how to proceed -- never loop
indefinitely.

### Step 9: Save Discoveries (default: save)

Append non-obvious findings to `.artifacts/knowledge.md` without asking. Real
gotchas, verified patterns, and environmental quirks all qualify.

SKIP only when:
- Already in knowledge.md (check first)
- Restatement of project conventions already documented elsewhere
- Change was purely mechanical (formatting, rename, dep bump with no behavior shift)

Targets:
- **Gotchas** -> `## Gotchas`
- **Normative conventions the codebase follows** -> `## Conventions`

Format per [knowledge.md](knowledge.md). No prompt — the next design or
implement flow reads these on load.

### Step 10: Update Task File

Set in `task.md` frontmatter:
- `status: done`
- `completed: {YYYY-MM-DD}`
- `patterns_discovered`: list of new patterns surfaced (or empty)
- `follow_up`: side effects, related issues, improvements noticed but not addressed (or empty)

### Step 11: Commit

Build the commit message per [commit-conventions.md](commit-conventions.md) and
commit (hooks run normally).

### Step 12: Archive

After the commit lands, move the task out of the live spec directory so a
later spec never forages it:

```bash
mv .artifacts/specs/{date}-{slug} .artifacts/archive/{date}-{slug}
```

If `.artifacts/archive/{date}-{slug}/` already exists, suffix the slug
(`{slug}-2`). The archive is never read during discovery.

## Scope Escalation

If during implementation the change turns out to be bigger than expected:

| Signal | Action |
|--------|--------|
| Canonical pattern needs to be reapplied (not mechanical) | Stop. Suggest `specify` with Medium scope. |
| Architectural decision needed (novel to the codebase) | Stop. Suggest `specify` with Large scope. |
| Requirements unclear | Stop. Suggest `specify` to clarify first. |
| Dependencies on other features | Stop. Suggest `specify` to map dependencies. |

When escalating, the quick task file serves as input for the specify phase.

## Guidelines

**DO:**
- Keep it simple -- quick mode exists to avoid ceremony for trivial changes
- Treat `task.md` as a hypothesis; surface alternatives before implementing infra/tooling tasks
- Run static gates before executing the change
- Save discoveries by default; skip only when criteria above apply
- Escalate to specify when in doubt about scope
- Treat the task as transitory: archived to `.artifacts/archive/` once committed (Step 12)
- For defect inputs: diagnose before implementing -- hypothesis + evidence + confidence in `## Diagnosis` (Step 6)
- For defect inputs: fix at the root, or label the workaround with the underlying defect

**DON'T:**
- Skip quality gates for small changes (contrasts: run static gates before executing)
- Implement task-as-written without enumerating alternatives when trigger signals fire (contrasts: treat task.md as hypothesis)
- Ask permission to record gotchas (contrasts: save by default)
- Force quick mode when scope is uncertain (contrasts: escalate when in doubt)
- Suppress a symptom with `try/catch`, default fallback, or silent recovery before diagnosing the cause (contrasts: Step 6 Diagnose, then root-fix)

## Quick Task Template

ALWAYS use this exact template structure:

````markdown
---
name: {{slug}}
status: pending
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
branch: {{branch-name or main}}
sources: []
completed: {{YYYY-MM-DD or empty}}
patterns_discovered: {{list or empty}}
follow_up: {{list or empty}}
---

# Quick Task: {{Description}}

## What

{{One-sentence description of the change}}

{{#if defect}}
## Diagnosis

- **Hypothesis:** {{one-sentence root cause — e.g., "expiry check uses `<` instead of `<=` at auth.ts:42"}}
- **Evidence:** {{file:line + repro signal — log excerpt, failing test, stack trace, observed behavior}}
- **Confidence:** {{high | medium | low}}
- **Fix type:** {{root-fix | workaround}}
- **Workaround justification (if applicable):** {{why root-fix is out of scope + follow-up reference}}
{{/if}}

## Files

- {{file to modify, if known}}

## Expected Outcome

{{What should be different after the change}}

## Session Context

{{Anything settled in this conversation that a clean session would need and
that no `sources:` pointer covers -- decisions made, content/copy to
implement, constraints, clarifications. Always present: write "None" when a
`sources:` entry covers it. A missing section is an omission; an explicit
"None" asserts nothing was lost.}}

- {{captured item, or "None"}}

## Quality Gates

Run after the change, before marking done:

- {{lint command}}
- {{typecheck command}}
- {{test command}}
````

## Error Handling

- No .artifacts/: Create it
- Scope too large: Escalate to specify
- Static gate fails: Fix before running the change end-to-end
- Same gate fails 3 times: Stop and ask the user
- task.md modified mid-session: Re-read before the next edit
