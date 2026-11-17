# Google Business Profile setup

Generated from `docs/platforms/google-business-setup.md`; edit it there. Facts checked 2026-10-24.

## Approval first

Google must approve your Cloud project for the Business Profile APIs:
https://support.google.com/business/contact/api_default ("Application for Basic API
Access"). Requirements: a Business Profile verified and active for 60+ days and a website
listed on it. Quota 0 means not yet approved; 300 QPM means approved.

## Project

1. Use the same Google Cloud project as YouTube or a new one.
2. Enable: Google My Business API (appears after approval), My Business Account Management
   API, My Business Business Information API, Business Profile Performance API.
3. OAuth consent screen: add scope `https://www.googleapis.com/auth/business.manage`;
   while in Testing, add yourself as a test user (tokens expire after 7 days in Testing).
4. Reuse the Desktop app OAuth client, or create one, and set
   `GBP_CLIENT_SECRET_PATH` (defaults to `YT_CLIENT_SECRET_PATH`).

## Sign in

`node scripts/auth.mjs --platform google-business` (loopback with PKCE), then
`--locations` to find `options.location`.

## Limits

Post types STANDARD, EVENT, OFFER; photos by https URL; calls to action BOOK, ORDER,
SHOP, LEARN_MORE, SIGN_UP, CALL. Review replies up to 4096 bytes. The Q&A API was
discontinued on 2025-11-03.

Sources: https://developers.google.com/my-business/content/prereqs,
https://developers.google.com/my-business/content/posts-data
