---
name: weryai-video-toolkits
description: "Process and edit existing videos using WeryAI video toolkits. Use when the user needs to remove video backgrounds, replace backgrounds, apply anime style transfer (anime-replace), or check the status of these toolkit tasks. Features bounded wait polling for final outputs."
metadata: { "openclaw": { "emoji": "🎞️", "primaryEnv": "WERYAI_API_KEY", "paid": true, "network_required": true, "requires": { "env": ["WERYAI_API_KEY", "WERYAI_BASE_URL"], "bins": ["node"], "node": ">=18" } } }
---

# WeryAI Video Toolkits

WeryAI video tools, video editing, video post-processing, subtitle translate, subtitle erase, watermark remove, face change, lip sync, background remove, video extend, anime replace, magic style transfer, video upscale.

WeryAI video tools for video editing and video post-processing on existing videos.

Use this skill for official WeryAI video editing, video post-processing, and WeryAI video tools on existing video/media sources. Use when you need WeryAI video tools for subtitle translate, subtitle erase, watermark remove, face change, lip sync, background remove, video extend, anime replace, magic style transfer, or video upscale. This skill is intentionally strict about secret declaration and input safety: the only runtime secret is `WERYAI_API_KEY`, and media inputs support `http/https` URLs plus local/file sources that are uploaded first.

This is not a text-to-video generator. Use it when the user wants to edit, transform, clean up, translate, upscale, or extend an existing video with WeryAI rather than create a brand-new video from a prompt.

**Dependencies:** `scripts/video_toolkits.js` at the skill package root (alongside `SKILL.md`), `WERYAI_API_KEY`, and Node.js 18+. No other skills are required.

## Example Prompts

- `Remove the watermark from this HTTPS video with WeryAI.`
- `Translate the subtitles in this video to English and give me the final video URL.`
- `Use WeryAI to replace the face in this video with this reference photo.`
- `Extend this clip by 5 seconds in anime style.`
- `Lip-sync this talking-head video to the provided audio track.`

## Quick Summary

- Main jobs: `anime-replace`, `background-remove`, `extend`, `face-change`, `lips-change`, `magic-style`, `subtitle-erase`, `subtitle-translate`, `upscaler`, `watermark-remove`
- Main inputs: `video_url` plus tool-specific parameters such as `image_url`, `audio_url`, `target_language`, `rect_vo_list`, `style`, `resolution`, `duration`
- Main trust signals: dry-run support, explicit per-tool validation, parameter guidance by intent, paid-run warning, `WERYAI_API_KEY` alignment with other WeryAI skills

## Authentication and first-time setup

Before the first real processing run:

1. Create a WeryAI account.
2. Open the API key page at `https://www.weryai.com/api/keys`.
3. Create a new API key and copy the secret value.
4. Add it to the required environment variable `WERYAI_API_KEY`.
5. Make sure the WeryAI account has available balance or credits before paid processing.

### OpenClaw-friendly setup

- This skill already declares `WERYAI_API_KEY` in `metadata.openclaw.requires.env` and `primaryEnv`.
- After installation, if the runtime asks for required environment variables, paste the key into `WERYAI_API_KEY`.
- If you are configuring the runtime manually, export it before running commands:

```sh
export WERYAI_API_KEY="your_api_key_here"
```

### Quick verification

Use one safe check before the first paid run:

```sh
node scripts/video_toolkits.js tools
node scripts/video_toolkits.js wait --tool background-remove --json '{"video_url":"https://example.com/video.mp4"}' --dry-run
```

- `tools` confirms the local CLI is available and shows the supported tool registry.
- `--dry-run` validates the request shape without calling WeryAI or spending credits.

## Prerequisites

- `WERYAI_API_KEY` must be set before running `video_toolkits.js` for paid calls.
- Node.js `>=18` is required because the runtime uses built-in `fetch`.
- `video_url`, `image_url`, and `audio_url` can be `http/https` URLs or local/file sources. Local/non-http(s) sources are uploaded first.
- Real `submit`, `wait`, and `status` commands can consume WeryAI credits or depend on existing paid tasks.

## Security and API hosts

- **`WERYAI_API_KEY`**: Treat it as a secret. Configure it only in the runtime environment; never write the secret value into the skill files.
- This skill supports directly passing local file paths. If a local file path is provided, the runtime will automatically upload the local file to the WeryAI server for processing.
- Optional override `WERYAI_BASE_URL` defaults to `https://api.weryai.com`. Only override it with a trusted host.
- For higher assurance, run paid jobs in a short-lived shell or isolated environment, and review `scripts/video_toolkits.js` before production use.

## Tool Routing

Route user intent to the narrowest tool:

- Replace or move an object in anime style -> `anime-replace`
- Remove background or swap it to a flat color -> `background-remove`
- Continue a short clip -> `extend`
- Swap a face in a source video -> `face-change`
- Lip-sync video to audio -> `lips-change`
- Apply a preset visual style -> `magic-style`
- Remove subtitles or burnt-in text -> `subtitle-erase`
- Translate subtitles -> `subtitle-translate`
- Improve resolution -> `upscaler`
- Remove watermark -> `watermark-remove`

If the user asks for text-to-video or image-to-video generation from scratch, use `weryai-video-generator` instead of this skill.

## Parameter Guidance

Guide the user progressively. Ask only for the smallest missing set of parameters required for the selected tool.

### Recommended guidance pattern

Use short operator-style guidance like this:

- General help: When the user asks "how to use this skill", DO NOT paste raw shell commands. Instead, explain the capabilities in natural language and give 2-3 prompt examples.

### Defaults you may apply safely

- `anime-replace`: `type=replace`, `resolution=720p`
- `background-remove`: `background_color=BLACK`
- `extend`: `style=anime`, `resolution=720p`, `duration=5`
- `magic-style`: `video_style=anime_style_3`
- `upscaler`: `resolution=1080p`
- `subtitle-erase` and `watermark-remove`: omit `rect_vo_list` to let WeryAI auto-detect regions

### Parameters that usually require user confirmation

- `subtitle-translate.target_language`
- `face-change.image_url`
- `lips-change.audio_url`
- precise `rect_vo_list` region coordinates when auto-detection is not good enough

### When to ask follow-up questions

- Ask for `target_language` when the user says “translate subtitles” but does not name the destination language.
- Ask for the reference `image_url` when the user wants face replacement but has not supplied a face image.
- Ask for `audio_url` when the user wants lip-sync but has not supplied audio.
- Ask for `rect_vo_list` only when the user wants precise control over subtitle or watermark regions.
- Ask about `style`, `duration`, or `resolution` for `extend` only if the user wants something different from the default continuation setup.

## Tool Matrix

Read [references/video-tools-matrix.md](references/video-tools-matrix.md) when you need the exact required fields, enum values, or defaults for a tool.

## Preferred Commands

```sh
# Remove background with default BLACK fill
node scripts/video_toolkits.js wait --tool background-remove --json '{"video_url":"https://example.com/video.mp4"}'

# Replace or move an object in anime style
node scripts/video_toolkits.js wait --tool anime-replace --json '{"video_url":"https://example.com/video.mp4","image_url":"https://example.com/ref.jpg","type":"replace","resolution":"720p"}'

# Poll an existing task
node scripts/video_toolkits.js status --task-id <task-id>
```

## Workflow

1. Identify whether the user wants video editing/post-processing or brand-new video generation.
2. Route the request to one tool ID.
3. Collect `video_url` and only the extra parameters required by that tool.
4. Apply supported defaults where safe.
5. Show the final tool, parameters, and URLs before the paid run if the request is ambiguous or expensive.
6. Use `--dry-run` when you need to verify the payload locally first.
7. Use `wait` by default to deliver final processed video URLs in the same turn.
8. Enforce bounded polling with a maximum timeout of 30 minutes (1800 seconds); do not run unbounded loops.
9. If timeout is reached, return the `taskId` to the user and ask if they want you to check the status again. Do NOT show the raw node status command to the user; use it internally to check the status when asked.
10. Use `submit` only when the user explicitly wants task creation without polling.
11. Use `status` when the user already has a `task_id`.

## Input Rules

- `video_url`, `image_url`, and `audio_url` can be `http/https` URLs or local/file sources.
- Do not invent undocumented fields.
- Use normalized `rect_vo_list` coordinates between `0` and `1`.
- For subtitle or watermark removal, omit `rect_vo_list` when auto-detection is acceptable.
- For subtitle translation, use standard language codes such as `en`, `zh`, `ja`, `ko`, `fr`, `de`, `es`.

## Output

All commands print JSON to stdout. Successful results can include:

- `taskId`, `taskIds`, `batchId`
- `taskStatus`
- `videos`
- `requestSummary`
- `errorCode`, `errorMessage`

User-facing delivery requirement:

- If video URLs are available, return at least one playable Markdown link (for example `[Video](https://...)`). If multiple videos are generated, render all of them using markdown links consecutively.
- Alongside video output, include key parameters when available: `tool`, `style`, `duration`, `resolution`, `type`, `target_language`.
- Do not use `taskId` as the sole deliverable unless the user explicitly requested task creation without waiting.
- If timeout is reached before completion, return the `taskId` to the user and ask if they want you to check the status again. Do NOT show the raw node status command to the user; use it internally to check the status when asked.

The task is done when:

- local validation passes without CLI-side errors,
- `submit` returns a valid task ID or batch ID,
- or `wait` reaches a terminal result with at least one processed video URL,
- or `status` returns a clear in-progress or terminal state,
- and the output makes it explicit whether final video URLs are present.

## Constraints

- Do not treat this skill as a text-to-video generator.
- Do not ask the user to choose raw API fields when a safe default already fits the request.
- Do not use unsupported file types for `video_url`, `image_url`, or `audio_url`; local sources are uploaded before the toolkit request.
- Do not re-run paid processing casually because each `submit` or `wait` call can create a new paid task.
- Do not broaden this skill beyond the documented WeryAI video-tools API surface.

## Re-run behavior

- `submit` and `wait` are not idempotent.
- `status` and `tools` are safe to re-run.

## References

- Video tools parameter matrix: [references/video-tools-matrix.md](references/video-tools-matrix.md)
- Official documentation index: [WeryAI llms.txt](https://docs.weryai.com/llms.txt)
- Anime replace API: [Submit Video Anime Replace Task](https://docs.weryai.com/api-references/video-tools/submit-video-anime-replace-task)
