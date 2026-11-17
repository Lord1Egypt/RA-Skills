# npm Package

Package name: `taskforce-loop-engineering`
Version source: the candidate checkout's `package.json`; do not infer the installed
or public-registry version from this skill. Check the actual installed package
and `npm view taskforce-loop-engineering version` separately.

The multi-IM OpenClaw diagnostic changes require `0.16.2` or newer;
the `0.16.1` package does not support them. A skill update alone does
not install these capabilities. See [OpenClaw multi-IM diagnostics](openclaw-diagnostics.md)
for capability checks, channel/account selection, and acceptance boundaries.

Install from npm:

```bash
npm install -g taskforce-loop-engineering
```

Hermes Agent integration commands:

```bash
loop-engineering-hermes-install --root /path/to/hermes/workspace --queue agent-tasks
loop-engineering-hermes-install --root /path/to/hermes/workspace --queue agent-tasks --confirm-install
loop-engineering-hermes-doctor --root /path/to/hermes/workspace --queue agent-tasks
loop-engineering-hermes-smoke --root /path/to/hermes/workspace --queue agent-tasks
```

Installed commands:

```bash
loop-engineering init --root /path/to/workspace
loop-engineering verify --root /path/to/workspace
loop-engineering run --root /path/to/workspace --config configs/loops/<id>.json
loop-engineering status --root /path/to/workspace
loop-engineering doctor --root /path/to/workspace
loop-engineering summarize --root /path/to/workspace --limit 20
loop-engineering project-intake --root /path/to/workspace --name <project> --brief "Project brief"
loop-engineering project-plan --root /path/to/workspace --project <project>
loop-engineering project-status --root /path/to/workspace --project <project>
loop-engineering enqueue --root /path/to/workspace --queue <queue> --title "Title" --task "Task body"
loop-engineering queue-init --root /path/to/workspace --queue <queue>
loop-engineering code-queue-init --root /path/to/workspace --queue <queue>
loop-engineering run-queue --root /path/to/workspace --config configs/loops/queues/<queue>.json
loop-engineering queue-status --root /path/to/workspace --queue <queue>
loop-engineering queue-scheduler-tick --root /path/to/workspace --config configs/loops/queues/<queue>.json
loop-engineering queue-peek --root /path/to/workspace --queue <queue>
loop-engineering queue-cancel --root /path/to/workspace --queue <queue> --task-id <id>
loop-engineering queue-requeue --root /path/to/workspace --queue <queue> --task-id <id>
loop-engineering queue-revision-next --root /path/to/workspace --queue <queue> --task-id <id>
loop-engineering queue-lineage --root /path/to/workspace --queue <queue> --task-id <id>
loop-engineering queue-lineage-bundle --root /path/to/workspace --queue <queue> --task-id <id>
loop-engineering queue-human-decision --root /path/to/workspace --queue <queue> --task-id <id> --decision approve|request_changes|reject
loop-engineering code-worktree-list --root /path/to/workspace --queue <queue>
loop-engineering code-worktree-inspect --root /path/to/workspace --queue <queue> --task-id <id>
loop-engineering code-worktree-diff --root /path/to/workspace --queue <queue> --task-id <id>
loop-engineering code-worktree-export --root /path/to/workspace --queue <queue> --task-id <id>
loop-engineering code-patch-verify --root /path/to/workspace --patch runtime/loops/<queue>/patches/<id>.patch
loop-engineering code-patch-apply-plan --root /path/to/workspace --patch runtime/loops/<queue>/patches/<id>.patch
loop-engineering code-patch-apply --root /path/to/workspace --patch runtime/loops/<queue>/patches/<id>.patch --confirm-apply
loop-engineering code-review-bundle --root /path/to/workspace --queue <queue> --task-id <id>
loop-engineering code-task-closeout --root /path/to/workspace --queue <queue> --task-id <id>
loop-engineering code-task-autoflow --root /path/to/workspace --queue <queue> --task-id <id>
loop-engineering code-task-autoflow --root /path/to/workspace --queue <queue> --all-actionable --until closeout
loop-engineering code-task-finish --root /path/to/workspace --queue <queue> --task-id <id> --confirm-apply --confirm-cleanup
loop-engineering code-task-run --root /path/to/workspace --queue <queue> --title "Title" --task "Task body" --confirm-apply --confirm-cleanup
loop-engineering code-task-dashboard --root /path/to/workspace --queue <queue>
loop-engineering code-task-status --root /path/to/workspace --queue <queue>
loop-engineering code-worktree-cleanup-plan --root /path/to/workspace --queue <queue>
loop-engineering code-worktree-cleanup --root /path/to/workspace --queue <queue> --confirm-cleanup
agent-loop status --root /path/to/workspace
LOOP_WORKDIR=/path/to/workspace run-loop-cron.sh configs/loops/<id>.json
```

`code-queue-init` creates an L2 assisted code queue config. Each task runs in
an isolated git worktree and branch, then runs configured verification commands
and records diff/status summaries. It does not push, merge, or delete
worktrees.

`queue-scheduler-tick` is the adaptive queue cadence command. It treats 10
minutes as the bootstrap interval, writes live cadence state to
`runtime/loops/<queue>/scheduler/state.json`, speeds up after successful work
when tasks remain queued, and backs off for empty queues, failures, human gates,
or long runs.

`project-intake` is the high-level entry for fuzzy project briefs. It writes a
deterministic project spec draft, human-readable plan, action policy, checks,
and initial backlog under `runtime/loops/projects/<project>/` without enqueuing
or executing work. `project-plan` solidifies that draft into
`configs/loops/projects/<project>.json`, generates the queue config, and writes
the initial backlog artifact. `project-status` aggregates the project queues
without changing queue state.

`code-worktree-list`, `code-worktree-inspect`, `code-worktree-diff`,
`code-worktree-export`, `code-patch-verify`, `code-patch-apply-plan`,
`code-patch-apply`, `code-review-bundle`, `code-task-closeout`,
`code-task-autoflow`, `code-task-finish`, `code-task-run`, `code-task-dashboard`,
`code-task-status`, `code-worktree-cleanup-plan`, and
`code-worktree-cleanup`
are review and
handoff commands for code queues.
They report branch, path, dirty status, verification status, diff summaries,
patch output, exported patch artifacts, untracked files, whether an exported
patch still passes `git apply --check --binary`, whether it is safe to apply,
review bundle files, which retained worktrees are cleanup candidates, and
confirmation-gated cleanup of reviewed worktrees. Closeout artifacts summarize
the task's final review, patch, apply-plan, cleanup, and next-action state.
Status ledgers summarize task-level queue, worktree, patch, review, closeout,
cleanup, and next-action state without writing artifacts.
Dashboards summarize queue counts, task counts, next-action counts,
cleanup/orphan state, priority tasks, and recommended commands without writing
artifacts.
Finish applies one reviewed patch to the main workspace and removes that one
reviewed worktree only after default patch, review, and closeout artifacts are
present and both `--confirm-apply` and `--confirm-cleanup` are supplied; it
also writes a finish artifact. Status and dashboard views read finish artifacts:
tasks ready to land report `ready_to_finish`, and successfully finished tasks
report `landed` with finish status, patch-applied, and worktree-cleaned fields.
Task run enqueues one code task, processes one worktree queue run, runs
autoflow through closeout, finishes the reviewed task, and reruns configured
worktree verification commands in the main workspace.
Autoflow runs export, patch verification, apply-plan, and review generation by
default, and can also write closeout artifacts with `--until closeout`; it skips
existing artifacts unless `--force` is supplied. Batch autoflow with
`--all-actionable` reads the status ledger and runs the same safe flow across
tasks that need export, review, or closeout artifacts.
Actual patch application requires `--confirm-apply` and still does not stage,
commit, push, merge, or change queue state.
Actual worktree cleanup requires `--confirm-cleanup`; dirty worktrees require a
default exported patch, passing patch verification, and an existing review
bundle.

The package contains `bin/`, `lib/`, `scripts/`, `templates/`, and
`skills/taskforce-loop-engineering/`.
