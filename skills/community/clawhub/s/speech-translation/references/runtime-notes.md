# Runtime Notes

## Bundled implementation

The bundled Python app exposes this flow:

1. `transcribe.py`
   - `faster-whisper`: real ASR
   - `mock`: read plain text from the input file
2. `translate.py`
   - `llm`: consume a translation that the surrounding agent/model already wrote to `--translation-file`
   - `manual`: same-language passthrough, translation file, or terminal paste
   - `service`: POST JSON to an HTTP translation service
3. `tts.py`
   - `piper`: real local synthesis
   - `mock`: create a short silent wav
4. `pipeline.py`
   - write outputs and optionally send stage notifications

## Translation default

The default backend is now `llm`.

Important: `llm` does not mean the Python script can directly call the live OpenClaw model runtime. Instead, it means the agent using this skill should:

1. obtain the transcript
2. translate it with the current model
3. write that translation to a file
4. pass the file via `--translation-file`

This keeps the skill deterministic while still making the model the default translation engine.

## Dependencies

Typical real run dependencies:

- Python 3.10+
- `faster-whisper`
- `requests`
- `piper` binary available on PATH, or pass `--piper-binary`
- a Piper `.onnx` voice model and matching `.onnx.json`

Install Python deps with:

```bash
pip install faster-whisper requests
```

On macOS, Piper is commonly installed with:

```bash
brew install piper
```

## Translation service contract

Request:

```json
{
  "text": "...",
  "source_lang": "zh",
  "target_lang": "en"
}
```

Response:

```json
{
  "translation": "..."
}
```

## Output contract

The pipeline writes:

- `01_transcript.txt`
- `02_translation.txt`
- `03_translation.wav`
- `result.json`

## Notification hooks

Use these only when external stage reporting is useful.

- `--transcript-command`: command reads transcript text from stdin
- `--translation-command`: command reads translated text from stdin
- `--audio-command`: command receives the audio path; supports `{audio_file}` placeholder

Helpers:

- `scripts/send_text.py`
- `scripts/send_audio.py`
- `scripts/mock_text_sender.py`
- `scripts/mock_audio_sender.py`

## Current limitations

- Real translation is only automatic when the surrounding agent supplies `--translation-file`, or when an external HTTP service is used.
- CLI currently requires `--piper-model` even when `--tts-backend mock`.
- Input is a file path, not a direct OpenClaw media attachment abstraction.
- No diarization, subtitle timing export, or chunked long-audio orchestration yet.
