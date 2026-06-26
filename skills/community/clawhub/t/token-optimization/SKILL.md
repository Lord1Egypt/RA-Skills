---
name: token-optimization
displayName: Token Optimization
description: "Reduce OpenClaw per-turn prompt costs by 70%+ through file splitting, prompt caching, context pruning, and model routing. Tested on production setup with 69 skills."
version: 1.1.0
tags:
  - optimization
  - tokens
  - cost-reduction
  - prompt-caching
  - context-pruning
---

# Token Optimization for OpenClaw

Systematic guide to reduce per-turn token consumption by 70%+ without losing any functionality.

## When to Use This Skill

- `session_status` shows Context > 30% on simple messages
- Cache hit rate is 0% or consistently low
- AGENTS.md > 5KB or MEMORY.md > 3KB
- You want to cut API costs on Anthropic models

## Prerequisites

- OpenClaw 2026.3.x or later
- Access to edit `openclaw.json`
- At least one Anthropic model configured

---

## Step 1: Audit Current State

Run `session_status` and record:

```
Cache: X% hit · Y cached, Z new
Context: Xk/200k (X%)
```

Then check file sizes:

```bash
wc -c ~/.openclaw/workspace/*.md
```

**Red flags:**
- Any single file > 10KB → needs splitting
- Total workspace files > 30KB → bloated
- Cache 0% → caching not enabled
- Context > 40% on simple message → pruning too loose

## Step 2: Split Large Files (Layer 1)

### AGENTS.md (biggest offender)

Move infrequently-needed content to separate files:

| Content | Move To | Load When |
|---------|---------|-----------|
| Subagent protocols | `AGENTS_SUBAGENT.md` | Only when spawning |
| Heartbeat rules | `AGENTS_HEARTBEAT.md` | Only during heartbeat |
| Detailed examples | `memory/` directory | On demand via `read` |

**Target: AGENTS.md ≤ 5KB**

Keep only: session rules, safety, formatting, quick-reference subagent table.

Add references at the top:
```markdown
> Subagent protocol → `AGENTS_SUBAGENT.md` (read on demand)
> Heartbeat protocol → `AGENTS_HEARTBEAT.md` (read during heartbeat)
```

### MEMORY.md

Move detailed SOPs and procedures to `memory/` subdirectory files. Keep only high-frequency referenced items.

**Target: MEMORY.md ≤ 3KB**

### BOOTSTRAP.md

Delete it after initial setup. It loads every turn for zero value.

```bash
mv ~/.openclaw/workspace/BOOTSTRAP.md ~/.openclaw/workspace/BOOTSTRAP.md.bak
```

### Verify

```bash
# Sum only files that load every turn
cat ~/.openclaw/workspace/{AGENTS,SOUL,TOOLS,IDENTITY,USER,HEARTBEAT,MEMORY}.md | wc -c
# Target: < 15KB total
```

## Step 3: Enable Prompt Caching (Layer 2)

Add `cacheRetention` to each Anthropic model in `openclaw.json`:

```json
{
  "agents": {
    "defaults": {
      "models": {
        "anthropic/claude-opus-4-6": {
          "params": { "cacheRetention": "long" }
        },
        "anthropic/claude-sonnet-4-6": {
          "params": { "cacheRetention": "long" }
        },
        "openrouter/anthropic/claude-3.5-sonnet": {
          "params": { "cacheRetention": "short" }
        }
      }
    }
  }
}
```

### Values

| Value | Cache Window | Best For |
|-------|-------------|----------|
| `none` | No caching | Bursty/notification agents |
| `short` | ~5 minutes | OpenRouter models |
| `long` | ~1 hour | Main agent (recommended) |

### Provider Support

| Provider | Support |
|----------|---------|
| Anthropic direct API | ✅ Full |
| OpenRouter `anthropic/*` | ✅ Auto cache_control injection |
| Bedrock Anthropic Claude | ✅ Pass-through |
| Other providers | ❌ No effect |

### Keep-Warm Tip

Pair `cacheRetention: "long"` with heartbeat at ~55 min intervals to keep cache permanently warm:

```json
"heartbeat": {
  "every": "55m",
  "model": "your/cheap-model"
}
```

## Step 4: Tune Context Pruning (Layer 3)

```json
{
  "agents": {
    "defaults": {
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
  }
}
```

### Parameter Guide

| Parameter | Aggressive | Moderate | Conservative |
|-----------|-----------|----------|-------------|
| `ttl` | 2m | 3m | 5m |
| `keepLastAssistants` | 1 | 2 | 3 |
| `softTrimRatio` | 0.20 | 0.25 | 0.30 |
| `hardClearRatio` | 0.40 | 0.45 | 0.50 |

### Tool Deny List

Move large, one-off tool outputs to `deny`:
- `web_fetch` — page content is large and rarely reused
- `web_search` — search results change every time

Keep frequently reused tools in `allow`:
- `exec` — command outputs often referenced in follow-up
- `read` — file contents may be discussed across turns
- `browser` — snapshot data may be referenced

## Step 5: Optimize Model Routing

Use cheap/free models for low-value tasks:

```json
"heartbeat": {
  "every": "4h",
  "model": "your/free-flash-model"
}
```

| Task | Model Tier | Why |
|------|-----------|-----|
| Heartbeat/cron | Free/flash | Simple checks, zero cost |
| Simple Q&A | Free/flash | Doesn't need intelligence |
| Medium tasks | Mid-tier | Balance cost and quality |
| Complex/multi-step | Premium | Worth the investment |

## Step 6: Validate & Monitor

After applying all changes, restart gateway and check:

```bash
openclaw gateway restart
```

Then send a simple message and run `session_status`:

### Target KPIs

| Metric | Target | Check Via |
|--------|--------|-----------|
| Cache Hit Rate | > 80% | `Cache: X% hit` |
| Simple Q&A Input | < 20k tokens | `Tokens: X in` |
| Context (idle) | < 30% | `Context: Xk/200k` |
| Compactions/day | < 2 | `Compactions: X` |

### Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Cache still 0% | Model doesn't support caching | Check provider is Anthropic |
| High cacheWrite every turn | Volatile content in system prompt | Move volatile files to on-demand |
| Context > 50% quickly | Pruning too loose | Lower `ttl` and `softTrimRatio` |
| Compactions > 3/day | Long conversations without pruning | Enable `cache-ttl` mode |

---

## Summary Checklist

- [ ] Audit: `wc -c` on workspace files + `session_status`
- [ ] Split: AGENTS.md ≤ 5KB, MEMORY.md ≤ 3KB
- [ ] Delete: BOOTSTRAP.md (if exists)
- [ ] Cache: `cacheRetention: "long"` on Anthropic models
- [ ] Prune: `contextPruning` with aggressive settings
- [ ] Route: Cheap model for heartbeat/simple tasks
- [ ] Validate: `session_status` shows cache hits + low context %
- [ ] Monitor: Weekly review of KPIs
