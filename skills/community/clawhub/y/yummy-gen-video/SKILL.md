---
name: yummy-gen-video
version: 1.0.0
description: "Use when the user wants to generate a video with Gemini Veo through yummycli, including text-to-video, image-to-video (single starting frame), and reference-image-guided generation (up to 3 images)."
metadata:
  requires:
    bins: ["yummycli"]
    skills: ["yummy-shared"]
  openclaw:
    requires:
      bins: ["yummycli"]
    primaryEnv: GEMINI_API_KEY
    related_skills: ["yummy-shared"]
  hermes:
    tags: [video, gemini, veo, generation, image-to-video, multimodal]
    related_skills: ["yummy-shared"]
    requires_toolsets: ["yummycli"]
install:
  - kind: node
    package: "@yummysource/yummycli"
    bins: ["yummycli"]
---

# Generate Video

Create videos with `yummycli gemini veo` using Google Veo.

## When to Use

Load this skill when the user asks to generate, create, or animate a video using AI — including text-to-video, animating a still image, or generating a video guided by reference images.

> **Prerequisite:** Apply the `yummy-shared` skill first.

This skill covers three generation modes with a single command:

- Text-to-video (no images)
- Image-to-video (one starting frame)
- Reference-guided video (two or three reference images)

## Command Contract

Two equivalent entry points are available:

| Entry point | When to use |
|-------------|-------------|
| `yummycli gemini veo` | Default — human-friendly, Gemini Veo presets applied |
| `yummycli video generate --provider gemini` | Scripting / automation — explicit, provider-agnostic form |

Both share the same flags and defaults. Prefer `gemini veo` unless the task explicitly requires the provider-agnostic form.

Basic usage:

```bash
yummycli gemini veo --prompt "<prompt>"
```

With one or more input images:

```bash
yummycli gemini veo \
  --prompt "<prompt>" \
  --input-image ./frame.png \
  --input-image ./style.jpg
```

Optional output controls:

```bash
--output <file.mp4>
--model <model>
--aspect-ratio <ratio>
--duration <seconds>
--resolution <resolution>
```

Default values when omitted: `--model veo-3.1-fast-generate-preview`, `--aspect-ratio 16:9`, `--duration 8`, `--resolution 1080p`.

## Image Routing Rules

The number of `--input-image` flags determines the API path automatically:

| Count | Behaviour |
|-------|-----------|
| 0 | Text-to-video. Prompt drives the entire generation. |
| 1 | Image-to-video. The image is used as the starting frame. |
| 2–3 | Reference-guided. Images are passed as ASSET reference images; the prompt describes the motion and content. |

Never pass more than 3 `--input-image` flags — the API rejects it.

## Model Selection

Default model: `veo-3.1-fast-generate-preview`.

Use the following mapping when the user explicitly names a model variant:

| User says | Use |
|-----------|-----|
| `veo 3.1`, `3.1 fast`, or no preference | `veo-3.1-fast-generate-preview` (default) |
| `veo 3.1 full` or `veo 3.1 standard` | `veo-3.1-generate-preview` |
| `veo 3`, `veo 3 fast` | `veo-3.0-fast-generate-001` |
| `veo 3 standard` | `veo-3.0-generate-001` |
| `veo 2` | `veo-2.0-generate-001` |

Do not switch models from vague quality words alone. Only apply a mapping when the user's wording clearly refers to model choice.

## Model Compatibility

### Supported duration values (seconds)

Duration accepts only discrete values — not a range.

| Model | Valid durations |
|-------|----------------|
| `veo-2.0-generate-001` | 5, 6, 7, 8 |
| `veo-3.0-*` | 4, 6, 8 |
| `veo-3.1-*` | 4, 6, 8 |

### Supported resolutions

| Model | Supported resolutions |
|-------|-----------------------|
| `veo-2.0-generate-001` | `720p` only |
| `veo-3.0-*` | `720p`, `1080p` |
| `veo-3.1-*` | `720p`, `1080p`, `4k` |

Constraints:
- `1080p` requires `--duration 8`.
- `4k` requires `--duration 8` and a veo-3.1 model.

### Supported aspect ratios

All models: `16:9` (landscape) and `9:16` (portrait).

## Intent to Parameters

Translate clear user intent into CLI flags when the mapping is obvious.

**Aspect ratio guidance:**
- Use `--aspect-ratio 9:16` for vertical/portrait outputs: phone wallpaper, short-form vertical video, story format.
- Use `--aspect-ratio 16:9` for landscape outputs: film, presentation, widescreen. This is the default.
- If the user already specifies a ratio, pass it through directly.

**Duration guidance:**
- Use the longest valid duration for the model unless the user requests shorter.
- If the user says "short clip" or "quick", use `--duration 4` (veo-3+) or `--duration 5` (veo-2).
- Never pass a duration that is not in the valid set for the selected model.

**Resolution guidance:**
- Default (`1080p`) is appropriate for most requests.
- Use `--resolution 4k` only when the user explicitly asks for 4K quality and a veo-3.1 model is in use; pair with `--duration 8`.
- Use `--resolution 720p` when the user asks for a smaller or faster result.

**Output path guidance:**
- If `--output` is omitted, `yummycli` generates a timestamped `.mp4` filename in the current working directory. Do not invent your own filename unless the user provides one.
- The output path must end in `.mp4`. Reject or correct any other extension.

## Output Contract

Video commands return JSON on stdout. Read the response and use the `output` field as the generated file path.

Example (text-to-video):

```json
{
  "provider": "gemini",
  "output": "veo_20260417_142301_047.mp4",
  "model": "veo-3.1-fast-generate-preview",
  "duration_seconds": 8,
  "aspect_ratio": "16:9",
  "resolution": "1080p",
  "elapsed_seconds": 73
}
```

Example (image-to-video, one starting frame):

```json
{
  "provider": "gemini",
  "output": "veo_20260417_143010_112.mp4",
  "model": "veo-3.1-fast-generate-preview",
  "duration_seconds": 8,
  "aspect_ratio": "16:9",
  "resolution": "1080p",
  "elapsed_seconds": 89,
  "input_images": ["./dog.jpg"]
}
```

## Execution Rules

- Check `yummycli auth status --provider gemini` before running if credentials may not be configured.
- Use one `--input-image` flag per local image file; preserve the user-specified order.
- Validate duration and resolution against the selected model's constraints before running.
- Video generation is slow (typically 45–120 seconds). Inform the user that generation is in progress; do not treat a long wait as an error.
- If the command returns a validation error (bad duration, unsupported resolution, missing file), fix the arguments before retrying. Do not retry with the same invalid arguments.
- Report the final `output` path back to the user after a successful run.

## Examples

Text-to-video:

```bash
yummycli gemini veo \
  --prompt "A golden retriever puppy chasing a red ball in a sunny park"
```

Image-to-video (animate a still):

```bash
yummycli gemini veo \
  --prompt "The dog starts running toward the camera" \
  --input-image ./dog.jpg
```

Reference-guided (two images):

```bash
yummycli gemini veo \
  --prompt "Combine the character from the first image with the environment from the second" \
  --input-image ./character.png \
  --input-image ./background.jpg
```

Short portrait clip with veo-2:

```bash
yummycli gemini veo \
  --prompt "Falling cherry blossoms in slow motion" \
  --model veo-2.0-generate-001 \
  --aspect-ratio 9:16 \
  --duration 5 \
  --resolution 720p
```

4K landscape with veo-3.1:

```bash
yummycli gemini veo \
  --prompt "Timelapse of clouds moving over mountain peaks at golden hour" \
  --resolution 4k \
  --duration 8
```
