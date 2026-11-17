# Smell Source Detective — Reference

Deep documentation for the diagnosis engine. The script's knowledge
base lives in `scripts/smell_detective.py`; this file explains the
model, evidence hierarchy, and protocols behind each verdict.

## 1. The Diagnosis Model

The engine scores each hypothesis with:

```
score = base_rate × location_match × timing_match
```

- **base_rate** — how common the source is in general (a dry P-trap
  beats a broken sewer lateral, statistically).
  - Very common (base 0.5-0.7): dry P-trap, garbage disposal film,
    dirty HVAC filter, trash residue, pet urine in pad.
  - Common (0.2-0.4): dead rodent in void, wax ring failure, mold
    cavity < 1 m², stored product off-gassing, litter box neglect.
  - Uncommon (0.05-0.15): vent blockage, roof leak into wall, AC
    coil biofilm, refrigerator drip pan, washing-machine gasket.
  - Rare (0.01-0.05): sewer lateral break, hidden plumbing leak in
    wall, electrical overheating, natural gas fitting.
- **location_match** — each source has an affinity set of locations
  (bathroom/kitchen/basement/bedroom/hallway/whole-house/car/garage/
  outdoors). A source scores 0 outside its affinity set.
- **timing_match** — trigger multipliers keyed to what the user
  reports: mornings-only, after-rain, when-appliance-runs, constant,
  sudden-onset, seasonal, after-vacation, worse-when-hot.

The confirming **check** is what makes a hypothesis actionable: a
hypothesis is only "diagnosed" after its check passes, never on
score alone.

## 2. The Four Danger Patterns

These override the ranking — screen them FIRST.

### 2.1 Gas (rotten-egg additive, mercaptan)
- **Why dangerous:** explosive range is narrow but real; additive
  fade in new gas can make leaks nearly odorless.
- **First 10 minutes:** don't flip switches, don't use phone indoors,
  don't light anything. Open windows on the way out. Call gas
  emergency line from OUTSIDE. Wait for them.
- **Never:** soap-bubble test with an open flame nearby, or
  "sniffing closer" to a fitting.

### 2.2 Fish smell with no fish
- **Why dangerous:** overheating PVC/plastic wire insulation and
  failing CFL/LED ballasts release amines that read as "fish."
  This is a recognized precursor to electrical fires.
- **Action:** unplug/switch off the nearest suspect fixture if
  safely reachable; if it's hardwired or the source is a breaker,
  switch off at the panel and get an electrician. Do not keep using
  the fixture because "it still works."

### 2.3 Sewage BACKUP (odor + water)
- Odor alone → normal engine. But odor + water appearing at the
  lowest fixture (floor drain, shower) = stop: don't run water,
  don't flush; every gallon adds to what comes back. Call plumber;
  city-side if it's street main (free in many municipalities).
- Check the cleanout: standing water in the cleanout = blockage
  downstream (your side vs city side determined by location).

### 2.4 Dead animal — when it's actually urgent
- Almost always a 1-2 week nuisance, not an emergency. BUT: a large
  animal (raccoon/opossum) in a chimney or crawlspace, or any animal
  in a shared wall near sleeping areas, warrants removal service —
  flies and liquids follow day 4-8. Bulk of cases (mice in wall
  voids): wait out the desiccation clock, seal entry.

## 3. Localization Protocol (no tools)

Order = cheapest, most discriminating test first.

1. **Sniff-map the gradient.** Stand in the strongest room. Smell at
   standard heights: ankle, waist, ceiling. Sewage gases are heavier
   → strongest low. Electrical/fish strongest AT the fixture. Musty
   strongest at the wall with moisture. Write the map down.
2. **Fixture elimination.** Bathroom: run each tap 30 s, flush, then
   re-sniff at 10 min. Kitchen: disposal (ice + citrus flush), run
   dishwasher
   empty cycle if linked to disposal. Laundry: pull gasket
   fold, sniff interior drum seal.
3. **Dry-trap pour test.** Any fixture unused for weeks (floor
   drains, guest bath, basement shower): pour 2 L water. If smell
   fades within minutes → trap was dry. Add 1 tbsp mineral oil to
   slow next evaporation.
4. **Appliance isolation.** Smell only when X runs → X's drain,
   filter, or heat path. Dishwasher→disposal hose; dryer → lint path
   + vent hood; furnace → filter + blower motor.
5. **Wall/void sniffing.** Outlet and switch boxes on exterior walls
   share wall cavities — sniff AT them (not the plate). Petrol/
   chemical smells at outlets = a spill wicked into the cavity, or
   bigger problems. Musty at ONE box = the cavity behind it.
6. **Weather correlation.** After-rain patterns split: septic/
   sewer odor worse in rain (saturated drain field or vent
   turbulence); musty worse in rain (moisture path); neither →
   interior source.

## 4. Kill Protocols (source → treatment)

### 4.1 Dry P-trap
Refill with water; cap evaporation with mineral/cooking oil (1 tbsp).
Floor drains in server rooms/workshops: check monthly in winter
(heating dries traps fast). Aromatic "trap seal" products exist but
oil is cheaper and doesn't perfume the diagnosis.

### 4.2 Garbage disposal film
1. Ice cubes + citrus peels to scrape; 2. baking soda + vinegar
foam 15 min; 3. if the rubber splash guard lifts out, wash it —
that underside is the #1 disposal smell site. Enzymatic cleaner
weekly if recurring.

### 4.3 Pet urine in carpet pad
Surface shampooing fails because the source is the PAD and
subfloor. Enzymatic cleaner in volume (saturate, not mist), cover
with plastic 12-24 h so enzymes stay wet and working, extract.
Blacklight mapping at night: salts fluoresce. Sealed subfloor
(shellac-based blocker) if repeated failures — odors re-emit with
humidity forever otherwise.

### 4.4 Mold decision line
- **DIY line:** ≤ 1 m² (10 ft²) patch, hard surfaces, no one
  immunocompromised/infant/asthmatic in the home → surface protocol.
- **Professional:** > 1 m², inside walls/HVAC, musty smell with no
  visible patch, health symptoms, or it returns after cleaning.
- **Surface protocol:** fix the moisture first (or it regrows),
  HEPA-vacuum, detergent wash (NOT bleach-only — see pitfalls),
  dry 48 h, HEPA filter the room air during/after.
- Bleach on porous materials kills surface, leaves roots; borax or
  detergent-based cleaners + drying beat bleach on drywall.

### 4.5 Dead animal in wall
- Timeline: smell peaks day 3-5, insects/flies day 4-8, substantially
  gone by day 10-14 (mouse/rat scale). Large animal: 2-4 weeks.
- What helps: odor-absorbing gel (activated carbon) in the room,
  sealing electrical-box holes that connect rooms to the void (slows
  spread), ventilation of the affected room.
- What doesn't: fragrance plug-ins (mask only), cutting the wall on
  day 1 (usually can't find it, and smell is temporary).
- Cutting the wall is justified when: multi-week smell without
  decline, liquids staining the wall, fly cycles repeating (>2
  generations = larger animal or wet void).

### 4.6 HVAC-origin smells
- Filter first — dated the sticker. Dusty/burnt-dust on first heat
  of season = normal burnt-off dust; persistent = duct cleaning
  evaluation or blower motor. Dirty sock syndrome (sour, coil-born)
  = evaporator coil cleaning.
- Concrete/damp basement air through return leaks: seal return-side
  duct leaks in basement/crawl spaces.

### 4.7 Off-gassing (paint, furniture, mattresses)
Source removal or wrap-and-ventilate; heat accelerates emission
(short "bake" with windows open cycles VOCs out faster). VOCs
concentrate indoors in winter; air-exchange beats charcoal bags at
room scale (bags work in enclosed closets/cars).

## 5. Timing → Cause Cheat Table

| Pattern | Likely family |
|---|---|
| Mornings only | dry traps (evaporated overnight is rare; more often after days unused); morning-flush surging vent issues |
| After vacation | dry traps; fridge/freezer failures; pet accidents |
| After rain | sewer/septic vent turbulence; moisture→mold activation |
| When dishwasher runs | drain air gap / disposal link hose |
| When furnace runs | filter, blower, duct dust, or return leaks |
| When hot outside | off-gassing; trash rooms; crawl-space soil gases |
| Sudden onset, no change | dead animal; spilled product; neighbor activity |
| Worsening over weeks | mold growth; hidden leak; electrical (fish) — check now |

## 6. Evidence for Landlord/Service Calls

The log output (dates, intensity, weather, fixture states) exists to
be exported: recurring sewage odor with confirmed wet cleanout is a
habitability issue in most jurisdictions; the printed episode list +
your pour-test results turn "there's a smell" into a documented
defect notice. Keep entries factual: date, time, intensity 1-5,
location, trigger, what you tested, result.
