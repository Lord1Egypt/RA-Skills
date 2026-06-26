---
name: sora-2-generate
description: "Generate videos with the NanoPhoto.AI Sora 2 API in text-to-video or image-to-video mode. Use when: (1) User wants to create a Sora 2 video from a prompt, (2) User provides one or more public image URLs and wants image-to-video generation, (3) User mentions Sora 2, NanoPhoto video generation, text to video, image to video, cinematic prompt generation, or checking Sora generation status. Supports submission, status checks, and optional in-process polling from a single bundled script. Prerequisite: Obtain an API key at https://nanophoto.ai/settings/apikeys and configure env.NANOPHOTO_API_KEY."
homepage: https://nanophoto.ai
metadata: {"openclaw":{"homepage":"https://nanophoto.ai","requires":{"env":["NANOPHOTO_API_KEY"]},"primaryEnv":"NANOPHOTO_API_KEY"}}
---

# Sora 2 Generate

Generate videos through the NanoPhoto.AI Sora 2 API.

## Prerequisites

1. Obtain an API key at: https://nanophoto.ai/settings/apikeys
2. Configure `NANOPHOTO_API_KEY` before using the skill.
3. Do not paste the API key into chat; store it in the platform's secure env setting for this skill.

Preferred OpenClaw setup:

- Open the skill settings for this skill
- Add an environment variable named `NANOPHOTO_API_KEY`
- Paste the API key as its value

Equivalent config shape:

```json
{
  "skills": {
    "entries": {
      "sora-2-generate": {
        "enabled": true,
        "env": {
          "NANOPHOTO_API_KEY": "your_api_key_here"
        }
      }
    }
  }
}
```

Other valid ways to provide the key:

- **Shell**: `export NANOPHOTO_API_KEY="your_api_key_here"`
- **Tool-specific env config**: any runtime that injects `NANOPHOTO_API_KEY`
- **OpenClaw config fallback**: the bundled script also falls back to `~/.openclaw/openclaw.json` at `skills.entries.sora-2-generate.env.NANOPHOTO_API_KEY`

Credential declaration summary:

- Primary credential: `NANOPHOTO_API_KEY`
- Resolution order in the bundled script: `--api-key` → `NANOPHOTO_API_KEY` environment variable → `~/.openclaw/openclaw.json` skill env
- No unrelated credentials are required

## Choose the mode

- Use `textToVideo` when the user gives only a prompt.
- Use `imageToVideo` when the user provides one or more **public image URLs**.
- Do **not** use local image files or base64 images for the API. The API only accepts public `imageUrls`.

## Recommended workflow

1. Collect the prompt.
2. Decide `mode`: `textToVideo` or `imageToVideo`.
3. Choose `modelTier`, `aspectRatio`, and `videoDuration`.
   - Default to `sora2`.
   - Use `sora2-pro-standard` or `sora2-pro-high` only if the user explicitly wants the pro tier or higher resolution output.
4. Submit the generation request.
5. If the user wants synchronous progress output in the same process, use `submit --follow`.
6. Wait 120 seconds before the first status check, then check every 20 seconds until `completed` or `failed`.
7. Return the final `videoUrl`, generation time, and credits used when available.
8. Expect real-world wait time to vary from roughly 120 seconds to 480 seconds depending on queue/load, model tier, and prompt complexity; avoid short timeouts.

## Preferred commands

Use the single bundled script with subcommands.

### Submit only

```bash
python3 scripts/sora2_generate.py submit \
  --prompt "A golden retriever running on a beach at sunset, cinematic lighting" \
  --mode textToVideo \
  --model-tier sora2 \
  --aspect-ratio landscape \
  --video-duration 10
```

### Submit and keep polling in the same process

```bash
python3 scripts/sora2_generate.py submit \
  --prompt "A golden retriever running on a beach at sunset, cinematic lighting" \
  --mode textToVideo \
  --model-tier sora2 \
  --aspect-ratio landscape \
  --video-duration 10 \
  --follow
```

### Check status of an existing task

```bash
python3 scripts/sora2_generate.py status --task-id task_abc123
```

### Image to video

```bash
python3 scripts/sora2_generate.py submit \
  --prompt "The person in the painting comes alive, moving naturally and reciting poetry" \
  --mode imageToVideo \
  --image-url https://static.nanophoto.ai/demo/nano-banana-pro.webp \
  --model-tier sora2 \
  --aspect-ratio landscape \
  --video-duration 10
```

## Script behavior

The bundled script resolves credentials in this order: `--api-key`, then `NANOPHOTO_API_KEY` from the environment, then `~/.openclaw/openclaw.json` at `skills.entries.sora-2-generate.env.NANOPHOTO_API_KEY`.

Subcommands:

- `submit`: submit a task
- `submit --follow`: submit and keep polling in the same process
- `status`: check an existing `taskId`

Cross-platform note:

- Use `python3` on macOS/Linux.
- Use `python` on Windows unless `python3` is available.
- The script uses Python's standard HTTP client and does not require `curl`.
- Use `--json-only` when another script/tool needs raw JSON output.
- Use `--initial-status-delay` to override the default 120-second wait before the first status check.
- Use `--status-check-interval` to override the default 20-second interval between progress checks.
- Default max wait is 1200 seconds.

## Manual API calls

### Submit generation

```bash
curl -X POST "https://nanophoto.ai/api/sora-2/generate" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $NANOPHOTO_API_KEY" \
  --data-raw '{
    "prompt": "A golden retriever running on a beach at sunset, cinematic lighting",
    "mode": "textToVideo",
    "modelTier": "sora2",
    "aspectRatio": "landscape",
    "videoDuration": "10"
  }'
```

### Check status

```bash
curl -X POST "https://nanophoto.ai/api/sora-2/check-status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $NANOPHOTO_API_KEY" \
  --data-raw '{"taskId": "task_abc123"}'
```

## Parameter guidance

- `modelTier`
  - `sora2`: default; lowest cost and fastest turnaround
  - `sora2-pro-standard`: 720p pro tier; use only when explicitly requested
  - `sora2-pro-high`: 1080p pro tier; use only when explicitly requested
- `aspectRatio`
  - `portrait`: vertical/default
  - `landscape`: horizontal
- `videoDuration`
  - `10`
  - `15`

## Error handling

| errorCode | Cause | Action |
|-----------|-------|--------|
| `LOGIN_REQUIRED` | Invalid or missing API key | Verify key at https://nanophoto.ai/settings/apikeys |
| `API_KEY_RATE_LIMIT_EXCEEDED` | Rate limit exceeded | Wait and retry |
| `INSUFFICIENT_CREDITS` | Not enough credits | Top up credits |
| `PROMPT_REQUIRED` | Missing prompt | Ask user for a prompt |
| `IMAGE_REQUIRED` | Missing image for image-to-video | Ask for public image URLs |
| `IMAGE_URLS_REQUIRED` | API needs `imageUrls` | Do not send base64 or local file paths |
| `TASK_NOT_FOUND` | Invalid or expired task ID | Re-submit or verify ownership |
| `GENERATION_FAILED` | Server-side failure | Retry or try a simpler prompt |

## Bundled files

- `scripts/sora2_generate.py`: single entry point for submit, status, and optional in-process polling.
- `references/api.md`: condensed API reference, costs, and response shapes.
