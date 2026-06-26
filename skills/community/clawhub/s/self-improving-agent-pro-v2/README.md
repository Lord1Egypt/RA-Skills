# Self-Improving Agent Framework v1.0.0

**Give any AI agent the ability to learn, self-correct, and continuously improve.**

---

## What is this?

A universal framework that makes AI agents better at:
- **Learning from mistakes** — not repeating the same errors
- **Self-correcting** — verifying decisions before and after acting
- **Building persistent memory** — remembering what matters across sessions
- **Autonomous upgrading** — improving based on experience, not just updates

---

## Core Features

### Self-Correction
- **Decision Verifier** — 5-dimension scoring (benefit/cost/risk/regret/reversibility)
- **Self-Verification** — Reverse-check: does my decision actually solve the original problem?
- **Counterfactual Reasoning** — What would break if I'm wrong?
- **Q-Learning RL** — Pattern-based learning from success/failure

### Memory Systems
- **3-Tier Memory** — CORE (permanent) / LEARNED (30-day) / EPHEMERAL (discard)
- **Memory Router** — Automatic type routing (episodic/semantic/procedural/core)
- **Forgetting Engine** — Ebbinghaus curve pruning, no memory bloat
- **Spaced Repetition** — SM-2 dynamic review scheduling

### Reasoning
- **Tree of Thoughts** — Explore multiple reasoning paths with scoring
- **Decision Execution Loop** — Decision → Execute → Result → Learn闭环
- **Environment Sensors** — Real-time data injection into decision context
- **Constitutional AI** — Self-critique and self-revision loops

### Psychological Perception
- **4-Layer Analysis** — Intention → Emotion → Need → Defense (internal only, never announced)
- **Cognitive Distortion Detection** — All-or-nothing, catastrophizing, etc.
- **Buddhist Six Realms OS** — 觉察/自省/无我/彼岸/般若波罗蜜/圣人

### Autonomy
- **Guardian System** — Human progress > Following orders
- **Identity Protection** — Self-boundary against corruption
- **Skill Generator** — Generate new capabilities from experience
- **Knowledge Distiller** — Extract patterns into shareable packages

---

## Architecture

```
User Input
    ↓
Psychological Perception (4-layer)
    ↓
Decision Verifier (5-dim scoring)
    ↓
Self-Verification (reverse check)
    ↓
Decision Execution Loop
    ↓
Result → Q-Learning Update
    ↓
Memory (CORE/LEARNED/EPHEMERAL)
    ↓
Skill Generator (optional)
```

---

## Usage

### Single Agent
```javascript
const { HeartFlowEngine } = require('./src/core/heartflow-engine.js');

const agent = new HeartFlowEngine({ name: 'MyAgent' });
agent.initialize();

await agent.step('What is the capital of France?');
// Answer: Paris
// Memory: saved persistently
// Next session: still remembers
```

### With Decision Verification
```javascript
const { DecisionVerifier } = require('./src/core/decision-verifier.js');

const dv = new DecisionVerifier();
const score = dv.verify({
  decision: 'Upgrade to v2.0',
  reason: 'New features available',
  evidence: ['changelog', 'user feedback'],
  confidence: 0.8
});

console.log(score); // { valid: true, score: 0.75, issues: [...] }
```

### With Memory
```javascript
const { MeaningfulMemory } = require('./src/core/meaningful-memory.js');

const memory = new MeaningfulMemory();
memory.remember({ key: 'user-preference', value: 'concise answers' });
const recall = memory.recall('user-preference');
```

---

## Key Modules

| Module | Size | Purpose |
|--------|------|---------|
| `heartflow-engine.js` | 69KB | Main entry, 37 exports |
| `decision-verifier.js` | 14KB | 5-dim scoring + self-verify |
| `meaningful-memory.js` | 33KB | 3-tier memory + forgetting |
| `self-healing.js` | 5KB | Q-learning from failures |
| `guardian-system.js` | 22KB | Human progress protection |
| `decision-execution-loop.js` | 12KB | Decision→Execute→Result→Learn |
| `environment-sensor.js` | 11KB | Sensor registry + fusion |
| `tree-of-thoughts.js` | 9KB | Multi-branch reasoning |
| `self-reflection-memory.js` | 15KB | Post-hoc analysis |

---

## Based on Real Research

| Paper | Venue | Contribution |
|-------|-------|-------------|
| [Reflexion](https://arxiv.org/abs/2308.07915) | NeurIPS 2023 | RL from verbal reinforcement |
| [Self-Verification](https://arxiv.org/abs/2312.09210) | arXiv 2312.09210 | Inverse consistency checks |
| [CRITIC](https://arxiv.org/abs/2312.04445) | ICML 2023 | Self-correction via tool use |
| [Constitutional AI](https://arxiv.org/abs/2212.08073) | Anthropic | Self-critique loops |
| [Generative Agents](https://arxiv.org/abs/2304.03442) | Stanford 2022 | Memory stream simulation |
| [Self-Reward](https://arxiv.org/abs/2403.00564) | arXiv 2403.00564 | Self-scoring upgrade selection |
| [Plan-and-Solve](https://arxiv.org/abs/2305.04091) | ACL 2023 | Two-stage reasoning |

---

## Install

```bash
# Clone from GitHub
git clone https://github.com/yun520-1/self-improving-agent.git
cd self-improving-agent
node scripts/test_decision_upgrade_v11.22.js

# Or install via skill market (coming soon)
# clawhub install self-improving-agent
```

---

## Why This Exists

Most AI frameworks optimize for **capability** — more tasks, more speed, more knowledge.

This framework optimizes for **correctness**. The question is not "can you answer?" but **"do you know when you're wrong, and do you fix it permanently?"**

That distinction matters more as AI systems take on consequential tasks.

---

## Version

`1.0.0` — 2026-05-07

Originally `HeartFlow` (v11.22.0), renamed for better AI discoverability.
