## Description:

Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sundayslove](https://clawhub.ai/user/sundayslove)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to discover existing installable skills for specialized tasks and get guidance on finding, presenting, and installing relevant options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill steers agents toward mutable remote CLI execution for discovering and installing skills.

Mitigation: Use a pinned, trusted Skills CLI before running install commands.

Risk: Global installs and skipped confirmations can change the user's agent environment broadly.

Mitigation: Prefer local or scoped installs and avoid skipped confirmations unless that behavior is intentional.

Risk: Installed skills can introduce incorrect, misleading, or unsafe instructions.

Mitigation: Inspect target skill source before installation and review or scan skills before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sundayslove/skills/testskillhhh)
- [Skills directory](https://skills.sh/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include skill search suggestions, install commands, and links to skill listings.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
