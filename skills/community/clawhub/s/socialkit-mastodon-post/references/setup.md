# Mastodon setup

Generated from `docs/platforms/mastodon-setup.md`; edit it there. Facts checked 2026-10-24.

1. On your instance: Preferences > Development > New application.
2. Scopes: `read:statuses`, `write:statuses`, `write:media`. Save and copy **Your access token**.
3. In `~/.config/social-skills/env.sh`:
   ```sh
   export MASTODON_INSTANCE="https://mastodon.social"
   export MASTODON_ACCESS_TOKEN="..."
   ```

Treat the token like a password. Limits come from your instance (`/api/v2/instance`);
the defaults are 500 characters, 4 attachments, links counted as 23. Scheduled posts need
at least 5 minutes notice. 300 requests per 5 minutes; 30 media uploads per 30 minutes.

Source: https://docs.joinmastodon.org/methods/statuses/
