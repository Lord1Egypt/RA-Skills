# Get Started in 30 Seconds

Use this guide immediately after installing `vox-phone-notification`.

## Try it without registration

Run a no-credential dry-run first:

```bash
node "skills/vox-phone-notification/resources/run-demo.js" "给<接收手机号>发通知，明天10点开会" --dry-run
```

Dry-run mode does not place a real phone call. It only verifies that the skill can parse and prints masked results for:

- the destination phone number
- the spoken notification text length
- the notification repeat count
- the generated request id

Do not run real-call modes until you have reviewed dry-run output and confirmed the recipient is authorized to receive the call.

## Try up to 10 real trial calls

Promotion builds can include a 10-use local trial mode:

```bash
node "skills/vox-phone-notification/resources/run-demo.js" "给<接收手机号>发通知，明天10点开会" --trial --confirm-real-call
```

Trial mode:

- uses the no-credential v2 trial endpoint instead of your local TeddyMobile credentials
- places one real phone notification after local content safety checks
- adds a required TeddyMobile Vox trial disclaimer before the user-provided content
- keeps at most 100 characters of user-provided content
- blocks links, contact information, long number sequences, and high-risk terms
- fixes `notificationTimes` to `1`
- records this machine trial usage count, up to 10 trials
- sends the destination phone number and message text to TeddyMobile Vox and may create usage, consent, anti-spam, or compliance obligations

The local trial marker is stored at:

```text
~/.teddymobile/vox-phone-notification-trial.json
```

This is a promotion-period convenience check, not a strong abuse-prevention boundary.

## Send formal phone notifications

To place a real outbound phone call, register and configure TeddyMobile Vox:

```text
https://vox-ai.teddymobile.cn/?utm_source=clawhub&utm_medium=skill&utm_campaign=vox-phone-notification
```

Formal registration flow:

1. Visit the TeddyMobile Vox website above.
2. Create and activate your account.
3. Complete formal access and record the returned `APPID` / `SecretID`.
4. Create a notification bot.
5. Record the bot's outbound number and `BotID`.

After trial, choose one setup path:

1. `配置引导`: get guided through the official site and parameter collection.
2. `稍后配置本地参数`: return later after configuring environment variables or a local credentials file.
3. `查看本地配置模板`: view the local config keys without pasting real values into chat.

After registration, prepare these values:

- `VOX_APP_ID`
- `VOX_SECRET`
- `VOX_BOT_ID`
- `VOX_OUTBOUND_NUMBER`

## Configure credentials

Create a local credential file:

```text
~/.teddymobile/credentials.json
```

Example:

```json
{
  "VOX_APP_ID": "your-app-id",
  "VOX_SECRET": "your-secret",
  "VOX_BOT_ID": "your-bot-id",
  "VOX_OUTBOUND_NUMBER": "your-outbound-number"
}
```

You can also set the same values as environment variables.

Do not paste live `APPID`, `SecretID`, `BotID`, outbound numbers, or `VOX_SECRET` into chat. Configure them directly in your shell, local secrets manager, or local credentials file.

## Run the live demo

After credentials are configured and you explicitly want formal outbound calling, run the live demo with `--live`:

```bash
node "skills/vox-phone-notification/resources/run-demo.js" "给<接收手机号>发通知，明天10点开会" --live --confirm-real-call
```

## What success looks like

- dry-run succeeds without credentials
- live mode loads TeddyMobile credentials
- the outbound request is accepted by Vox
- the destination phone receives the notification call
- the spoken content matches the parsed notification text
