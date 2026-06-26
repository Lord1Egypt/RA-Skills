# zouroboros-swarm-gate

Zero-cost task complexity classifier (~2ms, no API calls). Scores whether a task warrants multi-agent swarm orchestration using 7 weighted signals.

## Install

```bash
npm install -g zouroboros-swarm-gate
```

## CLI

```bash
npx zouroboros-swarm-gate "build a REST API with auth, tests, and deploy"
# → SWARM (score 0.68)

npx zouroboros-swarm-gate --json "fix typo on line 42"
# → { "decision": "DIRECT", "score": 0.05, ... }
```

**Exit codes:** `0` = SWARM, `2` = DIRECT, `3` = SUGGEST, `1` = Error

## API

```typescript
import { evaluate } from "zouroboros-swarm-gate";

const result = evaluate("implement dashboard with 9 components and API routes");

result.decision;      // "SWARM" | "DIRECT" | "SUGGEST" | "FORCE_SWARM"
result.score;         // 0.0–1.0+
result.signals;       // { parallelism: 0.8, scopeBreadth: 0.6, ... }
result.weightedSignals;
result.override;      // "force_swarm" | "bias_direct" | null
result.reason;        // Human-readable explanation
result.directive;     // Pipeline instructions (for SWARM/SUGGEST)
result.performanceMs; // ~2ms
```

### Custom thresholds

```typescript
const result = evaluate("task description", {
  thresholdSwarm: 0.50,   // default: 0.45
  thresholdSuggest: 0.35, // default: 0.30
  biasDirectPenalty: 0.20, // default: 0.15
});
```

## Signals

| Signal | Weight | Detects |
|--------|--------|---------|
| parallelism | 20% | Multiple independent workstreams |
| scopeBreadth | 15% | Files/systems/domains touched |
| qualityGates | 15% | Test/validation requirements |
| crossDomain | 15% | Multiple executor types needed |
| deliverableComplexity | 15% | Multiple output artifacts |
| mutationRisk | 10% | Production/shared state changes |
| durationSignal | 10% | Estimated effort/complexity |

## Overrides

- `"use swarm"` / `"swarm this"` → **FORCE_SWARM** (bypass scoring)
- `"just"` / `"quick"` / `"simple"` → **BIAS_DIRECT** (penalty -0.15)

## OpenClaw

Works as an OpenClaw skill. Install via ClawHub:

```bash
clawhub install zouroboros-swarm-gate
```

Runnable starter:
- `https://github.com/AlaricHQ/zouroboros-openclaw-examples/tree/main/examples/swarm-gate`

## Part of the Zouroboros Ecosystem

This package is part of the OpenClaw-facing distribution surface at `AlaricHQ/zouroboros-openclaw`. The canonical upstream framework lives at `marlandoj/Zouroboros`.

For the full experience — persistent memory, swarm orchestration, scheduled agents, persona routing, and self-healing infrastructure — get a [Zo Computer](https://zo-computer.cello.so/IgX9SnGpKnR).

## License

MIT
