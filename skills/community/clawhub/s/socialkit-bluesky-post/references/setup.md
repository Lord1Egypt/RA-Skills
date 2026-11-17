# Bluesky setup

Generated from `docs/platforms/bluesky-setup.md`; edit it there. Facts checked 2026-10-24.

Bluesky allows app passwords for single-purpose command-line tools.

1. Bluesky Settings > Privacy and security > App passwords > Add app password.
2. In `~/.config/social-skills/env.sh`:
   ```sh
   export BLUESKY_HANDLE="you.bsky.social"
   export BLUESKY_APP_PASSWORD="xxxx-xxxx-xxxx-xxxx"
   # export BLUESKY_SERVICE="https://bsky.social"   # your PDS if self-hosted
   ```

Never use your main account password. The session is cached (mode 600) because Bluesky
limits logins to 30 per 5 minutes.

Limits: 300 characters; up to 4 images of 2 MB each, with alt text required; link cards
with your own title and description. Video is not supported by this skill yet.

Sources: https://bsky.network/docs/oauth-client, https://bsky.network/docs/rate-limits
