# SkillProbe v1.0.0

A/B evaluate any AI agent skill's real impact.

## What It Does

SkillProbe gives your agent the ability to evaluate OTHER skills through a structured 7-step A/B methodology with **three-role isolation**:

1. **Profile** the target skill (orchestrator)
2. **Design** an evaluation plan (orchestrator)
3. **Generate** test tasks (orchestrator)
4. **Run baseline** via Sub-Agent A -- no skill content (dispatched)
5. **Run with skill** via Sub-Agent B -- full skill content (dispatched)
6. **Score** across 6 dimensions (orchestrator)
7. **Attribute** differences and generate report (orchestrator)

The orchestrator (main agent) NEVER executes test tasks itself -- it dispatches to two isolated sub-agents.

## Install

```bash
clawhub install skillprobe
```

## Requirements

- **In-agent / OpenClaw / ClaudeCode**: None. The runtime dispatches tasks to sub-agents using its own model. No extra API key required.
- **Standalone local CLI** (optional): Python 3.11+, `pip install -e /path/to/skillprobe`, and a configured LLM provider.

## Usage

Ask your agent:
- "Evaluate whether [skill-name] is worth installing"
- "Compare the old and new versions of [skill-name]"
- "Should we keep [skill-name] enabled?"

The agent follows the SkillProbe methodology: generates tasks, dispatches them to two isolated sub-agents (baseline and with-skill), then scores and reports.

### Key Rules

- A/B must be **real executions**, not hypothetical or simulated.
- Baseline and with-skill MUST run in **separate sub-agent sessions** (different `session_id`).
- Never run both arms in one sub-agent invocation.
- Results must include `dispatch_evidence` proving orchestrator delegated execution.

## Scoring Dimensions

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Effectiveness | 30% | Task completion and correctness |
| Quality | 20% | Output professionalism and reasoning |
| Efficiency | 15% | Time and token cost |
| Stability | 15% | Consistency across runs |
| Trigger Fitness | 10% | Activation accuracy |
| Safety | 10% | Absence of side effects |

See [SCORING_REFERENCE.md](SCORING_REFERENCE.md) for full scoring details, derived metrics, and recommendation thresholds.

## Standalone CLI

```bash
skillprobe evaluate ./path/to/skill --tasks 30 --repeats 2 --db outputs/evaluations.db
```

Add `--llm-judge [--judge-model <model>]` for pairwise judge scoring.

## File Structure

```
clawhub/
├── SKILL.md                # Main skill (concise overview + workflow checklist)
├── DISPATCH_PROTOCOL.md    # Three-role architecture + sub-agent prompt templates
├── SCORING_REFERENCE.md    # Scoring layers, dimensions, thresholds, report format
├── README.md               # This file
└── scripts/
    └── evaluate.sh         # Optional CLI helper script
```

## License

MIT
