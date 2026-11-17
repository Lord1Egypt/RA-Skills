## Description:

Export large Yahoo Mail archives with the folder-rotation IMAP workflow, resumable downloads, and safe delete-after-verify handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimdawdy-hub](https://clawhub.ai/user/jimdawdy-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to export large Yahoo Mail archives through a bounded IMAP folder-rotation workflow, then optionally pre-filter, vectorize, triage, and summarize copied email data with local tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can move and delete mailbox contents repeatedly.

Mitigation: Remove embedded credentials, supply credentials securely, test with --dry-run and --no-delete, verify message counts and backups, and require human approval before deletion.

Risk: Local export files, SQLite indexes, reports, and prompts may contain sensitive email data.

Mitigation: Treat the local ~/email-purge outputs as sensitive data and store, share, and delete them according to the user's data handling requirements.

Risk: Automated recurring execution can continue destructive mailbox operations after the intended migration window.

Mitigation: Avoid enabling the documented cron job unless it has an expiration condition and a human approval checkpoint before deletion.

## Reference(s):

- [Yahoo Mail IMAP Export ClawHub page](https://clawhub.ai/jimdawdy-hub/skills/yahoomail-export)
- [README.md](README.md)
- [YAHOO_EXPORT_GUIDE.md](YAHOO_EXPORT_GUIDE.md)
- [Yahoo app password setup](https://login.yahoo.com/account/security/app-passwords)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and Python script references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local .eml files, JSONL metadata and triage files, a SQLite vector index, and a Markdown summary report when the bundled scripts are adapted and run.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
