# Retirement Withdrawal Sequencer

**"Which account do I pull from?" is the highest-leverage untaxed decision in retirement — and most people get it wrong in one of two directions: drain the taxable account and walk into an RMD bracket spike, or sit on low-bracket headroom that expires every December 31.**

A couple drawing $96k/yr can pay 1–9% effective federal tax on the same portfolio depending purely on bucket order, timing of Roth conversions, and the **IRMAA trap**: a withdrawal spike this year raises their Medicare premiums two years later, tier by tier, on all income (a $1 conversion over a cliff ≈ $1,100–6,300/yr in extra premiums).

## What it does
- **RMD engine:** first-RMD year from birth year (73 or 75 under SECURE 2.0), Uniform Lifetime Table amounts, the missed-RMD 25%→10% excise repair path.
- **5-year draw plan:** cash → 0%-band LTCG sales → bracket-fill traditional → Roth last, with estimated federal tax, effective rate, and MAGI each year.
- **IRMAA cliff checker:** every year labeled with its tier and the Medicare year it hits (2-year lookback), plus SSA-44 appeal note for new retirees.
- **Conversion-window verdict:** compares projected first RMD against the 22% bracket and says whether to convert now — with the constraints (RMD-first stacking, irreversibility, IRMAA ceiling) printed.
- **QCD flag** when charitable giving + RMDs coexist: the IRA→charity direct transfer that erases the MAGI.

## Example
```
$ python3 scripts/withdrawal_sequencer.py --age1 68 --age2 66 --status MFJ \
    --taxable 350000 --traditional 900000 --roth 250000 --cash-pct 10 \
    --spend 96000 --other-income 42000 --charitable 5000
2026 (age 68): draw: cash $35,000, taxable-sale $19,000 (gain $7,600)
     taxable income $19,850 -> est. federal tax $4,754 (eff 9.3% of MAGI)
     MAGI $51,350 -> IRMAA OK — hits Medicare premiums in 2028
     QCD: direct $5,000 from IRA to charity — satisfies RMD, excluded from MAGI
CONVERSION WINDOW 2026-2030: projected first RMD ~$43,345 vs 22%-top $211,400
  VERDICT: RMDs contained — conversions optional; protect IRMAA headroom instead.
```

All rate tables live in one CONFIG block (2026 US estimates; every run prints the verify-first disclaimer). Stdlib-only Python, offline.

## License
MIT
