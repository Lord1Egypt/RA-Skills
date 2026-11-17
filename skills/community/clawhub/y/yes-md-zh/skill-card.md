## Description:

YES.md 中文版 is a Chinese-language engineering governance skill that prompts agents to rely on evidence, use available tools, validate changes, and check related impact during debugging, development, configuration, deployment, API integration, and data-processing work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sstklen](https://clawhub.ai/user/sstklen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to enforce evidence-first troubleshooting, safe file and deployment changes, and verification before reporting task completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill activates broadly during engineering tasks and may push agents toward extra tool use and validation before conclusions.

Mitigation: Apply it to engineering workflows where evidence checks are useful, and keep validation proportional to task risk.

Risk: The guidance encourages file backups, command execution, and deployment checks, which can affect a working tree or runtime environment if followed carelessly.

Mitigation: Review proposed commands before execution, prefer non-destructive checks, and keep backups scoped to files being changed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sstklen/skills/yes-md-zh)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language agent behavior guidance with broad activation during engineering tasks.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
