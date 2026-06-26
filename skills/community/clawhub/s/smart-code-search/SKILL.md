---
name: smart-code-search
description: Search code and docs by meaning, not keywords. Powered by ColGREP/NextPlaid, #1 on MTEB Code. 17M params, local CPU, sub-second, zero cost, 100% private. Outperforms 8B models at 54x smaller. Use when searching codebases for implementations or patterns, navigating unfamiliar projects, finding related docs across repos, or giving coding agents semantic awareness. Triggers on "search the code", "find where", "semantic search", "code search", "smart search", "codebase search", "find implementation", "colgrep", "nextplaid".
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": { "bins": ["colgrep"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "lightonai/tap/colgrep",
              "bins": ["colgrep"],
              "label": "Install ColGREP via Homebrew",
            },
          ],
      },
  }
---

# Smart Code Search

**Search code and docs by meaning, not just strings.**

Powered by [ColGREP](https://github.com/lightonai/next-plaid) and [NextPlaid](https://lighton.ai/lighton-blogs/introducing-lighton-nextplaid) from LightOn — the engine behind the **#1 ranked code retrieval model on MTEB** and the **#1 retriever on BrowseComp-Plus**, OpenAI's hardest agentic search benchmark.

grep finds strings. This finds intent. Ask "payment capture logic" and get results from files that never contain those exact words — because it understands what your code *does*, not just what it says.

## Why This Exists

Every developer has been here: you know *what* you're looking for but not *where* it lives. You chain 4 different `grep -r` attempts, guess filenames, scroll through directory trees. Coding agents are even worse — they grep, miss things, hallucinate file paths, waste tokens exploring blind.

ColGREP fixes this with **multi-vector semantic search**. It parses your code with Tree-sitter, embeds each function/method/class with token-level vectors, and ranks results by meaning. The model is 17M parameters, runs on CPU, and returns results in under a second.

## The Numbers

| Metric | Value |
|--------|-------|
| **MTEB Code Leaderboard** | #1 ([LateOn-Code](https://lighton.ai/lighton-blogs/lateon-code-colgrep-lighton)) |
| **BrowseComp-Plus** | 87.59% accuracy, beating all models up to 8B params ([blog](https://lighton.ai/lighton-blogs/the-bloated-retriever-era-is-over)) |
| **vs grep in coding agents** | 70% win rate head-to-head |
| **Model size** | 17M params — 54× smaller than competing 8B models |
| **Search latency** | 200–900ms on CPU |
| **API cost** | $0. Forever. Runs 100% local |
| **Privacy** | Code never leaves your machine |

## Install

```bash
brew install lightonai/tap/colgrep
```

Verify: `colgrep --version`

## Quick Start

### 1. Index Your Project

```bash
cd /path/to/project
colgrep init
```

That's it. ColGREP parses every file with Tree-sitter, builds multi-vector embeddings on CPU, and stores the index in `.colgrep/`. Takes 30–60 seconds for ~1000 files. After this, **the index auto-updates on every search** — changed files are detected and re-indexed automatically.

### 2. Search

```bash
colgrep "natural language description of what you want"
```

Results are ranked by semantic relevance score. Higher = better match.

**Examples:**
```bash
colgrep "authentication middleware token validation"
colgrep "database migration rollback strategy"
colgrep "React form validation with error display"
colgrep "webhook retry logic with exponential backoff"
```

### 3. Combine Regex + Semantics

Filter files by regex pattern first, then rank semantically:

```bash
colgrep -e "async.*await" "error handling patterns"
colgrep -e "def test_" "payment capture edge cases"
colgrep -e "\.tsx$" "patient dashboard layout"
```

## Search Options

```bash
colgrep "query"              # Default output: file:lines (score: X.XX)
colgrep "query" --json       # JSON output for piping to other tools
colgrep "query" -n 5         # Top 5 results only
```

## When to Use This vs grep

| You know... | Use |
|-------------|-----|
| The exact string or function name | `grep -r "functionName"` |
| The concept but not the words | `colgrep "what it does"` |
| A pattern + a concept | `colgrep -e "pattern" "meaning"` |
| Where something is implemented | `colgrep "description of behavior"` |
| How a feature works across files | `colgrep "feature workflow"` |

## Coding Agent Integration

ColGREP provides built-in integration with popular coding agents. After installing, restart your agent to enable semantic search:

- **Claude Code:** `colgrep --install-claude-code`
- **OpenCode:** `colgrep --install-opencode`
- **Codex:** `colgrep --install-codex`

These commands register ColGREP as a search tool within the agent. The agent will automatically use semantic search when navigating indexed projects.

## Multi-Project Setup

Index each project independently. Search from the project directory:

```bash
cd ~/code/api && colgrep init
cd ~/code/frontend && colgrep init
cd ~/code/infrastructure && colgrep init
cd ~/docs && colgrep init

# Search each independently
cd ~/code/api && colgrep "payment processing service"
cd ~/code/frontend && colgrep "checkout form validation"
```

Works great for monorepos, microservices, documentation vaults, and any directory with text/code files.

## How It Works

ColGREP uses **ColBERT late-interaction retrieval** — a fundamentally different approach than traditional single-vector embeddings:

1. **Tree-sitter** parses your code into structured units (functions, methods, classes, signatures)
2. **LateOn-Code-edge** (17M params) creates **multiple token-level embeddings** per code unit — not one lossy summary vector
3. **NextPlaid** stores these in a quantized, memory-mapped Rust index
4. At search time, query tokens interact with document tokens for **fine-grained relevance scoring**

This is why a 17M model beats 8B models — late interaction preserves token-level semantics that single-vector approaches compress away. Read the full technical story: [The Bloated Retriever Era Is Over](https://lighton.ai/lighton-blogs/the-bloated-retriever-era-is-over)

## Interpreting Scores

- **6.0+** — Near-exact conceptual match. The code does exactly what you described.
- **5.0–6.0** — Strong semantic match. Highly relevant code.
- **4.0–5.0** — Good match. Related code worth reviewing.
- **3.0–4.0** — Weak match. May or may not be relevant.
- **Below 3.0** — Likely noise. Ignore these results.

## Troubleshooting

**"Index is being updated by another process"** — Another colgrep instance is updating. Current search uses existing index. Safe to ignore.

**Re-index from scratch:**
```bash
rm -rf .colgrep/ && colgrep init
```

**Add to .gitignore:**
```
.colgrep/
```

## Links

- [ColGREP + NextPlaid on GitHub](https://github.com/lightonai/next-plaid)
- [LateOn-Code: #1 on MTEB Code](https://lighton.ai/lighton-blogs/lateon-code-colgrep-lighton)
- [The Bloated Retriever Era Is Over (BrowseComp-Plus results)](https://lighton.ai/lighton-blogs/the-bloated-retriever-era-is-over)
- [NextPlaid: Local-First Multi-Vector Database](https://lighton.ai/lighton-blogs/introducing-lighton-nextplaid)
- [Reason-ModernColBERT: Reasoning-Intensive Retrieval](https://lighton.ai/lighton-blogs/lighton-releases-reason-colbert)
