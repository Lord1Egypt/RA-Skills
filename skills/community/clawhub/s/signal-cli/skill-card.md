## Description: <br>
Send Signal messages and look up Signal recipients via the local signal-cli installation on macOS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pseudobun](https://clawhub.ai/user/pseudobun) <br>

### License/Terms of Use: <br>


## Use Case: <br>
People who use a local macOS signal-cli setup can ask an agent to look up Signal contacts, resolve recipients, and prepare or send user-confirmed Signal messages and attachments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can use a registered Signal account to send messages or attachments. <br>
Mitigation: Confirm the exact recipient, message text, and attachments with the user before sending. <br>
Risk: Recipient lookup may reveal local Signal contacts or return ambiguous matches. <br>
Mitigation: Use contact lookup only when needed and ask the user to choose among multiple matching recipients. <br>
Risk: Messages may contain sensitive information. <br>
Mitigation: Ask explicitly before sending sensitive content through Signal. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pseudobun/signal-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON helper output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local registered signal-cli account; sending should be confirmed by the user before execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
