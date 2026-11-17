---
name: workflow-orchestration
version: 1.0.0
description: A lightweight workflow orchestration engine for multi-phase task coordination with routing, phase execution, and exception handling.
author: Terr123123
license: MIT
tags:
  - workflow
  - orchestration
  - coordination
  - phases
  - routing
  - exception-handling
repo: https://github.com/Terr123123/openclaw-skills/tree/main/core-stack/workflow-orchestration
---

# Workflow Orchestration Skill

## Overview

A lightweight workflow orchestration engine that enables multi-phase task coordination with intelligent routing, phase execution, gate validation, and exception handling.

## Key Features

- **3 Preset Workflow Templates**: Standard (8 phases), Lightweight (4 phases), Hotfix (5 phases)
- **Intelligent Task Routing**: Route tasks to appropriate workflows based on change type, size, and risk
- **Phase Execution & Gate Validation**: Execute phases with gate checks and artifact validation
- **Exception Handling**: Handle workflow exceptions with rollback triggers and escalation
- **Custom Workflow Support**: Register and run custom workflow definitions
- **Persistence**: Save/load workflow instances to/from JSON/YAML

## Use Cases

- Multi-agent task coordination
- Development workflow orchestration
- CI/CD pipeline management
- Project lifecycle coordination
- Enterprise workflow governance

## Installation

```bash
clawhub install workflow-orchestration
```

## Usage

### Basic Usage

```python
from workflow_orchestration import WorkflowOrchestrator

# Initialize with template
orchestrator = WorkflowOrchestrator(template="standard")

# Start workflow instance
instance = orchestrator.start_workflow("standard", {
    "change_type": "feature",
    "change_size": "m",
    "risk_level": "medium"
})

# Advance phase
result = orchestrator.advance_phase(instance.id, gate_passed=True)

# Handle exception
result = orchestrator.handle_exception(
    instance.id,
    ExceptionType.QUALITY_GATE_FAILURE,
    SeverityLevel.CRITICAL
)

# Get status
status = orchestrator.get_workflow_status(instance.id)
```

### Task Routing

```python
from workflow_orchestration import TaskMetadata, ChangeType, SizeLevel, RiskLevel

metadata = TaskMetadata(
    change_type=ChangeType.BUGFIX,
    change_size=SizeLevel.S,
    risk_level=RiskLevel.MEDIUM
)

workflow_name = orchestrator.route_task(metadata)
```

### Custom Workflow

```python
from workflow_orchestration import WorkflowConfig, PhaseConfig

custom_workflow = WorkflowConfig(
    name="custom",
    description="Custom workflow",
    phases=[
        PhaseConfig(id="step1", gate="gate1", agent="agent1"),
        PhaseConfig(id="step2", gate="gate2", agent="agent2"),
    ]
)

orchestrator.register_workflow(custom_workflow)
instance = orchestrator.start_workflow("custom", {})
```

## API Reference

### WorkflowOrchestrator

- `start_workflow(workflow_name, initial_context)` → Start a workflow instance
- `advance_phase(instance_id, gate_passed)` → Advance to next phase
- `handle_exception(instance_id, exception_type, severity)` → Handle exception
- `get_workflow_status(instance_id)` → Get instance status
- `route_task(metadata)` → Route task to appropriate workflow
- `register_workflow(workflow_config)` → Register custom workflow
- `save_instance(instance_id)` → Save instance state
- `load_instance(data)` → Load instance from data

## Parameters

- `template`: Workflow template (standard, lightweight, hotfix)
- `workflow_name`: Workflow to start
- `initial_context`: Initial context with change_type, change_size, risk_level
- `gate_passed`: Whether gate validation passes
- `exception_type`: Exception type (REQUIREMENT_CHANGE, TECHNICAL_DEBT, etc.)
- `severity`: Exception severity (MINOR, MAJOR, CRITICAL)

## Quality Metrics

- 80 comprehensive tests (unit + integration + e2e)
- Complete documentation
- Multi-format support (JSON/YAML)
- MIT License

## Changelog

### v1.0.0 (2026-07-02)

- Initial release
- 3 preset workflow templates
- Task routing engine
- Phase execution with gate validation
- Exception handling with rollback triggers
- Custom workflow support
- Persistence support