## Description:

Never blank on a customer again - names, roles, companies, and the details that make conversations personal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Customer-facing agents use this skill to store, recall, and update customer identity cards so conversations can address people correctly and preserve relevant account context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists broad customer personal details for later recall.

Mitigation: Use it only with customer consent and documented retention, access, and deletion policies.

Risk: Stored notes may include sensitive or unnecessary personal-life details.

Mitigation: Filter sensitive data and avoid family or personal-life information unless there is a clear, authorized business need.

Risk: Customer context is sent to a third-party processor using an API key.

Mitigation: Use the skill only if BlueColumn is an approved processor and BLUECOLUMN_API_KEY is scoped appropriately.

## Reference(s):

- [BlueColumn API documentation](https://bluecolumn.ai/docs)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls]

**Output Format:** [Markdown with inline bash code blocks and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BLUECOLUMN_API_KEY and sends customer context to BlueColumn API endpoints for storage and retrieval.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
