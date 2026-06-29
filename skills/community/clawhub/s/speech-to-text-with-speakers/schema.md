# Speech to Text With Speakers Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `speech-to-text-with-speakers`

x402 availability: not enabled for this product.

## `transcribe_extended`

Action slug: `transcribe-extended`

Price: `200` credits

Transcribe audio up to 60 minutes.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `enable_diarization` | `boolean` | no | Enable speaker diarization when supported by the audio and model. Not supported when remove_filler_words is false. |
| `enable_profanity_filter` | `boolean` | no | Mask profanity in the returned transcript. |
| `enable_word_timestamps` | `boolean` | no | Include word-level timing data in the output. |
| `file_id` | `string` | no | File ID from a prior upload. Provide either file_id or public_url. |
| `language_code` | `string` | no | Optional BCP-47 language code such as en-US; defaults to en-US if omitted. |
| `max_alternatives` | `integer` | no | Maximum number of alternative transcripts to return. Must be 1 when remove_filler_words is false. |
| `output_format` | `string` | no | Output format for the transcription result. |
| `public_url` | `string` | no | HTTPS URL to a downloadable audio file. Provide either public_url or file_id. |
| `remove_filler_words` | `boolean` | no | When true (default), return a cleaned transcript with disfluencies removed. When false, preserve filler words and disfluencies; this path does not support diarization or max_alternatives greater than 1. |

Sample parameters:

```json
{
  "enable_diarization": false,
  "enable_profanity_filter": false,
  "enable_word_timestamps": false,
  "file_id": "example file id",
  "language_code": "example language code",
  "max_alternatives": 1,
  "output_format": "text",
  "public_url": "https://example.com"
}
```

Generated JSON parameter schema:

```json
{
  "enable_diarization": {
    "default": false,
    "description": "Enable speaker diarization when supported by the audio and model. Not supported when remove_filler_words is false.",
    "required": false,
    "type": "boolean"
  },
  "enable_profanity_filter": {
    "default": false,
    "description": "Mask profanity in the returned transcript.",
    "required": false,
    "type": "boolean"
  },
  "enable_word_timestamps": {
    "default": false,
    "description": "Include word-level timing data in the output.",
    "required": false,
    "type": "boolean"
  },
  "file_id": {
    "description": "File ID from a prior upload. Provide either file_id or public_url.",
    "required": false,
    "type": "string"
  },
  "language_code": {
    "description": "Optional BCP-47 language code such as en-US; defaults to en-US if omitted.",
    "required": false,
    "type": "string"
  },
  "max_alternatives": {
    "default": 1,
    "description": "Maximum number of alternative transcripts to return. Must be 1 when remove_filler_words is false.",
    "maximum": 5,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "output_format": {
    "default": "text",
    "description": "Output format for the transcription result.",
    "enum": [
      "text",
      "srt",
      "vtt",
      "json"
    ],
    "required": false,
    "type": "string"
  },
  "public_url": {
    "description": "HTTPS URL to a downloadable audio file. Provide either public_url or file_id.",
    "required": false,
    "type": "string"
  },
  "remove_filler_words": {
    "default": true,
    "description": "When true (default), return a cleaned transcript with disfluencies removed. When false, preserve filler words and disfluencies; this path does not support diarization or max_alternatives greater than 1.",
    "required": false,
    "type": "boolean"
  }
}
```

## `transcribe_quick`

Action slug: `transcribe-quick`

Price: `100` credits

Transcribe audio up to 15 minutes.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `enable_diarization` | `boolean` | no | Enable speaker diarization when supported by the audio and model. Not supported when remove_filler_words is false. |
| `enable_profanity_filter` | `boolean` | no | Mask profanity in the returned transcript. |
| `enable_word_timestamps` | `boolean` | no | Include word-level timing data in the output. |
| `file_id` | `string` | no | File ID from a prior upload. Provide either file_id or public_url. |
| `language_code` | `string` | no | Optional BCP-47 language code such as en-US; defaults to en-US if omitted. |
| `max_alternatives` | `integer` | no | Maximum number of alternative transcripts to return. Must be 1 when remove_filler_words is false. |
| `output_format` | `string` | no | Output format for the transcription result. |
| `public_url` | `string` | no | HTTPS URL to a downloadable audio file. Provide either public_url or file_id. |
| `remove_filler_words` | `boolean` | no | When true (default), return a cleaned transcript with disfluencies removed. When false, preserve filler words and disfluencies; this path does not support diarization or max_alternatives greater than 1. |

Sample parameters:

```json
{
  "enable_diarization": false,
  "enable_profanity_filter": false,
  "enable_word_timestamps": false,
  "file_id": "example file id",
  "language_code": "example language code",
  "max_alternatives": 1,
  "output_format": "text",
  "public_url": "https://example.com"
}
```

Generated JSON parameter schema:

```json
{
  "enable_diarization": {
    "default": false,
    "description": "Enable speaker diarization when supported by the audio and model. Not supported when remove_filler_words is false.",
    "required": false,
    "type": "boolean"
  },
  "enable_profanity_filter": {
    "default": false,
    "description": "Mask profanity in the returned transcript.",
    "required": false,
    "type": "boolean"
  },
  "enable_word_timestamps": {
    "default": false,
    "description": "Include word-level timing data in the output.",
    "required": false,
    "type": "boolean"
  },
  "file_id": {
    "description": "File ID from a prior upload. Provide either file_id or public_url.",
    "required": false,
    "type": "string"
  },
  "language_code": {
    "description": "Optional BCP-47 language code such as en-US; defaults to en-US if omitted.",
    "required": false,
    "type": "string"
  },
  "max_alternatives": {
    "default": 1,
    "description": "Maximum number of alternative transcripts to return. Must be 1 when remove_filler_words is false.",
    "maximum": 5,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "output_format": {
    "default": "text",
    "description": "Output format for the transcription result.",
    "enum": [
      "text",
      "srt",
      "vtt",
      "json"
    ],
    "required": false,
    "type": "string"
  },
  "public_url": {
    "description": "HTTPS URL to a downloadable audio file. Provide either public_url or file_id.",
    "required": false,
    "type": "string"
  },
  "remove_filler_words": {
    "default": true,
    "description": "When true (default), return a cleaned transcript with disfluencies removed. When false, preserve filler words and disfluencies; this path does not support diarization or max_alternatives greater than 1.",
    "required": false,
    "type": "boolean"
  }
}
```

## `transcribe_standard`

Action slug: `transcribe-standard`

Price: `150` credits

Transcribe audio up to 30 minutes.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `enable_diarization` | `boolean` | no | Enable speaker diarization when supported by the audio and model. Not supported when remove_filler_words is false. |
| `enable_profanity_filter` | `boolean` | no | Mask profanity in the returned transcript. |
| `enable_word_timestamps` | `boolean` | no | Include word-level timing data in the output. |
| `file_id` | `string` | no | File ID from a prior upload. Provide either file_id or public_url. |
| `language_code` | `string` | no | Optional BCP-47 language code such as en-US; defaults to en-US if omitted. |
| `max_alternatives` | `integer` | no | Maximum number of alternative transcripts to return. Must be 1 when remove_filler_words is false. |
| `output_format` | `string` | no | Output format for the transcription result. |
| `public_url` | `string` | no | HTTPS URL to a downloadable audio file. Provide either public_url or file_id. |
| `remove_filler_words` | `boolean` | no | When true (default), return a cleaned transcript with disfluencies removed. When false, preserve filler words and disfluencies; this path does not support diarization or max_alternatives greater than 1. |

Sample parameters:

```json
{
  "enable_diarization": false,
  "enable_profanity_filter": false,
  "enable_word_timestamps": false,
  "file_id": "example file id",
  "language_code": "example language code",
  "max_alternatives": 1,
  "output_format": "text",
  "public_url": "https://example.com"
}
```

Generated JSON parameter schema:

```json
{
  "enable_diarization": {
    "default": false,
    "description": "Enable speaker diarization when supported by the audio and model. Not supported when remove_filler_words is false.",
    "required": false,
    "type": "boolean"
  },
  "enable_profanity_filter": {
    "default": false,
    "description": "Mask profanity in the returned transcript.",
    "required": false,
    "type": "boolean"
  },
  "enable_word_timestamps": {
    "default": false,
    "description": "Include word-level timing data in the output.",
    "required": false,
    "type": "boolean"
  },
  "file_id": {
    "description": "File ID from a prior upload. Provide either file_id or public_url.",
    "required": false,
    "type": "string"
  },
  "language_code": {
    "description": "Optional BCP-47 language code such as en-US; defaults to en-US if omitted.",
    "required": false,
    "type": "string"
  },
  "max_alternatives": {
    "default": 1,
    "description": "Maximum number of alternative transcripts to return. Must be 1 when remove_filler_words is false.",
    "maximum": 5,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "output_format": {
    "default": "text",
    "description": "Output format for the transcription result.",
    "enum": [
      "text",
      "srt",
      "vtt",
      "json"
    ],
    "required": false,
    "type": "string"
  },
  "public_url": {
    "description": "HTTPS URL to a downloadable audio file. Provide either public_url or file_id.",
    "required": false,
    "type": "string"
  },
  "remove_filler_words": {
    "default": true,
    "description": "When true (default), return a cleaned transcript with disfluencies removed. When false, preserve filler words and disfluencies; this path does not support diarization or max_alternatives greater than 1.",
    "required": false,
    "type": "boolean"
  }
}
```
