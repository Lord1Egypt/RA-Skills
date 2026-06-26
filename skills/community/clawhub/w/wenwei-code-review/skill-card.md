## Description: <br>
代码评审帮助代理在开发完成后对照功能点文档、需求/澄清文档和概要设计文档审查代码实现，评估需求完成度、设计一致性并识别未完成项、BUG 和偏离设计的问题。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wed840313](https://clawhub.ai/user/wed840313) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
开发者和评审人员在功能开发完成后使用此技能，对照功能点文档、需求/澄清文档和概要设计文档验收代码实现。它用于确认需求是否完整交付、代码是否按设计落地，并输出通过或未通过的结构化评审结论。 <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to read project code and review materials, which may include sensitive implementation details. <br>
Mitigation: Share only the repository files, requirements, clarifications, and design documents that are relevant to the review. <br>
Risk: A review based on missing feature, requirement, or design materials may produce incomplete or misleading conclusions. <br>
Mitigation: Use the skill's material-confirmation gate and either provide the missing materials or explicitly accept the limits before continuing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wed840313/wenwei-code-review) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown code review report with requirement coverage, design-consistency findings, bug findings, and a pass or fail conclusion] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May pause to request missing feature, requirement, clarification, or design materials before performing the review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
