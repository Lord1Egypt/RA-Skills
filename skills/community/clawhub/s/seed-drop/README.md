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
| 贴吧 | API → Browser fallback | API | ★★☆ |
| 知乎 | API → Browser fallback | Browser | ★★☆ |
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

## Disclaimer / 免责声明

本工具是社区互动辅助工具，**不是**数据爬虫。使用本工具即表示您同意自行承担所有责任，遵守相关法律法规及各平台服务条款。工具使用您自己的账号凭证操作，不大规模采集或存储第三方数据。开发者不对使用本工具产生的任何后果负责。

详细免责条款请参阅 [SKILL.md](SKILL.md#disclaimer--免责声明)。
