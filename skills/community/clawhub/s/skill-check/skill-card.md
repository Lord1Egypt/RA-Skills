## Description:

审查和优化现有技能（Skill）结构质量，并在用户请求优化技能、审查技能或检查技能规范性时触发。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linchuncheng](https://clawhub.ai/user/linchuncheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to review an agent skill directory for structure, workflow clarity, logical consistency, and agent compatibility. It produces prioritized issues and concrete optimization steps for improving the skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run local Python scripts against a skill directory.

Mitigation: Use it only on skill directories you intend to review, and inspect script actions before running automation.

Risk: The optional review loop can create missing standard directories in the target skill.

Mitigation: Use the single-pass analyzer for read-only review, and run the review loop only when those narrow filesystem changes are desired.

Risk: The skill content and reports are primarily Chinese-language.

Mitigation: Use reviewers who can evaluate the Chinese-language instructions and output before applying recommendations.

## Reference(s):

- [Structure Patterns](references/structure-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/linchuncheng/skills/skill-check)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Code, Guidance]

**Output Format:** [Markdown review report with issue tables, shell commands, and actionable remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May optionally run a local review loop that creates missing standard directories in the target skill.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
