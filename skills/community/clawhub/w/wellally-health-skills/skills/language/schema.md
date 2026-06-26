# Language Settings Data Schema

## File Location

`data/user-settings.json`

## Schema Definition

```json
{
  "language": {
    "preferred": "string",     // User's preferred language (en|zh-CN)
    "detected": "string",      // Auto-detected language from input
    "detected_at": "string",   // ISO 8601 timestamp of last detection
    "confidence": "number"     // Detection confidence (0-1)
  },
  "onboarding": {
    "completed": "boolean",    // Whether onboarding is completed
    "language_set": "boolean", // Whether language has been set during onboarding
    "steps_completed": ["string"] // List of completed onboarding steps
  },
  "conversation": {
    "auto_detect": "boolean",  // Enable/disable automatic language detection
    "fallback_language": "string" // Fallback language (default: en)
  },
  "metadata": {
    "created_at": "string",    // ISO 8601 timestamp
    "last_updated": "string",  // ISO 8601 timestamp
    "version": "string"        // Schema version
  }
}
```

## Field Descriptions

### language.preferred
- **Type**: string
- **Values**: `"en"`, `"zh-CN"`
- **Default**: `"en"`
- **Description**: User's explicitly set language preference

### language.detected
- **Type**: string
- **Values**: `"en"`, `"zh-CN"`
- **Description**: Language auto-detected from user input when auto_detect is enabled

### onboarding.completed
- **Type**: boolean
- **Description**: Whether the user has completed the initial onboarding flow

### onboarding.language_set
- **Type**: boolean
- **Description**: Whether the user has set their language preference during onboarding

### conversation.auto_detect
- **Type**: boolean
- **Default**: `true`
- **Description**: When enabled, automatically detects language from user input

## Language Detection Algorithm

```
chinese_char_ratio = count(chinese_characters) / total_characters
if chinese_char_ratio > 0.3:
    detected = "zh-CN"
else:
    detected = "en"
```

## Update Rules

1. When user explicitly sets language via `/language set`:
   - Update `language.preferred`
   - Set `language.detected` = new value
   - Update `metadata.last_updated`

2. When auto-detection runs and language differs from preferred:
   - Update `language.detected`
   - Update `language.detected_at`
   - Update `language.confidence`
   - DO NOT change `language.preferred`

3. When onboarding completes:
   - Set `onboarding.completed = true`
   - If language was set, set `onboarding.language_set = true`
