## Description: <br>
Email Pro Optimized helps agents manage QQ, Gmail, and Outlook mailboxes through IMAP/SMTP and OAuth 2.0 commands for checking, searching, fetching, analyzing, and sending email. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[q012315](https://clawhub.ai/user/q012315) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to automate mailbox workflows across configured QQ, Gmail, and Outlook accounts, including inbox checks, message search, message retrieval, basic analysis, and outbound email. It is suited to scripted email operations where local credentials and OAuth consent are managed by the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled repository-publishing and workspace-sync scripts may perform actions outside normal email management. <br>
Mitigation: Remove or ignore scripts/auto-push.py and scripts/sync-updates.py before installation or execution unless they have been reviewed and are explicitly needed. <br>
Risk: Bundled Outlook OAuth credentials may grant unintended trust to a preconfigured application. <br>
Mitigation: Replace the bundled Outlook OAuth client details with user-owned, rotated credentials and confirm OAuth consent scopes before authorizing an account. <br>
Risk: Local mailbox configuration and OAuth token files can expose mailbox access. <br>
Mitigation: Treat ~/.openclaw/credentials/email-accounts.json and ~/.openclaw/credentials/oauth_tokens.json as secrets, restrict file permissions, and avoid printing account or token details in shared logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/q012315/q012315-email-pro-optimized) <br>
- [Publisher profile](https://clawhub.ai/user/q012315) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; command outputs are text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires locally configured mailbox credentials and OAuth tokens for live email operations.] <br>

## Skill Version(s): <br>
2.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
