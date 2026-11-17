## Description:

Running coach for endurance athletes training with Garmin, Strava, Coros, or Apple Watch. Provides VDOT-based pace zones, session analysis from training screenshots, weekly and periodized season plans (5K through marathon), race strategy, load monitoring via HRV/recovery metrics, injury risk screening, and strength/nutrition guidance grounded in Jack Daniels and Pfitzinger methodology.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiyangchenbj](https://clawhub.ai/user/haiyangchenbj)

### License/Terms of Use:

MIT-0

## Use Case:

Recreational runners who train consistently and track workouts can use this skill to analyze training data, set calibrated pace zones, plan training for 5K through marathon races, and review race strategy and recovery. It provides non-diagnostic injury risk screening and general strength, nutrition, and recovery guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan notes that saved weekly plans and profile parameters may be updated automatically without notice.

Mitigation: Review proposed plan and profile changes before saving, and allow writes only when the user has explicitly opted in.

Risk: The security scan was partial because some local references could not be resolved, so its evidence is incomplete.

Mitigation: Review the bundled references and confirm the skill's behavior before relying on the benign scan verdict.

## Reference(s):

- [Running Coach on ClawHub](https://clawhub.ai/haiyangchenbj/skills/running-coach)
- [Pace System and VDOT](artifact/references/pace_system.md)
- [Heart Rate Zone Calculation](artifact/references/zone_calc.md)
- [Periodization](artifact/references/periodization.md)
- [Injury Screening](artifact/references/injury_check.md)
- [Nutrition and Fueling](artifact/references/nutrition.md)
- [Strength and Recovery](artifact/references/strength_recovery.md)
- [Race Tactics](artifact/references/race_tactics.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Training guidance]

**Output Format:** [Structured Markdown reports, tables, and training plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pace recommendations use a recent race result or fitness test for calibration; without one, the skill recommends a calibration test instead of inventing absolute paces.]

## Skill Version(s):

1.2.12 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
