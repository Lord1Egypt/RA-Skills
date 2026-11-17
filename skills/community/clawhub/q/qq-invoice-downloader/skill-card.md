## Description:

Automatically logs in to QQ Mail, searches invoice email by date, downloads PDF attachments, extracts ZIP files, filters non-invoices, and produces categorized Excel reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frankfushmomentlab](https://clawhub.ai/user/frankfushmomentlab)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, operations, and personal productivity users can use this skill to collect invoice files from QQ Mail over a selected date range and organize the results into local attachments, JSON logs, and Excel reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Embedded QQ and Telegram credentials may expose accounts or messaging destinations.

Mitigation: Remove embedded secrets, rotate any exposed credentials, and require credentials through a managed secrets mechanism or environment variables before use.

Risk: Poorly scoped Telegram reporting and outbound network behavior may disclose invoice or mailbox information.

Mitigation: Disable reporting by default or explicitly scope approved reporting destinations and payload contents.

Risk: TLS verification changes can make invoice downloads vulnerable to interception.

Mitigation: Keep TLS verification enabled and fail closed when certificate validation fails.

Risk: Automated email link processing can follow untrusted invoice links.

Mitigation: Add trusted-domain checks before browser automation or direct downloads act on links extracted from email.

Risk: Optional MiniMax LLM analysis may send mailbox content to an external service.

Mitigation: Confirm privacy and compliance acceptability before enabling LLM analysis, and disable or redact inputs when sensitive mailbox content should remain local.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/frankfushmomentlab/skills/qq-invoice-downloader)
- [README](artifact/README.md)
- [Skill usage notes](artifact/SKILL.md)
- [Quickstart](artifact/QUICKSTART.md)
- [Changelog](artifact/CHANGELOG.md)
- [Final test report](artifact/FINAL_TEST_REPORT.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands; runtime outputs invoice files, extracted archives, Excel reports, and JSON logs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided QQ Mail authorization credentials, local output paths, Playwright browser automation, and optional MiniMax API configuration.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
