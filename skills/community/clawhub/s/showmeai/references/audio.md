# Speech and music

Read this reference for `tts` or `music`. Routing, Key, and polling rules remain in `SKILL.md`.

## Text to speech

The local catalog includes OpenAI-compatible TTS, Gemini preview TTS, and Qwen TTS identifiers. Actual visibility depends on the current token group.

```bash
python3 scripts/showmeai.py tts --text "A calm narration" --model tts-1 --voice alloy --response-format mp3 --speed 1
```

Common `tts-1` voices are alloy, echo, fable, onyx, nova, and shimmer. Supported output containers include mp3, opus, aac, flac, wav, and pcm. Model-specific voice support differs; use the setup model list and catalog parameters rather than assuming all voices work everywhere.

## Music

Suno-style music supports inspiration, custom, and continuation modes.

```bash
python3 scripts/showmeai.py music --mode inspiration --description "Optimistic acoustic folk" --instrumental
python3 scripts/showmeai.py music --mode custom --lyrics "..." --title "Morning" --tags "folk, warm"
```

The runtime submits to `/suno/submit/music`, polls `/suno/fetch/{task_id}` until `SUCCESS` or failure, and downloads every returned `audio_url`.
