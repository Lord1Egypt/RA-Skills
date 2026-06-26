# Quick Start

Get your first Quorum validation running in 60 seconds.

## 1. Install

```bash
pip install quorum-validator
```

## 2. Set your model provider

```bash
export ANTHROPIC_API_KEY=your-key
# or: export OPENAI_API_KEY=your-key
# Quorum uses LiteLLM — 100+ models supported
```

## 3. Run your first validation

```bash
quorum run --target your-file.py --depth quick
```

That's it. Quorum auto-detects the file type, picks the right rubric, spawns critics, and gives you a verdict.

## What You'll See

```
Running Quorum (quick depth, critics: correctness, completeness) ...

 ◆ QUORUM VERDICT: PASS_WITH_NOTES
 ──────────────────────────────────
   Issues: 0 HIGH · 1 MEDIUM · 2 LOW/INFO  (3 total)

   1. [MEDIUM] Function `process_data` has no error handling for
      empty input — raises unhandled IndexError at line 47
   2. [INFO]   Docstring for `validate` mentions param `strict`
      which doesn't exist in the function signature
   3. [INFO]   TODO marker at line 12 — "TODO: add retry logic"

   Cost: $0.14 (8,200 prompt + 1,840 completion tokens)
```

## Depth Levels

| Depth | Critics | Cost* | Use when |
|-------|---------|-------|----------|
| `quick` | 2 (correctness, completeness) | ~$0.15 | Sanity check before continuing |
| `standard` | 6 (+ security, code hygiene, cross-consistency, tester) | ~$0.50 | Default for most work |
| `thorough` | 6 + fix loops + full audit trail | ~$1.50+ | Production-bound, can't be wrong |

*Estimates on Claude Sonnet. Scales with model and artifact size.*

## Next Steps

- **Validate a directory:** `quorum run --target ./src/ --depth standard`
- **Use a custom rubric:** `quorum run --target report.md --rubric my-rubric.json`
- **Check cross-artifact consistency:** `quorum run --target ./docs/ --relationships quorum-relationships.yaml`
- **Build your own rubric:** [Rubric Building Guide](../guides/RUBRIC_BUILDING_GUIDE.md)
- **Understand the critics:** [The Nine](../architecture/THE_NINE.md)

## Troubleshooting

First run will prompt you to configure your model. If you hit issues:

- [Full Installation Guide](INSTALLATION.md)
- [Model Requirements](MODEL_REQUIREMENTS.md)
- [Config Reference](../configuration/CONFIG_REFERENCE.md)
