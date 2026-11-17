## Description:

Shuzhi Open helps agents use Shuzhi Open Platform APIs for blockchain evidence anchoring, automated evidence collection, custody certificate generation, and electronic signature workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alex098929](https://clawhub.ai/user/alex098929)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external teams use this skill to configure Shuzhi service credentials, prepare validated inputs, and run guided API workflows for on-chain records, evidence packages, custody PDFs, and contract signing. It is intended for workflows where users must explicitly provide and confirm legal, identity, contract, and service-specific fields before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles contracts, identity data, credentials, and service-side records.

Mitigation: Protect the workspace, use test credentials where possible, and treat terminal output and logs as sensitive.

Risk: Real appKey and appSecret values may be stored in config.json or exposed through command history.

Mitigation: Do not commit config.json with real secrets, prefer local-only secret handling, and avoid passing identity numbers or phone numbers directly on the command line.

Risk: Remote delete commands can affect Shuzhi service-side enterprise, personal, seal, or template records.

Mitigation: Review delete commands and target identifiers carefully before execution.

Risk: Misconfigured endpoints could send sensitive legal or identity data to the wrong service.

Mitigation: Verify baseUrl and product identifiers before each run.

## Reference(s):

- [Blockchain API service documentation](references/chain-api.md)
- [Automated evidence API documentation](references/evidence-api.md)
- [Custody certificate API documentation](references/certificate-api.md)
- [Electronic signature API documentation](references/sign-api.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands, JSON configuration examples, and JavaScript snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce service IDs, preview links, signing links, download links, and API results after user confirmation.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
