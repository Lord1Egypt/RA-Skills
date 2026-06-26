# The Synthetic Context Generator (SCG)

**Goal:** Feed it a goal/task → get the perfect context window with exactly what's needed, nothing more.

## Core Concept

AI coding assistants suffer from context overflow. You dump entire repos or files when you only need a specific function. SCG acts as an intelligent context broker:

```
Goal: "write secure SQL query" 
  → Search docs + examples + past vulnerabilities + StackOverflow
  → Inject only: the vulnerable patterns to avoid, secure alternatives, ORM best practices
```

## Architecture

### Components

1. **Goal Parser** — Extract intent, language, framework, security level from natural language
2. **Context Source Index** — Local docs, codebases, error logs, learned failures
3. **External Search** — StackOverflow, GitHub issues, framework docs (via API or scrape)
4. **Relevance Scorer** — Rank and weight findings by recency, success rate, similarity
5. **Context Composer** — Assemble final context window (truncate by token budget)

### Data Sources

| Source | Priority | Update Frequency |
|--------|----------|-------------------|
| Local project docs | High | On-demand |
| Code examples repo | High | Indexed at start |
| Past failures log | High | Every failure |
| StackOverflow | Medium | Cached results |
| Framework docs | Medium | Weekly refresh |

### CLI Interface

```bash
scg "write secure authentication middleware"
scg --goal "fix CORS vulnerability" --context ~/myproject --max-tokens 4000
scg --learn-from ./error-logs.json
```

### Output Format

```markdown
## Relevant Context (1,240 tokens)

### 📚 Documentation
- [Express.js Security](https://expressjs.com/en/advanced/best-practice-security.md)
- helmet.js configuration options

### ⚠️ Common Pitfalls
- DON'T: Store passwords as plain text (see: authservice.js:42)
- DON'T: Use eval() for dynamic permissions

### ✅ Recommended Patterns
- bcrypt.compare() for password verification
- JWT with RS256 for session tokens

### 🔧 StackOverflow Solutions
- [Best practice for JWT refresh tokens](https://stackoverflow.com/...) #847 votes
```

## Tech Stack

- **Runtime:** Node.js CLI
- **Search:** Local fuse.js for fuzzy + vector similarity (via embedding)
- **External:** StackExchange API, GitHub API
- **Storage:** SQLite for failure log + embeddings cache
- **Token counting:** tiktoken

## MVP Scope

1. Parse goal string → extract intent keywords
2. Search local files for matching patterns
3. Search a small "knowledge base" of examples
4. Output formatted context
5. `scg --learn` to add new examples to KB

## Future Ideas

- Cursor/Rovio plugin to auto-inject context
- Learn from user's codebase patterns
- Track what context actually helped (feedback loop)