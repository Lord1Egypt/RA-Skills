---
name: token-cost-optimization
description: Token savings and API cost optimization. Provides token calculator, three-tier optimization strategies (prompt compression / cache reuse / model downgrade), specific configuration guides, and quantified effect analysis.
---

# Token Cost Optimization

## Use Cases

User mentions token savings, API cost optimization, prompt compression, cache strategy, model downgrade, cost analysis.

## Quick Start

### Token Calculator
Run the calculation script, input conversation scale, and quickly estimate current token consumption and optimization potential:

```bash
python scripts/token_calculator.py
```

The script will prompt for:
- Number of conversation history items / average length
- Model and pricing used
- Current optimization status

Output: Current cost, optimized cost, savings percentage.

### Three-Tier Optimization Strategy
Ranked by effect / implementation cost:

| Tier | Strategy | Effect | Implementation Cost |
|------|----------|--------|---------------------|
| L1   | Prompt compression & output truncation | 10-30% | Low |
| L2   | Conversation summary caching | 30-50% | Medium |
| L3   | Model downgrade + task routing | 50-70% | High |

**Priority Recommendation**: Implement in order L1 → L2 → L3, verifying results at each stage before proceeding.

Detailed strategies, configuration guides, and pitfalls → See `references/tier-strategies.md`

## Phased Implementation Guide

### Phase 1: L1 Compression (Immediate Effect)
- Clean up redundant descriptions in system prompt
- Set max_tokens limits for long responses
- Remove outdated/unused messages from conversation history

### Phase 2: L2 Caching (1-3 Days)
- Establish FAQ shortcuts for high-frequency repeat questions
- Add summary compression at the beginning of conversations (execute every N rounds)

### Phase 3: L3 Routing (1-2 Weeks)
- Route simple tasks to cheaper models (e.g., 4o-mini / Haiku)
- Retain strong models for complex tasks
- Configure model routing rules

## Quantifiable Comparison Example

See the "Quantified Comparison" section in `references/tier-strategies.md` for details.