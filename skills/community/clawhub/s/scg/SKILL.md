# Synthetic Context Generator (SCG)

Generate optimized context windows for AI coding tasks.

## Description

SCG takes a goal/task as input and returns a curated context window containing exactly what's needed:
- Relevant code patterns from knowledge base
- Common pitfalls and anti-patterns
- StackOverflow solutions
- Local project context

## Usage

```bash
# Generate context for a task
scg "write secure authentication middleware"

# Skip web search
scg "create React component" --no-web

# Custom token limit
scg "optimize database query" --max-tokens 2000

# Index a local project
scg index ./my-project

# Learn from a codebase
scg learn ./src
```

## Options

- `--context` - Include local project context (default: true)
- `--max-tokens` - Maximum tokens in output (default: 4000)
- `--no-web` - Skip StackOverflow search
- `--verbose` - Show debug info

## Examples

```bash
# Security-focused
scg "secure SQL query"
# → SQL injection patterns, parameterized queries, secrets handling

# React development
scg "create React component with hooks"
# → Custom hooks, useEffect best practices, testing patterns

# API development
scg "build REST API with Express"
# → Rate limiting, Helmet, JWT, error handling
```

## Triggers

- "get context for..."
- "best practices for..."
- "how to write..."
- "implement..."
- "create..."