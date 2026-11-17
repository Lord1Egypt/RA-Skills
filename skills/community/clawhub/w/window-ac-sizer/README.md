# Window AC Sizer

The most common window air conditioner mistake is not undersizing — it's **oversizing**. A too-big unit hits setpoint in minutes, shuts off, and never runs long enough to pull water off the coil: the room ends up cold, clammy, and mold-prone, with a compressor short-cycling itself to death. Store folklore ("bedrooms need 8,000 BTU") pushes people exactly there.

This skill computes a transparent Manual-J-flavored room load — area × 20 BTU/sqft, adjusted line-by-line for ceiling height, sun exposure, insulation, climate, occupants, and kitchen load — then recommends a BTU band with a hard **+15% oversize ceiling**, because latent removal (dehumidification) needs sustained coil runtime, not brute force.

## What it does
- **`size`** — full load stack printed factor-by-factor (argue with any line), nearest shelf size with inverter-modulation advice when the smallest market size is >1.5× your load
- **`check`** — is your *existing* unit the reason the room is cold-but-clammy? Ratio verdicts: OVERSIZED / MILDLY OVERSIZED / RIGHT-SIZED / UNDERSIZED with fixes for each
- **`cost`** — CEER season-cost math at YOUR kWh price and hours: 10k BTU @ CEER 15 vs 11 is a $40/season difference; find your payback
- Purchase gates: 115V vs 230V circuits, window-type fit, single-hose portable SACC label lie (a "14,000 BTU" single-hose is often ~8,000 real), noise placement, window heat-pump option

## Real problem it solves
Millions of window ACs are bought by room-type folklore, then run a decade cold and damp, humming on/off every 4 minutes. A 5-minute honest load estimate picks the right shelf size, names the clamminess mechanism when the unit is already wrong, and prices the efficiency upgrade honestly.

## Quick start
```bash
python3 scripts/window_ac_sizer.py size --length 18 --width 14 --ceiling 9 \
    --sun west --insulation poor --occupants 3 --kitchen yes
# -> CALCULATED LOAD ~12,299 BTU/h -> BUY 12,000 (within +15% doctrine)

python3 scripts/window_ac_sizer.py check --length 12 --width 14 --ceiling 8 \
    --sun shaded --unit-btu 12000
# -> ratio 3.97: OVERSIZED — classic cold-but-clammy room
```

## Contents
- `SKILL.md` — load model, oversize doctrine, purchase gates, pitfalls
- `references/load-model-and-purchase-physics.md` — Manual J background, latent/sensible physics, short-cycle signatures, SACC, electrical gates, CEER math
- `scripts/window_ac_sizer.py` — stdlib-only CLI (size / check / cost)

## License
MIT
