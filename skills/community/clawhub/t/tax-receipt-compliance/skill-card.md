## Description: <br>
Helps agents run local invoice OCR, draft reimbursement data, prepare template-filled expense reports, and guide invoice verification or approval handoffs with enterprise-supplied configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fyniujin](https://clawhub.ai/user/fyniujin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance employees and developers use this skill to extract structured data from Chinese VAT invoices, draft reimbursement files, and prepare verification or approval workflows that require human and enterprise-system confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Verification and approval features may be interpreted as completed invoice validation or submitted approvals. <br>
Mitigation: Treat generated verification links, statuses, and approval responses as drafts or handoff artifacts; manually confirm tax-bureau checks and approval-system submissions. <br>
Risk: The DingTalk setup path is flagged by security evidence as pointing to the wrong service. <br>
Mitigation: Do not enter production DingTalk credentials through DuXiaoman-linked guidance; verify platform documentation and endpoints before configuring credentials. <br>
Risk: config.yaml and platform setup can contain invoice, API, or approval-system secrets. <br>
Mitigation: Protect configuration files, prefer environment variables or a secrets manager, restrict file permissions, and rotate credentials on a defined schedule. <br>
Risk: External OCR components and installers affect the local processing environment. <br>
Mitigation: Install Tesseract and related OCR dependencies only from trusted sources and verify the local environment before processing invoice data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fyniujin/skills/tax-receipt-compliance) <br>
- [Enterprise Setup Guide](references/setup-guide.md) <br>
- [API Endpoints](references/api-endpoints.md) <br>
- [Tax Rules](references/tax-rules.md) <br>
- [Risk Declaration](references/risk-declaration.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples, shell commands, Python scripts, YAML configuration, and generated local JSON or Excel artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local OCR and reimbursement drafts; verification and approval results require manual or enterprise-system confirmation.] <br>

## Skill Version(s): <br>
2.7.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
