## Description:

Plan one night of telescope observing from a CSV of targets, a site given as coordinates, and a date.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raktikoo](https://clawhub.ai/user/raktikoo)

### License/Terms of Use:

MIT-0

## Use Case:

Astronomers and telescope users can prepare and rank a one-night observing list from target coordinates, site coordinates, and a date. The plan reports observable windows, airmass, best observing times, Moon separation, and reasons targets are unobservable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial and did not resolve a local path-like reference, so it may not cover every reference.

Mitigation: Review the referenced source and installation instructions before installing.

Risk: Observing windows use planning-grade approximations and assume an ideal flat horizon without weather or telescope limits.

Mitigation: Use the plan as a scheduling aid and verify time-critical or equipment-specific decisions with appropriate observatory tools.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/raktikoo/skills/tonight)
- [Installation repository listed in the skill instructions](https://github.com/RakTikoo/tonight)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [Printed plain-text summary and optional CSV file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports observing windows, ranking, airmass, best time, Moon separation, and unobservable reasons. Times are UTC; the local column is mean solar time.]

## Skill Version(s):

0.1.1 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
