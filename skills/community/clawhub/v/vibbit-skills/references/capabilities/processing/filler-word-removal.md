# Filler-word removal

There is no automatic filler-removal command. Use [transcription](../analysis/speech-transcription.md) to locate possible verbal fillers, repetition, and pauses, then propose contextual cuts and intervals. Preserve meaning and deliberate emphasis.

Actual cuts need a supported local editing tool or verified timeline configuration. An analysis-only request does not authorize media processing. Prompt-based editing does not guarantee lossless frame-accurate cuts.

Reuse audio ASR or saved video recognition and obtain seconds-based sentence candidates through [transcript tools](../../runtime/transcript-tools.md). Missing/zero word times cannot support exact word deletion. Listen to establish pauses and meaning, then update captions and timeline mappings after cuts while retaining unchanged evidence.
