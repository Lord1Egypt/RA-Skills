## Description:

测试用例生成专家技能。当用户提供产品需求文档、API链接、页面链接，或要求生成测试用例时触发。功能：多维度需求分析、系统化测试用例设计（等价类划分、边界值分析、决策表、状态转换、场景法、错误推测法）、高覆盖率保障。输出语言统一使用中文，严格按照标准测试用例格式输出。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuhuqifei11111](https://clawhub.ai/user/wuhuqifei11111)

### License/Terms of Use:

MIT-0

## Use Case:

QA engineers, test developers, and product teams use this skill to analyze requirements, API links, page links, or uploaded product documents and generate Chinese-language test case suites with functional, boundary, equivalence-class, decision-table, state-transition, scenario, and risk coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill analyzes user-provided requirements documents, links, or uploaded files, which may contain sensitive product or business information.

Mitigation: Review and minimize sensitive requirements content before providing it to the agent.

Risk: Generated test cases may miss requirements, overstate coverage, or include incorrect expected results if the input requirements are incomplete or ambiguous.

Mitigation: Have QA or product reviewers validate generated cases against authoritative requirements before execution or release planning.

## Reference(s):

- [测试用例设计参考手册](references/templates.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Chinese Markdown test case suite with structured tables and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended to follow the skill's fixed test-case structure and remain focused on test-case generation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
