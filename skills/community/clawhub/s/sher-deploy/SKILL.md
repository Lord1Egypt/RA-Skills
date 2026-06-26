---
name: sher-deploy
description: Build and deploy frontend projects to instant preview URLs. Auto-detects frameworks.
homepage: https://sher.sh
metadata: {"clawdbot":{"emoji":"🔗","requires":{"anyBins":["npx","sher"]}}}
---

# sher — deploy to a live preview URL

sher is a CLI that builds your frontend project, uploads it, and returns a live preview URL.

Use it when the user wants to see a frontend project live.

## Install

Global (recommended for agents):

```bash
npm i -g shersh
```

Or one-off with npx:

```bash
npx shersh link
```

## Deploy

From the project root:

```bash
sher link
```

sher auto-detects the framework, runs the build, uploads the output, and returns a URL.

### Options

| Flag | Description |
|------|-------------|
| `--dir <path>` | Upload a specific directory (skips framework detection) |
| `--ttl <hours>` | Set link expiry in hours (default: 24) |
| `--no-build` | Skip the build step (use if already built) |
| `--pass [password]` | Password-protect the preview (Pro only) |

### Examples

```bash
sher link                  # standard deploy
sher link --no-build       # already built
sher link --dir ./dist     # specific output directory
sher link --ttl 2          # 2-hour link
```

## Parsing the output

The CLI prints the live URL to stdout:

```
  https://a8xk2m1p.sher.sh  (copied)
  expires 2/19/2026, 11:00 AM
```

The URL matches `https://[a-z0-9]{8}.sher.sh` and is copied to the clipboard.

## After deploying

Present the URL to the user:

> Your preview is live at https://a8xk2m1p.sher.sh

Mention expiry if `--ttl` was set, and share the password if `--pass` was used.

## Supported frameworks

sher auto-detects and builds:

- **Vite** → `dist/`
- **Next.js** → static export to `out/`
- **Astro** → `dist/`
- **Create React App** → `build/`
- **Any project** with a build script producing `dist/`, `build/`, or `out/`
- **Static HTML** — use `--dir .` to upload directly

## Agent-friendly

- Runs headless, with exit code 0 on success
- Works without an account (1 deploy, 10MB, 6h TTL)
- Authenticated: 25 deploys, 50MB, 24h TTL

## Troubleshooting

If `sher link` fails:

1. **Missing build script** — add one to `package.json`, or use `--dir`
2. **Build error** — fix the error first, then retry
3. **Size limit** — 10MB anonymous, 50MB authenticated, 100MB Pro
4. **Missing output directory** — ensure the build produces `dist/`, `build/`, or `out/`, or use `--dir`
