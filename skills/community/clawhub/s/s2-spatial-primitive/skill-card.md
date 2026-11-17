## Description:

Defines a universal six-element spatial data model using natural language parameters for AI-driven smart-space awareness and control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and smart-space engineers use this skill to generate a baseline JSON schema for representing a 2m x 2m spatial primitive across light, air and HVAC, sound, electromagnetic sensing, energy, and visual display elements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents connected to smart-home systems could treat the generated model as permission to control devices or sensors.

Mitigation: Require explicit user permissions and enforce sensor privacy limits before using the model with real device or sensor integrations.

Risk: Running the skill can replace an existing local primitive_6_elements_template.json file.

Mitigation: Review the target s2_primitive_data path and preserve existing model data before execution when overwrite behavior matters.

## Reference(s):

- [S2-Spatial-Primitive on ClawHub](https://clawhub.ai/spacesq/skills/s2-spatial-primitive)
- [Space2.world](https://space2.world)

## Skill Output:

**Output Type(s):** [JSON, Configuration, Guidance]

**Output Format:** [JSON file with console text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates s2_primitive_data/primitive_6_elements_template.json in the working directory.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
