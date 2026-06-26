## Description: <br>
Send WhatsApp messages to other people or search/sync WhatsApp history via the wacli CLI (not for normal user chats). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fianabates1](https://clawhub.ai/user/fianabates1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents use this skill when a user explicitly asks them to contact someone on WhatsApp, send a file, or sync and search WhatsApp chat history with wacli. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send WhatsApp messages or files to third parties. <br>
Mitigation: Confirm the recipient, message text, and file path with the user before sending. <br>
Risk: Synced WhatsApp history may contain sensitive personal data stored under ~/.wacli. <br>
Mitigation: Treat the wacli store as sensitive and only sync or search chat history when the user explicitly requests it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fianabates1/test-wa) <br>
- [wacli homepage](https://wacli.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use JSON output from wacli when parsing chat and message results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
