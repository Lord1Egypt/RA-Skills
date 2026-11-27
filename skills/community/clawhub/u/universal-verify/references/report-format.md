# checks.yaml and report format

## checks.yaml
```yaml
target: article.md
type: text
intensity: L2
checks:
  - id: T1
    criterion: No lexical AI-tone patterns above threshold
    method: script            # command | script | scorer | judge | human
    run: python scripts/ai_tone_lint.py article.md
    severity: major           # blocker | major | minor
    evidence_required: lint JSON, score <= 3 per 1000 chars
  - id: T5
    criterion: Paragraph structure is not uniform and the ending does not state a lesson
    method: judge
    severity: major
    evidence_required: quoted paragraphs
```

## Report
```
## Verification Report — <name>   Intensity: L2   Round: 2/3
Verdict: PASS | PASS_WITH_NOTES | FAIL | NEEDS_HUMAN

| check_id | layer | result | confidence | severity | evidence |
|---|---|---|---|---|---|

Auto-fixed this run: ...
Human review cards (max 5):
1. <issue> — evidence: <quote/screenshot/log> — suggested decision: <option A / B>
```
