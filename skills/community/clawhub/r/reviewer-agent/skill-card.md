## Description:

Reviewer Agent provides an independent review perspective for projects, checking quality, maintainability, and progress control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nic-yuan](https://clawhub.ai/user/nic-yuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project maintainers use this skill to review project completion claims, code quality, communication, efficiency, and maintainability from an independent perspective.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Review reports are written locally and review conclusions may be sent through Feishu with broad activation and weak scoping.

Mitigation: Require explicit approval before Feishu notification, define the content and recipient, and narrow triggers before use.

Risk: The helper script accepts project names and uses them to inspect local skill directories.

Mitigation: Validate project names and restrict review scope to intended workspace paths.

## Reference(s):


## Skill Output:

**Output Type(s):** [Analysis, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown review report with scored findings and actionable recommendations; helper script output is shell text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes review reports locally and may send review conclusions through Feishu.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
