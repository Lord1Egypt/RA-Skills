## Description:

Guides agents through creating, updating, scaffolding, and validating skills that extend agent capabilities with specialized workflows, knowledge, tools, and bundled resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chengxindl](https://clawhub.ai/user/chengxindl)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to design new skills, improve existing skill instructions, scaffold skill directories, and validate skill frontmatter and structure before release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled initializer can create persistent files at the requested output path.

Mitigation: Confirm the skill name and output directory before running it, then inspect generated files before deployment.

Risk: Generated or edited skill guidance may be incomplete, misleading, or unsuitable for the intended agent workflow.

Mitigation: Review the resulting skill instructions and run the bundled validator before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chengxindl/skills/skills-ttt)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and generated skill files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or create persistent skill files when the bundled initializer is run.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
