## Description: <br>
QuickBooks Online automation for chart of accounts setup, bank rule configuration, recurring transaction templates, reconciliation workflows, and journal entry generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Bookkeepers, accountants, finance operators, and developers use this skill to configure and automate QuickBooks Online bookkeeping workflows, including account setup, transaction categorization, reconciliation support, and journal entry drafting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents toward changes in live QuickBooks Online accounting records. <br>
Mitigation: Use a sandbox company first and require human approval before any write to production accounting data. <br>
Risk: QuickBooks credentials and refresh tokens could be exposed through prompts, logs, or unmanaged environment variables. <br>
Mitigation: Store credentials in a managed secret store, avoid placing tokens in prompts or logs, and use the least-privileged QBO account available. <br>
Risk: Bookkeeping guidance or generated journal entries may be incorrect for a specific business context. <br>
Mitigation: Have a qualified bookkeeper, accountant, or CPA review generated workflows and entries before relying on them for reporting or audit purposes. <br>


## Reference(s): <br>
- [QBO Automation ClawHub release](https://clawhub.ai/samledger67-dotcom/qbo-automation) <br>
- [Intuit OAuth token endpoint](https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer) <br>
- [QuickBooks Online API base URL](https://quickbooks.api.intuit.com) <br>
- [QuickBooks Online sandbox API base URL](https://sandbox-quickbooks.api.intuit.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python, bash, CSV, and accounting template examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose QuickBooks Online API calls and bookkeeping workflow steps that require human review before use on production accounting data.] <br>

## Skill Version(s): <br>
98.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
