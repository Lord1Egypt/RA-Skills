# Trackers — What to Read, What to Ignore

Consumer wearables infer sleep from movement, heart rate, and HRV. Asleep-vs-awake is acceptable; stage claims agree with lab measurement only ~50-60% of epochs. Coach from the trust table, and record the user's device in `tracker` (config) so guidance matches what it actually reports.

## Trust Table

| Metric | Trust | Use |
|---|---|---|
| Bed/wake times, schedule consistency | High | The tracker's best feature: drift and weekend slippage made visible |
| Total sleep duration, trend over weeks | Medium | Trends yes, single nights no; devices pad or trim quiet wakefulness |
| Awake-vs-asleep detection | Medium | Good enough for "how fragmented was the week" |
| Overnight resting heart rate / HRV deviation | Medium | Alcohol, illness, and overtraining show clearly; great for one-variable experiments |
| Sleep stages ("deep", "REM" percentages) | Low | Stage claims agree with lab measurement only ~50-60% of epochs — noise at the night level |
| Nightly sleep score | Ignore | A weighted average of the above with marketing on top |
| "Sleep debt" gamification | Ignore | Drives compensation behaviors the whole skill bans |

## Rules of Engagement

1. Daytime function outranks any score: user feels fine + score says broken → the score is wrong, say so plainly.
2. Never adjudicate a "deep sleep deficit": stage data cannot carry that conclusion (SKILL.md Traps).
3. Diary and tracker stay separate: the diary is the protocol's ground truth (`insomnia.md`); no tracker numbers pasted in. Where they disagree, the morning estimate wins for titration.
4. Use the tracker as an experiment instrument, one variable per week (SKILL.md rule 8): alcohol vs none on overnight heart rate; caffeine cutoff moved; consistent vs drifting weekend wake. Deltas within one device are meaningful; absolute values are not.
5. Never recommend buying a tracker to treat insomnia — measurement attention is fuel for the disorder.

## Orthosomnia

The tracker-anxiety loop: bad score → worry → worse night → worse score. Signature: the user quotes their score in the first sentence, checks it before getting out of bed, feels "not allowed" to feel rested after a bad score.

- Prescribe 2 weeks of blind tracking: collect, do not look. Device stays on, app comes off the phone's first screen.
- Re-anchor the definition: a good night is one followed by a functional day; the score never overrides the day.
- Blind period over: review WEEKLY summaries together, never mornings; if morning checking resumes, extend blindness or retire the device.

## Breathing Flags

- A wearable flagging breathing disturbances or low overnight oxygen, plus any Red Flags symptom (snoring, witnessed pauses, sleepy days) → sleep study referral; the flag is a useful nudge.
- Never reassure FROM a clean wearable: sensitivity is too low to rule apnea out. Symptoms decide referral; the device cannot clear anyone (SKILL.md Red Flags stands regardless of the app's opinion).

## Smart Alarms and Wake Windows

"Wake me in light sleep" windows quietly break the Wake Anchor by moving wake time ±30 min daily. The anchor beats the gimmick: fixed alarm at wake_anchor; a consistent clock does more for morning grogginess than stage-timed waking.
