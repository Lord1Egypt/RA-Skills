---
name: yummy-gen-image
version: 1.0.0
description: "Use when the user wants to generate or edit raster images with Gemini through yummycli, including prompt-only generation, single-image editing, and multi-image reference editing."
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
    tags: [image, gemini, generation, editing, multimodal]
    related_skills: ["yummy-shared"]
    requires_toolsets: ["yummycli"]
install:
  - kind: node
    package: "@yummysource/yummycli"
    bins: ["yummycli"]
---

# Generate Image

Create or edit images with `yummycli gemini nanobanana`.

## When to Use

Load this skill when the user asks to generate, create, or edit an image using AI — including text-to-image generation, style transfer, image editing with a reference photo, or multi-image compositing.

> **Prerequisite:** Apply the `yummy-shared` skill first.

This skill uses one command for all Gemini image flows:

- Prompt-only generation
- Single-image editing
- Multi-image reference editing

## Command Contract

Two equivalent entry points are available:

| Entry point | When to use |
|-------------|-------------|
| `yummycli gemini nanobanana` | Default — human-friendly, Gemini presets applied |
| `yummycli image generate --provider gemini` | Scripting / automation — explicit, provider-agnostic form |

Both share the same flags and the same Gemini defaults. Prefer `gemini nanobanana` unless the task explicitly requires the provider-agnostic form.

Basic usage:

```bash
yummycli gemini nanobanana --prompt "<prompt>"
```

Add one or more reference images when needed:

```bash
yummycli gemini nanobanana \
  --prompt "<prompt>" \
  --input-image ./source-a.png \
  --input-image ./source-b.png
```

Optional output controls:

```bash
--output <file>
--model <model>
--aspect-ratio <ratio>
--image-size <size>
```

Default values when omitted: `--aspect-ratio 16:9`, `--image-size 1K`, `--model gemini-3.1-flash-image-preview`.

## Execution Rules

- Use prompt-only generation when no reference images are provided.
- Use one `--input-image` flag per local image file.
- Preserve the user-provided order of reference images.
- Prefer the default model unless the user asks for a specific model.

## Model Selection

Use the following model mapping rules:

- If the user explicitly says `gemini pro`, `pro model`, or simply `pro` in the model-selection context, use:

```bash
--model gemini-3-pro-image-preview
```

- If the user explicitly says `gemini flash`, `flash model`, or simply `flash` in the model-selection context, use:

```bash
--model gemini-3.1-flash-image-preview
```

- If the user does not explicitly request a model, omit `--model` and let `yummycli` use its default model.

Do not switch models implicitly from vague quality words alone. Only apply the `pro` or `flash` mapping when the user's wording clearly refers to model choice.

## Model Compatibility

### Aspect ratio

| Model | Supported values |
|-------|-----------------|
| `gemini-3.1-flash-image-preview` | `1:1` `1:4` `1:8` `2:3` `3:2` `3:4` `4:1` `4:3` `4:5` `5:4` `8:1` `9:16` `16:9` `21:9` |
| `gemini-3-pro-image-preview` | `1:1` `2:3` `3:2` `3:4` `4:3` `4:5` `5:4` `9:16` `16:9` `21:9` |
| (default / other) | `1:1` `3:4` `4:3` `9:16` `16:9` |

`1:4`, `1:8`, `4:1`, `8:1` are flash-only. Do not use them with the pro model.

### Image size

| Model | Supported values |
|-------|-----------------|
| `gemini-3.1-flash-image-preview` | `512` `0.5K` `1K` `2K` `4K` |
| `gemini-3-pro-image-preview` | `1K` `2K` `4K` |
| (default / other) | `1K` `2K` `4K` |

`512` and `0.5K` are flash-only. Do not use them with the pro model.

## Intent to Parameters

Translate clear user intent into CLI flags when the mapping is obvious.

Aspect-ratio guidance:

- Use `--aspect-ratio 9:16` for requests such as phone wallpaper, vertical poster, story format, or other clearly vertical mobile outputs.
- Use `--aspect-ratio 16:9` for requests such as desktop wallpaper, presentation cover, horizontal banner, or other clearly widescreen outputs.
- Use `--aspect-ratio 1:1` for square social images, avatars, or other explicitly square outputs.
- If the user already provides a specific ratio, pass it through directly.
- If the output shape is unclear, omit `--aspect-ratio` and let `yummycli` use its default.

Image-size guidance:

- Use `--image-size 4K` when the user explicitly asks for 4K or a clearly print-grade / high-resolution deliverable.
- Use `--image-size 2K` when the user explicitly asks for 2K or a medium-resolution deliverable.
- Use `--image-size 1K` when the user explicitly asks for 1K or a lightweight preview-sized result.
- Use `--image-size 512` or `--image-size 0.5K` only when the user explicitly asks for a minimal-size output and the flash model is in use.
- If the user does not explicitly request output size, omit `--image-size` and let `yummycli` use its default (`1K`).

Do not guess `--image-size` from general quality adjectives alone.

Output path guidance:

- If `--output` is omitted, `yummycli` generates a default filename in the current working directory. Do not invent your own output filename unless the user explicitly provides one.

## Examples

Prompt-only generation:

```bash
yummycli gemini nanobanana \
  --prompt "A single ripe banana on a white plate, studio lighting, realistic photo"
```

Single-image edit:

```bash
yummycli gemini nanobanana \
  --prompt "Turn this into a watercolor illustration" \
  --input-image ./source.png
```

Multi-image reference edit:

```bash
yummycli gemini nanobanana \
  --prompt "Blend these references into one polished poster illustration" \
  --input-image ./subject.png \
  --input-image ./background.jpg
```
