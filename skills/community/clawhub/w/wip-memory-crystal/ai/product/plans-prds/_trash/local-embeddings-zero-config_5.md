# Local Embeddings: Zero-Config Default

**Source:** External evaluation feedback (2026-03-04)
**Priority:** High (adoption blocker)

## Problem

Memory Crystal requires an external embedding provider (OpenAI API, Google, or Ollama) for semantic search. That means an API key and ongoing cost just to get started. Competitors like `mcp-memory-service` run embeddings locally via ONNX (MiniLM-L6-v2) with zero API cost.

For anyone evaluating memory-crystal cold, this is real friction. "Local-first" should mean local embeddings too.

## Proposal

Add a local embedding provider as the **default**. Zero config = zero API keys.

Options:
- **ONNX Runtime + MiniLM-L6-v2** ... same approach as mcp-memory-service. Small model (~22MB), fast inference, good enough for retrieval.
- **Transformers.js** ... runs transformer models in Node.js via ONNX under the hood. More flexibility in model choice.
- **sqlite-vec built-in** ... if sqlite-vec adds native embedding support in the future.

Keep OpenAI/Google/Ollama as upgrade options for higher quality embeddings. The config already supports provider switching... this just adds a "none required" default.

## Tradeoffs

- MiniLM-L6-v2 (384d) is lower quality than text-embedding-3-small (1536d)
- But for personal memory search, it's more than good enough
- Eliminates the biggest objection for new users
- Aligns with the sovereignty story: your memory, your machine, no API keys required

## Migration consideration

The vectors are NOT compatible between providers. Different dimensions (384 vs 1536), different model architectures. You can't mix them in the same vector index. If a user starts with local embeddings and later upgrades to OpenAI (or vice versa), they'd need to re-embed all existing chunks.

Solution: store the embedding model name per chunk. On provider change, detect the mismatch and offer `crystal re-embed` to migrate. Text is always preserved... only the vectors need regenerating.
