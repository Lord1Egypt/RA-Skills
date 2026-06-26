# Gemini API Fallback

Use this path when OpenAI API generation is unavailable or fails, and `GEMINI_API_KEY` is set.

## Requirements

- `GEMINI_API_KEY` must be set.
- The default model is `gemini-3.1-flash-image-preview`.
- This path preserves the original Nano Banana workflow.

## Command

```bash
python <skill-root>/scripts/generate_image.py \
  --provider gemini \
  --prompt "your prompt here" \
  --output "/path/to/save/image.png"
```

To let the script choose OpenAI first and then Gemini:

```bash
python <skill-root>/scripts/generate_image.py \
  --provider auto \
  --prompt "your prompt here" \
  --output "/path/to/save/image.png"
```

## Options

```text
--gemini-model    gemini-3.1-flash-image-preview, gemini-3-pro-image-preview, gemini-2.5-flash-image
--aspect-ratio    1:1, 1:4, 1:8, 2:3, 3:2, 3:4, 4:1, 4:3, 4:5, 5:4, 8:1, 9:16, 16:9, 21:9
--image-size      512, 1K, 2K, 4K
--style-prefix    Custom style prefix
--no-style        Skip default style prefix
```

## When Gemini Is Useful

- OpenAI credentials are unavailable.
- The requested aspect ratio is wider or taller than OpenAI's `3:1` ratio limit.
- You want to keep compatibility with the previous workflow.
