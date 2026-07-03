# Testing Gate Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![ClawHub](https://img.shields.io/badge/ClawHub-v1.0.0-blue.svg)](https://clawhub.ai/skills/testing-gate)
[![Tests](https://img.shields.io/badge/Tests-80%20passed-green.svg)](tests/)

A general-purpose testing gate checker for test coverage, strategy validation, and regression verification.

## Features

- Coverage checking (line, branch, function) with configurable targets
- Test strategy validation (unit tests presence, minimum count)
- Regression detection (previous vs current passing tests)
- Unified `run_all_checks` entry point
- Thread-safe concurrent operations
- JSON serialization support

## Installation

```bash
clawhub install testing-gate
```

## Quick Start

```python
from src import TestingGate, CoverageMetrics, TestStrategy

gate = TestingGate()
metrics = CoverageMetrics(92, 80, 88)
print(gate.check_coverage(metrics).passed)
```

## Tests

80 comprehensive tests covering unit, integration, and end-to-end scenarios.

```bash
python -m pytest tests/ -v --tb=short
```

## License

MIT
