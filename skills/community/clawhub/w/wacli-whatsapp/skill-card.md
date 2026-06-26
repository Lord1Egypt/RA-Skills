## Description: <br>
Helps an agent use wacli to authenticate, sync, search WhatsApp history, and send WhatsApp text, reactions, quoted replies, or files from the command line. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[prantikmedhi](https://clawhub.ai/user/prantikmedhi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent operate wacli for WhatsApp messaging tasks. It supports checking installation, authenticating and syncing, finding chats or message IDs, and sending text, reactions, quoted replies, or files only after explicit user direction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WhatsApp messages, reactions, or files could be sent to the wrong recipient or with unintended content. <br>
Mitigation: Require an explicit user request with both recipient and message or file content, and ask one clarifying question when recipient, chat, message ID, or attachment details are ambiguous. <br>
Risk: Authentication and background syncing can leave WhatsApp session data on the local machine. <br>
Mitigation: Install and authenticate wacli only on a trusted machine; stop background sync and remove the local store when the user no longer wants WhatsApp session data kept on the device. <br>
Risk: Replies or reactions can target the wrong prior message if the message ID is stale or unclear. <br>
Mitigation: Use wacli message search, list, show, or context commands to verify the chat and message ID before sending replies or reactions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/prantikmedhi/wacli-whatsapp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes executable wacli commands and safety checks; the skill itself does not produce standalone files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
