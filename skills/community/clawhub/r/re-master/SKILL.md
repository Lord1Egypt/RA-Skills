---
name: re-master
description: Manage off-plan real estate investments, payment milestones, group buy allocations, and ROI simulations. Use when a user needs to: (1) Track property installments (Dubai 60/40, 70/30 plans), (2) Calculate proportional ownership between investors (Binkl/Dad/Friends), (3) Manage a cash buffer pool for admin payments, (4) Generate unique sharing links for investors, (5) Simulate ROI or payment gap scenarios.
metadata:
  {
    "openclaw": {
      "requires": {
        "bins": ["python3"]
      }
    }
  }
---

# Real Estate Master (Off-Plan Tracker) 🏙️

This skill enables precise management and simulation of off-plan property investments, particularly for group buy scenarios with an admin-managed cash pool.

## Core Workflows

### 1. Project Initialization
When a user adds a new unit (e.g., Rotana, Ohana):
1.  **Define Price & Fees:** Typically 4% DLD + registration.
2.  **Define Payment Plan:** (e.g., 10% DP + 1% monthly or 10% every 6 months).
3.  **Establish Buffer:** Define the starting cash pool (e.g., AED 480k).

### 2. Group Buy Allocation
Calculate equity based on:
-   **Initial DP Contribution:** Who put in what at the start.
-   **Monthly Commitment:** Ongoing AED/month contributions.
-   **Weighted Time:** Ownership adjusts dynamically as payments are made.

Use `scripts/equity_calc.py` for simple math or `scripts/re_sim.py` for full multi-month simulations.

### 3. Buffer & Milestone Simulation
The "Admin Cash Pool" strategy:
-   Use the pool to cover shortfalls or early milestones.
-   Simulate "Fair Share" requests to investors to keep the pool above a safety threshold (e.g., > AED 250k).

Run `python3 scripts/re_sim.py <config.json>` to generate a full funding forecast.

### 4. Sharing URLs (Developer Note)
The `re-master` skill provides data for per-investor views. To generate URLs:
-   **Local:** Use the `dash/<token>` routes if using the original Deal Tracker server.
-   **Static:** Use the simulation output to generate static reports for participants.
This skill does not run a web server; it provides the logic to power one.

## References

-   **Dubai Norms:** See [references/dubai_standards.md](references/dubai_standards.md) for tax, fee, and escrow basics.
-   **Equity Math:** See [references/equity_formulas.md](references/equity_formulas.md) for the "weighted contribution" logic used in group buys.

## Scripts

-   `scripts/re_sim.py`: Comprehensive multi-unit simulation engine. Input unit/account config ➔ Output monthly milestone funding breakdown.
-   `scripts/equity_calc.py`: Simple point-in-time equity calculator.

---
*Created for Binkl 👑 — 2026-03-06*
