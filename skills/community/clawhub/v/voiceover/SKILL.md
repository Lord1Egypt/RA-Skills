---
name: voiceover
description: >
  Generate spoken voiceover and narration from a script, one speaker, with control over emotion,
  pacing, and voice. Use when the user says "read this in a warm voice", "narrate my video",
  "voiceover for this ad", "turn this script into audio", "audiobook narration", "an IVR or phone
  greeting", or wants text-to-speech with a specific delivery. For two speakers trading turns, use
  dialogue-audio. To clone a specific voice or design a new one from a description, use
  voice-cloning. To attach the result to a video, use add-audio-to-video or talking-avatar.
---

# Voiceover and narration

Turn a written script into natural spoken audio with directed delivery: the right emotion, pacing, emphasis, and voice for a video, an ad, an audiobook, or an IVR prompt. The lever is inline `[bracket]` direction tags that steer how each line is read, not just the words themselves.

## Inputs to collect

- **The script.** The exact text to speak. (Ask only if none provided.)
- **The voice.** A preset/voice ID, or "pick a fitting one." For a custom or cloned voice see `voice-cloning`.
- **The delivery brief:** mood, energy, pace, and audience (calm audiobook, upbeat ad, neutral IVR, urgent alert). This drives the bracket tags.
- **The use:** video VO, ad, audiobook chapter, IVR/phone prompt. It sets the tone and whether filler words and non-verbals belong.
- Optional: language, and whether the source text is raw LLM output that needs normalizing (numbers, dates, abbreviations).

## Models

- **Default expressive narration: Fish Audio S2.1 Pro** (`fishaudio:s2.1@pro`). Flagship multilingual TTS with rich bracket-tag control over emotion and paralanguage, 80+ languages, fast streaming. Best general voiceover pick.
- **Conversational / realtime delivery: Inworld Realtime TTS-2** (`inworld:tts@2`). Free-form natural-language steering tags and built-in `settings.textNormalization` for clean speech from raw text. Strong for assistants, IVR, support agents.
- **Preset premium timbres: Qwen3-TTS CustomVoice** (`alibaba:qwen@3-tts-1.7b-customvoice`). Nine preset voices with a style hint via `positivePrompt`. Runware Optimized.
- **Streaming dialogue-style TTS: Dia2 2B** (`runware:dia2@2b`). Real-time streaming with non-verbal cues and speaker tags. Runware Optimized.
- Confirm each is `live` and inspect its exact fields via `runware-models` + `runware-run` before calling. Never hardcode a stale choice.

## Workflow

1. Resolve the model schema (`runware-run`) and confirm the field names. The shape is `audioInference` with `speech.text` plus `speech.voice` (some models accept `speech.language`).
2. Write the script into `speech.text` with inline `[bracket]` direction tags placed before the text each one applies to.
3. If the text is raw LLM output (digits, dates, `$1,249.99`, abbreviations), enable normalization so it is spoken cleanly: `settings.textNormalization: true` on Inworld TTS-2.
4. Run `audioInference` **asynchronously** and poll `getResponse` until terminal. Audio is a time-based task, do not block a sync call on it.
5. Read the result from `audioURL`. Listen back, check the delivery against the brief, and retry lines that miss.

## Technique

- **Direction tags steer delivery, apply forward.** A `[bracket]` tag placed before text tells the model how to read what follows. It carries forward **until the next tag** or the end of the input. You do not close or reset it. Drop a new tag where the mood shifts: `[speak cheerfully] Great news, the build passed! [lower voice, more serious] But we need to talk about the memory leak.`
- **Write stage directions, not keywords.** "Say this like you're confiding in a close friend late at night" beats "intimate". The model responds to prose. Layer multiple dimensions in one tag, mood plus pacing plus volume plus manner: `[say sadly with deliberate pauses in a low voice and hushed style]` is a real read, "sad" is not.
- **Core tags vs free-form.** Fish S2.1 Pro ships reliable built-in tags (`[excited]`, `[sad]`, `[whisper]`, `[laughs]`, `[angry]`, `[surprised]`) and also accepts any descriptive phrase (`[whispers sweetly]`, `[laughing nervously]`). Start with the core set for consistency, reach for free-form when you need nuance the core set misses.
- **Paralanguage for timing and texture.** Insert specific audio events where they land. Fish S2.1 Pro uses parenthesis cues `(break)`, `(long-break)`, `(breath)`, `(sigh)`, `(laugh)`, `(cough)` and **requires `settings.normalize: false`** for them. Inworld TTS-2 uses inline non-verbals `[laugh]`, `[sigh]`, `[breathe]`, `[clear throat]`, `[cough]`, `[yawn]`. Place them where a human would actually do them.
- **Text-level controls work without tags.** Capitalize a word to stress it (`I told you NOT to do that`), partial caps stress a syllable (`AbsoLUTEly`). Punctuation paces the read: periods are full stops, commas are short breaks, ellipses trail for hesitation. Use emphasis on one or two words per sentence at most.
- **Normalize when piping LLM output.** LLMs emit digits, dates, currencies, and markdown. `settings.textNormalization: true` (Inworld) expands `$1,249.99` to "one thousand two hundred forty-nine dollars and ninety-nine cents" and `3:45 PM` to "three forty-five PM" before synthesis. Or instruct the LLM to write spoken-form text and ban markdown in its system prompt (see the TTS-2 LLM system-prompts guide). Normalization can be ambiguous on dates, so normalize those yourself when the application handles them.
- **Match fillers to the use.** "Uh", "um", "well" make a companion sound human and make an IVR or support line sound broken. Include them for casual narration, exclude them for professional VO.
- **Don't fight the content.** A tag must match the line. `[sound happy]` on a somber line pulls the model in two directions and degrades the read. Keep each tag internally consistent. Pairing `[whisper]` with `[very loud]` conflicts.
- **Pronunciation overrides for genuine mispronunciations.** Fish S2.1 Pro supports CMU Arpabet phoneme control between `<|phoneme_start|>` and `<|phoneme_end|>` for homographs, brand names, and jargon, also gated on `settings.normalize: false`. Reserve it for words the model actually gets wrong.
- **For multiple speakers, this is the wrong skill.** See `dialogue-audio`. For a voice that is not a preset (a clone of a specific person or brand voice), see `voice-cloning`.

### Inline tag patterns

- **Emotion and steering tags apply forward.** A `[bracket]` tag placed before text steers everything that follows until the next tag or the end of input. Drop a new tag only where the mood shifts, not on every sentence.
- **Paralanguage drops in place.** Fish uses `(cue)` parentheses (`(break)`, `(breath)`, `(sigh)`) and needs `settings.normalize: false`. Inworld uses inline `[non-verbal]` brackets (`[laugh]`, `[sigh]`, `[breathe]`). Place each where a human would do it.
- **Text-normalization gate.** Inworld `settings.textNormalization: true` expands raw numbers, dates, and prices. Fish `settings.normalize` (default `true`) must be `false` for `(cues)` and `<|phoneme|>` overrides, so it strips them when on.
- Load `references/examples.md` for full worked requests (emotional ad read, normalized explainer, branded IVR).

## Parameters that matter

- `speech.text`: the script, including inline `[bracket]` direction tags and any paralanguage cues. Required.
- `speech.voice`: the voice ID or preset name. Different voices respond to the same direction with different intensity, so pick the voice first, then tune the tags to it.
- `speech.language`: set it where the model exposes it (Qwen, some Inworld locales) for correct phonetics.
- `settings.textNormalization` (Inworld TTS-2): `true` to expand numbers/dates/abbreviations from raw text into spoken form.
- `settings.normalize` (Fish S2.1 Pro): must be `false` for paralanguage `(cues)` and `<|phoneme|>` overrides, otherwise those tokens get stripped.
- `positivePrompt` (Qwen CustomVoice): an optional style/emotion hint, e.g. "Speak with great enthusiasm".
- Confirm exact field names against the live schema (`runware-run`). Bracket-tag and paralanguage syntax differs per model, so never carry one model's cues onto another without checking.

## Quality bar

- The read matches the brief: right emotion, pace, and energy for the use (calm audiobook, upbeat ad, neutral IVR).
- Direction tags carry forward correctly and shift only where the script's mood shifts, not on every sentence (over-tagging produces a jittery, unnatural read).
- Numbers, dates, prices, and abbreviations are spoken cleanly, not read as raw symbols (normalization on, or pre-expanded).
- No tag contradicts its line. Paralanguage and phoneme cues only used with normalization off on Fish. Emphasis is selective.
- Audio was generated async and read from `audioURL`. Retry any line that mispronounces, rushes, or misses the emotion.

## Related skills

`runware-run`, `runware-models`, `runware-prompting`; `dialogue-audio` (multiple speakers in one generation), `voice-cloning` (custom or cloned voice), `talking-avatar` (drive a face with the voiceover), `ugc-ad` (voiceover inside a full ad).
