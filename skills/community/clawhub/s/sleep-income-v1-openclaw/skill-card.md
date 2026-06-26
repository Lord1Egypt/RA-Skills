## Description: <br>
通过 OpenClaw 自动生成公众号内容、数字产品素材和市场发布资产，帮助创作者搭建可重复运行的 AI 副业工作流。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suda6632](https://clawhub.ai/user/suda6632) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
有 OpenClaw 经验并拥有微信公众号账号的创作者可用它规划和运行公众号内容工厂、数字产品打包流程和市场资产发布流程。它面向希望把 AI 写作、数据追踪、反馈收集和迭代升级组织成可重复副业闭环的用户。 <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring publishing workflows may upload WeChat drafts or marketplace assets without clear approval controls. <br>
Mitigation: Require explicit manual approval before WeChat draft upload or marketplace publication. <br>
Risk: Workspace scanning and asset packaging may expose credentials, private files, or unrelated local content. <br>
Mitigation: Restrict scanning to an allowlisted folder and exclude credentials and private files before packaging. <br>
Risk: The workflow depends on WeChat account credentials and publishing permissions. <br>
Mitigation: Store WeChat credentials only in approved secret storage and review permission scope before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/suda6632/sleep-income-v1-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with workflow diagrams, command references, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe scheduled publishing, credential-dependent setup, and manual review steps for marketplace or WeChat publication.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
