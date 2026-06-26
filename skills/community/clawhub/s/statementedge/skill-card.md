## Description: <br>
Convert PDF bank statements to CSV, Excel, QuickBooks, Xero, Sage, or OFX through the StatementEdge API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[saipradeep77](https://clawhub.ai/user/saipradeep77) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and finance operators use this skill to upload bank statement PDFs to StatementEdge, check conversion status, retrieve structured transaction data, and export completed jobs in accounting-friendly formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bank statement PDFs and optional PDF passwords are sent to StatementEdge for processing. <br>
Mitigation: Use the skill only after verifying the StatementEdge account, privacy terms, retention policy, and compliance fit for the documents being processed. <br>
Risk: The skill requires a StatementEdge API key and can access conversions associated with that account. <br>
Mitigation: Store the API key in STATEMENTEDGE_API_KEY, keep it scoped to the intended account, and revoke or rotate it if access changes. <br>


## Reference(s): <br>
- [StatementEdge Homepage](https://www.statementedge.com) <br>
- [StatementEdge API Documentation](https://www.statementedge.com/docs/api) <br>
- [StatementEdge Privacy](https://www.statementedge.com/privacy) <br>
- [StatementEdge Pricing](https://www.statementedge.com/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and STATEMENTEDGE_API_KEY; API responses may include JSON status data or downloaded export files.] <br>

## Skill Version(s): <br>
1.1.0 (source: artifact frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
