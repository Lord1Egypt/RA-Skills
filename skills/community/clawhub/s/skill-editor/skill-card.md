## Description:

技能编辑器提供中文指南，帮助开发者编辑、完善和审查 AgentSkills 的 SKILL.md、metadata、package.json 与发布前一致性。

This skill is ready for commercial/non-commercial use.

## Publisher:

[romicboy](https://clawhub.ai/user/romicboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to create, edit, clean up, and audit AgentSkills files, especially SKILL.md frontmatter, OpenClaw metadata, package.json display metadata, environment-variable declarations, and release version consistency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Editing guidance could introduce incorrect skill metadata, mismatched versions, or misleading activation descriptions if applied without review.

Mitigation: Review SKILL.md, package.json, environment-variable declarations, and release version values before publishing.

Risk: Example directory-wide metadata checks may inspect more skill folders than intended when paths are changed or copied into another environment.

Mitigation: Run directory-wide checks only against skill folders the maintainer intends to inspect.

Risk: The bilingual description and trigger-word convention may not fit every project or agent runtime.

Mitigation: Confirm the description convention against the target project before adopting it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/romicboy/skills/skill-editor)
- [Publisher profile](https://clawhub.ai/user/romicboy)
- [Skill homepage metadata](https://clawhub.ai/skills/skill-editor)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with YAML, JSON, Python, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No bundled code execution; outputs are editing and review guidance for skill files.]

## Skill Version(s):

1.2.4 (source: server release metadata, SKILL.md metadata, and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
