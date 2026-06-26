---
name: qwen-audio-lab
description: Hybrid text-to-speech, reusable voice cloning, and narrated audio generation for macOS plus Aliyun Qwen. Use when the user wants to convert text into speech, clone and reuse a voice from a reference recording, generate narration files from plain text or text files, or create PPT speaker-note voiceovers.
---

# Qwen Audio Lab

Use this skill for text-to-speech on macOS or with Aliyun Qwen.

## Choose the backend

- Use `mac-say` for fast local playback, notifications, and low-friction speech on a Mac.
- Use `qwen-tts` when the user wants better naturalness, reusable output files, custom voices, or voice cloning.
- If `DASHSCOPE_API_KEY` is missing, fall back to `mac-say` for local playback.

## Environment

- `DASHSCOPE_API_KEY`: required for Qwen synthesis and voice cloning.
- `QWEN_AUDIO_REGION`: optional, `cn` (default) or `intl`.
- `QWEN_AUDIO_OUTPUT_DIR`: optional directory for generated audio files. Defaults to `~/.openclaw/data/qwen-audio-lab/output`.
- `QWEN_AUDIO_STATE_DIR`: optional directory for local state such as remembered voices. Defaults to `~/.openclaw/data/qwen-audio-lab/state`.

## Commands

Run all commands through:

```bash
python3 ~/.openclaw/skills/qwen-audio-lab/scripts/qwen_audio.py <command> [...]
```


## Preferred high-level commands

Use these first for most user-facing narration tasks:

```bash
python3 ~/.openclaw/skills/qwen-audio-lab/scripts/qwen_audio.py narrate-text --text "这是要转成语音的正文"
python3 ~/.openclaw/skills/qwen-audio-lab/scripts/qwen_audio.py narrate-file --text-file /path/to/script.txt
python3 ~/.openclaw/skills/qwen-audio-lab/scripts/qwen_audio.py narrate-ppt --ppt /path/to/file.pptx
```

Use the older commands only when you specifically want the legacy workflow names.
Generated audio and remembered voice state now default to `~/.openclaw/data/qwen-audio-lab/` instead of the skill folder.

### Local macOS speech

```bash
python3 ~/.openclaw/skills/qwen-audio-lab/scripts/qwen_audio.py mac-say \
  --text "开会了，别忘了带电脑" \
  --voice Tingting
```

### Qwen TTS from inline text

```bash
python3 ~/.openclaw/skills/qwen-audio-lab/scripts/qwen_audio.py qwen-tts \
  --text "你好，我是你的语音助手。" \
  --voice Cherry \
  --model qwen3-tts-flash \
  --language-type Chinese \
  --download
```

### Qwen TTS from a text file

```bash
python3 ~/.openclaw/skills/qwen-audio-lab/scripts/qwen_audio.py qwen-tts \
  --text-file /path/to/script.txt \
  --voice Cherry \
  --download
```

### Qwen TTS from stdin

```bash
cat /path/to/script.txt | python3 ~/.openclaw/skills/qwen-audio-lab/scripts/qwen_audio.py qwen-tts \
  --stdin \
  --voice Cherry \
  --download
```

### Clone a voice

```bash
python3 ~/.openclaw/skills/qwen-audio-lab/scripts/qwen_audio.py clone-voice \
  --audio /path/to/reference.mp3 \
  --name claw-voice-01 \
  --target-model qwen3-tts-vc-2026-01-22
```

- Keep the cloning `target-model` aligned with the synthesis model family.
- Use a clean speech sample with minimal background noise.
- Ask before cloning a third party voice when consent is unclear.

### Design a voice from a text prompt

```bash
python3 ~/.openclaw/skills/qwen-audio-lab/scripts/qwen_audio.py design-voice \
  --prompt "沉稳的中年男性播音员，音色低沉浑厚，适合纪录片旁白。" \
  --name doc-voice-01 \
  --target-model qwen3-tts-vd-2026-01-26 \
  --preview-format wav
```

### Legacy command: reuse the latest cloned voice

```bash
python3 ~/.openclaw/skills/qwen-audio-lab/scripts/qwen_audio.py speak-last-cloned \
  --text "你好，这是我的声音测试。" \
  --download
```

### High-level narration from any text source

```bash
python3 ~/.openclaw/skills/qwen-audio-lab/scripts/qwen_audio.py narrate-text \
  --text "这是要转成语音的正文" \
  --output narration.wav

python3 ~/.openclaw/skills/qwen-audio-lab/scripts/qwen_audio.py narrate-file \
  --text-file /path/to/script.txt
```

- Default voice source is `last-cloned`.
- Use `--voice-source last-designed` to use the latest designed voice instead.
- Use `--voice` and optionally `--model` to force a specific voice id and synthesis model.

### Legacy command: narrate PPT speaker notes with the latest cloned voice

```bash
python3 ~/.openclaw/skills/qwen-audio-lab/scripts/qwen_audio.py ppt-own-voice   --ppt "/path/to/file.pptx"
```

### High-level PPT narration

```bash
python3 ~/.openclaw/skills/qwen-audio-lab/scripts/qwen_audio.py narrate-ppt   --ppt "/path/to/file.pptx"
```

- Default voice source is `last-cloned`.
- Use `--voice-source last-designed` to switch to the latest designed voice.
- Use `--voice` and optionally `--model` to force a specific voice id and synthesis model.
- Keep `ppt-own-voice` as the backward-compatible alias for the original workflow.

### Inspect or manage remembered voices

```bash
python3 ~/.openclaw/skills/qwen-audio-lab/scripts/qwen_audio.py list-voices
python3 ~/.openclaw/skills/qwen-audio-lab/scripts/qwen_audio.py show-last-voice --kind cloned
python3 ~/.openclaw/skills/qwen-audio-lab/scripts/qwen_audio.py delete-voice --voice claw-voice-01
```

## Workflow rules

- Reuse an existing cloned voice before asking for a new sample.
- Ask for a reference recording if the user wants their own voice and no cloned voice exists yet.
- Prefer the `narrate-*` commands as the primary high-level interface for narration tasks.
- Keep `speak-last-cloned` and `ppt-own-voice` for backward compatibility with older workflows.
- Keep only final outputs by default after segmented synthesis unless the user explicitly asks to keep fragments.
