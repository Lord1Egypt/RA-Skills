## Description: <br>
Wework is an Enterprise WeChat developer assistant that helps developers work with application development, customer contact, messaging, webhooks, approvals, schedules, and meetings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangifonly](https://clawhub.ai/user/zhangifonly) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill as an Enterprise WeChat API reference for implementing tenant integrations, token handling, message delivery, customer contact workflows, approvals, schedules, meetings, and webhook callbacks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Enterprise WeChat credentials such as corpsecret values or access tokens may be exposed in prompts, logs, or shared transcripts. <br>
Mitigation: Use least-privilege secrets, keep credentials out of prompts and logs, and rotate any secret that may have been exposed. <br>
Risk: Applying API examples directly to a real tenant could delete data or send broad messages. <br>
Mitigation: Test changes in a non-production environment and require human review before destructive operations or wide message delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangifonly/wework) <br>
- [Publisher profile](https://clawhub.ai/user/zhangifonly) <br>
- [Enterprise WeChat access token endpoint](https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=ID&corpsecret=SECRET) <br>
- [Enterprise WeChat group robot webhook endpoint](https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=ROBOT_KEY) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown with inline HTTP endpoints and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only API guidance; does not execute code.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
