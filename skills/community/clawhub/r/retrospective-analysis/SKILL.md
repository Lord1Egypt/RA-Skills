---
name: retrospective-analysis
version: 1.0.0
description: A project retrospective automation tool for friction identification, failure analysis, and improvement generation.
author: Terr123123
license: MIT
tags:
  - retrospective
  - analysis
  - improvement
  - process-optimization
repo: https://github.com/Terr123123/openclaw-skills/tree/main/business-stack/retrospective-analysis
---

# Retrospective Analysis Skill

## Overview

A project retrospective automation tool that helps teams identify process friction points, analyze failure causes, and generate actionable improvement candidates.

## Key Features

- **Structured Retrospectives**: Track what went well, what was slow, what failed, and gate friction.
- **Automatic Analysis**: Compute issue counts, friction points, and severity (low/medium/high/critical).
- **Improvement Generation**: Derive prioritized improvement candidates from frictions and failures.
- **Report Generation**: Produce recommendations and action items from a retrospective.
- **JSON Persistence**: Save/load retrospectives and export reports to disk.
- **Thread Safety**: Concurrent adds and retrospective creation are safe.

## Use Cases

- Post-change retrospective record keeping
- Process friction identification across gate checkpoints
- Continuous improvement candidate backlog generation
- Team retrospective reporting and archival

## Installation

```bash
clawhub install retrospective-analysis
```

## Usage

### Basic Usage

```python
from src import RetrospectiveAnalyzer
from src.models import ProjectInfo, GateFriction

analyzer = RetrospectiveAnalyzer()

project = ProjectInfo(name="Auth Refactor", team="Platform", duration="3 weeks", change_id="CH-42")
retro = analyzer.start_retrospective(project)

analyzer.add_what_went_well(retro.id, "fast design review")
analyzer.add_what_was_slow(retro.id, "manual test gate")
analyzer.add_what_failed(retro.id, "deploy rollback")
analyzer.add_gate_friction(
    retro.id,
    GateFriction(gate="testing-gate", issue="flaky tests", impact="blocked merge", suggested_change="stabilize suite"),
)

analysis = analyzer.analyze(retro.id)
print(analysis.severity, analysis.total_issues)

report = analyzer.generate_report(retro.id)
for item in report.action_items:
    print(item)
```

### Persistence

```python
analyzer.save_to_file(retro.id, "retro.json")
loaded = analyzer.load_from_file("retro.json")
analyzer.export_report(retro.id, "report.json")
```

## API Reference

### RetrospectiveAnalyzer

- `start_retrospective(project_info) -> Retrospective` — start a new retrospective
- `add_what_went_well(retro_id, item) -> None` — record something that went well
- `add_what_was_slow(retro_id, item) -> None` — record something slow/redundant
- `add_what_failed(retro_id, item) -> None` — record a failure/rework cause
- `add_gate_friction(retro_id, friction) -> None` — record gate friction
- `analyze(retro_id) -> AnalysisResult` — analyze the retrospective
- `generate_report(retro_id) -> RetrospectiveReport` — generate a report
- `get_improvement_candidates(retro_id) -> List[ImprovementCandidate]` — get candidates
- `archive(retro_id) -> None` — archive the retrospective
- `save_to_file(retro_id, path)` / `load_from_file(path)` / `export_report(retro_id, path)` — persistence

### Models

- `RetroStatus`: ACTIVE / ANALYZED / REPORTED / ARCHIVED
- `ProjectInfo`: name, team, duration, change_id
- `GateFriction`: gate, issue, impact, suggested_change
- `ImprovementCandidate`: target, recommendation, reason, priority
- `AnalysisResult`: total_issues, friction_points, improvement_candidates, summary, severity
- `Retrospective`: id, project_info, status, what_went_well, what_was_slow, what_failed, gate_frictions, created_at
- `RetrospectiveReport`: retro_id, project_info, analysis, recommendations, action_items

## Severity Logic

| Total Issues | Severity |
|--------------|----------|
| 0            | low      |
| 1–4          | medium   |
| 5–9          | high     |
| 10+          | critical |

## Quality Metrics

- 81 comprehensive tests (unit + extended unit + integration + e2e)
- JSON serialization round-trips for all models
- Concurrent operation safety
- MIT License

## Changelog

### v1.0.0 (2026-07-03)

- Initial release
- Retrospective lifecycle management
- Friction identification and failure analysis
- Improvement candidate generation with priority
- Report generation and JSON persistence
