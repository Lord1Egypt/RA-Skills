# OpenClaw Weixin notes

## Current compatibility rule

For current OpenClaw builds, the safest outbound-media format is a plain-text directive:

```text
MEDIA:file:///absolute/path/to/file.png
```

The gateway can parse this token from assistant text and route the file through the WeChat media-send path.

## Why the old skill broke

Older iterations of this skill relied on a JSON-like media envelope such as:

```json
{
  "text": "这是你要的图片",
  "mediaUrl": "file:///tmp/example.png"
}
```

If the gateway no longer extracts `mediaUrl` from structured output, that JSON is forwarded as plain text and the user receives text instead of an image.

## New default

Generate human-readable confirmation text plus a trailing `MEDIA:file://...` line. This keeps the skill compatible with gateways that only parse text directives.

## Failure diagnosis

When a send fails, capture or preserve any available runtime fields and pass them to `scripts/weixin_debug_send.js`, especially:

- `upload_url`
- `encrypted_param`
- `sendmessage_status`
- `sendmessage_response`
