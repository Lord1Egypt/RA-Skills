# <TICKER> pre-publication checks

> Template. Save as `research/<report-id>/checks.md`. Each row gets one result: passed / fixed / n/a. "fixed" and "n/a" need
> a sentence. A row ticked without a note counts as not checked.
> Sources: `references/judgment.md` section 9 and the implementation checklist in `references/quality-bar.md`.

| # | Check | Result | Note (fixed: what changed; n/a: why it does not apply) |
|---|---|---|---|
| 1 | The method used for consensus (implied, public compilation, options, wording) is stated in the report | | |
| 2 | Every mispricing has E1-E5 evidence; those without it were downgraded to "observation" | | |
| 3 | The catalyst path table is complete; anything with no catalyst in 12 months is marked "structural view" in the summary | | |
| 4 | The annual horizon states the benchmark (with why it was chosen), the start date (close of the publication date) and 12 months; all editions of the series use the same benchmark | | |
| 5 | The three-horizon outlook and the transition-condition box are in chapter 1 and appear once in the whole report | | |
| 6 | The decision chapter uses the five-item research-action format; each of its four information items appears exactly once | | |
| 7 | The target price has two independent paths; a gap above 20% is explained | | |
| 8 | WACC sensitivity, terminal-value share, the basis for probabilities, and the funding source and target-date assets use one set of books | | |
| 9 | The probability-weighted result is reconciled with the market-implied expectation; the differences are in the summary | | |
| 10 | No [D] in the payload chain of a core conclusion; any [C] has a +/-30% sensitivity run | | |
| 11 | Every core conclusion on the summary page is marked with its evidence strength | | |
| 12 | No look-ahead: no filing after the filing cutoff and no quote after the basis date is used | | |
| 13 | Quote freshness: the basis date is a closed trading day and two sources agree | | |
| 14 | Earnings date: the next earnings date is in the summary; if it is under 10 trading days away, the report says "figures in this edition may be updated on date X" | | |
| 15 | Opposite side answered: if the rating is not neutral, the opposing side's first three arguments are answered in the body, one by one | | |
| 16 | All eight required components are present (mechanism diagram / evidence grading / certainty layering / bull-bear comparison / falsifiability and observation calendar / known limitations / misreading section / audit revision log) | | |
| 17 | Known limitations contain the standing entries (including "events after the basis date are not reflected; settlement uses actuals") | | |
| 18 | Disclosures and conflicts of interest are taken verbatim from `assets/disclaimer.md`, and every conflict-of-interest item is written out (including "none") | | |
| 19 | Cross-edition alignment check shows zero differences; the second edition contains zero characters of the source script | | |
| 20 | (Updates) The prior-version settlement chapter is written; every ledger entry that came due is settled | | |
| 21 | After publishing: all core judgments, the annual rating, and the monthly and quarterly outlooks are registered in the ledger; the series is added to `research/watch.json`; `python3 scripts/desk.py check` reports 0 uncovered | | |
| 22 | The title is the claim, with a per-share impact; thesis and subtitle within their limits | | |
| 23 | At least three new facts, each with a section in Part 1, an exhibit, and a landing point on the value bridge | | |
| 24 | Part 3 takes management's public statements apart; Appendix A statement timeline complete | | |
| 25 | `check_report.py` exits 0 for every edition (length, footnotes, exhibits, sentence density, internal codes) | | |
| 26 | Verifiability lane: 30 footnotes and every exhibit source opened; text and numbers found at the stated location | | |
| 27 | All scenarios use one discounting timing convention; per-share conversion states share basis, tax rate and discount rate | | |
