# PMA Workflow

## Table of Contents

- [Hard Rules](#hard-rules)
- [Three-Phase Workflow](#three-phase-workflow)
- [Claim-Before-Work](#claim-before-work)
- [Sync Rules](#sync-rules)
- [Dependency Freshness](#dependency-freshness)
- [Session Checklist](#session-checklist)

## Hard Rules

1. Repository docs, task files, plan files, code comments, commit messages, PR text, and other remote-visible metadata stay in English by default.
2. Read before write: inspect call chains, config, tests, and changelog context before editing logic.
3. Make only the minimal requested change.
4. Do not use plan mode. Plans live only in `docs/plan/`.
5. Do not implement before explicit confirmation such as `proceed`.
6. Use English filenames only.
7. When the goal is unclear, stop and ask.
8. Trace root causes instead of patching symptoms.
9. Output only what changes the next decision.
10. When introducing or upgrading a dependency, default to the latest stable version verified at the registry — see *Dependency Freshness* below.

## Three-Phase Workflow

### Phase 1: Investigation

1. Trace upstream and downstream call chains, symbol references, and types.
2. Search related code, config, tests, migrations, and docs.
3. Read the tail of `docs/changelog.md`.
4. Find or create the matching task in `docs/task/index.md` and claim it with `[-]`.

Non-trivial task rule:

- If the change touches `>=3` files or crosses modules, create `docs/plan/PLAN-NNN.md` and write findings into the context section.

### Phase 2: Proposal

Output these items, then stop:

- current state
- proposal
- risks
- scope
- alternatives when multiple approaches exist

For non-trivial tasks:

- complete the remaining sections in `PLAN-NNN.md`
- append one line to `docs/plan/index.md` with `[ ]`
- wait for approval and address annotations before implementation

### Phase 3: Implement -> Verify -> Record

Only after approval:

1. If a plan exists, set the plan index marker to `[-]` and detail status to `implementing`.
2. Implement only the approved scope.
3. Run focused self-verification.
4. Set the task index marker to `[x]` and task detail status to `completed`.
5. If a plan exists, set the plan index marker to `[x]` and plan detail status to `completed`.
6. Update changelog when needed.

## Claim-Before-Work

Before writing implementation code:

1. Read `docs/task/index.md` and inspect `[-]` items.
2. If another agent owns the in-progress task, skip it.
3. Claim atomically:
   - update task index `[ ] -> [-]`
   - update task detail `status -> in_progress`
   - set `owner`
   - sync tool state if task tools exist
4. Start implementation only after the claim is fully written.

On completion:

- set task index `[-] -> [x]`
- set task detail `status -> completed`
- sync tool state if task tools exist

On close:

- set task index to `[~]`
- set task detail `status -> closed`
- record the reason

## Sync Rules

- Task status updates are immediate.
- Primary source of truth is `docs/task/` and `docs/plan/`.
- If task tools exist, keep tool state in sync with file state.
- If task tools are unavailable, continue with file-only sync and state that explicitly.

## Dependency Freshness

When introducing or upgrading a dependency, default to the **latest stable version**. Snippets copied from tutorials, blog posts, prior PRs, or LLM recall routinely carry outdated versions; that drift compounds across security audits, ecosystem compatibility, and breaking-change exposure.

### Rule

Before adding any new dependency or accepting any version number that came from somewhere other than the registry:

1. **Verify the latest stable at the registry** (commands per stack — see the stack skill's baseline):
   - crates.io / npmjs.com / pkg.go.dev are the sources of truth; the LLM is not.
2. **Confirm current API and breaking changes via official docs.** Use Context7 (`mcp__plugin_context7_context7__query-docs`) or the vendor site for libraries you are not already using at the latest version. Training-data recall lags real releases — treat it as a hint, not a fact.
3. **Pin to non-latest only with a recorded reason.** MSRV constraint, peer-dep incompatibility, blocked upstream — write the justification inline next to the dependency entry (`// PINNED: <reason> until <condition>`) or in `docs/decisions/`.
4. **Separate routine version bumps from feature work.** A `chore(deps): bump X to Y` commit or PR is reviewable; bundling it into a feature diff hides regressions.

### When to escalate

If the latest stable version conflicts with the project's runtime / MSRV / peer-dep constraints, surface the trade-off in the Phase 2 proposal — do not silently downgrade.

### Anti-patterns

- Copy-pasting `"some-lib": "^1.2.3"` from a tutorial without checking whether 1.x is still maintained.
- Reusing a version from another repo in the same org without re-verifying.
- Accepting a version the LLM "knows" without registry confirmation.
- Bumping a dependency inside an unrelated feature commit.

## Session Checklist

1. Session start: read `docs/task/index.md`, active task details, and `docs/plan/index.md`.
2. New task: create detail file first, then append the index line.
3. Before work: complete claim-before-work.
4. Session end: verify status files and update index header date.
