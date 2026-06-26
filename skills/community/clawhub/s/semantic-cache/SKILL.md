---
name: semantic-cache
description: |
  Semantic cache for LLM API calls using Redis. Caches responses by meaning, not exact match.
  Activate when the user wants to cache AI responses, reduce API costs, speed up repeated queries,
  or add semantic caching to any workflow. Use this skill to check cache before making expensive
  LLM calls and store results for future similar queries.
metadata:
  openclaw:
    requires:
      env: [REDIS_URL, OPENAI_API_KEY]
      bins: [node]
    primaryEnv: REDIS_URL
    emoji: "\u26A1"
    homepage: https://github.com/openclaw/clawhub
    install:
      - kind: node
        package: redis
        bins: []
      - kind: node
        package: openai
        bins: []
---

# Semantic Cache

Cache LLM responses by meaning using Redis vector search. Similar questions return cached answers instantly instead of making expensive API calls.

## How It Works

1. User asks a question or makes an LLM request
2. The question is embedded into a vector using OpenAI text-embedding-3-small
3. Redis vector search finds semantically similar cached queries (cosine similarity > 0.80)
4. **Cache hit**: Return the cached response instantly (~100ms)
5. **Cache miss**: Pass through to the LLM, cache the response for future similar queries

## Commands

### Cache a query and response
```bash
node scripts/cache.js store "What is the capital of France?" "The capital of France is Paris."
```

### Check cache for a similar query
```bash
node scripts/cache.js lookup "What's France's capital city?"
```

### Cache stats
```bash
node scripts/cache.js stats
```

### Clear all cached entries
```bash
node scripts/cache.js clear
```

### Interactive mode — wraps any LLM call with caching
```bash
node scripts/cache.js query "Your question here"
```
This checks cache first. On miss, calls OpenAI, caches the result, and returns it.

## When to Use This Skill

- Before making any LLM API call, check if a semantically similar query was already answered
- When building agents that answer repetitive questions (support bots, FAQ systems)
- When you want to reduce OpenAI/Anthropic API costs by 40-80%
- When you need faster response times for common queries

## Configuration

Set these environment variables:
- `REDIS_URL` — Redis connection string with vector search support (Redis Cloud or Redis Stack)
- `OPENAI_API_KEY` — For generating embeddings
- `SEMANTIC_CACHE_THRESHOLD` — Similarity threshold 0-1 (default: 0.80, higher = stricter matching)
- `SEMANTIC_CACHE_TTL` — Cache TTL in seconds (default: 86400 = 24 hours)

## Example Workflow

```
User: "How do I reset my password?"
  -> Embed query -> Search Redis -> MISS
  -> Call LLM -> Get response -> Cache it -> Return response

User: "I forgot my password, how do I change it?"
  -> Embed query -> Search Redis -> HIT (92.7% similar)
  -> Return cached response in 8ms (saved ~2 seconds + API cost)
```

## Performance

- Cache lookup: ~5-15ms (vs 1-5 seconds for LLM call)
- Embedding generation: ~50-100ms
- Storage per entry: ~6KB (1536-dim vector + metadata)
- Supports millions of cached entries
