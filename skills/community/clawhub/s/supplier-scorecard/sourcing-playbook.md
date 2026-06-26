# Sourcing Playbook — Logging, Sampling, Dual-Sourcing, and Switching

## Evidence log setup (the foundation)

Minimum fields per order row:

```
order_id | supplier | order_date | promised_ship | actual_ship |
units_ordered | units_received | incoming_defects | customer_defects_60d |
spec_deviations (description + approved Y/N) | comms_incidents | landed_cost/unit
```

- Reconstruct the last 90 days from PO history, email, and chat exports for the first scorecard; flag estimated cells.
- Log communication incidents in both directions: slow replies AND proactive warnings (the positive signal matters).
- 15 minutes per order at receiving time keeps the log current; batch reconstruction takes 10× longer.

## Sample evaluation protocol

1. **Blind side-by-side:** 3 units per candidate supplier, labels covered, evaluated against the written spec sheet by someone who doesn't know which is which.
2. **Spec sheet first:** if you can't write the spec (materials, tolerances, finish, packaging), you can't evaluate samples — write it before requesting them.
3. **Stress the failure mode:** test the thing customers return it for (zipper cycles, battery drain, seam pull, drop test) — not general "feel".
4. **Photograph everything:** sample photos become the golden-sample record attached to every future PO.
5. **Paid samples are fine:** free samples bias toward suppliers who invest in pre-sales; judge the product, not the generosity.

## Pilot order protocol

- Size: smallest MOQ the supplier accepts, or 5–10% of normal volume.
- 100% incoming inspection on the pilot (sampling comes later, once trust is scored).
- Run it through the REAL flow: your freight forwarder, your warehouse, your listing — pilot orders shipped to the office hide fulfillment problems.
- One pilot is data; two pilots (one in a busy season) is evidence.

## Dual-sourcing rules

- **Hero SKUs (top ~20% of revenue): always dual-source.** Default split 70/30 — enough volume for the backup to take you seriously and keep tooling warm.
- Accept slightly worse unit economics on the 30% line; it's insurance premium, priced in.
- Keep specs and packaging identical enough that a customer can't tell the lines apart; batch-code them so YOU can.
- Re-balance the split annually based on scorecards, not loyalty.
- For single-mold products where dual tooling is uneconomic: hold the second supplier "qualified-warm" (samples approved, pricing agreed, no standing orders) and accept the 60–90 day activation lag as known risk.

## Switching protocol

Trigger: score gap ≥15 points sustained 2 consecutive quarters, or any score-1 event (misrepresentation, deposit-and-renegotiate).

1. **Model switching cost first:** new tooling, pilot + inspection, MOQ of the first real order, listing risk from any quality change, management attention. Compare against the annualized cost of the score gap.
2. **Qualify before signaling:** samples + pilot from the new supplier BEFORE telling the incumbent anything.
3. **Overlap, never cut over:** run 70/30 old/new for one cycle, then 30/70, then exit. A single-PO cutover bets the listing on an unproven line.
4. **Exit clean:** settle balances, retrieve molds/tooling you paid for (get tooling ownership in writing at the START of any relationship), keep the door open — re-qualification is cheaper than starting cold.

## Negotiation with the scorecard

- Share the rubric and the supplier's scores annually; suppliers fix what's measured and rewarded.
- Trade improvements for commitments: "defects <1.5% for two quarters → we consolidate the new SKU with you."
- Use dimension scores, not the total, at the table: "your quality is a 9, your lead-time accuracy is a 5 — fix the 5 and the volume grows."
- Never fabricate a competing quote; suppliers verify market prices better than you do.
