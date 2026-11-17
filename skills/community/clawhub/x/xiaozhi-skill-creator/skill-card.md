## Description:

写一个新 SKILL 时用的编写工具：四层结构（角色/规则/记忆/输出）、安全与隐私边界、五步落地流程、常见问题诊断。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qizhitang](https://clawhub.ai/user/qizhitang)

### License/Terms of Use:

MIT-0

## Use Case:

SKILL authors and high-school students with basic programming or prompt-writing experience use it to design or revise educational SKILLs, define scope and privacy rules, and diagnose inconsistent behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A referenced security baseline was unavailable, leaving the security review with partial coverage.

Mitigation: Before using generated guidance, consult the applicable security baseline and review the target skill's privacy, consent, and escalation rules.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/qizhitang/skills/xiaozhi-skill-creator)
- [Skill templates library](references/skill-templates-library.md)
- [Shared vocabulary and thresholds](shared/vocab.md)
- [Platform conventions and privacy controls](shared/platform-conventions.md)
- [Handover protocol schema](shared/handover-protocol.schema.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese-language Markdown templates and writing guidance, with structured schema field references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reusable templates require adaptation to the target skill and platform.]

## Skill Version(s):

2.12.7 (source: frontmatter; server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
