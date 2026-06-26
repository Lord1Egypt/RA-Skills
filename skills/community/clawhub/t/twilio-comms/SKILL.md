---
name: twilio-comms
description: Twilio SMS, Voice, WhatsApp, and Verify (2FA) — send messages, make calls, and run verification flows from the CLI.
---
# Twilio Comms

Automate SMS, voice calls, WhatsApp messaging, and two-factor authentication flows via the Twilio API. Send and track messages, place and monitor outbound calls, send WhatsApp templates or free-form messages, and run complete Verify 2FA flows — all from a single Python CLI tool.

## Setup

```bash
export TWILIO_ACCOUNT_SID="ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export TWILIO_AUTH_TOKEN="your_auth_token_here"
export TWILIO_FROM_NUMBER="+15550001234"        # your Twilio number
export TWILIO_VERIFY_SERVICE_SID="VAxx..."      # optional, for Verify/2FA
```

Get credentials: [console.twilio.com](https://console.twilio.com) → Account Info.

## Commands / Usage

```bash
# ── SMS ─────────────────────────────────────────────────
# Send an SMS
python3 scripts/twilio_comms.py sms-send --to "+61400000000" --body "Hello from Twilio!"
python3 scripts/twilio_comms.py sms-send --to "+61400000000" --body "Custom sender" --from "+15550001234"

# List recent messages
python3 scripts/twilio_comms.py sms-list
python3 scripts/twilio_comms.py sms-list --limit 50 --to "+61400000000"

# Get delivery status of a message
python3 scripts/twilio_comms.py sms-status --sid "SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# ── VOICE ───────────────────────────────────────────────
# Make an outbound call (plays TwiML message)
python3 scripts/twilio_comms.py call-make --to "+61400000000" --message "Hello, this is an automated call."
python3 scripts/twilio_comms.py call-make --to "+61400000000" --twiml-url "https://demo.twilio.com/docs/voice.xml"

# List recent calls
python3 scripts/twilio_comms.py call-list
python3 scripts/twilio_comms.py call-list --limit 25 --status completed

# Get call details and status
python3 scripts/twilio_comms.py call-status --sid "CAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Get call recordings
python3 scripts/twilio_comms.py call-recordings --call-sid "CAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# ── WHATSAPP ────────────────────────────────────────────
# Send a free-form WhatsApp message (within 24h session window)
python3 scripts/twilio_comms.py wa-send --to "+61400000000" --body "Hi from WhatsApp via Twilio!"

# Send a template message (outside 24h window)
python3 scripts/twilio_comms.py wa-template --to "+61400000000" --template "Your appointment is confirmed for {{1}}." --params "Monday 3pm"

# ── VERIFY / 2FA ────────────────────────────────────────
# Send a verification code (SMS or call)
python3 scripts/twilio_comms.py verify-send --to "+61400000000"
python3 scripts/twilio_comms.py verify-send --to "+61400000000" --channel voice

# Check/verify the code
python3 scripts/twilio_comms.py verify-check --to "+61400000000" --code "123456"
```

## Requirements

- Python 3.8+
- `requests` (`pip install requests`)
- Environment variables: `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_FROM_NUMBER`
- Optional: `TWILIO_VERIFY_SERVICE_SID` for Verify/2FA commands
