# Youtube Transcript Fetcher Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `youtube-transcript-fetcher`

x402 availability: not enabled for this product.

## `fetch`

Action slug: `fetch`

Price: `25` credits

Fetch the transcript for a YouTube video. Provide either video_url or video_id. The transcript is saved to cloud storage and a signed download URL is returned.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `include_raw_response` | `boolean` | no | When true, the saved transcript file includes the full raw provider response (useful for debugging; may be large). Default: false. |
| `include_timestamps` | `boolean` | no | When true, the saved transcript file includes timestamped segments with start time and duration. Default: false. |
| `language` | `string` | no | Transcript language code (e.g., 'en', 'es', 'fr'). If omitted, the video's default language is used. |
| `video_id` | `string` | no | YouTube video ID (11 characters). Takes precedence over video_url if both are provided. |
| `video_url` | `string` | no | Full YouTube URL. Supported formats: youtube.com/watch?v=, youtu.be/, shorts, embeds, live. Provide either video_url or video_id. |

Sample parameters:

```json
{
  "include_raw_response": false,
  "include_timestamps": false,
  "language": "example language",
  "video_id": "example video id",
  "video_url": "https://example.com"
}
```

Generated JSON parameter schema:

```json
{
  "include_raw_response": {
    "default": false,
    "description": "When true, the saved transcript file includes the full raw provider response (useful for debugging; may be large). Default: false.",
    "required": false,
    "type": "boolean"
  },
  "include_timestamps": {
    "default": false,
    "description": "When true, the saved transcript file includes timestamped segments with start time and duration. Default: false.",
    "required": false,
    "type": "boolean"
  },
  "language": {
    "description": "Transcript language code (e.g., 'en', 'es', 'fr'). If omitted, the video's default language is used.",
    "required": false,
    "type": "string"
  },
  "video_id": {
    "description": "YouTube video ID (11 characters). Takes precedence over video_url if both are provided.",
    "required": false,
    "type": "string"
  },
  "video_url": {
    "description": "Full YouTube URL. Supported formats: youtube.com/watch?v=, youtu.be/, shorts, embeds, live. Provide either video_url or video_id.",
    "required": false,
    "type": "string"
  }
}
```
