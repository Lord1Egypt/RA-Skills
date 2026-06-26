## Description: <br>
测试用例生成专家技能。当用户提供产品需求文档、API链接、页面链接，或要求生成测试用例时触发。功能：多维度需求分析、系统化测试用例设计（等价类划分、边界值分析、决策表、状态转换、场景法、错误推测法）、高覆盖率保障。输出语言统一使用中文，严格按照标准测试用例格式输出。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuhuqifei11111](https://clawhub.ai/user/wuhuqifei11111) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and product teams use this skill to turn product requirements, API links, page links, or uploaded requirement documents into structured Chinese test case sets. It supports requirement analysis, test design method selection, coverage checks, and standardized markdown test documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Teams that need English or mixed-language output may receive unsuitable deliverables because the skill is designed to produce Chinese test documentation. <br>
Mitigation: Use the skill for Chinese-language workflows or explicitly override and review the output language requirements before adoption. <br>
Risk: Generated test cases may be incomplete or misleading when the supplied requirements are vague, outdated, or missing product-specific business rules. <br>
Mitigation: Review generated cases against the source requirements and add missing business, boundary, security, compatibility, and environment coverage before execution. <br>


## Reference(s): <br>
- [测试用例设计参考手册](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Chinese Markdown test case documentation with tables and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are constrained to Chinese and a fixed test case structure.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
