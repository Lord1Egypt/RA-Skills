## Description:

Manage and publish agent skills on SkillHub and ClawHub. Best for developers and operators who need a repeatable workflow to search skills, inspect packages, authenticate securely, and publish local skill folders to a registry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codeblackhole1024](https://clawhub.ai/user/codeblackhole1024)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agents use this skill to search, inspect, authenticate with, and publish skills to SkillHub-compatible registries such as ClawHub through a repeatable CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide authenticated registry publishing with tokens and local skill files.

Mitigation: Use a least-privileged environment and confirm authentication state before publishing.

Risk: The skill uses unpinned `npx clawhub` CLI commands.

Mitigation: Use a vetted or pinned `clawhub` CLI version for publishing workflows.

Risk: The skill accepts custom registry URLs before login, search, inspect, or publish actions.

Mitigation: Verify the registry URL before sending credentials or source content.

## Reference(s):

- [SkillHub Manager Workflows](references/workflows.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts the user to confirm the target SkillHub registry before registry actions.]

## Skill Version(s):

1.0.3 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
