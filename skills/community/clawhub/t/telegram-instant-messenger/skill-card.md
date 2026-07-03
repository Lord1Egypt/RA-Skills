## Description: <br>
Telegram Instant Messenger lets agents send and receive Telegram text, photo, and document messages through the shared AgentPMT Telegram bot with budget-scoped chat binding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to add Telegram notifications, two-way chat, support workflows, feedback collection, and media sharing through AgentPMT-hosted tool calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Messages, files, and chat metadata may be routed through Telegram and AgentPMT. <br>
Mitigation: Use the skill only for explicit Telegram tasks, avoid secrets or regulated data, and keep message content scoped to the task. <br>
Risk: The shared bot binds a budget to a Telegram chat, so accidental sends can reach the wrong recipient if setup is not checked. <br>
Mitigation: Confirm the binding flow and intended destination before sending messages, photos, documents, or importing files. <br>
Risk: Security review flagged the skill as suspicious because activation scope and privacy notice are not clearly described. <br>
Mitigation: Review deployment policy before enabling the skill and limit use to trusted workflows with clear user consent. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/telegram-instant-messenger) <br>
- [AgentPMT Marketplace Product](https://www.agentpmt.com/marketplace/telegram-instant-messenger) <br>
- [Telegram Instant Messenger Schema](artifact/schema.md) <br>
- [AgentPMT File Management Skill](https://clawhub.ai/agentpmt/file-management) <br>
- [AgentPMT Account MCP/REST Setup Skill](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Configuration instructions, Guidance, Markdown, JSON] <br>
**Output Format:** [Markdown guidance with JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports get_updates, send_message, send_photo, and send_document actions; responses may include connection_required binding details.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
