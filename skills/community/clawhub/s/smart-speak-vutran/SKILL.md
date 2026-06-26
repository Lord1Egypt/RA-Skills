---
name: smart-speak
description: Multilingual Text-to-Speech (TTS) with intelligent Pinyin-to-Hanzi conversion. Use when the user asks to generate audio for text that contains a mix of Vietnamese, Chinese (Pinyin), or English. This skill ensures correct pronunciation by converting Pinyin to Hanzi and using native-quality voices for each segment.
---

# Smart-Speak: Multilingual TTS

This skill provides a high-quality, multilingual text-to-speech workflow that handles Vietnamese, Chinese (including Pinyin), and English seamlessly.

## Core Features

1.  **Intelligent Pinyin Conversion:** Automatically converts Pinyin to Chinese characters (Hanzi) for more natural and accurate pronunciation by the Chinese TTS engine.
2.  **Language Segmentation:** Splits text into language-specific blocks to use specialized voices.
3.  **Native-Quality Voices:**
    *   🇻🇳 Vietnamese: `vi-VN-HoaiMyNeural` (Hoài Mỹ)
    *   🇨🇳 Chinese/Pinyin: `zh-CN-XiaoxiaoNeural` (Xiaoxiao)
    *   🇺🇸 English: `en-US-AvaNeural` (Ava)
4.  **Audio Merging:** Combines all generated segments into a single, high-quality MP3 file using `ffmpeg`.

## Workflow

### 1. Analyze & Pre-process

Before generating audio, the agent must:
- **Detect Pinyin:** Identify Pinyin within Vietnamese text. A word is likely Pinyin if it doesn't make sense in the Vietnamese context (e.g., *Nǐ hǎo*, *mā*, *shēn tǐ*).
- **Convert to Hanzi:** Replace all detected Pinyin with the equivalent Chinese characters (e.g., *Nǐ hǎo ma?* -> `你好吗？`). This ensures the `zh-CN-XiaoxiaoNeural` voice reads it with perfect tones.
- **Remove Emojis:** Strip out all emojis from the text to prevent the TTS engine from reading them as descriptions.
- **Handle Punctuation:** Ensure each segment ends with appropriate punctuation (commas, periods) to maintain natural pauses.

### 2. Segment the Text

Divide the processed text into blocks and assign the appropriate voice.

**Example Input:**
"Chào anh Vũ, 你好吗？ (Nǐ hǎo ma?) là câu chào."

**Example Segments:**
1. `{"text": "Chào anh Vũ, ", "voice": "vi-VN-HoaiMyNeural"}`
2. `{"text": "你好吗？", "voice": "zh-CN-XiaoxiaoNeural"}`
3. `{"text": " ( ", "voice": "vi-VN-HoaiMyNeural"}`
4. `{"text": "你好吗？", "voice": "zh-CN-XiaoxiaoNeural"}`
5. `{"text": " ) là câu chào.", "voice": "vi-VN-HoaiMyNeural"}`

### 3. Execute the Synthesis

Use the bundled Python script to generate and merge the audio.

```bash
python3 skills/public/smart-speak/scripts/smart_speak.py \
  --segments-json '[{"text": "Chào anh Vũ, ", "voice": "vi-VN-HoaiMyNeural"}, ...]' \
  --output /home/jackie_chen_phong/.openclaw/workspace/output_name.mp3
```

### 4. Deliver the Audio

Send the resulting MP3 file to the user using the `message` tool (`action=send`, `filePath`).

## Constraints

- **Absolute Paths:** Always use the absolute path for the output file within the workspace: `/home/jackie_chen_phong/.openclaw/workspace/`.
- **JSON Encoding:** Ensure the `--segments-json` string is properly escaped when passed to the shell.
- **TTS Location:** The script assumes `edge-tts` is located at `/home/jackie_chen_phong/.local/bin/edge-tts`.
