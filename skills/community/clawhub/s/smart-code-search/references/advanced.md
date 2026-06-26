# Advanced Usage & Architecture

## Architecture Deep Dive

ColGREP's pipeline:

```
Your Codebase
  → Tree-sitter (parse functions, methods, classes)
  → Structured representation (signature, params, calls, docstring, code)
  → LateOn-Code-edge · 17M params (multi-vector embedding per code unit, CPU)
  → NextPlaid (Rust index, quantized, memory-mapped, incremental)
  → Search (grep-compatible flags + SQLite filtering + semantic ranking)
```

### Why Multi-Vector Beats Single-Vector

Traditional embeddings (OpenAI `text-embedding-3-small`, Cohere, etc.) compress an entire document into **one vector** — a single point in high-dimensional space. This loses token-level nuance. "Payment capture with retry logic" and "Payment refund without retry" might map to nearly the same point.

ColBERT's late-interaction approach keeps **one vector per token**. At search time, each query token finds its best-matching document token. The final score is the sum of these fine-grained matches. This is why:

- Searches for "error handling in async functions" find error handling code even in files that use "rescue" or "catch" instead of "error"
- "Database connection pooling" finds connection pool implementations regardless of variable naming
- Concept-level queries work where keyword search fails completely

### Why 17M Beats 8B

Bigger isn't better when the architecture is wrong. Single-vector models need billions of parameters to compensate for the information loss of compressing to one vector. Late-interaction models preserve token-level information in the architecture itself, so a tiny model captures more useful signal than a massive one.

From LightOn's benchmarks:
- LateOn-Code-edge (17M) beats all single-vector models on MTEB Code
- Reason-ModernColBERT (149M) beats Qwen3-Embed-8B (8B) on BrowseComp-Plus
- 54× less compute, better results

## Indexing Details

### What Gets Indexed

- Functions, methods, classes (via Tree-sitter grammars)
- Signatures, parameters, return types
- Docstrings and inline comments
- Call sites and references
- Markdown content (headings, paragraphs, code blocks)

### What Gets Skipped

- Binary files
- `.gitignore`d paths
- Lock files, `node_modules/`, `vendor/`
- Files without Tree-sitter grammar support

### Index Storage

- Location: `.colgrep/` in the project root
- Contents: SQLite DB + quantized vectors + metadata
- Size: typically 1–10% of source code size
- Always add `.colgrep/` to your `.gitignore`

## Performance Characteristics

| Metric | Typical Value |
|--------|--------------|
| Initial index (1000 files) | 30–60 seconds |
| Incremental update (10 files) | < 2 seconds |
| Search latency | 200–900ms |
| Memory during search | ~50–100MB |
| Model size on disk | ~70MB (ONNX) |
| Runtime | ONNX on CPU (no GPU) |

## Using Results Programmatically

JSON output for piping to other tools:

```bash
colgrep "query" --json | jq '.[0].path'
```

Useful for building custom workflows, feeding results into LLM prompts, or integrating with CI/CD pipelines.

## Keeping Indexes Fresh

The index auto-updates on every search — no cron jobs, no watchers, no maintenance. If you switch branches with major changes, the next search handles it.

For a complete rebuild:
```bash
rm -rf .colgrep/
colgrep init
```
