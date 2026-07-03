---
name: tdai-memory-suite
description: "Complete local memory system for OpenClaw: 4-layer memory pipeline (L0→L1→L2→L3) + local vector search (nomic-embed-text) + ontology knowledge graph + Nomic Atlas interactive visualization. Everything runs locally — no external API dependencies for memory extraction."
version: 1.0.0
tags: ["memory", "long-term-memory", "embedding", "vector", "ontology", "knowledge-graph", "nomic", "visualization", "persona", "sqlite"]
author: paudyyin
---

# TDaí Memory Suite

A complete, fully-local memory system for OpenClaw agents. Four components work together to give your AI agent persistent memory, semantic search, structured knowledge, and visual introspection.

## Components

### 1. TDaí Core — 4-Layer Memory Pipeline

**Path:** `components/tdai-core/`

The heart of the system. Automatically captures conversations and extracts structured memories through a 4-layer pipeline:

| Layer | Name | Description |
|-------|------|-------------|
| L0 | Conversation Recording | Raw message capture → SQLite + JSONL |
| L1 | Memory Extraction | LLM extracts structured memories (persona/episodic/instruction) with vector dedup |
| L2 | Scene Induction | LLM归纳场景块 (Scene Blocks) from conversation clusters |
| L3 | User Persona | LLM generates/updates user personality profile → persona.md |

**Key features:**
- Gateway-integrated LLM extraction (no separate API key needed)
- Local SQLite + sqlite-vec storage backend
- Optional Tencent Cloud Vector Database backend
- Auto-recall: semantic search injects relevant memories into system context
- BM25 + vector hybrid search

**Memory types:**
- **persona**: Stable user attributes, preferences, skills, values
- **episodic**: Actions, decisions, plans, outcomes that occurred
- **instruction**: Long-term behavioral rules the user set for the AI

### 2. TDaí Vector — Local Vector Search

**Configuration:** `memorySearch.provider: "local"`

Uses `nomic-embed-text-v1.5.Q4_K_M.gguf` (quantized, ~270MB) for fully-local embeddings. No external embedding API needed.

**Setup:**
1. Download the model to your OpenClaw models directory
2. Set `memorySearch.provider: "local"` in `openclaw.json`
3. The system automatically uses local embeddings for memory search

### 3. TDaí Ontology — Knowledge Graph

**Path:** `components/tdai-ontology/`

Typed knowledge graph for structured agent memory. Stores entities and relationships as JSONL with schema validation.

**Supported entity types:**
- People: `Person`, `Organization`
- Work: `Project`, `Task`, `Goal`
- Time/Place: `Event`, `Location`
- Information: `Document`, `Note`, `Message`
- Meta: `Technology`, `Skill`, `Action`, `Policy`

**Key features:**
- Entity CRUD with constraint validation
- Relation creation with cardinality checks
- Auto-sync from daily memory files
- Backup memory fallback when primary search fails
- CLI tools: `ontology.py` and `ontology_sync.py`

### 4. TDaí Atlas — Memory Visualization

**Path:** `components/tdai-atlas/nomic_atlas_visualizer.py`

Interactive HTML visualization of your agent's memory using sentence-transformers + UMAP dimensionality reduction.

**Features:**
- 768-dimensional semantic embeddings via nomic-embed-text-v1.5
- UMAP projection to 2D
- Interactive HTML output (zoom, pan, hover for details)
- Fully local — no data leaves your machine
- TF-IDF fallback when model unavailable

## Installation

### Option A: Full Suite (Recommended)

```bash
clawhub install tdai-memory-suite
```

### Option B: Individual Components

```bash
# Core memory pipeline (required)
clawhub install tdai-core

# Ontology knowledge graph (optional)
clawhub install tdai-ontology

# Atlas visualization (optional)
clawhub install tdai-atlas
```

## Configuration

### Minimal Setup (TDaí Core only)

Add to your `openclaw.json`:

```json
{
  "plugins": {
    "allow": ["mx", "memory-tencentdb"],
    "load": {
      "paths": ["<path-to-tdai-core>"]
    },
    "entries": {
      "memory-tencentdb": {
        "enabled": true,
        "config": {
          "pipeline": {
            "everyNConversations": 3,
            "enableWarmup": true,
            "l1IdleTimeoutSeconds": 10
          }
        }
      }
    }
  }
}
```

### Full Setup (Core + Local Vector + Ontology)

```json
{
  "plugins": {
    "allow": ["mx", "memory-tencentdb"],
    "load": {
      "paths": ["<path-to-tdai-core>"]
    },
    "entries": {
      "memory-tencentdb": {
        "enabled": true,
        "config": {
          "pipeline": {
            "everyNConversations": 3,
            "enableWarmup": true,
            "l1IdleTimeoutSeconds": 10
          },
          "store": {
            "backend": "sqlite"
          }
        }
      }
    }
  },
  "memorySearch": {
    "provider": "local",
    "model": "nomic-embed-text-v1.5.Q4_K_M.gguf"
  }
}
```

### Ontology Auto-Sync (Cron)

```json
{
  "name": "Ontology Daily Sync",
  "schedule": { "kind": "cron", "expr": "0 22 * * *", "tz": "Asia/Shanghai" },
  "payload": {
    "kind": "agentTurn",
    "message": "Run ontology sync: python scripts/ontology_sync.py --days 7"
  },
  "sessionTarget": "isolated"
}
```

## Usage Examples

### Memory Search (automatic after installation)

Memories are automatically recalled and injected into context. You can also search manually:

```
"Search my memories for information about project X"
"What do you remember about my preferences?"
```

### Ontology Operations

```bash
# Create an entity
python components/tdai-ontology/scripts/ontology.py create --type Project --props '{"name":"New Product","status":"active"}'

# Query entities
python components/tdai-ontology/scripts/ontology.py query --type Task --where '{"status":"open"}'

# Create relations
python components/tdai-ontology/scripts/ontology.py relate --from proj_001 --rel has_task --to task_001

# Auto-sync from memory files
python components/tdai-ontology/scripts/ontology_sync.py --days 7
```

### Memory Visualization

```bash
# Generate interactive visualization
python components/tdai-atlas/nomic_atlas_visualizer.py

# Output: output/memory_visualization.html
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    TDaí Memory Suite                         │
├─────────────┬──────────────┬──────────────┬────────────────┤
│  TDaí Core  │ TDaí Vector  │ TDaí Ontology│  TDaí Atlas    │
│  (L0→L3     │ (nomic-embed │ (Knowledge   │  (UMAP +       │
│  Pipeline)  │  -text local)│  Graph)      │   HTML viz)    │
├─────────────┼──────────────┼──────────────┼────────────────┤
│ SQLite+FTS  │ GGUF Model   │ JSONL+Schema │ sentence-      │
│ JSONL Store │ BM25+Vector  │ Entity/Rel   │ transformers   │
└─────────────┴──────────────┴──────────────┴────────────────┘
         │              │              │              │
         └──────────────┴──────┬───────┴──────────────┘
                               │
                    ┌──────────┴──────────┐
                    │  OpenClaw Gateway    │
                    │  (LLM Extraction)    │
                    └─────────────────────┘
```

## Memory Fallback Hierarchy

When searching for memories, the system follows this priority:

1. **TDaí Core** (`tdai_memory_search`) — primary structured memory
2. **TDaí Ontology** (graph query) — structured entities and relations
3. **TDaí Atlas** (visualization) — for browsing and exploration

## Requirements

- OpenClaw Gateway with model configured (for LLM extraction)
- Node.js v18+ (for Core plugin)
- Python 3.9+ (for Ontology and Atlas scripts)
- ~300MB disk for nomic-embed-text model (optional, for local vector search)

## Troubleshooting

### L1 extraction returns empty
1. Check `plugins.allow` includes `"memory-tencentdb"`
2. Check `plugins.load.paths` points to the correct directory
3. Verify Gateway model is configured (`models.providers` and `agents.defaults.model`)

### Local vector search not working
1. Ensure model file exists: `nomic-embed-text-v1.5.Q4_K_M.gguf` in models directory
2. Check `memorySearch.provider` is set to `"local"`
3. Restart Gateway after config changes

### Ontology sync fails
1. Ensure `memory/ontology/` directory exists
2. Check Python dependencies: `pip install --user pyyaml`
3. Run with `--dry-run` to preview changes

## License

MIT

## Changelog

### v1.0.0 (2026-06-09)
- Initial release
- TDaí Core v0.3.8: 4-layer pipeline with Gateway-integrated LLM extraction
- TDaí Vector: local nomic-embed-text embeddings
- TDaí Ontology: typed knowledge graph with 20+ entity types
- TDaí Atlas: interactive memory visualization with UMAP
