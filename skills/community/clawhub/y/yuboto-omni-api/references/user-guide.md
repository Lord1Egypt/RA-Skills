# Yuboto Omni API Skill — User Guide

## What this skill helps with

- Send SMS messages
- Check delivery status (DLR)
- Send bulk SMS from CSV
- Track pending/delivered/failed messages locally
- Estimate sending cost by country/channel

## Prerequisites

- Active Yuboto/Octapush API key (base64 format)
- Approved sender ID (e.g., `YourSender`)
- Python 3 installed (no extra Python packages required)

## Environment variables

Recommended: set via OpenClaw config (`skills.entries.yuboto-omni-api.env`).
Alternative: export in your shell session.

- `OCTAPUSH_API_KEY` (required)
- `TEST_PHONENUMBER` (optional test recipient)
- `SMS_SENDER` (optional default sender)
- `YUBOTO_STATE_DIR` (optional override for runtime state location)
- `YUBOTO_LOG_DIR` (optional override for poll log location)
- `YUBOTO_STORE_FULL_PAYLOAD` (optional: `true` to persist full payload/text/recipients; default `false`)

Helper tooling:
- `scripts/refresh_swagger.py` uses Python stdlib `urllib` (no `requests` dependency).

By default, runtime state/logs are stored outside the skill folder under:
- `$XDG_STATE_HOME/openclaw/yuboto-omni-api` or
- `~/.local/state/openclaw/yuboto-omni-api`

## Quick start

Run from skill root:

```bash
python3 scripts/yuboto_cli.py balance
python3 scripts/yuboto_cli.py cost --channel sms --iso2 gr --phonenumber +3069XXXXXXX
python3 scripts/yuboto_cli.py send-sms --sender "YourSender" --text "hello" --to +3069XXXXXXX --batch-size 200 --sms-encoding auto
python3 scripts/yuboto_cli.py dlr --id <MESSAGE_GUID>
```

## Bulk send (CSV)

CSV example:

```csv
phonenumber,text,sender
+3069AAAAAAA,Campaign message one,YourSender
+3069BBBBBBB,Campaign message two,YourSender
```

Send:

```bash
python3 scripts/yuboto_cli.py send-csv \
  --file contacts.csv \
  --phone-col phonenumber \
  --text-col text \
  --sender-col sender \
  --sms-encoding auto
```

## Tracking and pending queue

```bash
python3 scripts/yuboto_cli.py status
python3 scripts/yuboto_cli.py poll-pending
python3 scripts/yuboto_cli.py history --last 20
```

## Encoding note

- If lowercase Greek or non-Latin text is altered, force Unicode:

```bash
python3 scripts/yuboto_cli.py send-sms --sender "YourSender" --to +3069XXXXXXX --text "καλημέρα" --sms-encoding unicode
```

- `--sms-encoding auto` usually picks Unicode correctly when non-GSM characters are present.

## Common issues

- `Sms Sender is not valid`:
  - Use an approved sender ID from your account.
- `Invalid omni_channel` on cost:
  - Use `channel=sms` and include `iso2` (e.g., `gr`).
- `Invalid Id` on DLR:
  - Use a real `messageGuid` returned from a successful send.

## Security notes

- Do not hardcode API keys in scripts.
- Prefer env vars over CLI `--api-key` to avoid shell history leaks.
- Treat local logs/state as sensitive (phone numbers + message previews).
- More product/account info: https://messaging.yuboto.com
