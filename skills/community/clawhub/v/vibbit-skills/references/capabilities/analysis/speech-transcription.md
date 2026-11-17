# Speech transcription

Choose the entry point from the actual input:

| Input | Command and result |
| --- | --- |
| Audio URL, including completed adopted speech | [transcribe_audio](../../api/transcribe_audio.md) with `url`; full text, sentences, and words |
| Local audio | [Upload](../../runtime/media-inputs.md) to obtain an `object_url`, then use `transcribe_audio`; do not reupload an accessible URL |
| Supported video/share URL | [breakdown](../../api/breakdown.md) with `sub_tasks: ["asr"]`; segment `from/to/content` |

Preserve audio `transcripts[].text`, `sentences[]`, and each sentence's `words[]`. `begin_time/end_time` are milliseconds; follow [timestamp interpretation](../../api/transcribe_audio.md#timestamp-interpretation) for conversion and zero-duration words. Channels are not speaker identities, and recognized emotion does not establish performance quality.

Preserve actual segment `from`, `to`, and `content` values. A continuous script, formatted subtitles, and a translation are derived outputs and should retain their relation to the source. Check task state before treating an empty response as silence.

Audio transcription uses `transcribe_audio` (`ASR`, only `url`); video transcription uses `breakdown` with `sub_tasks: ["asr"]`, without unrelated analysis. Captions and speech checks share the same applicable result. Reuse earlier timing only after establishing that the adopted soundtrack and its offset, trimming, and speed are unchanged; the same video duration alone is insufficient. New audio needs new timing evidence.

Preserve raw recognition, the adopted script, and actual speech separately. For mixed languages, numbers, names, or background music, listen to flagged passages before attributing errors to audio generation. Agreement between recognizers cannot replace listening evidence.

Routine production should not install Whisper, download models, or wait for new verification dependencies solely to cross-check speech. Use the existing official ASR and host listening capabilities; state unverified checks. Use another tool when specifically needed and supported by the environment and user's request.

When generated speech needs script checking or caption timing, call `transcribe_audio` on the adopted audio before avatar generation, compare it with the script, and listen to uncertain passages. Resolve audio known to need replacement before generating its lip sync. Do not force an extra ASR task when the user only wants their original audio to drive an avatar.

## Independent deliverables and reuse

Save completed results and source versions, then normalize with [transcript tools](../../runtime/transcript-tools.md). Reuse the result for subsequent operations without another ASR call:

- Export recognized TXT and sentence SRT/VTT. Corrections, line breaks, and bilingual display text bind to the original file hash and sentence IDs without replacing recognition.
- Compare adopted speech to obtain listening leads for omissions, repeats, brands, or numeric changes. Text agreement does not establish pronunciation quality.
- Locate literal keywords for sentence candidates. The host can derive summaries, chapters, key points, and semantic selections; actual cutting needs executable media tools.
- Check reuse against associated local file bytes. An equal URL cannot prove unchanged audio. Word export needs complete valid boundaries; zero-duration words do not block valid sentence captions.

Use [audio content workflows](../../workflows/audio-content.md) for recording organization, original audio with visuals, or audio translation. Reuse supplied SRT/VTT or applicable recognition for current media. A script without timing needs actual timing evidence; unspoken titles/information cards do not require ASR.

Burning subtitles is a separate operation. Use [subtitle correction and segmentation](../processing/subtitle-addition.md); precise word events follow [script and timing](../../creation/script-and-timing.md), without fabricated word boundaries. Audio ASR does not enable the currently unavailable dynamic subtitle templates.
