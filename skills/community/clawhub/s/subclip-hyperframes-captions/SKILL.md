---
name: subclip-hyperframes-captions
description: Convert a project's native captions into an editable HyperFrames caption layer when the creator names a HyperFrames caption style or asks for HyperFrames/GSAP-designed captions. The HyperFrames layer becomes the source of truth for caption design; native captions are hidden, never deleted unless asked, and the word data stays in the layer variables. Do not use for ordinary subtitle correction or for native Dynamic Captions presets.
---

# Subclip HyperFrames captions

Use this when the creator asks for a HyperFrames caption style (a registry caption-style id, "HyperFrames captions", GSAP word-by-word captions, a named kinetic caption look). For native presets, word emphasis or subtitle corrections use `$subclip-dynamic-captions` or `$subclip-text-captions` instead. For authoring the layer source itself, `$subclip-hyperframes-layer` still applies.

Two pieces of state matter. The native captions own the words and timing (they stay editable in the Captions panel). The HyperFrames layer owns the look. `convert_captions_to_hyperframes` copies the words into the layer variables (`captionWords`, project-time seconds) so the layer can be rebuilt, and hides the native words so captions are not drawn twice.

## Order of work

1. **Words first.** Inspect with `list_editor_assets` / `get_recording_captions`. If the project has no caption words, run the existing transcription flow (`transcribe_project` with `purpose: "captions"`, see `$subclip-transcription`) and wait for it to finish. Never fabricate or retype words.
2. **Find the style.** `list_hyperframes_registry` with the creator's style name, or with the query `caption` when no name was given (the registry list has no `caption-style` tag; the styles are the `caption-*` components). Search every named style separately. Prefer light styles (text, simple GSAP) over heavy ones (WebGL, Three.js, large particle or blur effects).
3. **Read it.** `get_hyperframes_registry_item` with `includeSources: true` for the chosen id. Note font, colour, weight, casing, stroke, entrance and highlight behaviour. The registry source is reference material, not installed code.
3b. **Direct from generated speech (no transcription).** When the voice is text-to-speech you just made (`generate_local_speech` then `import_generated_audio_to_timeline`), skip `transcribe_project` and pass `script: { text, audioItemId }` to `convert_captions_to_hyperframes`. The words are timed against the pauses found in the audio (commas and sentence ends land on the real silences), so no native captions exist or are touched. Timing is good for synthetic voices and a few tenths of a second off in places; for human speech or exact timing transcribe and convert the native captions instead. If native captions already exist the result warns that both render.
4. **Convert.** `convert_captions_to_hyperframes` with `styleId` (from step 2), `preset` (`energetic` 2-3 words per group, `conversational` 3-5, `calm` 4-6), `position`, and an explicit `style` object for anything the hints did not capture (for example `activeWordColor`, `uppercase`, `scrim`). Leave `hideNativeCaptions` on. Only what can be read from the item's CSS and script is applied (font, colours, weight, casing, stroke, shadow, a gradient's first colour, a pill background as a scrim); its animation is not copied and its font may not be installed. If the result warns that no style could be read, or the look must match exactly, restyle with `read_layer_source` + `edit_layer_source` after reading the item.
5. **Look at it.** Seek to a few spoken moments, the first cue and the last cue (`seek_timeline`, then `view_current_frame`). Check legibility over the footage, safe-zone placement (bottom 80-120 px landscape, about 600-700 px from the bottom in portrait), no overlap with a face, no two groups on screen at once, and that no native caption is still visible. A static source check is not visual proof.
6. **Fix the design.** Re-run `convert_captions_to_hyperframes` with changed options (it updates the same layer in place), or refine with `read_layer_source` + `edit_layer_source` and `update_runtime_layer`. Hand edits to the source are lost if you re-run the conversion, so finish option changes first. Keep one group visible at a time, keep the hard kill after every group, never apply CSS `filter` or `backdrop-filter` to text, and keep the layer transparent.
7. **Verify with a short ranged export.** Exports run only on the creator's request, so offer it or use it when they asked for a check: `export_video` with `startTime`/`endTime` over a few seconds that include a cue (see `$subclip-export`), never the whole video, then inspect the result.
8. **Record the result.** Mention the style id, preset, and that native captions are hidden (not deleted) in your session summary.

## Rules

- Captions are clamped to the project's current duration and the project duration is never changed; the result reports stray words past the end that were left out. Groups also break at the native caption page ends.
- Never delete native captions unless the creator explicitly asks. If they do, pass `deleteNativeCaptions: true` and `confirmed: true`; that cannot be undone by `restore_native_captions` (it refuses and keeps the layer). Hiding is the default and is reversible.
- To go back: `restore_native_captions` un-hides exactly the words the conversion hid (words the creator hid themselves stay hidden) and removes the HyperFrames layer. `removeHyperframesCaptions: false` keeps the layer, which draws a second set of captions.
- Do not delete the HyperFrames layer with `delete_runtime_layer` and leave the native words hidden; use `restore_native_captions` so the words come back.
- Pass `startTime`/`endTime` to convert only part of the video; native captions outside that range stay visible.
- Text overlays, speaker labels, or edits to the transcript after conversion: edit the native words (`update_caption_words`), then re-run the conversion so the layer rebuilds from them. Words the creator hid natively are not converted.
- Tell the creator that long caption layers are slower to export than native captions, and that on Linux (software GL) heavy templates are not suitable. Prefer light templates, split very long videos into ranged exports, and say so when the chosen registry style is heavy.
- Report what you verified (frames viewed, export checked) separately from what you only configured.
