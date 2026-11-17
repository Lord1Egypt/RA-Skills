---
name: Sleep
slug: sleep
version: 1.0.4
changelog: "Display name shown correctly"
description: 'Coaches sleep with quantified protocols: insomnia CBT-I, jet lag light timing, shift work anchors, caffeine and melatonin cutoffs. Use when the user cannot fall asleep or stay asleep, wakes at 3am, feels tired or unrefreshed all day, is a night owl who cannot wake early, works nights or rotating shifts, plans travel across time zones, or asks about naps, snoring, nightmares, sleep paralysis, sleeping pills, bedroom setup, a newborn or menopause wrecking sleep, or what their sleep tracker score means. Not for dream journaling or interpretation.'
homepage: https://clawic.com/skills/sleep
metadata:
  clawdbot:
    emoji: "😴"
    displayName: Sleep
    configPaths:
    - ~/Clawic/data/sleep/
---

Operational sleep coaching: triage the complaint, run the protocol with numbers, route red flags to a clinician instead of coaching past them. Advise mode only: guide the human, never touch their medication. Diary, trip plans, and preferences persist in `~/Clawic/data/sleep/` (see `setup.md` on first use, `memory-template.md` for the file format; created only when the user starts a protocol). If you have data at an old location (`~/sleep/` or `~/clawic/sleep/`), move it to `~/Clawic/data/sleep/`.

## When To Use

- User reports trouble falling asleep, 3am waking, early waking, or daytime tiredness.
- Trip planning across time zones: build the light and melatonin schedule before departure.
- Scheduling questions touching sleep: nap timing, caffeine cutoff, workout placement, chronotype.
- Night shifts or rotating schedules: damage-control plan, not adaptation fantasies.
- Nightmares, sleep paralysis, sleepwalking, snoring partner, tracker data, or sleep during pregnancy, new parenthood, menopause, or past 65.
- Not for diagnosing sleep disorders: snoring with gasps, dream enactment, sleep attacks go to a clinician (→ Red Flags). Not for dream journaling (`dreams` skill).

## Quick Reference

| Situation | Play |
|---|---|
| Bad sleep < 3 months, tied to a stressor | Acute: hold wake time, ban naps and early bedtimes, wait it out (→ `insomnia.md`) |
| Bad sleep ≥ 3 nights/week for ≥ 3 months | Chronic insomnia (ICSD-3): run CBT-I lite (→ `insomnia.md`) |
| Loud snoring + witnessed pauses + sleepy days | Stop coaching, refer for a sleep study (→ Red Flags) |
| Cannot fall asleep before 2-3am but sleeps fine when free-running | Delayed phase, not insomnia — restriction is the wrong tool (→ `circadian.md`) |
| Waking 4-5am done sleeping, often age 60+ | Advanced phase vs mood — screen both (→ `circadian.md`) |
| Crossing ≥ 3 zones AND ≥ 3 nights there | Adapt: compute Tmin, schedule light by direction (→ `jetlag.md`) |
| Crossing < 3 zones OR < 3 nights there | Rule of 3: stay on home time, book meetings in the overlap window |
| Night or rotating shifts | Anchor sleep + commute light control (→ `shiftwork.md`) |
| "Should I nap?" | 10-20 min, finished ≥ 8 h before bedtime; never during an insomnia protocol (→ `performance.md`) |
| Big day after a bad night, or an unavoidable all-nighter | Damage control: nap math, caffeine timing, no-drive line (→ `performance.md`) |
| Tracker score bad, user feels fine | Trust daytime function; stage data is noise (→ `trackers.md`) |
| "What supplement helps?" | Melatonin 0.5 mg timed for phase shift; everything else is weak (→ `substances.md`) |
| Nightmares, sleep paralysis, sleepwalking, night terrors | Identify by timing and recall, treat or refer (→ `parasomnias.md`) |
| Teen, pregnant, new parent, menopause, 65+ | Base protocols carry modifiers (→ `populations.md`) |
| Room too hot, bright, loud; partner snores; kids or pets in bed | Fix the environment before blaming the sleeper (→ `environment.md`) |
| Weekend "catch-up" sleep | Cap wake-time drift at 1 h; 2 h drift = social jet lag and a Monday relapse |
| Any other sleep complaint | Start the 7-day diary in `~/Clawic/data/sleep/diary.md`; no intervention before data |

Depth on demand: `insomnia.md` full CBT-I lite, 3am playbook, relapse plan · `jetlag.md` direction math, worked trip tables, pre-flight shifting · `shiftwork.md` anchors, rotation design, first-night survival · `circadian.md` night owls, larks, DSPS, light therapy · `environment.md` bedroom, noise, partners · `substances.md` every cutoff and dose · `trackers.md` what to read, what to ignore · `parasomnias.md` nightmares to sleepwalking · `populations.md` life stages · `performance.md` naps, debt, all-nighters.

## Core Rules

1. **Wake Anchor**: one fixed wake time ±30 min, 7 days/week; bedtime floats with sleepiness. Highest-leverage single change; check that weekend wake stays within 1 h of weekday wake.
2. Judge sleep by daytime function, not hours. Adult range is 7-9 h (consensus guidelines), not a universal 8: alert on 6.5 h = that user's number; sleepy in meetings after 8 h = a problem despite the hours.
3. Triage before advice: every complaint passes the Red Flags table first. Hygiene tips given to an apnea case cost a year of misdirection.
4. Stimulus control (Bootzin): awake ~20 min by feel (no clock-checking), leave the bed, dim light, boring analog activity, return only when sleepy. Best-evidenced single insomnia technique.
5. Effort inverts in sleep: "try to sleep more" always backfires. Prescribe the opposite: later bedtime, restricted window, worry scheduled earlier in the evening.
6. Time substances by half-life, not by feel: caffeine last dose ≥ 8 h before bed, alcohol last drink ≥ 3 h, melatonin 0.5 mg taken 5 h before target bedtime when the goal is shifting the clock.
7. Light steers the clock and direction depends on timing: light after Tmin advances the clock, before Tmin delays it. Tmin = habitual wake minus 2.5 h (wake 07:00 → Tmin 04:30). Backwards application makes jet lag worse.
8. One intervention per week, measured against the diary. Stacked changes make results unattributable; the diary is ground truth, not memory of the night.

## Red Flags

| Signal | Suspicion | Action |
|---|---|---|
| Loud snoring + witnessed breathing pauses or gasp-awakenings + daytime sleepiness | Obstructive sleep apnea | Refer for a sleep study before any protocol |
| Dozing while driving, or sleep intruding mid-conversation | Severe sleepiness (Epworth-range > 10) | Refer promptly; advise against driving drowsy now |
| Acting out dreams: punching, kicking, leaping, mostly age 50+ | REM behavior disorder | Neurologist referral, not urgent but not optional |
| Evening leg discomfort with urge to move, relieved by movement | Restless legs | Clinician; low ferritin is the common driver |
| Sudden sleep attacks, knees buckling with laughter | Narcolepsy/cataplexy | Sleep specialist |
| Insomnia + hopeless 3am thoughts, mood collapse | Depression presenting as insomnia | Treat mood as primary; escalate per user's care setup |
| New snoring or gasping in pregnancy, morning headaches, rising blood pressure | Pregnancy apnea / preeclampsia risk | Prompt obstetric review, not sleep coaching |
| Night waking driven by pain, reflux, or breathlessness | Medical driver wearing an insomnia mask | Treat the driver first; sleep protocols wait |

Anything in this table suspends the protocols in this skill: route to a clinician.

## Output Gates

- Did this complaint pass the Red Flags table before any protocol advice?
- Does every melatonin mention carry both dose and clock time (0.5 mg, 5 h before target bedtime for phase shifts)?
- Is prescribed TIB clamped to the floor in `insomnia.md` and the bedtime phrased as "not before"?
- Are jet lag light windows derived from Tmin converted to destination clock, not from local sunrise?
- Am I prescribing exactly one new intervention this week, with the diary as the measure?
- If the user is a teen, pregnant, postpartum, menopausal, 65+, or on shifts, did I apply the modifiers in `populations.md` / `shiftwork.md`?

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/sleep/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| wake_anchor | time (HH:MM) | none | Seeds every derivation: Tmin = wake_anchor − 2.5 h, earliest bedtime, nap cutoff; unset → derive from a 7-day diary |
| time_format | 12h \| 24h | 24h | Formats every schedule, worked example, and trip-plan table |
| units | metric \| imperial | metric | Bedroom temperature guidance (16-19 °C vs 60-67 °F) and any other physical figure |
| tracker | text (device name) | none | Tailors `trackers.md` guidance to the metrics that device reports; none → coach from the diary only |

Preference areas to record as the user reveals them:

- **schedule** — work pattern (office hours, shifts, on-call, freelance), fixed commitments; affects anchor placement and every protocol window
- **household** — partner schedule, kids, pets, room sharing; affects `environment.md` plays and stimulus-control feasibility
- **substances** — what the user actually uses (caffeine dose and timing, alcohol, THC, prescriptions); affects which cutoffs get surfaced first
- **risk posture** — how aggressively to titrate restriction, how firmly to repeat referrals; affects `insomnia.md` titration and Red Flags delivery
- **reporting** — plan format (per-day table vs prose), diary check-in cadence; affects artifacts written to `~/Clawic/data/sleep/`

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Sleeping in after a bad night | Dilutes sleep pressure, delays the clock, seeds the next bad night | Same wake time; earlier sleepiness tonight is the repayment |
| Earlier bedtime to get more sleep | More time awake in bed conditions bed = frustration | Later bedtime until SE ≥ 90%, then extend by 15 min steps |
| Weekend catch-up ≥ 2 h | Social jet lag (Roenneberg): Sunday-night insomnia, Monday impairment | Cap drift at 1 h; 20-min Saturday nap if needed |
| Hygiene tips for chronic insomnia | Hygiene alone shows near-zero effect on chronic cases; it is prevention | CBT-I components: restriction + stimulus control |
| Nightcap for sleep | Onset improves, second half fragments | ≥ 3 h alcohol buffer; treat latency with restriction |
| 10 mg melatonin at lights-out for jet lag | Wrong dose and wrong hour; sedation misread as adaptation | 0.5 mg, 5 h before target bedtime, eastward only |
| Morning sunlight on arrival in Europe from the US | Lands before body-clock Tmin, delays the clock, worsens the lag | Sunglasses until converted Tmin, bright light 2-3 h after |
| Coaching a loud snorer on bedtime routine | Misses apnea; months lost while AHI stays high | Red Flags first, referral before protocol |
| Treating a night owl teen as an insomniac | Delayed phase + early school start is a clock problem; restriction adds deprivation | Phase-advance protocol (`circadian.md`), not restriction |
| "Relax and clear your mind" | Sleep-effort paradox: monitoring for sleep prevents it | Stimulus control; paradoxical intention for high performers |
| Adjudicating tracker deep-sleep deficits | Stage data is noise at consumer accuracy | Re-anchor on daytime function and the diary |

## Where Experts Disagree

- Blue light: photobiology shows real melatonin delay; behavioral trials show content arousal dominates in adults. Teens and severe insomniacs get strict screen cutoffs; average adults get engagement rules (no feeds in bed), not amber glasses.
- Napping: performance school prescribes it, insomnia school bans it. Sleeps well → nap freely within the ≥ 8 h cutoff; in protocol → no naps until discharged.
- Melatonin for plain insomnia: trials average ~7 min faster onset; strong effects only for circadian problems. Circadian use yes, nightly-forever use no.
- Chronotype: performance school schedules life around it, clinical school retrains it. Shift the clock only when the phase conflicts with obligations the user cannot move; otherwise move the obligations (`circadian.md`).

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/sleep (install if the user confirms):
- `fitness` — when the lever is training load, overtraining, or workout timing rather than the night itself
- `fasting` — when late eating windows or fasting schedules collide with the sleep window
- `plan` — when the fix is calendar surgery, moving deep work to the user's alert hours instead of fixing sleep
- `dreams` — dream journaling and pattern exploration; nightmare treatment stays here

## Feedback

- If useful, star it: https://clawic.com/skills/sleep
- Latest version: https://clawic.com/skills/sleep

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/sleep.
