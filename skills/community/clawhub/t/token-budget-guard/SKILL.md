# Token Budget Guard

> Stop burning context. Manage your agent's token budget intelligently.

## The Problem

AI agents waste 40-60% of tokens on:
- Repeatedly loading full schemas when summaries suffice
- Including irrelevant context from previous turns
- Not compressing before context window fills
- Loading entire files when snippets would do

The AAI Gateway showed 99% token savings are possible. This skill makes token budgeting automatic.

## When to Use

- "token budget", "reduce tokens", "context too long", "running out of context"
- Before multi-tool workflows
- When hitting context limits
- Optimizing agent workflows for cost efficiency

## Core Principles

### 1. Progressive Disclosure
```
Level 0: Name only (1-5 tokens) — "browser tool available"
Level 1: Summary (10-30 tokens) — "browser: open/navigate/snapshot web pages"
Level 2: Schema (50-200 tokens) — full parameter descriptions
Level 3: Examples (200-500 tokens) — sample calls with output

Default: Level 1. Escalate only when tool is being used.
```

### 2. Summarize Before Including
- Previous conversation: summarize, don't replay
- File contents: extract relevant sections, don't cat entire files
- Tool outputs: compress to decisions + evidence, drop raw data
- Error logs: extract error line + 5 lines context, not full stack

### 3. Budget Allocation
```
Total context budget: 100%
├── System prompt: 15-20% (fixed)
├── Active task: 40-50% (working space)
├── Tool schemas: 10-15% (progressive)
├── Memory/History: 10-15% (summarized)
└── Reserve: 5-10% (safety margin)
```

### 4. Compression Triggers
- When context > 60% full → start compressing history
- When context > 80% full → aggressive summarization
- When context > 90% full → emergency mode (drop all but current task)

## Token Saving Strategies

### Strategy 1: Schema Stubs
```javascript
// Instead of full schema (200+ tokens):
// { "name": "web_search", "parameters": { "query": { "type": "string", ... }, ... } }

// Use stub (15 tokens):
// web_search(query) → search results
```

### Strategy 2: Conversation Compression
```
// Before compression (500 tokens of back-and-forth):
User: Can you find the latest Node.js version?
Agent: I'll search for that. [calls web_search]
Agent: The latest Node.js version is v22.22.2...
User: What about LTS?
Agent: [calls web_search] The current LTS is v22.x...

// After compression (30 tokens):
// Resolved: Node.js latest=v22.22.2, LTS=v22.x, user confirmed.
```

### Strategy 3: Selective File Reading
```bash
# Instead of: cat package.json  (often 100+ lines)
# Use: jq '.dependencies | keys' package.json  (just what you need)
# Or: head -5 package.json  (name + version)
```

### Strategy 4: Tool Result Filtering
```
// Instead of returning full API response (2000 tokens)
// Return structured summary (50 tokens):
// ✅ 3 issues found: 2 bugs (P1, P2), 1 feature request
// Key assignees: @alice, @bob
// No urgent items
```

## Budget Monitoring

Track token usage per task:

```markdown
### Token Budget Log — Task: "Build API endpoint"
| Action | Tokens | Running Total | Budget % |
|--------|--------|--------------|----------|
| System prompt | 2,000 | 2,000 | 10% |
| Tool schemas (stub) | 500 | 2,500 | 12.5% |
| Read 3 files (selective) | 1,200 | 3,700 | 18.5% |
| Write code | 800 | 4,500 | 22.5% |
| ... | ... | ... | ... |
```

## Quick Wins (Apply Immediately)

1. **Replace full file reads with targeted extraction** — `grep`, `jq`, `awk` > `cat`
2. **Use tool stubs during planning** — load full schemas only at execution time
3. **Summarize after every 5 tool calls** — don't let raw output accumulate
4. **Set a hard limit** — if a single file > 500 lines, read with offset/limit
5. **Drop completed subtask context** — keep decision, drop process

## Integration with Agent Workflows

```
Task received → Estimate token need → Allocate budget → Execute with monitoring
                                                       ↓
                                              Budget > 80%? → Compress
                                                       ↓
                                              Budget > 90%? → Emergency summarize
```

## Real Impact

Based on AAI Gateway benchmarks:
- Multi-MCP workflows: 99% reduction in schema tokens
- Conversation history: 60-80% compressible
- File operations: 40-70% savings with selective reading
- Overall context efficiency: 3-5x improvement typical

## License

MIT
