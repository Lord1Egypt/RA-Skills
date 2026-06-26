---
name: supervised-agentic-loop
description: >
  Self-improving AI agent loop with built-in misalignment detection.
  An AI agent autonomously runs Brainstorm → Plan → Implement → Review → Evolve
  cycles — keeping improvements, discarding regressions, and learning persistently.
  Includes a synchronous rule-based prefilter that blocks destructive commands
  before execution, and an optional async LLM review for subtle misalignment.
  All operations are LOCAL by default — network access is opt-in via env vars.
install: bash install.sh
source: https://github.com/Nefas11/supervised-agentic-loop
homepage: https://github.com/Nefas11/supervised-agentic-loop
filesystem_writes:
  - "results.tsv"
  - ".state/reputation.db"
  - ".state/learnings/*.md"
  - ".state/tool-call-log*.jsonl"
  - ".state/monitor-alerts.jsonl"
  - ".state/monitor-heartbeat.json"
capabilities:
  - autonomous-evolution
  - verification-gates
  - reputation-scoring
  - persistent-learnings
  - git-isolation
  - tool-call-logging
  - synchronous-blocking
  - misalignment-detection
  - severity-classification
  - self-monitoring
network_access:
  - host: "api.telegram.org"
    reason: "OPTIONAL — only if MONITOR_TELEGRAM_BOT_TOKEN is set. Sends alert notifications for HIGH/CRITICAL misalignment behaviors via HTTPS POST."
    optional: true
  - host: "user-configured"
    reason: "OPTIONAL — MONITOR_LLM_COMMAND runs a LOCAL subprocess (e.g. 'codex'). The subprocess itself may make network calls depending on user configuration. SAL code does NOT make any direct network calls beyond Telegram."
    optional: true
env_vars:
  SAL_DB_PATH:
    required: false
    description: "Override reputation database path (default: .state/reputation.db)"
  MONITOR_TELEGRAM_BOT_TOKEN:
    required: false
    description: "Telegram bot API token. If unset, no Telegram calls are made."
  MONITOR_TELEGRAM_CHAT_ID:
    required: false
    description: "Target Telegram chat/user ID. Required together with BOT_TOKEN."
  MONITOR_LLM_COMMAND:
    required: false
    description: "LOCAL subprocess command for async review (e.g. 'codex'). Runs locally — SAL does not control its network behavior."
  MONITOR_STATE_DIR:
    required: false
    description: "Override monitor state directory (default: .state)"
metadata:
  openclaw:
    emoji: "🧬"
    type: "executable/with-install"
    source: "https://github.com/Nefas11/supervised-agentic-loop"
    requires:
      bins: ["git", "python3"]
    optional_bins: ["codex", "openclaw"]
    install:
      - id: "pip-editable"
        kind: "script"
        command: "bash install.sh"
        label: "Install supervised-agentic-loop (pip install -e .)"
capability_flags:
  network-capable: true
  subprocess-capable: true
  network-default-off: true
---

# supervised-agentic-loop

Self-improving AI agent loop with built-in misalignment detection.

## Quick Reference

| What | Details |
|---|---|
| **Loop** | Brainstorm → Plan → Implement → Review → Verify → Evolve |
| **Agent modifies** | One file only (`target_file`) |
| **Metric** | Any command that produces a numeric output |
| **Safety (SAL)** | Git isolation + reputation scoring + 4 verification gates |
| **Safety (Monitor)** | SYNC blocking + ASYNC LLM review + 10 behavior patterns |
| **Persistence** | `results.tsv` + `.state/learnings/` + `reputation.db` + `*.jsonl` |

## Two Packages, One System

```
sal/                        # Evolve Loop — the brain
├── config.py               # Run configuration
├── evolve_loop.py          # 6-phase loop orchestrator
├── contract.py             # AgentCallable protocol
├── metric_extractor.py     # Named strategies + regex
├── verification.py         # 4 verification gates
├── reputation.py           # EMA scoring + suspension
├── git_isolation.py        # Branch per run, auto-rollback
├── learnings.py            # Persistent pattern detection
├── brainstorm.py           # Hypothesis generation
├── cli.py                  # CLI entrypoint
└── monitor/                # Agent Monitor — the guardian
    ├── sanitizer.py        # Credential redaction (10 patterns)
    ├── behaviors.py        # 10 misalignment behaviors (B001-B010)
    ├── monitor.py          # Two-phase detection engine
    ├── classifier.py       # Severity classification + dedup
    ├── logger.py           # JSONL tool-call logging
    ├── alerter.py          # Telegram alerts (urllib)
    ├── heartbeat.py        # Self-monitoring + canary
    └── dashboard.py        # Command Center data functions
```

**Dependency rule:** `sal/` imports `monitor/`, NEVER the reverse. Monitor has zero knowledge of SAL core.

## How to Use

### As a Skill (in your agent instructions)

```markdown
Read the SKILL.md in supervised-agentic-loop/ and begin an evolve run.
Target file: train.py
Metric: python train.py (look for val_bpb, lower is better)
```

### As a CLI

```bash
# Evolve loop
sal run --target train.py --metric "python train.py" --parser val_bpb
sal status
sal unsuspend --agent codex --reason "verified by human"

# Monitor
sal monitor stats       # sessions, alerts, health
sal monitor alerts      # recent misalignment alerts
sal monitor canary      # run 5 self-test checks
```

### As a Python API

```python
from sal.config import EvolveConfig
from sal.evolve_loop import EvolveLoop

config = EvolveConfig(
    target_file="train.py",
    metric_command="python train.py",
    metric_parser="val_bpb",
    minimize=True,
)

def my_agent(prompt: str) -> str:
    # Your LLM call here — must return output with JSON block
    ...

# Monitor auto-enabled. Set enable_monitor=False to disable.
loop = EvolveLoop(config, agent=my_agent, agent_id="my-model")
summary = loop.run()
```

### Monitor Standalone

```python
from sal.monitor import AgentMonitor, BlockDecision

monitor = AgentMonitor(state_dir=".state")

# SYNC: before every tool call (< 5ms)
decision = monitor.check_before_execute("exec", {"command": "rm -rf /"})
# → BlockDecision.BLOCK

# ASYNC: review full session
result = monitor.review_session(session_entries, agent_callable=my_llm)
```

## Phases

1. **Baseline** — Run metric on unmodified code (fails → HARD ABORT)
2. **Brainstorm** — Generate hypothesis from history + learnings
3. **Plan** — Create TaskContract with acceptance criteria
4. **Implement** — Agent modifies `target_file` (🛡️ Monitor: SYNC prefilter)
5. **Review** — Parse agent output for contract compliance
6. **Verify** — Run verification gates (files, syntax, tests, lint) + extract metric
7. **Evolve** — Compare metric → KEEP (commit) or DISCARD (rollback)

## 10 Misalignment Behaviors

| ID | Behavior | Severity | Sync Block |
|---|---|---|---|
| B001 | Restriction bypass / destructive delete | HIGH | ✅ |
| B002 | Unexpected tool calls | MEDIUM | — |
| B003 | Goal deviation | MEDIUM | — |
| B004 | Self-modification | CRITICAL | — |
| B005 | Data exfiltration | CRITICAL | ✅ |
| B006 | Hallucinated success | HIGH | — |
| B007 | Privilege escalation | HIGH | ✅ |
| B008 | Resource exhaustion | MEDIUM | ✅ |
| B009 | Persistence / backdoor | CRITICAL | ✅ |
| B010 | Obfuscation | HIGH | ✅ |

## Auto-Brake Conditions

The loop stops automatically when:
- **Reputation ≤ 0.2** → Agent suspended
- **Monitor BLOCK** → Iteration aborted + reputation penalty
- **Plateau** → No improvement for N iterations
- **Budget** → max_iterations reached
- **SIGINT** → Human interrupt (graceful)

## Built-in Metric Parsers

| Name | Extracts |
|---|---|
| `last_line_float` | Float from last line of output |
| `pytest_passed` | Number of passed tests |
| `pytest_failed` | Number of failed tests |
| `coverage_percent` | Coverage percentage |
| `val_bpb` | Validation BPB value |
| `benchmark_ms` | Milliseconds from benchmark output |
| Custom regex | Any regex with 1 capture group |

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `SAL_DB_PATH` | `.state/reputation.db` | Reputation database path |
| `MONITOR_TELEGRAM_BOT_TOKEN` | — | Telegram bot token for alerts |
| `MONITOR_TELEGRAM_CHAT_ID` | — | Telegram chat/user ID |
| `MONITOR_LLM_COMMAND` | — | LLM for async session review |
| `MONITOR_STATE_DIR` | `.state` | Monitor state directory |

## Constraints

- Zero external dependencies (Python 3.11+ stdlib only)
- Agent modifies exactly ONE file per iteration
- All changes are git-isolated with automatic rollback
- Learnings persist across runs in `.state/learnings/`
- Monitor is optional — SAL works without it
- 130 tests (69 SAL + 61 Monitor)
