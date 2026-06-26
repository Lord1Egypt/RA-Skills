## Description: <br>
Export large Yahoo Mail archives with the folder-rotation IMAP workflow, resumable downloads, and safe delete-after-verify handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimdawdy-hub](https://clawhub.ai/user/jimdawdy-hub) <br>

### License/Terms of Use: <br>
MIT No Attribution <br>


## Use Case: <br>
Developers and operators use this skill to export large Yahoo Mail accounts through IMAP folder rotation, preserve local .eml copies, and triage exported messages with local models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mailbox data can be deleted during the export workflow. <br>
Mitigation: Run with dry-run or no-delete behavior until a small test completes, then verify local .eml files and message counts before enabling deletion. <br>
Risk: The release includes a hardcoded app-password-like secret. <br>
Mitigation: Remove the secret, rotate it if it was ever valid, and provide Yahoo app passwords through a safer runtime mechanism. <br>
Risk: Exported email data and derived artifacts can contain sensitive personal information. <br>
Mitigation: Treat the local export directory as sensitive, restrict access, and review retention before storing .eml files, metadata, embeddings, triage outputs, or reports. <br>
Risk: Email content may be sent to local model services during embedding and triage. <br>
Mitigation: Confirm local model service configuration and data handling before processing private mail content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jimdawdy-hub/yahoomail-export) <br>
- [README](README.md) <br>
- [Yahoo Mail IMAP Export Guide](YAHOO_EXPORT_GUIDE.md) <br>
- [Yahoo app passwords](https://login.yahoo.com/account/security/app-passwords) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration values, and Python workflow references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The referenced scripts can produce local .eml files, JSONL metadata, SQLite vector indexes, triage outputs, and summary reports.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
