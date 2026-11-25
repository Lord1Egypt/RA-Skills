---
name: subclip-ai-generation
description: Discover and run Subclip cloud image, video, video-avatar, music, and speech generation, then inspect, reuse, import, or delete persistent AI outputs. Use for prompts that ask Subclip to generate new media or revisit previous AI generations; do not use for ordinary timeline edits to existing assets.
---

# Subclip AI Generation

Subclip generation is optional. Any agent may instead generate media with its own tools or providers (Codex image generation, a Grok bot, a local model) and import the file with `import_external_media` (path, https URL or base64); that path uses no Subclip credits. Use Subclip's `subclip_ai_editor` MCP server for generation when the user asks for it or its models fit best. Generated outputs are persistent cloud records, appear in the project chat and AI Generations panel, consume AI credits, and count toward the signed-in user's cloud-storage quota.

## Plan mode

Only call `list_ai_models`, `estimate_ai_generation`, `list_ai_voices`, `list_ai_operations`, and `get_ai_operation`. State the chosen model, required inputs, expected credit basis, and how the completed output would become a normal MediaPanel or AudioPanel item. Do not start, delete, or import a generation.

## Generate

1. Call `list_ai_models` for the requested output kind. Select a model from its live supported modalities and parameters; never hardcode provider models or pricing.
   - Image-specific prompting routes to `$subclip-image-generation`.
   - Video-specific prompting routes to `$subclip-video-generation`.
   - Talking-avatar prompting routes to `$subclip-avatar-generation`.
   - Background music routes to `$subclip-music-generation`; lyrics and sung songs route to `$subclip-songwriting`. Music is Audio, with the `text_to_music` operation.
   - Speech and voice selection route to `$subclip-tts`.
2. For speech, call `list_ai_voices` with the selected model ID and pass its stable Subclip voice ID. Never guess or expose a raw provider voice ID.
3. Confirm the prompt and model-specific inputs only when the current message has not already authorized them. A direct request to build, create, generate, or regenerate an exact output is confirmation for one matching generation. A reference attachment is not implicitly uploaded merely because it is visible in chat. Resolve project inputs with `list_editor_assets`, then pass supported references through `sourceAssets` with exact file/item IDs and roles; never place source IDs or references inside `settings`.
4. Call `estimate_ai_generation` with the exact model, settings and source durations before video/avatar generation; update the quote after changing them. Then call `generate_ai_media`, `generate_music`, or `generate_speech` once. Pass `confirmed: true` only when step 3 is satisfied; a direct request for those exact generation details is confirmation. Keep the returned operation ID. Do not poll in a loop or submit a duplicate when the result is queued.
5. End the agent turn after an accepted async result. The UI resolves the stable operation ID into a placeholder and later into an image, video, or audio player. Signed URLs are temporary and must never be written into project history or director notes.

If Subclip reports insufficient credits, stop and link to [Subclip account credits](https://subclip.app/account). If it reports exhausted storage, stop and direct the user to AI Generations to delete cloud outputs. Do not retry until the relevant limit changes.

## Reuse and cleanup

- Call `get_ai_operation` immediately before previewing or importing so URLs are fresh. Use `import_ai_operation_to_timeline` with the stable ID; do not download a signed URL yourself. This is a checkpointed local-project mutation and an explicit request to add or replace that generated output is sufficient authorization—call it directly and never claim that a separate approval policy blocked it.
- For “replace this image/clip with the generated video,” pass the exact selected target media item as `replaceItemId` in the video import. This atomically preserves the target timeline slot, framing, style, lane, and z-order and returns `fileId`, `itemId`, and `replacedItemId`. Do not first import a duplicate timeline item, do not scan the full inventory to rediscover the result, and do not call `replace_media_item_source` afterward.
- Import completed speech separately with its intended `startTime`. The response returns exact `fileId` and `itemId`; use those IDs for any follow-up and never infer failure merely because a prior blocked call returned no IDs.
- Completed image/video outputs import as ordinary editable MediaPanel files; completed speech and music import as an ordinary AudioPanel file. Their generated pixels or samples are not internally separated into editable source layers.
- Regeneration creates a new operation and preserves the earlier result. It is not an in-place redo.
- Before `delete_ai_operations`, name the exact operation(s) and obtain confirmation. Deletion removes the persistent record and owned cloud objects and releases their recorded quota. Deletion of a running media-generation operation also requests cancellation. Other operation types may reject deletion while running; respect the service response.

## Current model capabilities

Read [model selection and pricing](references/model-selection.md) when selecting a model, quoting credits, supplying references or comparing quality tiers. Live discovery overrides historical model lists.
