## Description:

Helps drivers check tire pressure and tread depth using vehicle placard values, temperature-aware estimates, and a local maintenance log.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Drivers and vehicle-maintenance assistants use the skill to record placard pressures, assess tire readings and tread depth, and plan monthly checks. It offers educational estimates rather than vehicle-specific safety advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Estimated pressure targets or tread and TPMS screening may be mistaken for vehicle-specific safety advice.

Mitigation: Use the vehicle door placard or manual as authoritative; seek professional inspection for damage, abnormal wear, repeated pressure loss, or an unresolved TPMS warning.

Risk: The local log contains vehicle names, placard pressures, pressure checks, and tread measurements.

Mitigation: Protect or delete the local JSON file as appropriate, and avoid sharing it unintentionally.

Risk: Documentation overstates some advanced features.

Mitigation: Confirm the available commands and do not rely on the tool for advanced load or speed calculations or detailed TPMS diagnostics.

## Reference(s):

- [ClawHub release](https://clawhub.ai/voronindenis5/skills/tire-pressure-coach)
- [Tire Pressure Coach reference](references/tire-science.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Plain text with per-tire assessments, suggested pressure targets, and maintenance history]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pressure checks, tread measurements, and vehicle details are saved to a local JSON file.]

## Skill Version(s):

1.0.2 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
