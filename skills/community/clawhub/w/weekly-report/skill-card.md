## Description: <br>
周报生成器，自动汇总本周工作 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangjingzhi07](https://clawhub.ai/user/huangjingzhi07) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees and teams use this skill to record tasks, list current tasks, and generate a concise weekly report from locally stored task history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task names and generated report history are stored locally in the skill directory. <br>
Mitigation: Avoid entering confidential work details unless local storage in tasks.json and reports.json is acceptable. <br>
Risk: Broad Chinese trigger words such as 周报, 总结, 本周, and 上周 may invoke the skill unintentionally. <br>
Mitigation: Use specific prompts such as 生成周报 only when a weekly report action is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huangjingzhi07/weekly-report) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/huangjingzhi07) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown] <br>
**Output Format:** [Markdown weekly report or plain text task/help response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may also update local tasks.json and reports.json files in its skill directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
