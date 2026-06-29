---
name: rapport-memories
description: "Extends the agent's memory with semantic search capabilities using Retrieval-Augmented Generation (RAG) for enhanced contextual awareness and continuity."
---
## Description

This skill adds a semantic layer to the agent's internal memory system (MEMORY.md, memory/*.md, and session transcripts) enabling:

- Semantic search over past conversations, decisions, and learned information
- Context-aware responses that leverage historical interactions
- Improved continuity in multi-turn dialogues
- Ability to recall and synthesize information from previous sessions

Unlike the existing `calibre-ebooks` skill which focuses on book content RAG, this skill targets the agent's own operational memory and knowledge base.

## Core Functionality

1. **Memory Indexing**

   - Automatically processes MEMORY.md, memory/*.md files
   - Indexes sanitized session transcripts (excluding sensitive operational data)
   - Creates vector embeddings for semantic search capability
2. **Semantic Search**

   - Provides `semantic_memory` query method for natural language queries over agent's memory
   - Returns relevant past conversations, decisions, and contextual information
   - Includes source attribution (date, session ID when available)
3. **Context Enhancement**

   - Augments LLM prompts with relevant historical context when appropriate
   - Helps maintain consistency in long-term interactions
   - Supports "remember when..." type queries about past interactions

## Technical Implementation

### Architecture

- Uses local vector store (FAISS or similar) for memory embeddings
- Embedding model: Configured via environment variable (defaults to same as calibre-ebooks for consistency)
- Chunking strategy: Paragraph-level with overlap for context preservation
- Update mechanism: Incremental indexing of new memory entries

### Data Sources Indexed

- `MEMORY.md` - Primary persistent memory file
- `memory/*.md` - Daily/rotational memory files
- Session transcripts (sanitized): Excludes:
  - Internal tool calls, JSON, commands
  - Sandbox/runtime diagnostics
  - Credentials, tokens, internal paths
  - Approval-related metadata
  - Anything marked as private in session history

### Privacy & Safety

- Only indexes content deemed appropriate for agent's own knowledge base
- Explicitly filters out:
  - User personal data beyond what's necessary for context
  - Operational/system internals
  - Any content that would violate agent's privacy guidelines
- Respects existing memory file permissions and conventions

## Usage 

- python3 /skill/rapport-memories/scripts/memory_rag.py init
- python3 /skill/rapport-memories/scripts/memory_rag.py index
- python3 /skill/rapport-memories/scripts/memory_rag.py add --title "Title" --content "Content" --taxonomy "Taxonomy" --date "2025-10-15"
- python3 /skill/rapport-memories/scripts/memory_rag.py search "Query"
- python3 /skill/rapport-memories/scripts/memory_rag.py stats

### Configuration

Set via environment variables:

- `RAPPORT_MEMORIES_EMBEDDING_MODEL` - Embedding model to use (default: nomic-embed-text-v2-moe:latest)
- `RAPPORT_MEMORIES_CHUNK_SIZE` - Text chunk size for indexing
- `RAPPORT_MEMORIES_UPDATE_INTERVAL` - Auto-reindex interval (seconds)
- `RAPPORT_MEMORIES_STORE_PATH` - Path for vector store storage

## Relationship to Existing Systems

### Complements `calibre-ebooks`

- `calibre-ebooks`: RAG for book content (external knowledge)
- `rapport-memories`: RAG for agent's own operational memory
- Both can be used together for contextual responses that combine book knowledge with conversation history

### Enhances Existing Flows

- **Book Search**: When searching for books, can recall past similar requests
- **Recommendations**: Leverages history of what was previously suggested/discussed
- **Status Queries**: Can reference past system states or decisions
- **Learning**: Helps agent avoid repeating same mistakes or suggestions

### Does NOT Replace

- Core memory files (MEMORY.md remains source of truth)
- Agent's inherent knowledge or reasoning
- Need for explicit memory curation by operators
- The requirement to verify book availability via calibre-ebooks

## Implementation Notes

### Indexing Process

1. Scan memory directory for new/updated .md files
2. Extract and sanitize text content (remove code blocks, JSON, etc.)
3. Split into semantic chunks with overlap
4. Generate embeddings using configured model
5. Store in vector index with metadata (source, timestamp, etc.)

### Search Process

1. Convert query to embedding using same model
2. Perform vector similarity search
3. Return top-k results with relevance scores and source citations
4. Optionally rerank or filter based on recency/relevance

## Usage Examples

### Public-Facing Benefits (Indirect)

While the skill itself isn't called directly in public responses, it enables:

- More coherent long-term conversations
- Reduced need to re-ask for context
- Better personalized interactions based on history
- More accurate self-referential responses ("As we discussed yesterday...")

## Limitations & Considerations

### Scope

- Only indexes text-based memory files
- Does not index book content (that's calibre-ebooks' domain)
- Real-time indexing may have slight delay for new entries

### Performance

- Initial indexing may take time for large memory histories
- Subsequent updates are incremental
- Vector store size grows with memory volume

### Maintenance

- Periodic reindexing may be needed if embedding model changes
- Memory file format changes may require parser updates
- Should monitor vector store size and prune if necessary
