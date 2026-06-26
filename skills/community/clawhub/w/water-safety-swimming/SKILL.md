---
name: water-safety-swimming
description: >-
  Water safety, basic swimming skills, and emergency water rescue techniques. Use when someone can't swim, is taking children near water, wants to learn basic water rescue, or needs pool/beach/river safety guidance.
metadata:
  category: skills
  tagline: >-
    How to not drown, how to help someone who's drowning without dying yourself, and basic water rescue everyone should know.
  display_name: "Water Safety & Swimming"
  submitted_by: HowToUseHumans
  last_reviewed: "2026-03-19"
  openclaw:
    requires:
      tools: [filesystem]
    install: "npx clawhub install water-safety-swimming"
---

# Water Safety & Swimming

Drowning is the third leading cause of unintentional injury death worldwide. It kills over 236,000 people per year. It's silent — no splashing, no screaming, no waving. Real drowning looks like someone standing still in the water with their head tilted back. Children can drown in 2 inches of water in under 2 minutes. This skill isn't swim coaching — it's survival. How to keep yourself alive in water, how to recognize drowning, how to rescue someone without becoming a second victim, and how to keep your family safe around water.

```agent-adaptation
# Localization note
- Emergency numbers: US 911, UK 999/112, EU 112, AU 000, NZ 111
- Water safety organizations:
  US: American Red Cross, YMCA
  UK: Royal Life Saving Society (RLSS UK), Royal National Lifeboat Institution (RNLI)
  AU: Royal Life Saving Society Australia, Surf Life Saving Australia
  CA: Lifesaving Society Canada
  NZ: Water Safety New Zealand
- CPR certification providers vary by country — swap Red Cross for local equivalent
- Pool fencing regulations vary:
  US: varies by state/municipality
  AU: mandatory 4-sided isolation fencing (national standard)
  UK: no national requirement but HSE guidance for public pools
- Beach flag systems are largely standardized but colors may vary
- Swap temperature units (Fahrenheit/Celsius) based on user location
```

## Sources & Verification

- **American Red Cross** -- water safety training, CPR/first aid certification, swimming skill levels. https://www.redcross.org/get-help/how-to-prepare-for-emergencies/types-of-emergencies/water-safety.html
- **CDC drowning prevention data** -- epidemiology and prevention strategies. https://www.cdc.gov/drowning/
- **International Life Saving Federation** -- global drowning statistics, water rescue standards. https://www.ilsf.org
- **WHO drowning prevention guidelines** -- global burden and intervention data. https://www.who.int/health-topics/drowning
- **Anthropic, "Labor market impacts of AI"** -- March 2026 research showing this occupation/skill area has near-zero AI exposure. https://www.anthropic.com/research/labor-market-impacts

## When to Use

- User can't swim or is a weak swimmer
- User is taking children near water (pool, beach, lake)
- User wants to learn basic water rescue techniques
- User is planning activities near open water (boating, kayaking, fishing)
- User wants to understand rip currents and ocean safety
- User fell into cold water or is asking about cold water shock
- User wants a water competency self-assessment
- User is a parent setting up a home pool or moving near water

## Instructions

### Step 1: Water competency self-assessment

**Agent action**: Before teaching anything, assess where the user is. This determines which sections they need most.

```
WATER COMPETENCY CHECKLIST — self-assess honestly

LEVEL 1: SURVIVAL (minimum everyone should have)
[ ] Can enter water over your head and return to the surface
[ ] Can float or tread water for 1 minute
[ ] Can turn over and orient yourself in the water
[ ] Can swim 25 yards (one pool length) without stopping
[ ] Can exit the water safely (climb out of a pool, get to shore)

LEVEL 2: BASIC SAFETY
[ ] Can tread water for 5 minutes
[ ] Can float on your back for 2 minutes without effort
[ ] Can swim 50 yards without stopping
[ ] Can open eyes underwater
[ ] Can retrieve an object from the bottom of a pool (chest depth)
[ ] Know what a rip current is and how to escape one
[ ] Know the reach-throw-don't-go rescue principle

LEVEL 3: WATER CONFIDENT
[ ] Can tread water for 15 minutes
[ ] Can swim 200 yards continuously
[ ] Can perform a reaching or throwing rescue
[ ] Can perform basic CPR
[ ] Comfortable in open water (lake, ocean)
[ ] Understand cold water shock response

SCORING:
- Missing Level 1 items: take swimming lessons. Now. This is urgent.
- Complete Level 1, missing Level 2: you can survive a fall into
  water but need to build endurance and safety knowledge.
- Complete Level 2, missing Level 3: you're safe for most situations.
  Level 3 is for people who are regularly around water.
```

### Step 2: Float to survive (the #1 drowning prevention skill)

**Agent action**: This is the single most important skill in this file. If someone falls into water unexpectedly, this is what keeps them alive.

```
FLOAT TO SURVIVE:

WHY THIS MATTERS:
Most drowning victims panic and try to swim. Panic burns energy and
oxygen. In cold water, your muscles lose function in minutes. The
instinct to fight the water is what kills. Floating is the opposite
of that instinct — and it works.

THE TECHNIQUE:
1. Lean back. Tilt your head back until your ears are in the water.
2. Extend your arms out to the sides, palms up.
3. Push your hips forward and up toward the surface.
4. Spread your legs slightly.
5. Breathe slowly and deeply. Air in your lungs = buoyancy.
6. Don't kick. Don't thrash. Be still.
7. You will float. Even if it feels like you won't.

WHY IT WORKS:
- Your lungs are natural flotation devices
- A full breath of air makes most people positively buoyant
- Relaxing reduces oxygen consumption and extends survival time
- A still body floats higher than a thrashing body

PRACTICE THIS IN A POOL:
- Start in chest-deep water
- Lean back slowly, letting the water support you
- If your legs sink: it's normal. Slightly arch your back more
  and push your hips up. Most people's legs are denser than
  their torso — this is fine, your face stays above water.
- Practice until you can float for 2 minutes without effort
- Then practice fully clothed (clothes change buoyancy and drag)

IN OPEN WATER:
- Float to survive until you've calmed the panic response (30-60 seconds)
- Then orient yourself and swim slowly to safety
- If you can't see shore or safety, keep floating and call for help
```

### Step 3: Tread water

**Agent action**: The active complement to floating. For situations where floating isn't possible (waves, current, cold water making it hard to relax).

```
TREADING WATER:

THE TECHNIQUE:
1. Body vertical in the water, head above surface
2. Arms: move them back and forth horizontally near the surface
   (like spreading butter on bread) — this creates lift
3. Legs: "eggbeater" kick — alternating circular kicks,
   like pedaling a bicycle with your legs apart
4. Keep movements slow and controlled — efficiency, not power
5. Breathe normally. Don't hyperventilate.

ENERGY CONSERVATION:
- Full treading: 15-20 minutes before exhaustion for most people
- Slow tread (minimal movement): 30-60 minutes
- Alternate between floating and treading to extend endurance
- In waves: time your breathing between waves, don't fight them

PRACTICE:
- Start in a pool where you can stand if needed
- Tread for 1 minute. Rest. Repeat.
- Build to 5 minutes continuous
- Practice with clothes on (shoes especially — they're heavy when wet)
```

### Step 4: Recognize drowning

**Agent action**: This is critical for anyone who supervises others near water. Drowning looks nothing like the movies.

```
WHAT DROWNING ACTUALLY LOOKS LIKE:

DROWNING IS SILENT.
There is no screaming. There is no waving. There is no splashing.
The instinctive drowning response takes over and the person CANNOT
call for help — their body prioritizes breathing over speaking.

REAL DROWNING SIGNS:
-> Head tilted back, mouth at water level
-> Eyes glassy, unfocused, or closed
-> Body vertical in the water, no leg movement visible
-> Arms pressing down on the water surface laterally (not waving)
-> Quiet. No sound. This is the most important sign.
-> Appears to be climbing an invisible ladder
-> Hair over forehead or eyes with no attempt to move it
-> Hyperventilating or gasping

WHAT DROWNING DOES NOT LOOK LIKE:
-> Yelling "Help!" (they can't — vocal cords prioritize breathing)
-> Waving arms above the head (arms are pressed down for buoyancy)
-> Thrashing dramatically (too little energy for that)
-> Going under and coming back up repeatedly (this is distressed
   swimmer, not active drowning — but they need help too)

THE 30-SECOND RULE:
If someone in the water looks like they might be in trouble,
watch for 30 seconds. If they haven't made progress toward
safety, act. Don't wait for certainty.

CHILDREN ESPECIALLY:
- Children drown in seconds, silently, in inches of water
- A child who is quiet in a pool is more dangerous than one
  who is loud
- Drowning can happen within arm's reach of other people who
  don't recognize it
```

### Step 5: Reach-throw-don't-go rescue

**Agent action**: This is the rescue framework everyone should know. The order matters — it's ranked by risk to the rescuer.

```
RESCUE PRINCIPLE: REACH — THROW — DON'T GO

A drowning person will grab anything — including you. An untrained
rescuer who swims to a drowning victim is the most common cause
of double drowning. Follow this order.

1. REACH (safest)
   - Extend something from shore or poolside:
     a pool noodle, a towel, a branch, a shirt, an oar, a belt
   - Lie flat on your stomach and reach — don't let them pull you in
   - Brace yourself. They will grab HARD.
   - Pull them to safety once they have a grip

2. THROW (if you can't reach)
   - Throw a flotation device: life ring, cooler, empty water jug
     with cap on, kickboard, anything that floats
   - Aim PAST the person and pull it toward them — they can't catch
     a thrown object in their state
   - If a rope is attached, pull them in after they grab it

3. ROW (if you have a boat)
   - Approach from the side or behind, not head-on
   - Extend an oar for them to grab
   - Be prepared for them to try to climb in — brace the boat

4. DON'T GO (last resort — trained rescuers only)
   - DO NOT swim to a drowning person unless you are trained
   - If you must enter the water: bring a flotation device between
     you and the victim
   - Approach from behind if possible
   - Push the flotation device to them and back away
   - If they grab you: take a breath, go underwater.
     They will let go to stay at the surface. Swim away, reapproach
     with a flotation device.

CALL 911 IMMEDIATELY:
- Before, during, or after any rescue attempt — call or have someone call
- Even if the person seems fine afterward — secondary drowning
  (water in lungs) can be fatal hours later
- Anyone who was submerged and had difficulty breathing needs
  medical evaluation
```

### Step 6: Rip current escape

**Agent action**: If the user is asking about ocean safety or has been caught in a rip current, this is the priority section.

```
RIP CURRENT SURVIVAL:

WHAT A RIP CURRENT IS:
A narrow, powerful channel of water flowing away from shore. It forms
when waves push water toward the beach faster than it can flow back.
The excess water finds a gap and rushes seaward through it.

HOW TO SPOT ONE FROM SHORE:
- A gap in the breaking waves (calmer-looking strip of water —
  paradoxically, the calm area is the dangerous one)
- Discolored or murky water heading seaward
- Foam, seaweed, or debris moving away from shore
- A line of choppy water between calmer areas

IF YOU'RE CAUGHT IN A RIP CURRENT:
1. DO NOT swim toward shore (against the current). You will exhaust
   yourself and drown. The current is stronger than you.
2. Swim PARALLEL to shore — perpendicular to the current's pull.
   Rip currents are narrow (10-30 feet wide usually).
3. Once free of the pull, swim diagonally toward shore.
4. If you can't swim out of it: FLOAT. Rip currents don't pull you
   under — they pull you OUT. They dissipate 50-100 yards offshore.
   Float until the current weakens, then swim parallel and back.
5. Stay calm. Rip currents don't drown you. Panic drowns you.

SPEED AND POWER:
- Rip currents can flow at 4-5 mph — faster than an Olympic swimmer
- Fighting them directly is physically impossible
- They typically extend 50-100 yards offshore before dissipating
- Once you stop being pulled, you're past the rip
```

### Step 7: Cold water shock response

**Agent action**: If someone fell into cold water or is planning cold-water activities (boating in spring/fall, ice fishing), cover this.

```
COLD WATER SHOCK:

Water below 60F (15C) triggers an involuntary gasp reflex and
hyperventilation. This is the #1 killer in cold water — not
hypothermia. People drown in the first 60 seconds.

THE FOUR STAGES OF COLD WATER IMMERSION:

STAGE 1 — COLD SHOCK (first 1-3 minutes):
- Involuntary gasp reflex (if your head is underwater, you inhale water)
- Uncontrollable hyperventilation
- Heart rate and blood pressure spike (cardiac arrest risk)
- SURVIVAL: get your face out of the water immediately. Float on
  your back. Do NOT try to swim. Focus only on controlling your
  breathing for the first 60 seconds. This stage passes.

STAGE 2 — SWIMMING FAILURE (3-30 minutes):
- Muscles cool and lose function rapidly
- Grip strength fails, arms and legs stop responding normally
- Stroke technique deteriorates until swimming is impossible
- SURVIVAL: if you entered the water near a boat/dock/shore,
  swim toward it NOW — before Stage 2 progresses. You have minutes,
  not hours. If you can't reach safety, float and call for help.

STAGE 3 — HYPOTHERMIA (30+ minutes):
- Core body temperature drops below 95F (35C)
- Confusion, slurred speech, loss of consciousness
- Without rescue, eventually fatal
- SURVIVAL: keep floating. Minimize movement (movement pumps
  warm blood to cold extremities, cooling your core faster).
  Assume HELP position: Heat Escape Lessening Posture — knees to
  chest, arms crossed. If in a group, huddle together.

STAGE 4 — POST-RESCUE COLLAPSE:
- Blood pressure drops when pulled from water (cold blood from
  extremities reaches the heart)
- Handle rescued cold water victims GENTLY — horizontal position
- Do NOT rub their extremities or give hot drinks immediately
- Get medical help — rewarming must be done carefully
```

### Step 8: Pool safety for families (layers of protection)

**Agent action**: If the user has children and a pool (or lives near water), this is critical. One barrier is never enough.

```
POOL SAFETY — LAYERS OF PROTECTION:

No single safety measure is enough. Use multiple layers.

LAYER 1: SUPERVISION
- Designated water watcher at all times (no phone, no book, no naps)
- Rotate every 15-30 minutes to prevent attention fatigue
- Within arm's reach for children under 5 at all times
- "I thought someone was watching" kills more children than anything else

LAYER 2: BARRIERS
- 4-sided pool fence, minimum 4 feet high, self-closing and
  self-latching gate
- The fence must isolate the pool from the house (a wall of the house
  does NOT count as one side of the fence)
- Remove anything a child could climb (chairs, tables, planters)
  from near the fence
- Door alarms on any house door that opens to the pool area

LAYER 3: SWIMMING ABILITY
- Swim lessons starting at age 1 (AAP now recommends)
- Swim lessons reduce drowning risk by 88% for children aged 1-4
- But swim lessons are NOT drown-proofing — supervision is still
  mandatory. Kids who "can swim" still drown.

LAYER 4: EMERGENCY PREPARATION
- CPR certification for all adults in the household
- Rescue equipment at poolside (life ring, reaching pole)
- Phone at poolside for 911 calls
- Post-pool headcount — know exactly how many kids were in the water
  and confirm they're all out

DRAIN SAFETY:
- Pool drains can trap hair, clothing, and limbs
- VGBA (Virginia Graeme Baker Act) requires anti-entrapment covers
  on all public pool drains
- For home pools: ensure your drain covers comply and are intact
- If a drain cover is missing or broken, do NOT use the pool

BATH/BUCKET SAFETY (infants and toddlers):
- A toddler can drown in a 5-gallon bucket
- Never leave a child alone in a bathtub — not for 10 seconds
- Empty all buckets, wading pools, and containers after use
- Toilet lid locks for homes with toddlers
```

## If This Fails

- User panics in water and can't float: This is what lessons are for. A written guide can teach concepts but the body needs practice. Find local swim lessons through the Red Cross, YMCA, or local recreation department. Many offer adult beginner classes specifically for people who never learned.
- User witnessed a drowning and couldn't help: Call 911 immediately. Throw anything that floats. Do not enter the water unless you are trained and have a flotation device. After the event, if the person was submerged, begin CPR if they're not breathing — even if you're not certified, compressions-only CPR is better than no CPR.
- User has a fear of water that prevents learning: Aquaphobia is real and common. A gradual exposure program with a patient instructor in a controlled environment (warm, shallow pool) is the standard treatment. Some areas have therapists who specialize in water phobia.
- CPR after water rescue: If the person isn't breathing, begin CPR. 30 compressions, 2 breaths, repeat. For drowning victims, rescue breaths are more important than in other cardiac arrest scenarios (the problem is usually oxygen deprivation, not cardiac).

## Rules

- Never leave children unattended near any body of water. Not for a second. Drowning is silent and takes less than 2 minutes.
- Never swim alone. Even strong swimmers can be incapacitated by cramps, medical events, or cold water shock.
- Never enter the water to rescue someone unless you are trained and have a flotation device. Double drowning is real and common.
- Alcohol and water don't mix. Alcohol is involved in up to 70% of adolescent and adult drowning deaths. It impairs judgment, balance, swimming ability, and cold tolerance.
- Life jackets for non-swimmers in any open water situation. Every time. No exceptions.

## Tips

- Float first, swim second. Teach every child and adult to float before teaching strokes. Floating keeps you alive. Strokes get you somewhere. Alive comes first.
- The safest-looking water is often the most dangerous. Rip currents appear calmer than surrounding surf. River undercurrents are invisible. Calm lake surfaces can hide cold thermoclines.
- Puddle jumpers and water wings give a false sense of security. They teach children to be vertical in water — the exact wrong position. Use Coast Guard-approved life jackets for children in open water.
- After any submersion incident where the person coughed, gagged, or had trouble breathing, go to the ER. Secondary drowning (fluid in the lungs causing inflammation hours later) is rare but fatal. Watch for coughing, fatigue, irritability, or difficulty breathing in the hours afterward.
- Cold water kills faster than deep water. A fall into 40F (4C) water gives you about 1 minute before cold shock makes swimming impossible. Wear a life jacket on any boat in cold water — you won't be able to put one on after you fall in.

## Agent State

```yaml
water_safety:
  user_swim_level: null
  level_1_complete: false
  level_2_complete: false
  level_3_complete: false
  competency_gaps: []
  has_children: null
  pool_at_home: null
  lives_near_water: null
  cpr_certified: null
  cpr_certification_date: null
pool_safety:
  fence_installed: null
  gate_self_closing: null
  door_alarms: null
  drain_covers_compliant: null
  rescue_equipment_poolside: null
  designated_water_watcher_system: null
family:
  children_swim_lessons_enrolled: null
  adults_cpr_certified: null
  life_jackets_for_all: null
```

## Automation Triggers

```yaml
triggers:
  - name: swim_lesson_recommendation
    condition: "water_safety.user_swim_level == null OR water_safety.level_1_complete IS false"
    action: "Based on your self-assessment, you're missing survival-level water competency. This is the highest-priority physical safety skill to develop. Let's find swim lessons near you — Red Cross, YMCA, or local rec centers all offer adult beginner classes."

  - name: pool_safety_audit
    condition: "water_safety.pool_at_home == true AND pool_safety.fence_installed IS null"
    action: "You have a home pool. Let's do a safety layer audit — fencing, alarms, drain covers, rescue equipment, and supervision protocols. Each layer is a barrier between a child and drowning."

  - name: cpr_recertification
    condition: "water_safety.cpr_certified == true AND months_since(water_safety.cpr_certification_date) > 24"
    schedule: "check quarterly"
    action: "Your CPR certification is over 2 years old. Skills degrade without practice. Time to recertify — most courses are 2-4 hours and cost $30-50."

  - name: seasonal_water_safety
    condition: "water_safety.has_children == true"
    schedule: "May 1 annually"
    action: "Summer is coming. Time for a water safety refresh: review supervision rules with all caregivers, check pool fence and equipment, confirm swim lesson enrollment, and verify life jacket fit for all children (they grow out of them)."
```
