# Photo intake, complete documentation and background processing

## Foreground comes first

When a parent sends a worksheet or wrong-question photo:

1. Preserve the original attachment with `photo_jobs.py enqueue`. Pass the actual local attachment path; never invent a path or recreate the original image. If attachments cannot be downloaded, state that original-image archival is pending.
2. Address the parent's immediate request: grade the clearly visible requested questions, explain corrections, and flag unreadable regions. A short foreground answer may focus on mistakes; the archive must cover **all visible items**.
3. Return the saved task ID and its actual status. Say “background processing” only if a supported isolated session has started or the configured cron worker is registered. A queued file alone is not an executing worker.
4. If no worker is available, use the same claim/finish flow in the current session after the urgent correction. Never silently abandon the full archive.

```bash
python3 {baseDir}/scripts/photo_jobs.py --workspace . enqueue \
  --image /absolute/path/page-1.jpg --image /absolute/path/page-2.jpg \
  --date 2026-10-01 --note "先讲错题，后台补齐整卷档案"
```

Saved originals live in `uploads/photo-jobs/<id>/`. Queue metadata lives in `.zhizhi-math-coach/photo-jobs/`. Repeated submission of the same images in the same order on the same date reuses the job. The note is context, not a replacement for the image evidence.

## Background worker

The queue does not implement OCR or call a model API. An **OpenClaw multimodal session** opens the saved images, understands the questions/diagrams, solves the math, and creates the structured payload. The scripts validate, render documents and aggregate evidence.

1. Read config. A scheduled worker must exit if `automation.enabled` or `automation.allow_photo_archive` is false.
2. Claim at most one job. If `job` is null, end quietly.
3. Build compact context with `build_grading_context.py`. Reuse established knowledge-point IDs and school scope. Read only matching history if necessary.
4. Open every page of this job. Use image crops/zoom when available. Inventory printed question numbers and subquestions before diagnosing mistakes.
5. For every visible item, transcribe the question, child answer/work, result, explanation, diagram description, page, recognition confidence and knowledge points. Include correct answers as positive evidence. Mark cropped/illegible questions `need-confirmation`; never fill missing diagram labels by guessing.
6. Create the payload below, then finish. `finish` supplies the original date, durable image paths and idempotency ID automatically. Do not separately call the recorder for the same job.
7. On error call `fail`. Leases expire after 15 minutes; use `heartbeat` for longer work. Expired leases and reported errors retry up to three attempts, then remain `failed` for inspection. Only `failed` jobs can be manually retried. `needs-confirmation` waits for new evidence, not automatic regrading of the same unreadable image.

```bash
python3 {baseDir}/scripts/photo_jobs.py --workspace . claim
python3 {baseDir}/scripts/photo_jobs.py --workspace . heartbeat --job-id ID --lease-token TOKEN
python3 {baseDir}/scripts/photo_jobs.py --workspace . finish --job-id ID --lease-token TOKEN --input diagnosis-update.json
python3 {baseDir}/scripts/photo_jobs.py --workspace . fail --job-id ID --lease-token TOKEN --error "具体失败原因"
python3 {baseDir}/scripts/photo_jobs.py --workspace . list
python3 {baseDir}/scripts/photo_jobs.py --workspace . retry --job-id ID
```

If a recorder call was interrupted, retry the exact `.zhizhi-math-coach/photo-inputs/<id>.json` saved by `finish`; do not regenerate a different diagnosis with the same record ID. The recorder rolls a pending transaction forward before deduplicating. Do not concurrently edit its pending output files by hand.

## Full-paper payload

```json
{
  "date": "2026-10-01",
  "source": "数学课堂练习，第1页",
  "source_type": "school",
  "grade": "一年级",
  "semester": "上学期",
  "coverage": "complete",
  "overall": "能辨认平面图形，需继续观察计数是否有遗漏。",
  "items": [
    {
      "item_no": "1(1)",
      "page": 1,
      "question": "图中有几个三角形？",
      "diagram_description": "3个分离的三角形和2个圆形，无重叠。",
      "student_answer": "3",
      "student_work": "在三个三角形旁各画了一条记号。",
      "correct_answer": "3",
      "result": "correct",
      "recognition_confidence": "high",
      "assisted": false,
      "knowledge_points": [
        {"id": "geometry.shape-recognition", "title": "平面图形辨认与计数", "confidence": "high", "result": "correct"}
      ],
      "explanation": "只数三角形，逐个标记，共3个。"
    }
  ]
}
```

- `items` is authoritative; the script derives the mistake subset and counts when omitted. Do not construct a second contradictory `mistakes` list.
- `coverage: complete` means every question in the supplied paper is represented. Use `partial` for cropped/missing pages; preserve known `total_items` or use `unknown`. Correct counts describe the supplied visible evidence, not an invented full-paper score.
- Results: `correct`, `wrong`, `unanswered`, `need-confirmation`. A blank answer is distinct from an unreadable answer.
- Wrong items also need `error_type`, `cause`, `confidence` (cause confidence), `evidence` and `remediation`. Unknown causes remain `待诊断` with low confidence; recognition confidence describes legibility, not certainty about the cause.
- Knowledge-point IDs must be stable across sessions. Use curriculum concepts, not the surface story (for example place value rather than “buying apples”). Reuse existing IDs from context; avoid merging distinct concepts or creating a new ID for every wording.
- For multi-concept items, put a per-concept `result` on each knowledge-point tag only when the written steps support it. A wrong final answer without step evidence must not mark every tagged concept wrong. The aggregator treats those tags as uncertain by default.
- `assisted` is true when answers required parent/teacher hints. If independence is unknown, do not count it as proven independent mastery; use low recognition/evidence confidence and explain the limitation.
- Use `diagram_description` to preserve shapes, positions, labels, occlusion and uncertainty from the original. Store a `geometry_spec` only if the visible geometry can be reconstructed faithfully. Complex overlapping diagrams can retain the original plus description; do not pretend a simplified SVG is identical.
- Direct text input can call `record_grading_diagnosis.py --mode auto --input ...` without a queue. `source_images` optionally lists local originals to archive. Legacy `mistakes`-only input remains supported, with a coverage warning.

## Knowledge assessment and follow-up

The recorder creates:

- `records/<date>-<source>-diagnosis.md`: original-image links and complete per-item documentation, followed by mistakes, explanations and next steps.
- The adjacent `.json`: reproducible structured evidence, including correct items and decisions.
- `records/<date>-<source>-assets/`: original image copies, kept outside the public site.
- `records/knowledge-state.json` and `records/knowledge-mastery.md`: per-concept recent evidence, observed accuracy, sample size, status, rationale and next review date.
- `records/next-practice.json`: dated practice suggestions. Correct concepts also get spaced checks.

The assessment is an evidence-based estimate, not a psychometric mastery probability. Only clear, independently answered items are scored. It keeps the most recent eight checks per concept:

- `待确认`: no scoreable evidence, or unresolved evidence prevents a positive conclusion.
- `待观察`: only one confirmed item.
- `需要巩固`: a confirmed error in the latest check or recent observed accuracy below 90%.
- `初步掌握`: at least two confirmed correct items, but insufficient spaced evidence.
- `稳定掌握`: at least five scored items, at least two check dates separated by seven days, recent accuracy at least 90%, and no confirmed error/unresolved evidence in the latest check.

These are configurable-in-code heuristics, not a guarantee of transfer. Different representations and independent explanation should be included in follow-up practice. Time alone never improves a status. Paper topics are observations of what this paper tests, not permission to overwrite the school's curriculum progress or infer an entire grade/semester.

## Configure the cron consumer

```bash
python3 {baseDir}/scripts/setup_scheduled_tasks.py \
  --workspace /path/to/personal-learning-workspace \
  --enable-config --photo-worker --auto-register --timezone Asia/Shanghai
```

This enables an isolated worker every five minutes for queued photo archival only. It does not enable automatic worksheet generation or public publishing. It needs an available OpenClaw CLI/gateway and a multimodal model with local-image access. If the CLI is unavailable the script prints the command; the worker is **not registered**. Check registration and one real photo run in the target OpenClaw environment.
