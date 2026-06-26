# Buffett Oracle — Methodology Audit

*Last updated: 2026-03-25*

## Why This Exists

The project originally surfaced a single headline number (`14/14`) that looked like an accuracy metric.
That framing is too optimistic.

What the repo currently has is **retrospective consistency** on a curated benchmark set, not validated predictive accuracy and not full Berkshire-history coverage.

## Current Snapshot

- Coverage scope: curated 29-case benchmark set, not the full Buffett/Berkshire universe
- Completed benchmark cases: 29
- Retrospective consistency: 29/29
- Ambiguous scored cases: 3
- Exception-assisted cases: 6
- Exit / non-binary cases: 1
- Core binary non-exception set: 19
- BUY cards with BUY control groups: 4
- Scope-drift cards: 1
- Gate-by-gate review now lives in `gate_review.md` and `python3 oracle.py gate-review`

Generate the live version with:

```bash
python3 oracle.py methodology
```

## Main Methodology Risks

1. Ambiguous conclusions inflate the headline win rate.
   Examples: `可投/非高确信`, `不投/谨慎`.

2. A finished benchmark can create false completeness.
   `29 / 29` sounds like total coverage unless the scope is stated explicitly.

3. Named exceptions can become post-hoc escape hatches.
   This is especially dangerous when the supporting evidence is not encoded in the card schema.

4. Control groups often identify the same quality tier instead of rejecting alternatives.
   A framework that says both target and comparable are BUY is not selecting, only describing.

5. Framework evolution can overfit history.
   Any new principle added after seeing outcomes must be treated as suspect until affected cases are re-run.
6. Point-in-time discipline can silently break.
   If a thesis uses facts that became knowable only after the decision date, the backtest is contaminated even if the final call was directionally right.
7. A framework that does not separate investment from speculation will overstate its own certainty.
   Graham's definition is stricter than "I have a thesis"; anything without analysis, principal safety, and adequate return is not core investment work.
8. Public/default guidance can drift too aggressive if investor type is left implicit.
   Graham's defensive-vs-enterprising split should be explicit, with the public build defaulting to defensive logic unless deeper work is justified.

## Rules Going Forward

1. Do not call the headline number "accuracy". Call it "retrospective consistency".
2. Never present the 29 rows as if they were the full Buffett/Berkshire universe.
3. Report ambiguous, exception-assisted, and non-binary cases separately.
4. Treat the core binary non-exception subset as the cleanest methodology sample.
5. Any framework update must list affected cases and re-run them before claiming improvement.
6. Any named exception must carry explicit structured evidence in the company card.
7. Every decision memo must be point-in-time. Later facts may appear only in the outcome reveal.
8. Every decision memo should explicitly classify itself as investment, speculation, or too hard.
9. Timing guesses must not be presented as if they were underwriting conclusions.
