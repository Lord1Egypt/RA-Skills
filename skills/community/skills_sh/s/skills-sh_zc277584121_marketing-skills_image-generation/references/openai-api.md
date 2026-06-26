# OpenAI API Fallback

Use this path when the built-in Codex image path is unavailable or when the user explicitly requests script/API execution.

## Requirements

- `OPENAI_API_KEY` must be set.
- The script uses `gpt-image-2` by default.
- The script sends requests directly to the OpenAI image generation endpoint.

## Command

```bash
python <skill-root>/scripts/generate_image.py \
  --provider openai \
  --prompt "your prompt here" \
  --output "/path/to/save/image.png"
```

For automatic fallback to Gemini if OpenAI generation fails:

```bash
python <skill-root>/scripts/generate_image.py \
  --provider auto \
  --prompt "your prompt here" \
  --output "/path/to/save/image.png"
```

## Size Mapping

The script accepts the same `--aspect-ratio` and `--image-size` inputs as the Gemini path, then maps them to valid `gpt-image-2` dimensions.

Useful defaults:

| Request | Script args | Typical OpenAI size |
|---------|-------------|---------------------|
| Article illustration | `--aspect-ratio 3:2 --image-size 1K` | `1536x1024` |
| Square image | `--aspect-ratio 1:1 --image-size 1K` | `1024x1024` |
| Social banner | `--aspect-ratio 16:9 --image-size 2K` | near `3840x2160` |
| Portrait image | `--aspect-ratio 2:3 --image-size 1K` | `1024x1536` |

OpenAI size constraints handled by the script:

- Max edge: `3840px`
- Width and height: multiples of `16px`
- Long-to-short ratio: at most `3:1`
- Total pixels: between `655,360` and `8,294,400`

If an aspect ratio exceeds `3:1`, the script skips OpenAI in `auto` mode and tries Gemini when `GEMINI_API_KEY` is available.

## Quality

Use `--openai-quality high` for final article visuals. Use `medium` or `low` only for drafts.

```bash
python <skill-root>/scripts/generate_image.py \
  --provider openai \
  --openai-quality high \
  --aspect-ratio 3:2 \
  --image-size 1K \
  --prompt "..." \
  --output images/example.png
```
