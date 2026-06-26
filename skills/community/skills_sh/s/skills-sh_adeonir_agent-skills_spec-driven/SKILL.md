---
name: spec-driven
description: >-
  Specification-driven feature development with auto-sized depth.
  Produces spec.md, design.md, and tasks.md artifacts with requirements
  traceability and an audit phase tied to Goals and Success Criteria.
  Verify runs inside implement per task -- never as a user phase.
  Use when planning a feature, specing a feature, turning a PRD into a
  spec, breaking a change into tasks or user stories, designing a feature,
  implementing a named user story or task, auditing goals at a commit
  boundary or before a PR, or discussing how to build a feature. Not for
  diagnosing unknown bugs, authoring standalone PRD/RFC/ADR/Design
  Doc documents, PR/commit mechanics, or PM backlog tracking.
argument-hint: "[t-N | us-N | --all] [--commit]"
---

# Spec-Driven Development

Structured development workflow with adaptive depth.

## Triggers

### Feature-level (auto-sized)

- **New feature** ("create new feature", "specify feature", "from PRD",
  "modify feature") → [specify.md](references/specify.md)
- **Discuss / capture context** ("discuss feature", "how should this
  work") → [discuss.md](references/discuss.md)
- **Feature design** ("design this feature", "designing a feature",
  "plan feature") → [design.md](references/design.md)
- **Research technology** ("cache research", "research topic") →
  [research.md](references/research.md)
- **Tasks** ("create tasks") → [tasks.md](references/tasks.md)
- **Implement** ("implement task", "execute task", "implement user story
  US-1", "implement task T-1"; add `--commit` to auto-commit each boundary,
  `--all` auto-commits implicitly) → [implement.md](references/implement.md)
- **Audit** ("audit feature", "validate goals", "audit goals and
  success criteria") → [audit.md](references/audit.md)
- **Manual testing** ("manual testing", "test manually") →
  [validate.md](references/validate.md)
- **Quick mode** ("quick fix", "quick task", "small change", "bug
  fix") → [quick-mode.md](references/quick-mode.md)
- **Status overview** ("list features", "show status") →
  [status-specs.md](references/status-specs.md)

### Methodological refs (loaded by other refs)

- **Verification (internal check)** →
  [verify.md](references/verify.md) (loaded by `implement.md` Step 5-After)
- **Subagent dispatch protocol** →
  [phases.md](references/phases.md)
- **Codebase exploration** →
  [codebase-exploration.md](references/codebase-exploration.md)
- **Coding principles** →
  [coding-principles.md](references/coding-principles.md)
- **Status workflow** ("when to update status") →
  [status-workflow.md](references/status-workflow.md)
- **Knowledge format** (decisions, gotchas, conventions) →
  [knowledge.md](references/knowledge.md)
- **Auto-sizing scope assessment** →
  [auto-sizing.md](references/auto-sizing.md) (loaded by `specify.md` Steps 1 and 9)
- **Discovery topics** →
  [discovery.md](references/discovery.md) (loaded by `specify.md` Step 7)
- **Code-correctness analysis** →
  [code-correctness.md](references/code-correctness.md) (loaded by
  `verify.md` Step 5)

## Workflow

```text
specify → design → tasks → implement → audit → done
                                     ^           ^
                                     |           |__ per-story commit OR pre-PR
                                     |__ verify runs inside implement per task
```

Adaptive by depth, not by skipping: Specify and Implement always run. Design
and Tasks run at every scope above Small -- light at Medium, full at
Large/Complex. Small routes to quick-mode and skips the pipeline. Verify is
internal to implement. Audit runs at the commit boundary (per-story or
end-of-spec), always before PR.

## Knowledge Verification Chain

For all technical decisions, follow in order:

1. Codebase
2. Project docs
3. External docs lookup (documentation service or vendored references)
4. Web search
5. Flag or ask

Never skip to step 5 if steps 1-4 are available. **Never assume or
fabricate** — follow the chain or say "I don't know."

Record the source that grounded each decision and the scope the premise holds
under — a decision with no codebase, docs, or ADR anchor is a red flag.

## Artifact Authority and Lifecycle

Every artifact's structure is canonical in the matching reference (each
ref carries its template inline, 1:1). Load the reference before reading
any existing artifact in `.artifacts/` -- existing files are context,
not structural reference. Template wins on divergence.

A spec lives in `.artifacts/specs/{date}-{name}/` while it is built and
moves to `.artifacts/archive/` once `done` (quick mode: once committed).
Discovery never forages siblings or `archive/` for shape or decisions --
a pile of old specs out-votes the template and leaks superseded decisions
into the current one. The only cross-feature input a new spec draws on is
`.artifacts/knowledge.md`. Reading `archive/` is reserved for locating a
*named* spec to re-audit or UAT.

## Guidelines

- Separate content by purpose: spec = WHAT, design = HOW, tasks = WHEN
- Follow status flow: `draft → ready → in-progress → to-review → done`
- Name spec dirs `{date}-{name}` — date-keyed, no counters
- Reuse research cache across features (`.artifacts/research/`)
- Auto-size depth based on complexity — skip phases that add no value
- Run audit at the commit boundary, before any PR

## Anti-Pattern: Forced Full Depth

Running every scope at full depth is process tax. Auto-sizing scales depth,
not phases: small fixes go through `quick-mode.md`; medium scopes run a *light*
design and *flat* tasks; large/complex scopes run the full
design and full breakdown. Forcing the heavy data-model
work and dependency graph onto a canonical reapplication is the tax to avoid --
respect the depth the sizing assigned.

## Anti-Pattern: Deferred Verification

Implementing all tasks first and verifying at the end loses traceability
between implementation and acceptance criteria. Verify runs internally
after every task or range -- never a final phase, never user-invoked.
Failed verification reverts checked AC and reopens the relevant tasks.

## Anti-Pattern: PR Before Audit

Opening a PR with `status: to-review` and running `audit` afterwards
puts Goals and Success Criteria validation on the wrong side of the
merge gate. Audit runs first at the commit boundary -- per-story or
end-of-spec -- and only then does the commit/PR proceed.

## Anti-Pattern: Knowledge Skipping

Jumping to "I'll guess based on dependency name" or "let me web-search
that" without exhausting steps 1-4 of the Knowledge Verification Chain
produces fabricated patterns that don't match the codebase. Read the
codebase first, then project docs, then external docs, then web. Only
flag or ask after the chain is exhausted.

## Anti-Pattern: Training Memory as Ground Truth

Treating trained-in knowledge as authoritative for version-sensitive
facts -- engine constraints, defaults, API surfaces, deprecations,
runtime requirements -- silently bypasses the chain. Verify against the
project's declared dep metadata, lockfile, and the dep's current
documentation. Training cutoffs lag dep behavior.
