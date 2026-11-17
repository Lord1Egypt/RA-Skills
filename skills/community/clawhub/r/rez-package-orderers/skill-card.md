## Description:

Guides developers through configuring Rez package orderers and diagnosing unexpected package or variant selections in successful resolves.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loonghao](https://clawhub.ai/user/loonghao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and studio engineers use this documentation to understand why Rez picks a particular package version, configure built-in or custom orderers, and verify how an orderer affects a resolve.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Changing package_orderers can alter future resolves, including variant selection.

Mitigation: Review configuration changes and compare resolves before and after applying an orderer.

Risk: Custom orderers run as Python configuration and can change package selection unexpectedly.

Mitigation: Review custom orderer code before use and prefer built-in orderers where possible.

## Reference(s):

- [Rez Package Orderers on ClawHub](https://clawhub.ai/loonghao/skills/rez-package-orderers)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Code]

**Output Format:** [Markdown with bash and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation only; does not install or execute code automatically.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
