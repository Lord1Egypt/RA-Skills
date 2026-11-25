# Bounded comic image concurrency

For an authorized multi-page comic with adopted shared references and page text, use the [comic workflow](../workflows/novel-comic.md) and `scripts/comic-batch.js` to avoid waiting for every page individually. The default is **3 unfinished remote image tasks**. This is an adjustable client policy, not a service quota or speed guarantee. Other workflows keep their existing batch policies.

## Fix references before independent pages

Reuse reviewed character, setting and style references. For a new work, generate one representative final page, inspect it and include it in delivery before expanding the rest. Do not create an extra test page or require user confirmation for every batch. Reuse suitable adopted references/pages when available.

Only include independent pages with ready references, storyboards and exact text. Story order alone is not a generation dependency: pages sharing fixed references need not form a chain. If a page really needs an earlier generated page, wait for that page, review it and obtain its real URL before preparing the dependent batch. Never remove necessary references or invent future output URLs to enable concurrency.

Preserve the selected model, authorized count and existing 1K defaults. Each page remains its own generation. Validate every request locally before cloud submission.

## Manifest and execution

Keep requests and the manifest in the user's private persistent production directory, outside the Skill. Example:

```json
{
  "version": 1,
  "references_ready": true,
  "pages": [
    {"page_id": "p002", "input_file": "requests/page-002.json", "name": "Chapter 1 page 002 v1"},
    {"page_id": "p003", "input_file": "requests/page-003.json", "name": "Chapter 1 page 003 v1"}
  ]
}
```

`references_ready=true` records the Agent's actual reference/page review; it is not a replacement for inspection or another user approval. `input_file` points to a real [gen_image request](../api/gen_image.md), relative to the manifest directory. Keep page IDs stable and unique, using ASCII letters, digits, underscores and hyphens. Optional `name` is local archive intent, not a cloud rename. Include only authorized pages that still need generation; do not add the completed representative page again.

```bash
node "$VIBBIT_SKILL_DIR/scripts/comic-batch.js" plan --manifest /absolute/private/comic/batch.json
node "$VIBBIT_SKILL_DIR/scripts/comic-batch.js" run --manifest /absolute/private/comic/batch.json --state-dir /absolute/private/comic/batch-state --concurrency 3
```

Reuse the execution environment's configured account through the shared client. Offline plan reads no credentials, sends no requests and writes no records. New state directories use 0700 and records 0600; existing directories must be private and owned. Use one directory per batch and one scheduler process. Resume with the same manifest, requests and state directory. Intentional content/revision changes need a separate revision batch, preserving earlier records.

The scheduler recovers submitted pages before filling free slots. It spaces submissions without waiting for generation completion. At 3 remote-active tasks it polls existing IDs; a completed page frees a slot immediately rather than waiting for the slowest page. Queries have bounded concurrency and at least 5 seconds between checks for each task. Retained completed results avoid extra queries, authentication and generation. The limit covers this batch only, not all batches, Agents or account activity.

Each invocation admits at most **6 new pages** and waits up to **50 seconds** by default. The Agent checks newly completed pages for shared problems, then continues the same command without asking the user to say "continue" again. If nothing new completed, continue following existing records. Stop admitting pages when a shared problem appears and revise unsubmitted pages in a new revision batch. Adjust `--max-new` to the review cadence. `--concurrency` accepts 1–8 but must respect known account limits; start at 3 when unknown and reduce after throttling instead of launching all 30 pages.

To follow existing tasks without admitting new generations:

```bash
node "$VIBBIT_SKILL_DIR/scripts/comic-batch.js" run --manifest /absolute/private/comic/batch.json --state-dir /absolute/private/comic/batch-state --query-only
```

## Recovery, review and delivery

- Each page uses the existing duplicate-submission journal. An uncertain write without a task ID stops new submissions; do not change identifiers and POST again. Continue read-only queries for known tasks. Throttling, authentication, credits or record errors also pause admissions without changing models, increasing requests or deleting records.
- Definitive failures affect only their pages. Preserve successes and pending tasks. Follow [task recovery](task-lifecycle.md) before retrying a rejected page; this tool never repeats its POST automatically. Prepare only failed-page revision/retry batches within authorization, without resubmitting the whole work.
- Normal exit releases the batch lock. After abrupt host termination, inspect its PID and verify the original process has exited before removing a stale lock. Preserve journals and never remove a live process lock.
- Output distinguishes total, completed, failed, active, unsubmitted and unknown pages. `wait_window`/`review_checkpoint` do not mean the comic is finished. Inspect actual images through each `result_file`; completion does not prove quality.
- Generation, review and file preparation can overlap when the host permits. Lower concurrency under resource pressure. Deliver in page order, not completion order, preserving character, setting, exact text and neighboring-page continuity checks.
- Apply [image archiving](image-archiving.md), verify actual 1K dimensions and keep each delivered image strictly below `1,500,000` bytes. Concurrency does not remove checks or justify regeneration to repair records.

Measure preparation, queue/generation, queries, review/revision and export separately. Report actual elapsed time and generation counts. Simulated scheduling or concurrency values do not prove proportional service speedups; backend queues, quotas and revisions can still dominate.
