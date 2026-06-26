---
name: weryai-image-toolkits
description: "Use when the user needs WeryAI image tools to analyze and transform existing images. Generate reusable prompts, convert and optimize visuals via background removal/change, canvas expansion, face swap, reframe, repair, text erase, translation, and upscale workflows."
metadata: { "openclaw": { "emoji": "🖼️", "primaryEnv": "WERYAI_API_KEY", "paid": true, "network_required": true, "requires": { "env": ["WERYAI_API_KEY", "WERYAI_BASE_URL"], "bins": ["node"], "node": ">=18" } } }
---

# WeryAI Image Toolkits

WeryAI image tools, image editing, image post-processing, background remove, background change, face swap, reframe, repair, text erase, translate, upscale, image-to-prompt.

WeryAI image tools for image editing and image post-processing on existing images.

Use this skill for official WeryAI image editing, image post-processing, and WeryAI image tools on an existing image source. Use when you need WeryAI image tools for image-to-prompt, background change, background remove, canvas expand, face swap, reframe, repair, text erase, image translate, image upscale, or prompt extraction. This skill is intentionally strict about secret declaration and input safety: the only runtime secret is `WERYAI_API_KEY`, and media inputs support `http/https` URLs plus local/file sources that are uploaded first.

This is not an image generation skill. Use it when the user wants to analyze, clean up, repair, translate, reframe, expand, upscale, or otherwise transform an existing image with WeryAI rather than generate a brand-new image from a prompt.

**Dependencies:** `scripts/image_toolkits.js` in this directory, `WERYAI_API_KEY`, and Node.js 18+. No other skills are required.

## Example Prompts

- `Remove the background from this HTTPS image with WeryAI.`
- `Translate the text in this image to English and return the translated image.`
- `Use WeryAI to swap the face in this portrait with the face from this reference image.`
- `Expand this square image into a 1024x1024 canvas.`
- `Turn this image into a reusable prompt with WeryAI image-to-prompt.`

## Quick Summary

- Main jobs: `image-to-prompt`, `background-change`, `background-remove`, `expand`, `face-swap`, `reframe`, `repair`, `text-erase`, `translate`, `upscale`
- Main inputs: `img_url` plus tool-specific parameters such as `image_size`, `prompt`, `bg_color`, `face_img_url`, `aspect_ratio`, `target_lang`, `original_image_size`, `canvas_size`, `original_image_location`
- Main trust signals: dry-run support, explicit per-tool validation, parameter guidance by intent, sync and async handling, `WERYAI_API_KEY` alignment with other WeryAI skills

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
node scripts/image_toolkits.js tools
node scripts/image_toolkits.js wait --tool background-remove --json '{"img_url":"https://example.com/image.jpg"}' --dry-run
```

- `tools` confirms the local CLI is available and shows the supported tool registry.
- `--dry-run` validates the request shape without calling WeryAI or spending credits.

## Prerequisites

- `WERYAI_API_KEY` must be set before running `image_toolkits.js` for paid calls.
- Node.js `>=18` is required because the runtime uses built-in `fetch`.
- `img_url` and `face_img_url` can be `http/https` URLs or local/file sources. Local/non-http(s) sources are uploaded first.
- Real `submit`, `wait`, and `status` commands can consume WeryAI credits or depend on existing paid tasks.

## Security And API Hosts

- **`WERYAI_API_KEY`**: Treat it as a secret. Configure it only in the runtime environment; never write the secret value into the skill files.
- This skill supports directly passing local file paths. If a local file path is provided, the runtime will automatically upload the local file to the WeryAI server for processing.
- Optional override `WERYAI_BASE_URL` defaults to `https://api.weryai.com`. Only override it with a trusted host.
- For higher assurance, run paid jobs in a short-lived shell or isolated environment, and review `scripts/image_toolkits.js` before production use.

## Tool Routing

Route user intent to the narrowest tool:

- Turn an image into a descriptive prompt -> `image-to-prompt`
- Replace or recolor background -> `background-change`
- Remove background -> `background-remove`
- Expand canvas or outpaint around an image -> `expand`
- Swap a face in an image -> `face-swap`
- Change image aspect ratio -> `reframe`
- Restore an old or damaged photo -> `repair`
- Erase text or watermark -> `text-erase`
- Translate text inside an image -> `translate`
- Enhance and upscale image quality -> `upscale`

If the user asks for text-to-image or image-to-image generation from scratch, use `weryai-image-generator` instead of this skill.

## Parameter Guidance

Guide the user progressively. Ask only for the smallest missing set of parameters required for the selected tool.

### Recommended guidance pattern

Use short operator-style guidance like this:

- General help: When the user asks "how to use this skill", DO NOT paste raw shell commands. Instead, explain the capabilities in natural language and give 2-3 prompt examples.

### Defaults you may apply safely

- `translate`: `type=image`
- For `background-remove`, `repair`, `text-erase`, and `upscale`, no extra parameter is needed beyond `img_url`

### Parameters that usually require user confirmation

- `background-change.prompt` or `background-change.bg_color`
- `face-swap.face_img_url`
- `reframe.aspect_ratio`
- `image-to-prompt.image_size`
- `translate.target_lang`
- `expand.original_image_size`, `expand.canvas_size`, and `expand.original_image_location`

### When to ask follow-up questions

- Ask for `image_size` when the user wants image-to-prompt and has not supplied the source image size in KB.
- Ask for `prompt` or `bg_color` when the user wants background change but has not said whether the new background is descriptive or a flat color.
- Ask for `face_img_url` when the user wants face swap but has not supplied the replacement face image.
- Ask for `aspect_ratio` when the user wants reframe but has not specified the target shape.
- Ask for `target_lang` when the user wants image translate but does not name the destination language.
- Ask for canvas dimensions and placement only when the user wants expand.

## Tool Matrix

Read [references/image-tools-matrix.md](references/image-tools-matrix.md) when you need the exact required fields, enum values, sync behavior, or defaults for a tool.

## Preferred Commands

```sh
# Remove image background
node scripts/image_toolkits.js wait --tool background-remove --json '{"img_url":"https://example.com/image.jpg"}'

# Change background with a descriptive prompt
node scripts/image_toolkits.js wait --tool background-change --json '{"img_url":"https://example.com/image.jpg","prompt":"clean white studio background"}'

# Poll an existing task
node scripts/image_toolkits.js status --task-id <task-id>
```

## Workflow

1. Identify whether the user wants image editing/post-processing or image generation.
2. Route the request to one tool ID.
3. Collect `img_url` and only the extra parameters required by that tool.
4. Apply supported defaults where safe.
5. Show the final tool, parameters, and URLs before the paid run if the request is ambiguous or expensive.
6. Use `--dry-run` when you need to verify the payload locally first.
7. For async tools, use `wait` by default to deliver final processed image URLs in the same turn.
8. Enforce bounded polling with a maximum timeout of 5 minutes (300 seconds); do not run unbounded loops.
9. If timeout is reached, return the `taskId` to the user and ask if they want you to check the status again. Do NOT show the raw node status command to the user; use it internally.
10. Use `submit` for synchronous `image-to-prompt` or when the user explicitly wants task creation without polling.
11. Use `status` when the user already has a `task_id`.

## Input Rules

- `img_url` and `face_img_url` can be `http/https` URLs or local/file sources.
- `image-to-prompt` requires `image_size` in KB.
- `background-change` requires `prompt` or `bg_color`.
- `expand` requires `original_image_size`, `canvas_size`, and `original_image_location`.
- `reframe` must use a supported `aspect_ratio`.
- `translate` must include `target_lang`; `type` can be `text` or `image`.
- Do not invent undocumented request fields.

## Output

All commands print JSON to stdout. Successful results can include:

- `taskId`, `taskIds`, `batchId`
- `taskStatus`
- `images`
- `prompt`
- `cost_mill`
- `requestSummary`
- `errorCode`, `errorMessage`

User-facing delivery requirement:

- If image URLs are available, return at least one user-visible image link (for example `[Image](https://...)`) or inline rendering when supported. If multiple images are generated, render all of them using markdown image syntax consecutively.
- Alongside image output, include key parameters when available: `tool`, `model`, `aspect_ratio`, `image_number`, `resolution`.
- Do not use `taskId` as the sole deliverable unless the user explicitly requested task creation without waiting.
- If timeout is reached before completion, return the `taskId` to the user and ask if they want you to check the status again. Do NOT show the raw node status command to the user; use it internally.

## Definition of done

The task is done when:

- local validation passes without CLI-side errors,
- `wait` returns final processed images for async tools,
- or `wait` reaches a terminal result with at least one processed image URL,
- or `image-to-prompt` returns a prompt string successfully,
- or `status` returns a clear in-progress or terminal state,
- or `wait` hits timeout and returns `taskId` plus a follow-up status command,
- and the output makes it explicit whether image URLs or prompt text are present.

## Constraints

- Do not treat this skill as a text-to-image or image-to-image generator.
- Do not ask the user to choose raw API fields when a safe default already fits the request.
- Do not use unsupported file types for `img_url` or `face_img_url`; local sources are uploaded before the toolkit request.
- Do not re-run paid processing casually because each `submit` or `wait` call can create a new paid task.
- Do not broaden this skill beyond the documented WeryAI image-tools API surface.

## Re-run behavior

- `submit` and `wait` are not idempotent for async tools.
- `image-to-prompt` is synchronous and safe to re-run if the user explicitly wants a fresh prompt analysis.
- `status` and `tools` are safe to re-run.

## References

- Image tools parameter matrix: [references/image-tools-matrix.md](references/image-tools-matrix.md)
- Official documentation index: [WeryAI llms.txt](https://docs.weryai.com/llms.txt)
