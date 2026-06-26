# EditPlan Schema Reference

## JSON Schema

```json
{
  "type": "object",
  "required": ["audio_start", "audio_duration", "clips"],
  "properties": {
    "audio_start": {
      "type": "string",
      "pattern": "^[0-9]{1,3}:[0-9]{2}$",
      "description": "Start time in the audio track in MM:SS format (e.g. 01:15)"
    },
    "audio_duration": {
      "type": "number",
      "exclusiveMinimum": 0,
      "description": "Total duration of the edit (seconds)"
    },
    "clips": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["video_start", "duration"],
        "properties": {
          "video_start": {
            "type": "string",
            "pattern": "^[0-9]{1,3}:[0-9]{2}$",
            "description": "Start time in the source video in MM:SS format (e.g. 02:30)"
          },
          "duration": {
            "type": "number",
            "exclusiveMinimum": 0,
            "description": "Duration of this clip (seconds)"
          },
          "description": {
            "type": "string",
            "description": "Why this clip was chosen"
          }
        }
      }
    },
    "reasoning": {
      "type": "string",
      "description": "Overall edit rationale"
    }
  }
}
```

## Timestamp Format

- **Positions** (`audio_start`, `video_start`): MM:SS strings — e.g. `"01:15"` for 1 minute 15 seconds, `"00:08"` for 8 seconds
- **Durations** (`audio_duration`, `duration`): Numbers in seconds — e.g. `2.5` for 2.5 seconds

This aligns with Gemini's native timestamp format for referring to moments in video.

## Validation Rules

### Hard Rules (must pass)

1. **Clips must exist**: `clips` array must be non-empty
2. **Valid audio_start format**: Must match MM:SS pattern (e.g. `"00:13"`, `"02:30"`)
3. **Non-negative audio_start**: Converted to seconds, must be >= 0
4. **Positive audio_duration**: `audio_duration > 0`
5. **Valid video_start format**: Every clip's `video_start` must match MM:SS pattern
6. **Non-negative video_start**: Converted to seconds, must be >= 0
7. **Positive clip duration**: Every clip's `duration > 0`
8. **Duration sum match**: Sum of all clip durations must equal `audio_duration` within 0.5s tolerance

### Soft Rules (warnings)

- Clips with `duration < 0.1` may produce glitchy output (too few frames)
- Clips with `duration > 30` may feel static in a beat-synced edit
- `video_start` beyond video length will produce black frames
- `audio_start + audio_duration` beyond audio length will produce silence

## Edge Cases

### Non-chronological clips

Clips need NOT be in chronological order relative to the source video. Non-linear ordering is intentional for creative edits:

```json
{
  "clips": [
    { "video_start": "02:00", "duration": 5 },
    { "video_start": "00:10", "duration": 5 },
    { "video_start": "01:00", "duration": 5 }
  ]
}
```

### Repeated source segments

The same source segment can appear multiple times:

```json
{
  "clips": [
    { "video_start": "00:30", "duration": 3 },
    { "video_start": "00:45", "duration": 3 },
    { "video_start": "00:30", "duration": 3 }
  ]
}
```

### Overlapping source segments

Clips can pull from overlapping regions of the source video:

```json
{
  "clips": [
    { "video_start": "00:10", "duration": 5 },
    { "video_start": "00:12", "duration": 5 }
  ]
}
```

### Rapid cuts

Beat-synced edits commonly use very short clips (0.25s). The system handles any number of clips.

## Duration Tolerance

The validation allows a 0.5-second tolerance between the sum of clip durations and `audio_duration`. This accounts for:
- Floating point arithmetic imprecision
- Gemini rounding individual clip durations
- Sub-frame timing differences

If the mismatch exceeds 0.5s, the plan is invalid. To fix:
- Adjust the last clip's duration to absorb the difference
- Re-generate with Gemini using a stricter prompt
