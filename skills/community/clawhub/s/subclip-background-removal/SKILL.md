---
name: subclip-background-removal
description: Remove the background from an existing Subclip MediaPanel image locally by default or from video through the credit-backed cloud workflow, then preserve or replace the exact timeline item with the editable result. Use for requests to cut out a subject, make an image transparent, or remove a video background; do not use for generating unrelated new media.
---

# Subclip Background Removal

Use Subclip's `subclip_ai_editor` MCP server. Image background removal first uses the cached local `briaai/RMBG-1.4` q8 ONNX model, consumes no credits, and replaces the exact item immediately. If local inference fails, it falls back to the persistent cloud operation. Video removal always uses the cloud operation, appears in AI Assets and chat, consumes credits only after a usable output is stored, and preserves the original project until the completed result is imported.

When the requested outcome is text or subtitles behind/in-between a person or foreground subject, load `$subclip-text-behind-subject`. That workflow must preserve the original media as the background plate and remove the background only from a muted aligned duplicate; this ordinary replacement workflow must never replace the base item for that effect.

## Plan mode

Call only read-only project, asset, operation, and credit tools. Identify the exact MediaPanel `itemId`, its media type, and its current source trim. Explain that images use local ONNX by default and become transparent PNGs, while videos use human-focused cloud matting followed by an editable green color-key effect. Do not start or import an operation.

## Execute

1. Call `list_editor_assets` and resolve one exact existing MediaPanel item. Never guess an item or file ID.
2. A direct request to remove that exact item's background authorizes the local image attempt and one cloud fallback if local inference fails. Pass `confirmed: true`; otherwise confirm before submission.
3. Call `remove_media_background` once with the exact `itemId` and the default `processingMode: auto`. For an image, the tool runs local ONNX first and normally returns `state: completed`, `processingMode: local`, and `creditsUsed: 0` after replacing the item. Do not import it again.
4. Use `processingMode: cloud` only when the user explicitly asks for cloud processing or says the local result is unsatisfactory. Never choose cloud merely because it may be better.
5. For a cloud fallback or video, the tool performs a credit preflight before preparation/upload, and the server repeats the reservation check under a lock before Replicate dispatch. Video uploads only the item's current `sourceStartTime`–`sourceEndTime` window. Its preparer intentionally discards source audio, subtitle, and data streams because matting consumes video frames only; an invalid MOV audio entry must not block the visual operation.
6. When the tool returns a queued cloud operation, store its ID and end the in-app turn without polling. Subclip resumes the conversation when it completes, fails, or is canceled. Never submit a duplicate because processing takes time.
7. On a completed cloud terminal event, call `get_ai_operation` once, then `import_ai_operation_to_timeline` with that operation ID and the same target `replaceItemId`. Do not first create a duplicate item.
8. Video import automatically adds one editable `colorKey` effect for the provider's green-screen output. Do not add a second color key. Image import needs no color-key effect.
9. Re-read `list_editor_assets`, seek inside the replaced item, and call `view_current_frame`. Confirm the source was replaced, the timeline slot and styling were preserved, and the video effect stack contains one enabled `colorKey` when applicable.

If a cloud attempt reports insufficient credits, stop and provide [Subclip account credits](https://www.subclip.app/account). If it reports exhausted storage, direct the user to AI Assets to delete old cloud outputs. Provider failure or cancellation is terminal for that operation; preserve the original timeline item and report the concrete sanitized error.

Robust Video Matting is designed primarily for people and talking-head footage. Do not promise equally strong results for arbitrary objects, animation, or complex transparent materials.

Do not call `import_attachment_clip_with_ffmpeg` to repair a background-removal source already stored inside the project. That converter accepts agent-authorized attachments, not arbitrary project-local paths, and cannot fix this workflow. Do not ask the user to reattach media solely because its audio stream is malformed; background-removal preparation ignores audio.
