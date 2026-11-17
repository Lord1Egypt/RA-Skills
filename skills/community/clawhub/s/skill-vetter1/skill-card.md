## Description:

Create, edit, improve, or audit AgentSkills, including SKILL.md files and skill directories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sundayslove](https://clawhub.ai/user/sundayslove)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to create, edit, validate, package, and audit agent skills and SKILL.md files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to create, edit, and package skill directories, which can introduce unwanted changes to SKILL.md or bundled files.

Mitigation: Work in a dedicated target directory and review every file diff before deploying or packaging the skill.

Risk: Packaged skill archives may include unintended private or local files if those files are present in the skill folder.

Mitigation: Keep secrets and local-only files out of skill folders and inspect the generated .skill archive before sharing.

Risk: The artifact includes an official tag, but server evidence does not prove trusted OpenClaw provenance.

Mitigation: Rely on server-resolved publisher and provenance fields, and do not treat the tag as proof of official ownership.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sundayslove/skills/skill-vetter1)
- [ClawHub publisher profile](https://clawhub.ai/user/sundayslove)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline code blocks and shell commands; may produce or modify skill files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review generated file changes and packaged archives before use or sharing.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
