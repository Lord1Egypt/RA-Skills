# QMD Memory Skill for OpenClaw

## 💰 Save $50-300/month in API Costs

**Stop paying for memory. Start compounding knowledge.**

Every time your agent searches memory via API, you pay. With QMD Memory, all searches run locally — completely free, forever.

[![ClawHub](https://img.shields.io/badge/ClawHub-Install-blue)](https://clawhub.com/skills/asabove/qmd-memory)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## The Math

| Without QMD | With QMD |
|-------------|----------|
| 50-200 memory searches/day | Same searches |
| $0.02-0.05 per search | **$0 per search** |
| $30-300/month in API costs | **$0/month** |

**Annual savings: $360-3,600**

---

## Quick Start

```bash
# Install
clawhub install asabove/qmd-memory

# Setup (5-10 minutes, one time)
openclaw skill run qmd-memory setup

# Done. Your memory now costs $0.
```

---

## What You Get

✅ **Local hybrid search** — BM25 + vectors + LLM re-ranking  
✅ **Auto-configured collections** — Based on your workspace structure  
✅ **Smart context** — QMD understands what's in each collection  
✅ **Nightly auto-updates** — Index stays fresh automatically  
✅ **Multi-agent support** — Shared memory via MCP server  
✅ **Zero ongoing costs** — All models run locally  

---

## How It Works

QMD (by Tobi Lütke) combines three search technologies:

1. **BM25** — Fast keyword matching (SQLite FTS5)
2. **Vector Search** — Semantic similarity (local embeddings)
3. **LLM Re-ranking** — Quality filtering (local Qwen model)

This skill configures QMD for OpenClaw and integrates it with your agent's memory system.

---

## Commands

```bash
# Calculate your savings
openclaw skill run qmd-memory calculate-savings

# Search your memory
qmd query "what did we decide about pricing"

# Refresh index
openclaw skill run qmd-memory refresh

# Start shared server (for multi-agent)
openclaw skill run qmd-memory serve
```

---

## Templates

```bash
# For traders/investors
openclaw skill run qmd-memory template trading

# For content creators
openclaw skill run qmd-memory template content

# For developers
openclaw skill run qmd-memory template developer
```

---

## System Requirements

- Node.js >= 22
- ~3GB disk space (models + index)
- ~2GB RAM during embedding

Models download automatically on first run (~2GB one-time).

---

## Support

- **Questions?** support@asabove.tech
- **Issues?** [GitHub Issues](https://github.com/asabove/qmd-memory-skill/issues)
- **Updates?** [Newsletter](https://asabove.tech/newsletter)

---

## Credits

- **QMD** by [Tobi Lütke](https://github.com/tobi/qmd) — the brilliant local search engine
- **OpenClaw** — the agent platform this skill integrates with
- **As Above Technologies** — this integration and setup automation

---

## License

MIT — Use freely, share widely.

---

**As Above Technologies**  
*Agent Infrastructure for Humans*

[asabove.tech](https://asabove.tech) • [@asabovetech](https://twitter.com/asabovetech)
