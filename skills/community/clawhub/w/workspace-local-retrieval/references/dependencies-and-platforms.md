# Dependencies and Platforms

Read this file when the user wants the skill to be runnable, reproducible, or publish-ready across macOS, Linux, and Windows.

## Goal

Keep the retrieval architecture portable while still declaring concrete dependencies.

This skill does **not** require one fixed backend. Instead, declare a supported baseline stack and make swaps explicit.

## Supported baseline stack

Use this baseline unless the user already has a different local stack:

- **Python**: 3.10+
- **Node.js**: 20+
- **SQLite**: 3.40+ with FTS5 preferred
- **Embedding backend**: one of
  - local Ollama embedding model
  - local GGUF embedding service already exposed through a wrapper
  - remote embedding API only if the user explicitly wants non-local fallback

## Why these dependencies exist

- **Python** is useful for deterministic indexing, file walking, chunking, and maintenance scripts.
- **Node.js** is useful for agent-facing wrappers and OpenClaw-adjacent script flows.
- **SQLite** gives a portable local keyword index and metadata store.
- **Embedding backend** provides semantic recall; keep it swappable.

## Baseline runtime dependencies to declare

Declare these requirements in the skill or the generated project:

### Required

- Python 3.10+
- Node.js 20+
- SQLite 3.40+ or Python `sqlite3` linked against a build with FTS enabled

### Recommended

- `sqlite-utils` or direct `sqlite3` usage for inspection
- a local embedding provider such as Ollama
- one stable embedding model name stored in config

### Optional

- `jq` for inspection and debugging
- `rg` for fast lexical fallback or smoke tests

## Python package baseline

If the generated implementation includes Python indexing scripts, a conservative baseline is:

```text
pydantic>=2,<3
orjson>=3,<4 ; platform_system != "Windows"
```

Use the standard library for as much as possible. Do not add heavy Python dependencies unless there is a real need.

## Node package baseline

If the generated implementation includes a Node wrapper, a conservative baseline is:

```json
{
  "type": "module",
  "engines": {
    "node": ">=20"
  }
}
```

Add package dependencies only if the wrapper actually needs them.

## SQLite notes

Prefer:
- SQLite with FTS5 support
- one local `.sqlite` file under `retrieval/indexes/`
- separate tables for documents, chunks, and refresh metadata

### macOS

- system Python usually includes `sqlite3`, but the linked SQLite version may vary
- Homebrew SQLite can be newer than the system one
- check FTS support before relying on it

### Linux

- distro packages often work well
- SQLite version and FTS support can vary by distro and age
- on older distros, pin or document the minimum version more explicitly

### Windows

- Python `sqlite3` often works fine, but path handling and shell examples differ
- avoid Bash-only instructions in the default workflow
- prefer Python scripts over shell pipelines for portable maintenance tasks

## Embedding backend options

### Option A — Ollama local embeddings

Good default for cross-platform local use if the user already runs Ollama.

Pros:
- local
- simple HTTP interface
- macOS / Linux / Windows support

Cons:
- requires Ollama install and model pull
- model names can vary

Suggested config fields:

```json
{
  "embeddingProvider": "ollama",
  "embeddingModel": "nomic-embed-text",
  "embeddingEndpoint": "http://127.0.0.1:11434/api/embeddings"
}
```

### Option B — local GGUF-backed embedding service

Good when the user already has a local embedding service stack.

Pros:
- local-first
- can align with an existing workstation setup

Cons:
- less standardized than Ollama
- harder to document portably unless the service contract is fixed

Suggested config fields:

```json
{
  "embeddingProvider": "local-service",
  "embeddingModel": "embeddinggemma-300m",
  "embeddingEndpoint": "http://127.0.0.1:8000/embed"
}
```

### Option C — remote API fallback

Use only when the user explicitly accepts network dependency and cost.

Pros:
- simple to start
- predictable quality

Cons:
- not local-first
- privacy and cost tradeoffs
- rate limits

## Cross-platform guidance

To keep the skill portable:

- prefer Python for environment checks and maintenance scripts
- avoid assuming Bash, GNU coreutils, or Homebrew
- store all backend settings in config files
- do not hard-code `/usr/local/...` paths
- normalize paths through Python or Node path libraries
- make embedding provider selection explicit in config

## Publish-safe dependency stance

For a public skill, separate these clearly:

- **required runtime dependencies**
- **recommended local tooling**
- **optional backend choices**

Do not pretend a local retrieval system is dependency-free.
But also do not hard-code one private stack if portability matters.
