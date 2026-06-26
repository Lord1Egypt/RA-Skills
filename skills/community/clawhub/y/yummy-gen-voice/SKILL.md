---
name: yummy-gen-voice
version: 1.0.0
description: "Use when the user wants to synthesise speech or text-to-speech (TTS) audio with Gemini through yummycli, including single-speaker narration, multi-speaker dialogue (up to 2 speakers), and listing available voices."
metadata:
  requires:
    bins: ["yummycli"]
    skills: ["yummy-shared"]
  openclaw:
    requires:
      bins: ["yummycli"]
    primaryEnv: GEMINI_API_KEY
    related_skills: ["yummy-shared"]
  hermes:
    tags: [audio, tts, speech, gemini, text-to-speech, voice, dialogue]
    related_skills: ["yummy-shared"]
    requires_toolsets: ["yummycli"]
install:
  - kind: node
    package: "@yummysource/yummycli"
    bins: ["yummycli"]
---

# Synthesise Speech

Generate spoken audio with `yummycli gemini speak` using Google Gemini TTS.

## When to Use

Load this skill when the user asks to synthesise speech, convert text to audio, generate a voiceover, create a narration, or produce a spoken dialogue — including single-speaker TTS and multi-speaker conversation.

> **Prerequisite:** Apply the `yummy-shared` skill first.

This skill covers three modes with a single command:

- Single-speaker narration (one voice, any language)
- Multi-speaker dialogue (up to 2 speakers, each with their own voice)
- Listing available prebuilt voices

## Command Contract

Two equivalent entry points are available:

| Entry point | When to use |
|-------------|-------------|
| `yummycli gemini speak` | Default — human-friendly, Gemini TTS presets applied |
| `yummycli audio speak --provider gemini` | Scripting / automation — explicit, provider-agnostic form |

Both share the same flags and defaults. Prefer `gemini speak` unless the task explicitly requires the provider-agnostic form.

Basic usage:

```bash
yummycli gemini speak --text "<text>"
```

With an explicit voice and output path:

```bash
yummycli gemini speak \
  --text "<text>" \
  --voice Kore \
  --output narration.wav
```

Optional controls:

```bash
--output <file.wav>
--model <model>
--voice <voice-name>
--language <bcp47-code>
```

Default values when omitted: `--model gemini-3.1-flash-tts-preview`, `--voice Aoede`.

## Speaker Routing Rules

The presence of `--speaker` flags determines the synthesis path automatically:

| Input | Behaviour |
|-------|-----------|
| No `--speaker` | Single-speaker synthesis. `--voice` selects the prebuilt voice. |
| 1–2 `--speaker` flags | Multi-speaker dialogue. Each flag maps a speaker name to a voice. `--voice` must not be used together. |

`--voice` and `--speaker` are mutually exclusive. Never pass both.

## Model Selection

Default model: `gemini-3.1-flash-tts-preview`.

| User says | Use |
|-----------|-----|
| `3.1`, `3.1 flash`, or no preference | `gemini-3.1-flash-tts-preview` (default) |
| `2.5 flash` or `flash 2.5` | `gemini-2.5-flash-preview-tts` |
| `2.5 pro` or `pro 2.5` | `gemini-2.5-pro-preview-tts` |

Do not switch models from vague quality words alone.

## Available Voices

30 prebuilt voices are available. Run `yummycli gemini voices` to list them all.

| Voice | Style |
|-------|-------|
| Aoede | Breezy |
| Kore | Firm |
| Charon | Informative |
| Puck | Upbeat |
| Fenrir | Excitable |
| Zephyr | Bright |
| Leda | Youthful |
| Orus | Firm |
| Callirrhoe | Easy-going |
| Autonoe | Bright |
| Enceladus | Breathy |
| Iapetus | Clear |
| Umbriel | Easy-going |
| Algieba | Smooth |
| Despina | Smooth |
| Erinome | Clear |
| Algenib | Gravelly |
| Rasalghul | Informative |
| Achird | Friendly |
| Zubenelgenubi | Casual |
| Vindemiatrix | Gentle |
| Sadachbia | Lively |
| Sadaltager | Knowledgeable |
| Sulafat | Warm |
| Schedar | Even |
| Gacrux | Mature |
| Pulcherrima | Forward |
| Laomedeia | Upbeat |
| Achernar | Soft |
| Alnilam | Firm |

When the user does not specify a voice, use the default (`Aoede`). Only apply a different voice when the user explicitly names one or describes a style that clearly maps to a specific voice.

## Language

- Language is auto-detected from the input text when `--language` is omitted.
- Pass `--language` only when the user explicitly specifies a language or when the text could be ambiguous (e.g. romanised transliteration).
- Use BCP-47 codes: `en-US`, `zh-CN`, `ja-JP`, `ko-KR`, `fr-FR`, etc.

## Intent to Parameters

**Voice guidance:**
- For neutral or general-purpose narration, use the default `Aoede` (Breezy).
- For formal or instructional content, consider `Charon` (Informative) or `Kore` (Firm).
- For energetic or promotional content, consider `Puck` (Upbeat) or `Fenrir` (Excitable).
- For warm conversational content, consider `Sulafat` (Warm) or `Achird` (Friendly).
- Only switch from the default when the user's intent clearly maps to a specific style.

**Output path guidance:**
- If `--output` is omitted, `yummycli` generates a timestamped `.wav` filename in the current working directory. Do not invent your own filename unless the user provides one.
- The output path must end in `.wav`. Reject or correct any other extension.

**Multi-speaker prompt format:**
- Each speaker's lines must be tagged with their name in square brackets: `[Alice]: Hello! [Bob]: Hi there!`
- Speaker names in `--speaker` flags must exactly match the names used in `--text`.

## Output Contract

Speak commands return JSON on stdout. Read the response and use the `output` field as the generated file path.

Single-speaker example:

```json
{
  "provider": "gemini",
  "output": "tts_20260420_142301_047.wav",
  "model": "gemini-3.1-flash-tts-preview",
  "voice": "Aoede",
  "elapsed_seconds": 3
}
```

Multi-speaker example:

```json
{
  "provider": "gemini",
  "output": "dialogue_20260420_143010_112.wav",
  "model": "gemini-3.1-flash-tts-preview",
  "speakers": [
    {"name": "Alice", "voice": "Aoede"},
    {"name": "Bob", "voice": "Kore"}
  ],
  "elapsed_seconds": 4
}
```

## Execution Rules

- Check `yummycli auth status --provider gemini` before running if credentials may not be configured.
- Never pass `--voice` and `--speaker` together.
- Never pass more than 2 `--speaker` flags — the API rejects it.
- Speaker names in `--speaker` flags must match the names used in the `--text` prompt exactly.
- If the command returns a validation error, fix the arguments before retrying. Do not retry with the same invalid arguments.
- Report the final `output` path back to the user after a successful run.

## Examples

Single-speaker narration:

```bash
yummycli gemini speak \
  --text "A golden retriever is the best dog in the world."
```

Narration with an explicit voice:

```bash
yummycli gemini speak \
  --text "Welcome to the future of AI-powered audio." \
  --voice Puck \
  --output welcome.wav
```

Chinese narration (auto-detected language):

```bash
yummycli gemini speak \
  --text "你好，欢迎使用 Gemini 语音合成服务。" \
  --voice Aoede \
  --output greeting.wav
```

Multi-speaker dialogue:

```bash
yummycli gemini speak \
  --text "[Alice]: 你好！今天天气真好。 [Bob]: 是啊，我们去散步吧！" \
  --speaker Alice:Aoede \
  --speaker Bob:Kore \
  --output dialogue.wav
```

List all available voices:

```bash
yummycli gemini voices
```
