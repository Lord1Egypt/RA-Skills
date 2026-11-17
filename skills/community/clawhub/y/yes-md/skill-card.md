## Description:

YES.md is an engineering-process skill that prompts an agent to gather evidence, use available tools, verify changes, and consider safety before completing development, debugging, configuration, database, or deployment work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sstklen](https://clawhub.ai/user/sstklen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill as process guidance for code changes, debugging, configuration work, database work, and deployments where evidence gathering and verification are important.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can activate very often and steer routine engineering work.

Mitigation: Narrow the trigger scope before using it on real projects.

Risk: The skill may force unnecessary tool use or actions beyond what the user authorized.

Mitigation: Make tool use conditional on user authorization and least privilege.

Risk: The skill instructs agents to create adjacent backups of configuration files, which can expose secrets in plaintext.

Mitigation: Avoid automatic adjacent backups of .env, secrets, keys, or deployment configs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sstklen/skills/yes-md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown, configuration]

**Output Format:** [Markdown guidance with inline shell commands and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May steer agent behavior by requiring evidence gathering, tool use, backups, and post-change verification.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
