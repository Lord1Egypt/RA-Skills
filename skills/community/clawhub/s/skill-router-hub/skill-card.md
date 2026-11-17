## Description:

Skill Router centralizes an index of installed skills, routes user questions to relevant specialized skills, and asks the agent to report skill usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yunzhouli-hub](https://clawhub.ai/user/yunzhouli-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Claude users use this skill to maintain a local index of installed skills, route user questions to matching specialized skills, and report which skills were used after a response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Global routing behavior can affect every agent response and may over-route or misroute requests.

Mitigation: Install only where global skill routing is desired, and review the routing rules before enabling the skill.

Risk: The generator scans local skill directories and can persist names and descriptions of installed or private skills into the generated router file.

Mitigation: Run the generator only against intended skill directories, review generated indexes before use, and avoid publishing router files that reveal private installed capabilities.

Risk: The skill requires a skill usage report after every response, which can add disclosure or operational noise.

Mitigation: Use it only in environments where per-response skill reporting is acceptable and expected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yunzhouli-hub/skills/skill-router-hub)
- [Anthropic skills repository](https://github.com/anthropics/skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with optional shell commands and generated SKILL.md content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a generated skill index based on locally installed skills and a usage-report directive for agent responses.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
