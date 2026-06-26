# Sora 2 Prompt Generator API Reference

## Endpoint

- `POST https://nanophoto.ai/api/sora-2/generate-prompt`

## Authentication

```text
Authorization: Bearer YOUR_API_KEY
```

For OpenClaw users, the recommended setup is:

- `env.NANOPHOTO_API_KEY=YOUR_API_KEY`
- Structured skill metadata should declare `requires.env=["NANOPHOTO_API_KEY"]` and `primaryEnv="NANOPHOTO_API_KEY"`

## Credits

- Costs 2 credits per generation
- Credits are pre-deducted and refunded automatically if generation fails

## Request fields

| Field | Type | Required | Notes |
|------|------|----------|------|
| `topic` | string | Yes | Max 500 characters |
| `mode` | string | No | `textToVideo` or `imageToVideo`; default `textToVideo` |
| `technique` | string | No | Default `montage` |
| `duration` | number | No | `10` or `15`; default `10` |
| `model` | string | No | Default `google/gemini-3-flash-preview` |
| `locale` | string | No | Default `en`; supported: `en`, `zh`, `zh-TW`, `ja`, `ko`, `es`, `fr`, `de`, `pt`, `ru`, `ar` |
| `imageUrls` | string[] | No | Public image URLs only; max 3; required for `imageToVideo` |

## Supported techniques

- `montage`
- `long-take`
- `time-lapse`
- `slow-motion`
- `tracking-shot`
- `aerial-view`
- `pov`
- `split-screen`
- `match-cut`
- `fade-transition`

## Response behavior

- The API returns streaming text (`Content-Type: text/plain; charset=utf-8`)
- The output is the generated Sora 2 prompt text
- The prompt typically includes scene structure, shot design, camera movement, lighting, mood, and timing details

## Error codes

| errorCode | HTTP Status | Description |
|-----------|-------------|-------------|
| `LOGIN_REQUIRED` | 401 | Authentication required |
| `API_KEY_RATE_LIMIT_EXCEEDED` | 429 | Rate limit exceeded |
| `INSUFFICIENT_CREDITS` | 402 | Not enough credits |
| `INVALID_INPUT` | 400 | Topic is missing, empty, or too long |

## Notes

- `imageUrls` must be publicly accessible URLs
- Base64 image upload is not supported
- Keep topics concise but descriptive for best results
