---
name: ultramemory
description: Structured AI agent memory with temporal versioning, relational tracking, and semantic search. Use when storing facts, recalling context, searching past conversations, tracking how knowledge changed over time, or building entity profiles. Replaces flat MEMORY.md with atomic fact extraction, update/contradict/extend relations, and hybrid semantic+temporal search. Use for any "remember this", "what do I know about X", "when did this change", or cross-session knowledge retrieval.
requirements:
  python: ">=3.10"
  packages:
    - ultramemory
  env:
    - name: ANTHROPIC_API_KEY
      required: true
      description: "Required for LLM fact extraction during ingest. Alternatively set OPENAI_API_KEY."
    - name: ULTRAMEMORY_DB
      required: false
      description: "Path to SQLite database file. Defaults to ./memory.db"
---

# Ultramemory

Structured agent memory: extracts atomic facts from text, detects relations to existing knowledge (updates, contradicts, extends), embeds for semantic search, and auto-builds entity profiles.

PyPI: `ultramemory` | GitHub: `jared-goering/ultramemory`

## Setup

```bash
# Install (creates venv automatically on first run)
pip install ultramemory

# Or from source
git clone https://github.com/jared-goering/ultramemory.git
cd ultramemory && pip install -e .
```

**Requirements:**
- Python 3.10+
- An LLM API key for fact extraction (Anthropic recommended, OpenAI also works)
- Local embeddings load automatically (sentence-transformers/all-MiniLM-L6-v2, ~80MB first run)

**Environment:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."  # or OPENAI_API_KEY
export ULTRAMEMORY_DB="./memory.db"    # default: memory.db in current dir
```

## Quick Start

```python
from ultramemory import MemoryEngine

engine = MemoryEngine(db_path="memory.db")

# Ingest text (extracts atomic facts, detects relations, builds profiles)
results = engine.ingest("Jared moved from Bel Aire to Wichita. The baby is due in July.")

# Search
matches = engine.search("Where does Jared live?", top_k=5)

# Recall (compact context block for agent prompts)
context = engine.recall("current projects and priorities", top_k=5)
```

## CLI Usage

The `scripts/memory.sh` wrapper handles venv activation and API key loading.

### Store memories (ingest)

```bash
bash scripts/memory.sh ingest \
  "Jared moved to Wichita. The baby is now due in August, not July." \
  --session "main-2026-03-22" --agent kit
```

Categories: `person`, `preference`, `project`, `decision`, `event`, `insight`

Relations auto-detected: `updates` (supersedes old fact), `contradicts`, `extends`, `supports`, `derives`

When a memory `updates` an existing one, the old memory is marked `superseded` and the new one gets an incremented version.

### Recall (agent-optimized search)

Compact context block for injecting into agent prompts:

```bash
bash scripts/memory.sh recall "Where does Jared live?" --top-k 5
```

Output:
```
[person] Jared moved to Wichita. (v2, current, 89% match)
  -> updates: Jared lives in Bel Aire, KS.
[project] Jared teaches Human-Centric Design at WSU. (v1, current, 72% match)
```

### Search (full JSON)

```bash
bash scripts/memory.sh search "baby due date" --top-k 10
# Include superseded memories:
bash scripts/memory.sh search "baby due date" --all
# Time travel: what did we know on March 1?
bash scripts/memory.sh search "baby due date" --as-of 2026-03-01
```

### Entity operations

```bash
bash scripts/memory.sh entities          # List all known entities
bash scripts/memory.sh history Jared     # Version timeline
bash scripts/memory.sh profile Jared     # Auto-built profile
bash scripts/memory.sh stats             # Counts, categories
```

## Integration Patterns

### Session startup

At the start of any session, hydrate context:
```bash
bash scripts/startup-recall.sh <agent-id>
```

### Post-conversation ingest

After meaningful conversations, pass the text directly:
```bash
bash scripts/memory.sh ingest "User decided to use React for the frontend. Budget is $50k." --session $SESSION_KEY --agent $AGENT_ID
```

### API Server

For multi-agent setups, run the API server (requires separate install from PyPI):
```bash
pip install ultramemory
python3 -m uvicorn ultramemory.server:app --port 8642 --host 127.0.0.1
```

Endpoints: `POST /api/ingest`, `POST /api/search`, `POST /api/recall`, `GET /api/stats`

### Advanced: Auto-ingest from session transcripts

For continuous ingestion from session files, see the [GitHub repo](https://github.com/jared-goering/ultramemory) which includes `auto_ingest.py` and `live_ingest.sh` scripts.

## Why Not Just Use MEMORY.md?

You'll outgrow a flat file fast. But you also can't replace it entirely. We tried.

At 18,000+ memories, search results get noisy. The DB is great at answering "what happened Tuesday?" but terrible as a session primer. Meanwhile, MEMORY.md is perfect for "who am I, who's my human, what are we working on" but can't hold 18K facts in 2K tokens.

The architecture we landed on uses three layers:

**Layer 1: MEMORY.md (always loaded, zero cost)**
Curated essentials under 2K tokens. Loaded every session, no API calls, no latency. Contains identity, active projects, key preferences. Think of it as working memory.

**Layer 2: Ultramemory plugin (opportunistic injection)**
When a message arrives, the plugin searches the DB and injects relevant memories if they score above a similarity threshold (we use 0.55). The agent never explicitly asks for this. It just gets richer context when the DB has something relevant.

**Layer 3: Ultramemory direct (precision recall)**
The agent explicitly searches when it needs specifics. "What was the benchmark result?" or "When did we decide to drop NYC?" This is the full 18K+ memory DB with semantic search, temporal filtering, and entity profiles.

MEMORY.md is the backup and the bootstrap. Ultramemory is the brain. You need both.

## Architecture

- **Storage:** Single SQLite DB with WAL mode. Agent-ID tagging for multi-agent isolation.
- **Extraction:** LLM extracts atomic facts, categorizes, detects entities, finds relations to existing memories.
- **Embeddings:** Local sentence-transformers (384-dim). No API calls for search.
- **Relations:** UPDATE, EXTEND, CONTRADICT, SUPPORT, DERIVE. Version chain with superseded tracking.
- **Profiles:** Auto-built entity profiles from accumulated facts.
- **Events:** Structured event extraction with canonical clustering and dedup.
- **Temporal:** Deterministic temporal expression parsing and date arithmetic (no LLM needed).

## Cost

- Ingest: ~$0.01-0.02 per call (3 LLM calls: extract, relate, profile)
- Search/recall: Free (local embeddings + SQLite)
- Embedding model: ~80MB download on first run, then cached

## Benchmark

80% accuracy on LongMemEval_s (production-relevant questions). 32ms median search latency.
