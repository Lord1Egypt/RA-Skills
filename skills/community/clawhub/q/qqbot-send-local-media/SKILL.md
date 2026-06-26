---
name: qqbot-send
description: Safely send local files, images, audio, video, and other media through QQBot. Use when a user asks to send a desktop/downloads/absolute-path file, resend a local attachment, or deliver media with <qqmedia>. The skill stages a disposable copy in the QQ media relay directory, sends only that staged copy, and cleans up the staged file without touching the original.
---

# QQBot Send Local Media

Safely deliver local files through QQBot by staging a disposable copy, sending it with `<qqmedia>`, and deleting only the staged copy afterward.

This skill is for agents that need a reliable end-to-end QQ file-send workflow instead of merely returning a local path.

## What it helps with

- Send local PDFs, images, audio, video, and other files through QQBot.
- Stage files into the OpenClaw QQ media relay directory.
- Avoid deleting or modifying the original user file.
- Clean up only the staged copy created for the current send.
- Handle URLs directly without unnecessary staging.

## Core rule

When the user wants a file sent through QQ, complete the full send flow instead of only returning a path.

For local files, always create a dedicated staged copy first, send that staged copy, and then delete only the staged copy returned by the staging script.

Never delete the original source file.

## Built-in staging and cleanup flow

For local files:

1. Run:
   - `python scripts/stage_media.py <source_path>`

2. The script copies the file into:
   - `~/.openclaw/media/qqbot/`

3. The script prints the staged absolute path.

4. Send the staged path with:
   - `<qqmedia>staged-absolute-path</qqmedia>`

5. After the QQBot send attempt finishes, clean up the staged file by running:
   - `python scripts/stage_media.py --cleanup <staged-absolute-path>`

The cleanup path must be exactly the path returned by the staging command.

Do not call cleanup on the original source path.

Do not call cleanup on a manually guessed path.

Do not call cleanup on an HTTP(S) URL.

## Decision flow

1. Identify the source.

   - If the source is a local absolute path, stage it first with `python scripts/stage_media.py <source_path>`.
   - If the source is already inside the OpenClaw QQ media relay directory, still stage it first to create a new disposable copy for this send.
   - If the source is an HTTP(S) URL, send it directly with `<qqmedia>...</qqmedia>` and do not run cleanup.
   - If the source is a local attachment path already provided in context, stage it first before sending.

2. For every local file send:

   - Use the bundled staging script.
   - Capture the exact staged path printed by the script.
   - Send only the staged path using `<qqmedia>...</qqmedia>`.
   - After sending, run cleanup only on that captured staged path.

3. For URL media:

   - Send the URL directly using `<qqmedia>...</qqmedia>`.
   - Do not stage.
   - Do not cleanup.

## Default practical flow

For local desktop/downloads/workspace-external files, and also for local files already under the QQ media relay directory:

1. Stage the source file into a new temporary file under `~/.openclaw/media/qqbot/`
2. Send the staged file with `<qqmedia>...</qqmedia>`
3. Delete only the staged file returned by the staging script

The source file must remain untouched.

## Cleanup safety rules

Cleanup is only allowed for a staged file produced during the current send flow.

The only valid cleanup target is the exact path returned by:

- `python scripts/stage_media.py <source_path>`

Never cleanup any of these:

- the original source path
- a user-provided path
- an HTTP(S) URL
- a path guessed from the source filename
- a path merely because it is under `~/.openclaw/media/qqbot/`
- a path that was not returned by the current staging command

If staging fails, do not send and do not cleanup.

If sending fails after staging succeeds, still attempt cleanup of the staged path.

If cleanup fails, report the cleanup failure, but do not retry cleanup on any other path.

## Size and path rules

- Absolute local paths only
- File size limit is 100 MB
- Copy the file, do not modify the original
- The staged copy uses a generated UUID filename
- The original extension is preserved semantically, but normalized to lowercase by the staging script
- Do not claim you cannot send local files when the path is readable and within the size limit

## File occupied behavior

If the staging script reports that the source file is occupied, locked, or cannot be opened, do not send the file.

Report that the file is currently occupied or unavailable.

Do not attempt cleanup because no staged file was safely created.

## Response behavior

- If the user asked to send the file, actually send it.
- Do not only explain the flow unless the user asked a conceptual question.
- If staging fails because the file does not exist, say that directly.
- If staging fails because the file is too large, say that directly.
- If staging fails because the file is occupied, say that directly.
- If sending succeeds but cleanup fails, say that the file was sent but the staged cleanup failed.
- Never say or imply that the original file was deleted.

## Examples

### Example 1: Desktop PDF

User asks: send `C:\Users\name\Desktop\resume.pdf` to QQ

Action:

1. Run:
   - `python scripts/stage_media.py "C:\Users\name\Desktop\resume.pdf"`

2. Suppose the script returns:
   - `C:\Users\name\.openclaw\media\qqbot\abc123.pdf`

3. Send:
   - `<qqmedia>C:\Users\name\.openclaw\media\qqbot\abc123.pdf</qqmedia>`

4. After the send attempt finishes, run:
   - `python scripts/stage_media.py --cleanup "C:\Users\name\.openclaw\media\qqbot\abc123.pdf"`

Never delete:

- `C:\Users\name\Desktop\resume.pdf`

### Example 2: File already under QQ media relay directory

User asks to send:

- `C:\Users\name\.openclaw\media\qqbot\old-file.pdf`

Action:

1. Still stage it first:
   - `python scripts/stage_media.py "C:\Users\name\.openclaw\media\qqbot\old-file.pdf"`

2. Suppose the script returns:
   - `C:\Users\name\.openclaw\media\qqbot\new-uuid.pdf`

3. Send:
   - `<qqmedia>C:\Users\name\.openclaw\media\qqbot\new-uuid.pdf</qqmedia>`

4. Cleanup only:
   - `python scripts/stage_media.py --cleanup "C:\Users\name\.openclaw\media\qqbot\new-uuid.pdf"`

Never delete:

- `C:\Users\name\.openclaw\media\qqbot\old-file.pdf`

### Example 3: URL image

User asks to send:

- `https://example.com/image.png`

Action:

1. Send directly:
   - `<qqmedia>https://example.com/image.png</qqmedia>`

2. Do not stage.
3. Do not cleanup.

## Notes

- Prefer completing the send in one turn.
- Use the bundled staging script whenever the source is local.
- Use `<qqmedia>...</qqmedia>` for final delivery.
- For local files, cleanup must happen after the send attempt using only the captured staged path.
- The cleanup step exists only to delete the temporary staged copy, never the original user file.