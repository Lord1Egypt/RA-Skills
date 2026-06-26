## Description: <br>
Work with the YouDo Business API to manage employees, projects, tasks, payments, webhooks, and signed API requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thisisevgeniy](https://clawhub.ai/user/thisisevgeniy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to plan and generate YouDo Business API interactions for employee, project, task, payment, document, agreement, invoice, balance, and webhook workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports sensitive business operations such as payments, invoices, employee and project changes, agreement changes, document access, and webhook modifications. <br>
Mitigation: Require explicit user confirmation before executing or recommending those operations, and verify IDs, amounts, and webhook URLs before use. <br>
Risk: JWTs, private keys, and signing material could be exposed through prompts, logs, or generated examples. <br>
Mitigation: Use least-privilege credentials and avoid placing private keys, JWTs, or other secrets in prompts, logs, or persisted outputs. <br>
Risk: Incorrect API requests or signed payloads could affect production business data. <br>
Mitigation: Prefer sandbox testing before production use and review generated request paths, bodies, headers, hashes, and signatures. <br>


## Reference(s): <br>
- [YouDo Business API Swagger](https://business-api.youdo.com/api/doc/index.html) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with API endpoint details and inline code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JWT header and payload guidance, request-signing inputs, endpoint paths, and request body fields.] <br>

## Skill Version(s): <br>
2026.3.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
