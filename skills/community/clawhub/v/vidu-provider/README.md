# openclaw-plugin-vidu

OpenClaw Vidu video generation provider plugin.

Published to [ClawHub](https://clawhub.ai) as `vidu-video-generation`.

## Install

```bash
clawhub install vidu-video-generation
```

## Development

```bash
pnpm install
pnpm test
pnpm typecheck
```

## Live Testing

Requires a real Vidu API key:

```bash
VIDU_API_KEY=<your-key> VIDU_LIVE_TEST=1 pnpm test vidu.live.test.ts
```
