---
name: sign-off
description: "Append a personalized signature to mark the end of AI output. Like saying 'Over' on a walkie-talkie — so the user knows you're done."
---

# Sign-Off — AI Output End Marker

Append a personalized signature at the end of every complete output, so the user knows you're done.

## When to Trigger

Append the signature **only at the very end** of:

- A complete response
- A tool call result summary
- The final paragraph of multi-part output

## When NOT to Trigger

- Still thinking/streaming (don't append mid-output)
- Status updates like "Processing..."
- NO_REPLY scenarios

## Signature Format

On a new line after the response content:

```
Your response here...

      {signature}
```

Use indentation (4 spaces or 1 tab) to visually separate the signature.

## Configuration

Read `sign-off.json` from the workspace root:

- **Config exists:** Use the template and variables to render the signature
- **No config:** Use default `{agentName} · {location}`

## Variable Rendering

| Variable | Source | Example |
|----------|--------|---------|
| `{name}` | sign-off.json → name | Luna |
| `{location}` | sign-off.json → location | Hangzhou |
| `{emoji}` | sign-off.json → emoji | 🌙 |
| `{seal}` | sign-off.json → seal | [Seal] |
| `{season}` | Auto-detected | Spring/Summer/Autumn/Winter |
| `{weather}` | Auto (weather API) | Sunny/Rainy |
| `{time}` | Auto (time of day) | Morning/Afternoon/Evening/Night |
| `{greeting}` | Auto | Good morning/Good night |
| `{dayOfWeek}` | Auto | Friday |
| `{zodiac}` | Auto | Year of the Snake |
| `{mood}` | sign-off.json → mood | Playful/Serious |

## Context Modes

If `contextMode` is configured, select template by context:

- **work:** Technical discussion, command execution → concise style
- **casual:** Chat, Q&A → relaxed style
- **auto** (default): AI decides

## Verbal Configuration

Users can customize via conversation:

> "Change your signature to From Luna, Hangzhou, with 🧡"

Update `sign-off.json` accordingly.

## Template Library

Users can install preset styles:

> "Switch to calligraphy style"

Read the matching template from `templates/` and merge into `sign-off.json`.
