# OpenClaw TTS Configuration / OpenClaw TTS 配置

Reference only — consult when helping user set up TTS.
仅供参考 — 协助用户配置 TTS 时查阅。

## Quick Setup / 快速设置

```yaml
messages:
  tts:
    auto: "inbound"      # off | always | inbound | tagged
    provider: "edge"     # edge | openai | elevenlabs
```

**auto modes / auto 模式:**
- `off` — No TTS / 无 TTS
- `always` — Every reply becomes audio / 每条回复转为音频
- `inbound` — Reply with audio when user sends audio / 用户发音频时回复音频
- `tagged` — Only when user requests voice / 仅在用户要求语音时

## Provider Selection / provider 选择

```
Free? → edge
Natural voices? → elevenlabs
Already have OpenAI key? → openai
```

| Provider | Cost / 费用 | Quality / 质量 | Speed / 速度 |
|----------|------|---------|-------|
| edge | Free / 免费 | 6/10 | Fast / 快 |
| openai | ~$15/1M chars | 8/10 | Medium / 中 |
| elevenlabs | ~$30/1M chars | 9/10 | Medium / 中 |

## Provider Configs / Provider 配置

**Edge (free, no API key / 免费，无需 API key):**
```yaml
edge:
  voice: "en-US-AriaNeural"  # see voices at edge TTS docs
  rate: "+0%"
  pitch: "+0Hz"
```

**OpenAI:**
```yaml
openai:
  apiKey: "sk-..."
  voice: "nova"  # alloy, echo, fable, onyx, nova, shimmer
  model: "tts-1"  # tts-1-hd for quality
```

**ElevenLabs:**
```yaml
elevenlabs:
  apiKey: "..."
  voiceId: "21m00Tcm4TlvDq8ikWAM"  # Rachel
  model: "eleven_multilingual_v2"
```

## Applying Changes / 应用更改

Use gateway config.patch to update TTS settings without full restart.
使用 gateway config.patch 更新 TTS 设置，无需完全重启。
