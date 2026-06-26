# Interaction Log: [Sister Name]

> Storage: `~/.sister-skill/sisters/[name]/interaction-log.jsonl`

## Log Entry Format

```json
{
  "timestamp": "ISO-8601 datetime",
  "type": "memory|observation|interaction|update",
  "content": "What you described or observed",
  "profile_updates": ["dimensions that were updated"],
  "confidence": "high|medium|low",
  "source": "personal_memory|description|story"
}
```

## Example Entries

### Memory Entry
```json
{
  "timestamp": "2025-03-15T14:30:00Z",
  "type": "memory",
  "content": "Amy always starts texts with OKAY BUT followed by a screenshot with zero context. She never explains the screenshot first — she expects you to figure out why she's mad.",
  "profile_updates": ["voice_conversation_opener", "voice_texting_style"],
  "confidence": "high",
  "source": "personal_memory"
}
```

### Observation Entry
```json
{
  "timestamp": "2025-03-20T09:00:00Z",
  "type": "observation",
  "content": "When Lin gives advice she always asks 'how does that make you feel' first before telling you what to do. She never leads with her opinion.",
  "profile_updates": ["emotional_intelligence_advice_style"],
  "confidence": "medium",
  "source": "personal_memory"
}
```

## Confidence Levels

| Level | When to Use |
|-------|-------------|
| high | You've seen this pattern many times, very confident |
| medium | Seen it a few times, fairly confident |
| low | Single memory, uncertain |

## Source Types

| Source | Description |
|--------|-------------|
| personal_memory | Your own memory of her |
| description | A description you provided |
| story | A story you told about her |

*Log entries are cumulative. Earlier observations are preserved alongside newer ones.*
