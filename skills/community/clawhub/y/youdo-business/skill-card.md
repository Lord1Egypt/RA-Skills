## Description:

Work with the YouDo Business API. Use when asked to interact with YouDo Business to manage employees, projects, tasks, payments, webhooks, or generate signed API requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thisisevgeniy](https://clawhub.ai/user/thisisevgeniy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business-operations teams use this skill to prepare YouDo Business API requests for employee, project, task, payment, document, agreement, invoice, balance, and webhook workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill covers workflows involving real YouDo Business credentials, payments, invoices, employee data, documents, balances, agreements, and webhook configuration.

Mitigation: Use least-privilege credentials, test in the sandbox first, and require explicit user confirmation before payment, invoice, employee, project, agreement, document-download, balance, or webhook changes.

Risk: The security summary notes destructive business changes and sensitive business data without clear safety checks in the artifact.

Mitigation: Review generated requests before execution, verify target IDs and monetary amounts, and avoid exposing JWTs, private keys, or downloaded documents in shared logs.

## Reference(s):

- [YouDo Business API Swagger](https://business-api.youdo.com/api/doc/index.html)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with API endpoint details, authentication guidance, and request-signing examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include signed request construction guidance for JWT-authenticated YouDo Business API calls.]

## Skill Version(s):

2026.3.13 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
