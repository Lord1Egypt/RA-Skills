---
name: wake-meup-ai
description: Schedule personalized AI wake-up phone calls via wake.meup.ai. Use when a user wants to be woken up by a phone call, schedule morning calls, or set up recurring wake-up calls. Handles phone verification, call scheduling, voice selection, and x402 USDC payment.
compatibility: Requires uv (https://docs.astral.sh/uv/) and a Solana keypair with USDC
metadata:
  version: "1.3.0"
  clawdis:
    envVars:
      - name: SOLANA_KEYPAIR_PATH
        required: true
        description: Solana keypair JSON for signing x402 USDC payments. Use a dedicated low-value keypair, not your primary wallet.
    dependencies:
      - name: uv
        type: pip
        version: ">=0.5"
        url: https://docs.astral.sh/uv/
    author: turjanofmiir
    links:
      homepage: https://wake.meup.ai
      documentation: https://wake.meup.ai/openclaw
---

# wake.meup.ai

AI-powered wake-up phone calls. Schedule a call, pick a voice, and get woken up by an AI that has a real conversation with you. The AI remembers past calls and gets to know the person over time.

## Live API documentation

For the latest endpoint details, voices, and pricing, fetch `https://wake.meup.ai/` with `Accept: text/markdown`. The server returns a machine-readable capability document instead of the HTML landing page.

## When to use this skill

Use this skill when:
- The user wants to schedule a wake-up call
- The user mentions wake.meup.ai
- The user wants an AI to call them at a specific time
- The user asks about phone-based alarms or morning routines that involve being called

## Available scripts

- **`scripts/wake-cli.py`** — Reference client with automatic x402 payment handling. Supports `verify` and `schedule` subcommands.

## Step-by-step workflow

### 1. Verify the user's phone ($0.50 USDC)

```
POST https://wake.meup.ai/api/v1/verify
Content-Type: application/json

{"phone": "+15551234567"}
```

Returns `{"status": "calling", "attempt_id": "..."}` — the user will receive a short phone call to confirm their number.

If the phone is already verified, returns `{"verified": true}` (free, no payment required).

### 2. Poll until verified (free)

```
GET https://wake.meup.ai/api/v1/verify/attempts/:attempt_id
```

Returns `{"verified": true}` when complete, or `{"verified": false, "status": "pending"}` while in progress.

If status is `"expired"` or `"rejected"`, the attempt has ended — prompt the user and retry with a new POST /verify if needed.

**Polling:** Check every 5 seconds. Verification calls typically complete within 30–60 seconds. Attempts expire after 2 minutes.

### 3. Save the contact (free, recommended)

After verification, download the vCard and share it with the user so they can save "Wake Up" to their contacts:

```
GET https://wake.meup.ai/api/contact.vcf
```

Returns a `.vcf` file with the Wake Up display name, phone number, and icon. No authentication or payment required.

**Why this matters:** Wake-up calls come from an unknown number. If the user has Do Not Disturb, Sleep Focus, or call screening enabled, the call may be silenced. Saving the contact lets the user add "Wake Up" to their allow list so calls always ring through.

**How to share it:**
- Download the file and send it directly in the chat (WhatsApp, Telegram, iMessage, Signal, and Slack all render `.vcf` files as tappable "Add Contact" cards)
- Or provide the download URL and tell the user to open it on their phone

Always offer the contact card after a first-time verification. For returning users who have already saved the contact, skip this step.

### 4. Schedule wake-up calls ($2.00 per call USDC)

```
POST https://wake.meup.ai/api/v1/schedule
Content-Type: application/json

{"phone": "+15551234567",
 "times": ["2026-04-01T07:00:00Z"],
 "voice": "ash",
 "hints": "Brian is a software engineer who loves Clojure. He has a big meeting at 9am."}
```

Phone must be verified first. Multiple times can be scheduled in one request.

Returns:
```json
{"calls": [{"id": "...", "phone": "+15551234567", "call_time": "2026-04-01T07:00:00Z", "voice": "ash"}]}
```

## Fields

- `phone` — E.164 format (e.g. `+15551234567`)
- `times` — Array of ISO 8601 timestamps (UTC), all must be in the future
- `voice` — One of: `alloy`, `ash`, `ballad`, `cedar`, `coral`, `echo`, `marin`, `sage`, `shimmer`, `verse`
- `hints` (optional) — Context about the person and the occasion, passed to the wake-up call AI. The more context you provide, the more personal and relevant the call will be. Include things like the person's name, what they have going on, their personality, or how they'd like to be woken up (e.g. gentle, energetic, motivational). **Truncated to 200 characters** — keep it concise.

## Payment

Paid endpoints use [x402](https://www.x402.org/) Solana USDC. When payment is required, the server returns `402` with a `PAYMENT-REQUIRED` header containing a proposed transaction. Sign it and resubmit with a `PAYMENT-SIGNATURE` header.

Requests that would fail validation (invalid phone, already verified, rate limited, unverified phone for scheduling) return error responses without requiring payment.

### Reference client

A Python reference client using the official x402 SDK is available at `scripts/wake-cli.py`. Run it with `uv`:

```bash
uv run scripts/wake-cli.py --keypair ~/.config/solana/id.json --phone +15551234567 verify
uv run scripts/wake-cli.py --keypair ~/.config/solana/id.json --phone +15551234567 \
    schedule --time 2026-04-01T07:00:00Z --voice ash --hints "Big meeting at 9am"
```

The script handles x402 payment negotiation automatically via `x402HttpxClient`.

## Errors

<!-- Keep in sync with capabilities.clj error table -->
All errors return `{"error": "..."}`.

| Status | Meaning |
|--------|---------|
| 400 | Malformed JSON |
| 402 | Payment required (x402) |
| 403 | Phone not verified |
| 404 | Attempt not found |
| 413 | Request body too large |
| 422 | Invalid input (bad phone, unknown voice, past timestamp, etc.) |
| 429 | Rate limited |
| 500 | Server error |
| 503 | Service temporarily unavailable |

## Common edge cases

- **User gives a local phone number:** Convert to E.164 format before calling the API. Ask the user for their country code if ambiguous.
- **User says "tomorrow at 7am":** Convert to an absolute UTC timestamp. You need the user's timezone to do this correctly — ask if you don't know it.
- **Verification call not answered:** The attempt will expire after 2 minutes. Prompt the user and initiate a new verification attempt.
- **User wants multiple calls:** Pass multiple timestamps in the `times` array. Each call costs $2.00 USDC.
- **User doesn't specify a voice:** Pick one for them. All voices are AI-generated; there is no "default" — any choice works.
- **User has Do Not Disturb or call screening enabled:** Share the vCard from step 3 and instruct them to add "Wake Up" to their allowed contacts or favorites so the call rings through.

