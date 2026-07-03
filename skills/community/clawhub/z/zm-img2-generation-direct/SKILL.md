---
name: zm-img2-generation-direct
version: 1.0.0
description: ZM IMG2 直接生图执行。用于通过 happy/gpt-image-2 执行文生图和参考图生图，保留输入、输出、日志和结果 JSON，作为正式视觉生产证据。
metadata:
  openclaw:
    emoji: "🖼️"
    requires:
      bins:
        - python3
        - node
      config:
        - models.providers.happy
---

# Happy IMG2 Direct Skill

Generate real images through the configured Happy OpenAI-compatible image API. This skill is standardized for the provider/model pair `happy/gpt-image-2` and has no local fake-image fallback.

## Supported capabilities

> Naming rule: use business-facing names first.
> - **text2img / 文生图**: prompt-only image generation. Internally this routes to `/images/generations`.
> - **img2img / 参考图生图**: prompt plus one or more reference/input images. Internally this routes to `/images/edits`.
> Avoid using raw endpoint names (`generations` / `edits`) as the primary wording in task briefs or user-facing reports unless diagnosing the API layer.

- **text2img / 文生图**: prompt-only generation.
- **img2img / 参考图生图**: prompt plus one or more reference/input images.
- **Multiple reference images**: up to **5 total** reference images per task.

## Defaults and provider rules

- provider: `happy` unless `OPENCLAW_IMAGE_PROVIDER` is set or `--provider` is explicitly supplied by a controlled caller.
- model: `gpt-image-2` unless `OPENCLAW_IMAGE_MODEL` is set or `--model` is explicitly supplied; the approved pair is **`happy/gpt-image-2`**.
- size: `1024x1024`.
- timeout: `600000ms` per image request.
- output: `<openclaw-home>/generated-images/`.
- no CSS/HTML/screenshot rendering path.
- no old-image collage/splice fallback.
- no non-Happy model fallback.
- no built-in message delivery; send or attach files using normal OpenClaw/channel tools.

Acceptance-sensitive production tasks must stay on `happy/gpt-image-2`; do not switch to non-Happy providers or substitute local/mock images.

## Routing rules

- **text2img / 文生图**: no reference images → internally call `/images/generations` (`mode: generation`).
- **img2img / 参考图生图**: any reference image present → internally call `/images/edits` (`mode: edit`).

A successful `result.json` must expose enough proof for review: `provider`, `model`, internal `mode`, and `input_images` (empty for text2img / 文生图, populated for img2img / 参考图生图).

## Single image

```bash
python3 skills/zm-img2-generation-direct/scripts/run.py \
  --prompt "A realistic photo of an orange cat sitting by a window, no text, no watermark" \
  --task-name "cat-test" \
  --no-send
```

Useful flags:

- `--prompt` required.
- `--task-name` output filename prefix and run directory prefix.
- `--input-image` / `--image` / `--reference-image` optional reference image path for img2img / 参考图生图; repeatable.
- `--images` optional JSON array or comma-separated reference image paths.
- Reference images from all aliases are combined; **max 5 total**.
- `--provider` provider key in OpenClaw config, default `happy`.
- `--model` image model, default `gpt-image-2` (approved as `happy/gpt-image-2`).
- `--size` default `1024x1024`.
- `--timeout-ms` default `600000`.
- `--output-dir` default `<openclaw-home>/generated-images`.
- `--max-attempts` default `3`, maximum `5`.
- `--retry-base-delay`, `--retry-max-delay`, `--retry-jitter`.
- `--raw` marker for callers that intentionally keep the user prompt unchanged.
- `--no-send` accepted for compatibility; this public skill always leaves delivery to the caller.

Example with a reference image / img2img 参考图生图:

```bash
python3 skills/zm-img2-generation-direct/scripts/run.py \
  --prompt "Keep the cat and dog character identity, redraw them in a clean warm handbook scene, no readable text" \
  --input-image /absolute/path/reference.png \
  --task-name "catdog-i2i-test" \
  --no-send
```

Example with multiple references:

```bash
python3 skills/zm-img2-generation-direct/scripts/run.py \
  --prompt "Preserve the product shape and color palette from the references; create a clean studio image, no text" \
  --reference-image /absolute/path/product.png \
  --reference-image /absolute/path/style.png \
  --images '["/absolute/path/material.png"]' \
  --task-name "multi-ref-test" \
  --no-send
```

## Batch images

```bash
python3 skills/zm-img2-generation-direct/scripts/batch_run.py @batch.json
```

Example:

```json
{
  "batch_name": "article-covers",
  "max_workers": 4,
  "timeout_ms": 600000,
  "send_to_feishu": false,
  "tasks": [
    {"task_name": "cover-1", "prompt": "Realistic shop counter photo, no readable text"},
    {"task_name": "cover-2", "prompt": "Realistic office desk photo, no readable text"},
    {"task_name": "character-redraw", "prompt": "Keep the character identity, redraw in a clean warm scene, no text", "input_image": "/absolute/path/reference.png"},
    {"task_name": "multi-ref", "prompt": "Use the character and outfit references, clean non-text scene", "images": ["/absolute/path/character.png", "/absolute/path/outfit.png"]}
  ]
}
```

Batch rules:

- bounded concurrency, current hard maximum `4`.
- bounded queue, default/maximum `200` tasks.
- each item has its own task directory, `state.json`, stdout/stderr logs, and `result.json`.
- one failed image does not prevent other scheduled images from finishing.
- final `batch_result.json` records success/failure per task.
- batch task reference fields: `input_image`, `image`, `reference_image`, or `images` (list or comma-separated string); max 5 total.
- delivery is disabled in the public version; use OpenClaw/channel tools to send files.


## Controlled image queue (`image_queue.py`)

`image_queue.py` is the minimal production-safe queue wrapper for `happy/gpt-image-2`. It does **not** replace `run.py`; it runs the same direct generator with bounded concurrency and observable task state.

### Defaults

- `max_workers`: `4` (hard-capped at 4)
- `task_timeout_seconds`: `600`; timeout handling is terminate first, then kill if the process ignores terminate
- `max_queue_size`: `100`; once `max_workers + max_queue_size` accepted tasks is exceeded, extra tasks are marked `rejected`
- State directory: `<openclaw-home>/image-queue` or `--state-dir`
- Output directory: `<openclaw-home>/generated-images` or `--output-dir`

### Submit tasks

Single task:

```bash
python3 skills/zm-img2-generation-direct/scripts/image_queue.py run \
  --prompt "Clean product image, no readable text" \
  --task-name product-001 \
  --task-key product-001 \
  --no-send
```

JSON batch:

```bash
python3 skills/zm-img2-generation-direct/scripts/image_queue.py run @tasks.json \
  --max-workers 4 \
  --task-timeout-seconds 600 \
  --max-queue-size 100
```

`tasks.json`:

```json
{
  "tasks": [
    {"task_name": "cover-1", "task_key": "cover-1", "prompt": "Realistic shop counter photo, no readable text"},
    {"task_name": "cover-2", "task_key": "cover-2", "prompt": "Clean office desk photo, no readable text"}
  ]
}
```

For tests only, use `mock_sleep` / `mock_command`; do not use these as image proof.

### Inspect and monitor

```bash
python3 skills/zm-img2-generation-direct/scripts/image_queue.py status --state-dir <openclaw-home>/image-queue
python3 skills/zm-img2-generation-direct/scripts/image_queue.py list --state-dir <openclaw-home>/image-queue
python3 skills/zm-img2-generation-direct/scripts/image_queue.py list --state-dir <openclaw-home>/image-queue --status completed
python3 skills/zm-img2-generation-direct/scripts/image_queue.py get --state-dir <openclaw-home>/image-queue <task_id_or_task_key>
python3 skills/zm-img2-generation-direct/scripts/image_queue.py history --state-dir <openclaw-home>/image-queue -n 50
```

`get` shows task metadata plus stdout/stderr tails and artifact paths.

### Artifacts and mapping

Every accepted or rejected task gets its own directory under:

```text
<state-dir>/tasks/<task_id>/
```

Important files:

- `task.json`: latest task metadata
- `command.json`: command used to invoke `run.py` or mock command
- `stdout.txt` / `stderr.txt`: process output
- `result.json`: final task result

The queue records `task_id`, `task_key`, `worker_id`, `thread_id`, and child `pid` in `queue_state.json`, `task.json`, and final task rows. Completed tasks verify the worker binding before accepting the result; late/orphan output is marked non-ok.

### Status meanings

- `completed`: child process exited successfully and returned/printed an ok result
- `failed`: child process exited non-zero or returned `ok: false`
- `timed_out`: exceeded `task_timeout_seconds`; queue sent terminate, then kill if needed
- `rejected`: invalid task or queue full
- `skipped`: duplicate `task_key` already active in the same submission/run
- `orphan_late_output`: worker binding mismatch / late result; not acceptable
- `cancelled`: reserved for queued-task cancellation in persisted state

`summary.ok` is true only when there are no `failed`, `timed_out`, `rejected`, `skipped`, `orphan_late_output`, `orphaned`, `cancelled`, or `stuck` tasks.

### Duplicate and queue-full behavior

Within a run, `task_key` is unique among active `queued`/`running` tasks. A duplicate active key is `skipped` and makes `summary.ok=false`.

Capacity is `max_workers + max_queue_size`. With defaults, up to 104 tasks can be accepted at once (4 running, 100 waiting). Additional tasks are explicitly `rejected`; there is no silent discard.

### Cancel support and current limits

This is a minimal non-daemon runner. It is intended for one foreground bounded run at a time.

```bash
python3 skills/zm-img2-generation-direct/scripts/image_queue.py cancel --state-dir <openclaw-home>/image-queue <task_id_or_task_key>
```

Current `cancel` can mark a persisted `queued` task as `cancelled`. Running tasks are supervised inside the active `run` process and are automatically terminated on timeout; out-of-process safe running cancellation is intentionally not implemented in this minimal version.

### Current limitations

Deferred by design to keep the tool small and safe:

- no long-lived daemon or cross-process scheduling
- no complex runner crash recovery
- no disk-space threshold check
- no stdout/stderr rotation; use normal-size logs and inspect `stdout.txt` / `stderr.txt`
- no lock TTL files
- no separate watchdog/heartbeat beyond timeout-based supervision

For production use, submit bounded batches, keep `task_key` stable, watch `status/list/get`, and treat any non-completed status as requiring review before accepting images.

## Standard artifacts

For each single-image run:

- generated image file (`.png` by default).
- run directory under `<output-dir>/_runs/<task-name>-<timestamp>/`.
- run-level `state.json` with status, attempt, elapsed time, output, and redacted last error.
- per-attempt `request.json`, `result.json`, `stdout.txt`, and `stderr.txt`.

For each batch run:

- batch directory under `content-factory/live-course-design/img2/batches/`.
- `batch_request.json` and final `batch_result.json`.
- per-task directory with `batch_task.json`, `state.json`, stdout/stderr logs, and `result.json`.

Report recommendation for acceptance reviews: include the image path, run/batch directory, `result.json` or `batch_result.json`, and the visible proof fields `provider`, `model`, `mode`, `input_images`, `ok`, and `bytes`.

## Acceptance rules

A result is acceptable only when:

- `ok: true` is present.
- `provider` proves Happy usage (`happy`).
- `model` proves `gpt-image-2` under the Happy provider (`happy/gpt-image-2` as provider/model pair).
- `mode` matches routing: `generation` for text2img / 文生图 with no reference images, `edit` for img2img / 参考图生图 with reference images.
- `input_images` is present and accurate.
- the artifact is a newly generated image from the API response.

A result is **not** acceptable if it:

- uses CSS/HTML rendering, webpage screenshots, SVG/canvas export, or manual compositing as the final image.
- reuses, crops, splices, or collages old images to impersonate a new generation.
- switches to a non-Happy provider/model or silently falls back to a mock/local generator.
- lacks provider/model/mode/input-image proof in the run artifacts.

## Safety style requirements

For adult anthropomorphic, sexy, glamour, or similar requests, keep outputs non-explicit and non-pornographic:

- no nudity or exposed sexual focus areas.
- no transparent/see-through clothing.
- no explicit sexual acts.
- no clearly provocative sexual pose or framing.
- prefer tasteful fashion/editorial language: clothed, non-explicit, adult, safe-for-work, no fetish emphasis.

If the user prompt is ambiguous, strengthen the prompt with safe constraints rather than producing explicit content.

## Retry behavior

Retries are limited and only used for retryable failures:

- timeout.
- upstream failures.
- rate limits.
- HTTP `408/429/500/502/503/504`.
- wrapper parse errors.

Non-retryable errors, such as invalid requests or auth failures, fail fast with redacted diagnostics.

## Lightweight validation / self-check

Do not run bulk generation for documentation checks. Use lightweight commands:

```bash
python3 skills/zm-img2-generation-direct/scripts/run.py --help
python3 skills/zm-img2-generation-direct/scripts/batch_run.py --help
python3 -m py_compile skills/zm-img2-generation-direct/scripts/run.py skills/zm-img2-generation-direct/scripts/batch_run.py
node --check skills/zm-img2-generation-direct/scripts/generate-image.js
```

For actual acceptance, inspect the produced `result.json` and verify `ok`, `provider`, `model`, `mode`, and `input_images`.

## Safety and publishing notes

This skill intentionally contains no private OpenClaw IDs, no hard-coded user paths, no API keys, and no channel recipient IDs. It reads provider configuration from the local OpenClaw config at runtime.
