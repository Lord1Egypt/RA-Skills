---
name: task
description: Universal task dispatcher. Start, route, and execute any task through the development workflow (Steps 0-9). Invoke on every task — /task <description>, /task #<issue>, or /task to start fresh.
version: 1.0.0
---

# /task

## Surface Routing

Before starting, pick the right tool for the job:

| Activity | Tool | Why |
|---|---|---|
| Architecture planning | Claude Code /plan | Opus, 1M context |
| Feature implementation | Claude Code | Hooks, subagents, worktrees |
| Quick single-file fix | VS Code Claude ext | Faster for small scope |
| DevOps / terminal | Codex CLI | Strong at terminal tasks |
| Background refactor | Codex Cloud | Fire-and-forget PR |
| Code review | GitHub Actions | Async, no session cost |
| Test writing | subagent: test-writer (CC) / inline (Codex) | Isolated context |
| Documentation | subagent: doc-writer (CC) / inline (Codex) | Cheap, focused |
| Research | Claude.ai Projects | Persistent, web search |

## Cross-Tool Notes

This skill uses Claude Code features. Portable equivalents for Codex/Cursor:

| Claude Code | Codex / Cursor |
|---|---|
| `TaskCreate` / `TaskUpdate` | Markdown checklist in `.branch-context.md` |
| `EnterWorktree` | Use absolute paths + `git -C` for all ops |
| `/orient`, `/brainstorming`, etc. | Read `.agents/skills/<name>/SKILL.md` and follow manually |
| Subagent dispatch (`implementer`, `test-writer`) | Execute sequentially in main session |
| Agent Teams | Not supported — use sequential work |
| `/review`, `/plan-review` | Read `.agents/skills/review/SKILL.md` and follow manually |

## Args

| Invocation | Behavior |
|---|---|
| `/task <description>` | Start new task |
| `/task #<issue>` | Start from GitHub issue |
| `/task` | Start new task — ask what to work on |

## Copilot Mode

In copilot mode (`operating-mode.md`), the workflow is a **menu, not a pipeline**:
- Present available steps. Execute what the human asks. Don't enforce order.
- Worktree-first is relaxed — primary worktree writes are allowed.
- Invariants below still apply except where `operating-mode.md` explicitly overrides.
- If the human says "follow the workflow," run step-by-step but pause for approval at each transition.

## Invariants

These rules are agent-interpreted guidance, not machine-enforced. They cannot be skipped regardless of task type or scope unless noted. Omission is not permission — any step not explicitly listed as skippable is required.

```starlark
REQUIRE task_list.all_steps_populated BEFORE step_1
REQUIRE worktree BEFORE code
REQUIRE orient.complete BEFORE plan
REQUIRE tests BEFORE implementation  # TDD: RED → GREEN → REFACTOR
REQUIRE review(plan).pass BEFORE build UNLESS scope == one_sentence OR task_type IN [fix, hotfix]
REQUIRE validate.pass BEFORE review(build)
REQUIRE review(build).pass BEFORE archive
REQUIRE task_list.no_pending_steps BEFORE ship
REQUIRE branch.base IS CURRENT(origin/main) UNLESS stacking
REQUIRE plan.commit BEFORE review(plan)
REQUIRE batch.commit BEFORE batch.next

WHEN ci.down:
  USE local_merge AT step_8
WHEN files_touched MATCH [AGENTS.md, config.toml, sync.sh, skills]:
  REQUIRE codex_specialist IN review_panel
```

## Steps

Persist significant decisions to `.branch-context.md` during Steps 3-5 — not just at reflect/bail time.

### Step 0 — Bootstrap

Create a task list with ALL steps for the detected path. Every step is a task — no exceptions. The task list is the enforcement mechanism: pending tasks are visible proof of unfinished required work.

- **Claude Code**: `TaskCreate` one task per step. Populate all steps upfront (adjust after orient detects path). Mark each `in_progress` before starting, `completed` when done.
- **Codex/Cursor**: add a markdown checklist to `.branch-context.md` with all steps.

### Step 1 — Orient

Invoke `/orient` with args (Codex: read `.agents/skills/orient/SKILL.md`). It produces:
- **task_type**: feat / fix / chore / docs / test / refactor
- **scope**: can the entire diff be described in one sentence? Yes → short path (skip Steps 3-4). No → full path. Note: short description ≠ small change — "update all deps" sounds short but may touch dozens of files.

After orient completes, populate the task list with remaining steps for the detected path:
- **Hotfix** (`fix/*`, `hotfix/*`): ALWAYS skip Steps 3-4 regardless of scope. No plan, no plan review — go directly to Step 5.
- **One-sentence scope** (any task type): skip Steps 3-4.
- **Everything else**: full path (Steps 0-9).

### Step 2 — Isolate

Invoke `/isolate` with the branch name from Step 1 (Codex: read `.agents/skills/isolate/SKILL.md`). It handles freshness (fetch origin main), worktree creation from origin/main, directory selection, gitignore safety, dependency install, and baseline test verification. If already in a worktree, it freshens the branch instead of creating a new one.

**Path discipline:** `cd` does not persist between Claude Code Bash calls. After worktree creation, use absolute paths for all file operations and `git -C <absolute-path>` for git commands. Never rely on `cd` carrying over.

### Step 3 — Plan

**Hotfix (`fix/*`, `hotfix/*`):** SKIP — proceed to Step 5. No architect agent, no plan file. Add a one-paragraph diagnosis to the commit message instead. Log: "Step 3 — Plan: SKIPPED (hotfix fast path)."

**One-sentence scope:** SKIP — proceed to Step 5. Log: "Step 3 — Plan: SKIPPED (one-sentence scope)."

**Full scope:**

**3a. Brainstorm.** Invoke `/brainstorming` with the task description. One round — refine the idea, confirm constraints, explore 2-3 approaches.

**3b. Write plan.** Write a plan to `ai-workspace/plans/<name>.md` using the template at `ai-workspace/plans/TEMPLATE.md`. Fill all template fields including:
- Branch, created date, status
- Threat model (advisory or adversarial)
- Scope ceiling
- Task description and scope
- Steps with checkboxes (include files to create/modify and testing strategy)
- Confidence scaffold (recommended for adversarial threat models)

Do NOT review the plan here — that's Step 4.

### Step 4 — Review Plan

**No plan (hotfix or one-sentence scope):** SKIP — proceed to Step 5.

**Has plan:**

Run `/review` against the plan file (Codex: read `.agents/skills/review/SKILL.md` and follow manually).
- Auto-assemble the plan review panel:
  - Always: `technical-editor`
  - Code architecture: add `architect-reviewer`
  - AGENTS.md / config.toml / sync.sh / skills: add `codex-specialist`
  - Auth / credentials / permissions: add `security-auditor`
  - UI / component / CSS: add `ui-designer`
- Gate: P2 (fix P0-P2, record P3+)
- Cap: 3 rounds

On APPROVE: proceed to Step 5.
On ESCALATE after 3 rounds: stop and present unresolved findings to human.

### Step 5 — Build

Invoke `/build` (Codex: read `.agents/skills/build/SKILL.md`). It handles plan parsing, batch-sequential/task-parallel subagent dispatch, TDD, inter-batch regression checks, and the validate hard gate. For hotfixes or one-sentence scope, it implements directly with TDD. Step 6 cannot begin until `/build` reports validate passing.

**Hotfix protocol** (applies when task_type is `fix` or `hotfix`):
- MUST fix the defect only — nothing else (minimal change principle).
- MUST NOT refactor during a hotfix; create a separate branch for cleanup.
- MUST test the specific failing case first (RED), then fix (GREEN).
- MUST document the root cause in the commit message body.
- MUST NOT modify agent profiles without explicit approval.

### Step 6 — Review Build

Run `/review` against the changed files (`git diff main...HEAD`) (Codex: read `.agents/skills/review/SKILL.md` and follow manually).
- Auto-assemble the **code** review panel (differs from Step 4's plan panel):
  - Always: `code-reviewer`
  - Code architecture: add `architect-reviewer`
  - AGENTS.md / config.toml / sync.sh / skills: add `codex-specialist`
  - Auth / credentials / permissions: add `security-auditor`
  - UI / component / CSS: add `design-reviewer`
- Gate: P2
- Cap: 3 rounds

On APPROVE: proceed to Step 7.
On ESCALATE: stop and present unresolved findings to human.

### Step 7 — Archive

**Has plan:**

Invoke `/archive` (Codex: fill Outcomes & Learnings in plan file, rename to `.done.md`). It fills Outcomes & Learnings in the plan file and renames to `.done.md`.

**No plan (hotfix / one-sentence):**

Ensure root cause or change rationale is documented in the commit message body. No plan file to archive.

### Step 8 — Ship

Invoke `/ship` (Codex: read `.agents/skills/ship/SKILL.md`). It handles validation, option presentation (PR + auto-merge vs local merge vs keep vs discard), CI up/down routing, shallow-clone merge for the local path, and worktree cleanup. CI status comes from conversation context — if the user said CI is down, /ship uses the local merge path.

When files touched include AGENTS.md, config.toml, sync.sh, or skills → `codex-specialist` must be in the review panel (enforced at Step 6).

### Step 9 — Reflect

Invoke `/reflect` (Codex: read `.agents/skills/reflect/SKILL.md`). It handles:
- Reading `.branch-context.md` for session learnings
- Writing to `MEMORY.md` on main
- Filing follow-up issues if needed
- Cleaning up branch artifacts

## Definition of Done

- [ ] Dependencies install (`pnpm install`)
- [ ] All tests pass (`pnpm test:all`)
- [ ] Types check (`pnpm typecheck`)
- [ ] Biome clean (`pnpm lint`)
- [ ] Formatter clean (`pnpm format:check`)
- [ ] Code reviewed (PR: by another agent; local merge: `/review` panel)
- [ ] Plan file has Outcomes & Learnings filled in
- [ ] PR/commit description written with context for reviewer
- [ ] Branch merged to primary (via PR or /local-merge)
- [ ] Key learnings consolidated with `/reflect` and pushed to primary

## Bail

Invoke `/bail` at any step to abort cleanly. It handles: learnings capture to `.branch-context.md`, issue update, PR close if open, worktree cleanup. Bail replaces Step 9 (Reflect) — it captures learnings itself. Clean up any open task list items.
