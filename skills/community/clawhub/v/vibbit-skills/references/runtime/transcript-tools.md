# Transcript files, subtitles, and speech checks

`scripts/transcript.js` uses Node 18+ and local files only. It makes no API calls, downloads, model installations, generation, or cuts. Obtain actual recognition through [speech transcription](../capabilities/analysis/speech-transcription.md); saved results need no account configuration.

## Save once and reuse by purpose

Save a completed query response or CLI result as `completed-asr.json`. Task journals support query recovery and do not contain full transcripts. Continue querying the original task when unfinished; pending or failed output is not caption evidence.

```bash
node "$VIBBIT_SKILL_DIR/scripts/transcript.js" normalize \
  --input /absolute/project/completed-asr.json \
  --media-file /absolute/project/adopted.mp3 --out /absolute/project/transcript.json
node "$VIBBIT_SKILL_DIR/scripts/transcript.js" text \
  --input /absolute/project/transcript.json --out /absolute/project/recognized.txt
```

Audio ASR `begin_time/end_time` are milliseconds and are divided by 1000. For video ASR `items` or `sub_results`, supply its confirmed `--time-unit seconds|milliseconds` and `--source-url "actual video URL"`. Multiple audio tracks require one actual `--channel-id`; channels do not establish speaker identity. Omit `--media-file` when only a URL exists. A local file must be the adopted source, not a different file of equal duration.

Normalized JSON preserves raw results, full text, and original sentence/word values. It adds seconds-based `start/end`, stable sentence `id` values, source URL, available task ID, input hash, and `issues`. A media hash records an operator-associated file, without proving that its audio matches the remote URL. Retain actual upload/adoption records and listening evidence. Trimming or retiming invalidates direct timing reuse. Every output must use a new path; existing files are never overwritten.

The [result example](../../examples/transcript-result.json) is an original offline fixture. Its URL, task ID, and text are not real task evidence or product facts.

## Subtitle files and derived display text

```bash
node "$VIBBIT_SKILL_DIR/scripts/transcript.js" subtitles \
  --input /absolute/project/transcript.json --format srt --out /absolute/project/captions.srt
```

Use `--format vtt` for WebVTT. Cues retain real sentence times; valid sentence captions can be exported despite zero-duration words. Missing, reversed, overlapping, or zero-duration sentences block export and require inspecting recognition or listening to establish corrections. The tool never distributes timing evenly. A subtitle file is not a captioned video.

For correction, line breaks, or bilingual captions, create a separate `display.json` and add `--display /absolute/project/display.json`:

```json
{
  "version": 1,
  "transcript_sha256": "actual SHA-256 of normalized transcript.json",
  "cues": [{ "id": "0", "text": "Corrected display text", "translation": "Optional translated text" }]
}
```

Use the SHA-256 returned by normalize and actual normalized sentence IDs. Recheck the binding if normalized file bytes change. Partial overrides are allowed; other cues keep recognition text. Display changes do not modify speech, recognition, or timing. Line breaks stay inside the same cue; sequential splits need real boundaries under [subtitle processing](../capabilities/processing/subtitle-addition.md).

## Speech differences and content locations

```bash
node "$VIBBIT_SKILL_DIR/scripts/transcript.js" compare \
  --input /absolute/project/transcript.json --script /absolute/project/adopted.txt \
  --out /absolute/project/speech-check.json
node "$VIBBIT_SKILL_DIR/scripts/transcript.js" locate \
  --input /absolute/project/transcript.json --query "brand or keyword" \
  --out /absolute/project/locations.json
```

compare ignores case and ordinary punctuation, preserves numeric differences, and reports missing, extra, or changed recognized text. Locations are sentence listening ranges; none are invented when full text cannot be mapped to sentence text. `matches_recognized_text` establishes text agreement only, not pronunciation, audio quality, or lip sync. Numbers spoken as words and phonetic variants may differ; listen before correcting captions, revising speech, or generating again. Compare very long recordings by actual passages if the bounded comparison limit is reached.

locate searches literal keywords and returns sentence candidates. The host can organize chapters, summaries, or semantic selections from the transcript and listen to establish boundaries. It does not cut media; use [video slicing](../capabilities/processing/video-slicing.md) or existing local media tools.

## Reuse and word timing

```bash
node "$VIBBIT_SKILL_DIR/scripts/transcript.js" reuse \
  --input /absolute/project/transcript.json --media-file /absolute/project/adopted.mp3
node "$VIBBIT_SKILL_DIR/scripts/transcript.js" words \
  --input /absolute/project/transcript.json --out /absolute/project/asr-words.json
```

reuse compares associated media bytes. Unchanged bytes allow reuse of the association; changed bytes require new evidence or a verified edit mapping. A URL-only check (`--source-url`) returns `reusable: null` even if equal, because a URL cannot prove unchanged audio or offset. The tool never submits ASR automatically.

words exports only complete, positive-duration, ordered word evidence matching each sentence. Missing/zero words or times outside sentence bounds block export while raw evidence remains intact. Observed punctuation is appended to exported `text` so decimal separators remain meaningful. Never drop, stretch, or evenly time words to pass checks.

Import valid word files with `production.js import-timing` under [local production](local-production.md), then bind word events. Usually record adopted speech as its own `kind: "audio"` output and import timing for that same file. The run's timing references this audio output, with `at_seconds` defining its program placement; verify the avatar video's soundtrack and synchronization relationship separately.

`media_sha256` belongs to the file associated during normalize. Speech audio and an avatar video have different file hashes; never replace the audio hash with a video hash or remove the check to force import. To use a video as the timing source, obtain/verify evidence for that actual video and its soundtrack relationship. File identity and range checks are not acoustic verification. Dynamic subtitle templates remain unavailable.
