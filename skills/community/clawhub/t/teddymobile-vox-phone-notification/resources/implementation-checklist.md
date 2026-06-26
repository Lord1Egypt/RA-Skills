# Vox Phone Notification Checklist

## Platform Setup

- Guide user to `https://vox-ai.teddymobile.cn/?utm_source=clawhub&utm_medium=skill&utm_campaign=vox-phone-notification`
- Enterprise account approved on TeddyMobile
- `appId` received
- `secret` received
- Bot created in the TeddyMobile platform
- `botid` recorded
- Outbound number recorded
- Network whitelist requirements confirmed if applicable

Only for callback-driven advanced mode:

- HTTPS callback URL configured on the bot

## Claw Runtime Integration

- `send_phone_notification` tool or equivalent action defined
- Input validation for `callee` and business payload implemented
- `requestId` generated or injected by caller
- Notification context persisted for callback lookup when needed
- Notification content designed for single-turn playback only

## Optional Vox Callback Handling

- Callback route accepts `POST` JSON
- Request body fields mapped to runtime context
- First-turn empty `message` handled
- Response uses `text/event-stream`
- Stream emits `data: {json}` frames only
- Stream always ends with `data: [DONE]`
- Closed or interrupted connections handled safely
- No multi-turn follow-up logic added unless explicitly required

## Outbound API

- GMT date generation implemented
- URI parameter sorting implemented for signing
- Official canonical signing string verified
- Final trailing newline included in canonical string
- HMAC-SHA256 signature implemented
- Required HMAC headers added
- trial `POST /vox/v2/outbound` no-credential client implemented
- formal `POST /vox/v1/outbound` signed client implemented
- Notification-only payload supports `extra.notification.text`
- Notification-only payload supports `extra.notification.times`

## Verification

- Deterministic signature test prepared
- Canonical string logged or inspectable during sandbox validation
- Callback endpoint smoke-tested locally
- SSE framing checked manually
- End-to-end outbound notification tested in TeddyMobile platform

Only if callback-driven mode is enabled:

- Callback endpoint smoke-tested locally
- SSE framing checked manually
