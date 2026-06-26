---
name: buffett-oracle
description: Point-in-time Buffett-style company analysis for stocks, Berkshire case studies, and BUY/PASS verdicts. Use when the user wants a Buffett/Graham underwriting memo, moat test, control-group comparison, or benchmark backtest grounded in cached company cards and strict decision-date discipline.
homepage: https://github.com/yixiao1032-publish/buffet-oracle
metadata:
  clawdbot:
    emoji: "🔮"
    requires:
      env: []
    files:
      - "SKILL.md"
      - "buffett-oracle.md"
      - "buffett_brain.md"
      - "backtest_results.md"
      - "coverage_scope.md"
      - "analysis_index.json"
      - "universe_expansion.md"
      - "universe_expansion_index.json"
      - "company_cards/"
---

Buffett Oracle is a research skill for deciding whether a company deserves a `BUY` or `PASS` under a strict Buffett + Graham underwriting framework.

Use this skill when the user wants:
- A Buffett-style memo on a public company, bank, utility, or crypto protocol
- A point-in-time re-underwriting of a Berkshire decision
- A moat explanation tied to hard numbers, not vibes
- A clean `BUY` / `PASS` verdict instead of a hedged summary
- A comparison against prior benchmark cases or same-era control groups

## Read Order

Read only what you need:

- `buffett-oracle.md`
  Use for the Buffett Oracle persona, output structure, and portable prompt wording.
- `buffett_brain.md`
  Use for the Graham operating layer, 7 hard gates, named exemptions, and moat logic.
- `coverage_scope.md`
  Read before making any claim about benchmark completion or historical coverage.
- `company_cards/`
  Check first. If a matching card already exists, reuse it and do not re-fetch the filing.
- `backtest_results.md` and `analysis_index.json`
  Use for benchmark precedents and indexed case linkage.
- `universe_expansion.md` and `universe_expansion_index.json`
  Use for non-benchmark precedents without polluting the benchmark hit-rate.
- `methodology_audit.md`
  Read when the user asks how reliable the framework is, or whether the score implies predictive power.
- `gate_review.md`
  Read when the user asks why certain high-quality assets still fail the hard gates.

## Non-Negotiables

- Use only information that was public on or before the decision date.
- Never describe the 29 benchmark rows as Buffett or Berkshire's full investment universe.
- Never re-fetch a company that already has a cached card in `company_cards/`.
- If any hard gate fails, default to `PASS` unless a named exemption clearly applies.
- Every `BUY` needs two same-era control groups.
- Lock the `BUY` / `PASS` conclusion before revealing what Buffett actually did.
- Treat this as a research framework, not personalized investment advice.

## Workflow

1. Classify the request as `INVESTMENT`, `SPECULATION`, or `TOO_HARD`.
   If it is `SPECULATION` or `TOO_HARD`, explain why and stop.
2. Check `company_cards/` for a cached `<TICKER>_<YEAR>.json`.
   Reuse the card if present. Only fetch a new filing when no card exists.
3. Run the 7 hard gates from `buffett_brain.md`.
   Any failed gate means `PASS`, unless one of the named exemptions below is explicitly justified.
4. Apply required overlays when triggered.
   If `g2` fails but moat still matters, add an owner-earnings note.
   If `g6` fails but moat still matters, add a quality-multiple note.
   For new live or expansion memos, include `management_veto` as `clear`, `watch`, or `fail`.
5. Write the moat paragraph.
   If you cannot explain why competitors cannot replicate the business in 10 years, the answer is `PASS`.
6. For every `BUY`, include the safety-margin math.
   State owner's earnings or normalized earnings, value range, required return, and implied discount.
7. Pick two same-era control-group companies that Buffett did not buy.
   Run the same gate logic on them. If they also pass, explain the differentiator.
8. Lock the verdict before reveal.
   Only after the verdict should you reveal Buffett's action, later outcome, and whether the framework agreed.
9. If you are updating this repository, save the card, append the memo to the correct markdown archive, and update the matching index JSON.

## Named Exemptions

- `CRISIS_PREFERRED`
  For Goldman 2008 / BAC 2011 / GE 2008 style preferred-plus-warrant rescue structures.
- `INFRA_EXEMPTION`
  For rail and utility monopolies when monopoly status is clear and `EV/EBITDA < 15x`.
- `GROWTH_EXCEPTION`
  For high-ROIC compounders where weak raw FCF mostly reflects value-creating expansion rather than bad economics.

If you invoke an exemption, say so explicitly and defend it.

## Output Contract

Use this summary block in the final answer:

```text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CLASSIFICATION: [INVESTMENT / SPECULATION / TOO_HARD]
VERDICT: [BUY / PASS]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Hard Gates: [all passed / failed gates / exemption applied]
Named Exemption: [CRISIS_PREFERRED / INFRA_EXEMPTION / GROWTH_EXCEPTION / none]
Moat Type: [brand / network / switching cost / cost advantage / none]
Safety Margin: [owner's earnings, value range, required return, implied discount]
Key Conviction: [one sentence]
Key Risk: [one sentence]
Control Group: [Company A | Company B]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Then reveal:
- what Buffett or Berkshire actually did
- what happened afterward
- whether the framework and Buffett agreed

## Data Guidance

- For US equities, prefer SEC EDGAR press-release or annual-report pages before full 10-K pulls.
- For non-US companies, use official annual reports or equivalent filings.
- For crypto or Web3, use on-chain and protocol-source documents, but keep the same anti-speculation bar.
- Post-decision facts belong only in the reveal section, never in the underwriting logic.

## Scope Reminder

The audited benchmark is a curated 29-case set. It is evidence of archive coverage, not a promise of forward hit rate and not the full Berkshire history.
