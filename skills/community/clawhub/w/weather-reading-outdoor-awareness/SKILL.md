---
name: weather-reading-outdoor-awareness
description: >-
  Practical weather observation and environmental awareness skills. Use when someone works outdoors, needs to make weather-dependent decisions without phone access, or wants to develop environmental situational awareness.
metadata:
  category: skills
  tagline: >-
    Read clouds, wind, and pressure changes. Know when a storm is 30 minutes away — not from an app, from the sky.
  display_name: "Weather Reading & Outdoor Awareness"
  submitted_by: HowToUseHumans
  last_reviewed: "2026-03-19"
  openclaw:
    requires:
      tools: [filesystem]
    install: "npx clawhub install weather-reading-outdoor-awareness"
---

# Weather Reading & Outdoor Awareness

Weather apps fail. Phones die. Cell service disappears. Mountains make their own weather. And the forecast is for your area, not your exact location. For anyone who works outside, hikes, farms, builds, or plans events, the ability to read what the sky is actually doing — right now, right here — is a practical skill that prevents hypothermia, lightning strikes, heatstroke, and bad decisions. This isn't meteorology theory. It's looking up and knowing what you're seeing.

```agent-adaptation
# Localization note
- Temperature: Fahrenheit (US) vs Celsius (everywhere else). Always provide both
  when giving thresholds.
- Distance: miles (US/UK) vs kilometers (metric countries)
- Pressure: inHg (US) vs hPa/mbar (everywhere else). 1 inHg ~ 33.86 hPa.
- Wind speed: mph (US/UK) vs km/h (metric) vs knots (marine/aviation)
- Severe weather alert systems:
  US: NWS (weather.gov), NOAA Weather Radio
  UK: Met Office warnings (metoffice.gov.uk)
  AU: Bureau of Meteorology (bom.gov.au)
  CA: Environment and Climate Change Canada (weather.gc.ca)
  EU: National meteorological services vary by country
- Regional weather patterns differ dramatically — adjust examples
  for user's hemisphere, latitude, and climate zone
- Tornado guidance is primarily US/Central US; swap for local severe
  weather types (cyclones in AU, typhoons in Asia, etc.)
```

## Sources & Verification

- **National Weather Service field guides** -- weather observation techniques and severe weather identification. https://www.weather.gov
- **NOAA weather observation guides** -- cloud identification, storm spotting, and environmental monitoring. https://www.noaa.gov
- **Wilderness Medical Society guidelines** -- environmental exposure management and field protocols. https://wms.org
- **Anthropic, "Labor market impacts of AI"** -- March 2026 research showing this occupation/skill area has near-zero AI exposure. https://www.anthropic.com/research/labor-market-impacts

## When to Use

- User works outdoors and needs to read weather without a phone
- User is planning outdoor activities and wants to know what to watch for
- User sees clouds and wants to know what they mean
- User is caught in changing weather and needs immediate guidance
- User wants to know when to cancel outdoor work or plans
- User is concerned about lightning, heat, or cold exposure
- User needs to dress for conditions and doesn't know the layering system
- User is outdoors and conditions are deteriorating

## Instructions

### Step 1: Read clouds (the 5 that matter)

**Agent action**: Most people can't name a single cloud type. They don't need to name 50 — they need to recognize 5 patterns and know what each means.

```
THE 5 CLOUD TYPES YOU NEED TO KNOW:

1. CUMULUS (fair weather clouds)
   - White, puffy, flat bottoms, look like cotton balls
   - Scattered across the sky with blue between them
   - MEANING: fair weather. These are fine.
   - WATCH FOR: if they start growing TALL (towering), they're
     becoming cumulonimbus. Time is running out.

2. CUMULONIMBUS (thunderstorm clouds)
   - Massive vertical development — towers reaching 40,000+ feet
   - Dark base, anvil-shaped top that spreads out flat
   - Often the only cloud in the area — everything else clears around it
   - MEANING: thunderstorm. Lightning, heavy rain, possible hail,
     possible tornadoes. GET INSIDE.
   - TIMING: if you see a cumulonimbus growing on the horizon,
     you have 30-60 minutes before it reaches you. If it's overhead
     and darkening, you have minutes.

3. STRATUS (overcast, grey blanket)
   - Low, uniform, grey layer covering the whole sky
   - Like a fog that's a few thousand feet up
   - MEANING: drizzle or light rain possible. Depressing but not
     dangerous. Temperature will stay stable.
   - Low stratus at ground level = fog. Reduce driving speed.

4. CIRRUS (high, wispy)
   - Thin, white, wispy streaks at very high altitude
   - Made of ice crystals
   - MEANING: fair weather NOW, but cirrus appearing and thickening
     over 12-24 hours often means a weather system is approaching.
   - "Mare's tails" (hooked cirrus) = frontal system in 24-48 hours

5. LENTICULAR (lens-shaped, over mountains)
   - Smooth, lens or UFO-shaped clouds that stay in one place
   - Form over and downwind of mountains
   - MEANING: extremely strong winds at altitude.
   - If you see these, expect gusty conditions in mountain terrain.
   - Pilots avoid these — the turbulence is severe.

RAPID ASSESSMENT:
- Clouds getting TALLER = instability increasing = storms possible
- Clouds getting DARKER at the base = more moisture = rain imminent
- Clouds moving FAST = strong winds aloft = weather changing soon
- Sky clearing from the WEST = improving weather
- Sky darkening from the WEST = deteriorating weather
  (most weather moves west to east in temperate zones)
```

### Step 2: Read wind

**Agent action**: Wind direction and speed tell you what's coming and when. No instruments needed.

```
WIND READING:

DIRECTION (where weather comes from):
- Face the wind. Weather is coming from that direction.
- In most of North America and Europe, weather moves west to east.
- A shift in wind direction means a weather change is imminent.
  - Wind shifting clockwise (veering): warming, often clearing
  - Wind shifting counterclockwise (backing): cooling, often
    worsening

SPEED ESTIMATION (Beaufort scale, simplified):
- Calm: smoke rises straight up
- Light (1-7 mph / 2-11 km/h): leaves rustle, you feel it on your face
- Moderate (8-18 mph / 13-29 km/h): small branches move, dust kicks up,
  loose paper blows
- Strong (19-31 mph / 30-50 km/h): large branches sway, walking is
  harder, umbrellas flip
- Gale (32-46 mph / 51-74 km/h): whole trees sway, walking against
  the wind is difficult. Stop outdoor work.
- Storm (47+ mph / 75+ km/h): structural damage possible.
  Get inside. Now.

GUSTS VS. SUSTAINED:
- A "20 mph wind with gusts to 40" means the average is 20 but
  it periodically hits 40. The gusts are what knock things over
  and blow you off balance.
- If you feel sudden strong blasts between calm periods, those
  are gusts. Plan for the gust speed, not the average.
```

### Step 3: Barometric pressure changes

**Agent action**: Most people don't carry a barometer. But your body and environment give pressure clues.

```
PRESSURE READING WITHOUT INSTRUMENTS:

WHAT PRESSURE MEANS:
- Rising pressure = improving weather (high pressure = fair)
- Falling pressure = worsening weather (low pressure = storms)
- Rapid drops = severe weather approaching fast

SIGNS OF FALLING PRESSURE:
- Your ears "pop" or feel full
- Sounds carry farther than usual (distant trains, highway noise)
- Smells are stronger (falling pressure releases gases from soil,
  water, and vegetation — that "rain smell" is a real signal)
- Clouds lower and thicken
- Smoke from chimneys or campfires curls downward instead of rising
- Joint pain increases (yes, this is real — tissues swell slightly
  with lower external pressure)

SIGNS OF RISING PRESSURE:
- Clouds thin and rise
- Visibility improves
- Temperature may drop (cold air is denser = higher pressure)
- Dew forms overnight (clear skies, high pressure, radiative cooling)

IF YOU HAVE A PHONE OR WATCH WITH BAROMETER:
- Normal: ~29.9 inHg / 1013 hPa
- Above 30.2 inHg / 1023 hPa: strong high pressure, clear weather
- Below 29.5 inHg / 999 hPa: low pressure, storms likely
- A drop of 0.1 inHg (3 hPa) in 3 hours: weather change coming
- A drop of 0.3 inHg (10 hPa) in 3 hours: severe weather likely
```

### Step 4: Lightning safety

**Agent action**: If the user is currently near lightning, give immediate shelter guidance first. The physics can wait.

```
LIGHTNING SAFETY:

THE RULE:
"When thunder roars, go indoors." If you can hear thunder, you
are within striking distance of lightning (up to 10 miles away).

DISTANCE CALCULATION:
- See lightning flash, start counting seconds until thunder
- Divide by 5 = distance in miles (divide by 3 for kilometers)
- Example: 15 seconds = 3 miles away
- At 30 seconds or less (6 miles): STOP outdoor activities
  and seek shelter immediately

SAFE SHELTER (in order of preference):
1. Substantial building (not a shed, pavilion, or tent)
2. Hard-topped vehicle (not convertible) with windows closed
3. If nothing available: crouch low in a ditch or depression,
   minimize contact with the ground, cover ears

UNSAFE LOCATIONS:
- Under isolated trees (lightning strikes the tallest object)
- On hilltops or ridges
- In open fields
- Near metal fences, poles, or equipment
- In or near water (pools, lakes, rivers) — exit water at
  the first sign of a storm
- Open shelters (gazebos, bus stops, rain shelters)

WAIT TO RESUME:
- 30 minutes after the LAST thunder before going back outside
- Storms can re-intensify, and lightning can strike from the
  back of a departing storm

IF SOMEONE IS STRUCK:
- Lightning victims do NOT carry an electrical charge — it's safe
  to touch them
- Call 911 immediately
- Begin CPR if they're not breathing. Lightning causes cardiac arrest.
- Check for burns at entry and exit points (often feet and head)
```

### Step 5: Heat and cold awareness

**Agent action**: Ask the user's current conditions. Provide the relevant section based on temperature and activity level.

```
HEAT ILLNESS RECOGNITION AND RESPONSE:

HEAT EXHAUSTION (warning stage):
- Heavy sweating, pale skin, nausea, dizziness
- Muscle cramps, headache, weakness
- Body temp may be elevated but under 104F (40C)
- RESPONSE: move to shade/AC, remove excess clothing, drink cool
  water slowly, cool skin with wet cloths. Rest. Monitor for 30 min.

HEAT STROKE (emergency — call 911):
- Body temp above 104F (40C)
- Hot, RED, DRY skin (sweating has stopped)
- Confusion, slurred speech, loss of consciousness
- RESPONSE: call 911 immediately. Move to coolest available location.
  Cool aggressively — ice on neck, armpits, groin (major blood vessels).
  Do NOT give fluids if confused or unconscious.

PREVENTION:
- Hydrate before you're thirsty (by the time you feel thirst,
  you're already behind)
- In heat over 90F (32C): 8 oz water every 15-20 minutes of
  exertion. More with humidity.
- Heat index above 105F (40C): extreme danger. Limit outdoor
  exposure. Mandatory rest breaks in shade.
- Wet bulb temperature above 90F (32C): lethal heat for sustained
  outdoor exertion regardless of fitness.

COLD EXPOSURE:

HYPOTHERMIA STAGES:
Mild (95-90F / 35-32C): shivering, numb hands, poor coordination
Moderate (90-82F / 32-28C): violent shivering, confusion, slurred speech
Severe (below 82F / 28C): shivering stops, unconsciousness, cardiac risk

RESPONSE:
- Get out of the cold, wind, and wet
- Remove wet clothing
- Warm the core first (warm drinks if conscious, body heat from another
  person, warm packs on neck/armpits/groin)
- Do NOT rub extremities, do NOT give alcohol
- Severe hypothermia: call 911. Handle gently — rough movement can
  trigger cardiac arrest.

FROSTBITE:
- White or grayish-yellow patches on skin (ears, nose, fingers, toes)
- Numbness, then pain as rewarming begins
- Do NOT rub frostbitten skin. Do NOT rewarm with direct heat.
- Soak in warm (not hot) water — 100-104F (37-40C)
- Seek medical attention for any frostbite beyond a small area
```

### Step 6: Dress for conditions (layering system)

**Agent action**: Ask the user's activity level and temperature range. This determines layer recommendations.

```
THE LAYERING SYSTEM:

WHY LAYERS:
One thick coat can't adapt. Three thinner layers can handle any
condition from 60F to -20F by adding, removing, or venting.

LAYER 1 — BASE LAYER (moisture management):
- Purpose: move sweat away from skin
- Material: merino wool or synthetic (polyester/nylon blend)
- NEVER cotton next to skin in cold. Cotton absorbs moisture,
  stays wet, and conducts heat away from your body.
  "Cotton kills" is not an exaggeration.
- Cost: $15-40 for a good synthetic or merino base layer top

LAYER 2 — INSULATION (warmth):
- Purpose: trap warm air
- Material: fleece, down, or synthetic insulation
- Fleece: cheap, warm when wet, heavy. Good for most situations.
- Down: lightest warmth-to-weight ratio, compresses small.
  Useless when wet unless treated.
- Synthetic insulation: heavier than down but works when wet.
  Best for wet climates.
- Cost: $20-80 depending on material

LAYER 3 — SHELL (wind and water protection):
- Purpose: block wind and rain
- Material: waterproof/breathable (Gore-Tex, eVent) or water-resistant
  softshell
- A shell that blocks wind is more important than insulation in
  many conditions. Wind chill is real — 30F with 20 mph wind
  feels like 17F.
- Cost: $40-200 depending on quality

TEMPERATURE GUIDE:
60-70F (15-21C): base layer only, maybe a light shell for wind
50-60F (10-15C): base layer + light insulation
40-50F (4-10C): base layer + insulation + shell if windy/wet
30-40F (-1 to 4C): base + mid-weight insulation + shell
20-30F (-7 to -1C): base + heavy insulation + shell
Below 20F (-7C): base + heavy insulation + shell + add layers,
  insulated pants, warm hat, good gloves
```

### Step 7: When to cancel

**Agent action**: This is the hardest decision for most outdoor workers and event planners. Give clear thresholds.

```
CANCEL/DELAY OUTDOOR WORK OR PLANS WHEN:

LIGHTNING:
- Thunder audible or lightning visible: stop immediately
- Do not resume until 30 minutes after last thunder

WIND:
- Sustained above 25 mph (40 km/h): cancel scaffolding, crane,
  and high-elevation work
- Sustained above 40 mph (65 km/h): cancel most outdoor activities
- Gusts above 50 mph (80 km/h): dangerous for anyone to be outside

HEAT:
- Heat index above 105F (40C): extreme danger for sustained exertion
- Wet bulb temperature above 90F (32C): potentially lethal conditions
- If workers show heat exhaustion symptoms: stop work, cool down,
  hydrate. Do not resume until fully recovered.

COLD:
- Wind chill below 0F (-18C): exposed skin gets frostbite in 30 min
- Wind chill below -20F (-29C): frostbite in 10 minutes. Limit exposure.
- If anyone shows confusion or shivering stops: emergency. Warm now.

VISIBILITY:
- Fog reducing visibility below 1/4 mile (400m): slow or stop
  driving. Cancel work involving vehicles or heavy equipment.

FLASH FLOOD RISK:
- "Turn around, don't drown" — never cross flowing water on a road
- If in a canyon or drainage: move to high ground at first sign
  of upstream storm activity
```

## If This Fails

- Can't identify cloud types: Start with one distinction — flat vs tall. Flat clouds = stable air = no storms. Tall clouds = unstable air = storms developing. That single observation keeps you safe.
- Weather changed faster than expected: This happens. Weather forecasts and observations have limits. The key is having a plan for deterioration before you go out. "If conditions worsen, we go to [location]."
- Heat illness despite precautions: Hydration alone isn't enough in extreme heat. You also need electrolytes and rest. If symptoms progress to heat stroke despite best efforts, call 911.
- Caught in lightning with no shelter: Avoid the tallest objects, avoid open ground, avoid water. If in a group, spread out (reduces multi-casualty risk). Crouch low, feet together, hands over ears. This is not a good position — it's the least-bad position.

## Rules

- Lightning kills more people per year than tornadoes or hurricanes in the US. Take it seriously. 30 seconds of counting = time to shelter.
- Never rely on a single information source. Phone forecast + sky observation + wind/pressure reading together are far more reliable than any one alone.
- Cotton kills in cold and wet conditions. This is not an exaggeration. Wet cotton conducts heat away from your body 25 times faster than dry insulation.
- Hydrate before you're thirsty. Thirst is a lagging indicator — by the time your brain signals thirst, your performance is already degraded.
- When in doubt, go in. The cost of canceling an afternoon of outdoor work is nothing compared to a lightning strike, heat stroke, or hypothermia evacuation.

## Tips

- The single most useful weather observation: watch how fast clouds are changing. Static clouds = stable conditions. Rapidly growing/darkening clouds = weather is deteriorating. You don't need to name them.
- "Red sky at night, sailor's delight. Red sky in morning, sailor's warning." This is real. Red sunset = dust particles in dry air coming from the west = fair weather approaching. Red sunrise = that dry air has passed and moisture is coming.
- A sudden temperature drop, wind shift, or increase in wind speed often precedes a storm by 15-30 minutes. These are your final warning signs.
- If you work outdoors, get a watch with a barometer (Casio makes them for $30-50). The 3-hour pressure trend is one of the most reliable short-term weather predictors you can carry.
- The most dangerous weather isn't the most dramatic. More people die from heat and cold than from tornadoes and hurricanes combined. The slow killers are the real threat.

## Agent State

```yaml
environment:
  user_location: null
  climate_zone: null
  current_activity: null
  current_temperature: null
  current_conditions: null
  elevation: null
  shelter_available: null
  water_available: null
awareness:
  can_identify_cumulonimbus: false
  knows_lightning_rule: false
  knows_layering_system: false
  knows_heat_illness_signs: false
  knows_hypothermia_signs: false
  has_barometer: false
gear:
  base_layer_material: null
  insulation_type: null
  shell_waterproof: null
  appropriate_for_conditions: null
```

## Automation Triggers

```yaml
triggers:
  - name: outdoor_activity_prep
    condition: "environment.current_activity IS SET AND environment.current_activity CONTAINS 'outdoor'"
    action: "You're heading outdoors. What's your location and planned duration? Let me give you a conditions briefing and help you prepare for what the sky's likely to do."

  - name: heat_safety_alert
    condition: "environment.current_temperature > 90 AND environment.current_activity IS SET"
    action: "High heat conditions. Let's review your hydration plan, rest schedule, and heat illness recognition. Heat stroke progresses fast — knowing the signs is the difference between an inconvenience and an emergency."

  - name: storm_approaching
    condition: "environment.current_conditions CONTAINS 'darkening' OR environment.current_conditions CONTAINS 'thunder'"
    action: "Conditions are deteriorating. Time to assess shelter options and review lightning safety protocol. When thunder roars, go indoors — no exceptions."

  - name: seasonal_gear_check
    condition: "environment.user_location IS SET"
    schedule: "October 1 and April 1 annually"
    action: "Season change approaching. Let's review your outdoor gear for the coming conditions — layering system, footwear, and any weather tools you should have."
```
