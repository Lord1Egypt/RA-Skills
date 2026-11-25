## Description:

Plans low-and-slow barbecue cooks backward from serving time, estimates cooking and fuel needs, and adjusts timing from thermometer readings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Home pitmasters use this skill to schedule smoked meats around a planned serving time, estimate cook and fuel needs, and adjust timing from live thermometer readings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags that tri-tip timing and probe guidance may fall below the skill's stated safety floor without accounting for carryover cooking.

Mitigation: Treat tri-tip recommendations as estimates, verify doneness with a reliable thermometer, and do not rely on the planner to assure food safety.

## Reference(s):

- [Smoker Pitmaster Planner ClawHub release](https://clawhub.ai/voronindenis5/skills/smoker-pitmaster-planner)
- [cook-physics.md](references/cook-physics.md)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text cook timeline, fuel estimates, and probe-mode timing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Estimates depend on meat, weight, pit temperature, and serving time; probe mode also uses elapsed time and current internal temperature.]

## Skill Version(s):

1.0.0 (source: frontmatter; target release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
