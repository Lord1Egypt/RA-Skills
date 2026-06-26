# Evolution Algorithms

Updated: 2026-04-15

Finance Journal now uses a two-layer evolution architecture:

1. long-term memory recall
2. bandit-style reranking and reminder generation

## Why Keep Bandit

Current data is still mostly trade-level, not full intraday state-action trajectories.
So the safest evolution layer remains:
- contextual recall of similar historical paths
- bandit-style prioritization of what to exploit first
- explicit risk-arm suppression

## What Changed

Previously the reminder layer relied heavily on direct tag overlap.
Now it can first draw candidates from:
- memory cells
- memory scenes
- hyperedge-linked contexts
- skill cards derived from stable paths

Then the existing bandit metrics decide:
- which historical arm is most worth rechecking
- which risk arm should be suppressed first

## Future Path

If richer trajectories later become available, the stack can evolve toward:
- embedding reranking
- stronger scene compaction
- offline RL or trajectory-policy learning

For now the recommended mode remains `contextual_bandit`.
