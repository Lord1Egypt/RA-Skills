# Script and semantic timing

Use this when captions, B-roll, graphics, or sound must follow particular words. Maintain one adopted script and use the selected actual audio as timing evidence. Reference-video timestamps, reading estimates, and measured word alignment are different.

## Choose the required precision

Ordinary clause captions and segment-level B-roll or charts can use actual segment times through [subtitle correction and segmentation](../capabilities/processing/subtitle-addition.md). Missing word data does not require installing aligners or block work that segment timing can support.

The word-binding procedure below applies to explicit word highlighting and precisely triggered graphics/sound. The local `production` binding tool requires real word evidence; segment captions can go directly to the selected compositor without fabricated word data. If exact effects need unavailable timing, preserve the design and deliverable parts and explain the gap.

## Express relationships first

Give events stable names, such as `battery-reveal`. A range covers words; a moment follows a word/phrase start or end. Explain deliberate offsets and identify repeated occurrences. Segment boundaries follow independently producible performances, not every camera cut.

Display spelling and pronunciation can differ, such as “API” versus “A P I”; retain their purposes separately. Word evidence must match adopted speech. Do not rewrite user dialogue to fit recognition errors. Silent animation can use explicit seconds/frames without fictional speech.

## Bind to actual media

1. Select the actual audio/video and corresponding script segment. Complete required trimming or speed changes before obtaining timing.
2. Obtain real word-level transcription/alignment with source and media identity. Missing words, wrong text, or missing times require investigation, not even distribution by character count.
3. Locate semantic events at measured word boundaries and add the selected segment's global placement. Captions and graphics share the same timing facts.
4. Adapt these events to real FFmpeg, Remotion/Hyperframes, or supported cloud composition and inspect the final video.

[Local production tools](../runtime/local-production.md) import evidence, check media hashes, and bind events. Video-breakdown ASR supplies segments. [Audio ASR](../api/transcribe_audio.md) returns `sentences[].words[]` as potential word evidence: establish the unit, audio origin, and speech correspondence before converting to the tool's seconds-based `text/start/end` input. Investigate zero-duration words, omissions, or wrong text rather than interpolating or dropping words to bypass validation. Without valid word data, retain event intent and report exact synchronization as pending.

The tool conservatively matches complete segment text, ignoring case and ordinary punctuation while preserving meaningful numeric separators. It does not resolve paraphrases, recognition mistakes, number pronunciation, or complex phonetic mappings. Use actual pronounced text in `speech`. A mismatch stops binding; approximate time must not be called precise alignment.

## Reuse after changes

| Change | Timing consequence |
| --- | --- |
| Caption color/layout or graphic appearance | Reuse valid evidence/events; rerender |
| Same voice, event follows another word | Reuse word evidence; rebind |
| Display spelling only | Reuse audio/timing; declare display-field dependencies |
| Segment placement | Reuse internal times; update global placement |
| New voice/performance, trimming, or speed | Obtain new evidence for the affected media |
| Script or segment identity | Verify new performance correspondence and affected evidence |

Unrelated segments can remain. The lightweight tool uses phrases and explicit occurrence, not stable word IDs or incremental alignment. Even a matching hash cannot prove an imported transcript really came from that media; inspect the evidence.
