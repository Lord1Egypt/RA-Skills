---
name: soil-water-management
description: >-
  Soil science, composting, and water management for food production. Use when someone wants to improve their garden soil, start composting, set up irrigation, harvest rainwater, or scale up food growing beyond containers.
metadata:
  category: skills
  tagline: >-
    Test your soil, build fertility with compost, harvest rainwater, and set up drip irrigation -- the foundation under every food-growing skill.
  display_name: "Soil & Water Management"
  submitted_by: HowToUseHumans
  last_reviewed: "2026-03-19"
  openclaw:
    requires:
      tools: [filesystem]
    install: "npx clawhub install soil-water-management"
---

# Soil & Water Management

This is the foundation under the grow-food-anywhere skill. You can know everything about planting and spacing and still fail if your soil is dead or your water management is wrong. Soil is not dirt -- it's a living system with billions of organisms in a handful, and those organisms do most of the work of feeding your plants. Water management means getting the right amount of water to the right place at the right time without wasting it. Both of these are learnable, and both reward paying attention more than spending money. A $10 soil test tells you more than $200 worth of random amendments.

```agent-adaptation
# Localization note -- soil science and water management principles are universal.
# Products, regulations, and climate factors vary.
# Agent must follow these rules when working with non-US users:
- Soil testing, composting, and irrigation principles are universal.
- Soil testing services:
  US: Cooperative Extension soil testing labs (every state has one, $10-25)
  UK: RHS soil testing, independent labs
  AU: State DPI soil testing services
  EU: varies by country -- search "soil testing laboratory" + country
- Rainwater harvesting legality:
  US: varies by state (legal in most, restricted in CO and some western states)
  UK: legal and encouraged
  AU: legal, encouraged, rebates available in some states
  EU: varies by country, generally legal
  Agent MUST check local regulations before advising on rainwater collection.
- Composting regulations:
  Some municipalities regulate or provide composting programs.
  UK: many councils provide subsidized composting bins.
  Agent should check local programs that may reduce cost.
- Measurement units:
  US: inches, feet, gallons, Fahrenheit
  UK/AU/EU: centimeters, meters, liters, Celsius
  Agent must convert when working with non-US users.
- Climate zones:
  US: USDA Hardiness Zones
  UK: RHS Hardiness Ratings
  AU: Climate zones per state
  EU: USDA-equivalent zones exist for most countries
  Composting rates, irrigation needs, and growing seasons vary by zone.
```

## Sources & Verification

- **USDA Cooperative Extension soil testing programs** -- university-based soil testing available in every US state, the most cost-effective way to know what your soil needs. [nifa.usda.gov/cooperative-extension-system](https://www.nifa.usda.gov/about-nifa/how-we-work/extension/cooperative-extension-system)
- **"Teaming with Microbes" by Jeff Lowenfels** -- the accessible reference on soil biology and how to feed the soil food web. Essential reading for anyone serious about growing food.
- **Master Gardener composting guides** -- Extension-based composting education. Available through state Master Gardener programs.
- **Irrigation Association efficiency data** -- research on irrigation system efficiency and water conservation. [irrigation.org](https://www.irrigation.org/)
- **American Rainwater Catchment Systems Association** -- standards and best practices for residential rainwater harvesting. [arcsa.org](https://www.arcsa.org/)

## When to Use

- User wants to improve garden soil but doesn't know where to start
- User is starting a compost pile or worm bin
- User needs to set up irrigation for a garden or food-growing area
- User wants to harvest rainwater for garden use
- User has poor soil (clay, sand, compacted) and needs to build fertility
- User is scaling up from containers to in-ground growing
- User is dealing with drainage problems on their property

## Instructions

### Step 1: Test Your Soil

**Agent action**: Before the user adds anything to their soil, determine what they have. A soil test eliminates guessing.

```
SOIL TESTING:

THE JAR TEST (free, do it yourself, takes 24 hours):
-> Fill a quart jar 1/3 with soil from your garden
-> Fill the rest with water, leaving an inch of air
-> Add a tablespoon of dish soap (breaks up clay particles)
-> Shake vigorously for 2 minutes
-> Set on a flat surface and don't touch for 24 hours
-> After 24 hours, you'll see layers:
   BOTTOM: sand (settles in minutes -- large, gritty particles)
   MIDDLE: silt (settles in hours -- fine, flour-like particles)
   TOP: clay (settles last -- may stay cloudy for days)
   FLOATING: organic matter
-> Ideal garden soil (loam): roughly equal parts sand, silt, and clay
-> Heavy clay: slow drainage, holds nutrients well, hard to work wet
-> Sandy: drains fast, loses nutrients quickly, easy to work
-> Now you know your soil texture and can amend accordingly

pH TESTING ($5-10 for strips, $10-15 for a probe or kit):
-> Most vegetables prefer pH 6.0-7.0 (slightly acidic to neutral)
-> Below 6.0: soil is too acidic. Add garden lime (calcium carbonate)
   per soil test recommendations.
-> Above 7.0: soil is too alkaline. Add elemental sulfur or peat moss
   per soil test recommendations.
-> Blueberries are the exception: they want 4.5-5.5 (very acidic)
-> pH affects nutrient availability. Plants can starve in nutrient-rich
   soil if the pH is wrong.

LAB SOIL TEST ($10-25 through your state Cooperative Extension):
-> The real test. Tells you exact pH, nutrient levels, organic matter
   percentage, and specific amendment recommendations.
-> How to take a sample: dig to 6 inches in 5-10 spots across your
   garden, mix the samples in a clean bucket, send 1-2 cups to the lab.
-> Results come back in 1-3 weeks with specific recommendations
   for what to add and how much.
-> Do this every 2-3 years or whenever you're starting a new bed.
-> This $15 test prevents hundreds of dollars in wrong amendments.
```

### Step 2: The Nutrient Big 3 (N-P-K)

**Agent action**: Explain macronutrients so the user can interpret their soil test and understand fertilizer labels.

```
NITROGEN, PHOSPHORUS, POTASSIUM (N-P-K):

Every fertilizer bag has three numbers: N-P-K (e.g., 10-10-10).
These are the percentages of each nutrient by weight.

NITROGEN (N) -- leaf and stem growth
-> Deficiency signs: yellow leaves starting from the bottom of the plant,
   stunted growth, pale green color overall
-> Sources: compost, manure (aged), blood meal, fish emulsion,
   cover crops (clover, peas, beans fix nitrogen from the air)
-> Too much: excessive leafy growth at the expense of fruit/flowers,
   soft growth that attracts pests

PHOSPHORUS (P) -- roots, flowers, fruit
-> Deficiency signs: purple/reddish tint to leaves (especially
   undersides), poor flowering, weak root system, slow growth
-> Sources: bone meal, rock phosphate, compost
-> Note: phosphorus doesn't move much in soil -- incorporate it
   into the root zone, don't just top-dress

POTASSIUM (K) -- overall plant health, disease resistance, water regulation
-> Deficiency signs: brown leaf edges (leaf scorch), weak stems,
   poor fruit quality
-> Sources: wood ash (also raises pH), greensand, kelp meal, compost

THE BEST ADVICE: Add compost. It contains all three nutrients plus
micronutrients plus organic matter plus beneficial microbes. If you
do only one thing for your soil, add compost.
```

### Step 3: Composting

**Agent action**: Help the user choose and start the composting method that fits their space, time, and lifestyle.

```
COMPOSTING METHODS:

METHOD 1: COLD PILE (lazy compost -- works, just slow)
-> Pile up yard waste and kitchen scraps in a corner
-> Walk away
-> In 6-12 months, the bottom of the pile is compost
-> Add material on top, harvest from the bottom
-> No turning, no monitoring, no effort
-> Downsides: slow, may attract pests if meat/dairy are added,
   doesn't kill weed seeds or pathogens

METHOD 2: HOT PILE (active compost -- faster, more effort)
-> Build a pile at least 3x3x3 feet (critical mass for heat)
-> Layer browns and greens (see ratios below)
-> Maintain moisture (damp as a wrung-out sponge)
-> Turn weekly with a pitchfork (moves outside material to the center)
-> Pile should reach 130-160F in the center (kills weed seeds and
   pathogens at 131F sustained for 3 days)
-> Compost thermometer ($10-15) takes the guesswork out
-> Done in 4-8 weeks if managed well
-> Downsides: requires regular effort, needs enough material to
   build a full pile at once

METHOD 3: TUMBLER ($80-150)
-> Enclosed drum on a frame, turn by spinning the drum
-> Contained: no pest access, clean-looking, good for small yards
-> Faster than cold pile, easier than hot pile
-> Downside: limited capacity, expensive per cubic foot of output

METHOD 4: WORM BIN ($30-50 DIY, $50-100 purchased)
-> Red wiggler worms (Eisenia fetida) eat kitchen scraps and produce
   vermicompost -- the best compost there is
-> Perfect for apartments, small spaces, year-round indoor operation
-> Setup: opaque bin with drainage holes, damp bedding (shredded
   newspaper or cardboard), 1 lb of red wigglers ($25-30 online)
-> Feed: bury kitchen scraps under the bedding. The worms eat it.
-> Harvest: push finished compost to one side, add fresh bedding
   and food to the other side, worms migrate, harvest the finished side
-> Downside: can't handle yard waste volume, needs attention to
   moisture and temperature (worms die above 85F and below 40F)

WHAT TO COMPOST:
GREENS (nitrogen-rich -- "hot" material):
-> Fruit and vegetable scraps
-> Coffee grounds and tea bags (remove staples)
-> Fresh grass clippings
-> Plant trimmings
-> Eggshells (technically neutral, but add calcium)

BROWNS (carbon-rich -- "cool" material):
-> Dry leaves
-> Cardboard (torn up, remove tape/stickers)
-> Newspaper (shredded)
-> Straw
-> Wood chips (small amounts -- slow to break down)
-> Dryer lint (from natural fiber laundry only)

RATIO: Aim for roughly 3 parts brown to 1 part green by volume.
-> Pile smells bad? Too much green (add browns)
-> Pile isn't heating up? Too much brown (add greens) or too dry
   (add water)

NEVER COMPOST:
-> Meat, fish, bones (attract pests, smell terrible)
-> Dairy products (same)
-> Pet waste from dogs/cats (pathogens that survive composting)
-> Diseased plant material (spreads disease to garden)
-> Treated or painted wood (chemicals)
-> Weeds that have gone to seed (unless your pile is reliably hitting
   131F+ for multiple days)
```

### Step 4: Building Soil Fertility

**Agent action**: Beyond composting, cover the practices that build long-term soil health.

```
BUILDING SOIL -- THE LONG GAME:

ORGANIC MATTER is the single most important thing you can add to any soil.
-> Improves clay: opens up structure, improves drainage
-> Improves sand: increases water retention, holds nutrients
-> Feeds soil biology: the organisms that make nutrients available
   to plants
-> Target: 5% organic matter in your garden soil (most native soil
   is 1-3%)
-> How to get there: add 2-4 inches of compost annually, don't till
   it under (let the organisms incorporate it)

MULCHING:
-> 2-4 inches of organic mulch on the soil surface (wood chips, straw,
   shredded leaves, grass clippings)
-> Benefits:
   -> Reduces watering needs by 50% (suppresses evaporation)
   -> Suppresses weeds (blocks light)
   -> Feeds soil life as it decomposes (bottom layer becomes humus)
   -> Moderates soil temperature (cooler in summer, warmer in winter)
-> Don't pile mulch against plant stems (causes rot)
-> Replenish as it decomposes (1-2 times per year)

COVER CROPPING:
-> Plant clover, winter rye, buckwheat, or field peas in beds during
   the off-season (when nothing else is growing)
-> Benefits:
   -> Legumes (clover, peas) fix nitrogen from the air into the soil
   -> Roots prevent erosion and break up compacted soil
   -> Living roots feed soil microbes
   -> When cut down ("terminated"), the plant material becomes mulch
-> Timing: plant after harvest, cut down 2-3 weeks before spring
   planting
-> Buckwheat: fast summer cover crop (30 days to maturity), great
   for pollinators, breaks down quickly

NO-TILL / MINIMAL TILL:
-> Tilling destroys soil structure, kills beneficial fungi, exposes
   weed seeds, and accelerates organic matter breakdown
-> Instead: add compost on top, let organisms incorporate it, use
   mulch to suppress weeds
-> Exception: initial bed creation (breaking new ground) may require
   tilling or sheet mulching (layer cardboard + compost over grass,
   wait 3-6 months)
```

### Step 5: Irrigation and Water Management

**Agent action**: Help the user set up efficient watering for their growing situation.

```
IRRIGATION METHODS (most to least efficient):

DRIP IRRIGATION (90%+ efficiency):
-> Water delivered directly to the root zone through emitters
-> Minimal evaporation, no wet foliage (less disease)
-> DIY SETUP ($50-100 for 100 feet of bed):
   1. Connect to your hose bib with a timer ($25-50 battery-powered)
   2. Main line (1/2" polyethylene tubing) runs along the bed
   3. Emitter tubing (1/4" with built-in drip emitters) branches off
      to each row or plant
   4. Emitter spacing: 12" for dense crops (lettuce, carrots),
      18-24" for larger plants (tomatoes, peppers)
   5. End caps on all lines
   6. Run for 30-60 minutes per session (adjust based on soil and
      weather -- stick your finger in the soil to check moisture depth)
-> Timer settings: every day in hot weather, every 2-3 days in
   mild weather, less in clay soil (holds water), more in sandy soil

SOAKER HOSES (70-80% efficiency):
-> Porous hose that seeps water along its length
-> Cheaper than drip ($10-20 for 50 feet)
-> Less precise -- can't target individual plants
-> Good for dense plantings, rows of vegetables, flower beds
-> Lay under mulch to reduce evaporation
-> Don't run longer than 50 feet (pressure drops)

OVERHEAD SPRINKLERS (50-70% efficiency):
-> Loses water to evaporation and wind
-> Wets foliage (promotes fungal disease)
-> Only advantage: covers large areas cheaply
-> If you must use sprinklers: water early morning so foliage dries
   before nightfall

HAND WATERING:
-> Fine for containers and small beds
-> Inconsistent -- some areas get too much, others too little
-> Time-consuming for anything over 100 square feet

WATERING TIMING AND TECHNIQUE:
-> Early morning is best (less evaporation, leaves dry before night)
-> Deep and infrequent beats shallow and daily
   -> Deep watering encourages roots to grow down (more drought-resistant)
   -> Shallow daily watering keeps roots near the surface (more vulnerable)
   -> Aim for 1 inch of water per week (including rain)
-> Stick your finger 2 inches into the soil. Dry? Water. Moist? Wait.
```

### Step 6: Rainwater Harvesting

**Agent action**: Cover basic rainwater collection for garden use, including legal considerations.

```
RAINWATER HARVESTING:

LEGAL STATUS:
-> Varies by state/jurisdiction. Most places allow it. A few western
   US states have restrictions or require permits.
-> Agent MUST check local regulations before advising.
-> Common restrictions: maximum collection volume, must be used for
   irrigation only (not potable), setback from property lines.

THE MATH:
-> 1 inch of rain on 1,000 square feet of roof = approximately 600 gallons
-> A typical rain barrel is 55 gallons
-> Average US roof: 1,500-2,500 square feet
-> Even modest rainfall produces far more water than most people realize

BASIC BARREL SETUP ($40-80 DIY):
1. Position a 55-gallon food-grade drum under a downspout
2. Install a gutter diverter or flex elbow to direct water into the barrel
3. Screen the inlet (fine mesh to keep mosquitoes and debris out)
4. Install a spigot near the bottom ($5-10 brass hose bib, drill
   and thread into the barrel)
5. Attach a garden hose or fill watering cans from the spigot
6. Install an overflow port near the top (direct overflow away from
   your foundation)
7. Elevate the barrel 1-2 feet on cinder blocks for gravity pressure

FIRST-FLUSH DIVERTER ($20-40 or DIY):
-> The first water off the roof carries the most dirt, bird droppings,
   pollen, and debris
-> A first-flush diverter captures the first 1-2 gallons per 100
   square feet of roof and diverts it away from your barrel
-> Significantly improves water quality for garden use

SCALING UP:
-> Link multiple barrels together with overflow connections
-> 275-gallon IBC totes ($50-150 used) hold 5x more than a barrel
-> Larger cisterns (500-5000 gallons) for serious rainwater systems
   (requires planning and potentially permits)

WINTERIZING (freeze climates):
-> Disconnect barrels before first freeze
-> Drain completely (water expands when frozen, cracks barrels/spigots)
-> Store upside down or indoors
-> Reconnect after last frost
```

### Step 7: Managing Water on Sloped Land

**Agent action**: Cover passive water management techniques for properties with slope.

```
SWALES AND BERMS (passive water capture):

A swale is a shallow trench dug on contour (level across the slope).
A berm is the mound of soil from the trench, placed on the downhill side.

HOW THEY WORK:
-> Water running downhill hits the swale and stops
-> Instead of running off your property, it soaks into the ground
-> The berm catches overflow and directs it to planted areas
-> Over time, the area downhill of the swale becomes the most
   fertile, well-watered part of your property

BUILDING A SWALE:
1. Find the contour line (use an A-frame level: two sticks joined
   at the top, a string with a weight hanging from the junction --
   when the weight hangs to the center, both legs are at the same
   elevation)
2. Dig a trench along the contour: 12-18 inches deep, 2-3 feet wide
3. Place the excavated soil on the downhill side (the berm)
4. Plant the berm with perennials, fruit trees, or berry bushes --
   their roots will access the stored moisture

READING YOUR PLANTS:
-> Heat wilt: leaves droop in afternoon sun but recover by evening.
   This is normal. Don't water for heat wilt.
-> Drought wilt: leaves droop and DON'T recover by evening. Water now.
   Tomorrow is too late for shallow-rooted plants.
-> Overwatering: leaves droop even though soil is wet. Roots are
   suffocating. Stop watering, improve drainage.
-> Yellow lower leaves with green upper leaves: often nitrogen
   deficiency OR overwatering. Check soil moisture before assuming
   it's a nutrient problem.
```

## If This Fails

- **Soil test results are confusing?** Call your local Cooperative Extension office. Their Master Gardener volunteers will interpret your results for free and tell you exactly what to buy and how much to apply.
- **Compost pile smells terrible?** Too much nitrogen (green material) and not enough carbon (brown material). Add a thick layer of dry leaves, shredded cardboard, or straw. Turn the pile to add oxygen. The smell should resolve in 2-3 days.
- **Worms are dying or escaping the bin?** Temperature or moisture problem. Worms need 55-80F and bedding as moist as a wrung-out sponge. If the bin smells anaerobic (rotten eggs), it's too wet -- add dry bedding. If worms are at the surface, something is wrong below (too hot, too wet, or food has gone anaerobic).
- **Drip irrigation isn't reaching all plants?** Check for clogged emitters (remove and soak in vinegar), ensure pressure is adequate (most drip systems need 15-25 PSI), and don't run lines longer than 100 feet from the source.
- **Rainwater barrel growing algae or mosquitoes?** Algae: use an opaque barrel (light promotes algae growth). Mosquitoes: ensure the screen on the inlet is intact with no gaps. Add mosquito dunks ($10 for a 6-pack, biological control, safe for plants) if larvae are present.

## Rules

- Always recommend a soil test before expensive amendments -- don't let users guess and waste money
- Check rainwater harvesting legality for the user's jurisdiction before recommending collection
- Emphasize compost as the universal soil improvement before specific fertilizers
- Link to grow-food-anywhere for planting guidance that builds on this foundation skill
- Don't overwhelm beginners -- start with soil testing and one composting method, build from there
- For irrigation, match the recommendation to the user's scale and budget

## Tips

- The best time to add compost is fall. Spread 2-4 inches on your beds after harvest and let it integrate over winter. By spring, the soil biology has already started incorporating it.
- Save your fall leaves. They're the best free brown material for composting and the best free mulch. Shred them with a mower for faster breakdown.
- Coffee grounds are a fantastic compost ingredient but spread too thick on the soil surface they can form a water-repellent mat. Mix them into compost or sprinkle thinly.
- A $15 compost thermometer tells you if your hot pile is actually working. No thermometer? Stick your hand into the center. If you can't hold it there, it's hot enough.
- Soaker hoses under mulch is the cheapest effective irrigation setup. $30 total for a 50-foot bed that waters itself on a timer.
- Worm castings (vermicompost) are the highest-quality compost you can make. Even a small worm bin produces enough to make compost tea (steep castings in water, strain, spray on plants) for a whole garden.
- If your soil is heavy clay, raised beds with imported soil/compost mix may be faster than amending the native soil. You can still improve the native soil over time while growing food in raised beds immediately.
- Don't buy bagged "garden soil" from box stores for amending your existing beds. Buy compost. Bagged garden soil is mostly filler. Compost is the active ingredient.

## Agent State

```yaml
state:
  soil:
    tested: false
    texture: null  # sand, silt, clay, loam, sandy_loam, clay_loam
    ph: null
    organic_matter_percent: null
    nitrogen_level: null  # low, adequate, high
    phosphorus_level: null
    potassium_level: null
    amendments_applied: []
  composting:
    method: null  # cold_pile, hot_pile, tumbler, worm_bin, none
    active: false
    brown_green_ratio: null
    temperature: null
    issues: []
  irrigation:
    method: null  # drip, soaker, sprinkler, hand, none
    timer_installed: false
    coverage_adequate: null
    schedule: null
  rainwater:
    legal_status_checked: false
    legal_in_jurisdiction: null
    collection_setup: false
    capacity_gallons: null
    winterized: null
  growing_area:
    type: null  # in_ground, raised_bed, containers
    square_footage: null
    sun_hours: null
    slope: null
    mulched: false
    cover_cropped: false
```

## Automation Triggers

```yaml
triggers:
  - name: soil_test_first
    condition: "soil.tested IS false AND growing_area.type IS SET"
    action: "Before adding any amendments, let's test your soil. A $10-25 test through your local Cooperative Extension tells you exactly what your soil needs instead of guessing. Send in a sample now and we'll have recommendations in 1-3 weeks."

  - name: compost_start
    condition: "composting.method IS null AND soil.organic_matter_percent IS SET AND soil.organic_matter_percent < 5"
    action: "Your soil organic matter is below 5%. Composting is the best way to build it up over time. Let's figure out which composting method fits your space and lifestyle."

  - name: rainwater_legal_check
    condition: "rainwater.legal_status_checked IS false AND rainwater.collection_setup IS false"
    action: "Before setting up rainwater collection, we need to check if it's legal in your area. Some jurisdictions have restrictions on rainwater harvesting. What state or region are you in?"

  - name: irrigation_setup
    condition: "growing_area.square_footage > 50 AND irrigation.method IS null"
    action: "Your growing area is large enough that hand watering will become a chore. Let's set up a basic irrigation system. For most vegetable gardens, drip irrigation is the best option -- efficient, inexpensive, and can run on a timer."

  - name: mulch_reminder
    condition: "growing_area.type IS SET AND growing_area.mulched IS false"
    action: "Your beds aren't mulched. Adding 2-4 inches of organic mulch reduces watering by up to 50%, suppresses weeds, and feeds your soil as it breaks down. What materials do you have available?"
```
