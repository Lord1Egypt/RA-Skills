# 1:1 visual remake

Use this when the user wants to retain a source video's camera work, actions, and structure while replacing people, objects, or scenes. “1:1” is a preservation goal, not a square aspect ratio or a promise of pixel/frame identity. For a new script borrowing expressive structure, use [reference adaptation](reference-remake.md).

When the source or replacement images are in the library, use [material reuse](../resources/materials.md) to read explicit IDs or inspect discovered candidates. Fix the source version and each identity/product/scene reference role. Names and categories do not prove identity or product equivalence; analyzed segments only help locate footage, while edit intervals still follow this workflow’s duration, action and sound rules.

## Source and selected elements

Use the actual attachment, direct URL, share link, or existing material. Resolve share pages and prepare local files through [media inputs](../runtime/media-inputs.md). Preserve source and selected versions, ratio, duration, audio, and relevant intervals.

Reuse explicit choices. If the user only asks what can be replaced, deliver candidates. If production is requested without a replacement target, show identified elements and obtain that selection rather than replace everything. At the start of actual production, check/reuse the key through [authentication](../runtime/authentication.md); if missing, open or provide setup and continue after verification. Check editing, upload, audio restoration/composition, and translation before generating pictures. Seedance 2.5 generates at most 30 seconds per request; edit inputs must be 4–30 seconds. Longer remakes must follow the splitting procedure below; automatic duration does not waive the limit.

Inspect actual video and relevant audio. Limited frames/transcripts support only limited observations. Identify:
- People by clothing, position, actions, appearances, and speaking role, including profiles, occlusion, reflections, and screen images.
- Objects by identity, placement, handling, close-ups, labels, reflections, and contact.
- Scenes by space, light, camera motion, perspective, foreground/background, contact surfaces, and shadows.

Keep one stable identifier per recurring entity. A concise candidate list can show the element, representative frame/time, description, and picture source: uploaded, existing, or newly generated. Only selected or already specified elements enter production. Music/voice changes require the relevant audio request, not image replacement.

## Replacement references

For each selection, retain original identity, target appearance, image purpose, and preserved elements. Appearance, market, and language are separate. Do not infer nationality from appearance or equate English with one appearance. When a vague request for a foreign presenter lacks a picture or role description, clarify the desired market/character; authorized autonomous design can use explicitly stated creative assumptions.

Use actual user pictures and resolve ambiguous mappings. A character picture is not a digital human resource ID. Generate a reference only when needed through [image generation](../capabilities/generation/image-generation.md).

For a face-only change, preserve clothing and action; for a full appearance change, specify its scope. Use clear face/clothing views compatible with the source; add side/full-body references only as needed. Scene pictures should support the camera perspective, scale, activity area, and light. Product pictures preserve real shape, material, and markings.

For an explicit facial-feature or hairstyle replacement, first follow [facial identity replacement](face-identity-replacement.md): reuse or prepare a suitable appearance anchor and obscure the source features/hair being replaced, then use this page's mode and audio route. Clear source/target selection does not skip identity preparation. Clothing-only changes retaining the performer continue normally.

Use actual `reference_image_urls` for image-based generation. Do not invent masks or singular fields, and do not claim an image was bound after merely describing it in words. Inspect and adopt the real output. Respect requests to choose pictures before production and authorized output counts.

Examples: [character image](../../examples/one-to-one-remake/character-image.json), [scene image](../../examples/one-to-one-remake/scene-image.json). Their fictional designs must be replaced with the user's requirements.

## Edit and inspect

Specify which source entity and intervals change, which reference controls each property, and what must remain. In a supported platform workflow, retain its actual candidate/asset selection. With public APIs, use [video editing](../capabilities/processing/video-editing.md#video-segment-edit); the public command does not automatically identify all replaceable elements or save a remake project.

For Seedance 2.5 edit, apply the audio and duration rules below first, then send the appropriate clip and replacement references with explicit numbering/roles. Use `aspect_ratio=adaptive` and `duration_seconds=-1` under the [API](../api/seedance.md). Automatic duration follows a compliant clip; it does not allow a video longer than 30 seconds. Do not switch to ordinary reference generation while claiming to edit the source.

Default output resolution to `720p` under [paid video settings](../capabilities/generation/video-generation.md#paid-video-settings). `adaptive` follows aspect ratio, not a source's 1080p/4k generation resolution; use another supported resolution only when explicitly specified by the user.

### Route audio before submission

Source BGM can affect remake reliability. Use the user's established change scope: changing appearance, products, or scenery does not imply changing dialogue, voice, or music. Do not ask again about already confirmed preservation requirements.

| Requested changes | Video submitted to Seedance | Audio after generation |
| --- | --- | --- |
| Visual changes only; dialogue, sound, and BGM unchanged | A real silent copy/clip with its audio stream removed; retain the original video/audio | Inspect and assemble the edited visuals, then restore the original BGM/audio on its source timeline |
| Dialogue, voice, or BGM changes, including downstream translation | Original video or corresponding clip with original audio intact | Inspect the sound to retain/change at the current stage, then complete planned audio changes; never overwrite adopted new audio with the original track |
| Source has no audio and no new sound is requested | Verify the absence of audio, then use the video/clip | Keep it silent |

**Silent route:**

1. Preserve the original video/audio and its duration, starting offset, sample rate, and stream mapping. If dialogue, BGM, and ambience are mixed and all remain unchanged, preserve the complete mix. Do not pretend to have isolated BGM or discard dialogue. If separate BGM already exists, restore the intended mix and other preserved sounds; do not automatically run source separation.
2. Use available [local composition](../capabilities/processing/local-composition.md) or a supported existing processing path to create an audio-free copy while preserving picture, timing, and aspect ratio. Verify it has no audio stream, upload that copy, and use its real URL. A “mute” prompt, muted playback, or the original audible URL is not a silent input.
3. Set `generate_audio=false`. Focus the prompt on visual replacement and preserved movement, mouth motion, and timing. Do not ask the model to reconstruct the soundtrack or send the old BGM as `reference_audio_urls`. This flag controls generated sound and does not remove audio from the input video.
4. Inspect actual output duration, movement/mouth timing, and replacement quality. For split work, assemble all adopted visuals first and restore the complete original audio once, avoiding music restarting at every join. Explicitly select the new video and original audio streams; discard unexpected generated sound to prevent doubled music/dialogue.
5. Check synchronization at the opening, joins, and ending, dialogue, music continuity, and total duration. Resolve timing drift in the affected visuals/time mapping before restoring audio. Do not conceal mismatches by truncating the tail with `-shortest` or arbitrarily stretching the original audio. Preserve usable work and identify unresolved clips; silent intermediates are not the final delivery.

**Audio-change route:** Preserve original audio and cut audio/video together. Specify the affected dialogue/sound/music and preserved parts in the prompt; enable audio generation as needed. Listen to the result and adopt the verified audio changes. Do not silently substitute the silent route. Preserve unaffected sound; if independent tracks are needed but unavailable, explain the limitation instead of claiming mixed BGM can be replaced independently.

If the same task requests translation or dialogue changes, use the audible-source route even when those changes belong to a downstream stage. Record which source speech Seedance should retain and which content the later stage must change; handling visuals first does not remove the user's audio-change request.

For speech-aware cut points or captions, reuse source video ASR or [transcribe the actual original audio](../capabilities/analysis/speech-transcription.md) and preserve a [timing record](../runtime/transcript-tools.md). Sentence times help avoid mid-sentence cuts but do not replace visual/action checks or the 4–30-second clip limit. Reuse caption times only after restoring unchanged original sound and verifying offset/speed; new sound needs new evidence.

### Split videos longer than 30 seconds, then assemble

1. Probe the actual requested interval. Above 30 seconds, plan consecutive clips around natural cuts, pauses, or sentence boundaries. Each edit input must be 4–30 seconds, with no more than 30 seconds of reference video in one request. Submit clips separately rather than putting the whole set into one request.
2. Cover the complete target interval and record source `start/end`, clip duration, and final timeline position. Adjust boundaries to avoid tails shorter than four seconds: 31 seconds can be 27+4; 61 seconds can be 30+27+4. Choose actual boundaries for the content. If the entire source is shorter than four seconds, use an available context-bearing source interval or another supported path; do not invent padded source content.
3. Cut on actual frame boundaries and measure exported durations instead of trusting requested offsets. Stream copying may be constrained by keyframes; use suitable accurate trimming when boundaries or limits are missed. Preserve source-to-local time mappings without gaps, duplicated coverage, or unrequested transitions.
4. Reuse the same adopted person/product/scene references, model, and output settings across clips. Describe entities actually present and convert source times to clip-local times. Submit silent clips for unchanged audio, audible source clips for audio changes.
5. Record each real input, request/task journal, and adopted output. Assemble in source order, matching necessary codec/size/frame-rate conditions. Inspect identity, products, lighting, camera movement, actions, and mouth motion at joins. For unchanged sound, restore the full original audio once after visual assembly; for audio changes, assemble the adopted edited sound and check continuity.
6. Reuse successful clips when another fails or needs revision; repair only failed/affected portions. Once all clips are ready, inspect final duration and complete ending coverage. Assembly does not guarantee cross-clip identity consistency; locate and repair actual drift.

[Replacement example](../../examples/one-to-one-remake/replace-person.json) demonstrates the unchanged-audio silent route. Replace demo URLs with a real silent clip and adopted references, update descriptions, then dry-run. For requested audio changes, use the real audible clip and adapt audio settings/prompts rather than copying the silent example. Inspect completeness of replacement and preservation, especially profiles, occlusion, hand contact, reflections, cuts, perspective, duration, and sound. A prompt to preserve audio is not proof that the output did.

## Continue into translation

Use this dependency order:

Source → selected replacement references → adopted edited video with correct source speech → target-language voice/subtitles/optional lip sync → final video.

Prepare language/terminology early, but submit the adopted edited visual version to translation. Do not accidentally send the original person again.

Verify the edited video's speech and synchronization first. If silent or damaged, restore correct source audio only when timing is compatible and checked; otherwise realign it. Silent footage is not a complete spoken-video translation input.

Use [video translation](../capabilities/processing/video-translation.md) with the edited `source_video.url` and `voice-only` to retain the selected new appearance. Enable lip sync when requested for visible speech; do not add another avatar. Reuse the same adopted visual version for additional languages unless markets require distinct visual versions. A person change does not determine voice support.

Set target languages explicitly. Subtitles and original-caption removal follow user needs. Speech translation does not translate every sign, chart, or product label. Check removal damage and each final language's text, speech, lip sync, and appearance. Automatic production uses `auto_translate: true`; manual review follows the translation contract.

[English translation example](../../examples/one-to-one-remake/translate-english.json) demonstrates a Chinese-speaking source being localized to English with visible speech and subtitles. Replace its URL with the inspected edited video and adapt language/options to the real task.

## Reuse and delivery

For residual marks, color errors, or other localized details in an adopted remake, use [video review](../capabilities/analysis/video-review.md) to locate every affected interval, prefer a reliable local fix or edit only the necessary clips, and splice them into the adopted video. Reuse the remaining replacements rather than restarting the whole remake. A global person or scene change follows its actual scope of impact.

Record source version, candidates/selections, reference roles, preserved elements, valid source audio, languages, and actual tasks/results using [handoff](../contracts/creative-handoff.md). Include requested dialogue/BGM changes, the chosen audio route, preserved original audio, each clip's source/local time mapping, silent/audible inputs, adopted outputs, and audio restoration status. Use a [production plan](../contracts/production-plan.md) for multiple stages/revisions.

A new picture affects corresponding visuals and dependent translated outputs. Added languages reuse adopted visuals/audio. Caption styling reuses valid media. A new source/trim range needs new appearance/time mapping. Preserve successful clips/languages and resume existing task IDs.

Distinguish replacement pictures, edited previews, and final language videos. Highlight final outputs when those are the requested deliverables and disclose remaining deviations or unreviewed parts.
