# Team-Discuss Skill

Multi-agent collaborative discussion tool for efficient collaboration and alignment.

## Features

- ✅ Multi-round discussions with auto-progression
- ✅ Dialectical logic for argument quality assessment
- ✅ Random speaking order to eliminate bias
- ✅ Shared state with persistent storage
- ✅ Real agent integration via sessions_spawn

## Quick Start

```bash
# Run example
cd /path/to/team-discuss
python3 teamDiscuss.py
```

## Full Documentation

See [SKILL.md](SKILL.md) for complete documentation.

## Project Location

Source code location:
```
/path/to/team-discuss/
```

## Core Components

| Component | Path | Function |
|:---|:---|:---|
| Shared Store | `src/core/shared_store.py` | File persistence, optimistic locking |
| Orchestrator | `src/core/orchestrator.py` | Multi-round discussion lifecycle |
| Dialectic | `src/core/dialectic.py` | Argument quality assessment |
| Agent Bridge | `src/agents/bridge.py` | sessions_spawn integration |

## Usage Example

```python
from core import SharedStore, DiscussionOrchestrator

# Initialize
store = SharedStore(base_dir="./discussions")
orchestrator = DiscussionOrchestrator(store)

# Create discussion
discussion = Discussion(...)
store.create_discussion(discussion)

# Run discussion
result = await orchestrator.run_discussion(discussion.id, callbacks)
```

## Real Agent Discussion

```bash
# Run real multi-agent discussion
cd /path/to/team-discuss
python3 examples/run_real_discussion.py
```

## Roadmap

Coming Soon:
- 🚧 Devil's Advocate mechanism
- 🚧 Stance change rewards
- 📋 CLI interface
- 📋 REST API
- 📋 Web UI dashboard

> 📦 Published to: [clawhub.com](https://clawhub.com)

## License

MIT
