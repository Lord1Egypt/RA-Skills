# 🔧 Token Optimization for OpenClaw

> Reduce per-turn prompt token costs by **70%+** through systematic workspace optimization.

## The Problem

Every time your OpenClaw agent processes a message, it loads all workspace files (AGENTS.md, SOUL.md, MEMORY.md, etc.) into the prompt. Over time these files grow, and you end up paying 50k+ tokens per turn even for a simple "ok".

**This skill gives you a repeatable 3-layer framework to fix that.**

## What This Skill Does

| Layer | What | Expected Savings |
|-------|------|-----------------|
| **1. File Structure** | Split bloated workspace files into stable (cached) vs volatile (on-demand) | 40-60% fewer tokens per turn |
| **2. Prompt Caching** | Enable `cacheRetention` for Anthropic models so repeated prompts hit cache | 80%+ cache hit rate |
| **3. Context Pruning** | Tune pruning thresholds to prevent context bloat in long conversations | Fewer compactions, lower tail costs |

## Quick Start

### 1. Audit your current costs

```
/status
```

Look at:
- **Context**: if > 30% on a simple message, you have bloat
- **Cache**: if 0% hit, caching isn't working
- **Tokens**: note your per-turn input token count

### 2. Install the skill

```bash
# From ClawHub
clawhub install token-optimization

# From OpenClaw 水产市场
openclawmp install skill/@Jack-Yang-ai/token-optimization

# From GitHub
git clone https://github.com/Jack-Yang-ai/token-optimization.git
```

### 3. Follow the SKILL.md guide

The skill walks you through each optimization step with exact config snippets you can copy-paste into your `openclaw.json`.

## Real-World Results

Tested on a production OpenClaw setup with 69 skills, 9 workspace files, and daily active use:

| Metric | Before | After |
|--------|--------|-------|
| Workspace files loaded per turn | 45 KB | 9.8 KB |
| AGENTS.md size | 19 KB | 1.8 KB |
| MEMORY.md size | 8 KB | 1.4 KB |
| Simple Q&A input tokens | ~50k | ~15k |
| Cache hit rate | 0% | 30%+ (first session, improves over time) |

## Key Techniques

### File Splitting Strategy

```
workspace/
├── AGENTS.md              ← Core rules only (≤5KB, loads every turn)
├── AGENTS_SUBAGENT.md     ← Read on demand (only when spawning)
├── AGENTS_HEARTBEAT.md    ← Read on demand (only during heartbeat)
├── SOUL.md                ← Stable, cacheable
├── MEMORY.md              ← Keep lean (≤3KB)
└── memory/
    ├── search-sop.md      ← Moved out of MEMORY.md
    └── YYYY-MM-DD.md      ← Daily notes (volatile, not cached)
```

### Prompt Caching Config

```json
{
  "agents": {
    "defaults": {
      "models": {
        "anthropic/claude-opus-4-6": {
          "params": { "cacheRetention": "long" }
        }
      }
    }
  }
}
```

### Context Pruning Config

```json
{
  "contextPruning": {
    "mode": "cache-ttl",
    "ttl": "3m",
    "keepLastAssistants": 2,
    "softTrimRatio": 0.25,
    "hardClearRatio": 0.45,
    "tools": {
      "allow": ["exec", "read", "browser"],
      "deny": ["web_search", "web_fetch"]
    }
  }
}
```

## Monitoring

After applying optimizations, track these KPIs via `/status`:

| Metric | Target |
|--------|--------|
| Cache Hit Rate | > 80% |
| Per-turn Input (simple msg) | < 20k tokens |
| Context Usage (idle) | < 30% |
| Compactions/day | < 2 |

## Compatibility

- **OpenClaw**: 2026.3.x+
- **Providers**: Anthropic (direct), OpenRouter Anthropic, Bedrock Anthropic
- **Models**: Any Anthropic Claude model (cacheRetention support)
- **Other providers**: File splitting and pruning still help; caching has no effect

## References

- [OpenClaw Prompt Caching docs](https://docs.openclaw.ai/reference/prompt-caching)
- [Session Pruning docs](https://docs.openclaw.ai/concepts/session-pruning)
- [Gateway Configuration](https://docs.openclaw.ai/gateway/configuration)

## License

MIT

## Author

Built by [Jack-Yang-ai](https://github.com/Jack-Yang-ai) with 🦞 海洋大总管.
