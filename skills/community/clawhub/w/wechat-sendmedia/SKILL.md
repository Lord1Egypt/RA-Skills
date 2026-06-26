---
name: wechat-sendmedia
description: send images and files to a wechat conversation through openclaw's wechat channel. use when the user asks to send a local image, send a screenshot, send a downloaded file, or send any media/file back to the current wechat chat or an optional recipient. optimized for openclaw builds where the gateway parses MEDIA:file:// tokens from plain text instead of json media envelopes.
---

# Wechat Sendmedia

Use this skill only for the `openclaw-weixin` channel.

## Core rule

For outbound media, prefer the **plain-text MEDIA token** format, not a JSON envelope.

Return the final assistant message as plain text like this:

```text
发送成功
- 类型：图片 | 文件
- 路径：<absolute path>
- 接收人：当前会话 | <recipient>

MEDIA:file:///absolute/path/to/file.png
```

Why: newer OpenClaw gateway builds parse media only from text directives such as `MEDIA:file:///...`. If you return JSON like `{ "mediaUrl": "file:///..." }`, the gateway may forward that JSON as plain text and no image/file will be delivered.

## Never do this

Do not rely on these formats as the primary output:

```json
{
  "text": "这是你要的图片",
  "mediaUrl": "file:///tmp/x.png"
}
```

or:

```json
{
  "text": "...",
  "mediaUrl": "MEDIA:file:///tmp/x.png"
}
```

These may be displayed to the user as literal text.

## Supported tasks

Handle these tasks:

- Send a local image file to WeChat.
- Take a browser or desktop screenshot, then send it.
- Send a non-image file such as a PDF, text file, archive, or document.
- Send to the current conversation by default.
- Send to a specific recipient only if the user explicitly provides one.
- Return `发送成功` or `发送失败` plus actionable diagnostics.

## Inputs

Interpret the request into:

- `file_path`: absolute local path to an existing file, or a screenshot path produced earlier.
- `recipient`: optional. Default `当前会话`.
- `caption`: optional short note for the human-readable confirmation text.
- `source_kind`: `image` or `file`.

If the user asks for a screenshot first, obtain the screenshot file before sending.

## Output contract

### Success outcome

Return plain text only:

```text
发送成功
- 类型：图片
- 路径：/tmp/browser-shot.png
- 接收人：当前会话

MEDIA:file:///tmp/browser-shot.png
```

Rules:

- The `MEDIA:file://...` directive must be on its own line.
- Use an absolute local path.
- Use `图片` for common image types and `文件` for everything else.
- Keep the confirmation short.
- Do not wrap the final reply in JSON unless the host explicitly requires JSON. For current OpenClaw builds, plain text is the safe default.

### Failure outcome

Return:

```text
发送失败
- 可能原因：<one line summary>
- 建议：<next step>

调试信息:
- file_path: <path>
- exists: true|false
- recipient: <recipient>
- upload_url: <value or n/a>
- upload_url_host: <value or n/a>
- encrypted_param_length: <number or 0>
- sendmessage_status: <value or n/a>
- sendmessage_response: <raw text or n/a>
- context_token_present: true|false
- media_type_guess: image|file|unknown
```

## Workflow

1. Resolve the user's intent.
2. Ensure the target file exists.
3. Run `scripts/emit_media_reply.py` to validate the file and build the plain-text reply payload.
4. Return the script's `reply_text` value as the assistant message.
5. If a send attempt fails or the user reports a failed send, run `scripts/weixin_debug_send.js` to produce targeted diagnostics.
6. Summarize the result in Chinese.

## File-type decision rules

Treat these as images by default:

- `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.bmp`

Treat everything else as files.

## Recipient rules

- If the user says `发给我` and the current task came from WeChat, use `当前会话`.
- Only override the recipient if the user explicitly names another receiver.
- If a concrete user id is unavailable, keep `recipient` as `当前会话` in the confirmation text and let the host runtime map it to the current chat.

## Troubleshooting rules

When debugging an OpenClaw WeChat media failure, prefer concrete evidence over guesses.

Common causes to mention only when supported by the debug output:

- File path does not exist.
- Host runtime treated the reply as plain text because no `MEDIA:` token was present.
- Missing context token for the current chat.
- Upload URL not returned.
- `x-encrypted-param` missing or unexpectedly short.
- `sendmessage` returned empty body or non-success JSON.
- Token/session mismatch between runtime state and on-disk account data.
- Wrong route used: JSON envelope or slash command text instead of `MEDIA:file://...`.

## Examples

### Example: screenshot request

Final reply:

```text
发送成功
- 类型：图片
- 路径：/tmp/browser-shot.png
- 接收人：当前会话

MEDIA:file:///tmp/browser-shot.png
```

### Example: document request

Final reply:

```text
发送成功
- 类型：文件
- 路径：/Users/example/Desktop/report.pdf
- 接收人：当前会话

MEDIA:file:///Users/example/Desktop/report.pdf
```

## Resources

- Use `scripts/emit_media_reply.py` to validate a path and build `reply_text`.
- Use `scripts/weixin_debug_send.js` to collect failure diagnostics.
- See `references/openclaw-weixin-notes.md` for compatibility notes.
