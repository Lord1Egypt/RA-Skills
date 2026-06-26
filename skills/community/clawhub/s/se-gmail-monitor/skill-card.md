## Description: <br>
Monitors and manages configured Gmail accounts for inbox triage, urgent-message scanning, unread-count checks, and approved outbound email via IMAP/SMTP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boris148](https://clawhub.ai/user/boris148) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and operators use this skill to inspect Gmail inboxes, identify urgent or security-related messages, and send approved operational email from configured accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read business Gmail inboxes and send email from configured accounts. <br>
Mitigation: Use least-privilege Gmail accounts and app passwords, restrict access to the local configuration file, and require explicit user approval for every outbound email. <br>
Risk: The release has broad and partly conflicting approval rules for sending email. <br>
Mitigation: Disable unattended sending and treat heartbeat checks as read-only unless a user approves a specific recipient, subject, body, and sending account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/boris148/se-gmail-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and Python script usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured Gmail accounts and app passwords; outbound email should require explicit user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
