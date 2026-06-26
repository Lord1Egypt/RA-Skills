## Description: <br>
Qordinate is a chat-native assistant that acts as durable, structured memory for OpenClaw agents by storing facts, lists, tasks, contacts, and reminders through WhatsApp, Telegram, or Slack. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SinghCoder](https://clawhub.ai/user/SinghCoder) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to let an OpenClaw agent save and retrieve long-term user facts, tasks, contacts, lists, and reminders through a linked Qordinate chat account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cause an agent to persist user facts, tasks, contacts, and reminders to an external Qordinate account through chat apps. <br>
Mitigation: Require user confirmation before storing sensitive information and prohibit secrets, OTPs, credentials, financial data, health data, and confidential business data. <br>
Risk: The release evidence notes insufficient privacy controls for external memory use. <br>
Mitigation: Verify Qordinate retention and deletion controls before relying on the integration for durable memory. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/SinghCoder/qordinate-structured-memory) <br>
- [Qordinate homepage](https://qordinate.ai) <br>
- [Qordinate Slack connection](https://qordinate.ai/slack) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with structured natural-language message examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the agent environment to send messages through WhatsApp, Telegram, or Slack.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata, released 2026-02-07) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
