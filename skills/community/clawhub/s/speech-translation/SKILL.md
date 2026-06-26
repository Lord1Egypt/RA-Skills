---
name: speech-translation
description: Build, adapt, or run an audio-processing workflow that takes spoken audio, transcribes it with Whisper or faster-whisper, translates the transcript using the current agent model by default, and synthesizes translated speech with Piper, the OpenClaw tts tool, or a mock backend. Use when the user wants 语音转写、翻译、译文语音合成, wants an existing voice translation prototype operationalized, or wants a chat-native flow where sending a voice message automatically yields transcript text, translation text, and translated audio.
---

# Voice Translate

Use this skill for two closely related modes:

1. **Chat-native mode**: the user sends audio or a voice note in OpenClaw; return transcript text, translation text, and translated audio.
2. **Local pipeline mode**: run a deterministic file-based pipeline that writes transcript, translation, wav, and metadata artifacts.

Default to an LLM-assisted translation workflow: let the current agent produce the translation, save it to a file when using the local pipeline, or use the surrounding agent turn directly when responding in chat.

## Workflow

### A. Chat-native mode

Use this when an inbound message already contains an audio transcript from OpenClaw media understanding, or when the user asks you to process a voice message conversationally.

1. Detect that the user sent audio or that the request is for voice translation.
2. Obtain or confirm the transcript text.
3. Translate with the current model.
4. Send the transcript text to the user.
5. Send the translated text to the user.
6. Synthesize the translated text as audio:
   - prefer the OpenClaw `tts` tool when you need an immediate chat reply with audio
   - prefer Piper when you need a local wav artifact
7. Keep the output order stable: transcript first, translation second, audio last.

### B. Local pipeline mode

1. Confirm input/output expectations: source language, target language, output directory, and whether the run should be real or mock.
2. Choose backends:
   - `faster-whisper` for real transcription, `mock` for pipeline testing.
   - `llm` as the default translation path when an agent/model is available.
   - `service` only when unattended HTTP translation is preferable.
   - `manual` only as a fallback.
   - `piper` for real TTS, `mock` for dry-run testing.
3. Run transcription.
4. If using the default `llm` path, read the transcript and translate it with the current model. Save the translated text to a file.
5. Run synthesis/output writing with `--translation-file`.
6. Inspect outputs:
   - `01_transcript.txt`
   - `02_translation.txt`
   - `03_translation.wav`
   - `result.json`
7. If the user wants chat updates during processing, pass notifier commands with `--transcript-command`, `--translation-command`, and `--audio-command`.

## Preferred execution patterns

### Default LLM-assisted path

Use this when the agent handling the task can translate the transcript itself.

1. Run the pipeline once transcription is available, or run the full command after preparing `translation.txt`.
2. Save the model-produced translation to a file.
3. Invoke:

```bash
bash scripts/run_voice_translate_llm.sh \
  /path/to/input.m4a \
  ./outputs/llm-run \
  zh \
  en \
  /path/to/en_US-lessac-medium.onnx \
  ./translation.txt \
  --whisper-model small \
  --transcribe-backend faster-whisper \
  --tts-backend piper
```

Read `references/llm-translation-pattern.md` when you need the exact orchestration pattern or a reusable translation prompt.

### Mock end-to-end validation

Use this first when you need to validate the pipeline structure without model/runtime dependencies.

```bash
python3 scripts/run_voice_translate.py \
  --input references/examples/mock-input.txt \
  --output-dir ./outputs/mock-run \
  --source-lang zh \
  --target-lang en \
  --transcribe-backend mock \
  --translation-file ./translated.txt \
  --translation-backend llm \
  --no-interactive-translate \
  --tts-backend mock \
  --piper-model ./dummy.onnx
```

Notes:
- `mock` transcription reads plain text from the input file.
- `mock` TTS writes a silent wav file.
- `--piper-model` is still required by the current CLI shape even when using mock TTS; use any placeholder path.
- `llm` mode currently means the translation must already exist in `--translation-file`.

### Service fallback

```bash
python3 scripts/run_voice_translate.py \
  --input /path/to/input.m4a \
  --output-dir ./outputs/service-run \
  --source-lang zh \
  --target-lang en \
  --whisper-model small \
  --transcribe-backend faster-whisper \
  --translation-backend service \
  --translation-service-url http://127.0.0.1:8000/translate \
  --tts-backend piper \
  --piper-model /path/to/en_US-lessac-medium.onnx
```

## Resources

### scripts/

- `run_voice_translate.py`: primary entrypoint.
- `run_voice_translate_llm.sh`: thin wrapper for the default LLM-assisted path.
- `voice_translate_app/`: pipeline modules.
- `send_text.py`: wrap stage text and forward it via a shell command.
- `send_audio.py`: forward generated audio via a shell command.
- `mock_text_sender.py`, `mock_audio_sender.py`: local smoke-test helpers.

### references/

- Read `references/runtime-notes.md` for dependency/setup details, backend behavior, and integration constraints.
- Read `references/llm-translation-pattern.md` when the surrounding agent should perform translation with its own model.
- Read `references/openclaw-chat-mode.md` when implementing or following the conversational flow: receive voice, output transcript text, output translation text, then output translated audio.

## Editing guidance

- Keep `SKILL.md` procedural and short.
- Put environment- or backend-specific detail in references.
- Treat `llm` as the preferred translation path for agent-driven workflows.
- In chat-native mode, preserve the user-visible ordering: transcript text, translation text, then audio.
- Prefer OpenClaw `tts` for immediate conversational audio replies; prefer Piper for local wav artifacts and offline pipelines.
- If the user wants tighter OpenClaw integration, add an attachment-aware outer workflow or hook instead of rewriting ASR/TTS first.
- Preserve the current file contract unless the user asks to change it: transcript, translation, wav, metadata JSON.
