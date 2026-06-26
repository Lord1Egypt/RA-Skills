---
title: Vox Phone Notification Skill Workflow
---

# Vox Phone Notification Skill Workflow

Use this skill when the user wants a Claw-based agent to try or place single-turn outbound phone notification calls through TeddyMobile Vox. For first-time use, always start with no-credential dry-run parsing, then offer up to 10 promotion trial calls, then guide formal TeddyMobile registration and live integration.

## Goal

Implement or guide the smallest complete onboarding and integration path that lets a Claw runtime do this:

1. Run a no-credential dry-run to parse the user's natural-language phone notification request.
2. If dry-run succeeds, ask the user to choose either one promotion `--trial` call or formal TeddyMobile registration. Trial and live calls require explicit real-call confirmation.
3. Run `--trial` only if the user chooses trial, or guide the user to register on `https://vox-ai.teddymobile.cn/?utm_source=clawhub&utm_medium=skill&utm_campaign=vox-phone-notification` if they choose formal ongoing use.
4. Run formal live mode only with an explicit `--live` flag after the user says TeddyMobile registration is complete.
5. Instruct the user to configure the returned `appId`, `secret`, `botid`, and outbound number through environment variables, a local secrets manager, or a local credentials file only after the user chooses formal live mode. Do not ask the user to paste live secrets into chat.
5. Accept a business-side "send notification" trigger from the agent or app.
6. Call TeddyMobile Vox outbound API with the registered `botid`.
7. Complete the phone notification in notification-only mode by default.
8. Only use callback-driven SSE response flow if the platform setup explicitly requires it.

This skill is specifically for phone notification scenarios, not generic chat-only bot integration, and it assumes the notification does not require multi-turn follow-up.

## What This Skill Should Help Build

The first-use flow must contain these default parts:

1. A dry-run parsing step that does not read credentials, does not place a call, and prints only masked phone/content values.
2. A two-option choice after successful dry-run:
   - `试用真实电话`: run promotion `--trial --confirm-real-call` through the no-credential v2 trial endpoint after dry-run preview and recipient authorization, local content safety checks, a trial disclaimer, `notificationTimes` fixed to `1`, and a local trial usage counter.
   - `正式注册并配置`: guide formal TeddyMobile platform registration and live credential setup.
3. A registration handoff step for formal TeddyMobile platform use after trial completion or when the user chooses registration.

The formal live implementation usually contains these parts:

1. A registration guidance step for the TeddyMobile platform.
2. A config layer for `appId`, `secret`, `botid`, and outbound number.
3. A formal outbound call client that signs and sends `POST /vox/v1/outbound`.

Optional advanced parts:

4. A Vox callback endpoint that accepts `POST` JSON and returns `text/event-stream`.
5. A thin adapter between Vox callback data and OpenClaw or another Claw runtime.

This skill package should remain self-contained so a Claw runtime can install it by folder copy or zip import.

Credential handling in formal live mode should follow this order:

1. read `VOX_APP_ID`, `VOX_SECRET`, `VOX_BOT_ID`, `VOX_OUTBOUND_NUMBER`, and optional `VOX_CALLBACK_URL` from environment variables
2. if any required values are still missing, fall back to `~/.teddymobile/credentials.json`
3. if `VOX_CREDENTIALS_FILE` is set, use that file path instead of the default fallback path

Do not ask for or load user-owned live credentials during dry-run or promotion trial. Promotion trial uses the no-credential `POST https://vox.teddymobile.cn/vox/v2/outbound` endpoint; formal live mode uses user-owned credentials. The bundled `resources/credentials.example.json` is an example only.

Do not collect live `APPID`, `SecretID`, `BotID`, outbound numbers, or `VOX_SECRET` through conversational chat. Give local setup instructions and ask the user to confirm when values have been configured locally.

## Platform Assumptions

Base the implementation on the currently known TeddyMobile Vox protocol facts already captured in this repository:

- The user manually completes enterprise onboarding and bot registration in the TeddyMobile platform.
- The platform issues `appId` and `secret`.
- The registered bot has a `botid`.
- The registration result for this use case also includes an outbound number for call display/capability confirmation.
- Trial outbound calls use no-credential `POST https://vox.teddymobile.cn/vox/v2/outbound`.
- Formal live outbound calls use signed `POST https://vox.teddymobile.cn/vox/v1/outbound`.
- Outbound requests require HMAC headers: `HMAC-APPID`, `HMAC-DATE`, `HMAC-SIGNATURE`, `HMAC-ALGORITHM`, `HMAC-SIGNED-HEADERS`.
- The official local doc copy confirms the canonical string order is `METHOD`, `PATH`, sorted `uriParams`, `appId`, `dateGMT`, `HMAC-APPID:<appId>`, with a final trailing newline.

Only for callback-driven advanced mode:

- Vox callback requests use `POST` with JSON body.
- Callback responses must use `text/event-stream`.
- Each SSE chunk is emitted as `data: {json}` and the stream ends with `data: [DONE]`.
- Known callback fields include `turn`, `calltype`, `callee`, `caller`, `callid`, `requestid`, `message`.

Do not invent undocumented fields. If the repository later contains newer platform docs, follow those instead.

## Required Inputs

Infer what exists in the repo first. Only ask if blocked.

For first-time use, do not collect formal live credentials. Use dry-run first, then ask the user to choose trial or formal registration.

Collect or confirm these values only when the user explicitly chooses formal live mode or says registration is already complete:

- `VOX_APP_ID`
- `VOX_SECRET`
- `VOX_BOT_ID`
- `VOX_OUTBOUND_NUMBER`
- optional local credentials file at `~/.teddymobile/credentials.json`
- notification target phone number source
- where in the Claw runtime the "send notification" action should be triggered

Only for callback-driven advanced mode:

- `VOX_CALLBACK_URL`

Optional credential file override:

- `VOX_CREDENTIALS_FILE`

Do not ask whether multi-turn follow-up is needed for this skill. Assume single-turn notification only unless the user explicitly asks to expand scope.

If formal live credentials are missing, do not block first-time usage. Run dry-run and then ask whether the user wants trial or formal registration. Ask for missing credentials only after the user chooses formal live mode.

## Execution Rules

1. If the user asks to execute, try, test, use this skill, or send a phone notification without explicitly requesting formal live mode, start with `--dry-run` only after the destination phone number and notification content are both available.
2. If the user has not provided a destination phone number, ask them to fill in the phone number to notify before running dry-run, trial, or live mode.
3. If the user has not provided notification content, ask them to fill in the spoken notification content before running dry-run, trial, or live mode.
4. Do not use documentation sample phone numbers or sample notification text as substitutes for missing user input.
5. After dry-run succeeds, present exactly two next-step choices and wait for the user's choice:
   - `试用真实电话`: run `--trial --confirm-real-call` for one promotion phone call, up to 10 total local trials, only after dry-run preview and recipient authorization.
   - `正式注册并配置`: guide TeddyMobile registration and live credential setup.
6. Do not run `--trial` until the user chooses trial and adds `--confirm-real-call` after reviewing the masked dry-run preview and confirming recipient authorization. Do not ask for formal credentials until the user chooses formal registration or says they already configured credentials locally.
7. If `--trial` is blocked because the local trial was already used or content safety rejects the content, report the block reason and continue to formal registration guidance.
8. Do not call `resources/credentials-loader.js`, inspect `~/.teddymobile/credentials.json`, or ask for `VOX_APP_ID` / `VOX_SECRET` / `VOX_BOT_ID` / `VOX_OUTBOUND_NUMBER` before dry-run and the user's next-step choice.
9. If a command is run without `--dry-run`, `--trial`, or `--live`, treat it as dry-run. Never use an unflagged command as formal live mode.
9a. If a command uses `--trial` or `--live` without `--confirm-real-call`, stop before any network call, show the masked real-call preview, and tell the user to re-run with `--confirm-real-call` only after authorization and compliance checks.
10. If `--trial` succeeds, the final assistant response must restate the formal setup choices from `POST-TRIAL-GUIDE.md`. Do not rely on tool output alone because host UIs may collapse or summarize it.
11. Inspect the repo and identify the user's actual runtime before proposing formal architecture.
12. Prefer integrating into the existing backend and agent abstraction.
13. If the user has not completed registration and wants formal ongoing use, guide them to `https://vox-ai.teddymobile.cn/?utm_source=clawhub&utm_medium=skill&utm_campaign=vox-phone-notification` to finish onboarding and bot creation.
14. If the user mentions OpenClaw, assume the skill should wrap an existing tool/action hook rather than replace the runtime.
15. Model the phone call as an external side effect triggered by the agent, not as a primary chat transport.
16. Keep the business contract small: one function or tool like `sendPhoneNotification(...)` is preferred.
17. Treat the notification as single-turn playback; do not design multi-turn dialog state unless the user explicitly requests it.
18. Default to notification-only implementation. Do not require callback handling unless the user's platform setup explicitly needs it.
19. Separate outbound call initiation from optional callback response generation.
20. For callback-driven mode SSE responses:
   - Set `Content-Type: text/event-stream`.
   - Emit only valid `data:` frames.
   - End successful streams with `[DONE]`.
21. For HMAC signing:
    - Use GMT date.
    - Normalize the path.
    - Sort URI params before signing.
    - Include the final trailing newline shown in the official sample.
    - If the platform rejects the signature, compare the raw canonical string, clock sync, and exact request path before changing the algorithm.

## Registration Guidance

When the user has not yet onboarded, first collect the destination phone number and notification content if either is missing, then run dry-run and ask whether they want up to 10 promotion trial calls or formal registration. If they choose formal registration, make the registration URL visually prominent and instruct them to go to `https://vox-ai.teddymobile.cn/?utm_source=clawhub&utm_medium=skill&utm_campaign=vox-phone-notification` and complete:

1. Visit the TeddyMobile Vox website.
2. Create and activate the account.
3. Complete formal access and record the returned `APPID` / `SecretID`.
4. Create a notification bot.
5. Record the bot outbound number and `BotID`.
6. Map these values into local config: `VOX_APP_ID`, `VOX_SECRET`, `VOX_BOT_ID`, and `VOX_OUTBOUND_NUMBER`.
7. Only if the platform setup requires runtime callback generation, configure the callback URL.

After showing the registration URL and overview, present exactly these three setup choices:

1. `配置引导`: guide the user through official-site registration, formal access, notification bot creation, and list the values to record.
2. `稍后配置本地参数`: let the user leave and return later after configuring environment variables, a local secrets manager, or `~/.teddymobile/credentials.json`.
3. `查看本地配置模板`: provide this local template for the user's own machine without asking them to paste real values into chat:

```text
VOX_APP_ID =
VOX_SECRET =
VOX_BOT_ID =
VOX_OUTBOUND_NUMBER =
```

Do not ask the user to paste secret values into chat. Use business labels first, then map them to local config names for local setup.

If the user says registration is already done, move directly to integration and ask only for the returned values if needed.

## Recommended Implementation Shape

### A. Notification Trigger Contract

Prefer a single internal tool contract such as:

```json
{
  "callee": "13800138000",
  "task": "payment_overdue_reminder",
  "variables": {
    "name": "张三",
    "amount": "299.00",
    "dueDate": "2026-05-20"
  },
  "requestId": "notif-20260511-001"
}
```

The Claw runtime can invoke this contract from a tool, workflow node, API handler, or scheduled task.

Because this skill is single-turn only, the `task` and `variables` should be enough to render one final spoken message without follow-up questioning.

If the skill is triggered from a chat box with natural language like `给<接收手机号>发通知，明天10点开会`, the runtime should normalize it before outbound dispatch:

```json
{
  "callee": "<接收手机号>",
  "requestId": "notif-20260512-001",
  "notificationText": "您好，提醒您明天10点开会。",
  "notificationTimes": 2
}
```

Use the bundled helper `./resources/chat-to-notification.js` when the runtime needs a default parser for Chinese chat instructions.

For natural-language usage, do not send a phone notification request until both of these are available:

- the destination phone number
- the final spoken sentence or paragraph to be played on the call

If `task` and `variables` are used internally, render them into one final notification sentence before calling the outbound helper.

### B. Outbound Call Initiation

Implement a helper or service that sends:

```json
{
  "appId": "<appId>",
  "botid": "<botid>",
  "callee": "13800138000",
  "requestId": "<unique-id>",
  "extra": "{\"notification\":{\"text\":\"您好,这是一条通知\",\"times\":2}}"
}
```

If the user's app needs stronger business correlation, store a minimized mapping between `requestId` and the notification payload before calling Vox.

Privacy requirements for any persisted notification context:

- Store the minimum fields needed for retry, callback, troubleshooting, or business correlation.
- Prefer salted hashes or masked forms for phone numbers unless full values are required for a retry.
- Encrypt full phone numbers, notification text, task variables, and callback message content at rest when they must be retained.
- Set an explicit retention period such as 7 to 30 days unless the business has a stricter requirement.
- Restrict access to service operators who need the data, and avoid exporting it to broad analytics sinks.
- Never log full phone numbers, full message text, secrets, request headers, or raw outbound request bodies.

For notification-only bots, prefer sending the final spoken content in `extra.notification.text` and `extra.notification.times` rather than requiring callback mode.

### C. Optional Callback-To-Agent Adapter

Only implement this section when the platform-side bot configuration requires callback-driven runtime content generation.

Translate Vox callback payload into the user's runtime shape.

Suggested mapping:

- `message` -> typically empty first-turn prompt for single-turn notification playback
- `requestid` -> request correlation key
- `callid` -> call session key
- `caller` / `callee` -> participant metadata
- `turn` -> conversational turn index
- `calltype` -> inbound/outbound mode marker

The adapter should load any saved notification context by `requestId` or `callId`, then instruct the Claw agent to produce the one notification sentence or paragraph to be spoken on the call.

### D. Optional SSE Response Contract

Only required for callback-driven advanced mode.

Return frames shaped like:

```text
data: {"id":"<requestid>","created":1678901234,"message":"您好，我是账单提醒助手。"}

data: {"id":"<requestid>","created":1678901235,"message":"您有一笔待处理账单，请及时登录系统处理。"}

data: [DONE]
```

### E. OpenClaw Integration Pattern

When the runtime is OpenClaw or a similar Claw framework, prefer this architecture:

1. Define a tool/action named `send_phone_notification`.
2. The tool validates business input and creates a `requestId`.
3. If the trigger comes from natural language, the tool extracts `callee` and renders one final `notificationText` sentence.
4. The tool invokes the Vox outbound API client.
5. In default mode, return a simple success payload to the runtime after dispatch.
6. Only in callback-driven mode, restore the original notification context from the callback endpoint.
7. Only in callback-driven mode, call the Claw runtime with a structured prompt or state payload.
8. Only in callback-driven mode, return one final notification script, optionally split into a few SSE chunks, and then end the stream.

Avoid binding TeddyMobile-specific request details deep into the agent prompt layer. Keep them in the adapter.

## Analysis Guidance

When the user asks for analysis, explain the implementation in these layers:

1. Platform side: how the user registers on TeddyMobile and obtains `appId`, `secret`, `botid`, and outbound number.
2. Transport side: outbound HMAC API, plus optional inbound callback SSE protocol.
3. Runtime side: how Claw triggers the outbound notification and produces a one-shot spoken script.
4. State side: how `requestId` correlates business context with outbound notification tasks, plus `callId` only if callback mode is enabled.
5. Risk side: credentials, retries, idempotency, and callback HTTPS only if callback mode is enabled.

## Verification Checklist

Verify as much as the environment allows:

1. Config names are documented.
2. Credential lookup order is documented and testable.
3. Outbound signature generation can be tested deterministically.
4. If callback mode is enabled, callback endpoint accepts the documented payload shape.
5. If callback mode is enabled, SSE frames end with `[DONE]`.
6. If callback mode is enabled, closed client connections do not crash the server.
7. Exact platform-side testing steps are documented for the user.
8. The response design stays single-turn.

## Recommended Deliverables

Produce the smallest set that fits the project:

- skill documentation for Claw users
- installation-ready skill metadata
- outbound HMAC client helper
- credential loader example and storage guidance
- optional callback endpoint example
- OpenClaw tool/action integration example
- env var documentation
- short verification guide

## Bundled References

Use these bundled files when helpful:

- `./resources/implementation-checklist.md`
- `./resources/hmac-outbound-client.js`
- `./resources/callback-server-example.js`
- `./resources/openclaw-integration-template.md`

## Final Response Requirements

In the final reply:

1. State what was implemented or analyzed.
2. Reference the files changed.
3. Call out required TeddyMobile platform inputs and manual steps.
4. Explain the registration -> trigger -> outbound call flow briefly, and only add callback -> SSE response flow if callback mode is in scope.
5. Provide concise verification steps.
