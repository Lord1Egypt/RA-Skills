# Yiliu (忆流)

> Capture anytime, auto-organize, surface on demand - AI-powered note-taking knowledge base

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.2.0-blue.svg)](https://github.com/DamingDong/yiliu)

[中文文档](./README_CN.md)

## Overview

Yiliu is an OpenClaw Skill focused on personal knowledge management. With AI capabilities for automatic organization and semantic search, it makes knowledge flow like water.

## Features

- ⚡ **Zero-barrier capture** - Record in 3 seconds, no categorization needed
- 🧠 **AI auto-organization** - Automatic summaries and tags
- 🔍 **Semantic search** - Understands intent, finds what you need
- 📱 **Capture anywhere** - WeChat as entry point
- 💾 **Local storage** - Data sovereignty, one-click export

## Quick Start

### Installation

```bash
# Clone the project
git clone https://github.com/DamingDong/yiliu.git
cd yiliu

# Install dependencies
npm install

# Build
npm run build
```

### Configuration

```bash
# Optional: Configure OpenAI API Key (enables AI enhancement features)
export OPENAI_API_KEY=your-api-key
```

**Note**: Without an API key, the app automatically falls back to local embedding models (`@huggingface/transformers`). Basic recording and search still work.

### Usage

```bash
# Start
npm start

# Or use built-in commands
./yiliu "record today's learnings"
./yiliu "search CRDT"
```

## Commands

| Command | Description |
|---------|-------------|
| `/记 <content>` | Record a note |
| `/搜 <keyword>` | Search notes |
| `/列表` | List all notes |
| `/历史 <id>` | View version history |
| `/统计` | View statistics |
| `/导出` | Export data |
| `/删除 <id>` | Delete note |
| `/帮助` | Show help |

## Project Structure

```
yiliu/
├── src/
│   ├── index.ts          # Entry point
│   ├── commands/         # Command handlers
│   ├── storage/          # Storage layer
│   ├── ai/               # AI capabilities
│   └── types/            # Type definitions
├── dist/                 # Build output
├── data/                 # Data storage
├── SKILL.md              # Usage documentation
└── package.json
```

## Tech Stack

- **Storage**: LibSQL (SQLite)
- **Embeddings**: OpenAI / HuggingFace Transformers
- **Framework**: OpenClaw Skill
- **Language**: TypeScript

## Configuration

| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API Key | - |
| `OPENAI_BASE_URL` | API endpoint | https://api.openai.com/v1 |
| `YILIU_DATA_PATH` | Data directory | ./data |

## Development

```bash
# Development mode (watch for changes)
npm run dev

# Test
npm test

# Build
npm run build
```

## Changelog

See [CHANGELOG.md](CHANGELOG.md)

## Roadmap

### v1.3 (Planned)
- Full embedjs integration
- Data migration scripts
- Unit tests

### v2.0 (Future)
- WebDAV sync
- Web scraping (readability)
- PDF processing
- Yjs real-time sync
- Web canvas interface

## Contributing

Issues and Pull Requests are welcome!

## License

MIT License - See [LICENSE](LICENSE)

## Contact

- Author: Daming Dong (董大明)
- Email: dmdong@gmail.com
- GitHub: https://github.com/DamingDong/yiliu
