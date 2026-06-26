## Description: <br>
Set up periodic email monitoring for any IMAP mailbox, guide mailbox configuration, test the connection, and create a scheduled task that checks for new messages and reports them in the user's chosen format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiusuo9809](https://clawhub.ai/user/qiusuo9809) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and operators use this skill to configure periodic monitoring for IMAP mailboxes, test access, receive summaries of new email, and optionally download attachments on a schedule. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mailbox credentials are stored in a local plaintext configuration file. <br>
Mitigation: Use a revocable app-specific password, avoid primary account passwords, restrict access to ~/.openclaw/email-monitor, and keep the directory out of backups. <br>
Risk: A scheduled cron job can continue accessing the mailbox after setup. <br>
Mitigation: Remove the cron job and stored configuration when monitoring is no longer needed. <br>
Risk: Optional attachment downloads write files from email messages to the local filesystem. <br>
Mitigation: Keep attachment downloads disabled unless filename handling has been reviewed and the destination directory is appropriate. <br>


## Reference(s): <br>
- [IMAP setup guide](references/imap-setup.md) <br>
- [Google App Passwords](https://myaccount.google.com/apppasswords) <br>
- [ClawHub release page](https://clawhub.ai/qiusuo9809/qiusuo-email-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets; the fetch script returns JSON email summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a local email-monitor configuration, state file, cron task, and optional downloaded attachment files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
