---
name: subclip-audio-editing
description: Add and mix music, voiceover, sound effects, and existing audio assets through Subclip AudioPanel, AudioLayer, and UnifiedTimeline. Use for requests about audio, music, voice, volume, muting, fades, looping, pan, playback rate, silence removal, or voice enhancement.
---

# Subclip Audio Editing

1. Call `list_editor_assets` and select an `audioFiles[].id`.
2. Call `place_editor_asset` with `kind: audio`; set start, duration, and volume deliberately.
3. When a supplied reference video provides the soundtrack, call `extract_attachment_audio_to_timeline` with the attachment path or its video-context `originalPath`. This uses native FFmpeg and immediately creates a normal, editable AudioPanel file and timeline item. The operation is idempotent for the same source: reuse the returned existing item instead of extracting or placing it again. Keep `setProjectDurationToAudio: true` when the soundtrack is the master clock.
4. If a local skill or FFmpeg command already created audio inside the project workspace, call `import_generated_audio_to_timeline`; never hide it in custom code or leave it outside the editable timeline.
5. To understand the edit, pass the returned audio `itemId` as `audioItemId` to `transcribe_project` with `purpose: "reference"`. Prefer cloud transcription for accuracy and ask once before starting it when the request has not already authorized credit use. Local Whisper remains available only for ordinary single-speaker transcription when the user explicitly requests local/on-device/no-cloud processing. Speaker detection is cloud-only; never request local diarization.
6. Use `update_audio_item` for the full AudioPanel control surface: timeline/source trim, `volume`, `muted`, `fadeIn`, `fadeOut`, `pan`, `loop`, and `playbackRate`. It preserves every field you do not pass.
7. Keep timing inside the project and avoid accidental overlaps between competing voice tracks. When the user explicitly asks to remove a duplicate, identify the exact muted/zero-volume item and call `delete_timeline_item`; do not leave it muted merely because it is currently inaudible. Confirm its ID is absent afterward.
8. `delete_timeline_item` keeps the source in AudioPanel. If the user explicitly asks to remove audio from the project library too, call `delete_project_assets` with the exact `audioFiles[].id` values and `confirmed: true`; it removes all linked placements. Re-list assets and verify the files and linked item IDs are absent. Never use `update_editor_state` as a deletion shortcut.

Mixing defaults:

- Spoken voice: volume near 1 unless clipping is evident.
- Background music under speech: start around 0.15–0.30 and adjust by context.
- Use short fades at abrupt music boundaries.
- Do not loop voice or sound effects unless explicitly requested.

To create a new sound effect (whoosh, hit, riser, UI sound, foley, ambience) rather than reuse an existing file, read `subclip-music-generation` and call `generate_music` with `modelId: "elevenlabs-sound-effects"`; it imports as an ordinary Audio asset.
- When extracted narration is the master track, call `set_all_video_audio` with `muted: true` so incidental source audio cannot double the voice.

Voice enhancement and silence removal are authenticated AI Tools workflows, not ordinary timeline mutations. Ask for confirmation if a route consumes credits. Report when a requested asset is not yet imported instead of fabricating it.
