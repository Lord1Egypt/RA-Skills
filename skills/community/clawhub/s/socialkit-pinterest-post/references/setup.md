# Pinterest setup

Bring your own Pinterest app. Facts checked 2026-10-24. Generated from
`docs/platforms/pinterest-setup.md`; edit it there.

## Access tiers

- **Trial** (immediate): Pins you create are visible only to you (sandbox entities).
- **Standard**: request in My apps > Upgrade with a demo video of the OAuth flow, even if
  you are the only user. Needed for public Pins.
- Apps registered on or after 2026-09-14 may be refused access to non-business accounts;
  use a Pinterest business account.

## App

1. https://developers.pinterest.com/apps > Connect app.
2. Redirect URI (exact match): `https://ahmadhussain.dev/social-skills-oauth/`.
3. In `~/.config/social-skills/env.sh`:
   ```sh
   export PINTEREST_APP_ID="..."
   export PINTEREST_APP_SECRET="..."
   export PINTEREST_REDIRECT_URI="https://ahmadhussain.dev/social-skills-oauth/"
   # export PINTEREST_SANDBOX=1   # use api-sandbox.pinterest.com
   ```

## Sign in

`node scripts/auth.mjs --platform pinterest --start`, then `--finish --url "..."`.
Access tokens last 30 days and refresh automatically (continuous refresh).
List boards for `options.boardId`: `node scripts/auth.mjs --platform pinterest --boards`.

## Limits

Title 100, description 800, link 2048, alt text 500 characters. Carousels 2-5 images.
Video Pins need a cover image URL.

## Sources

- Access tiers: https://developers.pinterest.com/docs/key-concepts/access-tiers/
- Authentication: https://developers.pinterest.com/docs/getting-started/set-up-authentication-and-authorization/
