---
name: wdp-prd-en
description: Use when the user runs /wdp-prd-en to discuss/record new requirements, view the backlog, or dispatch confirmed requirements to background subagents for parallel implementation. English variant of wdp-prd-zh. Subcommands: new, list, update, confirm, dispatch, accept
disable-model-invocation: true
---

# wdp-prd-en — Requirements Management

A superpowers-based requirements manager that **decouples discussion from implementation**. Brainstorm new requirements into cards at any time; confirmed ones are implemented in parallel by background subagents without blocking the main session.

## When to Use
- Discuss/record a new requirement (not implemented immediately) → `/wdp-prd-new`
- View the backlog / scheduling state → `/wdp-prd` or `/wdp-prd-list`
- Confirm a requirement as dispatchable → `/wdp-prd-confirm <id>`
- Dispatch implementation → `/wdp-prd-dispatch`
- Accept a completed requirement → `/wdp-prd-accept <id>`
- Edit a card → `/wdp-prd-update <id>`

## Storage Model
- Global root: `~/.wdp/prd/` (override with the `PRD_ROOT` environment variable).
- Per-project subdirectory: `<PRD_ROOT>/<project-slug>/`, containing:
  - `backlog/R-###.md` requirement cards
  - `execution-plan.md` scheduling view
  - `plans/` implementation-plan archive
- Bridge: a `.wdp-prd` file in the project root whose content is the absolute path of that project's global root (i.e. `<PRD_ROOT>/<slug>/`). Read it before every command operation.

### Initialization
If `<cwd>/.wdp-prd` does not exist:
1. Ask for the project name (slug, lowercase hyphenated).
2. Create `<PRD_ROOT>/<slug>/` (with `backlog/`, `plans/`) and an empty `execution-plan.md`, and create `docs/superpowers/specs/` inside the project.
3. Write `.wdp-prd` containing the absolute path of the global root.
4. Report that initialization is complete.

## State Machine
`draft → confirmed → in-progress → needs-review → accepted → done`
Also: `blocked` (unmet dependency / subagent failure), `cancelled`.

## Scheduling Rules
Compute a status report over all cards, with two rules (no topological sort in the MVP):
1. A dependency in `depends_on` that is still not `done` → `⏳ waiting for R-00X` (dependencies that are `cancelled` count as satisfied and do not block).
2. An entry in `conflicts_with` that is `in-progress` → `⚠ conflicts with R-00X(dev in progress); wait for it or let the user decide`.

Before computing, check the `depends_on` relations: if there is a cycle, report it (R-003↔R-004), mark the involved cards `blocked`, and do not dispatch; if a dependency id does not exist, report `dependency R-999 does not exist; check depends_on` and do not dispatch. Cards with a missing dependency go into the ⏳ blocked list with `dependency missing` noted in parentheses.

The parentheses in the blocking hint show the dependency card's actual current state (e.g. confirmed / in-progress / cancelled).

**Immediately dispatchable** = status==confirmed + all dependencies satisfied + no conflict with in-progress + in-progress count < concurrency cap.
**Concurrency cap** defaults to 2, configurable via the `PRD_MAX_CONCURRENT` environment variable. When exceeded, report `concurrency cap reached; accept what's in hand first`.
**Same-batch constraint**: the batch the user picks must be pairwise non-conflicting; if they pick a pair that lists each other in `conflicts_with`, force picking only one; each batch is at most `PRD_MAX_CONCURRENT − current in-progress` cards.

Report format:
```
▶ ready to dispatch in parallel   [R-001, R-002]
⏳ blocked by dependency           R-005 → wait for R-002(dev in progress)
⚠ conflicts with in-progress task R-003 ↔ R-004(dev in progress)
```

## execution-plan.md
Rewritten by Claude after every status change / dispatch / acceptance (based on the **current state of all cards**: needs-review/accepted/done cards naturally leave the in-progress / ready / blocked / conflict lists and no longer appear):
````markdown
# Execution Plan (auto-generated, do not edit by hand)
Updated: YYYY-MM-DD
in-progress: [R-001, R-002]
ready: []
blocked: R-005 → wait for R-002
conflicts: []
````

## Commands

### /wdp-prd — Main entry
1. Read all cards, output a backlog summary table (id/title/status/priority/dependencies).
2. Compute and output the current scheduling status report per the Scheduling Rules (ready / blocked by dependency / conflicts / concurrency-cap hint; format as above).
3. Prompt the available `/wdp-prd-*` commands.

### /wdp-prd-list — List
Output a backlog summary table sorted by priority from high to low, then by created ascending within the same priority. If there are no cards, state that explicitly.

### /wdp-prd-update <id> — Edit a card
1. Locate the card (if missing, report an error and list recent ids).
2. Ask which fields to change (status/priority/depends_on/conflicts_with/title).
3. Validate values: status must be in the state-machine set; priority must be high/medium/low.
4. Update the fields, set `updated` to today, keep `created` unchanged.
5. Rewrite `execution-plan.md` (if affected).

### /wdp-prd-confirm <id> — Confirm a requirement
1. The card exists and status==draft; otherwise report an error stating the current status.
2. On confirmation status→confirmed, `updated` is refreshed.
3. Rewrite `execution-plan.md`.

### /wdp-prd-dispatch — Dispatch
1. Produce the scheduling status report (rules in Scheduling Rules).
2. The user picks a batch to dispatch now (pairwise non-conflicting; when the concurrency cap is exceeded, prompt to accept first).
3. Spawn one **background subagent** per requirement, executed in a **git-worktree-isolated branch**:
   `superpowers:writing-plans` → `superpowers:test-driven-development` → development → `superpowers:verification-before-completion`;
   at dispatch time, move the card → in-progress, refresh `updated`, and rewrite `execution-plan.md` (so the card counts as in-progress for the subagent's entire run);
   when the subagent produces an implementation plan, archive it to `<pointer>/plans/<id>.md`.
4. The subagent returns a report: which files it changed, which tests it ran, results, leftover issues.
5. When the subagent finishes: move the card → needs-review, and prompt the user to run `/wdp-prd-accept <id>`.

**Non-git fallback**: when no git repository is detected, clearly warn that worktree isolation is unavailable, ask whether to still dispatch serially or abandon; never continue silently.

### /wdp-prd-accept <id> — Accept
1. The card status==needs-review, otherwise prompt to dispatch first.
2. Merge the subagent's worktree branch into the current working branch.
3. Run the **full integration test suite**; on failure → leave the card as needs-review, record the failure reason, and prompt to fix or roll back.
4. Run a **code review** (reuse `superpowers:requesting-code-review`).
5. Present the change summary + review verdict to the user → user confirms.
6. On confirmation → status→accepted→done, fill in the acceptance record, rewrite `execution-plan.md`.
7. After acceptance, remove the merged worktree (reuse the cleanup flow of `superpowers:using-git-worktrees`).

### /wdp-prd-new — Discuss and create a requirement
1. Confirm this project's `.wdp-prd` pointer exists (if missing, go through Initialization first).
2. Invoke `superpowers:brainstorming` to discuss the requirement with the user, producing a design document (saved to the project's `docs/superpowers/specs/`).
3. Create a new card `backlog/R-###.md` per `references/card-template.md`:
   - id auto-incremented (current max + 1); status=draft; priority set by the user or default medium.
   - created/updated = today.
   - Write the design-document path into the `Design Doc` section.
4. Rewrite `execution-plan.md`.

## Requirement Cards
See `references/card-template.md` for the format. Copy the template when creating.

## Error Handling
| Situation | Handling |
|-----------|----------|
| Non-git repository | Worktree isolation unavailable → warn clearly, fall back to serial/non-isolated (see dispatch flow) |
| Subagent failure | Card → blocked, report the reason, update execution-plan |
| Dependency cycle | Detect and report the cycle, do not dispatch |
| Missing dependency | Report the dependency id does not exist, prompt to check depends_on |
| Same-batch conflict | Force picking only one |
| Review failed | Card stays needs-review, record the verdict |
| User did not confirm | Card stays needs-review |
| No Agent tool | Fall back to a manual guided flow |
| `.wdp-prd` missing | Trigger initialization |

## Verification
Dry-run all scenarios (S1–S6) per `references/test-scenarios.md`. The skill passes only when every Expected is met.
