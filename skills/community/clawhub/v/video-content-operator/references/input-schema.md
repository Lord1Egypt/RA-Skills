# Input Schema (MVP)

This skill can be driven with a lightweight JSON payload.

## Minimal shape

```json
{
  "creator": {
    "name": "Fischer",
    "role": "Founder",
    "company": "Sparki",
    "platforms": ["Xiaohongshu", "YouTube"],
    "content_pattern": "Founder/process/thesis content",
    "current_problem": "Content direction is still too fragmented"
  },
  "goal": "Build trust",
  "platform": "Xiaohongshu",
  "materials": [
    {
      "title": "Founder monologue on creator OS",
      "strength": 9,
      "why": "Contains thesis, tension, and clear positioning"
    },
    {
      "title": "Product demo clip",
      "strength": 7,
      "why": "Provides proof and grounding"
    }
  ]
}
```

## Notes
- `creator` is optional but strongly recommended.
- `goal` and `platform` can be omitted; the script will infer a default.
- `materials` is optional, but without it the skill can only recommend high-level content direction.
- `strength` is a lightweight ranking hint, not a formal score.
