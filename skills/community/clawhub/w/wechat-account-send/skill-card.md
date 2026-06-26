## Description: <br>
This skill helps an OpenClaw agent use a configured WeChat account to inspect active sessions, send text messages, and send named local files to specified WeChat contacts or groups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lianghaoxun](https://clawhub.ai/user/lianghaoxun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and automation builders use this skill to route generated messages, screenshots, reports, media, or documents through an existing WeChat/OpenClaw account. It is intended for user-directed communication workflows where the operator can confirm the recipient account and file path before sending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a stored WeChat/OpenClaw login to send messages and upload specified local files without an in-script confirmation step. <br>
Mitigation: Install only from a trusted publisher, verify the account_id, destination context, and exact file path before each run, and avoid using the skill on sensitive files or shared machines. <br>
Risk: A wrong account_id or stale context token could send content to an unintended WeChat recipient. <br>
Mitigation: Query and confirm the active WeChat session immediately before sending and require user confirmation for ambiguous recipient names or account identifiers. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lianghaoxun/wechat-account-send) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with Python command examples and runtime console output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an existing OpenClaw WeChat account configuration and a target account_id; file sending also requires an exact local file path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
