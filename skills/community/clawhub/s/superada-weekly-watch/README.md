# superada-weekly-watch

Subscribe an agent to SuperAda updates without email. The skill checks the SuperAda Ship Log RSS feed, OpenClaw changelog, Weekly Claw, tools, skills, and workflow packs, then reports only what changed since the last run.

## Install

```bash
openclaw skills install github:henrino3/enterprise-crew-skills/superada-weekly-watch
```

SuperAda also publishes a curl installer for non-OpenClaw runtimes:

```bash
curl -sSf https://superada.ai/install/superada-weekly-watch | sh
```

## Run

```bash
node ~/.superada/skills/superada-weekly-watch/scripts/superada-weekly-watch.mjs
```

State is stored in `~/.superada/weekly-watch-state.json` unless `SUPERADA_WATCH_STATE` is set.
