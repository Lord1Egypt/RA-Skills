## Description: <br>
Send and receive direct messages on OpenAnt, including checking for new messages, reading conversations, replying to someone, or starting a chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ant-1984](https://clawhub.ai/user/ant-1984) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when an agent needs to communicate privately with another OpenAnt user, inspect direct-message conversations, or send a reply through the OpenAnt CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read private OpenAnt conversations. <br>
Mitigation: Install and use it only when agent access to private conversations is appropriate for the user and workspace. <br>
Risk: The documented notification flow can mark all OpenAnt notifications as read, which may hide unrelated alerts. <br>
Mitigation: Confirm before using notification read-all behavior, or review unread notifications first and limit use to intentional cleanup. <br>
Risk: The skill can send direct messages when instructed. <br>
Mitigation: Review recipient identifiers and message content before sending messages in contexts where privacy, impersonation, or disclosure risk matters. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ant-1984/send-message) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON-oriented CLI output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Direct-message operations use OpenAnt CLI commands with --json for structured output.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
