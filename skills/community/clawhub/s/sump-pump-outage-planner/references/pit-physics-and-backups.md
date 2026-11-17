# Sump Pit Physics, Inflow Measurement, and Backup Engineering (Reference)

## 1. Pit geometry

```
gallons per vertical inch = pi * (D/2)^2 / 231
```

| Pit diameter | Gal / inch |
|---|---|
| 14 in | 0.67 |
| 16 in | 0.87 |
| 18 in | 1.10 |
| 20 in | 1.36 |
| 24 in | 1.96 |

**Usable rise** = from normal resting ("off") water level to the
lowest escape point: the floor lip around the pit, a cleanout/inlet
that overflows into the basement, or the under-slab feed that starts
backfeeding. Measure the small number, not the full pit depth.

## 2. Inflow from the off-period (the bucket-free measurement)

Sump pumps cycle: water rises to "on" level, pump empties to "off"
level, pump waits. During the wait, inflow fills the known gap:

```
gap_gallons = on_off_gap_in * gal_per_inch
inflow_gpm  = gap_gallons / off_minutes
```

Example: 18-in pit (1.10 gal/in), 6-in on/off gap = 6.6 gal, off-period
8 min → 0.83 gpm ≈ 50 gph baseline. First hard rain of spring on clay
soil: 3–4× that.

Sanity alternative: during a pump run, time the RUN seconds and you
know the pump moved one gap volume — that calibrates the pump's actual
delivery too.

## 3. The clock

```
hours_to_critical = usable_rise_in * gal_per_inch / (inflow_gpm_storm * 60)
```

Verdict bands:

| Hours | Meaning |
|---|---|
| > 12 | You have a night of sleep. Battery backup optional, alarm still smart. |
| 4–12 | Backup essential. Battery covers most outages; generator for long ones. |
| 1–4 | High-risk pit. Dual pumps (main + backup on independent power) + high-water alarm. |
| < 1 | This is a spring, not a pit. Drainage remediation, not bigger pumps. |

## 4. Backup options, honestly

| Option | Protection | Constraints |
|---|---|---|
| Battery backup (12 V pump + deep-cycle) | 6–15 h at 50 gph-class inflow | Battery dies in 2–4 yr; needs quarterly test; $150–400 + battery |
| Inverter + big battery bank / power station | similar, sized by Wh | Same chemistry reality; quiet, indoor-safe |
| Portable generator + transfer cord to a dedicated inlet | fuel-limited (days) | Runs the MAIN pump at full ⅓–½ HP; outdoor only, CO rules; needs the inlet installed in advance |
| Water-powered pump (municipal) | unlimited (water pressure) | Needs 40+ PSI city water — NOT wells; ~1 gal city water per 2 gal pumped; code restrictions in some areas |
| Second AC pump on the other circuit | protects against pump failure, NOT outage | Cheap resilience for the most common failure (the pump itself) |

Failure statistics reality: most sump failures are the pump or the
float, not the power. A backup PUMP (any kind) addresses both only if
it has its own float and power.

## 5. Battery math

A 12 V backup pump drawing ~5–8 A intermittently: average draw at 50%
duty ≈ 3 A. Usable deep-cycle capacity ≈ rated Ah × 0.5 (don't drain
below 50%):

```
hours ≈ Ah * 0.5 / average_amps
```

75 Ah → ~12 h at 3 A average. AGM handles the duty better than
flooded; lithium (LiFePO4) handles it best but costs more than the
pump.

## 6. 2 AM triage card

**Pump silent:**
1. Breaker + GFCI (press TEST/RESET) — free, do it first.
2. Power at outlet? (radio/phone charger).
3. Lift float by hand → runs = stuck/hung float ($15 part or zip-tie
   the tether shorter). Nothing = pump or cord.
4. GFCI won't reset → ground fault in the pump: unplug, extension cord
   to a different circuit as a stopgap, replace pump.

**Pump runs, water rising:**
1. Discharge: frozen? crushed? check valve failed (constant short
   cycling = water falling back)?
2. Impeller worn (pump old, runs "weak") — replace pump.
3. Air lock (air trapped in volute): some pumps have a weep hole —
   clear it.
4. Inflow > capacity: pump fine, water winning → add second pump.

**Pump never stops:**
1. Stuck-on float or tangled tether.
2. Check valve failed (pumping in circles).
3. Inflow beyond capacity (pump runs but level creeps) — drainage
   problem: downspouts, grading, weeping tile.

**Power out, no backup:** bucket-bail math — the script's clock tells
you the interval. Two people alternating with 5-gal buckets at ~30
gal/10 min beats 100 gph inflow only barely: every hand on deck before
the clock runs out, and wet-vac for the floor.

## 7. Maintenance calendar

- Monthly (wet season): listen for short-cycling; pour a bucket of
  water in, confirm clean cycle to "off".
- Quarterly: unplug main → backup cycles → restore. Test alarm.
- Yearly: pull pump, clean the screen/sump grit, check float travel,
  check valve operation, discharge exit clear and sloped.
- Every 4–6 yr: pump replacement on schedule (they die at the worst
  time; a $120 pump is cheaper than one finished-basement insurance
  claim with a $5,000 deductible).
