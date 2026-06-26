# Rental Property Underwriter

**Domain:** Real Estate · Residential Investing
**Platforms:** Claude · Codex

## Purpose

Turns a property and a set of assumptions into a disciplined underwriting memo: NOI, cap rate, cash-on-cash, DSCR, break-even occupancy, a 5-year pro-forma, sensitivity matrix, deal-breaker check, and a GO / CONDITIONAL / NO-GO verdict with a renegotiation lever. Built for residential investors, agents, and analysts evaluating a single single-family, small multi-family, or short-term rental opportunity.

## When to Use

- Underwriting a property before submitting an offer
- Stress-testing a deal that "looks good on the listing"
- Building a packet for a DSCR-loan lender or capital partner
- Deciding whether to walk away, renegotiate, or proceed

## What It Does

1. Collects property facts, strategy (LTR / STR / mid-term / house hack / BRRRR), purchase, rent, operating, and financing assumptions through one-question-at-a-time intake
2. Confirms a one-screen assumption summary before computing anything
3. Computes Year-1 stabilized metrics — GSI, EGI, OpEx, NOI (lender and investor), cap rate, DSCR, cash-on-cash, break-even occupancy, rent-to-PITIA — and color-codes each against directional benchmarks
4. Projects a 5-year pro-forma and runs a sensitivity matrix on rent and vacancy (plus rate, for variable-rate financing)
5. Runs a deal-breaker check (DSCR floor, optimistic rent, missing reserves, insurance fragility, STR regulatory risk, HOA risk, comp risk, exit assumption) and issues a GO / CONDITIONAL / NO-GO verdict with a specific renegotiation lever

## Notes

This skill produces an **underwriting memo**, not investment, tax, or legal advice. Rent comps, insurance binders, HOA bylaws, STR regulations, and inspection findings must be verified before submitting an offer or signing financing. The skill treats property identifiers, financing details, and personal capital figures as confidential and prefers a property code over a full address when the user wants discretion.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.