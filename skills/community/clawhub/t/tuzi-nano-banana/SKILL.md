---
name: tuzi-nano-banana
description: Generate/edit images via Tuzi API (default), Google Gemini, OpenAI, DashScope, Replicate. Text-to-image + image-to-image editing; 1K/2K/4K resolution. Use for image create/modify/edit requests incl. --input-image.
---

# Nano Banana Image Generation & Editing

Multi-provider image generation and editing. Default provider: Tuzi (兔子API, api.tu-zi.com).

## Script Directory

**Agent Execution**:
1. `SKILL_DIR` = this SKILL.md file's directory
2. Script path = `${SKILL_DIR}/scripts/main.ts`

## Usage

Run the script using absolute path (do NOT cd to skill directory first):

**Generate new image:**
```bash
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "your image description" --filename "output.png" [--resolution 1K|2K|4K] [--provider tuzi|google|openai|dashscope|replicate] [--model MODEL_ID]
```

**Edit existing image:**
```bash
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "editing instructions" --filename "output.png" --input-image "path/to/input.png" [--resolution 1K|2K|4K]
```

**Important:** Always run from the user's current working directory so images are saved where the user is working.

## Default Workflow (draft → iterate → final)

Goal: fast iteration without burning time on 4K until the prompt is correct.

- Draft (1K): quick feedback loop
  - `npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "<draft prompt>" --filename "yyyy-mm-dd-hh-mm-ss-draft.png" --resolution 1K`
- Iterate: adjust prompt in small diffs; keep filename new per run
  - If editing: keep the same `--input-image` for every iteration until you're happy.
- Final (4K): only when prompt is locked
  - `npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "<final prompt>" --filename "yyyy-mm-dd-hh-mm-ss-final.png" --resolution 4K`

## Options

| Option | Description |
|--------|-------------|
| `--prompt <text>`, `-p` | Prompt text (required) |
| `--filename <path>`, `-f` | Output filename (required) |
| `--input-image <path>`, `-i` | Input image for editing |
| `--resolution 1K\|2K\|4K`, `-r` | Output resolution (default: 1K) |
| `--provider tuzi\|google\|openai\|dashscope\|replicate` | Force provider (default: auto-detect, Tuzi first) |
| `--model <id>`, `-m` | Model ID |
| `--api-key <key>`, `-k` | API key (overrides env var) |

## Resolution Options

- **1K** (default) - ~1024px resolution
- **2K** - ~2048px resolution
- **4K** - ~4096px resolution

Map user requests:
- No mention of resolution → `1K`
- "low resolution", "1080", "1080p", "1K" → `1K`
- "2K", "2048", "normal", "medium resolution" → `2K`
- "high resolution", "high-res", "hi-res", "4K", "ultra" → `4K`

## Provider Selection

1. `--provider` specified → use it
2. `--api-key` provided (no `--provider`) → Google (direct Gemini API)
3. Only one API key available → use that provider
4. Multiple available → Tuzi first

## Tuzi Models

| Model ID | Quality | Notes |
|----------|---------|-------|
| `gemini-3-pro-image-preview` | 1k/2k/4k | Default. High quality |
| `gemini-3.1-flash-image-preview` | 1k/2k/4k | Fast, extended aspect ratios |
| `gemini-3-pro-image-preview-vip` | 1k built-in | VIP |
| `gemini-3-pro-image-preview-2k-vip` | 2k built-in | VIP |
| `gemini-3-pro-image-preview-4k-vip` | 4k built-in | VIP |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `TUZI_API_KEY` | Tuzi API key (https://api.tu-zi.com) |
| `TUZI_IMAGE_MODEL` | Tuzi default model |
| `TUZI_BASE_URL` | Custom Tuzi endpoint |
| `GEMINI_API_KEY` | Google Gemini API key |
| `GOOGLE_API_KEY` | Google API key (alias) |
| `OPENAI_API_KEY` | OpenAI API key |
| `DASHSCOPE_API_KEY` | DashScope API key |
| `REPLICATE_API_TOKEN` | Replicate API token |

**Load Priority**: CLI `--api-key` > env vars > `<cwd>/.tuzi-skills/.env` > `~/.tuzi-skills/.env`

## Image Editing

When the user wants to modify an existing image:
1. Use `--input-image` parameter with the path to the image
2. The prompt should contain editing instructions
3. Resolution auto-detects from input image size if not specified

## Prompt Handling

**For generation:** Pass user's image description as-is to `--prompt`. Only rework if clearly insufficient.

**For editing:** Pass editing instructions in `--prompt` (e.g., "add a rainbow in the sky")

## Prompt Templates

- Generation: "Create an image of: <subject>. Style: <style>. Composition: <camera/shot>. Lighting: <lighting>. Background: <background>."
- Editing: "Change ONLY: <single change>. Keep identical: subject, composition, pose, lighting, color palette, background, text, and overall style."

## Filename Generation

Pattern: `yyyy-mm-dd-hh-mm-ss-name.png`
- Timestamp: Current date/time in 24-hour format
- Name: Descriptive lowercase text with hyphens (1-5 words)

## Preflight + Common Failures

- `command -v npx` (must exist)
- API key must be available (env or `--api-key`)
- If editing: input image must exist

## Output

- Saves PNG to current directory (or specified path)
- Script outputs the full path to the generated image
- **Do not read the image back** - just inform the user of the saved path
