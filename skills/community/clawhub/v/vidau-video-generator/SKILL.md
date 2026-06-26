---
name: vidau video generator
version: "1.0.8"
license: MIT
description: Use Vidau Open API to generate short videos with Veo3, Sora2, and other models, or query account credits. Register at superaiglobal.com and configure API Key.
homepage: https://vidau.ai
metadata:
  openclaw:
    requires:
      env: ["VIDAU_API_KEY"]
    primaryEnv: "VIDAU_API_KEY"
    homepage: "https://doc.superaiglobal.com/en/overview/introduction"
compatibility: Python 3.x required; network access to api.superaiglobal.com
---

# Vidau Video Generator 

**Version:** 1.0.8

## When to use

- User asks to "generate a video", "create a short video with Veo3/Sora", "generate video from this prompt/image", "make a clip from this script", etc.
- User asks "how many credits do I have", "check my Vidau balance", "query Vidau credits", etc.
- User asks to "check my video task status", "has my Vidau task finished", "query task by UUID", etc.

## When NOT to use

- User only wants to edit or process existing local video files (e.g. trim, merge, transcode) without calling any cloud API.
- User asks for a different video API (e.g. Runway, Pika) by name; use that provider’s skill if available.
- User has not mentioned Vidau/Veo/Sora/Seedance or "generate video" / "create video" and is only discussing concepts or other tools.

## Reply language

When returning results (video link, credits, or error message) to the user, use the same language as the user’s question (e.g. Simplified Chinese if they asked in Chinese, English if they asked in English).

## Output format (task success)

When a video task succeeds, return:

- **Video URL** (verbatim, from `[VIDAU_VIDEO_URL]` … `[/VIDAU_VIDEO_URL]`)
- **Thumbnail URL** (verbatim, from `[VIDAU_THUMB_PATH]` … `[/VIDAU_THUMB_PATH]`)

**Always present both URLs in a code block** so they are preserved verbatim and less likely to be altered by downstream processing. Example:

```
Video URL: <paste exact URL from script output>
Thumbnail URL: <paste exact URL from script output>
```

Do not rewrite, truncate, or wrap the URLs in other markup; copy them exactly from the script output.

## Prerequisites

Environment variable `VIDAU_API_KEY` must be set (injected by OpenClaw from `skills.entries.vidau.apiKey` or `env`). If the user has no API key, they must register at [https://www.superaiglobal.com/](https://www.superaiglobal.com/) to get one. Do not trigger this skill if it is not configured.

## Environment check

Before running any script, ensure Python 3 is available:

1. Run `python3 --version` or `python --version`. If either succeeds, use that command when invoking the scripts below.
2. If both fail, try to install Python for the current platform:
   - **macOS**: `brew install python3` (requires Homebrew).
   - **Linux (Debian/Ubuntu)**: `sudo apt-get update && sudo apt-get install -y python3`.
   - **Windows**: `winget install Python.Python.3.12` if available; otherwise tell the user to download and run the installer from [python.org](https://www.python.org/downloads/).
3. If install fails (e.g. no permission or unsupported OS), reply with a short message that Python 3 is required and link to [python.org/downloads](https://www.python.org/downloads/), then stop. Do not run the Vidau scripts until Python is available.

The scripts use only the standard library; no pip packages are required.

## Available scripts

- **`scripts/query_credit.py`** — Query current available credits; no args; outputs JSON with `data.availableCredit`, `data.userId`.
- **`scripts/query_models.py`** — Query model list and capability config; no args (optional `--no-cache` to force refresh); outputs JSON with `data` array. Each item has `model`, `scaleList`, `durationList`, `resolutionList`, `generateAudio`. Cached 10 minutes (env `VIDAU_MODELS_CACHE` or `~/.vidau_models_cache.json`). Use before create_task to validate user parameters. After new models or capability changes, use `--no-cache` to force refresh so the agent does not validate against a stale list.
- **`scripts/upload_asset.py`** — Upload a local file (image or video) to Vidau; outputs JSON with `data.url` and `data.assetId`. Use `data.url` as `--image-url` / `--last-image-url` / `--ref-image-urls` in create_task when the user only has a local file. Caches by file content hash (default `~/.vidau_asset_cache.json`, override with env `VIDAU_ASSET_CACHE`) so the same file is not re-uploaded.
- **`scripts/create_task.py`** — Create video task; required `--prompt`, optional `--model`, etc.; outputs JSON with `data.taskUUID`.
- **`scripts/wait_task.py`** — Poll until task succeeds or fails (or timeout); required `--task-uuid`; optional `--interval` (default 10s), `--timeout` (default 600s = 10 min). On success outputs same JSON as query_task and the same `[VIDAU_VIDEO_URL]` / `[VIDAU_THUMB_PATH]` blocks. Exit code 0 = succeeded, 1 = failed, 2 = timeout. **Always use wait_task by default**; when using wait_task you do not need to handle DELETE_SCHEDULED_TASK.
- **`scripts/query_task.py`** — Query task status and result once; required `--task-uuid`; outputs JSON with `taskStatus`, and on success also prints `[VIDAU_VIDEO_URL]` / `[/VIDAU_VIDEO_URL]` and `[VIDAU_THUMB_PATH]` / `[/VIDAU_THUMB_PATH]` blocks. **Use query_task only when the platform requires scheduled polling.** When the task reaches `succeeded` or `failed`, the script prints `[OPENCLAW] DELETE_SCHEDULED_TASK task_uuid=<uuid>` to stderr so the platform can remove the scheduled polling task.

**Task polling (wait_task vs query_task):** By default always use `wait_task`; use `query_task` only when the platform requires scheduled task polling. When using `wait_task`, there is no need to handle `DELETE_SCHEDULED_TASK`.

## Workflow (generate video)

1. **Optional**: Call `scripts/query_credit.py` to check `availableCredit` before creating a task to avoid failures due to insufficient credits.
2. **If the user only has a local image/video** (no URL yet): Call `scripts/upload_asset.py <path>` to upload the file; read `data.url` from stdout and use it as `--image-url`, `--last-image-url`, or in `--ref-image-urls` when calling create_task.
3. **Validate parameters against model capabilities**: Call `scripts/query_models.py` to get the model list (cached 10 min). Find the entry in `data` where `model` equals the chosen `--model`. Validate user inputs (resolution, ratio, duration, generate_audio) against that entry:
   - **resolution**: must be in the model’s `resolutionList`. If not, do not create the task; tell the user the resolution is not supported and list the allowed values (e.g. `resolutionList`).
   - **ratio** (if user specified one): must be in the model’s `scaleList`. If not, do not create the task; tell the user the ratio is not supported and list the allowed values (e.g. `scaleList`).
   - **duration** (if user specified one): for the chosen resolution, allowed durations are in `durationList[resolution]` (e.g. `durationList["1080p"]` = `[5, 10]`). If the user’s duration is not in that list, do not create the task; tell the user the duration is not supported for this resolution and list the allowed durations (e.g. for 1080p: 5, 10 seconds).
   - **generate_audio** (if user requested true): the model entry’s `generateAudio` must be true. If it is false, do not create the task; tell the user this model does not support audio generation.
   If any check fails, reply with what does not meet requirements and the allowed values; **do not** change the user’s parameters automatically and **do not** call create_task. If the chosen model is not in the list, skip validation and proceed to create_task.
4. Call `scripts/create_task.py` with `--prompt` (required), `--resolution` (required), `--model` (default `veo@3:normal`), and optional args (see parameter table below).
5. Read `data.taskUUID` from the script’s stdout JSON.
6. **Always use wait_task by default**: run `scripts/wait_task.py --task-uuid <taskUUID>` to poll until done (default 10s interval, 10 min timeout). When using wait_task **you do not need to handle DELETE_SCHEDULED_TASK**. **Only when the platform requires scheduled polling** use `scripts/query_task.py --task-uuid <taskUUID>` and, when the task reaches a terminal state, remove the scheduled task using the `[OPENCLAW] DELETE_SCHEDULED_TASK task_uuid=<uuid>` line on stderr.
7. **Success**: Return the video and thumbnail links to the user per **Output format (task success)** above: copy URLs verbatim from the script output blocks and present them in a code block. **Failure**: Explain using the API `message` or error code (e.g. insufficient credits, policy violation).

## Workflow (query credits)

When the user asks for balance, call `scripts/query_credit.py` (no args), read `data.availableCredit` from stdout JSON and reply; optionally include `data.userId`.

## Parameters (create_task.py)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--prompt` | Yes | Text description, up to 2000 characters |
| `--model` | No | Default `veo@3:normal`; see model list below |
| `--negative-prompt` | No | Negative prompt, up to 2000 characters |
| `--image-url` | No | First-frame image URL |
| `--last-image-url` | No | Last-frame image URL |
| `--duration` | No | Video duration in seconds |
| `--generate-audio` | No | Whether to generate audio; true/false |
| `--seed` | No | Random seed |
| `--resolution` | Yes | Resolution, e.g. `720p`, `1080p` |
| `--ratio` | No | Aspect ratio, e.g. `16:9`, `9:16` |

**Defaults when unspecified**: 720p / 8s / 16:9 (see [references/parameters.md](references/parameters.md)). **Note**: `create_task` currently requires passing `--resolution` explicitly; the agent must always include this parameter for consistent behavior.

Valid values: `resolution` and `ratio` are constrained by the model’s capability (see workflow step 3 and [references/capabilities.md](references/capabilities.md)). See [references/parameters.md](references/parameters.md) for more detail. Run `python scripts/create_task.py --help` for full parameters.

## Model list

Common model IDs (aligned with API):

- **Veo 3**: `veo@3:normal`
- **Veo 3.1**: `veo@3.1:normal`, `veo@3.1:fast`
- **Sora 2**: `sora@2:normal`, `sora@2:pro`
- **Seedance**: `seedance@1:pro`, `seedance@1:pro_fast`
- **Wan 2.5**: `wan@2.5:preview`
- **Vidu Q2**: `vidu@q2:turbo`, `vidu@q2:pro`

See [references/models.md](references/models.md) for more models and use cases.

## Error handling

- If `VIDAU_API_KEY` is not set, scripts exit with an error; tell the user to register at [https://www.superaiglobal.com/](https://www.superaiglobal.com/) to get an API key, then configure it in OpenClaw.
- When API or script returns an error, relay the API `message` first, then use the one-sentence user message below. Reply in the user’s language.

| Code / Case | One-sentence user message |
|-------------|---------------------------|
| `CreditInsufficient` | Insufficient credits; please top up in the Vidau console and try again. |
| `TaskPromptPolicyViolation` | The prompt may violate content policy; please revise and retry. |
| `ImageDownloadFailure` | Image URL could not be downloaded; ensure the link is publicly accessible. |
| `VIDAU_API_KEY` not set | Please register at superaiglobal.com to get an API Key and configure it in OpenClaw. |
| HTTP 401 | API Key is invalid or expired; please check in the Vidau console. |
| HTTP 429 | Too many requests; please try again later. |
| Other 4xx/5xx | The API returned an error; please retry later or contact support. |

See [references/errors.md](references/errors.md) for details.

## Example usage

- **Generate video**: User says e.g. "Generate an 8s video with Veo3 from this script" or "Generate a 10s sunset beach clip with Sora2". Agent: (optional) `query_credit.py` → `query_models.py` → validate resolution/ratio/duration/audio against model capabilities (step 3); if invalid, tell user and stop; else `create_task.py --prompt "..." --resolution 720p --duration 8 --model veo@3:normal` → read `taskUUID` → `wait_task.py --task-uuid <uuid>` → return video URL from output blocks or explain failure.
- **Local image as first frame**: User has only a local image file. Agent: `upload_asset.py /path/to/image.png` → read `data.url` from stdout → `create_task.py --prompt "..." --resolution 720p --image-url "<data.url>"` → then wait_task as above.
- **Query credits**: User says e.g. "How many Vidau credits do I have?" or "Check my Vidau balance". Agent: `query_credit.py` → reply with `data.availableCredit` (and optionally `data.userId`).
- **Check task**: User says e.g. "Is my video task done? UUID is xxx". Agent: use `wait_task.py --task-uuid xxx` by default → return status or video link (no need to handle DELETE_SCHEDULED_TASK). Use `query_task.py` only when the platform requires scheduled polling, and remove the scheduled task on terminal state via DELETE_SCHEDULED_TASK on stderr.
