## Description:

Creates shift-specific sleep plans, post-shift commute guidance, and informational screening flags for shift workers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Night, rotating-shift, and on-call workers use the skill to plan sleep windows, naps, caffeine cutoffs, and light exposure around work schedules, and to assess post-shift commute risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shift schedules, sleep times, quality ratings, and notes are stored in a local JSON file.

Mitigation: Avoid entering sensitive health details you do not want stored locally and protect the file accordingly.

Risk: Screening flags may be mistaken for a medical diagnosis.

Mitigation: Treat screening as informational and seek occupational health or sleep-medicine advice for persistent symptoms.

## Reference(s):

- [Shift-Work Circadian Science](references/circadian-strategies.md)
- [Sleep Shift Survivor on ClawHub](https://clawhub.ai/voronindenis5/skills/sleep-shift-survivor)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dated sleep plans, commute warnings, and informational screening flags; schedules and sleep logs are stored locally.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
