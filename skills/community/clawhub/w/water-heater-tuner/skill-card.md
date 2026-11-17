## Description:

Helps households choose a residential water-heater setpoint by balancing scald risk, Legionella prevention, energy use, vacation planning, and shower recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Householders and their advisers use this skill to compare tank-water-heater setpoints, estimate energy savings and shower recovery, and plan safe operation after periods of non-use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A saved household profile contains occupant details, heater settings, location, and optional bill information.

Mitigation: Review and protect the local heater_profile.json file; delete it when no longer needed.

Risk: Incorrect water temperatures can increase scald or Legionella exposure, especially for vulnerable occupants.

Mitigation: Verify temperatures at fixtures and consult a licensed professional for vulnerable-household concerns or changes to gas equipment, valves, or plumbing.

## Reference(s):

- [Water Heater Tuner — Reference](artifact/references/heater-science.md)
- [Water Heater Tuner on ClawHub](https://clawhub.ai/voronindenis5/skills/water-heater-tuner)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown and command-line text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setpoint recommendations, energy and recovery estimates, pasteurization instructions, and vacation plans; the profile command stores household details locally.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; bundled frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
