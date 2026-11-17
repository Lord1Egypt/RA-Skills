## Description:

Stock Assistant helps agents query A-share market quotes, manage local trade records, calculate positions and profit or loss, and import or export CSV trade data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[54meteor](https://clawhub.ai/user/54meteor)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect A-share quotes, maintain local trade records, calculate holdings and profit or loss, and prepare CSV imports or exports for trading records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu notifications can send holdings and profit or loss data to external webhook or chat destinations.

Mitigation: Use only trusted Feishu webhook URLs and avoid sending holdings or P&L to shared chats unless that disclosure is intentional.

Risk: Feishu app secrets are accepted through command-line arguments and scheduled job parameters.

Mitigation: Do not put real app secrets directly in shell commands or scheduled jobs; use a protected secret management path when deploying.

Risk: Local trade databases and CSV exports may contain sensitive trading, account, holdings, and P&L information.

Mitigation: Protect the local SQLite database and exported CSV files, restrict access to the data directory, and avoid sharing exported files broadly.

Risk: CSV imports from untrusted sources may expose users to malformed or sensitive data handling issues.

Mitigation: Import CSV files only from trusted sources and inspect unfamiliar files before opening or processing them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/54meteor/skills/stock-assistant)
- [Detailed Design](artifact/references/design.md)
- [Design Overview](artifact/DESIGN.md)
- [Tencent Finance](https://finance.qq.com/)

## Skill Output:

**Output Type(s):** [text, JSON, CSV files, shell commands, configuration guidance]

**Output Format:** [Markdown guidance with shell commands, CLI text output, Feishu card JSON, and CSV files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores trade records in a local SQLite database and can send notification content to Feishu when configured.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
