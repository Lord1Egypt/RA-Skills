# Language Settings Examples

## Example 1: First-Time User Setup

```
User: /language set zh-CN

System:
Language preference updated to Chinese (zh-CN).
您的语言偏好已设置为中文。

Current settings:
- Preferred language: 中文 (zh-CN)
- Auto-detection: enabled
```

## Example 2: Check Current Language

```
User: /language get

System:
Current language settings:
- Preferred language: English (en)
- Auto-detection: enabled
- Fallback language: English (en)

The system will respond in your preferred language.
```

## Example 3: Disable Auto-Detection

```
User: /language auto off

System:
Auto language detection disabled.
The system will always use your preferred language: English (en)

To re-enable, use: /language auto on
```

## Example 4: Switch Between Languages

```
User: /language set en

System:
Language preference updated to English.

User: /language set zh-CN

System:
语言偏好已更新为中文。
您的首选语言：中文 (zh-CN)
```

## Example 5: Onboarding Flow

```
User: [First message - no user-settings.json exists]

System:
Welcome to WellallyHealth!

Please select your preferred language / 请选择您的首选语言:
1. English
2. 中文 (Chinese)

User: 1

System:
Language set to English.
Let's continue setting up your profile...
```

## Example 6: Auto-Detection in Action

```
[auto_detect enabled, preferred: en]

User: 你好，我想查看我的血压记录

System:
[Detects Chinese characters > 30%]
[Updates detected: zh-CN]
[Responds in Chinese]

您好！我帮您查看血压记录...
[Shows blood pressure records in Chinese]
```

## Example 7: Mixed Language Input

```
[auto_detect enabled, preferred: en]

User: My BP is 120/80 mmHg

System:
[Detects English]
[Updates detected: en]
[Responds in English]

Blood pressure recorded: 120/80 mmHg
This is within the normal range.
```

## Example 8: Language Persistence

```
User: /language set en

System:
[Updates user-settings.json]
{
  "language": {
    "preferred": "en",
    "detected": "en",
    "detected_at": "2026-02-03T10:30:00Z",
    "confidence": 1.0
  },
  "onboarding": {
    "completed": true,
    "language_set": true,
    "steps_completed": ["language_selection"]
  },
  "conversation": {
    "auto_detect": true,
    "fallback_language": "en"
  }
}

Language preference saved. It will be used in all future conversations.
```
