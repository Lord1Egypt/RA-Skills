## Description: <br>
Use when you need to control Slack from Clawdbot via the slack tool, including reacting to messages or pinning/unpinning items in Slack channels or DMs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChaunceyLiu](https://clawhub.ai/user/ChaunceyLiu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and external users use this skill to operate Slack from Clawdbot, including reacting to messages, managing pins, sending or modifying messages, reading recent messages, fetching member information, and listing custom emoji. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read Slack messages and member details, which may expose sensitive workspace information. <br>
Mitigation: Use a least-privilege Slack bot token and restrict Clawdbot to intended channels where possible. <br>
Risk: The skill can send, edit, delete, pin, unpin, and react to Slack messages, which can alter shared workspace communication. <br>
Mitigation: Require explicit user confirmation before message-changing or pin-management actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ChaunceyLiu/testat1) <br>
- [Publisher profile](https://clawhub.ai/user/ChaunceyLiu) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with JSON action payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Slack channel IDs, message timestamps, user IDs, target identifiers, emoji names, or message content depending on the action.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
