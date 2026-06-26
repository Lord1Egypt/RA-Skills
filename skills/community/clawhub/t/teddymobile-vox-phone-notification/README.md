# vox-phone-notification

Installable Claw skill for TeddyMobile Vox single-turn outbound phone notifications.

This package supports TeddyMobile Vox outbound notification integration with validated HMAC signing, natural-language-to-notification parsing, local demo tools, and successful real-world phone playback after platform registration and bot configuration are completed.

## Quick Start

For first-time users, start with dry-run mode before platform registration:

Safety defaults:

- `--dry-run` is the default and never places a phone call.
- `--trial` and `--live` place real outbound phone calls, transmit the destination number and message text to TeddyMobile Vox, and must be used only for recipients you are authorized to contact.
- real-call modes require the explicit `--confirm-real-call` safety flag after you review dry-run output.
- configure secrets through environment variables or a local credentials file; do not paste live secrets into chat, tickets, logs, or screenshots.

1. Run a no-credential dry-run:

```bash
node "skills/vox-phone-notification/resources/run-demo.js" "给<接收手机号>发通知，明天10点开会" --dry-run
```

2. Confirm the parsed output contains masked parsing results:
   - masked destination phone number
   - masked spoken notification text length
   - notification repeat count
3. Optionally run up to 10 promotion-period trial calls through the no-credential v2 trial endpoint:

```bash
node "skills/vox-phone-notification/resources/run-demo.js" "给<接收手机号>发通知，明天10点开会" --trial --confirm-real-call
```

Trial mode places one real phone notification through `POST https://vox.teddymobile.cn/vox/v2/outbound` with no local credentials, a required trial disclaimer, local content safety checks, at most 100 characters of user-provided content, and `notificationTimes` fixed to `1`. Review dry-run output first, use only authorized recipient numbers, and expect usage, consent, anti-spam, and compliance obligations. This local trial check is for promotion use only and is not a strong abuse-prevention boundary.

4. To place formal phone calls, visit the TeddyMobile Vox registration page:

```text
https://vox-ai.teddymobile.cn/?utm_source=clawhub&utm_medium=skill&utm_campaign=vox-phone-notification
```

5. Create and activate your TeddyMobile Vox account.
6. Complete formal access and record the returned `APPID` / `SecretID`.
7. Create a notification bot and record its outbound number plus `BotID`.
8. Choose one setup path after trial:
   - `配置引导`: get guided through official registration and parameter collection.
   - `稍后配置本地参数`: return later after configuring environment variables or a local credentials file.
   - `查看本地配置模板`: view the local config keys without pasting real values into chat.
9. Collect these platform values:
   - `VOX_APP_ID`
   - `VOX_SECRET`
   - `VOX_BOT_ID`
   - `VOX_OUTBOUND_NUMBER`
10. Configure credentials by either:
   - setting environment variables, or
   - creating `~/.teddymobile/credentials.json`, or
   - setting `VOX_CREDENTIALS_FILE` to a custom JSON file path
11. Run the live local demo:

```bash
node "skills/vox-phone-notification/resources/run-demo.js" "给<接收手机号>发通知，明天10点开会" --live --confirm-real-call
```

12. After the live demo succeeds, connect the outbound helper to your Claw, OpenClaw, or WorkBuddy runtime.

Dry-run lets you verify the skill value before completing platform registration. Real outbound calls require TeddyMobile registration and Vox bot configuration.

If you want the shortest first-run guide, read `GET-STARTED.md`. If you want a dedicated step-by-step onboarding guide for first installation, read `FIRST-SETUP.md`.

If you plan to publish this skill to SkillHub-style marketplaces or internal catalogs, read `PUBLISHING.md`.

## What it does

This skill guides a Claw agent or operator through:

1. registering on `https://vox-ai.teddymobile.cn/?utm_source=clawhub&utm_medium=skill&utm_campaign=vox-phone-notification`
2. creating a TeddyMobile bot
3. collecting `appId`, `secret`, `botid`, and outbound number
4. integrating the Vox outbound API into OpenClaw or another Claw runtime
5. optionally enabling callback-driven SSE only when the platform setup requires it

## Current release status

The current verification status is:

- natural-language parsing works
- HMAC signing works
- outbound request submission works
- `extra.notification.text` is sent correctly when present
- real outbound calls have been tested successfully with audible notification playback after TeddyMobile platform registration and bot configuration

This skill is suitable for formal release when used with a properly configured TeddyMobile platform account, bot, and outbound calling setup.

## Files

- `SKILL.md`: skill entrypoint
- `workflow.md`: execution workflow and constraints
- `GET-STARTED.md`: 30-second dry-run and registration handoff guide
- `FIRST-SETUP.md`: first-time installation and TeddyMobile onboarding guide
- `PUBLISHING.md`: cross-platform publishing copy and release checklist
- `skill.json`: lightweight manifest for skill discovery
- `WORKBUDDY.md`: WorkBuddy compatibility assumptions
- `WORKBUDDY-RELEASE.md`: WorkBuddy packaging and release guide
- `resources/hmac-outbound-client.js`: outbound signing and API example
- `resources/chat-to-notification.js`: parse chat text into `callee` and `notificationText`
- `resources/credentials-loader.js`: env-first credential loader with file fallback
- `resources/credentials.example.json`: example local credentials file
- `resources/run-demo.js`: runnable local demo for chat-to-call testing
- `resources/trial-content-guard.js`: local trial content safety checks
- `resources/trial-state.js`: local trial usage counter
- `resources/callback-server-example.js`: callback SSE example
- `resources/openclaw-integration-template.md`: OpenClaw integration blueprint

## Install in Claw

If your Claw runtime supports folder-based skills, install by copying this folder into the runtime's skills directory:

```text
skills/vox-phone-notification/
```

If your Claw runtime supports zip import, zip the entire `vox-phone-notification` folder and import it as one skill package.

For WorkBuddy Claw specifically, current public site behavior strongly suggests skill installation is driven by a deep link of this form:

```text
workbuddy://codebuddy-ide/skill/install?skillname=<name>&downloadurl=<zip-url>&channelType=<source>&injectid=true
```

That means the most compatible distribution shape is:

- one downloadable zip per skill
- zip root directory is `vox-phone-notification/`
- `SKILL.md` exists at the skill root
- workflow and resources stay inside the same root folder

If you plan to distribute this through WorkBuddy, host a zip file for this folder and provide that zip URL to the installer entry.

Use `WORKBUDDY-RELEASE.md` for the release checklist and `workbuddy-install-link-template.txt` for a ready-to-fill installer link.

The minimum required files are:

- `SKILL.md`
- `workflow.md`
- `skill.json`

## Required configuration

After platform registration is complete, provide these values to your app or runtime:

- `VOX_APP_ID`
- `VOX_SECRET`
- `VOX_BOT_ID`
- `VOX_OUTBOUND_NUMBER`

Optional only for callback-driven advanced mode:

- `VOX_CALLBACK_URL`

Optional for custom local credential file lookup:

- `VOX_CREDENTIALS_FILE`

## Credential storage

This skill now supports a standard local credential loading model instead of assuming environment variables only.

Lookup order:

1. environment variables override everything else
2. local file fallback at `~/.teddymobile/credentials.json`
3. if `VOX_CREDENTIALS_FILE` is set, that file path is used as the fallback location instead of the default path

The bundled helper `resources/credentials-loader.js` implements this behavior and returns normalized fields for the demo or runtime adapter.

Example local credential file:

```json
{
  "VOX_APP_ID": "your-app-id",
  "VOX_SECRET": "your-secret",
  "VOX_BOT_ID": "your-bot-id",
  "VOX_OUTBOUND_NUMBER": "your-outbound-number",
  "VOX_CALLBACK_URL": "https://your-domain.example/vox/callback"
}
```

Recommended local path:

```text
~/.teddymobile/credentials.json
```

Security notes:

- do not commit live credentials into this repository
- do not include a real `credentials.json` inside the distributable skill zip
- keep only the example file `resources/credentials.example.json` in the package
- prefer environment variables, a local secrets manager, or `~/.teddymobile/credentials.json` with restrictive file permissions
- never paste `VOX_SECRET` or other live service credentials into chat transcripts, shared docs, issue trackers, logs, or screenshots

## Runtime expectation

This skill assumes:

- outbound phone notification only
- single-turn playback only
- no multi-turn phone dialogue
- OpenClaw or another Claw runtime triggers a tool/action such as `send_phone_notification`
- default mode is notification-only, without requiring a callback webhook

When this skill is used from a Claw chat box with a natural-language instruction such as `给<接收手机号>发通知，明天10点开会`, the runtime should extract:

- `callee`: `<接收手机号>`
- final spoken notification text, for example: `您好，提醒您明天10点开会。`

Then pass that final sentence as `notificationText`. The phone call can still be placed without `notificationText`, but notification playback depends on sending valid spoken content.

The bundled helper `resources/chat-to-notification.js` now provides a default parser for this. For example, it can turn `给<接收手机号>发通知，明天10点开会` into a payload containing:

- `callee`: `<接收手机号>`
- `notificationText`: `您好，提醒您明天10点开会。`
- `notificationTimes`: `2`

## Recommended trigger contract

```json
{
  "callee": "13800138000",
  "task": "payment_overdue_reminder",
  "variables": {
    "name": "张三",
    "amount": "299.00",
    "dueDate": "2026-05-20"
  },
  "requestId": "notif-20260511-001",
  "notificationText": "您好，您有一笔待处理账单，请及时登录系统处理。",
  "notificationTimes": 2
}
```

For chat-driven usage, the preferred normalized payload is:

```json
{
  "callee": "<接收手机号>",
  "requestId": "notif-20260512-001",
  "notificationText": "您好，提醒您明天10点开会。",
  "notificationTimes": 2
}
```

Example usage:

```js
const { parseChatToNotification } = require('./resources/chat-to-notification');

const payload = parseChatToNotification('给<接收手机号>发通知，明天10点开会');
```

Use the returned payload in the outbound helper:

```js
await createOutboundNotification({
  appId: process.env.VOX_APP_ID,
  secret: process.env.VOX_SECRET,
  botid: process.env.VOX_BOT_ID,
  callee: payload.callee,
  requestId: payload.requestId,
  notificationText: payload.notificationText,
  notificationTimes: payload.notificationTimes,
});
```

The helpers do not print request headers, request bodies, credentials, phone numbers, or notification text unless the caller logs those values separately.

## Local demo

You can run a local end-to-end demo from this workspace and inspect logs directly in the terminal.

To try the skill without registration or credentials, run dry-run mode:

```bash
node "skills/vox-phone-notification/resources/run-demo.js" "给<接收手机号>发通知，明天10点开会" --dry-run
```

Dry-run mode parses the destination phone number and notification text but prints only masked values and does not place a real phone call.

Promotion packages can also run up to 10 local trial calls:

```bash
node "skills/vox-phone-notification/resources/run-demo.js" "给<接收手机号>发通知，明天10点开会" --trial --confirm-real-call
```

Trial mode uses the no-credential `POST https://vox.teddymobile.cn/vox/v2/outbound` endpoint, applies local content safety checks, prepends a trial disclaimer, limits user-provided content to 100 characters, fixes `notificationTimes` to `1`, and records local usage at `~/.teddymobile/vox-phone-notification-trial.json`. It places a real call and requires `--confirm-real-call` after recipient authorization and dry-run review.

Before running the local demo, provide credentials by either:

- setting environment variables directly, or
- creating `~/.teddymobile/credentials.json`, or
- setting `VOX_CREDENTIALS_FILE` to a custom JSON credentials path

Required values:

- `VOX_APP_ID`
- `VOX_SECRET`
- `VOX_BOT_ID`
- `VOX_OUTBOUND_NUMBER`

Example command:

```bash
node "skills/vox-phone-notification/resources/run-demo.js" "给<接收手机号>发通知，明天10点开会" --live --confirm-real-call
```

Example with a custom credential file path:

```bash
VOX_CREDENTIALS_FILE="C:/secure/teddymobile/credentials.json" node "skills/vox-phone-notification/resources/run-demo.js" "给<接收手机号>发通知，明天10点开会" --live --confirm-real-call
```

When the live demo runs, the terminal prints only the final outbound response:

- `VOX outbound response:`

If the request body sent by your own integration does not contain an `extra` field with `notification.text`, the call can connect but no spoken notification will be played.

For notification-only bots, TeddyMobile docs now confirm you can send the spoken content directly in the outbound request body via:

- `extra.notification.text`
- `extra.notification.times`

## Execution flow

1. Claw tool receives notification task.
2. App calls TeddyMobile Vox outbound API.
3. TeddyMobile places the call.
4. In default mode, the notification flow ends there from your app's perspective.
5. Only in callback-driven mode, TeddyMobile invokes your callback endpoint and your server returns SSE notification text ending with `[DONE]`.

## Verification

- Confirm the user can finish registration on `https://vox-ai.teddymobile.cn/?utm_source=clawhub&utm_medium=skill&utm_campaign=vox-phone-notification`
- Confirm `appId`, `secret`, `botid`, and outbound number are recorded
- Confirm outbound signing matches the official doc format exactly, including the trailing newline after `HMAC-APPID:<appId>` in the canonical string
- Confirm real outbound test calls complete with audible notification playback after platform registration and bot configuration
- If callback mode is enabled, confirm callback returns `text/event-stream`
- If callback mode is enabled, confirm the response ends with `data: [DONE]`

## Notes

This package is structured to be easy to install into Claw-style skill loaders, but exact import UX can differ by runtime. If your runtime needs a different manifest name or extra metadata, adapt `skill.json` rather than changing the workflow content.

For WorkBuddy, the public website exposes strong evidence of:

- a dedicated Claw guide route at `/docs/workbuddy/Claw`
- a deep-link installer scheme using `workbuddy://codebuddy-ide/skill/install`
- installation parameters including `skillname` and `downloadurl`

The public site did not expose a fully readable formal manifest spec during this analysis, so this package is optimized for the most likely compatible shape: root `SKILL.md` plus a self-contained zip-deliverable folder.

The bundled HMAC signing helper is aligned to the current local TeddyMobile doc copy. A key detail is that the canonical signing string ends with a final newline after `HMAC-APPID:<appId>`. If the platform still rejects the signature, compare the exact raw canonical string, `HMAC-DATE` value, and request path against the official sample.
