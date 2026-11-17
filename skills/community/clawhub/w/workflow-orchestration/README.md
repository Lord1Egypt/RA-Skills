# Workflow Orchestration Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![ClawHub](https://img.shields.io/badge/ClawHub-v1.0.0-blue.svg)](https://clawhub.ai/skills/workflow-orchestration)
[![Tests](https://img.shields.io/badge/Tests-80%20passed-green.svg)](tests/)

A lightweight workflow orchestration engine for multi-phase task coordination.

## Features

- ✅ 3 preset workflow templates (standard, lightweight, hotfix)
- ✅ Intelligent task routing based on change type, size, and risk
- ✅ Phase execution with gate validation
- ✅ Exception handling with rollback triggers
- ✅ Custom workflow support
- ✅ Persistence support (JSON/YAML)

## Installation

```bash
clawhub install workflow-orchestration
```

## Quick Start

```python
from workflow_orchestration import WorkflowOrchestrator

# Initialize
orchestrator = WorkflowOrchestrator(template="standard")

# Start workflow
instance = orchestrator.start_workflow("standard", {
    "change_type": "feature",
    "change_size": "m",
    "risk_level": "medium"
})

# Advance phase
result = orchestrator.advance_phase(instance.id, gate_passed=True)
```

## Documentation

- [Usage Guide](docs/usage-guide.md)
- [API Reference](docs/api-reference.md)

## Tests

80 comprehensive tests covering unit, integration, and end-to-end scenarios.

```bash
python -m pytest tests/ -v
```

## License

MIT License - free for personal and commercial use.

## Author

Terr123123

## Links

- ClawHub: https://clawhub.ai/skills/workflow-orchestration
- GitHub: https://github.com/Terr123123/openclaw-skills/tree/main/core-stack/workflow-orchestration