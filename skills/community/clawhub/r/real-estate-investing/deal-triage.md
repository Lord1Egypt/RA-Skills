# Deal Triage

Run this screen before deep underwriting. The goal is to save time by killing bad deals fast.

## 30-second screen

Check these first:
- Does the deal fit the thesis and buy box?
- Is the ask price even close to realistic value?
- Is there believable rent support?
- Is the rehab scope within capability?
- Can likely financing support the plan?
- Is there a clean operational path after closing?

If two or more answers are "no" or "unknown in a dangerous way," do not underwrite yet.

## Red flags that justify fast rejection

- rent upside depends on fantasy renovations or illegal use
- seller numbers exclude obvious expenses
- insurance looks unavailable or dramatically mispriced
- foundation, structural, environmental, or title smoke already exists
- tenant mix or local regulation makes the execution model fragile
- BRRRR or flip math only works if the exit value is perfect

## Yellow flags that need focused follow-up

- taxes likely to reset after sale
- one big unit or one tenant drives too much of the income
- outdated systems with unclear remaining life
- neighborhood demand is real, but liquidity is thin
- property manager quality is unverified
- rents look strong, but concessions or bad debt are hidden

## Fast screen metrics

Use rough inputs only:

```text
gross_yield = annual_gross_rent / total_cost
break_even_guess = (opex + debt_service) / gross_scheduled_rent
cash_needed = down_payment + closing + rehab + startup reserves
```

Good triage questions:
- If rents land 10 percent lower, is the deal still alive?
- If rehab lands 20 percent higher, is the thesis still intact?
- If refinance never comes, is the hold still acceptable?

## Triage outputs

End each screen with one of three outcomes:
- advance -> worth full underwriting
- watch -> needs a few critical facts before deeper work
- pass -> weak fit or broken downside
