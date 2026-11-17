# Daily Grading Workflow

Use this reference for worksheet photos, teacher-marked papers, wrong-question batches, and direct `question + student answer` grading. For image intake, full-paper evidence, knowledge assessment and asynchronous execution, `photo-intake.md` is the primary workflow.

## One-Turn Modes

Do not make the parent send a second message just to save an ordinary grading result.

- Default recorder mode: `auto` (chooses light/full archive from evidence). Foreground feedback remains fast.
- Use `fast_grade_only` only when the parent explicitly says `只批改`, `先不记录`, `不要落库`, or the workspace is not initialized.
- Use `full_archive` when the parent explicitly asks for full recording/review, or when the evidence itself justifies it.

`fast_grade_light_record` grades, returns the parent-facing summary, and writes a light local record in the same task. The light record may update `records/`, the relevant mistake book, and `memory/active-context.md`; it should not update global/user-level `MEMORY.md`, run broad history scans, or change old weak-point statuses.

Auto-upgrade to `full_archive` when one or more of these are true:

- Two or more wrong or uncertain items in the same batch point to the same cause or weak point.
- A wrong item directly matches an active weak point in `memory/active-context.md` and looks like relapse, transfer failure, or spaced forgetting.
- The evidence is a formal test, teacher-marked paper, phase review, midterm/final review, or parent-provided official school mistake set.
- The batch gives high-confidence evidence for a new durable weak point, not just a one-off slip.
- The parent explicitly asks for `完整记录`, `完整归档`, `纳入错题本`, `更新薄弱项`, `阶段性复盘`, or `做复盘`.

When auto-upgrading, keep reads selective: start from the active context, then open only matching weak-point and mistake history. Do not update global/user-level `MEMORY.md` unless the update is about a stable workflow rule or the parent explicitly asks.

## Context Build

Before grading, build one compact context bundle:

```bash
python3 {baseDir}/scripts/build_grading_context.py \
  --workspace . \
  --format md
```

The context builder reads `.zhizhi-math-coach/config.json`, `memory/active-context.md`, and `curriculum/profile.md`, then returns a compact grading context and appends `.zhizhi-math-coach/run-log.jsonl`.

Only read fallback files such as `memory/long-term.md`, `memory/short-term.md`, `curriculum/progress.md`, or `records/learning-progress.md` when the context builder warns that `memory/active-context.md` is missing, stale, or incomplete.

Keep `memory/active-context.md` under 2500 bytes. If it grows beyond that, summarize it before recording new evidence.

## Foreground And Background

Save original photos and return the urgent correction first. A registered OpenClaw cron consumer or supported isolated session can complete the queued full archive later; see `photo-intake.md`. If no worker runs, process it in the current session and do not claim it is running in the background.

A worker receives one leased job, the saved images and compact context. It can open matching history and call `photo_jobs.py finish` to write its local archive. Keep writes tied to that claimed job, and leave unrelated files and public publishing alone. For direct text, use the recorder in the main session.

## History Reads

After the first image pass, choose the final recording mode from evidence:

- `fast_grade_light_record`: skip history reads.
- `full_archive`: use `rg -n "<topic|cause|slug>" weak-points mistakes records/learning-progress.md` or direct filenames to find relevant history. Open only matching files.

Read `references/relapse-handling.md` only when a matching weak point was previously `补齐理解`, `待巩固`, `已掌握`, or the new evidence looks like recurrence.

Do not read `knowledge-points/*.md` during ordinary grading unless creating or updating a reusable explanation card. Do not read unrelated GitHub setup, Pages publishing, sync, or automation references during ordinary grading.

## Recorder Payload

Create a compact `diagnosis-update.json`. For full-paper input, provide `items` for **every visible question** using the schema in `photo-intake.md`; correct items are required positive evidence. The recorder derives the mistake subset and counts. The fields below remain supported for legacy wrong-question-only input, which cannot describe complete paper coverage.

Required top-level keys:

- `date`, `source`, `source_type`, `grade`, `semester`, `total_items`, `correct_items`, `overall`.

Common optional top-level keys:

- `source_slug`, `semester_range`, `term_phase`, `scope`, `mistake_book`, `cause_summary`, `teaching_and_practice`, `next_steps`, `progress`, `weak_points`, `short_term_notes`, `long_term_notes`, `active_context_md`.

Required `mistakes[]` keys:

- `item_no`, `question`, `student_answer`, `correct_answer`, `result`, `error_type`, `cause`, `confidence`, `remediation`.

Useful `mistakes[]` optional keys:

- `historical_status`, `relapse_judgment`, `evidence`, `weak_point_slug`, `weak_point_title`, `repractice_status`.

Provide `weak_points[]` only when the selected mode is `full_archive` or the evidence should explicitly update a durable weak-point file. Ordinary light records should not create weak-point files merely because a wrong item has a cause.

Use `active_context_md` as the complete replacement text for `memory/active-context.md` when the compact current context should change.

## Validate And Record

Validate first:

```bash
python3 {baseDir}/scripts/validate_diagnosis_payload.py \
  --workspace . \
  --mode auto \
  --input diagnosis-update.json
```

Record after validation:

```bash
python3 {baseDir}/scripts/record_grading_diagnosis.py \
  --workspace . \
  --mode auto \
  --input diagnosis-update.json
```

The recorder validates internally, so the separate validator is optional. Use `--mode auto` normally; it reports the selected mode and reasons. Explicit `--mode full_archive` remains available. Recording the identical payload again returns the original result without appending duplicate evidence. `--dry-run` performs no writes, including logs.

Both scripts append `.zhizhi-math-coach/run-log.jsonl`.

## Sync

If automatic Git sync is enabled after local files are written:

```bash
python3 {baseDir}/scripts/sync_learning_repo.py \
  --workspace . \
  --mode after-task \
  --task-kind grading \
  --message "Update learning data"
```

When `.zhizhi-math-coach/config.json` has `git_sync.defer_push_after_grading: true`, grading sync commits locally and skips push. A later explicit sync, review, worksheet, or publish task can push.
