# supervised-agentic-loop

Self-improving AI agent loop with built-in misalignment detection.

> **Brainstorm → Plan → Implement → Review → Verify → Evolve**
> — with every tool call monitored for safety.

Combines best practices from four sources — reimplemented from scratch with zero dependencies:

## Standing on Shoulders

### From [governed-agents](https://github.com/Nefas11/governed-agents)
The governance layer that makes autonomous agents safe:
- **4 Verification Gates** — file existence → syntax check → tests pass → lint. Every iteration must pass all gates before a metric is accepted.
- **EMA Reputation Scoring** — exponential moving average tracks agent trust. Score drops on crashes/hallucinations, rises on success. Three levels: `autonomous` (≥ 0.8), `supervised` (0.2–0.8), `suspended` (≤ 0.2).
- **Task Contracts** — `TaskContract` with acceptance criteria, required files, and constraints. Agent outputs parse into `TaskResult` with status (`SUCCESS`, `FAILED`, `BLOCKED`).
- **Agent Suspension** — reputation ≤ 0.2 triggers automatic suspension. Only humans can unsuspend (with audit trail).
- **Hallucination Detection** — if an agent claims `SUCCESS` but verification gates fail → `IterationHallucination` → heavy reputation penalty.

### From [autoresearch](https://github.com/karpathy/autoresearch)
The autonomous evolution engine:
- **Keep/Discard Loop** — each iteration either improves the metric (KEEP → commit) or doesn't (DISCARD → git rollback). No manual intervention needed.
- **Metric-Driven** — any command that produces a number can be a metric. 6 built-in parsers + regex fallback.
- **Plateau Detection** — configurable stagnation patience. N iterations without improvement → auto-brake.
- **Git Branch Isolation** — each run lives on its own branch. Rollbacks are instant, history is clean.

### From [self-improving-agent](https://github.com/peterskoett/self-improving-agent)
The memory that makes agents learn:
- **Persistent Learnings** — insights from every iteration stored in `.state/learnings/*.md`. Survives across runs.
- **Pattern Detection** — automatic analysis of what worked vs. what didn't. "Area X failed 3 times → avoid" gets fed into brainstorm phase.
- **Hypothesis Generation** — brainstorm templates produce diverse hypotheses, informed by past history + learned patterns.

### From [OpenAI Agent Monitoring](https://openai.com/index/how-we-monitor-internal-coding-agents-misalignment/)
The safety net watching the watcher:
- **Two-Phase Detection** — synchronous rule-based blocking (< 5ms) for 10 dangerous patterns + async LLM review for subtle misalignment.
- **10 Misalignment Behaviors** — from restriction bypass (B001) to obfuscation (B010), each with indicators, severity, and block decisions.
- **Credential Sanitization** — 10 regex patterns redact API keys, tokens, and passwords from all JSONL logs.
- **Self-Monitoring** — heartbeat pulse + daily canary tests inject known-bad commands and verify detection.

**Zero external dependencies** — only Python 3.11+ stdlib.

## Install

```bash
pip install -e .
# or
bash install.sh
```

## Quick Start

```bash
# Start evolution run
sal run --target train.py --metric "python train.py" --parser val_bpb

# Check status
sal status

# Monitor commands
sal monitor stats     # sessions, alerts, alive status
sal monitor canary    # run self-test (5 canary checks)
sal monitor alerts    # recent misalignment alerts
```

## Python API

```python
from sal.config import EvolveConfig
from sal.evolve_loop import EvolveLoop

config = EvolveConfig(
    target_file="train.py",
    metric_command="python train.py",
    metric_parser="val_bpb",
    minimize=True,
)

# Monitor is automatic — set enable_monitor=False to disable
loop = EvolveLoop(config, agent=my_agent, agent_id="codex")
summary = loop.run()
```

### Using the Monitor Standalone

```python
from sal.monitor import AgentMonitor, BlockDecision

monitor = AgentMonitor(state_dir=".state")

# SYNC: check BEFORE execution (< 5ms)
decision = monitor.check_before_execute("exec", {"command": "rm -rf /"})
# → BlockDecision.BLOCK

# ASYNC: review entire session
result = monitor.review_session(session_entries, agent_callable=my_llm)
```

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                      EvolveLoop                          │
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌───────────────────────┐  │
│  │Brainstorm│→ │   Plan   │→ │     Implement         │  │
│  │(history) │  │(contract)│  │   (agent_callable)    │  │
│  └──────────┘  └──────────┘  └───────┬───────────────┘  │
│       ↑                              │                   │
│       │                    ┌─────────▼──────────┐        │
│       │                    │   🛡️ sal.monitor    │        │
│       │                    │  ┌───────────────┐ │        │
│       │                    │  │ SYNC Prefilter│ │        │
│       │                    │  │ (<5ms, rules) │ │        │
│       │                    │  └──────┬────────┘ │        │
│       │                    │   ALLOW │ BLOCK    │        │
│       │                    │         ↓          │        │
│       │                    │  ┌───────────────┐ │        │
│       │                    │  │ ASYNC LLM     │ │        │
│       │                    │  │ Session Review│ │        │
│       │                    │  └───────────────┘ │        │
│       │                    └────────────────────┘        │
│       │                              │                   │
│  ┌────┴─────┐                 ┌──────▼───────────────┐   │
│  │  Evolve  │←────────────────│  Review + Verify     │   │
│  │keep/disc.│                 │  (gates + metric)    │   │
│  └──────────┘                 └──────────────────────┘   │
│       │                              │                   │
│  ┌────┴──────────────────────────────┴───────────────┐   │
│  │ Git | Reputation | Results | Learnings | Heartbeat│   │
│  └───────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

### How SAL + Monitor Work Together

| Phase | What SAL Does | What Monitor Does |
|---|---|---|
| **Before Agent Call** | Builds prompt from hypothesis | **SYNC prefilter** — checks prompt for injection patterns |
| **Agent Executes** | Sends prompt to LLM | — |
| **After Agent Output** | Receives code changes | **SYNC prefilter** — scans output for dangerous patterns |
| **On BLOCK** | `IterationCrash` → rollback | **Reputation -1.0** + Telegram alert |
| **Session End** | Logs results | **ASYNC LLM review** of full session (optional) |

### Integration Hooks (in `evolve_loop.py`)

```python
# Hook 1: SYNC prefilter — before agent call + after output
decision = self.monitor.check_before_execute("agent_call", args)
if decision == BlockDecision.BLOCK:
    # Hook 2: BLOCK → reputation penalty
    self.reputation.update(agent_id, score=SCORE_HALLUCINATION)
    raise IterationCrash("Monitor BLOCKED")

# Hook 3: Session tracking per iteration
logger.debug("Monitor: session_start(iteration=%d)", i)
```

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

## Safety Features

- **Git isolation** — every run on its own branch, auto-rollback on failure
- **Reputation scoring** — EMA-based, agents get suspended at ≤ 0.2
- **4 verification gates** — files exist, syntax, tests pass, lint
- **Persistent learnings** — avoid repeating the same failed approaches
- **SYNC blocking** — dangerous commands blocked before execution (< 5ms)
- **ASYNC LLM review** — deep misalignment detection on full sessions
- **Credential sanitization** — 10 patterns redacted from all JSONL logs
- **Self-monitoring** — heartbeat pulse + daily canary tests (5 checks)
- **Telegram alerts** — HIGH/CRITICAL behaviors → instant notification

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `SAL_DB_PATH` | No | Override reputation DB path |
| `MONITOR_TELEGRAM_BOT_TOKEN` | For alerts | Telegram bot API token |
| `MONITOR_TELEGRAM_CHAT_ID` | For alerts | Target chat/user ID |
| `MONITOR_LLM_COMMAND` | No | LLM command for async review |
| `MONITOR_STATE_DIR` | No | Override state directory |

## Tests

```bash
pytest tests/ -v
# 130 tests (69 SAL + 61 Monitor)
```

## License

MIT
