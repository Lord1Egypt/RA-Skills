## Description:

对比 FAQ 知识库与金牌客服对话记录，识别口径不一致、过时内容和缺失条目，并生成差异报告与优化建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zenobiazizi](https://clawhub.ai/user/zenobiazizi)

### License/Terms of Use:

MIT-0

## Use Case:

Customer support and knowledge-management teams use this skill to audit whether FAQ knowledge-base entries match trusted service dialogue records, then prioritize updates for inconsistent, outdated, missing, or vague content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The file-reading helper has an under-scoped path check that could expose unintended local files in some setups.

Mitigation: Use only controlled input paths and files; harden canonical path containment checks and pin dependencies before use with untrusted files or agents.

Risk: FAQ and customer-service dialogue files may contain customer personal data.

Mitigation: Remove names, phone numbers, order numbers, and other personal data before analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zenobiazizi/skills/skill-knowledge-base-health-check)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports and prioritized recommendation lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a detailed inconsistency report and a prioritized optimization list; supported input files are converted to text with the bundled reader.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
