# Cron Setup for Content System

All parameters come from `openclaw.json` → `skills.entries["tg-channel-manager"].config`.

## News Scout

Searches for news and writes drafts to content-queue.md.

```bash
# For each time from config.cronScoutTimes:
openclaw cron add \
  --name "content-scout-<N>" \
  --schedule "<config.cronScoutTimes[N]>" \
  --timezone "<config.timezone>" \
  --prompt-file "{baseDir}/references/scout-prompt.md"
```

## Publisher

Takes pending posts and publishes them to the channel.

```bash
# For each time from config.cronPublisherTimes:
openclaw cron add \
  --name "content-pub-<N>" \
  --schedule "<config.cronPublisherTimes[N]>" \
  --timezone "<config.timezone>" \
  --prompt-file "{baseDir}/references/publisher-prompt.md"
```

## Management

```bash
# List crons
openclaw cron list

# Remove a cron
openclaw cron remove --name "content-scout-1"

# Check next trigger
openclaw cron status
```
