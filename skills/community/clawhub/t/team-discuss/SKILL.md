# Team-Discuss Skill

Multi-agent collaborative discussion tool for efficient collaboration and alignment.

## Features

- **Multi-round discussions**: Automatic progression until consensus or round limit
- **Dialectical logic**: Automatic citation detection, fallacy identification, argument quality assessment
- **Random speaking order**: Eliminates first-mover advantage
- **Shared state**: File-based persistence with concurrent access support
- **Real agent integration**: Call real sub-agents via sessions_spawn

## Use Cases

1. **Technology selection discussions** - SQLite vs PostgreSQL, React vs Vue, etc.
2. **Architecture design reviews** - Multi-role collaboration (architect, frontend, backend, tester)
3. **Product decision making** - Feature prioritization, UX trade-offs
4. **Philosophical debates** - Free will vs determinism, ethics in AI, consciousness theories
5. **Scientific controversies** - Interpretations of quantum mechanics, origins of life
6. **Policy analysis** - Economic strategies, environmental policies, social reforms
7. **Creative collaborations** - Story plot decisions, character development, artistic direction
8. **Any topic requiring multi-perspective analysis**

## Quick Start

### 1. Create Discussion

```python
from core import SharedStore, DiscussionOrchestrator
from models import Discussion, DiscussionConfig, Participant, AgentRole

# Initialize
store = SharedStore(base_dir="./discussions")
orchestrator = DiscussionOrchestrator(store)

# Create discussion
discussion = Discussion(
    id="my-discussion-001",
    topic="Which storage layer should we use?",
    description="SQLite vs PostgreSQL technology selection",
    max_rounds=3,
    config=DiscussionConfig(consensus_threshold=0.75),
    participants=[
        Participant(agent_id="architect", role_id=AgentRole.ARCHITECT),
        Participant(agent_id="backend", role_id=AgentRole.DEVOPS),
    ]
)

store.create_discussion(discussion)
```

### 2. Define Agent Callbacks

```python
async def agent_callback(discussion_id, round_num, previous_messages):
    # Build prompt
    prompt = build_prompt(round_num, previous_messages)
    
    # Call real agent
    response = await sessions_spawn(
        runtime="subagent",
        agentId="architect",
        mode="run",
        task=prompt
    )
    
    return response, MessageType.PROPOSAL

callbacks = {
    "architect": agent_callback,
    "backend": agent_callback,
}
```

### 3. Run Discussion

```python
# Run discussion
result = await orchestrator.run_discussion(discussion.id, callbacks)

# View results
print(f"Status: {result.status}")
print(f"Rounds: {result.current_round}")
print(f"Consensus: {result.consensus_level}")
```

## Dialectical Logic

### Automatic Detection

```python
from core import DialecticEngine

dialectic = DialecticEngine()
analysis = dialectic.analyze_message(message, previous_messages)

print(f"Quality: {analysis.quality}")  # strong/moderate/weak/fallacious
print(f"Score: {analysis.score}")
print(f"Citation: {analysis.has_citation}")
print(f"Fallacies: {analysis.fallacies}")
```

### Detected Fallacy Types

- `ad_hominem` - Personal attack
- `straw_man` - Straw man fallacy
- `false_dichotomy` - False dilemma
- `hasty_generalization` - Hasty generalization
- `appeal_to_authority` - Appeal to authority
- `slippery_slope` - Slippery slope

## Bias Prevention Mechanisms

### 1. Random Speaking Order

```python
# First round random shuffle, subsequent rounds rotate
order = coordinator.determine_speaking_order(
    participants,
    SpeakingOrder.ROUND_ROBIN
)
```

### 2. Mandatory Citation

From round 2, agents must cite opponent's original words:

```
I disagree with @architect's view:
> "Choosing PostgreSQL is not premature optimization"

This statement is misleading...
```

### 3. Devil's Advocate

Assign an agent to play devil's advocate:

```python
# Assign tester as Devil's Advocate
# Even if they agree internally, they must defend the minority position
```

## Project Structure

```
team-discuss/
├── src/
│   ├── core/
│   │   ├── shared_store.py      # Shared state storage
│   │   ├── orchestrator.py      # Multi-round orchestrator
│   │   ├── dialectic.py         # Dialectical logic engine
│   │   └── coordinator.py       # Coordinator logic
│   ├── agents/
│   │   └── bridge.py            # Agent bridge
│   └── models.py                # Data models
├── examples/
│   └── run_real_discussion.py   # Real discussion example
└── tests/
    └── test_integration.py      # Integration tests
```

## Configuration Options

### DiscussionConfig

```python
DiscussionConfig(
    max_rounds=5,                    # Maximum rounds
    min_rounds_before_consensus=2,   # Minimum rounds before consensus
    consensus_threshold=0.75,        # Consensus threshold (75% agreement)
    token_budget=50000,              # Token budget
)
```

### Speaking Order

```python
SpeakingOrder.FREE           # Free speaking (random)
SpeakingOrder.ROUND_ROBIN    # Round robin (recommended)
SpeakingOrder.ROLE_BASED     # Role-based priority
```

## Examples

### Technology Selection Discussion

```bash
# Run example
cd /root/.openclaw/workspace/data/projects/team-discuss
python3 examples/run_real_discussion.py
```

### Philosophical Debate Example

```python
# Create a philosophical discussion
discussion = Discussion(
    id="philosophy-debate-001",
    topic="Does free will exist, or is everything determined?",
    description="Philosophical debate on free will vs determinism",
    max_rounds=3,
    participants=[
        Participant(agent_id="philosopher1", role_id=AgentRole.REVIEWER),
        Participant(agent_id="scientist", role_id=AgentRole.ARCHITECT),
        Participant(agent_id="skeptic", role_id=AgentRole.TESTER),
    ]
)
```

Philosophical debates benefit from:
- **Dialectical logic** - Detects logical fallacies common in abstract reasoning
- **Mandatory citation** - Ensures philosophers engage with specific arguments
- **Multi-round structure** - Allows deep exploration of complex concepts

Sample output:
```
🔄 Round 1 started
💬 @architect (Architect):
   I support using PostgreSQL...
   📊 Quality: moderate (70.0 points)

💬 @backend (Backend Dev):
   I support using SQLite...
   📊 Quality: moderate (60.0 points)

✅ Round 1 ended

🔄 Round 2 started
💬 @architect:
   Responding to @backend:
   > "Premature optimization is the root of all evil"
   This statement confuses...
   📊 Quality: strong (85.0 points)
   📌 Citation: ✓

✅ Round 2 ended

✓ Discussion completed!
Final status: max_rounds_reached
Consensus level: partial
```

## Best Practices

### 1. Topic Design

- Clear, specific, debatable
- Avoid overly broad topics (e.g., "what's the best technology")
- Provide necessary context

### 2. Agent Selection

- Cover different perspectives (architecture, dev, test, product)
- Avoid homogeneity (don't use all backend devs)
- Consider adding Devil's Advocate

### 3. Round Settings

- Simple topics: 2-3 rounds
- Complex topics: 5 rounds
- Set `min_rounds_before_consensus` to prevent premature convergence

### 4. Result Interpretation

- `CONSENSUS_REACHED` - Consensus reached, can execute directly
- `MAX_ROUNDS_REACHED` - Requires human judgment
- `COMPLETED` - Discussion ended naturally

## Troubleshooting

### Agent Not Responding

```python
orchestrator = DiscussionOrchestrator(
    store=store,
    response_timeout=180  # Increase timeout
)
```

### Version Conflicts

Shared storage uses optimistic locking, automatically retries on conflict.

### Storage Location

```python
store = SharedStore(base_dir="/path/to/discussions")
```

## Extension Development

### Custom Agent Bridge

```python
class MyAgentBridge:
    async def generate_response(self, ...):
        # Custom calling logic
        pass
```

### Custom Dialectic Rules

```python
class MyDialecticEngine(DialecticEngine):
    def _detect_fallacies(self, content):
        # Add custom fallacy detection
        pass
```

## Related Links

- Project path: `/root/.openclaw/workspace/data/projects/team-discuss`
- Example code: `examples/run_real_discussion.py`
- Integration tests: `tests/test_integration.py`

## Version History

- v0.1.0 - Basic features: shared storage, multi-round orchestration, dialectical logic
- v0.2.0 - Real agent integration (sessions_spawn)
- v0.3.0 - CLI interface, Web UI (planned)

## Roadmap

### Coming Soon

| Feature | Status | Description |
|:---|:---:|:---|
| **Devil's Advocate** | 🚧 In Development | Auto-assign minority role, ensure opposition voices heard |
| **Stance Change Rewards** | 🚧 In Development | Reward agents for rationally changing position |
| **CLI Interface** | 📋 Planned | Command-line tool for creating/viewing/managing discussions |
| **REST API** | 📋 Planned | HTTP API for remote calls |
| **Web UI** | 📋 Planned | Visual discussion dashboard |

### Release Plan

- **v0.2.1** - Devil's Advocate + Stance Change Rewards
- **v0.3.0** - CLI Interface + REST API
- **v0.4.0** - Web UI Dashboard

> 📦 Published to [clawhub.com](https://clawhub.com)

---

## 中文简介

**Team-Discuss** 是一个多 Agent 协作讨论工具，支持多轮迭代、辩证逻辑分析、随机发言顺序等特性，帮助团队高效对齐方案。

### 核心功能

- ✅ 多轮讨论，自动推进
- ✅ 辩证逻辑，检测论证质量
- ✅ 随机发言顺序，消除偏向性
- ✅ 共享状态，持久化存储
- ✅ 真实 Agent 集成

### 快速开始

```bash
cd /root/.openclaw/workspace/data/skills/team-discuss
python3 example.py
```

### 项目路径

```
/root/.openclaw/workspace/data/projects/team-discuss/
```

### 即将发布

- 🚧 Devil's Advocate 机制
- 🚧 立场变更奖励
- 📋 CLI 接口
- 📋 REST API
- 📋 Web UI 仪表盘

> 📦 已发布到 [clawhub.com](https://clawhub.com)
