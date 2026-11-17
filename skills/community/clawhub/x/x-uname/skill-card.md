## Description:

x-uname provides an enhanced uname command with colorized, structured output for hostname, operating system, kernel, architecture, and version.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwinjhlee](https://clawhub.ai/user/edwinjhlee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and system operators use this skill to run x-cmd's structured uname command and inspect local system identity and platform details in a readable format.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The command output can reveal diagnostic system information such as hostname, kernel version, architecture, and full operating system version.

Mitigation: Avoid posting the output in public logs, chats, or tickets when those details are sensitive in the user's environment.

Risk: The skill depends on the separate x-cmd module for installation and operation.

Mitigation: Review the x-cmd dependency and its installation path before deploying this skill.

## Reference(s):

- [x-uname ClawHub skill page](https://clawhub.ai/edwinjhlee/skills/x-uname)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash command examples and tabular field descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The documented command output may include local hostname, kernel version, architecture, and full operating system version.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
