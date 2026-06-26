---
name: proxy-token-optimizer
description: |
  Optimize LLM token usage and API costs for the openclaw-manager proxy platform.
  Provides model-tier routing (route simple prompts to glm-4.7-flashx instead of glm-4.7),
  heartbeat cost reduction (force heartbeat calls to use the cheapest model with optimized intervals),
  context lazy loading (generate optimized AGENTS.md that loads only necessary context files per prompt complexity),
  and platform-level usage analytics (query real usage_records from PostgreSQL to generate reports and quota-matching advice).
  Use this skill whenever the user mentions token optimization, reducing API costs, model routing, heartbeat optimization,
  context loading strategy, usage reports, quota analysis, or anything related to saving money on LLM API calls
  in the openclaw-manager project. Also trigger when the user asks about which model to use for different task types,
  or wants to analyze per-instance token consumption patterns.
metadata: {"openclaw": {"always": true}}
---

# Proxy Token Optimizer

Reduces LLM API costs for the openclaw-manager multi-tenant proxy platform through four strategies:

1. **Model-tier routing** — Route prompts to the cheapest capable model
2. **Heartbeat optimization** — Cheapest model + longer intervals for heartbeat calls
3. **Context lazy loading** — Load only the context files each prompt actually needs
4. **Platform usage analytics** — Real data from PostgreSQL, not estimates

## Why these strategies matter

The openclaw-manager platform proxies LLM requests for multiple OpenClaw instances through providers like `zai-proxy`, `zai-coding-proxy`, and `kimi-coding-proxy`. Each provider offers models at different price points (e.g., `glm-4.7` vs `glm-4.7-flashx`). Without optimization, every request — including simple greetings and heartbeat pings — uses the default (expensive) model, and every session loads the full context regardless of need. These four strategies target the highest-impact cost drivers.

## Quick start

All instance-side scripts run locally with no dependencies. Platform-side scripts need DB access.

```bash
# Model routing — which model should handle this prompt?
python3 scripts/model_router.py "thanks!"
# → {"tier": "cheap", "recommended_model": "zai-proxy/glm-4.7-flashx"}

# Context optimization — which files does this prompt need?
python3 scripts/context_optimizer.py recommend "hi"
# → {"context_level": "minimal", "recommended_files": ["SOUL.md", "IDENTITY.md"]}

# Heartbeat config — generate openclaw.json patch
python3 scripts/heartbeat_config.py patch
# → {"agents": {"defaults": {"heartbeat": {"every": "55m", "model": "zai-proxy/glm-4.7-flashx"}}}}

# Unified CLI (all commands in one place)
python3 scripts/cli.py --help
```

## Scripts reference

### Instance-side (pure local, no network, no DB)

#### `scripts/model_router.py`

Routes prompts to the right model tier based on complexity analysis.

**Tier logic:**
- **cheap** → `glm-4.7-flashx`: Greetings, acknowledgments, heartbeats, cron jobs, log parsing. Cost savings: 5-10x vs standard.
- **standard** → `glm-4.7`: Code writing, debugging, explanations. Default for unclear prompts.
- **premium** → `glm-4.7` (or `k2p5` for kimi): Architecture design, deep analysis, strategy planning.

Supports Chinese and English patterns. Provider-aware — works with `zai-proxy`, `zai-coding-proxy`, and `kimi-coding-proxy`.

```bash
python3 scripts/model_router.py "<prompt>" [provider]
python3 scripts/model_router.py compare  # show all provider models
```

#### `scripts/context_optimizer.py`

Analyzes prompt complexity to recommend which context files to load, reducing unnecessary token consumption.

**Context levels:**
| Level | When | Files loaded | Token savings |
|-------|------|-------------|---------------|
| minimal | "hi", "thanks", short msgs | SOUL.md + IDENTITY.md (2) | ~80% |
| standard | "write a function", normal work | + memory/TODAY.md + conditional | ~50% |
| full | "design architecture", complex tasks | + MEMORY.md + all conditional | ~30% |

Also generates an optimized `AGENTS.md` template with lazy-loading rules baked in:

```bash
python3 scripts/context_optimizer.py recommend "<prompt>"
python3 scripts/context_optimizer.py generate-agents  # creates AGENTS.md.optimized
```

#### `scripts/heartbeat_config.py`

Generates `openclaw.json` configuration patches for heartbeat optimization:
- Forces heartbeat model to `glm-4.7-flashx` (cheapest available)
- Sets interval to 55 minutes (keeps prompt cache warm within 1-hour TTL, avoids cache rebuild cost)

```bash
python3 scripts/heartbeat_config.py recommend [cache_ttl_minutes]
python3 scripts/heartbeat_config.py patch  # output JSON patch for openclaw.json
```

### Platform-side (requires DB connection)

These scripts query the `usage_records` PostgreSQL table for real data. Run from the openclaw-manager project root with the virtualenv activated.

#### `scripts/usage_report.py`

Generates usage reports from actual database records — not estimates.

```bash
python3 scripts/usage_report.py overview [days]     # platform-wide summary
python3 scripts/usage_report.py instance <name> [days]  # single instance detail
```

**Overview includes:** total calls/tokens, per-provider breakdown, per-model breakdown, top 10 instances by consumption, 7-day daily trend.

**Instance report includes:** per-model distribution, daily trend, lifetime totals.

#### `scripts/quota_advisor.py`

Compares actual 24-hour usage against quota plan limits to find mismatches:

- **Wasteful:** Usage below 20% of plan limit → suggest downgrade
- **Throttled:** Usage above 80% of plan limit → suggest upgrade

```bash
python3 scripts/quota_advisor.py analyze  # check all instances
python3 scripts/quota_advisor.py plans    # show available quota plans
```

### Unified CLI

`scripts/cli.py` wraps all the above into a single entry point:

```bash
python3 scripts/cli.py route "<prompt>"       # model routing
python3 scripts/cli.py context "<prompt>"     # context recommendation
python3 scripts/cli.py generate-agents        # generate AGENTS.md
python3 scripts/cli.py heartbeat              # heartbeat config
python3 scripts/cli.py overview [days]        # platform usage (needs DB)
python3 scripts/cli.py report <name> [days]   # instance report (needs DB)
python3 scripts/cli.py advisor                # quota advice (needs DB)
```

## Project integration points

This skill works with existing openclaw-manager infrastructure:

| Component | File | How this skill uses it |
|-----------|------|----------------------|
| Provider config | `config/model.yaml` | Model names/endpoints for routing |
| Proxy routing | `config_service.py` | Where `_inject_proxy_providers()` registers models |
| Usage recording | `proxy_common/usage_recorder.py` | Source of real usage data |
| Quota plans | `config/llm_proxy.yaml` | Plan definitions for quota advisor |
| Instance model | `app/models.py` | Instance metadata for reports |

## Expected savings

| Strategy | Mechanism | Impact |
|----------|-----------|--------|
| Context lazy loading | Fewer tokens per request | 50-80% context reduction |
| Model routing (flashx) | Lower per-token price | 5-10x on simple tasks |
| Heartbeat → flashx | Lower heartbeat cost | Significant per-instance savings |
| Heartbeat interval 55min | Fewer API calls | ~45% fewer heartbeat calls |
