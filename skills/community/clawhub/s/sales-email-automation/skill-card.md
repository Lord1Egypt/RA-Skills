## Description: <br>
Read and send email via IMAP/SMTP, including checking unread messages, fetching content, searching mailboxes, marking messages read or unread, and sending emails with attachments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cjboy007](https://clawhub.ai/user/cjboy007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and operations agents use this skill to read, search, archive, and send customer email through standard IMAP and SMTP servers. It can also support sales follow-up workflows that draft replies, attach documents, and optionally sync activity to external review or CRM systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send email, archive mail, and write sales or CRM records. <br>
Mitigation: Use dedicated mailbox credentials and review generated messages, attachments, and CRM sync behavior before allowing the skill to act on real customer email. <br>
Risk: Optional integrations can send email data to OpenRouter, Discord, OKKI, or other configured services. <br>
Mitigation: Keep optional integrations disabled unless they are required, and use separate scoped API tokens for each enabled service. <br>
Risk: Local command construction and file access can increase impact when processing untrusted inbound email. <br>
Mitigation: Restrict local read and write directories, disable automatic capture or cron execution by default, and fix shell-command construction before production use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cjboy007/sales-email-automation) <br>
- [Publisher Profile](https://clawhub.ai/user/cjboy007) <br>
- [Google App Passwords](https://myaccount.google.com/apppasswords) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration examples, and generated email text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write local email artifacts, send SMTP messages, and call configured external services when enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
