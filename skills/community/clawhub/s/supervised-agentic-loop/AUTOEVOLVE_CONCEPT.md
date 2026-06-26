# supervised-agentic-loop — Self-Improving Governed Agent Skill

> *Self-improving AI agents. Verified at every step.*
>
> **Combining:** [autoresearch](https://github.com/karpathy/autoresearch) × [governed-agents](https://github.com/Nefas11/governed-agents) × [superpowers-workflow](https://github.com/Nefas11/openclaw-superpowers-workflow)
>
> **Review status:** v0.3 — all DrNeuron 🔴 + 🟡 findings resolved

## Problem

Today these three exist in isolation:

1. **autoresearch** — autonomous experiment loop, no verification, no reputation
2. **governed-agents** — verification + reputation, but single-shot (no iterative self-improvement)
3. **superpowers-workflow** — orchestrated pipeline, but no autonomous loop mode

**controlled-agentic-loop** unifies them: a skill that lets AI agents **iteratively improve code** through the Superpowers pipeline, **governed by verification gates**, with **autoresearch-style autonomous experimentation**.

---

## DrNeuron Review Resolution Tracker

| Finding                        | Severity | v0.2          | v0.3 Status                                    |
| ------------------------------ | -------- | ------------- | ---------------------------------------------- |
| metric_parser format undefined | 🔴       | Open          | ✅ Named strategies + regex fallback           |
| metric direction (↑/↓)       | 🔴       | Open          | ✅`minimize: bool` in EvolveConfig           |
| Exception handler missing      | 🔴       | Open          | ✅ try/except in `run()` with IterationError |
| Plateau N undefined            | 🟡       | Open          | ✅`plateau_patience: int = 5`                |
| git submodule vs pip           | 🟡       | Open          | ✅ pip pinned for install, submodule for dev   |
| suspension_reason / unsuspend  | 🟡       | Persistent    | ✅`cal unsuspend --agent <id>` CLI           |
| network_access justification   | 🟡       | Not addressed | ✅ Justified below                             |
| baseline() documentation       | 🟡       | Not addressed | ✅ Documented below                            |

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                  controlled-agentic-loop Skill                   │
│                                                                  │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐     │
│  │BRAINSTORM│──→│   PLAN   │──→│IMPLEMENT │──→│  REVIEW  │──┐  │
│  │          │   │(Contract)│   │(Codex    │   │(Council) │  │  │
│  │ Hypothe- │   │ Criteria │   │ Agent)   │   │ LLM/Peer │  │  │
│  │ sis Gen  │   │ Metric   │   │ Code Mod │   │ Critique │  │  │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘  │  │
│                                                               │  │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐                 │  │
│  │  VERIFY  │◄──┘          │   │  EVOLVE  │◄────────────────┘  │
│  │(4 Gates) │              │   │  LOOP    │                    │
│  │Files/Test│   ┌──────────┤   │ Keep or  │                    │
│  │Lint/AST  │──→│REPUTATION│──→│ Discard  │──→ next iteration  │
│  └──────────┘   │  UPDATE  │   │ git ops  │                    │
│                 └──────────┘   └──────────┘                    │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ results.tsv — Experiment Log (autoresearch-style)         │   │
│  │ reputation.db — Persistent Agent Scores (governed-agents) │   │
│  │ evolve_branch — Git Isolation (auto-create + auto-reset)  │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

### Phase 6: **Evolve Loop** (new — from autoresearch)

After Verify, the result feeds back into Brainstorm.
**Metric direction** is controlled by `minimize: bool` — the comparator flips accordingly:

```
improved = (new < best) if config.minimize else (new > best)

IF   improved AND all gates passed:
     → keep commit on evolve branch
     → log to results.tsv (status: keep)
     → reputation += 1.0
     → reset stagnation counter
     → Brainstorm new hypothesis

ELIF NOT improved (equal or worse):
     → git reset to last good commit
     → log to results.tsv (status: discard)
     → reputation += 0.0
     → increment stagnation counter
     → Brainstorm different approach

ELIF crash/gate failure:
     → git reset
     → log to results.tsv (status: crash)
     → reputation += -1.0 (if hallucinated) or 0.0 (if honest)
     → retry or skip

STOP CONDITIONS (all three enforced):
  1. reputation ≤ 0.2 → SUSPENDED (auto-brake)
  2. i ≥ max_iterations → budget exhausted
  3. stagnation_counter ≥ plateau_patience → plateau detected
  4. human interrupts (Ctrl+C / SIGINT)
```

### Baseline Phase

`baseline()` runs once before the loop starts:

1. Executes `metric_command` on the unmodified code
2. Parses the result via `metric_parser` (see Metric Parsing below)
3. Logs the result as iteration 0 with `status: keep, hypothesis: baseline`
4. Sets this as the initial `best_metric` value
5. If baseline **crashes**, the loop aborts — the codebase is broken before we start

### Suspension & Unsuspend

When an agent hits reputation ≤ 0.2, it is suspended with a `suspension_reason`:

```python
suspension = {
    "agent_id": "codex-gpt5.2",
    "reason": "Reputation 0.18 after 3 consecutive hallucinated successes",
    "suspended_at": "2026-03-19T11:18:00Z",
    "last_5_scores": [-1.0, -1.0, 0.0, -1.0, 0.0],
}
```

To unsuspend (human-only, with audit trail):

```bash
cal unsuspend --agent codex-gpt5.2 --reason "Reviewed failures, root cause was OOM not hallucination"
# → Reputation reset to 0.5 (neutral prior)
# → Audit log entry in reputation.db
```

---

## Proposed Changes

### New Repository: `controlled-agentic-loop`

---

#### [NEW] `SKILL.md`

OpenClaw + Antigravity + Claude Code compatible skill definition.

```yaml
---
name: controlled-agentic-loop
description: "Self-improving AI agent loop: Brainstorm → Plan → Implement → Review → Verify → Evolve. Combines governed-agents verification with autoresearch-style autonomous experimentation."
source: https://github.com/Nefas11/controlled-agentic-loop
homepage: https://github.com/Nefas11/controlled-agentic-loop
install: {"kind": "script", "script": "install.sh"}
filesystem_writes: ["~/.openclaw/workspace/.state/cal/"]
capabilities: ["persistent_db_writes", "external_cli_execution", "network_requests"]
network_access: true
network_justification: "Layer 2 Grounding Gate performs HTTP HEAD requests to verify URL reachability in agent outputs (max 5 URLs, timeout 3s each). No data is sent to external services."
env_vars:
  OPENCLAW_WORKSPACE: {required: false, description: "Workspace root"}
  CAL_METRIC: {required: true, description: "Target metric to optimize (e.g., 'pytest --tb=short', 'val_bpb')"}
  CAL_MAX_ITERATIONS: {required: false, description: "Max experiment iterations (default: 100)"}
  CAL_TIME_BUDGET: {required: false, description: "Time budget per experiment in seconds (default: 300)"}
  CAL_MINIMIZE: {required: false, description: "Set to 'false' if higher metric = better (default: true)"}
metadata:
  openclaw:
    emoji: "🧬"
    type: "executable/with-install"
    requires: {bins: ["codex", "git", "pytest"]}
    optional_bins: ["ruff", "flake8", "pylint"]
---
```

---

#### [NEW] `cal/evolve_loop.py`

Core evolution loop combining autoresearch experiment cycle with governed-agents verification.

```python
class EvolveLoop:
    def __init__(self, config: EvolveConfig):
        self.config = config
        self.orchestrator = None
        self.results = ResultsLog("results.tsv")
        self.branch = f"cal/{config.run_tag}"
        self.best_metric = None
        self.stagnation = 0

    def run(self):
        """Main loop — runs until brake triggers."""
        self.setup_branch()
        self.best_metric = self.baseline()  # iteration 0, see doc above

        for i in range(1, self.config.max_iterations + 1):
            try:
                hypothesis = self.brainstorm(self.results.history)
                contract = self.plan(hypothesis)
                agent_output = self.implement(contract)
                review = self.review(agent_output, contract)
                result = self.verify(contract)
                self.evolve(result, hypothesis)

            except IterationCrash as e:
                # Agent code crashed (OOM, SyntaxError, timeout)
                self.git.rollback()
                self.results.log(i, status="crash", error=str(e))
                self.reputation.update(score=0.0)  # honest crash, not hallucination
                continue

            except IterationHallucination as e:
                # Agent claimed success but gates failed
                self.git.rollback()
                self.results.log(i, status="crash", error=str(e))
                self.reputation.update(score=-1.0)
                # fall through to brake check

            except Exception as e:
                # Unexpected error — log and continue
                self.git.rollback()
                self.results.log(i, status="error", error=f"Unexpected: {e}")
                continue

            # === BRAKE CHECKS ===
            if self.reputation.score <= 0.2:
                self.suspend(reason=f"Reputation {self.reputation.score:.2f}")
                break
            if self.stagnation >= self.config.plateau_patience:
                self.log(f"PLATEAU — no improvement for {self.stagnation} iterations")
                break
```

---

#### [NEW] `cal/brainstorm.py`

Hypothesis generation using past results (TSV history analysis).

Key function:

- `generate_hypothesis(results_history, target_file)` → produces a structured hypothesis with expected improvement, risk level, and code change description.

---

#### [NEW] `cal/results_log.py`

TSV-based experiment logging (inspired by autoresearch `results.tsv`).

Format:

```
iteration	commit	metric_value	memory_mb	status	hypothesis	duration_s	reputation
1	a1b2c3d	0.997900	44000	keep	baseline	305	0.500
2	b2c3d4e	0.993200	44200	keep	increase LR to 0.04	310	0.650
3	c3d4e5f	1.005000	44000	discard	switch to GeLU	308	0.455
```

---

#### [NEW] `cal/git_isolation.py`

Git branch management for safe experimentation:

- `create_evolve_branch(tag)` — creates `cal/{tag}` from current HEAD
- `commit_experiment(message)` — commits current changes
- `rollback()` — `git reset --hard` to last known good commit
- `get_diff()` — returns the code diff for review phase

---

#### [NEW] `cal/config.py`

Configuration schema:

```python
@dataclass
class EvolveConfig:
    target_file: str              # File the agent modifies (like train.py)
    metric_command: str           # Shell command to run (e.g. "pytest -q", "uv run train.py")
    metric_parser: str            # Named strategy OR regex (see MetricExtractor)
    minimize: bool = True         # True → lower is better (loss, BPB)
                                  # False → higher is better (accuracy, coverage, passed)
    time_budget: int = 300        # Seconds per experiment
    max_iterations: int = 100
    plateau_patience: int = 5     # Stop after N iterations without improvement
    run_tag: str = ""             # Auto-generated from date if empty
    readonly_files: list = field(default_factory=list)
    council_size: int = 3         # For review phase
```

---

#### [NEW] `cal/metric_extractor.py`

**🔴 DrNeuron Blocker resolved:** Named strategies + regex fallback.

```python
import re
from typing import Callable

# Built-in named strategies
BUILTIN_PARSERS: dict[str, Callable[[str], float]] = {
    "last_line_float":    lambda out: float(out.strip().split("\n")[-1]),
    "pytest_passed":      lambda out: float(re.search(r"(\d+) passed", out).group(1)),
    "pytest_failed":      lambda out: float(re.search(r"(\d+) failed", out).group(1)),
    "coverage_percent":   lambda out: float(re.search(r"(\d+\.?\d*)%", out).group(1)),
    "val_bpb":            lambda out: float(re.search(r"^val_bpb:\s+([\d.]+)", out, re.M).group(1)),
    "benchmark_ms":       lambda out: float(re.search(r"([\d.]+)\s*ms", out).group(1)),
}

def get_parser(spec: str) -> Callable[[str], float]:
    """Resolve metric_parser spec to a callable.

    Resolution order:
    1. Named strategy (e.g. "pytest_passed")
    2. Regex with first capture group (e.g. r"score: ([\d.]+)")
    3. ValueError if neither works
    """
    if spec in BUILTIN_PARSERS:
        return BUILTIN_PARSERS[spec]

    # Treat as regex — must have exactly one capture group
    try:
        pattern = re.compile(spec)
        if pattern.groups != 1:
            raise ValueError(f"Regex must have exactly 1 capture group, got {pattern.groups}")
        return lambda out: float(pattern.search(out).group(1))
    except re.error as e:
        raise ValueError(f"metric_parser '{spec}' is not a named strategy or valid regex: {e}")
```

**Usage examples:**

```python
# Named strategy
EvolveConfig(metric_parser="pytest_passed", minimize=False)  # more passed = better

# Named strategy for loss
EvolveConfig(metric_parser="val_bpb", minimize=True)         # lower BPB = better

# Custom regex
EvolveConfig(metric_parser=r"F1 score: ([\d.]+)", minimize=False)
```

---

#### Dependencies (reused, not copied)

**Decision: pip with pinned version** for `install.sh`. Git submodule only for dev/contributor setup.

| Dependency                       | Source          | Production                             | Dev           |
| -------------------------------- | --------------- | -------------------------------------- | ------------- |
| `governed_agents.contract`     | governed-agents | `pip install governed-agents==0.4.2` | git submodule |
| `governed_agents.orchestrator` | governed-agents | (same package)                         | git submodule |
| `governed_agents.verifier`     | governed-agents | (same package)                         | git submodule |
| `governed_agents.reputation`   | governed-agents | (same package)                         | git submodule |

`install.sh` will:

```bash
# Production install: pinned pip dependency
pip install governed-agents==0.4.2

# Dev install (after git clone --recurse-submodules):
pip install -e ./governed-agents
```

---

## Platform Compatibility

| Platform              | Support                                            |
| --------------------- | -------------------------------------------------- |
| **OpenClaw**    | ✅ via SKILL.md +`sessions_spawn`                |
| **Antigravity** | ✅ via MCP task +`program.md`-style instructions |
| **Claude Code** | ✅ via `program.md`-style prompt + CLI           |
| **Codex CLI**   | ✅ individual experiments via `codex --task`     |

---

## Formal Model

### Evolution Function

```
E(i) = Brainstorm(H) → Plan(C) → Implement(A) → Review(R) → Verify(V) → Evolve(Δ)

where:
  H(i) = f(results[0..i-1])       Hypothesis from history
  C(i) = TaskContract(H(i))       Formal contract
  A(i) = AgentOutput(C(i))        Agent execution result
  R(i) = Council(A(i), C(i))      Optional review
  V(i) = Gates(A(i))              Verification (4 gates)
  m(i) = MetricExtractor(output)  Parsed metric value

  improved(i) = (m(i) < best)  if minimize = True
                (m(i) > best)  if minimize = False

  Δ(i) = keep    if V(i) = True  ∧ improved(i)
          discard if V(i) = True  ∧ ¬improved(i)
          crash   if V(i) = False ∨ exception
```

### Auto-Brake (from governed-agents)

```
STOP if R(t) ≤ 0.2                              (suspended — logged with reason)
STOP if i ≥ max_iterations                       (budget exhausted)
STOP if stagnation ≥ plateau_patience (default 5) (plateau detected)
STOP if SIGINT received                           (human interrupt)
```

---

## Verification Plan

### Automated Tests

```bash
# Unit tests for each new module
python3 -m pytest cal/tests/ -v

# Integration test: run 3 iterations on a toy metric
python3 -m pytest cal/tests/test_evolve_loop.py -v

# Reuse governed-agents test suite for verification gates
python3 -m pytest governed_agents/test_verification.py -v
```

### Manual Verification

1. **Dry run**: Start the evolve loop on a trivial Python file with `pytest` as metric — verify it creates branch, runs 3 iterations, logs to `results.tsv`
2. **Rollback test**: Introduce a deliberate failure → verify git reset works
3. **Auto-brake test**: Set reputation to 0.15 → verify loop stops
4. **OpenClaw integration**: Submit SKILL.md to ClawHub.ai for scan

---

## Comparison: What Each Repo Contributes

| Capability               | autoresearch | governed-agents | superpowers-workflow | **controlled-agentic-loop** |
| ------------------------ | :----------: | :-------------: | :------------------: | :-------------------------------: |
| Autonomous loop          |      ✅      |       ❌       |          ❌          |                ✅                |
| Verification gates       |      ❌      |       ✅       |          ✅          |                ✅                |
| Reputation scoring       |      ❌      |       ✅       |          ✅          |                ✅                |
| Git-based rollback       |      ✅      |       ❌       |          ❌          |                ✅                |
| Experiment TSV log       |      ✅      |       ❌       |          ❌          |                ✅                |
| 5-phase pipeline         |      ❌      |       ❌       |          ✅          |                ✅                |
| Council review           |      ❌      |       ✅       |         ⚠️         |                ✅                |
| Auto-brake (supervision) |      ❌      |       ✅       |          ✅          |                ✅                |
| Multi-platform skill     |      ❌      |       ✅       |          ✅          |                ✅                |
| Hypothesis generation    |      ❌      |       ❌       |          ❌          |             ✅ (new)             |
| Plateau detection        |      ❌      |       ❌       |          ❌          |             ✅ (new)             |
