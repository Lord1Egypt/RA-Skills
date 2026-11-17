# Insomnia — Triage to Discharge (CBT-I Lite)

Split by the 3-3 line: ≥ 3 nights/week for ≥ 3 months = chronic (ICSD-3); anything less is acute. The two arms get opposite energy: acute is watchful restraint, chronic is a structured protocol.

## Acute (most cases, self-resolving)

The job is preventing chronification, not fixing tonight.

- Hold the Wake Anchor even after a terrible night.
- Ban compensation: no naps, no earlier bedtime, no sleeping in, no nightcap. Compensation converts 2 bad weeks into 2 bad years.
- Name the mechanism to the user: a stressor plus a few bad nights is normal; the disorder starts when the person starts *trying* to sleep.
- Stressor gone but insomnia persists 4+ weeks → start the diary and treat as pre-chronic.

## The Diary (ground truth)

Diary 7 days before any chronic-arm intervention, one line per night in `~/Clawic/data/sleep/diary.md`:

`date | in bed | lights out | min to fall asleep | wakes (n, min) | final wake | out of bed | naps | caffeine last | alcohol`

- Filled each morning from estimates; no tracker data pasted in (`trackers.md` explains why).
- Estimates beat precision: clock-checking to "get the diary right" feeds the disorder. Hide the clock, guess in the morning.
- Compute sleep efficiency SE = total sleep time / time in bed. SE ≥ 85% is healthy; SE < 85% triggers restriction.

## Contraindications (check before restricting)

Do NOT run restriction with: bipolar or mania history, seizure disorder, suspected apnea, pregnancy, or a safety-critical week (commercial driving, machinery); refer instead. Prescribed sleep medication is untouchable; coaching runs alongside, tapering is the prescriber's job (`substances.md`). Suspected delayed or advanced phase → `circadian.md` first; restriction on a mistimed clock adds deprivation without fixing timing.

## Sleep Restriction

1. Prescribed TIB = average diary TST rounded to 15 min, clamped to the floor: 5 h (5.5 h if age 65+, long commute, or safety-adjacent job). The floor is a clamp, never an exit: diary TST 4 h 30 → prescribe 5 h 00 and continue.
2. Worked example: TST 5 h 50, TIB 8 h 30 → SE 69%. Prescribe TIB 5 h 45 (350 min rounded to 15 min), wake fixed 06:30 → earliest bedtime 00:45. Bedtime is a "not before" line; sleepiness is the entry ticket, fatigue is not sleepiness.
3. Weekly titration from the diary: SE ≥ 90% → extend TIB 15 min; 85% ≤ SE < 90% → hold; SE < 85% → cut 15 min (never below floor). A week with 3+ violations (naps, sleep-ins, early bedtimes) is re-run, not titrated on.
4. Weeks 1-2 feel worse: sleepier days are the mechanism (pressure building); say so upfront or the user quits at day 5. Warn about drowsy driving during this phase.
5. No improvement by week 4 with clean adherence → stop and refer to a CBT-I clinician.
6. Discharge at 4 straight weeks SE ≥ 85% with good daytime function. Keep forever: Wake Anchor + out-of-bed rule.

## Stimulus Control (runs alongside restriction)

Bootzin's full set — the bed must predict sleep and nothing else:

1. Bed only for sleep and sex: no phone, no laptop, no worrying, no eating.
2. Go to bed only when sleepy (eyelids heavy, head nodding) — never merely tired, and never "because it's time".
3. Awake ~20 min by feel (no clock-checking): leave the bed, dim light, boring analog activity (paper book, folding laundry), return only when sleepy. Repeat as often as needed; five round trips in one night is the protocol working, not failing.
4. No naps while in protocol.
5. Wake Anchor regardless of the night.

## The 3am Playbook

Middle-of-the-night waking, the most common single complaint:

- Waking between cycles is normal physiology; the problem is what happens next. The fork: return to drowsy (fine) vs snap to alert (conditioned arousal).
- No clock, no phone. Knowing it's 3:12 adds arithmetic panic ("only 3 h left"); the lit screen adds light and content arousal.
- Alert after ~20 min by feel → out-of-bed rule, exactly as at sleep onset.
- Same thought looping → it goes on tomorrow's worry list by title only; the 3am brain gets no editorial session.
- Repeated waking at the same early hour with dread or hopeless content → screen mood (SKILL.md Red Flags row 6). Early-morning awakening is a classic depression signature.

## Racing Mind Toolkit

- **Worry scheduling**: 15 min early evening, paper, two columns — worry → next physical action. Closed notebook = closed office; at night, "it's on the list" is the full response.
- **Paradoxical intention** for high performers: try to stay awake (eyes open in the dark, no media). Removes sleep effort; effort was the obstacle.
- **Cognitive reframe** for the catastrophizers: one bad night costs less than the panic about it predicts (`performance.md` has the numbers). The belief "8 hours or I'm ruined" is itself a driver.
- Relaxation (slow breathing, progressive muscle release) is an adjunct: fine as a wind-down, not a treatment for chronic insomnia on its own.

## Relapse Plan (give at discharge)

- 3 bad nights/week for 2 weeks → restart the diary.
- 2 more weeks like that → restart restriction at the last TIB that worked.
- Rehearse the first move now: "hold wake time, no compensation" — relapses are lost in the first compensating week, not the first bad night.

Falling asleep in < 5 min routinely is sleep deprivation, not talent; treat as a duration problem (`performance.md`).
