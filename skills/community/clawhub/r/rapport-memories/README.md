# Rapport Memories - Semantic Memory Extension

`rapport-memories` is a semantic Retrieval-Augmented Generation (RAG) memory extension for OpenClaw agents. It indexes the agent's persistent memories (`MEMORY.md` and `memory/*.md`) into a structured SQLite database and calculates vector embeddings stored in a ChromaDB database, allowing the agent to recall decisions, conversations, and taxonomies.

---

## ⚠️ CRITICAL REQUIREMENT: Docker Sandbox Image

Because ChromaDB compiles native binary libraries (e.g., SQLite extensions, `hnswlib`, `bcrypt`) and requires specific system dependencies, **you must build and install the sandbox Docker image before running this skill.** 

Running the skill within its dedicated Docker sandbox isolates these native dependencies and prevents compatibility issues with externally-managed Python environments on the host system.

### 1. Build or Pull the Docker Image
You can pull the pre-built image directly from Docker Hub:

```bash
docker pull carlosdelfino/rapport-openclaw-sandbox:latest
```

Alternatively, build it locally from the root of your workspace:

```bash
cd skills/rapport-memories
docker build -t carlosdelfino/rapport-openclaw-sandbox:latest .
```

### 2. Configure OpenClaw Sandbox
To use this skill, configure your OpenClaw agent or workspace to run the `rapport-memories` skill inside the sandbox container:

* Set the sandbox image for the skill to: `carlosdelfino/rapport-openclaw-sandbox:latest`
* Ensure the agent's active workspace directory is mounted to `/workspace` inside the container.

---

## Technical Features

1. **Structured Metadata Registry**: SQLite tracks file paths, modification times, and content hashes to ensure fast, incremental indexing (only new or modified files are processed).
2. **Text Sanitisation**: A built-in sanitiser strips markdown code blocks, raw JSON lines, diagnostic outputs, and common security keywords (API keys, passwords, credentials) before generating embeddings to prevent leaks.
3. **Semantic Vector Search**: Uses ChromaDB and an Ollama embedding model to run similarity searches.
4. **Resilient Fallback**: If ChromaDB or Ollama is unreachable, the skill automatically falls back to SQLite keyword search using Full-Text Search (FTS5), ensuring the agent never crashes.

---

## Configuration

The skill is configured via the following environment variables:

| Environment Variable | Default Value | Description |
|---|---|---|
| `RAPPORT_MEMORIES_STORE_PATH` | `/workspace/.rapport-memories` | Path where the SQLite DB and Chroma files are stored |
| `RAPPORT_MEMORIES_EMBEDDING_MODEL` | `nomic-embed-text-v2-moe:latest` | The Ollama model used to generate text embeddings |
| `OLLAMA_HOST` | `http://host.docker.internal:11434` | The URL of the Ollama server (Docker host address) |
| `RAPPORT_MEMORIES_CHUNK_SIZE` | `500` | Target character size for text chunks |

---

## Usage

### 1. Command Line Interface (CLI)

When running inside the Docker sandbox, you can execute the CLI commands directly. Here are examples of how to run them locally using docker:

#### Initialize Database
```bash
docker run --rm -v $(pwd):/workspace carlosdelfino/rapport-openclaw-sandbox:latest /skills/rapport-memories/scripts/memory_rag.py init
```

#### Index Workspace Memories
Searches for `MEMORY.md` and `memory/*.md` files (and agent subfolders) and runs incremental indexing:
```bash
docker run --rm -v $(pwd):/workspace carlosdelfino/rapport-openclaw-sandbox:latest /skills/rapport-memories/scripts/memory_rag.py index
```

#### Add a New Memory Entry
Writes a formatted Markdown file under `/workspace/memory/<date>_my_topic.md` and indexes it:
```bash
docker run --rm -v $(pwd):/workspace \
  -e OLLAMA_HOST=http://host.docker.internal:11434 \
  carlosdelfino/rapport-openclaw-sandbox:latest /skills/rapport-memories/scripts/memory_rag.py add \
  --title "Database Migration Decision" \
  --content "We decided to migrate the primary catalogue to PostgreSQL with pgvector for scalability." \
  --taxonomy "decision"
```

#### Semantic Search
```bash
docker run --rm -v $(pwd):/workspace \
  -e OLLAMA_HOST=http://host.docker.internal:11434 \
  carlosdelfino/rapport-openclaw-sandbox:latest /skills/rapport-memories/scripts/memory_rag.py search "database migration" --limit 3 --threshold 0.55
```

#### Display Statistics
```bash
docker run --rm -v $(pwd):/workspace carlosdelfino/rapport-openclaw-sandbox:latest /skills/rapport-memories/scripts/memory_rag.py stats
```

---

### 2. Python Library Interface

Agents and scripts can import `MemoryRAG` directly to interact programmatically:

```python
from skills.rapport_memories import MemoryRAG

# Initialize the manager (reads env variables for configuration)
memory_rag = MemoryRAG()

# Index current workspace memories
indexing_stats = memory_rag.index_memory_files()
print(f"Indexed: {indexing_stats['indexed']} files.")

# Add a memory entry dynamically
file_path = memory_rag.add_memory_entry(
    title="Session 3 Summary",
    content="Aligned on task delegation rules and added Docker sandbox instructions.",
    taxonomy="conversation"
)

# Semantically query memories
results = memory_rag.semantic_search(
    query="what did we decide about docker sandboxes?",
    limit=3,
    threshold=0.6
)

for result in results:
    print(f"Similarity Score: {result.score:.4f}")
    print(f"Source file: {result.metadata.get('file_path')}")
    print(f"Content:\n{result.content}\n---")
```
