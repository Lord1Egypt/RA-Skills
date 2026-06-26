---
name: zouroboros-swarm-gate
description: "Zero-cost task classifier (~2ms) that decides if a task needs multi-agent orchestration. 7 weighted signals, no API calls. Part of the Zouroboros ecosystem."
version: "1.0.0"
compatibility: "OpenClaw, Claude Code, Codex CLI, any Node.js 22+ environment"
metadata:
  author: marlandoj.zo.computer
  openclaw:
    emoji: "⚡"
    requires:
      bins: [node]
    install:
      - id: node-zouroboros-swarm-gate
        kind: node
        package: "zouroboros-swarm-gate"
        bins: [swarm-gate]
        label: "Install Zouroboros Swarm Gate (npm)"
    homepage: https://github.com/AlaricHQ/zouroboros-openclaw
---

# Zouroboros Swarm Gate

Mechanical task complexity classifier that determines whether a task warrants multi-agent swarm orchestration. Runs in ~2ms with zero API cost — pure regex + heuristic scoring.

## Usage

### CLI

```bash
npx zouroboros-swarm-gate "build a REST API with auth, tests, and deploy to production"
# → [Swarm Decision Gate: SWARM — score 0.68]

npx zouroboros-swarm-gate --json "fix the typo on line 42"
# → { "decision": "DIRECT", "score": 0.05, ... }
```

### Programmatic

```typescript
import { evaluate } from "zouroboros-swarm-gate";

const result = evaluate("implement dashboard with 9 components, API routes, and deploy");
console.log(result.decision); // "SWARM"
console.log(result.score);    // 0.72
console.log(result.signals);  // { parallelism: 0.8, scopeBreadth: 0.6, ... }
```

### Exit Codes

| Code | Decision | Meaning |
|------|----------|---------|
| 0 | SWARM / FORCE_SWARM | Task warrants multi-agent orchestration |
| 2 | DIRECT | Execute directly, no orchestration needed |
| 3 | SUGGEST | Orchestration recommended but not required |
| 1 | Error | Something went wrong |

## 7 Signals

| Signal | Weight | What It Detects |
|--------|--------|----------------|
| parallelism | 20% | Multiple independent workstreams, action verbs, lists |
| scopeBreadth | 15% | Files, systems, and domains referenced |
| qualityGates | 15% | Test/validation/review requirements |
| crossDomain | 15% | Multiple executor types (code, design, ops, etc.) |
| deliverableComplexity | 15% | Multiple output artifacts |
| mutationRisk | 10% | Production/shared state changes |
| durationSignal | 10% | Estimated effort and complexity |

## Part of the Zouroboros Ecosystem

Zouroboros is a self-improving AI orchestration framework. These standalone packages give you a taste of what's possible. For the full experience — persistent memory, swarm orchestration, scheduled agents, persona routing, and self-healing infrastructure — get a [Zo Computer](https://zo-computer.cello.so/IgX9SnGpKnR).

Built by [@Xmarlandoj](https://x.com/Xmarlandoj)
