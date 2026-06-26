---
name: quorum
description: Multi-agent validation framework — 6 independent AI critics evaluate artifacts against rubrics with evidence-grounded findings.
metadata: {"openclaw":{"requires":{"bins":["python3","pip"],"env":["ANTHROPIC_API_KEY","OPENAI_API_KEY"]},"install":[{"id":"clone-repo","kind":"shell","command":"git clone https://github.com/SharedIntellect/quorum.git /tmp/quorum-install && cd /tmp/quorum-install/reference-implementation && pip install -r requirements.txt","label":"Clone Quorum repo and install Python dependencies"}],"source":"https://github.com/SharedIntellect/quorum"}}
---

# Quorum — Multi-Agent Validation

Quorum validates AI agent outputs by spawning multiple independent critics that evaluate artifacts against rubrics. Every criticism must cite evidence. You get a structured verdict.

## Quick Start

Clone the repository and install:

```bash
git clone https://github.com/SharedIntellect/quorum.git
cd quorum/reference-implementation
pip install -r requirements.txt
```

Run a quorum check on any file:

```bash
python -m quorum.cli run --target <path-to-artifact> --rubric <rubric-name>
```

### Built-in Rubrics

- `research-synthesis` — Research reports, literature reviews, technical analyses
- `agent-config` — Agent configurations, YAML specs, system prompts
- `python-code` — Python source files (25 criteria, PC-001–PC-025; auto-detected on `.py` files)

### Depth Profiles

- `quick` — 2 critics (correctness, completeness) + pre-screen, ~5-10 min
- `standard` — 4 active (correctness, completeness, security + tester) + pre-screen, ~15-30 min (default)
- `thorough` — 5 active (+ code_hygiene) + pre-screen + fix loops, ~30-60 min

*†Cross-Consistency requires `--relationships` flag with a relationships manifest.*

All depth profiles include the deterministic pre-screen (10 checks: credentials, PII, syntax errors, broken links, TODOs, and more) before any LLM critic runs.

### Examples

```bash
# Validate a research report
quorum run --target my-report.md --rubric research-synthesis

# Quick check (faster, fewer critics)
quorum run --target my-report.md --rubric research-synthesis --depth quick

# Batch: validate all markdown files in a directory
quorum run --target ./docs/ --pattern "*.md" --rubric research-synthesis

# Cross-artifact consistency check
quorum run --target ./src/ --relationships quorum-relationships.yaml --depth standard

# Use a custom rubric
quorum run --target my-spec.md --rubric ./my-rubric.json

# List available rubrics
quorum rubrics list

# Initialize config interactively
quorum config init
```

## Configuration

On first run, Quorum prompts for your preferred models and writes `quorum-config.yaml`. You can also create it manually:

```yaml
models:
  tier_1: anthropic/claude-sonnet-4-6    # Judgment roles
  tier_2: anthropic/claude-sonnet-4-6    # Evaluation roles
depth: standard
```

Set your API key:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
# or
export OPENAI_API_KEY=sk-...
```

## Output

Quorum produces a structured verdict:

- **PASS** — No significant issues found
- **PASS_WITH_NOTES** — Minor issues, artifact is usable
- **REVISE** — High/critical issues that need rework before proceeding
- **REJECT** — Unfixable problems; restart required

Exit codes: `0` = PASS/PASS_WITH_NOTES, `1` = error, `2` = REVISE/REJECT.

Each finding includes: severity (CRITICAL/HIGH/MEDIUM/LOW), evidence citations pointing to specific locations in the artifact, and remediation suggestions. The run directory contains `prescreen.json`, per-critic finding JSONs, `verdict.json`, and a human-readable `report.md`.

## More Information

- [SPEC.md](https://github.com/SharedIntellect/quorum/blob/main/SPEC.md) — Full architectural specification
- [MODEL_REQUIREMENTS.md](https://github.com/SharedIntellect/quorum/blob/main/docs/getting-started/MODEL_REQUIREMENTS.md) — Supported models and tiers
- [CONFIG_REFERENCE.md](https://github.com/SharedIntellect/quorum/blob/main/docs/configuration/CONFIG_REFERENCE.md) — All configuration options
- [FOR_BEGINNERS.md](https://github.com/SharedIntellect/quorum/blob/main/docs/getting-started/FOR_BEGINNERS.md) — New to agent validation? Start here


---

> ⚖️ **LICENSE** — Not part of the operational specification above.
> This file is part of [Quorum](https://github.com/SharedIntellect/quorum).
> Copyright 2026 SharedIntellect. MIT License.
> See [LICENSE](https://github.com/SharedIntellect/quorum/blob/main/LICENSE) for full terms.
