## Description: <br>
Provides workflows, schemas, and code patterns for integrating agents with QuickBooks Online accounting, payments, webhooks, reports, and OAuth-based authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simonpierreboucher02](https://clawhub.ai/user/simonpierreboucher02) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and finance automation teams use this skill to connect agents or MCP tooling to QuickBooks Online for accounting workflows such as customer, invoice, payment, bill, report, webhook, and reconciliation automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides high-impact financial automation using sensitive QuickBooks credentials. <br>
Mitigation: Use the QuickBooks sandbox first, keep secrets out of committed files, restrict OAuth scopes, require human approval for payments or posting actions, and set transaction limits. <br>
Risk: The artifact includes query-string sanitization guidance for QuickBooks queries. <br>
Mitigation: Use an allowlisted query builder for IDS queries before production use. <br>


## Reference(s): <br>
- [QuickBooks Online API documentation](https://developer.intuit.com/app/developer/qbo/docs/learn/explore-the-quickbooks-online-api) <br>
- [ClawHub skill page](https://clawhub.ai/simonpierreboucher02/quickbook) <br>
- [authentication.md](authentication.md) <br>
- [webhooks.md](webhooks.md) <br>
- [queries_and_errors.md](queries_and_errors.md) <br>
- [ai_and_mcp.md](ai_and_mcp.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JSON, bash, Python, SQL, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Covers OAuth credentials, QuickBooks entity workflows, webhook handling, query/error handling, and MCP configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
