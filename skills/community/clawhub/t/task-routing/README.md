# Task Routing Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![ClawHub](https://img.shields.io/badge/ClawHub-v1.0.0-blue.svg)](https://clawhub.ai/skills/task-routing)
[![Tests](https://img.shields.io/badge/Tests-81%20passed-green.svg)](tests/)

A lightweight task routing engine for intelligent task assignment.

## Features

- ✅ 16 change types with routing rules
- ✅ Priority calculation engine
- ✅ Batch routing support
- ✅ Custom routing rules
- ✅ Rule persistence (JSON)
- ✅ Concurrent routing safety

## Installation

```bash
clawhub install task-routing
```

## Quick Start

```python
from task_routing.src import RoutingEngine
from task_routing.src.models import TaskMetadata, ChangeType, SizeLevel, RiskLevel

engine = RoutingEngine()
metadata = TaskMetadata(ChangeType.FEATURE, SizeLevel.M, RiskLevel.MEDIUM)
decision = engine.route(metadata)
```

## Tests

81 comprehensive tests covering unit, integration, and end-to-end scenarios.

```bash
python -m pytest tests/ -v
```

## License

MIT License - free for personal and commercial use.

## Author

Terr123123

## Links

- ClawHub: https://clawhub.ai/skills/task-routing
- GitHub: https://github.com/Terr123123/openclaw-skills/tree/main/core-stack/task-routing