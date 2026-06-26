---
name: memory-palace
description: Long-term memory system for AI agents using a file-based "palace" architecture with BGE-M3 vector search, metadata filtering, compound scoring (semantic + recency + importance), GraphRAG Lite neighbor expansion, and memory metabolism protocols. Use for: (1) Building agentic long-term memory from scratch, (2) Upgrading flat file memory with vector search and temporal weighting, (3) Managing agent knowledge with automatic consolidation, cold zone archiving, and structured reflection. Trigger on phrases like "long-term memory", "vector search", "agent memory", "memory management", "knowledge base for agent".
---

# Memory Palace

A file-based long-term memory system for AI agents, designed to be zero-infrastructure (no Docker, no external services).

## Architecture

```
palace/
├── grand_hall/          # Global navigation, room map, logs
├── chambers/            # Agent-specific knowledge (one per agent)
├── project_rooms/       # Long-running project storage
├── reflection_wing/     # Compiled insights: principles, kernels, patterns
├── dispatch_corridor/   # Task routing and status tracking
├── conflict_room/       # Conflict resolution records
└── archive_basement/    # Cold storage (excluded from default search)
```

## Quick Start

```bash
# 1. Initialize palace structure
mkdir -p palace/{grand_hall,chambers,project_rooms,reflection_wing,dispatch_corridor,conflict_room,archive_basement}

# 2. Install BGE-m3
pip install FlagEmbedding

# 3. Build index
python3 scripts/build_index_bge.py --force

# 4. Query
python3 scripts/query_bge.py "your search query"
python3 scripts/query_bge.py --type palace --priority high "query"
python3 scripts/query_bge.py --details "query"   # show sub-scores
python3 scripts/query_bge.py --raw "query"       # pure cosine (v2 compatibility)
```

## Search Scoring

Compound score = 0.5 × **Semantic** + 0.25 × **Recency** + 0.25 × **Importance**

- **Semantic**: BGE-m3 cosine similarity (clamped to [0,1])
- **Recency**: 30-day half-life decay based on file mtime
- **Importance**: `priority` field mapping (high=1.0, medium=0.6, low=0.3)

## Key Scripts

| Script | Purpose |
|--------|---------|
| `build_index_bge.py` | Build BGE-m3 vector index with incremental maintenance |
| `query_bge.py` | Search with compound scoring, metadata filter, raw mode |
| `graph_router.py` | Build 1-hop [[links]] neighbor graph |
| `cold_zone_blinding_patch.py` | Exclude archive_basement from search |

## Index Manifest Format

Each file in the manifest (`watchdog_manifest_v1.jsonl`) requires:
```json
{"path": "palace/chambers/01_agent/accumulated_knowledge.md", "type": "palace", "priority": "high"}
```

Fields: `path` (required), `type` (for metadata filtering), `priority` (for importance scoring).

## Memory Metabolism

See `references/memory_metabolism.md` for the full protocol:
- 3-tier upgrade path: Project Room → Reflection Wing → Constitution
- 5 output types: principle card, prompt kernel, failure pattern, thinking path, constitution candidate
- Reverse elimination rules for low-value content
