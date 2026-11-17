# Discord setup

Generated from `docs/platforms/discord-setup.md`; edit it there. Facts checked 2026-10-24.

Posting uses a **channel webhook**: no bot, one credential, one channel.

1. Channel settings > Integrations > Webhooks > New Webhook > Copy Webhook URL.
2. In `~/.config/social-skills/env.sh`:
   ```sh
   export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
   ```
   For more channels, add more variables and set `options.webhookEnv` in post.json.

The webhook URL is a secret: anyone with it can post to the channel. Delete and recreate
the webhook if it leaks; a deleted webhook returns 404 and must not be retried.

Limits: 2,000 characters, 10 attachments, 20 MiB per file by default. Mentions are
disabled unless `options.allowMentions` is true, so posts never ping @everyone by accident.

Source: https://docs.discord.com/developers/resources/webhook
