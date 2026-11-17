## Description:

心理学数据分析决策与执行助手，帮助用户收集研究设计信息、选择统计检验、运行 Python 分析或提供 SPSS 步骤，并解读结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjinhongmy-pixel](https://clawhub.ai/user/wangjinhongmy-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

心理学研究人员、学生和数据分析者使用此技能来选择合适的统计检验、执行本地数据分析、获得 SPSS 操作指导，并生成包含统计量、效应量、置信区间和 APA 风格表述的结果解读。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some documented or selectable analysis modes may be incomplete or unreliable, especially mediation, moderation, and chi-square workflows.

Mitigation: Verify statistical recommendations and script output against trusted statistical software or expert review before relying on results in formal research.

Risk: Psychology research datasets may contain sensitive participant data.

Mitigation: Use only user-selected datasets, run the script in an isolated virtual environment with pinned dependencies, and avoid sharing confidential data in prompts or logs.

## Reference(s):

- [统计检验决策树](references/stat_decision_tree.md)
- [Python 数据分析指南](references/python_guide.md)
- [SPSS 操作指南](references/spss_guide.md)
- [效应量参考表](references/effect_size.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline code blocks and local script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include statistical recommendations, command examples, SPSS syntax, Python snippets, and APA-style result text.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
