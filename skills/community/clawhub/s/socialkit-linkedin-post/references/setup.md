# LinkedIn setup

Bring your own LinkedIn app. Facts checked 2026-10-24. Generated from
`docs/platforms/linkedin-setup.md`; edit it there.

## What is possible

- **Personal profile:** yes, with the self-serve "Share on LinkedIn" product.
- **Company page:** needs the Community Management API, granted only to registered legal
  organisations after vetting, on a separate app. Not covered by default.
- No analytics or comment reading for personal-profile apps (those permissions are closed
  or Community Management only).

## App

1. https://www.linkedin.com/developers/apps > Create app (needs a LinkedIn Page to
   associate; any page you admin works).
2. Products: add **Share on LinkedIn** and **Sign In with LinkedIn using OpenID Connect**.
3. Auth tab: add the redirect URL (HTTPS), for example
   `https://ahmadhussain.dev/social-skills-oauth/`.
4. In `~/.config/social-skills/env.sh`:
   ```sh
   export LINKEDIN_CLIENT_ID="..."
   export LINKEDIN_CLIENT_SECRET="..."
   export LINKEDIN_REDIRECT_URI="https://ahmadhussain.dev/social-skills-oauth/"
   # export LINKEDIN_VERSION="202610"   # API version YYYYMM; versions last at least a year
   ```

## Sign in

`node scripts/auth.mjs --platform linkedin --start`, open the URL, then
`--finish --url "<URL you landed on>"`. Tokens last 60 days; self-serve apps get no refresh
tokens, so sign in again when it expires.

## Sources

- Posts API: https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api
- Authorization: https://learn.microsoft.com/en-us/linkedin/shared/authentication/authorization-code-flow
- Versioning: https://learn.microsoft.com/en-us/linkedin/marketing/versioning
