# X setup

Bring your own X developer app. Facts checked 2026-10-24. Generated from
`docs/platforms/x-setup.md`; edit it there.

## Cost first

The X API is pay-per-use with no free tier in the current docs: about **$0.015 per post**
and **$0.20 per post containing a link**. Buy credits in the X Developer Console before
posting. Prices: https://docs.x.com/x-api/getting-started/pricing

## App

1. https://console.x.com: create a project and app.
2. User authentication settings: OAuth 2.0, type **Native App** (public client, no secret).
   Permissions: Read and write.
3. Callback URL: `http://127.0.0.1:8765/callback` (exact match, including the path).
4. Copy the **Client ID**: `export X_CLIENT_ID="..."` in `~/.config/social-skills/env.sh`.
   Optional `X_REDIRECT_URI` if you registered a different port.

## Sign in

`node scripts/auth.mjs --platform x` opens the browser and listens on 127.0.0.1. Tokens
last 2 hours and are refreshed automatically (offline.access).

## Limits and rules

- 280 weighted characters (URLs count 23); up to 4 images or 1 video.
- 100 posts per 15 minutes per user.
- Since February 2026 self-serve apps may only reply when summoned by the original
  author, quote posts are Enterprise-only, and the developer guidelines forbid identical
  cross-posting and unsolicited @mentions: https://docs.x.com/developer-guidelines
