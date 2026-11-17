# Window AC Sizing — Load Model, Short-Cycling, and Purchase Physics

## 1. Where "20 BTU per sqft" comes from (and where it breaks)
The DOE/Energy Star quick table (~20 BTU/h per sqft, adjusted for sun/occupants/kitchen) is a condensed Manual J for *typical* US construction: 8-ft ceilings, average insulation, temperate climate design temps. It breaks when:
- Ceiling > 8 ft: conditioned volume grows linearly; +5% per extra foot is the working approximation.
- West-facing glass: afternoon solar gain through glazing dominates; whole-wall west exposure adds 10–15%.
- Poor envelope (pre-1950 uninsulated walls, single-pane, drafty): +15–25%; the AC ends up fighting infiltration more than conduction.
- Kitchen/cooking adjacency: +4,000 BTU/h (the classic Manual J allowance) — covers a dinner's worth of cooktop+oven+exhaust spill.
- Occupants: a seated person ≈ 600 BTU/h sensible+latent; add per person beyond two.
- Climate: deep-south design temps (95–105 °F outdoor) push the whole stack +10%; marine/coastal mild climates can relax −10%.

A room load computed this way lands within ~15% of a professional block-load Manual J for standard rooms — enough to pick the right shelf size, which comes in coarse steps anyway (5/6/8/10/12/15/18k).

## 2. Latent vs sensible — why oversizing feels wrong
Total cooling = sensible (temperature) + latent (moisture removal). A compressor removes latent heat only while the coil is below dew point *and* air is moving across it. Ratio matters:
- Short cycles (2–6 min): coil barely reaches condensation temperature before setpoint cuts the run; SHR effectively rises — you get sensible-only cooling. Room hits 72 °F at 65% RH = clammy.
- Long modulated runs (15–30+ min): steady condensate stream; 50–55% RH; feels dry and cooler than the number.
That's why the **+15% oversize ceiling** doctrine exists, and why inverter (variable-speed) units changed the calculus: they throttle to hold load, running continuously at 30–60% output — dehumidifying like a small unit while sized for the design day. If the smallest shelf size is >1.5× your load, an inverter model is the correct answer, not a bigger compressor.

## 3. Short-cycling signatures (existing-unit triage)
| Symptom | Mechanism | Verdict |
|---|---|---|
| Cold but damp/musty smell | Oversized; latent never condensed | Downsize on replacement; add standalone dehumidifier now |
| On/off every 3–5 min at moderate setpoint | Oversized or refrigerant/sensor fault | Check sizing first — it's free |
| Runs constantly, never cold enough | Undersized, dirty filter/coil, duct/leakage (portables), or 130 °F attic heat load | Clean filter, then re-run the load math |
| Icy coil (frost on fins) | Low airflow (filter) or low charge | Filter first; frost = pro service |
| Freezes then thumps | Crankcase slinger dry-mount tilt wrong | Re-level per manual |
Tracking: log on/off timestamps for an hour at a normal setpoint; >6 cycles/hour = short-cycling.

## 4. Electrical gates (US)
- 115V units: ≤ ~8,000 BTU generally; 10–12k exist at 115V but pull 9–12 A — want a dedicated 15A (or 20A) circuit; sharing with a PC/TV circuit trips breakers at compressor start (LRA 4–6× RLA for a second or two).
- 230V units: 12k+; need a matching receptacle (NEMA 6-15/6-20). There is no safe adapter — the circuit must exist.
- Old wiring/aluminum branch circuits: treat a 10 A continuous draw as a red flag; consult an electrician before any 115V 12k purchase.
- Soft-start/inverter units cut the inrush problem and often fit marginal circuits the old units tripped.

## 5. Efficiency math (CEER)
CEER = BTU/h ÷ watts, including standby. Season cost:
```
watts = btu / ceer
kwh_per_hour = watts / 1000
season_cost = kwh_per_hour × hours_per_day × days × price
```
Worked: 10,000 BTU, CEER 15 → 667 W → 8 h/day × 120 days × $0.17 = $109/season. Same unit at CEER 11 → 909 W → $149/season. The $40–60 price gap between efficiency tiers typically pays back in 1–2 seasons at 8 h/day usage — but only at real hours; a bedroom unit run 30 nights is nearly indifferent, buy on noise.

## 6. Portable units (the label lie)
Single-hose portables exhaust conditioned room air, creating negative pressure that pulls hot outside air in through every crack. DOE's 2017 test procedure (SACC — Seasonly Adjusted Cooling Capacity) reflects this: a "14,000 BTU (ASHRAE)" single-hose unit is often ~8,000 SACC. Rule: compare portables by SACC on the Energy Guide, prefer dual-hose (recovery of most of the loss), and apply the load model to the SACC number, not the box BTU.

## 7. Install details that decide satisfaction
- **Tilt**: follow the manual, not folklore — many modern units design-in a slight rear tilt for condensate drainage to the outdoor side or to the slinger fan; dead-leveling per old advice can leak indoors.
- **Bracket vs frame**: a support bracket carries most weight, reduces sash strain, and simplifies seasonal removal; check the manual allows it (some warranty-require the factory sill mount).
- **Sealing**: side filler panels foam-sealed; an unsealed gap is a hot-air slot machine at exactly the height you sleep. Insulated side panels beat the stock 1/8" plastic for winter heat loss too.
- **Winter**: remove or cover + seal; a unit left in the window is a $50–150/season heat leak in cold climates.
- **Bedroom placement**: don't aim at the bed — cold air directly on sleepers disrupts sleep thermoregulation; aim along the ceiling or use the low fan + upward vanes.

## 8. Window heat pumps (should you?)
- Modern window heat pumps (Midea/GE/etc.) cool like their BTU class and heat to below freezing with decent COP; great for buildings where the boiler runs Oct–Apr but the room is an oven Jun–Sep, or where resistive baseboard is the alternative.
- Check the heating output at YOUR design low (capacity falls with outdoor temp); below ~5 °F most window HPs fade — they're shoulder-season answers, not Minneapolis January answers.
- Cost math: heating at COP 3 vs resistive strips = 1/3 the kWh per BTU; the same `cost` command arithmetic applies with a COP divider.

## 9. Sources
DOE room AC sizing guidance & SACC test procedure (10 CFR 430), Energy Star room AC buying guidance, ACCA Manual J (load fundamentals), AHRI CEER definitions, NEC 210 branch-circuit basics. Factors are US-market conventions; for 230V/50Hz markets the BTU buckets differ (7/9/12k) but the physics is identical — swap the shelf table, keep the model.
