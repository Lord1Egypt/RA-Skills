## Description: <br>
Square API integration with managed OAuth for administering Square resources through Maton. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent read and administer Square locations, merchants, payments, refunds, customers, orders, catalog, inventory, invoices, team members, loyalty, checkout, cards, payouts, bank accounts, and terminal resources through managed OAuth. It is intended for users who need Square administration and can review account, resource, amount, and consequence details before any write action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change Square business and payment data. <br>
Mitigation: Use read-only requests first, verify the account, connection ID, resource ID, amount, and consequence, and require explicit approval before each POST, PUT, or DELETE request. <br>
Risk: MATON_API_KEY is a sensitive credential. <br>
Mitigation: Keep the key out of shared prompts, logs, files, and outputs; rotate it if exposed. <br>
Risk: Requests can target the wrong Square connection when multiple connections exist. <br>
Mitigation: Use the intended Maton-Connection header and revoke unused connections promptly. <br>
Risk: Broad Square OAuth permissions can increase blast radius. <br>
Mitigation: Use the least-privileged Square account and OAuth scopes suitable for the task. <br>


## Reference(s): <br>
- [ClawHub Square Skill](https://clawhub.ai/byungkyu/squareup) <br>
- [API Gateway Skill](https://clawhub.ai/byungkyu/api-gateway) <br>
- [Square API Overview](https://developer.squareup.com/docs) <br>
- [Square API Reference](https://developer.squareup.com/reference/square) <br>
- [Maton Settings](https://maton.ai/settings) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with Python, JavaScript, HTTP endpoint, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a Square OAuth connection; supported requests go through Maton and may read or mutate Square data.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
