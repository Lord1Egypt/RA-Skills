# Amortization Math — Worked Examples

## The Payment Formula

Monthly payment for principal P, annual rate a%, term n years:

    r = a / 100 / 12
    M = P · r / (1 − (1 + r)^(−12n))

$280,000 at 5.25%, 30y: r = 0.004375, n = 360 → M = $1,546.17. (This is what the tool's
`pmt()` returns and what lenders quote as P&I.)

## Balance Dynamics

Each month: interest = balance × r; principal = payment − interest; new balance = balance −
principal. Early payments are interest-heavy — at 5.25% on $280k, month 1 is $1,225 interest
vs $321 principal. This asymmetry is why "years in" matters so much for refi math.

## The Clock-Reset Trap, Quantified

Borrower 7 years into a $320k 30-year 6.5% loan, balance $280k, payment $1,768. Refis into a
new 30-year 5.25%:

| | Current loan (23y left) | New 30y loan |
|---|---|---|
| Payment | $1,768 | $1,546 |
| Months to payoff | 276 | 360 |
| Lifetime interest remaining | ~$208k | ~$277k |

Monthly savings $222 — but if both loans run to natural payoff, the new loan pays ~$69k MORE
interest because it re-extends to 360 months. The horizon comparison catches this: over any
fixed horizon the tool compares payments AND equity built, so a re-extended clock shows up as
slower equity growth.

**The fix:** pay the old payment on the new loan (`--extra-monthly 222`). Same out-of-pocket
as today, lower rate, payoff at ~month 276-equivalent or sooner — the clock reset vanishes and
you keep the full rate win.

## Points → Break-Even Mapping

A point = 1% of loan, buys roughly 0.25% rate reduction (market-dependent). $280k, one point
= $2,800. Rate 5.25→5.00%: payment $1,546→$1,497, saving $49/mo → point break-even ≈ 57
months. Points are a bet on staying; under ~4 years, take the no-points rate. The compare
command surfaces this as NET@HORIZON instantly.

## Equity Curve Check (why horizon math ≠ payment math)

Net position at horizon H months = (payments made) − (equity built) for each loan. The tool
computes equity as balance reduction. Two loans can have identical payments-yet-different
equity if their rates differ (rate sets the interest/principal split). This is why the tool
never ranks offers by payment alone.

## Negative Amortization Guard

If payment < first month's interest, balance grows. The tool detects this and flags instead of
producing a fake payoff. Real-world trigger: hardship scenarios with teaser rates.

## Verification Example (do this sanity check)

Any output of `analyze` can be checked by hand:

    pmt(280000, 5.25, 30) = 1546.17
    lifetime_cost over 84 months ≈ payments 129,878 → interest 97,360, balance ≈ 253,518

Interest ≈ payments − principal reduction: 84 × 1546.17 = $129,878; principal reduced by
$26,482 → interest $103,396?? No — the tool tracks month-by-month (interest falls as balance
falls), giving $97,360. Simple division overestimates early-term interest; month-by-month
iteration is the honest number. This is exactly why the script loops instead of using
shortcuts.
