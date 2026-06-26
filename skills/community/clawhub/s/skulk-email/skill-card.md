## Description: <br>
Skulk Email lets an agent read, search, and send email through DreamHost webmail and IMAP, with optional shared Gmail inbox reading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AdaInTheLab](https://clawhub.ai/user/AdaInTheLab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents, developers, and operators use this skill to set up mailbox credentials, check inboxes, search or read messages, and send email through DreamHost when direct SMTP access is unavailable. It is intended for controlled mailbox workflows where an agent is explicitly allowed to access and send email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent sensitive mailbox access and the ability to send email using stored mailbox passwords. <br>
Mitigation: Install it only for a mailbox the agent is allowed to access, prefer a dedicated low-privilege mailbox or app password, and require manual review before outgoing email is sent. <br>
Risk: Local credential files can expose DreamHost or Gmail mailbox access if file permissions or workstation access are weak. <br>
Mitigation: Store credentials only in the documented local path with restrictive directory and file permissions, avoid storing unused Gmail credentials, and keep the file out of source control. <br>
Risk: Automated email sending can create unintended or excessive outbound messages. <br>
Mitigation: Limit send volume, review recipients and message bodies before execution, and use a mailbox dedicated to agent workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/AdaInTheLab/skulk-email) <br>
- [Skill Instructions](artifact/SKILL.md) <br>
- [Email Script](artifact/scripts/skulk-email.sh) <br>
- [DreamHost Webmail](https://webmail.dreamhost.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown setup and command guidance with plaintext email command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, curl, jq, a DreamHost mailbox, and a local credentials file; command output can include email metadata, message content, unread counts, and send status.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
