---
name: vibevideoio-ai-script-to-video
description: Log into bollo.video or vibevideo.io, list Studio projects with web links, create a Studio episode from a script with style/aspect-ratio/project selection, and log out. Use when users ask to make or create an AI video, 创作视频, 生成视频, paste a script and ask to turn it into a video, make a video from a script, or explicitly ask for Studio login/project actions.
metadata: { "openclaw": { "emoji": "🎬", "requires": { "bins": ["node"] } } }
---

# VibeVideoIO AI Script to Video

Use this skill when the user wants OpenClaw to operate VibeVideo Studio directly instead of only generating storyboard text.

## Invocation Rules

- Route here when the user asks to create/make/generate a video, especially:
  - "帮我创作一个视频"
  - "帮我生成一个视频"
  - "make a video for me"
  - "create an AI video from this script"
  - "turn this story into a video"
  - "把这个剧本做成 AI 视频"
  - "我现在有个剧本，想把它做成 AI 视频"
  - when the user pastes a screenplay or short-video script and asks you to make it into a video
- The user does not need to mention `bollo.video`, `vibevideo.io`, or the skill name explicitly.

## Commands

Run the CLI directly from the skill folder:

```bash
node {baseDir}/scripts/vibevideo-studio.mjs login
node {baseDir}/scripts/vibevideo-studio.mjs projects
node {baseDir}/scripts/vibevideo-studio.mjs create-episode --text "..."
node {baseDir}/scripts/vibevideo-studio.mjs logout
```

Optional local registration is manual:

```bash
npm --prefix {packageRoot} run openclaw:register
```

## Login Rules

- Select the site automatically from the user's language unless they explicitly request a specific site:
  - Chinese user input → `bollo.video`
  - English user input → `vibevideo.io`
- Only ask which site to use if the user explicitly wants a different site or the language signal is mixed/ambiguous.
- After login, keep all subsequent operations on the same site family:
  - if the session is for `vibevideo.io`, use `vibevideo.io` web pages and `vibevideo.io` API endpoints for project listing, episode creation, and logout
  - if the session is for `bollo.video`, use `bollo.video` web pages and `bollo.video` API endpoints for project listing, episode creation, and logout
- Never mix `vibevideo.io` URLs/APIs with a `bollo.video` session, and never mix `bollo.video` URLs/APIs with a `vibevideo.io` session.
- Ask for:
  - owner email
  - sub-user email (optional)
- Fetch the CAPTCHA only once per login attempt. After the first `login` returns `kind=login-captcha-required`, reuse that pending CAPTCHA and wait for the user's reply. Do not run bare `login` again to request a fresh CAPTCHA unless the user says the image is unreadable, the CAPTCHA expires, or the backend rejects the entered CAPTCHA and requires a retry.
- In an OpenClaw conversation, the CLI will fetch CAPTCHA, save it under `~/.openclaw/media/vibevideo-studio-captcha/`, and return it through OpenClaw's `MEDIA:` protocol so the current conversation can preview it inline.
- The CLI does not spawn `openclaw message send` or auto-push outbound IM messages. If a client requires explicit media delivery, use the host conversation's message tool with `captcha_file`.
- In non-interactive OpenClaw runs, use the CLI's emitted `MEDIA:` line directly. Do not replace it with `captcha_file` or any absolute `/Users/...` path in your assistant reply.
- On Feishu, do not answer with raw `MEDIA:data:...`, `image:`, or base64 text. Use this flow instead:
  1. run `node {baseDir}/scripts/vibevideo-studio.mjs login --json --no-inline-media ...`
  2. if the result is `kind=login-captcha-required`, read `data.captcha_file`
  3. call the OpenClaw `message` tool with `action="send"`, put your short caption in `message`, set `path` or `filePath` to `captcha_file`, and omit `target` so it goes to the current conversation
  4. after the `message` tool succeeds, reply only with `NO_REPLY`
- If the current client is not Feishu and you have a local desktop session, do not paste raw `MEDIA:data:...`, `image:`, or base64 text. Instead, open `captcha_file` locally with a system preview command so the human can read it directly:
  1. macOS: `open <captcha_file>`
  2. Linux: `xdg-open <captcha_file>`
  3. Windows: `start \"\" <captcha_file>`
  4. then ask the user to read the CAPTCHA characters from the preview and reply with them
- Never attempt OCR or visual recognition on the CAPTCHA. Do not guess the characters. Do not paraphrase the image contents. Send the raw image to the current IM conversation and wait for the human user to reply with the CAPTCHA text.
- Use `buffer` only if you truly must send a `data:image/...` payload; prefer `path`/`filePath` from `captcha_file`.
- Never infer a fallback delivery target from some other OpenClaw session. If the current session key is unavailable, do not auto-send the CAPTCHA to Feishu, webchat, or any other conversation.
- If the first `login` run returns `kind=login-captcha-required`, ask the user to reply with the CAPTCHA characters, then run:

```bash
node {baseDir}/scripts/vibevideo-studio.mjs login --captcha-text "USER_CAPTCHA"
```

- If the next `login` run returns `kind=login-email-code-required`, ask the user to reply with the email verification code, then run:

```bash
node {baseDir}/scripts/vibevideo-studio.mjs login --verification-code "123456"
```

- The CLI persists pending login state between those turns, so do not ask the user to repeat site/email unless they want to restart the flow.
- The issued token is saved to a local OpenClaw session file by default; pass `--no-save` if you need an ephemeral login.
- If login returns an error, surface the exact CLI/API error first. Do not silently restart the login flow. Only fetch a fresh CAPTCHA when the user explicitly wants to retry or the error clearly says the previous CAPTCHA expired/was incorrect.

## Create Episode Rules

When turning a script into a Studio episode, ask for:

1. style mode
   - `AI recommend realistic`
   - `AI recommend animation`
   - `manual style`
2. aspect ratio
3. target project
   - allow blank selection for unclassified

Then run:

```bash
node {baseDir}/scripts/vibevideo-studio.mjs create-episode \
  --text "USER_SCRIPT" \
  --title "OPTIONAL_TITLE" \
  --style-mode auto-realistic \
  --aspect-ratio 16:9
```

For manual style:

```bash
node {baseDir}/scripts/vibevideo-studio.mjs create-episode \
  --text "USER_SCRIPT" \
  --style-mode manual \
  --style "cinematic watercolor realism"
```

If the script is long, prefer stdin or `--file`:

```bash
cat /tmp/script.txt | node {baseDir}/scripts/vibevideo-studio.mjs create-episode --style-mode auto-anime
node {baseDir}/scripts/vibevideo-studio.mjs create-episode --file /tmp/script.txt --project-id proj_123
```

## Error And Retry Rules

- If `create-episode` fails with `fetch failed`, timeout, HTTP/API errors, TLS/network errors, or any non-zero `error_code`, return that failure result directly to the user
- When `create-episode` fails, still show any known generation context in the failure response, including `video_id`, `title`, `aspect_ratio`, `style_mode`, `project`, and related URLs when available
- Do not automatically retry `create-episode`
- Do not silently switch from `bollo.video` to `vibevideo.io`, or from `vibevideo.io` to `bollo.video`, after a failure
- Do not silently modify the script, title, style mode, style prompt, aspect ratio, or project selection to force another attempt
- If the CLI returned JSON, pass through the JSON error result; if it returned plain stderr text, summarize it faithfully and include the key error text
- After returning the failure, ask the user whether they want to retry manually, change inputs, or stop

## Expected Results

- `projects` returns every Studio project with a direct project page URL
- `create-episode` returns:
  - `video_id`
  - selected project metadata when available
  - Studio project URL when available
  - direct Studio episode URL after polling succeeds
- `logout` clears the saved session and best-effort revokes the current token remotely
