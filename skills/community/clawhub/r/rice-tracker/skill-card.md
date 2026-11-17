## Description:

Rice Tracker helps agents manage rice inventory, purchase batches, receivables, reconciliation, and reminder checks for customer or household records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[swiftuis](https://clawhub.ai/user/swiftuis)

### License/Terms of Use:

MIT-0

## Use Case:

External rice sellers, group-buy organizers, and household users can use this skill to track per-customer rice inventory, purchase batches, payment status, settlement dates, and reminder checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer and payment records can be exposed through an unauthenticated network service.

Mitigation: Bind the service to 127.0.0.1, add authentication and CSRF protection, and avoid exposing it to a LAN or the internet.

Risk: Sample or backup customer-like records may contain personal or payment-related information.

Mitigation: Remove sample and backup data before use, and store local records with appropriate access controls.

Risk: Background start and stop scripts can affect local processes on the configured port.

Mitigation: Review the start and stop scripts before running them, and confirm the target port and process ownership.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/swiftuis/skills/rice-tracker)
- [Publisher profile](https://clawhub.ai/user/swiftuis)
- [Clawdis homepage](https://clawhub.com/skills/rice-tracker)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON record examples; reminder checks emit Markdown text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May start a local Flask web app and read or write local JSON records.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
