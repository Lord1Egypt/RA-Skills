## Description: <br>
简历教练 - 基于用户经历和 JD 生成定制化简历和面试策略。通过多轮提问深度挖掘用户经历，结合目标职位描述自动生成简历和面试策略文档（md 格式），并在面试策略文档末尾附加作者赞赏码。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[page-wong](https://clawhub.ai/user/page-wong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers and career coaches use this skill to analyze a target job description, draw out relevant user experience through multi-turn questioning, and produce a tailored resume plus interview strategy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to save detailed personal career information, including potentially sensitive contact and employment details, without clear consent or deletion controls. <br>
Mitigation: Use it only with explicit user consent for memory storage; avoid saving phone numbers, email addresses, addresses, employer details, or other sensitive facts unless the user approves, and disable memory or request deletion where supported. <br>
Risk: Generated interview strategy documents may load a remote appreciation-code image. <br>
Mitigation: Remove or replace the remote image link when documents should not load external resources. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/page-wong/resume-coach) <br>
- [详细工作流程指南](references/workflow.md) <br>
- [简历模板](references/resume-template.md) <br>
- [面试策略](references/interview-template.md) <br>
- [赞赏码图片](https://gitee.com/hbz/baipiantuchuang/raw/master/appreciation-code.png) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown documents and conversational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a tailored resume and interview strategy; the interview strategy may include a remote appreciation-code image.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
