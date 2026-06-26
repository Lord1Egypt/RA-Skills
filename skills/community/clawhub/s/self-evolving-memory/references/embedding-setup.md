# Embedding Setup Guide

This skill uses semantic search (`memory_search`) to recall relevant memories. This requires an embedding model.

Choose the option that fits your setup.

---

## Option A: Ollama (local, recommended for privacy)

Run a local embedding model with no internet dependency and no API costs.

### 1. Install Ollama

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

Or download from [ollama.ai](https://ollama.ai).

### 2. Pull an embedding model

```bash
# Recommended: nomic-embed-text (fast, good quality)
ollama pull nomic-embed-text

# Alternatives
ollama pull mxbai-embed-large   # larger, higher quality
ollama pull all-minilm          # lightweight
```

### 3. Configure OpenClaw

In `openclaw.json`, under `agents.defaults.memorySearch`:

```json
{
  "memorySearch": {
    "enabled": true,
    "sources": ["memory"],
    "provider": "ollama",
    "model": "nomic-embed-text",
    "sync": {
      "onSessionStart": true,
      "onSearch": true,
      "watch": true
    }
  }
}
```

If Ollama is running on a **remote machine or NAS**:

```json
{
  "memorySearch": {
    "enabled": true,
    "sources": ["memory"],
    "provider": "ollama",
    "remote": {
      "baseUrl": "http://<your-ollama-host>:11434/ollama",
      "apiKey": ""
    },
    "model": "nomic-embed-text"
  }
}
```

---

## Option B: OpenAI Embeddings (cloud)

Uses OpenAI's `text-embedding-3-small` or `text-embedding-3-large`.

### Configure OpenClaw

```json
{
  "memorySearch": {
    "enabled": true,
    "sources": ["memory"],
    "provider": "openai",
    "model": "text-embedding-3-small",
    "remote": {
      "baseUrl": "https://api.openai.com/v1",
      "apiKey": "YOUR_OPENAI_API_KEY"
    }
  }
}
```

Replace `YOUR_OPENAI_API_KEY` with your actual key (or set it as an environment variable).

**Models:**
| Model | Dimensions | Cost | Notes |
|-------|-----------|------|-------|
| `text-embedding-3-small` | 1536 | Low | Good balance |
| `text-embedding-3-large` | 3072 | Medium | Highest quality |
| `text-embedding-ada-002` | 1536 | Low | Legacy |

---

## Option C: OpenAI-compatible API (self-hosted or third-party)

Any provider implementing the OpenAI embeddings API format will work.

### Examples

**LocalAI:**
```json
{
  "memorySearch": {
    "provider": "openai",
    "model": "text-embedding-nomic-embed-text-v1",
    "remote": {
      "baseUrl": "http://localhost:8080/v1",
      "apiKey": "any-string"
    }
  }
}
```

**LM Studio:**
```json
{
  "memorySearch": {
    "provider": "openai",
    "model": "nomic-embed-text",
    "remote": {
      "baseUrl": "http://localhost:1234/v1",
      "apiKey": "lm-studio"
    }
  }
}
```

**Third-party OpenAI-compatible providers** (e.g., Groq, Together AI, Anyscale):
```json
{
  "memorySearch": {
    "provider": "openai",
    "model": "PROVIDER_MODEL_NAME",
    "remote": {
      "baseUrl": "https://api.YOUR_PROVIDER.com/v1",
      "apiKey": "YOUR_PROVIDER_API_KEY"
    }
  }
}
```

---

## Option D: No vector recall

The skill works without embedding search — memory routing, promotion, and hygiene all function based on explicit rules. You just won't have semantic similarity search.

To disable:

```json
{
  "memorySearch": {
    "enabled": false
  }
}
```

In this mode, the agent uses rule-based routing only (daily → structured → enforcement). Good enough for most use cases.

---

## Advanced: Hybrid search

For best recall quality, enable hybrid search (vector + keyword):

```json
{
  "memorySearch": {
    "enabled": true,
    "provider": "ollama",
    "model": "nomic-embed-text",
    "query": {
      "maxResults": 6,
      "minScore": 0.35,
      "hybrid": {
        "enabled": true,
        "vectorWeight": 0.7,
        "textWeight": 0.3,
        "mmr": {
          "enabled": true,
          "lambda": 0.7
        },
        "temporalDecay": {
          "enabled": true,
          "halfLifeDays": 30
        }
      }
    }
  }
}
```

This combines semantic similarity with keyword matching and deprioritizes stale memories over time.

---

## Troubleshooting

**Ollama not connecting:**
```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# Check the model is available
ollama list
```

**Memory search returning poor results:**
- Try a different embedding model (larger = better quality)
- Lower `minScore` if missing relevant results
- Raise `minScore` if getting too much noise

**Slow indexing:**
- Use `nomic-embed-text` (fastest Ollama option)
- Or switch to cloud embeddings for speed
