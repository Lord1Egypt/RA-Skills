## Description:

在需要新建或优化技能、判断复用还是重建、并生成最小可用技能文件时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangjinghua0127](https://clawhub.ai/user/yangjinghua0127)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to create or refine OpenClaw skills, decide whether to reuse an existing skill or create a new one, and produce a minimal viable SKILL.md-centered artifact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to create or modify files under a workspace skills directory.

Mitigation: Review generated skill files and any optional scripts before installing or deploying them.

Risk: Skill-generation guidance may produce unclear or overlapping skills if similar existing skills are not checked first.

Mitigation: Search for similar skills first and prefer extending an existing skill when it covers the requested use case.

## Reference(s):

- [Create-Skill on ClawHub](https://clawhub.ai/yangjinghua0127/skills/skill-create-cn)
- [Publisher profile](https://clawhub.ai/user/yangjinghua0127)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and optional generated skill files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output is a minimal SKILL.md; scripts or package metadata are generated only when needed.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
