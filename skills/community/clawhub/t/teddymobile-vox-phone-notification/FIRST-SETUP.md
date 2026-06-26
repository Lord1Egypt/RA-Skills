# First-Time Setup Guide

Use this guide when installing `vox-phone-notification` for the first time.

## Goal

Complete TeddyMobile platform onboarding, prepare the required credentials, and verify that the skill can place an outbound notification call successfully.

## Step 1: Try dry-run without registration

Before registering or configuring credentials, run:

```bash
node "skills/vox-phone-notification/resources/run-demo.js" "给<接收手机号>发通知，明天10点开会" --dry-run
```

This verifies that the skill can parse and print masked results for:

- the destination phone number
- the spoken notification content length
- the notification repeat count

No real phone call is placed in dry-run mode, and the parsed phone number plus notification text are masked in terminal output.

Use dry-run output as the required preview before any real call. Do not proceed unless the recipient number is authorized and the notification content is appropriate to transmit to TeddyMobile Vox.

## Step 2: Try up to 10 promotion trial calls

Run up to 10 real trial calls through the no-credential v2 trial endpoint:

```bash
node "skills/vox-phone-notification/resources/run-demo.js" "给<接收手机号>发通知，明天10点开会" --trial --confirm-real-call
```

Trial mode:

- uses the no-credential v2 trial endpoint instead of local user credentials
- places one real phone notification after local content safety checks
- prepends a TeddyMobile Vox trial disclaimer
- keeps at most 100 characters of user-provided content
- blocks links, contact information, long number sequences, and high-risk terms
- fixes `notificationTimes` to `1`
- stores a local trial usage counter at `~/.teddymobile/vox-phone-notification-trial.json`
- sends the destination phone number and message text to TeddyMobile Vox and may create usage, consent, anti-spam, or compliance obligations

This is a promotion-period convenience check and can be bypassed by users who modify local files. Use the server-side no-credential v2 trial endpoint for quota and abuse controls.

## Step 3: Register on TeddyMobile

Go to `https://vox-ai.teddymobile.cn/?utm_source=clawhub&utm_medium=skill&utm_campaign=vox-phone-notification` and complete the platform onboarding process.

Typical first-time setup includes:

1. creating or activating your TeddyMobile account
2. completing enterprise registration or review if required
3. enabling the Vox-related capabilities needed for outbound calling

## Step 4: Create and configure the bot

Inside the TeddyMobile platform, create or configure the bot that will be used for outbound notification calls.

Confirm that:

- the selected `botid` is the one intended for notification calls
- the bot has outbound notification capability enabled
- the platform setup for your environment supports direct notification playback or the callback mode your deployment requires

## Step 5: Collect the required platform values

Record these values from the TeddyMobile platform:

- `VOX_APP_ID`
- `VOX_SECRET`
- `VOX_BOT_ID`
- `VOX_OUTBOUND_NUMBER`

Optional only if your environment uses callback-driven advanced mode:

- `VOX_CALLBACK_URL`

## Step 6: Configure local credentials

This skill supports the following lookup order:

1. environment variables first
2. local file fallback at `~/.teddymobile/credentials.json`
3. custom file path override via `VOX_CREDENTIALS_FILE`

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

Security guidance:

- do not commit real credentials into source control
- do not publish real credentials inside the skill zip
- keep only example credentials in distributable files
- do not paste `APPID`, `SecretID`, `BotID`, outbound numbers, or `VOX_SECRET` into chat, shared docs, logs, tickets, or screenshots
- prefer environment variables, a local secrets manager, or `~/.teddymobile/credentials.json` with restrictive file permissions

## Step 7: Run the live local demo

From the workspace root, run:

```bash
node "skills/vox-phone-notification/resources/run-demo.js" "给<接收手机号>发通知，明天10点开会" --live --confirm-real-call
```

The demo should print:

- outbound response

## Step 8: Verify playback

Confirm that:

- the call is placed successfully
- the destination number receives the call
- the spoken notification is audible
- the spoken content matches the expected `notificationText`

## Step 9: Integrate into your runtime

After the demo succeeds, integrate the skill into your Claw, OpenClaw, WorkBuddy, or compatible runtime.

Recommended integration shape:

- parse natural-language chat input into `callee` and `notificationText`
- create a `requestId`
- call the bundled outbound helper
- return a simple success result to the runtime in notification-only mode

## If first-time setup is blocked

If you cannot continue, check these first:

- platform registration is approved
- the bot is configured for outbound notification usage
- the credentials match the active TeddyMobile environment
- the outbound number is enabled for the account
- the request body includes `extra.notification.text`

## Related files

- `SKILL.md`
- `README.md`
- `workflow.md`
- `resources/credentials-loader.js`
- `resources/run-demo.js`
