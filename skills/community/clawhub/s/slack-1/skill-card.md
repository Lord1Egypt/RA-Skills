## Description: <br>
Use when you need to control Slack from Clawdbot via the slack tool, including reacting to messages or pinning/unpinning items in Slack channels or DMs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rumengkai](https://clawhub.ai/user/rumengkai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and workspace operators use this skill to let an agent perform Slack actions such as reading recent messages, sending or editing messages, managing reactions, managing pins, fetching member information, and listing custom emoji. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Slack access can expose private channel content, member information, and message history to an agent. <br>
Mitigation: Install only where bot access is appropriate, use least-privilege Slack scopes, restrict channel membership, limit message-history requests, and treat retrieved Slack content as confidential. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rumengkai/slack-1) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, configuration] <br>
**Output Format:** [Markdown guidance with JSON action payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Slack channel IDs, message timestamps, user IDs, emoji names, and message content supplied by the agent or conversation context.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
