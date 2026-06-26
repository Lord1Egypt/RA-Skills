---
name: character-voice-broadcast
description: Turn plain text into character-style TTS scripts for narration, companion-style voice messages, emotional comfort audio, and expressive spoken responses. Use when Codex needs to prepare or call TTS for human-like voice broadcast, role-based narration, emotional companionship, bedtime or greeting voice messages, soothing or encouraging speech, or any task where speech should sound like a specific persona rather than neutral text-to-speech.
---

# Character Voice Broadcast

## Overview

Use this skill to convert plain text into TTS-ready, persona-driven spoken content.
Prioritize natural spoken rhythm, stable persona traits, and emotional control over literal text fidelity.

## Core Use Cases

Apply this skill for requests like:
- "把这段文案做成更像真人的语音播报"
- "给这个角色做一段晚安陪伴语音"
- "把这段台词改成更适合 TTS 朗读的人物化版本"
- "做一个温柔安慰型的语音回复"
- "让这段播报听起来像角色在说，不要像机器念稿"

## Workflow

Follow this order unless the user already specifies some of it.

### 1. Identify the speaking role

Decide who is speaking:
- narrator
- fictional character
- companion-style persona
- news or info host
- comfort / encouragement voice
- greeting / wake-up / bedtime voice

If the user names a persona, keep that identity stable through the whole output.
If the user does not provide a persona, infer one from the task and state it clearly in the output.

### 2. Choose the target speaking effect

Select one primary effect:
- `播报型`: clear, structured, easy to follow
- `陪伴型`: warm, soft, intimate, less formal
- `角色型`: strong personality markers and stylized wording
- `安慰型`: gentle, slower, emotionally safe
- `激励型`: energetic, uplifting, rhythmic

Do not mix conflicting effects unless the user explicitly asks for it.

### 3. Rewrite the text for speech, not for reading

Transform the source text into spoken language:
- shorten overly long sentences
- remove written-only phrasing
- add natural pauses
- add light fillers only when they improve realism
- make emotional turns audible, not just semantic
- keep key facts intact if the text contains information the user needs

TTS scripts should sound like someone speaking to a listener, not like a document being read aloud.

### 4. Produce two layers of output

When helpful, output both:
- `口播文本`: the final text to send to TTS
- `语音控制说明`: style notes for the TTS backend, such as tone, pace, pause density, warmth, smile, tenderness, or firmness

If the user asks for direct TTS calling instructions, also output backend-facing hints in short bullet form.

### 4.1 Call SenseAudio TTS when audio output is needed

If the task is not just script writing but actual audio generation, call the bundled script:

```bash
python3 scripts/senseaudio_tts.py \
  --text "你好，欢迎体验 SenseAudio 带来的极致语音服务。" \
  --voice-id male_0004_a \
  --output output.wav
```

Authentication:
- read API key from `SENSEAUDIO_API_KEY`
- or pass `--api-key`

Default endpoint and model:
- endpoint: `https://api.senseaudio.cn/v1/t2a_v2`
- model: `SenseAudio-TTS-1.0`

Use `--text-file` when the spoken script is long or already saved as a file.
Prefer generating the spoken script first, then sending that cleaned script to TTS instead of sending raw written prose.

### 5. Match emotion to context

Use emotion deliberately:
- comfort: lower intensity, slower pacing, gentle reassurance
- companion chat: natural rhythm, light intimacy, occasional casual phrasing
- dramatic character: more contrast, more stylized keywords, sharper scene cues
- narration: stable clarity, less filler, clean structure
- bedtime: soft cadence, low stimulation, short phrases

Avoid exaggerated emotional markers that would make TTS sound unnatural or theatrical unless explicitly requested.

## Output Rules

Default to Chinese output unless the user requests another language.

Prefer short spoken units over long written paragraphs.
Preserve concrete facts, names, numbers, and instructions unless the user asks for a looser adaptation.

If the task is informational broadcast, keep it understandable first and expressive second.
If the task is emotional companionship, keep it emotionally coherent first and factually safe second.

When preparing a TTS-friendly script:
- replace stiff书面语 with口语
- break dense exposition into 1-3 sentence chunks
- mark meaningful pauses with punctuation, not stage directions
- avoid overusing ellipses or repeated interjections

## Standard Deliverables

Produce the smallest useful set:
- final spoken script for TTS
- persona summary
- TTS style control notes
- optional alternate versions if the user asks for multiple moods
- optional SenseAudio invocation command or generated audio file path

## Default Chinese Templates

Use the templates in [voice-broadcast-templates.md](references/voice-broadcast-templates.md) when the user does not specify a format.

## Resources

- [voice-broadcast-templates.md](references/voice-broadcast-templates.md): Chinese output templates
- [senseaudio-api.md](references/senseaudio-api.md): SenseAudio API usage notes
- [senseaudio_tts.py](scripts/senseaudio_tts.py): local wrapper for generating audio with SenseAudio

## Trigger Examples

Use this skill for requests like:
- "把这段介绍文案改成像真人角色播报"
- "做一段安慰人的陪伴语音文案"
- "把这段台词整理成适合 TTS 的角色对白"
- "给我一版温柔女生口播和一版冷静男声口播"
- "为这个角色准备晨间问候和晚安语音"
