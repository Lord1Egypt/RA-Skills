# Contributing to self-smarter-everyday

Thank you for your interest in contributing to the **self-smarter-everyday** skill! This document provides guidelines for contributing new reflection prompts, evaluation metrics, skill templates, code improvements, and documentation.

---

## 🎯 How You Can Contribute

### 1. New Reflection Prompts

The daily and weekly reflection templates (`templates/daily-reflection.md`, `templates/weekly-evaluation.md`) use structured sections to guide self-assessment. You can contribute new sections or improve existing ones.

**What makes a good reflection prompt:**
- **Actionable** — The answer should lead to a concrete action or decision.
- **Measurable** — Include quantitative elements where possible (counts, percentages, time).
- **Non-redundant** — Check existing sections before adding new ones. If your idea overlaps with an existing section, propose an enhancement instead.
- **Context-aware** — Prompts should be relevant to AI agent operations, not generic journaling.

**How to contribute:**
1. Open an issue describing the new section and why it's valuable.
2. Draft the section in markdown, following the existing format (tables, bullet lists, example content).
3. Include at least one fully filled-in example (not just placeholder text).
4. Submit a pull request with the new section added to the appropriate template.

**Example proposal:**
```markdown
## Proposed Section: "Energy Management"

### Why:
Tracking energy levels across tasks helps identify patterns — some task types
are more draining than others. This enables better task scheduling.

### Format:
| Time Block | Energy Level (1-5) | Task Type | Notes |
|------------|-------------------|-----------|-------|
| 09:00-12:00 | 4 | Research | Fresh morning, good focus |
| 13:00-15:00 | 2 | Debugging | Post-lunch slump, slow progress |

### Example content:
[Include filled-in example]
```

### 2. New Evaluation Metrics

The `self_audit.py` script collects metrics in four categories: memory, errors, performance, and token efficiency. New metrics should follow these principles:

**Metric requirements:**
- **Collectible** — Can be measured programmatically from existing data sources (state files, logs, system metrics).
- **Meaningful** — Correlates with actual system quality or user experience.
- **Non-expensive** — Collection should take <1 second and not require external API calls.
- **Comparable** — Can be tracked over time (same unit, same scale across runs).

**How to add a new metric:**
1. Add a collector function in `scripts/self_audit.py` following the existing pattern:
   ```python
   def collect_your_metric(state_dir: Path) -> dict:
       """Description of what this metric measures."""
       # Read from state files, logs, or system metrics
       # Return a dict with metric values
       return {"metric_name": value, ...}
   ```
2. Add the collector to `generate_report()` in the same file.
3. Add the metric to `print_summary()` for human-readable output.
4. Update the health score calculation if the metric should affect it.
5. Document the metric in this file under "Metrics Registry" below.
6. Include a test case (see Testing Requirements).

**Metrics Registry:**

| Metric | Category | Unit | Range | Collector | Added In |
|--------|----------|------|-------|-----------|----------|
| `total_size_mb` | Memory | MB | 0+ | `collect_memory_metrics` | v1.0.0 |
| `file_count` | Memory | count | 0+ | `collect_memory_metrics` | v1.0.0 |
| `error_rate` | Errors | ratio | 0-1 | `collect_error_metrics` | v1.0.0 |
| `success_rate` | Performance | ratio | 0-1 | `collect_performance_metrics` | v1.0.0 |
| `token_efficiency` | Tokens | ratio | 0-1 | `collect_token_efficiency` | v1.0.0 |
| `health_score` | Overall | score | 0-100 | `generate_report` | v1.0.0 |

### 3. New Skill Templates

The improvement plan template (`templates/improvement-plan.md`) provides a structured format for planning system improvements. You can contribute new templates for other planning needs.

**Template ideas welcome:**
- Monthly strategic review template
- Incident post-mortem template
- Skill acquisition plan template
- Cross-agent knowledge sharing template
- Budget optimization plan template

**Template requirements:**
- Must include all section headers with descriptions of what goes in each section.
- Must include example filled-in content (not just empty placeholders).
- Must be at least 500 words (including example content).
- Must follow the existing markdown formatting style (tables, code blocks, emoji indicators).
- Must be relevant to AI agent self-improvement (not generic project management).

### 4. Code Improvements

**Areas where code contributions are most valuable:**
- Performance optimization (faster state file I/O, reduced memory usage).
- Better similarity algorithm for memory compaction (current: word overlap Jaccard).
- Additional mutation strategies for prompt evolution.
- More sophisticated fitness evaluation for prompt variants.
- Better error handling and recovery in the nightly routine.
- New phases for the nightly routine orchestrator.

**Code standards:**
- Python 3.8+ compatible (no f-string `=` syntax, no `match` statements).
- Type hints on function signatures (use `from typing import ...` for compatibility).
- Docstrings on all public functions (Google style).
- No external dependencies beyond Python standard library.
- All scripts must work without network access (offline-first).
- Maximum line length: 100 characters.
- Use `Path` objects (from `pathlib`) instead of string concatenation for file paths.

### 5. Documentation

Documentation improvements are always welcome:
- Fix typos, clarify ambiguous sections, add missing examples.
- Translate documentation to other languages.
- Create tutorials or walkthroughs for new users.
- Add diagrams explaining the system architecture.

---

## 🔀 Pull Request Process

### Before You Start
1. **Check existing issues** — Make sure your contribution isn't already planned or in progress.
2. **Open an issue first** — For significant changes (new sections, new metrics, refactoring), open an issue to discuss the approach before writing code.
3. **Fork and branch** — Fork the repository and create a feature branch from `main`.

### PR Requirements
1. **Single concern** — Each PR should address one specific improvement. Don't mix unrelated changes.
2. **Description** — Explain what changed and why. Reference the issue number if applicable.
3. **Testing** — All changes must pass existing tests and include new tests for new functionality (see Testing Requirements below).
4. **Documentation** — Update relevant documentation if your change affects behavior, configuration, or usage.
5. **No credentials** — Never include API keys, passwords, tokens, or other secrets. Use placeholders (`YOUR_API_KEY`, `sk-xxx`).
6. **Changelog** — Add an entry to `CHANGELOG.md` under `[Unreleased]` describing your change.

### Review Criteria

PRs are reviewed against these criteria:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Correctness | 30% | Does the code do what it claims? Are edge cases handled? |
| Consistency | 20% | Does it follow existing patterns and conventions? |
| Testing | 20% | Are there tests? Do they cover happy path and edge cases? |
| Documentation | 15% | Is the change documented? Are comments clear? |
| Simplicity | 15% | Is this the simplest solution that works? No over-engineering? |

### Review Timeline
- Initial review: within 48 hours of PR submission.
- Revision turnaround: contributors should aim for <72 hours between review feedback and updated PR.
- Stale PRs: PRs with no activity for 14 days will be closed with a note encouraging re-submission.

---

## 🧪 Testing Requirements

### Unit Tests
All new functions must have unit tests. The test structure follows the existing pattern:

```python
def test_your_function():
    """Test description."""
    # Arrange
    input_data = {...}
    expected = {...}
    
    # Act
    result = your_function(input_data)
    
    # Assert
    assert result == expected
```

### Integration Tests
New scripts or significant features should include integration tests:

```bash
# Test the full nightly routine in dry-run mode
python3 scripts/nightly_routine.py --dry-run --state-dir /tmp/test_state

# Verify state was not modified
test ! -f /tmp/test_state/routine_state.json
```

### Test Coverage Expectations
- **New functions:** 100% of public functions must have at least one test.
- **Edge cases:** Empty inputs, missing files, malformed JSON, permission errors.
- **Regression:** If fixing a bug, include a test that reproduces the bug before the fix.

### Running Tests
```bash
# Run all tests
python3 -m pytest tests/ -v

# Run specific test file
python3 -m pytest tests/test_self_audit.py -v

# Run with coverage
python3 -m pytest tests/ --cov=scripts/ --cov-report=term-missing
```

---

## 💬 Communication

### Issue Labels
- `enhancement` — New feature or improvement
- `bug` — Something isn't working
- `documentation` — Documentation improvements
- `good-first-issue` — Good for newcomers
- `help-wanted` — Extra attention needed

### Discussion Guidelines
- Be respectful and constructive.
- Focus on the problem, not the person.
- Provide evidence (logs, metrics, examples) when reporting bugs.
- Suggest solutions, not just problems.

---

## 📜 License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project. See the project root for license details.

---

*Thank you for helping make AI agents smarter every day!*
