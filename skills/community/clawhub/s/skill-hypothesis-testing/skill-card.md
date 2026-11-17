## Description:

统计假设检验工具；支持正态性检验(Shapiro-Wilk/K-S)、t检验(单样本/独立/配对)、卡方检验(拟合优度/独立性)、ANOVA、Levene检验、Mann-Whitney U检验；自动计算统计量、p值、置信区间与效应量；提供结果解释指南

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users can use this Chinese-language skill to select and run common statistical hypothesis tests on local numeric datasets, then interpret statistics, p-values, confidence intervals, and effect sizes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads user-provided local data files, which may contain sensitive or unintended data.

Mitigation: Provide only intended datasets and review file paths before execution.

Risk: The optional output path can write JSON results wherever the agent has filesystem permission.

Mitigation: Use explicit output paths in approved workspace locations and review generated files before reuse.

Risk: Statistical test results can be misread as proof of causality or practical significance.

Mitigation: Interpret p-values with effect sizes, confidence intervals, test assumptions, and the included interpretation guide.

## Reference(s):

- [假设检验结果解释指南](references/interpretation_guide.md)
- [Server-resolved source repository](https://github.com/duding-engicool/skill-hypothesis-testing)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-hypothesis-testing)
- [ClawHub publisher profile](https://clawhub.ai/user/duding-engicool)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell command examples; the bundled CLI emits JSON results or writes them to a JSON file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads numeric lists or local CSV, TXT, and Excel inputs; optional output path writes JSON where the agent has filesystem permission.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
