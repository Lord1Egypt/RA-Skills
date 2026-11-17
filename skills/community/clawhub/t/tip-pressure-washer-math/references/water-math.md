# Water Math — Pressure Washing Reference

The physics and shop doctrine behind `tip_math.py`.

## Cleaning Units: the honest metric

Cleaning power ≈ PSI × GPM ("cleaning units", CU). The industry
band table:

| CU range | Class |
|---|---|
| < 2,000 | light electric / toy |
| 2,000-3,000 | residential electric |
| 3,000-5,000 | residential gas / pro-electric |
| 5,000-8,000 | prosumer / light commercial |
| > 8,000 | commercial skid |

Rule of thumb: **1 GPM cuts rinse time more than +1000 PSI.** Flow is
time (how fast you can flood and rinse a area); pressure is impact
(whether you can break the bond of the soil). For almost all homeowner
soils, 2500-3200 PSI with 2.5-4 GPM beats 4000 PSI with 1.5 GPM.

## Orifice Sizing

Nozzle size numbers (2.0, 2.5, 3.0, ... 8.0) are the flow in GPM at
4000 PSI. At any other pressure the same hole passes:

```
flow = size × sqrt(PSI / 4000)
```

Examples at 3000 PSI (factor 0.866): a 3.0 tip passes 2.6 GPM; a 4.0
passes 3.46 GPM.

**Matching the pump.** The pump's rated GPM is what it can deliver;
if the orifice demands more, pressure sags to whatever the pump can
push through the hole and the unloader cycles (chatter) — which is
both ineffective and hard on the machine. Demand ratio above ~1.05×
rated GPM = size down. If the orifice demands far less than rated,
pressure rises toward the pump's max (that's how "3500 PSI" machines
make rated pressure with a small tip).

**Turbo/rotary nozzles** spin a 0°-equivalent jet in a circle. They
hit like a 0° but cover like a 25°, at the cost of ~20-25% effective
pressure derate and higher flow demand. When adding a turbo, step
DOWN one orifice size class and check the demand ratio again.

## Fan Angles (quick-connect color code)

| Color | Angle | Use |
|---|---|---|
| Red | 0° | stubborn spot stains only; pencil jet damages surfaces |
| Yellow | 15° | tough surfaces, heavy soil, paint prep |
| Green | 25° | general purpose: concrete, brick |
| White | 40° | fragile/soft: wood, vinyl, autos |
| Black | 65° + low pressure | soap/detergent application nozzle |

## Chemical Dilution

Two injection worlds:

- **Downstream injection** (after the pump): the venturi on the outlet
  side draws concentrate at roughly 10:1. Your tank mix should be what
  you want ON the surface × 10 — i.e., to apply a 1:30 final dilution
  of house wash, tank mix at ~1:3. Harsh chemistry never touches the
  pump. Long hose runs reduce draw ratio; keep runs under ~50 m.
- **Upstream / through-pump**: only pump-safe detergents. Stronger
  application but you're pumping the chemical.

Ratios per job class (tank concentrate:water for downstream setups
shown as final-on-surface targets):

- Concrete pre-treat: alkaline degreaser, final 1:5-1:10, dwell 5-10
  min, keep wet, rinse before it dries.
- House/vinyl soft wash: sodium-hypochlorite-based mix, final 1:9-1:12
  on siding, low pressure (black soap nozzle), apply bottom-up, rinse
  top-down.
- Car: pH-neutral foam wash 1:9-1:20 through a foam cannon, then
  contact wash. High pH dulls paint over time.
- Wood deck: wood cleaner (sodium percarbonate) ~1:4-1:8, gentle
  pressure with the grain, neutralize/brighten after.

Bleach note: never let bleach-based mixes dry on surfaces or plants;
rinse vegetation before and after, and never run them through the
pump.

## Surface Ceilings

| Surface | Max working PSI | Tip | Standoff | Notes |
|---|---|---|---|---|
| Concrete, unreinforced finish | 2500-4000 | 25-40°, turbo for stains | 4-8 in stains, 12 in rinse | keep fan moving; never 0° |
| Pavers with joint sand | 2500-3000 | 25° | 8-12 in | expect to re-sand joints after |
| Wood deck (softwood) | 1200-1500 | 25-40°, with grain | 12-18 in | test a hidden board; too close furs the grain |
| Composite decking | 1200-1500 | 40° | 12-18 in | follow maker; some forbid pressure entirely |
| Vinyl siding | 1300-1600 | 40° soap nozzle | 18+ in | bottom-up apply, top-down rinse; avoid forcing water behind laps |
| Painted walls | < 1200 | 40° | 24 in | test an inconspicuous patch |
| Automobile | 1000-1900 | 40° / foam | 12-24 in | never 0/15°; never closer than a hand-width |
| Windows | < 1000 | 40° | 24+ in | avoid sealing edges; check screens first |

## Safety Notes

- Never spray toward people, pets, or power lines; the jet can inject
  water through skin (high-pressure injection injury = ER, tell them
  the fluid).
- Goggles, always; the rebound carries grit.
- Electric washers: plug into GFCI; use extension cords rated for the
  draw or none at all.
- Ladders + recoil of a pressure lance = falls. Use extension wands
  from the ground for high work.
