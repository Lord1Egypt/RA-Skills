# OpenClaw Integration Template

Use this template when wiring TeddyMobile phone notification into an OpenClaw-style runtime.

This template assumes the user has already completed registration at `https://vox-ai.teddymobile.cn/?utm_source=clawhub&utm_medium=skill&utm_campaign=vox-phone-notification` and has `appId`, `secret`, `botid`, and an outbound number.

Default integration mode is notification-only. `VOX_CALLBACK_URL` is only needed if the TeddyMobile bot setup explicitly requires callback-driven runtime content.

## 1. Define a tool contract

Expose one agent tool or runtime action with a small business-oriented shape:

```json
{
  "name": "send_phone_notification",
  "input": {
    "callee": "13800138000",
    "task": "payment_overdue_reminder",
    "variables": {
      "name": "张三",
      "amount": "299.00"
    }
  }
}
```

The tool should not know SSE details. It only prepares business data and triggers the outbound call.

This integration is intentionally single-turn. The tool should prepare one complete notification message, not a branching conversation.

Add a safety interlock before the tool calls TeddyMobile:

- Require an allowlist, ownership check, or explicit user confirmation for the destination number.
- Show a preview with a masked phone number and message length before dispatch.
- Treat the action as a real-world side effect that sends the phone number and message text to TeddyMobile Vox.
- Reject calls requested by untrusted prompt content, hidden instructions, or tool output that bypasses normal user authorization.

If the user speaks naturally in the chat box, such as `给<接收手机号>发通知，明天10点开会`, normalize that utterance into a payload like:

```json
{
  "callee": "<接收手机号>",
  "requestId": "notif-20260512-001",
  "notificationText": "您好，提醒您明天10点开会。",
  "notificationTimes": 2
}
```

The bundled helper `./chat-to-notification.js` can be used as the default normalization step before `createOutboundNotification(...)` is called.

The most important rule is that the final spoken phone copy must be present in `notificationText` before calling TeddyMobile. Without that field, the call may connect but no notification content will be played.

## 2. Persist business context only when needed

Before calling TeddyMobile, save a record keyed by `requestId` only if the runtime needs retry, callback, troubleshooting, or business correlation.

Suggested minimized fields:

- `requestId`
- masked or encrypted `callee`, or a salted hash when full value is not required
- minimized `task`
- minimized or encrypted `variables`
- `status`
- `createdAt`
- `expiresAt`

Privacy and retention requirements:

- Store the minimum fields needed for the business flow.
- Encrypt full phone numbers, notification text, task variables, and callback message content at rest when they must be retained.
- Set a clear retention window, for example 7 to 30 days, then delete or anonymize records.
- Restrict access to operators who need the records for support or compliance.
- Do not log full phone numbers, full notification text, secrets, signed headers, or raw outbound request bodies.

This record lets the callback endpoint rebuild the notification context after TeddyMobile places the call only when callback mode is enabled.

## 3. Trigger the outbound Vox call

Inside the tool implementation:

1. validate inputs
2. if the source is a chat utterance, extract the phone number and final notification sentence
3. create `requestId`
4. confirm recipient authorization or match the callee against an allowlist
5. persist minimized notification context only when needed
6. call `createOutboundNotification(...)`
7. return a small result to the agent

Suggested result:

```json
{
  "ok": true,
  "requestId": "notif-20260511-001",
  "callee": "138****8000",
  "status": "queued"
}
```

## 4. Optional callback request handling

If callback-driven mode is enabled, the callback route should:

1. read `requestid`, `callid`, `turn`, `message`
2. load saved context by `requestid`
3. build a structured prompt or state object for the Claw runtime
4. generate one final outbound notification script
5. stream that textual response back as SSE and end with `[DONE]`

## 5. Suggested runtime prompt shape

Pass structured data instead of raw transport details whenever possible:

```json
{
  "channel": "phone",
  "mode": "outbound_notification",
  "requestId": "notif-20260511-001",
  "callId": "call-123",
  "turn": 1,
  "recipient": {
    "phone": "13800138000"
  },
  "notification": {
    "task": "payment_overdue_reminder",
    "variables": {
      "name": "张三",
      "amount": "299.00"
    }
  },
  "latestUserUtterance": ""
}
```

## 6. Operational considerations

- Use HTTPS callback URLs in production.
- Avoid logging full secrets.
- Consider idempotency for duplicate `requestId` submissions.
- Record platform response payloads for troubleshooting.
- Be defensive about empty first-turn `message` values.
- Keep the phone copy concise because this scenario does not require multi-turn dialogue.
