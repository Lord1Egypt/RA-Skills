---
name: todo
description: Core rules for the todo-* skills (todo-init, todo-plan, todo-add, todo-continue, todo-update, todo-status, todo-report, todo-release) - the task tree in TODO.md, compact task format, complexity levels and model routing, IDs, git flow with a no-git fallback, invariants, Definition of Done and hard guardrails. Load this before running any todo-* command or when editing a TODO.md in the `# Active Backlog` task-tree format. Invoked directly as /todo it only prints the command list and a read-only invariant check.
---

# todo (core)

The repository is a closed-loop state machine built from files that already exist. Nothing else stores state.

| Layer | File(s) | Role | Write policy |
|---|---|---|---|
| Requirements | `README.md`, `docs/*.md` | Ground truth: contracts, specs, setup, long plans | Read-mostly. Edited under "Documentation drift" in `todo-continue`; plan docs (`docs/plans/`) by `todo-init`/`todo-plan`/`todo-add`/`todo-update`; the README `Tests:` line by `todo-init` on a yes; the optional RTM (`reference/rtm.md`) by `todo-plan`/`todo-add`/`todo-continue` only when it already exists; `docs/status.html` by `todo-report` |
| Active queue | `TODO.md` | One task tree. A tracker of work items, not a place for design | Edited only by the todo-* skills |
| Validation | Source code + test suites | Ground truth for "done" | Changed only for the task at hand |
| Archive | `CHANGELOG.md` | Permanent, append-only (Keep a Changelog + Conventional Commits) | Only `## [Unreleased]` (on release: renamed to the version, a new empty one above it, and the link lines at the end) is touched, by a root drain and the confirmed `/todo-release`; `todo-init` creates the file or adds a missing `[Unreleased]` |
| Checks (optional) | `.todo/check.sh`, `.todo/todo-lint.sh`, CI job | Lint + tests, run by CI, a pre-push hook and `/todo-continue` | `check.sh` written by `/todo-init --ci` on a yes; `todo-lint.sh` copied in by the user; committed by the user |
| Version store | git | Branch or worktree per task. Nothing reaches the base branch unverified | See "Git mode" |

Prefer native file tools (Read/Edit/Write) for file edits; however you edit, change only the intended lines and keep the file's final newline. Use the shell only for `git`, test and `Done when` commands, the optional scripts, and the file commands a skill names (`cp`, `chmod`, `mkdir -p`, `date`, `grep`, `cmp`, `mv`, and `rm` of a skill's own temporary file).

**Backlog files** are `TODO.md`, `CHANGELOG.md`, `docs/plans/PROJECT.md`, `docs/plans/<ROOT-ID>-*.md` named by a `Ref:`, and the README `Tests:` and `Base:` lines written by a todo-* skill. README.md is staged by a backlog commit only while `git diff README.md` adds exactly those lines, optionally after a blank line; README edits a node makes under "Documentation drift" are that node's files and are committed with it; any other README change is the user's: it counts for the clean-tree check and is never staged by a backlog commit. Backlog edits stay uncommitted until the next commit a skill makes on a `todo/` branch (the tree claim, usually), which stages them by explicit path. New roots, and any change to a node of an unclaimed tree, are made only on the base branch; on a `todo/` branch the skills refuse them and name the base. The clean-tree check (`reference/git-flow.md`) ignores them.

## Direct use

`/todo` alone is read-only: list the commands, run the invariant check on `TODO.md` if it exists, report. Change nothing.

| Command | Purpose |
|---|---|
| `/todo-init` | Bootstrap files, detect test command and git, optional pre-planning and CI setup, migrate the old format |
| `/todo-plan` | Plan the work into lanes and a tree; revise the plan at any time |
| `/todo-add` | Add a task, or break a request into a tree |
| `/todo-continue` | Execute the next task node, verify it, merge it into its parent |
| `/todo-update` | Manual state and field changes |
| `/todo-status` | Read-only tree, lanes, history and search |
| `/todo-report` | Write an interactive HTML status page to `docs/status.html` |
| `/todo-release` | Turn `[Unreleased]` into a version after the user confirms it |

Each skill runs only its own command and never chains into another unprompted.

## Git mode

At the start of every command run `git rev-parse --is-inside-work-tree`.

- **Git repo:** each node works on its own branch or worktree (`reference/git-flow.md`). The **base branch** is the one the user names, otherwise the README `Base:` line, otherwise the first that exists of `main`, `master`, `trunk`, `develop`; with none of them, ask once. When the user names a base that differs from that default, offer to add `Base: <branch>` to README (written on a yes; a backlog file like the `Tests:` line). Every step that checks out or merges into the base (tree claim, claim release, base merge, release) runs in the **main checkout** (the first entry of `git worktree list`): from a linked worktree, `cd` there first; if it is on another branch with changes, stop and print the commands.
- **Not a git repo:** warn **once per command**: "This is not a git repository. The todo skills still work, but without branches, worktrees, commits or merges, so there is no isolation and no history. Run `git init` to enable them." Then use **no-git mode**: skip every git step, track progress in `State:` (including `files:` touched), still update markers and drain to CHANGELOG.md. Verification is unchanged.

Never tag, force-push, reset hard or clean. The one forced branch delete is of a branch holding only the skill's own unpublished claim commit (`reference/git-flow.md`, tree claim steps 2 and 5). **The skills' own git commands never touch the network:** no fetch, pull or push. Sharing commits is git's job and yours. A test command may download dependencies; if it fails for lack of network, block with that reason instead of retrying.

## TODO.md schema

```markdown
# Active Backlog

## 🌳 Task Tree
```

Exactly this heading and one section. No In Progress, Ready or Blocked sections: the marker on each task is its state. An empty tree is the two headings and no tasks.

A task is **2 to 4 lines**: what to do, how it is validated, optional links and state.

```markdown
- [ ] **FEAT-002** · P1 · mid · XL · Add token refresh to the auth service
  - Done when: old token rejected after refresh; `npx jest tests/auth`; regression: `npm test`
  - Links: Ref: docs/auth.md#refresh · Depends: TASK-001 · From: FIX-001
  - State: branch todo/FEAT-002-add-token-refresh-auth from main; next: build children
  - [ ] **FEAT-002.1** · mid · Refresh endpoint
    - Done when: endpoint covered by an integration test; `npx jest tests/auth/refresh.test.ts`
    - [/] **FEAT-002.1.1** · high · Token store interface
      - Done when: store round-trips a token; `npx jest tests/auth/store.test.ts`
      - State: attempts 1/3; baseline 42 passing; branch todo/FEAT-002.1.1-token-store-interface from todo/FEAT-002.1-refresh-endpoint; next: build
```

| Part | Rule |
|---|---|
| Header | `- [m] **ID** · [P0-P2, roots only ·] COMPLEXITY [· SIZE] · what to do, one sentence`: complexity `low`, `mid` or `high` (required); size `S`, `M`, `L` or `XL` (optional) |
| `Done when:` | **Required.** Criteria, then `; ` and at least one exact command in backticks. Optional `; regression: \`cmd\``; without it the regression is the project's full suite |
| `Links:` | Optional. `Ref: <path#anchor>`, `Depends: <IDs>`, `From: <ID>`, `Lane: <name>` (roots only), separated by ` · ` |
| `State:` | Optional, survives a context reset. Items separated by `; `, each at most once, in this order: `attempts n/3`, `baseline <n> passing` (or `none`, or `red: <failing test ids, comma-separated>`), `tier: <low|mid|high>` (only once raised above the node's complexity), `hyp: <one line>`, `branch todo/<ID>-<slug> from <branch it was created from>`, `no git`, `files: <paths>`, `docs: <paths>`, `next: <step>`. `next:` is one of `start <ID>`, `build children` (tree claim, ancestors), `read docs`, `plan proposed`, `build`, `drain`, `decompose`, `resume`, `redo after revert`. A later claim **replaces** the whole line, except that in no-git mode a root keeps `files:` and `docs:` rolled up from its finished children until the drain |
| `Blocked:` | On `[!]` tasks, instead of State and in its place (the last field line): `<reason> → <command in backticks> <error, at most 5 lines joined with " / "> → <action required>`. A manual block writes `n/a (manual)` in the middle |

Only these four fields exist; a task never has both State and Blocked. More than 4 lines is design prose and belongs in `docs/` (link it with `Ref:`). If a task needs more, split it.

Markers: `[ ]` open, `[/]` active (at most one in the file), `[!]` blocked, `[x]` verified and merged (or being merged) into its parent, waiting for its root to drain. To change a marker, replace only the character between the brackets: the `- ` before it, the ID and the indentation stay as they are (a task line that loses its `- ` fails I3), and re-read the line after the edit.

### Tree, levels and complexity

A node at level L has its header indented `2L` spaces and its fields `2L+2`. Maximum 3 levels.

**Scope rule.** Every leaf is one change that fits one context window and touches at most 5 files; bigger work is split into children (`/todo-add`). A node too big to split yet keeps `State: next: decompose` until `/todo-continue` breaks it down.

**Size** (optional, after the complexity) records scope when it helps a reader; when present, it must match the tree, and adding or dropping a node updates every ancestor's size:

| Size | Meaning | Where |
|---|---|---|
| `S` | One change, at most 2 files | Leaf |
| `M` | One context window, at most 5 files | Leaf |
| `L` | Has children, all leaves | Parent |
| `XL` | Has grandchildren | Parent |

A leaf with `State: next: decompose` may carry `L`/`XL`.

**Complexity** says how hard the reasoning is, not how big the change is, so an agent can pick a fitting model:

| Complexity | Meaning | Examples |
|---|---|---|
| `low` | Mechanical: the cause and the change are already known, no investigation | rename, docs, config, a guard or small function whose fix the task line states |
| `mid` | Ordinary work that needs some investigation or design (the default) | a new endpoint, a bug whose cause must be found |
| `high` | Hard reasoning or high risk | concurrency, security, data migration, unclear spec, design across modules, tricky algorithms |

A parent is rated by its integration step alone (usually `low` or `mid`); its children carry their own levels. Roots carry the priority and the lane; children inherit both.

### Model routing (optional)

A project maps levels to models with one README line, for example `Models: low=haiku, mid=sonnet, high=opus` (any names the agent understands). Without that line, or without a subagent tool, complexity is only a hint and work runs in the current model. With both:

- `/todo-continue --delegate` and lane runs give each node (or lane root, at its highest complexity) a subagent on the mapped model.
- The reviewer runs at the node's tier or higher.
- **Escalation:** after a failed verification attempt the next attempt runs one tier higher (`low` → `mid` → `high`), recorded in `State:` as `tier:`. A wrong `low` label costs one cheap attempt, not a blocked node.

## IDs

- Roots `<PREFIX>-<NNN>`, one global sequence, 3 digits. Children append `.n`: `FEAT-002.1`, `FEAT-002.1.2`. Dots equal the level.
- IDs are never reused. Next root number = highest FEAT-/FIX-/TASK- number found in `TODO.md`, `CHANGELOG.md` (including IDs after `Includes:`), `docs/plans/*.md` **and**, in git mode, commit subjects (`git log --all --format=%s`, which name dropped IDs), plus 1. Next child number = the highest child number under that parent found in the same places, plus 1.

| Prefix | Meaning | CHANGELOG heading | Commit type |
|---|---|---|---|
| `FEAT` | New capability | `### Added` | `feat` |
| `FIX` | Bug or regression | `### Fixed` | `fix` |
| `TASK` | Refactor, chore, docs, test, perf, build | `### Changed` | whichever fits |

Children use their root's prefix.

## Which node is next

A node is **workable** when: it is `[ ]`; every child is `[x]`; every `Depends:` ID is satisfied (in CHANGELOG.md as an entry ID or after `Includes:`, also in `git show <base>:CHANGELOG.md` in git mode, or `[x]` in TODO.md; when only the base's CHANGELOG satisfies it, `/todo-continue` merges the base into the branch the node will start from before starting it, step 3; read-only commands report "waits for a base merge"); no ancestor is `[!]`; and, in git mode, its root is not claimed by another branch. A root is **claimed** when its `State:` in the base branch's `TODO.md` (`git show <base>:TODO.md`) names a branch; its tree is workable only from a branch of that family (`todo/<ROOT-ID>-…` or `todo/<ROOT-ID>.…`). A skipped claimed tree is reported as `claimed by <branch>`; when that branch exists in this clone, add "if this is your work: `git switch <branch>` (or `cd` to its worktree) and rerun to resume". A branch in this clone can belong to another session, so it is never resumed from the base automatically. If backlog files hold uncommitted edits on the base, `git switch` to that branch fails: say so and offer `git stash push -- <backlog paths>` first and `git stash pop` back on the base.

**Interrupted work comes first (git mode).** On a tree branch (any `todo/` branch), list the tree's branches (`git branch --list 'todo/<ROOT-ID>-*' 'todo/<ROOT-ID>.*'`) and read each one's node in `git show <branch>:TODO.md`. A node that is `[x]` on a branch not yet merged into its parent's branch (`git merge-base --is-ancestor <branch> <parent branch>` fails) stopped before its merge: finish that merge and do nothing else (`/todo-continue` step 2). A node that is `[/]` is resumed, deepest first. A node that is `[!]` on any of the tree's branches counts as `[!]` everywhere (not workable; its ancestors wait), even where another branch still shows it `[ ]`; a branch whose node is no longer in its parent branch's TODO.md (dropped) is ignored; a branch already merged into its parent's branch is deleted with `git branch -d`. Skip this on the base branch.

### Lanes

A lane is a named track of root trees that one agent context works alone, in order. `Lane: <name>` (a lowercase letter, then lowercase letters, digits or dashes) on a root puts its whole tree in that lane; children inherit it and a root without it is in lane `main` (so `--lane main` selects those roots). Lanes are context, not tasks: a lane may hold one task or many, lanes run in parallel with each other (`/todo-continue --all-lanes`) and roots inside a lane run in sequence. Cross-lane order is only expressed with `Depends:`. Lane names are listed in the plan doc `docs/plans/PROJECT.md` when one exists.

Order: roots P0 → P1 → P2, then by ID number (the global sequence, ignoring the prefix) (with `--lane` only that lane's roots); within a root, depth-first in document order. A parent whose children are all `[x]` is workable: that is its **integration step**.

## Lifecycle by status

The marker is the status, and each command acts only as that status allows.

| Status | `/todo-continue` | `/todo-update` | `/todo-add --parent` |
|---|---|---|---|
| `[ ]` workable | branch, claim, build, review, verify, complete | `in-progress`, `blocked`, `drop`, edits | allowed |
| `[ ]` waiting | skip, say what it waits for | `blocked`, `drop`, edits | allowed |
| `[ ]` in a tree claimed by another branch | skip, report the branch | `ready` on the root releases the claim | refused |
| `[/]` | resume from `State:` | `ready`, `blocked`, edits; no `drop` | refused |
| `[!]` | skip, report `Blocked:` | `ready`, `drop`, edits | refused |
| `[x]` | never touches | `revert` only | refused |

Order for every node: **ready check → branch (in an unclaimed tree: tree claim published to the base first) → start `[/]` → build → review → verify → complete `[x]` → merge into parent**. "Claim" means the tree claim; marking a node `[/]` is its start. The branch exists before the status changes. Ancestors stay `[ ]` while a descendant is active.

**Ready check.** Lint passes, the node is workable, its `Ref:` (if any) exists, its `Done when` has a runnable command, the tree is clean (git mode), and the regression baseline is green (or `none`, or red for a FIX node; `reference/verification.md` step 1).

## CHANGELOG entry (written only by a root drain)

Inserted as the first `- ` item of the matching `###` list under `## [Unreleased]`, newest first, no blank line between entries. Create the heading if missing, in Keep a Changelog order (Added, Changed, Deprecated, Removed, Fixed, Security), with one blank line before and after it:

```markdown
- **FEAT-002** (feat): Add token refresh to the auth service. Ref: docs/auth.md#refresh. Validated: `npx jest tests/auth`. Includes: FEAT-002.1, FEAT-002.1.1.
```

One entry per root. Parts in this order, each only when it applies: `Ref:` (the root's), `Validated:` (the root's `Done when` commands, each in backticks, without a `regression:` command), `From: FIX-001.` (the root's `From:`), `Docs: updated docs/x.md.` (README/`docs/` files the tree changed: `git diff --name-only <base>...<root branch>` without backlog files, or the `docs:` items in no-git mode), and last `Includes:` with every descendant ID (a leaf root has none).

## Reference files

Loaded only when a command needs them, from `reference/` (`../todo/reference/` from a command skill):

| File | Contents | Loaded by |
|---|---|---|
| `reference/git-flow.md` | Branches, tree claim, staging, merging, refresh from base, conflicts | `/todo-continue`, `/todo-update --status in-progress` or `ready` |
| `reference/verification.md` | Verification protocol, writing a Done when, Definition of Done, command safety | `/todo-continue`, `/todo-add`, `/todo-plan`, `/todo-update --status in-progress`, `/todo-init --ci` |
| `reference/rtm.md` | Optional RTM: `docs/RTM.md` first, else README `## RTM`, else none; format and rules | `/todo-plan`, `/todo-add`, `/todo-continue`, only when an RTM exists |
| `reference/lanes.md` | Lane runs: coordinator, lane agents, merging lanes | `/todo-continue --lane` or `--all-lanes` |
| `reference/ci.md` | `.todo/check.sh` (lint + tests), CI job per provider, local pre-push fallback | `/todo-init --ci` |
| `reference/clarify.md` | Ambiguity checklist, stop triggers, where open questions go | `/todo-plan`, `/todo-add`, only for an unclear request |
| `reference/review.md` | Optional independent reviews: design review before the build, root review before the drain | `/todo-plan`, `/todo-continue`, only for a `high` or risky root |
| `reference/git-flow-edge.md` | A failed tree-claim fast-forward, `--worktree`, merge and rebase conflicts | `reference/git-flow.md`, only at those points |
| `reference/deliverables.md` | Red checks for scripts, CI YAML, docs and configuration; services and environment assignments in `Tests:` | `reference/verification.md`, only for those deliverables |
| `reference/doc-drift.md` | Searching README and docs for a changed interface name and reporting `file:line` hits | `/todo-continue`, only when a node changed an interface |

## Invariants (every todo-* skill checks these first)

| # | Invariant |
|---|---|
| I1 | At most one `[/]` task, and a `[/]` parent has no open children |
| I2 | Every ID is unique in TODO.md |
| I3 | Each task has a non-vacuous `Done when` with a backticked command, at most 4 lines, only the four fields, no State together with Blocked, a Blocked line on every `[!]`, a priority on roots only, a complexity of `low`, `mid` or `high`, an optional valid size and a title |
| I4 | TODO.md is at most 120 lines |
| I5 | No ID appears in both TODO.md and CHANGELOG.md (IDs after `Includes:` count) |
| I6 | The file is exactly `# Active Backlog` plus one `## … Task Tree` section |
| I7 | Every ID in `Depends:` or `From:` exists in TODO.md or CHANGELOG.md |
| I8 | Tree integrity: child ID = parent ID + `.n`, depth at most 3, even indent, no `[x]` root, no `[x]` node with open children, and any size given matches the tree |
| I9 | No dependency cycles, counting "parent waits for its children" |
| I10 | No forbidden command in `Done when`: `sudo`, `rm -r`/`-f`, `git push`, `git reset --hard`, `git clean`, `chmod -R`, `mkfs`, `dd if=`, the shell builtins `eval` and `exec`, a download whose output goes straight to a shell, one-liner code flags (`sh`/`bash`/`zsh`/`python` -c, `node`/`ruby`/`perl` -e, `php` -r), `find -exec rm` and `-delete`, publish, upload and deploy commands (`npm publish`, `twine upload`, `docker push`, `mvn deploy` and the like), and reads of credential files (SSH keys, cloud and tool credentials) |

**The invariant check** ("lint" in the skills) means: if `.todo/todo-lint.sh` exists in the project, run `bash .todo/todo-lint.sh` from the repository root (read it first under "Command safety" in `reference/verification.md`); otherwise check I1-I10 by reading. The plugin itself ships Markdown only: the lint and the other optional scripts (`todo-verify.sh`, `todo-rtm.sh`, `todo-replay.sh`, the Stop hook, `todo-report.sh`; all read-only except `todo-replay.sh --run`, which runs commands) live in the `tools/` folder of the todo-skills repository, and a user who wants them copies them into the project by hand (the skills never download anything). The lint needs bash, awk, grep, sed and tr and prints non-failing `WARN` lines for weak `Done when` commands. Its failures win over your own reading; a pass does not replace judging a command's safety (`reference/verification.md`). A lint run after an edit that fails means the edit is wrong: fix it or undo it before you stop.

On a violation, report it, change nothing, and ask, with one exception: a writing command (`todo-continue`, `todo-add`, `todo-update`, `todo-plan`) repairs **I5** when the IDs in TODO.md that are also in CHANGELOG.md are exactly the root and `Includes:` IDs of one CHANGELOG entry (an interrupted drain): delete that subtree from TODO.md and say so. `/todo`, `/todo-status` and `/todo-report` only report.

## Hard guardrails

1. No ghost tasks. Every change to TODO.md traces to a user command or a completed code transition.
2. No required tooling. Markdown plus git only; git itself is optional. The lint script and hook are optional and read-only.
3. No node is closed without running its `Done when` and its regression and seeing both pass.
4. CHANGELOG.md is append-only apart from `[Unreleased]` insertions by a root drain, the confirmed `/todo-release`, and `/todo-init` adding a missing `## [Unreleased]`. Never rewrite released sections.
5. "Git mode" above: no tag, fetch, pull or push. `[Unreleased]` becomes a version only through `/todo-release`, after the user confirms.
6. The base branch receives only tree claims (fast-forward), claim releases, the confirmed release commit and the merge of a verified root.
7. When a rule here conflicts with an explicit user instruction, state the conflict and ask.
