---
name: retirement-withdrawal-sequencer
description: "Use when a retiree or near-retiree asks which account to withdraw from, how RMDs work, whether to do Roth conversions, or how to avoid the IRMAA Medicare surcharge. Models year-by-year taxable/traditional/Roth draw order, RMDs from the Uniform Lifetime Table (age 73/75), bracket-fill conversions, and the 2-year-lookback IRMAA cliffs."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [retirement, taxes, rmd, irmaa, roth-conversion, withdrawals, finance]
---

# Retirement Withdrawal Sequencer

## The problem it solves
Retirees with three-account structures (taxable / traditional 401k-IRA / Roth) routinely lose $10k–$100k+ over a decade to withdrawal-order mistakes:
- taking everything from taxable first → later forced RMDs spike them into higher brackets;
- ignoring **IRMAA**: a large conversion or withdrawal pushes Medicare premiums up for TWO YEARS LATER (25%, 50%, 72%, 76%, 200% surcharge tiers on a 2-year-lookback MAGI);
- missing an RMD entirely → **25% excise tax** on the shortfall (SECURE 2.0; 10% if corrected within 2 years);
- leaving brackets unfilled in low-income years (the widow/er single-filer years are the worst);
- paying 15–22% on withdrawals that could have been 0–12%.

This skill produces a 5-year draw plan: which bucket, how much, estimated federal tax, effective rate, and IRMAA cliff warnings — plus a Roth-conversion window analysis.

## When to trigger
- "Which account should I withdraw from this year?" / "I just retired, how do I draw income?"
- "What's my RMD?" / "Do I have to take one at 73?" / "What if I miss it?"
- "Should I convert to Roth before RMDs start?"
- "Why did my Medicare premium jump?" → IRMAA lookback explanation + appeal paths.
- After a spouse's death (filing status change re-planning).

## Steps
1. Collect: ages, filing status, balances by bucket (taxable/traditional/Roth incl. cash %), annual spending need, other income (SS, pension), and current-year bracket data (defaults = 2026 estimates; **always verify against current IRS/SSA tables**).
2. **RMD engine:** first RMD year from birth year (born 1951–59 → 73; born 1960+ → 75); divide each traditional balance by the Uniform Lifetime Table factor; flag missed-RMD exposure + Form 5329 correction path.
3. **Sequencing engine (the default doctrine):**
   1. Cash/interest inside taxable →
   2. Taxable long-term gains (0% bracket headroom first: ~$49k single / $98k MFJ of taxable income 2026 est.) →
   3. Traditional withdrawals/conversions to *fill* the 12% (or 22%) bracket top →
   4. Roth last (spend order-of-last-resort; it's also the best inheritance asset).
   Social Security taken as given (claiming-age optimization is a separate skill).
4. **IRMAA cliff checker:** project MAGI each year against the tier thresholds (2026 est. single: $106k / $133k / $167k / $200k / $500k; MFJ ×2) and label each plan year: "affects Medicare year Y+2". Show the *cost per dollar over the cliff* (crossing a tier by $1 raises Part B+D premiums on ALL income ≈ $1,000–1,300/yr per tier single).
5. Output: 5-year table (bucket draws, taxable income, est. federal tax, effective rate, year-end balances, IRMAA flag), the conversion-window verdict, and the sequence-of-returns cash-buffer recommendation (hold 1–2 years of spending in cash before drawing from equities in a down market).

## Pitfalls
- **Brackets and IRMAA thresholds change yearly** — defaults are 2026 estimates; the output says so and the agent must verify current-year numbers before finalizing.
- **IRMAA is measured 2 years back**: premiums in 2028 depend on 2026 MAGI; first-year retirees can file SSA-44 (life-changing event) to appeal.
- **Roth conversions are irreversible** and stack on top of RMDs (RMD must come out first, conversion dollars come after).
- State taxes ignore-able in the model but real (some states exempt IRA income entirely).
- **QCD** (qualified charitable distribution, up to ~$110k/yr from IRA at 70½+) counts toward RMD without touching MAGI — the skill flags this when charitable giving + RMD coexist.
- ACA-pre-65: MAGI cliffs (premium tax credit) are far sharper than IRMAA — different engine, don't reuse this one.

## Example
```
$ python3 scripts/withdrawal_sequencer.py --age1 68 --age2 66 --status MFJ \
    --taxable 350000 --traditional 900000 --roth 250000 --cash-pct 10 --spend 96000 \
    --other-income 42000
YEAR 2026 (ages 68/66, MFJ)  spend $96,000, other income $42,000
  draw: taxable $54,000 (cash+LTCG, 0% LTCG bracket)  |  traditional $0
  est. federal tax: $1,905  effective on total income: 1.4%   IRMAA: OK (MAGI $96,000 < $212,000)
RMD START: 2031 (owner born 1958 -> age 73) projected first RMD ~$36,100
CONVERSION WINDOW: 2026-2030 — filling the 12% bracket top (~$105,700 taxable) adds ~$9,700/yr
  converted at 12% vs future 22-24% during RMD years -> ~$14k-19k/decade benefit per year converted.
```

## Files
- `scripts/withdrawal_sequencer.py` — RMD table, bracket engine, 5-year sequencer, IRMAA checker (stdlib only; all rates/tables in CONFIG at top, editable).
- `references/tax-tables-2026.md` — brackets, LTCG, standard deduction, IRMAA tiers, RMD factors (with verify-first sourcing note).
- `references/sequencing-doctrine.md` — the draw-order logic, Roth-conversion windows, QCD, widow/er re-planning, 25% excise fix.
- `README.md` — real-world framing.
