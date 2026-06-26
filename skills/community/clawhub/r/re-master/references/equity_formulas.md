# Equity Calculation Formulas (re-master)

This reference documents the logic used in the `scripts/equity_calc.py` and `scripts/re_sim.py` tools.

## Proportional Ownership Formula

Ownership is calculated based on the total cumulative capital contribution at any given point in time (Month $T$).

$$Ownership\%_{a,T} = \frac{Capital_{a,T}}{\sum_{i=1}^{n} Capital_{i,T}} \times 100$$

Where $Capital_{a,T}$ is:
$$Capital_{a,T} = DP_a + (Monthly_a \times T)$$

- **$DP_a$**: Initial Downpayment contribution from Account $a$.
- **$Monthly_a$**: Monthly recurring contribution from Account $a$.
- **$T$**: Months elapsed since the signing date.

## Admin Cash Pool Allocation (inv1)

In the current version of the simulation, the "Admin Cash Pool" (available liquid buffer) is treated as a contribution from the primary administrator account (**`inv1`**).

- At Month 0, the total available funding for the Downpayment includes `inv1.upfront` + `total_cash_pool`.
- This reflects the real-world scenario where the admin provides the initial liquidity buffer to secure the unit while partners catch up via monthly contributions.

## Fair Share Request Calculation

To maintain a buffer threshold (e.g., AED 250,000), the "Fair Share" request for Partner $P$ is calculated as:

$$Request_P = (TargetBuffer - CurrentBuffer) \times Ownership\%_P$$

This ensures that the cost of maintaining liquidity is borne proportionally by all equity holders.
