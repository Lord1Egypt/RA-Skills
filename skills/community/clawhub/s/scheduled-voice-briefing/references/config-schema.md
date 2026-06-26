# Config Schema / 配置结构建议

Suggested config location:
- `config/scheduled-voice-briefing.json`

## Runtime contract / 运行时约定

Recommended runtime fields:
- `provider`: runtime-provided voice backend name
- `voice`: abstract voice choice or runtime-specific voice name
- `rate`: speaking speed
- `volume`: playback volume
- `tone`: style hint such as calm / energetic / gentle
- `contextText`: richer style prompt for the runtime voice layer
- `fallback`: fallback playback strategy if the preferred provider is unavailable
- `playbackMode`: batch / staged / streaming

建议的运行时字段：
- `provider`：运行环境提供的语音后端名称
- `voice`：抽象 voice 选择或运行时特定 voice 名称
- `rate`：语速
- `volume`：播放音量
- `tone`：风格提示，例如 calm / energetic / gentle
- `contextText`：提供给语音层的更详细风格提示
- `fallback`：首选 provider 不可用时的降级策略
- `playbackMode`：batch / staged / streaming

## Example A — Scheduled weekday briefing / 示例 A：工作日定时播报

```json
{
  "enabled": true,
  "timezone": "UTC",
  "speaker": {
    "language": "zh",
    "voiceType": "female",
    "tone": "gentle",
    "runtime": {
      "provider": "runtime-local-voice",
      "voice": "default-female",
      "rate": 180,
      "volume": 1.0,
      "contextText": "温和、清晰、适合定时通知播报",
      "fallback": "text-only",
      "playbackMode": "batch"
    }
  },
  "schedules": [
    {
      "id": "scheduled-briefing",
      "enabled": true,
      "days": [1, 2, 3, 4, 5],
      "time": "08:00",
      "modules": ["opening", "environment_brief", "schedule_brief", "closing"],
      "style": {"length": "short", "variability": "medium"}
    }
  ]
}
```

## Example B — One-time reminder override / 示例 B：一次性提醒覆盖

```json
{
  "override": {
    "enabled": true,
    "date": "2026-03-30",
    "time": "08:30",
    "modules": ["opening", "closing"],
    "message": "记得带上资料，出门前再检查一次。"
  }
}
```

## Example C — Multi-slot daily schedules / 示例 C：多时段播报

```json
{
  "schedules": [
    {
      "id": "daily-briefing",
      "enabled": true,
      "days": [1, 2, 3, 4, 5],
      "time": "08:00",
      "modules": ["environment_brief", "schedule_brief"]
    },
    {
      "id": "evening-reminder",
      "enabled": true,
      "days": [1, 2, 3, 4, 5, 6, 7],
      "time": "21:00",
      "modules": ["opening", "closing"]
    }
  ]
}
```

## Optional staged sequence / 可选的分阶段通知序列

```json
{
  "speaker": {
    "runtime": {
      "playbackMode": "staged",
      "stagedSequence": {
        "enabled": true,
        "steps": [
          {
            "text": "It is time for your scheduled notification.",
            "pauseAfterMs": 1000,
            "contextText": "clear, energetic"
          },
          {
            "text": "Are you ready to continue?",
            "pauseAfterMs": 2000,
            "contextText": "soft, clear, and steady"
          }
        ]
      }
    }
  }
}
```

## Data-provider boundary / 数据提供边界

The public skill does not directly connect to calendar, weather, or proprietary data systems.
Those inputs should be provided by the user or injected by the runtime environment through adapters.

本公共 Skill 不直接连接日历、天气或私有数据系统。
这些输入应由用户提供，或由运行环境通过 adapter 注入。
