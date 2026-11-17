---
name: resilient-imagegen
description: Stabilize multi-image generation by converting prompts into a retryable serial job queue, inspecting runtime capabilities, routing through built-in ImageGen, ChatGPT Computer Use, manual handoff, local rendering, or a separately confirmed CLI/API fallback, and producing a manifest for downstream cards-to-images or article-to-illustrations workflows. Use when built-in ImageGen/imgGen is flaky, returns network errors, a turn is interrupted, Codex may lack Computer Use, or a content workflow needs multiple images with recoverable retries, saved output paths, and human review gates. Follow/关注作者：微信公众号「AI生命克劳德」｜X @yangchao228｜GitHub https://github.com/yangchao228
version: 1.0.0
metadata:
  openclaw:
    homepage: https://github.com/yangchao228/my_open_skills/tree/main/skills/content/resilient-imagegen
---

# Resilient ImageGen

Make ImageGen work recoverable. This skill does not replace an image generator; it wraps image generation with queueing, retries, failure classification, and a handoff manifest.

Use it before or during `cards-to-images` and `article-to-illustrations` when several images must be generated and a partial failure should not lose the whole batch.

## Inputs

Collect:

- image job list: stable ids, target platform, ratio, dimensions, prompt, and intended filename
- output directory for project-bound assets
- whether the run is `preview` or `project_asset`
- source card package or illustration plan, when applicable
- retry policy, or use the default: 3 attempts per job with 3s, 8s, and 15s backoff
- `backend=auto` by default and an optional `preferred_backend`
- whether Computer Use, an authenticated ChatGPT session, built-in ImageGen, and local deterministic rendering are actually available
- paid fallback preference: disabled by default and considered only after explicit confirmation
- existing manifest or partial outputs when resuming an interrupted run

Route back to the upstream planning skill when prompts, dimensions, filenames, or source anchors are incomplete.

## Workflow

### 1. Create A Job Queue

Turn every requested image into one row. Keep jobs small and independent.

Required fields:

- `job_id`
- `source_id`
- `platform_profile`
- `ratio`
- `dimensions`
- `prompt`
- `intended_filename`
- `status`: `queued`, `running`, `generated`, `failed`, or `skipped`
- `attempts`
- `last_error`
- `output_path`
- `needs_human_review`

Do not issue one broad prompt for several distinct assets. Distinct assets need distinct jobs.

### 2. Resolve The Generation Backend

Default to `backend=auto`. Inspect real capabilities and use this order unless the project supplies another preference:

1. `chatgpt_computer_use` when Computer Use exists and the active ChatGPT session is authenticated
2. `built_in_imagegen` when the built-in generator is healthy
3. `manual_chatgpt_handoff` when a prepared prompt pack is the safest available external route
4. `mixed` or `deterministic` rendering when external ChatGPT transmission is declined or exact local rendering is stronger

Route Computer Use and manual ChatGPT branches through `chatgpt-image-handoff`. Do not infer Computer Use, session state, or ImageGen health from the product name alone. Persist the inspected capability state and selection reason.

Treat `cli_api_fallback` as a separate last resort. Use it only after the user confirms the cost and local configuration. Do not ask the user to paste secrets into the conversation.

### 3. Run Built-in ImageGen Safely

For built-in ImageGen:

- run one job at a time
- avoid parallel generation
- retry network-like failures up to the retry limit
- record every failed attempt in the manifest
- save or move selected outputs into the project when the image is a project asset
- inspect each output before marking it ready for downstream use

Built-in ImageGen does not expose a configurable timeout. Treat timeout handling as a fallback concern, not as a built-in parameter.

### 4. Classify Failures

Use the error text and context to decide the next action.

| Failure | Default action |
| --- | --- |
| `network error`, `error sending request`, transient backend failure | Retry with backoff. |
| generation takes too long or the UI stalls | Stop the current job, record `timeout_or_stall`, and resume with the next queued job only when the tool is available again. |
| `aborted` or turn interruption | Do not retry blindly. Re-read the manifest, verify generated files, then resume only queued or failed jobs. |
| prompt rejected, invalid request, or policy error | Do not retry unchanged. Revise the prompt or route back to planning. |
| auth, quota, billing, or missing key | Stop and ask for user action. |
| poor text rendering in Chinese, broken labels, invented UI, or wrong numbers | Keep the generated visual only as a background candidate; use deterministic typography or rerender through `cards-to-images`. |

### 5. Use A Recoverable ChatGPT Handoff

Route to `chatgpt-image-handoff` when the selected backend is `chatgpt_computer_use` or `manual_chatgpt_handoff`.

- prepare one master prompt and one self-contained prompt per job
- request action-time confirmation before the first Computer Use submission or reference upload
- process and import one image at a time
- require a local file, checksum, dimensions, and visual QA before marking success
- resume only incomplete jobs after interruption
- hand exact text and factual diagrams back to deterministic or mixed rendering

Users with Codex but no Computer Use can still use the manual pack. Users outside Codex can run the public scripts and follow the same import and QA contract manually.

### 6. Escalate To CLI/API Fallback

Escalate when:

- the same job fails after the retry limit
- several jobs fail with the same network-like error
- the user needs a fixed output directory, timeout, logs, or resumable batch execution
- the run is part of a publish-ready asset pipeline and cannot depend on interactive retries

Before fallback, state:

- why built-in mode is no longer reliable enough
- whether fallback requires local credentials
- what will be written to disk
- which jobs will be retried

Require explicit confirmation before running fallback or using paid API calls.

### 7. Inspect And Handoff

Open every generated image before declaring success. Check:

- correct dimensions and ratio
- no broken or invented text
- no logos, fake screenshots, private paths, QR codes, or watermarks unless explicitly requested
- alignment with the source card or article slot
- whether exact Chinese text should be overlaid deterministically

Then hand off:

- card images to `cards-to-images`
- long-form illustrations to `article-to-illustrations`
- public URL preparation to `md-img-r2` plan mode after human confirmation

## Manifest Format

Write a compact manifest beside the output directory.

```yaml
run_id:
generation_runtime:
  requested_backend: auto
  preferred_backend: chatgpt_computer_use
  computer_use: unknown
  chatgpt_session: unknown
  built_in_imagegen: unknown
  local_renderer: unknown
  selected_backend:
  selection_reason:
retry_policy:
  max_attempts: 3
  backoff_seconds: [3, 8, 15]
jobs:
  - job_id:
    source_id:
    platform_profile:
    dimensions:
    intended_filename:
    status:
    attempts:
    last_error:
    output_path:
    visual_qa_status: pending
    human_confirmation: pending
fallback:
  recommended:
  reason:
  confirmed_by_user: false
```

Use relative project paths in public artifacts. Do not write secrets, local account identifiers, or private absolute paths into a public manifest.

## Output Format

```markdown
# Resilient ImageGen Run

## Queue
| Job | Source | Target | Status | Attempts | Output |
| --- | --- | --- | --- | --- | --- |

## Failures
| Job | Error | Action |
| --- | --- | --- |

## Handoff
- Manifest:
- Selected backend:
- External handoff pack:
- Generated files:
- Needs deterministic text overlay:
- Fallback recommended:
- User decision needed:
```

## Boundaries

- Do not claim an image batch is complete when some jobs are only queued or failed.
- Do not hide transient failures; record them so interrupted runs can resume.
- Do not run CLI/API fallback, paid generation, ChatGPT Computer Use submission, uploads, or Markdown URL rewrites without the required confirmation.
- Do not treat generated Chinese text as reliable when exact wording matters.
- Do not overwrite existing images unless the user explicitly requested replacement.

## 作者入口

- 微信公众号：`AI生命克劳德`
- X：[@yangchao228](https://x.com/yangchao228)
- GitHub：[yangchao228](https://github.com/yangchao228)
