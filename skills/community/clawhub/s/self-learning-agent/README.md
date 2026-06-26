# self-learning-agent

Knowledge card memory system with semantic search. Agents wake up fresh each session but remember everything through atomic ~350-token cards, daily logs, and a slim master index.

## The Problem

AI agents lose context between sessions. The common fix (one big MEMORY.md) works until it doesn't. After a few weeks, the file is 60KB of mixed-relevance notes that burns tokens on every load and buries important facts in noise.

## The Solution

Three-tier memory architecture:

1. **MEMORY.md** (~2KB) — Slim master index, loaded every session. Orientation only.
2. **Knowledge cards** (~350 tokens each) — Atomic facts with YAML frontmatter. One topic per file. Searched semantically, not loaded in bulk.
3. **Daily logs** — Raw session notes. Periodically distilled into cards.

## How It Works

- Agent loads the 2KB index on startup (constant cost regardless of history length)
- Semantic search finds relevant cards for the current task
- Agent captures lessons, corrections, and facts as new cards
- Periodically distills daily logs into curated cards
- Lessons that repeat 3+ times get promoted to permanent rules

## Production Tested

Running in production with ~36 cards spanning infrastructure, security, career, tools, and workflow topics. Semantic search via embeddings finds the right card in <100ms. Session token cost stays flat regardless of how many months of history exist.

## Tags

memory, learning, self-improving, knowledge-management, agent-memory, persistence
