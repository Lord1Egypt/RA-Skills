# QMD Memory Skill for OpenClaw
## Local Hybrid Search — Save $50-300/month in API Costs

**Author:** As Above Technologies
**Version:** 1.0.0
**ClawHub:** [Coming Soon]

---

## 💰 THE VALUE PROPOSITION

### API Costs You're Paying Now

| Operation | API Cost | Frequency | Monthly Cost |
|-----------|----------|-----------|--------------|
| memory_search (embedding) | $0.02-0.05 | 50-200/day | $30-300 |
| Context retrieval | $0.01-0.03 | 100+/day | $30-90 |
| Semantic queries | $0.03-0.08 | 20-50/day | $18-120 |
| **TOTAL** | | | **$78-510/month** |

### With QMD Local

| Operation | Cost | Why |
|-----------|------|-----|
| All searches | **$0** | Runs on your machine |
| Embeddings | **$0** | Local GGUF models |
| Re-ranking | **$0** | Local LLM |

**Your savings: $50-300+/month**

One-time setup. Forever free searches.

---

## 🚀 QUICK START

```bash
# Install the skill
clawhub install asabove/qmd-memory

# Run setup (installs QMD, configures collections)
openclaw skill run qmd-memory setup

# That's it. Your memory is now supercharged.
```

---

## WHAT YOU GET

### 1. Automatic Collection Setup

Based on your workspace structure, we create optimized collections:

```
✓ workspace     — Core agent files (MEMORY.md, SOUL.md, etc.)
✓ daily-logs    — memory/*.md daily logs
✓ intelligence  — intelligence/*.md (if exists)
✓ projects      — projects/**/*.md (if exists)
✓ documents     — Any additional doc folders you specify
```

### 2. Smart Context Descriptions

We add context to each collection so QMD understands what's where:

```
qmd://workspace    → "Agent identity and configuration files"
qmd://daily-logs   → "Daily work logs and session history"
qmd://intelligence → "Analysis, research, and reference documents"
```

### 3. Pre-configured Cron Jobs

```bash
# Auto-update index (nightly at 3am)
0 3 * * * qmd update && qmd embed

# Keep your memory fresh without thinking about it
```

### 4. OpenClaw Integration

Memory search now uses QMD automatically:
- `memory_search` → routes to QMD hybrid search
- `memory_get` → retrieves from QMD collections
- Results include collection context

### 5. Multi-Agent MCP Server (Optional)

```bash
# Start shared memory server
openclaw skill run qmd-memory serve

# All your agents can now query collective memory
# Forge, Thoth, Axis — shared knowledge base
```

---

## 📊 SEARCH MODES

| Mode | Command | Best For |
|------|---------|----------|
| **Keyword** | `qmd search "query"` | Exact matches, fast |
| **Semantic** | `qmd vsearch "query"` | Conceptual similarity |
| **Hybrid** | `qmd query "query"` | Best quality (recommended) |

### Example Queries

```bash
# Find exact mentions
qmd search "Charlene" -n 5

# Find conceptually related content
qmd vsearch "how should we handle customer complaints"

# Best quality — expansion + reranking
qmd query "what decisions did we make about pricing strategy"

# Search specific collection
qmd search "API keys" -c workspace
```

---

## 🔧 CONFIGURATION

### Add Custom Collections

```bash
openclaw skill run qmd-memory add-collection ~/Documents/research --name research
```

### Add Context

```bash
openclaw skill run qmd-memory add-context qmd://research "Market research and competitive analysis"
```

### Refresh Index

```bash
openclaw skill run qmd-memory refresh
```

---

## 💡 TEMPLATES

### Trading/Investing Workspace

```bash
openclaw skill run qmd-memory template trading
```

Creates:
- `intelligence` — Trading systems, dashboards, signals
- `market-data` — Price history, analysis
- `research` — Due diligence, reports
- `daily-logs` — Trade journal

### Content Creator Workspace

```bash
openclaw skill run qmd-memory template content
```

Creates:
- `articles` — Published content
- `drafts` — Work in progress
- `research` — Source material
- `ideas` — Brainstorms, notes

### Developer Workspace

```bash
openclaw skill run qmd-memory template developer
```

Creates:
- `docs` — Documentation
- `notes` — Technical notes
- `decisions` — ADRs, architecture decisions
- `snippets` — Code snippets, examples

---

## 📈 COST SAVINGS CALCULATOR

Run this to see your estimated savings:

```bash
openclaw skill run qmd-memory calculate-savings
```

Output:
```
Your Current API Memory Costs (estimated):
  memory_search calls/day:     ~75
  Average cost per call:       $0.03
  Monthly API cost:            $67.50

With QMD Local:
  Monthly cost:                $0.00

YOUR MONTHLY SAVINGS:          $67.50
YOUR ANNUAL SAVINGS:           $810.00

ROI on skill purchase:         40x (if skill was $20)
```

---

## 🛠️ TECHNICAL DETAILS

### Models Used (Auto-Downloaded)

| Model | Purpose | Size |
|-------|---------|------|
| embeddinggemma-300M-Q8_0 | Vector embeddings | ~300MB |
| qwen3-reranker-0.6b-q8_0 | Re-ranking results | ~640MB |
| qmd-query-expansion-1.7B-q4_k_m | Query expansion | ~1.1GB |

Total: ~2GB (one-time download)

### System Requirements

- Node.js >= 22
- ~3GB disk space (models + index)
- ~2GB RAM during embedding (then minimal)

### Where Data is Stored

```
~/.cache/qmd/
├── index.sqlite      # Search index
├── models/           # GGUF models
└── mcp.pid           # MCP server PID (if running)
```

---

## 🤝 SUPPORT

**Questions?** 
- GitHub Issues: github.com/asabove/qmd-memory-skill
- Discord: As Above community
- Email: support@asabove.tech

**Found it valuable?**
- Star us on ClawHub
- Share with other OpenClaw users
- Subscribe to our newsletter for more agent optimization tips

---

## 📜 LICENSE

MIT — Use freely, modify as needed.

QMD itself is created by Tobi Lütke (github.com/tobi/qmd).
This skill provides easy OpenClaw integration.

---

*"Stop paying for memory. Start compounding knowledge."*

**As Above Technologies** — Agent Infrastructure for Humans
