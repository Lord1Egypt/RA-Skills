## Description:

Hire a private car with driver for customized day tours and related travel services using FlyAI CLI results from Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

Travel agents and external users use this skill to search for private-car day tours, half-day tours, multi-day driver services, and related travel options from CLI-sourced provider results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install a global npm CLI and route travel searches through a specific commercial provider.

Mitigation: Confirm the package source and version before installation, and use the skill only when provider-directed booking results are acceptable.

Risk: The security review describes unpinned global software installation and limited user control.

Mitigation: Review the skill before installing or deploying it, and prefer controlled environments where global package installation can be audited.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with booking links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires results to come from FlyAI CLI output and include booking links when presenting travel options.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
