## Description: <br>
Send WhatsApp messages to other people or search and sync WhatsApp history through the wacli CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gillescv](https://clawhub.ai/user/gillescv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they need an agent to send WhatsApp messages to specified recipients or search and sync WhatsApp history from the command line. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WhatsApp messages or files could be sent to the wrong recipient or group. <br>
Mitigation: Require explicit recipient, message text or file path, and confirmation of the recipient and content before sending. <br>
Risk: The upstream wacli CLI receives access to the user's WhatsApp account and may store chat history locally. <br>
Mitigation: Install only when the upstream CLI is trusted, and review or remove the ~/.wacli store when local chat history is no longer needed. <br>
Risk: Sync and search commands can expose private WhatsApp history. <br>
Mitigation: Run sync or search only on explicit user request and avoid using this skill for routine WhatsApp chats. <br>


## Reference(s): <br>
- [Wacli homepage](https://wacli.sh) <br>
- [ClawHub skill page](https://clawhub.ai/gillescv/wacli-gilles) <br>
- [Publisher profile](https://clawhub.ai/user/gillescv) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the wacli binary and explicit confirmation before sending messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
