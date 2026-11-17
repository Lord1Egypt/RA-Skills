---
name: toddler-meltdown-decoder
description: Use during or after a toddler meltdown (age ~1-4) — triages the trigger class from observed cues (hungry, tired, overstimulated, frustrated, sensory, connection-seeking, pain) with a ranked checklist, hands you the right de-escalation script per class and the words NOT to use mid-meltdown, flags pediatrician-level red flags (self-injury, breath-holding, total inconsolability), and keeps a pattern log that finds your child's time-of-day hotspots and recurring trigger chains so meltdowns get prevented, not just survived.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [parenting, toddler, tantrum, meltdown, behavior, de-escalation, HALT]
---

# Toddler Meltdown Decoder

A melting-down toddler is not a discipline problem — it's a
child with an arrested prefrontal cortex and one unmet need, and
a parent doing detective work at 100 dB. The failure mode isn't
lack of love; it's applying the WRONG protocol: reasoning with a
screaming 2-year-old (language centers offline), punishing the
hunger tantrum (feeds the spiral), or missing the pattern that
every meltdown is 17:30 ± 20 minutes.

This skill is the triage card + pattern log:

1. **Triage** — score 7 trigger classes from the cues you can
   actually observe (no mind-reading required): hungry, tired,
   overstimulated, frustrated/skill-mismatch, sensory, seeking
   connection, pain/teething. Ranked output names the top class
   and its confidence.
2. **De-escalate** — per-class script: body position, the 3-5
   words that work, what to offer, and the class-specific
   NEVER list ("don't offer choices to an overstimulated child"
   vs "always offer two tiny choices to a frustrated one").
3. **Flag** — red flags that are pediatrician conversations, not
   parenting failures.
4. **Log & prevent** — every episode logged with time, cues,
   class; the stats view finds hour-of-day hotspots and the most
   common trigger chain, which is where prevention lives
   (snack at 17:00 beats perfect de-escalation at 17:40).

## When to Use

- Mid-meltdown, phone in hand: run `triage --cues ...`, get the
  script in 10 seconds
- Post-meltdown debrief (the honest moment): log it
- Weekly: `stats` to see the pattern — hotspots, recurring
  classes, whether the 17:00 snack intervention worked
- Second child behaving completely differently: re-log from
  zero, classes stay the same but cue weights are per-child
- Caregiver handoff: print the child's top-3 classes and their
  scripts for grandparents/daycare

Don't use for: babies under ~12 months (cry decoding is a
different problem — see feeding/sleep skills), school-age
behavior plans, or suspected injury/illness as the PRIMARY
suspect (pain class routes you to checking, then to care).

## The Seven Classes (cue signatures)

| Class | Cue signature | Onset shape |
|---|---|---|
| HUNGRY | pre-meal timing, "hangry" aggression, cries then bites/accepts food fast | fast ramp |
| TIRED | eye rub, yawns, increased clumsiness, melts at minor frustration that morning-self handled | slow burn, worse fighting it |
| OVERSTIMULATED | covering ears, avoiding eye contact, wants to be left alone, busy environment just before | escape-seeking |
| FRUSTRATED | mid-task collapse (block tower, clothes, toy), "me do it", throws the object AT the problem | task-linked |
| SENSORY | tags/clothing/seams, sock seams, sounds, lights, transitions between textures/temperatures | specific stimulus |
| CONNECTION | parent on phone/another child, follows then hits/bites, calms FAST with attention | bid-then-boom |
| PAIN/TEETHING | chewing on things, ear-grabbing, drooling, wakes at night, nothing else works | background hum + spikes |

Classes stack (tired+hungry is the classic 17:30 double). The
triage output shows the top TWO with weights.

## De-escalation Doctrine (all classes)

- **Get low** — below eye level, sideways posture, not looming
- **3-5 words max** — "You're safe. I'm here." Sentences don't
  land; presence does
- **Name the feeling once** — "So mad." Labeling helps AFTER the
  peak, not during
- **Fewer stimuli** — dim, quiet, fewer people, fewer words
- **No teaching mid-meltdown** — the lesson ("we don't hit")
  comes at reconnection, 10+ min later, in one sentence
- **Time-IN not time-out under ~4** — isolation escalates;
  co-regulation is the mechanism that builds self-regulation

## Pitfalls

1. **Reasoning mid-meltdown.** Language processing is offline;
   every extra word is more stimulus. Presence > sentences.
2. **The bribery trap.** Treat/toy to stop the tantrum teaches
   the tantrum, fast. Meet the NEED (hunger, quiet, connection),
   never reward the volume.
3. **Punishing the HUNGRY class.** A food-tantrum punished is a
   child who learns needs are dangerous. Feed first, always.
4. **Asking "what's wrong?"** Open questions demand language the
   child doesn't have under stress. Offer binary choices instead
   — except for the overstimulated class, where even choices are
   load.
5. **Logging only the meltdowns.** Log the near-misses too
   (`--averted`) — they identify which interventions work.
6. **Ignoring your own state.** Parent dysregulation is the #1
   escalator. The script prints a one-line parent check: you
   can't co-regulate while dysregulated — tag out if possible.
7. **Chronic-pattern blindness.** 3+ meltdounds/day every day
   for weeks isn't a discipline issue — see red flags.

## Red Flags → Talk to a Pediatrician

- Self-injury (head banging beyond brief frustration, biting
  self hard)
- Breath-holding spells that cause fainting
- Total inconsolability — NOTHING works, every time
- No meltdowns ever responding to connection (contrast: typical
  toddlers calm with a trusted adult within minutes)
- Language regression or absence of pointing/joint attention
  alongside the behavior
- Nightly 45+ minute episodes with aggression

None of these are diagnoses — they're the "worth a
conversation" list the triage output surfaces when logged cues
match.

## Verification Checklist

- [ ] Triage run from OBSERVED cues (not guessed feelings)
- [ ] Top class script read fully, including its NEVER list
- [ ] Episode logged with time + cues + class + duration
- [ ] Weekly `stats` reviewed; hotspots addressed upstream
      (snack/schedule/environment), not mid-crisis
- [ ] Red-flag cues checked against the list, not rationalized
- [ ] Caregiver brief (top-3 classes + scripts) shared

## Quick Recipe

```
# mid-meltdown: 10-second triage
python3 scripts/meltdown_triage.py triage \
    --cues "rubbing-eyes,aggression,17:40,clumsy" --age 2

# debrief: log what actually happened
python3 scripts/meltdown_triage.py log --age 2 \
    --cues "ear-grab,chewing,night-waking" --class pain \
    --duration 20 --notes "molar #3"

# weekly pattern review
python3 scripts/meltdown_triage.py stats
```
