## Description: <br>
A WeCom message sender for sending messages, reports, notifications, and alerts with configurable sender and recipient fields. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoqiangclub](https://clawhub.ai/user/xiaoqiangclub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to send WeCom text messages for task reports, job notifications, system alerts, daily summaries, and custom updates. It supports command-line use and Python function calls with recipient scoping by user, department, or tag. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default @all recipient can accidentally disclose message content or spam an entire WeCom organization. <br>
Mitigation: Change the default recipient to scoped users, departments, or tags, and require explicit confirmation of message content and recipients before sending. <br>
Risk: WeCom credentials and broad app permissions can expand impact if misconfigured or exposed. <br>
Mitigation: Use a limited-permission WeCom app and keep CorpID, CorpSecret, and AgentID in protected environment or .env configuration that is not committed. <br>
Risk: Sensitive reports may be sent to unintended recipients if recipient scoping is not enforced. <br>
Mitigation: Do not use this skill for sensitive reports unless recipient scoping is enforced and reviewed before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xiaoqiangclub/send-to-me) <br>
- [Publisher profile](https://clawhub.ai/user/xiaoqiangclub) <br>
- [WeCom configuration tutorial](https://xiaoqiangclub.blog.csdn.net/article/details/144614019) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python snippets, and text message templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sends text messages through WeCom when configured with a CorpID, CorpSecret, AgentID, and scoped recipients.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
