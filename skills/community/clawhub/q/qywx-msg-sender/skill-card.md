## Description: <br>
Sends notifications to WeCom group robot webhooks as text, Markdown, Markdown V2, image, or file messages, either by direct webhook URL/chat ID or by registered chat name. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gavinyao](https://clawhub.ai/user/gavinyao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to send deployment notices, service alerts, scheduled job results, reports, images, and files to WeCom chats from shell workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WeCom webhook URLs act like credentials and may be stored in the chat registry or printed by registration and listing commands. <br>
Mitigation: Store the registry with restrictive permissions, avoid sharing terminal output or logs, prefer environment or protected secret storage over command history, and rotate exposed webhook URLs. <br>
Risk: Messages, images, and files are sent to external WeCom webhook endpoints. <br>
Mitigation: Review the target chat name, webhook URL, chat ID, and message or file contents before sending. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gavinyao/qywx-msg-sender) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON payload behavior.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; WeCom webhook URLs and chat registry values must be treated as secrets.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
