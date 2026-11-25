# Rough-cut operating policy

## Source assembly

1. Record all pre-existing item IDs before editing.
2. Reuse an imported `mediaFiles[].id` when available. Otherwise import the authorized attachment or the `originalPath` from `.subclip-video-context`.
3. If native import fails, enqueue `import_attachment_clip_with_ffmpeg` once, store its job ID, and end the turn until Subclip resumes it.
4. Keep each source's natural playback rate and audio. Place all sequential material on lane 0 rather than stair-stepping it across lanes.

## Waveform silence pass

Map timeline time to source time with:

`sourceStartTime + (timelineTime - startTime) * playbackRate`

Then map source time proportionally into that file's waveform array.

- Estimate quiet from sustained values near the current file's local noise floor. Never assume zero means silence or reuse one threshold across normalized files.
- Reject isolated dips, breaths, consonants, impacts, and camera handling noise.
- Trim confident leading/trailing dead air while leaving about 80–160 ms of natural room tone around the first and last spoken sound.
- Remove an internal quiet span by default only when it is about 2 seconds or longer. Preserve shorter breath, conversational, comedic, and dramatic pauses unless the creator requests aggressive pacing.
- Snap every boundary to the project frame grid and a nearby waveform minimum.
- Use `trim_media_item` for heads/tails. For internal silence, split at the later boundary, split the earlier result at the earlier boundary, and delete only the isolated middle item.
- Plan all candidates before mutating, apply them latest-to-earliest, and re-list after every deletion.
- If waveform evidence is missing or ambiguous, do not guess. Keep the pause and flag it for review.

## Transcription loop

- Transcribe every surviving audible video item by exact `mediaItemId`, in timeline order and one terminal job at a time.
- Prefer Subclip Cloud; ask once when credit use is not already authorized. Use local Whisper only for an explicit local/offline/on-device/no-cloud request.
- Before each job, write completed and pending item IDs to the director brief. Store the returned job ID and end the turn. On resume, verify the exact source item's saved words before starting the next.

## Filler policy

Auto-remove only unmistakable non-semantic standalone vocal hesitations:

- `um`, `uh`, `erm`, `ah`, `hmm`
- equivalent hesitation sounds in the spoken language

Match case- and surrounding-punctuation-insensitively, but never inside another word. Apostrophes inside real words remain part of the word.

Do not remove these by default because they can be semantic: `like`, `so`, `well`, `right`, `actually`, `you know`, repeated words, and false starts. Include them only when the creator asks for an aggressive cleanup and the sentence remains natural.

- Keep a filler if deleting it would clip an adjacent phoneme, erase meaningful hesitation, or change the thought.
- Prefer a cut from the previous word's end to the next word's start, refined to nearby low waveform energy, instead of the filler token's tight phoneme bounds.
- Merge consecutive filler ranges and ranges separated by less than about 120 ms.
- Apply ranges latest-to-earliest. After each split/delete, re-list and use current IDs/times.
- Do not delete filler caption words before deleting their media. Native lane-0 media deletion removes overlapping owned words and ripple-shifts later captions.

## Verification

Confirm:

- all requested sources remain in the intended order;
- no lane-0 gaps/overlaps were introduced;
- source in/out values remain inside original file durations;
- removed filler words are absent and retained words remain chronological;
- duration ends at the last intentional item.

Seek immediately before/after representative joins, the shortest retained phrase, and the final frame. Inspect with `view_current_frame`, correct flash frames or wrong-source joins, and inspect again. Do not claim click-free audio when the available preview did not permit listening.
