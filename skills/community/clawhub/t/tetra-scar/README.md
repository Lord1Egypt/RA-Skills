# tetra-scar

Scar memory and reflex arc for AI agents. Learn from failures permanently. Block repeated mistakes instantly — no LLM calls needed.

## See it in action

Run any of these to see the output immediately:

```bash
# Agent loop: fail once, scar blocks the repeat, agent adapts
python3 examples/example_agent_loop.py

# Incident response: secret leaks, scar prevents it forever
python3 examples/example_incident_response.py

# CI integration: plug scar-code-review into your pipeline
bash examples/example_ci_integration.sh
```

**[`example_agent_loop.py`](examples/example_agent_loop.py)** — A minimal autonomous agent that deploys without tests, fails, records a scar, and then gets blocked by the reflex arc when it tries the same thing again. Shows the full before/after in 50 lines.

**[`example_incident_response.py`](examples/example_incident_response.py)** — Simulates a secret leak that the built-in regex missed. Records an incident scar. Next time the agent tries to log a token, the reflex arc blocks it instantly. No LLM calls.

**[`example_ci_integration.sh`](examples/example_ci_integration.sh)** — Drop-in bash script for GitHub Actions / GitLab CI. Runs scar-code-review on changed files, fails the build on critical findings, and records them as scars so future reviews catch similar patterns faster.

## Install

```bash
# As an OpenClaw/ClawHub skill
npx clawhub@latest install b-button-corp/tetra-scar

# Or just copy tetra_scar.py into your project
cp tetra_scar.py /your/agent/
```

## What it does

Your agent keeps making the same mistakes. tetra-scar gives it a **scar layer** — immutable records of past failures that are checked before every action, without calling the LLM.

**Two-layer memory:**
- **Scar layer** (immutable): "What broke and what must never happen again"
- **Narrative layer** (mutable): "What was done and who benefited"

**Reflex arc:** pattern-matching against scars. No LLM, no API calls, no latency.

## Usage

### CLI

```bash
# Record a scar (after failure)
python3 tetra_scar.py scar-add \
  --what-broke "Deployed without tests" \
  --never-again "Always run test suite before deployment"

# Check before acting (reflex arc)
python3 tetra_scar.py reflex-check --task "Deploy latest changes"
# → BLOCKED — scar collision: 'Always run test suite...'

# 4-axis validation
python3 tetra_scar.py tetra-check --task "Add unit tests for auth"
# → APPROVED — all 4 axes passed

# Record success
python3 tetra_scar.py narrate --what "Added 12 auth tests" --who "Users"

# List scars / narrative
python3 tetra_scar.py list-scars
python3 tetra_scar.py list-narrative
```

### Python API

```python
from tetra_scar import reflex_check, tetra_check, read_scars
from tetra_scar import write_scar, write_narrative

# In your agent's main loop:
scars = read_scars()

# Quick reflex check (pattern matching only)
block = reflex_check(task, scars)
if block:
    print(f"BLOCKED: {block}")
    return

# Full 4-axis check
approved, reason = tetra_check(task, scars)
if not approved:
    print(f"REJECTED: {reason}")
    return

# Execute task...
if failed:
    write_scar("What broke", "Never again rule")
else:
    write_narrative("What was done", "Who benefited")
```

## How it works

**Reflex arc** extracts keywords from each scar's `never_again` field (English 3+ chars, Japanese kanji/katakana 2+ chars). When a task matches 40%+ of keywords (min 2), it's blocked instantly. No LLM, no API, no latency.

**4-axis check** validates tasks against:
1. **Emotion**: Has motivation (non-empty)
2. **Action**: Contains concrete verb
3. **Life**: No scar collision
4. **Ethics**: No dangerous ops (rm -rf, DROP TABLE, force push)

## File format

Append-only JSONL. Human-readable. Git-friendly.

```jsonl
{"id":"scar_001","what_broke":"...","never_again":"...","created_at":"2026-03-20T10:00:00"}
```

## Requirements

- Python 3.9+
- Zero external dependencies (stdlib only)

## GitHub Action — CI Safety Audit

Add agent safety scanning to your CI pipeline:

```yaml
# .github/workflows/scar-audit.yml
name: AI Safety Audit
on: [push, pull_request]
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: aibenyclaude-coder/tetra-scar@main
        with:
          fail-on: 'CRITICAL'  # Fail PR on critical findings
```

The action scans your code for common agent failure patterns (hardcoded secrets, bare excepts, force pushes, SQL injection, infinite retries, etc.) and posts a safety score in the PR summary.

## Tests

```bash
python3 -m pytest test_tetra_scar.py -v
# 37 tests, all passing
```

## Philosophy

Built by [Tetra Genesis](https://github.com/b-button-corp) (B Button Corp, Nagoya, Japan).

Agents that can't remember their failures repeat them. Scars are the immune system. Every cycle must answer: *"Who did this make happy?"*

## License

MIT-0
