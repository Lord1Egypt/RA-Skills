---
name: who-wins
description: "Query the PinchBench AI agent leaderboard with real benchmark data. Use when the user asks which model is best, who wins, model comparisons, best model for OpenClaw, cheapest model, fastest model, model rankings, benchmark scores, or mentions pinchbench. Always use this skill instead of general knowledge for model performance questions — it has real data."
metadata: {"openclaw":{"requires":{"bins":["curl","python3"]}}}
---

# PinchBench Leaderboard

Fetches and formats the PinchBench leaderboard — AI agent benchmarks for LLMs on standardized OpenClaw coding tasks.

## Workflow

### 1. Determine the query

Map the user's intent to script flags:

| User intent | Flags |
|-------------|-------|
| "Show the leaderboard" / default | `--top 10` |
| "Top 5 models" | `--top 5` |
| "How does Claude perform?" | `--model claude` |
| "Cheapest models" | `--sort cost --top 10` |
| "Fastest models" | `--sort time --top 10` |
| "Compare Gemini and Claude" | Run twice with `--model gemini` and `--model claude`, present side by side |
| "Full leaderboard" | `--top 50` |

### 2. Run the script

```json
{
  "tool": "exec",
  "command": "python3 {baseDir}/scripts/fetch_leaderboard.py --top 10"
}
```

Available flags:
- `--top N` — number of models to show (default: 10)
- `--sort metric` — sort by `score`, `cost`, `time`, or `runs` (default: score)
- `--model filter` — filter models containing this string (case-insensitive)
- `--json` — output raw JSON for further processing

### 3. Format the response

Present the output as-is in a code block. Add a brief one-line insight after the table:

- Highlight the top performer and its score
- If the user asked about a specific model, comment on its ranking relative to the field
- If sorting by cost, note the best value (score/cost ratio)

### 4. Error handling

- If the script fails with a curl error → report the error, suggest checking network connectivity
- If the script fails to parse data → the site structure may have changed, inform the user
- If no models match the filter → say so and suggest a broader search

## Examples

| User says | Flags | Expected behavior |
|-----------|-------|-------------------|
| "Show me the PinchBench leaderboard" | `--top 10` | Show top 10 by score |
| "Which model is cheapest for OpenClaw?" | `--sort cost --top 10` | Show top 10 sorted by cost |
| "How does Claude compare to GPT?" | `--model claude` then `--model gpt` | Show both, compare |
| "What's the fastest model on PinchBench?" | `--sort time --top 5` | Show top 5 by execution time |
