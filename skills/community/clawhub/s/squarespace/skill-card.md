## Description:

Helps agents manage Squarespace Commerce products, inventory, orders, customer profiles, and transactions through a user-authorized Maton connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Store operators and developers use this skill to inspect and manage Squarespace commerce data, with approval for changes and optional automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Access to live commerce records can expose customer personal data and transaction details.

Mitigation: Use least-privilege Squarespace scopes and show only the data needed for the request.

Risk: Writes or deletions can change store data or remove records.

Mitigation: Confirm each write or deletion with the user before execution.

Risk: Persistent automations or broad trigger destinations can send data beyond the intended workflow.

Mitigation: Obtain approval for each automation and destination, restrict destinations, and revoke unused Maton connections or automations.

## Reference(s):

- [Squarespace skill on ClawHub](https://clawhub.ai/byungkyu/skills/squarespace)
- [Squarespace Commerce APIs](https://developers.squarespace.com/commerce-apis/overview)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Maton homepage](https://maton.ai)
- [API gateway skill for other apps](https://clawhub.ai/byungkyu/api-gateway)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with CLI commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live commerce data; limit displayed customer and transaction details to what the task needs.]

## Skill Version(s):

1.2.8 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
