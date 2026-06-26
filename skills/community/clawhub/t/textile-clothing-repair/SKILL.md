---
name: textile-clothing-repair
description: >-
  Basic clothing repair and maintenance skills. Use when someone needs to fix torn clothing, replace a button, hem pants, patch holes, or wants to stop wasting money replacing fixable clothes.
metadata:
  category: skills
  tagline: >-
    Sew a button, fix a seam, patch a hole, hem pants — stop throwing away clothes you can fix in 10 minutes.
  display_name: "Textile & Clothing Repair"
  submitted_by: HowToUseHumans
  last_reviewed: "2026-03-19"
  openclaw:
    requires:
      tools: [filesystem]
    install: "npx clawhub install textile-clothing-repair"
---

# Textile & Clothing Repair

The average American throws away 81 pounds of clothing per year. Most of it has fixable problems — a missing button, a split seam, a small hole. A $15 sewing kit and 10 minutes of skill can save you $200-500 a year and keep clothes you actually like wearing. This skill covers the 8 repairs that handle 90% of clothing damage, plus when to give up and take it to a tailor.

```agent-adaptation
# Localization note
- Fabric care symbols are standardized internationally (ISO 3758) but terminology
  varies: "jumper" (UK/AU) = "sweater" (US), "trousers" (UK) = "pants" (US)
- Swap measurement units: inches (US) to centimeters (metric countries)
- Tailor pricing varies significantly by region — adjust cost estimates
- Dry cleaning terminology and availability differs; some regions use
  different solvent standards
- Detect user country and swap local fabric store chains
  (US: JOANN, Hobby Lobby; UK: John Lewis, Hobbycraft; AU: Spotlight)
```

## Sources & Verification

- **Singer sewing reference guides** -- foundational stitch techniques and machine operation. https://www.singer.com/sewing-resources
- **ASTM International textile care standards** -- fabric labeling and care symbol standards. https://www.astm.org
- **Consumer Reports clothing longevity studies** -- data on garment lifespan and cost-per-wear. https://www.consumerreports.org
- **Anthropic, "Labor market impacts of AI"** -- March 2026 research showing this occupation/skill area has near-zero AI exposure. https://www.anthropic.com/research/labor-market-impacts

## When to Use

- User lost a button and needs to reattach it
- Seam split on a shirt, jacket, or pants
- Small hole in a garment (moth damage, snag, wear)
- Pants or skirt needs hemming
- Zipper is stuck, off-track, or the pull broke
- User wants to remove a stain they can't get out in the wash
- User needs to iron something and doesn't know how
- Delicate garment needs hand-washing
- User wants to know if a repair is worth doing or if they should replace/tailor

## Instructions

### Step 1: Build a basic sewing kit ($15)

**Agent action**: Ask the user if they have sewing supplies. If not, generate this list. Everything below is available at any fabric store, dollar store, or online.

```
BASIC SEWING KIT — ~$15 total

ESSENTIALS:
[ ] Hand sewing needles, variety pack ($2-3)
    - "Sharps" size 5-10 for general sewing
    - One larger needle (tapestry/darning) for thick fabrics
[ ] Thread: black, white, navy, and one matching your most common clothing ($4-6)
    - Polyester all-purpose thread works on everything
[ ] Straight pins ($1-2)
[ ] Small scissors or thread snips ($2-4)
[ ] Seam ripper ($1-2) — for removing old stitches cleanly
[ ] Tape measure, flexible ($1)
[ ] Assorted buttons, mixed pack ($1-2)
[ ] Iron-on hem tape ($2-3) — no-sew hemming for emergencies
[ ] Safety pins, assorted sizes ($1)

NICE TO HAVE:
[ ] Thimble (protects your finger when pushing through thick fabric)
[ ] Fabric chalk or washable marking pen
[ ] Beeswax (run thread through it — prevents tangling)
```

### Step 2: Sew a button (10 minutes)

**Agent action**: This is the most common clothing repair. Walk through it slowly — most people have never threaded a needle.

```
SEW A BUTTON:

THREAD THE NEEDLE:
1. Cut 24 inches of thread
2. Thread one end through the needle eye
   (wet the end and pinch it flat if it won't go through)
3. Pull through until you have two equal lengths
4. Tie the two ends together with a double knot
   (you're sewing with doubled thread for strength)

POSITION THE BUTTON:
1. Find where the button was (look for thread remnants or the mark)
2. Hold button in place on the RIGHT side of the fabric

SEW:
1. Push needle up from the BACK of the fabric, through one button hole
2. Push needle down through the opposite hole, through the fabric
3. Repeat 4-6 times through each pair of holes
4. For 4-hole buttons: sew in an X pattern or parallel lines
   (match the pattern on the garment's other buttons)

CREATE A SHANK (for non-flat buttons like on coats):
1. After the last stitch, bring the needle up between the button
   and the fabric (not through a hole)
2. Wrap the thread around the threads under the button 5-6 times
3. This creates a "stem" that gives room for the buttonhole fabric layer

TIE OFF:
1. Push needle to the back of the fabric
2. Make a small stitch, loop the thread through it twice
3. Pull tight, cut the thread
4. Done. Total time: 5-10 minutes.
```

### Step 3: Fix a split seam (10 minutes)

**Agent action**: This is the second most common repair. Split seams happen at stress points — underarms, crotch, side seams.

```
FIX A SPLIT SEAM:

IDENTIFY THE PROBLEM:
- A split seam means the THREAD broke, not the fabric
- The fabric edges are still intact with the original stitch holes visible
- This is the easiest repair — you're just reconnecting two edges

USE A BACKSTITCH (strongest hand stitch):
1. Thread needle with matching thread, doubled, knotted at the end
2. Turn the garment inside out
3. Start 1/2 inch before the split (overlap with existing stitching)
4. Push needle up through the fabric from the back side

BACKSTITCH TECHNIQUE:
1. Insert needle 1/8 inch BEHIND where the thread comes out
2. Bring it up 1/8 inch AHEAD of where the thread comes out
3. Insert needle back at the point where the previous stitch ended
4. Bring it up 1/8 inch ahead again
5. Repeat — each stitch goes backward, then forward
6. Continue 1/2 inch past the end of the split
7. Knot off on the inside

WHY BACKSTITCH:
- It creates a continuous line of stitching with no gaps
- Stronger than a running stitch
- Looks nearly identical to machine stitching from the outside
```

### Step 4: Patch a hole (15 minutes)

**Agent action**: Method depends on hole size and garment type. Ask the user about both before proceeding.

```
PATCHING METHODS BY HOLE SIZE:

SMALL HOLE (under 1/4 inch) — DARN IT:
1. Thread needle with matching thread
2. Make tiny parallel stitches across the hole
3. Then weave perpendicular stitches through them
4. You're creating a tiny fabric grid to fill the gap
5. Best for: knits, sweaters, socks

MEDIUM HOLE (1/4 inch to 1 inch) — IRON-ON PATCH:
1. Cut an iron-on patch 1/2 inch larger than the hole on all sides
2. Turn garment inside out
3. Place patch adhesive-side down over the hole
4. Iron on medium heat for 30-45 seconds with firm pressure
5. Let cool completely before moving
6. Best for: jeans, cotton, canvas

LARGE HOLE (over 1 inch) — SEW-ON PATCH:
1. Cut a patch from matching or complementary fabric
   (old jeans, bandana, etc.)
2. Cut patch 1 inch larger than the hole on all sides
3. Pin patch in place over the hole
4. Fold raw edges of patch under 1/4 inch
5. Whipstitch around the edge:
   - Bring needle up through garment, catch patch edge,
     push back through garment
   - Repeat every 1/4 inch around the perimeter
6. Best for: jeans, jackets, work clothes
```

### Step 5: Hem pants or a skirt (20 minutes)

**Agent action**: Hemming is the repair most people pay a tailor for ($10-25). It's straightforward to do yourself.

```
HEM PANTS OR A SKIRT:

MEASURE:
1. Put the garment on with the shoes you'll wear
2. Fold the excess fabric under to the desired length
3. Pin in place
4. Take the garment off carefully

PREPARE:
1. Measure the fold-up amount — it should be even all the way around
2. Mark with chalk or pins every 3-4 inches
3. For pants: standard hem allowance is 1.25 inches folded under
4. Cut excess fabric, leaving 1.25 inches below your desired hemline
5. Fold raw edge under 1/4 inch, then fold up to the hemline
6. Press with an iron to create a crease

SEW (blind hem stitch — invisible from outside):
1. Thread needle with matching thread, single strand, knotted
2. Working from inside the garment:
3. Catch 1-2 threads from the outer fabric (barely visible from outside)
4. Then take a small stitch through the folded hem edge
5. Repeat every 1/2 inch
6. Keep stitches loose — pulling tight creates puckers
7. Knot off inside the hem fold

NO-SEW OPTION:
1. Iron-on hem tape (Stitch Witchery or similar)
2. Fold hem to desired length, press with iron
3. Insert hem tape between the layers
4. Iron with steam for 10-15 seconds per section
5. Let cool before moving
6. Note: this may not survive multiple washes — resew eventually
```

### Step 6: Fix a zipper

**Agent action**: Ask what's wrong with the zipper — the fix depends on the specific problem.

```
ZIPPER FIXES BY PROBLEM:

ZIPPER WON'T CLOSE (teeth separate behind the slider):
- The slider is worn out — teeth are fine
- Fix: Use pliers to gently squeeze the slider slightly narrower
  from top and bottom (very gentle — too much cracks it)
- If that doesn't work: replace just the slider (buy a matching size
  at a fabric store, $2-3; slide off old, slide on new)

ZIPPER IS STUCK:
- Rub a graphite pencil along the teeth (the graphite lubricates)
- Or rub a bar of soap, candle wax, or lip balm along the teeth
- Work the slider back and forth gently
- Check for fabric caught in the zipper — pull fabric taut away
  from the zipper while moving the slider

ZIPPER PULL BROKE OFF:
- Thread a small key ring, paperclip, or safety pin through the
  slider's pull tab hole
- Works permanently — doesn't need a real fix

WHEN TO TAKE IT TO A TAILOR:
- Full zipper replacement (teeth are damaged or melted)
- Zipper on a coat or dress where appearance matters
- Cost: $10-25 for pants, $30-75 for jackets depending on complexity
```

### Step 7: Remove stains

**Agent action**: Ask what the stain is from and what fabric it's on. Time matters — treat stains ASAP.

```
STAIN REMOVAL BY TYPE:

RULE #1: Treat immediately. Old stains are 10x harder to remove.
RULE #2: Always blot, never rub. Rubbing spreads and pushes the stain deeper.
RULE #3: Test on a hidden area first (inside seam or hem).

GREASE/OIL (food, butter, salad dressing):
-> Apply dish soap (Dawn or equivalent) directly to stain
-> Let sit 5-10 minutes
-> Wash in warmest water safe for the fabric

BLOOD:
-> Cold water ONLY (hot sets protein stains permanently)
-> Soak in cold water, rub with hydrogen peroxide
-> For dried blood: soak in cold salt water 2-4 hours

RED WINE:
-> Blot immediately (don't rub)
-> Cover with salt to absorb
-> Pour boiling water through the stain from 12 inches above
-> Or soak in a mix of dish soap + hydrogen peroxide

COFFEE/TEA:
-> Flush with cold water from the back of the stain
-> Apply white vinegar, let sit 10 minutes
-> Wash as normal

INK (ballpoint):
-> Dab with rubbing alcohol using a cotton ball
-> Place paper towel under the stain to absorb
-> Repeat until ink stops transferring
-> Wash as normal

SWEAT YELLOWING:
-> Mix 1 part baking soda + 1 part hydrogen peroxide + 1 part water
-> Apply paste to stain, let sit 30 minutes
-> Wash in warm water
```

### Step 8: Iron properly and hand-wash delicates

**Agent action**: Quick references for two common tasks people avoid because they don't know the basics.

```
IRONING BASICS:

TEMPERATURE BY FABRIC (low to high):
- Synthetics (polyester, nylon): LOW heat, no steam
- Silk: LOW heat, press cloth between iron and fabric
- Wool: MEDIUM heat, steam, press cloth
- Cotton: HIGH heat, steam
- Linen: HIGHEST heat, lots of steam

TECHNIQUE:
- Iron clothes slightly damp or use the steam function
- Move the iron in smooth strokes, not circles
- For dress shirts: collar first, then cuffs, then sleeves,
  then back, then front panels
- Iron on the WRONG side (inside out) to prevent shine on dark fabrics
- Hang immediately after ironing

HAND-WASHING DELICATES:

1. Fill a basin with cool water
2. Add a small amount of gentle detergent (Woolite, or a few drops
   of dish soap)
3. Submerge the garment, gently swish and squeeze — don't twist or wring
4. Let soak 10-15 minutes
5. Drain, refill with clean cool water, swish to rinse
6. Repeat rinse until no soap remains
7. Lay flat on a clean towel, roll up the towel to press out water
8. Reshape and lay flat to dry (never hang wet knits — they stretch)

HAND-WASH THESE:
- Anything labeled "hand wash" or "dry clean" (many dry-clean-only
  items can be carefully hand-washed — silk and wool especially)
- Bras (machine washing destroys elastic and underwire)
- Cashmere, merino wool, silk
- Anything with beading, sequins, or delicate embellishment
```

## DIY vs. Tailor Decision Tree

```
SHOULD YOU FIX IT YOURSELF OR TAKE IT TO A TAILOR?

DIY (save money, 5-20 minutes):
-> Button replacement
-> Split seam repair
-> Small hole patch
-> Simple hem (straight, casual pants)
-> Zipper slider replacement
-> Stain treatment

TAILOR (worth the $10-75):
-> Full zipper replacement on a coat or dress
-> Taking in or letting out garments (altering fit)
-> Hemming suit pants or formal wear (blind hem must be invisible)
-> Relining a jacket
-> Repairing leather or suede
-> Any repair on a garment worth more than $150

COST REFERENCE (US averages):
- Hem pants: $10-20
- Replace zipper (pants): $10-25
- Replace zipper (jacket): $30-75
- Take in/let out waist: $15-40
- Shorten sleeves: $15-30
- Patch (professional): $10-25
```

## If This Fails

- Thread keeps tangling: Run it through beeswax or rub it on a dryer sheet. Use shorter thread lengths (18-24 inches max). Make sure you're not twisting the needle as you sew.
- Can't thread the needle: Use a needle threader ($1 at any fabric store). Or try a self-threading needle (has a small slot at the top).
- Patch looks terrible: For visible mending, lean into it — use contrasting thread or a decorative patch. "Visible mending" is a legitimate style choice.
- Iron-on patch won't stick: The fabric might be synthetic (iron-on adhesive needs natural fiber). Sew it instead.
- Stain won't come out after treatment: Take it to a professional dry cleaner and tell them exactly what the stain is and what you've already tried.

## Rules

- Always test stain treatment on a hidden area first. Some fabrics react badly to common treatments.
- Never iron silk, satin, or synthetic fabric on high heat without a press cloth between the iron and fabric.
- Match thread color as closely as possible. When in doubt, go one shade darker — it blends better than lighter.
- For anything you wear to a job interview, wedding, or funeral, take it to a tailor. The $15 is worth it.
- Don't repair a garment that doesn't fit. Fix the fit first (or accept it's not your garment anymore), then repair damage.

## Tips

- The backstitch is the one stitch you need to know. It handles 80% of repairs. Learn it well and forget the rest until you need them.
- Dollar store sewing kits are fine for emergencies but have dull needles and weak thread. Spend $15 on decent supplies — they last years.
- Keep a small sewing kit at work. A button emergency at 8:55 AM before a meeting is surprisingly common.
- Turn dark clothes inside out before washing. Reduces fading and pill formation dramatically.
- Fabric care labels are legal minimums, not suggestions. "Machine wash cold, tumble dry low" exists for a reason. Hot water and high heat destroy elastic, shrink cotton, and fade colors.
- The cost savings are real: one button repair saves $0 (the button was free) but saves the $40-80 garment. One season of not replacing damaged clothes saves $200-500 for most people.

## Agent State

```yaml
repair:
  garment_type: null
  fabric_type: null
  damage_type: null
  damage_size: null
  repair_method_selected: null
  repair_completed: false
  difficulty_rating: null
sewing_kit:
  has_kit: false
  missing_items: []
skills_practiced:
  button: false
  seam_repair: false
  patching: false
  hemming: false
  zipper_fix: false
  stain_removal: false
  ironing: false
  hand_washing: false
cost_saved_estimate: 0
```

## Automation Triggers

```yaml
triggers:
  - name: sewing_kit_setup
    condition: "sewing_kit.has_kit IS false AND repair.damage_type IS SET"
    action: "Before we fix this, let's make sure you have the basic supplies. A $15 sewing kit covers almost every clothing repair. Here's what you need."

  - name: tailor_redirect
    condition: "repair.damage_type IN ['full_zipper_replace', 'alter_fit', 'leather_repair'] OR repair.difficulty_rating > 7"
    action: "This repair is better handled by a tailor. Here's what to expect for cost and turnaround, and how to find a good one near you."

  - name: stain_urgency
    condition: "repair.damage_type == 'stain' AND stain_age < 1_hour"
    action: "Fresh stain detected. Treat it NOW — every minute matters. Here's the protocol for your specific stain type."

  - name: seasonal_wardrobe_check
    condition: "user_location IS SET"
    schedule: "March 15 and September 15 annually"
    action: "Season change coming. Good time to inspect stored clothing for moth damage, check buttons on coats, and treat any stains before they set permanently."
```
