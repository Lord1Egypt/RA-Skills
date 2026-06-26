---
name: weixin-send-media
description: Send images, PDFs, and other local files into an OpenClaw Weixin chat. Use when the user asks to send a picture, screenshot, PDF, document, attachment, or other media/file in the current Weixin conversation.
---

# weixin-send-media

Use this skill when the current channel is `openclaw-weixin` and the user wants a file or image delivered into chat.

## Rules

- Prefer sending the file directly instead of telling the user where it is.
- Always use an **absolute local path** for generated files.
- Before sending a user-facing export/share file, place it under `deliveries/YYYY-MM-DD/HHMMSS/`.
- If the source file belongs to a project folder, keep the source there and create a share/export copy in the delivery folder.
- If you need a test asset, generate a tiny file first, then send it.
- For this environment, if no first-class messaging tool is available, use the OpenClaw CLI.

## Send with CLI

Use:

```bash
openclaw message send \
  --channel openclaw-weixin \
  --account <account_id> \
  --target <chat_id_or_user_id> \
  --message "<optional caption>" \
  --media /absolute/path/to/file
```

## Where to get values

- `account_id`: use the trusted inbound metadata `account_id` for the current chat.
- `target`: use the trusted inbound metadata `chat_id` for the current chat.
- `media`: absolute path to the file you created or selected.

## Typical uses

- Send a generated PDF.
- Send a generated PNG/JPG screenshot.
- Send a DOCX/XLSX/PPTX file.
- Send a local attachment as a quick delivery step after creating it.

## Verification

After sending, briefly ask the user whether they received it.

## Example

```bash
openclaw message send \
  --channel openclaw-weixin \
  --account 30c94de8bd87-im-bot \
  --target o9cq8086Br1CV1qVLcKn5WqTRpTE@im.wechat \
  --message "测试文件" \
  --media /root/.openclaw/workspace-wx-30c94de8/test.pdf
```

