# Workflow Orchestration Skill - Usage Guide

## Installation

```bash
clawhub install workflow-orchestration
```

## Basic Usage

### 1. Initialize Orchestrator

```python
from workflow_orchestration import WorkflowOrchestrator

# Initialize with default template
orchestrator = WorkflowOrchestrator(template="standard")

# Or specify template
orchestrator = WorkflowOrchestrator(template="lightweight")
```

### 2. Start Workflow

```python
# Start standard workflow
instance = orchestrator.start_workflow("standard", {
    "change_type": "feature",
    "change_size": "m",
    "risk_level": "medium"
})

# Start lightweight workflow
instance = orchestrator.start_workflow("lightweight", {
    "change_type": "docs"
})

# Start hotfix workflow
instance = orchestrator.start_workflow("hotfix", {
    "change_type": "bugfix"
})
```

### 3. Advance Phase

```python
# Advance with gate passed
result = orchestrator.advance_phase(instance.id, gate_passed=True)

# Check result
if result.success:
    print(f"Advanced to: {instance.current_phase}")
else:
    print(f"Phase failed: {result.message}")
```

### 4. Handle Exceptions

```python
from workflow_orchestration import ExceptionType, SeverityLevel

# Handle minor exception
result = orchestrator.handle_exception(
    instance.id,
    ExceptionType.TECHNICAL_DEBT,
    SeverityLevel.MINOR
)

# Handle critical exception (triggers rollback)
result = orchestrator.handle_exception(
    instance.id,
    ExceptionType.PRODUCTION_ISSUE,
    SeverityLevel.CRITICAL
)
```

## Task Routing

### Route Task to Workflow

```python
from workflow_orchestration import TaskMetadata, ChangeType, SizeLevel, RiskLevel

metadata = TaskMetadata(
    change_type=ChangeType.BUGFIX,
    change_size=SizeLevel.S,
    risk_level=RiskLevel.MEDIUM
)

workflow_name = orchestrator.route_task(metadata)
print(f"Routed to: {workflow_name}")
```

### Routing Rules

- Bugfix/hotfix → hotfix workflow
- Docs/config/prompt (small + low risk) → lightweight workflow
- High risk → standard workflow
- Large size → standard workflow
- Feature/refactor → standard workflow

## Custom Workflows

### Register Custom Workflow

```python
from workflow_orchestration import WorkflowConfig, PhaseConfig, TransitionRule

custom_workflow = WorkflowConfig(
    name="custom",
    description="Custom workflow for my project",
    phases=[
        PhaseConfig(id="step1", gate="gate1", agent="agent1"),
        PhaseConfig(id="step2", gate="gate2", agent="agent2"),
        PhaseConfig(id="step3", gate="gate3", agent="agent3"),
    ],
    transitions=[
        TransitionRule("step1", "step2", "gate1 passed"),
        TransitionRule("step2", "step3", "gate2 passed"),
    ]
)

orchestrator.register_workflow(custom_workflow)
```

### Run Custom Workflow

```python
instance = orchestrator.start_workflow("custom", {})
```

## Persistence

### Save Instance

```python
# Save instance state to dict
instance_data = orchestrator.save_instance(instance.id)

# Save to file
import json
with open("instance.json", "w") as f:
    json.dump(instance_data, f)
```

### Load Instance

```python
# Load from file
with open("instance.json", "r") as f:
    instance_data = json.load(f)

# Load into orchestrator
loaded_instance = orchestrator.load_instance(instance_data)
```

## Workflow Templates

### Standard Workflow (8 Phases)

1. requirement → 2. design → 3. development → 4. code_review → 5. test_planning → 6. testing → 7. reflection → 8. archive

### Lightweight Workflow (4 Phases)

1. clarify → 2. update → 3. verify → 4. archive

### Hotfix Workflow (5 Phases)

1. diagnose → 2. fix → 3. regression_test → 4. reflection → 5. archive

## Exception Types

- REQUIREMENT_CHANGE: Requirement changes
- TECHNICAL_DEBT: Technical debt discovered
- QUALITY_GATE_FAILURE: Quality gate fails
- PRODUCTION_ISSUE: Production issues
- PERFORMANCE_REGRESSION: Performance degradation

## Severity Levels

- MINOR: Small impact, local adjustment
- MAJOR: Medium impact, needs assessment
- CRITICAL: Large impact, requires rollback