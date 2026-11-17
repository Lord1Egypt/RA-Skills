# Supplement Stack Checker

**Interaction flags, UL dose checks, and a timed schedule for multi-supplement routines.**

## The problem

Supplement stacks accrete from blog posts and well-meaning friends: a
multivitamin, magnesium for sleep, zinc since COVID, iron "for energy", fish
oil, and someone's St. John's Wort. Nobody checks that:

- **Calcium blocks iron absorption by up to 50%** when taken together,
- **Chronic zinc above 40 mg/day depletes copper** (anemia, neuropathy — months later),
- The multivitamin already supplied zinc/B6/vitamin A, so adding dedicated
  products **silently doubles past the Tolerable Upper Intake Level**,
- **St. John's Wort is a potent drug-clearing inducer** (contraceptives,
  statins, cyclosporine) and stacks dangerously with serotonergic agents.

Surveys consistently show supplement users don't report all products to
their doctor, and combination products make everyone lose track of totals.

## What it does

`scripts/stack_check.py` (stdlib-only, offline):

1. **Interaction matrix** — ~25 pair rules: BLOCK (separate 2+ h: calcium↔
   iron, zinc↔iron), ENHANCE (combine: vitamin C+iron, D+calcium), DEPLETE
   (chronic: zinc→copper), DANGER (prescriber talk: SJW+SSRIs, anticoagulant
   stacking, red yeast rice+statins).
2. **UL check** — daily totals summed across ALL products vs adult ULs
   (vitamin A 3000 µg, B6 100 mg, zinc 40 mg, selenium 400 µg, iron 45 mg,
   D 100 µg...). Handles IU→µg conversions.
3. **Duplicate detection** — the same ingredient arriving via 3 products.
4. **Scheduler** — a breakfast/lunch/dinner/evening plan applying the 2-hour
   rule: iron AM with vitamin C away from coffee, calcium at lunch, zinc at
   dinner away from iron, fat-solubles with the largest meal, magnesium/
   melatonin at night, stimulants before 14:00.

## Example

```bash
$ python3 scripts/stack_check.py --demo
```
flags 4 issues in a realistic 6-product stack (zinc 38 mg across two
products near UL + copper depletion, calcium-iron block, SJW+5-HTP danger
pair, iron scheduled away from calcium) and prints a corrected timing plan.

Your own stack:
```bash
python3 scripts/stack_check.py "Multi|zinc:15|vitamin A:600u" \
  "Iron+VitC|iron:18|vitamin C:90" "CalMag|calcium:500|magnesium:250" \
  --schedule
```

## Who needs this

Roughly half of adults take at least one supplement; millions take 3+. The
check it performs takes a pharmacist 20 minutes and this script 2 seconds —
before you buy, before you stack, and before you assume "natural = safe".

## Boundary

Educational instrument built from public nutrition references (NIH ODS
fact-sheet level). Not medical advice; pregnancy/pediatric thresholds differ;
drug interactions beyond the highlighted classes need a pharmacist.

## License

MIT © 2026 Denis Voronin
