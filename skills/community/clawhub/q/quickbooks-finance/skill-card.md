## Description: <br>
Manage QuickBooks accounts, customers, invoices, payments, bills, expenses, and financial workflows via the QuickBooks Online API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to read and manage QuickBooks Online accounting records, including customers, invoices, payments, bills, vendors, reports, and company settings through ClawLink-hosted OAuth tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate financial write operations, including invoices, payments, bills, expenses, and destructive actions. <br>
Mitigation: Use read and preview steps before writes, confirm the target resource and intended effect with the user, and execute only after explicit approval. <br>
Risk: OAuth access can expose QuickBooks company data available to the connected account. <br>
Mitigation: Install only when QuickBooks access through ClawLink is intended, review OAuth permissions during connection, and verify that the active integration is the expected QuickBooks company. <br>
Risk: Incorrect amounts, accounts, dates, recipients, or stale SyncToken values can cause inaccurate or rejected financial records. <br>
Mitigation: Check amounts, accounts, dates, recipients, and business impact before approval, and re-read records before updates that require the current SyncToken. <br>


## Reference(s): <br>
- [ClawHub QuickBooks Skill Page](https://clawhub.ai/hith3sh/quickbooks-finance) <br>
- [QuickBooks Online API](https://developer.intuit.com/) <br>
- [QuickBooks API Reference](https://developer.intuit.com/docs/api/accounting) <br>
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=quickbooks-finance) <br>
- [ClawLink Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON tool-call parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes confirmation-first workflows for QuickBooks write operations and ClawLink OAuth setup guidance.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
