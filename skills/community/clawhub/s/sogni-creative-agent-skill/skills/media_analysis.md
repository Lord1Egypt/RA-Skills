---
name: media_analysis
description: Vision analysis of uploaded images / videos and structured metadata extraction from previously rendered results.
always_loaded: false
tool_names:
  - analyze_image
  - analyze_video
  - extract_metadata
---

# Media analysis

Vision and metadata inspection of images and videos. The model uses these to ground later creative decisions on what's actually in the uploaded asset rather than guessing.

## Tools

- `analyze_image` — vision analysis of an uploaded or generated image.
- `analyze_video` — vision analysis of a video clip.
- `extract_metadata` — structured extraction of generation metadata (model, prompt, params) from previously rendered results.
