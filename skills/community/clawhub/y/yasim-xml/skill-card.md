## Description:

Provide a detailed specification for writing YASim XML files. Use when the user requests to create or modify the FDM of a YASim aircraft.

This skill is ready for commercial/non-commercial use.

## Publisher:

[container32](https://clawhub.ai/user/container32)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and aircraft simulation authors use this skill to create or modify YASim aircraft flight dynamics model XML using aircraft geometry and performance characteristics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict is benign with medium confidence, and Skillspector's review was partial because many local-looking references could not be resolved.

Mitigation: Review the skill instructions before installation and assess them for the intended use.

Risk: YASim is a rough approximation; unsuitable geometry or performance targets can produce unstable or non-flyable results.

Mitigation: Use credible aircraft geometry and performance limits, then tune and validate the resulting flight model in FlightGear.

## Reference(s):

- [yasim-xml on ClawHub](https://clawhub.ai/container32/skills/yasim-xml)

## Skill Output:

**Output Type(s):** [Guidance, XML configuration]

**Output Format:** [Markdown guidance with YASim XML element descriptions and examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Aircraft-specific values require suitable geometry and performance data, followed by tuning.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
