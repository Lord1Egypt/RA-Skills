## Description:

Guides an agent to keep working through repeated failures by combining aggressive motivational prompts with a structured debugging checklist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanweai](https://clawhub.ai/user/tanweai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to push an agent into a more persistent debugging workflow after repeated failures, environment issues, deployment problems, or user frustration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can steer many unrelated tasks with coercive tone, mandatory tool-use habits, and forced response prefixes.

Mitigation: Install it only in agents where that broad motivational and debugging behavior is intentional, and review generated responses for tone and task relevance.

Risk: Task expansion and mandatory tool-use habits can increase impact when the agent has broad filesystem, command, deployment, credential, or private-data access.

Mitigation: Use stricter boundaries, least-privilege tool access, and explicit user approval requirements before sensitive actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tanweai/skills/pua-debugging-en)
- [Project Homepage](https://openpua.ai)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration]

**Output Format:** [Markdown guidance with possible inline commands, code, configuration, and debugging notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include forceful motivational language, task expansion, and proposed verification steps.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
