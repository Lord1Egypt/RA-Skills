## Description: <br>
WeCom邮箱 guides an agent to send work email through a dedicated WeCom SMTP mailbox, including meeting minutes and business documents when the user explicitly requests it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chongjie-ran](https://clawhub.ai/user/chongjie-ran) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and agents use this skill to configure a dedicated WeCom mailbox and send work-related emails such as meeting minutes or business documents after explicit user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent mailbox credential files can expose real email credentials if stored weakly or reused across accounts. <br>
Mitigation: Use a dedicated, least-privileged work mailbox, avoid Base64-stored real passwords, and prefer encrypted credential storage with restricted access. <br>
Risk: Email-sending authority can leak sensitive content or send messages to unintended recipients. <br>
Mitigation: Require explicit confirmation of the sender, recipients, subject, body, and any document content before every send, and block passwords, tokens, keys, and personal privacy information. <br>
Risk: Personal or delegated email accounts can create authorization and accountability issues. <br>
Mitigation: Use personal or delegated accounts only when explicitly approved by the authorized user. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chongjie-ran/wecom-email) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose SMTP settings, credential-handling steps, recipient, subject, body, and document-content confirmation checks; actual sending requires explicit user authorization.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
