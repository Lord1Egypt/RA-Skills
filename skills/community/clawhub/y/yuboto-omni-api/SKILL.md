---
name: yuboto-omni-api
description: Implement, troubleshoot, and generate integrations for Yuboto Omni API (SMS/Viber/messaging endpoints, callbacks, lists/contacts/blacklist, cost/balance/account methods). Use when building code or workflows against Yuboto API docs, especially when endpoint details differ between PDF docs and live Swagger.
metadata:
  {
    "openclaw":
      {
        "emoji": "📨",
        "requires": { "bins": ["python3"], "env": ["OCTAPUSH_API_KEY"] },
        "primaryEnv": "OCTAPUSH_API_KEY",
      },
  }
---

# Yuboto Omni API

Use this skill to work with Yuboto Omni API safely and consistently.

**Note:** This skill requires the `OCTAPUSH_API_KEY` environment variable.

**Getting Started:** You need a Yuboto/Octapush account with API access. Register at [octapush.yuboto.com](https://octapush.yuboto.com) and request API access from support.

**OpenClaw Integration:** This skill supports native OpenClaw credential management. Store your API key in `openclaw.json` for centralized, secure credential handling.

## Source-of-truth order

1. `references/swagger_v1.json` (live endpoint contract)
2. `references/api_quick_reference.md` (human-readable endpoint map)
3. `references/omni_api_v1_10_raw.md` (legacy PDF extract)
4. `assets/OMNI_API_DOCUMENTATION_V1_10.pdf` (original PDF)

If PDF and Swagger conflict, prefer Swagger for endpoint paths/fields.

## Fast workflow

1. Identify the use case (send message, get DLR, contacts, subscriber lists, blacklist, cost/balance).
2. Find matching endpoint(s):
   - Read `references/api_quick_reference.md`, or
   - Run: `python3 scripts/find_endpoints.py --q "<keyword>"`
3. Validate request schema directly in `references/swagger_v1.json`:
   - parameters (path/query/header)
   - requestBody
   - response schema
4. Build implementation code with:
   - clear auth header handling
   - retries + timeout
   - structured error mapping
5. For advanced Viber features, check Swagger first.

## Available commands (provided by scripts/yuboto_cli.py)

- `balance` — get account balance
- `cost --channel sms --iso2 gr --phonenumber +30...` — estimate sending cost
- `send-sms --sender <approved_sender> --text "..." --to +30... --batch-size 200 --sms-encoding auto` — send SMS (auto-batched + auto Unicode/GSM)
- `dlr --id <messageGuid>` — check delivery status for one message
- `send-csv --file contacts.csv --phone-col phonenumber --text-col text --sender-col sender` — bulk send from CSV
- `poll-pending` — refresh statuses for all pending messages
- `history --last 20` — show recent send records
- `status` / `status --id <messageGuid>` — inspect tracked message state

## Output requirements

When generating code or integration instructions:

- Include exact method + path.
- Include required auth headers.
- Include minimal working request example.
- Include expected response shape.
- Include 1 failure case and handling.

## Environment Variables

### Required Credential
- `OCTAPUSH_API_KEY` — Your Yuboto/Octapush API key (already base64 encoded from Octapush)

**Note:** This is the only credential required.

### Optional Variables (for testing/overrides)
- `TEST_PHONENUMBER` — Phone number for testing (international format: +3069XXXXXXXX)
- `SMS_SENDER` — Default sender ID for SMS messages (must be approved)
- `YUBOTO_BASE_URL` — Override API base URL (default: `https://api.yuboto.com`)

### Getting an API Key

To use this skill, you need a Yuboto/Octapush API key:

1. **Register for an account** at [octapush.yuboto.com](https://octapush.yuboto.com)
2. **Contact Yuboto support** to request API access
3. **Get your API key** from your Octapush dashboard or via support

The API key is used for authentication with all Yuboto Omni API endpoints.

### Setup Instructions

#### Option 1: OpenClaw Config (✅ **Recommended**)
Add to your `openclaw.json` config file:
```json
"skills": {
  "entries": {
    "yuboto-omni-api": {
      "enabled": true,
      "env": {
        "OCTAPUSH_API_KEY": "your_base64_api_key_here"
      }
    }
  }
}
```

#### Option 2: Environment Variable
```bash
export OCTAPUSH_API_KEY="your_base64_api_key_here"
```

**Note:** `.env` files are not supported. Use OpenClaw config for secure, centralized credential management.

## Security + Ops Notes

- Store API key in environment variable `OCTAPUSH_API_KEY`, not in source files.
- Prefer env vars over CLI `--api-key` to avoid leaking credentials in shell history.
- `poll_pending.sh` reads `OCTAPUSH_API_KEY` from the process environment only (it does not source `.env`).
- Always use an account-approved sender ID for SMS. If sender is not approved, API returns `108 - Sms Sender is not valid`.
- Bulk safety defaults are enabled:
  - `send-sms` defaults to `--batch-size 200` (hard cap 1000 recipients/request)
  - `send-sms` defaults to `--batch-delay-ms 250`
  - `send-csv` defaults to `--delay-ms 100`
- Encoding defaults:
  - `--sms-encoding auto` detects non-GSM text and sends as Unicode
  - Force Unicode with `--sms-encoding unicode` for scripts like Greek/Arabic/Chinese
  - Force GSM-7 with `--sms-encoding gsm` when needed
- Local state retention is enabled by default:
  - Sent log rotates to last `5000` lines (`YUBOTO_MAX_SENT_LOG_LINES`)
  - State index keeps up to `5000` tracked IDs (`YUBOTO_MAX_STATE_RECORDS`)
- Runtime data location default is **outside** the skill folder:
  - CLI state default: `$XDG_STATE_HOME/openclaw/yuboto-omni-api` (fallback `~/.local/state/openclaw/yuboto-omni-api`)
  - Poll logs/state default under the same base (`YUBOTO_LOG_DIR`/`YUBOTO_STATE_DIR` override supported)
- Privacy-by-default storage:
  - Stored state/log keeps minimal metadata (messageGuid, timestamps, status, recipient count)
  - Full payload/text/recipient persistence is **off** by default
  - Enable full persistence only if needed via `YUBOTO_STORE_FULL_PAYLOAD=true`
- Runtime dependency model: Python standard library only (no `requests` install required).
- Helper scripts are also stdlib-only: `scripts/refresh_swagger.py` uses `urllib` (no pip installs).
- Treat local runtime logs/state as sensitive even in minimized mode.

## Notes

- Swagger URL: `https://api.yuboto.com/scalar/#description/introduction`
- Swagger JSON: `https://api.yuboto.com/swagger/v1/swagger.json`
- More product/account info: `https://messaging.yuboto.com`
- Keep generated examples language-neutral unless user requests GR/EN copy.
