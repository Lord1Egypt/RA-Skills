---
name: qqbot-send
description: Send local files, images, audio, video, and other media through QQBot end to end. Use when the user asks to send a file to QQ, send a desktop/downloads/local absolute-path file, resend a local attachment, or when QQBot file sending should automatically stage the file into the QQ media relay directory and then deliver it with qqmedia tagging.
---

# QQBot Send

Use this skill for QQ file sending end to end.

## Core rule

When the user wants a file sent through QQ, complete the full send flow instead of only returning a path.

## Built-in staging flow

This skill includes the old `qqbot-local-media` behavior.

For local files that are not already in the QQ media relay directory:

1. Run:
   - `python scripts/stage_media.py <source_path>`
2. The script copies the file into:
   - `~/.openclaw/media/qqbot/`
3. Use the returned absolute path in:
   - `<qqmedia>absolute-path</qqmedia>`

## Decision flow

1. Identify the source.
   - If the source is a local absolute path outside the QQ media relay area, stage it first.
   - If the source is already inside the OpenClaw QQ media relay directory, use it directly.
   - If the source is an HTTP(S) URL, send it directly with `<qqmedia>...</qqmedia>`.
   - If the source is a local attachment path already provided in context and QQBot can send it directly, send it directly.

2. For local files that need staging, use the bundled script in this skill.

3. Then send with QQ rich media.
   - Use `<qqmedia>absolute-path-or-url</qqmedia>`
   - One file per tag.

## Default practical flow

For most local desktop/downloads/workspace-external files:

1. Stage into `~/.openclaw/media/qqbot/`
2. Send with `<qqmedia>...</qqmedia>`

## Size and path rules

- Absolute local paths only
- File size limit is 10 MB
- Preserve the original file extension
- Copy the file, do not modify the original
- Do not claim you cannot send local files when the path is readable and within the size limit

## Response behavior

- If the user asked to send the file, actually send it.
- Do not only explain the flow unless the user asked a conceptual question.
- If staging fails because the file does not exist, say that directly.
- If staging fails because the file is too large, say that directly.

## Examples

### Example 1: Desktop PDF
- User asks: send `C:\Users\name\Desktop\resume.pdf` to QQ
- Action:
  1. `python scripts/stage_media.py "C:\Users\name\Desktop\resume.pdf"`
  2. send `<qqmedia>staged-absolute-path</qqmedia>`

### Example 2: Already staged file
- User asks to send `C:\Users\name\.openclaw\media\qqbot\abc.pdf`
- Action:
  1. send `<qqmedia>C:\Users\name\.openclaw\media\qqbot\abc.pdf</qqmedia>` directly

### Example 3: URL image
- User asks to send an image URL to QQ
- Action:
  1. send `<qqmedia>https://example.com/image.png</qqmedia>` directly

## Notes

- Prefer completing the send in one turn.
- Use the bundled staging script whenever the file is local and not already staged.
- Use `<qqmedia>...</qqmedia>` for final delivery.
