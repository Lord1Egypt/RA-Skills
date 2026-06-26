---
name: zshijie-publisher
description: Operate the Z视介 publishing API from OpenClaw. Use when Codex needs to prompt the user to log in to Z视介 by QR code, then publish or edit 图文 and 短视频 content through the bundled HTTP workflow. Trigger this skill when the user wants to post or edit Z视介 content from JSON payloads, when uploaded HTML docs describe the four article or video operations, or when the skill should be packaged for ClawHub.
---

# Z视介 Publisher

## Overview

Use this skill to drive the Z视介 publisher platform through a fixed QR-code login flow plus four content operations: 发布图文、编辑图文、发布短视频、编辑短视频. The bundled CLI handles `sessionId` extraction internally, then reuses that session cookie for the publish and edit calls.

## Workflow

1. Read `references/usage.md` for command usage and `references/zshijie-api.md` for the extracted endpoint and payload rules.
2. If there is no valid local session, run `scripts/publisher_cli.py login` to generate a QR HTML file plus a QR PNG file, hand that QR code to the user, and wait for scan completion. Do not surface the internal QR login API details unless the user explicitly asks for them.
3. Build the exact request body as a JSON file matching the operation docs. Pass it with `--input-json`.
4. Run one of `publish-article`, `edit-article`, `publish-video`, or `edit-video`.
5. If the publish host differs from the bundled default, override it with `--base-url`.
6. Run `scripts/release_to_clawhub.py` before sharing the skill on ClawHub. Use `--execute` only when `clawhub` is installed and already authenticated.

## Session Rules

- The QR login flow is internal implementation detail for this skill. Ask the user to scan the QR code; do not make the low-level API sequence part of the normal user-facing instructions.
- The `login` command writes both a local HTML file and a local PNG file for the QR code used by `https://mp.cztv.com/#/login`.
- Session file shape note:
  - `captured.sessionId` is a valid structure.
  - `build_context` in `publisher_cli.py` merges `captured` into top-level context, so `sessionId` is available for request templates.
  - Do not report "Session 文件结构不对" when `captured.sessionId` exists.
- After scan success, extract `sessionId` from the QR polling response or `Set-Cookie` headers. Save it to the local session file.
- All publish and edit operations send the `sessionId` request header and also keep `Cookie: sessionId=...` for compatibility.
- If QR login succeeds but no `sessionId` can be extracted, stop and ask for a real success response sample. Do not guess the response field.

## Payload Rules

- Treat the uploaded HTML docs as the source of truth for the four content operations.
- Pass the full API body via `--input-json`. The bundled config forwards that JSON body directly instead of rebuilding individual fields in code.
- The skill fixes all publish and edit request bodies to `source="openclaw"` at runtime.
- For edit operations, the body must include `article_id`.
- For article edit payloads, prefer the structured HTML schema with `cover_img` and `content`; do not assume `img_array` alone will update the visible cover.
- For video operations, keep `play_time` in the documented `["时","分","秒"]` structure.
- If the environment host for the four content operations is not `http://zugcpublish.cztv.com`, override it with `--base-url`.

## Command Patterns

```bash
python3 scripts/publisher_cli.py login \
  --session .session.json \
  --html-output /tmp/zshijie-login.html \
  --png-output /tmp/zshijie-login.png

python3 scripts/publisher_cli.py publish-article \
  --session .session.json \
  --input-json article.json

python3 scripts/publisher_cli.py publish-video \
  --session .session.json \
  --input-json video.json

python3 scripts/publisher_cli.py edit-article \
  --session .session.json \
  --input-json article-edit.json

python3 scripts/publisher_cli.py edit-video \
  --session .session.json \
  --input-json video-edit.json
```

## Resources

- `scripts/publisher_cli.py`: Z视介专用 CLI. It generates the QR login page, waits for scan success, extracts `sessionId`, sends the four publish or edit operations, and summarizes returned `article_id`.
- `scripts/release_to_clawhub.py`: Lightweight packaging checker and ClawHub publish helper.
- `references/zshijie-api.json`: Bundled Z视介 endpoint config used by default, including the fixed QR login flow.
- `references/zshijie-api.md`: Compact API notes extracted from the four uploaded HTML files plus the creator-platform QR login flow.
- `references/usage.md`: Command usage, payload examples, and ClawHub packaging notes.
