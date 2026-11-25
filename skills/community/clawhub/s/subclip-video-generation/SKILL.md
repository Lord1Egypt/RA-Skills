---
name: subclip-video-generation
description: Generate persistent cloud video with Subclip AI from text and model-supported image or video references. Use for new clips and generative edits of existing footage, including FLUX Video Edit. Ordinary trimming and reframing use native timeline tools.
---

# Subclip Video Generation

Follow `$subclip-ai-generation` for quota, credits, async completion, history, and deletion.

Call `list_ai_models` with `kind: video`. Select a live model by its `acceptedInputs`, `maxAssets`, required input, duration policy, resolution policy, end-frame support, and generated-audio support. Never send a duration or reference type outside that schema. Pass project inputs through `sourceAssets` using exact `sourceFileId` or `sourceItemId` values from `list_editor_assets`; use the explicit `start_frame`, `end_frame`, `reference`, `source_video`, or `audio_reference` role when the model distinguishes them. Source-duration models such as video-to-video editing require readable duration metadata and must use that duration for billing. Call `generate_ai_media` with `kind: video` and `confirmed: true` once when the current request authorizes those exact settings, then end the turn after it is accepted; do not poll.

Import a completed result as a normal MediaPanel video. Generated audio belongs to that video unless the user explicitly asks to extract it as an AudioPanel item.

## Current model capabilities

Read [model selection and pricing](references/model-selection.md) when selecting a model, quoting credits, supplying references or comparing quality tiers. Live discovery overrides historical model lists.
