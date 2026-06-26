# Clip State Contract

## Purpose

Every clip should have a clear state label so the pipeline never confuses candidate outputs with deliverables.

## Recommended states

- `image-approved`
  - the still image / first-frame image is approved for this clip

- `video-raw-ready`
  - a usable raw video exists
  - no subtitle/TTS/ambience claim implied

- `subtitle-ready`
  - subtitle text is locked for this clip

- `tts-ready`
  - TTS/dialogue asset exists and matches the active text policy

- `ambience-ready`
  - environment sound is present and scene-correct

- `lipsync-candidate`
  - lipsync output exists but has not yet replaced the main clip

- `final-single-ready`
  - the single clip is honestly deliverable

- `merged-ready`
  - the clip is included in a merged export with truthful labeling

## Output labels for user-facing reporting

Always distinguish:
- raw clip
- subtitled clip
- dialogue/TTS clip
- ambience clip
- lipsync candidate
- final single clip
- merged version

## Forbidden shortcuts

Do not mark a clip as final if:
- duration is unexpectedly shortened
- subtitle and audio intent conflict
- lipsync result is unverified
- ambience is claimed but not clearly present
- the file came from a probe task only
