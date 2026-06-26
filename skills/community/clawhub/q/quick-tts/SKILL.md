---
name: senseaudio-tts-quick
description: Zero-config text-to-speech — give text, get an mp3 file. Handles natural-language voice selection ("用女声", "撒娇语气", "生气一点") and auto-inserts pacing breaks for long text. Use this whenever a user wants to quickly synthesize speech without configuring API details, or says things like "帮我把这段话合成语音", "用温柔御姐的声音读一下", "生成一段生气语气的音频".
metadata:
  openclaw:
    requires:
      env:
        - SENSEAUDIO_API_KEY
      bins:
        - curl
        - jq
        - xxd
    primaryEnv: SENSEAUDIO_API_KEY
    homepage: https://senseaudio.cn
compatibility:
  required_credentials:
    - name: SENSEAUDIO_API_KEY
      description: API key from https://senseaudio.cn/platform/api-key
      env_var: SENSEAUDIO_API_KEY
---

# SenseAudio TTS Quick

Zero-config speech synthesis. User gives text, you produce an mp3 file — no API knowledge required.

## Voice Selection

Default voice: `male_0004_a` (儒雅道长, neutral).

Map natural-language requests to voice IDs before calling the API:

| User says | voice_id |
|-----------|----------|
| 女声 / 女生 / 女的 | `female_0006_a` (温柔御姐) |
| 温柔御姐 | `female_0006_a` |
| 嗲嗲 / 台妹 | `female_0033_a` |
| 撒娇 | `female_0033_c` |
| 低落 / 难过 / 悲伤 | `female_0033_d` |
| 委屈 | `female_0033_e` |
| 生气 / 愤怒 | `female_0033_f` |
| 开心 / 高兴 / 活泼 | `female_0033_b` |
| 傲娇 | `female_0027_f` |
| 病娇 | `female_0027_c` |
| 妩媚 / 性感 | `female_0027_e` |
| 男声 / 男生 | `male_0004_a` |
| 沙哑 / 深情 | `male_0018_a` |
| 撒娇青年 | `male_0023_a` |
| 乐观 / 少年 | `male_0026_a` |
| 儿童 / 小孩 / 萌娃 | `child_0001_b` |

If the user names a voice not in this table, use `male_0004_a` and note the fallback.

## Long Text Pacing

For text longer than 100 characters, insert `<break time="300"/>` after each `。` `！` `？` to improve natural rhythm:

```
原文：今天天气很好。我们出去走走吧。
处理后：今天天气很好。<break time="300"/>我们出去走走吧。<break time="300"/>
```

Do not insert breaks inside quoted speech or after mid-sentence punctuation like `，`.

## API Call

```bash
curl -s -X POST https://api.senseaudio.cn/v1/t2a_v2 \
  -H "Authorization: Bearer $SENSEAUDIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "SenseAudio-TTS-1.0",
    "text": "<TEXT>",
    "stream": false,
    "voice_setting": {
      "voice_id": "<VOICE_ID>"
    },
    "audio_setting": {
      "format": "mp3"
    }
  }' -o response.json

# Decode hex audio to mp3
jq -r '.data.audio' response.json | xxd -r -p > output.mp3
```

Check `base_resp.status_code == 0` before decoding. On error, show `base_resp.status_msg`.

## Output

After generating the file:
1. Save as a descriptive filename, e.g. `speech_<timestamp>.mp3` or based on the first few words of the text.
2. Report:
   - File path
   - Audio duration: `jq '.extra_info.audio_length' response.json` (ms → seconds)
   - Character count: `jq '.extra_info.usage_characters' response.json`
   - Voice used

Example output:
```
生成完成：speech_20240315.mp3
音色：温柔御姐 (female_0006_a)
时长：4.2 秒
字数：38 字
```

## Error Handling

| status_code | Likely cause | Action |
|-------------|--------------|--------|
| 401 | Invalid API key | Ask user to check SENSEAUDIO_API_KEY |
| 400 | Text too long (>10000 chars) | Split text and generate multiple files |
| 429 | Rate limit | Wait a moment and retry once |
