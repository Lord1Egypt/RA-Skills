# The Synthetic Context Generator ⚡

> Feed it a goal, get the perfect context window — nothing more, nothing less.

## The Problem

Your AI coding assistant needs context. But dumping entire repos or files creates context window bloat. You get irrelevant noise, hit token limits, and the AI misses what actually matters.

## The Solution

SCG is an intelligent context broker. You give it a goal, it finds exactly what you need:

```
$ scg "write secure SQL query"

⚠️ Common Pitfalls
- DON'T: Store passwords as plain text
- DON'T: Use string concatenation for SQL

✅ Recommended Patterns  
- Use parameterized queries
- bcrypt for password hashing
```

## Installation

```bash
git clone https://github.com/captainsvbot/The-Synthetic-Context-Generator.git
cd The-Synthetic-Context-Generator
npm install
npm link  # Make 'scg' available globally
```

## Usage

```bash
# Basic usage
scg "write secure authentication middleware"

# With project context
scg "fix CORS vulnerability" --context ./myproject

# Limit tokens
scg "optimize database queries" --max-tokens 2000

# Skip web search
scg "basic Express setup" --no-web

# Index a project for local search
scg index ./myproject

# Add to knowledge base
scg learn ./my-patterns.json
```

## Features

- **Goal Parser** — Extracts intent, language, security level from natural language
- **Local Search** — Indexes your projects for fuzzy search
- **Knowledge Base** — Curated patterns (security pitfalls, best practices)
- **Web Search** — Pulls relevant StackOverflow answers
- **Token Control** — Respects your context window limits

## Architecture

```
Goal: "write secure code"
    ↓
[Goal Parser] → intent: write, security
    ↓
[Parallel Search]
  - Local files (fuzzy search)
  - Knowledge base (curated)
  - StackOverflow (API)
    ↓
[Context Composer] → formats & truncates
    ↓
Perfect Context Window ⚡
```

## Tech Stack

- Node.js CLI
- Fuse.js for fuzzy search
- tiktoken for token counting
- StackExchange API

## Roadmap

- [ ] Cursor/Rovio plugin for auto-inject
- [ ] Learn from user's codebase patterns
- [ ] Feedback loop (track what context helped)
- [ ] Vector embeddings for semantic search
- [ ] GitHub issues/PRs search

---

Built by CaptainSV ⚓