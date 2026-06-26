---
name: vector-memory
description: Vector-based semantic memory using embeddings for intelligent recall. Store and search memories by meaning rather than keywords. Use when you need semantic search, similar document retrieval, or context-aware memory.
---

# Vector Memory Skill

This skill provides vector-based semantic memory storage using embeddings for intelligent recall by meaning.

## When to Use

- You need semantic search (find memories by meaning, not keywords)
- You want to retrieve similar documents or conversations
- You're building an agent that needs context-aware memory
- You need to cluster or group related memories

## Capabilities

- **vstore**: Store text with automatic embedding generation
- **vsearch**: Search memories by semantic similarity
- **vdelete**: Remove a memory by ID
- **vlist**: List all stored memories
- **vsimilar**: Find memories similar to a given ID
- **vclear**: Clear all memories

## How It Works

1. Text is converted to embeddings using OpenAI's API
2. Embeddings are stored in JSON with metadata
3. Search uses cosine similarity to find semantically related memories
4. No external vector database required - pure JSON storage

## Environment Variables

Required:
- `OPENAI_API_KEY` - For generating embeddings

Optional:
- `VECTOR_MEMORY_DIM` - Embedding dimensions (default: 1536 for text-embedding-ada-002)

## Usage Examples

```javascript
// Store a memory with semantic embedding
vstore('Meeting notes: Discussed Q1 roadmap and budget allocation')
// Returns: "Stored memory with ID: mem_abc123"

// Search by meaning (not keywords)
vsearch('What did we talk about regarding money?')
// Returns: Memories about budget, funding, financial discussions

// Find similar memories
vsimilar('mem_abc123')
// Returns: Semantically similar memories

// List all memories
vlist()
// Returns: List of stored memories with metadata

// Clear all
vclear()
// Returns: "Cleared all vector memories"
```

## Features

- **Semantic search**:Find by meaning, not keywords
- **Similarity scoring**: Results ranked by relevance score
- **Automatic embeddings**: No manual vector generation needed
- **Metadata support**: Store timestamps and tags with memories
- **Pure JSON**: No external database dependencies
