---
name: revenue-studio
description: A revenue-first solofounder studio that watches markets, finds monetizable pain, validates offers, ships narrow products, and compounds commercial memory across launches. Uses massive parallel agent orchestration with 8 layers: Signal Mesh, Extraction, Opportunity Graph, Cofounder Council, Revenue Lab, Build Studio, Launch Loop, and Portfolio Allocator.
metadata:
  openclaw:
    requires: { bins: [] }
---

# Revenue-First Solofounder Studio

A complete system for seeking revenue through disciplined stage-gated autonomy.

## Architecture

### 8 Layers

1. **Signal Mesh** - Collect market signals from X, Reddit, RSS, changelogs
2. **Commercial Extraction** - Score pain severity and money signals
3. **Opportunity Graph** - Build market structure from signals
4. **Cofounder Council** - 7-agent decision making (CEO, PM, Skeptic, Economics, Monetization, Distribution, Research)
5. **Revenue Lab** - Validate pricing, offers, and channels before build
6. **Build Studio** - Ship narrow wedges with telemetry
7. **Launch Loop** - Outbound, content, and demo execution
8. **Portfolio Allocator** - Kill/pause/scale decisions

## Key Principles

- **Revenue-first** - No build without monetization + distribution signoff
- **Stage-gated** - 7 stages from Observe to Scale/Kill, no skipping
- **Parallel orchestration** - Spawn 40+ agents for speed
- **Memory continuity** - Write-ahead logging for restart resilience
- **Governance** - Hard rules, approval gates, audit trails

## Quick Start

```bash
# Spawn signal collection
openclaw spawn "collect market signals from X and Reddit"

# Run council review
openclaw spawn "run council review on thesis-001"

# Validate revenue hypothesis
openclaw spawn "create validation landing page for thesis-001"
```

## Output Files

Located in `revenue-studio/`:
- `QUICKSTART.md` - Operator's guide
- `portfolio/thesis-001.md` - First validated thesis
- `council/` - 7 decision frameworks
- `revenue-lab/` - Pricing, conversion, offer frameworks
- `governance/` - Rules, stage-gates, approvals
- `signals/` - Market intelligence
- `scoring/` - RWOS calculator

## Thesis Scoring

Revenue-Weighted Opportunity Score (RWOS):
```
RWOS = Pain × Frequency × Buyer Density × Purchase Intent ×
       Speed-to-$ × Retention × Margin × Distribution × Expansion
       − Penalties
```

Decision bands:
- 0-20: PASS
- 21-35: WEAK
- 36-50: MODERATE
- 51-65: STRONG
- 66-80: EXCELLENT
- 81-100: EXCEPTIONAL
