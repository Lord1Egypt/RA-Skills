## Description: <br>
生成收钱吧生意贷（含消费贷）产品的完整 PRD（产品需求文档），并按固定 PRD 结构、前后端需求边界、异常流和贷款埋点规范输出。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runkecheng](https://clawhub.ai/user/runkecheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product managers and delivery teams use this skill to turn a loan-product business request into a complete PRD. The output standardizes project context, business flow, frontend and backend requirements, non-functional requirements, acceptance criteria, and loan analytics events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can broadly read internal Feishu knowledge bases and may use outdated, conflicting, or overly broad source material. <br>
Mitigation: Before use, specify the exact Feishu pages or topics the agent should read and require the agent to summarize the sources it used before drafting the PRD. <br>
Risk: The skill can write PRD output to Feishu without strong destination controls. <br>
Mitigation: Require a reviewed PRD draft first and approve the exact Feishu destination before allowing any write action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/runkecheng/write-loan-prd) <br>
- [产品建设知识库](https://sqb.feishu.cn/wiki/Z0iywE30EifJiVkfFPbctjzXn10) <br>
- [产品迭代](https://sqb.feishu.cn/wiki/PA2WwT1fMi4aoHk69XccbmJMnbc) <br>
- [月度产品功能需求计划](https://sqb.feishu.cn/wiki/K4CIwdQ9KiSmJDkkax3cQrpun8d) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown PRD with tables, checklists, and Mermaid diagram blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Feishu-ready PRD content and loan analytics event specifications.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
