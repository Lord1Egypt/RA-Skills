# Agent Memory V12 — Internal Developer Guide

> **Version**: 12.0.0 | **Python**: ≥3.10 | **License**: MIT

This is the **internal** developer guide for the `agent_memory` package.
For user-facing documentation, see the [root README](../README.md) and [ARCHITECTURE.md](../ARCHITECTURE.md).

## What Is This Package?

Agent Memory is a **personal memory operating system** for AI agents.
It goes beyond passive storage — the **Spirit butler** proactively patrols, diagnoses, and repairs the memory store, while four specialized engines handle ingestion, retrieval, maintenance, and cognition.

## V12 Architecture Summary

### TEMPR Five-Lane Retrieval

Five parallel retrieval lanes fused via Reciprocal Rank Fusion (RRF, k=60):

| Lane | Method | Module |
|------|--------|--------|
| 1 | FTS5 + LIKE (structured full-text) | `fts_manager.py`, `store.py` |
| 1.5 | BM25 sparse retrieval | `bm25_index.py` |
| 2 | Semantic vector (vec0 / ChromaDB) | `embedding_store.py` |
| 3 | Entity expansion (relationship graph) | `entity.py` |
| 4 | Causal chain traversal (max depth 2) | `memory_links` via `recall_engine.py` |

### Four Engines

| Engine | File | Responsibility |
|--------|------|----------------|
| IngestEngine | `engines/ingest.py` | Dedup, quality scoring, auto-linking |
| RecallEngine | `engines/recall_engine.py` | TEMPR 5-lane retrieval + RRF + intent + MMR |
| MaintainEngine | `engines/maintain.py` | Lifecycle, decay, distillation |
| CognitionEngine | `engines/cognition.py` | Causal reasoning, knowledge graph |

### 13 Mixins

`AgentMemory` composes behavior via mixins in `mixins/`:

MemoryMixin · RecallMixin · SessionMixin · MaintenanceMixin · DistillMixin · EncyclopediaMixin · TimelineMixin · StatsMixin · PersonaMixin · RoleMixin · MediaStyleMixin · ReactorMixin · ExportMixin

### Spirit Butler

`spirit/` — Dual-LLM security protocol, natural language command interface, proactive health checks, cross-agent dedup, preference sync, memory partitioning. Isolated from core via `spirit/interface.py`.

## Module Directory

| Subpackage / Module | Description |
|----------------------|-------------|
| `engines/` | Four core engines + decay policy + curiosity + federation + feedback + metacognitive loop |
| `mixins/` | 13 behavior mixins composed into AgentMemory |
| `spirit/` | Spirit butler: commands, health checks, reports, LLM layer, proactive delivery |
| `storage/` | SQLite store, embedding store, CryptoStore, FTS manager, agent manager, cache |
| `config/` | Unified settings (env > JSON > defaults), schema.sql, dimension definitions |
| `collectors/` | Multi-source collectors: DingTalk, WeChat, Email, Calendar, File + scheduler |
| `enterprise/` | Audit log, compliance guard, knowledge distiller, offboarding, permission matrix, skill marketplace |
| `privacy/` | PII analyzer, consent management, guard, patterns, rules |
| `plugins/` | Plugin framework: auto-tagger, sentiment monitor, Obsidian sync, Slack notifier |
| `integration/` | LangChain connector, bridge utilities |
| `infra/` | Metrics collection |
| `tests/` | pytest test suite (see Testing below) |
| `protocols.py` | 7 ABC interfaces decoupling engine contracts from implementations |
| `container.py` | Dependency injection via ComponentContainer with lazy factory lambdas |
| `temporal.py` | Dual-timeline reasoning (valid_from/valid_until + occurrence/mention) |
| `entity.py` | Entity resolution: rule-based extraction, 3-level matching, alias index |
| `models.py` | Data models (MemoryInput, etc.) |
| `mcp_server.py` | MCP Server exposing 11 tools (stdio / streamable-http / HTTP fallback) |
| `cli.py` | Command-line interface (`agent-memory` entry point) |
| `server.py` | HTTP API server (`agent-memory-server` entry point) |
| `bm25_index.py` | BM25 sparse retrieval index |
| `embedding_store.py` | Vector storage (sqlite-vec / ChromaDB fallback) |
| `recall.py` | Legacy recall module (deprecated, use `engines/recall_engine.py`) |
| `pipeline.py` | Legacy ingest pipeline (deprecated, use `engines/ingest.py`) |
| `decay.py` | Legacy decay module (deprecated, use `engines/decay_policy.py`) |

## Development Setup

```bash
# Clone and install in editable mode with dev dependencies
pip install -e ".[dev]"

# With semantic search support (recommended)
pip install -e ".[dev,semantic]"

# Verify installation
python -c "from agent_memory import AgentMemory; print('OK')"
```

### Key Dependencies

- **Required**: `typing_extensions`, `sqlite-vec`
- **Optional**: `sentence-transformers` (semantic), `rank-bm25` (BM25), `jieba` (Chinese tokenization), `FlagEmbedding` (reranker), `fastapi`+`uvicorn` (web API), `asyncpg` (PostgreSQL), `cryptography` (encrypted storage)

All optional dependencies degrade gracefully — core functionality works without them.

## Testing

```bash
# Run full test suite
pytest

# Run with coverage (80% threshold)
pytest --cov=agent_memory --cov-report=term-missing

# Run a specific test file
pytest agent_memory/tests/test_recall.py -v

# Lint
ruff check agent_memory/

# Type check
mypy agent_memory/ --ignore-missing-imports
```

Test configuration lives in `pyproject.toml` under `[tool.pytest.ini_options]`.

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Mixin composition over inheritance** | 13 mixins compose into AgentMemory; each mixin is independently testable and replaceable |
| **Protocol interfaces (ABC)** | `protocols.py` defines 7 contracts decoupling engines from implementations — swap storage without touching engine logic |
| **Dependency injection via ComponentContainer** | Lazy factory lambdas avoid circular imports and enable per-test overrides |
| **TEMPR 5-lane RRF fusion** | No single retrieval method covers all queries; RRF combines structured, sparse, semantic, entity, and causal signals |
| **Dual timeline (temporal.py)** | Inspired by Zep (t_valid) and Hindsight (occurrence/mention) — facts have both validity periods and occurrence timestamps |
| **Graceful degradation** | Optional deps (sqlite-vec, transformers, jieba, cryptography) are checked at import time; missing deps produce warnings, not crashes |
| **SQLite + WAL as primary store** | Zero-config, single-file, concurrent reads — ideal for single-agent deployments |
| **CryptoStore as proxy** | Encryption is a transparent proxy over MemoryStore, not a separate store — no data duplication |
| **Spirit isolation** | Spirit butler communicates via `SpiritInterface`, never directly imports engine internals |

## Import Conventions

```python
# Public API (lazy-loaded, always use these)
from agent_memory import AgentMemory, MemoryInput

# Internal modules (use absolute imports within the package)
from agent_memory.engines.recall_engine import RecallEngine
from agent_memory.storage.sqlite_store import SqliteMemoryStore
from agent_memory.config.settings import get_settings
from agent_memory.protocols import MemoryStoreProtocol

# Check optional dependencies at runtime
from agent_memory import check_optional_deps
deps = check_optional_deps()  # {"sqlite_vec": True, "transformers": False, ...}
```

The public API (`AgentMemory`, `MemoryInput`) is lazy-loaded via `__getattr__` to avoid importing heavy dependencies on `import agent_memory`.
