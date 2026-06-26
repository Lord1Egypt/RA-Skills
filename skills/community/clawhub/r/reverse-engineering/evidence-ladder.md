# Evidence Ladder

Use these confidence levels when reporting findings:

| Level | Label | Standard | Safe claim style |
|-------|-------|----------|------------------|
| 0 | Unverified | Hunch, anecdote, or indirect clue only | "Possible" |
| 1 | Observed | Seen in one artifact, request, trace, or sample | "Observed in sample X" |
| 2 | Reproduced | Confirmed by a controlled replay or repeated sample | "Reproduced under conditions Y" |
| 3 | Cross-checked | Confirmed through two or more independent paths | "High confidence" |
| 4 | Operational | Proven in a way that supports implementation or migration | "Ready to act on" |

## Reporting Rules

- Never use stronger language than the evidence level supports.
- A decompiled function without a behavioral repro is usually Level 1 or 2, not Level 4.
- A single packet capture can describe what happened once, not the full protocol contract.
- If conflicting evidence appears, drop confidence first and reconcile second.

## Minimal Ledger Template

```markdown
| Claim | Evidence Level | Source | Next test |
|------|----------------|--------|-----------|
| The token expires after 15 minutes | 2 | replayed auth flow twice | verify with clock skew |
| Byte 12 flags compression | 1 | one sample diff | test against three more files |
```

## Promotion Rules

- Promote from 0 to 1 when an artifact directly supports the claim.
- Promote from 1 to 2 when the result can be replayed deliberately.
- Promote from 2 to 3 when a second independent source agrees.
- Promote to 4 only when the model is stable enough for implementation, migration, or operational guidance.
