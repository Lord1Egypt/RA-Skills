# Telegram Authentication Flow

Reference: https://core.telegram.org/api/auth

## Login Steps

1. **auth.sendCode** — Sends OTP to the phone number
2. **auth.signIn** — Validates OTP code
3. If 2FA enabled: **auth.checkPassword** — SRP-based password verification

## Key Points

- OTP codes expire in ~60 seconds
- 2FA uses SRP protocol (Telethon handles it automatically with `client.sign_in(password=...)`)
- Session file persists auth across restarts
- Only one client can use a session file at a time (SQLite lock)
- Flood limits: ~5 login attempts per day per number
- The API ID owner's phone gets more generous flood limits

## Paid Media

Reference: https://core.telegram.org/api/paid-media

- Uses `inputMediaPaidMedia` with `messages.sendMedia`
- `stars_amount`: price in Telegram Stars
- `extended_media`: array of photos/videos
- **Only works in channels** (`EXTENDED_MEDIA_PEER_INVALID` in private chats)
- Channel must have `paid_media_allowed` flag

## Code Types

Telegram may send codes via:
- In-app notification (`sentCodeTypeApp`)
- SMS (`sentCodeTypeSms`)
- Phone call (`sentCodeTypeCall`)
- Fragment.com (`sentCodeTypeFragmentSms`)
- Email (`sentCodeTypeEmailCode`)

Third-party apps cannot use Firebase SMS — only official apps can.
