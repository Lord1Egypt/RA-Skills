---
name: video-prompt-generator
description: "Generate professional Sora 2 video prompts with the NanoPhoto.AI Prompt Generator API. Use when: (1) User wants a polished video prompt from a topic or scene idea, (2) User wants prompt generation for text-to-video or image-to-video workflows, (3) User mentions Sora 2 prompt generation, prompt writing, cinematic prompt creation, shot planning, or converting a topic into a production-ready video prompt. Supports locale, technique, duration, and public image URL inputs. Prerequisite: Obtain an API key at https://nanophoto.ai/settings/apikeys and configure env.NANOPHOTO_API_KEY."
metadata: {"openclaw":{"homepage":"https://nanophoto.ai","requires":{"env":["NANOPHOTO_API_KEY"]},"primaryEnv":"NANOPHOTO_API_KEY"}}
---

# Video Prompt Generator

Generate polished Sora 2 video prompts through the NanoPhoto.AI Prompt Generator API.

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
      "video-prompt-generator": {
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
- **OpenClaw config fallback**: the bundled script also falls back to `~/.openclaw/openclaw.json` at `skills.entries.video-prompt-generator.env.NANOPHOTO_API_KEY`

Credential declaration summary:

- Primary credential: `NANOPHOTO_API_KEY`
- Resolution order in the bundled script: `--api-key` → `NANOPHOTO_API_KEY` environment variable → `~/.openclaw/openclaw.json` skill env
- No unrelated credentials are required

## Recommended workflow

1. Collect the user's topic or scene idea.
2. Decide whether the prompt is for `textToVideo` or `imageToVideo`.
3. Choose a technique, duration, locale, and optional model override.
4. For image-to-video mode, require one to three public image URLs.
5. Run the bundled script or call the API directly.
6. Return the generated prompt text exactly as produced unless the user asks for adaptation or rewriting.

## Parameter guidance

- `topic`
  - Required
  - Maximum 500 characters
  - Keep it specific enough to imply subject, mood, or motion
- `mode`
  - `textToVideo`: default
  - `imageToVideo`: requires public `imageUrls`
- `technique`
  - Default: `montage`
  - Choose the technique that best matches the intended visual language
- `duration`
  - `10`
  - `15`
- `locale`
  - Default: `en`
  - Supported: `en`, `zh`, `zh-TW`, `ja`, `ko`, `es`, `fr`, `de`, `pt`, `ru`, `ar`

## Preferred command

Use the bundled script for reliable prompt generation:

### Text-to-video prompt

```bash
python3 scripts/video_prompt_generator.py \
  --topic "A serene Japanese garden with cherry blossoms falling into a koi pond" \
  --mode textToVideo \
  --technique slow-motion \
  --duration 15 \
  --locale en
```

### Image-to-video prompt

```bash
python3 scripts/video_prompt_generator.py \
  --topic "Animate this landscape with gentle wind and floating clouds" \
  --mode imageToVideo \
  --technique long-take \
  --duration 10 \
  --locale en \
  --image-url https://example.com/landscape.jpg
```

The script resolves credentials in this order: `--api-key`, then `NANOPHOTO_API_KEY` from the environment, then `~/.openclaw/openclaw.json` at `skills.entries.video-prompt-generator.env.NANOPHOTO_API_KEY`.

## Output behavior

- The API returns streaming text, but the bundled script prints the final assembled prompt text
- Return the prompt directly when the user asked for prompt generation
- If the user wants editing or localization after generation, transform the generated prompt in a second step instead of changing API parameters retroactively

## Manual API call

```bash
curl -X POST "https://nanophoto.ai/api/sora-2/generate-prompt" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $NANOPHOTO_API_KEY" \
  --data-raw '{
    "topic": "A futuristic cityscape at sunset with flying vehicles and neon lights",
    "technique": "aerial-view",
    "duration": 15,
    "locale": "en"
  }'
```

## Error handling

| errorCode | Cause | Action |
|-----------|-------|--------|
| `LOGIN_REQUIRED` | Invalid or missing API key | Verify key at https://nanophoto.ai/settings/apikeys |
| `API_KEY_RATE_LIMIT_EXCEEDED` | Rate limit exceeded | Wait and retry |
| `INSUFFICIENT_CREDITS` | Not enough credits | Top up credits |
| `INVALID_INPUT` | Missing or invalid topic | Ask for a valid topic under 500 characters |

## Bundled files

- `scripts/video_prompt_generator.py`: generate a prompt from a topic using the NanoPhoto Prompt Generator API
- `references/api.md`: condensed API reference, inputs, and error behavior
