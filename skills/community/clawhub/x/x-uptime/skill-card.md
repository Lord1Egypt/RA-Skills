## Description:

Enhanced uptime command guidance for x-cmd that helps agents request structured YAML output for system uptime, logged-in user count, and 1/5/15-minute load averages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwinjhlee](https://clawhub.ai/user/edwinjhlee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agents use this skill to inspect local system uptime and load through x-cmd, choosing structured YAML for parsing or raw uptime output when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a separately installed x-cmd dependency that is outside the submitted artifact.

Mitigation: Install x-cmd only from a trusted source and review that dependency before enabling the skill.

## Reference(s):

- [x-uptime ClawHub skill page](https://clawhub.ai/edwinjhlee/skills/x-uptime)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires x-cmd; supports YAML and raw uptime output modes.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
