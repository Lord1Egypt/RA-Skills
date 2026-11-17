---
name: voice-cloning
description: >
  Create a custom voice and speak text in it. Use when the user says "clone my voice", "make it
  sound like this recording", "use my voice for the narration", "design a voice that sounds like
  an old wizard", "a warm female voice with a British accent", or wants a repeatable custom voice
  rather than a stock preset. Two paths: clone from an audio sample, or design a new one from a
  written description. If the user just wants narration in a stock voice, use voiceover. For two
  speakers, use dialogue-audio.
---

# Voice cloning

Produce speech in a *custom* voice, one you either clone from a real recording or design from a text description, then synthesize any text in it. The difference from plain text-to-speech: the voice is bespoke, not picked off a preset list. Two intents live here, clone-from-sample and design-from-description, and they route to different models.

## Inputs to collect

- **Which intent:** clone an existing voice (have a recording) or design a new one (have a description). This picks the model.
- **For cloning:** a clean reference recording of the target voice. A few seconds is enough (Qwen ~3s, Dia ~5-10s). Mono, low noise, single speaker. Plus a transcript of what's said in it if using the Qwen clone path.
- **For designing:** a voice description covering gender, age, timbre, accent, pace, and mood (e.g. "warm older male, gentle British accent, unhurried").
- **The text to speak**, and the target language.
- **Consent / likeness:** clone only voices you own or have explicit rights to. Refuse cloning a third party's voice without permission.

## Models

- **Clone from a sample (single speaker): Qwen3-TTS Base** (`alibaba:qwen@3-tts-1.7b-base`). Takes the reference recording in `inputs.audio` with `speech.voice: "clone"`. Highest-similarity mode (ICL) needs a `transcript` of the sample; embedding-only mode (`settings.xVectorOnly: true`) skips the transcript at lower similarity. 10+ languages.
- **Clone for dialogue / multi-speaker: Dia 1.6B** (`runware:dia@1.6b`) or **Dia2 2B** (`runware:dia2@2b`). Reference voices go in `inputs.audios` (first = `[S1]`, second = `[S2]`), supports non-verbal cues. English only. Dia2 streams and is the newer pick.
- **Design from a description: Qwen3-TTS VoiceDesign** (`alibaba:qwen@3-tts-1.7b-voicedesign`). The voice is created from a natural-language description in `positivePrompt`, with `speech.voice: "design"`. No recording needed.
- **Premium preset timbres (not cloning): Qwen3-TTS CustomVoice** (`alibaba:qwen@3-tts-1.7b-customvoice`). Nine curated timbres (`aiden`, `serena`, `vivian`, …) plus a style hint. Use it when a polished stock voice with style control beats a clone.

Confirm each model is `live` and inspect its schema via `runware-models` + `runware-run` before calling. Voice/cloning fields differ per model, never hardcode them.

## Workflow

1. Resolve the chosen model's schema (`runware-run`) and confirm the cloning/voice fields and `speech.text` limit.
2. Upload the reference recording (cloning paths) into `inputs.audio` (Qwen) or `inputs.audios` (Dia). For designing, no upload, just the description.
3. Build the request: `taskType: "audioInference"`, the model AIR, `speech.text` with the lines to speak, plus the voice field for that model.
4. Run **asynchronously** and poll `getResponse` to terminal. Audio is a time-based task, do not block a sync call on it.
5. Read the audio URL from the result, then check it before returning (see Quality bar).

## Technique

- **Reference quality sets the ceiling.** A clean, dry, single-speaker sample clones well. Background music, reverb, or two voices in the clip degrade similarity more than any setting can recover.
- **Qwen clone, ICL vs embedding.** Provide the `transcript` of the reference for the high-similarity ICL mode. Only fall back to `settings.xVectorOnly: true` (no transcript) when you cannot transcribe the sample, and expect a looser match.
- **Design by stacking traits.** For VoiceDesign, write the `positivePrompt` as ordered attributes: gender and age, then timbre, then accent, then pace and mood. "A bright young female voice, soft timbre, light Spanish accent, quick and upbeat" beats a vague "nice voice."
- **Style and emotion ride the prompt.** On CustomVoice and VoiceDesign, a style hint in `positivePrompt` ("Speak with great enthusiasm") shapes delivery on top of the voice. This is the same emotion/delivery lever covered in `voiceover`.
- **Dia speaks dialogue.** Tag lines `[S1]` / `[S2]` in `speech.text` and align them to the reference order in `inputs.audios`. Insert non-verbal cues inline like `(laughs)`, `(sighs)`, `(coughs)`. For turning that into a back-and-forth scene, compose with `dialogue-audio`.
- **One voice, many lines.** Once a clone or design reads right, reuse the exact same inputs (same reference, same description, same voice settings) across every line so the character stays one voice and does not drift between clips.

## Parameters that matter

- `speech.text` - the lines to speak. Max **2000** chars on Qwen variants, **3000** on Dia. Split longer scripts.
- `speech.voice` - `"clone"` (Qwen Base), `"design"` (VoiceDesign), a preset id (CustomVoice). Dia has no `voice` field, the reference audio is the voice.
- `inputs.audio` (Qwen Base, single string) / `inputs.audios` (Dia, up to 2) - the reference recording(s) as URL, UUID, or base64.
- `settings.transcript` + `settings.xVectorOnly` (Qwen Base) - transcript drives high-similarity ICL, `xVectorOnly: true` trades similarity for skipping it.
- `speech.language` - `Auto`, `English`, `Chinese`, `Japanese`, `Korean`, `German`, `French`, `Russian`, `Portuguese`, `Spanish`, `Italian` (Qwen). Dia is English only.
- `speech.speed` - 0.25 to 4 on Qwen variants (default 1).
- `CFGScale` / `settings.temperature` (Dia) - lower temperature is cleaner and more consistent, higher is more expressive but riskier. Confirm exact field names against the live schema, never guess.

## Quality bar

- The cloned voice is recognizably the reference speaker, or the designed voice matches every requested trait (gender, age, accent, mood).
- Speech is clean: no clipping, garble, dropped words, or runaway hallucinated tail audio. Retry with a lower temperature or a cleaner reference if it drifts.
- Across a multi-line set the voice stays identical (same inputs reused), not a near-cousin per clip.
- Likeness consent was confirmed for any cloned real person.

## Related skills

`runware-run`, `runware-models`, `runware-prompting`; `voiceover` (single-narrator delivery and emotion control), `dialogue-audio` (multi-speaker conversations from these voices).
