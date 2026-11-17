# spex apply

Apply a specification to implement code step by step.

## Usage

```text
/spex apply [spec_name | --all]
```

## Inputs

- OPT: `$spec_name` or `--all`

## Preconditions

- Follow phases in order. Do not skip or reorder.
- Debug timeline: when debug is enabled, scripts append APPLY
  anchors to `$spec_path/debug.log` automatically (task begin,
  committed, review begin/round, task done, post-action). Do not
  call `mark-phase`.

## Execution

### Phase 1: Resolve Spec

- IF `$spec_name` is `--all`:
  - CMD: `$spex_skill_dir/scripts/spex list --json --must-undone`
  - Parse stdout as JSON array `$specs` of objects (`spec_name`,
    `spec_path`)
  - For each entry in `$specs` (outer loop): set `$spec_name` /
    `$spec_path` -> Phases 2–9 (Phase 9 when that spec's tasks all
    done)
  - After Phase 9 for one spec -> next `$specs` entry at Phase 2.
    IF none remain -> **STOP**
- ELSE -> CMD:

```bash
$spex_skill_dir/scripts/spex list --json --must-undone "$spec_name"
```

- Parse stdout as JSON array:
  - IF single element -> set `$spec_name` / `$spec_path` from entry
  - IF multiple -> numbered `spec_name` list -> user chooses -> set
    `$spec_name` / `$spec_path` from selected entry
  - IF script exits error -> report error -> STOP

### Phase 2: Validate Branch

- CMD:

```bash
$spex_skill_dir/scripts/spex apply-helper precheck --name $spec_name
```

- IF non-zero exit -> error already on stderr -> STOP
- ELSE -> continue

### Phase 3: Build Prompt / Resume Gate

- CMD:

```bash
$spex_skill_dir/scripts/spex prompt apply-one-task --json --name $spec_name
```

- Parse JSON stdout:
  - IF `"all_done": true` -> Phase 9 (skip Phase 8). In `--all`
    mode, after Phase 9 continue Phase 1 outer loop next `$specs`
    entry at Phase 2, or **STOP** if none remain
  - IF non-zero exit -> report stderr -> STOP
  - ELSE save:
    - `$prompt` ← `"prompt"`
    - `$current_task_id` ← `"task_id"`
    - `$resume_phase` ← `"resume_phase"` (`implement` or `review`)
    - `$commit_title` ← `"commit_title"` (may be empty)

- **Single render:** Call `prompt apply-one-task` **once** per task
  iteration. Reuse `$prompt` for Phase 4 and sub-agent handoff. Do
  **not** re-run unless `$prompt` was lost (e.g. new session).

- Step incomplete until `completed_at` set. IF `commit_title` set
  AND `completed_at` empty -> `$resume_phase` is `review` (skip
  implement/commit)

- **Route:**
  - IF `$resume_phase` is `review` -> skip Phases 4–5 -> Phase 6 in
    main context. Do NOT set `$commit_sha` from `HEAD` here —
    Phase 6 **6-entry** resolves it (prefer review file's
    `commit_sha`)
  - IF `$resume_phase` is `implement` -> launch sub-agent for
    Phases 4–5 only (implement + first commit). Instruct it to
    follow Phases 4–5 of this command exactly. Pass `$prompt` as
    Phase 4 guide, plus `$current_task_id` and `$spec_name`.
    Implementation prompt must NOT create the commit — sub-agent
    runs Phase 5 (`apply-commit`) after implementation. ON_FAIL:
    report + retry **once**; IF still fails -> STOP. After OK ->
    Phase 6 in main context

### Phase 4: Execute Task

- Using `$prompt` as guide (from Phase 3 — do **not** re-run
  `prompt apply-one-task`), implement current task. Follow rendered
  prompt precisely (spec, completed steps, task description,
  guidelines)
- Deliver production code + tests together
- IF no file changes -> report issue -> STOP
- Do NOT create git commit here — Phase 5 handles commit

### Phase 5: Commit (record commit_title only)

- CMD:

```bash
$spex_skill_dir/scripts/spex prompt apply-commit --name $spec_name
```

- **Single render:** Call `prompt apply-commit` **once** per commit.
  Save output as `$commit_prompt` and reuse for staging/commit. Do
  **not** re-run unless `$commit_prompt` was lost.

- `$commit_prompt` ← output. Using `$commit_prompt`, stage relevant
  changes + commit:
  - Do NOT stage any files under `$spex_root/`
  - Commit via heredoc: `git commit -F- <<-EOF ... EOF`
  - ON_FAIL (e.g. pre-commit hook): fix + retry **once**; IF still
    fails -> STOP + report

- After commit OK:

```bash
git log -1 --pretty="%h: %s"
```

- `$commit_title` ← output

```bash
git rev-parse --short HEAD
```

- `$commit_sha` ← output

- **Persist commit_title now — do NOT set `completed_at` yet**
  (review/fix may still be pending; enables interrupt resume):

```bash
$spex_skill_dir/scripts/spex todo-helper --name $spec_name edit \
  --id "$current_task_id" --commit-title "$commit_title"
```

### Phase 6: Review Loop

- Load and follow `references/apply-review-loop.md` exactly (includes
  single-prompt rules for `$review_prompt` / `$fix_prompt`;
  review-helper always needs `--name`; most subcommands need
  `--step`; prefer `status` / `next` / `show` — `list`/`get` are
  show aliases; reuse last status JSON — do not re-status right
  after 6b or after a successful `bump-round`)
- IF review loop **STOP**s due to abnormal failure (e.g. fix/amend
  verification fails after relaunch) -> end entire `/spex apply`
  immediately — do **not** run Phase 7, Phase 8, or Phase 9; do
  **not** start next task or next `--all` spec. Step stays
  incomplete so later `/spex apply` can resume via Phase 3 →
  Phase 6. Round-3 open majors are **not** a reason to STOP —
  loop must enter 6c and fix them in this same invocation

### Phase 7: Mark Task Complete

- Only after review/fix loop finishes successfully. Refresh
  `$commit_title` if needed, then set **`completed_at`** (step not
  done until this runs):

```bash
$spex_skill_dir/scripts/spex todo-helper --name $spec_name edit \
  --id "$current_task_id" --completed-at now \
  --commit-title "$commit_title"
```

- ON_FAIL: report error -> STOP

### Phase 8: Next Task

- Go back to Phase 3 for next undone task. Each iteration uses
  fresh sub-agent for Phases 4–5 when `resume_phase` is `implement`
- When Phase 3 reports `"all_done": true`, Phase 3 routes to
  Phase 9 (do not loop further for this spec)

### Phase 9: Post Action

- Run for **current** `$spec_name` (once per completed spec,
  including each `--all` entry):

```bash
$spex_skill_dir/scripts/spex apply-helper post-action --name $spec_name
```

- Display output to user
- IF `--all` mode -> continue Phase 1 outer loop next `$specs`
  entry at Phase 2, or **STOP** if none remain
- ELSE -> **STOP.** Do NOT implement additional steps or modify
  project files beyond what was already committed

## STOP / Outputs

- Phases 1–9 including `--all` outer loop, Phase 8 next-task loop,
  Phase 9 post-action
- Abnormal Phase 6 STOP leaves step incomplete for resume
