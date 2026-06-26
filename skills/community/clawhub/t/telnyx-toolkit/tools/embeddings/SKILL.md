---
name: telnyx-embeddings
description: Text-to-vector embeddings and semantic search using Telnyx AI. Generate embedding vectors via an OpenAI-compatible API — no OpenAI or Google API keys required.
metadata: {"openclaw":{"emoji":"🔮","requires":{"bins":["python3"],"env":["TELNYX_API_KEY"]},"primaryEnv":"TELNYX_API_KEY"}}
---

# Telnyx Embeddings

Generate embedding vectors from text using Telnyx's OpenAI-compatible AI API. Convert any text to high-dimensional vectors for similarity comparisons, clustering, classification, or building custom search indexes — all with just a `TELNYX_API_KEY`. No OpenAI or Google API keys required.

## Requirements

- **Python 3.8+** — stdlib only, no external dependencies
- **TELNYX_API_KEY** — get yours at [portal.telnyx.com](https://portal.telnyx.com/#/app/api-keys)

## Quick Start

```bash
export TELNYX_API_KEY="KEY..."
python3 {baseDir}/tools/embeddings/embed.py "Hello, world!"
```

That's it. No pip install, no setup wizard, no external provider keys.

## Text-to-Vector Embedding

Generate embedding vectors for any text input. The API is OpenAI-compatible, so existing integrations work out of the box.

### Basic Usage

```bash
# Embed text (uses thenlper/gte-large by default)
./embed.py "text to embed"

# Use a specific model
./embed.py "text to embed" --model intfloat/multilingual-e5-large

# Read from file
./embed.py --file input.txt

# Pipe from stdin
echo "text to embed" | ./embed.py --stdin

# JSON output (for scripting)
./embed.py "text" --json

# List available models
./embed.py --list-models
```

### Available Models

| Model | Description |
|-------|-------------|
| `thenlper/gte-large` | General text embeddings (default) |
| `intfloat/multilingual-e5-large` | Multilingual text embeddings |

### OpenAI-Compatible Client

The embeddings API is OpenAI-compatible, so you can use the OpenAI Python SDK with `base_url` pointed at Telnyx:

```python
from openai import OpenAI

client = OpenAI(
    api_key="KEY...",
    base_url="https://api.telnyx.com/v2/ai/openai"
)

response = client.embeddings.create(
    model="thenlper/gte-large",
    input="Hello, world!"
)
print("Dimensions:", len(response.data[0].embedding))
```

### From Python (Direct)

```python
from embed import embed_text

result = embed_text("your text here")
for item in result.get("data", []):
    vector = item["embedding"]       # list of floats
    dims = item["dimensions"]        # vector dimensionality
    print(f"{dims}-dimensional vector")
```

## Bucket Search

Search any Telnyx Storage bucket using natural language. Upload files, trigger server-side embedding, then run similarity search — the query embedding happens server-side too.

### Search

```bash
# Search with default bucket (from config.json)
./search.py "what are the project requirements?"

# Search a specific bucket
./search.py "meeting notes" --bucket my-bucket

# Get more results
./search.py "API rate limits" --num 10

# JSON output (for scripting)
./search.py "deployment steps" --json

# Custom timeout
./search.py "long query" --timeout 45

# Full content (no truncation)
./search.py "details" --full
```

### Output Format

Results are ranked by certainty score with confidence indicators:

```
--- Result 1 [HIGH] (certainty: 0.923) ---
Source: docs/requirements.md

The project requires Python 3.8+ and a valid Telnyx API key...

--- Result 2 [MED] (certainty: 0.871) ---
Source: notes/planning.md

We discussed the requirements in the planning meeting...
```

Confidence levels: `[HIGH]` >= 0.90, `[MED]` >= 0.85, `[LOW]` < 0.85

### From Python

```python
from search import search, similarity_search

# Quick search (returns formatted text)
print(search("your query", bucket_name="my-bucket"))

# Get structured results
results = similarity_search("your query", num_docs=5, bucket_name="my-bucket")
for doc in results.get("data", []):
    print(doc["source"], doc["certainty"])
    print(doc["content"][:200])
```

## Index Content

Upload files to a Telnyx Storage bucket and trigger embedding so they become searchable.

### Upload Files

```bash
# Upload a single file
./index.py upload path/to/file.md

# Upload to a specific bucket
./index.py upload path/to/file.md --bucket my-bucket

# Upload with a custom key (filename in bucket)
./index.py upload path/to/file.md --key docs/custom-name.md

# Upload all markdown files from a directory
./index.py upload path/to/dir/ --pattern "*.md"

# Upload all files from a directory
./index.py upload path/to/dir/
```

### Trigger Embedding

After uploading files, trigger the embedding process to make them searchable:

```bash
# Embed files in default bucket
./index.py embed

# Embed files in a specific bucket
./index.py embed --bucket my-bucket
```

### Check Embedding Status

```bash
./index.py status <task_id>
```

### List Files and Buckets

```bash
# List files in default bucket
./index.py list

# List files in a specific bucket
./index.py list --bucket my-bucket

# List files with a prefix filter
./index.py list --prefix docs/

# Show embedding status for a bucket
./index.py list --embeddings

# List all embedded buckets
./index.py buckets
```

### Create a Bucket

```bash
./index.py create-bucket my-new-bucket

# With a specific region
./index.py create-bucket my-new-bucket --region us-central-1
```

### Delete a File

```bash
./index.py delete filename.md
./index.py delete filename.md --bucket my-bucket
```

## Workflow

The typical workflow for making content searchable via bucket search:

```
1. Upload files          2. Trigger embedding       3. Search
   ./index.py upload        ./index.py embed           ./search.py "query"
        |                        |                          |
        v                        v                          v
   Telnyx Storage  --->  Telnyx AI Embeddings  --->  Similarity Search
   (S3-compatible)       (server-side vectors)       (server-side matching)
```

### Step-by-step Example

```bash
# 1. Create a bucket for your content
./index.py create-bucket my-knowledge

# 2. Upload files
./index.py upload ~/docs/ --pattern "*.md" --bucket my-knowledge

# 3. Trigger embedding (converts files to searchable vectors)
./index.py embed --bucket my-knowledge

# 4. Wait 1-2 minutes for embedding to process

# 5. Search!
./search.py "how do I deploy?" --bucket my-knowledge
```

## Configuration

Edit `config.json` to set defaults:

```json
{
  "bucket": "openclaw-main",
  "region": "us-central-1",
  "default_num_docs": 5
}
```

| Field | Default | Description |
|-------|---------|-------------|
| `bucket` | `openclaw-main` | Default bucket for search and index operations |
| `region` | `us-central-1` | Telnyx Storage region |
| `default_num_docs` | `5` | Default number of search results |

All settings can be overridden with CLI flags (`--bucket`, `--num`).

## Integration

### From Other Tools/Bots

```bash
# Embed text and capture vector
vector=$(python3 {baseDir}/tools/embeddings/embed.py "your text" --json)

# Search and capture results
results=$(python3 {baseDir}/tools/embeddings/search.py "your query" --json)

# Upload and index a file
python3 {baseDir}/tools/embeddings/index.py upload /path/to/file.md --bucket my-bucket
python3 {baseDir}/tools/embeddings/index.py embed --bucket my-bucket
```

### From Python

```python
import subprocess, json

# Embed text
result = subprocess.run(
    ["python3", "{baseDir}/tools/embeddings/embed.py", "your text", "--json"],
    capture_output=True, text=True
)
vector = json.loads(result.stdout)

# Search
result = subprocess.run(
    ["python3", "{baseDir}/tools/embeddings/search.py", "your query", "--json"],
    capture_output=True, text=True
)
data = json.loads(result.stdout)
```

### Replacing OpenAI/Google Memory Search

If your bot uses `memory_search` with OpenAI or Google embeddings, switch to:

```bash
# Before (requires OPENAI_API_KEY):
# memory_search("query")

# After (only needs TELNYX_API_KEY):
python3 {baseDir}/tools/embeddings/search.py "query" --bucket your-memory-bucket --json
```

## Relationship to RAG Tool

This tool is **complementary** to `tools/rag/`, not a replacement:

| Feature | Embeddings (this tool) | RAG (`tools/rag/`) |
|---------|----------------------|-------------------|
| **Purpose** | Text-to-vector + search primitives | Full RAG pipeline |
| **Search** | Direct similarity search | Retrieve + rerank + generate |
| **Indexing** | Upload + embed trigger | Auto-sync + smart chunking |
| **Q&A** | No (returns raw results) | Yes (LLM-powered answers) |
| **Use case** | Vectors, standalone search, integrations | Workspace-level knowledge base |

Use **embeddings** when you need vectors or simple search. Use **RAG** when you need AI-powered answers with source citations.

## Troubleshooting

### "No Telnyx API key found"
Set your API key:
```bash
export TELNYX_API_KEY="KEY..."
# or
echo 'TELNYX_API_KEY=KEY...' > .env
```

### "HTTP 401" or "HTTP 403"
Your API key is invalid or expired. Get a new one at [portal.telnyx.com](https://portal.telnyx.com/#/app/api-keys).

### "HTTP 404" on search
The bucket doesn't exist or embeddings haven't been enabled:
```bash
./index.py create-bucket your-bucket
./index.py embed --bucket your-bucket
```

### "No results found"
- Wait 1-2 minutes after triggering embedding
- Check that files were uploaded: `./index.py list --bucket your-bucket`
- Verify embeddings are active: `./index.py list --embeddings --bucket your-bucket`

### "Network error"
Check your internet connection. The tool needs access to `api.telnyx.com` and `*.telnyxcloudstorage.com`.

## Credits

Built for [OpenClaw](https://github.com/openclaw/openclaw) using [Telnyx Storage](https://telnyx.com/products/cloud-storage) and AI APIs.
