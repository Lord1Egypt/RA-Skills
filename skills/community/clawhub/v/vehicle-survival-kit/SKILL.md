---
name: vehicle-survival-kit
description: >-
  Practical vehicle maintenance and roadside emergency skills. Use when someone needs to change a tire, jump-start a battery, handle a breakdown, deal with a fender bender, or perform basic car maintenance.
metadata:
  category: skills
  tagline: >-
    Change a tire, jump a battery, handle a breakdown and a fender bender — the 10 car skills every driver needs before they need them.
  display_name: "Vehicle Survival Kit"
  submitted_by: HowToUseHumans
  last_reviewed: "2026-03-19"
  openclaw:
    requires:
      tools: [filesystem]
    install: "npx clawhub install vehicle-survival-kit"
---

# Vehicle Survival Kit

Most people drive every day and can't change a tire. They've never opened their hood, don't know what coolant looks like, and their emergency plan is "call someone." That works until you're on a highway shoulder at 11 PM with no cell signal. This skill covers the 10 things every driver should be able to do before the situation demands it — tire changes, jump starts, breakdowns, fender benders, and the basic maintenance that prevents most of these emergencies in the first place.

```agent-adaptation
# Localization note
- Swap driving side (left-hand traffic in UK, AU, JP, IN; right-hand everywhere else)
  and adjust roadside positioning advice accordingly
- Emergency numbers: US 911, UK 999, EU 112, AU 000
- Roadside assistance programs: US AAA, UK AA/RAC, AU NRMA/RACV, CA CAA, DE ADAC
- Insurance systems vary significantly — swap references to US-style
  liability/collision/comprehensive for local equivalents
- Measurement units: US uses PSI for tire pressure, most other countries use bar or kPa.
  Torque in ft-lbs (US) vs Nm (metric). Distances in miles (US/UK) vs km.
- Seasonal prep section: adjust for hemisphere and climate zone
```

## Sources & Verification

- **AAA Foundation for Traffic Safety** -- roadside emergency data and driver education. https://aaafoundation.org
- **NHTSA (National Highway Traffic Safety Administration)** -- vehicle safety guides, tire safety, recalls. https://www.nhtsa.gov
- **State DMV resources** -- vary by state; search "[state] DMV driver handbook" for local rules
- **Anthropic, "Labor market impacts of AI"** -- March 2026 research showing this occupation/skill area has near-zero AI exposure. https://www.anthropic.com/research/labor-market-impacts

## When to Use

- User got a flat tire or wants to learn how before it happens
- Car battery is dead or user wants to know jump-start procedure
- User broke down on a highway and doesn't know what to do
- User was in a fender bender and needs to know what to document
- User wants to check their own oil, coolant, or tire pressure
- User is building a trunk emergency kit
- User wants to know what basic car maintenance they can handle themselves
- User's car is overheating and they need immediate guidance

## Instructions

### Step 1: Build a trunk emergency kit ($50 budget)

**Agent action**: Ask the user if they already have an emergency kit. If not, generate this checklist. If yes, audit what they have against this list.

```
TRUNK EMERGENCY KIT — ~$50 total

TOOLS:
[ ] Lug wrench (confirm it fits your car's lug nuts — most cars include one)
[ ] Scissor jack or hydraulic bottle jack (most cars include a scissor jack)
[ ] Jumper cables, 4-gauge, 20 ft ($20-25 at any auto parts store)
[ ] Tire pressure gauge, digital or dial ($5-8)
[ ] Flashlight + extra batteries or a rechargeable USB flashlight ($10)
[ ] Multi-tool or basic pliers + flathead/Phillips screwdriver ($8-12)

SAFETY:
[ ] Reflective triangles or LED road flares ($10-15 for a set)
[ ] High-visibility vest ($3-5)
[ ] First aid kit, basic ($8-12)

SUPPLIES:
[ ] 1 quart motor oil (match your car's spec — check owner's manual)
[ ] 1 gallon distilled water (coolant emergency top-off)
[ ] Duct tape
[ ] Zip ties, assorted sizes
[ ] Rags or paper towels
[ ] Phone charger (car adapter or battery pack)
[ ] Pen + paper (for accident documentation when phone is dead)
[ ] $20 cash (for emergencies where cards don't work)

SEASONAL (cold climates):
[ ] Blanket
[ ] Ice scraper
[ ] Small bag of cat litter or sand (traction on ice)
```

### Step 2: Change a flat tire

**Agent action**: Walk the user through each step. If they're currently on the roadside, emphasize safety positioning first.

```
TIRE CHANGE PROCEDURE:

1. SAFETY FIRST
   - Pull completely off the road onto a flat, firm surface
   - Turn on hazard lights
   - Set the parking brake
   - Place reflective triangles 50, 100, and 200 feet behind your car
   - If on a highway, exit from the passenger side (away from traffic)

2. GATHER TOOLS
   - Lug wrench (in trunk or under cargo floor)
   - Jack (check owner's manual for location — usually under a panel in the trunk)
   - Spare tire (under trunk floor, or mounted under the vehicle on trucks/SUVs)

3. LOOSEN LUG NUTS (before jacking up)
   - Remove hubcap/wheel cover if present (pry with flat end of lug wrench)
   - Turn each lug nut counterclockwise 1/2 turn only — do NOT remove yet
   - "Lefty loosey" — if a nut is stuck, stand on the wrench handle
     and use your body weight
   - Loosen in a star pattern (opposite nuts, not adjacent)

4. JACK UP THE VEHICLE
   - Find the jack point — reinforced spot on the frame near the flat tire
   - Owner's manual shows exact location (usually a notch or arrow on the frame)
   - WRONG placement can crush body panels or drop the car
   - Raise until the flat tire is 6 inches off the ground

5. SWAP THE TIRE
   - Remove lug nuts completely (put them in your pocket, not on the ground)
   - Pull flat tire straight toward you and set aside
   - Mount spare tire — align holes, push onto bolts
   - Hand-tighten lug nuts in a star pattern

6. LOWER AND TORQUE
   - Lower jack until tire touches ground but car's weight isn't fully on it
   - Tighten lug nuts firmly in star pattern (most cars: 80-100 ft-lbs)
   - Lower jack completely, remove jack
   - Give each lug nut one final tighten

7. AFTER
   - Compact spare tires ("donuts") are limited: max 50 mph, max 70 miles
   - Get the flat repaired or replaced within a day or two
   - Re-check lug nut tightness after driving 25-50 miles
```

### Step 3: Jump-start a dead battery

**Agent action**: Walk through the procedure. Emphasize cable order — getting it wrong can damage electronics or cause sparks near the battery.

```
JUMP-START PROCEDURE:

REQUIREMENTS:
- Jumper cables (4-gauge, 20 ft recommended)
- A running vehicle with a good battery (the "donor")
- Both vehicles in park/neutral, engines off, keys out

CABLE CONNECTION ORDER (this matters):
1. RED clamp -> DEAD battery POSITIVE terminal (+)
2. RED clamp -> GOOD battery POSITIVE terminal (+)
3. BLACK clamp -> GOOD battery NEGATIVE terminal (-)
4. BLACK clamp -> UNPAINTED METAL on dead car's engine block
   (NOT the dead battery's negative terminal — this prevents sparks
   near the battery, which can off-gas hydrogen)

START SEQUENCE:
1. Start the donor vehicle, let it run 2-3 minutes
2. Try starting the dead vehicle
3. If it doesn't start, wait 5 minutes with donor running, try again
4. If it starts, leave BOTH vehicles running

CABLE REMOVAL ORDER (reverse of connection):
1. BLACK clamp from previously-dead car's engine block
2. BLACK clamp from donor battery
3. RED clamp from donor battery
4. RED clamp from previously-dead battery

AFTER:
- Drive the jumped car for at least 20-30 minutes to recharge
- If the battery dies again within a day, the battery needs replacing
- Most auto parts stores will test your battery for free
- Average battery replacement cost: $100-200 installed
```

### Step 4: Check oil and coolant

**Agent action**: Guide the user to locate their dipstick and coolant reservoir. Owner's manual is the definitive reference for their specific vehicle.

```
OIL CHECK (do this monthly):
1. Park on level ground, engine off for 5 minutes (lets oil drain back to pan)
2. Open hood (pull interior release, then lift safety latch under hood)
3. Find the dipstick — usually a yellow or orange loop/handle
4. Pull it out, wipe clean with a rag
5. Reinsert fully, pull out again
6. Read the level — oil should be between the two marks (MIN and MAX)
7. Check color: golden/amber = good, dark brown = due for change,
   black/gritty = overdue, milky = coolant leak (get to a mechanic)

ADDING OIL:
- Buy the weight listed in your owner's manual (e.g., 5W-30, 0W-20)
- Add through the oil filler cap (NOT the dipstick hole)
- Add 1/4 quart at a time, recheck level — overfilling is bad

COOLANT CHECK:
1. NEVER open the radiator cap when the engine is hot — pressurized steam
   will burn you severely
2. Find the coolant overflow reservoir (translucent plastic tank with
   MIN/MAX marks)
3. Check level is between MIN and MAX when engine is cool
4. If low, add a 50/50 mix of coolant and distilled water
5. If you're losing coolant regularly, you have a leak — see a mechanic
```

### Step 5: Replace wiper blades

**Agent action**: This is the easiest maintenance task and costs $15-30 DIY vs $40-60 at a shop.

```
WIPER BLADE REPLACEMENT:
1. Measure your current blades or check owner's manual for size
   (driver and passenger sides are often different lengths)
2. Buy replacements at any auto parts store — staff can look up your car
3. Lift the wiper arm away from the windshield
4. Find the release tab where the blade meets the arm
5. Press tab, slide old blade off
6. Slide new blade on until it clicks
7. Gently lower the arm back — don't let it snap against the glass

REPLACE WHEN:
- Streaking or smearing
- Squeaking
- Visible cracks or tears in the rubber
- Every 6-12 months regardless (rubber degrades in sun/cold)
```

### Step 6: Recognize brake warning signs

**Agent action**: This is a "know when to get help" skill. Brakes are not DIY for beginners.

```
BRAKE WARNING SIGNS — get to a shop if you notice any of these:

SOUNDS:
- High-pitched squealing when braking = brake pads are worn
  (built-in wear indicator is making contact — you have some time but don't wait)
- Grinding metal-on-metal = pads are gone, rotor damage happening NOW
  (drive directly to a shop or have it towed — this gets expensive fast)

FEEL:
- Vibration/pulsing in brake pedal = warped rotors
- Car pulls to one side when braking = uneven pad wear or stuck caliper
- Brake pedal feels soft or goes to the floor = possible fluid leak (DANGEROUS)
- Brake pedal feels hard and unresponsive = possible booster failure

VISUAL:
- Brake warning light on dashboard = check fluid level first,
  then get inspected
- Visible brake dust on wheels is normal; rust-colored dust may
  indicate rotor wear

COST EXPECTATIONS:
- Brake pad replacement: $150-300 per axle (parts + labor)
- Pads + rotors: $300-600 per axle
- If you wait until grinding: $500-1000+ (rotor replacement mandatory)
```

### Step 7: Handle a highway breakdown

**Agent action**: If the user is currently broken down, prioritize safety positioning. Everything else can wait.

```
HIGHWAY BREAKDOWN PROTOCOL:

1. GET OFF THE ROAD
   - Signal, move to the right shoulder as far as possible
   - If you can't reach the shoulder, turn on hazards and stay in
     the vehicle with seatbelt on until help arrives
   - NEVER stop in a traffic lane to check the car

2. MAKE YOURSELF VISIBLE
   - Hazard lights on immediately
   - Place reflective triangles or flares behind the vehicle
   - If you have a high-vis vest, put it on before exiting
   - At night: interior dome light on so other drivers see the vehicle

3. EXIT SAFELY
   - Exit from the passenger side (away from traffic)
   - Stand well away from the vehicle, behind the guardrail if possible
   - NEVER stand between your car and another vehicle

4. ASSESS AND CALL
   - Can you identify the problem? (flat tire, overheating, etc.)
   - If you can fix it safely: proceed with the relevant skill
   - If not: call roadside assistance (AAA: 1-800-222-4357)
   - If you feel unsafe: call 911

5. IF YOU MUST STAY IN THE CAR
   - Seatbelt on
   - Doors locked
   - Call for help
   - If someone stops to "help" and you feel unsafe,
     crack the window and ask them to call 911 for you
```

### Step 8: Document a fender bender

**Agent action**: Provide the full checklist. If the user is at the scene now, walk them through it step by step.

```
FENDER BENDER DOCUMENTATION CHECKLIST:

AT THE SCENE:
[ ] Move vehicles out of traffic if safe to do so (most states require this)
[ ] Check for injuries — call 911 if anyone is hurt
[ ] Turn on hazard lights
[ ] Call police for a report (required in most states if damage > $500
    or anyone is injured)

EXCHANGE WITH THE OTHER DRIVER:
[ ] Full name
[ ] Phone number
[ ] Insurance company and policy number
[ ] Driver's license number
[ ] License plate number
[ ] Vehicle make, model, year, color

DOCUMENT THE SCENE:
[ ] Photos of all damage to both vehicles (close-up and wide angle)
[ ] Photos of the overall scene (intersection, road conditions, traffic signs)
[ ] Photos of both license plates
[ ] Photos of both driver's licenses
[ ] Photo of the other driver's insurance card
[ ] Note the time, date, location, weather conditions
[ ] Note the direction each car was traveling

WITNESSES:
[ ] Get names and phone numbers of any witnesses
[ ] Ask if anyone has dashcam footage

DO NOT:
[ ] Do not admit fault or apologize (it can be used against you)
[ ] Do not argue with the other driver
[ ] Do not accept cash settlements at the scene
[ ] Do not leave the scene before exchanging info (hit-and-run is criminal)
```

### Step 9: Handle an overheating engine

**Agent action**: If the user's temperature gauge is in the red RIGHT NOW, give the immediate steps first.

```
OVERHEATING — IMMEDIATE RESPONSE:

1. Turn OFF the air conditioning
2. Turn the HEATER to maximum (draws heat away from engine)
3. If temperature doesn't drop within 2 minutes:
   - Pull over safely, turn off the engine
   - Pop the hood (from inside) but DO NOT OPEN the radiator cap
   - Wait at least 30 minutes for the engine to cool
4. After cooling, check coolant level in the overflow reservoir
   - If low, add water or coolant as a temporary fix to get to a shop
5. If you see steam, fluid on the ground, or a cracked hose:
   - Do NOT drive. Call for a tow.
   - Driving an overheating engine causes warped heads and blown
     gaskets — $1,500-4,000 in repairs

COMMON CAUSES:
- Low coolant (leak or evaporation)
- Failed thermostat ($150-300 to replace)
- Failed water pump ($300-750 to replace)
- Clogged radiator
- Broken radiator fan
```

### Step 10: Seasonal vehicle prep

**Agent action**: Ask user's location and season, then provide the relevant checklist.

```
WINTER PREP (before first freeze):
[ ] Check battery — cold reduces capacity; test at any auto parts store (free)
[ ] Check tire tread depth (penny test: insert penny head-first into tread;
    if you see all of Lincoln's head, tires need replacing)
[ ] Consider winter tires if you get regular snow/ice
[ ] Check antifreeze/coolant concentration (should protect to -34F/-36C)
[ ] Top off windshield washer fluid with winter formula (won't freeze)
[ ] Replace wiper blades if worn
[ ] Check heater and defroster operation
[ ] Pack winter emergency supplies (blanket, ice scraper, sand/cat litter)

SUMMER PREP (before sustained heat):
[ ] Check coolant level and condition
[ ] Check AC operation (recharge kits are $20-40 at auto parts stores)
[ ] Check tire pressure (heat increases pressure — don't overinflate)
[ ] Check battery (heat kills batteries faster than cold)
[ ] Top off windshield washer fluid
```

## If This Fails

- Can't loosen lug nuts: Use a breaker bar or stand on the wrench handle. If they're truly stuck (corrosion, overtorqued), call roadside assistance. This is common.
- Jump start doesn't work after 3 attempts: Battery is likely completely dead or has a failed cell. Needs replacement, not a jump. Call for a tow or get a new battery delivered (AAA does this).
- Overheating won't stop: Do not drive. Period. Call a tow truck. Driving with an overheating engine turns a $300 repair into a $3,000 repair.
- Insurance company is unresponsive after an accident: File a complaint with your state's Department of Insurance. They have enforcement power.

## Rules

- Safety before repair. Getting off the road and being visible to traffic matters more than fixing the car.
- Never crawl under a vehicle supported only by a jack. Jacks are for lifting, jack stands are for holding. This kills people every year.
- Never open a radiator cap on a hot engine. Pressurized steam causes severe burns instantly.
- Brake problems are not DIY for beginners. Know the warning signs, then get professional help.
- If you feel unsafe at any point — from traffic, from another person, from the situation — stay in the vehicle with doors locked and call 911.

## Tips

- Your owner's manual is the single most useful document in your car. It tells you jack point locations, tire pressure specs, oil weight, fuse locations, and warning light meanings. Read it once. Keep it in the glove box.
- Most auto parts stores (AutoZone, O'Reilly, Advance) will read diagnostic codes, test batteries, and test alternators for free. Use this.
- Tire pressure should be checked monthly. The correct pressure is on a sticker inside the driver's door jamb, NOT on the tire sidewall (that number is the maximum, not the target).
- Lug nuts should be tightened in a star pattern, never in a circle. This prevents warping the brake rotor.
- AAA membership ($60-100/year) pays for itself the first time you need a tow. Covers battery jump, lockout, fuel delivery, and up to 100 miles of towing depending on tier.

## Agent State

```yaml
vehicle:
  year: null
  make: null
  model: null
  tire_pressure_spec_psi: null
  oil_weight: null
  emergency_kit_complete: false
  emergency_kit_missing: []
  last_oil_change_date: null
  last_oil_change_miles: null
  tire_tread_ok: null
  battery_age_years: null
  roadside_assistance_provider: null
  roadside_assistance_number: null
skills_practiced:
  tire_change: false
  jump_start: false
  oil_check: false
  coolant_check: false
  wiper_replacement: false
incident:
  type: null
  date: null
  location: null
  police_report_number: null
  insurance_claim_number: null
  documentation_complete: false
```

## Automation Triggers

```yaml
triggers:
  - name: seasonal_prep_reminder
    condition: "vehicle.year IS SET"
    schedule: "October 15 and April 15 annually"
    action: "Time for seasonal vehicle prep. Based on your location, here's the checklist for the upcoming season. Let's walk through it."

  - name: oil_change_reminder
    condition: "vehicle.last_oil_change_miles IS SET AND current_miles - vehicle.last_oil_change_miles > 5000"
    schedule: "check monthly"
    action: "You're past 5,000 miles since your last oil change. Time to schedule one or check your oil level."

  - name: battery_age_warning
    condition: "vehicle.battery_age_years >= 3"
    schedule: "check quarterly"
    action: "Your battery is over 3 years old. Get it tested for free at any auto parts store before it leaves you stranded — most batteries fail between 3-5 years."

  - name: emergency_kit_audit
    condition: "vehicle.emergency_kit_complete IS false"
    schedule: "once"
    action: "Your trunk emergency kit is missing items. Let's review what you need — the full kit costs about $50 and covers most roadside situations."
```
