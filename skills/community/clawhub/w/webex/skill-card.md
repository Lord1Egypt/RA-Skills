## Description: <br>
Webex API integration with managed OAuth. Send messages, manage rooms and teams, list memberships, handle webhooks, manage people and team memberships. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and collaboration teams use this skill to connect Webex through managed OAuth, inspect rooms and memberships, send messages, manage teams, and configure event webhooks from chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires managed OAuth and sensitive Webex credentials through ClawLink. <br>
Mitigation: Install only when you intend to connect Webex through ClawLink, and review the OAuth permissions before authorizing the account. <br>
Risk: Delete, membership, room, and webhook actions can affect real Webex spaces and users. <br>
Mitigation: Require user confirmation for write or delete actions and verify target room, message, membership, team, and webhook identifiers before execution. <br>
Risk: Insufficient Webex permissions can cause moderator, membership, room, or webhook operations to fail. <br>
Mitigation: Check connection status and account permissions before attempting administrative actions, and reconnect through the ClawLink dashboard after authorization failures. <br>


## Reference(s): <br>
- [Webex API Docs](https://developer.webex.com/docs/api-basics) <br>
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=webex) <br>
- [ClawLink Docs](https://docs.claw-link.dev/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses managed OAuth through ClawLink; write and delete actions may affect live Webex spaces, memberships, messages, teams, or webhooks.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
