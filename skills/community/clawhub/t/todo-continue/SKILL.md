---
name: todo-continue
description: Execute the next workable node of the TODO.md task tree end to end, driven by each task's status. Use for /todo-continue [--plan] [--lane <name> | --all-lanes [--seq]] [--worktree] [--delegate] [--merge]. Creates the node's git branch first, then marks it in progress, builds with red-green-refactor, runs Done when plus regression, completes it in the branch, merges it into its parent, and drains a finished root to CHANGELOG.md as one entry. Works without git, with a warning. Completes at most one node per invocation, except lane runs, where one subagent per lane works one root of that lane.
argument-hint: "[--plan] [--lane <name> | --all-lanes [--seq]] [--worktree] [--delegate] [--merge]"
---

# /todo-continue

First load the `todo` core skill and read `reference/git-flow.md` and `reference/verification.md` from its folder (`reference/lanes.md` too with a lane flag). If the core is not a skill, read `../todo/SKILL.md` and those files from `../todo/reference/`.

Complete at most one node per invocation (lane runs excepted). Flags, all optional; an invalid combination is reported and nothing runs:
- `--plan`: stop for approval after reading, before writing code (step 6). Not with a lane flag.
- `--lane <name>`: only roots of that lane, in order. `--all-lanes [--seq]`: one subagent per lane, in parallel (`--seq`: one after another); see `reference/lanes.md`. Not together, and not with `--worktree`.
- `--worktree`: work in a separate worktree; the main checkout is never switched (`reference/git-flow.md`, "--worktree").
- `--delegate`: steps 6-9 run in a subagent on the model the node's tier maps to (core "Model routing"); you keep the other steps and rerun the verify commands yourself. Without a subagent tool or a `Models:` line, say so and work in this thread.
- `--merge`: when a **root** finishes, also merge it into the base. Without it the commands are printed.

## Steps

The order of every node is the core's "Lifecycle by status".

1. **Git mode and invariants.** Check git and run the invariant check (core). If it fails only on the active node's `State:` line, show the corrected line and ask; on I5, apply the core's repair; otherwise report and stop.
2. **Select by status.**
   - **Interrupted merge** (on a `todo/` branch; core "Interrupted work comes first"): finish it as step 10 item 3 (the merge only), then lint (the lint script, else the core invariant check), report and stop. No tests here; the parent's integration step runs them.
   - **Interrupted drain** (a root branch whose uncommitted `CHANGELOG.md` holds its entry): make the drain commit (10.4.3 d), go on at 10.4.4, report and stop. A drained root branch not yet merged into the base is reported with its merge commands (with `--merge`: go to 10.4.4).
   - **A `[/]` node:** resume it on its branch (or worktree); check `git status` and `git diff --stat`. Uncommitted changes that fit its task line are its earlier work, committed at step 10; anything else: stop and ask, never revert or commit it. Skip steps 3-5 and go on where `next:` says: `read docs` or `plan proposed` → 6, `build` → 7, `drain` → 10.4, other or missing → 6. Without a baseline in `State:`, the regression must be fully green with no test deleted, skipped or weakened.
   - **Otherwise** the first **workable** `[ ]` node (core "Which node is next"); claimed trees are skipped with the resume hint, `[!]` nodes (also those `[!]` only on their own branch) are skipped, `[x]` nodes are never touched. A node with `next: decompose` is broken down, not built: on the base for an unclaimed tree (as step 3 "Where to start"), with `../todo-add/SKILL.md` steps 7-8 (over 120 lines: write nothing, say so, stop); show the children, write them after the user confirms (on a `todo/` branch commit `chore(backlog): decompose <ID>`), and stop. Nothing workable: list what blocks progress and stop.
3. **Ready check** (new nodes only), in this order:
   - Lint clean; the `Ref:` path, if any, exists; tree clean by the git-flow definition (otherwise stop and ask).
   - **Where to start** (git mode). A node in an unclaimed tree (no branch in its root's `State:` in `git show <base>:TODO.md`) starts from the base: on a `todo/` branch first commit pending backlog edits there (`chore(backlog): pending edits <IDs>`, by path), then `git switch <base>`. A root missing from the committed base is workable when it is an uncommitted root on the base in the main checkout's `TODO.md`; carry those backlog edits into the claim. Otherwise skip it and say it must be added on the base. Every other node stays on its tree's branch.
   - **Base dependency.** A `Depends:` satisfied only by the base's CHANGELOG: first `git merge <base>` into the start branch (`Merge <base> into <its ID>`). This merge only brings in the base and stays even if the baseline is then red; nothing else changes.
   - **Baseline.** Run the regression command (`reference/verification.md`, protocol step 6) on the start branch: the nearest ancestor branch that exists (the base for an unclaimed tree); for a leaf that already has its own branch, the branch after its `from`; for a parent's integration step, its own branch.
     - Green: note the pass count. No tests (none run): `baseline none`.
     - Red: a `FIX` node whose `Done when` runs at least one failing test may start with `baseline red: <ids>`. Otherwise change nothing more, report "baseline red" with the command and its failing tests, suggest `/todo-add "fix the failing baseline: <failing test ids>" --type fix --priority P0` (ids as the runner prints them), and stop.
4. **Branch first** (git mode). Follow `reference/git-flow.md`: in an unclaimed tree, root branch → tree claim commit → fast-forward of the base (**do not go on until it succeeded**) → missing ancestor branches → the node's branch; otherwise only the missing branches. No git: skip.
5. **Start.** On the node's branch set `[/]` and replace `State:` with `attempts 0/3; baseline <n> passing; branch <name> from <branch it was created from>; next: read docs` (or `baseline none` / `red: …`). No git: `attempts 0/3; baseline …; no git; files: <a root's rolled-up files, else ->; docs: <rolled-up docs, if any>; next: read docs`. Commit `chore(backlog): start <ID>` with any pending backlog edits. Nothing but backlog files changes before this.
6. **Read before write.** Read the `Ref:` doc and the README/doc sections that govern the area, then only the code the node needs. A missing `Ref:` or a doc that contradicts the task line: stop and ask.
   - **Plan** (`--plan`, or `next: plan proposed`). If a plan was proposed, show it (the body of the newest commit whose subject is exactly `chore(backlog): plan <ID>`; none or no git: print a new one) and ask "approve the plan? (yes / change: …)": yes sets `next: build` and goes on; a change is committed the same way (`--allow-empty` if `TODO.md` is unchanged) and stops. Otherwise print a plan of at most 10 lines (files, approach, risks), set `next: plan proposed`, commit it as `chore(backlog): plan <ID>` with the plan as the body, and **stop**.
7. **Build.**
   - **Resume:** code and tests already exist: skip red and go to review (its findings are fixed like any others).
   - **Red** (new `FIX`/`FEAT` leaf): write the tests and see them fail for the expected reason; quote the first failing assertion or missing-symbol error. Already passing: stop and ask (offer `/todo-update <ID> --status drop` or a tighter `Done when`). `TASK` refactors get characterization tests.
   - **Green:** implement only the task line. Adjacent findings go to the report, not into the code or TODO.md. No new `TODO`/`FIXME`. No git: list touched files in `State: files:`.
   - **Refactor** with tests green. **Integration step** (a parent): `reference/verification.md`, protocol step 8; no feature code.
8. **Review** the whole change (`git diff`; no git: each file in `State: files:`), spec compliance first, then quality:
   - **Spec:** every hunk traces to the task line and nothing it asks for is missing; the tests assert the `Done when` criteria (not vacuous, nothing weakened) and carry the ID in the test name, or in a docstring or comment when `Done when` fixes the name.
   - **Quality:** no debug output, commented-out code, new `TODO`/`FIXME`, unrelated reformatting, generated files, secrets or `.env` in the diff or in backlog text you wrote.
   - With a subagent tool, a fresh-context reviewer does both in one call (at the node's tier or higher with a `Models:` line), given only the task lines, the `Ref` path and the diff, and returns a verdict for each, `ok` or `fail`, with its findings; it never edits files or runs tests. Fix what is valid (at most 2 rounds; findings still valid then block the node, "Test failures"). Without one, review yourself.
9. **Verify** in full and unnarrowed: the `Done when` commands, then the regression; update `State:` whenever a cycle changes one of its items (`attempts`, `hyp:`, `baseline`, `next:`). All gates must pass:
   - Done when exited 0 **and** ran tests ("0 tests", "no tests found", "collected 0 items", "NO TESTS RAN" fail), the command does not mask failures (`|| true`, `; exit 0`) and every test path it names exists; `todo-verify.sh` (core, optional) checks these. Regression green, no fewer passing tests than the baseline, none deleted or skipped.
   - Each item of the project's Definition of Done, if any.
   - RTM (only if one exists; `reference/rtm.md`): when the node proves a requirement row, record its `Done when` test paths or ids in that row's Verification cell. It is committed with the node (step 10.2); no RTM, no step.
   - Documentation drift (below).
10. **Complete, in this order.**
    1. **Non-root node:** no git: first copy its `files:`/`docs:` into the root's `State:`. Set `[x]`, delete `State:`, lint. (A root is never `[x]`; item 4 drains it.)
    2. Commit the node's files and any changed `TODO.md` by path (skip if nothing changed): `<type>(<scope>): <title>` with body `Refs: <ID>`, `Red: <first failing assertion>` (leaves that started red), `Reviewed: subagent, spec <ok|fail> quality <ok|fail>, <n> findings fixed` (the first round's verdicts) or `Reviewed: self, <n> findings fixed`, and `Checked: <command>` for each command in `Done when` or the regression that is not a known test, lint, typecheck or build runner (the lint's W3 warning) and that you judged safe (`reference/git-flow.md`, "Commits").
    3. **Non-root node:** switch to the parent's branch, `git merge --no-ff` with `Merge <ID> into <PARENT-ID>`, `git branch -d` the child (worktrees: git-flow "--worktree"). Report and stop; the node stays `[x]` until its root drains.
    4. **Root** (a leaf root, or its integration step just passed):
       1. Refresh from the base (`reference/git-flow.md`); if that brought changes, rerun `Done when` and the regression. For a `high` root, or one touching security, data migration, concurrency or a public interface, offer the optional root review once (`reference/review.md`, "Root review"; read it only then).
       2. **Last gate:** if `.todo/check.sh` exists, read it: only the shebang, comments, `set -eu`, `cd`, the lint line, an optional `.todo/todo-replay.sh` line and test commands that pass command safety (`reference/verification.md`), and read each `.todo/` script it calls the same way; otherwise show what fails and ask. Run it (in a worktree without `.todo/`, run its lines there instead: the lint via the main checkout's `.todo/todo-lint.sh`, then the tests). Red blocks the root.
       3. Drain: (a) insert one entry as the core's "CHANGELOG entry" says; (b) delete the subtree from TODO.md; (c) lint; (d) commit both files as `chore(backlog): drain <ID>`, body `Refs: <ID>` (and `Includes: <IDs>` with descendants).
       4. With `--merge`, merge into the base as git-flow "Root" says; otherwise print those commands. Never push.
       No git: items 2 and 3 (a)-(c).
11. **Report**, short (also on an early stop: which step and why): ID and title, commands and results (regression against the baseline; say "not run" when the path ran no tests), files changed, branch and commit, `children done/total` for a parent root, the checked-out branch, and the merge commands for a root without `--merge`. Then adjacent problems as `/todo-add "<description>" --from <ID>` commands to run on the base (never add them yourself), the next workable node (or "none"), and a suggestion to clear context.

## Test failures

- Diagnose first: reproduce, read the first failing assertion, write one hypothesis in `State:` (`hyp:`), make the smallest change that tests it, rerun.
- At most **3** attempts across sessions (`State:` counter). An attempt is a failed verification run after implementing started; the first red run is not one.
- **Escalation** (core "Model routing"): with a `Models:` line and work in a subagent (`--delegate`, lanes), each failed attempt raises the next one a tier (`low` → `mid` → `high`), recorded as `tier:`. Without routing, say in the report that a stronger model might help.
- You may change code and the tests this node creates, within the task line.
- Forbidden: editing `Done when`, deleting, skipping or weakening tests, `|| true`, loosened assertions, a narrower command.
- A failure outside the node (a flaky test, a regression beyond the task line), and the third failed attempt (list each hypothesis), block the node: `[!]`, `State:` replaced by a `Blocked:` line in the core format (secrets redacted; no git: a root's `files:`/`docs:` go into the action part as `(files: …; docs: …)`), committed with the node's changed files as `chore(backlog): block <ID>`; stop. Roots block the same way.
- Run commands only under the safety rules in `reference/verification.md`.

## Documentation drift

- If the implementation must deviate from the `Ref` doc, stop and let the user choose: change the code, or update the doc in this node.
- Only when the node changed a public interface (a command, flag, endpoint, config key or exported symbol, added, renamed, removed or with a changed meaning), read `reference/doc-drift.md` and follow it. A node that changed no interface skips this, and drift that already existed for other reasons never blocks it.
- Report README setup or test instructions that disagree with the commands that passed.
- TODO.md never duplicates docs; spec-like text goes to `docs/` with a `Ref:`.
