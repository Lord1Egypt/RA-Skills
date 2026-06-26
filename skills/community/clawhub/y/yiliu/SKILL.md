---
name: yiliu
description: "Yiliu - AI-powered note-taking knowledge base with semantic search, auto-summarization, and version management"
version: 1.2.0
author: Daming Dong
license: MIT
tags:
  - note
  - knowledge
  - memory
  - search
  - AI
  - semantic-search
  - rag
security:
  network: true
  notes: |
    This skill makes optional network requests to OpenAI API for AI features.
    - External API: OpenAI (optional, requires user's own API key)
    - Local embeddings: HuggingFace Transformers (no network required)
    - No eval() or arbitrary code execution
    - No hardcoded credentials
    - Data stored locally in SQLite/LibSQL
---

# Yiliu - AI Note-Taking Knowledge Base

Capture anytime, auto-organize, surface on demand.

## ✨ What's New (v1.2.0)

- **LibSQL Storage**: Replaced sql.js with LibSQL for better performance
- **Semantic Search**: Vector similarity search with hybrid ranking
- **AI Enhancement**: Auto-generated summaries and tags
- **Local Embeddings**: Support for HuggingFace Transformers (no API key needed)
- **Version Management**: Auto-save + manual marking for important versions

## Features

| Feature | Description | Command |
|---------|-------------|---------|
| Record | Quick capture with AI enhancement | `/记` or type directly |
| Semantic Search | Find content by intent | `/搜 <keyword>` |
| List | View recent notes | `/列表` |
| Edit | Modify existing notes | `/编辑 <id> <content>` |
| History | View version history | `/历史 <id>` |
| Export | Export to Markdown | `/导出` |
| Stats | View statistics | `/统计` |

## Quick Start

### Install

```bash
git clone https://github.com/DamingDong/yiliu.git
cd yiliu
npm install
npm run build
```

### Configure AI (Optional)

```bash
export OPENAI_API_KEY="your-api-key"
# Optional: Custom API endpoint
export OPENAI_BASE_URL="https://api.openai.com/v1"
```

**Without API Key**: Falls back to local embeddings via `@huggingface/transformers`. Core features still work.

### Usage

```
# Record a note (AI auto-summarizes + tags)
/记 Today I learned about CRDT sync with Last-Write-Wins strategy

# Semantic search (understands intent)
搜 distributed sync methods

# List notes
/列表

# View stats
/统计

# Export backup
/导出
```

## AI Features

| Feature | Model | Description |
|---------|-------|-------------|
| Embeddings | text-embedding-3-small / all-MiniLM-L6-v2 | Semantic search |
| Summaries | gpt-4o-mini | Auto summaries |
| Tags | gpt-4o-mini | Auto tags |

**No API Key**: Falls back to keyword search, core features remain functional.

## Data Storage

- **LibSQL**: Notes, version history
- **Vector Index**: Semantic search
- **Path**: `data/yiliu.db`, `data/vectors.json`

## Architecture

```
yiliu/
├── src/
│   ├── index.ts       # Entry
│   ├── commands/      # Command handlers
│   ├── storage/       # Storage (LibSQL + Vector)
│   ├── ai/            # AI capabilities
│   └── types/         # Type definitions
├── data/              # Data directory
└── SKILL.md
```

## Version History

- **v1.2.0** (2026-03-20) - LibSQL, semantic search, AI enhancement, local embeddings
- **v1.0.0** (2026-03-19) - MVP release

## License

MIT License