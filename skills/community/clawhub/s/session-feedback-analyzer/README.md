# session-feedback-analyzer

Extract implicit user feedback from Claude Code session logs. Part of the [auto-improvement-orchestrator](../../) pipeline.

## What it does

Parses `~/.claude/projects/**/*.jsonl` session files, detects skill invocations (both `tool_use` blocks and `/slash-commands`), then classifies how the user responded within a 3-turn window: correction, partial acceptance, or acceptance. Outputs one JSON event per feedback signal to `feedback-store/feedback.jsonl`.

## Quick start

```bash
# Analyze all sessions
python3 scripts/analyze.py

# Analyze a single skill with privacy mode
python3 scripts/analyze.py --skill-filter deslop --no-snippets

# View metrics
python3 -c "
from pathlib import Path
from scripts.metrics import load_feedback_events, compute_all_skill_metrics, format_metrics_report
events = load_feedback_events(Path('feedback-store/feedback.jsonl'))
print(format_metrics_report(compute_all_skill_metrics(events)))
"
```

## Directory structure

```
session-feedback-analyzer/
  SKILL.md              # Full specification (detection rules, classification, formulas)
  README.md             # This file
  scripts/
    analyze.py          # Main analyzer CLI
    metrics.py          # Metrics computation library
  tests/
    test_analyze.py     # Tests for session parsing and outcome classification
    test_metrics.py     # Tests for correction_rate, trend, and hotspot computation
```

## CLI flags

| Flag | Default | What it does |
|------|---------|-------------|
| `--session-dir` | `~/.claude/projects/` | Where to find session JSONL files |
| `--output` | `feedback-store/feedback.jsonl` | Where to write feedback events |
| `--no-snippets` | off | Strip user message text from output |
| `--skill-filter` | all | Only analyze one skill |
| `--min-invocations` | 5 | Minimum sample size for meaningful metrics |

## Output format

Each line in `feedback.jsonl` is a JSON object:

```json
{
  "event_id": "a1b2c3d4...",
  "timestamp": "2026-04-05T10:00:00Z",
  "session_id": "uuid",
  "skill_id": "cpp-expert",
  "outcome": "correction",
  "confidence": 0.9,
  "correction_type": "rejection",
  "dimension_hint": "accuracy"
}
```

See [SKILL.md](SKILL.md) for the full schema and all field descriptions.

## Tests

```bash
python3 -m pytest tests/ -v
```

## How it fits in the pipeline

```
session-feedback-analyzer  -->  feedback.jsonl  -->  improvement-generator
                                                          |
                                                    improvement-discriminator
                                                          |
                                                    improvement-evaluator
                                                          |
                                                    improvement-executor
                                                          |
                                                    improvement-gate
```

The analyzer is the entry point: it produces the signal that tells the rest of the pipeline which skills need improvement and in which dimensions.

## License

MIT
