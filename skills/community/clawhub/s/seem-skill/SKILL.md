---
name: SEEM
version: 0.1.0
description: Advanced episodic memory system for multi-turn conversations. Store and retrieve structured conversation memories with fact graph, PPR retrieval, and three recall modes (Lite/Pro/Max). Supports hybrid retrieval (dense + sparse), dynamic memory integration, and fact deduplication.
metadata: {"openclaw":{"emoji":"🧠","requires":{"bins":["python3","pip"],"env":["LLM_API_KEY","MM_ENCODER_API_KEY"]},"primaryEnv":"LLM_API_KEY"}}
---

# SEEM Skill

Structured Episodic & Entity Memory for multi-turn conversations.

## Quick Start

```python
from seem_skill import SEEMSkill, SEEMConfig, RecallMode

config = SEEMConfig()
skill = SEEMSkill(config)

# Store conversation
memory_id = skill.store({
    "text": "Lena asked about Scottish Terriers",
    "speaker": "Alice"
})

# Recall (default: LITE mode — facts + episodic memory, no raw chunks)
result = skill.recall({"text": "What did Lena ask?"}, top_k=3)
# result = {"memories": [...], "facts": [...]}

# Recall with raw chunks
result = skill.recall({"text": "What did Lena ask?"}, mode=RecallMode.PRO)

# Recall with backfill
result = skill.recall({"text": "What did Lena ask?"}, mode=RecallMode.MAX)
```

## Recall Modes

| Mode | Facts | Episodic Memory | Raw Chunks | Backfill |
|------|-------|-----------------|------------|----------|
| **Lite** (default) | ✅ | ✅ (summary + events) | ❌ | ❌ |
| **Pro** | ✅ | ✅ | ✅ (top_k) | ❌ |
| **Max** | ✅ | ✅ | ✅ (top_k + backfill ≤ 2×top_k) | ✅ |

- **Lite**: Lightest context. Facts + structured memory only. Best for LLM agents that want concise context.
- **Pro**: Includes raw observation text for the top_k retrieved chunks.
- **Max**: Full context with backfill from associated memories (up to 2×top_k chunks).

## Retrieval Strategies

| Strategy | Method | Best For |
|----------|--------|----------|
| **DPR** | Dense vector similarity | Simple keyword-matching queries |
| **Hybrid RRF** | Dense + BM25 sparse fusion | Mixed keyword + semantic queries |
| **PPR** | Personalized PageRank over knowledge graph | Multi-hop, entity-rich queries |

Default strategy is configured in `config.py` (currently `ppr`).

## Configuration

### Environment Variables (Recommended)

```bash
export LLM_API_KEY="sk-xxx"
export LLM_BASE_URL="https://api.deepseek.com"
export LLM_MODEL="deepseek-chat"

export MM_ENCODER_API_KEY="sk-xxx"
export MM_ENCODER_BASE_URL="https://api.siliconflow.cn/v1"
export MM_ENCODER_MODEL="Qwen/Qwen3-Embedding-8B"
```

### Unified Configuration File

All default settings are centralized in `seem_skill/config.py`:

```python
LLM_CONFIG = {
    "base_url": "https://api.deepseek.com",
    "model": "deepseek-chat",
}

EMBEDDING_CONFIG = {
    "base_url": "https://api.siliconflow.cn/v1",
    "model": "Qwen/Qwen3-Embedding-8B",
}
```

### Custom Configuration

Override defaults programmatically:

```python
config = SEEMConfig(
    llm_api_key="your-key",
    llm_model="custom-model",
    retrieve_strategy=RetrieveStrategy.PPR,
    top_k_facts=10,
    ppr_damping=0.6,
)
```

### Key Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `retrieve_strategy` | `hybrid_rrf` | DPR / Hybrid RRF / PPR |
| `top_k_chunks` | 3 | Number of chunks to retrieve |
| `top_k_facts` | 5 | Number of fact triples to retrieve |
| `top_k_candidates` | 3 | Integration candidate count |
| `rrf_rank_constant` | 30 | RRF smoothing constant |
| `ppr_damping` | 0.5 | PPR teleport probability |
| `backfill_chunks` | 5 | Max additional chunks per backfill |
| `enable_fact_graph` | True | Build fact graph on store |
| `entity_similarity_threshold` | 0.9 | Entity linking threshold |
| `enable_integration` | True | Dynamic memory integration |
| `integration_window` | 3 | Batch size for deferred integration |

## Operations

### Store

```bash
python scripts/cli_memory.py store --text "Your message" --speaker user
python scripts/cli_memory.py store --dialogue-id "D1:1" --speaker "Alice" --text "Message"
```

### Recall

```bash
python scripts/cli_memory.py recall --query "Your query" --mode lite
python scripts/cli_memory.py recall --query "Your query" --mode pro --strategy ppr --top-k 5
python scripts/cli_memory.py recall --query "Your query" --mode max --top-k-facts 10
```

### Facts (Knowledge Graph)

```bash
python scripts/cli_memory.py facts               # Show all fact triples
python scripts/cli_memory.py facts --entity 小米   # Filter by entity
```

### Display (Detailed)

```bash
python scripts/cli_memory.py display
python scripts/cli_memory.py display --dialogue-id "D1:1"
```

### View (Compact 5W1H)

```bash
python scripts/cli_memory.py view
```

### Stats

```bash
python scripts/cli_memory.py stats
```

### Clear

```bash
python scripts/cli_memory.py clear --yes
```

## Features

- **Episodic Memory Extraction**: LLM extracts structured summary + events (5W1H) from each turn
- **Fact Graph Construction**: Extracts subject-predicate-object triples, builds NetworkX knowledge graph
- **Fact Deduplication**: Two-stage dedup — normalized exact match (O(1)) + embedding similarity (threshold 0.93)
- **PPR Retrieval**: Personalized PageRank over entity-fact-chunk graph for graph-aware retrieval
- **Three Recall Modes**: Lite/Pro/Max controlling context granularity
- **Dynamic Integration**: Auto-merges related memories (MODERATE or STRONG coherence)
- **Hybrid Retrieval**: Dense (vector) + Sparse (BM25) with RRF fusion
- **Entity Linking**: Embedding-based entity normalization (threshold 0.9)
- **Multimodal Support**: Images participate in embedding and retrieval
- **LRU Cache**: Reduces repeated embedding computation
- **NetworkX Graph**: Full graph algorithms available (PPR, connected components, etc.)

## Architecture

**Store Pipeline:**
1. Chunk storage (raw observation)
2. Episodic extraction (LLM) → summary + events
3. Fact extraction from events → subject-predicate-object triples
4. Fact deduplication (exact match + embedding similarity)
5. Entity node creation and fact graph construction (NetworkX)
6. Multimodal embedding
7. Candidate retrieval (dense similarity)
8. Integration judgment (LLM, MODERATE or STRONG → integrate)
9. Memory merge/insert

**Recall Pipeline:**
1. Query encoding
2. Strategy routing (DPR / Hybrid RRF / PPR)
3. Chunk retrieval (strategy-specific, returns top_k chunks with scores)
4. Fact retrieval (vector similarity, returns top_k facts)
5. Result assembly (mode-dependent):
   - LITE: structured memory (summary + events) + facts
   - PRO: + raw chunks (top_k)
   - MAX: + backfill chunks (up to 2×top_k)

**Graph Structure (NetworkX DiGraph):**
- Node types: `entity`, `chunk`
- Edge types: `entity_chunk` (entity → chunk), `fact` (entity ↔ entity), `synonymy` (entity ↔ entity)
- Fact deduplication: normalized exact match + embedding similarity (threshold 0.93)

## File Structure

```
SEEM/
├── SKILL.md              # This file
├── README.md             # Quick reference
├── config.py             # Unified configuration (LLM + Embedding)
├── requirements.txt      # Python dependencies
├── __init__.py           # Package entry point
├── core/
│   ├── __init__.py
│   ├── seem_skill.py     # Core implementation (SEEMSkill class)
│   ├── schema.py         # Data structures (SEEMConfig, RecallMode, etc.)
│   ├── prompts.py        # LLM prompts
│   └── utils.py          # LLM client, embedding, BM25, cache
├── scripts/
│   └── cli_memory.py     # CLI: store, recall, facts, display, view, stats, clear
├── data/                 # Persistent storage (auto-created)
└── tests/
```

## Dependencies

- `openai>=1.0.0` — LLM and embedding API client
- `numpy>=1.21.0` — Vector operations
- `networkx>=3.0` — Knowledge graph, PPR, connected components
- `scipy>=1.0` — Required by `nx.pagerank()`
- `rank-bm25>=0.2.2` — BM25 sparse retrieval
- `nltk>=3.8.0` — Tokenization

## When to Use SEEM

- Multi-turn conversations need structured context preservation
- Complex event relationships exist across dialogue turns
- Need entity-centric retrieval (fact graph + PPR)
- Want control over context granularity (Lite/Pro/Max modes)
- Dynamic memory integration is valuable

## Troubleshooting

### API Key Errors

```
Error: Missing API keys
```

Set environment variables or update `config.py`:
```bash
export LLM_API_KEY="sk-xxx"
export MM_ENCODER_API_KEY="sk-xxx"
```

### PPR Requires scipy

```
ModuleNotFoundError: No module named 'scipy'
```

```bash
pip install scipy networkx
```
