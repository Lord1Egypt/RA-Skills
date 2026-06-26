---
name: sora-watermark-remover
description: "Remove watermarks from Sora 2 generated videos via the NanoPhoto.AI API. Use when: (1) User needs Sora watermark removal or a watermark remover for a Sora video, (2) User provides a Sora share link from sora.chatgpt.com and wants a clean downloadable video, (3) User mentions remove watermark, no watermark, clean Sora export, Sora share link, or NanoPhoto. Prerequisite: Obtain an API key at https://nanophoto.ai/settings/apikeys and configure env.NANOPHOTO_API_KEY."
---

# Sora Watermark Remover

Remove watermarks from Sora 2 generated videos via the NanoPhoto.AI API.

Publisher / source:

- Publisher: NanoPhotoHQ
- Homepage: https://nanophoto.ai
- API key management: https://nanophoto.ai/settings/apikeys
- Additional publishing notes: [PUBLISHING.md](PUBLISHING.md)

## Prerequisites

1. Obtain an API key at: https://nanophoto.ai/settings/apikeys
2. Configure `NANOPHOTO_API_KEY` before using the skill.
3. Do not paste the API key into chat; store it in the platform's secure env setting for this skill.

Preferred OpenClaw setup:

- Open the skill settings for this skill
- Add an environment variable named `NANOPHOTO_API_KEY`
- Paste the API key as its value

Equivalent config shape:

```json
{
  "skills": {
    "entries": {
      "sora-watermark-remover": {
        "enabled": true,
        "env": {
          "NANOPHOTO_API_KEY": "your_api_key_here"
        }
      }
    }
  }
}
```

Other valid ways to provide the key:

- **Shell**: `export NANOPHOTO_API_KEY="your_api_key_here"`
- **Tool-specific env config**: any runtime that injects `NANOPHOTO_API_KEY`

Credential declaration summary:

- Required env var: `NANOPHOTO_API_KEY`
- Primary credential: `NANOPHOTO_API_KEY`
- No unrelated credentials are required

If the env var is not set, ask the user to configure it before proceeding.

## Workflow

1. Collect the Sora 2 share link from the user (format: `https://sora.chatgpt.com/p/...`)
2. Validate the link contains `sora.chatgpt.com/p/`
3. Confirm the user is authorized to process the content and that watermark removal is allowed for their use case
4. Call the API to remove the watermark
5. Return the clean video URL to the user

## API Call

```bash
curl -X POST "https://nanophoto.ai/api/sora/remove-watermark" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $NANOPHOTO_API_KEY" \
  --data-raw '{
    "share_link": "https://sora.chatgpt.com/p/s_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
  }'
```

**Success response:**
```json
{
  "success": true,
  "status": "completed",
  "url": "https://video.nanophoto.ai/sora/watermark-remover/xxx.mp4"
}
```

## Error Handling

| errorCode | Cause | Action |
|-----------|-------|--------|
| `LOGIN_REQUIRED` | Invalid or missing API key | Verify key at https://nanophoto.ai/settings/apikeys |
| `API_KEY_RATE_LIMIT_EXCEEDED` | >100 requests/hour | Wait and retry |
| `MISSING_SHARE_LINK` | No `share_link` in body | Ask user for the Sora share link |
| `INVALID_SHARE_LINK` | Link doesn't match `sora.chatgpt.com/p/` | Ask user to provide a valid Sora 2 share link |
| `GENERATION_FAILED` | Server-side processing error | Retry or report to user |

## Full API Reference

See [references/api.md](references/api.md) for complete endpoint documentation.
