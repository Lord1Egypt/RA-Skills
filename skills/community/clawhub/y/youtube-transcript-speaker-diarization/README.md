# Standalone Skill

This folder contains the standalone OpenClaw skill.

This is the fastest way to try the integration. It is also the most inspectable path if you want a plain shell script you can audit end to end.

Before installing:

1. sign up at [diarize.io](https://diarize.io)
2. create an API key at [diarize.io/settings/api-keys](https://diarize.io/settings/api-keys)
3. make sure `bash`, `curl`, and `jq` are available

Install locally:

```bash
openclaw skills install ./skill
```

If you later move to the native plugin, remove this standalone skill from your active OpenClaw workspace first. The plugin already bundles its own skill guidance, and keeping both installed can create confusing precedence issues.

Primary files:

- [SKILL.md](./SKILL.md)
- [scripts/youtube-transcript.sh](./scripts/youtube-transcript.sh)
