# spex apply-one-step

Apply a single step from a specification's todo list.

## Usage

```text
/spex apply-one-step [spec_name]
```

## Inputs

- OPT: `$spec_name`

## Preconditions

- Follow phases in order. Do not skip or reorder.
- Exactly one step then STOP

## Execution

### Phase 1: Resolve Spec

- CMD:

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
  - IF `"all_done": true` -> report completion -> run post-action
    (covers last step finished but Phase 8 interrupted) and
    **STOP**:

    ```bash
    $spex_skill_dir/scripts/spex apply-helper post-action --name $spec_name
    ```

    Display output to user. Do not implement further steps
  - IF non-zero exit -> report stderr -> STOP
  - ELSE save:
    - `$prompt` ← `"prompt"`
    - `$current_task_id` ← `"task_id"`
    - `$resume_phase` ← `"resume_phase"` (`implement` or `review`)
    - `$commit_title` ← `"commit_title"` (may be empty)

- **Single render:** Call `prompt apply-one-task` **once** per task
  iteration. Reuse `$prompt` for Phase 4. Do **not** re-run unless
  `$prompt` was lost (e.g. new session).

- Step incomplete until `completed_at` set. IF `commit_title` set
  AND `completed_at` empty -> `$resume_phase` is `review` (skip
  implement/commit)

- **Route:**
  - IF `$resume_phase` is `review` -> skip Phases 4–5 -> Phase 6.
    Do NOT set `$commit_sha` from `HEAD` here — Phase 6
    **6-entry** resolves it (prefer review file's `commit_sha`)
  - IF `$resume_phase` is `implement` -> Phase 4

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
  verification fails after relaunch) -> end this invocation without
  Phase 7 or Phase 8. Step stays incomplete (`completed_at` unset)
  so later `/spex apply-one-step` can resume via Phase 3 → Phase 6.
  Round-3 open majors are **not** a reason to STOP — loop must
  enter 6c and fix them in this same invocation

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

### Phase 8: Summary and Conditional Post Action

- Count remaining undone tasks in `$spec_path/todo.json` (items
  with empty/`null` `completed_at`) -> `$remaining`
- Display summary:
  - Completed step name and `$commit_title`
  - `$remaining` (undone tasks left)
- IF `$remaining` is 0 -> run post-action (spec fully done):

  ```bash
  $spex_skill_dir/scripts/spex apply-helper post-action --name $spec_name
  ```

  Display output to user
- ELSE IF `$remaining` > 0 -> skip `post-action` (unfinished work
  remains)

- **This command implements exactly one step. STOP here.** Do NOT
  loop back to Phase 3 or implement additional steps. User must
  invoke `/spex apply-one-step` again to continue

## STOP / Outputs

- Exactly one step then STOP
- Conditional post-action only when `$remaining` == 0
- Abnormal Phase 6 STOP leaves step incomplete for resume
