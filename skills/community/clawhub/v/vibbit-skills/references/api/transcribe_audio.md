# Audio transcription: transcribe_audio

Task type: `ASR`. Mode: `async`; account access depends on the actual response.

[Submission contract](https://vibbit.apifox.cn/522015345e0) · [Query contract and result example](https://vibbit.apifox.cn/522015766e0)

## Input and submission

| Field | Type | Required |
| --- | --- | --- |
| `url` | Publicly readable audio HTTP(S) URL | Yes |

Upload local files through [media inputs](../runtime/media-inputs.md) to obtain an `object_url`; reuse accessible audio URLs directly. Send only `url`, without `audio_url`, `video_url`, or guessed language/model options. The public example uses MP3; it does not establish support for every format, duration, or language.

Replace the example URL with the actual adopted audio:

```json
{
  "task_type": "ASR",
  "input_info": {
    "input": "{\"url\":\"https://example.com/speech.mp3\"}"
  }
}
```

POST `/openapi/v1/tasks`. `input_info` is an object containing a JSON string in `input`. The client input file contains only `{ "url": "ACTUAL_AUDIO_URL" }`; the script supplies the task envelope.

```bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" transcribe_audio --input /absolute/path/request.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" transcribe_audio --input /absolute/path/request.json --wait
```

Alternatively use `transcribe_audio --url "ACTUAL_AUDIO_URL"`. Save the returned `task_id` and journal. Query GET `/openapi/v1/tasks/{task_id}`; after a wait deadline, continue querying or resume the original task without submitting again.

## Query result

A completed task has `task_info.task_type: "ASR"`. `task_result.result` is a JSON string, decoded and preserved by the client as `result`:

| Path | Meaning |
| --- | --- |
| `transcripts[].text` | Full recognized text for that transcription track |
| `transcripts[].sentences[]` | Sentences with `text`, `begin_time`, `end_time`, `sentence_id`, `language`, `emotion`, and `words` |
| `transcripts[].sentences[].words[]` | Words with `text`, `punctuation`, `begin_time`, and `end_time` |
| `transcripts[].channel_id` | Returned channel identifier; not an established speaker ID |
| `file_url`, `audio_info` | Source media URL and actual format/sample-rate metadata |

Preserve track order, raw text, punctuation, and timestamps. The source audio is not a newly generated deliverable. Do not concatenate multiple tracks into one speech stream without establishing their temporal relationship. Missing text, sentences, or words require inspecting the result before concluding silence.

### Timestamp interpretation

Audio ASR sentence and word `begin_time/end_time` values are milliseconds. Preserve raw values and divide by 1000 for seconds; [transcript tools](../runtime/transcript-tools.md) normalize completed results directly. Times belong to source audio. Trimming, retiming, or adding preceding media requires verifying its timeline mapping. This contract does not establish video breakdown `from/to` units.

Some example words have `begin_time == end_time`. Preserve these values and flag uncertain boundaries rather than stretching intervals, distributing time, or deleting words to fabricate alignment. Valid sentence timing can still produce SRT/VTT or ordinary captions. Word highlighting needs actual boundaries, matching speech text, and final synchronization checks. Transcript tools export seconds-based input for [local production](../runtime/local-production.md) only when complete word evidence is valid; the raw API shape is not directly importable.

[Replaceable input example](../../examples/transcribe-audio.json) · [Transcription and speech checks](../capabilities/analysis/speech-transcription.md) · [Authentication](../runtime/authentication.md) · [Task waiting and recovery](../runtime/task-lifecycle.md)
