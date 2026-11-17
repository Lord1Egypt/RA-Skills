## Description:

Generates complete AgentSkill packages from user requirements, including SKILL.md, scripts, references, asset folders, packaging, and ClawHub upload guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timyljob2011-sudo](https://clawhub.ai/user/timyljob2011-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this agent skill to turn a requested capability into a structured AgentSkill package with documentation, optional helper scripts, metadata, and packaging guidance for ClawHub distribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Packaging can accidentally include files outside the intended skill folder.

Mitigation: Use a dedicated empty workspace, inspect the skill folder for symlinks before packaging, and list generated ZIP contents before upload.

Risk: Generated skill packages may contain placeholder or inaccurate documentation, metadata, or scripts.

Mitigation: Review generated SKILL.md, manifest.json, scripts, and references before installing, publishing, or running the package.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/timyljob2011-sudo/skills/skill-creater)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance, generated skill files, and ZIP package artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write SKILL.md, manifest.json, helper scripts, reference files, asset folders, README files, and ready-to-upload ZIP archives in the working directory.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact/manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
