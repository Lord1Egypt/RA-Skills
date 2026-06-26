## Description: <br>
Sends and receives QQ Mail messages for OpenClaw agents over SMTP/POP3, with support for attachments and CC/BCC. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[feastfuyan](https://clawhub.ai/user/feastfuyan) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and teams using OpenClaw agents use this skill to send task updates, scheduled reports, and files through QQ Mail, and to check inbox messages for multi-agent coordination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Email automation can send messages or attachments to unintended recipients. <br>
Mitigation: Confirm every recipient and attachment before sending, and avoid broad local file paths or secret-bearing content. <br>
Risk: Mailbox reading and auto-replies can expose message contents or send responses without clear approval. <br>
Mitigation: Use a dedicated, revocable QQ Mail authorization code and enable scheduled checks or auto-replies only with explicit rules and a clear stop mechanism. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/feastfuyan/qqmail-sender) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Email actions require QQ Mail SMTP/POP3 credentials and explicit recipient, attachment, and automation choices.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
