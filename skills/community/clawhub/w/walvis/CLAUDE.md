# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Overview

**W.A.L.V.I.S.** (Walrus Autonomous Learning & Vibe Intelligence System) is an OpenClaw skill that acts as a personal AI-powered bookmark manager. Users send links, text, or images via Telegram; the AI analyzes and tags them; everything is stored on Walrus decentralized storage; and a static web UI on Walrus Sites lets users browse and search.

**Hackathon:** OpenClaw x Sui Hackathon 2026 — Track 2: Local God Mode

**Core Technologies:**
- OpenClaw skill (SKILL.md) for Telegram integration
- TypeScript with ES modules (Node 18+)
- OpenAI-compatible LLM API for content analysis
- Walrus decentralized storage (testnet)
- Walrus Sites for web UI hosting
- TanStack Router + Vite + React 19 for web UI
- @mysten/dapp-kit for Sui wallet connection

## Project Structure

```
walvis/
├── bin/cli.js                    # npx walvis installer
├── skill/
│   ├── SKILL.md                  # OpenClaw skill definition
│   └── scripts/
│       ├── types.ts              # Shared TypeScript types
│       ├── storage.ts            # ~/.walvis/ file operations
│       ├── analyze.ts            # LLM analysis (OpenAI-compatible)
│       ├── walrus-sync.ts        # Walrus upload/download
│       ├── walrus-query.ts       # Local search index
│       └── wallet-setup.ts      # Sui wallet helper
├── hooks/openclaw/
│   ├── HOOK.md                   # Hook definition
│   └── handler.ts                # message:received handler
├── templates/soul-injection.md   # Agent personality
├── web/                          # Vite + React frontend
│   ├── src/routes/               # TanStack Router file-based routes
│   ├── src/components/           # ItemCard, SpaceCard, SearchBar, TagFilter
│   └── src/lib/                  # walrus.ts, types.ts
├── SKILL.md                      # Root copy for ClawHub
└── package.json
```

## Data Storage

All data lives at `~/.walvis/`:
- `manifest.json` — config, space→blobId mapping, LLM settings
- `spaces/<id>.json` — individual space files with BookmarkItem arrays

## Development Commands

```bash
# Install web dependencies
cd web && npm install

# Web dev server
npm run dev:web

# Build web UI
npm run build:web

# Deploy to Walrus Sites (requires site-builder)
npm run deploy:web
```

## Walrus API

- Publisher (testnet): `https://publisher.walrus-testnet.walrus.space`
- Aggregator (testnet): `https://aggregator.walrus-testnet.walrus.space`
- Upload: `PUT /v1/blobs?epochs=5` with JSON body
- Download: `GET /v1/blobs/{blobId}`
- Response: `newlyCreated.blobObject.blobId` or `alreadyCertified.blobId`

## OpenClaw Integration

- Skill installed to `~/.openclaw/skills/walvis/`
- Config in `~/.openclaw/openclaw.json` under `skills.entries.walvis`
- `WALVIS_LLM_API_KEY` env var required
- Scripts run with `node --import tsx/esm` or compiled JS

## Module System

ES modules (`"type": "module"`):
- All imports use `.js` extension (even for `.ts` source files)
- Top-level `await` supported
