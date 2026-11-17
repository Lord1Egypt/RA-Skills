## Description:

Query and manage Salesforce CRM data via the Salesforce CLI (`sf`), including SOQL/SOSL queries, schema inspection, record operations, bulk import/export, Apex execution, metadata deployment, and REST API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, administrators, and agents use this skill to inspect and manage Salesforce org data and metadata from the command line while preserving review steps for sensitive operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Salesforce access can expose CRM data, org metadata, and authentication material if tokens or verbose org details are printed or pasted.

Mitigation: Do not print or paste Salesforce access tokens, refresh tokens, SFDX auth URLs, or verbose org-display output; use the skill only with orgs the agent is trusted to access.

Risk: Create, update, delete, deploy, bulk import/delete, REST mutation, and Apex actions can change or destroy production data.

Mitigation: Require an explicit target org, review the exact command, Apex, metadata, or file scope, and confirm immediately before each mutating or destructive operation.

Risk: Piping Salesforce query results or API responses to network commands can transmit sensitive CRM data outside the local environment.

Mitigation: Keep exports local and use approved organizational transfer processes instead of network-transmitting command pipelines.

Risk: Unpinned Salesforce CLI installations can change behavior or introduce unreviewed dependencies.

Mitigation: Prefer a pinned or organization-approved Salesforce CLI installation.

## Reference(s):

- [Salesforce CLI documentation](https://developer.salesforce.com/tools/salesforcecli)
- [ClawHub skill listing](https://clawhub.ai/snazar-faberlens/skills/salesforce-hardened)
- [Publisher profile](https://clawhub.ai/user/snazar-faberlens)
- [Faberlens Salesforce safety evaluation](https://faberlens.ai/explore/salesforce)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, SQL, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Salesforce CLI JSON output where applicable and asks for confirmation before mutating or destructive operations.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
