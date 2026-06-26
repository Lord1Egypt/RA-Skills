---
name: sleep-hygiene-overhaul
description: >-
  Evidence-based sleep improvement protocol. Use when someone has trouble falling asleep, staying asleep, waking unrefreshed, or wants to optimize sleep quality without medication.
metadata:
  category: mind
  tagline: >-
    Fix your sleep in two weeks using evidence-based protocols — wind-down rituals, sleep anchoring, caffeine timing, and environment optimization
  display_name: "Sleep Hygiene Overhaul"
  openclaw:
    requires:
      tools: [calendar, filesystem]
    install: "npx clawhub install sleep-hygiene-overhaul"
---

# Sleep Hygiene Overhaul

Poor sleep is not a character flaw or a busyness badge. It is a reversible physiological problem in most cases. This protocol applies the evidence-based interventions with the strongest research support: sleep restriction, stimulus control, consistent timing, and environmental optimization. Most people see measurable improvement within 7-14 days. This skill addresses common sleep dysfunction — not clinical insomnia disorder, sleep apnea, or restless leg syndrome, which require medical evaluation.

## Sources & Verification

- Walker, M., *Why We Sleep: Unlocking the Power of Sleep and Dreams*, Scribner, 2017 — the most accessible synthesis of sleep science for general readers
- American Academy of Sleep Medicine (AASM) Clinical Practice Guidelines for Insomnia — the clinical standard for behavioral sleep interventions. aasm.org
- Edinger et al., "Cognitive behavioral therapy for adults with insomnia," *Sleep*, 2021 ([DOI: 10.5664/jsl.8558](https://doi.org/10.5664/jsl.8558)) — CBT-I outperforms sleep medication in long-term outcomes
- Czeisler, C.A., "Duration, timing and quality of sleep are each vital for health," *Sleep Health*, 2015 — consistent wake time as the strongest single lever
- Chang et al., "Evening use of light-emitting eReaders negatively affects sleep," *PNAS*, 2015 ([DOI: 10.1073/pnas.1418490112](https://doi.org/10.1073/pnas.1418490112)) — blue light suppresses melatonin
- Drake et al., "Caffeine effects on sleep taken 0, 3, or 6 hours before going to bed," *Journal of Clinical Sleep Medicine*, 2013 — caffeine 6 hours before bed cuts sleep by 1 hour
- National Sleep Foundation sleep duration recommendations: sleepfoundation.org — verified active March 2026

## When to Use

- User takes more than 30 minutes to fall asleep most nights
- Wakes multiple times during the night
- Wakes feeling unrefreshed even after 7-8 hours
- Relies on alarm clocks, caffeine, or willpower to function in the morning
- Has tried "sleep hygiene" advice before but inconsistently
- Wants to reduce reliance on melatonin, alcohol, or sleep aids
- Experiences regular Sunday-night insomnia or social jet lag

## Instructions

### Step 1: Sleep audit

**Agent action**: Ask the user each question below, one at a time. Record answers in agent state. Use the results to generate a personalized protocol with specific times filled in.

```
SLEEP AUDIT — answer honestly, no judgment

1. What time do you currently go to bed? (average)
2. What time do you currently wake up? (average on weekdays)
3. What time do you actually fall asleep after getting into bed?
4. How many times do you wake up during the night?
5. How do you feel within 30 minutes of waking?
   (1 = exhausted, 5 = alert and rested)
6. Do you use alcohol to help you sleep?
7. Do you use screens (phone, TV, laptop) in bed?
8. What time is your last caffeine most days?
9. Do you nap? If yes, how long and when?
10. Is your bedroom dark? Cool? Quiet?
```

**Scoring red flags** — if any apply, note them in state for the relevant protocol steps:
- Falls asleep in under 5 minutes: may be chronically sleep-deprived
- Wakes unrefreshed regardless of duration: possible sleep apnea (recommend doctor consult)
- Uses alcohol to sleep: address this first (Step 3 note)
- Last caffeine after 2pm: address in Step 4

### Step 2: Set your sleep anchor (do this first, everything else second)

The single most powerful intervention is a **consistent wake time** — 7 days a week, including weekends.

**Agent action**: Ask the user: "What time must you be awake for work or responsibilities?" Set a daily morning reminder at that time. Label it "sleep anchor — do not move this." Track wake time adherence in state.

```
SLEEP ANCHOR RULES:

1. Pick one wake time. Keep it every day, including weekends.
   Variation of more than 30 minutes breaks the system.

2. Do NOT try to "catch up" on sleep on weekends.
   "Sleep debt" caught up this way resets your anchor.

3. Get out of bed within 10 minutes of your alarm.
   Do not lie in bed trying to squeeze out more sleep.

4. Your body will correct bedtime naturally within 1-2 weeks
   once the anchor is consistent.

WHY THIS WORKS:
Your sleep drive (adenosine) builds from the moment you wake.
Consistent wake time = consistent sleep drive at the same hour
each night = falling asleep faster and sleeping deeper.
```

### Step 3: Build a 30-minute wind-down ritual

Your brain cannot switch from "go mode" to "sleep mode" instantly. You need a transition period.

**Agent action**: Help the user build their specific ritual from the menu below. Save the selected ritual to state. Set a daily reminder 35 minutes before their target bedtime labeled "wind-down start."

```
WIND-DOWN RITUAL BUILDER — pick 2-3 from each tier

START (35 min before bed):
[ ] Dim all lights in your home (or switch to lamps only)
[ ] Stop eating — digestion competes with sleep
[ ] Set out tomorrow's clothes, bag, keys
[ ] Write tomorrow's 3-item priority list

MIDDLE (20 min before bed):
[ ] Take a warm shower or bath (the body temperature drop
    afterward triggers sleep onset)
[ ] Read a physical book or e-ink reader (no backlit screens)
[ ] Do 5 minutes of gentle stretching or yoga
[ ] Write a "brain dump" — everything in your head, on paper

FINAL (10 min before bed):
[ ] Phone face-down, on charger outside the bedroom (or
    set to Do Not Disturb with exceptions only for true
    emergencies)
[ ] Drop bedroom temperature to 65-68F / 18-20C if possible
[ ] 4-7-8 breathing: inhale 4s, hold 7s, exhale 8s (x3)
[ ] No clock-checking — turn clocks away
```

### Step 4: Caffeine cutoff calculator

Caffeine has a half-life of 5-7 hours in most people (longer if you are over 50, on certain medications, or a slow metabolizer).

**Agent action**: Based on the user's target wake time, calculate their caffeine cutoff time and add it to their morning state notes.

```
CAFFEINE CUTOFF CALCULATOR:

Target bedtime: [user's bedtime]
Half-life: 6 hours (conservative average)

To have <25% caffeine remaining at bedtime:
  Last caffeine = bedtime minus 12 hours

EXAMPLES:
  Bedtime 10:30pm → last caffeine by 10:30am
  Bedtime 11:30pm → last caffeine by 11:30am
  Bedtime midnight → last caffeine by noon

HIDDEN CAFFEINE SOURCES:
  - Green tea: 25-45mg per cup
  - Dark chocolate: 12-25mg per ounce
  - "Decaf" coffee: 2-25mg per cup
  - Pre-workout and energy drinks: read the label
  - Some pain relievers (Excedrin): 65mg per tablet
```

### Step 5: Optimize the sleep environment

**Agent action**: Ask the user which of these they currently have and which they don't. Flag the missing ones that are free or low-cost to fix first.

```
SLEEP ENVIRONMENT CHECKLIST:

DARKNESS (most impactful after timing):
[ ] Blackout curtains or sleep mask
[ ] No LED indicator lights in the bedroom
    (cover with black electrical tape if needed)
[ ] No screen glow at all

TEMPERATURE:
[ ] Bedroom at 65-68F / 18-20C
[ ] Cooling options if you run hot: fan, lighter duvet,
    cotton sheets, open window

QUIET (or consistent noise):
[ ] White noise machine or fan (consistent noise > silence
    for most people — it masks irregular sounds)
[ ] Earplugs if partner snores

BED IS FOR SLEEP (stimulus control):
[ ] No working in bed
[ ] No watching TV in bed
[ ] No scrolling in bed
[ ] If you can't sleep after 20 minutes, GET UP.
    Do something boring in dim light until sleepy.
    Return to bed only when sleepy.
    (This feels counterintuitive — it works.)
```

### Step 6: Nap rules

Naps can pay down sleep debt without ruining night sleep — if done correctly.

```
SAFE NAP PROTOCOL:

- Maximum length: 20 minutes (set an alarm)
- Latest possible nap: 3pm (or 8+ hours before bedtime)
- Location: NOT your bed if possible (chair, couch)
- Do NOT nap if you have nighttime sleep onset problems --
  your sleep drive needs to build undisturbed

COFFEE NAP HACK (counterintuitive but evidence-backed):
  Drink a coffee immediately before a 20-min nap.
  Caffeine takes 20-30 min to absorb. You wake up
  just as it kicks in. More effective than either alone.
  (Horne & Reyner, "Sleep inertia," *Psychophysiology*, 1996)
```

### Step 7: Two-week check-in

**Agent action**: After 14 days, re-administer the sleep audit. Compare to baseline. Calculate sleep onset time improvement and wake-feeling score. If scores haven't improved on 2+ dimensions, prompt doctor consultation checklist.

```
TWO-WEEK PROGRESS CHECK:

Questions (compare to your audit answers):
1. How long does it take to fall asleep now?
2. How many times do you wake up?
3. How do you feel within 30 minutes of waking? (1-5)
4. Are you keeping your wake anchor time? (days per week)

IF NO IMPROVEMENT after 14 days with anchor + environment fixes:
  Consider: sleep apnea screening (ask your doctor about a
  home sleep test — many insurers cover these), or
  a referral to a sleep medicine specialist for CBT-I
  (Cognitive Behavioral Therapy for Insomnia — more effective
  than any medication, no side effects).
```

## If This Fails

1. **Waking unrefreshed no matter what**: Snoring, gasping in sleep, or being told you stop breathing are signs of sleep apnea. This skill cannot address that. Ask your doctor about a home sleep study.
2. **Can't stop racing thoughts at night**: This is anxiety driving sleep problems, not sleep driving anxiety. See the anxiety-emergency skill. Consider a referral for CBT-I, which specifically addresses rumination at bedtime.
3. **Tried everything and still struggling**: Ask your doctor about CBT-I (Cognitive Behavioral Therapy for Insomnia). The American College of Physicians recommends CBT-I as first-line treatment over sleep medication. Find a provider at the Society of Behavioral Sleep Medicine: behavioralsleep.org
4. **Using alcohol to sleep**: Alcohol reduces sleep quality by suppressing REM sleep in the second half of the night. You'll fall asleep faster and wake up exhausted. Removing alcohol often causes a 2-3 night rebound of worse sleep before improvement. Know this going in.

## Rules

- Never recommend prescription sleep medication — this skill is behavioral, not pharmacological
- Never dismiss sleep problems as "you just need to relax" — sleep dysfunction has physiological drivers
- Always flag waking-unrefreshed + snoring as a potential medical issue requiring doctor evaluation
- Progress takes 7-14 days — set this expectation upfront to prevent early abandonment

## Tips

- The single most impactful change for most people is wake-time consistency, not bedtime. Fix the anchor first.
- Warm showers work because cooling down after warmth is a sleep trigger, not the warmth itself.
- Weekend "sleep ins" of even 90 minutes shift your circadian rhythm by the equivalent of mild jet lag.
- Blue light from screens suppresses melatonin for 1-3 hours. The issue isn't just brightness — it's the wavelength.
- If a user is on shift work, overnight care duty, or across time zones regularly, this protocol needs modification — their situation requires circadian rhythm management, not just sleep hygiene.

## Agent State

Persist across sessions:

```yaml
sleep:
  audit:
    bedtime_current: null
    wake_time_current: null
    sleep_onset_minutes: null
    night_wakings: null
    morning_feel_score: null
    uses_alcohol: null
    uses_screens_in_bed: null
    last_caffeine_time: null
    naps: null
    environment_dark: null
    environment_cool: null
    environment_quiet: null
    audit_date: null
  sleep_anchor_time: null
  anchor_adherence_days: 0
  wind_down_ritual: []
  caffeine_cutoff_time: null
  protocol_start_date: null
  checkin_scores: []
  flags:
    possible_sleep_apnea: false
    alcohol_dependency: false
    anxiety_driven: false
```

## Automation Triggers

```yaml
triggers:
  - name: morning_anchor_reminder
    condition: "sleep_anchor_time IS SET"
    schedule: "daily at sleep_anchor_time"
    action: "Good morning. Time to get up — keeping this consistent is the most important thing you can do for your sleep. How did last night go? (1-5)"

  - name: wind_down_start
    condition: "wind_down_ritual IS SET"
    schedule: "daily 35 minutes before target bedtime"
    action: "Wind-down time. Dim your lights now and start wrapping up. Screens off in 25 minutes."

  - name: screen_off_reminder
    condition: "wind_down_ritual IS SET"
    schedule: "daily 10 minutes before target bedtime"
    action: "Screens off now. Phone on charger, face down. Bedroom temp check. 4-7-8 breathing when ready."

  - name: two_week_checkin
    condition: "protocol_start_date IS SET"
    schedule: "14 days after protocol_start_date"
    action: "Two-week check-in. Let's re-run the sleep audit and see how things have changed. Ready?"

  - name: sleep_apnea_flag
    condition: "audit.morning_feel_score <= 2 AND audit.sleep_onset_minutes < 5"
    action: "Falling asleep very fast AND waking unrefreshed can indicate sleep deprivation from disrupted sleep architecture. If you or anyone near you has noticed snoring or pauses in breathing, mention this to your doctor."
```
