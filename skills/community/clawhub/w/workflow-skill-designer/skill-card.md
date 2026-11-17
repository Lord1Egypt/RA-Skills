## Description:

Creates structured workflow skills with a coordinating SKILL.md, progressively loaded phase files, task tracking patterns, and inter-phase data flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yumingtao](https://clawhub.ai/user/yumingtao)

### License/Terms of Use:

MIT

## Use Case:

Developers designing multi-step agent workflows use this skill to turn commands, requirements, existing skills, or a natural-language description into a coordinating SKILL.md and detailed phase files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that generated skills may be granted broad tools, including shell and file editing, beyond what their workflows need.

Mitigation: Review each generated skill's allowed tools and retain only the permissions required by its workflow.

Risk: The security review says some referenced content was only partly inspected.

Mitigation: Read the complete generated SKILL.md and phase files before using or sharing the skill.

## Reference(s):

- [Workflow Skill Designer on ClawHub](https://clawhub.ai/yumingtao/skills/workflow-skill-designer)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Configuration, Code, Shell commands]

**Output Format:** [Markdown skill package (SKILL.md and phase files)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Organized as a coordinator document and progressively loaded phase instructions; may include workflow configuration, tool guidance, code, or shell commands.]

## Skill Version(s):

1.3.1 (source: server-resolved ClawHub release metadata; artifact frontmatter lists 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
