## Description: <br>
Automatically signs in to QQ Mail, searches invoice emails by date range, downloads PDF attachments and ZIP archives, filters non-invoice files, and creates classified Excel and JSON reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frankfushmomentlab](https://clawhub.ai/user/frankfushmomentlab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, finance operators, and developers can use this skill to collect invoice files from QQ Mail over a requested date range and produce organized invoice reports for reconciliation or recordkeeping. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Embedded QQ and Telegram secrets may expose real accounts or allow unauthorized access. <br>
Mitigation: Remove embedded secrets, rotate affected credentials, and require users to provide credentials through secure local configuration or environment variables. <br>
Risk: SSL verification bypass can weaken protection when downloading invoice files. <br>
Mitigation: Disable the bypass by default, require explicit user approval for any fallback, and log when certificate verification is not enforced. <br>
Risk: Invoice email content and reports may be shared with MiniMax or Telegram without sufficient disclosure. <br>
Mitigation: Document all external data sharing, make integrations opt-in, and avoid sending sensitive invoice data unless the user has approved the destination. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/frankfushmomentlab/qq-invoice-downloader) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [QUICKSTART.md](artifact/QUICKSTART.md) <br>
- [FINAL_TEST_REPORT.md](artifact/FINAL_TEST_REPORT.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with command examples; generated runtime outputs include downloaded invoice files, Excel workbooks, and JSON logs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-supplied QQ Mail credentials and optional MiniMax API configuration; Playwright browser steps must run serially.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
