## Description:

Amazon SP-API skill for OpenClaw agents. Fetch orders, check FBA inventory, manage listings and pricing. Works with any marketplace and seller account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub)

### License/Terms of Use:


## Use Case:

Developers and seller-operations teams use this skill to connect OpenClaw agents to Amazon SP-API workflows for validating credentials, retrieving orders, checking FBA inventory, inspecting listings, and updating listing prices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SP-API credentials and exported order, inventory, or listing data may expose sensitive seller information.

Mitigation: Use least-privilege SP-API credentials, store credential files with restrictive permissions, and keep exported files in private directories.

Risk: Listing price updates can modify live seller listings with weak built-in safeguards.

Mitigation: Avoid listing-write permissions unless required, and require an external confirmation or dry-run process before price updates.

Risk: The Node dependency can affect authentication, data access, and listing update behavior.

Mitigation: Pin and lock the npm dependency before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zero2ai-hub/skills/skill-spapi)
- [Amazon SP-API marketplace IDs](https://developer-docs.amazon.com/sp-api/docs/marketplace-ids)
- [ClawHub publisher profile](https://clawhub.ai/user/zero2ai-hub)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands, JSON credential examples, and Node.js script outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include sensitive seller data, order details, inventory summaries, listing records, and listing price update responses.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
