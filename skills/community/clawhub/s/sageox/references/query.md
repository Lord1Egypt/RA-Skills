# Query — Search Team Knowledge

Search across team discussions, docs, session history, and local code
using `ox query`.

## Usage

```bash
ox query "<text>" [--source team|code|all] [--limit N] [--mode hybrid|knn|bm25]
```

## Source selection

| Source | What it searches | When to use |
|---|---|---|
| `team` (default) | Team discussions, docs, decisions, session history | "How do we handle auth?" — team knowledge |
| `code` | Local code index (symbols, git history, diffs) | "Where is the auth middleware?" — codebase |
| `all` | Both team context and code index | Broad searches spanning knowledge + code |

## Search modes

| Mode | How it works | When to use |
|---|---|---|
| `hybrid` (default) | Combines semantic + keyword matching | Best general-purpose mode |
| `knn` | Pure semantic similarity (vector search) | Conceptual questions, fuzzy matches |
| `bm25` | Pure keyword matching | Exact terms, specific names |

## Workflow

1. Accept the user's natural language question.
2. Choose source based on the question:
   - Questions about decisions, conventions, processes → `--source team`
   - Questions about code structure, symbols, implementations → `--source code`
   - Unclear → `--source all`
3. Run: `ox query "<question>" --source <src> --limit 10`
4. Present results with source attribution (which discussion, session,
   or code file each result came from).
5. Offer follow-up:
   - "Want to refine the query?"
   - "Try a different source (team/code/all)?"
   - "Try a different mode (knn for semantic, bm25 for exact)?"

## Iterative refinement

If results are sparse:
- Broaden the query (fewer specific terms)
- Try `--source all` if only searching one source
- Switch mode: `knn` finds conceptual matches that keyword search misses

If results are noisy:
- Narrow the query (more specific terms)
- Try `--mode bm25` for exact keyword matching
- Reduce `--limit` to surface only the strongest matches

## Examples

```bash
# Team knowledge
ox query "how do we handle database migrations" --source team --limit 10

# Code search
ox query "authentication middleware" --source code --limit 5

# Combined search with semantic mode
ox query "error handling patterns" --source all --mode knn --limit 10
```
