## Description:

Queries store order information from a MySQL database and generates an order analysis report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bondli](https://clawhub.ai/user/bondli)

### License/Terms of Use:

MIT-0

## Use Case:

Store operators, analysts, and developers use this skill to query MySQL order and order-item tables by date range, then produce sales, payment, status, product, and SKU analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill needs read access to a store database and stores database credentials in a local plaintext configuration file.

Mitigation: Use a read-only database account limited to the required order tables, restrict local access to the skill data directory, and keep the config file out of repositories and shared backups.

Risk: The skill stores raw order exports and generated reports on the local machine.

Mitigation: Treat generated files as sensitive business data, keep the data directory private, and delete exports and reports when they are no longer needed.

Risk: The security guidance calls out verifying the mysql2 dependency version before deployment.

Mitigation: Review and update the mysql2 dependency as part of deployment approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bondli/skills/store-order-query)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report, JSON order export, and terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local database configuration and writes order data plus reports to the local skill data directory.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact package.json reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
