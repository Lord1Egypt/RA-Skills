## Description:

Skill Picker helps agents discover and recommend agent skills based on user intent, including skill combinations, while only suggesting install commands for user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yao00oo](https://clawhub.ai/user/yao00oo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to find relevant skills for a task, compare fit, and receive user-run install commands. It is useful when a request would benefit from specialized agent capabilities or a workflow assembled from multiple skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run an unpinned npx skills search command when broad discovery triggers apply.

Mitigation: Use a pinned or locally installed audited skills CLI when possible, and require user approval before first-time package retrieval or proactive searches.

Risk: Skill recommendations and install commands could be mistaken for approved actions.

Mitigation: Keep installation as an explicit user action and review recommended skills before running any install command.

## Reference(s):

- [ClawHub Skill Picker page](https://clawhub.ai/yao00oo/skills/skill-picker)
- [Skills registry](https://skills.sh/)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides recommendations, fit rationale, and install commands for the user to run or explicitly confirm.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
