---
name: runware-prompting
description: >
  Write effective prompts for Runware's image and video models. Use whenever an
  agent is composing a prompt and wants model-appropriate phrasing, in-image
  text, negation, or cinematic grammar. Foundation skill - outcome skills lean
  on it for the actual wording.
---

# Prompting Runware models

Different model families read prompts differently. Match the phrasing to the model. When in doubt, confirm the model's strengths via `runware-models`.

## Cross-family principles

- **Layer the scene** for complex images: subject → environment → camera/framing → lighting → mood. Name objects *and their positions*, not just objects.
- **Short and interpretive vs long and structured.** Modern models reward concise intent; older/diffusion models reward dense descriptive stacks. Pick per family below.
- **In-image text is quoted, exact, and placed.** To render words in an image, quote the exact string and state placement and style. Models render what you quote, not what you describe.
- **Negation:** some models take inline negation in the positive prompt (write "Negative prompt: X, Y" as a clause and the model obeys); others have a real `negativePrompt` field. Check the schema.

## Image families

- **LLM-based image models (gpt-image-2, Nano Banana 2):** parse full natural language. Use structured briefs, inline negation, even pseudocode; say "photorealistic" explicitly; use camera language for composition. Nano Banana 2 has a `thinking` setting for hard prompts and renders legible in-image text well; it also grounds on real facts via `providerSettings.google.webSearch`.
- **Seedream / Recraft:** short interpretive prompts work; layer (subject → lighting → composition) for control. Recraft's Utility variants give flat, predictable output for mockups; constrain color with `settings.colors`.
- **Ideogram:** operates on a **structured JSON** (reserved keys: `description`, `style`, `background`, `elements`), not a sentence. Text is a first-class `text` element. Use Magic Prompt to expand natural language, or hand-craft the JSON for repeatable layouts.
- **Grok / typography models:** quoting the exact text is non-negotiable; placement and script/style are refinements.

## Video families

- **Cinematic grammar (Gemini-Omni, Luma, Runway, Kling):** use a compact scaffold - framing/camera motion, style, lighting, location, action. Three to four sentences beat a wall of adjectives. These models read camera vocabulary (dolly, push-in, rack focus) directly.
- **Image-to-video (Runway Gen, Pixverse, HappyHorse):** the image fixes the subject and composition; the prompt should direct *only the motion* (subject motion + camera motion). Don't re-describe the scene the image already shows.
- **Multi-shot in one call (HappyHorse, Kling Turbo, Pixverse):** use the model's beat/shot template (`shot N, seconds, description;` or `Begin with… / Cut to… / End on…`). Per-shot seconds must sum to the total `duration`.

## Quality bar

- Phrasing matches the chosen model family (not a generic prompt).
- Any required in-image text is quoted exactly and placed.
- For video, the prompt directs motion/camera, not a static scene description.

## Related skills

`runware-models` (which model), `runware-run` (send it), and outcome skills (each adds its domain build-order on top of these basics).
