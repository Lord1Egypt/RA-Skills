---
name: task-routing
version: 1.0.0
description: A lightweight task routing engine for intelligent task assignment based on change type, size, risk, and urgency.
author: Terr123123
license: MIT
tags:
  - routing
  - task-assignment
  - prioritization
  - workflow-selection
  - agent-routing
repo: https://github.com/Terr123123/openclaw-skills/tree/main/core-stack/task-routing
---

# Task Routing Skill

## Overview

A lightweight task routing engine that enables intelligent task assignment based on task characteristics (type, size, risk, urgency).

## Key Features

- **16 Change Types**: Feature, bugfix, hotfix, refactor, docs, test, config, etc.
- **5 Size Levels**: XS, S, M, L, XL
- **4 Risk Levels**: Low, medium, high, critical
- **4 Urgency Levels**: Low, medium, high, urgent
- **6 Condition Operators**: equals, not_equals, in, not_in, greater_than, less_than
- **Priority Calculation**: Weighted priority scoring based on multiple factors
- **Batch Routing**: Route multiple tasks in single call
- **Rule Persistence**: Save/load routing rules to/from JSON

## Use Cases

- Workflow selection (development process)
- Agent assignment (multi-agent systems)
- Team allocation (capacity-based routing)
- Task prioritization (priority ranking)
- Enterprise governance (compliance routing)

## Installation

```bash
clawhub install task-routing
```

## Usage

### Basic Usage

```python
from task_routing.src import RoutingEngine
from task_routing.src.models import TaskMetadata, ChangeType, SizeLevel, RiskLevel

# Initialize routing engine
engine = RoutingEngine()

# Create task metadata
metadata = TaskMetadata(
    change_type=ChangeType.FEATURE,
    change_size=SizeLevel.M,
    risk_level=RiskLevel.MEDIUM
)

# Route task
decision = engine.route(metadata)
print(f"Target: {decision.target}")
print(f"Confidence: {decision.confidence}")
```

### Custom Routing Rules

```python
from task_routing.src.models import RoutingRule, RoutingCondition

custom_rule = RoutingRule(
    name="security_to_security_team",
    conditions=[
        RoutingCondition("change_type", ChangeType.SECURITY),
        RoutingCondition("risk_level", [RiskLevel.HIGH, RiskLevel.CRITICAL], "in")
    ],
    target="security_team",
    priority=200
)

engine.add_rule(custom_rule)
```

### Priority Ranking

```python
tasks = [
    TaskMetadata(ChangeType.SECURITY, SizeLevel.M, RiskLevel.CRITICAL),
    TaskMetadata(ChangeType.BUGFIX, SizeLevel.S, RiskLevel.HIGH),
    TaskMetadata(ChangeType.DOCS, SizeLevel.XS, RiskLevel.LOW),
]

ranking = engine.get_priority_ranking(tasks)
for r in ranking:
    print(f"Rank {r['rank']}: {r['task']['change_type']} - Priority: {r['priority_score']}")
```

## API Reference

- `route(metadata)` → Route single task
- `route_batch(tasks)` → Route multiple tasks
- `add_rule(rule)` → Add custom routing rule
- `remove_rule(rule_name)` → Remove routing rule
- `calculate_priority(metadata)` → Calculate priority score
- `get_priority_ranking(tasks)` → Get priority ranking
- `save_rules()` → Save rules to JSON
- `load_rules(rules_data)` → Load rules from JSON

## Quality Metrics

- 81 comprehensive tests (unit + integration + e2e)
- Multi-format serialization (JSON)
- Concurrent routing safety
- MIT License

## Changelog

### v1.0.0 (2026-07-03)

- Initial release
- 16 change types with routing rules
- Priority calculation engine
- Batch routing support
- Rule persistence support