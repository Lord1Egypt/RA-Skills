---
name: language
description: Set, view, or switch user language preference. Use when user wants to change language, check current language setting, or enable/disable auto language detection.
argument-hint: <operation [set|get|auto] [language_code|on|off]>
allowed-tools: Read, Write
---

# Language Settings Skill

Manage user language preferences for the health management system. Supports Chinese (zh-CN) and English (en).

## Core Flow

```
User Input -> Parse Operation -> [set] Update preferred language -> Save
                             -> [get] Read current settings -> Display
                             -> [auto] Enable/disable auto-detection -> Save
```

## Step 1: Parse Operation Type

| Input Keywords | Operation |
|----------------|-----------|
| set, change, switch, 设置, 切换 | set |
| get, view, show, current, 查看, 显示 | get |
| auto, detect, automatic, 自动, 检测 | auto |

## Step 2: Set Language (set)

### Supported Languages

| Code | Language | Native Name |
|------|----------|-------------|
| en | English | English |
| zh-CN | Chinese | 中文 |

### Examples

```
/language set en
/language set zh-CN
/language switch to English
```

## Step 3: Get Language (get)

Display current language settings:

```
/language get
/language show
```

Response format:
- Preferred language
- Auto-detection status
- Fallback language

## Step 4: Auto-Detection (auto)

Enable or disable automatic language detection from user input.

```
/language auto on
/language auto off
```

## Data Structure

The language skill reads and updates `data/user-settings.json`:

```json
{
  "language": {
    "preferred": "en",
    "detected": "en",
    "detected_at": "2026-02-03T10:00:00Z",
    "confidence": 0.95
  },
  "onboarding": {
    "completed": false,
    "language_set": false,
    "steps_completed": []
  },
  "conversation": {
    "auto_detect": true,
    "fallback_language": "en"
  },
  "metadata": {
    "created_at": "2026-02-03T10:00:00Z",
    "last_updated": "2026-02-03T10:00:00Z",
    "version": "1.0.0"
  }
}
```

## Execution Instructions

```
1. Parse operation type
2. [set] Validate language code -> Update user-settings.json -> Confirm
3. [get] Read user-settings.json -> Format display
4. [auto] Toggle auto_detect flag -> Save
```

## Example Interactions

### Set Language

```
User: /language set en

Response:
Language preference updated to English.
Your preferred language: en
```

### Get Language

```
User: /language get

Response:
Current language settings:
- Preferred language: English (en)
- Auto-detection: enabled
- Fallback language: English (en)
```

### Disable Auto-Detection

```
User: /language auto off

Response:
Auto language detection disabled.
The system will always use your preferred language: en
```

## Language Detection Logic

When `auto_detect` is enabled:
1. Analyze user input for Chinese character ratio
2. If Chinese characters > 30%, detect as zh-CN
3. Otherwise, detect as en
4. Store detection result in `detected` field
5. Use detected language for current response
