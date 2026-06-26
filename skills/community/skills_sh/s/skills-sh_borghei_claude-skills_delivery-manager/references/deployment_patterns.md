# Deployment Patterns: Blue-Green, Canary, Rolling

Read this when selecting a deployment strategy and defining its rollback path and canary success thresholds. Moved verbatim from `SKILL.md`.

## Select Deployment Strategy

| Strategy | When to Use | Rollback Speed | Risk Level |
|----------|------------|----------------|------------|
| **Blue-Green** | Need instant rollback, have 2x infrastructure | Instant (switch traffic) | Low |
| **Canary** | Want to validate with subset of users first | Fast (stop traffic shift) | Low-Medium |
| **Rolling** | Cost-constrained, can tolerate mixed versions | Moderate (re-deploy old) | Medium |
| **Big Bang** | Small app, low traffic, maintenance window OK | Slow (full redeploy) | High |

**Blue-Green deployment:**
```
Load Balancer -> [BLUE v2.4 - Active] | [GREEN v2.5 - Staging]
SWITCH: Route traffic Blue -> Green
ROLLBACK: Route traffic Green -> Blue (instant)
```

**Canary deployment progression:**
```
Stage 1: 95% old / 5% new   -- Monitor for 30 min
Stage 2: 75% old / 25% new  -- Monitor for 1 hour
Stage 3: 50% old / 50% new  -- Monitor for 2 hours
Stage 4: 0% old / 100% new  -- Full rollout
```

**Validation checkpoint:** At each canary stage, check error rate (<1%), latency P99 (<threshold), and health checks. Any breach halts progression and triggers rollback.
