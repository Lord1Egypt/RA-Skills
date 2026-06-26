# PulseMon Skill for OpenClaw

Monitor your cron jobs and background tasks with [PulseMon](https://pulsemon.dev).

## Install

```
clawhub install pulsemon
```

## Setup

1. Create a free account at [pulsemon.dev](https://pulsemon.dev)
2. Generate an API key under **Dashboard > Settings > API Keys**
3. Set the environment variable:
   ```
   PULSEMON_API_KEY=pm_your-key-here
   ```

## What You Can Do

- **List monitors** — "check my monitors", "show all monitors"
- **Create monitors** — "create a monitor called nightly-backup that runs daily"
- **Update monitors** — "change the interval on nightly-backup to every 12 hours"
- **Delete monitors** — "delete the data-sync monitor"
- **Pause/resume** — "pause nightly-backup", "resume nightly-backup"
- **View history** — "show recent pings for nightly-backup", "any incidents today?"
- **Set duration limits** — "set max duration on etl-pipeline to 5 minutes"
- **Send pings** — "ping nightly-backup with status start", "ping nightly-backup with body 'processed 500 rows'"

All through natural language via your OpenClaw agent.
