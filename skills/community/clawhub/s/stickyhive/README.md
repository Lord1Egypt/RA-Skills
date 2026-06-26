# stickyhive

CLI tool for managing StickyHive communities, post scheduling, automation workflows, and DM sequences — designed for AI agents (OpenClaw, Claude Code, etc.) and human operators alike.

## Quick Start

```bash
npm install -g stickyhive
export STICKYHIVE_API_KEY=hm_live_...
stickyhive communities:list
```

## OpenClaw / AI Agent Integration

This package includes a `SKILL.md` file that enables automatic discovery by OpenClaw and compatible AI agents. After installing globally, agents can read the skill file to learn all available commands.

## Documentation

Run `stickyhive --help` for a full list of commands, or see [SKILL.md](./SKILL.md) for detailed usage.

## Authentication

Get your API key from the StickyHive dashboard under **Settings → API Keys**. Keys use the `hm_live_` prefix for production and `hm_test_` for sandbox.

## License

MIT
