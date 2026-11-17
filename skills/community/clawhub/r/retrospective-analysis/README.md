# Retrospective Analysis

A project retrospective automation tool for friction identification, failure analysis, and improvement generation.

## Install

```bash
clawhub install retrospective-analysis
```

## Quick Start

```python
from src import RetrospectiveAnalyzer
from src.models import ProjectInfo, GateFriction

analyzer = RetrospectiveAnalyzer()
retro = analyzer.start_retrospective(
    ProjectInfo(name="Auth Refactor", team="Platform", duration="3 weeks", change_id="CH-42")
)

analyzer.add_what_went_well(retro.id, "fast design review")
analyzer.add_what_was_slow(retro.id, "manual test gate")
analyzer.add_what_failed(retro.id, "deploy rollback")
analyzer.add_gate_friction(
    retro.id,
    GateFriction(gate="testing-gate", issue="flaky tests", impact="blocked merge", suggested_change="stabilize suite"),
)

analysis = analyzer.analyze(retro.id)
report = analyzer.generate_report(retro.id)
print(analysis.severity, analysis.total_issues)
for item in report.action_items:
    print(item)
```

## Persistence

```python
analyzer.save_to_file(retro.id, "retro.json")
loaded = analyzer.load_from_file("retro.json")
analyzer.export_report(retro.id, "report.json")
```

## Tests

```bash
python -m pytest tests/ -v --tb=short
```

## License

MIT
