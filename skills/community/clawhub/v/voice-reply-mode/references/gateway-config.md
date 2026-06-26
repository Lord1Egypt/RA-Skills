# Gateway config

## Core idea

For automatic same-modality behavior, the usual decisive config is:

```json
{
  "messages": {
    "tts": {
      "auto": "inbound",
      "provider": "edge",
      "edge": {
        "enabled": true,
        "voice": "zh-CN-XiaoxiaoNeural",
        "lang": "zh-CN",
        "outputFormat": "audio-24khz-48kbitrate-mono-mp3"
      }
    }
  }
}
```

Meaning:
- inbound voice/audio → auto voice reply
- inbound text → normal text reply

## Important caveats

### 1. Workspace rules are not enough

Updating `SOUL.md` / `IDENTITY.md` alone does not guarantee automatic voice replies.
Gateway-level `messages.tts` is typically what actually enables the behavior.

### 2. Agent identity voice may be schema-limited

Some deployments may reject `identity.voice` in `openclaw.json`.
If schema validation fails, keep preferred voice documented only in workspace files.

### 3. Inbound transcription is separate

If the platform needs voice-note understanding/transcription, also inspect audio understanding / transcription related config in the gateway.

## Safe rollout order

1. Add workspace snippets
2. Enable `messages.tts.auto = "inbound"`
3. Restart / reload gateway
4. Test with one text and one voice message

## Platform-neutral guidance

This pattern is not Telegram-only. It can work anywhere the channel supports:
- receiving voice/audio messages
- sending audio/voice replies
- agent-side or gateway-side TTS routing

Examples include Telegram and Feishu, but actual success depends on the channel plugin capabilities in the user's deployment.
