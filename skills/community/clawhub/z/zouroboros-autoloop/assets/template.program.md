# Program: {name}

## Objective
{One sentence: what are we optimizing? e.g., "Minimize validation loss for the classifier prompt."}

## Metric
- **name**: {metric name, e.g., "eval_accuracy", "sharpe_ratio", "lighthouse_score"}
- **direction**: {lower_is_better | higher_is_better}
- **extract**: {shell command that prints ONLY the numeric metric value, e.g., `jq -r .accuracy eval-result.json`}

## Setup
{One-time setup steps the agent runs before the loop starts. Leave empty if none needed.}

```bash
# Example: install deps, prepare data, etc.
```

## Target File
{Relative path to the single file the agent edits, e.g., `prompts/classifier.md` or `strategy.py`}

## Run Command
{Shell command to execute one experiment. Must be non-interactive and finish within the time budget.}

```bash
# Example:
bun run evaluate.ts --config eval-config.json
```

## Read-Only Files
{List of files the agent must NOT modify, one per line. The target file is always editable.}

- prepare.py
- evaluate.ts

## Constraints
- **Time budget per run**: 5 minutes
- **Max experiments**: 100
- **Max duration**: 8 hours
- **Max cost (USD)**: 10.00

## Simplicity Criterion
All else being equal, simpler is better. A small improvement that adds ugly complexity is not
worth it. Removing something and getting equal or better results is a great outcome — that's a
simplification win. When evaluating whether to keep a change, weigh the complexity cost against
the improvement magnitude.

## Stagnation
- **Threshold**: 10 experiments with no improvement triggers radical exploration
- **Double threshold**: 20 experiments combines best past approaches
- **Triple threshold**: 30 experiments auto-stops with summary report

## Notes
{Any additional context for the agent: domain knowledge, things to try, things to avoid.}
