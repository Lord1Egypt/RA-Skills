---
name: subclip-text-behind-subject
description: Composite editable TextPanel text or timed captions between an original background plate and an exactly aligned background-removed foreground duplicate. Use when a creator asks for text behind a person or subject, subtitles behind the speaker, text between foreground and background, or the cutout text-behind effect. Do not use for ordinary top-layer text or standalone background removal.
---

# Subclip Text Behind Subject

Build one editable three-plane composite in the requested segment:

1. original media with its background, unchanged on the base `media` plane
2. existing or newly created TextPanel text/captions in the middle
3. an exactly aligned, muted, background-removed duplicate on `above-text` or `above-captions`

Use Subclip's `subclip_ai_editor` MCP server. Load `subclip-background-removal` for the removal lifecycle and `subclip-text-captions` or `subclip-dynamic-captions` for the chosen middle layer. Never remove or replace the base item's background.

## Resolve the request before processing

1. Read `active-project` and call `list_editor_assets`. Resolve the exact requested timeline segment and the one base MediaPanel item visible behind the intended subject. Never infer a target when multiple overlapping media items could be the plate.
2. Inspect all TextPanel items and caption words/pages overlapping that segment before asking for copy. Classify the intended middle layer:
   - **Normal text:** an existing TextPanel title, label, callout, or supplied text string.
   - **Subtitles:** existing timed ordinary/Dynamic Captions, imported timestamped cues, or speech the creator explicitly wants transcribed.
3. Reuse existing text/captions when the creator's wording and segment identify them unambiguously. Preserve their copy, timing, position, typography, priorities, page grouping, and source ownership unless the creator asks for changes.
4. Ask one concise clarification before any mutation or background-removal job when required information is absent or ambiguous:
   - no existing text/caption content and no copy/source was supplied: ask what text to show; for subtitles, ask whether to transcribe the segment's speech or use supplied copy/cues
   - no exact interval can be derived from the selected/identified text, captions, or request: ask where on the timeline it should start and end
   - no screen position exists and the creator did not specify one: ask where it should sit, such as top, middle, bottom, or an exact area
   - both overlapping TextPanel text and captions could be intended: ask which layer should go behind the subject
   - multiple overlapping media items could be the foreground source: ask which subject/item
5. Do not start removal, transcription, duplication, or text creation while one of those choices is unresolved. When existing content supplies timing and position, do not ask the creator to repeat it.

## Prepare the middle layer

1. For existing TextPanel text or captions, leave it in its native layer and record every overlapping item/page and its exact visible interval.
2. For supplied normal text, call `add_text_overlay` only after copy, interval, and placement are known. Refine it with `update_text_item`; keep it static unless the creator explicitly requests motion.
3. For requested subtitles with no caption words, follow `subclip-text-captions`: transcribe the exact audible base media/audio item or import exact timestamped cues. Run one background transcription job at a time and resume this composite only after it is terminal. If the creator requests viral/dynamic captions, load `subclip-dynamic-captions` and finish its semantic priorities/pages before compositing.
4. Define the composite interval as the requested range or, when the request points to existing text/captions, the exact union of their visible intervals clipped to the base media item's timeline window. Never extend the effect across unrelated speech or text.

## Create the foreground duplicate

1. Record the base item's `fileId`, type, timeline start/end, source in/out, playback rate, loop state, mute/volume, fit mode, position, size, rotation, scale, opacity, focus, zoom, crop, styling, effects, keyframes, lane, and composition placement.
2. Keep the base item unchanged and audible. Call `place_editor_asset` with the same media `fileId` to create a new top item only for the composite interval.
3. Map the interval to the same source pixels. For a non-looping base:

   `topSourceStart = baseSourceStart + (compositeStart - baseTimelineStart) * playbackRate`

   `topSourceEnd = topSourceStart + (compositeEnd - compositeStart) * playbackRate`

   Apply those exact values with `trim_media_item` or `update_media_item`. For a looping source that crosses a source wrap, partition it at each wrap into separate contiguous duplicates instead of inventing an impossible source window.
4. Reproduce the base's static framing and every visual property that affects pixel alignment. Copy relevant media keyframes/effect states within the interval using named tools and add boundary states when motion crosses the interval edge. The foreground silhouette must use the same source frame, fit/crop, focus, transform, and timing as the base at every moment.
5. Set every top duplicate to `muted: true`, `volume: 0`, and a separate overlapping lane. The base remains the only audible video copy.
6. Choose the composition plane from the middle layer:
   - TextPanel text: top duplicate uses `layerPlacement: "above-text"`.
   - Ordinary or Dynamic Captions: top duplicate uses `layerPlacement: "above-captions"`.
   - When both must sit behind the subject, use `above-captions` so the foreground covers both.
7. Keep a cloud-bound video duplicate at opacity `0` until its processed replacement is ready so an opaque temporary copy does not hide existing text/captions while processing. Before paid removal, prove from state that its source window and geometry match the base; do not spend credits on a knowingly misaligned duplicate.

## Remove only the duplicate's background

1. A direct request for text/subtitles behind or between the subject and background authorizes one matching background-removal pass for the resolved duplicate after the clarification gate. Pass `confirmed: true`. If the request expands to multiple unrelated paid video removals, disclose the exact count and obtain confirmation for that expanded scope.
2. Call `remove_media_background` with the top duplicate's exact `itemId`, never the base item ID.
3. For a local image result, continue after the tool confirms completion. For video or cloud fallback, store the operation ID and end the in-app turn without polling; Subclip resumes the same conversation on success, failure, or cancellation.
4. On cloud success, call `get_ai_operation`, then `import_ai_operation_to_timeline` with the same duplicate as `replaceItemId`. Video import owns its one editable `colorKey` effect; never add another.
5. Restore the processed top duplicate to opacity `1`, preserve its `above-text`/`above-captions` plane, exact geometry, timeline/source window, and muted state. Do not alter the base plate or middle-layer timing.
6. On terminal failure, preserve the original media and existing text/captions. Delete only an invisible temporary duplicate created by this run when it has no useful processed result; never delete the user's base or source file.

## Verify the composite

1. Re-read assets and prove the stack at the requested time: unchanged base, intended middle text/captions, processed muted foreground duplicate.
2. Seek shortly after the composite starts, at representative subject movement or shot changes, around every text/caption placement change, and just before the composite ends. Call `view_current_frame` at each point.
3. Confirm visible glyphs pass behind the foreground silhouette while remaining visible over the original background. Reject text that is merely placed above the person, entirely hidden, outside safe margins, or unreadable against the plate.
4. Confirm there is no doubled edge, position drift, scale mismatch, green spill, black matte, second color-key effect, duplicate audio, or one-frame timing flash at either boundary.
5. If foreground motion or the shot changes enough to break alignment/matting, split on the real boundary and rebuild a stable aligned top segment. Do not chase the subject by moving only the cutout independently of its base.
6. Update the director brief with the base item, middle-layer item/source, composite interval, foreground duplicate/operation, layer plane, audio policy, and inspected timestamps. Report completion only after rendered pixels pass.

The visual illusion depends on exact duplication. Successful background removal without source/timing/geometry alignment is not a completed text-behind-subject effect.
