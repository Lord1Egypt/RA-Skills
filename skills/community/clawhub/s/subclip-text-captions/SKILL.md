---
name: subclip-text-captions
description: Create and style editable text overlays, subtitles, and dynamic captions through Subclip TextPanel, TextLayer, CaptionsPanel, and caption tools. Use for titles, lower thirds, calls to action, subtitle correction, transcription, caption timing, caption presets, typography, and readable on-screen text.
---

# Subclip Text and Captions

Distinguish text overlays from spoken-word captions.

When the creator asks for text, titles, or subtitles behind a person, behind the subject, or between the subject and the original background, route to `$subclip-text-behind-subject`. It owns the required media duplication, background removal, and composition-plane order; this skill alone must not place the text on top of the subject.

## Text overlays

1. Call `add_text_overlay` with text, timing, position, font size, and color.
2. Use `update_text_item` for the full TextPanel surface: timing, typography, fill/gradient/composite/background, case, weight/style, alignment, outline, shadow, placement, width, scale, spacing, and animation. It preserves fields you do not pass.
   - Every text overlay must span at least one complete project frame: `endTime - startTime >= 1 / fps`. Never create equal, inverted, non-finite, or sub-frame timing. Prefer at least 0.5 seconds for intentionally visible text unless the creator requests a shorter flash. Re-read the item after a timing update and confirm its saved end remains after its start.
3. Keep Text layers static by default for ordinary video edits. Adding, replacing, styling, positioning, resizing, or retiming text does not authorize animation. Do not add Text keyframes or preset animation unless either:
   - the creator explicitly asks for that text to move, animate, enter, exit, fade, scale, rotate, type on, or otherwise change over time; or
   - the request is clearly for a motion-led video, such as kinetic typography, a motion-graphics piece, animated explainer, promo, title sequence, or animated information card, where coordinated text motion is intrinsic to the requested result.
   In a motion-led video, use text motion only when it supports the beat; the exception permits keyframes but does not require every Text layer to animate.
4. When text motion is authorized by the rule above, use `add_text_keyframe` for all new TextPanel motion. Times are absolute project seconds; X and Y are canvas percentages from 0 to 100. Position, text size, scale, rotation, and opacity can change at each point. Add multiple points to the same text item ID instead of duplicating the text.
   - A simple move needs exactly two keyframes: the starting state and the destination state. The destination automatically holds until another keyframe or the item end. Do not add an identical terminal keyframe merely to create a hold.
   - Add a third point only when the text must change again after reaching the destination, such as pausing and then departing.
   - Use `delete_text_keyframe` to remove one exact point without deleting the text item.
5. Do not use `set_text_animation` for new edits. Preset animation fields remain render-compatible for old projects, but authorized new fade, scale, slide, pop, float, glide, wave, and typewriter-like movement must be expressed with explicit TextPanel keyframes so timing and distance remain inspectable.
6. Keyframes remain editable in TextPanel. Moving or duplicating the text item moves its absolute keyframe times with it. Keep every keyframe inside the text item's start/end range. Selecting a keyframe seeks to its time; adjust the Position and Size controls while that point is active to edit that keyframe rather than the base text style.
7. Keep critical text inside safe margins. For static text, inspect a representative visible frame. For animated text, seek to the first keyframe, intermediate travel, and final keyframe, then inspect each with `view_current_frame`.
8. Use `add_text_effect`, `update_text_effect`, and `delete_text_effect` for the ordered **Text Effects** stack. Call `list_element_catalog` first for the exact supported types and parameter schema. This stack is intentionally separate from TextPanel typography, background, shadow, outline, composite mode, and legacy preset-animation fields; never rewrite those fields merely to add an effect. Use the typography outline for a conventional text stroke; use the `outline` effect only when the user wants an alpha-silhouette effect with width, edge simplification, color, opacity, or outline-only controls. When an effect must switch at a specific text keyframe, pass `remotionEffects` to `add_text_keyframe` instead of duplicating the text item.

## Captions

When the creator asks for dynamic, viral, scroll-stopping, emphasized, word-by-word, or preset-based captions, route to `$subclip-dynamic-captions`. When the creator names a HyperFrames caption style or wants captions authored as a HyperFrames layer, route to `$subclip-hyperframes-captions`. Keep this skill for transcription, corrections, speakers, visibility/deletion, and ordinary caption styling.

1. Read existing caption words before changing them.
2. Use `update_caption_words` for wording and timing corrections. Use `update_caption_style` for project-wide caption typography, colors, background card, outline, shadow, placement, width, or animation. Do not use guarded raw state for controls exposed by that named tool.
   - Use `assign_caption_speaker` when one caption page, sentence, or time range is assigned to the wrong speaker. Select an existing `speakerId`; this must not rename other segments.
   - Use `create_caption_speaker` when the creator needs a new named identity that is not in the current speaker list, then use `assign_caption_speaker` to apply it to the intended segment.
   - Use `rename_caption_speaker` when the creator wants one identity renamed everywhere, such as `Speaker A` to `Female`. This updates the speaker list and every assigned caption word.
   - Treat **delete/remove** and **hide/turn off** as different creator intents. For “delete” or “remove,” call `delete_caption_segment`; select an entire clip with `sourceItemId`, one sentence with `sourceItemId` plus one-based `sentenceIndex`, one word with `wordId`, or use `pageId`, `wordIds`, or an exact time range. Source-aware selectors preserve captions owned by other clips. The prompt checkpoint/Undo provides recovery. An explicit delete request is sufficient authorization; do not ask again or substitute hiding.
   - For “hide,” “turn off,” or “do not render,” call `set_caption_segment_visibility`. Use `set_caption_speaker_visibility` to hide or restore every rendered caption assigned to one speaker. Hidden captions remain editable transcript data, appear struck through in the Captions library and UnifiedTimeline, and must never be described as deleted.
   - After deletion, re-read the caption inventory and confirm the selected word IDs or time range are absent. After hiding, confirm the words remain with `hidden: true` and that preview/export no longer renders them.
3. Use `transcribe_project` with `purpose: "captions"` when visible captions do not exist, the user requests regeneration, or another soundtrack needs captions. Pass an exact `mediaItemId`/`audioItemId` for one clip. Set `allTimelineClips: true` when the user asks for every clip or the finished audible timeline should become one coherent replacement transcript; never guess missing item IDs. Exact-item mode preserves other sources and replaces only that source, while all-timeline mode atomically replaces the complete caption set. Pass base ISO codes such as `fr`, not regional locales such as `fr-FR`. Do not manually offset words, clear `subtitleData`, or ask for an SRT while audible timeline items exist. Prefer `mode: "cloud"` only when chosen or diarization is requested; cloud work may consume credits.
4. Use `mode: "local"` only for ordinary single-speaker transcription when the user explicitly asks for local, on-device, offline, or no-cloud processing. Local diarization does not exist. If the user requests speaker detection, use cloud mode or explain that speaker-aware transcription requires Subclip Cloud. Local processing itself is already authorized and free; after the user selects it, do not ask for another approval. Start one model and never launch another local model concurrently.
5. Before replacing any active local or cloud transcription, call `stop_transcription` and wait for its successful response. Then start the selected route. Prefer one `allTimelineClips: true` run when every audible clip is in scope. Use sequential exact-item runs only when independently owned caption batches are required; never clear current captions first.
6. Store the `jobId` returned by every local or cloud `transcribe_project` call. For the in-app coding agent, do not poll: the host resumes the same conversation only after completion, a concrete error, or cancellation. On an exact-item run, existing captions from every other source remain present and are not proof that the new job completed. Do not manually move the completed words or interpret an unchanged total word count as success or failure. External MCP clients may call `get_transcription_status` with `projectId` and the exact `jobId`.
7. Use `stop_transcription` whenever the user asks to stop, cancel, replace, or abandon transcription. One call stops local Whisper, aborts the desktop cloud job, and sends cancellation to its active Subclip Cloud server run. The tool is safe when no run is active; inspect its `serverCancellation` result instead of assuming a remote run existed.
8. Preserve chronological word order, nonnegative times, and readable page grouping.

## Speaker-aware transcription

- Speaker detection is off by default. Enable it only when the user asks to detect, separate, identify, or label speakers.
- Call `transcribe_project` with `detectSpeakers: true`. Use `expectedSpeakerCount` only when the user supplies a count or reliable project evidence makes it clear; otherwise leave it unset for automatic detection. Do not infer the number of audible speakers solely from visible faces.
- Speaker-aware transcription is cloud-only. Cloud mode uses Subclip's diarized multi-speaker STT. Speaker detection is automatic; an expected count is validation metadata, not a provider control. Never offer or request local diarization, sherpa-onnx, isolated speaker tracks, or per-speaker local Whisper passes.
- When regenerating captions that already contain speaker metadata, preserve speaker-aware mode unless the user explicitly disables it. A requested speaker-aware run that returns no labeled speakers is an error; do not replace the existing captions with an unassigned transcript or report partial diarization as success.
- Store `speakerId`, `speakerLabel`, and the project speaker list with captions. Show a speaker label above its sentence in the Captions library only. Never insert speaker names into the rendered subtitle text or show them as UnifiedTimeline labels unless the user explicitly requests visible labels.
- Preserve manual speaker renames and assignments when captions are regrouped or restyled.

Prioritize contrast, short line lengths, consistent placement, and legibility on the selected aspect ratio. Do not turn decorative titles into caption words or rewrite spoken content without the user's intent.

## Perspective tilt

Use `update_text_item / update_caption_style` with optional `tiltX`, `tiltY`, and `tiltZ` fields in degrees, each from -88 to +88. X tilts vertically, Y tilts horizontally, and Z rotates in the image plane. These static appearance controls preserve existing animation and are editable under Perspective tilt in the layer settings. Use small angles for legibility; never add a back face or substitute a 3D model. Set all three to 0 to reset. For text overlays use update_text_item with the exact itemId; update_caption_style changes project-wide captions.

Keyframes: use `add_text_keyframe` for animated `tiltX`, `tiltY`, `tiltZ` (-88..88 degrees) and `scale` (multiplier). These values interpolate with the keyframe easing, preserve omitted settings, and remain editable in the keyframe UI.

## Tilt troubleshooting and scope

- Supply only finite numeric degrees for `tiltX` (vertical), `tiltY` (horizontal), and `tiltZ` (in-plane), within -88..88. Never send NaN, Infinity, or unit-suffixed strings.
- Reset with numeric zero on all three axes. Do not replace native layers with a 3D model.
- Use `add_text_keyframe` on the exact existing item ID and absolute project time to animate tilt and scale. Omitted tilt inherits the previous keyframe or base style; missing base tilt is zero. Keep existing scale unless the user requests a change.
- Changing base tilt alone will not override explicit tilt keyframes. Update the relevant keyframes instead. Older media keyframes need no recreation merely because they lack tilt fields; the sampler provides defaults.
- Distinguish saving settings from visually confirming the effect. Do not claim preview/export validation unless it was performed.
