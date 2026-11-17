# Slow Cooker Converter

**"Can I just throw this in the Crock-Pot?" — now with an answer
that isn't curdled.**

Converting recipes between stovetop, oven, slow cooker and Instant
Pot fails in predictable ways: milk breaks after hour two, pasta
turns to paste, wine never cooks off in a sealed pot, the sauce
stays thin because a slow cooker cannot reduce. This tool rewrites
a recipe for the target appliance with the rules that actually
matter: time mappings grounded in collagen-to-gelatin kinetics,
liquid adjustments for each appliance's evaporation class, capacity
fill checks, and an INSERT-AT timeline for every problem ingredient
it finds in your text.

## What it does

- **convert** — paste a recipe; get rewritten cook times, liquid
  adjustment (−25% slow, −50% pressure), and an INSERT-AT timeline
  for dairy, pasta, tender herbs, thickeners, alcohol, rice, fast
  veg, and delicate fish
- **time** — 15 directed mappings across 7 appliance modes, with
  natural-release guidance for braises
- **capacity** — servings × dish class vs cooker liters: the
  half-to-two-thirds fill rule with scorch/boil-over verdicts
- **ingredients** — the full triage table per target mode, including
  the food-safety traps (frozen meat into slow cooker, kidney-bean
  toxin, "warm" is not a cook)

## Quick start

```bash
python3 scripts/slow_converter.py convert --from oven --to slow-low \
    --recipe "Beef stew: brown beef 10 min; oven 325F 2.5h; 1 cup red wine, 2 tbsp flour"
python3 scripts/slow_converter.py time --from oven --minutes 150 --to pressure
python3 scripts/slow_converter.py capacity --servings 6 --cooker 6.5
```

Stdlib-only Python 3, offline. No-mapping zone documented: baked
goods, custards, candy — a slow cooker is a braising machine, not
an oven.

## License

MIT
