# Unified Memory Documentation

> 🧠 Enterprise-grade memory management system with hybrid search, atomic transactions, and plugin architecture

[![Version](https://img.shields.io/badge/version-5.2.0-blue.svg)](https://github.com/mouxangithub/unified-memory)
[![Node.js](https://img.shields.io/badge/node-%3E%3D18.0.0-green.svg)](https://nodejs.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Quick Links

| I want to... | Go to |
|-------------|-------|
| Get started quickly | [Quick Start](./getting-started/quickstart.md) |
| Install the system | [Installation Guide](./getting-started/installation.md) |
| Configure settings | [Configuration Guide](./getting-started/configuration.md) |
| Learn basic usage | [Basic Usage Guide](./guides/basic-usage.md) |
| Explore advanced features | [Advanced Usage](./guides/advanced-usage.md) |
| Build a plugin | [Plugin Development](./guides/plugins.md) |
| Integrate with my app | [Integration Guide](./guides/integration.md) |
| Understand the architecture | [Architecture Overview](./architecture/overview.md) |
| Find API reference | [API Reference](./api/overview.md) |
| Troubleshoot issues | [Troubleshooting](./reference/troubleshooting.md) |

## ✨ Key Features

### 🔍 Hybrid Search
Unified Memory combines multiple search algorithms for optimal relevance:
- **BM25**: Traditional keyword-based search
- **Vector Search**: Semantic similarity using embeddings
- **RRF (Reciprocal Rank Fusion)**: Combines results from multiple rankers

### ⚡ Atomic Transactions
Enterprise-grade data consistency:
- **WAL (Write-Ahead Logging)**: Crash recovery guarantee
- **Two-Phase Commit**: Atomic writes across JSON and vector storage
- **fsync Guarantee**: Data is written to disk, preventing loss

### 🔌 Plugin System
Extensible architecture with hot-reload support:
- **Lifecycle Hooks**: Before/after operation hooks
- **Sync Bridges**: Connect to external memory systems
- **Custom Processors**: Add custom memory processing

### 📊 Performance
Optimized for production workloads:
- **5-10x faster** search with optimized vector engine
- **60% storage reduction** through intelligent compression
- **78% cache hit rate** with semantic caching
- **45ms average query time**

## 📦 Quick Start

```bash
# Install
curl -fsSL https://raw.githubusercontent.com/mouxangithub/unified-memory/main/install.sh | bash

# Store a memory
unified-memory add "Remember to review quarterly reports" --tags work,reminder

# Search memories
unified-memory search "quarterly reports"

# Use via JavaScript API
node -e "
const { addMemory, searchMemories } = require('unified-memory');
(async () => {
  await addMemory({ text: 'My preference for morning meetings', tags: ['preference'] });
  const results = await searchMemories('meeting schedule');
  console.log(results);
})();
"
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Client Applications                       │
│        (OpenClaw, Web UI, CLI, API, MCP Clients)            │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                    API Gateway Layer                        │
│           (REST API, MCP Server, WebSocket)                 │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                    Service Layer                            │
│     (Memory Service, Search Service, Cache Service)           │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                    Storage Layer                            │
│        (SQLite, Vector Database, File System)                │
└─────────────────────────────────────────────────────────────┘
```

## 📚 Documentation Sections

### Getting Started
- [Quick Start](./getting-started/quickstart.md) - 5-minute introduction
- [Installation](./getting-started/installation.md) - Full installation guide
- [Configuration](./getting-started/configuration.md) - Configuration options

### User Guides
- [Basic Usage](./guides/basic-usage.md) - Core operations
- [Advanced Usage](./guides/advanced-usage.md) - Advanced features
- [Plugin Development](./guides/plugins.md) - Build plugins
- [Integration](./guides/integration.md) - Connect to other systems

### Architecture
- [Overview](./architecture/overview.md) - System design
- [Design Principles](./architecture/design-principles.md) - Key principles
- [Modules](./architecture/modules.md) - Module reference
- [Data Flow](./architecture/data-flow.md) - How data moves through the system

### API Reference
- [Overview](./api/overview.md) - API introduction
- [Core API](./api/core-api.md) - Core functions
- [MCP Tools](./api/mcp-tools.md) - MCP tool reference
- [Plugin API](./api/plugin-api.md) - Plugin development

### Reference
- [Configuration Reference](./reference/configuration.md) - All config options
- [Troubleshooting](./reference/troubleshooting.md) - Common issues
- [FAQ](./reference/faq.md) - Frequently asked questions

## 🔧 Development

```bash
# Clone and setup
git clone https://github.com/mouxangithub/unified-memory.git
cd unified-memory
npm install

# Run tests
npm test

# Build for production
npm run build
```

## 🤝 Contributing

We welcome contributions! Please read our [Contributing Guidelines](./contributing/guidelines.md) before submitting PRs.

## 📄 License

MIT License - see [LICENSE](../../LICENSE) file for details.

## 📞 Support

- [GitHub Issues](https://github.com/mouxangithub/unified-memory/issues)
- [GitHub Discussions](https://github.com/mouxangithub/unified-memory/discussions)

---

**Version**: 5.2.0 | **Last Updated**: 2026-04-20
