## Description: <br>
QuickBooks API integration with managed OAuth for reading and administering QuickBooks Online customers, vendors, invoices, payments, and reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and business operations users use this skill to connect an agent to QuickBooks Online through Maton-managed OAuth, retrieve accounting records, run reports, and prepare explicitly approved accounting changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access or change QuickBooks financial records through an agent-controlled API connection. <br>
Mitigation: Install only for intended QuickBooks accounting administration, use a least-privileged QuickBooks account, start with read-only requests, and approve write or delete actions only after checking the exact endpoint, record, amount, and consequence. <br>
Risk: A request may target the wrong QuickBooks company or Maton connection when multiple connections exist. <br>
Mitigation: Verify the Maton connection ID and company before each request and include the Maton-Connection header, especially before any write operation. <br>
Risk: The MATON_API_KEY grants access to the connected QuickBooks integration. <br>
Mitigation: Protect MATON_API_KEY as a sensitive credential and revoke unused connections promptly. <br>


## Reference(s): <br>
- [QuickBooks Skill Page](https://clawhub.ai/byungkyu/quickbooks) <br>
- [Publisher Profile](https://clawhub.ai/user/byungkyu) <br>
- [QuickBooks API Overview](https://developer.intuit.com/app/developer/qbo/docs/get-started) <br>
- [QuickBooks Customer API](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/customer) <br>
- [QuickBooks Invoice API](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/invoice) <br>
- [QuickBooks Payment API](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/payment) <br>
- [QuickBooks Profit and Loss Report API](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/report-entities/profitandloss) <br>
- [Maton](https://maton.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, API calls] <br>
**Output Format:** [Markdown with inline bash, Python, JavaScript, JSON, and SQL examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a valid QuickBooks OAuth connection.] <br>

## Skill Version(s): <br>
1.0.6 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
