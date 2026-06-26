## Description: <br>
Xero API integration with managed OAuth for managing contacts, invoices, payments, accounts, bank transactions, and financial reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to interact with Xero accounting data through Maton-managed OAuth. It helps retrieve and modify contacts, invoices, payments, accounts, bank transactions, and financial reports after the user approves write operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access or modify financial records in a connected Xero account through Maton-proxied API calls. <br>
Mitigation: Confirm the target resource, amounts, and intended effect before approving any create, update, or delete operation. <br>
Risk: MATON_API_KEY grants access to Maton-managed Xero connections and must be treated as a sensitive credential. <br>
Mitigation: Store the key securely, avoid exposing it in logs or shared shell history, and revoke unused Maton or Xero connections. <br>
Risk: Using the wrong Xero connection can send accounting requests to the wrong tenant or account. <br>
Mitigation: When multiple Xero connections exist, set the Maton-Connection header and verify the selected connection before issuing requests. <br>


## Reference(s): <br>
- [ClawHub Xero Skill](https://clawhub.ai/byungkyu/xero) <br>
- [Xero API Overview](https://developer.xero.com/documentation/api/accounting/overview) <br>
- [Xero Contacts API](https://developer.xero.com/documentation/api/accounting/contacts) <br>
- [Xero Invoices API](https://developer.xero.com/documentation/api/accounting/invoices) <br>
- [Xero Payments API](https://developer.xero.com/documentation/api/accounting/payments) <br>
- [Xero Reports API](https://developer.xero.com/documentation/api/accounting/reports) <br>
- [Maton](https://maton.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline shell, Python, JavaScript, HTTP, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a connected Xero OAuth account.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
