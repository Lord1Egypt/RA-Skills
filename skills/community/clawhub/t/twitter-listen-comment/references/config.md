# Config

Create `references/config.json` by copying `references/config.example.json` and editing:

- `fromUsers`: usernames to monitor (without `@`)
- `agentTarget`: agent routing target, e.g. `telegram:7164765349`
- `notifyChannel`: message channel for notices
- `notifyTarget`: where to send notices
- `maxTweetAgeSeconds`: only reply to tweets newer than this age

Required environment variables:
- `TWITTER_TOKEN`

Optional environment variables:
- `OPENCLAW_BIN` (defaults to `openclaw` in PATH)
- `TWITTER_LISTEN_COMMENT_DATA_DIR` (defaults to `<skill>/data`)
