# SeedDrop v3

社区互动助手 — OpenClaw Skill。监控 B站、贴吧、知乎、小红书的相关讨论，生成有价值的回复。

## Quick Start

```bash
clawhub install seeddrop
seeddrop setup
seeddrop auth add bilibili
seeddrop monitor bilibili
```

## Tech Stack

- **Runtime**: Node.js 24+ / Bun via `npx tsx`
- **Language**: TypeScript (strict mode, ESM)
- **Dependencies**: tsx, typescript (dev only)
- **Platform**: Cross-platform (Windows, Linux, macOS)

## Supported Platforms

| Platform | Monitor | Reply | Difficulty |
|----------|---------|-------|------------|
| B站 | API | API | ★☆☆ |
| 贴吧 | API | API | ★☆☆ |
| 知乎 | API | Browser | ★★☆ |
| 小红书 | API/Browser | Browser | ★★★ |

## Scripts

| Script | Purpose |
|--------|---------|
| `npx tsx scripts/auth-bridge.ts` | Credential management |
| `npx tsx scripts/monitor.ts` | Platform monitoring |
| `npx tsx scripts/scorer.ts` | Post scoring engine |
| `npx tsx scripts/responder.ts` | Reply generation |
| `npx tsx scripts/analytics.ts` | Statistics & reports |

## Pipeline

```
auth-bridge → monitor → scorer → responder → interaction-log
```

See `guides/quickstart.md` for details.
