# Session Observer Checklist

## Primary tool
- `session_status`

## Key fields to summarize
- model
- tokens in / out
- context used / total
- cache hit ratio
- usage remaining
- runtime, reasoning, elevated status

## Suggested interpretations
- <30% context: healthy
- 30-60% context: watch
- >60% context: consider new thread / compaction-friendly behavior

## Good follow-ups
- suggest a new thread for topic shifts
- suggest sub-agents for large tasks
- suggest tighter outputs when context pressure rises
