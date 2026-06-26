---
name: senseaudio-voice-picker
description: Recommend the best SenseAudio voice for any scenario or emotion. Use when users ask which voice to use — e.g. "儿童故事播客用什么音色", "电商直播带货适合哪个声音", "我需要撒娇感的女声", "有没有傲娇的音色". No API key needed for recommendations; optionally generates a TTS preview sample.
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
      description: Only needed for preview audio. Get from https://senseaudio.cn/platform/api-key
      env_var: SENSEAUDIO_API_KEY
---

# SenseAudio Voice Picker

Recommend the right voice for any use case. No API call needed — just match the user's description to the best voice IDs.

## Voice Library

### Free Plan (免费版)

| Name | voice_id | Style |
|------|----------|-------|
| 可爱萌娃 | `child_0001_a` | 开心 |
| 可爱萌娃 | `child_0001_b` | 平稳 |
| 儒雅道长 | `male_0004_a` | 平稳 |
| 沙哑青年 | `male_0018_a` | 深情 |

### Starter Plan (尝鲜版) — VIP

| Name | voice_id | Style |
|------|----------|-------|
| 亢奋主播 | `male_0027_a` | 热情介绍 |
| 亢奋主播 | `male_0027_b` | 卖点解读 |
| 亢奋主播 | `male_0027_c` | 促销逼单 |
| 撒娇青年 | `male_0023_a` | 平稳 |

### Advanced/Pro/Business (高级版+) — SVIP

| Name | voice_id | Style |
|------|----------|-------|
| 嗲嗲台妹 | `female_0033_a` | 平稳 |
| 嗲嗲台妹 | `female_0033_b` | 开心 |
| 嗲嗲台妹 | `female_0033_c` | 撒娇 |
| 嗲嗲台妹 | `female_0033_d` | 低落 |
| 嗲嗲台妹 | `female_0033_e` | 委屈 |
| 嗲嗲台妹 | `female_0033_f` | 生气 |
| 魅力姐姐 | `female_0027_a` | 平稳 |
| 魅力姐姐 | `female_0027_b` | 撒娇 |
| 魅力姐姐 | `female_0027_c` | 病娇 |
| 魅力姐姐 | `female_0027_d` | 低落 |
| 魅力姐姐 | `female_0027_e` | 妩媚 |
| 魅力姐姐 | `female_0027_f` | 傲娇 |
| 气质学姐 | `female_0008_a` | 生气 |
| 气质学姐 | `female_0008_b` | 开心 |
| 气质学姐 | `female_0008_c` | 平稳 |
| 温柔御姐 | `female_0006_a` | 深情 |
| 乐观少年 | `male_0026_a` | 平稳 |
| 乐观少年 | `male_0026_b` | 开心 |
| 乐观少年 | `male_0026_c` | 深情 |
| 孔武青年 | `male_0019_a` | 平稳 |
| 可靠青叔 | `male_0028_a` | 内容剖析 |
| 可靠青叔 | `male_0028_b` | 开场介绍 |
| 可靠青叔 | `male_0028_c` | 广告中插 |
| 可靠青叔 | `male_0028_d` | 轻松铺陈 |
| 可靠青叔 | `male_0028_e` | 细心提问 |
| 可靠青叔 | `male_0028_f` | 主题升华 |
| 知心少女 | `female_0035_a` | 内容剖析 |
| 知心少女 | `female_0035_b` | 开场介绍 |
| 知心少女 | `female_0035_c` | 广告中插 |
| 知心少女 | `female_0035_d` | 轻松铺陈 |
| 知心少女 | `female_0035_e` | 细心提问 |
| 知心少女 | `female_0035_f` | 主题升华 |

## Scenario Matching Guide

Use this to map user descriptions to the right voices:

| Scenario / Keyword | Top picks |
|--------------------|-----------|
| 儿童故事 / 童话 / 儿童教育 | `child_0001_b`, `child_0001_a` |
| 电商直播 / 带货 / 促销 | `male_0027_c`, `male_0027_a` |
| 新闻播报 / 正式 / 专业 | `male_0004_a`, `female_0008_c` |
| 有声书 / 故事叙述 | `male_0018_a`, `female_0006_a` |
| 播客 / 知识分享 | `male_0028_a`, `female_0035_a` |
| 广告 / 营销文案 | `male_0028_c`, `female_0035_c` |
| 轻松日常 / 闲聊 | `male_0026_a`, `male_0028_d` |
| 撒娇 / 可爱嗲 | `female_0033_c`, `female_0027_b` |
| 傲娇 | `female_0027_f` |
| 病娇 | `female_0027_c` |
| 妩媚 / 性感 | `female_0027_e` |
| 开心 / 活泼 | `female_0033_b`, `male_0026_b` |
| 生气 / 愤怒 | `female_0033_f`, `female_0008_a` |
| 深情 / 感人 | `male_0018_a`, `male_0026_c` |
| 低落 / 难过 | `female_0033_d`, `female_0027_d` |
| 委屈 | `female_0033_e` |

## Recommendation Format

Always show 1–3 options. For each:

```
**温柔御姐** — female_0006_a
风格：深情
套餐：高级版+（SVIP）
适合：有声书、情感类内容、温柔叙述场景
```

If the user mentions their plan tier, filter to only show voices they can access.

## Optional: TTS Preview

If the user wants to hear a sample, ask for a preview sentence (or use a default like "你好，欢迎体验 SenseAudio 语音服务。"), then call the TTS API:

```bash
curl -s -X POST https://api.senseaudio.cn/v1/t2a_v2 \
  -H "Authorization: Bearer $SENSEAUDIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"SenseAudio-TTS-1.0\",
    \"text\": \"<PREVIEW_TEXT>\",
    \"stream\": false,
    \"voice_setting\": { \"voice_id\": \"<VOICE_ID>\" },
    \"audio_setting\": { \"format\": \"mp3\" }
  }" -o preview.json

jq -r '.data.audio' preview.json | xxd -r -p > preview_<VOICE_ID>.mp3
```

Generate one file per recommended voice so the user can compare directly.
