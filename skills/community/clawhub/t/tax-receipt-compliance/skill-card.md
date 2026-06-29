## Description: <br>
Tax Receipt Compliance helps agents process Chinese VAT receipts through local OCR, invoice verification handoffs, reimbursement form generation, and optional approval-system submission. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fyniujin](https://clawhub.ai/user/fyniujin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance operations teams and enterprise developers use this skill to extract invoice fields, prepare reimbursement forms, and connect verification or approval workflows configured by the organization. It is a technical support tool and does not provide tax advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invoice images, OCR JSON, cache files, and reimbursement outputs may contain sensitive financial data. <br>
Mitigation: Store outputs in restricted directories, limit access to finance users, and delete OCR JSON or cache files when no longer needed. <br>
Risk: Verification and approval workflows can send invoice data or credentials to configured third-party or custom endpoints. <br>
Mitigation: Use environment variables or a secrets manager for credentials, review endpoint configuration, and require human confirmation before sending invoice data outside the machine. <br>
Risk: Installer scripts may install system packages or download a Windows Tesseract installer. <br>
Mitigation: Run installer scripts manually, verify downloaded installers independently, and prefer a Python virtual environment for package installation. <br>
Risk: Invoice verification results may be links, manual handoffs, or third-party responses rather than authoritative determinations. <br>
Mitigation: Treat verification results as manual or third-party evidence unless the configured provider is confirmed to return authoritative responses. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fyniujin/skills/tax-receipt-compliance) <br>
- [Enterprise Setup Guide](references/setup-guide.md) <br>
- [API Endpoints](references/api-endpoints.md) <br>
- [Tax Rules](references/tax-rules.md) <br>
- [Risk Declaration](references/risk-declaration.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON, Spreadsheet files, Guidance] <br>
**Output Format:** [Markdown guidance with shell and Python commands, plus generated JSON and Excel files when scripts are run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May process sensitive invoice data locally and may call configured verification or approval endpoints.] <br>

## Skill Version(s): <br>
2.5.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
