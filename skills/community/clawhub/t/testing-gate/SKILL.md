---
name: testing-gate
version: 1.0.0
description: A testing gate checker for test coverage, strategy validation, and regression verification.
author: Terr123123
license: MIT
tags:
  - testing
  - coverage
  - quality-assurance
  - regression
---

# Testing Gate Skill

## Overview

A general-purpose testing gate checker that validates test coverage, test strategy soundness, and regression necessity. Use it as a quality gate before merging or releasing code.

## Key Features

- **Coverage Checking**: Validate line, branch, and function coverage against configurable targets.
- **Test Strategy Validation**: Ensure test suites have unit tests and meet minimum test count.
- **Regression Verification**: Detect regressions by comparing previously passing tests against current results.
- **Unified Gate API**: Run all checks via a single `run_all_checks` entry point.
- **Thread-Safe**: Concurrent checks are safe via internal locking.
- **Serialization**: Full JSON round-trip for metrics, strategies, and results.

## Use Cases

- CI/CD quality gates before merge
- Release-readiness verification
- Regression detection after changes
- Test coverage enforcement
- Hotfix verification

## Installation

```bash
clawhub install testing-gate
```

## Usage

### Basic Usage

```python
from src import TestingGate, CoverageMetrics, TestStrategy

gate = TestingGate()

# Check coverage
metrics = CoverageMetrics(line_coverage=92, branch_coverage=80, function_coverage=88)
result = gate.check_coverage(metrics)
print(result.passed, result.score)

# Check test strategy
strategy = TestStrategy(
    unit_tests=["test_a", "test_b"],
    integration_tests=["test_int"],
    e2e_tests=["test_e2e"],
    min_test_count=3,
)
result = gate.check_test_strategy(strategy)

# Check regression
result = gate.check_regression({
    "previous_passing": 50,
    "current_passing": 50,
    "current_total": 50,
})

# Run all checks at once
context = {
    "coverage_metrics": metrics,
    "test_strategy": strategy,
    "regression_artifacts": {
        "previous_passing": 50,
        "current_passing": 55,
        "current_total": 55,
        "new_tests": 5,
    },
}
results = gate.run_all_checks(context)
print(gate.overall_passed())
```

### Custom Targets

```python
metrics = CoverageMetrics(
    line_coverage=60,
    branch_coverage=50,
    function_coverage=60,
    target_line=60,
    target_branch=50,
    target_function=60,
)
```

## API Reference

- `check_coverage(metrics: CoverageMetrics) -> GateResult` - Check coverage against targets
- `check_test_strategy(strategy: TestStrategy) -> GateResult` - Check test strategy validity
- `check_regression(artifacts: Dict) -> GateResult` - Check for regressions
- `run_all_checks(context: Dict) -> List[GateResult]` - Run all enabled checks
- `overall_passed() -> bool` - True if all recorded results passed
- `clear()` - Clear recorded results

## Quality Metrics

- 80 comprehensive tests (unit + integration + e2e)
- Thread-safe concurrent operations
- JSON serialization support
- MIT License

## Changelog

### v1.0.0 (2026-07-03)

- Initial release
- Coverage, strategy, and regression checking
- Thread-safe implementation
- 80 tests covering unit, integration, and end-to-end scenarios
