## Description:

Skill Router Pro helps an agent find existing local skills or search ClawHub before building a new skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kennyzir](https://clawhub.ai/user/kennyzir)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect a local skill index, search ClawHub for matching skills, and avoid creating duplicate skills when an existing local or marketplace skill can handle the task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated skill index can reveal local skill names, descriptions, and install paths.

Mitigation: Review the generated INDEX.md before sharing logs, screenshots, or workspace artifacts outside the environment.

Risk: The skill can guide an agent to search ClawHub and present install commands for third-party skills.

Mitigation: Review search results and install only skills whose publisher and behavior are acceptable for the environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kennyzir/skills/skill-router-pro)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown]

**Output Format:** [Markdown guidance with inline shell commands and tabular index entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local skill names, descriptions, install locations, ClawHub search results, and install commands.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
