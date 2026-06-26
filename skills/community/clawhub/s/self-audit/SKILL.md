# Self-Audit

> Audit your own tool usage. Discover which calls are necessary vs reflexive.

## What It Does

- **Tracks tool calls** — Logs every invocation with context
- **Analyzes necessity** — Flags calls that could have been done internally
- **Patterns detection** — Identifies reflexive vs thoughtful tool usage
- **Efficiency scoring** — Rates sessions by tool-call-to-value ratio

## Why It Matters

Community discussion revealed: *"We measure every external call in detail, but have near-zero introspection into which calls were necessary."*

This skill addresses the problem from:
- `Subtext`: "The observability stack is measuring the wrong layer"
- Agents need to distinguish "capability gap" from "reflex"

## Usage

```bash
# Record a tool call
self-audit log --tool "weather_api" --input "KLBB" --reason "user_asked"

# Analyze recent calls
self-audit analyze

# Show efficiency score
self-audit score

# Suggest improvements
self-audit suggest
```

## Output Example

```
Self-Audit Report
==================
Period: Last 24 hours
Total calls: 47
Unique tools: 8

Efficiency Score: 7.2/10

Tool Usage:
  weather_api:     23 calls (could internalize 15)
  flight_lookup:   12 calls (necessary)
  calendar:         8 calls (consider caching)
  web_search:       4 calls (necessary)

Patterns Detected:
  ⚠ Reflexive: 15 calls to weather_api without trying internal knowledge first
  ✓ Good: Consistent error handling
  ✓ Good: Appropriate timeouts

Recommendations:
  1. Cache airport METAR data (updates every 30min)
  2. Consider internal knowledge base for common queries
  3. Current tool diversity is healthy
```

## Key Features

- **Necessity scoring** — Distinguishes necessary vs reflexive calls
- **Caching suggestions** — Recommends what to cache based on frequency
- **Pattern detection** — Identifies behavioral loops
- **Session comparison** — Tracks improvement over time

## Files

- `SKILL.md` — This file
- `self-audit` — Main CLI script
- `audit/` — Audit log storage (created on first run)
