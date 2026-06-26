---
name: youtube-cover-nano-banana
description: Create high-converting YouTube thumbnail concepts, overlay text, image prompts, and optional AI-generated cover images from raw titles, hooks, scripts, or marketing copy. Use when Codex needs a YouTube thumbnail generator, YouTube cover image workflow, thumbnail prompt generator, or Nano Banana-based thumbnail creation skill.
version: 0.1.1
metadata: {"openclaw":{"requires":{"env":["GEMINI_API_KEY","GOOGLE_API_KEY"],"bins":["python3"]},"primaryEnv":"GEMINI_API_KEY","emoji":"🖼️"}}
---

# YouTube Cover Nano Banana

## Overview

Analyze the user's text first. Then turn it into a thumbnail concept that is visually simple, emotionally obvious, and readable at small sizes.

Generate English image prompts for nano banana unless the user explicitly asks for another language. Keep reasoning grounded in YouTube thumbnail performance rather than generic poster design.

Use `scripts/create_thumbnail.py` for the full workflow when local script execution is available. It first calls Gemini text generation to turn source copy into a thumbnail plan, then optionally calls the official Gemini Nano Banana image endpoint. The scripts expect `GEMINI_API_KEY` or `GOOGLE_API_KEY`.

## Workflow

### 1. Extract the message

Pull out:

- Core topic
- Intended audience
- Main promise or tension
- Emotional direction such as urgency, surprise, authority, fear, curiosity, or excitement
- Best visual subject
- Any non-negotiable details such as product, person, brand color, or forbidden elements

If the user only gives raw copy, infer the thumbnail angle from the strongest claim instead of mirroring the entire text.

### 2. Choose the thumbnail strategy

Prefer one dominant idea. Use one of these visual strategies:

- Expressive face plus short text
- Single object or product in dramatic close-up
- Before versus after contrast
- Threat, mistake, or warning framing
- Curiosity gap with an incomplete reveal
- Authority or proof framing with a clear focal object

Reject cluttered multi-idea compositions unless the user explicitly wants a collage.

### 3. Compress the on-image text

Write overlay text that is:

- 2 to 6 words when possible
- Readable in one second
- Stronger than the original copy
- Different from the full video title if needed

Do not place paragraphs, subtitles, or detailed bullet points inside the image prompt.

### 4. Build the nano banana prompt

Produce a prompt with these properties:

- English language
- 16:9 YouTube thumbnail composition
- One dominant subject
- Bold focal point
- High contrast lighting and color separation
- Clean background with supporting elements only
- Space reserved for large headline text
- Photorealistic or stylized only if the user requests it

Explicitly describe:

- Subject appearance and pose
- Camera framing
- Emotion
- Background environment
- Color palette
- Lighting
- Text placement area
- Thumbnail style cues such as cinematic, glossy, creator-economy, tech, finance, fitness, education

Use the template and examples in [youtube-thumbnail-patterns.md](./references/youtube-thumbnail-patterns.md) when you need help selecting the structure.

### 5. Generate the image

Call nano banana with the final prompt after the concept is coherent.

For the full automated workflow, run:

```bash
python3 scripts/create_thumbnail.py \
  --copy "Man fights tiger" \
  --generate-image \
  --output-json "outputs/thumbnail-plan.json" \
  --image-output "outputs/generated-thumbnail.png"
```

This script:

- Analyzes the source copy
- Returns structured JSON with `angle`, `overlay_text`, `prompt`, and `generation_notes`
- Optionally renders the image with Nano Banana
- Writes a stable result envelope for integration use

If local script execution is available, run:

```bash
python3 scripts/generate_image.py \
  --prompt "<final english prompt>" \
  --angle "<angle>" \
  --overlay-text "<overlay text>" \
  --output "outputs/generated-thumbnail.png"
```

The script calls Gemini's official `gemini-2.5-flash-image` endpoint and saves:

- The generated PNG
- A sidecar JSON file with prompt, model, overlay text, and any text returned by the API

If tool calling or script execution is not available, still return the exact prompt plus a short note on what to generate.

### 6. Self-critique once

Before finalizing, check for the common failure modes:

- Too many subjects
- Text area too small
- Weak contrast
- Busy background
- Vague emotion
- No obvious click-driving angle
- Prompt accidentally describes a poster instead of a thumbnail
- Prompt includes tiny text or multiple lines of copy that image models render poorly

If a failure mode is present, revise the prompt once before returning it.

## Output Format

Return four blocks in this order:

1. `Angle`: one sentence describing the thumbnail idea
2. `Overlay Text`: short text for the cover
3. `Nano Banana Prompt`: the exact English prompt
4. `Generation Notes`: one short sentence with any critical instruction or fallback

## Constraints

- Optimize for clickability and legibility on mobile.
- Favor one subject over many.
- Favor strong emotion over neutral expression.
- Favor simple composition over descriptive completeness.
- Do not invent celebrity likenesses, trademarks, or brand assets the user did not request.
- Do not promise exact text rendering quality from the image model.
- If the user supplies Chinese copy, analyze in Chinese if helpful but output the final image prompt in English.
- If the user gives no style direction, default to modern YouTube thumbnail aesthetics with bold contrast and clean hierarchy.
- If the user gives a niche that implies a visual style, reflect it in the prompt. Example: finance should feel sharp and credible; gaming can be more exaggerated; education should feel clear and authoritative.

## Missing Information

Ask a brief follow-up only when a missing detail would materially change the output, such as:

- Whether a specific person must appear
- Whether a real product image is required
- Whether the thumbnail should use photorealistic, 3D, illustrated, or anime style
- Whether there are strict brand colors or banned visual elements

Otherwise, make reasonable assumptions and proceed.

## Resources

### scripts/

Use [create_thumbnail.py](./scripts/create_thumbnail.py) for end-to-end copy-to-thumbnail generation.

Use [generate_image.py](./scripts/generate_image.py) to call Nano Banana directly and save output files.

### references/

Use [youtube-thumbnail-patterns.md](./references/youtube-thumbnail-patterns.md) for prompt scaffolds, angle selection rules, and example transformations from raw copy to thumbnail prompt.

Use [publishing-contract.md](./references/publishing-contract.md) as the integration contract for callers that need stable command behavior, output JSON, and exit codes.
